---
title: Cómo contribuir
description: Documentación de contribución derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Desarrollo
lang: es
---

<a id="contributing"></a>

# Cómo contribuir

Esta guía está dirigida a personas que desean crear, probar, documentar o ampliar ASCII VJ Remix.

El proyecto es un laboratorio de renderizado Tauri nativo local. Trate esto como una restricción al contribuir: evite las dependencias del tiempo de ejecución en línea, mantenga el acceso amplio al sistema de archivos fuera de la aplicación y preserve la calidad del renderizador cada vez que se agregue una función solo de escritorio.

<a id="repository-map"></a>

## Mapa del repositorio

|Camino|Objetivo|
| --- | --- |
|`index.html`, `style.css`, `app.js`|Interfaz de usuario del laboratorio de renderizado principal y lógica de control.|
|`renderers/gpu/`|Renderizador GPU, abstracción de fuente de medios, backends WebGPU/WebGL2 y activos de renderizador.|
|`renderers/desktop/`|Adaptador Tauri y ayudantes de visualización de salida.|
|`renderers/shared/midi-mapping.js`|Perfil UC-33e, validación de mapeo, escalado, soft takeover y fusión de eventos.|
|`assets/branding/`|Ilustraciones de aplicaciones canónicas utilizadas para generar íconos de plataforma.|
|`src-tauri/`|Shell de escritorio Tauri v2, ventana de salida nativa, registro de medios, proveedores de audio, motor de medios FFmpeg, capacidades, íconos generados y configuración de empaquetado.|
|`media/`|Imagen/vídeo de demostración integrados y accesorios de desarrollo ocultos.|
|`experiments/`|Experimentos de secuencias y vectores de códecs heredados/adaptativos.|
|`scripts/`|Comprobaciones de compilación, configuración de Podman, asistentes de lanzamiento, asistentes de actualización, scripts de preparación/compilación FFmpeg y pruebas de humo.|
|`docs/`|[Índice de documentación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md), guías de usuario/desarrollador, guías prácticas, registros de lanzamiento y evidencia de desempeño.|

<a id="prerequisites"></a>

## Requisitos previos

Herramientas mínimas de desarrollo:

- Node.js 24 o posterior.
- npm.
- Cadena de herramientas estable Rust con Cargo.
- Git.
- Un navegador actualizado. Se recomienda Chromium para las pruebas de WebGPU.

Requisitos previos de escritorio específicos de la plataforma:

- macOS: herramientas de línea de comandos de Xcode.
- Windows: Herramientas de compilación de Visual Studio con la carga de trabajo C++ y el tiempo de ejecución WebView2.
- Linux: paquetes de desarrollo WebKitGTK 4.1, appindicator, encabezados de desarrollo ALSA, librsvg, OpenSSL, patchelf y herramientas de compilación.

Opcional pero útil:

- Podman para el shell de desarrollo reproducible Linux y experimentos de Python/OpenCV.
- FFmpeg/ffprobe para el desarrollo de motores de medios.
- Dependencias de Playwright para las pruebas de humo en el navegador.
- GitHub CLI para la gestión de secretos de lanzamiento.

<a id="first-time-setup"></a>

## Configuración por primera vez

Instale las dependencias JavaScript:

```bash
npm ci
```

Ejecute el servidor de desarrollo del navegador:

```bash
npm run dev
```

Abierto:

```text
http://127.0.0.1:8010/
```

Ejecute la prueba de humo estático:

```bash
npm run smoke:static
```

Ejecute la aplicación de escritorio en modo de desarrollo:

```bash
npm run tauri:dev
```

Ejecute las comprobaciones principales de la aplicación de escritorio:

```bash
npm run check:desktop
```

En los espacios de trabajo macOS almacenados en iCloud Drive, el asistente de compilación Tauri redirige la salida de destino a `/private/tmp/ascii-vj-remix-tauri-target` para que los atributos extendidos de iCloud no interrumpan la firma de la aplicación. Puede anular el directorio de compilación con `ASCILINE_TAURI_TARGET_DIR` o `CARGO_TARGET_DIR`.

<a id="common-commands"></a>

## Comandos comunes

|Comando|Usar|
| --- | --- |
|`npm run dev`|Servidor de desarrollo del navegador en `127.0.0.1:8010`.|
|`npm run build`|Compilación de producción Vite más copia de activos en tiempo de ejecución.|
|`npm run preview`|Obtenga una vista previa de la compilación de producción.|
|`npm run tauri:dev`|Modo de desarrollo de escritorio Tauri.|
|`npm run tauri:build:dev -- --bundles app`|Aplicación de desarrollo macOS optimizada.|
|`npm run bundle:debug`|Cree y valide un paquete de escritorio de depuración local.|
|`npm run bundle:test`|Windows desarrollo de perfil de lanzamiento EXE/MSI con FFmpeg preparado.|
|`npm run bundle:test:linux`|Desarrollo de Linux AppImage, deb y rpm con FFmpeg por etapas.|
|`npm run icons:generate`|Regenerar íconos de plataforma desde la fuente canónica.|
|`npm run midi:probe`|Listar los puertos MIDI; agregue `-- --connect` para abrir ambas direcciones mioXC.|

La [Referencia rápida de pruebas](/es/docs/operations/testing/#quick-reference) posee comandos de validación; sus [conjuntos de verificación recomendados](/es/docs/operations/testing/#recommended-check-sets) explican cuál ejecutar para variar.

Las solicitudes de extracción del mismo repositorio también empaquetan artefactos de desarrollo deshabilitados por el actualizador después de que pasa la puerta de escritorio de la plataforma. El instalador sin firmar `ASCII VJ Remix Dev` Windows se construye en modo de lanzamiento, verifica el subsistema gráfico PE y se instala junto con la identidad de producción. Linux produce paquetes AppImage, deb y rpm a partir de la misma identidad de desarrollo. CI crea y verifica los recursos FFmpeg/ffprobe anclados para cada conjunto de paquetes antes de agruparlos. Los artefactos `ascii-vj-remix-windows-test-<commit>` y `ascii-vj-remix-linux-test-<commit>` se conservan durante 14 días. Consulte [Linux VM QA](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/LINUX_VM_QA.md) para conocer la matriz de VM mantenida.

<a id="podman-development-shell"></a>

## Shell de desarrollo de Podman

El repositorio incluye una configuración de Podman para un entorno Linux reproducible en macOS y Linux. Es especialmente útil para experimentos con códecs Python/OpenCV y para evitar diferencias entre hosts Python/OpenSSL.

```bash
scripts/podman-doctor.sh
scripts/podman_build.sh
scripts/podman_venv.sh
scripts/podman_run.sh bash
```

La imagen de Podman tiene como valor predeterminado el Nodo 24. Para probar una versión más reciente del Nodo par:

```bash
NODE_MAJOR=26 scripts/podman_build.sh
```

Ejecute el conjunto de códecs/vectores heredado a través de Podman:

```bash
scripts/podman_codec_tests.sh
```

Para comandos de ejecución prolongada, el contenedor Podman puede reiniciar salidas inesperadas:

```bash
PORT=8010 ASCILINE_RESTART=1 scripts/podman_run.sh python -m http.server 8010 --bind 0.0.0.0
```

Si un puerto ya está en uso, elija otro puerto de host:

```bash
HOST_PORT=8011 CONTAINER_PORT=8010 ASCILINE_RESTART=1 scripts/podman_run.sh python -m http.server 8010 --bind 0.0.0.0
```

<a id="development-rules"></a>

## Reglas de desarrollo

- Mantenga el comportamiento del tiempo de ejecución local primero. No agregue CDN, decodificadores en línea, fuentes alojadas, análisis, SDK de proveedores remotos ni descargas de códecs en tiempo de ejecución.
- Mantenga los archivos seleccionados por el usuario detrás de la selección explícita del usuario.
- No agregue concesiones amplias de directorio principal o sistema de archivos.
- Mantenga la interfaz de usuario de origen normal centrada en fuentes locales estáticas. El modo Stream sigue siendo solo de desarrollo.
- Conserve el arnés de humo estático/Vite y la portabilidad del renderizador al agregar funciones Tauri solo de escritorio.
- Mantenga la superposición de estadísticas controlada por el usuario. La aleatorización, los ajustes preestablecidos y la reactividad del audio no deben apagarlo silenciosamente.
- Evite reinicios del renderizador al cambiar ajustes preestablecidos, configuraciones de audio o controles seguros en vivo.
- Realice las comprobaciones adecuadas antes de abrir un PR.

Utilice los documentos de práctica del proyecto cuando cambie el comportamiento compartido:

- [Seguridad](/es/docs/operations/security/): capacidades de Tauri, medios locales, permisos, firma de actualizador, sidecars de FFmpeg y manejo de secretos.
- [Rendimiento](/es/docs/operations/performance/): renderizador FPS, Pop Out nativo, conmutación de fuente, latencia de cámara, respuesta de audio y validación de compilación optimizada.
- [Pruebas](/es/docs/operations/testing/): selección de verificación, cobertura de humo, verificaciones de liberación y validación manual de hardware.
- [Accesibilidad](/es/docs/operations/accessibility/): mejores prácticas de teclado, enfoque, etiquetas, contraste y control denso.
- [Internacionalización](/es/docs/operations/internationalization/): límite de idioma actual, propiedad de cadenas y reglas de interfaz de usuario seguras para la localización.

<a id="frontend-and-renderer-work"></a>

## Trabajo de frontend y renderizador

La aplicación utiliza módulos HTML/CSS/ES básicos con Vite. No existe una capa de aplicación React/Svelte.

Conceptos estatales importantes:

- `params`: estado de renderizado persistente canónico.
- `effectiveParams`: estado de renderizado en vivo después de la reactividad del audio u otra modulación no persistente.
- `SOURCE_PRESETS`: fuentes integradas visibles.
- `BUILTIN_PRESETS`: biblioteca preestablecida de solo lectura.
- `StaticRuntime`: fuente de medios del navegador más renderizador WebGPU/WebGL2/Canvas.
- `StreamRuntime`: ruta de transmisión heredada/de desarrollo.
- `AudioReactiveRuntime`: análisis de audio local y modulación de parámetros efectivos.

Al agregar un control visible:

1. Agréguelo al modelo de parámetros canónicos.
2. Agregue metadatos de control.
3. Agregue reglas de visibilidad condicional si no son válidas para todas las fuentes/backend.
4. Enrute los cambios a través de la misma ruta de configuración que los controles deslizantes, ajustes preestablecidos, WTF mode y MIDI.
5. Verifique que funcione en vivo sin reiniciar los medios a menos que sea explícitamente un cambio estructural de renderizador/fuente.

<a id="desktop-and-tauri-work"></a>

## Escritorio y Tauri Trabajo

Los comandos Tauri se declaran en `src-tauri/src/lib.rs` y se controlan mediante capacidades en `src-tauri/capabilities/`.

Mantenga las capacidades limitadas:

- Ventana principal: selección de medios, gestión de salida, proveedores de audio, actualizador.
- Ventana de salida: permisos mínimos de escucha/cierre/pantalla completa únicamente.

La superficie de comando MIDI es únicamente la ventana principal. El código nativo MIDI se encuentra en `src-tauri/src/midi.rs`; El primer puerto admitido es el mioXC con conexión DIN. No otorgue comandos MIDI o SysEx a la ventana de salida. Consulte [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar el perfil de hardware.

Seleccione [MIDI comprueba](/es/docs/operations/testing/#midi-uc-33e-or-sysex-changes) para cambios de mapeo, transporte o SysEx.

El CSP de producción en `src-tauri/tauri.conf.json` bloquea intencionalmente conexiones HTTP(S) remotas arbitrarias. Si necesita un nuevo protocolo o ruta de recursos, actualice la política deliberadamente y ejecute:

```bash
npm run check:tauri-policy
```

El ícono de la aplicación tiene una fuente de verdad: `assets/branding/ascii-vj-remix-app-icon-1024.png`. No edite manualmente los archivos de la plataforma en `src-tauri/icons/`. Regenerarlos y verificarlos con:

```bash
npm run icons:generate
npm run check:icons
```

<a id="macos-permissions-during-development"></a>

## Permisos macOS durante el desarrollo

La producción y el desarrollo utilizan identidades de aplicaciones independientes:

```text
ASCII VJ Remix      com.asciline.remix
ASCII VJ Remix Dev  com.asciline.remix.dev
```

`npm run tauri:dev`, `npm run bundle:debug` y `npm run tauri:build:dev` aplican automáticamente `src-tauri/tauri.dev.conf.json`. No utilice un paquete con nombre de producción para pruebas locales de cámara, micrófono o audio del sistema.

Cree la identidad de firma de código local estable una vez:

```bash
npm run desktop:codesign:local
```

Luego cree, instale e inicie la aplicación de desarrollo:

```bash
npm run desktop:run-local -- --build
```

El ejecutor local instala `~/Applications/ASCII VJ Remix Dev.app`, verifica `com.asciline.remix.dev` y rechaza la firma ad hoc de forma predeterminada. Para una compilación desechable que no recibirá concesiones de privacidad persistentes, regístrese explícitamente con `ASCILINE_ALLOW_ADHOC_LOCAL=1`.

Anule `ASCILINE_CODESIGN_IDENTITY` solo cuando pruebe deliberadamente una identidad de firma estable diferente.

Restablecer las concesiones de privacidad de desarrollo cuando sea necesario:

```bash
tccutil reset Camera com.asciline.remix.dev
tccutil reset Microphone com.asciline.remix.dev
tccutil reset ScreenCapture com.asciline.remix.dev
tccutil reset AudioCapture com.asciline.remix.dev
```

<a id="ffmpeg-and-media-engine-work"></a>

## Trabajo de FFmpeg y Media Engine

La canalización Rust/FFmpeg proporciona preparación de medios/transmisiones locales sin agrupar Python en producción. Python/OpenCV sigue siendo una infraestructura de desarrollo y referencia.

Los comandos de desarrollo utilizan estas variables de entorno cuando se configuran:

```bash
ASCILINE_FFMPEG=/path/to/ffmpeg
ASCILINE_FFPROBE=/path/to/ffprobe
```

En macOS y Windows, los contenedores Podman reutilizan una conexión Podman predeterminada en buen estado antes de iniciar `podman-machine-default`. Esto evita colisionar con la máquina virtual que ya se está ejecutando en otro proceso de pago. Configure `ASCILINE_PODMAN_MACHINE` solo cuando la máquina alternativa tenga un nombre diferente.

Vista previa del canal de medios:

```bash
npm run media:decode-preview -- media/demo-video-2.mp4 96 54 2
npm run media:pipeline-preview -- media/demo-video-2.mp4 96 54 12 5 false
npm run media:native-session-preview -- media/demo-video-2.mp4 96 54 12 5 true 4
```

Ejecute [FFmpeg y comprobaciones de medios](/es/docs/operations/testing/#ffmpeg-and-media-engine) al cambiar la preparación del marco, la decodificación o las sesiones de medios nativos.

El flujo de trabajo de lanzamiento utiliza sidecars FFmpeg/ffprobe revisados. Organiza binarios locales con procedencia explícita:

```bash
npm run ffmpeg:stage -- --ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe --license LGPL-2.1-or-later --source "reviewed reproducible build notes"
npm run check:ffmpeg-resources
```

El flujo de trabajo de lanzamiento crea FFmpeg a partir del tarball fuente oficial 8.1.2 fijado con protocolos de red deshabilitados y presenta sidecars compatibles con LGPL. No confirme los binarios secundarios generados ni las claves de liberación privadas.

<a id="release-and-updater-work"></a>

## Trabajo de lanzamiento y actualización

Siga la [Guía de lanzamiento y actualización](/es/docs/operations/release/) para empaquetar, firmar, publicar, artefactos inmutables y aceptación posterior a la publicación. Utilice [Prueba: Lanzamiento y Actualizador](/es/docs/operations/testing/#release-and-updater) para seleccionar la verificación. La evidencia específica de la versión se encuentra en [registros de publicación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md).

<a id="pull-request-checklist"></a>

## Lista de verificación de solicitud de extracción

Elija el [conjunto de comprobaciones recomendado](/es/docs/operations/testing/#recommended-check-sets) más acotado que cubra el cambio y complete las [pruebas de humo manuales](/es/docs/operations/testing/#manual-smoke-checklist) correspondientes. Si mueve documentación, verifique también los enlaces relativos, las anclas de los encabezados y las referencias a rutas; `git diff --check` por sí solo no comprueba enlaces.

<a id="contribution-flow"></a>

## Flujo de contribución

1. Crea una rama enfocada.
2. Mantenga los cambios enfocados a la característica o error.
3. Agregue o actualice pruebas cuando cambie el comportamiento.
4. Update documenta cuando el comportamiento del usuario, el proceso de lanzamiento o la arquitectura cambian.
5. Ejecute las comprobaciones pertinentes.
6. Abra un PR con:
   - lo que cambió.
   - por qué cambió.
   - cómo fue probado.
   - cualquier limitación conocida.

<a id="license"></a>

## Licencia

El repositorio utiliza el texto de licencia ascendente ASCILINE: Licencia MIT con restricción antipublicidad. Consulte [LICENSE](https://github.com/aindaco1/ascii-vj-remix/blob/main/LICENSE).

Las contribuciones deben ser compatibles con esa licencia y con la política de tiempo de ejecución local primero del proyecto.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
