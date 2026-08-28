---
title: Guía para agentes
description: Documentación de la Guía del agente derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Desarrollo
lang: es
---

# Guía para agentes

Este documento es para agentes codificadores LLM que trabajan en ASCII VJ Remix. Explica qué contexto cargar primero, qué restricciones del proyecto son más importantes y qué archivos suelen poseer cada tipo de cambio.

## Carga rápida de contexto

Léalos en orden antes de realizar cambios no triviales:

1. [README](/es/docs/overview/ascii-vj-remix/): descripción general del producto, conjunto de funciones actuales para el usuario, notas de instalación, requisitos del sistema, licencia/soporte/información de contacto.
2. [Changelog](/es/docs/reference/changelog/): línea base de características de la versión actual y expectativas de comportamiento recientes.
3. [Roadmap](/es/docs/reference/roadmap/): solo trabajos potenciales.
4. [Motor de renderizado](/es/docs/development/rendering-engine/): flujo de origen, backends de renderizado, arquitectura de salida nativa, motor de medios, reactividad de audio e integración de MIDI.
5. [Guía del colaborador](/es/docs/development/contributing/): configuración de desarrollo, comandos de prueba, notas de versión/actualización, política complementaria de FFmpeg y flujo de trabajo de contribución.
6. Documentos de práctica del proyecto cuando sea relevante: [Security](/es/docs/operations/security/), [Performance](/es/docs/operations/performance/), [Testing](/es/docs/operations/testing/), [Accessibility](/es/docs/operations/accessibility/) e [Internationalization](/es/docs/operations/internationalization/).

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

## Identidad del proyecto

ASCII VJ Remix es un laboratorio de renderizado de escritorio nativo local para macOS, Windows y Linux. El producto previsto es la aplicación de escritorio Tauri, no una aplicación web alojada ni una compilación exclusiva del navegador.

El repositorio combina renderizado WebGPU/WebGL de alta calidad, rutas de compatibilidad de Canvas, infraestructura de códec y flujo derivado de ASCILINE y empaquetado de escritorio Tauri. La aplicación es una superficie de control creativa para imágenes ASCII/celulares en vivo.

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

## Línea de base actual orientada al usuario

La versión actual del código fuente/paquete y la última versión pública verificada son 0.9.12. El registro de cambios posee el historial de versiones; la Hoja de Ruta es sólo prospectiva.

Fuentes:

- La imagen de demostración es la fuente de inicio predeterminada.
- El vídeo de demostración es la única fuente de vídeo integrada visible.
- Se pueden seleccionar imágenes y videos locales personalizados.
- La cámara es una fuente de primera clase.
- Se pueden combinar varias cámaras localmente cuando el sistema operativo o el tiempo de ejecución admiten la captura simultánea.
- Los controles de la cámara aparecen directamente debajo de Fuente mientras la cámara está activa.

Representación:

- WebGPU es el principal objetivo de calidad.
- WebGL2 es el principal respaldo integrado de GPU.
- Canvas2D y Pixel Canvas siguen siendo alternativas de compatibilidad.
- La salida nativa Pop Out usa `wgpu` cuando esté disponible, con Metal en macOS y los backends GPU correspondientes en Windows/Linux.
- El renderizador activo está controlado por un modelo de parámetro canónico.
- El Pop Out nativo conserva los parámetros del modo glifo y del conjunto de caracteres para los ajustes preestablecidos ASCII tradicionales.
- Dieciséis paletas nativas del proyecto, mapeo de luminancia/más cercano y difuminado Bayer 2x2/4x4/8x8 utilizan el catálogo de paletas compartido y la LUT de 32x32x32 en caché.
- El atlas Unicode generado neutral cubre los bloques BMP comunes aprobados en dieciséis páginas de 1024px. La caché de páginas decodificadas del navegador tiene un límite de cuatro; La salida nativa y del navegador GPU utiliza identificadores escalares Unicode y una rampa máxima de 96 identificadores.
- La densidad normal está limitada por la columna acelerada/software compartida y los límites totales de celdas. Advanced Density es global, permite hasta 900 columnas sin una garantía de 30 FPS y nunca debe almacenarse en ajustes preestablecidos visuales.
- El catálogo de conjunto de caracteres compartido incluye 23 rampas de luminancia derivadas de ascii.today acreditadas y ajustes preestablecidos de solo lectura coincidentes.
- La salida de glifos nativos utiliza recursos de rampa/atlas paginados delimitados; `fontFamily` son metadatos de interfaz de usuario/vista previa, no un receptor de carga de fuentes nativo.
- Reutilice recursos estables WebGPU/WebGL, mantenga las cargas de fuentes nativas vinculadas a las versiones del marco de origen y no intercambie calidad/resolución por rendimiento.

Comportamiento en vivo:

- Los ajustes preestablecidos son de solo lectura a menos que los cree el usuario.
- Las transiciones preestablecidas son fundidos cruzados suaves, no fundidos a negro.
- Los ajustes preestablecidos conservan la fuente de medios activa a menos que se cambien explícitamente.
- WTF mode se ejecuta indefinidamente mientras está activo y realiza transiciones a través de configuraciones aleatorias seguras en vivo, incluidos anclajes de ajustes preestablecidos ASCII tradicionales.
- La reactividad de audio está habilitada de forma predeterminada, comienza desde el micrófono/entrada de forma predeterminada y modula los parámetros efectivos en vivo sin reescribir los ajustes preestablecidos guardados.
- La reactividad de audio utiliza vectores de características acotados, incluidos RMS, bandas, transitorios/flujo, presencia, brillo, densidad, pulso y fase. No envíe buffers de audio sin procesar a través de IPC o diagnósticos.
- Los límites de seguridad evitan que las salidas de negro puro o blanco puro entren en estados aleatorios o controlados por audio.
- El equipo experimental MIDI es el UC-33e a través de ambas direcciones DIN de un mioXC; No se admite UC USB directo.
- MIDI utiliza cuatro páginas con dirección de canal, toma de control suave, espacios preestablecidos numéricos, anulaciones de aprendizaje de MIDI y captura/restauración de banco completo limitado de SysEx.
- MIDI apunta únicamente al comportamiento visual/audio/preestablecido/WTF. No agregue acciones de fuente, cámara, Pop Out, visualización de salida, archivo, actualizador o informe de fallas.
- Lea [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar las asignaciones o la política de hardware.

Interfaz de usuario:

- El tema actual es negro/blanco/gris extremo con detalles en rosa neón y azul neón.
- El diseño es intencionadamente denso.
- No reduzca la densidad de control al cambiar el estilo visual.
- Evite agregar texto de marketing explicativo dentro de la interfaz de usuario de la aplicación.
- Mantenga accesible el control Reports de la barra superior con una cola vacía; El estado pendiente es aditivo. No adjunte diagnósticos de medios locales ni registros arbitrarios.
- Mantenga la selección de backend en el control central. Los diagnósticos de backend resueltos pertenecen al Stats Overlay propiedad del usuario, no a una lectura duplicada de la barra superior.

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
|Ruta de latencia de cámara nativa macOS|[native_camera.rs](https://github.com/aindaco1/ascii-vj-remix/blob/main/src-tauri/src/native_output/native_camera.rs)|
|Motor multimedia Rust, códec, sesiones FFmpeg|[src-tauri/src/media_engine/](https://github.com/aindaco1/ascii-vj-remix/tree/main/src-tauri/src/media_engine)|
|Medios de demostración integrados y accesorios ocultos|[medios/](https://github.com/aindaco1/ascii-vj-remix/tree/main/media)|
|Experimentos de códec/vector|[experimentos/](https://github.com/aindaco1/ascii-vj-remix/tree/main/experiments)|
|Construir, fumar, liberar, Podman, scripts FFmpeg|[guiones/](https://github.com/aindaco1/ascii-vj-remix/tree/main/scripts)|
|Documentos de usuario/desarrollador|[docs/](https://github.com/aindaco1/ascii-vj-remix/tree/main/docs) y [README](/es/docs/overview/ascii-vj-remix/)|

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
- Update documenta al cambiar el comportamiento del producto, el comportamiento de la versión, la arquitectura del renderizador o los requisitos de configuración.

## Comandos de validación comunes

Elija el conjunto más pequeño que cubra el cambio.

Sólo documentación:

```bash
git diff --check
```

Para una selección de pruebas más amplia, lea [Testing](/es/docs/operations/testing/).

Comportamiento de interfaz/UI/fuente:

```bash
npm run build
npm run smoke:static
```

Comportamiento Rust/Tauri:

```bash
npm run test:rust
npm run check:desktop
```

Comportamiento MIDI:

```bash
npm run test:midi
npm run midi:probe -- --connect
npm run test:rust
```

Construcción optimizada de la aplicación macOS:

```bash
npm run tauri:build:dev -- --bundles app
```

Embalaje de lanzamiento:

```bash
npm run ffmpeg:build-sidecar
npm run check:release
npm run bundle:release
```

Nota de compilación de lanzamiento local esperada:

- Los artefactos públicos 0.9.12 macOS están firmados con ID de desarrollador, notariados, engrapados y validados por Gatekeeper. Los artefactos públicos 0.9.12 Windows son vistas previas sin firmar. Las compilaciones locales normales utilizan `ASCII VJ Remix Dev` / `com.asciline.remix.dev`; el iniciador local requiere una identidad estable antes de realizar la prueba de permiso.
- Si `TAURI_SIGNING_PRIVATE_KEY` o `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` están ausentes mientras los artefactos del actualizador están habilitados, el paquete de versiones fallará al firmar el actualizador. Las rutas de validación locales están documentadas en la guía para contribuyentes; nunca confirme ninguno de los archivos.

## Tauri y notas de embalaje

- Tauri v2 es el shell del escritorio.
- Las compilaciones de producción realizan una verificación de actualización sin bloqueo por lanzamiento. Una verificación de antecedentes actual o fallida permanece en silencio; descargar/instalar sigue siendo una acción explícita del usuario a través del control Update existente.
- `src-tauri/tauri.conf.json` es la configuración base de producción multiplataforma; su identidad ad hoc macOS se utiliza únicamente en rutas de empaquetado explícitas y no certificadas por notario.
- `src-tauri/tauri.dev.conf.json` aísla los comandos locales normales del nombre de producción, el identificador del paquete y el actualizador.
- `src-tauri/tauri.notarized.conf.json` es para compilaciones de lanzamiento de macOS certificadas por ID de desarrollador.
- `assets/branding/ascii-vj-remix-app-icon-1024.png` es el ícono de la aplicación canónica. Ejecute `npm run icons:generate` en lugar de editar archivos de plataforma en `src-tauri/icons/` de forma independiente; `npm run check:icons` verifica el conjunto generado completo.
- `src-tauri/tauri.windows-signed.conf.json` y su asistente Authenticode existen pero están inactivos. La ruta de lanzamiento actual de Windows utiliza la configuración sin firmar predeterminada.
- macOS se integra en los espacios de trabajo de iCloud Drive y redirige la salida de destino a `/private/tmp/ascii-vj-remix-tauri-target` a través de scripts auxiliares para evitar que los atributos extendidos de iCloud rompan el código de diseño.
- Los artefactos del actualizador de versiones están firmados con una clave minisign. La clave pública está comprometida; la clave privada pertenece a los secretos de acciones GitHub.
- Los sidecars FFmpeg deben ser revisados, locales y verificados por políticas. La aplicación empaquetada no descarga FFmpeg, códecs, recursos de renderizado ni fuentes en tiempo de ejecución.

Consulte la [Guía del colaborador: Trabajo de publicación y actualización](/es/docs/development/contributing/#trabajo-de-lanzamiento-y-actualización) para conocer el procedimiento completo de publicación/actualización.

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

## Reglas de actualización de documentación

Cuando el comportamiento cambie, actualice el documento duradero más cercano:

- Función de cara al usuario o comportamiento de instalación: [README](/es/docs/overview/ascii-vj-remix/).
- Comportamiento de versiones actuales e inéditas: [Changelog](/es/docs/reference/changelog/).
- Solo trabajo prospectivo: [Roadmap](/es/docs/reference/roadmap/).
- Arquitectura de renderizador, flujo de medios, salida nativa, modulación de audio, arquitectura MIDI: [Rendering Engine](/es/docs/development/rendering-engine/).
- Compilación, prueba, lanzamiento, FFmpeg, Podman o flujo de trabajo del colaborador: [Guía del colaborador](/es/docs/development/contributing/).
- Modelo de seguridad, medios locales, permisos, firma del actualizador o capacidades Tauri: [Security](/es/docs/operations/security/).
- Representador sensible al rendimiento, Pop Out, cámara, audio o comportamiento de la fuente: [Performance](/es/docs/operations/performance/).
- Selección de cheques y verificación manual: [Testing](/es/docs/operations/testing/).
- Comportamiento del teclado/enfoque/contraste/etiqueta de control: [Accesibilidad](/es/docs/operations/accessibility/).
- Cadena visible para el usuario, configuración regional o arquitectura de traducción: [Internacionalización](/es/docs/operations/internationalization/).
- Supuestos de incorporación de agentes: este archivo.

Mantenga la atención en la aplicación nativa de Documentos. Los documentos del estado actual utilizan el tiempo presente y describen el comportamiento verificado. No incluya propuestas, futuros candidatos, trabajos diferidos o planes de liberación completos en esos documentos. Coloque los trabajos potenciales en [Roadmap](/es/docs/reference/roadmap/) y mantenga el historial de lanzamientos en [Changelog](/es/docs/reference/changelog/).


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
