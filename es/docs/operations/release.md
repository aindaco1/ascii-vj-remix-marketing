---
title: Lanzamiento y actualizaciones
description: Documentación de versiones y actualizaciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Operaciones
lang: es
---

<a id="release-and-updates"></a>

# Lanzamiento y actualizaciones

Esta guía define el procedimiento mantenido de empaquetado, firma, publicación y actualización. Ejecute los comandos desde la raíz del repositorio. Consulte [Pruebas](/es/docs/operations/testing/#release-and-updater) para seleccionar las comprobaciones y [Seguridad](/es/docs/operations/security/#release-security-posture) para el modelo de seguridad de las publicaciones.

Las decisiones y pruebas específicas de la versión se guardan en [registros de publicación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md). Son instantáneas históricas, no el procedimiento de publicación actual.

<a id="evidence-and-release-records"></a>

## Evidencia y registros de versiones

Al recopilar evidencia de una versión, registre la versión exacta, el commit o la etiqueta, el nombre y hash del artefacto y la plataforma probada. Distinga estas etapas:

1. Metadatos de origen y comprobaciones locales.
2. Trabajos de CI para el commit exacto del candidato o de la etiqueta.
3. Artefactos empaquetados, firmas y bytes publicados.
4. Aceptación de aplicaciones instaladas y actualizadores frente a esos artefactos.
5. Resultados de interacción manual y hardware físico.

Una compilación o publicación correcta no demuestra aceptación en hardware físico. Registre el alcance de cualquier aplazamiento aprobado por el responsable y enlace la comprobación pendiente desde [Pruebas](/es/docs/operations/testing/#hardware-and-platform-checks) y la [Hoja de ruta](/es/docs/reference/roadmap/#distribution-and-platform-validation).

Cree los registros de cada versión en `docs/releases/`, indique la fecha y la etapa de evidencia y añádalos al [índice de versiones](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md). Conserve las filas pendientes como evidencia histórica; no las marque como aprobadas solo porque después se publicó una versión. Las guías de usuario y arquitectura describen el comportamiento mantenido, y el [Registro de cambios](/es/docs/reference/changelog/) conserva el historial de versiones.

<a id="release-workflow"></a>

## Flujo de trabajo de lanzamiento

Las compilaciones de escritorio ASCII VJ Remix deben permanecer independientes en tiempo de ejecución. El actualizador Tauri es una ruta en línea intencional: la aplicación de producción lo invoca una vez en segundo plano durante el inicio y cuando el usuario solicita una nueva verificación manual. Una verificación de inicio actual o fallida permanece en silencio. La descarga, la instalación y el reinicio siguen siendo acciones explícitas del usuario a través del control Update existente.

Las publicaciones se realizan mediante `.github/workflows/release-desktop.yml`. La matriz compila y verifica los artefactos de macOS, Windows y Linux, genera fragmentos del manifiesto del actualizador, los combina en `latest.json` y sube los instaladores, paquetes de actualización, firmas y `latest.json` a GitHub Releases. La compilación usa la etiqueta `v*` solicitada, de modo que los artefactos corresponden al código etiquetado y no a cambios posteriores de `main`.

`.github/workflows/auto-version-release.yml` automatiza la ruta de lanzamiento común. Cuando `package.json`, `package-lock.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json` o `CHANGELOG.md` cambian en `main`, valida que las versiones de la aplicación coincidan con `npm run release:version:check`, crea `vX.Y.Z` cuando esa etiqueta aún no existe y envía el flujo de trabajo de la versión de escritorio con esa etiqueta. Si la etiqueta ya existe, omite el envío de la versión para que las inserciones repetidas no sobrescriban accidentalmente una versión publicada.

<a id="updater-signing"></a>

## Firma del actualizador

El actualizador consulta este manifiesto en GitHub Releases:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

Los paquetes de actualización se firman con un par de claves minisign. La clave pública está versionada en `src-tauri/tauri.conf.json`. La clave privada debe almacenarse como secreto de GitHub Actions con el nombre `TAURI_SIGNING_PRIVATE_KEY`; nunca debe incluirse en el repositorio. La clave cifrada actual también requiere `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`.

La clave pública actual se generó con una clave protegida por contraseña:

```bash
npm run tauri -- signer generate --ci -w /private/tmp/ascii-vj-remix-updater.key -p "$(cat /private/tmp/ascii-vj-remix-updater.password)"
```

En este entorno local, se espera la clave privada generada en `/private/tmp/ascii-vj-remix-updater.key` y su contraseña en `/private/tmp/ascii-vj-remix-updater.password`. Nunca incluya ninguno de estos archivos en el repositorio.

Configure/verifique la clave del actualizador con GitHub CLI:

```bash
npm run updater:secret:check
npm run updater:secret:set
npm run release:secrets:check
npm run release:secrets:check:public
```

El script secreto del actualizador pasa valores a `gh secret set` a través de la entrada estándar, no como argumentos de línea de comandos. Utilice `-- --repo owner/repo` o `-- --key /path/to/key` después del script npm si los valores predeterminados son incorrectos.

`release:secrets:check:public` requiere la firma del actualizador y la preparación para la certificación notarial del ID del desarrollador macOS. La ruta de lanzamiento actual de Windows publica artefactos de vista previa sin firmar y no requiere secretos de firma de Windows.

<a id="local-packaging-and-app-identity"></a>

## Empaquetado local e identidad de la aplicación

Para paquetes locales con actualizador deshabilitado, use los [comandos del colaborador](/es/docs/development/contributing/#common-commands). En macOS, siga [Permisos durante el desarrollo](/es/docs/development/contributing/#macos-permissions-during-development) para una firma de desarrollo estable.

El empaquetado con la configuración de producción también requiere la clave del actualizador. No instale ese paquete para pruebas locales de permisos.

La configuración base conserva `bundle.macOS.signingIdentity = "-"` para los valores predeterminados de empaquetado portátil, pero los comandos locales normales colocan la capa `src-tauri/tauri.dev.conf.json` para cambiar el nombre y el identificador de la aplicación y deshabilitar las actualizaciones de producción. Las versiones públicas de macOS utilizan `src-tauri/tauri.notarized.conf.json` y fallan si faltan las credenciales de firma y certificación de ID del desarrollador.

<a id="macos-release-signing"></a>

## macOS Firma de lanzamiento

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

<a id="windows-signing-tooling"></a>

## Windows Herramientas de firma

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

<a id="build-and-package"></a>

## Construir y empaquetar

Elija las comprobaciones en [Pruebas: Lanzamiento y Actualización](/es/docs/operations/testing/#release-and-updater). Las anulaciones de directorios de compilación locales están documentadas en [Guía del colaborador: configuración inicial](/es/docs/development/contributing/#first-time-setup).

Las compilaciones locales de publicación ejecutan `npm run ffmpeg:build-sidecar` antes de `npm run check:release`. El CI de publicación usa el mismo código oficial fijado de FFmpeg 8.1.2, promueve únicamente las descargas completas, verifica el SHA-256 del código fuente, deshabilita los protocolos de red y comprueba los recursos compatibles con LGPL. Compila ese runtime en paralelo con `tauri build --no-bundle`. Exige que el flujo `Desktop` haya pasado para el commit exacto enviado a `main` y entrega ambas salidas a los trabajos de empaquetado como artefactos inmutables con un día de retención. Antes de que `tauri bundle` empaquete sin recompilar, verifica el commit, la plataforma, la versión, el tamaño y el SHA-256 del binario recuperado. El runtime permanece sin acceso a la red; tras descargar artefactos en Unix se restablece el permiso de ejecución de `ffmpeg` y `ffprobe` antes de comprobar los recursos de publicación, ya que la transferencia en ZIP restablece los permisos. También se verifican los hashes y las entradas de cámara disponibles. CI puede descargar código oficial durante la compilación, pero la aplicación empaquetada nunca descarga FFmpeg, códecs ni recursos de renderizado al ejecutarse.

<a id="published-artifact-acceptance"></a>

## Aceptación de artefactos publicados

Después de publicar, el flujo ejecuta `scripts/smoke_tauri_release_install.mjs` en macOS, Windows y Linux. Descarga los artefactos de GitHub Releases para detectar archivos faltantes, URL incorrectas en `latest.json`, errores de estructura del instalador, un control Update oculto o descargas firmadas defectuosas. En macOS también extrae paquetes de actualización consecutivos; exige que el DMG contenga la aplicación real, el enlace exacto a `/Applications` y los metadatos de Finder revisados de Tauri; valida el DMG descargado y la aplicación montada; exige el requisito designado estable de producción; realiza una sustitución real mediante el actualizador; y valida la identidad resultante. La subida de una publicación no reemplaza los bytes de artefactos ya publicados para la misma etiqueta.

Si un ejecutor posterior a la publicación expone un defecto en las herramientas de aceptación, corrija las herramientas y ejecute el flujo de trabajo `Release Acceptance` con la etiqueta inmutable existente. Reutiliza los bytes publicados sin reconstruir ni reemplazar activos.

La prueba de actualización entre versiones usa por defecto `ASCILINE_UPDATER_SMOKE_MIN_VERSION=0.9.0`. Las versiones antiguas `0.1.x` usaban una clave de firma incompatible: pueden conservarse como historial, pero no sirven como punto de partida criptográfico para actualizar a la línea actual.

<a id="ci-smoke-hooks"></a>

### Puntos de entrada para pruebas de humo en CI

Estos puntos de entrada permanecen inactivos salvo que se habiliten explícitamente mediante variables de entorno.

- `ASCILINE_DESKTOP_SMOKE=launch`: prueba de inicio acotada que genera un informe.
- `ASCILINE_DESKTOP_SMOKE=updater-ui`: requiere que los controles de producción empaquetados Update y Reports permanezcan visibles después de la inicialización y requiere que la lectura duplicada del backend de la barra superior esté ausente.
- `ASCILINE_CRASH_REPORT_SMOKE=submit`: prueba de aceptación exclusiva de producción. Rechaza la ejecución si ya hay un informe pendiente o la preferencia está en `off`, captura un único informe predefinido y saneado, lo envía mediante el relay de Rust y exige que la cola vuelva a quedar vacía.
- `ASCILINE_UPDATER_SMOKE=download`: comprueba `latest.json`, descarga el paquete de actualización firmado, verifica su firma, escribe un informe y sale.
- `ASCILINE_UPDATER_SMOKE=install`: descarga y verifica el paquete de actualización, escribe un informe de preinstalación e invoca la ruta del instalador de Tauri.
- `ASCILINE_UPDATER_SMOKE_FORCE_FROM_VERSION`: registra el salto forzado de la versión anterior utilizado por CI.

El verdadero salto de actualización basado en aplicaciones necesita una versión anterior que ya contenga `ASCILINE_UPDATER_SMOKE=install`. Las versiones anteriores a v0.1.5 solo pueden participar en la instalación directa y la descarga del actualizador.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/RELEASING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RELEASING.md)
