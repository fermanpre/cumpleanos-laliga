"use strict";

/* Tema (auto, claro, oscuro) e idioma (es, en), compartidos por todas las páginas del sitio.
   El primer paso de aplicar el tema guardado se hace en el <head> de cada página para evitar el parpadeo. */
(function () {
  var ETIQUETAS_TEMA = {
    es: { auto: "Tema: auto", claro: "Tema: claro", oscuro: "Tema: oscuro" },
    en: { auto: "Theme: auto", claro: "Theme: light", oscuro: "Theme: dark" }
  };
  var oyentesDeIdioma = [];

  function idiomaGuardado() {
    try {
      var guardado = localStorage.getItem("idioma");
      if (guardado === "es" || guardado === "en") { return guardado; }
    } catch (error) { /* sin almacenamiento */ }
    return (navigator.language || "es").slice(0, 2) === "es" ? "es" : "en";
  }

  function idiomaActual() {
    return document.documentElement.lang === "en" ? "en" : "es";
  }

  function etiquetaTema() {
    var atributo = document.documentElement.getAttribute("data-theme");
    if (atributo === "light") { return "claro"; }
    if (atributo === "dark") { return "oscuro"; }
    return "auto";
  }

  function pintarBotones() {
    var idioma = idiomaActual();
    var botonIdioma = document.getElementById("btnIdioma");
    var botonTema = document.getElementById("btnTema");
    if (botonIdioma) { botonIdioma.textContent = idioma === "es" ? "EN" : "ES"; }
    if (botonTema) { botonTema.textContent = ETIQUETAS_TEMA[idioma][etiquetaTema()]; }
    var titulo = document.body.getAttribute("data-titulo-" + idioma);
    if (titulo) { document.title = titulo; }
  }

  function aplicarIdioma(idioma) {
    document.documentElement.lang = idioma;
    pintarBotones();
  }

  function cambiarIdioma() {
    var nuevo = idiomaActual() === "es" ? "en" : "es";
    try { localStorage.setItem("idioma", nuevo); } catch (error) { /* sin almacenamiento */ }
    aplicarIdioma(nuevo);
    oyentesDeIdioma.forEach(function (oyente) { oyente(nuevo); });
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
    pintarBotones();
  }

  document.documentElement.lang = idiomaGuardado();
  var botonIdioma = document.getElementById("btnIdioma");
  var botonTema = document.getElementById("btnTema");
  if (botonIdioma) { botonIdioma.addEventListener("click", cambiarIdioma); }
  if (botonTema) { botonTema.addEventListener("click", cambiarTema); }
  pintarBotones();

  window.Comun = {
    idioma: idiomaActual,
    alCambiarIdioma: function (oyente) { oyentesDeIdioma.push(oyente); }
  };
})();
