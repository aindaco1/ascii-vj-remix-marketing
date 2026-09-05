---
title: Lanzamiento y actualizaciones
description: Documentación de versiones y actualizaciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Operaciones
lang: es
---

# Lanzamiento y actualizaciones

Los documentos fuente actuales describen la línea de versiones **1.0.3**. Los procedimientos de publicación y las medidas de seguridad se copian de las guías oficiales del repositorio principal.

Consulta la [versión v1.0.3](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.3) para ver los instaladores publicados, los paquetes del actualizador y las notas de validación por plataforma.

## Liberar la postura de seguridad

La línea de lanzamiento actual incluye estas reglas de refuerzo de seguridad:

- El CSP de producción solo permite el origen de la aplicación, Tauri IPC, y el protocolo de recursos Tauri necesarios para los medios locales seleccionados. Los puntos finales de Localhost HTTP/WebSocket existen solo en el CSP de desarrollo; El modo streaming no es una fuente de producción.
- El envío de informes de fallos se implementa en Rust, no en webview `fetch`, por lo que el CSP de producción no obtiene acceso remoto arbitrario a `connect-src`.
- Los secretos de firma del actualizador de acciones GitHub tienen como alcance la verificación del secreto del actualizador y los pasos de empaquetado de Tauri. No coloque `TAURI_SIGNING_PRIVATE_KEY`, `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, valores de certificados de Apple ni contraseñas de llavero en bloques de entorno de flujo de trabajo a nivel de trabajo.
- El CI de la versión pública macOS falla al cerrarse cuando la firma o certificación notarial del ID de desarrollador de Apple está incompleta. Los artefactos públicos macOS están firmados, notariados, grapados y validados por Gatekeeper; Los artefactos Windows actuales son vistas previas sin firmar.
- Los artefactos públicos macOS deben conservar el ID de equipo `PWT3Q52LZ2` y el identificador estable/requisito designado de equipo. CI valida tanto la aplicación creada como el archivo de actualización extraído y rechaza la identidad ad-hoc o de solo código hash.
- Las herramientas de lanzamiento local requieren la identidad `ASCII VJ Remix Dev` separada y un certificado de firma local estable. Nunca se sincroniza con la ruta de la aplicación de producción.
- Acciones GitHub Los trabajos macOS están anclados a `macos-26` en lugar de `macos-latest`. La pila nativa `wgpu`/`apple-metal` necesita el SDK macOS 26 ​​Metal, y el alias móvil `macos-latest` puede seleccionar un SDK más antiguo.
- El estado de la aplicación frontend conserva la URL de reproducción derivada o la identificación del medio en lugar de la ruta local seleccionada. Los diagnósticos redactan las URL de archivos y activos antes de escribir `/tmp/asciline-media-diagnostics.log`.
- Los registros de medios y las concesiones de activos de Tauri son locales de sesión. El comando `forget_media_file` revoca la concesión de una ruta después de que se elimina su registro final; Los metadatos persistentes de origen personalizado no conservan el acceso a la ruta cuando se reinicia la aplicación.
- Las importaciones preestablecidas deben estar delimitadas, verificadas en el esquema, sujetas a través de los metadatos de control compartido y eliminadas de los campos de fuente/medios antes de que puedan afectar el estado del renderizador.
- La salida nativa del modo Glifo trata `charset` y las rampas personalizadas como datos que no son de confianza. Las rampas resueltas están restringidas a la cobertura BMP admitida, desinfectadas como escalares Unicode y limitadas a 96 identificadores antes de alcanzar los buffers de renderizado. Mantenga `fontFamily` fuera de las rutas de carga de fuentes nativas o de búsqueda de recursos.
- El atlas de glifos neutrales se genera fuera de línea a partir de una fuente anclada y con suma de verificación que se conserva con sus archivos de licencia. El código de ejecución puede cargar sólo las 16 páginas del atlas incluidas; nunca resuelve las fuentes del sistema ni los recursos de fuentes remotos.
- Las auditorías de dependencia cubren npm y Rust. Las advertencias `cargo audit` de la pila transitiva GTK/WebKit actual de Tauri se rastrean como riesgo del marco de escritorio ascendente; Los avisos directos/transitivos procesables deben corregirse antes del lanzamiento cuando haya una actualización disponible.

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

Las versiones de versión local ejecutan `npm run ffmpeg:build-sidecar` antes que `npm run check:release`. El CI de lanzamiento público mantiene la misma fuente oficial fijada de FFmpeg 8.1.2, la promoción de descarga completa, la fuente SHA-256, los protocolos de red deshabilitados y las comprobaciones de recursos compatibles con LGPL, pero construye ese tiempo de ejecución en paralelo con `tauri build --no-bundle`. Requiere el flujo de trabajo `Desktop` de empuje principal exitoso de la confirmación exacta, luego entrega ambas salidas a los trabajos del paquete como artefactos de flujo de trabajo inmutables de un día. El binario de la aplicación restaurada se verifica con su confirmación, plataforma, versión, tamaño de bytes y SHA-256 antes de que `tauri bundle` lo empaquete sin volver a compilarlo. Las compilaciones en tiempo de ejecución permanecen fuera de línea; Las descargas de artefactos Unix restauran el modo ejecutable en `ffmpeg` y `ffprobe` antes de las comprobaciones de entrada de lanzamiento, porque las transferencias de artefactos comprimidos restablecen los permisos de los archivos. Los hashes en tiempo de ejecución y la disponibilidad de entrada de la cámara aún se verifican. CI puede descargar la fuente oficial durante las versiones de lanzamiento, pero la aplicación empaquetada nunca descarga FFmpeg, códecs o recursos de renderizado en tiempo de ejecución.

El flujo de trabajo de lanzamiento también ejecuta `scripts/smoke_tauri_release_install.mjs` en macOS, Windows y Linux después de la publicación. Descarga artefactos de las versiones de GitHub en lugar de reutilizar directorios de compilación locales, detecta activos faltantes, URL de `latest.json` incorrectas, problemas de diseño del instalador, un control Update oculto y descargas de actualizadores firmados rotas. macOS además extrae archivos de actualización consecutivos, requiere que el DMG contenga la aplicación real, el enlace exacto de `/Applications` y los metadatos revisados ​​del Buscador de Tauri; valida el DMG descargado y la aplicación montada; extrae archivos de actualización consecutivos; requiere el requisito designado de producción estable; realiza un verdadero auto-reemplazo del actualizador; y valida la identidad de la aplicación resultante. La carga de la versión no reemplaza los bytes de artefactos ya publicados para la misma etiqueta. Los ganchos de humo solo de CI están inactivos a menos que se establezcan estas variables de entorno:

El humo del salto del actualizador tiene por defecto `ASCILINE_UPDATER_SMOKE_MIN_VERSION=0.9.0`. Las versiones anteriores de `0.1.x` usaban una clave de firma de actualizador incompatible, por lo que pueden conservarse como versiones históricas, pero no pueden usarse como una base de actualización criptográfica para la línea de aplicación actual.

- `ASCILINE_DESKTOP_SMOKE=launch`: humo de lanzamiento acotado con informe.
- `ASCILINE_DESKTOP_SMOKE=updater-ui`: requiere que los controles de producción empaquetados Update y Reports permanezcan visibles después de la inicialización y requiere que la lectura duplicada del backend de la barra superior esté ausente.
- `ASCILINE_CRASH_REPORT_SMOKE=submit`: canario de aceptación solo de producción. Se niega a ejecutarse con un informe pendiente existente o una preferencia `off`, captura un informe desinfectado codificado, lo envía a través de la ruta de retransmisión Rust y requiere que la cola vuelva a estar vacía.
- `ASCILINE_UPDATER_SMOKE=download`: comprueba `latest.json`, descarga el paquete de actualización firmado, verifica su firma, escribe un informe y sale.
- `ASCILINE_UPDATER_SMOKE=install`: descarga y verifica el paquete de actualización, escribe un informe de preinstalación e invoca la ruta del instalador de Tauri.
- `ASCILINE_UPDATER_SMOKE_FORCE_FROM_VERSION`: registra el salto forzado de la versión anterior utilizado por CI.

El verdadero salto de actualización basado en aplicaciones necesita una versión anterior que ya contenga `ASCILINE_UPDATER_SMOKE=install`. Las versiones anteriores a v0.1.5 solo pueden participar en la instalación directa y la descarga del actualizador.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
