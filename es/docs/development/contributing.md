---
title: Cómo contribuir
description: Documentación de contribución derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Desarrollo
lang: es
---

# Cómo contribuir

Esta guía es para personas que desean construir, probar, documentar o ampliar ASCII VJ.
Remezclar.

El proyecto es un laboratorio de renderizado Tauri nativo local. Trata eso como un
restricción al contribuir: evitar dependencias de tiempo de ejecución en línea, mantener amplio
acceso al sistema de archivos desde la aplicación y preserva la calidad del renderizador cada vez que se
Se agrega la función solo de escritorio.

## Mapa del repositorio

|Camino|Propósito|
| --- | --- |
|`index.html`, `style.css`, `app.js`|Interfaz de usuario del laboratorio de renderizado principal y lógica de control.|
|`renderers/gpu/`|Renderizador GPU proporcionado/adaptado, abstracción de fuente de medios, backends WebGPU/WebGL2 y recursos de renderizado.|
|`renderers/desktop/`|Adaptador Tauri y ayudantes de visualización de salida.|
|`src-tauri/`|Shell de escritorio Tauri v2, ventana de salida nativa, registro de medios, proveedores de audio, motor de medios FFmpeg, capacidades, íconos y configuración de empaquetado.|
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
- Windows: Herramientas de compilación de Visual Studio con la carga de trabajo C++ y WebView2
tiempo de ejecución.
- Linux: WebKitGTK 4.1 paquetes de desarrollo, appindicator, desarrollo ALSA
encabezados, librsvg, OpenSSL, patchelf y herramientas de compilación.

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

En los espacios de trabajo macOS almacenados en iCloud Drive, el asistente de compilación Tauri redirige
salida de destino a `/private/tmp/ascii-vj-remix-tauri-target` para que iCloud se extienda
Los atributos no interrumpen la firma de la aplicación. Puede anular el directorio de compilación con
`ASCILINE_TAURI_TARGET_DIR` o `CARGO_TARGET_DIR`.

## Comandos comunes

|Comando|uso|
| --- | --- |
|`npm run dev`|Servidor de desarrollo del navegador en `127.0.0.1:8010`.|
|`npm run build`|Compilación de producción Vite más copia de activos en tiempo de ejecución.|
|`npm run preview`|Obtenga una vista previa de la compilación de producción.|
|`npm run check:offline`|Compile y verifique que no se requieran activos de tiempo de ejecución remotos.|
|`npm run smoke:static`|Prueba de humo del navegador para la interfaz de usuario de origen, el inicio del renderizador, el respaldo de salida y los dispositivos de audio falsos.|
|`npm run tauri:dev`|Modo de desarrollo de escritorio Tauri.|
|`npm run check:desktop`|Compilación sin conexión, política Tauri, simulación de visualización de salida, manifiesto de actualización, política de recursos FFmpeg, pruebas Rust y compilación sin paquete de depuración.|
|`npm run bundle:debug`|Cree un paquete de escritorio de depuración local y valídelo.|
|`npm run bundle:release`|Ejecute puertas de lanzamiento, cree un paquete de lanzamiento y valídelo.|
|`npm run test:rust`|Ejecute pruebas Rust.|
|`npm run check:media`|Ejecute la preparación de fotogramas, la decodificación/cambio de tamaño y las comprobaciones de medios de sesión nativas.|
|`npm run test:output-display`|Simulación determinista de ubicación de pantalla secundaria.|
|`npm run smoke:native-output`|Ayudante de humo con rendimiento de salida nativa.|
|`npm run smoke:ui-perf`|Ayudante de humo para el rendimiento de la interfaz de usuario.|

## Shell de desarrollo de Podman

El repositorio incluye una configuración de Podman para un entorno Linux reproducible en macOS.
y Linux. Es especialmente útil para experimentos con códecs Python/OpenCV y para
evitando las diferencias entre el host Python y OpenSSL.

```bash
scripts/podman-doctor.sh
scripts/podman_build.sh
scripts/podman_venv.sh
scripts/podman_run.sh bash
```

La imagen de Podman tiene como valor predeterminado el Nodo 24. Para probar un Nodo par más nuevo
lanzamiento:

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

- Mantenga el comportamiento del tiempo de ejecución local primero. No agregue CDN, decodificadores en línea, alojados
fuentes, análisis, SDK de proveedores remotos o descargas de códecs en tiempo de ejecución.
- Mantenga los archivos seleccionados por el usuario detrás de la selección explícita del usuario.
- No agregue concesiones amplias de directorio principal o sistema de archivos.
- Mantenga la interfaz de usuario de origen normal centrada en fuentes locales estáticas hasta que se active el modo de transmisión.
completamente producido.
- Preservar el arnés de humo estático/Vite y la portabilidad del renderizador al agregar
Funciones Tauri solo de escritorio.
- Mantenga la superposición de estadísticas controlada por el usuario. Aleatorización, ajustes preestablecidos y audio.
La reactividad no debe apagarlo silenciosamente.
- Evite reinicios del renderizador al cambiar ajustes preestablecidos, configuraciones de audio o seguridad en vivo
controles.
- Realice las comprobaciones adecuadas antes de abrir un PR.

Utilice los documentos de práctica del proyecto cuando cambie el comportamiento compartido:

- [Seguridad](/es/docs/operations/security/): capacidades de Tauri, medios locales, permisos,
firma de actualizador, sidecars FFmpeg y manejo de secretos.
- [Rendimiento](/es/docs/operations/performance/): renderizador FPS, Pop Out nativo, cambio de fuente,
latencia de la cámara, respuesta de audio y validación de compilación optimizada.
- [Pruebas](/es/docs/operations/testing/): selección de verificación, cobertura de humo, verificaciones de liberación y
Validación manual del hardware.
- [Accesibilidad](/es/docs/operations/accessibility/): teclado, enfoque, etiquetas, contraste y
mejores prácticas de control denso.
- [Internacionalización](/es/docs/operations/internationalization/): futura cadena y catálogo de traducción incluido
reglas de propiedad.

## Trabajo de frontend y renderizador

La aplicación utiliza módulos HTML/CSS/ES básicos con Vite. No hay React/Svelte
capa de aplicación.

Conceptos estatales importantes:

- `params`: estado de renderizado persistente canónico.
- `effectiveParams`: estado de renderizado en vivo después de reactividad de audio u otro
Modulación no persistente.
- `SOURCE_PRESETS`: fuentes integradas visibles.
- `BUILTIN_PRESETS`: biblioteca preestablecida de solo lectura.
- `StaticRuntime`: fuente de medios del navegador más renderizador WebGPU/WebGL2/Canvas.
- `StreamRuntime`: ruta de transmisión heredada/de desarrollo.
- `AudioReactiveRuntime`: análisis de audio local y modulación de parámetros efectivos.

Al agregar un control visible:

1. Agréguelo al modelo de parámetros canónicos.
2. Agregue metadatos de control.
3. Agregue reglas de visibilidad condicional si no son válidas para todas las fuentes/backend.
4. Enrute los cambios a través de la misma ruta de configuración que los controles deslizantes, ajustes preestablecidos, WTF mode y
futuro MIDI.
5. Verifique que funcione en vivo sin reiniciar los medios a menos que sea explícitamente un
renderizador estructural/cambio de fuente.

## Escritorio y Tauri Trabajo

Los comandos Tauri se declaran en `src-tauri/src/lib.rs` y se controlan a través de
capacidades en `src-tauri/capabilities/`.

Mantenga las capacidades limitadas:

- Ventana principal: selección de medios, gestión de salida, proveedores de audio, actualizador.
- Ventana de salida: permisos mínimos de escucha/cierre/pantalla completa únicamente.

El CSP de producción en `src-tauri/tauri.conf.json` bloquea intencionalmente
conexiones HTTP(S) remotas arbitrarias. Si necesita un nuevo protocolo o recurso
ruta, actualice la política deliberadamente y ejecute:

```bash
npm run check:tauri-policy
```

## Permisos macOS durante el desarrollo

La aplicación utiliza un identificador de paquete:

```text
com.asciline.remix
```

Restablezca las concesiones de privacidad locales cuando sea necesario:

```bash
tccutil reset Camera com.asciline.remix
tccutil reset Microphone com.asciline.remix
tccutil reset ScreenCapture com.asciline.remix
tccutil reset AudioCapture com.asciline.remix
```

Para obtener permisos de medios locales estables en las reconstrucciones, cree una firma de código local
identidad una vez:

```bash
npm run desktop:codesign:local
```

Luego ejecuta:

```bash
ASCILINE_CODESIGN_IDENTITY="ASCII VJ Remix Local Code Signing" npm run desktop:run-local
```

Sin una identidad estable, macOS puede tratar las reconstrucciones como una aplicación diferente para
fines de privacidad.

## Trabajo de FFmpeg y Media Engine

El proyecto está avanzando en la preparación de transmisiones/medios a largo plazo hacia un Rust/FFmpeg.
pipeline en lugar de agrupar Python en producción.

Los comandos de desarrollo utilizan estas variables de entorno cuando se configuran:

```bash
ASCILINE_FFMPEG=/path/to/ffmpeg
ASCILINE_FFPROBE=/path/to/ffprobe
```

Vista previa del canal de medios:

```bash
npm run media:decode-preview -- media/point-click-test.mp4 96 54 2
npm run media:pipeline-preview -- media/point-click-test.mp4 96 54 12 5 false
npm run media:native-session-preview -- media/point-click-test.mp4 96 54 12 5 true 4
```

Ejecute comprobaciones de paridad:

```bash
npm run test:frame-prep
npm run test:decode-resize
npm run check:media
```

Las versiones de lanzamiento deben utilizar sidecars FFmpeg/ffprobe revisados. Escenario binarios con
procedencia explícita:

```bash
npm run ffmpeg:stage -- --ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe --license LGPL-2.1-or-later --source "reviewed reproducible build notes"
npm run check:ffmpeg-resources
```

El flujo de trabajo de lanzamiento crea FFmpeg a partir de la fuente oficial 8.1.2 fijada.
tarball con protocolos de red deshabilitados y presenta sidecars compatibles con LGPL.
No confirme los binarios secundarios generados ni las claves de liberación privadas.

## Trabajo de lanzamiento y actualización

Las compilaciones de escritorio ASCII VJ Remix deben permanecer independientes en tiempo de ejecución. el unico
La ruta en línea intencional es el actualizador Tauri, que verifica la versión GitHub.
metadatos cuando la aplicación invoca el complemento de actualización.

Los lanzamientos son publicados por `.github/workflows/release-desktop.yml`. la liberación
Matrix construye artefactos macOS, Windows y Linux, los verifica y escribe el actualizador.
manifiesta fragmentos, fusiona esos fragmentos en `latest.json` y los carga
instaladores, paquetes de actualización, firmas y versiones de `latest.json` a GitHub.
El flujo de trabajo se construye a partir de la etiqueta `v*` solicitada para que los artefactos de lanzamiento coincidan con la etiqueta `v*` solicitada.
fuente etiquetada, no lo que sea que esté en `main` más tarde.

`.github/workflows/auto-version-release.yml` automatiza la ruta de lanzamiento común.
Cuando `package.json`, `package-lock.json`, `src-tauri/Cargo.toml`,
`src-tauri/tauri.conf.json`, o `CHANGELOG.md` cambia en `main`, valida
que las versiones de la aplicación coincidan con `npm run release:version:check`, crea
`vX.Y.Z` cuando esa etiqueta aún no existe y envía el escritorio
liberar el flujo de trabajo con esa etiqueta. Si la etiqueta ya existe, omite el lanzamiento.
despachar para que las pulsaciones repetidas no sobrescriban accidentalmente una versión publicada.

El actualizador de versiones GitHub dice:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

Los paquetes de actualización están firmados con un par de claves minisign. La clave pública es
cometido en `src-tauri/tauri.conf.json`. La clave privada debe almacenarse como
GitHub Acciones secretas `TAURI_SIGNING_PRIVATE_KEY`; nunca lo cometas.
Se requiere `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` para el cifrado actual
tecla de liberación.

La clave pública actual se generó con una clave protegida por contraseña:

```bash
npm run tauri -- signer generate --ci -w /private/tmp/ascii-vj-remix-updater.key -p "$(cat /private/tmp/ascii-vj-remix-updater.password)"
```

Para este espacio de trabajo local, se espera que la clave privada generada esté en
`/private/tmp/ascii-vj-remix-updater.key` y se espera la contraseña en
`/private/tmp/ascii-vj-remix-updater.password`. Nunca confirme ninguno de los archivos.

Configure/verifique la clave del actualizador con GitHub CLI:

```bash
npm run updater:secret:check
npm run updater:secret:set
npm run release:secrets:check
npm run release:secrets:check:public
```

El script secreto del actualizador pasa valores a `gh secret set` a través de la entrada estándar, no como
Argumentos de línea de comando. Utilice `-- --repo owner/repo` o `-- --key /path/to/key`
después del script npm si los valores predeterminados son incorrectos.

Para 0.9.3, `release:secrets:check:public` requiere la firma del actualizador y macOS
Preparación para la certificación notarial de identificación del desarrollador. Los artefactos Windows se publican como sin firmar.
vistas previas y no requieren secretos de firma Windows.

Para un paquete de depuración local con la clave de actualización generada:

```bash
TAURI_SIGNING_PRIVATE_KEY="$(cat /private/tmp/ascii-vj-remix-updater.key)" TAURI_SIGNING_PRIVATE_KEY_PASSWORD="$(cat /private/tmp/ascii-vj-remix-updater.password)" npm run bundle:debug
```

Las compilaciones locales/predeterminadas actuales de macOS están firmadas ad hoc por
`bundle.macOS.signingIdentity = "-"` en `src-tauri/tauri.conf.json`. eso mantiene
firma de código de paquetes locales válida pero no es certificación notarial de Apple. Público macOS
las compilaciones de lanzamiento usan `src-tauri/tauri.notarized.conf.json` y fallan si el desarrollador
Faltan las credenciales de firma de identificación y notarización.

Las concesiones de privacidad de medios locales macOS pueden ser sensibles a la firma final de la aplicación.
`scripts/run_local_desktop_app.sh` acepta
`ASCILINE_CODESIGN_IDENTITY="<identity>"` para que las compilaciones de prueba locales se puedan volver a firmar
con una identidad local estable/autofirmada en lugar de una firma ad hoc cambiante:

```bash
npm run desktop:codesign:local
ASCILINE_CODESIGN_IDENTITY="ASCII VJ Remix Local Code Signing" npm run desktop:run-local
```

La firma de identificación de desarrollador y la certificación notarial requieren el Programa de Desarrolladores de Apple
membresía, una aplicación de ID de desarrollador base64 `.p12`, su contraseña, un CI
contraseña del llavero y credenciales de la API de App Store Connect o ID de Apple
credenciales de notario. Verifique la preparación o cargue la API de App Store Connect
credenciales con:

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

Cuando se omite `--keychain-password-file`, el script genera un código aleatorio
contraseña temporal del llavero y la almacena en `KEYCHAIN_PASSWORD`.

Las futuras versiones firmadas de Windows pueden usar Azure Artifact Signing a través de
`src-tauri/tauri.windows-signed.conf.json`, que invoca
`src-tauri/windows-artifact-sign.cmd`; ese envoltorio llama
`scripts/windows_artifact_sign.ps1`. Esto firma artefactos Windows antes de Tauri
crea firmas de actualización. La ruta de versión activa 0.9.3 Windows no utiliza
esta configuración y publica artefactos de vista previa sin firmar. Configurar los valores de Azure
solo si Azure se convierte en el backend de firma Windows elegido:

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

El asistente almacena `AZURE_CLIENT_SECRET` como un secreto de acciones GitHub y el otro
ID de Azure como variables del repositorio GitHub. El secreto del cliente de Azure es el único
se requiere el secreto de firma Windows; manténgalo fuera del historial de shell y de los registros de chat.
Prefiera la futura vía de limpieza de licencia/Fundación SignPath antes de habilitar el pago
Firma de Azure para lanzamientos públicos de rutina.

Utilice estas comprobaciones antes de publicar cambios en la versión:

```bash
npm run check:desktop
npm run test:updater-manifest
npm run check:bundle:debug
```

En este espacio de trabajo de iCloud Drive macOS, la salida de la compilación Tauri se redirige a
`/private/tmp/ascii-vj-remix-tauri-target` para evitar los atributos extendidos de iCloud
rompiendo `codesign`. Se siguen utilizando espacios de trabajo normales de CI y que no son de iCloud
`src-tauri/target`. Anular con `ASCILINE_TAURI_TARGET_DIR` o
`CARGO_TARGET_DIR` cuando sea necesario.

Las versiones de lanzamiento ejecutan `npm run ffmpeg:build-sidecar` antes
`npm run check:release`. Eso se basa en el FFmpeg 8.1.2 oficial fijado
tarball de origen, verifica el SHA-256 de origen, deshabilita los protocolos de red FFmpeg,
y organiza binarios FFmpeg/ffprobe compatibles con LGPL como recursos locales Tauri.
Las compilaciones en tiempo de ejecución permanecen fuera de línea; CI puede descargar la fuente oficial durante el lanzamiento
compila, pero la aplicación empaquetada nunca descarga FFmpeg, códecs o recursos de renderizado
en tiempo de ejecución.

El flujo de trabajo de lanzamiento también ejecuta `scripts/smoke_tauri_release_install.mjs` después
publicación. Descarga artefactos de versiones GitHub en lugar de reutilizar locales
crear directorios, detectar activos faltantes, URL `latest.json` incorrectas, instalador
problemas de diseño y descargas rotas de actualizadores firmados. Los ganchos para humo exclusivos de CI están
inactivo a menos que se establezcan estas variables de entorno:

El humo del salto del actualizador tiene por defecto `ASCILINE_UPDATER_SMOKE_MIN_VERSION=0.9.0`.
Las versiones anteriores de `0.1.x` utilizaban una clave de firma de actualizador incompatible, por lo que pueden
Se mantienen como publicaciones históricas, pero no se pueden utilizar como un salto de actualización criptográfico.
línea de base para la línea de aplicación actual.

- `ASCILINE_DESKTOP_SMOKE=launch`: humo de lanzamiento acotado con informe.
- `ASCILINE_UPDATER_SMOKE=download`: comprueba `latest.json`, descarga el firmado
paquete de actualización, verifica su firma, escribe un informe y sale.
- `ASCILINE_UPDATER_SMOKE=install`: descarga y verifica el paquete de actualización,
escribe un informe previo a la instalación e invoca la ruta del instalador de Tauri.
- `ASCILINE_UPDATER_SMOKE_FORCE_FROM_VERSION`: registra la versión anterior forzada
lúpulo utilizado por CI.

El verdadero salto de actualización basado en aplicaciones necesita una versión anterior que ya contenga
`ASCILINE_UPDATER_SMOKE=install`. Las versiones anteriores a v0.1.5 solo pueden participar en
Instalación directa y descarga del actualizador Smoke.

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
```

## Flujo de contribución

1. Crea una rama enfocada.
2. Mantenga los cambios enfocados a la característica o error.
3. Agregue o actualice pruebas cuando cambie el comportamiento.
4. Actualizar documentos cuando se trate de comportamiento, proceso de lanzamiento o arquitectura de cara al usuario
cambios.
5. Ejecute las comprobaciones pertinentes.
6. Abra un PR con:
   - lo que cambió.
   - por qué cambió.
   - cómo fue probado.
   - cualquier limitación conocida.

## Licencia

El repositorio utiliza el texto de licencia ASCILINE ascendente: Licencia MIT con una
Restricción antipublicidad. Ver `LICENSE`.

Las contribuciones deben ser compatibles con esa licencia y con los objetivos del proyecto.
Política de tiempo de ejecución local primero.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
