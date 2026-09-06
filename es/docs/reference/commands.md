---
title: Comandos
description: Documentación de comandos derivados del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Referencia
lang: es
---

<a id="commands"></a>

# Comandos

Los comandos se leen del objeto de scripts `package.json` completo. Utilice scripts fuente como autoridad; Estos documentos son regenerados por `scripts/sync_ascii_docs.rb`.

Las rutas de dispositivos de medios agrupados se generalizan en esta referencia pública. Utilice `package.json` cuando inspeccione la implementación exacta del script.

|Comando|Guión fuente|
| --- | --- |
|`npm run dev`|`vite --host 127.0.0.1 --port 8010`|
|`npm run dev:vite`|`vite --host 127.0.0.1 --port 1420 --strictPort`|
|`npm run build`|`vite build && node scripts/copy_static_assets.mjs`|
|`npm run preview`|`vite preview --host 127.0.0.1 --port 8010`|
|`npm run check`|`npm run check:offline`|
|`npm run check:offline`|`npm run build && node scripts/check_offline_bundle.mjs`|
|`npm run check:desktop`|`npm run check:offline && npm run check:tauri-policy && npm run check:icons && npm run check:glyph-atlas && npm run test:release-build-reuse && npm run test:render-math && npm run test:preset-backend-contract && npm run test:preset-playlists && npm run test:canvas-readback && npm run test:renderer-fallback && npm run test:media-source-policy && npm run test:audio-reactive && npm run test:midi && npm run test:crash-report-ui && npm run test:crash-relay && npm run test:output-display && npm run test:desktop-updater && npm run test:updater-manifest && npm run test:macos-artifacts && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run check:ffmpeg-resources && npm run test:rust && npm run tauri:build:dev -- --debug --no-bundle`|
|`npm run check:release`|`npm run check:offline && npm run check:tauri-policy && npm run check:icons && npm run check:glyph-atlas && npm run test:release-build-reuse && npm run test:render-math && npm run test:preset-backend-contract && npm run test:preset-playlists && npm run test:canvas-readback && npm run test:renderer-fallback && npm run test:media-source-policy && npm run test:audio-reactive && npm run test:midi && npm run test:crash-report-ui && npm run test:crash-relay && npm run test:output-display && npm run test:desktop-updater && npm run test:updater-manifest && npm run test:macos-artifacts && npm run test:macos-secret-args && npm run test:windows-secret-args && npm run test:ffmpeg-policy && npm run check:release-runtime && npm run test:rust`|
|`npm run check:bundle`|`node scripts/check_tauri_bundle.mjs`|
|`npm run check:bundle:debug`|`node scripts/check_tauri_bundle.mjs --profile debug --expected-bundle-id com.asciline.remix.dev`|
|`npm run check:bundle:release`|`node scripts/check_tauri_bundle.mjs --profile release --expected-bundle-id com.asciline.remix`|
|`npm run check:ffmpeg-resources`|`node scripts/check_ffmpeg_resources.mjs`|
|`npm run check:icons`|`node scripts/check_app_icons.mjs`|
|`npm run check:glyph-atlas`|`node scripts/check_glyph_atlas.mjs`|
|`npm run check:ffmpeg-release`|`node scripts/check_ffmpeg_resources.mjs --require-current-platform`|
|`npm run check:release-runtime`|`npm run test:ffmpeg-source-build && npm run check:ffmpeg-release`|
|`npm run check:macos-notarization`|`node scripts/check_macos_notarization.mjs --profile release`|
|`npm run check:windows-authenticode`|`node scripts/check_windows_authenticode.mjs --profile release`|
|`npm run check:windows-gui`|`node scripts/check_windows_gui_subsystem.mjs --profile release`|
|`npm run check:media`|`npm run test:frame-prep && npm run test:decode-resize && npm run media:pipeline-preview -- media/<bundled-test-fixture>.mp4 96 54 12 5 false && npm run media:pipeline-preview -- media/<bundled-test-fixture>.mp4 96 54 12 5 true && npm run media:native-session-preview -- media/<bundled-test-fixture>.mp4 96 54 12 5 false 4 && npm run media:native-session-preview -- media/<bundled-test-fixture>.mp4 96 54 12 5 true 4`|
|`npm run check:tauri-policy`|`node scripts/check_tauri_policy.mjs`|
|`npm run bundle:debug`|`npm run tauri:build:dev -- --debug && npm run check:bundle:debug`|
|`npm run bundle:test`|`npm run check:ffmpeg-release && npm run tauri:build:dev -- --bundles nsis,msi && node scripts/check_tauri_bundle.mjs --profile release --expected-bundle-id com.asciline.remix.dev && npm run check:windows-gui`|
|`npm run bundle:test:linux`|`npm run check:ffmpeg-release && npm run tauri:build:dev -- --bundles appimage,deb,rpm && node scripts/check_tauri_bundle.mjs --profile release --expected-bundle-id com.asciline.remix.dev`|
|`npm run bundle:release`|`npm run ffmpeg:build-sidecar && npm run check:release && npm run tauri:build && npm run check:bundle:release`|
|`npm run desktop:run-local`|`bash scripts/run_local_desktop_app.sh`|
|`npm run desktop:run-local:foreground`|`ASCILINE_FOREGROUND=1 bash scripts/run_local_desktop_app.sh`|
|`npm run desktop:run-local:reset`|`ASCILINE_RESET_TCC=1 bash scripts/run_local_desktop_app.sh`|
|`npm run desktop:codesign:local`|`bash scripts/create_local_codesign_identity.sh`|
|`npm run ffmpeg:stage`|`node scripts/stage_ffmpeg_sidecars.mjs`|
|`npm run ffmpeg:build-sidecar`|`bash scripts/build_ffmpeg_sidecar.sh`|
|`npm run ffmpeg:sign:macos`|`node scripts/sign_macos_ffmpeg_sidecars.mjs`|
|`npm run icons:generate`|`node scripts/tauri_env.mjs icon assets/branding/ascii-vj-remix-app-icon-1024.png --output src-tauri/icons`|
|`npm run glyphs:generate`|`node scripts/generate_glyph_atlas.mjs`|
|`npm run macos:notarize-dmg`|`node scripts/notarize_macos_dmg.mjs`|
|`npm run release:version:check`|`node scripts/check_release_version.mjs`|
|`npm run release:secrets:check`|`node scripts/check_github_release_secrets.mjs`|
|`npm run release:secrets:check:notarized`|`node scripts/check_github_release_secrets.mjs --require-notarization`|
|`npm run release:secrets:check:public`|`node scripts/check_github_release_secrets.mjs --require-public-signing`|
|`npm run release:secrets:set:macos`|`node scripts/set_macos_notarization_secrets.mjs`|
|`npm run release:secrets:set:windows`|`node scripts/set_windows_artifact_signing_secrets.mjs`|
|`npm run updater:secret:set`|`node scripts/set_tauri_updater_secret.mjs`|
|`npm run updater:secret:check`|`node scripts/set_tauri_updater_secret.mjs --dry-run`|
|`npm run media:decode-preview`|`node scripts/cargo_env.mjs run --manifest-path src-tauri/Cargo.toml --example decode_preview --`|
|`npm run media:native-session-preview`|`node scripts/cargo_env.mjs run --manifest-path src-tauri/Cargo.toml --example native_session_preview --`|
|`npm run media:pipeline-preview`|`node scripts/cargo_env.mjs run --manifest-path src-tauri/Cargo.toml --example pipeline_preview --`|
|`npm run midi:probe`|`node scripts/cargo_env.mjs run --manifest-path src-tauri/Cargo.toml --example midi_probe --`|
|`npm run smoke:static`|`npm run build && node scripts/smoke_static_pages.mjs`|
|`npm run smoke:native-output`|`node scripts/smoke_native_output_perf.mjs`|
|`npm run smoke:ui-perf`|`node scripts/smoke_ui_perf.mjs`|
|`npm run smoke:primary-presets`|`node scripts/smoke_primary_presets.mjs`|
|`npm run bench:density`|`node scripts/benchmark_renderer_density.mjs`|
|`npm run smoke:release-install`|`node scripts/smoke_tauri_release_install.mjs`|
|`npm run test:decode-resize`|`node scripts/check_decode_resize_parity.mjs`|
|`npm run test:desktop-updater`|`node scripts/test_desktop_updater.mjs`|
|`npm run test:ffmpeg-policy`|`node scripts/test_ffmpeg_resource_policy.mjs`|
|`npm run test:ffmpeg-source-build`|`node scripts/test_ffmpeg_source_build_config.mjs`|
|`npm run test:frame-prep`|`node scripts/check_frame_prep_parity.mjs`|
|`npm run test:output-display`|`node scripts/test_output_display_placement.mjs`|
|`npm run test:updater-manifest`|`node scripts/test_tauri_update_manifest.mjs`|
|`npm run test:macos-identity`|`node scripts/test_macos_app_identity.mjs`|
|`npm run test:macos-dmg-layout`|`node scripts/test_macos_dmg_layout.mjs`|
|`npm run test:macos-artifacts`|`npm run test:macos-identity && npm run test:macos-dmg-layout`|
|`npm run test:macos-secret-args`|`node scripts/test_macos_notarization_secret_args.mjs`|
|`npm run test:windows-secret-args`|`node scripts/test_windows_artifact_signing_secret_args.mjs`|
|`npm run test:audio-reactive`|`node scripts/test_audio_reactive.mjs`|
|`npm run test:midi`|`node scripts/test_midi_mapping.mjs`|
|`npm run test:media-source-policy`|`node scripts/test_media_source_policy.mjs`|
|`npm run test:native-output-log`|`node scripts/analyze_native_output_log.mjs`|
|`npm run test:render-math`|`node scripts/test_render_math.mjs`|
|`npm run test:preset-backend-contract`|`node scripts/test_preset_backend_contract.mjs`|
|`npm run test:preset-playlists`|`node scripts/test_preset_playlists.mjs`|
|`npm run test:canvas-readback`|`node scripts/test_canvas_readback.mjs`|
|`npm run test:renderer-fallback`|`node scripts/test_renderer_fallback.mjs`|
|`npm run test:release-build-reuse`|`node scripts/test_release_build_reuse.mjs`|
|`npm run test:crash-report-ui`|`node scripts/test_crash_report_ui.mjs`|
|`npm run test:crash-relay`|`npm --prefix crash-relay test`|
|`npm run test:vectors`|`node scripts/test_vectors.mjs`|
|`npm run test:rust`|`node scripts/cargo_env.mjs test --manifest-path src-tauri/Cargo.toml`|
|`npm run tauri`|`node scripts/tauri_env.mjs`|
|`npm run tauri:dev`|`node scripts/tauri_env.mjs dev --config src-tauri/tauri.dev.conf.json`|
|`npm run tauri:build`|`node scripts/tauri_env.mjs build`|
|`npm run tauri:build:dev`|`node scripts/tauri_env.mjs build --config src-tauri/tauri.dev.conf.json`|

<a id="command-guidance"></a>

## Guía de comando

- Utilice controles específicos antes de las puertas de lanzamiento amplias durante el desarrollo.
- Ejecute comprobaciones del renderizador después de cambiar las matemáticas compartidas, los ajustes preestablecidos, el comportamiento del backend, los adaptadores de origen, las transiciones, la modulación de audio o el comportamiento de Pop Out.
- Ejecute comprobaciones de escritorio/versión después de cambiar las capacidades de Tauri, la configuración del actualizador, la firma, los informes de fallos, la salida nativa o el empaquetado de la plataforma.
- Mantenga los secretos y el material de firma fuera de fuentes comprometidas.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [package.json](https://github.com/aindaco1/ascii-vj-remix/blob/main/package.json)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
