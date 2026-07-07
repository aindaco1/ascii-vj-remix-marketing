---
title: Motor de renderizado
description: Documentación del motor de renderizado derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Desarrollo
lang: es
---

# Motor de renderizado

Este documento describe cómo ASCII VJ Remix procesa fuentes en ASCII/celda
salida visual en contextos de navegador y escritorio Tauri.

Documentos de práctica relacionados:

- [Rendimiento](/es/docs/operations/performance/) para latencia de renderizado/salida y validación de FPS.
- [Seguridad](/es/docs/operations/security/) para medios locales, capacidad Tauri, actualizador y
Límites del sidecar FFmpeg.
- [Probando](/es/docs/operations/testing/) para el renderizador actual, los medios, la salida nativa y
matriz de validación de versiones.
- [Accesibilidad](/es/docs/operations/accessibility/) e [Internacionalización](/es/docs/operations/internationalization/) para
Reglas de UX de la superficie de control que afectan los controles orientados al renderizador.

## Objetivos

- Preservar la salida WebGPU/WebGL de alta calidad adaptada de
`ascii-point-and-click`.
- Mantenga el lienzo rápido y el linaje de transmisión adaptable de ASCILINE disponibles como respaldo
e infraestructura de desarrollo.
- Mantenga el uso normal de la aplicación localmente primero y sin conexión.
- Mantenga todos los controles en vivo encaminados a través de un modelo de parámetros canónicos.
- Permitir que los ajustes preestablecidos, WTF mode, la reactividad de audio y el control futuro de MIDI compongan
sin bifurcar el estado del renderizador.
- Mantenga la salida de Pop Out lo más libre de latencia posible, especialmente para transmisiones en vivo.
fuentes de la cámara.

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

La selección de fuente puede provenir de medios integrados, archivos seleccionados por el usuario, cámara
transmisiones, cámaras mixtas o sesiones de transmisión de desarrollo. El tiempo de ejecución del renderizador
elige el mejor backend para la fuente y el entorno activos.

## Capa de origen

### Medios integrados

Los elementos incorporados visibles son:

- Imagen de demostración: `media/demo.svg`.
- Vídeo de demostración: `media/demo-video-2.mp4`.

Accesorios ocultos como `media/point-click-test.mp4` y
`media/point-click-test-30s.mp4` permanecen para desarrollo, pruebas de paridad y
Pruebas de humo de rendimiento.

### Archivos personalizados

El modo de explorador utiliza las API de archivos del explorador y las URL de blobs. El modo Tauri utiliza un nativo
comando de diálogo y registra el archivo seleccionado bajo una identificación de medio local de sesión.
Esa identificación de medio está expuesta a la vista web a través del protocolo de activos de Tauri.

El límite de seguridad importante es que el renderizador reciba un medio reproducible.
URL o identificación registrada. No obtiene acceso amplio al sistema de archivos.

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

Los controles de la cámara incluyen selección de dispositivo, tamaño de captura, FPS, diseño, encuadre,
y espejo. Los controles del modo de orientación están ocultos cuando son irrelevantes para el objeto seleccionado.
capacidades del dispositivo.

Tauri Pop Out nativo tiene una ruta macOS adicional para salida de una sola cámara:

```text
AVFoundation capture
  -> latest BGRA/RGB frame
  -> native output renderer
```

Esa ruta evita la lectura del lienzo de WebView y se introdujo para reducir la cámara.
latencia.

### Audio

El audio no es una fuente visual. Es una fuente de análisis que modula el render.
parámetros.

Fuentes de audio del navegador:

- archivo de audio local.
- micrófono/entrada a través de `getUserMedia`.
- mostrar/tabular audio a través de `getDisplayMedia` cuando la plataforma expone un
pista de audio.

Fuentes de audio de escritorio Tauri:

- navegador/proveedores de audio web cuando estén disponibles.
- Proveedores de funciones nativas de sistema/audio de entrada para compilaciones de escritorio.

La capa de audio genera vectores de características acotadas, no buffers de audio sin formato o sin formato.
marcos visuales.

### Sesiones de transmisión

Las sesiones de transmisión son infraestructura de desarrollo/avanzada en 0.9.0.

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

La interfaz de usuario de origen normal oculta el modo de transmisión hasta que este flujo de trabajo esté listo para la normalidad.
usuarios.

## Modelo de parámetros

La aplicación mantiene un objeto de parámetro canónico, al que comúnmente se hace referencia en el código.
como `params`.

Principales grupos de parámetros:

- fuente: modo de fuente, URL/id de medio, tipo de medio, nombre de fuente.
- cámara: ID de dispositivo seleccionado, resolución, FPS, diseño, encuadre, espejo.
- backend: automático, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- cuadrícula: columnas, filas, filas automáticas, ancho de celda, alto de celda, corrección de aspecto.
- color: saturación, contraste, brillo, gamma, combinación de fondo,
cuantización.
- muestreo: FPS, cantidad de fluctuación, velocidad de fluctuación, muestra X/Y, suavizado.
- glifo/celda: modo glifo, modo sólido, juego de caracteres compacto y familia de fuentes
menús, intensidad mínima de glifos.
- flujo: códec, calidad, tolerancia, configuración del búfer, sincronización de fotogramas.
- UI/rendimiento: superposición de estadísticas, segundos de transición.

La superficie de control, ajustes preestablecidos, persistencia, cambios de fuente, WTF mode, audio
reactividad, salida nativa y MIDI futuro, todos leen o escriben a través de este
modelo.

Las transiciones estáticas entre renderizadores y familias mantienen la propiedad de los medios en `StaticRuntime`
capa. Los renderizadores Canvas2D, pixel Canvas, WebGL y WebGPU pueden realizar fundidos cruzados.
la misma fuente de video/cámara en vivo en lugar de destruir y recargar medios cuando
Cambios `solidMode`, `glyphMode`, `pixel` o `backend`.

### Matemáticas de renderizado compartido

La versión 0.9.2 comienza a reducir las matemáticas del renderizador duplicado sin cambiar lo visible
Salida de lienzo o flujo.

Los ayudantes compartidos de JavaScript viven en:

```text
renderers/shared/render-math.js
renderers/shared/render-math-vectors.json
```

El módulo compartido posee actualmente:

- Procesamiento de color estilo GPU utilizado por instantáneas de software y pruebas de paridad nativa.
- Procesamiento de color Legacy Canvas.
- Procesamiento de color de flujo heredado.
- Ayudantes de hash de jitter estilo sombreador.
- conjunto de caracteres compacto y ayudantes de luminancia a glifo.

Las funciones heredadas de Canvas y Stream se nombran intencionalmente por separado de
la función GPU. La cuantización del lienzo/transmisión y el comportamiento de combinación de fondo son
conservado en 0.9.2 por lo que esta versión no introduce regresiones visuales mientras
el contrato de sombreador/matemático se está consolidando.

`npm run test:render-math` valida los ayudantes JavaScript contra compartidos
vectores. Las pruebas de salida nativa Rust consumen el mismo archivo vectorial para el color GPU
paridad de procesamiento.

### Parámetros efectivos

Algunas funciones deberían afectar la representación en vivo sin cambiar el estado guardado.

La reactividad del audio es el ejemplo principal:

```text
base params
  + audio feature modulation
  -> effective params
  -> renderer.updateParams()
```

Los parámetros efectivos no deben persistir en los ajustes preestablecidos del usuario a menos que el usuario
guarda explícitamente el estado actual como un valor preestablecido.

## Selección de back-end

El backend `auto` intenta primero la ruta viable de mayor calidad.

Prioridad típica del navegador:

1. WebGPU.
2. WebGL2.
3. Canvas2D.
4. Pixel Canvas cuando se seleccione o sea necesario.

El usuario puede anular el backend manualmente. Controles que no se aplican a la
El backend activo está oculto o deshabilitado.

## Renderizador WebGPU

El renderizador WebGPU es el principal objetivo de calidad.

Las fuentes de vídeo utilizan `importExternalTexture()` por cuadro. Las fuentes de imágenes se cargan una vez
con `copyExternalImageToTexture()` en un `texture_2d<f32>`.

El renderizador utiliza un flujo GPU de dos etapas:

1. Pase celular:
   - divide la fuente en una cuadrícula.
   - muestrear un punto por celda.
   - aplicar fluctuación animada por celda.
   - opcionalmente reflejar X.
   - aplicar procesamiento de color.
   - escriba un color procesado por celda en una textura de almacenamiento.
2. Pase de renderizado:
   - dibuja un triángulo de pantalla completa.
   - asigne píxeles de salida a celdas utilizando el ancho/alto de la celda.
   - buscar el color de la celda procesada.
   - llenar el lienzo de salida.

El procesamiento del color incluye:

- aumento de saturación alrededor del promedio de luminancia.
- aumento de contraste alrededor del punto medio.
- brillo.
- gama.
- Cuantización de color opcional.
- El fondo se mezcla con el color oscuro del lienzo de la aplicación.

Jitter utiliza un hash determinista sembrado por la posición y el tiempo de la celda, por lo que es estático
las imágenes pueden animarse sin cambiar el medio de origen.

## Renderizador WebGL2

El backend WebGL2 refleja el modelo visual WebGPU lo más fielmente posible:

- Los cuadros de video se cargan con `texImage2D()` por cuadro.
- Las imágenes se cargan una vez.
- primero pase muestras de un color por celda a una textura de color de celda.
- La segunda pasada expande la textura del color de la celda al lienzo visible.
- Los uniformes de sombreado coinciden con el conjunto de parámetros WebGPU siempre que sea posible.

WebGL2 es el navegador alternativo más importante porque está ampliamente disponible en
máquinas que no exponen WebGPU.

## Renderizadores de lienzo

Las rutas de lienzo conservan la compatibilidad con ASCILINE y el comportamiento de reserva de bajo nivel.

El modo glifo/texto Canvas2D representa celdas con apariencia de caracteres. Representaciones Pixel Canvas
datos de bloques/píxeles coloreados más directamente.

Estos caminos son importantes para:

- navegadores o vistas web más antiguos.
- compatibilidad con marcos de flujo.
- probando la salida del códec adaptativo.
- entornos donde falla la inicialización de GPU.

El respaldo del lienzo debe seguir siendo funcional incluso cuando no sea de la más alta calidad.
camino.

## Tiempo de ejecución estático

`StaticRuntime` administra fuentes locales nativas del navegador y backends GPU/Canvas.

Responsabilidades:

- cargar o reconstruir la fuente activa.
- elija el servidor.
- iniciar y detener la reproducción multimedia.
- mantenga vivo el renderizador a través de cambios de parámetros seguros en vivo.
- reconstruir las superficies del renderizador cuando cambian los parámetros estructurales.
- preservar el estado de reproducción de vídeo al cambiar ajustes preestablecidos que no cambian el
fuente.
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

## Tiempo de ejecución de la transmisión

`StreamRuntime` maneja secuencias de cuadros codificados estilo ASCILINE.

Puede consumir:

- Marcos WebSocket del servidor Python/FastAPI heredado.
- lotes de sesiones nativas Rust/FFmpeg en las rutas de desarrollo Tauri.

Las tramas de flujo transportan metadatos INIT y mensajes de framebuffer. El decodificador JS
apoya:

- marcos sin procesar heredados.
- RAW adaptativo.
- ZLIB adaptativo.
- DELTA adaptativo.

El modo de transmisión permanece oculto de la interfaz de usuario de origen normal en 0.9.0. se retiene
para el desarrollo y la futura productización.

## Códec adaptativo

El códec adaptativo existe para reducir el ancho de banda en comparación con el envío completo
framebuffer cada cuadro.

Cada cuadro codificado elige uno de:

- RAW: búfer de fotogramas completo.
- ZLIB: framebuffer comprimido.
- DELTA: celdas cambiadas desde el cuadro anterior.

La calidad del códec puede permitir deltas temporales basados en tolerancias para planos de color mientras
manteniendo los planos de los personajes exactos cuando corresponda.

Reglas de compatibilidad:

- Los clientes heredados existentes aún pueden recibir marcos sin formato.
- Los decodificadores JS y Rust deben seguir siendo compatibles con los vectores generados por Python.
- Los cambios de códec requieren pruebas vectoriales.

## Canalización de medios Rust/FFmpeg

La ruta Rust/FFmpeg transfiere la ruta de preparación de flujo Python/FastAPI hacia un
Motor local empaquetado en escritorio.

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

- `media_engine::ffmpeg`: FFmpeg/ffprobe límite de proceso, sonda de vídeo, RGB
Lector, opciones de lector de cámara.
- `media_engine::frame_prep`: framebuffer de texto/color/píxel compatible con ASCILINE
preparación.
- `media_engine::codec`: codificador/decodificador de códec adaptativo.
- `media_engine::pipeline`: decodificar -> preparación -> codificar -> decodificar opcional
verificación.

Modos de preparación de fotogramas:

- Modo texto: escala de grises a paleta ASCII.
- Modos de color 2 a 5: celdas `[char, R, G, B]` con niveles de color cuantificados.
- Modo de píxel: celdas `[B, G, R]`.

La ruta Rust no pretende reemplazar el renderizador estático WebGPU/WebGL. es
la respuesta a largo plazo para la preparación de medios empaquetados estilo streaming y más amplia
soporte de decodificación nativa.

## Representador de salida nativo

El renderizador de salida nativo existe porque se abrió una segunda ventana emergente renderizada por WebView.
Demasiado caro para salidas en vivo de baja latencia.

Flujo de escritorio:

```text
main UI params/source state
  -> Tauri native output command
  -> native output state
  -> source frame acquisition
  -> native `wgpu` presenter
  -> output window
```

Para imágenes/vídeos respaldados por archivos, Rust resuelve recursos empaquetados o registrados
ID de medios, decodifica fotogramas, carga el último fotograma en GPU, aplica la celda
matemáticas de color y presentaciones a través de la cadena de intercambio nativa.

Para la salida de una sola cámara macOS, AVFoundation captura los últimos fotogramas directamente para
el presentador nativo. Los ajustes preestablecidos de la cámara en vivo no deben usar el espejo del navegador
transporte de forma predeterminada porque la lectura del lienzo y la transferencia de cuadros IPC también son
caro para una producción sostenida.

Para los ajustes preestablecidos de glifos de estilo Canvas2D, la salida nativa consume el mismo valor canónico.
Parámetros `glyphMode` y `charset` como superficie de control. El `wgpu` nativo
El presentador utiliza un atlas de glifos de mapa de bits fijo y una rampa de luminancia para
Los ajustes preestablecidos tradicionales de ASCII permanecen como texto en Pop Out en lugar de volverse sólidos.
celdas de color. Los ajustes preestablecidos de estilo WebGL/WebGPU desactivan el enmascaramiento de glifos nativos incluso cuando
sus parámetros guardados todavía llevan `glyphMode`; su vista previa principal se muestra sólida
GPU rectángulos de celda, por lo que Pop Out hace lo mismo.
`fontFamily` sigue siendo un parámetro de superficie de control/previsualización; el camino nativo lo hace
no cargue fuentes arbitrarias y en su lugar enmascare celdas a través del atlas/rampa fijo.

Para fuentes alternativas/espejadas, se pueden enviar instantáneas de píxeles sin procesar delimitadas desde el
renderizador principal a la salida nativa.

Reglas de diseño de salida nativas:

- La ventana de salida no debe poseer amplios permisos Tauri.
- El presentador debe consumir los últimos parámetros en vivo.
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

La amortiguación de mezcla densa utiliza la función de densidad para reducir el ritmo y el flujo intensos.
Modulación durante pasajes de banda ancha concurridos sin silenciar transitorios dispersos.

Los objetivos de modulación son controles visuales seguros para la vida:

- brillo.
- contraste.
- saturación.
- gama.
- mezcla de fondo.
- cantidad de inquietud.
- velocidad de fluctuación.
- compensaciones de muestra.

Controles estructurales como fuente, backend, asignación de cuadrícula y dispositivos de cámara.
no se modulan por tiempo porque provocarían una rotación del renderizador.

## Presets, modo WTF y futuro MIDI

Todas estas son capas de control sobre el mismo modelo de parámetros.

Preajustes:

- aplicar conjuntos de parámetros conocidos.
- puede especificar la duración de la transición.
- Los usuarios pueden guardar/importar/exportar.

WTF mode:

- crea parámetros de destino aleatorios.
- ancla algunos estados aleatorios alrededor de familias preestablecidas extremas y tradicionales
Preajustes ASCII.
- transiciones indefinidamente hasta que se detiene.
- evita estados inseguros donde todo blanco/todo negro.

Futuro MIDI:

- debe utilizar un registro de destino de control compartido.
- debería llamar a los mismos configuradores que los controles visibles de la interfaz de usuario.
- debe respetar los metadatos de objetivos de vida segura frente a los estructurales.
- no debe bifurcar el estado del renderizador.

## Empaquetado y tiempo de ejecución sin conexión

El renderizador no debe depender de los recursos en línea en tiempo de ejecución.

Los activos empaquetados incluyen:

- paquete de interfaz.
- código de renderizado.
- Activos GPU.
- fuentes.
- medios de demostración incorporados.
- Código nativo Tauri.
- futuros sidecars FFmpeg revisados.

El CSP de producción bloquea el acceso remoto arbitrario al tiempo de ejecución HTTP(S). el activo
El protocolo tiene un alcance limitado y una sesión local para los medios seleccionados por el usuario.

## Estrategia de prueba

Las pruebas relacionadas con el renderizador deben cubrir:

- Inicio de fuente estática.
- conmutación de fuente.
- fuente de la cámara y rutas de dispositivos falsos.
- aplicación preestablecida.
- suavidad de transición.
- WebGL2 y respaldos de Canvas.
- Ubicación de la pantalla de salida.
- rendimiento de salida nativa y análisis de registros.
- vectores de códec adaptativos.
- Rust/Paridad de preparación de fotogramas de Python.
- FFmpeg/OpenCV decodifica/cambia el tamaño de la paridad limitada.

Comandos útiles:

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

## Trabajo de ingeniería abierto

- Consolide las matemáticas de colores duplicados en WebGPU, WebGL2, Canvas, stream y
salida nativa.
- Agregue rutas de cámara más directas para compartir texturas:
  - AVFoundation/CVPixelBuffer/Metal en macOS.
  - Media Foundation/D3D en Windows.
  - PipeWire/V4L2/Vulkan o GLES en Linux.
- Productice el modo de transmisión o manténgalo oculto.
- Agregue el registro de control MIDI y el adaptador nativo MIDI.
- Mejore la captura de audio del sistema nativo a través de API de plataforma más estrechas.
- Agregue pruebas de rendimiento que reproduzcan Pop Out/ventana principal informada por el usuario
la contienda automáticamente.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
