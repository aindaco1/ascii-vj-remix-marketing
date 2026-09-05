---
title: Pruebas
description: Documentación de prueba derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Operaciones
lang: es
---

# Pruebas

Esta guía documenta las verificaciones automatizadas actuales, las rutas de verificación manual y las brechas de cobertura conocidas para ASCII VJ Remix.

Las pruebas se centran en paquetes fuera de línea, inicio del renderizador, cambio de fuente, salida nativa, comportamiento de medios/cámara/audio, permisos Tauri, sidecars FFmpeg, artefactos de lanzamiento y manifiestos de actualización.

## Referencia rápida

```bash
npm run build                    # Vite production build plus local asset copy
npm run check:offline            # Build and verify bundled/offline assets
npm run smoke:static             # Static UI/renderer smoke harness
npm run check:tauri-policy       # Production CSP and local-only runtime policy
npm run check:icons              # Canonical source and generated platform icons
npm run check:glyph-atlas        # Unicode atlas manifest, dimensions, source, hashes
npm run test:output-display      # Secondary-display placement simulation
npm run test:desktop-updater     # Once-per-launch and manual updater orchestration
npm run test:updater-manifest    # Tauri latest.json/updater manifest tests
npm run test:macos-identity      # macOS bundle/team/designated-requirement tests
npm run test:macos-secret-args   # macOS notarization secret argument safety
npm run test:ffmpeg-policy       # FFmpeg policy checks
npm run check:ffmpeg-resources   # FFmpeg sidecar resource metadata checks
npm run test:frame-prep          # Rust/JS frame-prep parity
npm run test:decode-resize       # Decode/resize parity checks
npm run check:media              # Media pipeline checks
npm run test:render-math         # Shared renderer math vectors
npm run test:canvas-readback     # Contained success and blocked Canvas2D readback
npm run test:renderer-fallback   # GPU-to-Canvas fallback and bounded diagnostics
npm run test:preset-playlists    # Playlist schema, bounds, reorder, loop selection
npm run test:audio-reactive      # Audio-reactive controls, clamps, dense-mix damping
npm run test:midi                # UC-33e map, scaling, pickup, actions, coalescing
npm run midi:probe -- --connect  # Physical mioXC input/output open test
npm run test:crash-report-ui     # Reports visibility, count, and action-state tests
npm run test:crash-relay         # Cloudflare crash relay sanitizer/rate-limit tests
npm run test:vectors             # Adaptive codec vector checks
npm run test:rust                # Rust tests
npm run check:desktop            # Main desktop validation gate
npm run check:release            # Release-oriented gate; expects staged FFmpeg sidecar
npm run bundle:debug             # Build and validate local debug bundle
npm run bundle:test              # Windows release-profile dev installer + GUI check
npm run bundle:test:linux        # Linux release-profile dev AppImage/deb/rpm
npm run bundle:release           # Release gate, release build, bundle check
npm run check:windows-authenticode # Inactive signed-Windows path signature check
npm run check:windows-gui        # Require the release EXE GUI subsystem
npm run smoke:native-output      # Native output performance helper
npm run smoke:ui-perf            # UI performance helper
npm run smoke:primary-presets    # Installed WebKit primary-view preset sweep
npm run bench:density            # Optimized density/feature comparison reports
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
|Arnés de interfaz de usuario estática|`npm run smoke:static`, que incluye activación, limpieza de perfil predeterminada, búsqueda de ajustes preestablecidos en vivo, edición/guardado/reordenamiento/controles de bucle de listas de reproducción, interfaz de usuario de captura de pantalla nativa accesible, geometría de selección alineada, salida visible, errores de WebGL, finalización de páginas de glifos y comprobaciones de aspecto para cada ajuste preestablecido de Demo Image integrado.|
|Política Tauri|`npm run check:tauri-policy`|
|Iconos de aplicaciones|`npm run check:icons`|
|Atlas de glifos Unicode|`npm run check:glyph-atlas`, afirmaciones de bloque completo en pruebas matemáticas del renderizador/Rust|
|Lógica de visualización de salida|`npm run test:output-display`|
|Listas de reproducción preestablecidas|`npm run test:preset-playlists`, además de alineación de token de control renderizada, creación sin avisos, evitación de ajustes preestablecidos activos, despido modal, estado de transición veraz, enrutamiento de transición compartido y cobertura de inicio/detención en `npm run smoke:static`|
|Comportamiento del actualizador de escritorio|`npm run test:desktop-updater`|
|Manifiestos del actualizador|`npm run test:updater-manifest`|
|Identidad de la aplicación macOS|`npm run test:macos-identity`, libera inspección de artefactos en macOS|
|Manejo de secretos macOS|`npm run test:macos-secret-args`|
|FFmpeg política/recursos|`npm run test:ffmpeg-policy`, `npm run check:ffmpeg-resources`, `npm run check:ffmpeg-release`|
|Preparación/decodificación de fotogramas multimedia|`npm run test:frame-prep`, `npm run test:decode-resize`, `npm run check:media`|
|Matemáticas del renderizador/retroceso|Pruebas de vector compartido `npm run test:render-math`, `npm run test:renderer-fallback`, Rust a través de `npm run test:rust`|
|MIDI|`npm run test:midi`, Rust MIDI/Pruebas SysEx, `npm run midi:probe -- --connect`|
|Informes de fallos|`npm run test:crash-report-ui`, `npm run test:crash-relay`|
|Vectores de códec adaptativos|`npm run test:vectors`|
|Módulos Rust/Tauri|`npm run test:rust`|
|Rendimiento de salida nativa|`npm run smoke:native-output`, `npm run test:native-output-log`|
|Rendimiento de la interfaz de usuario|`npm run smoke:ui-perf`, `npm run bench:density` con transiciones/valores predeterminados fijos, configuración de funciones, percentiles de fase, reemplazos de renderizador y restablecimientos de fotogramas|
|Ajustes preestablecidos primarios instalados|`npm run smoke:primary-presets`, los 71 integrados en Demo Image con visibilidad primaria por ajuste preestablecido, familia de backend, estado de ejecución, error GPU y verificaciones de aspecto|
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

Agregue comprobaciones manuales para cambio de fuente, transiciones preestablecidas, WTF mode y reactividad de audio cuando cambia el comportamiento.

### Cambios en el backend del renderizador

```bash
npm run build
npm run test:render-math
npm run test:renderer-fallback
npm run check:glyph-atlas
npm run smoke:static
npm run check:media
```

También compare manualmente la salida de WebGPU y WebGL2 para determinar los estados representativos de desactivación de funciones, paleta/difusor, Braille, CJK/Kana, Hangul y de rampa personalizada escrita. Registre el backend real; un backend solicitado que retrocede no es evidencia del backend solicitado.

### Salida nativa o cambios Pop Out

```bash
npm run test:output-display
npm run smoke:native-output
npm run test:native-output-log
npm run test:rust
```

Utilice una compilación de aplicación optimizada antes de sacar conclusiones sobre el rendimiento. El humo del rendimiento de la interfaz de usuario comienza a partir de valores predeterminados visuales canónicos, utiliza transiciones numéricas no estructurales fijas, registra cada backend visitado y rechaza un lienzo primario sin señal de píxeles visible incluso cuando su contador FPS avanza. Configure `ASCILINE_UI_PERF_SMOKE_STRUCTURAL=1` para alternar familias de renderizadores de glifos y sólidos y ejercite la ruta de fundido cruzado nativo de reloj compartido. Seleccione un paquete exacto y una muestra más larga con:

```bash
ASCILINE_SOURCE_APP="/absolute/path/ASCII VJ Remix.app" \
ASCILINE_UI_PERF_SMOKE_DURATION_MS=30000 \
npm run smoke:ui-perf
```

Para cambios preestablecidos principales, `npm run smoke:primary-presets` es la puerta de aceptación Apple WebKit instalada. La matriz Chromium `smoke:static` sigue siendo útil pero no sustituye a este barrido de escritorio. El muestreador de señal conserva un límite máximo de 960x540, por lo que se evalúan máscaras Unicode escasas de un píxel antes de que una pequeña miniatura pueda promediarlas en el fondo.

El análisis de registros nativos informa tanto de las tasas de carga de origen como de carga y omisión. Una fuente saludable de 24 FPS en una pantalla de 60 Hz carga cerca de la frecuencia de la fuente y omite los ticks de visualización duplicados mientras la presentación permanece cerca de la frecuencia de actualización. Para cambios en el modo de glifo, incluya ASCII tradicional, Braille, CJK/Kana, Hangul y una rampa de tipo mixto en las comprobaciones principales/Pop Out. Confirme que las páginas del atlas se carguen solo para la rampa activa, que se informen los escalares no admitidos y que los cambios en el conjunto de caracteres/familia de fuentes no oculten los controles de glifo.

Para la cámara Pop Out, verifique el modo de salida resuelto y el movimiento visible. macOS, Windows y Linux deben seleccionar `native-camera` para una cámara. Varias cámaras deben seleccionar `mirror`; Windows/Linux también debería volver a intentar reflejar cuando la verificación previa nativa no pueda producir un marco. En Windows físico, confirme los avances de la imagen de la cámara tanto en la ventana principal como en la de Pop Out con `exclusiveCameraActive` verdadero. En esa sesión de propietario único, confirme que `nativeOutputPreview.transport` es `binary-jpeg`, ambas vistas avanzan y la cámara del navegador se vuelve a adquirir después del cierre sin cambiar las fuentes. `test:output-display` ejecuta el orden de transferencia de origen Windows y las pruebas de regresión geométrica de vista previa; `smoke:static` renderiza aparatos con vista previa nativa 4:3/16:9 y comprueba sus bordes derechos. Utilice `SMOKE_REQUIRE_WEBGPU=1` en un tiempo de ejecución de prueba compatible con WebGPU para rechazar el respaldo y ejercitar el reemplazo de texturas de WebGPU. En Linux, confirme los avances nativos de Pop Out mientras la vista previa exclusiva de WebView está en pausa y que la vista previa se vuelve a adquirir después del cierre. Capture un informe manual del cuadro de diálogo Reports existente; una simulación de política local no reemplaza la aceptación del dispositivo.

En Windows y Linux, mantenga también abierto Pop Out mientras cambia repetidamente entre Demo Image, Demo Video y Cámara. Cada cambio de modo debe finalizar el trabajador nativo anterior antes de que se reutilice la ventana de salida compartida. Cierre y vuelva a abrir inmediatamente Pop Out después de esa secuencia; la aplicación no debe entrar en pánico en una superficie `wgpu` no válida ni poner en cola un informe `underlying handle is not available` durante el desmontaje normal.

Para cambios de salida de color, compare los estados de paleta, brillo, contraste, fondo y escala de grises neutral entre principal y Pop Out. El conjunto de unidades Rust requiere que el selector de superficie nativo prefiera formatos no normales que no sean sRGB incluso cuando la plataforma informa primero un formato sRGB.

Para el contrato de densidad normal 0.9.11, ejecute compilaciones optimizadas con funciones activadas y desactivadas coincidentes en 640 columnas con audio sintético y salida nativa:

```bash
ASCILINE_UI_PERF_SMOKE_BACKEND=webgl2 \
ASCILINE_DENSITY_BENCH_COLUMNS=640 \
ASCILINE_DENSITY_BENCH_REPORT_PATH=/tmp/feature-off.json \
npm run bench:density

ASCILINE_UI_PERF_SMOKE_BACKEND=webgl2 \
ASCILINE_UI_PERF_SMOKE_PALETTE=signal-court \
ASCILINE_UI_PERF_SMOKE_DITHER=bayer4 \
ASCILINE_UI_PERF_SMOKE_CHARSET=cjk-basic \
ASCILINE_DENSITY_BENCH_COLUMNS=640 \
ASCILINE_DENSITY_BENCH_REPORT_PATH=/tmp/feature-on.json \
npm run bench:density
```

`bench:density` es una puerta de liberación: sale de un valor distinto de cero cuando falla cualquier humo de UI infantil, cuando su informe no es aceptado o cuando el RSS constante crece más que el valor mayor de 64 MB y 25 por ciento después del calentamiento. Una ejecución de macOS cuyas ventanas están en segundo plano puede ser útil para probar la vida útil de la memoria, pero su velocidad de fotogramas limitada no debe registrarse como aceptación del rendimiento de la ventana visible.

### Cambios en MIDI, UC-33e o SysEx

```bash
npm run test:midi
npm run check:tauri-policy
npm run test:rust
npm run midi:probe -- --connect
npm run smoke:static
```

La sonda física verifica que CoreMIDI pueda enumerar y abrir simultáneamente ambas direcciones del mioXC. No reemplaza el barrido de control y la lista de verificación de captura/restauración de banco completo en [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

### Tauri Comandos, permisos o capacidades

```bash
npm run check:tauri-policy
npm run test:crash-relay
npm run test:rust
npm run check:desktop
```

La puerta de política también verifica que cada comando invocado por el adaptador de escritorio tenga un permiso Tauri generado y una concesión en la capacidad de la ventana principal. Un comando Rust registrado en `generate_handler!` no se puede llamar desde una vista web empaquetada hasta que existan ambas partes de ACL.

Verifique manualmente el comportamiento de la cámara macOS, el micrófono, la pantalla/sistema de audio y Pop Out cuando cambie el modelo de permiso.

Para los cambios en los informes de fallos, verifique también que las compilaciones de depuración se capturen localmente pero no las envíen, que las compilaciones de lanzamiento utilicen solo `https://crash.dustwave.xyz/v1/reports` y que la ventana de salida no tenga permisos de informes de fallos. El control Reports permanece visible con una cola vacía, los diagnósticos de medios locales nunca se envían y los informes del procesador contienen solo el resumen de eventos estructurado delimitado. La salida de Windows WebView2 GPU aún requiere la aceptación física de Windows además de estas comprobaciones de contratos multiplataforma.

La aceptación manual del informe debe comenzar con una cola vacía: ingrese una nota breve, capture el estado actual, confirme que la vista previa contiene un informe `manual-diagnostic` y un contexto de salida/representador limitado, luego confirme que una compilación de desarrollo mantiene el envío deshabilitado. Verifique por separado el envío de producción sin adjuntar medios, capturas de pantalla, rutas de archivos, URL o registros de procesos arbitrarios.

La prueba 2026-08-29 Windows 11 estableció que Signal Court y Midnight Scan CJK podían inicializarse en blanco tanto en WebGPU como en WebGL2, mientras que la ruta sólida/píxel de Neon Sledgehammer permanecía visible y la cámara se abría sin un informe de diagnóstico de medios falso. La regla general de glifo a lienzo Windows ahora se eliminó después de la reparación de la textura de glifo compacto. Vuelva a verificar los ajustes preestablecidos representativos de ASCII, Braille, CJK, Hangul, sólidos y de píxeles en el instalador de reemplazo antes de fusionarlos.

La matriz preestablecida estática también verifica la propiedad del backend: el estado limpio y las funciones integradas sin un backend de compatibilidad explícita retienen Auto y se resuelven en WebGPU/WebGL2 en el tiempo de ejecución de humo Chromium capaz. El barrido preestablecido empaquetado por separado requiere el contrato de propiedad de Canvas centralizado 71 en total / 43 acelerado / 28 explícito. El carril CI Windows ejecuta toda la matriz visible; La aceptación física de Windows también debe confirmar que los 43 ajustes preestablecidos acelerados se resuelven en WebGPU en la máquina RTX de destino y permanecen visibles.

El mismo humo genera muestras de colores conocidas a través de WebGL2 real y las compara con el asignador de paletas compartido para las 17 paletas en los modos más cercano y de luminancia, incluidos los cambios de paleta en vivo y de inicio. También verifica que las cargas de paletas conserven la configuración de orientación de la imagen de origen.

### FFmpeg y motor de medios

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
npm run check:media
npm run test:rust
```

`test:media-source-policy` cubre tanto la selección de la plataforma Demo Video como los identificadores de fuente empaquetados exactos elegibles para el respaldo nativo de FFmpeg. La suite Rust rechaza los identificadores agrupados transversales y no reconocidos. La aceptación física de Linux aún debe demostrar que una falla de decodificación de vista web alcanza el respaldo y muestra cuadros en avance.

Para sidecars de lanzamiento:

```bash
npm run test:ffmpeg-source-build
npm run check:ffmpeg-release
```

### Lanzamiento y actualizador

```bash
npm run test:desktop-updater
npm run check:release
npm run bundle:release
npm run smoke:release-install
npm run test:macos-dmg-layout
```

Ejecute `npm run ffmpeg:build-sidecar` antes que `npm run check:release` en un clon limpio. `npm run bundle:release` ejecuta el paso de compilación del sidecar automáticamente.

El humo de lanzamiento descarga artefactos de los lanzamientos GitHub y verifica el diseño del instalador, los activos incluidos, los paquetes de actualización firmados, el comportamiento de `latest.json`, los controles empaquetados visibles Update y Reports y la ausencia de una lectura de backend duplicada en la barra superior. En macOS, verifica el DMG descargado, lo monta como de solo lectura en una raíz temporal privada, valida el diseño exacto de la aplicación a las aplicaciones e inspecciona la aplicación montada antes del salto del actualizador.

Si la publicación del artefacto se realiza correctamente pero un ejecutor posterior a la publicación expone un defecto en las herramientas de aceptación, ejecute el flujo de trabajo `Release Acceptance` con la etiqueta inmutable existente después de corregir las herramientas. Reutiliza los bytes publicados y no reconstruye ni reemplaza los activos de lanzamiento. Updater-hop smoke usa `0.9.0` como la versión anterior mínima predeterminada porque las versiones anteriores de `0.1.x` se firmaron con una clave de actualización diferente.

La prueba del controlador verifica que la disponibilidad de producción permita exactamente una verificación silenciosa por lanzamiento, que los resultados actuales/fuera de línea no anuncien el estado, que una actualización disponible no se instale automáticamente y que la ruta manual existente aún realice nuevas verificaciones e instalaciones activadas por el usuario.

Las versiones 0.9.6 y 0.9.7 se enviaron sin la capacidad de nombre de aplicación de la ventana principal utilizada por la puerta de disponibilidad del actualizador, por lo que su control Update puede parpadear y luego desaparecer. Instale 0.9.8 manualmente desde el DMG notariado. Reinicie 0.9.8 y confirme que la verificación de inicio de la versión actual permanece silenciosa mientras el control Update permanece visible, luego use el control y confirme que informa `Up to date`. Para la versión 0.9.10, inicie la aplicación 0.9.9 instalada y confirme que la verificación de antecedentes aparezca en la versión 0.9.10 sin descargarla automáticamente. Después de la instalación aprobada por el usuario, confirme que el ícono de la nueva aplicación esté presente, que Reports permanezca visible en su estado vacío o de recuento pendiente y que la lectura del backend del lado derecho esté ausente.

En macOS, Release Smoke extrae las cargas útiles actuales y anteriores de `.app.tar.gz`, requiere `com.asciline.remix`, ID de equipo `PWT3Q52LZ2`, tiempo de ejecución reforzado, aceptación de Gatekeeper y exactamente el mismo requisito designado, luego ejecuta la aplicación anterior a través del actualizador y revalida el paquete reemplazado. La aprobación interactiva del TCC en sí sigue siendo una verificación manual.

## Lista de verificación manual de humo

Úselo después de realizar cambios en el renderizador, la fuente, el audio o la salida de cara al usuario:

1. Inicie la aplicación de escritorio.
2. Confirme que aparece la imagen de demostración y el renderizador se inicia automáticamente.
3. Cambie a Vídeo de demostración y confirme que comienza la reproducción.
4. Vuelva a la imagen de demostración y confirme que el renderizador no se atasca.
5. Seleccione Cámara y confirme la solicitud de permiso/comportamiento del dispositivo.
6. Seleccione Micrófono/Entrada y confirme que se inicia la reactividad de audio o solicita permiso. Sin un dispositivo de entrada disponible, confirme el estado amigable inactivo y que Reports permanezca vacío, incluso después de reiniciar en una cola anterior.
7. Cambie de dispositivo de audio y confirme que la captura se reinicia automáticamente.
8. Activar pantalla/audio del sistema cuando sea compatible y confirmar errores son útiles cuando la fuente seleccionada no tiene pista de audio.
9. Haga clic en varios ajustes preestablecidos y confirme transiciones suaves.
10. Seleccione un ajuste preestablecido ASCII tradicional y confirme que el conjunto de caracteres y la familia de fuentes permanezcan compactos y visibles.
11. Seleccione ajustes preestablecidos de paleta/dither más Braille, Hiragana, Katakana, CJK, Hangul y una rampa personalizada mixta; confirme que main y Pop Out permanecen en paridad.
12. Cambie Advanced Density y confirme que el modo normal regresa al techo protegido; Confirme que la preferencia no se copia en un ajuste preestablecido visual.
13. Active y desactive WTF mode y confirme que sigue respondiendo y puede visitar estados tradicionales de aspecto ASCII.
14. Abra Pop Out y confirme que la vista previa principal sigue respondiendo.
15. Confirme que Pop Out refleja los ajustes preestablecidos, WTF mode y la reactividad de audio mientras está completamente visible, y que sus colores coinciden con la vista previa principal.
16. Confirmar superposición de estadísticas informa el valor preestablecido/fuente/backend/grid/FPS activo.
17. Cierre Pop Out y confirme que se establezca el uso de CPU/GPU.
18. Con una cámara seleccionada en Windows, capture un diagnóstico manual mientras Pop Out está abierto y confirme que `cameraFallbackActive` sea falso. Confirme que la salida en vivo se mantiene fluida mientras cambia los ajustes preestablecidos y FPS. Con `exclusiveCameraActive`, confirme los avances de la vista previa principal a través de `nativeOutputPreview`, su FPS aceptado es distinto de cero y la vista previa normal de la cámara se restaura después de cerrar con `previewRestoreSucceeded` aumentando. Si se activa la copia de seguridad del espejo, confirme que `nativeOutputAdapter.nativeCameraFailureReason` explica el motivo y se volverá a adquirir la vista previa.
19. Repita la prueba de una sola cámara en Ubuntu con AppImage/deb y Fedora con rpm. La vista previa de la cámara principal puede pausarse mientras V4L2 sea propiedad del Pop Out nativo; confirme que se restaure después del cierre. Si se activa la reserva, confirme que se vuelva a adquirir la vista previa y que el informe incluya el espejo distinto de cero aceptado FPS.

## Comprobaciones de hardware y plataforma

La aplicación depende del hardware real y de las pilas de medios del sistema operativo. Las pruebas automatizadas no cubren todas las combinaciones de hardware y plataforma.

Matrices manuales importantes:

- macOS Apple Silicon con cámara integrada y pantalla externa.
- macOS con cámara USB externa.
- macOS con sistema de captura de audio.
- Windows con WebView2, D3D12/WebGL2, cámara, micrófono y ruta de instalación.
- Linux con aceleración WebKitGTK, GPU, cámara, micrófono y rutas AppImage/deb/rpm. La matriz de VM mantenida y la lista de verificación de paquetes se encuentran en [Linux VM QA](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/LINUX_VM_QA.md).
- Equipo experimental macOS Apple Silicon MIDI: Evolution/M-Audio UC-33e a través de ambas direcciones DIN de un iConnectivity mioXC, alimentado por separado.

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

Podman es principalmente para un shell de desarrollo reproducible similar a Linux y trabajo heredado de Python/OpenCV/vector. No es el tiempo de ejecución de producción.

Comandos útiles:

```bash
scripts/podman-doctor.sh
scripts/podman_build.sh
scripts/podman_venv.sh
scripts/podman_codec_tests.sh
```

La imagen de Podman tiene como valor predeterminado el Nodo 24. Utilice `NODE_MAJOR=26` solo cuando pruebe explícitamente una línea base de Nodo más nueva.

## CI y comportamiento de liberación

Lanzamiento de CI:

- requiere una ejecución exitosa de la inserción principal `Desktop` para la confirmación de lanzamiento exacta.
- Compile la aplicación y cree FFmpeg simultáneamente en macOS, Windows y Linux, luego verifique y reutilice esas entradas exactas para empaquetar solo en paquetes.
- verificar el comportamiento del paquete sin conexión.
- verificar la política Tauri.
- construir/comprobar sidecars FFmpeg.
- ejecute Rust y pruebas de medios.
- generar fragmentos del manifiesto del actualizador.
- fusionar fragmentos en `latest.json`.
- cargue instaladores, paquetes de actualización, firmas y `latest.json`.
- valide la firma de ID del desarrollador macOS, la certificación notarial, el grapado y la aceptación del Gatekeeper antes de publicar los artefactos macOS.
- publica artefactos Windows como vistas previas sin firmar; la ruta Windows firmada inactiva incluye el firmante de Authenticode y la validación de marca de tiempo.
- marca el ejecutable de la versión Windows como una aplicación GUI e inicia FFmpeg/ffprobe sin consolas secundarias visibles.
- ejecute comprobaciones de humo de instalación y de interfaz de usuario de actualización visible después de la publicación.
- ejecute el actualizador macOS de identidad/humo de reemplazo en `macos-26`.

## Brechas conocidas

- No existe un paquete integral de accesibilidad automatizada.
- No hay un conjunto de pruebas completo de i18n/l10n.
- No hay un paquete de salida visual dorado para ajustes preestablecidos.
- Sin punto de referencia de latencia de cámara automatizado.
- El análisis experimental de MIDI, el mapeo, los eventos falsos y el ensamblaje de SysEx están automatizados; Los barridos de control físico y la restauración del banco completo aún requieren el equipo UC-33e/mioXC.
- La cobertura de audio/cámara/medios nativos de Linux está limitada fuera de CI.

El seguimiento del lanzamiento potencial, la plataforma, la accesibilidad, la localización y la cobertura de rendimiento se realiza en [Roadmap](/es/docs/reference/roadmap/).


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
