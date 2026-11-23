# -*- coding: utf-8 -*-
"""Lista, por temporada, los equipos cuyas parejas cambian según se use la fecha de Wikipedia o la de Wikidata.

Entrada: comparacion_wikidata.json (generado por contrastar_wikidata.py).
Solo se usan las fechas de Wikidata que son completas (mes y día distintos de 0 y distintas del 1 de enero,
que suele ser un marcador de posición).
"""
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
CARPETA = os.path.dirname(os.path.abspath(__file__))


def fecha_wikidata_fiable(fecha):
    if not fecha:
        return False
    if fecha[1] == 0 or fecha[2] == 0:
        return False
    return not (fecha[1] == 1 and fecha[2] == 1)


def agrupar(filas, usar_wikidata):
    por_equipo = defaultdict(lambda: defaultdict(list))
    for fila in filas:
        fecha = fila["wikipedia"]
        if usar_wikidata and fecha_wikidata_fiable(fila["wikidata"]):
            fecha = fila["wikidata"]
        etiqueta = fila["nombre"] + " (" + str(fila["dorsal"]) + ")"
        por_equipo[fila["equipo"]][(fecha[1], fecha[2])].append(etiqueta)
    resultado = {}
    for equipo, grupos in por_equipo.items():
        pares = []
        for clave, nombres in sorted(grupos.items()):
            if len(nombres) > 1:
                pares.append((clave, nombres))
        resultado[equipo] = pares
    return resultado


def main():
    with open(os.path.join(CARPETA, "comparacion_wikidata.json"), encoding="utf-8") as fichero:
        registro = json.load(fichero)
    temporadas = sorted({fila["temporada"] for fila in registro}, reverse=True)
    for temporada in temporadas:
        filas = [fila for fila in registro if fila["temporada"] == temporada]
        con_wikipedia = agrupar(filas, False)
        con_wikidata = agrupar(filas, True)
        print("==", temporada, "| equipos con pareja: Wikipedia", sum(1 for v in con_wikipedia.values() if v),
              "| Wikidata", sum(1 for v in con_wikidata.values() if v))
        for equipo in sorted(con_wikipedia):
            if con_wikipedia[equipo] != con_wikidata[equipo]:
                print(" ", equipo)
                print("     Wikipedia:", con_wikipedia[equipo])
                print("     Wikidata :", con_wikidata[equipo])


if __name__ == "__main__":
    main()
