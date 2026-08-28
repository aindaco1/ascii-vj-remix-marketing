---
title: Motor de renderizado
description: Documentación del motor de renderizado derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Desarrollo
lang: es
---

# Motor de renderizado

Este documento describe cómo ASCII VJ Remix procesa fuentes en salida visual ASCII/celda en contextos de navegador y escritorio Tauri.

Documentos de práctica relacionados:

- [Rendimiento](/es/docs/operations/performance/) para latencia de renderizado/salida y validación de FPS.
- [Seguridad](/es/docs/operations/security/) para medios locales, capacidad Tauri, actualizador y límites del sidecar FFmpeg.
- [Prueba](/es/docs/operations/testing/) para el renderizador actual, los medios, la salida nativa y la matriz de validación de versiones.
- [Accesibilidad](/es/docs/operations/accessibility/) e [Internacionalización](/es/docs/operations/internationalization/) para reglas de UX de superficie de control que afectan los controles orientados al renderizador.

## Propiedades de arquitectura

- La salida WebGPU/WebGL es el objetivo de calidad visual.
- Las rutas de flujo adaptable y Canvas derivadas de ASCILINE permanecen disponibles como infraestructura de compatibilidad y desarrollo.
- El uso normal de la aplicación es local primero y sin conexión.
- Todos los controles en vivo se dirigen a través de un modelo de parámetro canónico.
- Los ajustes preestablecidos, WTF mode, la reactividad de audio y el control MIDI componen sin bifurcar el estado del renderizador.
- Pop Out utiliza rutas nativas de cuadros más recientes cuando están disponibles para minimizar la latencia de la cámara en vivo.
- El comportamiento de paleta, tramado ordenado, glifo y densidad se define una vez en catálogos/matemáticas compartidos y se implementa en cada backend sin estado paralelo.

## Flujo de datos de alto nivel

```text
Source selection
  -> source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

La selección de fuente puede provenir de medios integrados, archivos seleccionados por el usuario, transmisiones de cámara, cámaras mixtas o sesiones de transmisión de desarrollo. El tiempo de ejecución del renderizador elige el mejor backend para la fuente y el entorno activos.

## Capa de origen

### Medios integrados

Los elementos incorporados visibles son:

- Imagen de demostración: `media/demo.svg`.
- Vídeo de demostración: `media/demo-video-2.mp4`.

Los archivos multimedia adicionales incluidos permanecen ocultos como accesorios de desarrollo para pruebas de paridad y pruebas de humo de rendimiento.

### Archivos personalizados

El modo de explorador utiliza las API de archivos del explorador y las URL de blobs. El modo Tauri utiliza un comando de diálogo nativo y registra el archivo seleccionado bajo una identificación de medio local de sesión. Esa identificación de medio está expuesta a la vista web a través del protocolo de activos de Tauri.

El límite de seguridad importante es que el renderizador reciba una URL de medio reproducible o una identificación registrada. No obtiene acceso amplio al sistema de archivos.

### Cámaras

La captura de la cámara del navegador utiliza `getUserMedia`.

Para una sola cámara:

```text
MediaDevices.getUserMedia
  -> hidden video element
  -> MediaSource abstraction
  -> WebGPU/WebGL2/Canvas renderer
```

Para varias cámaras:

```text
N camera streams
  -> hidden video elements
  -> Canvas2D mixer
  -> captured/mixed media source
  -> renderer
```

Los controles de la cámara incluyen selección de dispositivo, tamaño de captura, FPS, diseño, encuadre y espejo. Los controles del modo frontal están ocultos cuando son irrelevantes para las capacidades del dispositivo seleccionado.

Tauri Pop Out nativo tiene una ruta macOS adicional para salida de una sola cámara:

```text
AVFoundation capture
  -> latest BGRA/RGB frame
  -> native output renderer
```

Esa ruta evita la lectura del lienzo de WebView y se introdujo para reducir la latencia de la cámara.

### Audio

El audio no es una fuente visual. Es una fuente de análisis que modula los parámetros de renderizado.

Fuentes de audio del navegador:

- archivo de audio local.
- micrófono/entrada a través de `getUserMedia`.
- mostrar/tabular audio a través de `getDisplayMedia` cuando la plataforma expone una pista de audio.

Fuentes de audio de escritorio Tauri:

- navegador/proveedores de audio web cuando estén disponibles.
- Proveedores de funciones nativas de sistema/audio de entrada para compilaciones de escritorio.

La capa de audio genera vectores de características delimitados, no búferes de audio sin formato ni marcos visuales sin formato.

### Sesiones de transmisión

Las sesiones de transmisión son desarrollo e infraestructura avanzada. No son una fuente normal de cara al usuario.

Camino heredado:

```text
Python/FastAPI/OpenCV
  -> ASCILINE frame preparation
  -> adaptive WebSocket frames
  -> JS decoder
  -> Canvas stream runtime
```

Ruta Rust/FFmpeg:

```text
registered media id
  -> Rust media session
  -> FFmpeg probe/decode
  -> Rust frame preparation
  -> adaptive encode
  -> Tauri batch read
  -> StreamRuntime
```

La interfaz de usuario de origen normal oculta el modo de transmisión. El trabajo de productización potencial se rastrea en [Roadmap](/es/docs/reference/roadmap/).

## Modelo de parámetros

La aplicación mantiene un objeto de parámetro canónico, comúnmente denominado en el código `params`.

Principales grupos de parámetros:

- fuente: modo de fuente, URL/id de medio, tipo de medio, nombre de fuente.
- cámara: ID de dispositivo seleccionado, resolución, FPS, diseño, encuadre, espejo.
- backend: automático, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- cuadrícula: columnas, filas, filas automáticas, ancho de celda, alto de celda, corrección de aspecto, preferencia global Advanced Density.
- color: saturación, contraste, brillo, gamma, combinación de fondo, cuantización, identificación de paleta, mapeo de paleta.
- tramado: matriz ordenada, fuerza, escala, sesgo, inversión.
- muestreo: FPS, cantidad de fluctuación, velocidad de fluctuación, muestra X/Y, suavizado.
- Glifo/celda: modo de glifo, modo sólido, conjunto de caracteres, rampa escrita personalizada, profundidad, desplazamiento, inversión, modo/color de color de glifo, color de fondo, estilo de atlas neutro, metadatos de familia de fuentes, intensidad mínima de glifo.
- flujo: códec, calidad, tolerancia, configuración del búfer, sincronización de fotogramas.
- UI/rendimiento: superposición de estadísticas, segundos de transición.

La superficie de control, los ajustes preestablecidos, la persistencia, los cambios de fuente, WTF mode, la reactividad de audio, la salida nativa y MIDI leen o escriben a través de este modelo.

Las transiciones estáticas entre familias de renderizadores mantienen la propiedad de los medios en la capa `StaticRuntime`. Los renderizadores Canvas2D, pixel Canvas, WebGL y WebGPU pueden realizar fundidos cruzados sobre la misma fuente de video/cámara en vivo en lugar de destruir y recargar medios cuando cambian `solidMode`, `glyphMode`, `pixel` o `backend`.

### Matemáticas de renderizado compartido

Los ayudantes compartidos reducen las matemáticas duplicadas del renderizador sin cambiar el lienzo establecido o la salida del flujo.

Los ayudantes compartidos de JavaScript viven en:

```text
renderers/shared/character-sets.js
renderers/shared/density-policy.js
renderers/shared/glyph-atlas.js
renderers/shared/palettes.js
renderers/shared/render-math.js
renderers/shared/render-math-vectors.json
```

El módulo compartido posee actualmente:

- Procesamiento de color estilo GPU utilizado por instantáneas de software y pruebas de paridad nativa.
- Procesamiento de color Legacy Canvas.
- Procesamiento de color de flujo heredado.
- Ayudantes de hash de jitter estilo sombreador.
- un catálogo limitado de conjuntos de caracteres canónicos, que incluye adaptaciones acreditadas de ascii.today.
- metadatos de cobertura Unicode aprobados completos y validación de rampa personalizada limitada.
- ID/colores de paleta nativos del proyecto, una tabla de búsqueda de paleta de 32x32x32 en caché y matrices Bayer inmutables.
- columna acelerada/software compartida y límites de densidad de celda total.
- Identificadores de glifos escalares Unicode, direccionamiento de páginas de atlas de 1024 px, mips de navegador de cobertura máxima en caché, caché decodificada de cuatro páginas y carga diferida de páginas locales.
- conjunto de caracteres compacto y ayudantes de luminancia a glifo.

Las funciones Canvas y Stream se nombran intencionalmente por separado de la función GPU. Su comportamiento establecido de cuantificación y combinación de fondo sigue siendo distinto, mientras que los vectores compartidos protegen la compatibilidad.

`npm run test:render-math` valida los ayudantes JavaScript frente a vectores compartidos. Las pruebas de salida nativa de Rust consumen el mismo archivo vectorial para la paridad de procesamiento de color de GPU.

### Parámetros efectivos

Algunas funciones afectan la representación en vivo sin cambiar el estado guardado.

La reactividad del audio es el ejemplo principal:

```text
base params
  + audio feature modulation
  -> effective params
  -> renderer.updateParams()
```

Los parámetros efectivos no deben persistir en los ajustes preestablecidos del usuario a menos que el usuario guarde explícitamente el estado actual como un ajuste preestablecido.

## Selección de back-end

El backend `auto` intenta primero la ruta viable de mayor calidad.

Prioridad típica del navegador:

1. WebGPU.
2. WebGL2.
3. Canvas2D.
4. Pixel Canvas cuando se seleccione o sea necesario.

El usuario puede anular el backend manualmente. Los controles que no se aplican al backend activo están ocultos o deshabilitados.

La elección del backend se resuelve una vez por construcción del renderizador en `renderers/gpu/ascii/renderer/backend-policy.js`; no se evalúa en el bucle del cuadro. La vista principal macOS Apple WebKit utiliza la ruta limitada Canvas2D para el modo de glifo incluso cuando un backend GPU del navegador está disponible o se solicita manualmente, porque ambas rutas del atlas de glifos GPU del navegador pueden exponer un renderizador en vivo mientras se presenta un lienzo vacío allí. Los ajustes preestablecidos primarios de sólidos/píxeles aún pueden usar WebGPU, y el modo de glifo conserva la representación de GPU del navegador en tiempos de ejecución compatibles. La selección de backend nativa de Pop Out es independiente y no cambia.

## Renderizador WebGPU

El renderizador WebGPU es el principal objetivo de calidad.

Las fuentes de vídeo utilizan `importExternalTexture()` por cuadro. Las fuentes de imágenes se cargan una vez con `copyExternalImageToTexture()` en un `texture_2d<f32>`.

El renderizador utiliza un flujo GPU de dos etapas:

1. Pase celular:
   - divide la fuente en una cuadrícula.
   - muestrear un punto por celda.
   - aplicar fluctuación animada por celda.
   - opcionalmente reflejar X.
   - aplicar procesamiento de color, umbrales ordenados y búsqueda de paleta.
   - escriba un color procesado por celda en una textura de almacenamiento.
2. Pase de renderizado:
   - dibuja un triángulo de pantalla completa.
   - asigne píxeles de salida a celdas utilizando el ancho/alto de la celda.
   - buscar el color de la celda procesada.
   - llene el lienzo de salida o enmascúrelo a través de la rampa de glifo Unicode seleccionada.

El procesamiento del color incluye:

- aumento de saturación alrededor del promedio de luminancia.
- aumento de contraste alrededor del punto medio.
- brillo.
- gama.
- Cuantización de color opcional.
- El fondo se mezcla con el color oscuro del lienzo de la aplicación.
- tramado ordenado Bayer 2x2/4x4/8x8 opcional.
- mapeo opcional de paleta de color más cercano o rampa de luminancia a través de un búfer de búsqueda de paleta que cambia solo cuando cambia la paleta/mapeo.

Jitter utiliza un hash determinista sembrado por la posición y el tiempo de la celda, por lo que las imágenes estáticas pueden animarse sin cambiar el medio de origen.

Los ArrayBuffers/DataViews uniformes, las vistas de textura y los grupos de enlaces cuyos recursos no cambian se crean una vez y se reutilizan. El vídeo del navegador sigue importando una textura externa y crea su enlace de cálculo dependiente de la fuente por fotograma; ese recurso tiene un alcance de marco de WebGPU. Las reconstrucciones de cuadrícula/fuente crean un nuevo renderizador y, por lo tanto, un nuevo conjunto de recursos completo.

El renderizador de glifos utiliza identificadores escalares Unicode en un búfer de almacenamiento de 96 entradas y una matriz de texturas R8 de 16 capas. Las páginas del Atlas se generan sin conexión, se agrupan localmente y se cargan bajo demanda. Las actualizaciones de audio/transición en vivo comparan una clave de entrada de glifo compacta antes de resolver rampas o tocar recursos del atlas.

## Renderizador WebGL2

El backend WebGL2 refleja el modelo visual WebGPU lo más fielmente posible:

- Los cuadros de video se cargan con `texImage2D()` por cuadro.
- Las imágenes se cargan una vez.
- primero pase muestras de un color por celda a una textura de color de celda.
- La paleta de primer paso/matemática de tramado coincide con el contrato compartido.
- La segunda pasada expande la textura del color de la celda y, opcionalmente, muestra el mismo contrato de rampa/atlas escalar Unicode que WebGPU.
- Los uniformes de sombreado coinciden con el conjunto de parámetros WebGPU siempre que sea posible.
- las 18 ubicaciones uniformes de sombreado se almacenan en caché después de vincular el programa en lugar de consultarse nuevamente durante cada cuadro.

WebGL2 es el navegador alternativo GPU más importante porque está ampliamente disponible en máquinas que no exponen WebGPU. La vista de glifo principal macOS Apple WebKit actualmente usa Canvas2D en lugar de la ruta del atlas GPU del navegador.

## Renderizadores de lienzo

Las rutas de lienzo conservan la compatibilidad con ASCILINE y el comportamiento de reserva de bajo nivel.

El modo glifo/texto Canvas2D representa celdas con apariencia de caracteres. Pixel Canvas representa datos de bloques/píxeles coloreados de forma más directa.

Canvas utiliza el mismo catálogo de paletas, tabla de búsqueda, umbrales ordenados y rampa de glifos activos limitada. No carga fuentes del sistema operativo en la ruta de salida nativa y permanece gobernado por el límite de densidad de software más bajo.

Estos caminos son importantes para:

- navegadores o vistas web más antiguos.
- compatibilidad con marcos de flujo.
- probando la salida del códec adaptativo.
- entornos donde falla la inicialización de GPU.

El respaldo de Canvas sigue siendo funcional aunque no sea la ruta de mayor calidad.

## Tiempo de ejecución estático

`StaticRuntime` administra fuentes locales nativas del navegador y backends GPU/Canvas.

Responsabilidades:

- cargar o reconstruir la fuente activa.
- elija el servidor.
- iniciar y detener la reproducción multimedia.
- mantenga vivo el renderizador a través de cambios de parámetros seguros en vivo.
- reconstruir las superficies del renderizador cuando cambian los parámetros estructurales.
- preservar el estado de reproducción de video al cambiar ajustes preestablecidos que no cambian la fuente.
- actualizar estadísticas.

Para cambios estructurales, el tiempo de ejecución utiliza superficies de renderizado en capas:

```text
old renderer stays visible
  -> new renderer initializes behind or beside it
  -> non-structural params tween
  -> surfaces crossfade
  -> old renderer is destroyed
```

Esto evita cuadros negros durante las transiciones preestablecidas.

Para una interpolación numérica no estructural, solo los controles cuyos valores cambian se sincronizan durante los cuadros de animación. Las listas de fuentes, las opciones de dispositivos de cámara, la visibilidad, los medidores, la persistencia y la superficie de control completa se concilian en el límite estatal final. Esta es únicamente una optimización del trabajo de la interfaz de usuario; Los parámetros de renderizado efectivos y la sincronización nativa/Pop Out aún avanzan durante la interpolación.

## Tiempo de ejecución de la transmisión

`StreamRuntime` maneja secuencias de cuadros codificados estilo ASCILINE.

Puede consumir:

- Marcos WebSocket del servidor Python/FastAPI heredado.
- lotes de sesiones nativas Rust/FFmpeg en las rutas de desarrollo Tauri.

Las tramas de flujo transportan metadatos INIT y mensajes de framebuffer. El decodificador JS admite:

- marcos sin procesar heredados.
- RAW adaptativo.
- ZLIB adaptativo.
- DELTA adaptativo.

El modo de transmisión está oculto de la interfaz de usuario de origen normal y se conserva como infraestructura de desarrollo.

## Códec adaptativo

El códec adaptativo existe para reducir el ancho de banda en comparación con enviar el framebuffer completo en cada cuadro.

Cada cuadro codificado elige uno de:

- RAW: búfer de fotogramas completo.
- ZLIB: framebuffer comprimido.
- DELTA: celdas cambiadas desde el cuadro anterior.

La calidad del códec puede permitir deltas temporales basados ​​en la tolerancia para los planos de color y, al mismo tiempo, mantener los planos de caracteres exactos cuando corresponda.

Reglas de compatibilidad:

- Los clientes heredados existentes aún pueden recibir marcos sin formato.
- Los decodificadores JS y Rust deben seguir siendo compatibles con los vectores generados por Python.
- Los cambios de códec requieren pruebas vectoriales.

## Canalización de medios Rust/FFmpeg

La ruta Rust/FFmpeg transfiere la ruta de preparación de flujo Python/FastAPI hacia un motor local empaquetado en escritorio.

Forma actual:

```text
Tauri selected media
  -> Rust registry id
  -> ffprobe metadata
  -> ffmpeg RGB frame reader
  -> frame preparation
  -> adaptive encoder
  -> native session batches
  -> StreamRuntime or validation tools
```

Módulos clave:

- `media_engine::ffmpeg`: FFmpeg/ffprobe límite de proceso, sonda de video, lector RGB, opciones de lector de cámara.
- `media_engine::frame_prep`: preparación de framebuffer de texto/color/píxel compatible con ASCILINE.
- `media_engine::codec`: codificador/decodificador de códec adaptativo.
- `media_engine::pipeline`: decodificar -> preparación -> codificar -> verificación de decodificación opcional.

Modos de preparación de fotogramas:

- Modo texto: escala de grises a paleta ASCII.
- Modos de color 2 a 5: celdas `[char, R, G, B]` con niveles de color cuantificados.
- Modo de píxel: celdas `[B, G, R]`.

La ruta Rust complementa, en lugar de reemplazar, el renderizador estático WebGPU/WebGL. Proporciona preparación de medios empaquetados estilo flujo e integración de decodificador nativo.

## Representador de salida nativo

El renderizador de salida nativo existe porque una segunda ventana emergente renderizada por WebView era demasiado costosa para una salida en vivo de baja latencia.

Flujo de escritorio:

```text
main UI params/source state
  -> Tauri native output command
  -> native output state
  -> source frame acquisition
  -> native `wgpu` presenter
  -> output window
```

Para imágenes/vídeos respaldados por archivos, Rust resuelve recursos agrupados o identificadores de medios registrados, decodifica fotogramas, carga el fotograma más reciente en GPU, aplica matemáticas de color de celda y presenta a través de la cadena de intercambio nativa.

En la ruta del enlace de visualización macOS, la versión decodificada del marco fuente se pasa al presentador. Cuando esa versión y las dimensiones del marco no han cambiado, el presentador reutiliza la textura de origen existente mientras sigue codificando/presentando con los últimos parámetros visuales y audio-reactivos. Las personas que llaman de reserva sin versión retienen las cargas incondicionales. Los registros exponen la carga de origen y los contadores de omisión.

Para la salida de una sola cámara macOS, AVFoundation captura los últimos fotogramas directamente para el presentador nativo. Los ajustes preestablecidos de la cámara en vivo no utilizan el transporte espejo del navegador de forma predeterminada porque la lectura del lienzo y la transferencia de fotogramas IPC son demasiado costosas para una salida sostenida.

La salida nativa consume los mismos parámetros canónicos de paleta, tramado, `glyphMode`, conjunto de caracteres/rampa personalizada, profundidad/desplazamiento/inversión y glifo/color de fondo que la superficie de control. El presentador nativo `wgpu` fusiona paleta y trabajo de tramado ordenado en su paso de celda, luego enmascara las celdas a través del mismo contrato de rampa/página escalar Unicode que los renderizadores GPU del navegador.

La interfaz resuelve la entrada de catálogo seleccionada en una base delimitada `charsetRamp`; Rust valida los escalares admitidos y aplica profundidad, desplazamiento y retroceso una vez para crear una rampa máxima de 96 id. Las páginas del atlas R8 de 1024 px requeridas se decodifican/cargan de forma perezosa y se retienen en la textura fija de 16 capas del presentador. `fontFamily` sigue siendo metadatos de vista previa/superficie de control; La salida nativa nunca carga fuentes arbitrarias del sistema o del usuario.

Para fuentes alternativas/reflejadas, se pueden enviar instantáneas de píxeles sin procesar delimitadas desde el renderizador principal a la salida nativa.

Reglas de diseño de salida nativas:

- La ventana de salida no posee amplios permisos Tauri.
- El presentador consume los últimos parámetros en vivo.
- Se prefiere la semántica del último fotograma al almacenamiento en búfer profundo.
- El comportamiento del renderizador principal no debe retroceder cuando Pop Out está abierto.
- el respaldo del navegador debe permanecer disponible.

## Modulación audio-reactiva

El análisis de audio actualiza los parámetros de renderizado efectivos a la velocidad de fotogramas.

Características:

- RMS.
- bajo.
- medio-bajo.
- medio.
- medio-alto.
- triple.
- presencia.
- brillo.
- densidad.
- flujo espectral.
- batir el pulso.
- fase/oscilación.

La amortiguación de mezcla densa utiliza la función de densidad para reducir la modulación con mucho ritmo/flujo durante pasajes de banda ancha abarrotados sin silenciar los transitorios dispersos.

Los objetivos de modulación son controles visuales seguros para la vida:

- brillo.
- contraste.
- saturación.
- gama.
- mezcla de fondo.
- cantidad de inquietud.
- velocidad de fluctuación.
- compensaciones de muestra.

Los controles estructurales como la fuente, el backend, la asignación de cuadrícula y los dispositivos de cámara no se modulan por tiempo porque provocarían una rotación del renderizador.

## Presets, modo WTF y MIDI

Todas estas son capas de control sobre el mismo modelo de parámetros.

Preajustes:

- aplicar conjuntos de parámetros conocidos.
- puede especificar la duración de la transición.
- Los usuarios pueden guardar/importar/exportar.

WTF mode:

- crea parámetros de destino aleatorios.
- ancla algunos estados aleatorios alrededor de familias preestablecidas extremas y ajustes preestablecidos ASCII tradicionales.
- transiciones indefinidamente hasta que se detiene.
- evita estados inseguros donde todo blanco/todo negro.

Experimental MIDI:

```text
UC-33e DIN output
  -> mioXC/CoreMIDI
  -> bounded Rust event queue
  -> frame-coalesced mapping engine
  -> canonical visual/audio target
  -> params/effective params
  -> main preview and native Pop Out synchronization
```

- Utiliza los mismos rangos, abrazaderas, definidores y metadatos estructurales que los controles visibles de la interfaz de usuario.
- Aplica configuraciones básicas visuales o audiorreactivas; no bifurca el estado del renderizador ni escribe parámetros efectivos derivados de audio en los ajustes preestablecidos.
- Reinicia la soft takeover después de cambios visuales preestablecidos.
- Mantiene los bordes de los botones ordenados mientras fusiona cambios continuos de alta velocidad.
- Restringe las acciones a parámetros visuales, configuraciones audio-reactivas, ajustes preestablecidos visuales y WTF mode. Las fuentes, la cámara, Pop Out y las pantallas de salida no son objetivos.
- Utiliza cuatro páginas UC-33e con dirección de canal y ranuras numéricas preestablecidas estables.
- Captura/restaura paquetes SysEx opacos delimitados a través de la salida mioXC seleccionada sin exponer los permisos MIDI a la ventana de salida.
- Las capas de mapeo y transporte están cubiertas por pruebas automatizadas, pero la restauración/verificación física del banco completo sigue siendo una brecha de aceptación experimental.

Consulte [UC-33e y mioXC MIDI Control](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) para ver el mapa físico.

## Empaquetado y tiempo de ejecución sin conexión

El renderizador no debe depender de los recursos en línea en tiempo de ejecución.

Los activos empaquetados incluyen:

- paquete de interfaz.
- código de renderizado.
- Activos GPU.
- fuentes.
- medios de demostración incorporados.
- Código nativo Tauri.
- sidecares FFmpeg revisados.

El CSP de producción bloquea el acceso remoto arbitrario al tiempo de ejecución HTTP(S). El protocolo de activos tiene un alcance limitado y una sesión local para los medios seleccionados por el usuario.

## Validación

La matriz de validación mantenida se encuentra en [Testing](/es/docs/operations/testing/). Los comandos principales de renderizado, salida, códec y medios son:

```bash
npm run smoke:static
npm run test:output-display
npm run smoke:native-output
npm run smoke:ui-perf
npm run test:vectors
npm run test:frame-prep
npm run test:decode-resize
npm run check:media
npm run test:rust
```

El seguimiento del trabajo potencial de renderizado, cámara, transmisión, audio y MIDI solo se realiza en [Roadmap](/es/docs/reference/roadmap/).


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
