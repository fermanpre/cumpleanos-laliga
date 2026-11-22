# -*- coding: utf-8 -*-
"""Recoge las plantillas de Primera División (dorsales 1 a 25) desde la Wikipedia en español.

Salida: datos_brutos.json (todos los jugadores con dorsal) e incidencias.csv (casos a revisar).
Las fechas de nacimiento salen de la plantilla {{edad|día|mes|año}} de cada jugador.
"""
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_CACHE = os.path.join(CARPETA, "cache")
API = "https://es.wikipedia.org/w/api.php"
CABECERAS = {"User-Agent": "CumpleanosLaLiga/0.1 (proyecto personal de portfolio)"}

# Temporada -> página de la liga y fecha de corte de la versión del artículo del club.
# Para la temporada en curso se usa la versión actual (corte vacío).
TEMPORADAS = {
    "2026-27": {"liga": "Primera División de España 2026-27", "corte": "", "seccion": "2026-27"},
    "2025-26": {"liga": "Primera División de España 2025-26", "corte": "2025-09-15T00:00:00Z", "seccion": "2025-26"},
}


def pedir_json(parametros):
    """Hace una petición a la API con caché en disco para no repetirla."""
    clave = hashlib.sha1(json.dumps(parametros, sort_keys=True).encode("utf-8")).hexdigest()
    ruta_cache = os.path.join(CARPETA_CACHE, clave + ".json")
    if os.path.exists(ruta_cache):
        with open(ruta_cache, encoding="utf-8") as fichero:
            return json.load(fichero)
    url = API + "?" + urllib.parse.urlencode(parametros)
    peticion = urllib.request.Request(url, headers=CABECERAS)
    espera_segundos = 10
    for intento in range(8):
        try:
            with urllib.request.urlopen(peticion, timeout=60) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as error:
            if error.code != 429 or intento == 7:
                raise
            print(f"    429: espero {espera_segundos} s", flush=True)
            time.sleep(espera_segundos)
            espera_segundos = espera_segundos * 2
    with open(ruta_cache, "w", encoding="utf-8") as fichero:
        json.dump(datos, fichero, ensure_ascii=False)
    time.sleep(1.5)
    return datos


def wikitexto_actual(titulo):
    datos = pedir_json({"action": "parse", "page": titulo, "prop": "wikitext",
                        "format": "json", "redirects": 1})
    if "error" in datos:
        return None, None
    return datos["parse"]["wikitext"]["*"], datos["parse"]["title"]


def wikitexto_a_fecha(titulo, corte):
    """Última versión del artículo anterior a la fecha de corte."""
    if not corte:
        return wikitexto_actual(titulo)
    datos = pedir_json({"action": "query", "prop": "revisions", "titles": titulo,
                        "rvlimit": 1, "rvstart": corte, "rvdir": "older",
                        "rvslots": "main", "rvprop": "content|ids|timestamp",
                        "format": "json", "redirects": 1})
    for pagina in datos["query"]["pages"].values():
        if "revisions" not in pagina:
            return None, None
        revision = pagina["revisions"][0]
        return revision["slots"]["main"]["*"], pagina["title"] + " @" + revision["timestamp"]
    return None, None


def equipos_de_la_liga(titulo_liga):
    """Devuelve [(artículo, nombre corto)] leyendo la tabla «Información de los equipos»."""
    texto, _ = wikitexto_actual(titulo_liga)
    inicio = texto.find("Información de los equipos")
    final = texto.find("\n==", inicio + 40)
    bloque = texto[inicio:final]
    equipos = []
    for fila in bloque.split("\n|-")[1:]:
        lineas = [linea for linea in fila.strip().split("\n") if linea.startswith("|")]
        if not lineas:
            continue
        coincidencia = re.match(r"\|\s*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lineas[0])
        if coincidencia:
            articulo = coincidencia.group(1).strip()
            nombre = (coincidencia.group(2) or articulo).strip()
            equipos.append((articulo, nombre))
    return equipos


def extraer_plantillas(texto, inicio_plantilla="{{Jugador de fútbol"):
    """Devuelve el texto interior de cada {{Jugador de fútbol ...}} (con llaves equilibradas)."""
    resultados = []
    posicion = 0
    while True:
        inicio = texto.find(inicio_plantilla, posicion)
        if inicio < 0:
            break
        profundidad = 0
        indice = inicio
        while indice < len(texto):
            if texto.startswith("{{", indice):
                profundidad += 1
                indice += 2
            elif texto.startswith("}}", indice):
                profundidad -= 1
                indice += 2
                if profundidad == 0:
                    break
            else:
                indice += 1
        resultados.append(texto[inicio + 2:indice - 2])
        posicion = indice
    return resultados


def separar_parametros(contenido):
    """Divide por '|' de primer nivel (fuera de [[...]] y {{...}}) y devuelve un diccionario."""
    partes = []
    actual = []
    nivel_llaves = 0
    nivel_corchetes = 0
    indice = 0
    while indice < len(contenido):
        par = contenido[indice:indice + 2]
        if par == "{{":
            nivel_llaves += 1
            actual.append(par)
            indice += 2
        elif par == "}}":
            nivel_llaves -= 1
            actual.append(par)
            indice += 2
        elif par == "[[":
            nivel_corchetes += 1
            actual.append(par)
            indice += 2
        elif par == "]]":
            nivel_corchetes -= 1
            actual.append(par)
            indice += 2
        elif contenido[indice] == "|" and nivel_llaves == 0 and nivel_corchetes == 0:
            partes.append("".join(actual))
            actual = []
            indice += 1
        else:
            actual.append(contenido[indice])
            indice += 1
    partes.append("".join(actual))
    parametros = {}
    for parte in partes[1:]:
        if "=" in parte:
            clave, valor = parte.split("=", 1)
            parametros[clave.strip()] = valor.strip()
    return parametros


def limpiar_nombre(valor):
    valor = re.sub(r"<!--.*?-->", "", valor)
    coincidencia = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", valor)
    if coincidencia:
        texto = coincidencia.group(2) or coincidencia.group(1)
        articulo = coincidencia.group(1).strip()
    else:
        texto = valor
        articulo = ""
    texto = texto.replace("'''", "").replace("''", "")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto, articulo


def leer_fecha(valor):
    """Extrae (año, mes, día) de {{edad|día|mes|año}}; None si no se puede."""
    coincidencia = re.search(r"\{\{\s*[Ee]dad\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})\s*\|\s*(\d{4})", valor)
    if coincidencia:
        dia = int(coincidencia.group(1))
        mes = int(coincidencia.group(2))
        anio = int(coincidencia.group(3))
        return [anio, mes, dia]
    return None


def leer_dorsal(valor):
    limpio = valor.replace("'''", "").replace("''", "").strip()
    return int(limpio) if limpio.isdigit() else None


def seccion_de_plantilla(texto, etiqueta_temporada):
    """Devuelve el texto desde el encabezado de plantilla hasta la siguiente sección sin jugadores."""
    patron = re.compile(r"=+\s*Plant(?:illa|el)[^=\n]*" + re.escape(etiqueta_temporada) + r"[^=\n]*=+")
    coincidencia = patron.search(texto)
    if not coincidencia:
        coincidencia = re.search(r"=+\s*Plant(?:illa|el)[^=\n]*=+", texto)
        if not coincidencia:
            return None
    resto = texto[coincidencia.end():]
    # Cortamos en el primer encabezado de nivel 2 o 3 (los subencabezados de plantilla suelen ser de nivel 4).
    siguiente = re.search(r"\n==+[^=\n]+==+\s*\n", resto)
    return resto if not siguiente else resto[:siguiente.start()]


def recoger_temporada(etiqueta, configuracion, incidencias):
    equipos = equipos_de_la_liga(configuracion["liga"])
    print(f"{etiqueta}: {len(equipos)} equipos en la liga", flush=True)
    resultado = []
    for articulo, nombre in equipos:
        texto, titulo_real = wikitexto_a_fecha(articulo, configuracion["corte"])
        if texto is None:
            incidencias.append((etiqueta, nombre, "", "", "Artículo del club no encontrado: " + articulo))
            continue
        seccion = seccion_de_plantilla(texto, configuracion["seccion"])
        if seccion is None:
            incidencias.append((etiqueta, nombre, "", "", "Sin sección de plantilla"))
            continue
        jugadores = []
        for contenido in extraer_plantillas(seccion):
            parametros = separar_parametros(contenido)
            dorsal_bruto = parametros.get("num", parametros.get("no", parametros.get("número", "")))
            dorsal = leer_dorsal(dorsal_bruto)
            nombre_jugador, articulo_jugador = limpiar_nombre(
                parametros.get("nombre", parametros.get("name", parametros.get("jugador", ""))))
            fecha = leer_fecha(parametros.get("edad", ""))
            if dorsal is None:
                incidencias.append((etiqueta, nombre, "", nombre_jugador,
                                    "Dorsal no numérico: " + dorsal_bruto))
                if fecha is None or not nombre_jugador:
                    continue
            jugadores.append({"dorsal": dorsal, "nombre": nombre_jugador, "articulo": articulo_jugador,
                              "nacimiento": fecha, "edad_bruta": parametros.get("edad", "")})
        print(f"  {nombre}: {len(jugadores)} jugadores con dorsal ({titulo_real})", flush=True)
        resultado.append({"articulo": articulo, "nombre": nombre, "fuente": titulo_real, "jugadores": jugadores})
    return resultado


def main():
    os.makedirs(CARPETA_CACHE, exist_ok=True)
    incidencias = []
    salida = {}
    for etiqueta, configuracion in TEMPORADAS.items():
        salida[etiqueta] = recoger_temporada(etiqueta, configuracion, incidencias)
    with open(os.path.join(CARPETA, "datos_brutos.json"), "w", encoding="utf-8") as fichero:
        json.dump(salida, fichero, ensure_ascii=False, indent=1)
    with open(os.path.join(CARPETA, "incidencias.csv"), "w", encoding="utf-8-sig", newline="") as fichero:
        escritor = csv.writer(fichero, delimiter=";")
        escritor.writerow(["temporada", "equipo", "dorsal", "jugador", "incidencia"])
        escritor.writerows(incidencias)
    print("Incidencias:", len(incidencias))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
