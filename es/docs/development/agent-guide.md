---
title: Guía para agentes
description: Documentación de la Guía del agente derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Desarrollo
lang: es
---

# Guía para agentes

Este documento es para agentes codificadores LLM que trabajan en ASCII VJ Remix. explica
qué contexto cargar primero, qué restricciones del proyecto son más importantes y qué
Los archivos suelen ser propietarios de cada tipo de cambio.

## Carga rápida de contexto

Léalos en orden antes de realizar cambios no triviales:

1. [README](/es/docs/overview/ascii-vj-remix/): descripción general del producto, conjunto de funciones actuales para el usuario,
Notas de instalación, requisitos del sistema, licencia/soporte/información de contacto.
2. [Changelog](/es/docs/reference/changelog/): línea base de características de la versión actual y reciente
expectativas de comportamiento.
3. [Roadmap](/es/docs/reference/roadmap/): solo trabajos potenciales.
4. [Motor de renderizado](/es/docs/development/rendering-engine/): flujo de origen, backends del renderizador,
arquitectura de salida nativa, motor multimedia, reactividad de audio y MIDI
integración.
5. [Guía del colaborador](/es/docs/development/contributing/): configuración de desarrollo, comandos de prueba,
notas de la versión/actualización, política complementaria FFmpeg y flujo de trabajo de contribución.
6. Documentos de práctica del proyecto cuando sea relevante:
[Seguridad](/es/docs/operations/security/), [Rendimiento](/es/docs/operations/performance/),
[Pruebas](/es/docs/operations/testing/), [Accesibilidad](/es/docs/operations/accessibility/) y
[Internacionalización](/es/docs/operations/internationalization/).

Para MIDI, mapeo UC-33e o trabajo SysEx, lea también
[UC-33e y mioXC MIDI Control](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

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

ASCII VJ Remix es un laboratorio de renderizado de escritorio nativo local para macOS, Windows,
y Linux. El producto previsto es la aplicación de escritorio Tauri, no una aplicación web alojada.
o compilación solo para navegador.

El repositorio combina renderizado WebGPU/WebGL de alta calidad, Canvas
rutas de compatibilidad, infraestructura de códec y transmisión derivada de ASCILINE, y
Embalaje de escritorio Tauri. La aplicación es una superficie de control creativa para vivir.
ASCII/visuales de celda.

## Restricciones no negociables

- El tiempo de ejecución debe ser local primero y sin conexión de forma predeterminada.
- No agregue CDN, fuentes alojadas, descodificadores alojados, telemetría ni tiempo de ejecución en línea
dependencias.
- Las rutas de ejecución en línea intencionales se limitan al actualizador de versiones GitHub y
Envío de informes de fallos revisados/desinfectados solo para producción.
- Conserve el nombre de la aplicación: ASCII VJ Remix.
- Conserve la dirección de la aplicación nativa para macOS, Windows y Linux.
- No replantee el modo de navegador como el producto. Las rutas del navegador/Vite son útiles para
desarrollo, pruebas de humo y portabilidad del renderizador.
- Mantenga alta la calidad del renderizado. La salida WebGPU/WebGL es el objetivo de calidad visual.
- Conserve las rutas alternativas a menos que se implemente y pruebe un reemplazo.
- Trate el rendimiento y la latencia de Pop Out como un comportamiento crítico de cara al usuario.
- Mantenga locales los medios locales seleccionados por el usuario. No cargue archivos ni datos de cámara/audio.
- Mantenga la superposición de estadísticas como propiedad del usuario. Los ajustes preestablecidos aleatorios, WTF mode y los ajustes preestablecidos de audio no
No lo desactive a menos que el usuario lo haga explícitamente.
- La infraestructura de transmisión existe pero no es un modo de fuente visible normal. mantener
su interfaz de usuario oculta; La productización prospectiva pertenece a la hoja de ruta.
- Seguridad, rendimiento, accesibilidad y orientación i18n en vivo en una plataforma dedicada
practicar documentos bajo `docs/`; actualizarlos cuando los supuestos arquitectónicos
cambiar.

## Línea de base actual orientada al usuario

La versión empaquetada actual y la última versión pública son 0.9.6. El registro de cambios
es el único documento del estado actual que incluye cambios inéditos.

Fuentes:

- La imagen de demostración es la fuente de inicio predeterminada.
- El vídeo de demostración es la única fuente de vídeo integrada visible.
- Se pueden seleccionar imágenes y videos locales personalizados.
- La cámara es una fuente de primera clase.
- Se pueden combinar varias cámaras localmente cuando el sistema operativo o el tiempo de ejecución admiten la función simultánea
captura.
- Los controles de la cámara aparecen directamente debajo de Fuente mientras la cámara está activa.

Representación:

- WebGPU es el principal objetivo de calidad.
- WebGL2 es el principal respaldo integrado de GPU.
- Canvas2D y Pixel Canvas siguen siendo alternativas de compatibilidad.
- La salida nativa Pop Out utiliza `wgpu` cuando esté disponible, con Metal en macOS y
backends GPU correspondientes en Windows/Linux.
- El renderizador activo está controlado por un modelo de parámetro canónico.
- El Pop Out nativo conserva el modo de glifo y los parámetros de conjunto de caracteres para el modo tradicional.
Preajustes ASCII.
- El catálogo de conjunto de caracteres compartido incluye 23 títulos ascii.today acreditados.
rampas de luminancia y ajustes preestablecidos de solo lectura coincidentes.
- La salida de glifos nativos utiliza recursos de rampa/atlas fijos limitados;
`fontFamily` son metadatos de interfaz de usuario/vista previa, no un receptor de carga de fuentes nativo.
- Reutilice recursos estables WebGPU/WebGL, mantenga las cargas de fuentes nativas vinculadas a
versiones del marco fuente y no intercambian calidad/resolución por rendimiento.

Comportamiento en vivo:

- Los ajustes preestablecidos son de solo lectura a menos que los cree el usuario.
- Las transiciones preestablecidas son fundidos cruzados suaves, no fundidos a negro.
- Los ajustes preestablecidos conservan la fuente de medios activa a menos que se cambien explícitamente.
- WTF mode se ejecuta indefinidamente mientras está activo y pasa a modo seguro en vivo.
configuraciones aleatorias, incluidos anclajes de ajustes preestablecidos ASCII tradicionales.
- La reactividad de audio está habilitada de forma predeterminada, comienza desde el micrófono/entrada de forma predeterminada y
Modula parámetros efectivos en vivo sin reescribir los ajustes preestablecidos guardados.
- La reactividad de audio utiliza vectores de características acotados, incluidos RMS, bandas,
transitorio/flujo, presencia, brillo, densidad, pulso y fase. no
envíe buffers de audio sin procesar a través de IPC o diagnósticos.
- Las abrazaderas seguras evitan que las salidas de negro puro o blanco puro sean aleatorias o
estados controlados por audio.
- El equipo experimental MIDI es el UC-33e a través de ambas direcciones DIN de un
mioXC; No se admite UC USB directo.
- MIDI utiliza cuatro páginas con dirección de canal, toma de control suave, ranuras numéricas preestablecidas,
MIDI Aprenda anulaciones y captura/restauración SysEx de banco completo limitado.
- MIDI apunta únicamente al comportamiento visual/audio/preestablecido/WTF. No agregue fuente, cámara,
Pop Out, acciones de visualización de resultados, archivos, actualizadores o informes de fallos.
- Lea [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar las asignaciones o la política de hardware.

Interfaz de usuario:

- El tema actual es negro/blanco/gris extremo con rosa neón y azul neón.
acentos estatales.
- El diseño es intencionadamente denso.
- No reduzca la densidad de control al cambiar el estilo visual.
- Evite agregar texto de marketing explicativo dentro de la interfaz de usuario de la aplicación.

## Mapa de propiedad del repositorio

Utilice este mapa para encontrar al probable propietario de un cambio:

|Área|Archivos primarios|
| --- | --- |
|UI principal, parámetros, ajustes preestablecidos, controles de fuente, WTF, UI de audio|[app.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/app.js), [index.html](https://github.com/aindaco1/ascii-vj-remix/blob/main/index.html), [style.css](https://github.com/aindaco1/ascii-vj-remix/blob/main/style.css)|
|Abstracción de fuente de medios y renderizador GPU|[renderizadores/gpu/](https://github.com/aindaco1/ascii-vj-remix/tree/main/renderers/gpu)|
|Mapeo MIDI, adquisición suave, perfil UC-33e|[midi-mapping.js](https://github.com/aindaco1/ascii-vj-remix/blob/main/renderers/shared/midi-mapping.js), [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md)|
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
- Mantenga la selección de fuente, ajustes preestablecidos, WTF mode, modulación de audio y salida nativa
sincronización de acuerdo.
- Preservar el modelo de capacidad y permisos limitados de Tauri.
- Mantenga los activos de tiempo de ejecución agrupados localmente.
- Utilice scripts de compilación existentes en lugar de comandos de compilación ad hoc cuando sea posible.
- Actualice los documentos al cambiar el comportamiento del producto, el comportamiento de lanzamiento y el renderizador
arquitectura o requisitos de configuración.

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

- Los artefactos públicos 0.9.6 macOS están firmados con el ID del desarrollador, notariados, grapados y
Validado por Gatekeeper. Los artefactos públicos 0.9.6 Windows son vistas previas sin firmar.
Uso normal de compilaciones locales
`ASCII VJ Remix Dev` / `com.asciline.remix.dev`; el lanzador local requiere un
identidad estable antes de la prueba de permiso.
- Si `TAURI_SIGNING_PRIVATE_KEY` o `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` es
ausente mientras los artefactos del actualizador están habilitados, el paquete de versiones fallará en
firma del actualizador. Las rutas de validación locales están documentadas en el colaborador.
guía; nunca confirme ninguno de los archivos.

## Tauri y notas de embalaje

- Tauri v2 es el shell del escritorio.
- `src-tauri/tauri.conf.json` es la configuración base de producción multiplataforma; es
La identidad ad hoc macOS se utiliza únicamente en rutas de empaquetado explícitas y no certificadas por notario.
- `src-tauri/tauri.dev.conf.json` aísla los comandos locales normales del
nombre de producción, identificador de paquete y actualizador.
- `src-tauri/tauri.notarized.conf.json` es para ID de desarrollador notariado macOS
versiones de lanzamiento.
- `src-tauri/tauri.windows-signed.conf.json` y su asistente Authenticode existen
pero están inactivos. La ruta de lanzamiento actual de Windows utiliza el archivo sin firmar predeterminado.
configuración.
- macOS se integra en los espacios de trabajo de iCloud Drive y redirige la salida de destino a
`/private/tmp/ascii-vj-remix-tauri-target` a través de los scripts de ayuda para evitar
Atributos extendidos de iCloud rompiendo el código.
- Los artefactos del actualizador de versiones están firmados con una clave minisign. La clave pública es
comprometido; la clave privada pertenece a los secretos de acciones GitHub.
- Los sidecars FFmpeg deben ser revisados, locales y verificados por políticas. La aplicación empaquetada
no descarga FFmpeg, códecs, recursos de renderizado ni fuentes en tiempo de ejecución.

Consulte la [Guía del colaborador: versión y actualización Work](/es/docs/development/contributing/#trabajo-de-lanzamiento-y-actualización)
para conocer el procedimiento completo de lanzamiento/actualización.

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

- Los parámetros guardados y los parámetros efectivos son diferentes. Se modifica la reactividad del audio.
parámetros efectivos, no definiciones preestablecidas guardadas.
- La identidad de la fuente importa. Las transiciones preestablecidas no restablecen la fuente ni se reinician
reproducción multimedia.
- La salida nativa necesita nuevos parámetros y marcos. Si Pop Out parece obsoleto, inspeccione
sincronización de salida nativa antes de agregar otro renderizador.
- El trabajo de latencia de la cámara utiliza rutas nativas de captura/presentación del último fotograma donde
implementado en lugar de rutas de decodificación almacenadas en búfer.
- Las rutas alternativas son importantes para Windows/Linux y para entornos sin los mejores
Servidor GPU.

Consulte [Motor de renderizado](/es/docs/development/rendering-engine/) para obtener detalles de arquitectura más profundos.

## Reglas de actualización de documentación

Cuando el comportamiento cambie, actualice el documento duradero más cercano:

- Función de cara al usuario o comportamiento de instalación: [README](/es/docs/overview/ascii-vj-remix/).
- Comportamiento de versiones actuales e inéditas: [Changelog](/es/docs/reference/changelog/).
- Solo trabajo prospectivo: [Roadmap](/es/docs/reference/roadmap/).
- Arquitectura de renderizador, flujo de medios, salida nativa, modulación de audio, MIDI
arquitectura: [Motor de renderizado](/es/docs/development/rendering-engine/).
- Compilación, prueba, lanzamiento, FFmpeg, Podman o flujo de trabajo de colaborador:
[Guía del colaborador](/es/docs/development/contributing/).
- Modelo de seguridad, medios locales, permisos, firma del actualizador o Tauri
capacidades: [Seguridad](/es/docs/operations/security/).
- Representador sensible al rendimiento, Pop Out, cámara, audio o comportamiento de fuente:
[Rendimiento](/es/docs/operations/performance/).
- Selección de cheques y verificación manual: [Testing](/es/docs/operations/testing/).
- Comportamiento del teclado/enfoque/contraste/etiqueta de control:
[Accesibilidad](/es/docs/operations/accessibility/).
- Arquitectura de cadena, configuración regional o traducción visible para el usuario:
[Internacionalización](/es/docs/operations/internationalization/).
- Supuestos de incorporación de agentes: este archivo.

Mantenga la atención en la aplicación nativa de Documentos. Los documentos sobre el estado actual utilizan el tiempo presente y describen
comportamiento verificado. No poner propuestas, futuros candidatos, trabajos aplazados, o
planes de lanzamiento completos en esos documentos. Poner el trabajo potencial en el
[Roadmap](/es/docs/reference/roadmap/) y mantenga el historial de versiones en el
[Registro de cambios](/es/docs/reference/changelog/).


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
