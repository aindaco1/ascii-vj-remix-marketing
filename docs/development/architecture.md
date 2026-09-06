---
title: "Architecture"
description: "Source-derived Architecture documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 2
parent: "Development"
---

# Architecture

This page assembles the architecture contract from the mother repository's agent and rendering guides instead of maintaining a parallel ownership model here.

## Project Identity

ASCII VJ Remix is a local-first native desktop renderer lab for macOS, Windows,
and Linux. The intended product is the Tauri desktop app, not a hosted web app
or browser-only build.

The repository combines high-quality WebGPU/WebGL rendering, Canvas
compatibility paths, ASCILINE-derived stream and codec infrastructure, and
Tauri desktop packaging. The app is a creative control surface for live
ASCII/cell visuals.

## Architecture Properties

- WebGPU/WebGL output is the visual-quality target.
- ASCILINE-derived Canvas and adaptive-stream paths remain available as
  compatibility and development infrastructure.
- Normal app use is local-first and offline.
- All live controls route through one canonical parameter model.
- Presets, WTF mode, audio reactivity, and MIDI control compose without forking
  renderer state.
- Pop Out uses latest-frame native paths where available to minimize live-camera
  latency.
- Palette, ordered-dither, glyph, and density behavior is defined once in
  shared catalogs/math and implemented by each backend without parallel state.

## High-Level Data Flow

```text
Source selection
  -> source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

Source selection can come from built-in media, user-selected files, camera
streams, mixed cameras, or development stream sessions. The renderer runtime
chooses the best backend for the active source and environment.

## Parameter Model

The app maintains one canonical parameter object, commonly referred to in code
as `params`.

Major parameter groups:

- source: source mode, media URL/id, media type, source name.
- camera: selected device ids, resolution, FPS, layout, framing, mirror.
- backend: auto, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- grid: columns, rows, auto rows, cell width, cell height, aspect correction,
  global Advanced Density preference.
- color: saturation, contrast, brightness, gamma, background blend,
  quantization, palette id, palette mapping.
- dither: ordered matrix, strength, scale, bias, invert.
- sampling: FPS, jitter amount, jitter speed, sample X/Y, smoothing.
- glyph/cell: glyph mode, solid mode, character set, custom typed ramp, depth,
  offset, reverse, glyph-color mode/color, background color, neutral atlas
  style, font family metadata, minimum glyph intensity.
- stream: codec, quality, tolerance, buffer settings, frame timing.
- UI/performance: stats overlay, transition seconds.

The control surface, presets, persistence, source changes, WTF mode, audio
reactivity, native output, and MIDI all read from or write through this
model.

Static renderer-family transitions keep media ownership at the `StaticRuntime`
layer. Canvas2D, pixel Canvas, WebGL, and WebGPU renderers can crossfade over
the same live video/camera source instead of destroying and reloading media when
`solidMode`, `glyphMode`, `pixel`, or `backend` changes.

### Shared Renderer Math

Shared helpers reduce duplicated renderer math without changing the established
Canvas or stream output.

Shared JavaScript helpers live in:

```text
renderers/shared/character-sets.js
renderers/shared/density-policy.js
renderers/shared/glyph-atlas.js
renderers/shared/palettes.js
renderers/shared/render-math.js
renderers/shared/render-math-vectors.json
```

The shared module currently owns:

- GPU-style color processing used by software snapshots and native parity tests.
- Legacy Canvas color processing.
- Legacy stream color processing.
- shader-style jitter hash helpers.
- a bounded canonical character-set catalog, including credited ascii.today
  adaptations.
- complete approved Unicode coverage metadata and bounded custom-ramp
  validation.
- project-native palette ids/colors, a cached 32x32x32 palette lookup table,
  and immutable Bayer matrices.
- shared accelerated/software column and total-cell density limits.
- Unicode-scalar glyph ids, 1024px atlas page addressing, cached max-coverage
  browser mips, a four-page decoded cache, and lazy local page loading.
- compact charset and luminance-to-glyph helpers.

The Canvas and stream functions are intentionally named separately from the GPU
function. Their established quantization and background-blend behavior remains
distinct while shared vectors protect compatibility.

`npm run test:render-math` validates the JavaScript helpers against shared
vectors. Rust native output tests consume the same vector file for GPU color
processing parity.

### Effective Params

Some features affect live rendering without changing saved state.

Audio reactivity is the main example:

```text
base params
  + audio feature modulation
  -> effective params
  -> renderer.updateParams()
```

Effective params must not persist back into user presets unless the user
explicitly saves the current state as a preset.

## Repository Ownership Map

Use this map to find the likely owner of a change:

| Area | Primary Files |
| --- | --- |
| Main UI, params, presets, source controls, WTF, audio UI | [app.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/app.js), [index.html](https://github.com/aindaco1/ascii-vj-remix/blob/main/index.html), [style.css](https://github.com/aindaco1/ascii-vj-remix/blob/main/style.css) |
| GPU renderer and media source abstraction | [renderers/gpu/](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/gpu) |
| MIDI mapping, soft takeover, UC-33e profile | [midi-mapping.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/renderers/shared/midi-mapping.js), [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) |
| Tauri adapter and output-display helpers | [renderers/desktop/](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/desktop) |
| Tauri shell, commands, permissions, updater, native audio, native output | [src-tauri/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri) |
| Native MIDI input/output and SysEx | [midi.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/midi.rs) |
| Native Pop Out renderer | [native_output.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output.rs), [gpu.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/gpu.rs) |
| Platform-native camera paths | [native_camera.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs), [ffmpeg.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/media_engine/ffmpeg.rs) |
| Rust media engine, codec, FFmpeg sessions | [src-tauri/src/media_engine/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri/src/media_engine) |
| Built-in demo media and hidden fixtures | [media/](https://github.com/aindaco1/ascii-vj-remix/tree/main/media) |
| Codec/vector experiments | [experiments/](https://github.com/aindaco1/ascii-vj-remix/tree/main/experiments) |
| Build, smoke, release, Podman, FFmpeg scripts | [scripts/](https://github.com/aindaco1/ascii-vj-remix/tree/main/scripts) |
| User/developer docs | [docs/](https://github.com/aindaco1/ascii-vj-remix/tree/main/docs) and [README](/docs/overview/ascii-vj-remix/) |

## Non-Negotiable Constraints

- Runtime must be local-first and offline by default.
- Do not add CDN, hosted font, hosted decoder, telemetry, or online runtime
  dependencies.
- Intentional online runtime paths are limited to the production app's bounded
  release-metadata check for signed updater artifacts at launch, explicit
  updater download/install actions, and production-only reviewed/sanitized
  crash report submission.
- Preserve the app name: ASCII VJ Remix.
- Preserve the native app direction for macOS, Windows, and Linux.
- Do not reframe browser mode as the product. Browser/Vite paths are useful for
  development, smoke tests, and renderer portability.
- Keep renderer quality high. WebGPU/WebGL output is the visual quality target.
- Preserve fallback paths unless a replacement is implemented and tested.
- Treat Pop Out performance and latency as critical user-facing behavior.
- Keep user-selected local media local. Do not upload files or camera/audio data.
- Keep stats overlay user-owned. Random presets, WTF mode, and audio presets do
  not turn it off unless the user explicitly does.
- Stream infrastructure exists but is not a normal visible source mode. Keep
  its UI hidden; prospective productization belongs in the roadmap.
- Security, performance, accessibility, and i18n guidance live in dedicated
  practice docs under `docs/`; update them when architectural assumptions
  change.

## Behavior and Ownership Constraints

Use the [User Guide](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md) for current behavior and
[Rendering Engine](/docs/development/rendering-engine/) for the detailed contracts. When editing:

- Preserve the clean-profile Demo Image / Classic Camera ASCII state and keep
  backend preference on Auto. Existing profiles retain their settings.
- Keep preset backend ownership in
  `renderers/shared/preset-backend-contract.js` (71 total, 43 accelerated,
  28 explicit Canvas). Intentional changes must update the contract and visible
  preset-matrix evidence together. Platform identity must not preemptively
  reassign ownership.
- Keep one canonical parameter model. Saved presets, live effective params,
  source selection, transitions, WTF, audio, MIDI, and native output must agree.
  Preset transitions preserve source identity and playback.
- Extend shared palette, character-set, glyph-atlas, and grid policies. Keep
  Advanced Density global and out of presets; do not add per-renderer limits or
  runtime system-font lookup. Read the renderer guide before changing bounds.
- Reuse GPU resources and source-frame versions; do not reduce visual quality
  or resolution to obtain a performance improvement.
- Keep audio feature frames bounded and raw audio out of IPC and diagnostics.
  Preserve safe clamps and avoid rewriting saved presets during modulation.
- Keep UC-33e control on the documented mioXC DIN path. MIDI targets visual,
  audio, preset, and WTF behavior; it must not target source, Camera, Pop Out,
  output-display, file, updater, or report actions. Read [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md)
  before changing mapping or hardware policy.
- Preserve the dense black/white/grey UI with pink/blue state accents. Do not
  reduce control density or add explanatory marketing text inside the app.
- Keep Reports reachable with an empty queue. Renderer diagnostics follow the
  bounded [security contract](/docs/operations/security/#crash-reporting); do not attach local
  media diagnostics or arbitrary logs.
- Keep backend selection in the center control and resolved-backend diagnostics
  in the user-owned Stats Overlay, without a duplicate top-bar readout.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
