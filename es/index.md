---
title: ASCII VJ Remix
description: "ASCII VJ Remix convierte video, cámaras y sonido en visuales ASCII en vivo. Video compartido con NDI y Syphon en macOS en 1.3.0."
layout: homepage
lang: es
nav_enabled: false
nav_exclude: true
---
<section class="hero" aria-labelledby="home-title">
  <div class="hero-title-block">
    <h1 id="home-title">Visuales simples para DJs. Control ASCII profundo para VJs.</h1>
    <p class="release-status">Última versión: <a href="#release-heading"><strong>v{{ site.data.product.latest_release.version }}</strong> · Entrada y salida de video nativo</a></p>
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
  <p class="section-intro">macOS Apple Silicon · Windows x64 en versión preliminar · Linux x86_64</p>
</section>

<section class="section-band" aria-labelledby="product-heading">
  <p class="kicker">Producto</p>
  <h2 id="product-heading">Un visualizador que sí puedes manejar durante un set.</h2>
  <p class="section-intro">Empieza con la fuente que tienes, elige un look que le quede al cuarto y mantén los controles cerca para ajustar mientras la música se mueve.</p>
  <div class="card-grid">
    <article class="card pink">
      <h3>Para DJs</h3>
      <p>Corre una capa visual simple sin armar un rig completo de VJ. Carga un clip, usa una cámara o deja que el audio mueva la imagen para que la pantalla se sienta viva.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix/releases/tag/v{{ site.data.product.latest_release.version }}">Descargar la app</a>
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
    <article class="card"><h3>Control de paleta, dithering y glifos</h3><p>Combina 21 paletas integradas con dithering Bayer, controles de profundidad y color de glifos, conjuntos multilingües y rampas Unicode personalizadas.</p></article>
    <article class="card"><h3>De bloques grandes a detalles finos</h3><p>Ajusta el tamaño y la separación de las celdas o activa Advanced Density para usar hasta 900 columnas.</p></article>
    <article class="card"><h3>Listas de presets</h3><p>Guarda una secuencia de looks, cambia su orden y repítela en orden o al azar. Define cuánto dura cada preset y deja que las transiciones avancen mientras tu fuente sigue reproduciéndose.</p></article>
    <article class="card"><h3>Guarda un fotograma</h3><p>Captura el visual actual como PNG directamente en tu Escritorio, sin incluir la superposición de estadísticas.</p></article>
  </div>
</section>

<section class="section-band" aria-labelledby="release-heading">
  <p class="kicker">Última versión</p>
  <h2 id="release-heading">v{{ site.data.product.latest_release.version }}: entrada y salida de video nativo.</h2>
  <p class="section-intro">Incorpora una señal en vivo a tu set ASCII y comparte los visuales con otras apps o receptores. La versión 1.3.0 añade entrada y salida <a href="https://ndi.video/">NDI®</a> en macOS Apple Silicon, Windows x64 y Linux x86_64, además de Syphon en macOS.</p>
  <div class="card-grid">
    <article class="card pink"><h3>Mezcla una señal en vivo</h3><p>Elige un emisor NDI o Syphon en Video I/O y conserva la señal al cambiar de preset, usar WTF o ajustar los controles visuales. NDI usa tu red local; Syphon conecta apps en la misma Mac.</p></article>
    <article class="card"><h3>Comparte mientras proyectas</h3><p>Envía el video terminado por NDI o Syphon mientras Pop Out llena otra pantalla. Elige 720p o 1080p a 30 o 60 fps.</p></article>
    <article class="card pink"><h3>Conserva la transparencia al mezclar</h3><p>Conserva la transparencia de la fuente al pasar a otra app para superponer y combinar visuales. El negro opaco sigue siendo opaco.</p></article>
  </div>
  <p class="release-link"><a href="{{ '/es/docs/overview/changelog-baseline/#130-release-notes' | relative_url }}">Ver las novedades de v{{ site.data.product.latest_release.version }}</a> · <a href="{{ '/es/docs/overview/features/#native-video-sharing' | relative_url }}">Guía para compartir video nativo</a></p>
  <p class="section-intro">NDI® es una marca registrada de Vizrt NDI AB.</p>
</section>

<section class="section-band" aria-labelledby="looks-heading">
  <p class="kicker">Looks integrados</p>
  <h2 id="looks-heading">Encuentra tu look.</h2>
  <div class="release-summary">
    <img class="release-app-icon" src="{{ site.data.product.app_icon.path | relative_url }}?v={{ site.data.product.app_icon.path | asset_fingerprint }}" width="512" height="512" alt="Icono de la app ASCII VJ Remix con símbolo de reproducción y píxeles de neón" loading="lazy" decoding="async">
    <div>
      <p class="section-intro">Explora ASCII clásico de terminal, estilos de píxeles, ciclos de color y texturas de glifos, y lleva tus visuales a escenas espaciales.</p>
      <p class="section-intro"><strong>96 presets integrados, 21 paletas.</strong> Cada look es un punto de partida para tu propia mezcla de color, textura y movimiento.</p>
    </div>
  </div>
  <div class="card-grid">
    <article class="card pink"><h3>Elige un punto de partida</h3><p>Busca presets por nombre y cambia de look mientras tu video o cámara sigue funcionando.</p></article>
    <article class="card"><h3>Ajusta cada detalle</h3><p>Combina paletas, conjuntos de caracteres, dithering, formas de celda y movimiento. Guarda tus propios presets y llévalos al siguiente set.</p></article>
    <article class="card pink"><h3>Mantén el set en movimiento</h3><p>Arma una lista de favoritos o deja que WTF genere una secuencia de looks con transiciones suaves.</p></article>
  </div>
  <p class="release-link"><a href="{{ '/es/docs/overview/features/' | relative_url }}">Explora los controles visuales</a></p>
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
