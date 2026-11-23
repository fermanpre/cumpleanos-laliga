# -*- coding: utf-8 -*-
"""Convierte datos_brutos.json en site/datos.json (dorsales 1 a 25, solo mes y día de nacimiento)
y calcula las coincidencias por equipo para contrastarlas luego con las del navegador."""
import json
import os
import re
import unicodedata
from collections import defaultdict
from datetime import date

CARPETA = os.path.dirname(os.path.abspath(__file__))
DORSAL_MINIMO = 1
DORSAL_MAXIMO = 25
FECHA_CONSULTA = "2026-11-20"
TEMPORADA_LALIGA = "2026-27"  # plantilla oficial de laliga.com; el resto, Wikipedia + Wikidata

# Errores de la Wikipedia en español detectados al contrastar con Wikidata y confirmados con una tercera fuente
# (LaLiga, ficha oficial del club, Premier League, etc.): (equipo, jugador) -> [año, mes, día]
CORRECCIONES = {
    ("Atlético de Madrid", "Arnau Ortiz"): [2001, 10, 29],
    ("Atlético de Madrid", "Julián Alvarez"): [2000, 1, 31],
    ("Atlético de Madrid", "Johnny Cardoso"): [2001, 9, 20],
    ("Getafe", "Borja Mayoral"): [1997, 4, 5],
    ("Elche", "Grady Diangana"): [1998, 4, 19],
    ("Real Betis", "Álvaro Valles"): [1997, 7, 25],
    ("Getafe", "Abdel Abqar"): [1999, 3, 10],  # LaLiga y Wikidata
    ("Real Betis", "Ricardo Rodríguez"): [1992, 8, 25],  # Wikidata; pendiente de una tercera fuente
}


MAPA_LALIGA = {
    "athletic-club": "Athletic Club", "atletico-de-madrid": "Atlético de Madrid", "c-a-osasuna": "Osasuna",
    "rc-celta": "Celta de Vigo", "d-alaves": "Alavés", "elche-c-f": "Elche", "fc-barcelona": "Barcelona",
    "getafe-cf": "Getafe", "levante-ud": "Levante", "malaga-cf": "Málaga", "r-racing-club": "Racing de Santander",
    "rayo-vallecano": "Rayo Vallecano", "rc-deportivo": "Deportivo de A Coruña", "rcd-espanyol": "Espanyol",
    "real-betis": "Real Betis", "real-madrid": "Real Madrid", "real-sociedad": "Real Sociedad",
    "sevilla-fc": "Sevilla", "valencia-cf": "Valencia", "villarreal-cf": "Villarreal",
}


def normalizar(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z ]", "", sin_tildes.lower().replace(".", " ")).strip()


def nombre_completo(jugador_laliga, jugadores_wikipedia):
    """Devuelve el nombre de Wikipedia si es el mismo jugador (misma fecha y nombre compatible)."""
    corto = normalizar(jugador_laliga["nombre"])
    fecha = jugador_laliga["nacimiento"][1:]
    for candidato in jugadores_wikipedia:
        completo = normalizar(candidato["nombre"])
        if corto == completo:
            return candidato["nombre"]
    for candidato in jugadores_wikipedia:
        completo = normalizar(candidato["nombre"])
        palabras_cortas = [palabra for palabra in corto.split() if len(palabra) > 1]
        if palabras_cortas and all(palabra in completo for palabra in palabras_cortas):
            return candidato["nombre"]
    return jugador_laliga["nombre"]


def jugadores_desde_laliga(nombre_equipo, jugadores_wikipedia):
    with open(os.path.join(CARPETA, "laliga_plantillas.json"), encoding="utf-8") as fichero:
        laliga = json.load(fichero)
    for identificador, nombre in MAPA_LALIGA.items():
        if nombre == nombre_equipo:
            resultado = []
            for jugador in laliga[identificador]["jugadores"]:
                resultado.append({"dorsal": jugador["dorsal"],
                                  "nombre": nombre_completo(jugador, jugadores_wikipedia),
                                  "nacimiento": jugador["nacimiento"]})
            return resultado
    return jugadores_wikipedia


ALIAS_BDFUTBOL = {"Betis": "Real Betis", "Oviedo": "Real Oviedo"}


def palabras_de(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    letras = re.sub(r"[^a-z ]", "", sin_tildes.lower().replace("-", " "))
    return [palabra for palabra in letras.split() if len(palabra) > 1]


def rellenar_dorsales_con_bdfutbol(temporada, nombre_equipo, jugadores_wikipedia, informe):
    """Da dorsal a los jugadores de Wikipedia que no lo traen, si su nombre casa con una sola fila de bdfutbol."""
    ruta = os.path.join(CARPETA, "bdfutbol_" + temporada + ".json")
    if not os.path.exists(ruta):
        return jugadores_wikipedia
    with open(ruta, encoding="utf-8") as fichero:
        bdfutbol = json.load(fichero)
    filas = []
    for club, lista in bdfutbol.items():
        if ALIAS_BDFUTBOL.get(club, club) == nombre_equipo:
            filas = lista
    dorsales_usados = {j["dorsal"] for j in jugadores_wikipedia if j["dorsal"] is not None}
    resultado = []
    for jugador in jugadores_wikipedia:
        if jugador["dorsal"] is None:
            palabras = palabras_de(jugador["nombre"])
            candidatos = set()
            for fila in filas:
                texto_fila = palabras_de(fila["nombre"]) + palabras_de(fila["apodo"])
                if palabras and all(palabra in texto_fila for palabra in palabras):
                    candidatos.add(fila["dorsal"])
            if len(candidatos) == 1:
                dorsal = candidatos.pop()
                if dorsal not in dorsales_usados:
                    jugador = dict(jugador, dorsal=dorsal)
                    dorsales_usados.add(dorsal)
                    informe.append(f"{nombre_equipo}: {jugador['nombre']} -> dorsal {dorsal}")
        resultado.append(jugador)
    return resultado


def cargar_fechas_wikidata():
    """Devuelve {(temporada, equipo, nombre): [año, mes, día]} con las fechas de Wikidata que se pueden usar.

    Regla: la fecha de Wikidata sustituye a la de Wikipedia solo si es completa (mes y día distintos de 0),
    no es el 1 de enero (marcador de posición habitual) y el año coincide con el de Wikipedia (misma persona).
    """
    ruta = os.path.join(CARPETA, "comparacion_wikidata.json")
    fechas = {}
    with open(ruta, encoding="utf-8") as fichero:
        registro = json.load(fichero)
    for fila in registro:
        wikidata = fila["wikidata"]
        wikipedia = fila["wikipedia"]
        if not wikidata or wikidata[1] == 0 or wikidata[2] == 0:
            continue
        if wikidata[1] == 1 and wikidata[2] == 1:
            continue
        if wikidata[0] != wikipedia[0]:
            continue
        fechas[(fila["temporada"], fila["equipo"], fila["nombre"])] = wikidata
    return fechas


def crear_identificador(nombre):
    sin_tildes = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", sin_tildes.lower()).strip("-")


def agrupar_por_cumpleanos(jugadores):
    grupos = defaultdict(list)
    for jugador in jugadores:
        grupos[(jugador["mes"], jugador["dia"])].append(jugador)
    return {clave: lista for clave, lista in grupos.items() if len(lista) > 1}


def main():
    with open(os.path.join(CARPETA, "datos_brutos.json"), encoding="utf-8") as fichero:
        brutos = json.load(fichero)
    salida = {"consulta": FECHA_CONSULTA, "temporadas": {}}
    resumen_texto = []
    informe_dorsales = []
    fechas_wikidata = cargar_fechas_wikidata()
    cambios_wikidata = 0
    for temporada, equipos in brutos.items():
        lista_equipos = []
        con_coincidencia = 0
        for equipo in equipos:
            jugadores = []
            brutos_equipo = equipo["jugadores"]
            if temporada != TEMPORADA_LALIGA:
                brutos_equipo = rellenar_dorsales_con_bdfutbol(temporada, equipo["nombre"], equipo["jugadores"], informe_dorsales)
            if temporada == TEMPORADA_LALIGA:
                brutos_equipo = jugadores_desde_laliga(equipo["nombre"], equipo["jugadores"])
            for bruto in brutos_equipo:
                if bruto["dorsal"] is None or not (DORSAL_MINIMO <= bruto["dorsal"] <= DORSAL_MAXIMO):
                    continue
                clave = (equipo["nombre"], bruto["nombre"])
                fecha = bruto["nacimiento"]
                if temporada != TEMPORADA_LALIGA:
                    fecha_wd = fechas_wikidata.get((temporada, equipo["nombre"], bruto["nombre"]))
                    if fecha_wd and fecha_wd != fecha:
                        fecha = fecha_wd
                        cambios_wikidata += 1
                anio, mes, dia = CORRECCIONES.get(clave, fecha)
                date(anio, mes, dia)  # falla si la fecha no existe
                jugadores.append({"dorsal": bruto["dorsal"], "nombre": bruto["nombre"],
                                  "mes": mes, "dia": dia})
            jugadores.sort(key=lambda jugador: (jugador["dorsal"], jugador["nombre"]))
            grupos = agrupar_por_cumpleanos(jugadores)
            if grupos:
                con_coincidencia += 1
            lista_equipos.append({"id": crear_identificador(equipo["nombre"]), "nombre": equipo["nombre"],
                                  "articulo": equipo["articulo"], "jugadores": jugadores})
            detalle = "; ".join(
                f"{dia:02d}/{mes:02d}: " + " y ".join(f'{j["nombre"]} ({j["dorsal"]})' for j in lista)
                for (mes, dia), lista in sorted(grupos.items()))
            resumen_texto.append(f"{temporada} | {equipo['nombre']} | {len(jugadores)} jug. | {detalle or '-'}")
        lista_equipos.sort(key=lambda equipo: equipo["nombre"])
        salida["temporadas"][temporada] = {"equipos": lista_equipos}
        resumen_texto.append(f"==> {temporada}: {con_coincidencia} de {len(lista_equipos)} equipos con coincidencia")
    os.makedirs(os.path.join(CARPETA, "site"), exist_ok=True)
    with open(os.path.join(CARPETA, "site", "datos.json"), "w", encoding="utf-8") as fichero:
        json.dump(salida, fichero, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(CARPETA, "coincidencias_python.txt"), "w", encoding="utf-8") as fichero:
        fichero.write("\n".join(resumen_texto) + "\n")
    print("\n".join(resumen_texto))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    main()
