---
title: ASCII VJ Remix
description: "ASCII VJ Remix es un visualizador de escritorio para DJs y VJs que quieren video ASCII, cámara y visuales reactivos al sonido."
layout: homepage
lang: es
nav_enabled: false
nav_exclude: true
---
<section class="hero" aria-labelledby="home-title">
  <div class="hero-title-block">
    <h1 id="home-title">Visuales simples para DJs. Control ASCII profundo para VJs.</h1>
    <p class="release-status">Última versión: <strong>v{{ site.data.product.latest_release.version }}</strong></p>
  </div>
  <aside class="demo-frame demo-frame--video" aria-label="Preview de ASCII VJ Remix">
    {% assign hero_webm = '/assets/videos/ascii-hero.webm' %}
    {% assign hero_mp4 = '/assets/videos/ascii-hero.mp4' %}
    <video class="hero-video" width="1200" height="766" autoplay muted loop playsinline preload="metadata" fetchpriority="high" poster="{{ '/assets/images/ascii-demo.svg' | relative_url }}" aria-label="Preview de video ASCII en vivo de ASCII VJ Remix">
      <source src="{{ hero_webm | relative_url }}?v={{ hero_webm | asset_fingerprint }}" type="video/webm">
      <source src="{{ hero_mp4 | relative_url }}?v={{ hero_mp4 | asset_fingerprint }}" type="video/mp4">
      <img src="{{ '/assets/images/ascii-demo.svg' | relative_url }}" width="1200" height="766" alt="Preview visual de ASCII VJ Remix" decoding="async">
    </video>
  </aside>
</section>

<section class="hero-action-band" aria-label="Resumen y acciones de ASCII VJ Remix">
  <p class="hero-lede">ASCII VJ Remix convierte clips de video, cámaras y sonido en visuales ASCII en vivo. Los DJs pueden tener un visualizador limpio corriendo rápido. Los VJs pueden ajustar la imagen, empujar más fuerte los filtros y enviar la salida a una pantalla.</p>
  <div class="cta-row">
    {% include download-latest-button.html label="Descargar la última versión" %}
  </div>
</section>

<section class="section-band" aria-labelledby="product-heading">
  <p class="kicker">Producto</p>
  <h2 id="product-heading">Un visualizador que sí puedes manejar durante un set.</h2>
  <p class="section-intro">Empieza con la fuente que tienes, elige un look que le quede al cuarto y mantén los controles cerca para ajustar mientras la música se mueve.</p>
  <div class="card-grid">
    <article class="card pink">
      <h3>Para DJs</h3>
      <p>Corre una capa visual simple sin armar un rig completo de VJ. Carga un clip, usa una cámara o deja que el audio mueva la imagen para que la pantalla se sienta viva.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix/releases/latest">Descargar la app</a>
    </article>
    <article class="card">
      <h3>Para VJs</h3>
      <p>Moldea la imagen con control sobre densidad, filas, tamaño de celda, brillo, contraste, color, jitter, estilo de glyph y respuesta al movimiento.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix">Ver el proyecto</a>
    </article>
    <article class="card pink">
      <h3>Para salida en vivo</h3>
      <p>Mantén la superficie de control separada del visual proyectado. Saca la salida a otra ventana, ponla en fullscreen y sigue ajustando sin mostrar los controles.</p>
      <a href="{{ '/es/support/' | relative_url }}">Apoyar el proyecto</a>
    </article>
  </div>
</section>

<section class="section-band" aria-labelledby="capabilities-heading">
  <p class="kicker">Capacidades</p>
  <h2 id="capabilities-heading">Rápido cuando lo necesitas. Detallado cuando lo quieres.</h2>
  <div class="stack-list">
    <article class="card"><h3>Video y cámara</h3><p>Usa clips o cámaras en vivo como material base y conviértelos en visuales ASCII, de celda, pixel y glyph.</p></article>
    <article class="card"><h3>Movimiento reactivo al sonido</h3><p>Deja que ritmo, brillo, densidad y bandas de frecuencia muevan la imagen para que los visuales respondan al set.</p></article>
    <article class="card"><h3>Rango de presets</h3><p>Muévete rápido entre ASCII limpio, patrones densos, looks sólidos/pixel, modos de alto jitter y tratamientos cargados de color.</p></article>
    <article class="card"><h3>Control fino</h3><p>Ajusta el filtro hasta que le quede al track, al cuarto y a la pantalla: desde textura ASCII legible hasta salida abstracta agresiva.</p></article>
  </div>
</section>

<section class="section-band" aria-labelledby="release-heading">
  <p class="kicker">Última versión</p>
  <h2 id="release-heading">Qué cambió en v{{ site.data.product.latest_release.version }}.</h2>
  <p class="section-intro">La versión actual mantiene accesibles las preferencias de informes de fallos, simplifica la barra superior y amplía las comprobaciones de la interfaz empaquetada.</p>
  <div class="card-grid">
    <article class="card pink"><h3>Informes siempre accesibles</h3><p>El control Informes permanece visible aunque la cola esté vacía, para que puedas revisar Preguntar, Siempre o Desactivado antes de que ocurra un fallo.</p></article>
    <article class="card"><h3>Un solo control de backend</h3><p>Se eliminó la lectura duplicada del lado derecho. El selector central sigue siendo el único lugar para elegir y detener el renderizador.</p></article>
    <article class="card pink"><h3>Mejores comprobaciones de interfaz</h3><p>Las apps empaquetadas para macOS, Windows y Linux deben conservar Actualizar e Informes y no mostrar la lectura duplicada del backend.</p></article>
  </div>
  <p class="section-intro"><strong>¿Ya usas v0.9.6 o v0.9.7 en macOS?</strong> Instala la versión actual una vez desde el DMG notarizado; esas dos versiones no pueden mostrar la actualización dentro de la app. Los usuarios de v0.9.8 pueden actualizar dentro de la app.</p>
  <p class="release-link"><a href="{{ '/es/docs/overview/changelog-baseline/' | relative_url }}">Leer la base de la versión v{{ site.data.product.latest_release.version }}</a></p>
</section>

<section class="section-band" aria-labelledby="workflow-heading">
  <p class="kicker">Flujo</p>
  <h2 id="workflow-heading">Tres movimientos: fuente, look, salida.</h2>
  <div class="card-grid">
    <article class="card"><h3>Elige la fuente</h3><p>Trae video, cámara o sonido. Empieza rápido en vez de perder los primeros diez minutos conectando piezas.</p></article>
    <article class="card"><h3>Ajusta el filtro</h3><p>Elige un preset y ajusta el carácter visual hasta que funcione para el track, el venue o la superficie de proyección.</p></article>
    <article class="card"><h3>Mándalo en vivo</h3><p>Pon la salida en la pantalla, mantén los controles cerca y sigue moldeando el visual mientras el set avanza.</p></article>
  </div>
</section>
