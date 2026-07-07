---
title: "Source Map"
description: "Source-derived Source Map documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 4
parent: "Reference"
---

# Source Map

The sync script uses the following source files from the ASCII VJ Remix repository.

| Source | Destination / use |
| --- | --- |
| `README.md` | Product scope, feature set, requirements, packaging, support/contact, and developer entry point. |
| `CHANGELOG.md` | Current release baseline, recent behavior changes, security notes, and validation expectations. |
| `docs/RENDERING_ENGINE.md` | Source flow, parameter model, renderer backends, effective params, Pop Out, audio, and stream paths. |
| `docs/CONTRIBUTORS.md` | Setup, contribution workflow, release/updater notes, FFmpeg sidecar policy. |
| `docs/AGENTS.md` | Agent context-loading order, constraints, ownership map, and safe-working guidance. |
| `docs/SECURITY.md` | Local-first boundary, Tauri capabilities, crash reporting, updater, media, and secrets handling. |
| `docs/PERFORMANCE.md` | Renderer/output latency, camera, FPS, and performance validation. |
| `docs/TESTING.md` | Source-derived verification matrix. |
| `docs/ACCESSIBILITY.md` | Control-surface accessibility rules. |
| `docs/I18N.md` | Internationalization and localization expectations. |
| `docs/ROADMAP.md` | Planned, deferred, and current direction. |
| `package.json` | NPM command reference. |

## Regenerate Docs

```bash
ruby scripts/sync_ascii_docs.rb
```

## Rebuild Spanish Docs

```bash
python3 scripts/build_spanish_docs.py
```
