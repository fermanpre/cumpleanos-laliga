# -*- coding: utf-8 -*-
"""Lee de bdfutbol.com los dorsales de cada club de Primera 2025-26 (solo dorsal y nombre; no se publican)."""
import json
import os
import sys

from playwright.sync_api import sync_playwright

CARPETA = os.path.dirname(os.path.abspath(__file__))
TEMPORADA = sys.argv[1] if len(sys.argv) > 1 else "2025-26"
URL_TEMPORADA = "https://www.bdfutbol.com/es/t/t" + TEMPORADA + ".html"
SCRIPT_FILAS = r"""
() => {
  const resultado = [];
  document.querySelectorAll('tr').forEach(fila => {
    const celdas = Array.from(fila.querySelectorAll('td')).map(c => c.innerText.trim());
    const textos = celdas.slice(1).filter(c => c.length > 0 && c !== '⬤');
    if (celdas.length >= 3 && /^\d{1,2}$/.test(celdas[0]) && textos.length >= 2) { resultado.push([celdas[0], textos[0], textos[1]]); }
  });
  return resultado;
}
"""


def main():
    resultado = {}
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(channel="msedge")
        pagina = navegador.new_page(viewport={"width": 1300, "height": 1000})
        pagina.goto(URL_TEMPORADA, wait_until="domcontentloaded", timeout=60000)
        pagina.wait_for_timeout(4000)
        enlaces = pagina.eval_on_selector_all("a", "els => els.map(e => [e.innerText.trim(), e.href])")
        clubes = {}
        for texto, url in enlaces:
            if "/t/t" + TEMPORADA + "" in url and url.endswith(".html") and texto and url not in clubes.values():
                resto = url.split("/t/t" + TEMPORADA)[1].replace(".html", "")
                if resto.isdigit() and texto not in clubes:
                    clubes[texto] = url
        print("clubes:", len(clubes), flush=True)
        for nombre, url in clubes.items():
            pagina.goto(url, wait_until="domcontentloaded", timeout=60000)
            pagina.wait_for_timeout(2500)
            filas = pagina.evaluate(SCRIPT_FILAS)
            jugadores = []
            for dorsal, celda_nombres, _edad in filas:
                lineas = [linea.strip() for linea in celda_nombres.splitlines() if linea.strip() and linea.strip() != "⬤"]
                if len(lineas) >= 2:
                    jugadores.append({"dorsal": int(dorsal), "apodo": lineas[0], "nombre": lineas[1]})
            resultado[nombre] = jugadores
            print(" ", nombre, len(jugadores), flush=True)
        navegador.close()
    with open(os.path.join(CARPETA, "bdfutbol_" + TEMPORADA + ".json"), "w", encoding="utf-8") as fichero:
        json.dump(resultado, fichero, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
