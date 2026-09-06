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
| `README.md` | Product scope and lineage; upstream installation and first-run entry point. |
| `docs/README.md` | Upstream documentation ownership and navigation. |
| `docs/USER_GUIDE.md` | Detailed feature set, system requirements, hardware, and thermal guidance. Full usage, permissions, and troubleshooting remain linked upstream. |
| `CHANGELOG.md` | Current release baseline, recent behavior changes, security notes, and validation expectations. |
| `docs/RENDERING_ENGINE.md` | Source flow, parameter model, renderer backends, effective params, Pop Out, audio, and stream paths. |
| `docs/CONTRIBUTORS.md` | Quickstart, local app identity, contribution workflow, FFmpeg, and Podman. |
| `docs/RELEASING.md` | Reusable packaging, signing, publication, updater, and artifact acceptance procedure. |
| `docs/releases/README.md` | Linked index of historical release records; not current procedure or live acceptance status. |
| `docs/AGENTS.md` | Agent context-loading order, constraints, ownership map, and safe-working guidance. |
| `docs/SECURITY.md` | Local-first boundary, Tauri capabilities, crash reporting, updater, media, and secrets handling. |
| `docs/PERFORMANCE.md` | Renderer/output latency, camera, FPS, and performance validation. |
| `docs/TESTING.md` | Source-derived verification matrix. |
| `docs/ACCESSIBILITY.md` | Control-surface accessibility rules. |
| `docs/I18N.md` | Internationalization and localization expectations. |
| `docs/ROADMAP.md` | Prospective direction only. |
| `package.json` | NPM command reference. |
| `src-tauri/icons/icon.png` | Approved canonical app icon copied into the marketing site. |

## Guide Ownership

The [upstream documentation index](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md) owns the full guide map, including MIDI, character-preset credits, Linux VM QA, component docs, and benchmark evidence. These specialized guides remain linked to their canonical source files.

[Release records](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) preserve dated decisions and evidence. Use [Release and Updates](/docs/operations/release/) for the current procedure, [Testing](/docs/operations/testing/) for verification, and [Roadmap](/docs/reference/roadmap/) for prospective work.

## Regenerate Docs

```bash
ruby scripts/sync_ascii_docs.rb
```

## Rebuild Spanish Docs

```bash
python3 scripts/build_spanish_docs.py
```
