---
title: Motor de renderizado
description: Documentación del motor de renderizado derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Desarrollo
lang: es
---

<a id="rendering-engine"></a>

# Motor de renderizado

Este documento describe cómo ASCII VJ Remix procesa fuentes en salida visual ASCII/celda en contextos de navegador y escritorio Tauri.

Documentos de práctica relacionados:

- [Rendimiento](/es/docs/operations/performance/) para latencia de renderizado/salida y validación de FPS.
- [Seguridad](/es/docs/operations/security/) para medios locales, capacidad Tauri, actualizador y límites del sidecar FFmpeg.
- [Prueba](/es/docs/operations/testing/) para el renderizador actual, los medios, la salida nativa y la matriz de validación de versiones.
- [Accesibilidad](/es/docs/operations/accessibility/) e [Internacionalización](/es/docs/operations/internationalization/) para reglas de UX de superficie de control que afectan los controles orientados al renderizador.

<a id="architecture-properties"></a>

## Propiedades de arquitectura

- La salida WebGPU/WebGL es el objetivo de calidad visual.
- Las rutas de flujo adaptable y Canvas derivadas de ASCILINE permanecen disponibles como infraestructura de compatibilidad y desarrollo.
- El uso normal de la aplicación es local primero y sin conexión.
- Todos los controles en vivo se dirigen a través de un modelo de parámetro canónico.
- Los ajustes preestablecidos, WTF mode, la reactividad de audio y el control MIDI componen sin bifurcar el estado del renderizador.
- Pop Out utiliza rutas nativas de cuadros más recientes cuando están disponibles para minimizar la latencia de la cámara en vivo.
- El comportamiento de paleta, tramado ordenado, glifo y densidad se define una vez en catálogos/matemáticas compartidos y se implementa en cada backend sin estado paralelo.

<a id="high-level-data-flow"></a>

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

<a id="source-layer"></a>

## Capa de origen

<a id="built-in-media"></a>

### Medios integrados

Los elementos incorporados visibles son:

- Imagen de demostración: `media/demo.svg`.
- Demo Video: `media/demo-video-2.mp4` (H.264) en macOS y Windows, y `media/demo-video-2.webm` (VP8) en Linux, por lo que las vistas web limpias de Linux no requieren un complemento GStreamer H.264 opcional. Ambas URL representan la misma fuente lógica integrada; Las selecciones guardadas se normalizan según la plataforma actual. Si la vista web no puede decodificar ninguno de los recursos, la misma fuente de fotograma sin formato FFmpeg incluida utilizada para los vídeos seleccionados se hace cargo localmente.

Los archivos multimedia adicionales incluidos permanecen ocultos como accesorios de desarrollo para pruebas de paridad y pruebas de humo de rendimiento.

<a id="custom-files"></a>

### Archivos personalizados

El modo de explorador utiliza las API de archivos del explorador y las URL de blobs. El modo Tauri utiliza un comando de diálogo nativo y registra el archivo seleccionado bajo una identificación de medio local de sesión. Esa identificación de medio está expuesta a la vista web a través del protocolo de activos de Tauri. Los archivos MKV utilizan inmediatamente la ruta de marco sin formato FFmpeg incluida. Otros videos seleccionados prueban primero el decodificador de la plataforma y vuelven a intentarlo a través de FFmpeg incluido si ese decodificador rechaza el archivo.

El límite de seguridad importante es que el renderizador reciba una URL de medio reproducible o una identificación registrada. No obtiene acceso amplio al sistema de archivos.

<a id="cameras"></a>

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

Pop Out nativo de Tauri tiene rutas de captura de una sola cámara específicas para cada plataforma:

```text
macOS: AVFoundation capture
Windows: Media Foundation source reader
Linux: bundled FFmpeg V4L2 input
  -> latest BGRA/RGB frame
  -> native output renderer
```

La presentación nativa de Pop Out evita la lectura del canvas del WebView y el envío de cada fotograma por Tauri IPC. En Windows, un único cliente nativo controla la cámara para ambas vistas; reduce el tamaño del último fotograma, lo codifica como JPEG y lo devuelve mediante una respuesta binaria de Tauri a un canvas que consume el preview WebGPU existente. En Linux, el preview principal del WebView se pausa mientras Pop Out nativo controla un dispositivo V4L2 exclusivo y recupera la cámara al cerrarse. Windows/Linux comprueban un fotograma antes de mostrar la salida nativa y recurren a la duplicación acotada si no pueden abrir el dispositivo. Windows conserva esa primera captura en vez de abrir dos veces la cámara. El callback asíncrono de Media Foundation actualiza un único espacio para el último fotograma, independientemente del renderizado GPU y de las lecturas del preview.

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

<a id="stream-sessions"></a>

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

<a id="parameter-model"></a>

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

<a id="shared-renderer-math"></a>

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

<a id="effective-params"></a>

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

La consulta de características de audio y la sincronización de la salida reactiva tienen una frecuencia objetivo de 120 Hz, con una sola lectura nativa en curso. Se ignoran las lecturas duplicadas y las respuestas de sesiones detenidas. Los analizadores FFT del navegador no añaden suavizado: ambas rutas de captura usan la misma envolvente de ataque inmediato y caída según el tiempo transcurrido. Smoothing en cero omite la envolvente. La entrada nativa solicita búferes de 128 muestras por canal dentro del rango admitido por el dispositivo y conserva el búfer predeterminado como alternativa. El historial de pulsos y su caída dependen del tiempo, no del número de callbacks. En funcionamiento estable, Pop Out consume estos parámetros efectivos sin aplicar la modulación de audio dos veces. Las transiciones nativas preparadas reciben extremos sin modular y mantienen su respuesta de audio nativa directa mientras se suspende la sincronización de parámetros.

<a id="backend-selection"></a>

## Selección de back-end

El backend `auto` intenta primero la ruta viable de mayor calidad.

Prioridad típica del navegador:

1. WebGPU.
2. WebGL2.
3. Canvas2D.
4. Pixel Canvas cuando se seleccione o sea necesario.

El usuario puede anular el backend manualmente. Los controles que no se aplican al backend activo están ocultos o deshabilitados.

La elección del backend se resuelve una vez por construcción del renderizador en `renderers/gpu/ascii/renderer/backend-policy.js`; no se evalúa en el bucle del cuadro. Sólo un backend de Canvas seleccionado explícitamente pasa por alto la construcción GPU. La identidad de la plataforma y el agente de usuario no cambian la propiedad preestablecida: las vistas empaquetadas macOS, Windows y Linux intentan el mismo orden de reserva WebGPU, WebGL2 y luego Canvas. La selección de backend nativa de Pop Out es independiente y no cambia.

<a id="webgpu-renderer"></a>

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

Los ArrayBuffers y DataViews de uniformes, las vistas de textura y los grupos de enlaces con recursos estables se crean una vez y se reutilizan. El video del navegador sigue importando una textura externa y creando su enlace de cómputo dependiente de la fuente en cada fotograma. Cuando está disponible, `VideoFrame` conserva la imagen decodificada hasta `queue.submit` y se cierra en `finally`. Esto evita depender de la vida útil de la textura de video HTML almacenada en caché por WebKit durante cambios del decodificador o de ventana. El [contrato de texturas externas de WebGPU](https://www.w3.org/TR/webgpu/#external-texture-creation) mantiene válida una textura respaldada por VideoFrame hasta cerrar el fotograma. Los huecos del decodificador omiten un fotograma; otros fallos GPU siguen siendo notificables. Los envíos fallidos no avanzan los contadores ni el historial de realimentación, y el bucle de animación se vuelve a programar incluso tras un error. Reconstruir la cuadrícula o la fuente crea un renderizador nuevo y un conjunto completo de recursos.

El renderizador de glifos decodifica solo las páginas del atlas que necesita la rampa activa, luego empaqueta hasta 96 máscaras escalares Unicode y sus cinco niveles de cobertura máxima en una textura RGBA de 768x62 de dos filas. Mantener el ancho compacto por debajo de 1024 píxeles evita el límite de carga amplia Apple WebKit y al mismo tiempo conserva la búsqueda de texturas en tiempo constante en el paso del fragmento. Las páginas de Atlas se generan sin conexión, se agrupan localmente y se cargan a través de sus URL de activos. Las actualizaciones de audio/transición en vivo comparan una clave de entrada de glifo compacta antes de resolver rampas o tocar recursos del atlas.

<a id="webgl2-renderer"></a>

## Renderizador WebGL2

El backend WebGL2 refleja el modelo visual WebGPU lo más fielmente posible:

- Los cuadros de video se cargan con `texImage2D()` por cuadro.
- Las imágenes se cargan una vez.
- primero pase muestras de un color por celda a una textura de color de celda.
- La paleta de primer paso/matemática de tramado coincide con el contrato compartido.
- Las texturas de búsqueda de paleta conservan el orden de las filas de datos, mientras que las imágenes de origen mantienen su propia configuración de giro vertical.
- La segunda pasada expande la textura del color de la celda y, opcionalmente, muestra el mismo contrato de rampa/atlas escalar Unicode que WebGPU.
- Los uniformes de sombreado coinciden con el conjunto de parámetros WebGPU siempre que sea posible.
- las 18 ubicaciones uniformes de sombreado se almacenan en caché después de vincular el programa en lugar de consultarse nuevamente durante cada cuadro.

WebGL2 es el navegador alternativo GPU más importante porque está ampliamente disponible en máquinas que no exponen WebGPU.

El valor predeterminado visual de perfil limpio y la preferencia del renderizador tienen propietarios separados: Classic Camera ASCII proporciona los parámetros visuales iniciales, mientras que el backend global sigue siendo Automático. Un ajuste preestablecido integrado hereda Auto a menos que declare explícitamente un backend de compatibilidad. Esto mantiene los ajustes preestablecidos de sólidos/píxeles en WebGPU o WebGL2 y al mismo tiempo preserva la propiedad intencional de Canvas2D para los ajustes preestablecidos de texto tradicionales y Paper Shredder.

`StaticRuntime` trata la construcción de GPU como una operación recuperable. Si el renderizador WebGPU/WebGL2 solicitado no se puede inicializar, crea el renderizador Canvas equivalente tanto para el inicio inicial como para las transiciones preestablecidas en vivo. Un retroceso fallido del Canvas deja activa la superficie de transición anterior.

La aceptación en hardware físico con Windows 11 y WebView2 detectó un fallo concreto: la inicialización de GPU y los contadores de fotogramas funcionaban, pero el atlas de glifos producía una salida vacía mientras las celdas sólidas seguían visibles. La primera solución enviaba todos los previews de glifos de Windows a Canvas2D y reducía los presets acelerados a unos siete. La textura compacta de la rampa activa sustituyó la carga problemática de glifos y la versión 1.0 retiró esa solución general. La matriz actual de Windows debe conservar 62 presets acelerados y 28 asignados explícitamente a Canvas. Un fallo real al crear el renderizador sigue recurriendo a Canvas2D.

<a id="canvas-renderers"></a>

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

<a id="static-runtime"></a>

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

La construcción del renderizador registra una secuencia limitada de eventos estructurados. Una falla de GPU que activa Canvas, o una falla de transición total, pone en cola un elemento Reports deduplicado con backend solicitado/resuelto, valor preestablecido, clase de origen y resúmenes de eventos recientes. Los informes son asincrónicos y nunca bloquean el respaldo o la transición; no se incluye ningún marco, carga útil de medios ni registro local arbitrario.

Para cambios estructurales, el tiempo de ejecución utiliza superficies de renderizado en capas:

```text
old renderer stays visible
  -> new renderer initializes behind or beside it
  -> non-structural params tween
  -> surfaces crossfade
  -> old renderer is destroyed
```

Esto evita cuadros negros durante las transiciones preestablecidas.

Cuando el Pop Out nativo está activo, el controlador arma un contrato de transición que contiene los parámetros canónicos nuevos y antiguos, el tipo de transición, la duración y una hora de inicio compartida del reloj Unix. La vista principal y el enlace de visualización nativa derivan el progreso independientemente de esa misma marca de tiempo. Las transiciones numéricas utilizan la función de aceleración compartida; Las transiciones estructurales de la familia de renderizadores renderizan ambos estados nativos y los componen con la misma curva de opacidad saliente que la vista primaria en capas. Las actualizaciones del cuadro de animación IPC se suprimen hasta que se completa el contrato, luego se envía un estado canónico final.

Para una interpolación numérica no estructural, solo los controles cuyos valores cambian se sincronizan durante los cuadros de animación. Las listas de fuentes, las opciones de dispositivos de cámara, la visibilidad, los medidores, la persistencia y la superficie de control completa se concilian en el límite estatal final. Esta es únicamente una optimización del trabajo de la interfaz de usuario; Los parámetros de renderizado efectivos y la sincronización nativa/Pop Out aún avanzan durante la interpolación.

<a id="stream-runtime"></a>

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

<a id="adaptive-codec"></a>

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

<a id="rustffmpeg-media-pipeline"></a>

## Canalización de medios Rust/FFmpeg

La ruta Rust/FFmpeg transfiere la ruta de preparación de flujo Python/FastAPI hacia un motor local empaquetado en escritorio.

Forma actual:

```text
Tauri selected or vetted bundled media
  -> Rust registry id or exact bundled source id
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

La ruta Rust complementa, en lugar de reemplazar, el renderizador estático WebGPU/WebGL. Proporciona preparación de medios empaquetados estilo flujo e integración de decodificador nativo. Los identificadores de fuente incluidos resuelven sólo los recursos de demostración MP4 y WebM enviados; no amplían el protocolo de activos ni exponen caminos arbitrarios.

<a id="native-output-renderer"></a>

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

La superficie nativa GPU prefiere `Bgra8Unorm` o `Rgba8Unorm` que no sean sRGB, lo que coincide con la codificación del lienzo del navegador esperada por la matemática de color compartida. Los formatos sRGB informados por la plataforma siguen siendo un último recurso cuando no hay una superficie no normal disponible.

En la ruta del enlace de visualización macOS, la versión decodificada del marco fuente se pasa al presentador. Cuando esa versión y las dimensiones del marco no han cambiado, el presentador reutiliza la textura de origen existente mientras sigue codificando/presentando con los últimos parámetros visuales y audio-reactivos. Las personas que llaman de reserva sin versión retienen las cargas incondicionales. Los registros exponen la carga de origen y los contadores de omisión.

Para salida de una sola cámara, AVFoundation en macOS, Media Foundation en Windows y la entrada local incluida FFmpeg V4L2 en Linux capturan fotogramas directamente para el presentador nativo. Los ajustes preestablecidos de la cámara en vivo no utilizan el transporte espejo del navegador de forma predeterminada porque la lectura del lienzo y la transferencia de fotogramas IPC son demasiado costosas para una salida sostenida. Varias cámaras y fallas de apertura nativa mantienen la ruta del espejo limitada.

La salida nativa consume los mismos parámetros canónicos de paleta, tramado, `glyphMode`, conjunto de caracteres/rampa personalizada, profundidad/desplazamiento/inversión y glifo/color de fondo que la superficie de control. El presentador nativo `wgpu` fusiona paleta y trabajo de tramado ordenado en su paso de celda, luego enmascara las celdas a través del mismo contrato de rampa/página escalar Unicode que los renderizadores GPU del navegador.

La interfaz resuelve la entrada del catálogo seleccionada en una base delimitada `charsetRamp`; Rust valida los escalares admitidos y aplica profundidad, desplazamiento y retroceso una vez para crear una rampa máxima de 96 id. Las páginas del atlas R8 de 1024 px requeridas se decodifican/cargan de forma perezosa y se retienen en la textura fija de 16 capas del presentador. Windows también carga los cuatro niveles MIP de cobertura máxima utilizados por la ruta de glifos de celdas pequeñas del navegador. macOS y Linux conservan su muestreo de página base existente. `fontFamily` sigue siendo metadatos de vista previa/superficie de control; La salida nativa nunca carga fuentes arbitrarias del sistema o del usuario.

Para fuentes alternativas/reflejadas, se pueden enviar instantáneas de píxeles sin procesar delimitadas desde el renderizador principal a la salida nativa.

Reglas de diseño de salida nativas:

- La ventana de salida no posee amplios permisos Tauri.
- El presentador consume los últimos parámetros en vivo.
- Se prefiere la semántica del último fotograma al almacenamiento en búfer profundo.
- Los cambios de fuente y modo de duplicación en Windows/Linux detienen el hilo nativo anterior y esperan a que termine antes de reutilizar la ventana de salida. Los errores de validación de superficie o la pérdida del identificador de ventana durante el cierre o reemplazo normal son condiciones de cierre recuperables, no un pánico del proceso ni un evento para el informe de fallos.
- La captura nativa de cámara en Windows/Linux debe producir un fotograma de comprobación antes de abrir la ventana de salida. Windows conserva esa captura como único cliente. Ambas plataformas restauran la cámara del WebView antes de recurrir a la duplicación o después de cerrar una sesión nativa exclusiva. Durante una sesión exclusiva de Windows, un puente binario JPEG acotado con el último fotograma mantiene vivo el preview WebGPU principal. Windows emite el evento de cierre solo después de que el hilo de Media Foundation haya liberado el dispositivo. El sufijo de modelo USB opcional de Chromium solo se admite cuando la coincidencia con el nombre descriptivo de Media Foundation no es ambigua.
- El comportamiento del renderizador principal no debe retroceder cuando Pop Out está abierto.
- el respaldo del navegador debe permanecer disponible.

<a id="audio-reactive-modulation"></a>

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

El inicio de captura y las lecturas de características comparten un identificador de generación que descarta trabajo obsoleto. Stop invalida el trabajo pendiente, libera los flujos del navegador que llegan tarde y serializa los comandos nativos de inicio y parada para que una parada antigua no cierre una sesión nueva. Solo la generación actual puede modificar el estado o los errores. La selección de presets de audio comparte una función de ajuste entre la interfaz y MIDI, restaura todos los controles deslizantes y conserva la fuente, el dispositivo y el estado de activación. El selector muestra explícitamente los ajustes Custom. Editar el audio o pulsar Stop devuelve una transición nativa autónoma a las actualizaciones dirigidas por la aplicación, incluso si la confirmación de preparación llega después de la edición.

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

<a id="presets-wtf-mode-and-midi"></a>

## Presets, modo WTF y MIDI

Todas estas son capas de control sobre el mismo modelo de parámetros.

Preajustes:

- aplicar conjuntos de parámetros conocidos.
- empiezan en Flat Media para todos los looks integrados; los looks personalizados guardados conservan el modo visual elegido. Las configuraciones de escena siguen disponibles para activarlas manualmente.
- puede especificar la duración de la transición.
- Los usuarios pueden guardar/importar/exportar.

WTF mode:

- crea parámetros de destino aleatorios.
- ancla algunos estados aleatorios alrededor de familias preestablecidas extremas y ajustes preestablecidos ASCII tradicionales.
- elige Flat Media de forma independiente con una probabilidad del 80 %; en los demás casos reparte la elección por igual entre los modos espaciales canónicos. La elección se hace una vez antes de los reintentos de seguridad visual y se conserva en la alternativa final. Los destinos espaciales usan la cámara de su configuración de escena y el backend Auto, con las alternativas normales del renderizador. Los estilos de color y glifos de referencia siguen siendo aleatorios.
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

<a id="packaging-and-offline-runtime"></a>

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

<a id="validation"></a>

## Validación

La matriz de validación mantenida y los comandos se encuentran en [Testing](/es/docs/operations/testing/). Utilice sus [verificaciones de backend del renderizador](/es/docs/operations/testing/#renderer-backend-changes), [verificaciones de salida nativas](/es/docs/operations/testing/#native-output-or-pop-out-changes) y [verificaciones de medios](/es/docs/operations/testing/#ffmpeg-and-media-engine) para las rutas afectadas.

El seguimiento del trabajo potencial de renderizado, cámara, transmisión, audio y MIDI solo se realiza en [Roadmap](/es/docs/reference/roadmap/).

<a id="indexed-palette-cycling"></a>

## Ciclos de paleta indexada

`renderers/shared/palette-contract.json` define los límites de 256 colores y ocho rangos. Las paletas contienen colores base inmutables y rangos inclusivos sin solapamientos. La LUT de fuente a índice siempre usa los colores base; una tabla RGBA independiente anima sus entradas RGB. Alfa guarda la luminancia base para que los ciclos no cambien la máscara del glifo. Off es el valor predeterminado de compatibilidad. El catálogo tiene 21 paletas y el contrato de presets establece 90 en total: 62 acelerados y 28 asignados explícitamente a Canvas.

`palette-cycling.js` define la validación de rangos, el módulo con signo, la consulta clásica o interpolada, la intensidad y la integración temporal de la velocidad. `cell-color.wgsl.js` aporta el procesamiento de color WGSL compartido entre navegador y renderizador nativo. El evaluador de Rust consume el mismo contrato JSON y los mismos vectores de referencia; WebGL2 consulta una textura RGBA32F de 256×1, mientras Canvas y el renderizador nativo por software evalúan la misma tabla de colores una vez por fotograma.

La app mantiene un único reloj monótono compartido por ambos lados de una transición y por Pop Out en el navegador. El estado nativo incluye una muestra del reloj del emisor; al sincronizar, Rust adapta ese punto de referencia a su reloj local, también al reabrir o reanudar. La latencia del IPC es la incertidumbre restante de fase. Las rampas de velocidad integran la curva de suavizado existente sin reiniciar el tiempo. Los relojes de ejecución se excluyen de los ajustes guardados, las importaciones y exportaciones y las definiciones de presets.

Las tablas de búsqueda, canalizaciones, datos de glifos y texturas de origen siguen siendo independientes de la tabla de visualización cíclica. La salida nativa/del navegador recibe los mismos controles; la salida reflejada recibe píxeles ya renderizados y no aplica ningún segundo ciclo.

<a id="spatial-stage-110"></a>

## Etapa espacial (1.1.0)

`renderers/shared/spatial-contract.json` define valores predeterminados, enumeraciones, límites y etiquetas de controles. La normalización JS, la interfaz y la validación Rust consumen ese contrato; `spatial-audio.json` define las rutas de audio acotadas adicionales. El movimiento de escena reutiliza el integrador de movimiento de paleta con estado propio, de modo que los cambios de velocidad con signo conservan la fase. La salida nativa ajusta la referencia del reloj emisor. El estado de movimiento y reinicio solo existe durante la ejecución y se excluye de los presets guardados.

`spatial-shader.wgsl.js` contiene los cálculos originales compartidos de escena y efectos posteriores al color. WebGPU y wgpu nativo lo usan directamente. `spatial-shader.js` convierte su subconjunto pequeño de sintaxis con tipos explícitos a GLSL; no es un traductor general de WGSL. La compilación real de sombreadores y las comparaciones de píxeles cubren ambos lenguajes. `spatial-canvas.js` es la referencia de geometría y efectos por software.

El motor inicial lanza un rayo desde el plano de cámara por celda, con un máximo de 64 pasos DDA y 40 unidades de distancia. Continúa tras los bloques bajos, intersecta cubiertas y compara la profundidad de suelos y techos con la de las paredes. El mapa se repite cada 32 unidades y limita la geometría lateral. Los hashes de fachadas muestrean justo dentro de la superficie de impacto para evitar redondeos hacia otra celda. La iluminación combina luz direccional, oscurecimiento de contacto artístico y emisión analítica de ventanas; no es iluminación global. Los suelos mojados lanzan un rayo reflejado acotado con perturbación de ondas; la lluvia usa cuatro láminas en coordenadas del mundo recortadas por la profundidad opaca. Orbitals usa hasta 48 pasos de trazado de esferas. Relief interpreta la luminancia de la fuente como altura de los bloques. El encuadre respeta la proporción física de las superficies: 2:1 en paredes y cuadrada en superficies horizontales. Los paneles grandes, el muestreo de cubiertas y techos y el fondo orbital conservan las formas de la fuente; las configuraciones opcionales mezclan entre un 80 y un 95 % del material de entrada. Los rayos incluyen la inclinación de cámara. Corridor usa un túnel estrecho y bajo; Cathedral intersecta un techo inclinado de dos planos; Coast mantiene bloques costeros bajos sin marcas viales. Relief muestrea un campo de altura y color alineado con la fuente, sin carreteras y desde una cámara elevada. Orbitals gira la cámara e inclina el anillo. El bloque de uniformes espaciales contiene diez vec4 (160 bytes); el último incluye inclinación de cámara y zoom, detalle y forma fractal.

Recursive ruins, Mandelbulb y Mandelbox comparten un trazador de esferas limitado a 64 pasos y 32 unidades, con hasta ocho iteraciones del estimador. Mandelbulb primero intersecta su esfera contenedora para omitir rayos y recorridos vacíos; calcula su potencia radial compartida una vez por iteración. Mandelbrot usa hasta 128 iteraciones, color de escape suave y un ciclo de zoom limitado a una precisión útil de float32. El color de los límites con escape lento se desvanece hacia el interior para reducir el parpadeo numérico. Las ruinas usan un campo periódico de cajas con cortes recursivos en cruz; el bulbo usa iteración de potencias esféricas y la caja usa pliegues de caja y esfera. El material de entrada controla el color de las superficies, la luminancia de los glifos y la distorsión de contornos de Mandelbrot. No se descarga código ni recursos externos durante la ejecución.

El RGB de la escena entra en la etapa existente de color, paleta y dithering. El canal alfa de cada celda sigue identificando un glifo, no una profundidad. Los glifos opcionales de materiales y bordes añaden ocho símbolos a un máximo de 88 glifos base. Una máscara estable de cobertura de 16 celdas atenúa la sustitución por materiales al aumentar la aportación del material de entrada; con aportación completa, la luminancia de la fuente elige el glifo. La dirección de los bordes usa gradientes de luminancia y el glifo anterior cerca del umbral. El procesamiento plano conserva su textura de celdas de 8 bits. Bright output es una preferencia global persistente, excluida de los presets y conservada al cambiar de preset o usar WTF. Empieza desactivada; activarla aplica la elevación de luminancia. Se conservan las preferencias guardadas. Con colores de la fuente, después de la saturación y antes del contraste y gamma, la luminancia L se eleva a L^0.22. El RGB se escala a esa luminancia y la crominancia se comprime hacia ella solo si hace falta para caber en la gama RGB. Así se conservan el tono y los extremos negro y blanco mientras se iluminan colores saturados oscuros y grises. En las paletas, la búsqueda no cambia y el RGB resultante se ilumina después para conservar los rangos de los ciclos. La luminancia de glifos aplica la misma elevación sobre la luminancia base estable de la paleta, independientemente del color animado. Las rutas de software JS, WebGL2, WGSL compartido entre navegador y salida nativa y software Rust comparten vectores de referencia. El bloque de parámetros de celda ocupa 112 bytes, con el interruptor en el byte 96. Cambiarlo actualiza los uniformes y borra el historial sin reconstruir la fuente ni los recursos GPU.

La realimentación usa dos texturas de historial reutilizables en coma flotante, separadas de la salida de celdas de 8 bits. La retención, el zoom y la rotación del historial dependen del tiempo transcurrido. WebGL2 usa dos destinos de renderizado; WebGPU y la salida nativa escriben las celdas y el historial en la misma pasada de cómputo. Los grupos de enlaces de imagen se almacenan en caché en ambas direcciones del historial. Canvas reutiliza dos arrays de coma flotante y una salida de bytes. La alternativa de bytes para WebGL2 antiguo corrige la cuantización según el tiempo transcurrido para evitar estelas permanentes. No se reconstruye el atlas de glifos ni la fuente en cada fotograma.

Cambiar de modo de escena produce una transición visual sobre la fuente existente. La salida nativa recibe los parámetros de escena, el reloj y el estado de audio acotado; las escenas aceleradas no necesitan enviar capturas de pantalla por IPC. La salida espacial de los presets asignados explícitamente a Canvas usa la ruta de duplicación existente. El softbuffer nativo informa que la ruta no está disponible si no puede presentar una escena GPU; no la sustituye silenciosamente por Flat Media. El renderizador heredado de flujos del servidor conserva su comportamiento y oculta los controles espaciales.

La caché de geometría por columna es una posible optimización futura, no parte de esta implementación. El sombreador de celdas medido sirve como referencia inicial; conserve los casos de paridad geométrica y la continuidad de la fuente al modificar el recorrido.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
