# -*- coding: utf-8 -*-
"""Lee con un navegador la plantilla oficial de cada club de Primera en laliga.com (temporada en curso).

Para cada jugador guarda dorsal, nombre y fecha de nacimiento. El texto de la página llega con las
secciones concatenadas, así que se trocea con una expresión regular anclada en la posición del jugador.
Salida: laliga_plantillas.json
"""
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

CARPETA = os.path.dirname(os.path.abspath(__file__))
URL_CLUBES = "https://www.laliga.com/laliga-easports/clubes"
POSICIONES = "Portero|Defensa|Centrocampista|Delantero"
ENCABEZADOS = "Porteros|Defensas|Centrocampistas|Delanteros"
PATRON_JUGADOR = re.compile(
    r"(?:Kg|Peso-|" + ENCABEZADOS + r")(\d{1,3})(.*?)(" + POSICIONES + r")(.*?)Nacimiento(\d{2}/\d{2}/\d{4})")


def listar_clubes(pagina):
    pagina.goto(URL_CLUBES, wait_until="domcontentloaded", timeout=60000)
    pagina.wait_for_timeout(6000)
    for _ in range(5):
        pagina.mouse.wheel(0, 800)
        pagina.wait_for_timeout(800)
    enlaces = pagina.eval_on_selector_all(
        "a", "elementos => elementos.map(elemento => elemento.href)")
    identificadores = []
    for enlace in enlaces:
        coincidencia = re.search(r"laliga\.com/(?:[a-z]{2}-[A-Z]{2}/)?clubes/([a-z0-9-]+)/plantilla$", enlace)
        if coincidencia and coincidencia.group(1) not in identificadores:
            identificadores.append(coincidencia.group(1))
    return identificadores


def leer_plantilla(pagina, identificador):
    pagina.goto("https://www.laliga.com/clubes/" + identificador + "/plantilla",
                wait_until="domcontentloaded", timeout=60000)
    pagina.wait_for_timeout(4500)
    texto = pagina.evaluate("document.body.textContent")
    apodo = re.search(r'"nickname":"([^"]+)"', texto)
    apodo = apodo.group(1) if apodo else ""
    inicio = texto.find("Plantilla oficial del")
    final = texto.find("COMPARADOR DE JUGADORES", inicio)
    bloque = texto[inicio:final] if inicio >= 0 and final > inicio else ""
    jugadores = []
    for coincidencia in PATRON_JUGADOR.finditer(bloque):
        dorsal = int(coincidencia.group(1))
        nombre = coincidencia.group(2)
        if apodo and nombre.endswith(apodo):
            nombre = nombre[:-len(apodo)]
        dia, mes, anio = coincidencia.group(5).split("/")
        jugadores.append({"dorsal": dorsal, "nombre": nombre.strip(),
                          "nacimiento": [int(anio), int(mes), int(dia)]})
    return apodo, jugadores


def main():
    resultado = {}
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(channel="msedge")
        pagina = navegador.new_page(viewport={"width": 1300, "height": 1000})
        clubes = listar_clubes(pagina)
        print("clubes encontrados:", len(clubes), clubes, flush=True)
        for identificador in clubes:
            apodo, jugadores = leer_plantilla(pagina, identificador)
            en_rango = [jugador for jugador in jugadores if 1 <= jugador["dorsal"] <= 25]
            print(f"  {identificador} ({apodo}): {len(jugadores)} jugadores, {len(en_rango)} con dorsal 1-25", flush=True)
            resultado[identificador] = {"apodo": apodo, "jugadores": jugadores}
        navegador.close()
    with open(os.path.join(CARPETA, "laliga_plantillas.json"), "w", encoding="utf-8") as fichero:
        json.dump(resultado, fichero, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
