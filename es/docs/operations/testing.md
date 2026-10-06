---
title: Pruebas
description: Documentación de prueba derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Operaciones
lang: es
---

<a id="testing"></a>

# Pruebas

Esta guía documenta las verificaciones automatizadas actuales, las rutas de verificación manual y las brechas de cobertura conocidas para ASCII VJ Remix.

Las pruebas se centran en paquetes fuera de línea, inicio del renderizador, cambio de fuente, salida nativa, comportamiento de medios/cámara/audio, permisos Tauri, sidecars FFmpeg, artefactos de lanzamiento y manifiestos de actualización.

<a id="quick-reference"></a>

## Referencia rápida

```bash
npm test                         # Desktop gate, static smoke, live synthetic Jev review
npm test -- --offline            # Same deterministic checks, explicitly skip Jev
npm run test:jev -- --dry-run     # Preview requests without credentials or network
npm run test:jev-harness          # Offline evaluator and workflow regression tests
npm run build                    # Vite production build plus local asset copy
npm run check:offline            # Build and verify bundled/offline assets
npm run smoke:static             # Static UI/renderer smoke harness
npm run test:smoke-diagnostics    # Failure capture, bounded waits, and artifact-write failures
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

<a id="jev-development-testing"></a>

## Pruebas de desarrollo Jev

`npm test` es la entrada habitual para las pruebas de desarrollo. Ejecuta las pruebas del evaluador Jev, las comprobaciones de `check:desktop`, `smoke:static` y, por último, la evaluación de Jev alojada. Si falla un paso, se detiene el proceso; Jev nunca invalida un fallo determinista. Estas comprobaciones compilan un binario de desarrollo, pero no lo empaquetan, instalan, etiquetan ni publican. `npm test -- --offline`, también disponible como `npm run test:offline`, omite solo la evaluación alojada e indica que no se ejecutó la evaluación semántica. Los comandos específicos y las comprobaciones de publicación conservan su comportamiento. Desktop CI prueba el evaluador sin conexión y no dispone de credenciales de Jev.

El evaluador usa los helpers existentes de fallback e informes del renderizador, la captura de diagnósticos de las pruebas de humo y el controlador de actualizaciones con entradas sintéticas fijas. Seis resultados comprueban las diferencias entre recuperación y fallo, inicialización y carga del documento, ausencia de diagnóstico y fallo original, y actualización disponible e instalación correcta o comprobación fallida. Primero se ejecutan las aserciones exactas. Catorce controles positivos y negativos etiquetados preceden a los seis casos de comportamiento. Son simulaciones de componentes: no prueban cámaras reales, presentación nativa, calidad de imagen ni transacciones reales del actualizador. Las pruebas de humo en navegador se ejecutan por separado. El comando Jev no acepta informes arbitrarios, capturas, archivos de código, medios del usuario, datos de cámara o audio ni registros privados.

<a id="setup-and-commands"></a>

### Configuración y comandos

```bash
git submodule update --init shared/dust-wave-platform
npm ci
npm run test:jev -- --dry-run
npm run test:jev
npm test
```

Configure `CLOUDFLARE_ACCOUNT_ID` en el entorno o coloque solo el ID de cuenta en el `.ascii-vj-development.json` ignorado como `{"cloudflare_account_id":"YOUR_ACCOUNT_ID"}`. Configure `CLOUDFLARE_API_TOKEN` en el entorno o utilice un inicio de sesión de Wrangler existente. El adaptador utiliza la dependencia Wrangler anclada del repositorio; `--wrangler-auth` selecciona explícitamente ese inicio de sesión. No se guarda ningún token en la configuración o en los informes. La falta de autenticación es un error, nunca un pase silencioso sin conexión.

El comando alojado envía como máximo 20 solicitudes con 20 preguntas atómicas y un límite total de 64.000 bytes. Las solicitudes son secuenciales, tienen un tiempo máximo de 45 segundos y se detienen ante el primer error del proveedor, sin reintentos ni compras de créditos. Revisa la vista previa exacta antes de ampliar el corpus; el uso se factura a la cuenta configurada del proveedor. Los límites de solicitudes no garantizan un precio concreto. Jev utiliza [preguntas tipadas](https://docs.typesafe.ai/introduction) a través de Cloudflare, con cabeceras que solicitan omitir caché y registros; esas cabeceras no demuestran la política de retención del proveedor.

<a id="results-and-shared-ownership"></a>

### Resultados y propiedad compartida

Cada ejecución crea un directorio nuevo, excluido de Git, en `jev-results/<timestamp>/`, o en la ubicación nueva indicada con `--output-dir`. Conserva solicitudes, hashes del código, respuestas parciales y originales, el `report.json` final y `review.md`. Rechaza directorios de salida existentes. Las simulaciones no intentan acceder a la red, permanecen incompletas y se identifican como `dry-run`. Los códigos de salida son 0 para éxito o vista previa, 1 para fallo o revisión y 2 para error de configuración o proveedor. `releaseAccepted` siempre es false.

Los resultados casi empatados, con margen inferior a 0,10, las respuestas inciertas, las versiones no reconocidas del evaluador o los controles con respuestas conocidas incorrectas requieren revisión y producen un código de salida distinto de cero. Inicialmente solo se reconoce `jev-1.13.0`. El margen es provisional para estos casos etiquetados por ingeniería; no hereda la calibración de CutNotes ni demuestra fiabilidad general. No cambies los prompts ni los umbrales solo para obtener un resultado positivo. Usa los controles observados como pruebas de regresión y reserva ejemplos nuevos antes de afirmar que hay calibración tras modificar los prompts.

La primera ejecución local detectó un falso positivo en un control negativo de captura de diagnósticos y solicitó revisión correctamente. La pregunta general sobre distinguir fallos se sustituyó por el requisito explícito de conservar el arranque del renderizador como fallido; se fijaron dos formulaciones nuevas antes de repetir la evaluación. Sin cambiar el umbral, la nueva ejecución superó los 14 controles y los seis casos de comportamiento en Jev 1.13.0. Se conservan ambas ejecuciones como evidencia local. Esta verificación es limitada y no demuestra calibración independiente ni aceptación en hardware físico. El [registro de verificación de la integración](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/testing/JEV_EVALUATION.md) conserva los resultados exactos, los hashes y los límites de limpieza.

La construcción de solicitudes, el transporte de Cloudflare, la validación de respuestas y la decisión de solicitar revisión reutilizan Platform Test Core mediante la entrada pública `test-core/jev`. [platform-desktop.json](https://github.com/aindaco1/ascii-vj-remix/blob/main/platform-desktop.json) define el commit inmutable actual y las versiones exactas de los paquetes. La integración original usaba Test Core 0.3.0 de [Platform PR 46](https://github.com/aindaco1/dust-wave-platform/pull/46); sus resultados fechados permanecen en el registro de verificación. El adaptador rechaza una copia de Platform con otra revisión o cambios locales. ASCII VJ mantiene su corpus, autenticación, límites, informes y ejecución de comandos. No importa otro proyecto vecino, copia un cliente del modelo, añade una dependencia npm, llama al modelo desde la app ni cambia la versión de la app. No se copia el repositorio compartido en `dist`. El evaluador verifica Test Core 0.3.1, pero todavía escribe `0.3.0` en el campo `testCoreVersion` del informe. Hasta que se corrija ese metadato, usa `platformCommit`, los hashes del código y el manifiesto para verificar la procedencia de las dependencias.

Para revertir únicamente Jev, elimina conjuntamente sus cuatro scripts de prueba, comandos, paso de pruebas de CI y documentación. Conserva el submódulo de Platform y el manifiesto: el actualizador y el relay también los usan. Consulta la [migración de servicios de escritorio compartidos](/es/docs/development/shared-desktop-services/#independent-rollback) para revertir esa integración por separado. No se requiere migración de la aplicación ni de datos.

<a id="test-categories"></a>

## Categorías de prueba

|Área|Comprobaciones actuales|
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
|Ajustes preestablecidos primarios instalados|`npm run smoke:primary-presets`: los 96 presets integrados sobre Demo Image, comprobando para cada uno visibilidad en el preview principal, familia de backend, estado de ejecución, errores GPU y proporción de imagen|
|Lanzamiento de instalación/actualización|`npm run smoke:release-install`|

<a id="recommended-check-sets"></a>

## Conjuntos de comprobaciones recomendados

<a id="documentation-only"></a>

### Sólo documentación

```bash
git diff --check
```

Para guías movidas o divididas, verifique también los enlaces de archivos relativos, los anclajes de encabezado y las referencias de flujo de trabajo/script a las rutas anteriores. Incluya los nuevos archivos en la validación del enlace; `git diff --check` solo detecta errores de espacios en blanco. El [índice de documentación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md#maintaining-documentation) define la propiedad.

<a id="frontend-ui-css-presets-sources-audio-ui"></a>

### Interfaz de usuario frontal, CSS, ajustes preestablecidos, fuentes, interfaz de usuario de audio

```bash
npm run build
npm run smoke:static
```

Agregue comprobaciones manuales para cambio de fuente, transiciones preestablecidas, WTF mode y reactividad de audio cuando cambia el comportamiento.

La prueba de humo estática muestra la versión del navegador y el nombre de su ejecutable. Si falla, conserva el error original, la fase actual, un conjunto acotado de errores de consola y de página, solicitudes fallidas y errores HTTP, y el estado de arranque de cada página de prueba. Las URL omiten credenciales, parámetros de consulta y fragmentos. La captura de estado y de pantalla tiene tiempos máximos de espera para que una página bloqueada no impida registrar el fallo. El navegador se cierra tanto al terminar correctamente como al fallar.

Cada ejecución fallida guarda `failure.json` y, cuando es posible, capturas de pantalla en una carpeta con marca de tiempo dentro de `tmp-smoke-static/`. Use `SMOKE_DIAGNOSTICS_DIR` para elegir otro directorio. Estos contextos nuevos del navegador contienen datos sintéticos de prueba; los diagnósticos no vuelcan el almacenamiento, las variables de entorno ni el DOM completo. El trabajo Windows Desktop sube los diagnósticos como artefacto independiente durante siete días. Esto no reduce los límites de tiempo de inicio, las comprobaciones del renderizador visible ni el contrato de presets 96/68/28.

<a id="audio-response"></a>

### Respuesta al audio

Ejecute `npm run test:audio-reactive` para comprobar modulación acotada, ataques inmediatos, caída independiente de la tasa de fotogramas, suavizado cero, una sola lectura nativa en curso, lecturas duplicadas y carreras entre parada y reinicio. `npm run test:rust` también comprueba la selección del búfer nativo, la detección de ataques y la caída de pulsos con distintos tamaños de búfer. Las pruebas de inicio retrasan los permisos del navegador, la reanudación de AudioContext, la reproducción de archivos y los comandos nativos para verificar cancelación, liberación de pistas y Stop/Start rápidos. Cubren la restauración de ajustes de presets y las ediciones de audio durante la preparación de transiciones nativas. La prueba estática cubre cambios de fuente y dispositivo de captura, ajustes en vivo y responsabilidad sobre los parámetros efectivos de Pop Out en estado estable y durante transiciones, además de la etiqueta Custom y la reselección mediante los controles reales de audio. `npm run test:renderer-resources` comprueba que el fotograma decodificado siga vivo hasta el envío a GPU, la liberación de recursos tras fallos y la recuperación del bucle de animación.

Tras compilar la aplicación Dev optimizada, puede ejecutar una prueba local de tiempos de entrada nativa junto con las comprobaciones existentes de rendimiento de video, Pop Out y transiciones:

```bash
ASCILINE_UI_PERF_SMOKE_NATIVE_AUDIO=1 \
ASCILINE_UI_PERF_SMOKE_FOREGROUND=1 \
ASCILINE_UI_PERF_SMOKE_COLUMNS=640 \
ASCILINE_UI_PERF_SMOKE_DURATION_MS=15000 \
ASCILINE_UI_PERF_REPORT_PATH=/tmp/ascii-native-audio.json \
npm run smoke:ui-perf
```

Mantenga visibles la aplicación y Pop Out durante la prueba. Se usa el micrófono o entrada nativa seleccionado con el permiso habitual del sistema. Los errores nuevos del frontend hacen fallar la prueba; los informes guardados existentes se conservan. Se registra la duración de la ventana de análisis, el tiempo de ida y vuelta por IPC y un límite de antigüedad de las características al recibirlas: su edad en la instantánea nativa más el viaje completo. No se graba audio sin procesar ni se mide la latencia física del sonido a la pantalla. Compare el renderizado con los umbrales existentes sin rebajarlos para obtener un resultado. La escucha física, los tiempos de la interfaz de audio o loopback, la captura del sistema y el hardware Windows/Linux requieren comprobaciones manuales independientes.

<a id="renderer-backend-changes"></a>

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

La prueba de humo estática también fuerza un `SecurityError` al cargar una imagen externa en WebGL2 (#35), compara los píxeles y la orientación recuperados con la carga directa y verifica que las construcciones repetidas reutilicen una sola lectura autorizada sin abandonar WebGL2. `test:canvas-readback` comprueba por separado el rechazo de imágenes con restricciones de origen y la exclusión de vídeo de este reintento. Estos casos sintéticos no reproducen la imagen privada del informe original.

<a id="native-output-or-pop-out-changes"></a>

### Salida nativa o cambios Pop Out

`smoke:native-output` exige una presentación real de la GPU, aplica parámetros y ciclos de paleta en vivo, cierra mediante el observador habitual de ventanas y exige otra presentación tras reabrir. El informe distingue la respuesta al comando del tiempo hasta la primera presentación. En las PR, CI de Windows y Linux lo ejecuta sobre el binario de desarrollo optimizado tras empaquetarlo, con los binarios auxiliares de FFmpeg verificados. Linux usa una pantalla virtual Xvfb. Esto prueba el renderizador nativo y el ciclo de vida de la ventana; la matriz de cámara y pantalla físicas que aparece más abajo se valida por separado. Usa `ASCILINE_NATIVE_OUTPUT_REPORT_PATH` para conservar el informe JSON. macOS también comprueba la cadencia de display-link con el analizador de registros existente.

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

<a id="midi-uc-33e-or-sysex-changes"></a>

### Cambios en MIDI, UC-33e o SysEx

```bash
npm run test:midi
npm run check:tauri-policy
npm run test:rust
npm run midi:probe -- --connect
npm run smoke:static
```

La sonda física verifica que CoreMIDI pueda enumerar y abrir simultáneamente ambas direcciones del mioXC. No reemplaza el barrido de control y la lista de verificación de captura/restauración de banco completo en [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

<a id="tauri-commands-permissions-or-capabilities"></a>

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

La matriz estática de presets también comprueba la asignación de backends: un estado limpio y los presets sin un backend de compatibilidad explícito conservan Auto y usan WebGPU/WebGL2 en el Chromium compatible de la prueba. La prueba de presets de la aplicación empaquetada exige por separado el contrato centralizado de 96 presets: 68 acelerados y 28 asignados explícitamente a Canvas. CI de Windows ejecuta toda la matriz visible; la aceptación física debe confirmar además que los 68 acelerados usen WebGPU y permanezcan visibles en el equipo RTX de destino.

La misma prueba renderiza muestras de color conocidas mediante WebGL2 real y las compara con el mapeo compartido de las 21 paletas en los modos de color más cercano y luminancia, tanto al arrancar como al cambiar de paleta. También verifica que cargar una paleta conserve la orientación de la imagen de origen.

<a id="ffmpeg-and-media-engine"></a>

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

<a id="release-and-updater"></a>

### Lanzamiento y actualizador

La [Guía de actualización y lanzamiento](/es/docs/operations/release/) posee empaquetado, firma, publicación, repeticiones de aceptación de etiquetas inmutables y configuración de gancho de humo de CI. Utilice estas comprobaciones para validar los cambios de versión:

```bash
npm run check:desktop
npm run test:desktop-updater
npm run test:updater-manifest
npm run check:bundle:debug
npm run check:release
npm run bundle:release
npm run smoke:release-install
npm run test:macos-dmg-layout
```

Ejecute `npm run ffmpeg:build-sidecar` antes que `npm run check:release` en un clon limpio. `npm run bundle:release` ejecuta el paso de compilación del sidecar automáticamente.

El humo de lanzamiento descarga artefactos de los lanzamientos GitHub y verifica el diseño del instalador, los activos incluidos, los paquetes de actualización firmados, el comportamiento de `latest.json`, los controles empaquetados visibles Update y Reports y la ausencia de una lectura de backend duplicada en la barra superior. En macOS, verifica el DMG descargado, lo monta como de solo lectura en una raíz temporal privada, valida el diseño exacto de la aplicación a las aplicaciones e inspecciona la aplicación montada antes del salto del actualizador.

La prueba del controlador verifica que la disponibilidad de producción permita exactamente una verificación silenciosa por lanzamiento, que los resultados actuales/fuera de línea no anuncien el estado, que una actualización disponible no se instale automáticamente y que la ruta manual existente aún realice nuevas verificaciones e instalaciones activadas por el usuario.

Para una verificación manual del actualizador, inicie la versión compatible anterior instalada, confirme que la verificación de antecedentes muestre la versión de destino sin descargarla automáticamente y luego realice la acción de instalación explícita. Verifique la versión de destino y el ícono de la aplicación después del reinicio, la visibilidad de Reports con una cola vacía/pendiente y la ausencia de la lectura duplicada del backend en la barra superior. Registre las versiones de origen y de destino y las identidades de los artefactos. La recuperación del control heredado faltante-Update se documenta en la [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md#upgrading-from-096-or-097).

En macOS, Release Smoke extrae las cargas útiles actuales y anteriores de `.app.tar.gz`, requiere `com.asciline.remix`, ID de equipo `PWT3Q52LZ2`, tiempo de ejecución reforzado, aceptación de Gatekeeper y exactamente el mismo requisito designado, luego ejecuta la aplicación anterior a través del actualizador y revalida el paquete reemplazado. La aprobación interactiva del TCC en sí sigue siendo una verificación manual.

<a id="manual-smoke-checklist"></a>

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
20. Con Pop Out abierto, repita Cámara → Demo Image → Demo Video → Cámara, luego cierre y vuelva a abrir Pop Out. Compruebe la apariencia de celda diminuta de Acid Snowstorm y el borde derecho de Arcade Rain en comparación con la vista principal; cambie el tamaño y cambie FPS y ajustes preestablecidos mientras ambas superficies son visibles. Mantenga una cámara funcionando durante al menos dos minutos. Registre los tiempos en frío y repita los tiempos del primer fotograma visible por separado de los tiempos de finalización de comandos.

<a id="hardware-and-platform-checks"></a>

## Comprobaciones de hardware y plataforma

La aplicación depende del hardware real y de las pilas de medios del sistema operativo. Las pruebas automatizadas no cubren todas las combinaciones de hardware y plataforma.

La decisión de lanzamiento [1.0.3](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.0.3.md#release-decision--2026-09-04) registra la aceptación del propietario de Windows y el aplazamiento explícito de las pruebas de la cámara física de Ubuntu/Fedora. Que la brecha de cobertura Linux permanece abierta en el expediente documentado; ejecute las comprobaciones de una sola cámara en la [lista de verificación manual de humo](#manual-smoke-checklist) en los artefactos instalados exactos antes de registrar la aceptación. Las comprobaciones de paquetes de CI y Hyper-V no cierran la cobertura de la cámara física.

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

<a id="podman-checks"></a>

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

<a id="ci-and-release-behavior"></a>

## CI y comportamiento de liberación

La [Guía de lanzamiento y actualización](/es/docs/operations/release/#build-and-package) documenta el requisito previo de confirmación exacta del escritorio, las compilaciones paralelas de la aplicación/FFmpeg, la transferencia de entrada inmutable, la firma de la plataforma, la publicación y la aceptación posterior a la publicación. [Security](/es/docs/operations/security/#release-security-posture) posee las restricciones de seguridad.

Mantenga separados los resultados locales, de CI, de artefactos publicados, de aplicaciones instaladas y de plataforma física al informar la validación. La evidencia histórica por versión se encuentra en [registros de publicación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md).

<a id="known-gaps"></a>

## Brechas conocidas

- No existe un paquete integral de accesibilidad automatizada.
- No hay un conjunto de pruebas completo de i18n/l10n.
- No hay un paquete de salida visual dorado para ajustes preestablecidos.
- Sin punto de referencia de latencia de cámara automatizado.
- El análisis experimental de MIDI, el mapeo, los eventos falsos y el ensamblaje de SysEx están automatizados; Los barridos de control físico y la restauración del banco completo aún requieren el equipo UC-33e/mioXC.
- La cobertura de audio/cámara/medios nativos de Linux está limitada fuera de CI.

El seguimiento del lanzamiento potencial, la plataforma, la accesibilidad, la localización y la cobertura de rendimiento se realiza en [Roadmap](/es/docs/reference/roadmap/).

<a id="spatial-renderer-changes"></a>

## Cambios en el renderizador espacial

- `npm run test:spatial`: comprueba oclusión con alturas variables, intersecciones de cubiertas, rayos sin impacto y sobre ejes o esquinas, proyección rectilínea, repetición del mundo, movimiento con signo, controles finitos y acotados, límites de audio, desvanecimiento largo, respuesta a formas distintas de la fuente y diferencias entre pares de escenas activadas manualmente sobre una entrada oscura. También verifica los valores iniciales Flat Media y los límites exactos de probabilidad de WTF para cada modo. Los vectores de uniformes compartidos se ejecutan en JS y Rust; `npm run test:rust` también valida todo el WGSL nativo.
- `npm run smoke:spatial`: compara lecturas reales de celdas WebGPU/WebGL2 con la referencia Canvas; comprueba Bright output desactivado inicialmente y sus cambios en vivo, tanto en RGB como en luminancia de glifos; persistencia entre presets, WTF y mensajes nativos; Flat Media tras cada selección de preset integrado; 24 controles en las nueve escenas activadas manualmente; ediciones manuales y MIDI durante interpolaciones y transiciones de presets espaciales guardados; persistencia de cambios y limpieza de capas; elección independiente de escena en WTF durante la generación de referencias, reintentos y alternativa final; igualdad de fotogramas congelados; desvanecimiento en coma flotante; límites Canvas; y reproducción continua de un video de 30 segundos entre los nuevos presets y Classic Camera ASCII. Las nueve configuraciones de escena y el modo Relief heredado deben responder a dos fotogramas en movimiento con histogramas de color y brillo idénticos, pero formas distintas, tanto en RGB como en glifos. WebGPU requiere Chromium instalado con soporte GPU; `CHROMIUM_EXECUTABLE` permite seleccionarlo. Por defecto se abre un navegador visible y aislado. `SPATIAL_SMOKE_HEADLESS=1` es opcional en controladores con una cadena de presentación WebGPU fiable sin ventana. La prueba numérica usa un destino GPU fuera de pantalla e inicia la aplicación de prueba en WebGL2 porque Chromium informa de forma intermitente de una cadena de presentación inválida al iniciar tanto el renderizador WebGPU de referencia como el candidato. Los diagnósticos GPU siguen haciendo fallar la prueba; la presentación se comprueba por separado en las pruebas nativas y visibles.
- `npm run smoke:wtf`: generación determinista de destinos, rechazo explícito de apagones, rampas vacías y glifos negros fijos, comprobación de la alternativa y de fallos de lectura, conservación de fuentes negras, todas las escenas opcionales y lecturas finales de imágenes de glifos en WebGPU/WebGL2/Canvas tras un corte a una imagen oscura con audio sintético intenso. WebGPU usa un destino de presentación fuera de pantalla para evitar el problema de la cadena de presentación sin ventana. `WTF_SMOKE_REPORT=/path/report.json` guarda la salida medida y el tiempo de generación. Las comprobaciones de límites tonales compartidos y audio también se ejecutan en `test:spatial`. Para medir las transiciones de la vista previa y salida nativa instaladas en macOS, ejecuta `smoke:ui-perf` con `ASCILINE_UI_PERF_SMOKE_WTF=1` y `ASCILINE_UI_PERF_SMOKE_SYNTHETIC_AUDIO=1` sobre una compilación Dev optimizada.
- `npm run smoke:static`: comprueba todos los presets integrados, paletas, glifos, rutas de medios y redimensionado y errores JavaScript/GPU, incluidos los valores iniciales Flat Media del catálogo completo. La prueba nativa verifica esos mismos valores en la aplicación, el renderizador y los parámetros de salida nativa (`flatMediaPassed`).
- `node scripts/capture_spatial_review.mjs /tmp/spatial-review.png` captura una fuente oscura con el brillo desactivado y activado, y las nueve escenas espaciales habilitadas manualmente, mediante presentación real en WebGL2. Añada `--fractals` para los cuatro looks fractales sobre la fuente de demostración sin modificar y con Bright Output desactivado; añada `--flat-presets` para capturar sus valores iniciales en Flat Media. El atlas de glifos debe terminar de cargarse antes de la captura.
- Para medir el rendimiento de escenas nativas, use el entorno de pruebas de interfaz mantenido, por ejemplo `ASCILINE_UI_PERF_SMOKE_SPATIAL='{"visualMode":"city","sceneWet":0.55,"sceneRain":0.2,"sceneMedia":0.85}' ASCILINE_UI_PERF_SMOKE_COLUMNS=640 ASCILINE_UI_PERF_SMOKE_SYNTHETIC_AUDIO=1 npm run smoke:ui-perf`. Es una prueba exclusivamente local y debe usar la identidad de desarrollo. Conserve los umbrales habituales de tiempo por fotograma y actualización reactiva; una captura de pantalla no mide el rendimiento.

Aceptación manual: confirme que Bright Output empieza desactivado en un perfil limpio y conserva una elección guardada. Compare Bright output activado y desactivado con cámaras, imágenes y videos oscuros; vuelva a seleccionar cada preset integrado para comprobar Flat Media y active manualmente su modo espacial. Compare el preview y la salida nativa al cambiar modo, fuente, densidad, paleta y rampa. Ajuste el zoom, detalle y forma fractal tras seleccionar un preset y durante su transición; pruebe congelación, inversión y reinicio, estelas largas, continuidad del video, orientación de cámara, inicio y parada de audio, captura del valor MIDI y cierre y reapertura de la salida. Verifique por separado una segunda pantalla física y el hardware mínimo de referencia. Consulte el [registro de 1.1.0](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md).


<a id="fractal-accent-regression-checks"></a>

### Pruebas de regresión de acentos fractales

`test:spatial` también ejecuta `test_fractal_accents.mjs`: omisión exacta con valores cero, diferencias visibles de color y glifos en cada escena, variaciones seleccionadas, límites de Subtle Limit a máxima intensidad, audio acotado, reutilización del campo, congelación, desvanecimiento y alternativa de estelas, conservación de presets y selección determinista de recetas/Off en WTF. `smoke:spatial` compara cada acento y su intensidad máxima con la referencia de Canvas en WebGPU y WebGL2, incluidas todas las escenas opcionales con cada estilo sin estelas. Comprueba la atenuación y el desvanecimiento visibles de lace, la conservación del interruptor global al cambiar presets o WTF, los controles de variación, los datos MIDI enviados a la salida nativa y la reproducción continua de video. El historial congelado de coma flotante admite un byte de error de cuantización sin acumular desviación. Todos los casos de acentos también comparan WebGPU directamente con WebGL2, incluidas las direcciones de glifos (error medio ≤0.5/255 y ≤1% de canales con diferencias superiores a 8). Las comparaciones con CPU mantienen un error medio ≤2/255; el vidrio espacial permite que el 2.5% de los canales RGB supere 8, frente al 2% en los demás casos, porque los rayos desplazados encuentran distintos límites fractales sensibles a la precisión numérica. Esto no cambia las comprobaciones existentes de las escenas. Revisa la salida real junto con estas comprobaciones numéricas.

`node scripts/capture_spatial_review.mjs /tmp/fractal-accents.png --accents` captura pares de vistas con el acento desactivado y activado usando la salida real de WebGL2; el último par usa el historial de una fuente en movimiento. Añade `--accent-combinations` para revisar combinaciones de glifos con color fijo, monocromo y escenas opcionales. Para estos cambios, usa la matriz estática habitual, el barrido de presets de la vista principal instalada y las pruebas de rendimiento optimizadas de interfaz y salida nativa. La aceptación en hardware físico Windows/Linux y en el equipo mínimo de referencia sigue siendo independiente.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
