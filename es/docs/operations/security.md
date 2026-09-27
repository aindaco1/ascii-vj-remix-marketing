---
title: Seguridad
description: Documentación de seguridad derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Operaciones
lang: es
---

<a id="security"></a>

# Seguridad

Esta guía documenta el modelo de seguridad actual, las compensaciones aceptadas y las prácticas de validación para ASCII VJ Remix.

El perfil de riesgo de ASCII VJ Remix es una aplicación de escritorio Tauri local que maneja medios locales, cámaras, micrófonos, audio del sistema, ventanas de salida nativas, sidecars FFmpeg incluidos, artefactos de actualización firmados e informes de fallos revisados/desinfectados.

<a id="security-principles"></a>

## Principios de seguridad

- Mantenga la aplicación empaquetada localmente primero y fuera de línea de forma predeterminada.
- No agregue CDN, fuentes alojadas, códecs alojados, telemetría, renderizadores alojados ni descargas de dependencias de tiempo de ejecución.
- Trate el actualizador de versiones GitHub y el informe de fallas solo de producción como las únicas rutas de ejecución en línea intencionales.
- Mantenga local los medios seleccionados por el usuario, los fotogramas de la cámara y el análisis de audio.
- Requerir una selección explícita del usuario antes de leer un archivo local.
- Mantenga las capacidades de Tauri limitadas y específicas de ventana.
- Mantenga la ventana de salida como una superficie de presentación, no como un segundo controlador de aplicación privilegiado.
- Mantenga los secretos de firma de lanzamiento, firma de actualizador y certificación notarial fuera del repositorio.
- El identificador del paquete de producción es `com.asciline.remix`; cambiarlo crea una migración de concesión de privacidad macOS.
- Mantener el desarrollo local en `com.asciline.remix.dev`; nunca firme ni instale una compilación de desarrollo ad-hoc con el identificador de producción.

<a id="security-architecture"></a>

## Arquitectura de seguridad

|Superficie|Límite actual|Nivel de riesgo|Notas|
| --- | --- | --- | --- |
|Archivos de imagen/vídeo locales|API de archivos del navegador o cuadro de diálogo Tauri más registro de medios local de sesión|Medio|Los archivos se seleccionan explícitamente sin acceso amplio al sistema de archivos.|
|Medios de demostración incorporados|Incluido en `media/` y copiado en los recursos de la aplicación|Bajo|Los medios de demostración son locales y versionados.|
|Paletas integradas/atlas de glifos|Catálogo de paletas propiedad del proyecto más páginas de glifos ancladas, generadas y agrupadas localmente|Bajo|Sin importación/descarga de paquetes de paletas de tiempo de ejecución, fuentes, CDN o recursos de idioma.|
|Entrada de cámara|Navegador `getUserMedia`; ruta nativa AVFoundation, Media Foundation o FFmpeg V4L2 incluida para Pop Out de una sola cámara|Medio|Requiere permiso de privacidad del sistema operativo. Los fotogramas permanecen en el equipo. Windows usa un único cliente de Media Foundation para la salida nativa y un puente binario de preview en memoria; Linux libera la cámara del WebView para la captura exclusiva V4L2.|
|Audio de micrófono/entrada|Proveedores de audio web y Tauri nativos|Medio|Requiere permiso de privacidad del sistema operativo. Las funciones de análisis están limitadas.|
|Audio del sistema/pantalla|El navegador muestra audio cuando está presente; proveedores de escritorio nativos donde estén disponibles|Medio|Los permisos de la plataforma varían. No amplíe la captura más allá de las necesidades de funciones.|
|Preajustes/configuraciones|Almacenamiento del navegador local, IndexedDB, JSON importado/exportado|Bajo a Medio|Datos escritos por el usuario. Validar las importaciones antes de aplicar.|
|Capturas de pantalla|Escritor de escritorio Rust solo para ventana principal|Medio|Acepta solo bytes PNG delimitados, crea un archivo único y no devuelve ninguna ruta. No hay un alcance amplio del sistema de archivos ni un cuadro de diálogo para guardar.|
|Ventana de salida|Ventana de salida Tauri con permisos mínimos|Medio|No debe exponer la selección de medios, el sistema de archivos, el actualizador ni las API de comandos amplios.|
|Comandos Tauri|`src-tauri/src/lib.rs` más archivos de capacidad|Alto|Trate cada comando como un límite de seguridad. Validar entradas en Rust.|
|Protocolo de activos|Vacío de forma predeterminada, expandido solo para necesidades de sesión/medios seleccionados|Alto|Evite caminos amplios y persistentes.|
|sidecares FFmpeg|Recursos agrupados con comprobaciones de políticas y metadatos de fuente/procedencia|Medio|Sin descargas de tiempo de ejecución. Los sidecars de liberación desactivan los protocolos de red.|
|Actualizador|Una verificación de inicio de producción más acciones explícitas de manual/descarga/instalación contra el punto final de versiones GitHub con paquetes firmados|Alto|Los controles de lanzamiento no envían datos del producto. La clave de firma privada es externa; La clave pública está comprometida.|
|reportero de accidentes|POST solo de Rust a `https://crash.dustwave.xyz/v1/reports` en compilaciones de producción|Alto|Los informes están delimitados, desinfectados, configurables por el usuario y retransmitidos a los problemas de GitHub mediante un Cloudflare Worker.|
|Experimental MIDI y UC-33e SysEx|Comandos Rust solo de la ventana principal, lista de puertos permitidos mioXC, colas acotadas y límites de paquetes|Medio|Los perfiles permanecen locales y no pueden apuntar a fuentes, cámaras, Pop Out ni pantallas de salida. La verificación de restauración física del banco completo sigue incompleta.|
|Registros e informes de humo.|Artefactos de prueba/desarrollador local|Bajo a Medio|No registre rutas de archivos privados, audio sin formato ni valores ambientales confidenciales a menos que sea necesario para una depuración explícita.|

<a id="release-security-posture"></a>

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

<a id="tauri-runtime-policy"></a>

## Política de tiempo de ejecución Tauri

El tiempo de ejecución de producción es intencionalmente limitado:

- `src-tauri/tauri.conf.json` mantiene una Política de Seguridad de Contenidos de producción restrictiva.
- El CSP de producción no permite puntos finales HTTP/WebSocket de host local arbitrarios; Los puntos finales de desarrollo/transmisión de localhost solo existen en `devCsp`.
- `npm run check:tauri-policy` verifica la política de tiempo de ejecución solo local, la excepción del punto final del actualizador GitHub y el límite del comando del informe de fallos solo Rust. También hace coincidir cada invocación literal de Tauri de la interfaz con su archivo de permisos generado y la concesión de capacidad de la ventana principal.
- Las capacidades de `src-tauri/capabilities/` dividen los privilegios de la ventana principal de los privilegios de la ventana de salida.
- La ventana principal posee selección de medios, administración de salida, proveedores de audio y trabajo de captura de pantalla, actualización e informe de fallas.
- La ventana de salida solo escucha mensajes de renderizado/salida y expone el comportamiento mínimo de cierre/pantalla completa que necesita.

Al agregar un comando Tauri:

1. Prefiera un comando limitado con entradas escritas a un comando genérico.
2. Valide rutas, identificadores, dimensiones, valores de enumeración y límites numéricos en Rust.
3. Otorgue el comando solo a la ventana que lo necesita.
4. Evite devolver rutas sin formato del sistema de archivos a la vista web a menos que la interfaz de usuario necesite mostrar un nombre de archivo seleccionado por el usuario.
5. Agregue o actualice una prueba/verificación cuando el comando cambie la postura de seguridad de la aplicación.

<a id="crash-reporting"></a>

## Informe de fallos

Los informes de fallas se aceptan por preferencia y son solo de producción para el envío de la red. Las compilaciones de depuración/desarrollo pueden capturar informes locales para realizar pruebas, pero Rust se niega a enviarlos.

El relay compartido también tiene adaptadores con activación independiente para Podcast Visualizer, MKV Magic, Auto Subtitle, CutNotes, Road Notice, Paper y Record. Cada uno mantiene un esquema acotado de campos permitidos y un repositorio de destino fijo, y reutiliza la agregación serializada de incidencias. No amplían los datos admitidos por los informes de ASCII VJ. La [guía del relay](https://github.com/aindaco1/ascii-vj-remix/blob/main/crash-relay/README.md) define los esquemas de cada ruta, la evidencia de despliegue y los límites de deduplicación; la [guía de migración](/es/docs/development/shared-desktop-services/) documenta los paquetes compartidos y los cambios posteriores a la última versión de escritorio.

El adaptador de MKV Magic usa una entrada con activación independiente y una página de revisión del mismo origen en el navegador. Solo una acción explícita de Send envía la proyección de campos permitidos, limitada a 4 KiB; no se aceptan registros sin filtrar, medios, mensajes arbitrarios, credenciales ni incidentes completos de fallo. La página elimina los datos del fragmento antes de renderizar y usa CSP con nonce, no-referrer y no-store. Comparte la agregación serializada y el escritor de GitHub, pero no el código de la aplicación ni los permisos de escritorio. La app principal de MKV sigue sin permisos de red. El acceso al repositorio y las pruebas sintéticas sobre el despliegue se validan por separado; consulta la guía del relay para la retención y reversión.

El reportero de accidentes puede capturar:

- eventos front-end `error`.
- eventos front-end `unhandledrejection`.
- Fallos del comando Tauri.
- Rust informes de gancho de pánico importados en el próximo lanzamiento.
- Informes de respaldo/fallo del renderizador que contienen solo campos limitados preestablecidos/backend, clase de origen, resumen de errores y eventos recientes del renderizador.
- Fallos de medios nativos/cámara/espejo con una etiqueta de componente delimitada y un resumen de errores desinfectado.
- instantáneas manuales explícitas del estado actual con una nota de usuario limitada opcional y el mismo contexto estructurado de renderizado/salida.

Requisitos de seguridad:

- Los informes deben estar delimitados antes del almacenamiento local y antes de su envío.
- Reports debe redactar rutas locales, URL de activos/archivos, correos electrónicos, tokens, cookies, contraseñas y claves de contexto similares a las de autenticación.
- Reports no debe incluir archivos multimedia del usuario, fotogramas decodificados, capturas de pantalla, audio sin formato, volcados de almacenamiento local, volcados de entorno ni registros arbitrarios.
- Los informes de micrófonos no disponibles/desconectados esperados de versiones anteriores se eliminan localmente utilizando el mismo clasificador de errores de hardware estrecho utilizado en el momento de la captura; Los errores inesperados del micrófono permanecen en cola.
- La pérdida del identificador de la ventana de salida nativa durante el cierre normal o el reemplazo del trabajador es un desmontaje, no un bloqueo. Las fallas inesperadas de medios, cámaras, espejos o renderizadores siguen siendo reportables a través del contrato de error/componente limitado.
- Los diagnósticos del renderizador se limitan a los ocho eventos estructurados desinfectados más recientes. No deben convertirse en una ruta general de carga de registros locales.
- La aplicación almacena como máximo una pequeña cola local y permite al usuario elegir `ask`, `always` o `off`.
- El control Reports permanece accesible con una cola vacía para que se pueda revisar la preferencia antes de que ocurra un error. El estado vacío no crea ni envía un informe.
- El envío utiliza únicamente la superficie de comando Rust. La ventana de salida no debe tener permisos de informe de fallos.
- El envío requiere además un binario del modo de lanzamiento y el identificador exacto del paquete de producción. Los paquetes optimizados de desarrollo y control de calidad conservan su identidad independiente y su cola local, pero no pueden enviar informes.
- Las credenciales GitHub no deben estar presentes en la aplicación de escritorio, la configuración del repositorio o el paquete visible para el cliente.

Arquitectura de retransmisión de fallos:

```text
release desktop app
  -> Rust crash reporter command
  -> https://crash.dustwave.xyz/v1/reports
  -> Cloudflare Worker validation, rate limiting, and sanitization
  -> GitHub App installation token
  -> aggregated GitHub issue
```

El Cloudflare Worker vive en `crash-relay/`. Los secretos de su aplicación GitHub se configuran con `wrangler secret put`, y sus espacios de nombres KV limitan la velocidad de admisión y las huellas dactilares de bloqueo del índice. Los informes similares actualizan un problema abierto en lugar de crear un problema nuevo para cada informe. La huella digital prefiere dimensiones estables como tipo, superficie, plataforma, modo comando/backend/fuente, estado de salida nativa y campos de código de error explícitos; El marco de pila normalizado o el mensaje son alternativas. Los organismos emisores mantienen un estado agregado acotado en lugar de concatenar cada informe.

Las fallas del escritor de diagnóstico de medios local de mejor esfuerzo no son fatales y deben ser ignoradas tanto por el adaptador de escritorio como por el relé. No describen una falla de la aplicación y no deben crear problemas GitHub.

El canario de aceptación de producción opcional está codificado y se niega a ejecutarse cuando ya hay un informe de usuario pendiente o la preferencia es `off`. Nunca debe expandirse a una ruta de carga de registros general.

<a id="local-media-and-file-access"></a>

## Acceso a archivos y medios locales

Los archivos personalizados deben permanecer detrás de la selección explícita del usuario.

Normas:

- No agregue concesiones de directorio de inicio amplio, carpeta de descargas, unidad extraíble o directorio recursivo.
- No persista las capacidades de acceso a archivos sin formato más allá de lo que la plataforma requiere para la sesión seleccionada.
- No cargue medios seleccionados a un servidor.
- No envíe rutas de medios a análisis o registros remotos.
- Los archivos preestablecidos/de perfil importados deben analizarse y validarse como datos, no ejecutarse.
- Las exportaciones preestablecidas actuales excluyen los campos de origen y multimedia, incluidos los archivos multimedia privados y las rutas multimedia absolutas.

<a id="camera-microphone-and-system-audio"></a>

## Cámara, micrófono y sistema de audio

La cámara y la captura de audio son entradas locales sensibles. La captura comienza desde el comportamiento visible de la aplicación, como seleccionar Cámara o habilitar Reactividad de audio. La reactividad de audio es un modo predeterminado intencional, por lo que la aplicación puede solicitar permiso de entrada/micrófono durante el inicio. La captura permanece local y controlada por el sistema operativo, y el usuario puede detenerla desactivando la reactividad de audio o cambiando la fuente de audio.

La cámara única Pop Out puede abrir la cámara ya seleccionada a través de un proveedor de plataforma nativa: AVFoundation en macOS, Media Foundation en Windows o V4L2 a través del tiempo de ejecución FFmpeg incluido con red deshabilitada en Linux. No agrega un nuevo punto final remoto ni persiste los fotogramas de la cámara. Los diagnósticos manuales pueden contener contadores de tiempo y de reserva independientes del dispositivo, nunca bytes de trama. Windows utiliza un cliente de captura Media Foundation mientras la salida nativa está abierta. No envía píxeles de la cámara a través de una red o un almacén persistente. El trabajador nativo expone solo su último JPEG reducido a través de una respuesta de comando binario al WebView principal. El fotograma se dibuja en la memoria, no se registra ni persiste y se reemplaza por el siguiente fotograma.

Identificador de paquete macOS actual:

```text
com.asciline.remix
```

Las compilaciones de desarrollo utilizan `com.asciline.remix.dev`. Restablecer las subvenciones de desarrollo con ese identificador; no utilice un paquete ad hoc con nombre de producción para pruebas de medios.

Ayudantes de restablecimiento de permisos:

```bash
tccutil reset Camera com.asciline.remix
tccutil reset Microphone com.asciline.remix
tccutil reset ScreenCapture com.asciline.remix
tccutil reset AudioCapture com.asciline.remix
```

Reglas de desarrollo:

- Mantenga las cadenas de uso en `src-tauri/Info.plist` precisas y específicas.
- Mantenga los derechos en `src-tauri/Entitlements.plist` alineados con el uso real de funciones.
- Prefiera permisos de audio del sistema nativo más limitados cuando la plataforma los exponga.
- Mantenga los marcos de entidades delimitados. No envíe buffers de audio ilimitados sin procesar a través de IPC cuando los vectores de características sean suficientes. La reactividad de audio utiliza características derivadas como RMS, bandas, transitorio/flujo, presencia, brillo, densidad, pulso y fase.
- Evite los bucles de reintento automático de captura que siguen solicitando o capturando después de que el usuario niega el acceso.

<a id="updater-and-release-secrets"></a>

## Actualizador y secretos de lanzamiento

El actualizador es la ruta en línea intencional. Dice:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

La aplicación de producción verifica esos metadatos una vez por inicio sin bloquear el inicio del renderizador. Los resultados de la versión actual y de los fallos de la red permanecen silenciosos; cuando existe una versión firmada más reciente, el control Update existente la muestra. La descarga, instalación y reinicio requieren una acción explícita del usuario. La solicitud no contiene medios, fotogramas, datos de cámara o audio, ajustes preestablecidos, estado MIDI, informes de fallos, rutas locales, credenciales o identificadores de análisis. Las compilaciones de desarrollo no reciben el punto final de producción. La solicitud de inicio necesariamente expone metadatos de conexión ordinarios a GitHub y la red circundante.

Requisitos de seguridad:

- Los paquetes de actualización deben estar firmados.
- La clave de actualización pública pertenece a `src-tauri/tauri.conf.json`.
- La clave de actualización privada pertenece al secreto de acciones GitHub `TAURI_SIGNING_PRIVATE_KEY`.
- La contraseña de la clave de actualización pertenece al secreto de acciones GitHub `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`; Las claves de actualización cifradas no se pueden firmar en trabajos de versión no interactivos sin ellas.
- No confirme `/private/tmp/ascii-vj-remix-updater.key` ni ninguna clave privada de reemplazo.
- Utilice `npm run updater:secret:set` y `npm run updater:secret:check` para el flujo de trabajo secreto actual GitHub.
- Los flujos de trabajo de lanzamiento no deben imprimir valores secretos ni pasar claves privadas como argumentos de línea de comandos.
- Los flujos de trabajo de lanzamiento deben limitar los secretos de firma del actualizador a los pasos de solo firma, nunca a todo el trabajo.

La firma de ID de desarrollador de Apple agrega más secretos. Los certificados, contraseñas, claves API y contraseñas de llavero CI se encuentran en secretos GitHub, mientras que las credenciales de prueba locales permanecen fuera del repositorio. Las herramientas inactivas Windows Authenticode siguen el mismo límite: los valores secretos permanecen en secretos GitHub y los identificadores de Azure no secretos usan variables del repositorio GitHub cuando esas herramientas están habilitadas explícitamente.

<a id="ffmpeg-and-codec-sidecars"></a>

## FFmpeg y sidecars de códec

Los sidecars FFmpeg se incluyen para mantener la funcionalidad multimedia independiente. También son un límite importante para la cadena de suministro y las licencias.

Normas:

- No descargue FFmpeg, códecs ni archivos binarios de ayuda multimedia en tiempo de ejecución.
- El respaldo nativo para medios integrados acepta solo los dos identificadores de fuente exactos enviados Demo Video; no otorga a la vista web una ruta general del sistema de archivos.
- Los sidecars de lanzamiento se crean a partir de una fuente oficial fijada.
- Los protocolos de red permanecen deshabilitados para las compilaciones de lanzamiento FFmpeg a menos que una función de transmisión en formato producto requiera explícitamente una excepción revisada.
- Los sidecars necesitan versión, SHA-256, licencia, fuente y metadatos de AVISO.
- No confirme los binarios secundarios generados a menos que cambie la política de lanzamiento.

Validación:

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
npm run check:ffmpeg-release
```

<a id="presets-and-midi-data"></a>

## Preajustes y datos MIDI

Los ajustes preestablecidos y los mapas MIDI son datos locales, pero aún pueden dañar la aplicación si la ruta de importación confía en ellos.

Reglas de importación:

- Analizar solo como datos JSON.
- Valide la versión del esquema y los campos admitidos.
- Sujete los valores numéricos a través de los mismos metadatos de control en vivo utilizados por la interfaz de usuario.
- Mantenga los identificadores de conjuntos de caracteres en la lista permitida. Cualquier rampa resuelta enviada a la salida nativa debe estar limitada a 96 escalares admitidos y restringida a la cobertura del atlas incluido.
- Rechace campos estructurales desconocidos en lugar de aplicarlos silenciosamente.
- No permita que los ajustes preestablecidos importados deshabiliten Stats Overlay a menos que el usuario haya importado esa opción intencionalmente y la interfaz de usuario lo deje claro.
- No incluya rutas de medios absolutas privadas en los paquetes exportados de forma predeterminada.
- Las listas de reproducción preestablecidas almacenan solo un nombre limitado, metadatos de tiempo/modo e identificaciones preestablecidas estables. No duplican configuraciones visuales ni conservan campos de fuente/medios.

<a id="midi-and-sysex-rules"></a>

### MIDI y reglas SysEx

- El adaptador nativo acepta sólo nombres de puertos de entrada/salida que contengan `mioXC`; No se admite USB UC-33e directo.
- Los comandos MIDI pertenecen únicamente a la ventana de control principal. La ventana de salida nunca debe enumerar dispositivos, leer eventos, capturar volcados ni enviar SysEx.
- Las colas de eventos, las lecturas de eventos, los recuentos de asignaciones, los recuentos de paquetes, los bytes decodificados y la base64 almacenada deben permanecer delimitados.
- Cada paquete saliente debe comenzar con `F0`, terminar con `F7` y permanecer dentro del límite de bytes de transferencia total.
- La instalación del perfil debe ser explícita a menos que el usuario haya habilitado Ensure Profile on Connection.
- Garantizar la conexión envía como máximo una vez por reconexión física y no debe realizar un bucle mientras la interfaz permanece conectada.
- MIDI Los objetivos de aprendizaje deben provenir del registro de objetivos visuales, de audio o de acción incluidos en la lista permitida. No agregue fuente, cámara, Pop Out, pantalla de salida, actualizador, archivo ni destinos de informes de fallas.
- Los perfiles capturados y las asignaciones aprendidas permanecen locales y no deben contener rutas de medios, fotogramas, audio sin procesar, credenciales ni datos de red.

<a id="security-validation"></a>

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
npm run test:desktop-updater
npm run test:updater-manifest
npm run updater:secret:check
```

FFmpeg y sidecars multimedia:

```bash
npm run test:ffmpeg-policy
npm run check:ffmpeg-resources
```

<a id="known-risks"></a>

## Riesgos conocidos

- Las indicaciones de privacidad de macOS siguen siendo sensibles a la ruta de la aplicación, el identificador del paquete y la identidad de firma. Las identidades de producción y desarrollo están aisladas, pero una construcción de desarrollo deliberadamente ad hoc aún recibe subvenciones específicas para esa construcción.
- La firma ad hoc macOS solo es aceptable para compilaciones locales; los lanzamientos públicos están firmados con el ID del desarrollador, notariados, engrapados y validados por Gatekeeper.
- Los artefactos Windows actuales son vistas previas sin firmar y pueden activar advertencias de Editor desconocido, SmartScreen o Defender.
- El comportamiento de los medios/cámara/audio de Linux varía según la distribución, WebKitGTK, los controladores y la configuración del portal.
- El modo de transmisión existe en las rutas de desarrollo, pero está oculto en la interfaz de usuario normal y excluido del CSP de producción.

El posible fortalecimiento de la seguridad, la firma Windows, la exposición de la transmisión y el trabajo del perfil MIDI se rastrean en el [Roadmap](/es/docs/reference/roadmap/).

<a id="reporting-security-issues"></a>

## Informar problemas de seguridad

Informar problemas de seguridad de forma privada a:

[alonso@dustwave.xyz](mailto:alonso@dustwave.xyz)

Incluya el sistema operativo, la versión de la aplicación, el tipo de fuente, si Pop Out estaba activo y cualquier permiso relevante o estado del actualizador.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
