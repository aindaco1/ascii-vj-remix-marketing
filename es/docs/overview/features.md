---
title: Conjunto de funciones
description: Documentación del conjunto de funciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Resumen
lang: es
---

<a id="feature-set"></a>

# Conjunto de funciones

Esta página describe la línea base de funciones ASCII VJ Remix actual para desarrolladores que planean bifurcaciones, puertos, integraciones o trabajo de funciones. El mapa de capacidades se genera a partir de la Guía del usuario del repositorio principal.

<a id="current-capabilities"></a>

## Capacidades actuales

<a id="sources"></a>

### Fuentes

- Imagen de demostración incorporada, utilizada como fuente de inicio predeterminada.
- H.264/MP4 Demo Video integrado en macOS y Windows, con un recurso VP8/WebM coincidente seleccionado en instalaciones limpias de Linux.
- Archivos de imagen y vídeo locales seleccionados por el usuario.
- Soporte de selección MKV en el selector de archivos del escritorio. Si la vista web de la plataforma no puede decodificar la demostración integrada o un video seleccionado, la aplicación de escritorio lo vuelve a intentar a través de la ruta FFmpeg incluida.
- Entrada de cámara web/cámara local.
- Múltiples cámaras simultáneas cuando el sistema operativo y el tiempo de ejecución del escritorio lo permitan.
- Diseños del mezclador de cámaras: cuadrícula, fila dividida, pila e imagen en imagen.
- Los controles de la cámara aparecen directamente debajo del panel Fuente mientras la Cámara está activa.
- Los medios estáticos y los fotogramas de las cámaras permanecen locales. No se suben a un servidor.

<a id="rendering"></a>

### Representación

- El renderizador WebGPU es el principal objetivo de calidad en tiempos de ejecución de escritorio compatibles.
- El renderizador WebGL2 es el principal respaldo integrado de GPU.
- Las rutas Canvas2D y Pixel Canvas siguen siendo alternativas de compatibilidad.
- Las vistas de escritorio empaquetadas prueban WebGPU para cada ajuste preestablecido elegible para aceleración, luego WebGL2 y Canvas2D como alternativas limitadas. Los ajustes preestablecidos con un backend de compatibilidad explícita conservan Canvas2D en todas las plataformas.
- La ventana de salida nativa Tauri utiliza un presentador `wgpu` cuando esté disponible:
  - Metal en macOS.
  - D3D12 en Windows.
  - Vulkan/GLES en Linux.
- El Pop Out nativo conserva los parámetros del modo glifo y del conjunto de caracteres para los ajustes preestablecidos ASCII tradicionales en lugar de aplanarlos en celdas sólidas.
- Veintiuna paletas del proyecto, el mapeo por color más cercano o luminancia y el dithering ordenado Bayer 2x2/4x4/8x8 comparten los mismos parámetros y tablas de consulta entre los renderizadores del navegador, Canvas y la salida nativa.
- Los controles de glifo cubren profundidad, desplazamiento, inversión, color de origen/fijo, fondo, Braille, bloques de dibujo/símbolos comunes, latín extendido, griego, cirílico, marcas CJK, Hiragana, Katakana, CJK unificado U+4E00-U+9FFF, Hangul y rampas personalizadas de hasta 96 escalares Unicode compatibles.
- El atlas neutral Unicode se genera y verifica fuera de línea, se incluye localmente y se carga en páginas delimitadas de 1024 px solo cuando los glifos seleccionados las necesitan.
- La densidad normal está protegida por el rendimiento mediante límites de columnas compartidas y de celdas totales. La preferencia global Advanced Density expone hasta 900 columnas sin una garantía de 30 FPS y nunca se almacena en ajustes preestablecidos visuales.
- El renderizador omite cargas duplicadas de fotogramas de origen nativos, reutiliza recursos GPU estables y limita el trabajo de la interfaz de usuario en tiempo de transición sin cambiar las configuraciones matemáticas o de calidad del renderizador.
- El renderizador expone controles en vivo para cuadrícula, tamaño de celda, color, gamma, brillo, contraste, saturación, combinación de fondo, cuantificación, fluctuación, posición de muestra, suavizado, FPS, comportamiento de glifo/celda y estado de rendimiento.
- **Color → Bright output** empieza desactivado. Actívelo para iluminar tomas oscuras; se conserva cualquier elección guardada. Eleva los colores oscuros antes de seleccionar los glifos, de modo que las cámaras, imágenes y videos con poca luz producen colores más brillantes y glifos más densos. La elección se conserva al reiniciar, cambiar de preset, reproducir listas o usar WTF. Déjelo desactivado para mantener la respuesta de color original; los controles Brightness y Gamma siguen funcionando. El negro puro permanece negro. Con una paleta, se iluminan los colores resultantes sin alterar su tabla de búsqueda ni los rangos de los ciclos de color; los glifos de color fijo mantienen el color elegido.
- La superposición de estadísticas está habilitada de forma predeterminada y sigue siendo controlada por el usuario.

<a id="presets-and-live-controls"></a>

### Presets y controles en vivo

- Ajustes preestablecidos visuales integrados de solo lectura, que incluyen estilos extremos como Neon Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder, Cyberdelic Riot, Acid Snowstorm, Terminal Collapse y Neon Razorstorm.
- Preajustes ASCII tradicionales integrados, incluidos Classic Camera ASCII, ANSI Newsprint, Terminal Mono y Dense Typewriter.
- ASCII World Mint aplica glifos de líneas de color menta con un jitter suave sobre un fondo verde azulado oscuro a la imagen, el video o la cámara seleccionados. Está inspirado en [ASCII World de yeahpython](https://yeahpython.github.io/game/game.html).
- ASCII City Nightshift usa un fondo casi negro, luces ámbar y verde salvia, y caracteres densos de terminal con jitter. Está inspirado en [ASCII City de tweakyourpc](https://tweakyourpc.github.io/ascii-city/). Ambos presets animan las imágenes fijas incluso con la reactividad al audio desactivada.
- Classic Camera ASCII es el valor predeterminado para un perfil limpio. Los perfiles persistentes existentes mantienen su configuración visual en lugar de restablecerse silenciosamente. La opción visual de perfil limpio no anula la preferencia global de renderizado automático; Los ajustes preestablecidos sin un backend de compatibilidad explícito utilizan WebGPU/WebGL2 cuando el tiempo de ejecución los admite.
- Veintitrés ajustes preestablecidos de caracteres de solo lectura adaptados de [ascii.today](https://ascii.today/), incluidos Broadway KB, Computer, Doom, Ghost, Modular, Standard, Univers y Doh. El paquete acreditado completo se encuentra en [ascii.today Character Presets](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ASCII_TODAY_PRESETS.md).
- Built-in y My Presets se muestran como secciones separadas, ordenadas alfabéticamente de forma independiente con una búsqueda de nombre en vivo. El nombre anterior Point & Click Default ahora se muestra como Dense Color ASCII; su identificación preestablecida estable no cambia.
- El conjunto de caracteres, la familia de fuentes, la paleta y otras selecciones comparten la misma geometría de control, por lo que el ajuste ASCII tradicional permanece alineado en la densa barra lateral.
- Los controles de paleta, mapeo, tramado ordenado, rampa de glifos y color de glifos se pueden ajustar y guardar de forma independiente a través del esquema visual preestablecido existente.
- Las once variantes integradas de paletas y glifos incluyen ASCII City Nightshift, Braille, dibujo de cajas, marcas CJK, Hiragana, Katakana, CJK Unified y Hangul. Otras seis paletas sin ciclos de color se incorporan a presets existentes. Las cuatro paletas con ciclos de color se describen a continuación.
- Los ajustes preestablecidos del usuario se pueden guardar, duplicar, actualizar, eliminar, importar y exportar.
- Se pueden guardar varias listas de reproducción preestablecidas con nombre con entradas preestablecidas estables reordenadas, un intervalo de espera compartido y bucles aleatorios o en orden. La reproducción de la lista de reproducción utiliza el control de transición predeterminado existente, limitado a 1 a 5 segundos.
- Las transiciones preestablecidas se funden en lugar de fundirse en negro.
- El tiempo de transición es configurable.
- Editar un control visual durante una transición la detiene en el aspecto actual y conserva el cambio. El look interrumpido pasa a ser Custom y el material seleccionado sigue reproduciéndose. Los controles visuales MIDI siguen la misma regla.
- Los ajustes preestablecidos conservan la fuente de medios activa a menos que el usuario la cambie explícitamente.
- WTF pasa continuamente entre ajustes aleatorios seguros para uso en vivo, combinando familias de presets ASCII extremos y tradicionales y evitando una salida completamente blanca o negra. Cada transición elige Flat Media con una probabilidad del 80 %; el 20 % restante se reparte entre los diez modos espaciales, con un 2 % para cada uno. Son probabilidades por transición, por lo que pueden aparecer varios looks planos o espaciales seguidos.

<a id="pixel-art-and-color-cycling"></a>

### Pixel art y ciclos de color

Ocho presets originales combinan píxeles sólidos y glifos en cuatro paletas: Tidal Glass, Ember Grotto, Fern After Rain y Violet Dusk. Transforman la cámara, el vídeo o la imagen activos sin interrumpir su reproducción. Busca el nombre de una familia en Presets.

En el panel Color, elige una paleta con ciclos de color y configura **Color cycling** en Classic, con pasos discretos, o Blend, con transiciones suaves. **Cycle speed** va de −4× a 4×: cero congela la fase actual y los valores negativos invierten el sentido. **Cycle amount** mezcla los colores animados con la paleta fija. Start/Stop pausa y reanuda el ciclo. Las sombras y luces fijas y las formas de los glifos permanecen estables mientras cambian los rangos de color seleccionados. Los presets anteriores usan Off de forma predeterminada.

Estos looks originales están inspirados en [Mark Ferrari](https://www.markferrari.com/image-archives), [Living Worlds](https://www.effectgames.com/demos/worlds/) y [ejemplos de ciclo de color de Amiga](https://amiga.lychesis.net/specials/ColorCycling.html). No incluyen imágenes de esos artistas ni animaciones de escenas de autor.

<a id="audio-reactivity"></a>

### Reactividad de audio

- La reactividad de audio está activada de forma predeterminada.
- El micrófono/entrada es la fuente reactiva de audio predeterminada.
- Los archivos de audio locales pueden impulsar la modulación visual.
- El audio del sistema/pantalla se admite cuando el sistema operativo proporciona una pista de audio a la aplicación de escritorio.
- Las compilaciones de escritorio Tauri incluyen rutas de captura de audio nativas para funciones de audio de entrada/sistema.
- Pistas de análisis de audio RMS, graves, medios-bajos, medios, medios-altos, agudos, presencia, brillo, densidad, energía transitoria, pulso de ritmo y movimiento espectral.
- Los ataques responden inmediatamente a cada nueva lectura de audio. Smoothing controla cuánto tarda en decaer la respuesta; póngalo en cero para obtener la respuesta más directa. El hardware de captura y la pantalla siguen aportando cierta latencia.
- Los controles de amortiguación de mezcla densa y de nivel de ruido ayudan a que las canciones ocupadas se mantengan reactivas sin fijar la vibración y la respuesta de ritmo al máximo.
- Cambiar un control deslizante de audio muestra **Custom** en el selector de presets de audio. Seleccionar cualquier preset de audio, incluso el mismo, restaura todos sus ajustes. La fuente de audio, el dispositivo de entrada y el look visual se conservan.
- Stop cancela tanto el inicio de captura pendiente como la reactividad activa. Los cambios de audio también se aplican durante las transiciones de presets de Pop Out.
- La modulación de audio no es persistente: afecta los parámetros de renderizado efectivos en vivo sin reescribir los ajustes preestablecidos guardados.
- Los límites de seguridad evitan que la alta sensibilidad lleve al renderizador a pantallas de color blanco puro o negro puro.

<a id="pop-out-and-external-displays"></a>

### Pop Out y pantallas externas

- Pop Out crea una ventana de salida separada destinada a un proyector, una tarjeta de captura o una pantalla secundaria.
- La ventana de control principal permanece visible e interactiva.
- La ventana de salida del escritorio es nativa, no una segunda superficie de interfaz de usuario duplicada y pesada.
- La selección de visualización de salida persiste cuando Tauri puede enumerar visualizaciones.
- La salida de una sola cámara usa captura nativa de cada plataforma: AVFoundation en macOS, Media Foundation en Windows y V4L2 mediante FFmpeg local incluido en Linux. Los fotogramas de Windows/Linux alimentan el presentador nativo `wgpu`; la duplicación acotada del fotograma actual sigue disponible cuando falla la apertura nativa o se seleccionan varias cámaras.
- El botón con icono de cámara guarda la imagen actual del renderizador principal como PNG directamente en el Escritorio. La superposición HTML Stats Overlay queda fuera de la captura y no se abre ningún diálogo para guardar.

<a id="experimental-midi-control"></a>

### Control experimental MIDI

- Control experimental nativo DIN MIDI para un Evolution/M-Audio UC-33e conectado a través de un mioXC de iConnectivity.
- Cuatro páginas de hardware para control visual, de audio, preestablecido y fino/de usuario, con los 9 atenuadores, 24 controladores giratorios y 14 botones asignables asignados.
- Ranuras numéricas preestablecidas visualmente del 1 al 128 con Enter, Previous y Next.
- La soft takeover está habilitada de forma predeterminada para evitar saltos después de cambios preestablecidos de software.
- Anulaciones de MIDI Learn, monitoreo de conexión y reconexión automática de mioXC.
- Captura limitada de SysEx de banco completo, instalación/restauración explícita, verificación y Ensure Profile on Connection opcional.
- MIDI está restringido a parámetros visuales, configuraciones audio-reactivas, ajustes preestablecidos visuales y WTF mode. No puede cambiar las fuentes de medios, la cámara, Pop Out ni las pantallas de salida.
- La validación de hardware físico actual cubre macOS Apple Silicon con el UC-33e conectado por DIN a través de un mioXC. No se admite USB directo UC-33e y la validación física de Windows/Linux no está completa.

MIDI sigue siendo experimental. Pasan las pruebas de mapeo automatizado, seguridad, transporte nativo y SysEx acotado. Ensure Profile on Connection permanece deshabilitado de forma predeterminada y requiere un perfil de hardware capturado y verificado manualmente.

<a id="desktop-packaging-and-updates"></a>

### Paquetes y actualizaciones de escritorio

- Construido con Tauri v2.
- El tiempo de ejecución de producción es solo local de forma predeterminada.
- La aplicación empaquetada bloquea conexiones HTTP(S) remotas arbitrarias a través de una Política de seguridad de contenido de producción.
- La aplicación utiliza capacidades Tauri limitadas divididas por ventana:
  - La ventana de control principal puede abrir medios seleccionados y administrar la salida.
  - La ventana de salida tiene una superficie de comando mínima.
- La aplicación de producción verifica los metadatos de las publicaciones GitHub para los paquetes de actualización firmados una vez en segundo plano cada vez que se abre la aplicación de producción. Una verificación actual o fuera de línea es silenciosa; cuando existe una versión más reciente, el control Update de la barra superior la muestra. Si actualiza desde 0.9.6 o 0.9.7, consulte las [notas de recuperación del actualizador heredado](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md#upgrading-from-096-or-097).
- El mismo control Update permanece disponible para una nueva verificación manual. La descarga, la instalación y el reinicio siguen siendo iniciados explícitamente por el usuario.
- El control Reports permanece visible aunque no haya informes de fallos pendientes, para que las preferencias `ask`, `always` y `off` siempre sean accesibles. El contador y la advertencia aparecen solo después de capturar un informe acotado y sin datos privados. El mismo diálogo permite capturar un diagnóstico manual del estado actual con una descripción opcional del problema; usa el esquema y la cola de informes existentes, sin adjuntar registros arbitrarios de la aplicación. Las compilaciones de desarrollo conservan los informes en el equipo para revisarlos y mantienen Send desactivado; solo puede enviarlos una compilación de lanzamiento con el identificador de producción. Se eliminan de la cola los informes antiguos de micrófono no disponible, ya que un dispositivo ausente o desconectado es un estado normal del hardware.
- Los artefactos públicos macOS están firmados con ID de desarrollador, notariados, grapados y validados por Gatekeeper. Los artefactos Windows actuales son vistas previas sin firmar.
- Los comandos de desarrollo normales utilizan la aplicación `ASCII VJ Remix Dev` visiblemente separada y el identificador de paquete `com.asciline.remix.dev`. Las compilaciones de desarrollo no pueden reemplazar ni heredar las concesiones de privacidad de la aplicación de producción.
- Las rutas en línea intencionales se limitan al flujo de verificación/descarga del actualizador y al envío de informes de fallas revisados/desinfectados solo en producción.
- El envío del informe de fallos pasa a través de la capa de escritorio Rust hasta el relé `https://crash.dustwave.xyz` Cloudflare Worker. La vista web no obtiene capacidad HTTP arbitraria y los medios seleccionados nunca se cargan. Las fallas del renderizador pueden adjuntar un resumen de evento limitado y desinfectado con un estado preestablecido/de fondo; No se adjuntan diagnósticos de medios locales ni registros arbitrarios.

<a id="advanced-and-development-only-paths"></a>

### Rutas avanzadas y solo de desarrollo

La ruta de transmisión heredada ASCILINE y el código de sesión de transmisión Rust/FFmpeg son infraestructura de desarrollo. El modo de transmisión, el selector estático/transmisión, la etiqueta de conexión y el contador de búfer no están expuestos en la interfaz de usuario de origen normal.

La configuración inicial del hardware y el mapa completo del controlador se encuentran en [UC-33e y mioXC Guide](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).

<a id="spatial-visuals-and-trails-110"></a>

## Visuales espaciales y estelas (1.1.0)

Todos los presets integrados empiezan en **Space / Motion → Visual mode → Flat media**, incluido Ashen Ruins. Aplican el tratamiento de color, glifos o celdas sólidas directamente al material de entrada. Ashen Ruins empieza con un aspecto monocromático claro de celdas sólidas. Los once presets nuevos siguen disponibles; sus ajustes de cámara y escena se cargan, pero solo se aplican al elegir manualmente un modo espacial. Volver a seleccionar un preset integrado restaura Flat Media. Los presets personalizados guardados conservan su modo y no se migran los ajustes existentes. La versión 1.1.0 está disponible en [GitHub Releases](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.1.0) y mediante el actualizador de la aplicación de producción. Consulte el [registro de publicación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md#published-artifacts-and-acceptance) para conocer la validación de instaladores y actualizaciones y las comprobaciones físicas pendientes.

|Preset|Visual mode opcional|Escena al activarlo|
| --- | --- | --- |
|Neon Night Drive|City streets|Recorrido rápido y bajo entre calles, edificios altos, pavimento mojado y lluvia|
|Media Corridor|Media corridor|Túnel estrecho y simétrico de pantallas, lente angular y glifos de bloque|
|Wet Coast|Wet coast|Recorrido lento por la costa, agua abierta, edificios bajos y textura Braille|
|Neon Cathedral|Vaulted hall|Vista ascendente de una nave con columnas altas, techo inclinado y glifos finos|
|Orbital Chamber|Orbitals|Esfera coloreada con el material de entrada y anillo inclinado giratorio|
|Ashen Ruins|Recursive ruins|Arquitectura monocromática, pasajes abiertos y niebla clara en la distancia|
|Fractal Dive|Mandelbrot dive|Zoom giratorio de Mandelbrot con color y distorsión de contornos derivados de la fuente|
|Mandelbulb Bloom|Mandelbulb|Vista orbital de un fractal orgánico con textura Braille en la superficie|
|Mandelbox Passage|Mandelbox|Cubos recursivos y arquitectura plegada|
|Edge Etching|Flat media|Glifos de líneas orientadas sobre los bordes marcados de la imagen|
|Phosphor Echo|Flat media|Estelas que se desvanecen con zoom y rotación suaves|

**Travel speed** admite valores positivos y negativos: los negativos invierten el movimiento. **Freeze scene** detiene el reloj de la escena y el movimiento y desvanecimiento del eco; el video y el audio siguen reproduciéndose. **Route position** añade un desplazamiento. **Reset scene / trails** devuelve el reloj y el desplazamiento de cámara al origen y borra las estelas. El avance recorre un mundo que se repite; Street weave se mueve dentro de la calle libre y Look around / orbit gira la vista en movimiento o rodea los objetos orbitales. **Camera tilt** orienta la cámara hacia arriba o abajo; Relief usa una cámara elevada sobre el terreno. Son recorridos de cámara restringidos, sin vuelo libre ni edición del mundo.

**Media amount** mezcla la fuente seleccionada sobre las superficies. Las configuraciones opcionales de escena usan entre un 80 y un 95 % para que el material de entrada determine su apariencia. Cero usa materiales procedurales. Las imágenes de las paredes ocupan paneles de 8 × 4 unidades; las cubiertas y los techos también usan la fuente, y Orbital Chamber la muestra detrás de las formas del primer plano. **Surface framing** controla la repetición, el ajuste o el recorte dentro de cada superficie. El selector de fuente, la inversión de cámara y los controles de reproducción siguen gestionando el material. Los ajustes guardados o personalizados conservan sus valores; vuelva a seleccionar un preset relacionado y active su modo espacial para cargar la configuración de esa escena. Cambiar de preset visual no selecciona otra fuente ni reinicia la reproducción.

**Fractal zoom**, **Fractal detail** y **Fractal shape** aparecen al activar uno de los cuatro modos fractales. Zoom cambia la escala; Detail ajusta el número acotado de iteraciones; Shape modifica los cortes, la potencia del Mandelbulb, los pliegues del Mandelbox o la distorsión de contornos a partir del material de entrada. La velocidad, la congelación, los controles de cámara y la mezcla del material siguen disponibles en vivo. Ashen Ruins, Fractal Dive y Mandelbox Passage usan celdas sólidas; active Glyph mode y desactive Solid mode para obtener textura ASCII. Brightness Relief se retiró del catálogo de presets, pero su modo visual sigue disponible para los looks personalizados existentes.

**Material glyphs** distingue superficies, agua, ventanas y cielo. Reserva ocho de los 96 espacios para glifos. Al aumentar Media amount, disminuye la sustitución por glifos de materiales para conservar el brillo y las formas de la fuente. Desactívelo y ponga Edge glyphs en cero para usar la rampa personalizada completa sin cambios. Edge glyphs funciona sobre Flat Media y elige trazos horizontales, verticales o diagonales, con histéresis cerca del umbral. Los ciclos de paleta siguen usando la luminancia base estable para los glifos habituales.

**Phosphor / echo**, **Trail half-life**, **Echo zoom** y **Echo rotation** funcionan en modos planos y espaciales. Las estelas largas pueden ocultar detalles finos. El historial se borra al cambiar Bright output, la fuente, la cuadrícula, la escena, la semilla, el desplazamiento de ruta, la paleta o la disposición de glifos, y cuando el renderizado se interrumpe durante más de un segundo. Las transiciones estructurales nativas también borran el historial. El historial en coma flotante evita que las estelas tenues queden fijas; los dispositivos WebGL2 antiguos sin destinos de renderizado en coma flotante usan una alternativa de bytes con desvanecimiento más rápido.

Los ajustes de audio existentes añaden un movimiento moderado de graves al campo de visión y a la altura de cámara, presencia a la luz, acentos de ritmo al resplandor y agudos a los reflejos del agua. Usan la sensibilidad, las intensidades por característica y la atenuación por densidad existentes. MIDI Learn incluye los controles espaciales, Freeze Scene y Reset Scene and Trails; no añade acciones de fuente ni de cámara.

Los controles espaciales se aplican a imágenes, videos y cámaras locales, incluidas composiciones de cámaras. El renderizador heredado de flujos del servidor conserva su comportamiento. WebGPU, WebGL2 y wgpu nativo renderizan localmente. Los presets asignados explícitamente a Canvas mantienen el límite de densidad por software y usan la duplicación de salida para Pop Out espacial. Si la presentación GPU nativa no está disponible, elija Canvas para usar esa alternativa. Los límites de densidad normal y avanzada no han cambiado. Relief, Orbitals, los reflejos y las escenas densas pueden requerir más tiempo de GPU; reduzca Columns antes de elevar otros límites. La aceptación física en M1/16 GB y Windows/Linux sigue pendiente para esta versión.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/USER_GUIDE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md)
