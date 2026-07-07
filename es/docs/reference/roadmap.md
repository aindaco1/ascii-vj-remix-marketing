---
title: Hoja de ruta
description: Documentación de hoja de ruta derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Referencia
lang: es
---

# Hoja de ruta

Esta hoja de ruta separa la línea base de características actual 0.9.3 del trabajo planificado.
Su objetivo es guiar el producto, el renderizador, el empaquetado de escritorio y la contribución.
decisiones.

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
Superficie de control creativo para vídeo, imagen, cámara, audio-reactivo y futuro.
Imágenes ASCII basadas en MIDI.

## Línea base de características actuales: 0.9.3

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
- Las compilaciones locales macOS están autofirmadas ad hoc de forma predeterminada; CI de lanzamiento público
requiere firma y certificación notarial del ID del desarrollador.
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

### Control de hardware nativo MIDI

Construya la capa de control MIDI alrededor de un registro de destino de control genérico, con el
Evolution/M-Audio UC33e a través de iConnectivity mioXC como primer equipo de validación.

Alcance:

- Adaptador nativo Tauri MIDI que utiliza un backend multiplataforma Rust MIDI.
- MIDI enumeración de entradas, estado de conexión y monitor de último mensaje.
- MIDI Modo de aprendizaje.
- Persistencia de mapeo separada de los ajustes preestablecidos visuales.
- Importación/exportación de mapeos.
- Toma/captación suave para atenuadores y perillas.
- Configuración de valores: mínimo/máximo, inversión, banda muerta, suavizado, lineal/exponencial/log
curvas.
- Modos de botón: disparador, alternar, momentáneo, preestablecer siguiente/anterior, alternar WTF,
alternancia de audio, acciones emergentes donde sea seguro.
- Perfil de inicio UC33e después de capturar mensajes de hardware reales.
- Inyección de evento MIDI falso para CI.

Regla de regresión: MIDI debe enrutarse a través de las mismas rutas de control en vivo que la interfaz de usuario.
No debe reiniciar los medios ni omitir la semántica preestablecida/audio/WTF a menos que el mapeado
El objetivo es explícitamente estructural.

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
- El desarrollo local mantiene rutas de firma ad hoc/predeterminadas.
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
  - mantener la firma ad hoc como respaldo del desarrollo local.
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
- El actualizador de extremo a extremo prueba el salto de una versión instalada anterior a una más nueva.
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
- Registros de salida nativos con contadores para fotogramas adquiridos, fotogramas presentados y parámetros.
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
Equipo UC33e/mioXC.
- Agregue una matriz de solución de problemas para permisos, reserva GPU y ventana de salida
problemas.
- Agregue comprobaciones de accesibilidad automatizadas para el comportamiento del teclado/enfoque/ARIA.
- Agregue un catálogo i18n incluido solo cuando exista un flujo de trabajo de localización real.

## Riesgos abiertos

- La compatibilidad con WebGPU varía según los navegadores y las vistas web de Tauri.
- El soporte de Linux WebGPU puede permanecer inconsistente por un tiempo.
- La captura multicámara depende del sistema operativo, el firmware de la cámara, la topología USB y el navegador.
comportamiento.
- Las indicaciones de privacidad de macOS pueden ser sensibles al identificador del paquete y a la firma
identidad.
- La licencia FFmpeg debe seguir siendo una puerta de liberación explícita.
- La decodificación de medios nativos y la interoperabilidad de GPU difieren significativamente según la plataforma.
- Los eventos MIDI futuros de alta tasa podrían causar abandono de la interfaz de usuario sin cuadro de animación
fusionándose.
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
- La compatibilidad con el controlador MIDI se implementa o se aplaza explícitamente desde 1.0.
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
