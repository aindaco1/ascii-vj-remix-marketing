---
title: Conjunto de funciones
description: Documentación del conjunto de funciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Resumen
lang: es
---

# Conjunto de funciones

Esta página describe la línea base de funciones ASCII VJ Remix actual para desarrolladores que planean bifurcaciones, puertos, integraciones o trabajo de funciones. El mapa de capacidades se genera a partir del archivo README del repositorio principal.

## Capacidades actuales

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
- Dieciséis paletas nativas del proyecto, mapeo de color/luminancia más cercano y tramado Bayer 2x2/4x4/8x8 ordenado comparten un parámetro y un contrato de tabla de búsqueda en el navegador, Canvas y rutas de salida nativas.
- Los controles de glifo cubren profundidad, desplazamiento, inversión, color de origen/fijo, fondo, Braille, bloques de dibujo/símbolos comunes, latín extendido, griego, cirílico, marcas CJK, Hiragana, Katakana, CJK unificado U+4E00-U+9FFF, Hangul y rampas personalizadas de hasta 96 escalares Unicode compatibles.
- El atlas neutral Unicode se genera y verifica fuera de línea, se incluye localmente y se carga en páginas delimitadas de 1024 px solo cuando los glifos seleccionados las necesitan.
- La densidad normal está protegida por el rendimiento mediante límites de columnas compartidas y de celdas totales. La preferencia global Advanced Density expone hasta 900 columnas sin una garantía de 30 FPS y nunca se almacena en ajustes preestablecidos visuales.
- La versión 0.9.6 elimina las cargas duplicadas del marco fuente nativo, reutiliza recursos estables GPU y limita el trabajo de la interfaz de usuario en tiempo de transición sin cambiar las matemáticas del renderizador o la configuración de calidad.
- El renderizador expone controles en vivo para cuadrícula, tamaño de celda, color, gamma, brillo, contraste, saturación, combinación de fondo, cuantificación, fluctuación, posición de muestra, suavizado, FPS, comportamiento de glifo/celda y estado de rendimiento.
- La superposición de estadísticas está habilitada de forma predeterminada y sigue siendo controlada por el usuario.

### Presets y controles en vivo

- Ajustes preestablecidos visuales integrados de solo lectura, que incluyen estilos extremos como Neon Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder, Cyberdelic Riot, Acid Snowstorm, Terminal Collapse y Neon Razorstorm.
- Preajustes ASCII tradicionales integrados, incluidos Classic Camera ASCII, ANSI Newsprint, Terminal Mono y Dense Typewriter.
- Classic Camera ASCII es el valor predeterminado para un perfil limpio. Los perfiles persistentes existentes mantienen su configuración visual en lugar de restablecerse silenciosamente. La opción visual de perfil limpio no anula la preferencia global de renderizado automático; Los ajustes preestablecidos sin un backend de compatibilidad explícito utilizan WebGPU/WebGL2 cuando el tiempo de ejecución los admite.
- Veintitrés ajustes preestablecidos de caracteres de solo lectura adaptados de [ascii.today](https://ascii.today/), incluidos Broadway KB, Computer, Doom, Ghost, Modular, Standard, Univers y Doh. El paquete acreditado completo se encuentra en [ascii.today Character Presets](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ASCII_TODAY_PRESETS.md).
- Built-in y My Presets se muestran como secciones separadas, ordenadas alfabéticamente de forma independiente con una búsqueda de nombre en vivo. El nombre anterior Point & Click Default ahora se muestra como Dense Color ASCII; su identificación preestablecida estable no cambia.
- El conjunto de caracteres, la familia de fuentes, la paleta y otras selecciones comparten la misma geometría de control, por lo que el ajuste ASCII tradicional permanece alineado en la densa barra lateral.
- Los controles de paleta, mapeo, tramado ordenado, rampa de glifos y color de glifos se pueden ajustar y guardar de forma independiente a través del esquema visual preestablecido existente.
- Diez variantes integradas de paleta/glifo incluyen Braille, dibujo de cuadro, marcas CJK, Hiragana, Katakana, CJK Unificado y Hangul. Las otras seis paletas se incorporan a los ajustes preestablecidos existentes.
- Los ajustes preestablecidos del usuario se pueden guardar, duplicar, actualizar, eliminar, importar y exportar.
- Las transiciones preestablecidas se funden en lugar de fundirse en negro.
- El tiempo de transición es configurable.
- Los ajustes preestablecidos conservan la fuente de medios activa a menos que el usuario la cambie explícitamente.
- WTF mode realiza una transición continua a través de configuraciones aleatorias seguras en vivo y se inclina hacia familias preestablecidas ASCII tanto extremas como tradicionales, evitando al mismo tiempo la salida de blanco puro o negro puro.

### Reactividad de audio

- La reactividad de audio está activada de forma predeterminada.
- El micrófono/entrada es la fuente reactiva de audio predeterminada.
- Los archivos de audio locales pueden impulsar la modulación visual.
- El audio del sistema/pantalla se admite cuando el sistema operativo proporciona una pista de audio a la aplicación de escritorio.
- Las compilaciones de escritorio Tauri incluyen rutas de captura de audio nativas para funciones de audio de entrada/sistema.
- Pistas de análisis de audio RMS, graves, medios-bajos, medios, medios-altos, agudos, presencia, brillo, densidad, energía transitoria, pulso de ritmo y movimiento espectral.
- Los controles de amortiguación de mezcla densa y de nivel de ruido ayudan a que las canciones ocupadas se mantengan reactivas sin fijar la vibración y la respuesta de ritmo al máximo.
- La modulación de audio no es persistente: afecta los parámetros de renderizado efectivos en vivo sin reescribir los ajustes preestablecidos guardados.
- Los límites de seguridad evitan que la alta sensibilidad lleve al renderizador a pantallas de color blanco puro o negro puro.

### Pop Out y pantallas externas

- Pop Out crea una ventana de salida separada destinada a un proyector, una tarjeta de captura o una pantalla secundaria.
- La ventana de control principal permanece visible e interactiva.
- La ventana de salida del escritorio es nativa, no una segunda superficie de interfaz de usuario duplicada y pesada.
- La selección de visualización de salida persiste cuando Tauri puede enumerar visualizaciones.

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

### Paquetes y actualizaciones de escritorio

- Construido con Tauri v2.
- El tiempo de ejecución de producción es solo local de forma predeterminada.
- La aplicación empaquetada bloquea conexiones HTTP(S) remotas arbitrarias a través de una Política de seguridad de contenido de producción.
- La aplicación utiliza capacidades Tauri limitadas divididas por ventana:
  - La ventana de control principal puede abrir medios seleccionados y administrar la salida.
  - La ventana de salida tiene una superficie de comando mínima.
- La versión 0.9.8 comprueba metadatos de GitHub Releases para paquetes de actualización firmados una vez en segundo plano cada vez que se abre la aplicación de producción. Una verificación actual o fuera de línea es silenciosa; cuando existe una versión más reciente, el control Update de la barra superior la muestra. Las versiones 0.9.6 y 0.9.7 requieren una actualización manual de DMG a 0.9.8 porque una capacidad de producción faltante ocultaba su control Update.
- El mismo control Update permanece disponible para una nueva verificación manual. La descarga, la instalación y el reinicio siguen siendo iniciados explícitamente por el usuario.
- El control Reports permanece visible cuando no hay informes de fallos pendientes, por lo que siempre se puede acceder a las preferencias `ask`, `always` y `off`. Un recuento pendiente y un estado de advertencia aparecen solo después de que se captura un informe desinfectado y delimitado. Los paquetes de desarrollo conservan los informes localmente para su revisión y mantienen el envío desactivado; solo se puede enviar una compilación en modo de lanzamiento con el identificador del paquete de producción. Los informes de micrófonos no disponibles heredados se eliminan de la cola porque un dispositivo de entrada desconectado o ausente es un estado de hardware normal.
- Los artefactos públicos 1.0.0 macOS están firmados con el ID del desarrollador, notariados, engrapados y validados por Gatekeeper. Los artefactos públicos 1.0.0 Windows son vistas previas sin firmar.
- Los comandos de desarrollo normales utilizan la aplicación `ASCII VJ Remix Dev` visiblemente separada y el identificador de paquete `com.asciline.remix.dev`. Las compilaciones de desarrollo no pueden reemplazar ni heredar las concesiones de privacidad de la aplicación de producción.
- Las rutas en línea intencionales se limitan al flujo de verificación/descarga del actualizador y al envío de informes de fallas revisados/desinfectados solo en producción.
- El envío del informe de fallos pasa a través de la capa de escritorio Rust hasta el relé `https://crash.dustwave.xyz` Cloudflare Worker. La vista web no obtiene capacidad HTTP arbitraria y los medios seleccionados nunca se cargan. Las fallas del renderizador pueden adjuntar un resumen de evento limitado y desinfectado con un estado preestablecido/de fondo; No se adjuntan diagnósticos de medios locales ni registros arbitrarios.

### Rutas avanzadas y solo de desarrollo

La ruta de transmisión heredada ASCILINE y el código de sesión de transmisión Rust/FFmpeg son infraestructura de desarrollo. El modo de transmisión, el selector estático/transmisión, la etiqueta de conexión y el contador de búfer no están expuestos en la interfaz de usuario de origen normal.

La configuración inicial del hardware y el mapa completo del controlador se encuentran en [docs/MIDI_UC33E.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/MIDI_UC33E.md).



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
