---
title: "Agent Guide"
description: "Source-derived Agent Guide documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 5
parent: "Development"
---

# Agent Guide

This document is for LLM coding agents working on ASCII VJ Remix. It explains
what context to load first, what project constraints matter most, and which
files usually own each kind of change.

## Fast Context Load

Read these in order before making non-trivial changes:

1. [README](/docs/overview/ascii-vj-remix/): product overview, current user-facing feature set,
   install notes, system requirements, license/support/contact information.
2. [Changelog](/docs/reference/changelog/): current release feature baseline and recent
   behavioral expectations.
3. [Roadmap](/docs/reference/roadmap/): prospective work only.
4. [Rendering Engine](/docs/development/rendering-engine/): source flow, renderer backends,
   native output architecture, media engine, audio reactivity, and MIDI
   integration.
5. [Contributor Guide](/docs/development/contributing/): development setup, test commands,
   release/updater notes, FFmpeg sidecar policy, and contribution workflow.
6. Project practice docs when relevant:
   [Security](/docs/operations/security/), [Performance](/docs/operations/performance/),
   [Testing](/docs/operations/testing/), [Accessibility](/docs/operations/accessibility/), and
   [Internationalization](/docs/operations/internationalization/).

For MIDI, UC-33e mapping, or SysEx work, also read
[UC-33e and mioXC MIDI Control](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

For desktop packaging or permissions work, also inspect:

- [Tauri config](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/tauri.conf.json)
- [Tauri capabilities](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/capabilities/default.json)
- [macOS Info.plist](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/Info.plist)
- [macOS entitlements](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/Entitlements.plist)

For renderer or Pop Out work, also inspect:

- [Main app controller](https://github.com/aindaco1/ascii-vj-remix/blob/main/app.js)
- [GPU renderer directory](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/gpu)
- [Desktop adapter](https://github.com/aindaco1/ascii-vj-remix/blob/main/renderers/desktop/tauri-adapter.js)
- [Native output module](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output.rs)
- [Native output GPU presenter](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/gpu.rs)
- [Native camera module](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs)

## Project Identity

ASCII VJ Remix is a local-first native desktop renderer lab for macOS, Windows,
and Linux. The intended product is the Tauri desktop app, not a hosted web app
or browser-only build.

The repository combines high-quality WebGPU/WebGL rendering, Canvas
compatibility paths, ASCILINE-derived stream and codec infrastructure, and
Tauri desktop packaging. The app is a creative control surface for live
ASCII/cell visuals.

## Non-Negotiable Constraints

- Runtime must be local-first and offline by default.
- Do not add CDN, hosted font, hosted decoder, telemetry, or online runtime
  dependencies.
- Intentional online runtime paths are limited to the GitHub Releases updater and
  production-only reviewed/sanitized crash report submission.
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

## Current User-Facing Baseline

The current packaged version and latest public release are 0.9.6. The Changelog
is the only current-state document that includes unreleased changes.

Sources:

- Demo Image is the default startup source.
- Demo Video is the single visible built-in video source.
- Custom local images and videos can be selected.
- Camera is a first-class source.
- Multiple cameras can be mixed locally when the OS/runtime supports concurrent
  capture.
- Camera controls appear directly below Source while Camera is active.

Rendering:

- WebGPU is the primary quality target.
- WebGL2 is the main embedded GPU fallback.
- Canvas2D and pixel Canvas remain compatibility fallbacks.
- Native Pop Out output uses `wgpu` where available, with Metal on macOS and
  corresponding GPU backends on Windows/Linux.
- The active renderer is controlled by one canonical parameter model.
- Native Pop Out preserves glyph-mode and character-set params for traditional
  ASCII presets.
- The shared character-set catalog includes 23 credited ascii.today-derived
  luminance ramps and matching read-only presets.
- Native glyph output uses bounded fixed atlas/ramp resources;
  `fontFamily` is UI/preview metadata, not a native font-loading sink.
- Reuse stable WebGPU/WebGL resources, keep native source uploads keyed to
  source-frame versions, and do not trade quality/resolution for performance.

Live behavior:

- Presets are read-only unless created by the user.
- Preset transitions are smooth crossfades, not fade-to-black.
- Presets preserve the active media source unless explicitly changed.
- WTF mode runs indefinitely while active and transitions through live-safe
  randomized settings, including anchors from traditional ASCII presets.
- Audio reactivity is enabled by default, starts from Mic/Input by default, and
  modulates live effective params without rewriting saved presets.
- Audio reactivity uses bounded feature vectors, including RMS, bands,
  transient/flux, presence, brightness, density, beat pulse, and phase. Do not
  ship raw audio buffers through IPC or diagnostics.
- Safe clamps prevent pure black or pure white outputs from randomized or
  audio-driven states.
- The experimental MIDI rig is the UC-33e through both DIN directions of a
  mioXC; direct UC USB is not supported.
- MIDI uses four channel-addressed pages, soft takeover, numeric preset slots,
  MIDI Learn overrides, and bounded full-bank SysEx capture/restore.
- MIDI targets visual/audio/preset/WTF behavior only. Do not add source, Camera,
  Pop Out, output-display, file, updater, or crash-report actions.
- Read [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) before changing mappings or hardware policy.

UI:

- The current theme is extreme black/white/grey with neon pink and neon blue
  state accents.
- The layout is intentionally dense.
- Do not reduce control density when changing visual styling.
- Avoid adding explanatory marketing text inside the app UI.

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
| macOS native camera latency path | [native_camera.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs) |
| Rust media engine, codec, FFmpeg sessions | [src-tauri/src/media_engine/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri/src/media_engine) |
| Built-in demo media and hidden fixtures | [media/](https://github.com/aindaco1/ascii-vj-remix/tree/main/media) |
| Codec/vector experiments | [experiments/](https://github.com/aindaco1/ascii-vj-remix/tree/main/experiments) |
| Build, smoke, release, Podman, FFmpeg scripts | [scripts/](https://github.com/aindaco1/ascii-vj-remix/tree/main/scripts) |
| User/developer docs | [docs/](https://github.com/aindaco1/ascii-vj-remix/tree/main/docs) and [README](/docs/overview/ascii-vj-remix/) |

## Working Safely

Before editing:

- Check `git status --short`.
- Assume uncommitted changes may be user work.
- Do not reset, checkout, or revert unrelated changes.
- Search with `rg` before changing shared behavior.
- Prefer existing patterns and helper APIs over new abstractions.
- Keep changes scoped to the request.

When editing:

- Use the canonical parameter model rather than creating parallel renderer state.
- Keep source selection, presets, WTF mode, audio modulation, and native output
  synchronization in agreement.
- Preserve Tauri's narrow permissions and capability model.
- Keep runtime assets bundled locally.
- Use existing build scripts rather than ad hoc build commands when possible.
- Update docs when changing product behavior, release behavior, renderer
  architecture, or setup requirements.

## Common Validation Commands

Pick the smallest set that covers the change.

Documentation only:

```bash
git diff --check
```

For broader test selection, read [Testing](/docs/operations/testing/).

Frontend/UI/source behavior:

```bash
npm run build
npm run smoke:static
```

Rust/Tauri behavior:

```bash
npm run test:rust
npm run check:desktop
```

MIDI behavior:

```bash
npm run test:midi
npm run midi:probe -- --connect
npm run test:rust
```

Optimized macOS app build:

```bash
npm run tauri:build:dev -- --bundles app
```

Release packaging:

```bash
npm run ffmpeg:build-sidecar
npm run check:release
npm run bundle:release
```

Expected local release-build note:

- Public 0.9.6 macOS artifacts are Developer ID signed, notarized, stapled, and
  Gatekeeper-validated. Public 0.9.6 Windows artifacts are unsigned previews.
  Normal local builds use
  `ASCII VJ Remix Dev` / `com.asciline.remix.dev`; the local launcher requires a
  stable identity before permission testing.
- If `TAURI_SIGNING_PRIVATE_KEY` or `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` is
  absent while updater artifacts are enabled, release bundling will fail at
  updater signing. The local validation paths are documented in the contributor
  guide; never commit either file.

## Tauri and Packaging Notes

- Tauri v2 is the desktop shell.
- `src-tauri/tauri.conf.json` is the cross-platform production base config; its
  macOS ad-hoc identity is used only by explicit non-notarized packaging paths.
- `src-tauri/tauri.dev.conf.json` isolates normal local commands from the
  production name, bundle identifier, and updater.
- `src-tauri/tauri.notarized.conf.json` is for Developer ID notarized macOS
  release builds.
- `src-tauri/tauri.windows-signed.conf.json` and its Authenticode helper exist
  but are inactive. The current Windows release path uses the default unsigned
  config.
- macOS builds in iCloud Drive workspaces redirect target output to
  `/private/tmp/ascii-vj-remix-tauri-target` through the helper scripts to avoid
  iCloud extended attributes breaking codesign.
- Release updater artifacts are signed with a minisign key. The public key is
  committed; the private key belongs in GitHub Actions secrets.
- FFmpeg sidecars must be reviewed, local, and policy-checked. The packaged app
  does not download FFmpeg, codecs, renderer assets, or fonts at runtime.

See [Contributor Guide: Release and Updater Work](/docs/development/contributing/#release-and-updater-work)
for the full release/updater procedure.

## Renderer Mental Model

Use this flow when reasoning about bugs:

```text
source selection
  -> source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

Important implications:

- Saved params and effective params are different. Audio reactivity modifies
  effective params, not saved preset definitions.
- Source identity matters. Preset transitions do not reset source or restart
  media playback.
- Native output needs fresh params and frames. If Pop Out looks stale, inspect
  native output synchronization before adding another renderer.
- Camera latency work uses latest-frame native capture/presentation paths where
  implemented instead of buffered decode paths.
- Fallback paths matter for Windows/Linux and for environments without the best
  GPU backend.

See [Rendering Engine](/docs/development/rendering-engine/) for deeper architecture details.

## Documentation Update Rules

When behavior changes, update the closest durable doc:

- User-facing feature or install behavior: [README](/docs/overview/ascii-vj-remix/).
- Current and unreleased release behavior: [Changelog](/docs/reference/changelog/).
- Prospective work only: [Roadmap](/docs/reference/roadmap/).
- Renderer architecture, media flow, native output, audio modulation, MIDI
  architecture: [Rendering Engine](/docs/development/rendering-engine/).
- Build, test, release, FFmpeg, Podman, or contributor workflow:
  [Contributor Guide](/docs/development/contributing/).
- Security model, local media, permissions, updater signing, or Tauri
  capabilities: [Security](/docs/operations/security/).
- Performance-sensitive renderer, Pop Out, camera, audio, or source behavior:
  [Performance](/docs/operations/performance/).
- Check selection and manual verification: [Testing](/docs/operations/testing/).
- Keyboard/focus/contrast/control-label behavior:
  [Accessibility](/docs/operations/accessibility/).
- User-visible string, locale, or translation architecture:
  [Internationalization](/docs/operations/internationalization/).
- Agent onboarding assumptions: this file.

Keep docs native-app focused. Current-state docs use present tense and describe
verified behavior. Do not put proposals, future candidates, deferred work, or
completed release plans in those documents. Put prospective work in the
[Roadmap](/docs/reference/roadmap/), and keep release history in the
[Changelog](/docs/reference/changelog/).


## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
