# Cumpleaños en LaLiga

La paradoja del cumpleaños aplicada a las plantillas de Primera División (dorsales del 1 al 25): qué jugadores de cada equipo comparten cumpleaños y cuántos equipos tienen coincidencias. Cinco temporadas, de la 2022/23 a la 2026/27 (plantilla al cierre del mercado de verano).

Web estática en `docs/` (español e inglés, modo claro y oscuro). Los scripts de `scripts/` recogen y contrastan los datos (`recoger_plantillas.py`, `leer_laliga.py`, `leer_bdfutbol.py`, `contrastar_wikidata.py`) y generan los datos y las páginas del sitio (`construir_datos.py`, `generar_paginas.py`).

## Fuentes
- Plantilla oficial de LALIGA (2026/27) y Wikipedia en español (CC BY-SA 4.0).
- Fechas de nacimiento contrastadas con Wikidata (CC0).
- Los dorsales que faltaban en las temporadas anteriores a la 2026/27 se completaron con bdfutbol.com (solo dorsal, nombre y fecha publicados).
- Regla de fechas: la de Wikidata sustituye a la de Wikipedia solo si es completa, no es el 1 de enero y el año coincide.

## Limitaciones
Hay equipos con menos de 25 dorsales ocupados, y algunos dorsales repetidos por altas y bajas. Las fechas se contrastaron de forma sistemática con Wikidata, pero solo una parte de las discrepancias se confirmó con una tercera fuente. Puede haber errores.

## Licencia
Todos los derechos reservados, salvo los datos que proceden de fuentes con licencia libre (ver `LICENSE`).
