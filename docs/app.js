"use strict";

var TEXTOS = {
  es: {
    titulo: "Cumpleaños en LaLiga",
    temporada: "Temporada",
    resumen_titulo: "¿Cuántos equipos de Primera tienen dos jugadores con el mismo cumpleaños?",
    explicacion: "La paradoja del cumpleaños dice que en un grupo de solo 23 personas hay más de un 50 % de probabilidad de que dos cumplan años el mismo día. Una plantilla de fútbol tiene hasta 25 dorsales (del 1 al 25). Aquí está comprobado con las plantillas reales.",
    de_equipos: "de {n} equipos tienen al menos dos jugadores que cumplen años el mismo día",
    observado: "Observado",
    esperado: "Esperado",
    nota_esperado: "Esperado = probabilidad teórica de coincidencia según el número de jugadores de cada equipo (365 días, cumpleaños uniformes).",
    equipos: "Equipos",
    buscar: "Buscar equipo…",
    jugadores: "jugadores",
    pareja_una: "1 coincidencia",
    pareja_n: "{n} coincidencias",
    atras: "← Volver al resumen",
    dorsal: "Dorsal",
    jugador: "Jugador",
    cumple: "Cumpleaños",
    sin_coincidencias: "En esta plantilla no hay dos jugadores con el mismo cumpleaños.",
    coinciden: "Comparten cumpleaños",
    calendario: "Calendario de cumpleaños",
    un_jugador: "1 jugador",
    varios: "2 o más jugadores",
    ninguno: "Ninguno",
    nota_plantilla: "Jugadores con dorsal del 1 al 25 que figuran en la plantilla del club (fuentes al pie de la página). Puede haber dorsales sin jugador o altas y bajas recientes.",
    fuente: "Fuentes: plantilla oficial de LALIGA (temporada 2026/27); Wikipedia en español (CC BY-SA 4.0) y bdfutbol.com (solo dorsales) para el resto, con fechas contrastadas con Wikidata (CC0). Plantillas al cierre del mercado de verano; consultadas el {fecha}. Puede haber errores en fechas y dorsales. Proyecto de portfolio.",
    y: " y ",
    no_encontrado: "No se ha encontrado ese equipo.",
    x_de: "{a} de {b}",
    subtitulo: "La paradoja del cumpleaños en el fútbol",
    selecciona: "Selecciona una temporada",
    todas: "Todas",
    tema_auto: "Tema: auto",
    tema_claro: "Tema: claro",
    tema_oscuro: "Tema: oscuro",
    todas_titulo: "Las cinco temporadas juntas",
    todas_explicacion: "Suma de todos los equipos y temporadas: cada equipo-temporada cuenta una vez si tiene al menos dos jugadores con el mismo cumpleaños.",
    de_equipos_temporada: "de {n} plantillas (equipo y temporada) tienen al menos dos jugadores que cumplen años el mismo día",
    col_temporada: "Temporada",
    col_equipos: "Equipos",
    col_observado: "Con coincidencia",
    col_esperado: "Esperado",
    total: "Total",
    por_temporada: "Resumen por temporada",
    veces: "{a} de {b} temporadas con coincidencia",
    ultima_plantilla: "Ver la plantilla más reciente"
  },
  en: {
    titulo: "Birthdays in LaLiga",
    temporada: "Season",
    resumen_titulo: "How many Primera División teams have two players sharing a birthday?",
    explicacion: "The birthday paradox says that in a group of just 23 people there is a better than 50% chance that two share a birthday. A football squad has up to 25 shirt numbers (1 to 25). Here it is checked against real squads.",
    de_equipos: "of {n} teams have at least two players with the same birthday",
    observado: "Observed",
    esperado: "Expected",
    nota_esperado: "Expected = theoretical probability of a match given each team's number of players (365 days, uniform birthdays).",
    equipos: "Teams",
    buscar: "Search team…",
    jugadores: "players",
    pareja_una: "1 match",
    pareja_n: "{n} matches",
    atras: "← Back to summary",
    dorsal: "No.",
    jugador: "Player",
    cumple: "Birthday",
    sin_coincidencias: "No two players in this squad share a birthday.",
    coinciden: "Sharing a birthday",
    calendario: "Birthday calendar",
    un_jugador: "1 player",
    varios: "2 or more players",
    ninguno: "None",
    nota_plantilla: "Players with shirt numbers 1 to 25 listed in the club's squad (sources at the bottom of the page). Some numbers may be vacant, and recent signings or departures may be missing.",
    fuente: "Sources: official LALIGA squads (2026/27 season); Spanish Wikipedia (CC BY-SA 4.0) and bdfutbol.com (shirt numbers only) for the others, with dates cross-checked against Wikidata (CC0). Squads at the close of the summer window; retrieved {fecha}. Dates and shirt numbers may contain errors. Portfolio project.",
    y: " and ",
    no_encontrado: "Team not found.",
    x_de: "{a} of {b}",
    subtitulo: "The birthday paradox in football",
    selecciona: "Pick a season",
    todas: "All",
    tema_auto: "Theme: auto",
    tema_claro: "Theme: light",
    tema_oscuro: "Theme: dark",
    todas_titulo: "All five seasons together",
    todas_explicacion: "Sum of every team and season: each team-season counts once if it has at least two players with the same birthday.",
    de_equipos_temporada: "of {n} squads (team and season) have at least two players with the same birthday",
    col_temporada: "Season",
    col_equipos: "Teams",
    col_observado: "With a match",
    col_esperado: "Expected",
    total: "Total",
    por_temporada: "Summary by season",
    veces: "{a} of {b} seasons with a match",
    ultima_plantilla: "See the latest squad"
  }
};

var estado = { idioma: "es", datos: null, temporada: null };

function t(clave, valores) {
  var texto = TEXTOS[estado.idioma][clave] || clave;
  if (valores) {
    Object.keys(valores).forEach(function (nombre) {
      texto = texto.replace("{" + nombre + "}", valores[nombre]);
    });
  }
  return texto;
}

function escapar(texto) {
  return String(texto).replace(/[&<>"']/g, function (caracter) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[caracter];
  });
}

function nombreMes(numeroMes) {
  return new Intl.DateTimeFormat(estado.idioma, { month: "long", timeZone: "UTC" })
    .format(new Date(Date.UTC(2024, numeroMes - 1, 1)));
}

function textoFecha(mes, dia) {
  var mesCorto = new Intl.DateTimeFormat(estado.idioma, { month: "short", timeZone: "UTC" })
    .format(new Date(Date.UTC(2024, mes - 1, 1))).replace(".", "");
  return estado.idioma === "es" ? dia + " " + mesCorto : mesCorto + " " + dia;
}

/* Agrupa jugadores por mes y día; devuelve solo los grupos con 2 o más. */
function coincidenciasDe(jugadores) {
  var grupos = {};
  jugadores.forEach(function (jugador) {
    var clave = jugador.mes + "-" + jugador.dia;
    if (!grupos[clave]) { grupos[clave] = []; }
    grupos[clave].push(jugador);
  });
  return Object.keys(grupos)
    .map(function (clave) { return grupos[clave]; })
    .filter(function (grupo) { return grupo.length > 1; })
    .sort(function (a, b) { return (a[0].mes * 100 + a[0].dia) - (b[0].mes * 100 + b[0].dia); });
}

/* Probabilidad teórica de que entre n personas haya al menos dos con el mismo cumpleaños. */
function probabilidadTeorica(n) {
  var sinCoincidencia = 1;
  for (var i = 0; i < n; i++) { sinCoincidencia *= (365 - i) / 365; }
  return 1 - sinCoincidencia;
}

function formatoNumero(valor, decimales) {
  return new Intl.NumberFormat(estado.idioma, { minimumFractionDigits: decimales, maximumFractionDigits: decimales }).format(valor);
}

function equiposDeTemporada() {
  return estado.datos.temporadas[estado.temporada].equipos;
}

/* Vista «Todas»: suma de todos los equipos y temporadas. */
function calcularAgregado() {
  var temporadas = Object.keys(estado.datos.temporadas).sort().reverse();
  var filas = [];
  var porEquipo = {};
  var totalEquipos = 0;
  var totalObservado = 0;
  var totalEsperado = 0;
  temporadas.forEach(function (clave) {
    var observado = 0;
    var esperado = 0;
    var equipos = estado.datos.temporadas[clave].equipos;
    equipos.forEach(function (equipo) {
      var grupos = coincidenciasDe(equipo.jugadores);
      if (grupos.length > 0) { observado++; }
      esperado += probabilidadTeorica(equipo.jugadores.length);
      if (!porEquipo[equipo.id]) {
        porEquipo[equipo.id] = { id: equipo.id, nombre: equipo.nombre, temporadas: 0, con: 0, ultima: clave, parejas: [] };
      }
      var acumulado = porEquipo[equipo.id];
      acumulado.temporadas++;
      if (grupos.length > 0) { acumulado.con++; }
    });
    filas.push({ clave: clave, equipos: equipos.length, observado: observado, esperado: esperado });
    totalEquipos += equipos.length;
    totalObservado += observado;
    totalEsperado += esperado;
  });
  var lista = Object.keys(porEquipo).map(function (id) { return porEquipo[id]; });
  lista.sort(function (a, b) { return a.nombre.localeCompare(b.nombre); });
  return { filas: filas, lista: lista, totalEquipos: totalEquipos, totalObservado: totalObservado, totalEsperado: totalEsperado };
}

function pintarAgregado() {
  var agregado = calcularAgregado();
  estado.agregado = agregado;
  var html = "";
  html += "<h1>" + escapar(t("todas_titulo")) + "</h1>";
  html += '<p class="explica">' + escapar(t("todas_explicacion")) + "</p>";
  html += '<div class="cifra"><span class="grande">' + agregado.totalObservado + "</span>" +
    '<span class="texto">' + escapar(t("de_equipos_temporada", { n: agregado.totalEquipos })) + "</span></div>";
  html += '<div class="comparacion">';
  html += '<div class="fila-barra"><span>' + escapar(t("observado")) + '</span><div class="pista"><div class="relleno real" style="width:' +
    (agregado.totalObservado / agregado.totalEquipos * 100) + '%"></div></div><strong>' + agregado.totalObservado + "</strong></div>";
  html += '<div class="fila-barra"><span>' + escapar(t("esperado")) + '</span><div class="pista"><div class="relleno teorico" style="width:' +
    (agregado.totalEsperado / agregado.totalEquipos * 100) + '%"></div></div><strong>' + formatoNumero(agregado.totalEsperado, 1) + "</strong></div>";
  html += '<p class="nota">' + escapar(t("nota_esperado")) + "</p></div>";
  html += "<h2>" + escapar(t("por_temporada")) + "</h2>";
  html += '<table class="resumen-tabla"><thead><tr><th>' + escapar(t("col_temporada")) + '</th><th class="cifra-celda">' +
    escapar(t("col_equipos")) + '</th><th class="cifra-celda">' + escapar(t("col_observado")) + '</th><th class="cifra-celda">' +
    escapar(t("col_esperado")) + "</th></tr></thead><tbody>";
  agregado.filas.forEach(function (fila) {
    html += '<tr><td><a href="#/' + fila.clave + '">' + escapar(fila.clave.replace("-", "/")) + '</a></td><td class="cifra-celda">' + fila.equipos +
      '</td><td class="cifra-celda">' + fila.observado + '</td><td class="cifra-celda">' + formatoNumero(fila.esperado, 1) + "</td></tr>";
  });
  html += '<tr class="total"><td>' + escapar(t("total")) + '</td><td class="cifra-celda">' + agregado.totalEquipos + '</td><td class="cifra-celda">' +
    agregado.totalObservado + '</td><td class="cifra-celda">' + formatoNumero(agregado.totalEsperado, 1) + "</td></tr></tbody></table>";
  html += "<h2>" + escapar(t("equipos")) + "</h2>";
  html += '<input class="filtro" id="filtro" type="search" placeholder="' + escapar(t("buscar")) + '" aria-label="' + escapar(t("buscar")) + '">';
  html += '<div class="rejilla" id="rejilla"></div>';
  document.getElementById("contenido").innerHTML = html;
  var filtro = document.getElementById("filtro");
  filtro.addEventListener("input", function () { pintarTarjetasAgregado(filtro.value); });
  pintarTarjetasAgregado("");
}

function pintarTarjetasAgregado(consulta) {
  var buscado = sinTildes(consulta);
  var html = "";
  estado.agregado.lista.forEach(function (equipo) {
    if (buscado && sinTildes(equipo.nombre).indexOf(buscado) < 0) { return; }
    html += '<a class="tarjeta' + (equipo.con ? " coincide" : "") + '" href="#/' + equipo.ultima + "/" + equipo.id + '">';
    html += "<strong>" + escapar(equipo.nombre) + "</strong>";
    html += "<small>" + escapar(t("veces", { a: equipo.con, b: equipo.temporadas })) + "</small>";
    html += "<small>" + escapar(t("ultima_plantilla")) + " (" + escapar(equipo.ultima.replace("-", "/")) + ")</small>";
    html += "</a>";
  });
  document.getElementById("rejilla").innerHTML = html;
}

function pintarResumen() {
  if (estado.temporada === "todas") { pintarAgregado(); return; }
  var equipos = equiposDeTemporada();
  var conCoincidencia = 0;
  var esperado = 0;
  equipos.forEach(function (equipo) {
    equipo.grupos = coincidenciasDe(equipo.jugadores);
    if (equipo.grupos.length > 0) { conCoincidencia++; }
    esperado += probabilidadTeorica(equipo.jugadores.length);
  });
  var total = equipos.length;
  var html = "";
  html += "<h1>" + escapar(t("resumen_titulo")) + "</h1>";
  html += '<p class="explica">' + escapar(t("explicacion")) + "</p>";
  html += '<div class="cifra"><span class="grande">' + conCoincidencia + "</span>" +
    '<span class="texto">' + escapar(t("de_equipos", { n: total })) + "</span></div>";
  html += '<div class="comparacion">';
  html += '<div class="fila-barra"><span>' + escapar(t("observado")) + '</span><div class="pista"><div class="relleno real" style="width:' +
    (conCoincidencia / total * 100) + '%"></div></div><strong>' + conCoincidencia + "</strong></div>";
  html += '<div class="fila-barra"><span>' + escapar(t("esperado")) + '</span><div class="pista"><div class="relleno teorico" style="width:' +
    (esperado / total * 100) + '%"></div></div><strong>' + formatoNumero(esperado, 1) + "</strong></div>";
  html += '<p class="nota">' + escapar(t("nota_esperado")) + "</p></div>";
  html += "<h2>" + escapar(t("equipos")) + "</h2>";
  html += '<input class="filtro" id="filtro" type="search" placeholder="' + escapar(t("buscar")) + '" aria-label="' + escapar(t("buscar")) + '">';
  html += '<div class="rejilla" id="rejilla"></div>';
  document.getElementById("contenido").innerHTML = html;
  var filtro = document.getElementById("filtro");
  filtro.addEventListener("input", function () { pintarTarjetas(filtro.value); });
  pintarTarjetas("");
}

function sinTildes(texto) {
  return texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

function pintarTarjetas(consulta) {
  var buscado = sinTildes(consulta);
  var html = "";
  equiposDeTemporada().forEach(function (equipo) {
    if (buscado && sinTildes(equipo.nombre).indexOf(buscado) < 0) { return; }
    var cantidad = equipo.grupos.length;
    html += '<a class="tarjeta' + (cantidad ? " coincide" : "") + '" href="#/' + estado.temporada + "/" + equipo.id + '">';
    html += "<strong>" + escapar(equipo.nombre) + "</strong>";
    html += "<small>" + equipo.jugadores.length + " " + escapar(t("jugadores")) + "</small>";
    if (cantidad) {
      html += '<span class="etiqueta">' + escapar(cantidad === 1 ? t("pareja_una") : t("pareja_n", { n: cantidad })) + "</span>";
      equipo.grupos.forEach(function (grupo) {
        html += "<small>" + escapar(textoFecha(grupo[0].mes, grupo[0].dia)) + ": " +
          grupo.map(function (jugador) { return escapar(jugador.nombre); }).join(escapar(t("y"))) + "</small>";
      });
    }
    html += "</a>";
  });
  document.getElementById("rejilla").innerHTML = html;
}

function diasDelMes(mes) {
  return [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1];
}

function pintarEquipo(idEquipo) {
  var equipo = equiposDeTemporada().filter(function (candidato) { return candidato.id === idEquipo; })[0];
  var contenedor = document.getElementById("contenido");
  if (!equipo) {
    contenedor.innerHTML = '<p>' + escapar(t("no_encontrado")) + '</p><a href="#/' + estado.temporada + '">' + escapar(t("atras")) + "</a>";
    return;
  }
  var grupos = coincidenciasDe(equipo.jugadores);
  var conPareja = {};
  grupos.forEach(function (grupo) {
    grupo.forEach(function (jugador) { conPareja[jugador.dorsal + "|" + jugador.nombre] = true; });
  });
  var ocupacion = {};
  equipo.jugadores.forEach(function (jugador) {
    var clave = jugador.mes + "-" + jugador.dia;
    if (!ocupacion[clave]) { ocupacion[clave] = []; }
    ocupacion[clave].push(jugador);
  });
  var html = '<a class="atras" href="#/' + estado.temporada + '">' + escapar(t("atras")) + "</a>";
  html += "<h1>" + escapar(equipo.nombre) + " · " + escapar(estado.temporada.replace("-", "/")) + "</h1>";
  if (grupos.length) {
    html += "<h2>" + escapar(t("coinciden")) + "</h2><ul class=\"pares\">";
    grupos.forEach(function (grupo) {
      html += "<li><strong>" + escapar(textoFecha(grupo[0].mes, grupo[0].dia)) + "</strong>: " +
        grupo.map(function (jugador) { return escapar(jugador.nombre) + " (" + jugador.dorsal + ")"; }).join(escapar(t("y"))) + "</li>";
    });
    html += "</ul>";
  } else {
    html += '<p class="explica">' + escapar(t("sin_coincidencias")) + "</p>";
  }
  html += "<h2>" + escapar(t("calendario")) + "</h2><div class=\"calendario\">";
  for (var mes = 1; mes <= 12; mes++) {
    html += '<div class="mes"><span class="etq">' + escapar(nombreMes(mes).slice(0, 3)) + "</span>";
    for (var dia = 1; dia <= 31; dia++) {
      if (dia > diasDelMes(mes)) { html += '<span class="dia fuera"></span>'; continue; }
      var jugadoresDelDia = ocupacion[mes + "-" + dia] || [];
      var cantidad = jugadoresDelDia.length;
      var clase = cantidad > 1 ? "varios" : cantidad === 1 ? "uno" : "";
      var textoTooltip = textoFecha(mes, dia);
      jugadoresDelDia.forEach(function (jugador) {
        textoTooltip += "\n" + jugador.nombre + " (" + jugador.dorsal + ")";
      });
      html += '<span class="dia ' + clase + '" title="' + escapar(textoTooltip) + '"></span>';
    }
    html += "</div>";
  }
  html += '<div class="leyenda"><span><i style="background:var(--vacio)"></i>' + escapar(t("ninguno")) +
    '</span><span><i style="background:var(--ocupado)"></i>' + escapar(t("un_jugador")) +
    '</span><span><i style="background:var(--acento)"></i>' + escapar(t("varios")) + "</span></div></div>";
  html += "<h2>" + escapar(t("jugadores").charAt(0).toUpperCase() + t("jugadores").slice(1)) + "</h2>";
  html += "<table><thead><tr><th>" + escapar(t("dorsal")) + "</th><th>" + escapar(t("jugador")) + "</th><th>" + escapar(t("cumple")) + "</th></tr></thead><tbody>";
  equipo.jugadores.forEach(function (jugador) {
    var par = conPareja[jugador.dorsal + "|" + jugador.nombre];
    html += "<tr" + (par ? ' class="par"' : "") + '><td class="num">' + jugador.dorsal + "</td><td>" +
      escapar(jugador.nombre) + "</td><td>" + escapar(textoFecha(jugador.mes, jugador.dia)) + "</td></tr>";
  });
  html += '</tbody></table><p class="nota">' + escapar(t("nota_plantilla")) + "</p>";
  contenedor.innerHTML = html;
  window.scrollTo(0, 0);
}

function pintarCabeceraYPie() {
  document.documentElement.lang = estado.idioma;
  document.title = t("titulo");
  var elementos = document.querySelectorAll("[data-i18n]");
  Array.prototype.forEach.call(elementos, function (elemento) {
    elemento.textContent = t(elemento.getAttribute("data-i18n"));
  });
  document.getElementById("btnIdioma").textContent = estado.idioma === "es" ? "EN" : "ES";
  document.getElementById("btnTema").textContent = t("tema_" + etiquetaTema());
  document.getElementById("pie").textContent = t("fuente", { fecha: estado.datos.consulta });
}

function pintarTemporadas() {
  var selector = document.getElementById("selTemporada");
  selector.innerHTML = "";
  var opcionTodas = document.createElement("option");
  opcionTodas.value = "todas";
  opcionTodas.textContent = t("todas");
  selector.appendChild(opcionTodas);
  Object.keys(estado.datos.temporadas).sort().reverse().forEach(function (clave) {
    var opcion = document.createElement("option");
    opcion.value = clave;
    opcion.textContent = clave.replace("-", "/");
    selector.appendChild(opcion);
  });
  selector.value = estado.temporada;
}

function enrutar() {
  var partes = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  if (partes[0] && (partes[0] === "todas" || estado.datos.temporadas[partes[0]])) { estado.temporada = partes[0]; }
  document.getElementById("selTemporada").value = estado.temporada;
  if (partes[1] && estado.temporada !== "todas") { pintarEquipo(partes[1]); } else { pintarResumen(); }
}

/* Tema: automático (según el sistema), claro u oscuro; se guarda en el navegador si se puede. */
function etiquetaTema() {
  var atributo = document.documentElement.getAttribute("data-theme");
  if (atributo === "light") { return "claro"; }
  if (atributo === "dark") { return "oscuro"; }
  return "auto";
}

function cambiarTema() {
  var siguiente = { auto: "light", claro: "dark", oscuro: "auto" }[etiquetaTema()];
  if (siguiente === "auto") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", siguiente);
  }
  try {
    if (siguiente === "auto") { localStorage.removeItem("cumple-tema"); } else { localStorage.setItem("cumple-tema", siguiente); }
  } catch (error) { /* sin almacenamiento: vale solo para esta visita */ }
  document.getElementById("btnTema").textContent = t("tema_" + etiquetaTema());
}

function guardarIdioma() {
  try { localStorage.setItem("idioma", estado.idioma); } catch (error) { /* sin almacenamiento */ }
}

function iniciar(datos) {
  estado.datos = datos;
  var guardado = null;
  try { guardado = localStorage.getItem("idioma"); } catch (error) { /* sin almacenamiento */ }
  estado.idioma = guardado === "en" || guardado === "es" ? guardado :
    (navigator.language || "es").slice(0, 2) === "es" ? "es" : "en";
  estado.temporada = Object.keys(datos.temporadas).sort().reverse()[0];
  pintarTemporadas();
  pintarCabeceraYPie();
  document.getElementById("selTemporada").addEventListener("change", function (evento) {
    var partes = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    location.hash = "#/" + evento.target.value + (partes[1] ? "/" + partes[1] : "");
  });
  document.getElementById("btnIdioma").addEventListener("click", function () {
    estado.idioma = estado.idioma === "es" ? "en" : "es";
    guardarIdioma();
    pintarTemporadas();
    pintarCabeceraYPie();
    enrutar();
  });
  document.getElementById("btnTema").addEventListener("click", cambiarTema);
  window.addEventListener("hashchange", enrutar);
  enrutar();
}

fetch("datos.json")
  .then(function (respuesta) { return respuesta.json(); })
  .then(iniciar)
  .catch(function (error) {
    document.getElementById("contenido").textContent = "Error: " + error;
  });
