---
title: Arquitectura
description: Documentación de arquitectura derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Desarrollo
lang: es
---

<a id="architecture"></a>

# Arquitectura

Esta página reúne el contrato de arquitectura del agente del repositorio principal y las guías de renderizado en lugar de mantener aquí un modelo de propiedad paralelo.

<a id="project-identity"></a>

## Identidad del proyecto

ASCII VJ Remix es un laboratorio de renderizado de escritorio nativo local para macOS, Windows y Linux. El producto previsto es la aplicación de escritorio Tauri, no una aplicación web alojada ni una compilación exclusiva del navegador.

El repositorio combina renderizado WebGPU/WebGL de alta calidad, rutas de compatibilidad de Canvas, infraestructura de códec y flujo derivado de ASCILINE y empaquetado de escritorio Tauri. La aplicación es una superficie de control creativa para imágenes ASCII/celulares en vivo.

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

<a id="repository-ownership-map"></a>

## Mapa de propiedad del repositorio

Utilice este mapa para encontrar al probable propietario de un cambio:

|Área|Archivos primarios|
| --- | --- |
|UI principal, parámetros, ajustes preestablecidos, controles de fuente, WTF, UI de audio|[app.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/app.js), [index.html](https://github.com/aindaco1/ascii-vj-remix/blob/main/index.html), [style.css](https://github.com/aindaco1/ascii-vj-remix/blob/main/style.css)|
|Abstracción de fuente de medios y renderizador GPU|[renderizadores/gpu/](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/gpu)|
|Mapeo MIDI, soft takeover, perfil UC-33e|[midi-mapping.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/renderers/shared/midi-mapping.js), [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md)|
|Adaptador Tauri y ayudantes de visualización de salida|[renderizadores/escritorio/](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/desktop)|
|Shell Tauri, comandos, permisos, actualizador, audio nativo, salida nativa|[src-tauri/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri)|
|Entrada/salida nativa MIDI y SysEx|[midi.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/midi.rs)|
|Renderizador nativo Pop Out|[native_output.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output.rs), [gpu.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/gpu.rs)|
|Rutas de cámara nativas de la plataforma|[native_camera.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs), [ffmpeg.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/media_engine/ffmpeg.rs)|
|Motor multimedia Rust, códec, sesiones FFmpeg|[src-tauri/src/media_engine/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri/src/media_engine)|
|Medios de demostración integrados y accesorios ocultos|[medios/](https://github.com/aindaco1/ascii-vj-remix/tree/main/media)|
|Experimentos de códec/vector|[experimentos/](https://github.com/aindaco1/ascii-vj-remix/tree/main/experiments)|
|Scripts de compilación, pruebas de humo, publicación, Podman y FFmpeg|[guiones/](https://github.com/aindaco1/ascii-vj-remix/tree/main/scripts)|
|Documentos de usuario/desarrollador|[docs/](https://github.com/aindaco1/ascii-vj-remix/tree/main/docs) y [README](/es/docs/overview/ascii-vj-remix/)|

<a id="non-negotiable-constraints"></a>

## Restricciones no negociables

- El tiempo de ejecución debe ser local primero y sin conexión de forma predeterminada.
- No agregue CDN, fuentes alojadas, descodificadores alojados, telemetría ni dependencias de tiempo de ejecución en línea.
- Las rutas intencionales de tiempo de ejecución en línea se limitan a la verificación de metadatos de lanzamiento limitados de la aplicación de producción para detectar artefactos de actualización firmados en el momento del lanzamiento, acciones explícitas de descarga/instalación del actualizador y envío de informes de fallas revisados/desinfectados solo en producción.
- Conserve el nombre de la aplicación: ASCII VJ Remix.
- Conserve la dirección de la aplicación nativa para macOS, Windows y Linux.
- No replantee el modo de navegador como el producto. Las rutas del navegador/Vite son útiles para el desarrollo, las pruebas de humo y la portabilidad del renderizador.
- Mantenga alta la calidad del renderizado. La salida WebGPU/WebGL es el objetivo de calidad visual.
- Conserve las rutas alternativas a menos que se implemente y pruebe un reemplazo.
- Trate el rendimiento y la latencia de Pop Out como un comportamiento crítico de cara al usuario.
- Mantenga locales los medios locales seleccionados por el usuario. No cargue archivos ni datos de cámara/audio.
- Mantenga la superposición de estadísticas como propiedad del usuario. Los ajustes preestablecidos aleatorios, WTF mode y los ajustes preestablecidos de audio no lo desactivan a menos que el usuario lo haga explícitamente.
- La infraestructura de transmisión existe pero no es un modo de fuente visible normal. Mantenga oculta su interfaz de usuario; La productización prospectiva pertenece a la hoja de ruta.
- La seguridad, el rendimiento, la accesibilidad y la orientación de i18n se encuentran en documentos de práctica dedicados en `docs/`; actualizarlos cuando cambien los supuestos arquitectónicos.

<a id="behavior-and-ownership-constraints"></a>

## Restricciones de comportamiento y propiedad

Utilice la [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md) para conocer el comportamiento actual y el [Motor de renderizado](/es/docs/development/rendering-engine/) para conocer los contratos detallados. Al editar:

- Conserve el estado de perfil limpio Demo Image / Classic Camera ASCII y mantenga la preferencia de backend en Auto. Los perfiles existentes conservan su configuración.
- Mantenga la propiedad de backend preestablecida en `renderers/shared/preset-backend-contract.js` (71 en total, 43 acelerados, 28 Canvas explícitos). Los cambios intencionales deben actualizar el contrato y la evidencia visible de la matriz preestablecida en conjunto. La identidad de la plataforma no debe reasignar la propiedad de forma preventiva.
- Mantenga un modelo de parámetro canónico. Los ajustes preestablecidos guardados, los parámetros efectivos en vivo, la selección de fuente, las transiciones, WTF, audio, MIDI y la salida nativa deben coincidir. Las transiciones preestablecidas preservan la identidad de la fuente y la reproducción.
- Amplíe las políticas de paleta compartida, conjunto de caracteres, atlas de glifos y cuadrícula. Mantenga Advanced Density global y fuera de los ajustes preestablecidos; no agregue límites por renderizador ni búsqueda de fuentes del sistema en tiempo de ejecución. Lea la guía del renderizador antes de cambiar los límites.
- Reutilizar recursos GPU y versiones del marco fuente; no reduzca la calidad visual ni la resolución para obtener una mejora del rendimiento.
- Mantenga acotados los datos de análisis de audio y excluya el audio sin procesar de IPC y de los diagnósticos. Conserve los límites de seguridad y evite reescribir los presets guardados durante la modulación.
- Mantenga el control del UC-33e en la ruta DIN mioXC documentada. MIDI apunta al comportamiento visual, de audio, preestablecido y WTF; no debe apuntar a la fuente, la cámara, Pop Out, la visualización de salida, el archivo, el actualizador ni las acciones de informe. Lea [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar la política de mapeo o hardware.
- Conserve la interfaz de usuario densa en negro, blanco y gris con acentos de estado en rosa y azul. No reduzca la densidad de control ni agregue texto de marketing explicativo dentro de la aplicación.
- Mantenga Reports accesible con una cola vacía. Los diagnósticos del renderizador siguen el [contrato de seguridad](/es/docs/operations/security/#crash-reporting); no adjunte diagnósticos de medios locales ni registros arbitrarios.
- Mantenga la selección de backend en el control central y los diagnósticos de backend resueltos en el Stats Overlay propiedad del usuario, sin una lectura duplicada en la barra superior.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
