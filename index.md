---
title: ASCII VJ Remix
description: "ASCII VJ Remix turns video, cameras and sound into live ASCII visuals, with native NDI and macOS Syphon sharing. Version 1.3.1 adds a TLS security fix."
layout: homepage
nav_enabled: false
nav_exclude: true
---
<section class="hero" aria-labelledby="home-title">
  <div class="hero-title-block">
    <h1 id="home-title">Simple visuals for DJs. Deep ASCII control for VJs.</h1>
    <p class="release-status">Latest release: <a href="#release-heading"><strong>v{{ site.data.product.latest_release.version }}</strong> · Security update</a></p>
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
  <p class="section-intro">macOS Apple Silicon · Windows x64 preview · Linux x86_64</p>
</section>

<section class="section-band" aria-labelledby="product-heading">
  <p class="kicker">Product</p>
  <h2 id="product-heading">A visualizer you can actually manage during a set.</h2>
  <p class="section-intro">Start with the source you have, pick a look that fits the room, and keep the controls close enough to adjust while the music is moving.</p>
  <div class="card-grid">
    <article class="card pink">
      <h3>For DJs</h3>
      <p>Run a simple visual layer without building a full VJ rig. Load a clip, use a camera, or let audio drive the motion so the room has something alive on screen.</p>
      <a href="https://github.com/aindaco1/ascii-vj-remix/releases/tag/v{{ site.data.product.latest_release.version }}">Get the app</a>
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
    <article class="card"><h3>Palette, dither, and glyph control</h3><p>Combine 21 built-in palettes with Bayer dithering, glyph depth and color controls, multilingual character sets, and custom Unicode ramps.</p></article>
    <article class="card"><h3>From bold blocks to fine detail</h3><p>Adjust cell size and spacing, or enable Advanced Density for grids up to 900 columns.</p></article>
    <article class="card"><h3>Preset playlists</h3><p>Save a sequence of looks, reorder it, and loop it in order or at random. Set a shared hold interval and let the presets crossfade while your source keeps playing.</p></article>
    <article class="card"><h3>Save a frame</h3><p>Capture the current visual as a PNG straight to your Desktop, with the Stats Overlay left out of the image.</p></article>
  </div>
</section>

<section class="section-band" aria-labelledby="release-heading">
  <p class="kicker">Latest release</p>
  <h2 id="release-heading">v{{ site.data.product.latest_release.version }}: Security update.</h2>
  <p class="section-intro">Version 1.3.1 strengthens certificate checks for HTTPS connections by rejecting compromised eMudhra certificate chains. It includes the native video sharing and visual controls introduced in earlier releases.</p>
  <p class="release-link"><a href="{{ '/docs/overview/changelog-baseline/' | relative_url }}">See what’s new in v{{ site.data.product.latest_release.version }}</a></p>
</section>

<section class="section-band" aria-labelledby="native-video-heading">
  <p class="kicker">Native video sharing</p>
  <h2 id="native-video-heading">Bring a live feed into your ASCII set.</h2>
  <p class="section-intro">Share the finished visuals with other apps or receivers. Introduced in 1.3.0, <a href="https://ndi.video/">NDI®</a> input and output run on macOS Apple Silicon, Windows x64 and Linux x86_64, with Syphon on macOS.</p>
  <div class="card-grid">
    <article class="card pink"><h3>Mix a live feed</h3><p>Choose one NDI or Syphon sender in Video I/O, then keep it running through presets, WTF and your usual visual controls. NDI uses your local network; Syphon connects apps on the same Mac.</p></article>
    <article class="card"><h3>Share while you project</h3><p>Send your finished video through NDI or Syphon while Pop Out fills another screen. Choose 720p or 1080p at 30 or 60 fps.</p></article>
    <article class="card pink"><h3>Keep transparency in the mix</h3><p>Carry source transparency into your next app for overlays and layered visuals. Opaque black stays opaque.</p></article>
  </div>
  <p class="release-link"><a href="{{ '/docs/overview/features/#native-video-sharing' | relative_url }}">Native video sharing guide</a></p>
  <p class="section-intro">NDI® is a registered trademark of Vizrt NDI AB.</p>
</section>

<section class="section-band" aria-labelledby="looks-heading">
  <p class="kicker">Built-in looks</p>
  <h2 id="looks-heading">Find your look.</h2>
  <div class="release-summary">
    <img class="release-app-icon" src="{{ site.data.product.app_icon.path | relative_url }}?v={{ site.data.product.app_icon.path | asset_fingerprint }}" width="512" height="512" alt="ASCII VJ Remix neon play-and-pixel app icon" loading="lazy" decoding="async">
    <div>
      <p class="section-intro">Explore classic terminal ASCII, bold pixel treatments, vivid color cycles and textured glyphs, then take your visuals into spatial scenes.</p>
      <p class="section-intro"><strong>96 built-in presets, 21 palettes.</strong> Each look is a starting point for your own mix of color, texture and motion.</p>
    </div>
  </div>
  <div class="card-grid">
    <article class="card pink"><h3>Pick a starting point</h3><p>Search the preset library by name and switch looks while your video or camera keeps running.</p></article>
    <article class="card"><h3>Shape every detail</h3><p>Mix palettes, character sets, dithering, cell shapes and motion. Save your own presets and bring them into the next set.</p></article>
    <article class="card pink"><h3>Keep it moving</h3><p>Build a playlist of favorites or let WTF generate a changing sequence of looks with smooth transitions.</p></article>
  </div>
  <p class="release-link"><a href="{{ '/docs/overview/features/' | relative_url }}">Explore the visual controls</a></p>
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
