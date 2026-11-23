# -*- coding: utf-8 -*-
"""Genera las páginas estáticas del sitio (cabecera con logos, cinta inferior y contenido bilingüe).

Salida en site/: index.html, acerca.html, autor.html, cerveza.html, enlaces.html, privacidad.html,
changelog.html, feed.xml y LICENSE. El contenido de cada página está en español e inglés: el idioma
visible lo decide el atributo lang de <html> (ver comun.js y style.css).
"""
import datetime
import os
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
SITIO = os.path.join(CARPETA, "site")
URL_BASE = "https://fermanpre.github.io/cumpleanos-laliga/"
VERSION_ACTIVOS = "20261123c"
URL_GITHUB = "https://github.com/fermanpre"
URL_LINKEDIN = "https://www.linkedin.com/in/fernandomanzanarespreciado/"
URL_SPONSORS = "https://github.com/sponsors/fermanpre"
URL_REPOSITORIO = "https://github.com/fermanpre/cumpleanos-laliga"

SVG_GITHUB = (
    '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" aria-hidden="true">'
    '<path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
    '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
    '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
    '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 '
    '1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 '
    '1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)
SVG_LINKEDIN = (
    '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" aria-hidden="true">'
    '<path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 '
    '1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 '
    '1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 '
    '1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 '
    '1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 '
    '0 7.225 0 7.225h2.4z"/></svg>'
)
SVG_SPONSOR = (
    '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" aria-hidden="true">'
    '<path fill-rule="evenodd" d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.565 '
    '20.565 0 008 13.393a20.561 20.561 0 003.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3 '
    '-1.373 0-2.609.986-3.029 2.456a.75.75 0 01-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5z"/></svg>'
)


def bi(texto_es, texto_en):
    """Texto bilingüe: el CSS enseña solo el del idioma activo."""
    return '<span class="i18n-es">' + texto_es + '</span><span class="i18n-en">' + texto_en + "</span>"


# Páginas informativas: archivo, texto del menú en español e inglés.
PAGINAS_INFORMATIVAS = [
    ("acerca.html", "Acerca de", "About"),
    ("enlaces.html", "Enlaces", "Links"),
    ("autor.html", "Sobre el autor", "About the author"),
    ("privacidad.html", "Privacidad y cookies", "Privacy and cookies"),
    ("changelog.html", "Historial de cambios", "Change log"),
]

# Historial de cambios (de lo más reciente a lo más antiguo). También alimenta feed.xml.
CAMBIOS = [
    {
        "fecha": "2026-11-23",
        "titulo_es": "Vista «Todas», modo oscuro y páginas del sitio",
        "titulo_en": "“All” view, dark mode and site pages",
        "texto_es": "Nueva opción «Todas» en el selector de temporada, con el agregado de las cinco temporadas: 59 de 100 plantillas con coincidencia, frente a 51,6 esperadas. Etiqueta «Selecciona una temporada» junto al selector, botón de tema claro, oscuro o automático, logos de GitHub, LinkedIn y GitHub Sponsors en la cabecera, y una cinta inferior con las páginas Acerca de, Enlaces, Sobre el autor, Privacidad, Historial de cambios, RSS y Licencia.",
        "texto_en": "New “All” option in the season selector, with the aggregate of the five seasons: 59 of 100 squads with a match, against 51.6 expected. A “Pick a season” label next to the selector, a light, dark or automatic theme button, GitHub, LinkedIn and GitHub Sponsors logos in the header, and a bottom ribbon with the About, Links, About the author, Privacy, Change log, RSS and License pages.",
    },
    {
        "fecha": "2026-11-23",
        "titulo_es": "Cinco temporadas y tooltips en el calendario",
        "titulo_en": "Five seasons and tooltips in the calendar",
        "texto_es": "Se añaden las temporadas 2022/23, 2023/24 y 2024/25, con la plantilla al cierre del mercado de verano: se usa la versión de cada artículo de Wikipedia de mediados de septiembre y los dorsales que faltan se completan con bdfutbol. Las fechas de nacimiento se contrastan con Wikidata, que prevalece si es completa, no es el 1 de enero y el año coincide. Al pasar el ratón por el calendario de cumpleaños de un equipo, el tooltip dice qué jugadores cumplen años ese día.",
        "texto_en": "The 2022/23, 2023/24 and 2024/25 seasons are added, with the squad at the close of the summer window: each Wikipedia article is taken as of mid-September and missing shirt numbers are completed from bdfutbol. Birth dates are cross-checked against Wikidata, which prevails if it is complete, is not 1 January and has the same year. Hovering over a team's birthday calendar, the tooltip tells you which players have a birthday that day.",
    },
    {
        "fecha": "2026-11-22",
        "titulo_es": "Primera publicación",
        "titulo_en": "First release",
        "texto_es": "Primera versión del sitio con dos temporadas, 2025/26 y 2026/27: resumen de cuántos equipos de Primera tienen dos jugadores con el mismo cumpleaños, plantilla de cada equipo con las parejas resaltadas y calendario anual. En español e inglés.",
        "texto_en": "First version of the site with two seasons, 2025/26 and 2026/27: a summary of how many Primera División teams have two players sharing a birthday, each team's squad with the matches highlighted, and a yearly calendar. In Spanish and English.",
    },
]


def cabecera_html(subnav_html):
    return (
        '<header class="cabecera-sitio">\n'
        '  <div class="interior">\n'
        '    <a class="marca" href="index.html">🎂 ' + bi("Cumpleaños en LaLiga", "Birthdays in LaLiga")
        + "<small>" + bi("La paradoja del cumpleaños en el fútbol", "The birthday paradox in football") + "</small></a>\n"
        '    <div class="controles">\n'
        '      <a class="icono-autor" href="' + URL_GITHUB + '" target="_blank" rel="noopener" aria-label="GitHub" title="GitHub">' + SVG_GITHUB + "</a>\n"
        '      <a class="icono-autor" href="' + URL_LINKEDIN + '" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn">' + SVG_LINKEDIN + "</a>\n"
        '      <a class="icono-autor" href="' + URL_SPONSORS + '" target="_blank" rel="noopener" aria-label="GitHub Sponsors" title="GitHub Sponsors">' + SVG_SPONSOR + "</a>\n"
        '      <button id="btnTema" type="button" aria-label="Tema claro, oscuro o automático / Light, dark or automatic theme">Tema: auto</button>\n'
        '      <button id="btnIdioma" type="button" aria-label="Idioma / Language">EN</button>\n'
        "    </div>\n"
        "  </div>\n"
        "</header>\n"
        + subnav_html
    )


def subnav_selector_html():
    return (
        '<nav class="subnav" aria-label="Temporada"><div class="interior">\n'
        '  <label for="selTemporada" id="etqTemporada">' + bi("Selecciona una temporada", "Pick a season") + "</label>\n"
        '  <select id="selTemporada"></select>\n'
        "</div></nav>\n"
    )


def subnav_paginas_html(archivo_activo):
    enlaces = ['<a href="index.html">' + bi("Inicio", "Home") + "</a>"]
    for archivo, texto_es, texto_en in PAGINAS_INFORMATIVAS:
        atributo = ' aria-current="page"' if archivo == archivo_activo else ""
        enlaces.append('<a href="' + archivo + '"' + atributo + ">" + bi(texto_es, texto_en) + "</a>")
    return '<nav class="subnav" aria-label="Secciones"><div class="interior">' + "".join(enlaces) + "</div></nav>\n"


def pie_html():
    enlaces_pie = [
        ("LICENSE", "Licencia", "License"),
        ("privacidad.html", "Privacidad y cookies", "Privacy and cookies"),
        ("changelog.html", "Historial de cambios", "Change log"),
        ("feed.xml", "RSS", "RSS"),
        ("acerca.html", "Acerca de", "About"),
        ("autor.html", "Sobre el autor", "About the author"),
        ("enlaces.html", "Enlaces", "Links"),
        ("cerveza.html", "Invítame a una cerveza", "Buy me a beer"),
        (URL_REPOSITORIO, "GitHub", "GitHub"),
    ]
    piezas = []
    for destino, texto_es, texto_en in enlaces_pie:
        piezas.append('<a href="' + destino + '">' + bi(texto_es, texto_en) + "</a>")
    return (
        '<footer class="pie">\n'
        '  <p class="nota" id="pie">'
        + bi("Proyecto personal sin relación con LaLiga ni con ningún club. Datos de Wikipedia (CC BY-SA 4.0), Wikidata (CC0), LALIGA y bdfutbol.",
             "Personal project, not affiliated with LaLiga or any club. Data from Wikipedia (CC BY-SA 4.0), Wikidata (CC0), LALIGA and bdfutbol.")
        + "</p>\n"
        '  <nav aria-label="Pie">' + "\n    ".join(piezas) + "</nav>\n"
        "</footer>\n"
    )


def pagina_html(archivo, titulo_es, titulo_en, descripcion, subnav_html, cuerpo_html, scripts_extra=""):
    return (
        '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + titulo_es + "</title>\n"
        '<meta name="description" content="' + descripcion + '">\n'
        '<link rel="canonical" href="' + URL_BASE + archivo + '">\n'
        '<link rel="alternate" type="application/rss+xml" title="Cumpleaños en LaLiga · Historial de cambios" href="feed.xml">\n'
        '<link rel="stylesheet" href="style.css?v=' + VERSION_ACTIVOS + '">\n'
        "<script>try{var tema=localStorage.getItem('cumple-tema');if(tema==='light'||tema==='dark'){document.documentElement.setAttribute('data-theme',tema);}}catch(e){}</script>\n"
        '</head>\n<body data-titulo-es="' + titulo_es + '" data-titulo-en="' + titulo_en + '">\n'
        + cabecera_html(subnav_html)
        + cuerpo_html
        + pie_html()
        + '<script src="comun.js?v=' + VERSION_ACTIVOS + '"></script>\n'
        + scripts_extra
        + "</body>\n</html>\n"
    )


def cabecera_pagina(titulo_es, titulo_en, subtitulo_es, subtitulo_en):
    return (
        '<div class="cabecera-pagina">\n  <h1>' + bi(titulo_es, titulo_en) + "</h1>\n"
        '  <p class="subtitulo">' + bi(subtitulo_es, subtitulo_en) + "</p>\n</div>\n"
    )


def generar_index():
    cuerpo = '<main id="contenido" aria-live="polite"></main>\n'
    scripts = '<script src="app.js?v=' + VERSION_ACTIVOS + '"></script>\n'
    return pagina_html(
        "index.html", "Cumpleaños en LaLiga", "Birthdays in LaLiga",
        "La paradoja del cumpleaños aplicada a las plantillas de Primera División: qué jugadores de cada equipo comparten cumpleaños.",
        subnav_selector_html(), cuerpo, scripts)


def generar_acerca():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Acerca de este sitio", "About this site",
        "Qué es y cómo se mantiene.", "What it is and how it is kept up to date.")
    cuerpo += '<div class="prosa">\n'
    cuerpo += "<h2>" + bi("Qué es", "What it is") + "</h2>\n"
    cuerpo += "<p>" + bi(
        "La paradoja del cumpleaños dice que en un grupo de solo 23 personas hay más de un 50 % de probabilidad de que dos cumplan años el mismo día. Este sitio la comprueba con un grupo real y fácil de verificar: las plantillas de Primera División, con los jugadores que llevan dorsal del 1 al 25.",
        "The birthday paradox says that in a group of just 23 people there is a better than 50% chance that two share a birthday. This site checks it against a real group that is easy to verify: Primera División squads, with the players wearing shirt numbers 1 to 25.") + "</p>\n"
    cuerpo += "<h2>" + bi("Qué hay", "What is here") + "</h2>\n<ul>\n"
    cuerpo += "<li>" + bi("<b>Resumen</b> de cada temporada: cuántos de los 20 equipos tienen al menos dos jugadores con el mismo cumpleaños, frente a lo que esperaría la teoría según el tamaño de cada plantilla.",
                          "<b>Summary</b> of each season: how many of the 20 teams have at least two players with the same birthday, against what theory would expect given each squad's size.") + "</li>\n"
    cuerpo += "<li>" + bi("<b>Todas</b>: el agregado de las cinco temporadas (de la 2022/23 a la 2026/27).",
                          "<b>All</b>: the aggregate of the five seasons (2022/23 to 2026/27).") + "</li>\n"
    cuerpo += "<li>" + bi("<b>Plantilla de cada equipo</b>, con las parejas resaltadas y un calendario anual cuyo tooltip dice quién cumple años cada día.",
                          "<b>Each team's squad</b>, with the matches highlighted and a yearly calendar whose tooltip says who has a birthday each day.") + "</li>\n</ul>\n"
    cuerpo += "<h2>" + bi("Cómo se hace", "How it is made") + "</h2>\n"
    cuerpo += "<p>" + bi(
        "Unos scripts de Python recogen las plantillas una sola vez y generan un fichero de datos. La web es estática: todo el cálculo de las coincidencias ocurre en tu navegador, sin servidor ni anuncios. La plantilla de la temporada 2026/27 es la oficial de LALIGA; las anteriores son las de Wikipedia al cierre del mercado de verano (mediados de septiembre), con los dorsales que faltan completados con bdfutbol. Las fechas de nacimiento se contrastan con Wikidata.",
        "Python scripts collect the squads once and generate a data file. The site is static: all the match calculation happens in your browser, with no server or ads. The 2026/27 squads are the official LALIGA ones; the earlier ones come from Wikipedia at the close of the summer window (mid-September), with missing shirt numbers completed from bdfutbol. Birth dates are cross-checked against Wikidata.") + "</p>\n"
    cuerpo += "<h2>" + bi("Qué conviene tener presente", "Worth keeping in mind") + "</h2>\n<ul>\n"
    cuerpo += "<li>" + bi("Hay equipos con menos de 25 dorsales ocupados, y algún dorsal repetido por altas y bajas.",
                          "Some teams have fewer than 25 shirt numbers in use, and a few numbers are repeated because of arrivals and departures.") + "</li>\n"
    cuerpo += "<li>" + bi("Las fechas se contrastan con Wikidata, pero solo una parte de las discrepancias se ha confirmado con una tercera fuente. Puede haber errores.",
                          "Dates are cross-checked against Wikidata, but only some of the discrepancies were confirmed with a third source. There may be errors.") + "</li>\n"
    cuerpo += "<li>" + bi("El «esperado» supone 365 días y cumpleaños repartidos por igual, sin tener en cuenta el 29 de febrero ni que haya más nacimientos en unos meses que en otros.",
                          "“Expected” assumes 365 days and evenly spread birthdays, ignoring 29 February and the fact that some months have more births than others.") + "</li>\n</ul>\n"
    cuerpo += "<h2>" + bi("Datos y licencia", "Data and license") + "</h2>\n"
    cuerpo += "<p>" + bi(
        'Las fuentes están en <a href="enlaces.html">Enlaces</a>. El código y el diseño del sitio tienen los derechos reservados salvo lo que indique la <a href="LICENSE">licencia</a>.',
        'Sources are listed under <a href="enlaces.html">Links</a>. The code and design of the site are all rights reserved except where the <a href="LICENSE">license</a> says otherwise.') + "</p>\n"
    cuerpo += "</div>\n</main>\n"
    return pagina_html("acerca.html", "Acerca de · Cumpleaños en LaLiga", "About · Birthdays in LaLiga",
                       "Qué es Cumpleaños en LaLiga y cómo se mantiene.", subnav_paginas_html("acerca.html"), cuerpo)


def generar_autor():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Sobre el autor", "About the author", "Fernando Manzanares Preciado.", "Fernando Manzanares Preciado.")
    cuerpo += '<div class="prosa">\n'
    cuerpo += "<p>" + bi(
        "Me dedico al análisis de datos y la inteligencia de negocio: Power BI, DAX y Python, construyendo paneles y pipelines. Tengo la certificación Microsoft Power BI Data Analyst Associate (PL-300).",
        "I work in data analysis and business intelligence: Power BI, DAX and Python, building dashboards and pipelines. I hold the Microsoft Power BI Data Analyst Associate (PL-300) certification.") + "</p>\n"
    cuerpo += "<p>" + bi(
        'Este sitio es ese mismo oficio aplicado a una afición personal. Forma parte de una serie de proyectos pequeños, junto a <a href="https://fermanpre.github.io/f1-stats/">F1 Lap Times &amp; Gap Chart</a> y <a href="https://fermanpre.github.io/pondera/">PONDERA</a>.',
        'This site is that same craft applied to a personal hobby. It is part of a series of small projects, alongside <a href="https://fermanpre.github.io/f1-stats/">F1 Lap Times &amp; Gap Chart</a> and <a href="https://fermanpre.github.io/pondera/">PONDERA</a>.') + "</p>\n"
    cuerpo += "<h2>" + bi("Dónde encontrarme", "Where to find me") + "</h2>\n<ul class=\"lista-enlaces\">\n"
    cuerpo += '<li><a href="' + URL_GITHUB + '">GitHub: @fermanpre</a></li>\n'
    cuerpo += '<li><a href="' + URL_LINKEDIN + '">LinkedIn: Fernando Manzanares Preciado</a></li>\n'
    cuerpo += '<li><a href="cerveza.html">' + bi("Invítame a una cerveza", "Buy me a beer") + "</a></li>\n</ul>\n</div>\n</main>\n"
    return pagina_html("autor.html", "Sobre el autor · Cumpleaños en LaLiga", "About the author · Birthdays in LaLiga",
                       "Sobre el autor de Cumpleaños en LaLiga.", subnav_paginas_html("autor.html"), cuerpo)


def generar_cerveza():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Invítame a una cerveza", "Buy me a beer",
        "Sin expectativas, solo una opción para quien le apetezca.", "No expectations, just an option for anyone who feels like it.")
    cuerpo += '<div class="prosa">\n'
    cuerpo += "<p>" + bi(
        "Este sitio no lleva anuncios, no vende tus datos y no tiene intención de cobrar nada por nada. Lo hago porque me gusta, y seguiría haciéndolo igual aunque nadie donara un euro. Dicho esto, he pensado que estaría bien habilitar una opción para que quien quiera invitarme a algo lo pueda hacer.",
        "This site has no ads, does not sell your data and has no intention of charging for anything. I do it because I like it, and I would keep doing it even if nobody donated a cent. That said, I thought it would be nice to offer an option for anyone who wants to treat me to something.") + "</p>\n"
    cuerpo += '<p><a class="enlace-contacto-autor" href="' + URL_SPONSORS + '" target="_blank" rel="noopener">' + SVG_SPONSOR + "GitHub Sponsors</a></p>\n"
    cuerpo += "<p>" + bi("Con eso, o sin eso, gracias por pasarte por aquí.", "With that, or without it, thanks for stopping by.") + "</p>\n</div>\n</main>\n"
    return pagina_html("cerveza.html", "Invítame a una cerveza · Cumpleaños en LaLiga", "Buy me a beer · Birthdays in LaLiga",
                       "Una opción para quien quiera invitarme a una cerveza.", subnav_paginas_html("cerveza.html"), cuerpo)


def elemento_enlace(url, texto_es, texto_en, nota_es="", nota_en=""):
    nota = "<span>" + bi(nota_es, nota_en) + "</span>" if nota_es else ""
    return '<li><a href="' + url + '">' + bi(texto_es, texto_en) + "</a>" + nota + "</li>\n"


def generar_enlaces():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Enlaces", "Links", "Las fuentes de los datos y otros sitios relacionados.", "The data sources and other related sites.")
    cuerpo += '<div class="prosa">\n<h2>' + bi("Fuentes de los datos", "Data sources") + "</h2>\n<ul class=\"lista-enlaces\">\n"
    cuerpo += elemento_enlace("https://es.wikipedia.org/wiki/Primera_Divisi%C3%B3n_de_Espa%C3%B1a", "Wikipedia en español: Primera División de España",
                              "Spanish Wikipedia: Primera División de España",
                              "Plantillas de los clubes y lista de equipos de cada temporada (CC BY-SA 4.0).",
                              "Club squads and the list of teams for each season (CC BY-SA 4.0).")
    cuerpo += elemento_enlace("https://www.wikidata.org/", "Wikidata", "Wikidata",
                              "Fechas de nacimiento para contrastar las de Wikipedia (CC0).",
                              "Birth dates used to cross-check Wikipedia's (CC0).")
    cuerpo += elemento_enlace("https://www.laliga.com/laliga-easports/clubes", "LALIGA: clubes y plantillas",
                              "LALIGA: clubs and squads",
                              "Plantilla oficial de la temporada 2026/27, con dorsal y fecha de nacimiento.",
                              "Official 2026/27 squads, with shirt number and birth date.")
    cuerpo += elemento_enlace("https://www.bdfutbol.com/", "BDFutbol", "BDFutbol",
                              "Dorsales de las temporadas anteriores (solo dorsal y nombre; no se copian sus tablas).",
                              "Shirt numbers for the earlier seasons (only number and name; its tables are not copied).")
    cuerpo += "</ul>\n<h2>" + bi("Código", "Code") + "</h2>\n<ul class=\"lista-enlaces\">\n"
    cuerpo += elemento_enlace(URL_REPOSITORIO, "github.com/fermanpre/cumpleanos-laliga", "github.com/fermanpre/cumpleanos-laliga",
                              "Repositorio del sitio, con los scripts que recogen y contrastan los datos.",
                              "The site's repository, with the scripts that collect and cross-check the data.")
    cuerpo += "</ul>\n<h2>" + bi("Otros proyectos del autor", "Other projects by the author") + "</h2>\n<ul class=\"lista-enlaces\">\n"
    cuerpo += elemento_enlace("https://fermanpre.github.io/f1-stats/", "F1 Lap Times & Gap Chart".replace("&", "&amp;"), "F1 Lap Times &amp; Gap Chart",
                              "Tiempos por vuelta y diferencias con el líder de las carreras de Fórmula 1.",
                              "Lap times and gaps to the leader in Formula 1 races.")
    cuerpo += elemento_enlace("https://fermanpre.github.io/pondera/", "PONDERA", "PONDERA",
                              "Previsión de las elecciones generales de España de 2026.",
                              "Forecast for the 2026 Spanish general election.")
    cuerpo += elemento_enlace(URL_GITHUB, "GitHub: @fermanpre", "GitHub: @fermanpre")
    cuerpo += elemento_enlace(URL_LINKEDIN, "LinkedIn", "LinkedIn")
    cuerpo += "</ul>\n</div>\n</main>\n"
    return pagina_html("enlaces.html", "Enlaces · Cumpleaños en LaLiga", "Links · Birthdays in LaLiga",
                       "Fuentes de los datos y otros sitios relacionados.", subnav_paginas_html("enlaces.html"), cuerpo)


def generar_privacidad():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Privacidad y cookies", "Privacy and cookies",
        "Qué datos guarda esta web y cómo puedes controlarlos.", "What data this site stores and how you can control it.")
    cuerpo += '<div class="prosa">\n'
    cuerpo += "<h2>" + bi("Qué datos recoge", "What data it collects") + "</h2>\n<p>" + bi(
        "Es un proyecto personal sin cuentas, formularios ni publicidad. La web no te pide ni guarda datos personales, y no usa herramientas de analítica ni cookies.",
        "It is a personal project with no accounts, forms or ads. The site does not ask for or store personal data, and uses no analytics tools or cookies.") + "</p>\n"
    cuerpo += "<h2>" + bi("Almacenamiento en tu navegador", "Storage in your browser") + "</h2>\n<p>" + bi(
        "La web guarda en tu navegador, sin enviarlas a nadie, dos preferencias: el tema claro, oscuro o automático (<code>cumple-tema</code>) y el idioma (<code>idioma</code>). Son necesarias para el funcionamiento de la página y no requieren consentimiento. Puedes borrarlas desde los ajustes de tu navegador.",
        "The site stores two preferences in your browser, without sending them anywhere: the light, dark or automatic theme (<code>cumple-tema</code>) and the language (<code>idioma</code>). They are needed for the page to work and do not require consent. You can delete them from your browser settings.") + "</p>\n"
    cuerpo += "<h2>" + bi("Alojamiento", "Hosting") + "</h2>\n<p>" + bi(
        "El sitio se aloja en GitHub Pages (GitHub, Inc.), que puede registrar datos técnicos de las visitas, como la dirección IP, según su propia política de privacidad. Este sitio no tiene acceso a esos registros.",
        "The site is hosted on GitHub Pages (GitHub, Inc.), which may log technical data about visits, such as the IP address, under its own privacy policy. This site has no access to those logs.") + "</p>\n"
    cuerpo += "<h2>" + bi("Contacto", "Contact") + "</h2>\n<p>" + bi(
        'Para cualquier duda, consulta <a href="autor.html">Sobre el autor</a> o abre una incidencia en el <a href="' + URL_REPOSITORIO + '/issues">repositorio del proyecto</a>.',
        'For any question, see <a href="autor.html">About the author</a> or open an issue in the <a href="' + URL_REPOSITORIO + '/issues">project repository</a>.') + "</p>\n"
    cuerpo += "</div>\n</main>\n"
    return pagina_html("privacidad.html", "Privacidad y cookies · Cumpleaños en LaLiga", "Privacy and cookies · Birthdays in LaLiga",
                       "Qué datos guarda esta web y cómo controlarlos.", subnav_paginas_html("privacidad.html"), cuerpo)


def fecha_legible(fecha_iso):
    fecha = datetime.date.fromisoformat(fecha_iso)
    meses_es = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    meses_en = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    texto_es = str(fecha.day) + " de " + meses_es[fecha.month - 1] + " de " + str(fecha.year)
    texto_en = meses_en[fecha.month - 1] + " " + str(fecha.day) + ", " + str(fecha.year)
    return bi(texto_es, texto_en)


def generar_changelog():
    cuerpo = '<main class="contenedor-pagina">\n' + cabecera_pagina(
        "Historial de cambios", "Change log",
        'Registro de las actualizaciones del sitio, de la más reciente a la más antigua. <a href="feed.xml">RSS</a>.',
        'Record of the site\'s updates, from the most recent to the oldest. <a href="feed.xml">RSS</a>.')
    cuerpo += '<section id="cambios">\n'
    for indice, cambio in enumerate(CAMBIOS):
        cuerpo += ('<article class="entrada-cambio" id="cambio-' + str(indice) + '"><time datetime="' + cambio["fecha"] + '">'
                   + fecha_legible(cambio["fecha"]) + "</time><h3>" + bi(cambio["titulo_es"], cambio["titulo_en"])
                   + "</h3><p>" + bi(cambio["texto_es"], cambio["texto_en"]) + "</p></article>\n")
    cuerpo += "</section>\n</main>\n"
    return pagina_html("changelog.html", "Historial de cambios · Cumpleaños en LaLiga", "Change log · Birthdays in LaLiga",
                       "Historial de cambios del sitio.", subnav_paginas_html("changelog.html"), cuerpo)


def escapar_xml(texto):
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generar_feed():
    items = []
    for indice, cambio in enumerate(CAMBIOS):
        fecha = datetime.datetime.fromisoformat(cambio["fecha"] + "T12:00:00+00:00")
        fecha_rfc = fecha.strftime("%a, %d %b %Y %H:%M:%S +0000")
        enlace = URL_BASE + "changelog.html#cambio-" + str(indice)
        items.append(
            "    <item>\n      <title>" + escapar_xml(cambio["titulo_es"]) + "</title>\n"
            "      <link>" + enlace + "</link>\n      <guid isPermaLink=\"true\">" + enlace + "</guid>\n"
            "      <pubDate>" + fecha_rfc + "</pubDate>\n"
            "      <description>" + escapar_xml(cambio["texto_es"]) + "</description>\n    </item>\n")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n'
        "    <title>Cumpleaños en LaLiga · Historial de cambios</title>\n"
        "    <link>" + URL_BASE + "changelog.html</link>\n"
        "    <description>Cambios del sitio Cumpleaños en LaLiga.</description>\n"
        "    <language>es</language>\n" + "".join(items) + "  </channel>\n</rss>\n")


def generar_licencia():
    return (
        "Copyright (c) 2026 fermanpre. All rights reserved.\n\n"
        "This repository and its contents, including but not limited to source\n"
        "code, design, and the specific compilation and presentation of data, may\n"
        "not be copied, reproduced, distributed, republished, or used to create\n"
        "derivative works, in whole or in part, without prior written permission\n"
        "from the copyright holder.\n\n"
        "Viewing and linking to the published site is, of course, welcome.\n\n"
        "Exception: the squad and birth-date data come in part from Spanish Wikipedia\n"
        "(CC BY-SA 4.0) and Wikidata (CC0) and remain available under those licences.\n"
        "Official squad data from LALIGA and shirt numbers from BDFutbol remain subject\n"
        "to their own terms.\n\n"
        "This website is unofficial and is not associated with LaLiga, any club or\n"
        "any player.\n")


def escribir(nombre, contenido):
    with open(os.path.join(SITIO, nombre), "w", encoding="utf-8", newline="\n") as fichero:
        fichero.write(contenido)
    print("escrito:", nombre, len(contenido), "caracteres")


def main():
    escribir("index.html", generar_index())
    escribir("acerca.html", generar_acerca())
    escribir("autor.html", generar_autor())
    escribir("cerveza.html", generar_cerveza())
    escribir("enlaces.html", generar_enlaces())
    escribir("privacidad.html", generar_privacidad())
    escribir("changelog.html", generar_changelog())
    escribir("feed.xml", generar_feed())
    escribir("LICENSE", generar_licencia())


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
