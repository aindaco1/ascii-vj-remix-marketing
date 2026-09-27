---
title: "Feature Set"
description: "Source-derived Feature Set documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 2
parent: "Overview"
---

# Feature Set

This page describes the current ASCII VJ Remix feature baseline for developers planning forks, ports, integrations, or feature work. The capability map is generated from the mother repository's User Guide.

## Current Capabilities

### Sources

- Built-in Demo Image, used as the default startup source.
- Built-in H.264/MP4 Demo Video on macOS and Windows, with a matching VP8/WebM
  asset selected on clean Linux installations.
- User-selected local image and video files.
- MKV selection support in the desktop file picker. If the platform webview
  cannot decode the built-in demo or a selected video, the desktop app retries
  it through the bundled FFmpeg path.
- Local webcam/camera input.
- Multiple simultaneous cameras when the operating system and desktop runtime
  allow it.
- Camera mixer layouts: grid, split row, stack, and picture-in-picture.
- Camera controls appear directly under the Source panel while Camera is active.
- Static media and camera frames stay local. They are not uploaded to a server.

### Rendering

- WebGPU renderer is the primary quality target on capable desktop runtimes.
- WebGL2 renderer is the main embedded GPU fallback.
- Canvas2D and pixel Canvas paths remain compatibility fallbacks.
- Packaged desktop views attempt WebGPU for every acceleration-eligible preset,
  then WebGL2 and Canvas2D as bounded fallbacks. Presets with an explicit
  compatibility backend retain Canvas2D on every platform.
- Native Tauri output window uses a `wgpu` presenter where available:
  - Metal on macOS.
  - D3D12 on Windows.
  - Vulkan/GLES on Linux.
- Native Pop Out preserves glyph-mode and character-set params for traditional
  ASCII presets instead of flattening them into solid cells.
- Twenty-one project-native palettes, nearest-color/luminance mapping, and ordered
  Bayer 2x2/4x4/8x8 dithering share one parameter and lookup-table contract
  across browser, Canvas, and native output paths.
- Glyph controls cover depth, offset, reverse, source/fixed color, background,
  Braille, common drawing/symbol blocks, Latin Extended, Greek, Cyrillic, CJK
  marks, Hiragana, Katakana, CJK Unified U+4E00-U+9FFF, Hangul, and custom typed
  ramps of up to 96 supported Unicode scalars.
- The neutral Unicode atlas is generated and verified offline, bundled locally,
  and loaded in bounded 1024px pages only as selected glyphs need them.
- Normal density is performance-guarded by shared column and total-cell limits.
  The global Advanced Density preference exposes up to 900 columns without a
  30 FPS guarantee and is never stored in visual presets.
- The renderer skips duplicate native source-frame uploads, reuses stable GPU
  resources, and bounds transition-time UI work without changing renderer math
  or quality settings.
- The renderer exposes live controls for grid, cell size, color, gamma,
  brightness, contrast, saturation, background blend, quantization, jitter,
  sample position, smoothing, FPS, glyph/cell behavior, and performance status.
- Stats overlay is enabled by default and remains user-controlled.

### Presets and Live Controls

- Built-in read-only visual presets, including extreme looks such as Neon
  Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder,
  Cyberdelic Riot, Acid Snowstorm, Terminal Collapse, and Neon Razorstorm.
- Built-in traditional ASCII presets, including Classic Camera ASCII, ANSI
  Newsprint, Terminal Mono, and Dense Typewriter.
- ASCII World Mint applies gently jittering mint line-character glyphs on a dark
  teal background to the selected image, video, or camera, inspired by
  [yeahpython's ASCII World](https://yeahpython.github.io/game/game.html).
- ASCII City Nightshift uses a near-black background, amber and sage lighting,
  and jittering dense terminal characters, inspired by
  [tweakyourpc's ASCII City](https://tweakyourpc.github.io/ascii-city/).
  Both presets animate still images even with audio reactivity off.
- Classic Camera ASCII is the default for a clean profile. Existing persisted
  profiles keep their visual settings instead of being silently reset. The
  clean-profile visual choice does not override the global Auto renderer
  preference; presets without an explicit compatibility backend use
  WebGPU/WebGL2 when the runtime supports them.
- Twenty-three read-only character presets adapted from
  [ascii.today](https://ascii.today/), including Broadway KB, Computer, Doom,
  Ghost, Modular, Standard, Univers, and Doh. The complete credited pack is in
  [ascii.today Character Presets](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ASCII_TODAY_PRESETS.md).
- Built-in and My Presets are shown as separate, independently alphabetized
  sections with a live name search. The prior Point & Click Default display
  name is now the more descriptive Dense Color ASCII; its stable preset id is
  unchanged.
- Character Set, Font Family, Palette, and other selects share the same control
  geometry so traditional ASCII tuning stays aligned in the dense sidebar.
- Palette, mapping, ordered-dither, glyph-ramp, and glyph-color controls are
  independently tunable and saved through the existing visual-preset schema.
- Eleven built-in palette/glyph variants include ASCII City Nightshift, Braille,
  box drawing, CJK marks, Hiragana, Katakana, CJK Unified, and Hangul looks. The
  six additional non-cycling palettes are incorporated into existing presets.
  The four cycling palettes are covered below.
- User presets can be saved, duplicated, updated, deleted, imported, and
  exported.
- Multiple named preset playlists can be saved with reordered stable preset
  entries, one shared hold interval, and random or in-order looping. Playlist
  playback uses the existing Default Transition control, bounded to 1–5 seconds.
- Preset transitions crossfade instead of fading to black.
- Transition time is configurable.
- Presets preserve the active media source unless the user explicitly changes
  it.
- WTF mode continuously transitions through randomized live-safe settings and
  leans into both extreme and traditional ASCII preset families while avoiding
  pure white or pure black output.

### Pixel Art and Color Cycling

Eight original presets pair solid pixels and glyphs in four palettes: Tidal
Glass, Ember Grotto, Fern After Rain, and Violet Dusk. They transform the active
camera, video, or image and preserve its playback. Search a family name in Presets.

In the Color panel, choose a cycling palette and set **Color cycling** to
Classic (stepped) or Blend (smooth). **Cycle speed** runs from −4× to 4×;
zero freezes the current phase and negative values reverse it. **Cycle amount**
blends the moving colors with the fixed palette. Start/Stop pauses and resumes
cycling. Fixed shadows/highlights and glyph shapes remain stable while the
selected color ranges move. Older presets default to cycling Off.

These original looks are inspired by [Mark Ferrari](https://www.markferrari.com/image-archives),
[Living Worlds](https://www.effectgames.com/demos/worlds/), and the
[Amiga color-cycling examples](https://amiga.lychesis.net/specials/ColorCycling.html).
They do not include those artists' images or authored scene animations.

### Audio Reactivity

- Audio reactivity is on by default.
- Mic/input is the default audio-reactive source.
- Local audio files can drive visual modulation.
- System/display audio is supported where the operating system provides an
  audio track to the desktop app.
- Tauri desktop builds include native audio capture paths for system/input
  audio features.
- Audio analysis tracks RMS, bass, low-mid, mid, high-mid, treble, presence,
  brightness, density, transient energy, beat pulse, and spectral movement.
- Dense-mix dampening and noise-floor controls help busy songs stay reactive
  without pinning jitter and beat response at maximum.
- Audio modulation is non-persistent: it affects live effective render params
  without rewriting saved presets.
- Safe clamps prevent high sensitivity from driving the renderer into pure
  white or pure black screens.

### Pop Out and External Displays

- Pop Out creates a separate output window intended for a projector, capture
  card, or secondary display.
- The main control window remains visible and interactive.
- The desktop output window is native, not a second heavyweight duplicated UI
  surface.
- Output display selection is persisted when Tauri can enumerate displays.
- Single-camera output uses platform-native capture: AVFoundation on macOS,
  Media Foundation on Windows, and V4L2 through the bundled local FFmpeg
  runtime on Linux. Windows/Linux frames feed the native `wgpu` presenter;
  bounded current-frame mirroring remains available when native device opening
  fails or multiple cameras are selected.
- The camera-icon control saves the current primary renderer surface as a PNG
  directly to Desktop. The HTML Stats Overlay is outside that captured surface,
  and no save dialog is opened.

### Experimental MIDI Control

- Experimental native DIN MIDI control for an Evolution/M-Audio UC-33e
  connected through an iConnectivity mioXC.
- Four hardware pages for Visual, Audio, Presets, and Fine/User control, with
  all 9 faders, 24 rotary controllers, and 14 assignable buttons mapped.
- Numeric visual-preset slots from 1 through 128 with Enter, Previous, and Next.
- Soft takeover is enabled by default to prevent jumps after software preset
  changes.
- MIDI Learn overrides, connection monitoring, and automatic mioXC reconnection.
- Bounded full-bank SysEx capture, explicit Install/Restore, verification, and
  optional Ensure Profile on Connection.
- MIDI is restricted to visual parameters, audio-reactive settings, visual
  presets, and WTF mode. It cannot change media sources, Camera, Pop Out, or
  output displays.
- Current physical hardware validation covers macOS Apple Silicon with the
  UC-33e connected by DIN through a mioXC. Direct UC-33e USB is not supported,
  and Windows/Linux physical validation is not complete.

MIDI remains experimental. Automated mapping, safety, native transport, and
bounded SysEx tests pass. Ensure Profile on Connection stays disabled by default
and requires a manually captured and verified hardware profile.

### Desktop Packaging and Updates

- Built with Tauri v2.
- Production runtime is local-only by default.
- The packaged app blocks arbitrary remote HTTP(S) connections through a
  production Content Security Policy.
- The app uses narrow Tauri capabilities split by window:
  - The main control window can open selected media and manage output.
  - The output window has a minimal command surface.
- The production app checks GitHub Releases metadata for signed updater packages once
  in the background whenever the production app opens. A current or offline
  check is silent; when a newer release exists, the top-bar Update control shows
  it. If upgrading from 0.9.6 or 0.9.7, see the
  [legacy updater recovery notes](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md#upgrading-from-096-or-097).
- The same Update control remains available for a manual recheck. Downloading,
  installation, and relaunch remain explicitly user initiated.
- The Reports control remains visible when no crash reports are pending so the
  `ask`, `always`, and `off` preference is always reachable. A pending count and
  warning state appear only after a bounded, sanitized report is captured.
  The same dialog can capture a manual current-state diagnostic with an optional
  problem description; it uses the existing bounded report schema and queue,
  not arbitrary application logs.
  Development bundles retain reports locally for review and keep Send disabled;
  only a release-mode build with the production bundle identifier may submit.
  Legacy unavailable-microphone reports are removed from the queue because a
  disconnected or absent input device is a normal hardware state.
- Public macOS artifacts are Developer ID signed, notarized, stapled, and
  Gatekeeper-validated. Current Windows artifacts are unsigned previews.
- Normal development commands use the visibly separate `ASCII VJ Remix Dev`
  app and `com.asciline.remix.dev` bundle identifier. Development builds cannot
  replace or inherit privacy grants from the production app.
- Intentional online paths are limited to the updater check/download flow and
  production-only reviewed/sanitized crash report submission.
- Crash report submission goes through the Rust desktop layer to the
  `https://crash.dustwave.xyz` Cloudflare Worker relay. The webview does not get
  arbitrary HTTP capability and selected media is never uploaded. Renderer
  failures may attach a bounded, sanitized event summary with preset/backend
  state; local media diagnostics and arbitrary logs are not attached.

### Advanced and Development-Only Paths

The legacy ASCILINE stream path and the Rust/FFmpeg stream-session code are
development infrastructure. Stream mode, the Static/Streaming selector, the
connection label, and the buffer counter are not exposed in the normal Source
UI.

The initial hardware setup and complete controller map live in
[UC-33e and mioXC guide](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/USER_GUIDE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md)
