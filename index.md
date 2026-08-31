---
title: ASCII VJ Remix
description: "ASCII VJ Remix is a desktop visualizer for DJs and VJs who want live ASCII video, camera, and audio-reactive visuals."
layout: homepage
nav_enabled: false
nav_exclude: true
---
<section class="hero" aria-labelledby="home-title">
  <div class="hero-title-block">
    <h1 id="home-title">Simple visuals for DJs. Deep ASCII control for VJs.</h1>
    <p class="release-status">Latest release: <strong>v{{ site.data.product.latest_release.version }}</strong></p>
  </div>
  <aside class="demo-frame demo-frame--video" aria-label="ASCII VJ Remix product preview">
    {% assign hero_webm = '/assets/videos/ascii-hero.webm' %}
    {% assign hero_mp4 = '/assets/videos/ascii-hero.mp4' %}
    <video class="hero-video" width="1200" height="766" autoplay muted loop playsinline preload="metadata" fetchpriority="high" poster="{{ '/assets/images/ascii-demo.svg' | relative_url }}" aria-label="ASCII VJ Remix live ASCII video preview">
      <source src="{{ hero_webm | relative_url }}?v={{ hero_webm | asset_fingerprint }}" type="video/webm">
      <source src="{{ hero_mp4 | relative_url }}?v={{ hero_mp4 | asset_fingerprint }}" type="video/mp4">
      <img src="{{ '/assets/images/ascii-demo.svg' | relative_url }}" width="1200" height="766" alt="ASCII VJ Remix preview graphic" decoding="async">
    </video>
  </aside>
</section>

<section class="hero-action-band" aria-label="ASCII VJ Remix summary and actions">
  <p class="hero-lede">ASCII VJ Remix turns video clips, cameras, and sound into live ASCII visuals. DJs can get a clean visualizer running fast. VJs can fine-tune the image, push the filters harder, and send the output to a screen.</p>
  <div class="cta-row">
    {% include download-latest-button.html label="Download latest" %}
  </div>
</section>

<section class="section-band" aria-labelledby="product-heading">
  <p class="kicker">Product</p>
  <h2 id="product-heading">A visualizer you can actually manage during a set.</h2>
  <p class="section-intro">Start with the source you have, pick a look that fits the room, and keep the controls close enough to adjust while the music is moving.</p>
  <div class="card-grid">
    <article class="card pink">
      <h3>For DJs</h3>
      <p>Run a simple visual layer without building a full VJ rig. Load a clip, use a camera, or let audio drive the motion so the room has something alive on screen.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix/releases/latest">Get the app</a>
    </article>
    <article class="card">
      <h3>For VJs</h3>
      <p>Shape the image with control over density, rows, cell size, brightness, contrast, color behavior, jitter, glyph style, and motion response.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix">View the project</a>
    </article>
    <article class="card pink">
      <h3>For live output</h3>
      <p>Keep the control surface separate from the projected visual. Pop the output out, fullscreen it, and keep tuning without exposing the controls.</p>
      <a href="{{ '/support/' | relative_url }}">Support the project</a>
    </article>
  </div>
</section>

<section class="section-band" aria-labelledby="capabilities-heading">
  <p class="kicker">Capabilities</p>
  <h2 id="capabilities-heading">Fast when you need it. Detailed when you want it.</h2>
  <div class="stack-list">
    <article class="card"><h3>Video and camera input</h3><p>Use clips or live camera sources as raw material, then turn them into ASCII, cell, pixel, and glyph-based visuals.</p></article>
    <article class="card"><h3>Sound-reactive motion</h3><p>Let rhythm, brightness, density, and frequency bands move the image so the visuals respond to the set instead of sitting still.</p></article>
    <article class="card"><h3>Palette, dither, and glyph control</h3><p>Combine 16 built-in palettes with Bayer dithering, glyph depth and color controls, multilingual character sets, and custom Unicode ramps.</p></article>
    <article class="card"><h3>Performance-aware density</h3><p>Stay inside shared renderer guardrails by default, or explicitly enable Advanced Density for grids up to 900 columns without a 30 FPS guarantee.</p></article>
  </div>
</section>

<section class="section-band" aria-labelledby="release-heading">
  <p class="kicker">Latest release</p>
  <h2 id="release-heading">What changed in v{{ site.data.product.latest_release.version }}.</h2>
  <div class="release-summary">
    <img class="release-app-icon" src="{{ site.data.product.app_icon.path | relative_url }}?v={{ site.data.product.app_icon.path | asset_fingerprint }}" width="512" height="512" alt="ASCII VJ Remix neon play-and-pixel app icon" loading="lazy" decoding="async">
    <div>
      <p class="section-intro">v{{ site.data.product.latest_release.version }} is the first stable desktop release. It makes presets faster to find, restores the same acceleration-first renderer policy across macOS, Windows, and Linux, and brings built-in video and native Pop Out behavior into closer cross-platform parity.</p>
      <p class="section-intro"><strong>One renderer contract.</strong> All 69 built-in presets must remain visible: 41 are acceleration-eligible and 28 intentionally use Canvas2D. Capable systems try WebGPU first, with WebGL2 and Canvas2D kept as real fallbacks.</p>
    </div>
  </div>
  <div class="card-grid">
    <article class="card pink"><h3>Find a look mid-set</h3><p>Start clean with Classic Camera ASCII, search presets by name, and move through separate alphabetical Built-in and My Presets sections without losing the active source.</p></article>
    <article class="card"><h3>Video that keeps moving</h3><p>The built-in demo uses a host-appropriate video format, and bundled or selected videos can retry through the included FFmpeg path when the system decoder cannot play them.</p></article>
    <article class="card pink"><h3>Pop Out stays in step</h3><p>The main preview and native output now share transition timing, advance video playback together, and use a browser-parity surface format to keep colors aligned.</p></article>
  </div>
  <p class="section-intro"><strong>Already on macOS v0.9.6 or v0.9.7?</strong> Install v{{ site.data.product.latest_release.version }} once from the notarized DMG; those two versions cannot surface the in-app update. v0.9.8 and newer can update in the app.</p>
  <p class="release-link"><a href="{{ '/docs/overview/changelog-baseline/' | relative_url }}">Read the v{{ site.data.product.latest_release.version }} release baseline</a></p>
</section>

<section class="section-band" aria-labelledby="workflow-heading">
  <p class="kicker">Workflow</p>
  <h2 id="workflow-heading">Three moves: source, look, output.</h2>
  <div class="card-grid">
    <article class="card"><h3>Choose the source</h3><p>Bring in video, camera, or sound. Start fast instead of spending the first ten minutes wiring things together.</p></article>
    <article class="card"><h3>Dial the filter</h3><p>Pick a preset and adjust the visual character until it feels right for the track, venue, or projection surface.</p></article>
    <article class="card"><h3>Send it live</h3><p>Put the output on the screen, keep your controls nearby, and keep shaping the visual while the set keeps moving.</p></article>
  </div>
</section>
