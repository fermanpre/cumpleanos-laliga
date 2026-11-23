# -*- coding: utf-8 -*-
"""Contrasta con Wikidata (P569) la fecha de nacimiento de los jugadores que forman pareja."""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import recoger_plantillas as recogida

CABECERAS = {"User-Agent": "CumpleanosLaLiga/0.1 (proyecto personal de portfolio)"}
datos = json.load(open("datos_brutos.json", encoding="utf-8"))
CORRECCIONES = {"Arnau Ortiz": [2001, 10, 29]}

jugadores_en_pareja = []
for temporada, equipos in datos.items():
    for equipo in equipos:
        grupos = defaultdict(list)
        for jugador in equipo["jugadores"]:
            if jugador["dorsal"] is None or 1 <= jugador["dorsal"] <= 25:
                grupos[tuple(jugador["nacimiento"][1:])].append(jugador)
        for lista in grupos.values():
            for jugador in lista:
                jugadores_en_pareja.append((temporada, equipo["nombre"], jugador))
print("jugadores a contrastar:", len(jugadores_en_pareja))

# Artículo de la Wikipedia -> identificador de Wikidata
articulos = sorted({j["articulo"] for _, _, j in jugadores_en_pareja if j["articulo"]})
identificadores = {}
for inicio in range(0, len(articulos), 40):
    lote = articulos[inicio:inicio + 40]
    respuesta = recogida.pedir_json({"action": "query", "prop": "pageprops", "ppprop": "wikibase_item",
                                     "titles": "|".join(lote), "redirects": 1, "format": "json"})
    redirigidos = {r["from"]: r["to"] for r in respuesta["query"].get("redirects", [])}
    normalizados = {n["from"]: n["to"] for n in respuesta["query"].get("normalized", [])}
    por_titulo = {p["title"]: p.get("pageprops", {}).get("wikibase_item") for p in respuesta["query"]["pages"].values()}
    for titulo in lote:
        final = normalizados.get(titulo, titulo)
        final = redirigidos.get(final, final)
        identificadores[titulo] = por_titulo.get(final)

# Fecha en Wikidata
fechas = {}
qids = sorted({q for q in identificadores.values() if q})
for inicio in range(0, len(qids), 25):
    lote = qids[inicio:inicio + 25]
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "wbgetentities", "ids": "|".join(lote), "props": "claims", "format": "json"})
    contenido = None
    espera = 15
    for intento in range(8):
        try:
            contenido = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=CABECERAS), timeout=60).read().decode("utf-8"))
            break
        except urllib.error.HTTPError as error:
            if error.code != 429:
                raise
            print("    429 en Wikidata: espero", espera, "s", flush=True)
            time.sleep(espera)
            espera = espera * 2
    time.sleep(3)
    for qid, entidad in contenido["entities"].items():
        declaraciones = entidad.get("claims", {}).get("P569", [])
        if declaraciones:
            tiempo = declaraciones[0]["mainsnak"]["datavalue"]["value"]["time"]  # +2001-10-29T00:00:00Z
            fechas[qid] = [int(tiempo[1:5]), int(tiempo[6:8]), int(tiempo[9:11])]

coinciden = 0
discrepancias = []
sin_dato = []
for temporada, equipo, jugador in jugadores_en_pareja:
    esperado = fechas.get(identificadores.get(jugador["articulo"]))
    usado = CORRECCIONES.get(jugador["nombre"], jugador["nacimiento"])
    if esperado is None:
        sin_dato.append((temporada, equipo, jugador["nombre"]))
    elif esperado == usado:
        coinciden += 1
    else:
        discrepancias.append((temporada, equipo, jugador["nombre"], usado, esperado))
print("coinciden con Wikidata:", coinciden)
print("sin dato en Wikidata:", sin_dato)
print("DISCREPANCIAS:")
for fila in discrepancias:
    print("  ", fila)

# Guarda la comparación completa para analizarla sin repetir peticiones
registro = []
for temporada, equipo, jugador in jugadores_en_pareja:
    registro.append({"temporada": temporada, "equipo": equipo, "dorsal": jugador["dorsal"],
                     "nombre": jugador["nombre"], "wikipedia": jugador["nacimiento"],
                     "wikidata": fechas.get(identificadores.get(jugador["articulo"]))})
json.dump(registro, open("comparacion_wikidata.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
