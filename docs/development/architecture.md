---
title: "Architecture"
description: "Source-derived Architecture documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 2
parent: "Development"
---

# Architecture

## Product Shape

ASCII VJ Remix is a Tauri v2 desktop app with a vanilla/Vite renderer UI, GPU/Canvas rendering paths, native output work, and local media/audio adapters.

The app should be understood as a desktop performer tool, not a hosted SaaS app. Browser mode helps development and portability, but the packaged desktop app is the product.

## High-Level Flow

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

## Ownership Map

| Area | Primary source locations |
| --- | --- |
| Main UI, params, presets, source controls, WTF, audio UI | `app.js`, `index.html`, `style.css` |
| GPU renderer and media source abstraction | `renderers/gpu/` |
| Tauri adapter and output-display helpers | `renderers/desktop/` |
| Tauri shell, commands, permissions, updater, native audio, native output | `src-tauri/` |
| Native Pop Out renderer | `src-tauri/src/native_output.rs`, `src-tauri/src/native_output/gpu.rs` |
| macOS native camera latency path | `src-tauri/src/native_output/native_camera.rs` |
| Rust media engine and FFmpeg sessions | `src-tauri/src/media_engine/` |
| Build, smoke, release, Podman, FFmpeg scripts | `scripts/` |
| User/developer docs | `docs/`, `README.md`, `CHANGELOG.md` |

## Non-negotiable Constraints

- Preserve the app name and native desktop direction.
- Keep normal runtime local-first and offline by default.
- Keep renderer quality high; WebGPU/WebGL output is the visual quality target.
- Preserve fallback paths unless a replacement is implemented and tested.
- Treat Pop Out performance and latency as critical user-facing behavior.
- Keep selected local media local.
- Keep stats overlay user-owned.
- Keep stream infrastructure hidden until the stream workflow is productized end to end.
- Do not reduce the control density of the VJ surface when restyling.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
