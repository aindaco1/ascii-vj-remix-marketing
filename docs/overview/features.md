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
- **Color → Bright output** is off by default. Enable it to lift dark footage; existing saved choices are retained. It strongly lifts dark colors
  before glyph selection, so low-light camera,
  image and video inputs produce brighter colors and denser glyphs. Your choice
  persists across launches, preset switches, playlists and WTF mode. Leave it
  off for the original color response; the Brightness and Gamma sliders still
  work. Pure black stays black. With a palette, the mapped colors are lifted
  while its lookup and cycling ranges stay intact; fixed glyph colors keep
  their chosen color.
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
- Editing a visual control during a preset transition stops the transition at
  the current look and keeps your edit. The interrupted look becomes Custom;
  the selected media keeps playing. MIDI visual controls follow the same rule.
- Presets preserve the active media source unless the user explicitly changes
  it.
- WTF mode continuously transitions through randomized live-safe settings and
  leans into both extreme and traditional ASCII preset families while avoiding
  pure white or pure black output. Each transition independently chooses Flat
  Media with 95% probability; the other 5% is shared equally among the ten
  spatial modes (0.5% each). This is a probability per transition, so runs can
  include consecutive flat or spatial looks. WTF checks dim footage, glyph coverage,
  fixed glyph colors, and active audio response before accepting a target. If no
  candidate or fallback is safe, it holds the current look and retries. Naturally
  black source frames remain valid. Bright Output stays under your control.

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
- Attacks follow each fresh audio reading immediately. Smoothing controls how
  quickly the response falls away; set it to zero for the sharpest response.
  Capture hardware and the display still contribute some delay.
- Dense-mix dampening and noise-floor controls help busy songs stay reactive
  without pinning jitter and beat response at maximum.
- Changing an audio slider labels the audio preset **Custom**. Selecting any
  audio preset, including the same one again, restores its slider tuning.
  The selected audio source, input device and visual look stay in place.
- Stop cancels pending capture startup as well as active reactivity. Audio
  control changes also take effect during Pop Out preset transitions.
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

## Spatial visuals and trails (1.1.0)

All built-in presets start with **Space / Motion → Visual mode → Flat media**,
including Ashen Ruins. They apply their color, glyph or solid-cell treatment
directly to your input. Ashen Ruins starts as a pale monochrome, solid-cell look.
The eleven new presets remain available; their camera and scene settings are
loaded but only take effect when you choose a spatial Visual mode manually.
Reselecting a built-in preset restores Flat Media. Saved custom presets retain
their chosen mode, and existing saved settings are not migrated.
Version 1.1.0 is available in [GitHub Releases](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.1.0)
and through the production in-app updater. See the
[release record](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md#published-artifacts-and-acceptance)
for installer/updater validation and remaining physical-platform checks.

| Preset | Optional Visual mode | Scene after opting in |
| --- | --- | --- |
| Neon Night Drive | City streets | Fast, low street weave, tall buildings, wet streets and rain |
| Media Corridor | Media corridor | Narrow, symmetric screen tunnel, wide lens and block glyphs |
| Wet Coast | Wet coast | Slow waterfront view, open water, short shoreline buildings and Braille texture |
| Neon Cathedral | Vaulted hall | Upward-looking nave with tall columns, a pitched roof and fine glyphs |
| Orbital Chamber | Orbitals | Media-colored sphere and rotating tilted ring |
| Ashen Ruins | Recursive ruins | Monochrome architecture, open passages and pale distance fog |
| Fractal Dive | Mandelbrot dive | Rotating Mandelbrot zoom with source-driven color and contour distortion |
| Mandelbulb Bloom | Mandelbulb | Orbiting organic fractal with Braille surface texture |
| Mandelbox Passage | Mandelbox | Recursive cube forms and folded architecture |
| Edge Etching | Flat media | Directional line glyphs on strong image edges |
| Phosphor Echo | Flat media | Decaying trails with gentle zoom and rotation |

**Travel speed** is signed: negative values reverse motion. **Freeze scene**
stops the scene clock and echo decay/motion; the selected video and audio keep
running. **Route position** adds an offset. **Reset scene / trails** returns
the camera clock and offset to their origin and clears stored trails. Forward
travel wraps through a repeating world; Street weave moves within the clear
road, and Look around / orbit rotates the travelling view or circles the orbital objects.
**Camera tilt** looks up or down; Relief uses an elevated camera above its terrain. These are constrained
camera routes, not free flight or an editable world.

**Media amount** blends the selected source into surfaces. The optional scene
recipes use 80–95% so your input drives their appearance. Zero uses procedural
materials. Wall images occupy larger 8×4-unit panels; roofs and ceilings also
use the source, and Orbital Chamber includes it behind the foreground shapes. **Surface framing** controls repeat, fit or crop within surface
tiles. The existing source picker, camera mirroring and playback controls still
own media. Previously saved/custom settings keep their values; reselect a
related preset and then enable its spatial Visual mode to load its scene recipe.
Changing a visual preset does not select a new source or restart it.

**Fractal zoom**, **Fractal detail** and **Fractal shape** appear when you enable one of the four fractal modes. Zoom changes scale; Detail changes the bounded iteration count; Shape changes carving, bulb power, box folding or media-driven contour distortion. Travel speed, freeze, camera controls and media blending remain live and editable. Ashen Ruins, Fractal Dive and Mandelbox Passage use solid cells; turn Glyph mode on and Solid mode off for ASCII texture. The removed Brightness Relief preset remains available as a visual mode for existing custom looks.

**Material glyphs** distinguishes surfaces, water, windows and sky. It reserves
eight of the 96 glyph slots. As Media amount rises, its glyph override fades
so the source brightness and shapes remain legible. Disable it and set Edge glyphs to zero to use the
entire custom ramp unchanged. Edge glyphs works on flat media and chooses
horizontal, vertical or diagonal strokes with hysteresis near its threshold.
Palette cycling continues to use stable base luminance for ordinary glyphs.

**Phosphor / echo**, **Trail half-life**, **Echo zoom** and **Echo rotation**
work on flat and spatial modes. Long trails can hide fine details. History is
cleared when Bright output, the source, grid, scene, seed, route offset, palette or glyph layout
changes, and when a render gap exceeds one second. Native structural crossfades
also clear history. Floating-point history prevents dim trails from getting
stuck; older WebGL2 devices without floating-point render attachments use a
faster-decaying byte fallback.

Existing audio settings add restrained bass movement to field of view and
camera height, presence to light, beat accents to glow and treble to wet
shimmer. These use the existing sensitivity, per-feature amounts and density
dampening. MIDI Learn includes the spatial sliders/selectors, Freeze Scene and
Reset Scene and Trails actions; it does not add source or camera actions.

Spatial controls apply to local image/video/camera rendering, including camera
composites. The legacy server-stream renderer keeps its existing behavior.
WebGPU, WebGL2 and native wgpu render locally. Explicit Canvas retains the
existing software density limit and uses the output mirror for spatial Pop Out.
If a native GPU presenter is unavailable, choose Canvas for that fallback.
Normal and Advanced density limits have not changed. Relief, orbitals, wet
reflections and dense scenes can require more GPU time; reduce Columns before
raising other limits. Physical M1/16 GB and Windows/Linux acceptance is still
pending for this release.

## Fractal Accents

The six new looks keep your selected media in Flat Media and add small fractal
textures. Selecting them preserves source playback and your global Subtle Limit.

| Preset | Accent |
| --- | --- |
| Threadlight | Fine orbit-trap threads along edges, with Braille texture |
| Silver Etching | Quiet monochrome contour engraving in midtones |
| Contour Silk | Soft angular bands across quieter solid-cell areas |
| Julia Glass | Small, edge-protected distortions in solid cells |
| Chromatic Undertow | Color currents with a tonal response in monochrome and glyph looks |
| Phosphor Lace | Fractal attenuation of short moving-source trails |

Open **Fractal Accents** to adjust **Fractal amount**, **Coverage**, **Placement**,
**Texture scale**, **Drift** and **Audio accent**. Amount controls intensity;
Coverage changes how much of the image receives it. Placement selects Edges,
Midtones, Quiet areas or Trails. Trails uses your Phosphor / echo settings,
or supplies a short echo when that control is zero; it is clearest with a moving
source. Select **Off**, or set Amount or Coverage to zero, to bypass the accent.
Accents work over every preset and optional spatial/fractal Visual mode. Their
color and glyph-density changes also show in fixed-color and monochrome looks.

Switching ordinary built-in presets keeps your current accent settings, including
Off. Selecting one of the six accent presets loads its recipe. Saved custom
presets restore their own accent settings.

WTF independently adds an accent to 65% of its targets, choosing among all six
recipes and varying amount, coverage, scale, drift, audio response and variation.
The remaining 35% switch accents off. This works with both flat and scene targets;
WTF preserves your global Subtle Limit.

**Subtle Limit** starts enabled globally. It caps the accent's brightness,
color and displacement changes even when a slider, audio or MIDI asks for
more. Turning it off allows stronger treatments. Your choice persists across
presets and launches; saved presets do not change it. Other color and audio
controls retain their normal range.

**Variation** selects one of six curated Julia fields. **Another variation**
cycles them while keeping the rest of your look. Drift uses the existing
scene clock; **Freeze scene**, **Travel speed** and **Reset scene / trails**
remain available under Space / Motion. Audio accent adds a restrained
presence-driven accent when Audio Reactivity is running. The controls and
Another variation are available through MIDI Learn.

The accents share WebGPU, WebGL2, native Pop Out and the existing bounded
Canvas fallback. No additional files, downloads or online service are needed.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/USER_GUIDE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md)
