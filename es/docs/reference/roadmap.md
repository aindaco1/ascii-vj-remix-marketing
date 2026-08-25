---
title: Hoja de ruta
description: Documentación de hoja de ruta derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Referencia
lang: es
---

# Hoja de ruta

Esta hoja de ruta separa la línea base de características lanzadas 0.9.5, el trabajo activo 0.9.6,
y el trabajo de seguimiento planificado.
Su objetivo es guiar el producto, el renderizador, el empaquetado de escritorio y la contribución.
decisiones.

## Trabajo de lanzamiento activo: 0.9.6

### Rendimiento sin reducción de calidad

- Reutilice el almacenamiento uniforme, las vistas de texturas y los grupos de vinculación estables de WebGPU.
de recrearlos por fotograma.
- Almacenar en caché las ubicaciones uniformes de WebGL2 después de vincular el programa.
- Mantenga los marcos de transición numéricos en la ruta de actualización de valores/controles pequeños; correr
Actualizaciones de fuente, cámara, visibilidad, medidor y superficie de control completa únicamente
en el límite estatal final.
- Versión nativa de los marcos fuente Pop Out para actualizar la presentación y la visualización en vivo.
La modulación de parámetros no convierte repetidamente y carga un 24 FPS sin cambios.
fotograma de vídeo en 60 FPS.
- Preservar el código del sombreador, las matemáticas del renderizador, la resolución de fuente/salida, la calidad de los glifos,
y todos los controles de calidad visibles.
- Mantenga la medición de construcción optimizada repetible con valores predeterminados limpios y fijos
objetivos de transición no estructurales, métricas P10/P50, selección exacta de paquetes,
y contadores nativos de carga/salto.

### MIDI Se reanudó la puesta en servicio

- Mantenga MIDI etiquetado como experimental y mantenga desactivado Garantizar perfil en conexión
hasta que la restauración manual y la verificación byte por byte se realicen correctamente.
- Programe los atenuadores/rotativos como CC 1-33 correspondientes en el canal individual 00.
- Programe C34-C47 con modo extendido 146, coincidiendo con CC 34-47, presione 127,
liberación 0 y canal individual 00. El modo de botón CC estándar simple es un
alternar y no es aceptable.
- Almacenar la superficie común en las memorias 01-04 con los canales globales 1-4.
- Captura completa del banco, restauración explícita, recuperación, verificación, física
barrido, reconexión, control suave, ranuras numéricas y controles de acción prohibida en
macOS Manzana Silicio.
- Conserve la validación directa del USB UC-33e y física Windows/Linux como continuación
trabajo.

### macOS Protección de identidad de permisos

- Mantenga los lanzamientos públicos en `ASCII VJ Remix` / `com.asciline.remix` y normal
desarrollo en `ASCII VJ Remix Dev` / `com.asciline.remix.dev`.
- Requerir una identidad de firma local estable antes de lanzar un paquete de desarrollo
que solicitará acceso a la cámara, el micrófono o el audio del sistema.
- Evite que las herramientas locales copien o vuelvan a firmar la aplicación de producción.
- Requerir archivos de actualización públicos para conservar el ID del desarrollador ID del equipo `PWT3Q52LZ2`,
tiempo de ejecución reforzado y el mismo requisito designado basado en equipo en todo
lanzamientos.
- Ejecute un reemplazo del actualizador macOS basado en la aplicación después de la publicación y
revalidar la identidad de la aplicación resultante.

### Endurecimiento de instalación macOS DMG

- Tauri sigue siendo el único propietario de la creación de DMG, con su aplicación a aplicaciones
diseño explícito en la configuración comprometida.
- El contrato de imagen montada compartida verifica la integridad, el paquete de aplicación real,
`Applications -> /Applications` y revisó los metadatos de Tauri.
- Reutilice la identidad, la firma, el grapado, el Gatekeeper y el actualizador de la aplicación existente
verificaciones de archivo con la aplicación montada desde el DMG final notariado.
- El humo de liberación publicada requiere el DMG descargado antes de ejercer el
salto de actualización existente.
- Mantenga como opcionales EasyDMG y manipuladores cautelosos similares; no agregues un automatico
dependencia del instalador o del tiempo de ejecución.
- La aplicación local optimizada/canario DMG pasa la verificación del paquete montado compartido. un
La identificación del desarrollador firmada/notarizada por un canario de DMG sigue siendo necesaria antes de realizar la reclamación.
el trabajo de instalación de 0.9.6 está listo para su lanzamiento. Ver
[Plan de refuerzo de instalación macOS para 0.9.6](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MACOS_INSTALL_0.9.6_PLAN.md).

## Dirección de producto

ASCII VJ Remix es el primer laboratorio de renderizado local para ASCII en vivo y basado en células.
visuales. Combina:

- Línea de vídeo ASCII de alto rendimiento de ASCILINE: codificación de fotogramas adaptable,
Experimentos de Python/OpenCV, ideas de reproducción de terminales, rutas alternativas de Canvas y
preparación de medios orientada a la transmisión.
- El visual WebGPU/WebGL de alta calidad del renderizador `ascii-point-and-click`
salida y arquitectura de fuente de medios nativa del navegador.
- Un shell de escritorio Tauri que mantiene la aplicación independiente, fuera de línea de forma predeterminada y
utilizable para flujos de trabajo de salida en vivo.

El proyecto no adopta la interfaz de usuario del juego de apuntar y hacer clic. El objetivo es una densa
superficie de control creativo para video, imagen, cámara, audio-reactivo y
Imágenes ASCII basadas en MIDI.

## Línea base de características actuales: 0.9.5

### Aplicación de escritorio local con arnés Vite

- El mismo laboratorio de renderizado HTML/CSS/ESM básico se ejecuta dentro de Tauri, con un Vite.
Arnés estático retenido para desarrollo y pruebas de humo.
- Vite crea un paquete determinista `dist/`.
- Los recursos en tiempo de ejecución se copian localmente en el resultado de la compilación.
- Las compilaciones de escritorio empaquetadas están diseñadas para ejecutarse sin conectividad en línea.
- Las rutas de ejecución en línea intencionales se limitan al actualizador de versiones GitHub y
Envío de informes de fallos revisados/desinfectados solo para producción.

### Flujo de trabajo de origen

- La interfaz de usuario normal comienza en modo de fuente local estática.
- La imagen de demostración es la fuente de inicio predeterminada.
- El vídeo de demostración es la única fuente de vídeo integrada visible.
- Los dispositivos MP4 adicionales de apuntar y hacer clic siguen siendo activos ocultos de desarrollo/prueba.
- Los archivos de imagen/vídeo locales personalizados se pueden seleccionar a través del escritorio/vista web
ruta del selector de archivos.
- Los archivos personalizados Tauri se exponen a través de una concesión de protocolo de activos local de sesión,
no amplio acceso al sistema de archivos.
- La cámara es una fuente de primera clase.
- Se pueden seleccionar varios dispositivos de cámara cuando el sistema operativo y la vista web integrada lo permiten
captura concurrente.
- El mezclador de cámaras compone varias cámaras localmente con Canvas2D.
- Los controles de la cámara aparecen directamente debajo de Fuente mientras la cámara está activa.
- La URL de medios estáticos y los selectores manuales de tipo de medios están intencionalmente ausentes de
la interfaz de usuario normal. Se infiere el tipo de fuente.

### Estado de la transmisión

- El código de transmisión heredado de FastAPI/WebSocket permanece en el repositorio.
- El códec adaptativo RAW/ZLIB/DELTA sigue siendo parte del código base y de prueba
suite.
- Existe trabajo de sesión multimedia Rust/FFmpeg para futuros paquetes en modo de transmisión local.
- StreamRuntime puede consumir lotes de sesiones nativas en las rutas de desarrollo Tauri.
- El modo de transmisión aún no es un modo de fuente normal orientado al usuario.
- El selector Estático/Transmisión, el contador de búfer, la etiqueta de conexión de transmisión y
La superficie de control específica de la transmisión permanece oculta hasta que se produzca el modo de transmisión.
de extremo a extremo.

### Representación de backends

- WebGPU es el principal objetivo de calidad en tiempos de ejecución de Chromium/WebView capaces.
- WebGL2 es el principal recurso alternativo de GPU.
- Canvas2D glifo/texto y lienzo de píxeles siguen siendo opciones alternativas de compatibilidad.
- La selección automática de backend prefiere el mejor renderizador disponible y al mismo tiempo conserva un
Selector de backend manual.
- El renderizador utiliza un modelo de parámetro canónico único para controles de interfaz de usuario, ajustes preestablecidos,
aleatorización, modulación de audio y sincronización de salida.

### Controles de renderizado en vivo

El modelo de control actual incluye:

- Fuente: medios integrados, archivos personalizados, cámara, bucle, silencio, volumen.
- Cámara: selección múltiple de dispositivo, modo de orientación cuando sea relevante, tamaño de captura, captura
FPS, maquetación, marcos, espejo.
- Backend: Automático, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- Cuadrícula: columnas, filas, filas automáticas, ancho de celda, alto de celda, corrección de aspecto.
- Color: saturación, contraste, brillo, gamma, combinación de fondo,
cuantización, modo de color de transmisión cuando sea relevante.
- Muestreo: objetivo FPS, cantidad de jitter, velocidad de jitter, muestra X/Y, suavizado.
- Glifo/Celda: modo glifo, modo sólido, juego de caracteres compacto y familia de fuentes
menús, intensidad mínima de glifos.
- Rendimiento: superposición de estadísticas, estado del backend, FPS, tamaño de cuadrícula.
- Reactividad de audio: fuente, preajuste, dispositivo de entrada, sensibilidad, suavizado, ritmo,
graves, medios, agudos, transitorios/flujo, presencia, amortiguación de densidad, ruido de fondo,
y metros en vivo.
- Salida: Pop Out, selector de visualización de salida, ventana de salida con capacidad de pantalla completa.

Los controles están ocultos condicionalmente cuando no son relevantes para el activo
fuente/backend.

### Tema de la interfaz de usuario

- La interfaz de usuario utiliza una paleta extrema de negro, blanco y gris con rosa neón y azul neón.
acentos estatales en lugar de las anteriores superficies azules saturadas.
- Diseño de control denso, tamaño de panel compacto y monoespacio estilo VCR
Se conserva la tipografía.
- Los niveles del panel de grafito separan el shell de la aplicación, la barra de herramientas, el inspector, los grupos y
filas sin reducir la legibilidad.
- El blanco es el principal acento activo/enfoque y reemplaza la luz anterior.
superficies azules/púrpuras.
- El azul neón está reservado para los estados listo/encendido.
- El rosa neón está reservado para estados de advertencia, actualización y WTF.
- El rojo permanece reservado para estados de error.
- El color del tema está centralizado a través de tokens CSS, por lo que los cambios futuros en la paleta lo harán
no requiere ediciones codificadas dispersas.

### Presets y transiciones

- Los ajustes preestablecidos integrados son de solo lectura.
- Los usuarios pueden guardar, duplicar, actualizar, eliminar, importar y exportar ajustes preestablecidos.
- El panel preestablecido se mantiene compacto y al mismo tiempo admite un gran conjunto de preajustes.
- Las transiciones utilizan la duración configurada en segundos.
- Interpolación de parámetros numéricos sin problemas.
- Los parámetros discretos se invierten en puntos controlados cuando es necesario.
- Las reconstrucciones del renderizador utilizan fundidos cruzados de dos superficies en lugar de fundidos a negro.
- Las transiciones conservan la fuente multimedia y el tiempo de reproducción de vídeo cuando la fuente está
sin cambios.
- Las funciones integradas actuales incluyen:
  - Apuntar y hacer clic predeterminado.
  - Cámara clásica ASCII.
  - Papel periódico ANSI.
  - Terminal mono.
  - Máquina de escribir densa.
  - Veintitrés adaptaciones de personajes de ascii.today acreditadas, de Broadway
KB a Doh; ver
[ascii.today Ajustes preestablecidos de caracteres](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ASCII_TODAY_PRESETS.md).
  - Martillo de neón.
  - Lluvia arcade.
  - Sumidero Gamma.
  - Herida cromada.
  - Fragmentador de caramelos.
  - Sueño posterizado.
  - Confeti del canal muerto.
  - Guillotina solar.
  - Trituradora de papel.
  - Disturbios ciberdélicos.
  - Terminal de visión nocturna.
  - Decodificador candente.
  - Tormenta de nieve ácida.
  - Espejismo de píxeles.
  - Fusión cromática.
  - Aplastamiento de luz negra.
  - Pérdida de señal.
  - Voltaje del azúcar.
  - Reactor de teletexto.
  - Quemaduras de sol por Bitcrush.
  - Ditherpunk Ultra.
  - Colapso de terminales.
  - Disturbios infrarrojos.
  - Podredumbre por láser.
  - Catedral estática.
  - Semitono tóxico.
  - Moretón por plasma.
  - Telemetría de magma.
  - Orquídea falla.
  - Sirena ultravioleta.
  - Tormenta de neón.

### Modo WTF

- WTF mode alterna transiciones aleatorias continuas.
- Utiliza duraciones de transición aleatorias.
- Se apoya en familias preestablecidas extremas, anclajes preestablecidos ASCII tradicionales y
controles aleatorios de vida segura.
- Evita estados de salida en blanco y negro puro.
- No desactiva la superposición de estadísticas.
- El cambio de fuente se cancela y se reanuda de forma segura sin dejar el renderizador atascado
en la fuente anterior.

### Representación audiorreactiva

- La reactividad de audio está habilitada de forma predeterminada.
- Mic/Input es la fuente de audio predeterminada.
- Se pueden seleccionar dispositivos de audio concretos.
- Al cambiar los dispositivos de entrada de audio, se reinicia la captura automáticamente.
- La reactividad de archivos de audio funciona localmente.
- El audio de visualización/pestaña del navegador funciona cuando la plataforma proporciona pistas de audio.
- Las compilaciones de escritorio Tauri incluyen proveedores de captura de audio nativos para escritorio
pruebas.
- Extractos de análisis RMS, graves, medios-graves, medios, medios-altos, agudos, presencia,
brillo, densidad, flujo espectral, pulso de latido y reloj de fase.
- Los controles de mezcla densa reducen la reacción exagerada de la banda ancha en canciones ocupadas mientras mantienen
transitorios escasos que responden.
- La modulación se aplica como parámetros efectivos y no persiste en
ajustes preestablecidos guardados.
- Las abrazaderas seguras evitan que la alta sensibilidad cause negro puro o blanco puro.
pantallas.
- Stats Overlay informa el estado/preajuste audio-reactivo activo.

### Salida nativa y Pop Out

- La interfaz de usuario principal sigue siendo la superficie de control.
- Pop Out abre una ventana de salida separada.
- Las compilaciones de escritorio Tauri prefieren una superficie de salida nativa `wgpu`.
- macOS utiliza Metal.
- Windows apunta a D3D12 a `wgpu`.
- Linux apunta a Vulkan/GLES hasta `wgpu`.
- Las imágenes estáticas, SVG, archivos de vídeo y fuentes de una sola cámara pueden utilizar archivos nativos.
rutas de salida.
- Los ajustes preestablecidos del modo de glifo tradicional conservan sus máscaras de conjunto de caracteres en formato nativo.
Salida `wgpu`.
- La salida de glifos nativos utiliza recursos de rampa/atlas fijos acotados en lugar de
cargar fuentes seleccionadas por el usuario en la ruta nativa.
- macOS de una sola cámara Pop Out utiliza una ruta de captura nativa AVFoundation para reducir
latencia de la cámara.
- Las fallas de salida nativa retienen una reserva de vista web/lienzo.
- La selección de visualización de salida persiste cuando la enumeración de monitores está disponible.
- La ubicación de la pantalla secundaria está cubierta por pruebas de simulación deterministas.

### Control de hardware nativo experimental MIDI (0.9.5)

- El equipo experimental inicial es un Evolution/M-Audio UC-33e conectado por DIN
en ambas direcciones a través de un iConnectivity mioXC.
- Rust `midir` proporciona entrada/salida nativa con CoreMIDI como principal probado
backend y backends Windows/Linux retenidos para su validación.
- Cuatro memorias UC proporcionan páginas visuales, de audio, preestablecidas y finas/de usuario.
- Los 47 controles asignables tienen asignaciones predeterminadas en cada página.
- Adquisición suave, fusión, aprendizaje MIDI, espacios preestablecidos estables y reconexión
Se implementan monitoreos.
- SysEx de banco completo se puede capturar, restaurar explícitamente y verificar. Opcional
Asegúrese de que Perfil al conectarse esté desactivado de forma predeterminada.
- MIDI no puede cambiar las fuentes de medios, la cámara, Pop Out ni las pantallas de salida.
- El mapa completo del controlador y el procedimiento de hardware se encuentran en
[MIDI_UC33E](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

#### Estado de puesta en servicio del hardware: reanudando en 0.9.6

MIDI sigue siendo experimental en el estado implementado y de aprobación de pruebas automatizadas. la sesion fisica
confirmó que este UC-33e identifica el teclado numérico como C34–C43 y el
Botones de transporte Detener, Reproducir, Rebobinar y Avanzar rápido como C44–C47. esas identificaciones
son ahora el mapeo canónico.

Lista de verificación del currículum:

1. Programa C34–C47 con botón extendido UC-33e modo 146 como control momentáneo
Cambiar mensajes cuyo número CC coincida con la identificación del controlador, con liberación
valor 0 y presione el valor 127.
2. Almacene las memorias UC 01–04 con los canales globales MIDI 1–4 y el documentado
Mapas visuales, de audio, preestablecidos y finos/de usuario.
3. Capture un volcado SysEx de banco completo verificado desde el dispositivo bidireccional
equipo UC-33e/mioXC conectado.
4. Ejercite Instalar/Restaurar y Verificar con ese perfil capturado.
5. Habilite y valide el perfil opcional Garantizar al conectarse solo después del manual
la restauración tiene éxito.
6. Complete el barrido de control físico, la prueba de reconexión, la prueba de toma de control suave y
verificación de aceptación de acciones prohibidas en macOS Apple Silicon.
7. Realice la validación física de Windows y Linux más tarde; estancias USB directas UC-33e
diferido.

Durante la puesta en servicio no está previsto ningún nuevo alcance MIDI; las fallas deben corregirse
dentro del límite de seguridad visual/audio existente.

### Embalaje y seguridad de escritorio

- Tauri v2 es el shell del escritorio.
- El CSP de producción bloquea el acceso remoto arbitrario al tiempo de ejecución HTTP(S).
- El alcance del protocolo de activos está vacío de forma predeterminada y se expande solo para la sesión local
medios seleccionados.
- Las capacidades se dividen entre las ventanas principal y de salida.
- La ventana principal puede seleccionar medios, administrar la salida, usar proveedores de audio e invocar
acciones del actualizador.
- La ventana de salida tiene permisos mínimos de escucha/cierre/pantalla completa.
- Las cadenas de uso de cámara, micrófono, captura de pantalla y captura de audio macOS están
presente.
- Las compilaciones de desarrollo normales de macOS utilizan una identidad de paquete `.dev` separada y el
El iniciador local requiere una firma estable. La CI de lanzamiento público requiere desarrollador
Firma de DNI y certificación notarial bajo la identidad de producción.
- La versión Windows 0.9.3 CI publica artefactos de vista previa sin firmar. Firmado Windows
la distribución pública se difiere hasta SignPath Foundation, Azure Artifact
Se prueba la firma u otro backend de firma.
- GitHub La infraestructura del actualizador de versiones está configurada.
- La versión CI crea artefactos de actualización firmados cuando la clave privada está presente.
- Los informes de fallos de producción capturan la interfaz desinfectada limitada, el comando Tauri,
y Rust informes de pánico y los envía a través de un relé Cloudflare Worker a
problemas agregados de GitHub cuando está habilitado.

### Trabajo de FFmpeg y Media Engine

- Los módulos del motor de medios Rust pueden sondear y decodificar vídeo local a través de FFmpeg.
- La preparación de fotogramas puede producir búferes de píxeles y colores ASCII compatibles con ASCILINE.
- Se prueba la paridad de codificación/decodificación del códec adaptativo.
- Los sidecars FFmpeg se presentan con la versión, SHA-256, licencia, fuente y AVISO.
metadatos.
- Lanzamiento de compilaciones de origen de CI fijadas con sidecars FFmpeg 8.1.2 con protocolos de red
configuración deshabilitada y compatible con LGPL.
- El modo de transmisión empaquetado aún no se ha promocionado entre los usuarios normales.

### Validación

Los controles actuales incluyen:

- `npm run smoke:static`.
- `npm run check:offline`.
- `npm run check:desktop`.
- `npm run check:release`.
- `npm run test:output-display`.
- `npm run test:updater-manifest`.
- `npm run test:frame-prep`.
- `npm run test:decode-resize`.
- `npm run check:media`.
- `npm run test:rust`.
- `npm run test:vectors`.
- `npm run test:render-math`.
- `npm run test:crash-relay`.
- Análisis de registros de salida nativos y ayudas de humo de rendimiento.

La matriz de validación mantenida se encuentra en [Testing](/es/docs/operations/testing/). renderizador y
Las expectativas de rendimiento de salida se encuentran en [Performance](/es/docs/operations/performance/), y el
El modelo de seguridad en tiempo de ejecución reside en [Security](/es/docs/operations/security/).

## Funciones futuras

### MIDI Trabajo de seguimiento

La base nativa MIDI y el perfil UC-33e/mioXC se enviaron como experimentales en
0.9.5 y la puesta en servicio continúa en 0.9.6. Trabajo de seguimiento después de eso:

- Compatibilidad directa con USB UC-33e después de que la ruta DIN/mioXC sea estable.
- Validación física de Windows y Linux más allá de compilaciones de CI y pruebas de eventos falsos.
- Importación/exportación de perfiles de mapeo más allá de las anulaciones de aprendizaje MIDI persistentes localmente.
- Perfiles de controlador adicionales.
- Controles opcionales de suavizado de banda muerta y por enlace en la interfaz de usuario de mapeo.
- Construcción/edición automática de SysEx propietario UC-33e sin primero
capturando un volcado de hardware de banco completo verificado.

Regla de regresión: MIDI debe seguir usando las mismas rutas de control en vivo que la interfaz de usuario y
no debe obtener acciones de fuente, cámara, Pop Out o visualización de salida sin una nueva
Decisión de producto y revisión de seguridad.

### Modo de transmisión productizado

Promocione el modo de transmisión solo cuando sea coherente para los usuarios normales.

Alcance:

- Decida si la ruta de transmisión normal es Rust/FFmpeg, un sidecar incluido, un
conector de servidor externo o una combinación de ellos.
- Mantenga Python/FastAPI como ruta de desarrollo/referencia a menos que esté explícitamente
empaquetado.
- Agregue un flujo de trabajo de origen de Stream claro sin contaminar el panel de origen predeterminado.
- Restaure las métricas específicas de la transmisión solo cuando sea útil: búfer, ancho de banda por cable/sin procesar,
modo códec, latencia de transmisión, estado de reinicio.
- Conserve la salida nativa y el comportamiento de transición preestablecido en el modo de transmisión.
- Verifique el comportamiento del mensaje de control de WebSocket para parámetros suaves y de reinicio.
- Agregue pruebas de humo de flujo de extremo a extremo con medios representativos.

### Mejoras de audio del sistema nativo

Mejore la captura de audio del sistema de escritorio manteniendo las funciones de audio locales.

Alcance:

- macOS: migrar desde el respaldo de audio del sistema ScreenCaptureKit hacia Core Audio
Toca para que la aplicación pueda solicitar un permiso de grabación de audio del sistema más limitado donde
posible.
- Windows: agrega bucle invertido WASAPI.
- Linux: agregue proveedores PipeWire/PulseAudio.
- Mantenga los marcos de entidades delimitados. No transmita muestras de audio sin procesar ilimitadas
Tauri IPC.
- Conserve el comportamiento del micrófono/entrada de Web Audio como alternativa compatible con el navegador.

### Tuberías de textura de cámara directa

Continúe reduciendo la latencia de la cámara y la sobrecarga de copia.

Alcance:

- macOS: AVFoundation/CVPixelBuffer para compartir texturas Metal.
- Windows: Media Foundation para compartir texturas D3D.
- Linux: Interoperabilidad de PipeWire/V4L2 a Vulkan/GLES donde sea realista.
- Mezcla nativa multicámara sin forzar todas las rutas a través del lienzo WebView
relectura.
- Mantenga la semántica del cuadro más reciente para presentaciones en vivo en lugar de almacenar en búfer los antiguos
marcos de cámara.

### Consolidación del motor de renderizado

Reduzca el comportamiento duplicado de sombreadores/matemáticos en el navegador GPU, Canvas, streaming y
rutas de salida nativas.

0.9.2 estado:

- Los ayudantes matemáticos de renderizado JavaScript compartidos y los accesorios vectoriales existen en
`renderers/shared/`.
- Los vectores de procesamiento de color GPU son consumidos por los nativos JavaScript y Rust.
pruebas de salida.
- Los asistentes de color de lienzo y flujo mantienen intencionalmente nombres heredados y
preservación del comportamiento. La unificación numérica total es todavía un trabajo futuro.

Alcance:

- Defina un esquema de parámetros de renderizado compartido por UI, ajustes preestablecidos, audio, WTF, MIDI,
renderizadores de navegador, renderizadores de secuencias y salida nativa.
- Mantenga el procesamiento del color numéricamente consistente en WebGPU, WebGL2, Canvas,
y nativo `wgpu`.
- Agregue pruebas visuales limitadas o de salida dorada para ajustes preestablecidos representativos.
- Haga que las reservas de backend sean visibles y diagnosticables.
- Continuar preservando la calidad visual de WebGPU/WebGL mientras se mejora la salida nativa
latencia.

### Gestión de perfiles y ajustes preestablecidos

Amplíe los flujos de trabajo preestablecidos orientados al usuario.

Alcance:

- Cambie el nombre de los ajustes preestablecidos del usuario.
- Selección de preajustes de inicio.
- Carpetas/etiquetas preestablecidas.
- Búsqueda/filtro preestablecido.
- Separe los paquetes preestablecidos de las asignaciones MIDI.
- Validación de importación con errores legibles.
- Exporte paquetes que contengan ajustes preestablecidos visuales, configuraciones reactivas de audio y futuros.
Perfiles MIDI sin incluir rutas de medios privados.

### Liberación de endurecimiento

Pase de paquetes locales/autofirmados a una ruta de distribución pública más fluida.

0.9.3 estado:

- El CI de lanzamiento público macOS requiere credenciales de firma/ notarización de ID de desarrollador
y verifica el diseño del código, el tiempo de ejecución reforzado, la aceptación del Gatekeeper de DMG/aplicación y
Estado de notarización antes de su publicación.
- Windows 0.9.3 versión CI publica artefactos de vista previa sin firmar en lugar de
bloqueo de la firma de artefactos de Azure de pago.
- El desarrollo local mantiene un ad-hoc explícitamente aceptado y disponible con permiso
respaldo; Las pruebas de permisos normales requieren una firma estable.
- Los comandos locales normales aíslan la identidad del paquete/producto de desarrollo, desactivan el
actualizador de producción y requiere una firma estable antes de probar el permiso.
- Las puertas de liberación macOS verifican la identificación exacta del equipo de producción y la designación.
requisito tanto en la aplicación como en el archivo de actualización extraído.
- El CI de versión publicada realiza un reemplazo real del actualizador macOS desde el
liberación elegible anterior y revalida la identidad resultante.
- El comportamiento de instalación real de la máquina limpia Windows sigue siendo una verificación de versión manual para
vista previa de los artefactos y un punto de validación requerido una vez que se realiza la firma Windows
habilitado.

Alcance:

- macOS Firma y notarización de ID de desarrollador:
  - inscribirse y mantener las credenciales del Programa de Desarrolladores de Apple para la firma de lanzamientos.
  - almacene el certificado de identificación del desarrollador y las credenciales de notarización como GitHub
Secretos de acciones.
  - cree artefactos de lanzamiento macOS con el tiempo de ejecución reforzado habilitado.
  - envíe paquetes de aplicaciones macOS o DMG a la certificación notarial de Apple durante el lanzamiento de CI.
  - boletos de notarización básicos para los artefactos enviados.
  - validar artefactos finales con `codesign --verify`, inspección de derechos,
`spctl -a -vv` y una primera prueba de humo abierta en una máquina macOS limpia.
  - mantenga la firma ad-hoc solo como un desarrollo explícito que requiere permiso
respaldo.
- Windows Mitigación de pantalla inteligente:
  - firmar instaladores y ejecutables Windows con una firma de código Authenticode
certificado.
  - Prefiera la firma de código EV si el volumen de distribución o la fricción del usuario lo justifican.
el costo y la complejidad del flujo de trabajo de token/CI.
  - agregue marcas de tiempo para que las firmas sigan siendo válidas después de la expiración del certificado.
  - conservar el nombre del editor, el nombre de la aplicación, los metadatos del instalador y los metadatos de la versión
estable en todas las versiones para construir reputación.
  - publicar artefactos de lanzamiento de manera consistente a través de lanzamientos GitHub y el
Actualizador Tauri.
  - documentar el comportamiento esperado de SmartScreen en la primera instalación mientras se mantiene la reputación.
edificio.
  - Comportamiento de instalación/apertura/actualización de prueba de humo en máquinas limpias Windows, no solo
corredores de CI alojados.
- Futura vía de distribución de licencias SignPath Foundation/OSI:
  - trate a SignPath Foundation como el Windows preferido sin costos recurrentes
ruta de firma si el proyecto puede satisfacer sus políticas, código abierto y
requisitos de construcción reproducible.
  - no cambie la licencia del proyecto a MIT simple hasta que se derive ASCILINE
La fuente ha sido re-licenciada con permiso ascendente o reemplazada por
Implementaciones de salas limpias que preservan el comportamiento.
  - primero congele el comportamiento actual con cobertura de regresión para el inicio,
medios estáticos, cámara, salida de lienzo Canvas2D/píxel, vectores audio-reactivos,
salida nativa, compatibilidad de transmisión cuando se retenga, activos de actualización y
liberar flujos de humo.
  - reescribir archivos heredados de superficie del producto a partir de comportamientos/especificaciones documentados
en lugar de refactorizar la implementación copiada en su lugar.
  - eliminar o eliminar claramente el alcance de los archivos Python/streaming heredados del público
elegibilidad de liberación si permanecen bajo la licencia upstream actual.
  - publicar una política de firma de código que cubra la autoridad de publicación y la firma SignPath
flujo, trazabilidad de fuente/liberación, identidades de mantenedor y vulnerabilidad
divulgación.
  - actualice la documentación de privacidad para los informes de fallos de producción antes de enviarlos
una aplicación de SignPath Foundation.
  - reestructurar el CI de lanzamiento de Windows para que los artefactos firmados por SignPath y Tauri
Los archivos del actualizador `.sig` se generan en el orden correcto, luego verifique
Firmas de autenticado y firmas de actualizador antes de la publicación.
  - mantenga Azure Artifact Signing o los artefactos de vista previa Windows sin firmar como
respaldo hasta que se demuestre la aceptación de SignPath y la liberación de CI.
- Pruebas de humo del instalador Windows en máquinas reales más allá de CI.
- Linux Validación de AppImage/deb en distribuciones comunes.
- Confirmación manual con máquina limpia de que las subvenciones de TCC permanecen presentes en todo el país.
salto de actualización automatizado y con identidad estable.
- Se corrigió la estrategia de tiempo de ejecución de WebView2 si la aplicación Windows debe instalarse sin
requisitos previos en línea.

### Arnés de rendimiento

Cree pruebas de rendimiento repetibles para regresiones de renderizado y salida.

Alcance:

- Pruebas de compilación optimizadas solo para afirmaciones de rendimiento de la ventana de salida.
- La ventana principal FPS y la ventana de salida FPS se miden por separado.
- Pruebas de latencia de cámara con fotogramas sintéticos o con marca de tiempo.
- Comprobaciones de suavidad de transición preestablecidas.
- Comprobaciones del tiempo de respuesta de la audiorreactividad.
- Registros de salida nativos con contadores para fotogramas adquiridos, fotogramas presentados, parámetros
versión, versión fuente y ritmo de visualización.

### Documentación y ejemplos

Convierta los documentos del repositorio en un conjunto de documentación mantenida.

Alcance:

- Mantenga el archivo README centrado en el usuario.
- Mantenga examinados los documentos de los contribuyentes.
- Mantenga los documentos del motor de renderizado alineados con los cambios de código.
- Mantenga [Seguridad](/es/docs/operations/security/), [Rendimiento](/es/docs/operations/performance/),
[Pruebas](/es/docs/operations/testing/), [Accesibilidad](/es/docs/operations/accessibility/) y
[Internacionalización](/es/docs/operations/internationalization/) alineada con la arquitectura nativa de escritorio.
- Agregue capturas de pantalla del tema negro de la interfaz de usuario para la configuración normal del usuario, Pop Out y
flujos de trabajo de permisos.
- Agregue guías de configuración de hardware para cámaras, interfaces de audio, proyectores y el
Equipo UC-33e/mioXC.
- Agregue una matriz de solución de problemas para permisos, reserva GPU y ventana de salida
problemas.
- Agregue comprobaciones de accesibilidad automatizadas para el comportamiento del teclado/enfoque/ARIA.
- Agregue un catálogo i18n incluido solo cuando exista un flujo de trabajo de localización real.

## Riesgos abiertos

- La compatibilidad con WebGPU varía según los navegadores y las vistas web de Tauri.
- El soporte de Linux WebGPU puede permanecer inconsistente por un tiempo.
- La captura multicámara depende del sistema operativo, el firmware de la cámara, la topología USB y el navegador.
comportamiento.
- Las indicaciones de privacidad de macOS siguen siendo sensibles al identificador del paquete y a la firma
identidad; El aislamiento de producción/desarrollo evita que las compilaciones locales normales
contaminando las subvenciones públicas.
- La licencia FFmpeg debe seguir siendo una puerta de liberación explícita.
- La decodificación de medios nativos y la interoperabilidad de GPU difieren significativamente según la plataforma.
- Los eventos MIDI de alta tasa aún pueden causar abandono del renderizador cuando los usuarios asignan muchos
controles estructurales simultáneamente; Los eventos continuos se fusionan y
Los cambios estructurales siguen teniendo un ritmo limitado.
- La transmisión no debe volver a la interfaz de usuario normal hasta que sea lo suficientemente confiable para
usuarios no desarrolladores.

## Definición de Listo para 1.0

- La aplicación se instala limpiamente en macOS, Windows y Linux.
- La aplicación de escritorio funciona sin conexión, excepto para comprobaciones de actualización deliberadas.
- La imagen de demostración, el vídeo de demostración, los archivos personalizados y la cámara funcionan desde el primer inicio.
- Pop Out tiene rendimiento y es estable en las principales plataformas compatibles.
- Los ajustes preestablecidos, WTF, reactividad de audio y controles en vivo no reinician los medios a menos que
el usuario cambia de fuente o es inevitable una reconstrucción estructural.
- El modo de transmisión está desarrollado o claramente ausente en la interfaz de usuario del usuario normal.
- La compatibilidad con el controlador MIDI permanece estable en el equipo UC-33e/mioXC documentado.
- Los artefactos de la versión macOS están firmados con el ID del desarrollador, notariados, grapados y
Validado por Gatekeeper para distribución pública, o el lanzamiento es explícitamente
marcado como una compilación local/de prueba.
- Los artefactos de la versión Windows se marcan explícitamente como vistas previas sin firmar o
están firmados con Authenticode, tienen marca de tiempo y se prueban con respecto al comportamiento de SmartScreen
en máquinas limpias, con las advertencias restantes de la primera instalación documentadas.
- Los documentos del motor de renderizado, los documentos de los colaboradores y el registro de cambios coinciden con la versión.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/ROADMAP.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ROADMAP.md)
