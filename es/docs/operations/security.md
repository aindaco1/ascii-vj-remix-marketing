---
title: Seguridad
description: Documentación de seguridad derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Operaciones
lang: es
---

# Seguridad

Esta guía documenta el modelo de seguridad actual, las compensaciones aceptadas y
prácticas de validación para ASCII VJ Remix.

El perfil de riesgo de ASCII VJ Remix es una aplicación de escritorio Tauri local que maneja
medios locales, cámaras, micrófonos, audio del sistema, ventanas de salida nativas, incluidos
Sidecars FFmpeg, artefactos de actualización firmados e informes de fallos revisados/desinfectados.

## Principios de seguridad

- Mantenga la aplicación empaquetada localmente primero y fuera de línea de forma predeterminada.
- No agregue CDN, fuentes alojadas, códecs alojados, telemetría, renderizadores alojados ni
Descargas de dependencias en tiempo de ejecución.
- Trate el actualizador de versiones GitHub y el informe de fallas solo de producción como el
sólo rutas de ejecución en línea intencionales.
- Mantenga local los medios seleccionados por el usuario, los fotogramas de la cámara y el análisis de audio.
- Requerir una selección explícita del usuario antes de leer un archivo local.
- Mantenga las capacidades de Tauri limitadas y específicas de ventana.
- Mantenga la ventana de salida como una superficie de presentación, no como una segunda aplicación privilegiada
controlador.
- Mantenga los secretos de firma de lanzamiento, firma de actualizador y certificación notarial fuera del alcance de
repositorio.
- El identificador del paquete de producción es `com.asciline.remix`; cambiarlo crea
una migración de concesión de privacidad macOS.
- Mantener el desarrollo local en `com.asciline.remix.dev`; nunca firme ni instale un
compilación de desarrollo ad-hoc bajo el identificador de producción.

## Arquitectura de seguridad

|Superficie|Límite actual|Nivel de riesgo|Notas|
| --- | --- | --- | --- |
|Archivos de imagen/vídeo locales|API de archivos del navegador o cuadro de diálogo Tauri más registro de medios local de sesión|Medio|Los archivos se seleccionan explícitamente sin acceso amplio al sistema de archivos.|
|Medios de demostración incorporados|Incluido en `media/` y copiado en los recursos de la aplicación|Bajo|Los medios de demostración son locales y versionados.|
|Entrada de cámara|Navegador `getUserMedia`; macOS ruta nativa AVFoundation para Pop Out|Medio|Requiere permiso de privacidad del sistema operativo. Los marcos permanecen locales.|
|Audio de micrófono/entrada|Proveedores de audio web y Tauri nativos|Medio|Requiere permiso de privacidad del sistema operativo. Las funciones de análisis están limitadas.|
|Audio del sistema/pantalla|El navegador muestra audio cuando está presente; proveedores de escritorio nativos donde estén disponibles|Medio|Los permisos de la plataforma varían. No amplíe la captura más allá de las necesidades de funciones.|
|Preajustes/configuraciones|Almacenamiento del navegador local, IndexedDB, JSON importado/exportado|Bajo a Medio|Datos escritos por el usuario. Validar las importaciones antes de aplicar.|
|Ventana de salida|Ventana de salida Tauri con permisos mínimos|Medio|No debe exponer la selección de medios, el sistema de archivos, el actualizador ni las API de comandos amplios.|
|Comandos Tauri|`src-tauri/src/lib.rs` más archivos de capacidad|Alto|Trate cada comando como un límite de seguridad. Validar entradas en Rust.|
|Protocolo de activos|Vacío de forma predeterminada, expandido solo para necesidades de sesión/medios seleccionados|Alto|Evite caminos amplios y persistentes.|
|sidecares FFmpeg|Recursos agrupados con comprobaciones de políticas y metadatos de fuente/procedencia|Medio|Sin descargas de tiempo de ejecución. Los sidecars de liberación desactivan los protocolos de red.|
|Actualizador|GitHub lanza punto final con paquetes de actualización firmados|Alto|La clave de firma privada es externa. La clave pública está comprometida.|
|reportero de accidentes|POST solo de Rust a `https://crash.dustwave.xyz/v1/reports` en compilaciones de producción|Alto|Los informes están delimitados, desinfectados, configurables por el usuario y retransmitidos a los problemas de GitHub mediante un Cloudflare Worker.|
|Experimental MIDI y UC-33e SysEx|Comandos Rust solo de la ventana principal, lista de puertos permitidos mioXC, colas acotadas y límites de paquetes|Medio|Los perfiles permanecen locales y no pueden apuntar a fuentes, cámaras, Pop Out ni pantallas de salida. La verificación de restauración física del banco completo sigue incompleta.|
|Registros e informes de humo.|Artefactos de prueba/desarrollador local|Bajo a Medio|No registre rutas de archivos privados, audio sin formato ni valores ambientales confidenciales a menos que sea necesario para una depuración explícita.|

## Liberar la postura de seguridad

La línea de lanzamiento actual incluye estas reglas de refuerzo de seguridad:

- El CSP de producción solo permite el origen de la aplicación, Tauri IPC y el activo Tauri.
protocolo necesario para los medios locales seleccionados. Puntos finales de localhost HTTP/WebSocket
existir sólo en el CSP de desarrollo; El modo streaming no es una fuente de producción.
- El envío de informes de fallos se implementa en Rust, no en webview `fetch`, por lo que el
El CSP de producción no obtiene acceso remoto arbitrario a `connect-src`.
- GitHub Los secretos de firma del actualizador de acciones tienen como ámbito la verificación del secreto del actualizador.
y pasos de empaquetado Tauri. No coloque `TAURI_SIGNING_PRIVATE_KEY`,
`TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, valores de certificado de Apple o llavero
contraseñas en bloques de entorno de flujo de trabajo a nivel de trabajo.
- El CI de la versión pública macOS falla al cerrarse cuando se firma el ID de desarrollador de Apple o
la notarización está incompleta. Los artefactos públicos 0.9.6 macOS están firmados,
notariado, engrapado y validado por Gatekeeper; Los artefactos Windows 0.9.6 son
vistas previas sin firmar.
- Los artefactos públicos macOS deben conservar el ID del equipo `PWT3Q52LZ2` y el establo.
Requisito de identificador/equipo designado. CI valida tanto la aplicación creada como
el archivo de actualización extraído y rechaza la identidad ad-hoc o de solo código hash.
- Las herramientas de lanzamiento local requieren la identidad `ASCII VJ Remix Dev` separada y
un certificado de firma local estable. Nunca se sincroniza con la producción.
ruta de la aplicación.
- Acciones GitHub Los trabajos macOS están anclados a `macos-26` en lugar de
`macos-latest`. La pila nativa `wgpu`/`apple-metal` necesita el macOS 26
Metal SDK y el alias móvil `macos-latest` pueden seleccionar un SDK más antiguo.
- El estado de la aplicación frontend conserva la URL de reproducción derivada o la identificación del medio en lugar de la
ruta local seleccionada. Los diagnósticos redactan las URL de archivos y activos antes de escribir
`/tmp/asciline-media-diagnostics.log`.
- Los registros de medios y las concesiones de activos de Tauri son locales de sesión. El
El comando `forget_media_file` revoca la concesión de una ruta después de su registro final
se elimina; Los metadatos persistentes de origen personalizado no conservan el acceso a la ruta.
en todos los reinicios de la aplicación.
- Las importaciones preestablecidas deben estar limitadas, verificadas en el esquema y sujetas a través del espacio compartido.
controlar los metadatos y eliminar los campos de fuente/medios antes de que puedan afectar
estado del renderizador.
- La salida nativa en modo glifo trata a `charset` como datos incluidos en la lista de permitidos. Resuelto
Las rampas de catálogo personalizadas deben estar delimitadas, estar orientadas al espacio, ser únicas y restringidas.
al atlas de glifos fijos. Mantenga `fontFamily` fuera de la carga de fuentes nativas o
rutas de búsqueda de recursos.
- Las auditorías de dependencia cubren npm y Rust. `cargo audit` advertencias de
La pila transitiva GTK/WebKit actual de Tauri se rastrea como escritorio ascendente
riesgo marco; Los avisos directos/transitivos procesables deben solucionarse antes de
lanzar cuando haya una actualización disponible.

## Política de tiempo de ejecución Tauri

El tiempo de ejecución de producción es intencionalmente limitado:

- `src-tauri/tauri.conf.json` mantiene una producción restrictiva Seguridad de Contenidos
Política.
- El CSP de producción no permite puntos finales HTTP/WebSocket de host local arbitrarios;
Los puntos finales de desarrollo/transmisión de localhost solo existen en `devCsp`.
- `npm run check:tauri-policy` verifica la política de tiempo de ejecución solo local, la
Excepción del punto final del actualizador GitHub y el comando de informe de fallos exclusivo de Rust
límite.
- Las capacidades en `src-tauri/capabilities/` dividen los privilegios de la ventana principal de
privilegios de ventana de salida.
- La ventana principal posee selección de medios, administración de salida, proveedores de audio y
trabajo de actualización/informe de fallos.
- La ventana de salida solo escucha mensajes de renderizado/salida y expone
el comportamiento mínimo de cierre/pantalla completa que necesita.

Al agregar un comando Tauri:

1. Prefiera un comando limitado con entradas escritas a un comando genérico.
2. Valide rutas, identificadores, dimensiones, valores de enumeración y límites numéricos en Rust.
3. Otorgue el comando solo a la ventana que lo necesita.
4. Evite devolver rutas sin formato del sistema de archivos a la vista web a menos que la interfaz de usuario lo necesite
mostrar un nombre de archivo seleccionado por el usuario.
5. Agregue o actualice una prueba/verificación cuando el comando cambie la seguridad de la aplicación
postura.

## Informe de fallos

Los informes de fallas se activan por preferencia y son solo de producción para la red.
sumisión. Las compilaciones de depuración/desarrollo pueden capturar informes locales para realizar pruebas, pero Rust
se niega a presentarlos.

El reportero de accidentes puede capturar:

- eventos front-end `error`.
- eventos front-end `unhandledrejection`.
- Fallos del comando Tauri.
- Rust informes de gancho de pánico importados en el próximo lanzamiento.

Requisitos de seguridad:

- Los informes deben estar delimitados antes del almacenamiento local y antes de su envío.
- Los informes deben redactar rutas locales, URL de activos/archivos, correos electrónicos, tokens, cookies,
contraseñas y claves de contexto similares a las de autenticación.
- Los informes no deben incluir archivos multimedia del usuario, marcos decodificados, capturas de pantalla, archivos sin formato.
audio, volcados de almacenamiento local, volcados de entorno o registros arbitrarios.
- La aplicación almacena como máximo una pequeña cola local y permite al usuario elegir `ask`,
`always` o `off`.
- El envío utiliza únicamente la superficie de comando Rust. La ventana de salida no debe tener
Permisos de informe de fallos.
- Las credenciales GitHub no deben estar presentes en la aplicación de escritorio, configuración del repositorio,
o paquete visible para el cliente.

Arquitectura de retransmisión de fallos:

```text
release desktop app
  -> Rust crash reporter command
  -> https://crash.dustwave.xyz/v1/reports
  -> Cloudflare Worker validation, rate limiting, and sanitization
  -> GitHub App installation token
  -> aggregated GitHub issue
```

El Cloudflare Worker vive en `crash-relay/`. Se establecen los secretos de la aplicación GitHub
con `wrangler secret put` y su índice y entrada de límite de velocidad de espacios de nombres KV
huellas dactilares de accidentes. Informes similares actualizan un problema abierto en lugar de crear un
nuevo número para cada informe. La huella digital prefiere dimensiones estables como
tipo, superficie, plataforma, modo comando/backend/fuente, estado de salida nativa y
campos de código de error explícitos; El marco de pila normalizado o el mensaje son alternativas.
Los organismos emisores mantienen un estado agregado acotado en lugar de concatenar cada
informe.

## Acceso a archivos y medios locales

Los archivos personalizados deben permanecer detrás de la selección explícita del usuario.

Normas:

- No agregue un directorio de inicio amplio, una carpeta de descargas, una unidad extraíble o
concesiones de directorio recursivas.
- No persista las capacidades de acceso a archivos sin formato más allá de lo que requiere la plataforma
para la sesión seleccionada.
- No cargue medios seleccionados a un servidor.
- No envíe rutas de medios a análisis o registros remotos.
- Los archivos preestablecidos/perfiles importados deben analizarse y validarse como datos, no
ejecutado.
- Las exportaciones preestablecidas actuales excluyen los campos de fuente y medios, incluidos los privados
archivos multimedia y rutas multimedia absolutas.

## Cámara, micrófono y sistema de audio

La cámara y la captura de audio son entradas locales sensibles. La captura comienza desde visible
comportamiento de la aplicación, como seleccionar Cámara o habilitar la Reactividad de Audio. Audio
La reactividad es un modo predeterminado intencional, por lo que la aplicación puede solicitar
Permiso de micrófono/entrada durante el inicio. La captura sigue siendo local y controlada por el sistema operativo,
y el usuario puede detenerlo desactivando la reactividad de audio o cambiando el audio
fuente.

Identificador de paquete macOS actual:

```text
com.asciline.remix
```

Las compilaciones de desarrollo utilizan `com.asciline.remix.dev`. Restablecer las subvenciones para el desarrollo con
ese identificador; no utilice un paquete ad hoc con nombre de producción para pruebas de medios.

Ayudantes de restablecimiento de permisos:

```bash
tccutil reset Camera com.asciline.remix
tccutil reset Microphone com.asciline.remix
tccutil reset ScreenCapture com.asciline.remix
tccutil reset AudioCapture com.asciline.remix
```

Reglas de desarrollo:

- Mantenga las cadenas de uso en `src-tauri/Info.plist` precisas y específicas.
- Mantenga los derechos en `src-tauri/Entitlements.plist` alineados con la característica real
uso.
- Prefiere permisos de audio del sistema nativos más limitados cuando la plataforma expone
ellos.
- Mantenga los marcos de entidades delimitados. No envíe buffers de audio ilimitados sin procesar a través de
IPC cuando los vectores de características son suficientes. Usos de reactividad de audio derivados.
características como RMS, bandas, transitorio/flujo, presencia, brillo, densidad,
latir pulso y fase.
- Evite los bucles de reintento automático de captura que siguen solicitando o capturando después del usuario
niega el acceso.

## Actualizador y secretos de lanzamiento

El actualizador es la ruta en línea intencional. Dice:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

Requisitos de seguridad:

- Los paquetes de actualización deben estar firmados.
- La clave de actualización pública pertenece a `src-tauri/tauri.conf.json`.
- La clave de actualización privada pertenece al secreto de acciones GitHub
`TAURI_SIGNING_PRIVATE_KEY`.
- La contraseña de la clave de actualización pertenece al secreto de acciones GitHub
`TAURI_SIGNING_PRIVATE_KEY_PASSWORD`; Las claves de actualización cifradas no se pueden firmar.
en trabajos de lanzamiento no interactivos sin él.
- No cometa `/private/tmp/ascii-vj-remix-updater.key` ni ningún reemplazo
clave privada.
- Utilice `npm run updater:secret:set` y `npm run updater:secret:check` para
flujo de trabajo secreto actual GitHub.
- Los flujos de trabajo de lanzamiento no deben imprimir valores secretos ni pasar claves privadas como
Argumentos de línea de comando.
- Los flujos de trabajo de lanzamiento deben limitar los secretos de firma del actualizador a los pasos de solo firma.
nunca a todo el trabajo.

La firma de ID de desarrollador de Apple agrega más secretos. Certificados, contraseñas, claves API,
y las contraseñas del llavero CI residen en secretos GitHub, mientras que las credenciales de prueba locales
permanecer fuera del repositorio. La herramienta inactiva Windows Authenticode sigue el
Mismo límite: los valores secretos permanecen en los secretos GitHub y se utilizan identificadores de Azure no secretos.
Variables del repositorio GitHub cuando esa herramienta está habilitada explícitamente.

## FFmpeg y sidecars de códec

Los sidecars FFmpeg se incluyen para mantener la funcionalidad multimedia independiente. ellos son
También es un importante límite entre la cadena de suministro y las licencias.

Normas:

- No descargue FFmpeg, códecs ni archivos binarios de ayuda multimedia en tiempo de ejecución.
- Los sidecars de lanzamiento se crean a partir de una fuente oficial fijada.
- Los protocolos de red permanecen deshabilitados para las compilaciones de lanzamiento FFmpeg a menos que
La función de transmisión en serie requiere explícitamente una excepción revisada.
- Los sidecars necesitan versión, SHA-256, licencia, fuente y metadatos de AVISO.
- No confirme los binarios secundarios generados a menos que cambie la política de lanzamiento.

Validación:

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
npm run check:ffmpeg-release
```

## Preajustes y datos MIDI

Los ajustes preestablecidos y los mapas MIDI son datos locales, pero aún pueden dañar la aplicación si
la ruta de importación confía en ellos.

Reglas de importación:

- Analizar solo como datos JSON.
- Valide la versión del esquema y los campos admitidos.
- Sujete los valores numéricos a través de los mismos metadatos de control en vivo utilizados por la interfaz de usuario.
- Mantenga los identificadores de conjuntos de caracteres en la lista permitida. Cualquier rampa resuelta enviada a la salida nativa
debe estar limitado y restringido al atlas de glifos agrupados fijos.
- Rechace campos estructurales desconocidos en lugar de aplicarlos silenciosamente.
- No permita que los ajustes preestablecidos importados desactiven la superposición de estadísticas a menos que el usuario haya importado
esa elección es intencional y la interfaz de usuario lo deja claro.
- No incluya rutas de medios absolutas privadas en los paquetes exportados de forma predeterminada.

### MIDI y reglas SysEx

- El adaptador nativo acepta sólo nombres de puertos de entrada/salida que contengan `mioXC`;
No se admite USB UC-33e directo.
- Los comandos MIDI pertenecen únicamente a la ventana de control principal. La ventana de salida debe
nunca enumere dispositivos, lea eventos, capture volcados ni envíe SysEx.
- Colas de eventos, lecturas de eventos, recuentos de asignaciones, recuentos de paquetes, bytes decodificados y
La base64 almacenada debe permanecer limitada.
- Cada paquete saliente debe comenzar con `F0`, terminar con `F7` y permanecer dentro del
límite de bytes de transferencia completa.
- La instalación del perfil debe ser explícita a menos que el usuario haya habilitado Garantizar
Perfil en conexión.
- Garantizar la conexión envía como máximo una vez por reconexión física y no debe realizar un bucle
mientras la interfaz permanece conectada.
- MIDI Los objetivos de aprendizaje deben provenir del objetivo visual, de audio o de acción incluido en la lista permitida.
registro. No agregue fuente, cámara, Pop Out, pantalla de salida, actualizador, archivo,
o objetivos de informes de fallos.
- Los perfiles capturados y las asignaciones aprendidas permanecen locales y no deben contener medios.
rutas, fotogramas, audio sin procesar, credenciales o datos de red.

## Validación de seguridad

Utilice el conjunto de verificación relevante más pequeño para el cambio.

General:

```bash
git diff --check
npm run check:offline
npm run check:tauri-policy
npm run test:midi
```

Seguridad y embalaje de escritorio:

```bash
npm run check:desktop
npm run test:macos-secret-args
npm run release:secrets:check
```

Actualizador:

```bash
npm run test:updater-manifest
npm run updater:secret:check
```

FFmpeg y sidecars multimedia:

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
```

## Riesgos conocidos

- Las indicaciones de privacidad de macOS siguen siendo sensibles a la ruta de la aplicación, el identificador del paquete y
firma de identidad. Las identidades de producción y desarrollo están aisladas, pero una
La construcción de desarrollo deliberadamente ad hoc todavía recibe subvenciones específicas para la construcción.
- La firma ad hoc macOS solo es aceptable para compilaciones locales; los comunicados públicos son
Identificación del desarrollador firmada, notariada, grapada y validada por Gatekeeper.
- Los artefactos Windows 0.9.6 son vistas previas sin firmar y pueden activar Desconocido
Advertencias de Publisher, SmartScreen o Defender.
- El comportamiento de medios/cámara/audio de Linux varía según la distribución, WebKitGTK, controladores,
y configuración del portal.
- El modo Stream existe en las rutas de desarrollo pero está oculto en la interfaz de usuario normal y
excluidos de la producción de CSP.

Fortalecimiento de seguridad prospectivo, firma Windows, exposición de transmisión y MIDI
El trabajo del perfil se rastrea en [Roadmap](/es/docs/reference/roadmap/).

## Informar problemas de seguridad

Informar problemas de seguridad de forma privada a:

[alonso@dustwave.xyz](mailto:alonso@dustwave.xyz)

Incluya el sistema operativo, la versión de la aplicación, el tipo de fuente, si Pop Out fue
activo y cualquier permiso o estado de actualización relevante.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
