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
    <article class="card"><h3>Control de paleta, dithering y glifos</h3><p>Combina 16 paletas integradas con dithering Bayer, controles de profundidad y color de glifos, conjuntos multilingües y rampas Unicode personalizadas.</p></article>
    <article class="card"><h3>Densidad consciente del rendimiento</h3><p>Mantente dentro de los límites compartidos del renderizador o activa Densidad avanzada para usar hasta 900 columnas sin garantía de 30 FPS.</p></article>
  </div>
</section>

<section class="section-band" aria-labelledby="release-heading">
  <p class="kicker">Última versión</p>
  <h2 id="release-heading">Qué cambió en v{{ site.data.product.latest_release.version }}.</h2>
  <div class="release-summary">
    <img class="release-app-icon" src="{{ site.data.product.app_icon.path | relative_url }}?v={{ site.data.product.app_icon.path | asset_fingerprint }}" width="512" height="512" alt="Icono de la app ASCII VJ Remix con símbolo de reproducción y píxeles de neón" loading="lazy" decoding="async">
    <div>
      <p class="section-intro">v0.9.12 restaura una salida primaria visible y con proporciones correctas para todos los presets integrados. También incluye las paletas, el dithering, los glifos multilingües y los controles de densidad de v0.9.11, además del icono aprobado de v0.9.10.</p>
      <p class="section-intro"><strong>Un solo icono canónico.</strong> Los recursos para macOS, Windows, Linux, iOS, Android y marketing ahora parten del mismo diseño aprobado de reproducción y píxeles de neón.</p>
    </div>
  </div>
  <div class="card-grid">
    <article class="card pink"><h3>Todos los presets visibles</h3><p>v0.9.12 corrige lienzos primarios de glifos en blanco, conserva las proporciones de la fuente y prueba los 69 presets integrados de Imagen de demostración en la app empaquetada con Apple WebKit.</p></article>
    <article class="card"><h3>16 paletas y dithering ordenado</h3><p>Usa paletas propias del proyecto, mapeo por cercanía o luminancia y dithering Bayer 2x2, 4x4 u 8x8 en Canvas, WebGL2, WebGPU y Pop Out nativo.</p></article>
    <article class="card pink"><h3>Rango de glifos multilingüe</h3><p>Ajusta profundidad, desplazamiento, dirección, colores, Braille, símbolos, CJK, Hiragana, Katakana, Hangul o una rampa personalizada de hasta 96 escalares Unicode compatibles.</p></article>
  </div>
  <p class="section-intro"><strong>¿Ya usas v0.9.6 o v0.9.7 en macOS?</strong> Instala la versión actual una vez desde el DMG notarizado; esas dos versiones no pueden mostrar la actualización dentro de la app. v0.9.8 y versiones posteriores pueden actualizarse dentro de la app.</p>
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
