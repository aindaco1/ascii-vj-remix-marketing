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

1. [README](/docs/overview/ascii-vj-remix/): product overview, install basics, first run, and
   current source/release version. The [User Guide](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md) owns the full
   feature set, system requirements, permissions, and troubleshooting.
2. [Changelog](/docs/reference/changelog/): recent released and unreleased changes.
3. [Roadmap](/docs/reference/roadmap/): prospective work only.
4. [Rendering Engine](/docs/development/rendering-engine/): source flow, renderer backends,
   native output, media engine, audio reactivity, and MIDI integration.
5. [Contributor Guide](/docs/development/contributing/): setup, local app identity, FFmpeg,
   Podman, and contribution workflow.
6. [Testing](/docs/operations/testing/): check selection and manual verification. Read the
   relevant [Security](/docs/operations/security/), [Performance](/docs/operations/performance/),
   [Accessibility](/docs/operations/accessibility/), and [Internationalization](/docs/operations/internationalization/) guide
   for the affected behavior.

The [documentation index](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md) routes to every maintained guide. For
packaging, signing, publication, or updater work, also read
[Release and Updater Guide](/docs/operations/release/). Version-specific
[release records](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) preserve historical evidence and do not
replace the current guides.

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
  `renderers/shared/preset-backend-contract.js` (90 total, 62 accelerated,
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

## Validation and Packaging

`npm test` runs the existing desktop/static checks plus live Jev on built-in
synthetic component evidence. Use `-- --offline` explicitly to skip hosted
evaluation. Keep Jev development-only and reuse the pinned Platform Test Core
entry; see [Jev development testing](/docs/operations/testing/#jev-development-testing).
Never pass private diagnostics or media to this evaluator or interpret its
result as visual, native hardware, or release acceptance.

Use [Testing: Recommended Check Sets](/docs/operations/testing/#recommended-check-sets) to
select the smallest checks that cover the change. Documentation-only changes
require `git diff --check`; moves also require link, anchor, and path-reference
validation. Do not treat local checks, CI packages, installed-app smokes, and
physical hardware acceptance as interchangeable.

Use [Contributor Guide](/docs/development/contributing/) for local build commands and
[macOS development identity](/docs/development/contributing/#macos-permissions-during-development).
Normal local builds use `ASCII VJ Remix Dev` / `com.asciline.remix.dev`, and
permission testing requires stable local signing. The contributor guide also
owns the iCloud build-directory behavior and canonical icon generation flow.

Use [Release and Updater Guide](/docs/operations/release/) for packaging configs, signing,
secrets, FFmpeg release inputs, and public-artifact validation. Updater-enabled
bundling requires its signing key/password; missing secrets are not a reason to
weaken the release gate. Never commit them. Public macOS signing and the current
unsigned Windows preview path are defined there and in [Security](/docs/operations/security/).

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

Use the ownership map in the [documentation index](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md). Update the
closest durable guide and link to it instead of maintaining parallel procedures:

- Product overview, installation basics, first run: [root README](/docs/overview/ascii-vj-remix/).
- Detailed user behavior, requirements, permissions, troubleshooting:
  [User Guide](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md).
- Released/unreleased changes: [Changelog](/docs/reference/changelog/).
- Proposals and future work: [Roadmap](/docs/reference/roadmap/).
- Rendering/media/output/audio/MIDI architecture: [Rendering Engine](/docs/development/rendering-engine/).
- Local setup, development identity, FFmpeg/Podman, contributions:
  [Contributor Guide](/docs/development/contributing/).
- Packaging, signing, publication, updater procedure: [Release Guide](/docs/operations/release/).
- Version-specific decisions and evidence: [release records](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md).
- Security, performance, check selection, accessibility, and string ownership:
  the corresponding practice guide linked above.
- Agent onboarding and source ownership: this file.

Current-state guides describe verified behavior in the present tense. Keep
proposals in the Roadmap and completed plans in release records. Testing may
state known coverage gaps, but a historical pending row must not become a claim
about current release status. Keep the docs native-app focused and preserve the
source/CI/artifact/installed-app/physical-platform evidence boundaries.


## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
