---
title: Registro de cambios
description: Documentación de registro de cambios derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Referencia
lang: es
---

# Registro de cambios

La versión 0.9.9 mantiene accesibles las preferencias de informes de fallos aunque la cola esté vacía, elimina la lectura duplicada del backend de la barra superior y amplía las pruebas de humo de la interfaz empaquetada para cubrir ambos controles. La versión 0.9.8 restaura el control Actualizar de producción y la comprobación al inicio, agrega una prueba de regresión de la interfaz empaquetada y acorta las compilaciones al compilar la app y el entorno FFmpeg en paralelo antes de reutilizar los artefactos verificados. La versión 0.9.7 incorpora el controlador de comprobación silenciosa al inicio, conserva la instalación aprobada por el usuario y refuerza la resiliencia del transporte de versiones. La versión 0.9.6 continúa la puesta en marcha experimental de MIDI, reduce la sobrecarga medida de las rutas críticas del renderizador y la salida sin cambiar las matemáticas visuales ni la calidad, y refuerza la instalación de macOS mediante arrastre a Aplicaciones. La versión 0.9.5 añade 23 presets de caracteres con créditos e inspirados en ascii.today, además de control MIDI DIN nativo experimental para un Evolution/M-Audio UC-33e mediante un iConnectivity mioXC, con cuatro páginas completas de control, soft takeover, selección numérica de presets, MIDI Learn y captura/restauración SysEx del banco completo. La versión 0.9.3 adopta la distribución pública firmada y notarizada para macOS, publica Windows como vista previa sin firmar mientras se aplaza la firma y amplía la reactividad de audio con controles de mezcla densa que reducen la sobrerreacción a música cargada. La versión 0.9.0 sigue siendo la primera base documental del conjunto de funciones actual de ASCII VJ Remix.

## [0.9.9] - 2026-08-26

### Corregido

- El control Informes de la barra superior permanece visible en las compilaciones Tauri aunque la cola de fallos esté vacía, de modo que los usuarios pueden revisar la preferencia `ask`, `always` u `off` sin esperar a que ocurra un error. Los informes pendientes todavía añaden un contador y un estado de advertencia; Enviar y Descartar permanecen desactivados cuando la cola está vacía.
- Se eliminó la lectura duplicada del backend del lado derecho de la barra superior. El selector Backend central sigue siendo el control canónico, mientras que la superposición Estadísticas continúa mostrando el backend resuelto en tiempo de ejecución.
- Los listeners de la prueba de humo de la interfaz del actualizador empaquetado ahora se registran antes de inicializar los dispositivos, por lo que una solicitud temprana no puede competir con el arranque de la cámara o el audio.

### Seguridad

- Los informes siguen conteniendo únicamente datos de fallos limitados y sanitizados. Los diagnósticos de medios locales y los registros arbitrarios no se adjuntan ni se envían.
- Se añadió un canario opcional de aceptación del relay de fallos de producción que se niega a ejecutarse cuando ya hay un informe de usuario pendiente y solo envía una carga sintética fija.

### Validación

- Se añadieron pruebas deterministas de la interfaz de informes de fallos para los estados de navegador, vacío, pendiente, desactivado y ocupado.
- Las pruebas de humo estática y empaquetada ahora exigen que no exista el estado duplicado del backend. La prueba empaquetada para macOS, Windows y Linux también exige que el control Informes permanezca visible, ya sea vacío o con el contador de informes pendientes.

## [0.9.8] - 2026-08-26

### Fijado

- Se restauró el control de actualización de producción y la verificación de inicio automático otorgando
la ventana principal el permiso estrecho `core:app:allow-name` utilizado para verificar el
Identidad de la aplicación de producción. El permiso faltante provocó el control y el estado.
El área parpadeará y luego desaparecerá en 0.9.6 y 0.9.7.
- Las fallas de disponibilidad del actualizador ahora registran su causa en lugar de fallar silenciosamente.

### Cambió

- La versión CI ahora resuelve una confirmación de etiqueta inmutable, requiere la exactitud
`Desktop` flujo de trabajo de empuje principal para tener éxito en ese compromiso y construye el
El tiempo de ejecución FFmpeg y el binario de la aplicación Tauri en paralelo.
- La agrupación restaura los artefactos exactos del flujo de trabajo de un día. FFmpeg mantiene su
comprobaciones de fuente/hash/recurso ancladas, mientras que la transferencia binaria de la aplicación verifica
confirmación, plataforma, versión, tamaño de bytes y SHA-256 antes de que Tauri lo empaquete
sin recompilar.

### Validación

- Se agregaron pruebas de reutilización de lanzamiento y compilación que cubren la selección exacta de ejecución del flujo de trabajo y
Rechazo de archivos binarios de aplicaciones alterados o no coincidentes.
- Smoke de lanzamiento publicado ahora inicia la aplicación empaquetada en macOS, Windows y
Linux y requiere que el control Actualizar permanezca visible, cubriendo la información real
Ruta de la interfaz de usuario en lugar de invocar únicamente el actualizador nativo directamente.

## [0.9.7] - 2026-08-26

### Agregado

- La aplicación de escritorio de producción ahora realiza una versión de metadatos sin bloqueo.
compruebe si hay paquetes de actualización firmados cada vez que se abra. Versión actual y
las comprobaciones de inicio fuera de línea permanecen silenciosas; una versión más nueva aparece a través del
control de actualización existente en la barra superior. Se evitó una regresión de la capacidad de producción
ese control permanezca disponible hasta la corrección 0.9.8.
- El control de actualización manual permanece disponible para una nueva verificación inmediata, y
la descarga, la instalación y el reinicio siguen siendo iniciados explícitamente por el usuario.

### Fijado

- Las descargas de fuentes de lanzamiento ahora reintentan fallas de transporte transitorias limitadas y
promover solo archivos tar FFmpeg completados antes de la verificación SHA-256 fijada.
- El envío automático de lanzamiento de escritorio ahora reintenta fallas transitorias de la API GitHub
con retroceso acotado.

### Seguridad

- Las comprobaciones automáticas reutilizan el punto final del actualizador Tauri existente y están firmados.
artefactos. No envían medios, cámara, audio, ajustes preestablecidos, MIDI, informes de fallos ni
los datos de ruta local y las compilaciones de desarrollo continúan deshabilitando la producción
puntos finales del actualizador.

### Validación

- Se agregó cobertura determinista del controlador-actualizador para una verificación por lanzamiento.
resultados silenciosos actuales/fuera de línea, descubrimiento de actualizaciones sin instalación automática,
el respaldo manual, el progreso de la descarga y la transferencia de reinicio.

## [0.9.6] - 2026-08-17

### Cambió

- El macOS nativo Pop Out ahora convierte y carga solo un fotograma fuente RGB decodificado
cuando cambia su versión del marco de origen. El enlace de visualización puede continuar presentando
y aplicar parámetros visuales/audio en vivo al actualizar la pantalla sin cargar
el mismo cuadro de video nuevamente.
- WebGPU reutiliza almacenamiento de respaldo uniforme, vistas de textura y grupos de enlace estables;
El enlace de textura externa de vídeo y navegador por fotograma permanece dinámico según sea necesario.
- WebGL2 resuelve las ubicaciones uniformes del sombreador en la inicialización en lugar de mirar
hasta las 18 ubicaciones en cada cuadro renderizado.
- Las transiciones numéricas preestablecidas/WTF actualizan solo los controles cuyos valores están cambiando.
Listas de fuentes, opciones de cámara, visibilidad, medidores y el resto del control.
Las superficies se sincronizan una vez al finalizar en lugar de en cada animación.
marco.
- El humo de rendimiento de interfaz de usuario optimizado utiliza valores predeterminados limpios y no estructurales fijos
objetivos de transición, registra P10/P50 así como el promedio FPS, informa el
backends realmente visitados y acepta un paquete de aplicaciones exacto a través de
`ASCILINE_SOURCE_APP` para comparaciones de versiones.
- Avanzó la versión de escritorio/paquete a 0.9.6. MIDI sigue siendo experimental mientras
Se completa la puesta en servicio física del UC-33e/mioXC.
- Los comandos normales de desarrollo y paquete de depuración de Tauri ahora usan `ASCII VJ Remix
Dev` with bundle identifier `com.asciline.remix.dev`. El nombre de la producción y
El identificador `com.asciline.remix` sigue siendo exclusivo del embalaje de lanzamiento.
- El macOS DMG mantiene Tauri como su único empaquetador, hace el estándar
diseño de aplicación a aplicaciones explícito y documenta el DMG como el principal
instalador manual. El `.app.tar.gz` sigue siendo un artefacto de actualización.

### Fijado

- Se corrigió la guía de puesta en servicio del UC-33e para usar el modo de botón extendido 146 para
distintos valores de prensa/comunicados. Una asignación CC estándar simple alterna entre
dos valores y no proporciona los bordes momentáneos esperados por la aplicación.
- Se aclaró que Control Select es el único botón físico `SELECT` y se agregó
programación exacta en el panel frontal, almacenamiento, captura/restauración SysEx y verificación
pasos.

### Rendimiento

- En la versión de prueba optimizada de Apple Silicon macOS, se presentó un video de 24 FPS en
60 FPS en Pop Out nativo con aproximadamente 23,8 cargas de origen y 36,3 omisiones de carga
por segundo: aproximadamente el 60% del trabajo de conversión/carga duplicado anterior se
eliminado mientras la presentación permaneció en 60.1 FPS.
- Las fases constantes de construcción optimizada se mantuvieron en calidad equivalente y no retrocedieron:
la referencia 0.9.5 publicada midió 35,8 FPS principal / 39,3 FPS con Pop Out,
mientras que el candidato final 0.9.6 midió 38.6/39.0 FPS y sostuvo 35.9
FPS durante su fase de transición numérica fija.
- El arnés de humo estático ahora afirma que una transición numérica no realiza
Más de dos sincronizaciones de control de fuente y una cámara/visual completo.
sincronización, en lugar de repetir el trabajo completo de la interfaz de usuario durante toda la interpolación.
- Código de sombreador de renderizador, muestreo, procesamiento de color, cálculo de glifos, salida
La resolución, la fuente FPS y los controles de calidad no cambian.

### Seguridad

- Se eliminó la sincronización del corredor local en `/Applications/ASCII VJ Remix.app`.
El corredor ahora acepta solo el identificador del paquete de desarrollo y lo rechaza.
firma ad hoc de forma predeterminada, lo que evita que las reconstrucciones locales reemplacen el
aplicación de producción o contaminar sus concesiones de privacidad macOS.
- Las compilaciones de desarrollo deshabilitan los artefactos del actualizador y los puntos finales del actualizador de producción.
- La validación de la versión macOS ahora requiere el identificador exacto del paquete de producción,
ID de desarrollador ID de equipo `PWT3Q52LZ2`, tiempo de ejecución reforzado y un equipo estable
requisito designado. Las identidades ad-hoc/solo hash de código fallan al cerrarse.
- La validación de la versión extrae la carga útil real del actualizador `.app.tar.gz` y
verifica que su identidad y el requisito designado coincidan con el documento notariado
paquete de aplicaciones.
- La validación de la versión verifica la integridad de DMG, monta la imagen como de solo lectura bajo un
raíz temporal privada, acepta solo la aplicación, el enlace exacto `/Applications` y
revisó los metadatos Tauri (el ícono de volumen requerido más un ícono regular opcional)
`.DS_Store`), y aplica la estructura de la aplicación existente y la identidad de producción.
cheques a la copia montada.
- El humo de lanzamiento publicado ahora requiere y revalida el DMG descargado antes
ejercitando el salto del actualizador. La editorial se niega a reemplazar el artefacto existente
bytes para la misma etiqueta de lanzamiento.

### Validación

- Se agregó una prueba unitaria Rust para decisiones de carga de fuentes nativas versionadas.
- Se agregó cobertura de humo del navegador para el trabajo de interfaz de usuario de transición numérica limitada.
- Análisis extendido de registros de salida nativos con tasas de carga de origen y de omisión de carga.
- Se agregó cobertura de unidad multiplataforma para el análisis de identidad de firma de código macOS y
Rechazo de requisitos ad-hoc, identificadores incorrectos, equipos incorrectos y modificados.
artefactos.
- Se agregó diseño DMG multiplataforma, punto de montaje, descubrimiento de artefactos y montaje.
pruebas de contrato de estructura de aplicación.
- Se agregó un trabajo de humo de lanzamiento publicado macOS 26 que compara
Requisitos de identificación del desarrollador, realiza un reemplazo del actualizador basado en la aplicación,
y revalida la identidad del paquete actualizado.
- Se validó la compilación optimizada de `.app` más renderizado estático, matemáticas del renderizador,
reactividad de audio, los 188 enlaces predeterminados MIDI, la política Tauri y 47 Rust
pruebas en macOS Apple Silicon.
- Construyó y montó una aplicación local 0.9.6/canario DMG optimizada y aprobó el protocolo compartido.
verificación de paquete/recurso/diseño. Este artefacto local está firmado ad hoc; la final
Se requiere un canario firmado y certificado por notario con la identificación del desarrollador antes de la publicación.

## [0.9.5] - 2026-08-04

### Agregado

- Se agregaron 23 ajustes preestablecidos de personajes inspirados en ascii.today de solo lectura, incluido Broadway.
KB, Computadora, Doom, Ghost, Modular, Estándar, Univers y Doh.
- Se agregó un catálogo de juego de caracteres delimitado compartido con metadatos de fuente/autor y
entradas del menú Conjunto de caracteres coincidentes para cada nuevo ajuste preestablecido.
- Se agregaron fuentes acreditadas y notas de adaptación en
`docs/ASCII_TODAY_PRESETS.md`.
- Se agregó entrada/salida experimental nativa multiplataforma MIDI a través de Rust
`midir`, con CoreMIDI como backend principal de macOS Apple Silicon y
Se conservan los backends Windows y Linux compatibles para CI y hardware futuro.
validación.
- Se agregó Evolution/M-Audio UC-33e a través de iConnectivity mioXC como el primero
perfil de hardware experimental. La entrada USB directa del UC-33e permanece fuera del alcance.
- Se agregaron cuatro páginas completas de 47 controles: Visual, Audio, Presets y Fine/User.
- Se agregó adquisición suave, fusión de entradas, curvas, soporte de inversión/rango, MIDI.
Aprenda anulaciones, monitoreo de puertos y reconexión automática de mioXC.
- Se agregaron ranuras preestablecidas MIDI estables del 1 al 128 con entrada numérica, Enter,
Acciones Anterior, Siguiente y Borrar.
- Se agregó un panel de escritorio MIDI con estado de entrada/salida, página activa, último mensaje
monitorear, restablecer mapeo, capturar perfil, instalar/restaurar y verificar acciones.
- Se agregó captura SysEx de banco completo limitada y restauración de ritmo a través de mioXC.
conexión DIN de retorno, además de un perfil opcional de garantía en la conexión.
- Se agregó una sonda física de descubrimiento/conexión mioXC y una impresora completa
mapa del controlador en `docs/MIDI_UC33E.md`.

### Cambió

- El glifo nativo Pop Out ahora consume la rampa de carácter compartido resuelta y
lo acepta sólo cuando es líder en el espacio, único, acotado y completamente cubierto
por el atlas de glifos agrupados fijos.
- La puesta en marcha del hardware MIDI se pausa explícitamente después de confirmar la
ID de controlador para el teclado C34–C43 y el transporte C44–C47. El software permanece
implementado; Se registra el trabajo restante de restauración física y aceptación.
en la Hoja de Ruta.
- MIDI está etiquetado como experimental en la interfaz de usuario y en la documentación porque la versión completa
barrido de control físico y lista de verificación de verificación/restauración SysEx de extremo a extremo
permanecen incompletos. Asegúrese de que Perfil al conectarse permanezca deshabilitado de forma predeterminada.
- Los controles de UI y MIDI ahora se dirigen a través de los mismos rangos de parámetros canónicos,
sujeción, manejo de cambios estructurales, configuración de audio y transición preestablecida
comportamiento.
- Los cambios preestablecidos visuales rearman la toma de control suave para que los controles UC-33e no motorizados
No se puede saltar el valor del software activo.
- MIDI está restringido intencionalmente a parámetros visuales, configuraciones audio-reactivas,
ajustes preestablecidos visuales y WTF mode. No puede cambiar fuentes, cámara, Pop Out o
pantallas de salida.

### Seguridad

- Los comandos MIDI y SysEx se otorgan únicamente a la ventana de control principal. el
La ventana de salida de solo presentación no recibe permisos MIDI.
- El adaptador nativo inicial acepta solo puertos cuyos nombres contengan `mioXC`.
- Colas MIDI, recuentos de paquetes SysEx, bytes decodificados, asignaciones almacenadas y ajustes preestablecidos.
las ranuras están limitadas y validadas.
- Los perfiles de controlador capturados permanecen locales y no contienen rutas de medios, marcos,
audio, credenciales o datos de red.

### Validación

- Comprobaciones matemáticas de renderizado ampliadas para cubrir las 23 nuevas entradas del catálogo, incluidas
identificaciones, límites, unicidad, glifos imprimibles, metadatos de atribución y Broadway
Búsqueda de luminancia de KB.
- Cobertura de humo estático extendida para requerir nombres ascii.today tanto en el
Control de conjunto de caracteres y panel de ajustes preestablecidos incorporado.
- Se agregó cobertura Rust para la aceptación y rechazo de la rampa de caracteres nativos.
- Se agregó `npm run test:midi` para los 188 enlaces de hardware predeterminados, valor
escalamiento, adquisición suave, márgenes de acción, fusión de eventos y exclusiones de alcance.
- Se agregaron pruebas Rust para análisis MIDI, ensamblaje SysEx fragmentado y transferencia.
validación y alcance de puerto exclusivo de mioXC.
- Se agregaron `npm run midi:probe` y `npm run midi:probe -- --connect` para físicos.
Puerto CoreMIDI y validación simultánea de entradas/salidas.
- Cobertura de humo estático extendida para validar el objetivo canónico visual/audio MIDI
enrutamiento y asegúrese de que el modo navegador mantenga oculto el panel MIDI solo de escritorio.
- Se ampliaron las comprobaciones de la política Tauri para requerir permisos MIDI en la ventana principal
y prohibirlos en la ventana de salida.

## [0.9.3] - 2026-06-26

### Agregado

- Se agregaron futuras herramientas de firma Windows a través de Azure Artifact Signing y
Tauri's Windows `signCommand`; la ruta de lanzamiento activa 0.9.3 Windows permanece
una vista previa sin firmar.
- Se agregó la herramienta de verificación Windows Authenticode para futuras versiones firmadas.
artefactos, incluidas comprobaciones de firmante y marca de tiempo.
- Se agregó `src-tauri/tauri.windows-signed.conf.json` para futuros Windows firmados.
Liberar el trabajo manteniendo la configuración predeterminada adecuada para el desarrollo local.
y la vista previa sin firmar 0.9.3 Windows.
- Se agregó un módulo reactivo de audio compartido para valores predeterminados, metadatos de control, ajustes preestablecidos,
presentan normalización, amortiguación de mezcla densa y modulación de parámetros de renderizado.
- Se agregaron controles audio-reactivos para cantidad de transitorio/flujo, cantidad de presencia,
amortiguación de densidad y piso de ruido.
- Se agregaron medidores de flujo y densidad, además de un ajuste preestablecido audio-reactivo de Dense Mix Control.
- Se agregaron canales de funciones de audio limitados para medios bajos, medios altos, presencia,
brillo y densidad en el navegador y en las rutas de audio nativas.

### Cambió

- Las versiones públicas de macOS ahora requieren la firma y certificación notarial del ID del desarrollador
en lugar de recurrir a firmas ad hoc.
- Los artefactos de la versión Windows 0.9.3 se publican como versiones preliminares sin firmar.
hasta SignPath Foundation, Azure Artifact Signing u otro backend de firma
está comprobado.
- La versión CI mantiene las credenciales de firma en el ámbito de los pasos de firma y brinda la
trabajo de publicación el único token GitHub con capacidad de escritura.
- La detección de latidos audiorreactivos es más conservadora durante la banda ancha densa.
pasajes preservando al mismo tiempo una fuerte respuesta para transitorios dispersos.
- La configuración de audio predeterminada de Pulse Reactor es más fuerte y menos amortiguada, por lo que
Las pistas modestas o densas aún producen movimiento visible sin cambiar los guardados.
ajustes preestablecidos del usuario.
- Los rangos de controles deslizantes reactivos al audio existentes se amplían, con navegador y
Abrazaderas nativas.
- La vista previa del navegador, Pop Out, las rutas de transmisión y la salida nativa ahora consumen lo mismo
reglas de modulación audio-reactiva compartidas.
- La cámara en vivo Pop Out mantiene la rápida ruta de cámara nativa para glifos, sólidos y
ajustes preestablecidos de píxeles; El transporte espejo del navegador permanece reservado para fuentes alternativas.
donde la captura nativa no está disponible.
- El Pop Out nativo ahora desactiva el enmascaramiento de glifos para los ajustes preestablecidos de estilo WebGL/WebGPU, por lo que
Los ajustes preestablecidos que no son Canvas2D mantienen la misma forma de celda sólida que la vista previa principal.
- Las transiciones estáticas de vídeo/cámara ahora pueden realizar un fundido cruzado entre GPU, sólido/píxel,
y renderizadores de glifos Canvas2D sin destruir la fuente de medios compartida.
- Los ajustes preestablecidos tradicionales de Canvas2D ASCII ahora utilizan de forma predeterminada la fluctuación de imagen estática visible
y migrar copias guardadas sin fluctuaciones de esas funciones integradas.
- WTF mode ahora permite que los anclajes ASCII/glifos usen su backend Canvas2D nuevamente, por lo que
las transiciones aleatorias de sólido a glifo son visibles en lugar de convertirse en GPU
variantes de celda sólida.

### Fijado

- Se corrigió un modo WTF `ReferenceError` cuando los ajustes preestablecidos de sólido/píxel sesgaban el siguiente
objetivo aleatorio hacia los ajustes preestablecidos de anclaje ASCII tradicionales.
- Se corrigieron los permisos de limpieza del detector de eventos Tauri para la ventana principal y se hicieron
nativo Pop Out limpieza de escucha cercana rechazo seguro, evitando
Informes de fallos de `event.unlisten not allowed`.

### Seguridad

- La firma futura Windows utiliza credenciales de firma de ámbito ambiental y no
no confirmar archivos de certificados, secretos de clientes ni material de firma privado.
- La reactividad de audio todavía envía solo vectores de características acotados a través de IPC; crudo
El audio, los fotogramas, los archivos multimedia y las rutas permanecen locales.
- Las comprobaciones de firma de lanzamiento y de firma de actualizador ahora tratan a macOS como público
distribución como un camino cerrado ante fallos. Los artefactos Windows 0.9.3 son explícitamente
vistas previas sin firmar.

### Validación

- Se agregó `npm run test:audio-reactive`.
- Se agregó `npm run check:windows-authenticode`.
- `npm run check:desktop` y `npm run check:release` ahora incluyen el
Pruebas auxiliares audiorreactivas.
- La cobertura de humo estático ahora afirma que los ajustes preestablecidos de la cámara en vivo no recurren a
Transporte espejo de forma predeterminada.
- La cobertura de humo estático ahora afirma que el enmascaramiento de glifos nativos sigue el activo
familia backend en lugar de filtrar la salida de glifos de estilo Canvas2D en los ajustes preestablecidos de GPU.
- La cobertura de humo estático ahora afirma que las transiciones de vídeo de sólido a glifo se mantienen
reproducción en vivo en lugar de pausar durante las reconstrucciones de la familia de renderizadores.
- La cobertura de humo estático ahora afirma que los objetivos WTF sólidos/píxeles pueden
sesgo determinista en anclajes ASCII sin lanzar.
- La cobertura de humo estático ahora afirma que los ajustes preestablecidos tradicionales Canvas2D ASCII
animar su fluctuación de imagen estática predeterminada y exponer el control de fluctuación.
- Las comprobaciones de políticas Tauri ahora requieren permiso de limpieza de eventos de la ventana principal mientras
manteniendo ese permiso fuera de la ventana de salida de solo presentación.

## [0.9.2] - 2026-06-25

### Agregado

- Se agregó un informe de fallas solo de producción para errores de interfaz, no controlados
rechazos, fallas de comando Tauri e informes de gancho de pánico Rust.
- Se agregaron preferencias de informes de fallos revisados/desinfectados: preguntar, enviar siempre y desactivar.
- Se agregó un relevo de choque Cloudflare Worker en `crash.dustwave.xyz` que limita la velocidad.
entrada, desinfecta cargas útiles, informes de huellas dactilares y crea o actualiza
Problemas agregados de GitHub a través de una aplicación GitHub.
- Se agregó una plantilla de informe de fallas GitHub y un flujo de trabajo de implementación de retransmisión de fallas.
- Se agregaron vectores matemáticos de renderizado compartido que cubren el legado y el procesamiento de color GPU.
Comportamiento del color del lienzo/transmisión.

### Cambió

- El envío del informe de fallos de Tauri ahora se ejecuta únicamente desde Rust; la vista web no se pone
capacidad HTTP arbitraria.
- La ventana de salida sigue siendo solo de presentación y no recibe ningún informe de fallas.
comandos.
- La agregación de retransmisión de fallos ahora agrupa por dimensiones de fallo estables, incluyendo
plataforma y campos de código de error explícitos cuando estén presentes, antes de recurrir a
pila normalizada o coincidencia de mensajes.
- El lienzo del navegador y las imágenes de la transmisión se conservan intencionalmente. El 0.9.2
El trabajo de consolidación extrae primero los ayudantes y pruebas compartidos en lugar de cambiarlos.
salida numérica.
- Los ayudantes de color/hash/juego de caracteres del renderizador ahora se encuentran en `renderers/shared/` para
reutilización por código de aplicación y pruebas.

### Seguridad

- Los informes de fallos se delimitan y desinfectan antes del almacenamiento o envío local.
Archivos multimedia, fotogramas, audio sin procesar, rutas completas, tokens, cookies y datos privados.
Los valores ambientales no están incluidos.
- El envío de informes de fallas en la red está deshabilitado para compilaciones que no son de producción o de depuración.
- Las credenciales GitHub residen únicamente en los secretos Cloudflare Worker; no hay token GitHub
integrado en la aplicación de escritorio.

### Validación

- Se agregaron `npm run test:render-math` y `npm run test:crash-relay`.
- `npm run check:desktop` y `npm run check:release` ahora incluyen crash Relay y
comprobaciones matemáticas del renderizador.

## [0.9.1] - 2026-06-24

### Agregado

- Se agregaron ajustes preestablecidos tradicionales de estilo ASCII:
  - Cámara clásica ASCII.
  - Papel periódico ANSI.
  - Terminal mono.
  - Máquina de escribir densa.
- Se agregó un conjunto de caracteres de cámara clásica inspirado en la pequeña rampa de luminancia utilizada.
por `idevelop/ascii-camera`.
- Se agregó representación de glifos nativos `wgpu` Pop Out para los ajustes preestablecidos de `glyphMode`:
  - La salida nativa ahora acepta `glyphMode` y `charset` del formato canónico.
parámetros del renderizador.
  - La salida nativa de GPU utiliza un atlas de glifos de mapa de bits fijo y una rampa de juego de caracteres.
  - La representación de prueba/respaldo del software nativo utiliza la misma lógica de rampa de glifos.
- Se agregó cobertura Rust para análisis de metadatos de glifos nativos, diseño uniforme de representación,
y salida de máscara de glifo.

### Cambió

- Los ajustes preestablecidos ASCII tradicionales seleccionan Canvas2D para la vista previa principal para que los glifos sean
visible inmediatamente en la imagen de demostración, el vídeo de demostración, los medios personalizados y la cámara
fuentes, mientras que el Pop Out nativo representa máscaras de glifos coincidentes.
- WTF mode ahora puede anclar objetivos aleatorios seguros en torno al tradicional
Preajustes ASCII, así como las familias de preajustes extremos.
- Los menús de selección de conjunto de caracteres y familia de fuentes ahora utilizan el diseño de selección compacto
utilizado por los controles de reactividad de audio.
- La salida nativa ahora conserva el estilo de texto/glifo para medios estáticos y sencillos.
fuentes de cámara en lugar de aplanar los ajustes preestablecidos de glifos en bloques de celdas sólidos.
- La cobertura de humo estático ahora afirma que el grupo Glifo/Célula permanece visible
y compacto mientras renderiza los nuevos ajustes preestablecidos ASCII tradicionales.
- Redacción de diagnóstico de medios reforzados para rutas locales integradas y limitadas
Tamaño del mensaje de diagnóstico.

## [0.9.0] - 2026-06-23

### Agregado

- Se cambió el nombre y se posicionó la aplicación como ASCII VJ Remix.
- Se cambió el nombre de la identidad del repositorio/paquete a `ascii-vj-remix` y se actualizó el
Referencias remotas/actualizadoras GitHub.
- Se agregó un shell de aplicación de escritorio Tauri v2 alrededor del laboratorio de renderizado.
- Se agregó una canalización de compilación Vite para que la misma interfaz básica pueda ejecutarse en un navegador.
o dentro de la aplicación de escritorio empaquetada.
- Se agregó un flujo de trabajo de fuente estática primero local:
  - Imagen de demostración como fuente de inicio predeterminada.
  - Vídeo de demostración como dispositivo de vídeo incorporado visible.
  - selección personalizada de archivos de imagen/vídeo local.
  - Soporte de selección de archivos MKV donde la ruta del decodificador activo puede manejarlo.
  - soporte de fuente de cámara.
  - selección multicámara y mezcla de cámara local Canvas2D.
- Se agregaron backends de renderizado de alta calidad:
  - WebGPU como ruta principal de GPU del navegador.
  - WebGL2 reserva.
  - Canvas2D y respaldos de Pixel Canvas.
- Se agregaron controles densos de renderizado en vivo para cuadrícula, filas, dimensiones de celda, color,
brillo, contraste, gamma, mezcla de fondo, cuantificación, inquietud, muestra
posición, suavizado, FPS, modo de glifo/celda y estado de rendimiento.
- Se agregaron ajustes preestablecidos visuales incorporados, incluido un conjunto más amplio de fluctuaciones extremas,
Aspectos de alto contraste, alta saturación, columnas bajas, gamma baja y gamma alta.
- Se agregaron flujos de trabajo preestablecidos para guardar, copiar, actualizar, eliminar, importar y exportar preestablecidos por el usuario.
- Se agregaron transiciones preestablecidas suaves con interpolación numérica y superficie de renderizado.
fundidos cruzados.
- Se agregó WTF mode para transiciones aleatorias continuas y seguras en vivo.
- Se agregó una superposición de estadísticas que muestra el ajuste preestablecido actual, la fuente, el backend, la cuadrícula, FPS,
tiempo de transición y estado de audio-reactividad.
- Se agregó renderizado audio-reactivo:
  - Fuente predeterminada de micrófono/entrada.
  - fuente del archivo de audio local.
  - navegador Mostrar audio donde el navegador proporciona pistas de audio.
  - rutas de captura de audio nativas Tauri para compilaciones de escritorio.
  - RMS, modulación de graves, medios, agudos, transitorios y basada en ritmos.
  - Abrazaderas seguras para evitar salidas de blanco puro o negro puro a alta sensibilidad.
- Se agregó salida nativa Tauri Pop Out:
  - ventana de salida separada para otra pantalla.
  - Presentador nativo `wgpu` para fuentes de vídeo/imagen respaldadas por archivos.
  - Ruta Metal en macOS.
  - Soporte de destino D3D12/Vulkan/GLES a través de `wgpu`.
  - ruta de captura nativa de una sola cámara macOS a través de AVFoundation para cámara baja
latencia en Pop Out.
  - selección de pantalla de salida y pruebas de simulación de pantalla secundaria.
- Se agregó selección de medios de escritorio solo local a través de un cuadro de diálogo Tauri y
registro de medios con ámbito de sesión.
- Se agregó una política de seguridad de contenido de producción y capacidades divididas de Tauri.
- Se agregó la infraestructura del actualizador de versiones GitHub.
- Se agregó la firma de aplicaciones macOS ad-hoc como alternativa local/de versión predeterminada.
- Se agregó una estructura opcional del flujo de trabajo de certificación notarial de ID de desarrollador para uso futuro.
- Se agregó la política de creación y preparación del sidecar FFmpeg para el trabajo del motor de medios independiente.
- Se agregaron segmentos del motor multimedia Rust para sondeo/decodificación FFmpeg, preparación de fotogramas y
Validación de codificación de flujo adaptativo.
- Se agregaron pruebas estáticas de humo del navegador, pruebas de visualización de resultados y manifiesto del actualizador.
pruebas, comprobaciones de política de recursos FFmpeg, comprobaciones de paridad de medios y pruebas Rust.
- Se agregaron documentos de práctica de proyectos para seguridad, rendimiento, pruebas,
accesibilidad e internacionalización.

### Cambió

- La interfaz de usuario de origen normal ahora expone fuentes locales estáticas en lugar de una fuente visible.
Selector estático/streaming.
- El panel Fuente ahora muestra Imagen de demostración, Video de demostración, Cámara y archivo personalizado.
entradas únicamente.
- Los controles de la cámara ahora aparecen directamente debajo de Fuente cuando la cámara está activa.
- La interfaz de usuario de solo transmisión, como el recuento de búfer y el estado de la conexión de transmisión en la parte superior derecha, es
oculto del uso normal de estática/cámara/archivo.
- Los ajustes preestablecidos y WTF mode ya no alternan la superposición de estadísticas a menos que el usuario cambie
esa configuración directamente.
- Las transiciones preestablecidas preservan la fuente de medios activa y el tiempo de reproducción de video cuando
la fuente no ha cambiado.
- La aplicación ahora está documentada como una herramienta creativa independiente y local en lugar de
que solo como una bifurcación del servidor de transmisión ASCILINE.
- El tema de la interfaz de usuario ahora utiliza superficies negras y grafito con detalles activos en blanco.
estados listos/encendidos de color azul neón y estados de advertencia/WTF/actualización de color rosa neón en lugar de
la paleta anterior con predominio del azul, conservando al mismo tiempo el control compacto
densidad y acentos de estatus de alto contraste.

### Desarrollo y lanzamiento

- Node.js 24 es el tiempo de ejecución básico de JavaScript.
- La versión CI se basa en macOS, Windows y Linux.
- Lanzamiento de compilaciones de CI revisadas FFmpeg/ffprobe sidecars del funcionario fijado
Fuente FFmpeg con protocolos de red deshabilitados.
- La clave privada del actualizador es intencionalmente externa y debe proporcionarse a través de
`TAURI_SIGNING_PRIVATE_KEY`.
- La clave del actualizador está protegida por contraseña; La automatización de lanzamientos ahora también requiere
`TAURI_SIGNING_PRIVATE_KEY_PASSWORD`.
- Las compilaciones locales de macOS pueden utilizar una identidad autofirmada estable para un mejor TCC
Reutilización de permisos durante el desarrollo.

### Limitaciones conocidas

- El modo Stream existe como infraestructura heredada/de desarrollo, pero está oculto de lo normal.
IU de origen hasta que el flujo de trabajo independiente esté completamente productivo.
- El control de hardware MIDI está planificado pero no se incluye en 0.9.0.
- La firma y la certificación notarial del ID de desarrollador de Apple se aplazan.
- El comportamiento de Linux WebGPU depende en gran medida de WebKitGTK, los controladores de Mesa/proveedor y
embalaje de distribución; WebGL2 puede ser el recurso práctico de Linux.
- La compatibilidad con MKV depende de la ruta del decodificador de plataforma activa.
- El comportamiento de captura de audio del sistema/pantalla varía según el sistema operativo y el navegador.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
