---
title: Cómo contribuir
description: Documentación de contribución derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Desarrollo
lang: es
---

# Cómo contribuir

Esta guía está dirigida a personas que desean crear, probar, documentar o ampliar ASCII VJ Remix.

El proyecto es un laboratorio de renderizado Tauri nativo local. Trate esto como una restricción al contribuir: evite las dependencias del tiempo de ejecución en línea, mantenga el acceso amplio al sistema de archivos fuera de la aplicación y preserve la calidad del renderizador cada vez que se agregue una función solo de escritorio.

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
|`docs/`|Hoja de ruta, guía del motor de renderizado, seguridad, rendimiento, pruebas, accesibilidad, i18n, guía del agente LLM y documentación para contribuyentes.|

## Requisitos previos

Herramientas mínimas de desarrollo:

- Node.js 24 o posterior.
- npm.
- Cadena de herramientas estable Rust con Cargo.
- Vaya.
- Un navegador actual. Se prefiere el cromo para las pruebas WebGPU.

Requisitos previos de escritorio específicos de la plataforma:

- macOS: herramientas de línea de comandos de Xcode.
- Windows: Herramientas de compilación de Visual Studio con la carga de trabajo C++ y el tiempo de ejecución WebView2.
- Linux: paquetes de desarrollo WebKitGTK 4.1, appindicator, encabezados de desarrollo ALSA, librsvg, OpenSSL, patchelf y herramientas de compilación.

Opcional pero útil:

- Podman para el shell de desarrollo reproducible Linux y experimentos de Python/OpenCV.
- FFmpeg/ffprobe para el desarrollo de motores de medios.
- Dependencias de dramaturgos para pruebas de humo del navegador.
- GitHub CLI para la gestión de secretos de lanzamiento.

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

Ejecute la puerta de validación del escritorio principal:

```bash
npm run check:desktop
```

En los espacios de trabajo macOS almacenados en iCloud Drive, el asistente de compilación Tauri redirige la salida de destino a `/private/tmp/ascii-vj-remix-tauri-target` para que los atributos extendidos de iCloud no interrumpan la firma de la aplicación. Puede anular el directorio de compilación con `ASCILINE_TAURI_TARGET_DIR` o `CARGO_TARGET_DIR`.

## Comandos comunes

|Comando|Usar|
| --- | --- |
|`npm run dev`|Servidor de desarrollo del navegador en `127.0.0.1:8010`.|
|`npm run build`|Compilación de producción Vite más copia de activos en tiempo de ejecución.|
|`npm run preview`|Obtenga una vista previa de la compilación de producción.|
|`npm run check:offline`|Compile y verifique que no se requieran activos de tiempo de ejecución remotos.|
|`npm run smoke:static`|Prueba de humo del navegador para la interfaz de usuario de origen, el inicio del renderizador, el respaldo de salida y los dispositivos de audio falsos.|
|`npm run test:renderer-fallback`|Pruebas deterministas de respaldo de GPU a Canvas y de contrato de informe de renderizado limitado.|
|`npm run tauri:dev`|Modo de desarrollo de escritorio Tauri.|
|`npm run check:desktop`|Compilación sin conexión, política Tauri, simulación de visualización de salida, manifiesto de actualización, política de recursos FFmpeg, pruebas Rust y compilación sin paquete de depuración.|
|`npm run icons:generate`|Regenere todos los íconos de la plataforma Tauri desde la fuente canónica de 1024px.|
|`npm run check:icons`|Regenere íconos de forma aislada y verifique las coincidencias del conjunto confirmado.|
|`npm run bundle:debug`|Cree un paquete de escritorio de depuración local y valídelo.|
|`npm run bundle:test`|En Windows con los recursos FFmpeg verificados actuales preparados, cree un instalador de desarrollo de perfil de versión sin firmar y verifique su subsistema GUI.|
|`npm run bundle:test:linux`|En Linux con los recursos FFmpeg verificados actualmente en preparación, cree paquetes de desarrollo AppImage, deb y rpm deshabilitados para el actualizador.|
|`npm run bundle:release`|Ejecute puertas de lanzamiento, cree un paquete de lanzamiento y valídelo.|
|`npm run test:rust`|Ejecute pruebas Rust.|
|`npm run check:media`|Ejecute la preparación de fotogramas, la decodificación/cambio de tamaño y las comprobaciones de medios de sesión nativas.|
|`npm run test:output-display`|Simulación determinista de ubicación de pantalla secundaria.|
|`npm run test:desktop-updater`|Lanzamiento/organización del actualizador manual, verificación silenciosa, instalación y pruebas de progreso.|
|`npm run smoke:native-output`|Ayudante de humo con rendimiento de salida nativa.|
|`npm run smoke:ui-perf`|Ayudante de humo para el rendimiento de la interfaz de usuario.|
|`npm run test:midi`|MIDI pruebas de mapa, escalado, soft takeover, acción y alcance.|
|`npm run midi:probe`|Enumere las entradas/salidas físicas de MIDI; agregue `-- --connect` para abrir ambas direcciones mioXC.|

Las solicitudes de extracción del mismo repositorio también empaquetan artefactos de desarrollo deshabilitados por el actualizador después de que pasa la puerta de escritorio de la plataforma. El instalador sin firmar `ASCII VJ Remix Dev` Windows se construye en modo de lanzamiento, verifica el subsistema gráfico PE y se instala junto con la identidad de producción. Linux produce paquetes AppImage, deb y rpm a partir de la misma identidad de desarrollo. CI crea y verifica los recursos FFmpeg/ffprobe anclados para cada conjunto de paquetes antes de agruparlos. Los artefactos `ascii-vj-remix-windows-test-<commit>` y `ascii-vj-remix-linux-test-<commit>` se conservan durante 14 días. Consulte [Linux VM QA](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/LINUX_VM_QA.md) para conocer la matriz de VM mantenida.

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

## Escritorio y Tauri Trabajo

Los comandos Tauri se declaran en `src-tauri/src/lib.rs` y se controlan mediante capacidades en `src-tauri/capabilities/`.

Mantenga las capacidades limitadas:

- Ventana principal: selección de medios, gestión de salida, proveedores de audio, actualizador.
- Ventana de salida: permisos mínimos de escucha/cierre/pantalla completa únicamente.

La superficie de comando MIDI es únicamente la ventana principal. El código nativo MIDI se encuentra en `src-tauri/src/midi.rs`; El primer puerto admitido es el mioXC con conexión DIN. No otorgue comandos MIDI o SysEx a la ventana de salida. Consulte [MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md) antes de cambiar el perfil de hardware.

MIDI comprueba:

```bash
npm run test:midi
npm run midi:probe
npm run midi:probe -- --connect
npm run test:rust
```

El CSP de producción en `src-tauri/tauri.conf.json` bloquea intencionalmente conexiones HTTP(S) remotas arbitrarias. Si necesita un nuevo protocolo o ruta de recursos, actualice la política deliberadamente y ejecute:

```bash
npm run check:tauri-policy
```

El ícono de la aplicación tiene una fuente de verdad: `assets/branding/ascii-vj-remix-app-icon-1024.png`. No edite manualmente los archivos de la plataforma en `src-tauri/icons/`. Regenerarlos y verificarlos con:

```bash
npm run icons:generate
npm run check:icons
```

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

Restablecer las concesiones de privacidad de desarrollo cuando sea necesario:

```bash
tccutil reset Camera com.asciline.remix.dev
tccutil reset Microphone com.asciline.remix.dev
tccutil reset ScreenCapture com.asciline.remix.dev
tccutil reset AudioCapture com.asciline.remix.dev
```

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

Ejecute comprobaciones de paridad:

```bash
npm run test:frame-prep
npm run test:decode-resize
npm run check:media
```

El flujo de trabajo de lanzamiento utiliza sidecars FFmpeg/ffprobe revisados. Organiza binarios locales con procedencia explícita:

```bash
npm run ffmpeg:stage -- --ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe --license LGPL-2.1-or-later --source "reviewed reproducible build notes"
npm run check:ffmpeg-resources
```

El flujo de trabajo de lanzamiento crea FFmpeg a partir del tarball fuente oficial 8.1.2 fijado con protocolos de red deshabilitados y presenta sidecars compatibles con LGPL. No confirme los binarios secundarios generados ni las claves de liberación privadas.

## Trabajo de lanzamiento y actualización

Las compilaciones de escritorio ASCII VJ Remix deben permanecer independientes en tiempo de ejecución. El actualizador Tauri es una ruta en línea intencional: la aplicación de producción lo invoca una vez en segundo plano durante el inicio y cuando el usuario solicita una nueva verificación manual. Una verificación de inicio actual o fallida permanece en silencio. La descarga, la instalación y el reinicio siguen siendo acciones explícitas del usuario a través del control Update existente.

Los lanzamientos son publicados por `.github/workflows/release-desktop.yml`. La matriz de versiones crea artefactos macOS, Windows y Linux, los verifica, escribe fragmentos del manifiesto del actualizador, fusiona esos fragmentos en `latest.json` y carga instaladores, paquetes de actualización, firmas y `latest.json` en las versiones GitHub. El flujo de trabajo se construye a partir de la etiqueta `v*` solicitada, de modo que los artefactos de lanzamiento coincidan con la fuente etiquetada, no con lo que suceda más adelante en `main`.

`.github/workflows/auto-version-release.yml` automatiza la ruta de lanzamiento común. Cuando `package.json`, `package-lock.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json` o `CHANGELOG.md` cambian en `main`, valida que las versiones de la aplicación coincidan con `npm run release:version:check`, crea `vX.Y.Z` cuando esa etiqueta aún no existe y envía el flujo de trabajo de la versión de escritorio con esa etiqueta. Si la etiqueta ya existe, omite el envío de la versión para que las inserciones repetidas no sobrescriban accidentalmente una versión publicada.

El actualizador de versiones GitHub dice:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

Los paquetes de actualización están firmados con un par de claves minisign. La clave pública se confirma en `src-tauri/tauri.conf.json`. La clave privada debe almacenarse como el secreto de acciones GitHub `TAURI_SIGNING_PRIVATE_KEY`; nunca lo cometas. Se requiere `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` para la clave de liberación cifrada actual.

La clave pública actual se generó con una clave protegida por contraseña:

```bash
npm run tauri -- signer generate --ci -w /private/tmp/ascii-vj-remix-updater.key -p "$(cat /private/tmp/ascii-vj-remix-updater.password)"
```

Para este espacio de trabajo local, la clave privada generada se espera en `/private/tmp/ascii-vj-remix-updater.key` y la contraseña en `/private/tmp/ascii-vj-remix-updater.password`. Nunca confirme ninguno de los archivos.

Configure/verifique la clave del actualizador con GitHub CLI:

```bash
npm run updater:secret:check
npm run updater:secret:set
npm run release:secrets:check
npm run release:secrets:check:public
```

El script secreto del actualizador pasa valores a `gh secret set` a través de la entrada estándar, no como argumentos de línea de comandos. Utilice `-- --repo owner/repo` o `-- --key /path/to/key` después del script npm si los valores predeterminados son incorrectos.

`release:secrets:check:public` requiere la firma del actualizador y la preparación para la certificación notarial del ID del desarrollador macOS. La ruta de lanzamiento actual de Windows publica artefactos de vista previa sin firmar y no requiere secretos de firma de Windows.

Para un paquete de desarrollo local con actualizador deshabilitado:

```bash
npm run bundle:debug
```

El paquete de lanzamiento en forma de producción aún requiere la clave de actualización y no debe instalarse como una compilación de prueba de permisos local.

La configuración base conserva `bundle.macOS.signingIdentity = "-"` para los valores predeterminados de empaquetado portátil, pero los comandos locales normales colocan la capa `src-tauri/tauri.dev.conf.json` para cambiar el nombre y el identificador de la aplicación y deshabilitar las actualizaciones de producción. Las versiones públicas de macOS utilizan `src-tauri/tauri.notarized.conf.json` y fallan si faltan las credenciales de firma y certificación de ID del desarrollador.

`scripts/run_local_desktop_app.sh` requiere la identidad local estable de forma predeterminada. Anule `ASCILINE_CODESIGN_IDENTITY` solo cuando pruebe deliberadamente una identidad de firma estable diferente:

```bash
npm run desktop:codesign:local
npm run desktop:run-local -- --build
```

La firma y certificación de ID de desarrollador requieren membresía del Programa de Desarrolladores de Apple, una aplicación de ID de desarrollador base64 `.p12`, su contraseña, una contraseña de llavero CI y credenciales API de App Store Connect o credenciales de notarización de ID de Apple. Verifique la preparación o cargue las credenciales de la API de App Store Connect con:

```bash
npm run release:secrets:check:notarized
npm run release:secrets:set:macos -- \
  --certificate /path/to/developer-id-application.p12 \
  --certificate-password-file /path/to/p12-password.txt \
  --api-key ABCDE12345 \
  --api-issuer 00000000-0000-0000-0000-000000000000 \
  --api-key-file /path/to/AuthKey_ABCDE12345.p8
```

También se admiten credenciales de ID de Apple:

```bash
npm run release:secrets:set:macos -- \
  --certificate /path/to/developer-id-application.p12 \
  --certificate-password-file /path/to/p12-password.txt \
  --apple-id-file /path/to/apple-id-email.txt \
  --apple-password-file /path/to/app-specific-password.txt \
  --apple-team-id TEAMID12345
```

Cuando se omite `--keychain-password-file`, el script genera una contraseña de llavero temporal aleatoria y la almacena en `KEYCHAIN_PASSWORD`.

El repositorio contiene una ruta de Azure Artifact Signing inactiva en `src-tauri/tauri.windows-signed.conf.json`, que invoca `src-tauri/windows-artifact-sign.cmd`; ese contenedor llama `scripts/windows_artifact_sign.ps1`. Esto firma los artefactos Windows antes de que Tauri cree firmas de actualización. La ruta de lanzamiento actual de Windows no utiliza esta configuración y publica artefactos de vista previa de Windows sin firmar. Configure los valores de Azure solo después de que la firma Windows esté habilitada como política de lanzamiento:

```bash
npm run release:secrets:set:windows -- \
  --client-id "<app-client-id>" \
  --tenant-id "<tenant-id>" \
  --client-secret-file /path/to/azure-client-secret.txt \
  --endpoint "https://<region>.codesigning.azure.net/" \
  --account "<signing-account-name>" \
  --certificate-profile "<certificate-profile-name>"
node scripts/check_github_release_secrets.mjs --require-windows-signing
```

El asistente almacena `AZURE_CLIENT_SECRET` como un secreto de acciones GitHub y los demás ID de Azure como variables del repositorio GitHub. El secreto del cliente de Azure es el único secreto de firma Windows requerido; manténgalo fuera del historial de shell y de los registros de chat. La selección de proveedores y la implementación de la firma Windows siguen siendo decisiones de la hoja de ruta; las herramientas inactivas no describen la postura de distribución actual.

Utilice estas comprobaciones antes de publicar cambios en la versión:

```bash
npm run check:desktop
npm run test:desktop-updater
npm run test:updater-manifest
npm run check:bundle:debug
```

En este espacio de trabajo de iCloud Drive macOS, la salida de la compilación Tauri se redirige a `/private/tmp/ascii-vj-remix-tauri-target` para evitar que los atributos extendidos de iCloud rompan `codesign`. Los espacios de trabajo normales de CI y fuera de iCloud continúan usando `src-tauri/target`. Anule con `ASCILINE_TAURI_TARGET_DIR` o `CARGO_TARGET_DIR` cuando sea necesario.

Las versiones de versión local ejecutan `npm run ffmpeg:build-sidecar` antes que `npm run check:release`. El CI de lanzamiento público mantiene la misma fuente oficial fijada de FFmpeg 8.1.2, la promoción de descarga completa, la fuente SHA-256, los protocolos de red deshabilitados y las comprobaciones de recursos compatibles con LGPL, pero construye ese tiempo de ejecución en paralelo con `tauri build --no-bundle`. Requiere el flujo de trabajo `Desktop` de empuje principal exacto de la confirmación exacta y luego entrega ambas salidas a los trabajos del paquete como artefactos inmutables del flujo de trabajo de un día. El binario de la aplicación restaurada se verifica con su confirmación, plataforma, versión, tamaño de bytes y SHA-256 antes de que `tauri bundle` lo empaquete sin volver a compilarlo. Las compilaciones en tiempo de ejecución permanecen fuera de línea; CI puede descargar la fuente oficial durante las versiones de lanzamiento, pero la aplicación empaquetada nunca descarga FFmpeg, códecs o recursos de renderizado en tiempo de ejecución.

El flujo de trabajo de lanzamiento también ejecuta `scripts/smoke_tauri_release_install.mjs` en macOS, Windows y Linux después de la publicación. Descarga artefactos de las versiones de GitHub en lugar de reutilizar directorios de compilación locales, detecta activos faltantes, URL de `latest.json` incorrectas, problemas de diseño del instalador, un control Update oculto y descargas de actualizadores firmados rotas. macOS además extrae archivos de actualización consecutivos, requiere que el DMG contenga la aplicación real, el enlace exacto de `/Applications` y los metadatos revisados ​​del Buscador de Tauri; valida el DMG descargado y la aplicación montada; extrae archivos de actualización consecutivos; requiere el requisito designado de producción estable; realiza un verdadero auto-reemplazo del actualizador; y valida la identidad de la aplicación resultante. La carga de la versión no reemplaza los bytes de artefactos ya publicados para la misma etiqueta. Los ganchos de humo solo de CI están inactivos a menos que se establezcan estas variables de entorno:

El humo del salto del actualizador tiene por defecto `ASCILINE_UPDATER_SMOKE_MIN_VERSION=0.9.0`. Las versiones anteriores de `0.1.x` usaban una clave de firma de actualizador incompatible, por lo que pueden conservarse como versiones históricas, pero no pueden usarse como una base de actualización criptográfica para la línea de aplicación actual.

- `ASCILINE_DESKTOP_SMOKE=launch`: humo de lanzamiento acotado con informe.
- `ASCILINE_DESKTOP_SMOKE=updater-ui`: requiere que los controles de producción empaquetados Update y Reports permanezcan visibles después de la inicialización y requiere que la lectura duplicada del backend de la barra superior esté ausente.
- `ASCILINE_CRASH_REPORT_SMOKE=submit`: canario de aceptación solo de producción. Se niega a ejecutarse con un informe pendiente existente o una preferencia `off`, captura un informe desinfectado codificado, lo envía a través de la ruta de retransmisión Rust y requiere que la cola vuelva a estar vacía.
- `ASCILINE_UPDATER_SMOKE=download`: comprueba `latest.json`, descarga el paquete de actualización firmado, verifica su firma, escribe un informe y sale.
- `ASCILINE_UPDATER_SMOKE=install`: descarga y verifica el paquete de actualización, escribe un informe de preinstalación e invoca la ruta del instalador de Tauri.
- `ASCILINE_UPDATER_SMOKE_FORCE_FROM_VERSION`: registra el salto forzado de la versión anterior utilizado por CI.

El verdadero salto de actualización basado en aplicaciones necesita una versión anterior que ya contenga `ASCILINE_UPDATER_SMOKE=install`. Las versiones anteriores a v0.1.5 solo pueden participar en la instalación directa y la descarga del actualizador.

## Lista de verificación de solicitud de extracción

Antes de abrir un PR, ejecute el conjunto de comprobaciones más pequeño y útil para su cambio.

Consulte [Testing](/es/docs/operations/testing/) para obtener la matriz de verificación completa y la lista de verificación manual de humo.

Sólo documentación:

```bash
git diff --check
```

Interfaz de usuario/interfaz de origen:

```bash
node --check app.js
npm run smoke:static
```

Escritorio/Tauri:

```bash
npm run check:desktop
```

Motor de medios:

```bash
npm run check:media
npm run test:rust
```

Embalaje de lanzamiento:

```bash
npm run check:release
npm run bundle:release
npm run test:macos-dmg-layout
```

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

## Licencia

El repositorio utiliza el texto de licencia ASCILINE ascendente: Licencia MIT con restricción antipublicidad. Ver `LICENSE`.

Las contribuciones deben ser compatibles con esa licencia y con la política de tiempo de ejecución local primero del proyecto.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
