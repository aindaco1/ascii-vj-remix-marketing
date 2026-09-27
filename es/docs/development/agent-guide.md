---
title: Guía para agentes
description: Documentación de la Guía del agente derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Desarrollo
lang: es
---

<a id="agent-guide"></a>

# Guía para agentes

Este documento es para agentes codificadores LLM que trabajan en ASCII VJ Remix. Explica qué contexto cargar primero, qué restricciones del proyecto son más importantes y qué archivos suelen poseer cada tipo de cambio.

<a id="fast-context-load"></a>

## Carga rápida de contexto

Léalos en orden antes de realizar cambios no triviales:

1. [README](/es/docs/overview/ascii-vj-remix/): descripción general del producto, conceptos básicos de instalación, primera ejecución y versión fuente/lanzamiento actual. La [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md) posee el conjunto completo de funciones, requisitos del sistema, permisos y solución de problemas.
2. [Changelog](/es/docs/reference/changelog/): cambios recientes publicados y no publicados.
3. [Roadmap](/es/docs/reference/roadmap/): solo trabajos potenciales.
4. [Motor de renderizado](/es/docs/development/rendering-engine/): flujo de origen, backends de renderizado, salida nativa, motor de medios, reactividad de audio e integración de MIDI.
5. [Guía del colaborador](/es/docs/development/contributing/): configuración, identidad de la aplicación local, FFmpeg, Podman y flujo de trabajo de contribución.
6. [Pruebas](/es/docs/operations/testing/): selección de comprobaciones y verificación manual. Consulte las guías de [Seguridad](/es/docs/operations/security/), [Rendimiento](/es/docs/operations/performance/), [Accesibilidad](/es/docs/operations/accessibility/) e [Internacionalización](/es/docs/operations/internationalization/) que correspondan al comportamiento afectado.

El [índice de documentación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md) enlaza todas las guías mantenidas. Para tareas de empaquetado, firma, publicación o actualización, consulte también la [Guía de lanzamiento y actualizaciones](/es/docs/operations/release/). Los [registros de versiones](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) conservan evidencia histórica y no sustituyen las guías actuales.

Para el trabajo con MIDI, mapeo UC-33e o SysEx, lea también [UC-33e y mioXC MIDI Control](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

Para el trabajo de permisos o empaquetado de escritorio, inspeccione también:

- [Tauri configuración](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/tauri.conf.json)
- [Tauri capacidades](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/capabilities/default.json)
- [macOS Información.plist](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/Info.plist)
- [macOS derechos](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/Entitlements.plist)

Para trabajos de renderizado o Pop Out, inspeccione también:

- [Controlador de aplicación principal](https://github.com/aindaco1/ascii-vj-remix/blob/main/app.js)
- [directorio de renderizado GPU](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/gpu)
- [Adaptador de escritorio](https://github.com/aindaco1/ascii-vj-remix/blob/main/renderers/desktop/tauri-adapter.js)
- [Módulo de salida nativo](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output.rs)
- [Salida nativa GPU presentador](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/gpu.rs)
- [Módulo de cámara nativo](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs)

<a id="project-identity"></a>

## Identidad del proyecto

ASCII VJ Remix es un laboratorio de renderizado de escritorio nativo local para macOS, Windows y Linux. El producto previsto es la aplicación de escritorio Tauri, no una aplicación web alojada ni una compilación exclusiva del navegador.

El repositorio combina renderizado WebGPU/WebGL de alta calidad, rutas de compatibilidad de Canvas, infraestructura de códec y flujo derivado de ASCILINE y empaquetado de escritorio Tauri. La aplicación es una superficie de control creativa para imágenes ASCII/celulares en vivo.

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
- Mantenga la propiedad de backend preestablecida en `renderers/shared/preset-backend-contract.js` (79 en total, 51 acelerados, 28 Canvas explícitos). Los cambios intencionales deben actualizar el contrato y la evidencia visible de la matriz preestablecida en conjunto. La identidad de la plataforma no debe reasignar la propiedad de forma preventiva.
- Mantenga un modelo de parámetro canónico. Los ajustes preestablecidos guardados, los parámetros efectivos en vivo, la selección de fuente, las transiciones, WTF, audio, MIDI y la salida nativa deben coincidir. Las transiciones preestablecidas preservan la identidad de la fuente y la reproducción.
- Amplíe las políticas de paleta compartida, conjunto de caracteres, atlas de glifos y cuadrícula. Mantenga Advanced Density global y fuera de los ajustes preestablecidos; no agregue límites por renderizador ni búsqueda de fuentes del sistema en tiempo de ejecución. Lea la guía del renderizador antes de cambiar los límites.
- Reutilizar recursos GPU y versiones del marco fuente; no reduzca la calidad visual ni la resolución para obtener una mejora del rendimiento.
- Mantenga acotados los datos de análisis de audio y excluya el audio sin procesar de IPC y de los diagnósticos. Conserve los límites de seguridad y evite reescribir los presets guardados durante la modulación.
- Mantenga el control del UC-33e en la ruta DIN mioXC documentada. MIDI apunta al comportamiento visual, de audio, preestablecido y WTF; no debe apuntar a la fuente, la cámara, Pop Out, la visualización de salida, el archivo, el actualizador ni las acciones de informe. Lea [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar la política de mapeo o hardware.
- Conserve la interfaz de usuario densa en negro, blanco y gris con acentos de estado en rosa y azul. No reduzca la densidad de control ni agregue texto de marketing explicativo dentro de la aplicación.
- Mantenga Reports accesible con una cola vacía. Los diagnósticos del renderizador siguen el [contrato de seguridad](/es/docs/operations/security/#crash-reporting); no adjunte diagnósticos de medios locales ni registros arbitrarios.
- Mantenga la selección de backend en el control central y los diagnósticos de backend resueltos en el Stats Overlay propiedad del usuario, sin una lectura duplicada en la barra superior.

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

<a id="working-safely"></a>

## Trabajar con seguridad

Antes de editar:

- Marque `git status --short`.
- Suponga que los cambios no confirmados pueden ser trabajo del usuario.
- No restablezca, retire ni revierta cambios no relacionados.
- Busque con `rg` antes de cambiar el comportamiento compartido.
- Prefiera los patrones existentes y las API auxiliares a las nuevas abstracciones.
- Mantenga los cambios en el ámbito de la solicitud.

Al editar:

- Utilice el modelo de parámetros canónicos en lugar de crear un estado de renderizado paralelo.
- Mantenga la selección de fuente, los ajustes preestablecidos, WTF mode, la modulación de audio y la sincronización de salida nativa en concordancia.
- Preservar el modelo de capacidad y permisos limitados de Tauri.
- Mantenga los activos de tiempo de ejecución agrupados localmente.
- Utilice scripts de compilación existentes en lugar de comandos de compilación ad hoc cuando sea posible.
- Actualice la documentación cuando cambie el comportamiento del producto, el proceso de publicación, la arquitectura del renderizador o los requisitos de configuración.

<a id="validation-and-packaging"></a>

## Validación y empaquetado

`npm test` ejecuta las comprobaciones estáticas/de escritorio existentes además de Jev en vivo en evidencia de componentes sintéticos incorporados. Utilice `-- --offline` explícitamente para omitir la evaluación alojada. Mantenga Jev solo para desarrollo y reutilice la entrada anclada de Plataforma Test Core; consulte [Pruebas de desarrollo Jev](/es/docs/operations/testing/#jev-development-testing). Nunca pase diagnósticos o medios privados a este evaluador ni interprete su resultado como visual, hardware nativo o aceptación de versión.

Utilice [Pruebas: conjuntos de comprobaciones recomendados](/es/docs/operations/testing/#recommended-check-sets) para elegir las comprobaciones mínimas que cubran el cambio. Los cambios de documentación requieren `git diff --check`; si mueve archivos, también debe validar enlaces, anclas y referencias a rutas. Distinga entre comprobaciones locales, paquetes de CI, pruebas de humo de la aplicación instalada y aceptación en hardware físico.

Utilice [Guía del colaborador](/es/docs/development/contributing/) para comandos de compilación locales y [identidad de desarrollo macOS](/es/docs/development/contributing/#macos-permissions-during-development). Las compilaciones locales normales utilizan `ASCII VJ Remix Dev` / `com.asciline.remix.dev` y las pruebas de permisos requieren una firma local estable. La guía para colaboradores también posee el comportamiento del directorio de compilación de iCloud y el flujo de generación de íconos canónicos.

Utilice la [Guía de lanzamiento y actualizaciones](/es/docs/operations/release/) para la configuración de paquetes, firmas, secretos, recursos de FFmpeg y validación de artefactos publicados. El empaquetado con actualizador habilitado requiere la clave de firma y su contraseña; la falta de secretos no justifica reducir las comprobaciones de publicación. Nunca incluya esos secretos en el repositorio. Esa guía y [Seguridad](/es/docs/operations/security/) definen la firma pública de macOS y los actuales paquetes preliminares sin firmar de Windows.

<a id="renderer-mental-model"></a>

## Modelo mental del renderizador

Utilice este flujo cuando razone sobre errores:

```text
source selection
  -> source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

Implicaciones importantes:

- Los parámetros guardados y los parámetros efectivos son diferentes. La reactividad del audio modifica los parámetros efectivos, no las definiciones preestablecidas guardadas.
- La identidad de la fuente importa. Las transiciones preestablecidas no restablecen la fuente ni reinician la reproducción multimedia.
- La salida nativa necesita nuevos parámetros y marcos. Si Pop Out parece obsoleto, inspeccione la sincronización de salida nativa antes de agregar otro renderizador.
- El trabajo de latencia de la cámara utiliza rutas de captura/presentación nativas del último fotograma cuando se implementan en lugar de rutas de decodificación almacenadas en búfer.
- Las rutas alternativas son importantes para Windows/Linux y para entornos sin el mejor backend GPU.

Consulte [Motor de renderizado](/es/docs/development/rendering-engine/) para obtener detalles de arquitectura más profundos.

<a id="documentation-update-rules"></a>

## Reglas de actualización de documentación

Consulte la distribución de responsabilidades del [índice de documentación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md). Actualice la guía mantenida que corresponda y enlace a ella, en lugar de duplicar procedimientos:

- Descripción general del producto, conceptos básicos de instalación, primera ejecución: [root README](/es/docs/overview/ascii-vj-remix/).
- Comportamiento detallado del usuario, requisitos, permisos y solución de problemas: [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md).
- Cambios publicados/inéditos: [Changelog](/es/docs/reference/changelog/).
- Propuestas y trabajos futuros: [Roadmap](/es/docs/reference/roadmap/).
- Renderizado/medios/salida/audio/arquitectura MIDI: [Motor de renderizado](/es/docs/development/rendering-engine/).
- Configuración local, identidad de desarrollo, FFmpeg/Podman, contribuciones: [Guía del colaborador](/es/docs/development/contributing/).
- Procedimiento de empaquetado, firma, publicación, actualización: [Guía de lanzamiento](/es/docs/operations/release/).
- Decisiones y pruebas específicas de la versión: [registros de publicación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md).
- Seguridad, rendimiento, selección de comprobaciones, accesibilidad y propiedad de cadenas: la guía práctica correspondiente vinculada anteriormente.
- Incorporación de agentes y propiedad de la fuente: este archivo.

Las guías del estado actual describen el comportamiento verificado en tiempo presente. Mantenga las propuestas en la hoja de ruta y los planes completados en los registros de publicación. Las pruebas pueden indicar brechas de cobertura conocidas, pero una fila histórica pendiente no debe convertirse en un reclamo sobre el estado de liberación actual. Mantenga la aplicación nativa de documentos enfocada y preserve los límites de evidencia de fuente/CI/artefacto/aplicación instalada/plataforma física.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
