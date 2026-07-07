---
title: Comandos
description: Documentación de comandos derivados del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Referencia
lang: es
---

# Comandos

Los comandos se leen desde `package.json` cuando están disponibles. Utilice scripts fuente como autoridad; Estos documentos son regenerados por `scripts/sync_ascii_docs.rb`.

|Comando|Guión fuente|
| --- | --- |
|`npm run dev`|`vite --host 127.0.0.1 --port 8010`|
|`npm run dev:vite`|`vite --host 127.0.0.1 --port 1420 --strictPort`|
|`npm run build`|`vite build && node scripts/copy_static_assets.mjs`|
|`npm run preview`|`vite preview --host 127.0.0.1 --port 8010`|
|`npm run check`|`npm run check:offline`|
|`npm run check:offline`|`npm run build && node scripts/check_offline_bundle.mjs`|
|`npm run check:desktop`|`npm run check:offline && npm run check:tauri-policy && npm run test:render-math && npm run test:audio-reactive && npm run test:crash-relay && npm run test:output-display && npm run test:updater-manifest && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run check:ffmpeg-resources && npm run test:rust && npm run tauri -- build --debug --no-bundle`|
|`npm run check:release`|`npm run check:offline && npm run check:tauri-policy && npm run test:render-math && npm run test:audio-reactive && npm run test:crash-relay && npm run test:output-display && npm run test:updater-manifest && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run test:ffmpeg-source-build && npm run check:ffmpeg-release && npm run test:rust`|
|`npm run check:bundle`|`node scripts/check_tauri_bundle.mjs`|
|`npm run check:bundle:debug`|`node scripts/check_tauri_bundle.mjs --profile debug`|
|`npm run check:bundle:release`|`node scripts/check_tauri_bundle.mjs --profile release`|
|`npm run check:ffmpeg-resources`|`node scripts/check_ffmpeg_resources.mjs`|
|`npm run check:ffmpeg-release`|`node scripts/check_ffmpeg_resources.mjs --require-current-platform`|
|`npm run check:macos-notarization`|`node scripts/check_macos_notarization.mjs --profile release`|
|`npm run check:windows-authenticode`|`node scripts/check_windows_authenticode.mjs --profile release`|
|`npm run check:media`|`npm run test:frame-prep && npm run test:decode-resize && npm run media:pipeline-preview -- media/point-click-test.mp4 96 54 12 5 false && npm run media:pipeline-preview -- media/point-click-test.mp4 96 54 12 5 true && npm run media:native-session-preview -- media/point-click-test.mp4 96 54 12 5 false 4 && npm run media:native-session-preview -- media/point-click-test.mp4 96 54 12 5 true 4`|
|`npm run check:tauri-policy`|`node scripts/check_tauri_policy.mjs`|
|`npm run release:version:check`|`node scripts/check_release_version.mjs`|
|`npm run release:secrets:check`|`node scripts/check_github_release_secrets.mjs`|
|`npm run release:secrets:check:notarized`|`node scripts/check_github_release_secrets.mjs --require-notarization`|
|`npm run release:secrets:check:public`|`node scripts/check_github_release_secrets.mjs --require-public-signing`|
|`npm run release:secrets:set:macos`|`node scripts/set_macos_notarization_secrets.mjs`|
|`npm run release:secrets:set:windows`|`node scripts/set_windows_artifact_signing_secrets.mjs`|
|`npm run smoke:static`|`npm run build && node scripts/smoke_static_pages.mjs`|
|`npm run smoke:native-output`|`node scripts/smoke_native_output_perf.mjs`|
|`npm run smoke:ui-perf`|`node scripts/smoke_ui_perf.mjs`|
|`npm run smoke:release-install`|`node scripts/smoke_tauri_release_install.mjs`|
|`npm run test:decode-resize`|`node scripts/check_decode_resize_parity.mjs`|
|`npm run test:ffmpeg-policy`|`node scripts/test_ffmpeg_resource_policy.mjs`|
|`npm run test:ffmpeg-source-build`|`node scripts/test_ffmpeg_source_build_config.mjs`|
|`npm run test:frame-prep`|`node scripts/check_frame_prep_parity.mjs`|
|`npm run test:output-display`|`node scripts/test_output_display_placement.mjs`|
|`npm run test:updater-manifest`|`node scripts/test_tauri_update_manifest.mjs`|
|`npm run test:macos-secret-args`|`node scripts/test_macos_notarization_secret_args.mjs`|
|`npm run test:windows-secret-args`|`node scripts/test_windows_artifact_signing_secret_args.mjs`|
|`npm run test:audio-reactive`|`node scripts/test_audio_reactive.mjs`|
|`npm run test:native-output-log`|`node scripts/analyze_native_output_log.mjs`|
|`npm run test:render-math`|`node scripts/test_render_math.mjs`|
|`npm run test:crash-relay`|`npm --prefix crash-relay test`|
|`npm run test:vectors`|`node scripts/test_vectors.mjs`|
|`npm run test:rust`|`node scripts/cargo_env.mjs test --manifest-path src-tauri/Cargo.toml`|
|`npm run tauri`|`node scripts/tauri_env.mjs`|
|`npm run tauri:dev`|`node scripts/tauri_env.mjs dev`|
|`npm run tauri:build`|`node scripts/tauri_env.mjs build`|

## Guía de comando

- Utilice controles específicos antes de las puertas de lanzamiento amplias durante el desarrollo.
- Ejecute comprobaciones del procesador después de cambiar las matemáticas compartidas, los ajustes preestablecidos, el comportamiento del backend, los adaptadores de origen, las transiciones, la modulación de audio o el comportamiento de Pop Out.
- Ejecute comprobaciones de escritorio/versión después de cambiar las capacidades de Tauri, la configuración del actualizador, la firma, los informes de fallos, la salida nativa o el empaquetado de la plataforma.
- Mantenga los secretos y el material de firma fuera de fuentes comprometidas.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [paquete.json](https://github.com/aindaco1/ascii-vj-remix/blob/main/package.json)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
