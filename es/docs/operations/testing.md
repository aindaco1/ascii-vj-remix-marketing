---
title: Pruebas
description: Documentación de prueba derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Operaciones
lang: es
---

# Pruebas

Esta guía documenta los controles automatizados actuales, las rutas de verificación manual,
y expectativas de pruebas futuras para ASCII VJ Remix.

Las pruebas se centran en paquetes fuera de línea, inicio del renderizador, cambio de fuente,
salida nativa, comportamiento de medios/cámara/audio, permisos Tauri, sidecars FFmpeg,
lanzar artefactos y manifiestos de actualización.

## Referencia rápida

```bash
npm run build                    # Vite production build plus local asset copy
npm run check:offline            # Build and verify bundled/offline assets
npm run smoke:static             # Static UI/renderer smoke harness
npm run check:tauri-policy       # Production CSP and local-only runtime policy
npm run test:output-display      # Secondary-display placement simulation
npm run test:updater-manifest    # Tauri latest.json/updater manifest tests
npm run test:macos-identity      # macOS bundle/team/designated-requirement tests
npm run test:macos-secret-args   # macOS notarization secret argument safety
npm run test:ffmpeg-policy       # FFmpeg policy checks
npm run check:ffmpeg-resources   # FFmpeg sidecar resource metadata checks
npm run test:frame-prep          # Rust/JS frame-prep parity
npm run test:decode-resize       # Decode/resize parity checks
npm run check:media              # Media pipeline checks
npm run test:render-math         # Shared renderer math vectors
npm run test:audio-reactive      # Audio-reactive controls, clamps, dense-mix damping
npm run test:midi                # UC-33e map, scaling, pickup, actions, coalescing
npm run midi:probe -- --connect  # Physical mioXC input/output open test
npm run test:crash-relay         # Cloudflare crash relay sanitizer/rate-limit tests
npm run test:vectors             # Adaptive codec vector checks
npm run test:rust                # Rust tests
npm run check:desktop            # Main desktop validation gate
npm run check:release            # Release-oriented gate; expects staged FFmpeg sidecar
npm run bundle:debug             # Build and validate local debug bundle
npm run bundle:release           # Release gate, release build, bundle check
npm run check:windows-authenticode # Future signed Windows release signature check
npm run smoke:native-output      # Native output performance helper
npm run smoke:ui-perf            # UI performance helper
npm run smoke:release-install    # Release artifact install/updater smoke
```

Para cambios de documentación únicamente:

```bash
git diff --check
```

## Categorías de prueba

|Área|Cheques actuales|
| --- | --- |
|Tiempo de ejecución sin conexión|`npm run check:offline`, `scripts/check_offline_bundle.mjs`|
|Arnés de interfaz de usuario estática|`npm run smoke:static`|
|Política Tauri|`npm run check:tauri-policy`|
|Lógica de visualización de salida|`npm run test:output-display`|
|Manifiestos del actualizador|`npm run test:updater-manifest`|
|Identidad de la aplicación macOS|`npm run test:macos-identity`, libera inspección de artefactos en macOS|
|Manejo de secretos macOS|`npm run test:macos-secret-args`|
|FFmpeg política/recursos|`npm run test:ffmpeg-policy`, `npm run check:ffmpeg-resources`, `npm run check:ffmpeg-release`|
|Preparación/decodificación de fotogramas multimedia|`npm run test:frame-prep`, `npm run test:decode-resize`, `npm run check:media`|
|Paridad matemática del renderizador|Pruebas de vectores compartidos `npm run test:render-math`, Rust a través de `npm run test:rust`|
|MIDI|`npm run test:midi`, Rust MIDI/Pruebas SysEx, `npm run midi:probe -- --connect`|
|Relevo de choque|`npm run test:crash-relay`|
|Vectores de códec adaptativos|`npm run test:vectors`|
|Módulos Rust/Tauri|`npm run test:rust`|
|Rendimiento de salida nativa|`npm run smoke:native-output`, `npm run test:native-output-log`|
|Rendimiento de la interfaz de usuario|`npm run smoke:ui-perf` con valores predeterminados/transiciones fijos y promedio/P10/P50/mínimo FPS|
|Lanzamiento de instalación/actualización|`npm run smoke:release-install`|

## Conjuntos de cheques recomendados

### Sólo documentación

```bash
git diff --check
```

### Interfaz de usuario frontal, CSS, ajustes preestablecidos, fuentes, interfaz de usuario de audio

```bash
npm run build
npm run smoke:static
```

Agregue comprobaciones manuales para cambio de fuente, transiciones preestablecidas, WTF mode y audio
Reactividad cuando cambia el comportamiento.

### Cambios en el backend del renderizador

```bash
npm run build
npm run test:render-math
npm run smoke:static
npm run check:media
```

También compare manualmente la salida WebGPU y WebGL2 para obtener ajustes preestablecidos representativos.

### Salida nativa o cambios Pop Out

```bash
npm run test:output-display
npm run smoke:native-output
npm run test:native-output-log
npm run test:rust
```

Utilice una compilación de aplicación optimizada antes de sacar conclusiones sobre el rendimiento.
El humo del rendimiento de la interfaz de usuario comienza con valores predeterminados visuales canónicos, utiliza elementos fijos.
transiciones numéricas no estructurales y registra cada backend visitado, así que repita
las carreras son comparables. Seleccione un paquete exacto y una muestra más larga con:

```bash
ASCILINE_SOURCE_APP="/absolute/path/ASCII VJ Remix.app" \
ASCILINE_UI_PERF_SMOKE_DURATION_MS=30000 \
npm run smoke:ui-perf
```

El análisis de registros nativos informa tanto de las tasas de carga de origen como de tasas de omisión de carga. Un saludable
24 FPS la fuente en una pantalla de 60 Hz debe cargar una velocidad cercana a la fuente y omitir el
duplicar ticks de visualización mientras la presentación permanece cerca de la frecuencia de actualización.
Para cambios en el modo de glifo, incluya al menos un ajuste preestablecido ASCII tradicional en el manual
Pop Out comprueba y confirma que los cambios en el conjunto de caracteres/familia de fuentes no ocultan el
Controles de glifo/celda.

### Cambios en MIDI, UC-33e o SysEx

```bash
npm run test:midi
npm run check:tauri-policy
npm run test:rust
npm run midi:probe -- --connect
npm run smoke:static
```

La sonda física verifica que CoreMIDI pueda enumerar y abrir simultáneamente
ambas direcciones del mioXC. No reemplaza el barrido de control y
Lista de verificación de captura/restauración de banco completo en [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

### Tauri Comandos, permisos o capacidades

```bash
npm run check:tauri-policy
npm run test:crash-relay
npm run test:rust
npm run check:desktop
```

Verifique manualmente la cámara macOS, el micrófono, la pantalla/audio del sistema y Pop Out
comportamiento cuando cambia el modelo de permiso.

Para cambios en informes de fallas, verifique también que las compilaciones de depuración se capturen localmente, pero no
no enviar, las versiones de lanzamiento usan solo `https://crash.dustwave.xyz/v1/reports`, y
la ventana de salida no tiene permisos de informe de fallos.

### FFmpeg y motor de medios

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
npm run check:media
npm run test:rust
```

Para sidecars de lanzamiento:

```bash
npm run test:ffmpeg-source-build
npm run check:ffmpeg-release
```

### Lanzamiento y actualizador

```bash
npm run check:release
npm run bundle:release
npm run smoke:release-install
npm run test:macos-dmg-layout
```

Ejecute `npm run ffmpeg:build-sidecar` antes que `npm run check:release` en limpio
clonar. `npm run bundle:release` ejecuta el paso de compilación del sidecar automáticamente.

El humo de lanzamiento descarga artefactos del instalador de lanzamientos y comprobaciones GitHub.
diseño, activos incluidos, paquetes de actualización firmados y comportamiento de `latest.json`. encendido
macOS verifica el DMG descargado, lo monta como solo lectura en un temporal privado
root, valida el diseño exacto de aplicación a aplicaciones e inspecciona el archivo montado
aplicación antes del salto del actualizador.
Updater-hop smoke usa `0.9.0` como la versión anterior mínima predeterminada porque
Las versiones anteriores de `0.1.x` se firmaron con una clave de actualización diferente.

En macOS, la liberación de humo extrae el `.app.tar.gz` actual y anterior.
cargas útiles, requiere `com.asciline.remix`, ID de equipo `PWT3Q52LZ2`, tiempo de ejecución reforzado,
La aceptación del gatekeeper y exactamente el mismo requisito designado, luego ejecuta el
aplicación anterior a través del actualizador y revalida el paquete reemplazado. el
La aprobación interactiva de TCC en sí sigue siendo una verificación manual.

## Lista de verificación manual de humo

Úselo después de realizar cambios en el renderizador, la fuente, el audio o la salida de cara al usuario:

1. Inicie la aplicación de escritorio.
2. Confirme que aparece la imagen de demostración y el renderizador se inicia automáticamente.
3. Cambie a Vídeo de demostración y confirme que comienza la reproducción.
4. Vuelva a la imagen de demostración y confirme que el renderizador no se atasca.
5. Seleccione Cámara y confirme la solicitud de permiso/comportamiento del dispositivo.
6. Seleccione Micrófono/Entrada y confirme que se inicia la reactividad de audio o solicita permiso.
7. Cambie de dispositivo de audio y confirme que la captura se reinicia automáticamente.
8. Activar pantalla/audio del sistema cuando sea compatible y confirmar errores es útil
cuando la fuente seleccionada no tiene pista de audio.
9. Haga clic en varios ajustes preestablecidos y confirme transiciones suaves.
10. Seleccione un ajuste preestablecido ASCII tradicional y confirme el conjunto de caracteres y la familia de fuentes
permanece compacto y visible.
11. Active y desactive WTF mode y confirme que sigue respondiendo y puede visitar
estados tradicionales de apariencia ASCII.
12. Abra Pop Out y confirme que la vista previa principal sigue respondiendo.
13. Confirme que Pop Out refleja los ajustes preestablecidos, WTF mode y la reactividad de audio mientras está completamente
visible.
14. Confirmar superposición de estadísticas informa el valor preestablecido/fuente/backend/grid/FPS activo.
15. Cierre Pop Out y confirme que se establezca el uso de CPU/GPU.

## Comprobaciones de hardware y plataforma

La aplicación depende del hardware real y de las pilas de medios del sistema operativo. Las pruebas automatizadas no pueden
cubrir todo todavía.

Matrices manuales importantes:

- macOS Apple Silicon con cámara integrada y pantalla externa.
- macOS con cámara USB externa.
- macOS con sistema de captura de audio.
- Windows con WebView2, D3D12/WebGL2, cámara, micrófono y ruta de instalación.
- Linux con WebKitGTK, aceleración GPU, cámara, micrófono y ruta AppImage/deb.
- Equipo experimental macOS Apple Silicon MIDI: Evolution/M-Audio UC-33e hasta
ambas direcciones DIN de un iConnectivity mioXC, alimentado por separado.

Al informar los resultados del hardware, incluya:

- Versión del sistema operativo.
- CPU/GPU.
- versión de la aplicación y tipo de compilación.
- tipo de fuente.
- back-end.
- Estado Pop Out.
- fuente de audio.
- nombres de dispositivos de cámara y resolución solicitada/FPS.

## Comprobaciones de Podman

Podman es principalmente para un shell de desarrollo y legado reproducible similar a Linux
Trabajo con Python/OpenCV/vector. No es el tiempo de ejecución de producción.

Comandos útiles:

```bash
scripts/podman-doctor.sh
scripts/podman_build.sh
scripts/podman_venv.sh
scripts/podman_codec_tests.sh
```

La imagen de Podman tiene como valor predeterminado el Nodo 24. Use `NODE_MAJOR=26` solo cuando esté explícitamente
probando una línea base de Nodo más nueva.

## CI y expectativas de lanzamiento

La versión CI debe:

- construir artefactos macOS, Windows y Linux.
- verificar el comportamiento del paquete sin conexión.
- verificar la política Tauri.
- construir/comprobar sidecars FFmpeg.
- ejecute Rust y pruebas de medios.
- generar fragmentos del manifiesto del actualizador.
- fusionar fragmentos en `latest.json`.
- cargue instaladores, paquetes de actualización, firmas y `latest.json`.
- validar macOS Firma de ID de desarrollador, notarización, grapado y Gatekeeper
aceptación antes de publicar artefactos macOS.
- publicar artefactos Windows 0.9.5 como vistas previas sin firmar; futuro firmado Windows
Las versiones deben validar el firmante de Authenticode y el estado de la marca de tiempo antes de
publicar artefactos Windows.
- Ejecute instalar controles de humo después de la publicación.
- ejecute el actualizador macOS de identidad/humo de reemplazo en `macos-26`.

El endurecimiento de versiones futuras debería agregar:

- real Windows y Linux instalan pruebas de humo en máquinas físicas o VM.
- una verificación de retención de subvenciones de TCC manual o con máquina limpia a través de una actualización pública.
- Windows Verificaciones de reputación de SmartScreen en máquinas limpias.

## Brechas conocidas

- Aún no existe un paquete integral de accesibilidad automatizada.
- Aún no hay un conjunto de pruebas completo de i18n/l10n.
- Aún no hay un paquete de salida visual dorado para ajustes preestablecidos.
- Aún no hay una prueba comparativa de latencia de cámara automatizada.
- Se incluyen análisis, mapeo, eventos falsos y ensamblaje SysEx experimentales de MIDI.
automatizado; Los barridos de control físico y la restauración del banco completo aún requieren la
Equipo UC-33e/mioXC.
- La cobertura de medios/cámaras/audio nativos de Linux necesita pruebas automáticas más amplias.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
