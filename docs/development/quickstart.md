---
title: "Quickstart"
description: "Source-derived Quickstart documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 1
parent: "Development"
---

# Quickstart

## Prerequisites

Use the source repository as the working tree:

```bash
git clone https://github.com/aindaco1/ascii-vj-remix.git
cd ascii-vj-remix
```

Install JavaScript dependencies:

```bash
npm install
```

For desktop work, install the Tauri prerequisites for the target OS. Linux development also needs the WebKitGTK/WebView stack required by Tauri v2.

## Common Local Commands

| Command | Source script |
| --- | --- |
| `npm run dev` | `vite --host 127.0.0.1 --port 8010` |
| `npm run dev:vite` | `vite --host 127.0.0.1 --port 1420 --strictPort` |
| `npm run build` | `vite build && node scripts/copy_static_assets.mjs` |
| `npm run preview` | `vite preview --host 127.0.0.1 --port 8010` |
| `npm run check` | `npm run check:offline` |
| `npm run check:offline` | `npm run build && node scripts/check_offline_bundle.mjs` |
| `npm run check:desktop` | `npm run check:offline && npm run check:tauri-policy && npm run test:render-math && npm run test:audio-reactive && npm run test:crash-relay && npm run test:output-display && npm run test:updater-manifest && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run check:ffmpeg-resources && npm run test:rust && npm run tauri -- build --debug --no-bundle` |
| `npm run check:release` | `npm run check:offline && npm run check:tauri-policy && npm run test:render-math && npm run test:audio-reactive && npm run test:crash-relay && npm run test:output-display && npm run test:updater-manifest && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run test:ffmpeg-source-build && npm run check:ffmpeg-release && npm run test:rust` |
| `npm run check:bundle` | `node scripts/check_tauri_bundle.mjs` |
| `npm run check:bundle:debug` | `node scripts/check_tauri_bundle.mjs --profile debug` |
| `npm run check:bundle:release` | `node scripts/check_tauri_bundle.mjs --profile release` |
| `npm run check:ffmpeg-resources` | `node scripts/check_ffmpeg_resources.mjs` |
| `npm run check:ffmpeg-release` | `node scripts/check_ffmpeg_resources.mjs --require-current-platform` |
| `npm run check:macos-notarization` | `node scripts/check_macos_notarization.mjs --profile release` |
| `npm run check:windows-authenticode` | `node scripts/check_windows_authenticode.mjs --profile release` |
| `npm run check:media` | `npm run test:frame-prep && npm run test:decode-resize && npm run media:pipeline-preview -- media/point-click-test.mp4 96 54 12 5 false && npm run media:pipeline-preview -- media/point-click-test.mp4 96 54 12 5 true && npm run media:native-session-preview -- media/point-click-test.mp4 96 54 12 5 false 4 && npm run media:native-session-preview -- media/point-click-test.mp4 96 54 12 5 true 4` |
| `npm run check:tauri-policy` | `node scripts/check_tauri_policy.mjs` |
| `npm run release:version:check` | `node scripts/check_release_version.mjs` |
| `npm run release:secrets:check` | `node scripts/check_github_release_secrets.mjs` |
| `npm run release:secrets:check:notarized` | `node scripts/check_github_release_secrets.mjs --require-notarization` |
| `npm run release:secrets:check:public` | `node scripts/check_github_release_secrets.mjs --require-public-signing` |
| `npm run release:secrets:set:macos` | `node scripts/set_macos_notarization_secrets.mjs` |
| `npm run release:secrets:set:windows` | `node scripts/set_windows_artifact_signing_secrets.mjs` |
| `npm run smoke:static` | `npm run build && node scripts/smoke_static_pages.mjs` |
| `npm run smoke:native-output` | `node scripts/smoke_native_output_perf.mjs` |
| `npm run smoke:ui-perf` | `node scripts/smoke_ui_perf.mjs` |
| `npm run smoke:release-install` | `node scripts/smoke_tauri_release_install.mjs` |
| `npm run test:decode-resize` | `node scripts/check_decode_resize_parity.mjs` |
| `npm run test:ffmpeg-policy` | `node scripts/test_ffmpeg_resource_policy.mjs` |
| `npm run test:ffmpeg-source-build` | `node scripts/test_ffmpeg_source_build_config.mjs` |
| `npm run test:frame-prep` | `node scripts/check_frame_prep_parity.mjs` |
| `npm run test:output-display` | `node scripts/test_output_display_placement.mjs` |
| `npm run test:updater-manifest` | `node scripts/test_tauri_update_manifest.mjs` |
| `npm run test:macos-secret-args` | `node scripts/test_macos_notarization_secret_args.mjs` |
| `npm run test:windows-secret-args` | `node scripts/test_windows_artifact_signing_secret_args.mjs` |
| `npm run test:audio-reactive` | `node scripts/test_audio_reactive.mjs` |
| `npm run test:native-output-log` | `node scripts/analyze_native_output_log.mjs` |
| `npm run test:render-math` | `node scripts/test_render_math.mjs` |
| `npm run test:crash-relay` | `npm --prefix crash-relay test` |
| `npm run test:vectors` | `node scripts/test_vectors.mjs` |
| `npm run test:rust` | `node scripts/cargo_env.mjs test --manifest-path src-tauri/Cargo.toml` |
| `npm run tauri` | `node scripts/tauri_env.mjs` |
| `npm run tauri:dev` | `node scripts/tauri_env.mjs dev` |
| `npm run tauri:build` | `node scripts/tauri_env.mjs build` |

## First Verification Path

1. Install dependencies with `npm install`.
2. Run the source repo's focused checks before changing behavior.
3. For renderer changes, inspect [Rendering Engine](/docs/development/rendering-engine/) and run renderer-specific checks from [Commands](/docs/reference/commands/).
4. For desktop packaging or permissions changes, inspect Tauri config, capabilities, macOS plist/entitlements, and release notes.
5. For user-facing controls, check accessibility and i18n expectations before shipping copy or UI changes.

## Development Boundary

Do not add hosted fonts, CDNs, online decoders, telemetry, or hosted runtime dependencies. Runtime assets should remain bundled locally, and selected user media should stay local.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
