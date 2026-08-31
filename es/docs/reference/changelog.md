---
title: Registro de cambios
description: Documentación de registro de cambios derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Referencia
lang: es
---

# Registro de cambios

## [1.0.0] - 2026-08-31

### Añadido

- Se agregó búsqueda en vivo de nombres preestablecidos con secciones Built-in y My Presets separadas y ordenadas alfabéticamente de forma independiente, estado de resultados, borrado del teclado y estados sin resultados.
- Se agregaron paquetes de solicitud de extracción de perfil de lanzamiento para control de calidad físico: un instalador de desarrollo Windows sin firmar y con el actualizador deshabilitado más paquetes de desarrollo AppImage, deb y rpm Linux retenidos durante 14 días. Cada conjunto de paquetes incluye los recursos FFmpeg/ffprobe anclados, construidos en plataforma y verificados.
- Se agregó una guía de aceptación y arranque de Hyper-V no destructiva para máquinas virtuales de prueba Ubuntu 26.04.1 y Fedora 44 x86_64 en Windows 11 Pro.
- Se agregó una puerta de subsistema PE que rechaza un ejecutable en modo de lanzamiento Windows a menos que esté marcado como una aplicación gráfica.

### Cambiado

- Se promovieron los metadatos de fuente/paquete sincronizados a la versión estable 1.0.0.
- Se convirtió Classic Camera ASCII en el estado visual predeterminado para un perfil limpio y al mismo tiempo se conservan los perfiles persistentes, y Point & Click Default ahora se muestra como Dense Color ASCII sin cambiar su identificador estable de preset.
- Se estandarizaron los anchos y alturas de los selectores, las columnas de las etiquetas, el espaciado entre filas y la presentación de valores; se eliminó el control redundante Atlas Style de una opción.
- Se etiquetó Advanced Density con su límite de `Up to 900 columns` y la advertencia de que no garantiza 30 FPS directamente en la fila de control.
- Ejecutores de aceptación de compilación y lanzamiento de Linux fijados en Ubuntu 24.04.

### Corregido

- Envío remoto de fallos vinculado tanto al identificador del paquete de producción como a una versión de lanzamiento. Los paquetes de control de calidad de `ASCII VJ Remix Dev` optimizados ahora mantienen los informes locales, etiquetan ese estado en la interfaz de usuario de Reports y no pueden enviarse como producción.
- Se agregaron marcas de tiempo de captura reales RFC 3339 más secuencias de comandos/líneas/columnas seguras y contexto de renderizado solicitado/resuelto para diagnosticar problemas sin exponer rutas locales. Los marcos de pila nativos de WebKit ya no se confunden con los correos electrónicos.
- Contenía lectura de píxeles Canvas2D bloqueada, incluido el código 18 de WebKit `SecurityError`, dentro del renderizador en lugar de escalarla como un error global de la aplicación.
- Se agregó una geometría de inicio de 1000x680 propiedad de Linux con un mínimo de 900x600 en lugar de heredar la ventana más grande macOS/Windows, mientras que el título de la ventana de desarrollo se deriva de su identidad de producto en lugar de duplicar la geometría.
- Se agregaron formatos Demo Video integrados propiedad de la plataforma: H.264/MP4 para vistas web macOS y Windows, y VP8/WebM para instalaciones limpias de Ubuntu y Fedora que carecen de códecs H.264 GStreamer opcionales. Las selecciones de Demo Video guardadas existentes migran al recurso de plataforma correcto, mientras que tanto los formatos de demostración enviados como los videos seleccionados por el usuario vuelven a intentarlo a través de FFmpeg incluido si el decodificador de la plataforma los rechaza. Los identificadores de origen empaquetados exactos preservan el estrecho límite de acceso a archivos existente.
- Trate los dispositivos de micrófono desconectados o no disponibles como una condición de hardware esperada. La aplicación puede intentar utilizar el navegador alternativo y ya no pone en cola un informe de fallo simplemente porque una máquina virtual no tiene un micrófono utilizable; Los informes heredados para esa condición exacta se eliminan en el próximo lanzamiento.
- Hizo que los contenedores de Podman reutilizaran una conexión predeterminada que ya estaba en buen estado antes de iniciar su VM alternativa, evitando la colisión de una máquina activa de macOS con otras salidas de proyectos.
- Se desacopló el aspecto de perfil limpio Classic Camera ASCII de la preferencia de renderizado global. Los presets integrados que no solicitan explícitamente un backend de compatibilidad ahora comienzan desde Auto y se resuelven en WebGPU/WebGL2 cuando están disponibles en cada host de escritorio empaquetado.
- Se restauró la representación de glifos WebGPU reales en la vista empaquetada macOS Apple WebKit. Las páginas de glifos ahora se decodifican a través de la URL del activo incluido y compactan la rampa activa de hasta 96 escalares más su cobertura en una textura RGBA de dos filas debajo del problemático límite de textura amplia de WebKit. El barrido preestablecido instalado resuelve 41 presets integrados en WebGPU y 28 ajustes preestablecidos de compatibilidad intencionales en Canvas2D, con los 69 visibles; Paper Shredder conserva explícitamente Canvas2D para preservar el aspecto anterior a la paridad del atlas de glifos.
- Se aumentó la resolución de muestra del lienzo principal del barrido preestablecido empaquetado para que se evalúen los escasos trazos Braille, kana, Hangul y de dibujo de cuadro antes de que la reducción de resolución de miniaturas pueda promediarlos.
- Transiciones sincronizadas de vista primaria y Pop Out nativas en un reloj con marca de tiempo. Las transiciones numéricas ahora usan el mismo progreso de suavizado en ambas superficies, los cambios en la familia de renderizadores usan la misma curva de fundido cruzado y la presentación nativa usa un buffering de cadena de intercambio mínimo en lugar de seguir los recorridos de ida y vuelta de los parámetros en cola.
- Se marcó la hora de la transferencia de reproducción de video principal para que el decodificador nativo avance su búsqueda inicial según el tiempo dedicado a abrir la ventana de salida e iniciar el decodificador, eliminando el retraso evitable en la reproducción Pop Out.
- Se fijó Pop Out nativo a un formato de superficie unorm no sRGB con paridad de navegador cuando la plataforma lo admite, lo que evita que el orden del formato de la plataforma aplique una conversión sRGB adicional a los colores del renderizador compartido.
- Se evitó que la aplicación Windows en modo de lanzamiento y los procesos secundarios FFmpeg/ffprobe abrieran ventanas visibles de la consola. Las compilaciones de depuración conservan el comportamiento normal de la consola de diagnóstico.
- Se eliminó la política general de glifo a lienzo Windows WebView2 ahora que la textura compacta del glifo de rampa activa es compartida por la ruta WebGPU reparada. Los ajustes preestablecidos automáticos intentan nuevamente WebGPU en Windows, con WebGL2 y Canvas2D mantenidos como alternativas de construcción reales. Un contrato centralizado de 69 presets en total / 41 acelerados / 28 explícitos de Canvas2D, una regresión de siete unidades colapsadas, el barrido preestablecido visible y la matriz CI Windows protegen este límite de propiedad.
- Hizo que el menú adicional preestablecido enfocara su primera acción, se cerrara con Escape y restaurara el enfoque a su disparador.
- Hizo que el arranque de firma local importara su identidad PKCS#12 temporal con una contraseña compatible con Keychain, y hizo que el iniciador local se negara a eliminar un paquete cuando sus rutas de origen e instalación son las mismas.

La versión 1.0.0 completa la primera versión de escritorio estable con un flujo de trabajo preestablecido pulido, manejo de medios empaquetados multiplataforma, transiciones y color Pop Out nativos sincronizados y un contrato de renderizador integrado explícito de 69 en total / 41 acelerado / 28 Canvas. Los artefactos macOS permanecen firmados con la identificación del desarrollador, notariados, engrapados y validados por Gatekeeper; Los artefactos Windows siguen siendo vistas previas sin firmar claramente documentadas.

## [0.10.0] - 2026-08-29

### Añadido

- Se agregaron diagnósticos de renderizador limitados al flujo de trabajo Reports existente. Una creación fallida del procesador registra los backends preestablecidos, solicitados y resueltos, el resultado alternativo, la clase de origen, el resumen de errores y hasta ocho eventos recientes del procesador sin adjuntar medios, capturas de pantalla, rutas locales o registros arbitrarios.
- Las solicitudes de extracción del mismo repositorio ahora retienen un instalador de desarrollo Windows sin firmar y deshabilitado por el actualizador durante 14 días después de que pasa la puerta de escritorio Windows, lo que permite el control de calidad físico sin reemplazar la aplicación de producción.

### Cambiado

- Se reemplazó la insignia del encabezado `VJ` de solo texto con el ícono canónico de neón de la aplicación de reproducción y píxeles, preservando al mismo tiempo la huella de la barra superior existente.

### Corregido

- Se reemplazó la ruta de diagnóstico de medios `/tmp` exclusiva de Unix con el directorio temporal del sistema operativo para que las escrituras de diagnóstico Windows ya no fallen ni se conviertan en informes de fallos falsos. Las fallas del escritor de diagnóstico también se clasifican como no fatales tanto por los clientes actuales como por el relé.
- Se aplicó el respaldo WebGPU/WebGL2-to-Canvas a las transiciones preestablecidas en vivo, así como al inicio inicial. Si fallan tanto el renderizador solicitado como el respaldo de Canvas, el ajuste preestablecido anterior permanece activo y se pone en cola un informe de diagnóstico revisable.
- Enrute los ajustes preestablecidos del atlas de glifos a través del renderizador Canvas2D limitado en el tiempo de ejecución empaquetado Windows WebView2. Las pruebas físicas de Windows 11 mostraron que WebGPU y WebGL2 podían reportar una inicialización exitosa mientras producían una superficie de glifo en blanco; Los ajustes preestablecidos sólidos/píxeles GPU permanecen acelerados.

La versión 0.10.0 hace que los ajustes preestablecidos de glifos Windows sean confiables a través de una ruta de compatibilidad limitada con Canvas2D, extiende las fallas del renderizador al flujo de trabajo existente de Reports limitado por privacidad y reemplaza la insignia `VJ` del encabezado principal con el ícono de la aplicación canónica. La versión 0.9.12 restaura todos los ajustes preestablecidos integrados en la vista principal de la aplicación mientras conserva la relación de aspecto de origen y la ruta nativa Pop Out.

## [0.9.12] - 2026-08-28

### Corregido

- Se restauró la salida visible de la vista principal para cada ajuste preestablecido Demo Image incorporado corrigiendo las cargas de páginas de glifos de WebGL y usando mips de atlas de cobertura máxima en caché para glifos representados en celdas muy pequeñas.
- Mantuvo los lienzos preestablecidos de sólidos, píxeles y glifos en la relación de aspecto de origen resolviendo los recuentos de filas estáticas a partir del ancho y alto real de la celda.
- Se agregó una matriz de pruebas de humo de vista primaria totalmente preestablecida que cubre la activación, la salida visible, los errores de WebGL, la finalización diferida de la página de glifos y el aspecto del lienzo.
- Se evitaron lienzos de glifos de vista primaria en blanco en el tiempo de ejecución de macOS Apple WebKit seleccionando allí la ruta de glifo Canvas2D limitada existente. Los ajustes preestablecidos primarios de sólidos/píxeles conservan WebGPU, los tiempos de ejecución compatibles conservan los glifos GPU y el renderizador nativo Pop Out no cambia.
- Hizo que la prueba de humo de rendimiento del escritorio empaquetado rechazara un renderizador que avanzaba cuyo lienzo principal no tiene señal de píxeles visible.
- Se agregó un barrido Apple WebKit empaquetado que activa los 69 ajustes preestablecidos de Demo Image integrados y verifica la visibilidad de la vista principal, la familia de renderizador, el estado de ejecución, los errores de GPU y el aspecto de fuente/lienzo para cada superficie final.

La versión 0.9.11 agrega paletas de proyecto con presupuesto de rendimiento, tramado ordenado, controles de glifos multilingües, rampas Unicode personalizadas, límites de densidad y paridad de renderizado/salida nativa. La versión 0.9.10 reemplaza el arte de televisión heredado con un icono canónico de la aplicación generado para cada plataforma empaquetada y incorpora la corrección de aceptación de Reports posterior a 0.9.9. La versión 0.9.9 mantiene las preferencias de informes de fallas accesibles con una cola vacía, elimina la lectura duplicada del backend de la barra superior y amplía la prueba de humo de la interfaz empaquetada para cubrir ambos controles. La versión 0.9.8 restaura el control de producción y la verificación de inicio de Update, agrega una prueba de humo de regresión de UI empaquetada y acorta las compilaciones de lanzamiento al compilar la aplicación y el tiempo de ejecución de FFmpeg simultáneamente antes de la reutilización de artefactos verificados. La versión 0.9.7 agrega el controlador de verificación de lanzamiento silencioso al tiempo que conserva la instalación aprobada por el usuario y fortalece la resiliencia del transporte de lanzamiento. La versión 0.9.6 continúa el trabajo de puesta en servicio experimental de MIDI, elimina la sobrecarga medida de la ruta activa de salida/renderizador sin cambiar las matemáticas o la calidad visual, y refuerza la ruta de lanzamiento de arrastrar a las aplicaciones de macOS. La versión 0.9.5 agrega 23 ajustes preestablecidos de caracteres inspirados en ascii.today acreditados y un control DIN MIDI nativo experimental para un Evolution/M-Audio UC-33e a través de un mioXC de iConnectivity, incluidas cuatro páginas de controlador completas, soft takeover, selección de preajustes numéricos, aprendizaje de MIDI y captura/restauración de banco completo de SysEx. La versión 0.9.3 traslada las versiones de escritorio públicas a la distribución macOS firmada/notariada, publica Windows como una vista previa sin firmar mientras se difiere la firma y amplía la reactividad del audio con controles de mezcla densa que reducen la reacción exagerada en música ocupada. La versión 0.9.0 sigue siendo la primera base de documentación para el conjunto de funciones actual ASCII VJ Remix.

## [0.9.11] - 2026-08-28

### Añadido

- Se agregaron 16 paletas integradas nativas del proyecto compartidas por controles, ajustes preestablecidos, Canvas, WebGL2, WebGPU y salida nativa `wgpu`: Signal Court, Ember Gold, Prism Armor, Verdigris Clay, Forest Kiln, Blush Lichen, Solar Standard, Primary Rite, Jewel Circuit, Spectrum Vault, Soft Voltage, Midnight Scan, Moss Ultraviolet, Cyan Fog, Dark Parade y Sea Glass Array.
- Se agregó mapeo de rampa de luminancia y color más cercano, además de difuminado Bayer 2x2, 4x4 y 8x8 ordenado con controles de intensidad, escala, polarización e inversión.
- Se agregó profundidad de glifo, desplazamiento, inversión, color de glifo fuente/fijo, color de fondo y controles de rampa personalizados escritos. Las rampas personalizadas están limitadas a 96 escalares Unicode admitidos.
- Se agregó un atlas de glifos neutros deterministas y agrupados localmente con ASCII, Braille, bloques, dibujos de cuadros, formas, flechas, símbolos matemáticos y técnicos, latín extendido, griego, cirílico, puntuación/radicales CJK, Hiragana, Katakana, CJK ideogramas unificados U+4E00-U+9FFF y sílabas Hangul.
- Se agregaron diez ajustes preestablecidos de paleta/glifo e incorporó las paletas restantes a los ajustes preestablecidos existentes sin agregar el paquete de paleta o la importación JSON de paleta.
- Se agregó una preferencia global Advanced Density que expone hasta 900 columnas fuera de los ajustes preestablecidos visuales y elimina claramente la garantía de 30 FPS.

### Cambiado

- Búsqueda de paleta fusionada y tramado ordenado en el paso de celda existente. Una tabla de búsqueda compartida de 32x32x32 se reconstruye solo cuando cambia la paleta o la asignación.
- Se reemplazó la ruta fija del índice de glifos incluidos con identificadores de glifos escalares Unicode y un atlas paginado compartido por el navegador GPU y los renderizadores nativos Pop Out.
- Volvió a editar el atlas en dieciséis páginas de 1024x1024 R8. La asignación total de GPU permanece limitada mientras que la selección multilingüe realiza operaciones de decodificación/carga diferidas más pequeñas; el caché de la página del navegador decodificada tiene un límite de cuatro páginas.
- Se agregó una clave de entrada de recursos de glifos para que las actualizaciones de transición y audio de 60 Hz no reconstruyan rampas, asignen buffers ni carguen recursos de glifos cuando la configuración de glifos no se modifica.
- El Pop Out nativo ahora busca una superficie disponible antes de que se escriba la cola del marco de origen, drena el trabajo de liberación automática del enlace de visualización de macOS por tick y sondea el trabajo de GPU completado. Las salidas ocluidas ya no retienen una asignación de preparación de carga por fotograma decodificado.
- Se reajustaron los ajustes preestablecidos integrados que anteriormente solicitaban de 700 a 900 columnas en el sobre de densidad normal medido. Advanced Density sigue estando disponible como preferencia explícita de la máquina.
- WTF extendido, reactividad de audio y MIDI a través de las rutas de parámetros canónicos existentes para el comportamiento de paleta, tramado y glifo.

### Rendimiento

- El techo acelerado normal es de 640 columnas y 160.000 celdas en total; el techo del software es de 120 columnas y 6.000 celdas. Advanced Density permite hasta 900 columnas y 500.000 celdas sin promesa de velocidad de fotogramas.
- En un host de validación M1 Max/64 GB optimizado en 640 columnas con video de 1080p, reactividad de audio sintético y Pop Out nativo, la característica desactivada WebGL2 midió 39,1 FPS principal, 39,9 FPS con Pop Out y 35,4 FPS durante las transiciones.
- La carga de trabajo completa de Signal Court/Bayer 4/CJK midió 37,9, 40,1 y 37,0 FPS para las mismas fases, con una peor fase P95 de 31,6 ms y aproximadamente 446 MB de RSS máximo. El Pop Out nativo presentó cerca de 60 FPS con cero fallas en GPU.
- Una ejecución de oclusión prefijada desatendida de 15 minutos aumentó de 156,5 MB a 9.411,9 MB de RSS constante. La repetición fija comenzó en 156,1 MB y finalizó en 155,5 MB, con un pico de inicio de 446,1 MB y sin fallas de sincronización nativa. La limitación de la ventana de fondo hizo que la memoria repetida fuera evidencia en lugar de evidencia FPS.
- Estas cifras son evidencia local de un host más rápido que el piso, no de la aceptación física de M1/16 GB o Windows integrado-GPU.

### Validación

- Se agregó verificación determinista de fuente/manifiesto/hash de glifos y pruebas completas de cobertura de bloques comunes para 34,895 escalares Unicode en 16 páginas.
- El humo estático extendido para demostrar que el estado de rampa multilingüe de paleta/difuminado/personalizado llega al renderizador de salida WebGL2 y carga solo las páginas de atlas requeridas.
- Informes de rendimiento de la interfaz de usuario ampliados con configuración de funciones solicitadas, recuentos de reemplazo de renderizador, restablecimientos de fotogramas y selección de backend real.
- Los puntos de referencia de densidad ahora fallan en su proceso cuando una ejecución secundaria no cumple con su contrato FPS o excede el presupuesto de deriva de memoria estable; un informe fallido ya no se puede imprimir desde un comando de evaluación comparativa exitoso.
- Matemáticas de renderizado, verificación de atlas, humo estático optimizado, humo Pop Out nativo y las 48 pruebas Rust pasan localmente. WebGPU no fue expuesto por la vista web local macOS durante la ejecución de aceptación optimizada, por lo que volvió a WebGL2 y no se reclama como resultado de rendimiento local de WebGPU.

## [0.9.10] - 2026-08-26

### Cambiado

- Se reemplazó el ícono de la aplicación de televisión heredada con la nueva marca de reproducción y píxel de neón en los recursos macOS, Windows, Linux, iOS y Android generados por Tauri.
- Se agregó una fuente de ícono RGBA canónica de 1024px y un comando de generación única; Los archivos de íconos específicos de la plataforma son resultados generados en lugar de fuentes de arte independientes.

### Corregido

- La aceptación de la interfaz de usuario de la versión publicada ahora reconoce ambos estados válidos de Reports: la etiqueta `Reports` vacía y la etiqueta de recuento pendiente. Un informe pendiente válido ya no hace que la aceptación de Windows o Linux rechace artefactos de lanzamiento inmutables que de otro modo funcionarían.

### Validación

- Se agregó una verificación de íconos multiplataforma que regenera todos los activos de íconos Tauri de la fuente canónica y compara su contenido de imagen decodificado y compuesto alfa. Las cargas útiles PNG dentro de los contenedores ICO e ICNS están normalizadas para que la compresión específica de la plataforma, los datos RGB transparentes, el orden de los contenedores y los finales de línea XML generados no enmascaren los cambios en las ilustraciones. Una tolerancia de píxeles estrechamente limitada cubre diferencias menores de remuestreo entre plataformas y rechaza la deriva visible.
- Las puertas de escritorio y de lanzamiento ahora ejecutan la verificación de coherencia de los íconos antes de compilar o empaquetar la aplicación.

## [0.9.9] - 2026-08-26

### Corregido

- El control Reports de la barra superior ahora permanece visible en las compilaciones Tauri cuando la cola de fallos está vacía, por lo que los usuarios pueden revisar las preferencias existentes `ask`, `always` y `off` sin esperar a que se produzca un error. Los informes pendientes aún añaden un recuento y un estado de advertencia; Enviar y Descartar permanecen deshabilitados con una cola vacía.
- Se eliminó la lectura duplicada del backend del lado derecho de la barra superior. El selector de backend central sigue siendo el control canónico, mientras que el Stats Overlay, propiedad del usuario, continúa informando el backend en tiempo de ejecución resuelto.
- Los detectores de humo de la interfaz de usuario del actualizador empaquetado ahora se vinculan antes de la inicialización del dispositivo, por lo que las solicitudes tempranas de humo no pueden acelerar el inicio de la cámara o el audio.

### Seguridad

- Los informes siguen conteniendo únicamente datos de accidentes limitados y desinfectados. Los diagnósticos de medios locales y los registros arbitrarios no se adjuntan ni envían.
- Se agregó un canario de aceptación de retransmisión de fallas de producción opcional que se niega a ejecutarse cuando algún informe de usuario ya está pendiente y envía solo una carga útil sintética codificada.

### Validación

- Se agregaron pruebas de estado deterministas de la interfaz de usuario de informes de fallas para los estados del navegador, vacío, pendiente, deshabilitado y ocupado.
- El humo de liberación estática y empaquetada ahora requiere que el estado de backend duplicado esté ausente. El humo empaquetado macOS, Windows y Linux también requiere que el control Reports permanezca visible con una cola vacía.

## [0.9.8] - 2026-08-26

### Corregido

- Se restauró el control de producción Update y la verificación de inicio automático otorgando a la ventana principal el permiso limitado `core:app:allow-name` utilizado para verificar la identidad de la aplicación de producción. El permiso faltante provocó que el área de control y estado parpadeara y luego desapareciera en 0.9.6 y 0.9.7.
- Las fallas de disponibilidad del actualizador ahora registran su causa en lugar de fallar silenciosamente.

### Cambiado

- La versión CI ahora resuelve una confirmación de etiqueta inmutable, requiere el flujo de trabajo de inserción principal `Desktop` exacto para que esa confirmación tenga éxito y crea el tiempo de ejecución FFmpeg y el binario de la aplicación Tauri en paralelo.
- La agrupación restaura los artefactos exactos del flujo de trabajo de un día. FFmpeg mantiene sus comprobaciones de fuente/hash/recursos anclados, mientras que la transferencia binaria de la aplicación verifica la confirmación, la plataforma, la versión, el tamaño de bytes y SHA-256 antes de que Tauri la empaquete sin volver a compilarla.

### Validación

- Se agregaron pruebas de reutilización de versión y compilación que cubren la selección exacta de ejecución del flujo de trabajo y el rechazo de archivos binarios de aplicaciones alterados o que no coinciden.
- Smoke de versión publicada ahora inicia la aplicación empaquetada en macOS, Windows y Linux y requiere que el control Update permanezca visible, cubriendo la ruta real de la interfaz de usuario en lugar de invocar solo el actualizador nativo directamente.

## [0.9.7] - 2026-08-26

### Añadido

- La aplicación de escritorio de producción ahora realiza una verificación de metadatos de versión sin bloqueo para los paquetes de actualización firmados cada vez que se abre. Las comprobaciones de versión actual y de inicio fuera de línea permanecen silenciosas; Aparece una versión más nueva a través del control Update de la barra superior existente. Una regresión de la capacidad de producción impidió que ese control permaneciera disponible hasta la corrección 0.9.8.
- El control manual Update permanece disponible para una nueva verificación inmediata, y la descarga, instalación y reinicio siguen siendo iniciados explícitamente por el usuario.

### Corregido

- Las descargas de fuentes de versiones ahora reintentan fallas de transporte transitorias limitadas y promueven solo archivos tar FFmpeg completados antes de la verificación SHA-256 anclada.
- El envío automático de lanzamiento de escritorio ahora reintenta fallas transitorias de la API GitHub con retroceso limitado.

### Seguridad

- Las comprobaciones automáticas reutilizan el punto final del actualizador Tauri existente y los artefactos firmados. No envían medios, cámaras, audio, ajustes preestablecidos, MIDI, informes de fallas o datos de ruta local, y las versiones de desarrollo continúan deshabilitando los puntos finales del actualizador de producción.

### Validación

- Se agregó cobertura determinista del actualizador-controlador para una verificación por inicio, resultados silenciosos actuales/fuera de línea, descubrimiento de actualizaciones sin instalación automática, respaldo manual, progreso de descarga y transferencia de reinicio.

## [0.9.6] - 2026-08-17

### Cambiado

- El macOS nativo Pop Out ahora convierte y carga un fotograma fuente RGB decodificado solo cuando cambia su versión del fotograma fuente. El enlace de visualización puede continuar presentando y aplicando parámetros visuales/de audio en vivo al actualizar la pantalla sin cargar nuevamente el mismo cuadro de video.
- WebGPU reutiliza almacenamiento de respaldo uniforme, vistas de textura y grupos de enlace estables; El enlace de textura externa de vídeo y navegador por fotograma permanece dinámico según sea necesario.
- WebGL2 resuelve las ubicaciones uniformes del sombreador durante la inicialización en lugar de buscar las 18 ubicaciones en cada cuadro renderizado.
- Las transiciones numéricas preestablecidas/WTF actualizan solo los controles cuyos valores están cambiando. Las listas de fuentes, las opciones de cámara, la visibilidad, los medidores y el resto de la superficie de control se sincronizan una vez al finalizar, en lugar de en cada cuadro de animación.
- La prueba de humo de rendimiento de la interfaz de usuario optimizado utiliza valores predeterminados limpios y objetivos de transición no estructurales fijos, registra P10/P50 así como el FPS promedio, informa los backends realmente visitados y acepta un paquete de aplicaciones exacto a través de `ASCILINE_SOURCE_APP` para comparaciones de versiones.
- Avanzó la versión de escritorio/paquete a 0.9.6. MIDI sigue siendo experimental mientras se completa la puesta en servicio física del UC-33e/mioXC.
- Los comandos normales de desarrollo y depuración de paquetes de Tauri ahora usan `ASCII VJ Remix Dev` con el identificador de paquete `com.asciline.remix.dev`. El nombre de producción y el identificador `com.asciline.remix` siguen siendo exclusivos del embalaje de lanzamiento.
- macOS DMG mantiene Tauri como su único empaquetador, hace explícito el diseño estándar de aplicación a aplicaciones y documenta el DMG como el instalador manual principal. El `.app.tar.gz` sigue siendo un artefacto de actualización.

### Corregido

- Se corrigió la guía de puesta en servicio del UC-33e para usar el modo de botón extendido 146 para distintos valores de presión/liberación. Una asignación CC estándar simple alterna entre dos valores y no proporciona los límites momentáneos esperados por la aplicación.
- Se aclaró que Control Select es el único botón físico `SELECT` y se agregaron pasos exactos de programación, almacenamiento, captura/restauración de SysEx y verificación en el panel frontal.

### Rendimiento

- En la versión de prueba optimizada de macOS Apple Silicon, un video de 24 FPS se presentó en 60 FPS en Pop Out nativo con aproximadamente 23,8 cargas de origen y 36,3 saltos de carga por segundo: aproximadamente el 60 % del trabajo de conversión/carga duplicado anterior se eliminó mientras que la presentación permaneció en 60,1 FPS.
- Las fases constantes de construcción optimizada se mantuvieron con calidad equivalente y sin regresión: la referencia 0.9.5 publicada midió 35,8 FPS principal / 39,3 FPS con Pop Out, mientras que el candidato 0.9.6 final midió 38,6 / 39,0 FPS y mantuvo 35,9 FPS durante su reparación. fase de transición numérica.
- El arnés de humo estático ahora afirma que una transición numérica no realiza más de dos sincronizaciones de control de fuente y una sincronización de cámara/visual completa, en lugar de repetir el trabajo completo de la interfaz de usuario durante toda la interpolación.
- El código del sombreador de renderizado, el muestreo, el procesamiento del color, la matemática de glifos, la resolución de salida, el código fuente FPS y los controles de calidad no se modifican.

### Seguridad

- Se eliminó la sincronización del corredor local en `/Applications/ASCII VJ Remix.app`. El ejecutor ahora acepta solo el identificador del paquete de desarrollo y rechaza la firma ad hoc de forma predeterminada, lo que evita que las reconstrucciones locales reemplacen la aplicación de producción o contaminen sus concesiones de privacidad macOS.
- Las compilaciones de desarrollo deshabilitan los artefactos del actualizador y los puntos finales del actualizador de producción.
- La validación de la versión macOS ahora requiere el identificador exacto del paquete de producción, el ID del desarrollador, el ID del equipo `PWT3Q52LZ2`, un tiempo de ejecución reforzado y un requisito designado estable basado en el equipo. Las identidades ad-hoc/solo hash de código fallan al cerrarse.
- La validación de la versión extrae la carga útil real del actualizador `.app.tar.gz` y verifica que su identidad y el requisito designado coincidan con el paquete de aplicaciones notariadas.
- La validación de la versión verifica la integridad de DMG, monta la imagen como de solo lectura en una raíz temporal privada, acepta solo la aplicación, el enlace exacto `/Applications` y los metadatos Tauri revisados (el ícono de volumen requerido más un `.DS_Store` regular opcional) y aplica la estructura de la aplicación existente y las comprobaciones de identidad de producción a la copia montada.
- El humo de lanzamiento publicado ahora requiere y revalida el DMG descargado antes de realizar el salto de actualización. La publicación se niega a reemplazar los bytes de artefactos existentes para la misma etiqueta de versión.

### Validación

- Se agregó una prueba unitaria Rust para decisiones de carga de fuentes nativas versionadas.
- Se agregó cobertura de humo del navegador para el trabajo de interfaz de usuario de transición numérica limitada.
- Análisis extendido de registros de salida nativos con tasas de carga de origen y de omisión de carga.
- Se agregó cobertura de unidad multiplataforma para el análisis de identidad de firma de código macOS y el rechazo de artefactos ad-hoc, de identificador incorrecto, de equipo incorrecto y de requisitos modificados.
- Se agregaron pruebas de contrato de estructura de aplicación montada, punto de montaje, descubrimiento de artefactos y diseño DMG multiplataforma.
- Se agregó un trabajo de humo de la versión publicada macOS 26 que compara los requisitos de ID de desarrollador consecutivos, realiza un reemplazo del actualizador basado en la aplicación y revalida la identidad del paquete actualizado.
- Se validó la compilación optimizada de `.app` más renderizado estático, matemáticas del renderizador, reactividad de audio, los 188 enlaces predeterminados de MIDI, política Tauri y 47 pruebas de Rust en macOS Apple Silicon.
- Creó y montó una aplicación local 0.9.6/canario DMG optimizado y pasó la verificación de paquete/recurso/diseño compartido. Este artefacto local está firmado ad hoc; El canario final firmado y certificado por notario con la identificación del desarrollador sigue siendo necesario antes de la publicación.

## [0.9.5] - 2026-08-04

### Añadido

- Se agregaron 23 ajustes preestablecidos de caracteres de solo lectura inspirados en ascii.today, incluidos Broadway KB, Computer, Doom, Ghost, Modular, Standard, Univers y Doh.
- Se agregó un catálogo de juego de caracteres delimitado compartido con metadatos de fuente/autor y entradas de menú de juego de caracteres coincidentes para cada nuevo ajuste preestablecido.
- Se agregaron notas de adaptación y fuente acreditadas en `docs/ASCII_TODAY_PRESETS.md`.
- Se agregó entrada/salida experimental nativa multiplataforma MIDI a través de Rust `midir`, con CoreMIDI como el backend principal macOS Apple Silicon y los backends compatibles Windows y Linux conservados para CI y futura validación de hardware.
- Se agregó Evolution/M-Audio UC-33e a través de iConnectivity mioXC como el primer perfil de hardware experimental. La entrada USB directa del UC-33e permanece fuera del alcance.
- Se agregaron cuatro páginas completas de 47 controles: Visual, Audio, Presets y Fine/User.
- Se agregó toma de control suave, fusión de entradas, curvas, compatibilidad con inversión/rango, anulaciones de aprendizaje MIDI, monitoreo de puertos y reconexión automática de mioXC.
- Se agregaron ranuras preestablecidas estables MIDI del 1 al 128 con entrada numérica, acciones Intro, Anterior, Siguiente y Borrar.
- Se agregó un panel de escritorio MIDI con estado de entrada/salida, página activa, monitor de último mensaje, restablecimiento de mapeo, captura de perfil, instalación/restauración y acciones de verificación.
- Se agregó captura de SysEx de banco completo limitada y restauración de ritmo a través de la conexión DIN de retorno mioXC, además de Ensure Profile on Connection opcional.
- Se agregó una sonda física de descubrimiento/conexión mioXC y un mapa de controlador imprimible completo en `docs/MIDI_UC33E.md`.

### Cambiado

- El glifo nativo Pop Out ahora consume la rampa de caracteres compartidos resueltos y la acepta solo cuando está en el espacio, es única, está delimitada y está completamente cubierta por el atlas de glifos integrado fijo.
- La puesta en servicio del hardware MIDI se pausa explícitamente después de confirmar las identificaciones del controlador para el teclado C34–C43 y el transporte C44–C47. El software sigue implementado; el trabajo restante de restauración y aceptación física se registra en la hoja de ruta.
- MIDI está etiquetado como experimental en la interfaz de usuario y en la documentación porque el barrido de control físico completo y la lista de verificación de restauración/verificación de extremo a extremo de SysEx permanecen incompletos. Ensure Profile on Connection permanece deshabilitado de forma predeterminada.
- Los controles de la interfaz de usuario y MIDI ahora se dirigen a través de los mismos rangos de parámetros canónicos, sujeción, manejo de cambios estructurales, configuraciones de audio y comportamiento de transición preestablecido.
- Los cambios preestablecidos visuales rearman la toma de control suave para que los controles UC-33e no motorizados no puedan saltar a través del valor de software activo.
- MIDI está restringido intencionalmente a parámetros visuales, configuraciones audio-reactivas, ajustes preestablecidos visuales y WTF mode. No puede cambiar fuentes, cámara, Pop Out ni pantallas de salida.

### Seguridad

- Los comandos MIDI y SysEx se otorgan únicamente a la ventana de control principal. La ventana de salida de solo presentación no recibe permisos MIDI.
- El adaptador nativo inicial acepta solo puertos cuyos nombres contengan `mioXC`.
- Las colas MIDI, los recuentos de paquetes SysEx, los bytes decodificados, las asignaciones almacenadas y las ranuras preestablecidas están delimitadas y validadas.
- Los perfiles de controlador capturados permanecen locales y no contienen rutas de medios, marcos, audio, credenciales ni datos de red.

### Validación

- Comprobaciones matemáticas de renderizado ampliadas para cubrir las 23 nuevas entradas del catálogo, incluidos identificadores, límites, unicidad, glifos imprimibles, metadatos de atribución y búsqueda de luminancia de Broadway KB.
- Cobertura de humo estático extendida para requerir nombres ascii.today tanto en el control del conjunto de caracteres como en el panel de ajustes preestablecidos integrado.
- Se agregó cobertura Rust para la aceptación y rechazo de la rampa de caracteres nativos.
- Se agregó `npm run test:midi` para los 188 enlaces de hardware predeterminados, escalamiento de valores, soft takeover, márgenes de acción, fusión de eventos y exclusiones de alcance.
- Se agregaron pruebas Rust para el análisis de MIDI, ensamblaje fragmentado de SysEx, validación de transferencia y alcance de puerto solo mioXC.
- Se agregaron `npm run midi:probe` y `npm run midi:probe -- --connect` para el puerto físico CoreMIDI y validación simultánea de entrada/salida.
- Cobertura de humo estático extendida para validar el enrutamiento de destino visual/audio canónico MIDI y garantizar que el modo de navegador mantenga oculto el panel MIDI solo de escritorio.
- Se ampliaron las comprobaciones de la política Tauri para exigir permisos MIDI en la ventana principal y prohibirlos en la ventana de salida.

## [0.9.3] - 2026-06-26

### Añadido

- Se agregaron futuras herramientas de firma Windows a través de Azure Artifact Signing y Windows `signCommand` de Tauri; la ruta de lanzamiento activa 0.9.3 Windows sigue siendo una vista previa sin firmar.
- Se agregó la herramienta de verificación Windows Authenticode para futuros artefactos de lanzamiento firmados, incluidas verificaciones de firmante y marca de tiempo.
- Se agregó `src-tauri/tauri.windows-signed.conf.json` para futuros trabajos de lanzamiento firmados de Windows, manteniendo la configuración predeterminada adecuada para el desarrollo local y la vista previa sin firmar 0.9.3 Windows.
- Se agregó un módulo reactivo de audio compartido para valores predeterminados, metadatos de control, ajustes preestablecidos, normalización de funciones, amortiguación de mezcla densa y modulación de parámetros de renderizado.
- Se agregaron controles audiorreactivos para cantidad de transitorio/flujo, cantidad de presencia, amortiguación de densidad y nivel de ruido.
- Se agregaron medidores de flujo y densidad, además de un ajuste preestablecido audio-reactivo de Dense Mix Control.
- Se agregaron canales de funciones de audio limitados para medios bajos, medios altos, presencia, brillo y densidad en las rutas de audio nativas y del navegador.

### Cambiado

- Las versiones públicas de macOS ahora requieren la firma y certificación notarial del ID del desarrollador en lugar de recurrir a la firma ad hoc.
- Los artefactos de la versión Windows 0.9.3 se publican como compilaciones preliminares sin firmar hasta que se pruebe SignPath Foundation, Azure Artifact Signing u otro backend de firma.
- La versión CI mantiene las credenciales de firma en el ámbito de los pasos de firma y proporciona al trabajo de publicación el único token GitHub con capacidad de escritura.
- La detección de ritmos audiorreactivos es más conservadora durante pasajes densos y de banda ancha, al tiempo que conserva una fuerte respuesta para transitorios escasos.
- La configuración de audio predeterminada de Pulse Reactor es más fuerte y menos amortiguada, por lo que las pistas modestas o densas aún producen movimiento visible sin cambiar los ajustes preestablecidos guardados por el usuario.
- Los rangos de controles deslizantes reactivos al audio existentes se amplían con navegadores compatibles y abrazaderas nativas.
- La vista previa del navegador, Pop Out, las rutas de transmisión y la salida nativa ahora consumen las mismas reglas de modulación reactiva de audio compartidas.
- La cámara en vivo Pop Out mantiene la ruta rápida de la cámara nativa para ajustes preestablecidos de glifos, sólidos y píxeles; El transporte espejo del navegador permanece reservado para fuentes alternativas donde la captura nativa no está disponible.
- Pop Out nativo ahora desactiva el enmascaramiento de glifos para los ajustes preestablecidos de estilo WebGL/WebGPU, de modo que los ajustes preestablecidos que no son Canvas2D mantengan la misma forma de celda sólida que la vista previa principal.
- Las transiciones estáticas de video/cámara ahora pueden realizar un fundido cruzado entre los renderizadores de glifos GPU, sólido/píxel y Canvas2D sin destruir la fuente de medios compartida.
- Los ajustes preestablecidos tradicionales de Canvas2D ASCII ahora utilizan de forma predeterminada la fluctuación de imagen estática visible y migran las copias guardadas con fluctuación cero de esas funciones integradas.
- WTF mode ahora permite que los anclajes ASCII/glifo usen su backend Canvas2D nuevamente, por lo que las transiciones aleatorias de sólido a glifo son visibles en lugar de convertirse en variantes de celda sólida de GPU.

### Corregido

- Se corrigió un modo WTF `ReferenceError` cuando los ajustes preestablecidos de sólidos/píxeles desviaban el siguiente objetivo aleatorio hacia los ajustes preestablecidos de anclaje ASCII tradicionales.
- Se corrigieron los permisos de limpieza del detector de eventos Tauri para la ventana principal y se hizo que el rechazo nativo de la limpieza del detector cercano Pop Out fuera seguro, evitando los informes de fallas de `event.unlisten not allowed`.

### Seguridad

- La firma futura Windows utiliza credenciales de firma de ámbito ambiental y no confirma archivos de certificado, secretos de cliente ni material de firma privado.
- La reactividad de audio todavía envía solo vectores de características acotados a través de IPC; El audio sin formato, los fotogramas, los archivos multimedia y las rutas permanecen locales.
- Las comprobaciones de firma de versiones y de firmas de actualizadores ahora tratan la distribución pública de macOS como una ruta cerrada ante fallas. Los artefactos Windows 0.9.3 son vistas previas explícitamente sin firmar.

### Validación

- Se agregó `npm run test:audio-reactive`.
- Se agregó `npm run check:windows-authenticode`.
- `npm run check:desktop` y `npm run check:release` ahora incluyen las pruebas auxiliares audiorreactivas.
- La cobertura de humo estático ahora afirma que los ajustes preestablecidos de la cámara en vivo no recurren al transporte en espejo de forma predeterminada.
- La cobertura de humo estático ahora afirma que el enmascaramiento de glifos nativos sigue la familia de backend activa en lugar de filtrar la salida de glifos de estilo Canvas2D en los ajustes preestablecidos de GPU.
- La cobertura de humo estático ahora afirma que las transiciones de vídeo de sólido a glifo mantienen la reproducción activa en lugar de pausarla durante las reconstrucciones de la familia de renderizadores.
- La cobertura de humo estático ahora afirma que los objetivos sólidos/píxeles de WTF pueden sesgarse de manera determinista en anclajes ASCII sin lanzarse.
- La cobertura de humo estático ahora afirma que los ajustes preestablecidos tradicionales de Canvas2D ASCII animan su fluctuación de imagen estática predeterminada y exponen el control de fluctuación.
- Las comprobaciones de políticas Tauri ahora requieren permiso de limpieza de eventos de la ventana principal y mantienen ese permiso fuera de la ventana de salida de solo presentación.

## [0.9.2] - 2026-06-25

### Añadido

- Se agregó un informe de fallas solo de producción para errores de front-end, rechazos no controlados, fallas del comando Tauri e informes de gancho de pánico Rust.
- Se agregaron preferencias de informes de fallos revisados/desinfectados: preguntar, enviar siempre y desactivar.
- Se agregó un relé de fallas Cloudflare Worker en `crash.dustwave.xyz` que limita la ingesta, desinfecta cargas útiles, informes de huellas digitales y crea o actualiza problemas agregados de GitHub a través de una aplicación GitHub.
- Se agregó una plantilla de informe de fallas GitHub y un flujo de trabajo de implementación de retransmisión de fallas.
- Se agregaron vectores matemáticos de renderizador compartido que cubren el procesamiento de color GPU y el comportamiento de color heredado de Canvas/stream.

### Cambiado

- El envío del informe de fallos de Tauri ahora se ejecuta únicamente desde Rust; la vista web no obtiene capacidad HTTP arbitraria.
- La ventana de salida sigue siendo solo de presentación y no recibe comandos de informe de fallas.
- La agregación de retransmisión de fallos ahora agrupa por dimensiones de fallo estables, incluida la plataforma y los campos de código de error explícito cuando están presentes, antes de recurrir a la pila normalizada o la coincidencia de mensajes.
- El lienzo del navegador y las imágenes de la transmisión se conservan intencionalmente. El trabajo de consolidación 0.9.2 extrae primero los ayudantes y pruebas compartidos en lugar de cambiar la salida numérica.
- Los ayudantes de color/hash/conjunto de caracteres del renderizador ahora se encuentran en `renderers/shared/` para su reutilización por el código de la aplicación y las pruebas.

### Seguridad

- Los informes de fallos se delimitan y desinfectan antes del almacenamiento o envío local. No se incluyen archivos multimedia, fotogramas, audio sin formato, rutas completas, tokens, cookies ni valores de entorno privado.
- El envío de informes de fallas en la red está deshabilitado para compilaciones que no son de producción o de depuración.
- Las credenciales GitHub residen únicamente en los secretos Cloudflare Worker; No hay ningún token GitHub integrado en la aplicación de escritorio.

### Validación

- Se agregaron `npm run test:render-math` y `npm run test:crash-relay`.
- `npm run check:desktop` y `npm run check:release` ahora incluyen retransmisión de fallos y comprobaciones matemáticas del renderizador.

## [0.9.1] - 2026-06-24

### Añadido

- Se agregaron ajustes preestablecidos tradicionales de estilo ASCII:
  - Cámara clásica ASCII.
  - Papel periódico ANSI.
  - Terminal mono.
  - Máquina de escribir densa.
- Se agregó un conjunto de caracteres de cámara clásica inspirado en la pequeña rampa de luminancia utilizada por `idevelop/ascii-camera`.
- Se agregó representación de glifos nativos `wgpu` Pop Out para los ajustes preestablecidos de `glyphMode`:
  - La salida nativa ahora acepta `glyphMode` y `charset` de los parámetros de renderizado canónicos.
  - La salida nativa de GPU utiliza un atlas de glifos de mapa de bits fijo y una rampa de juego de caracteres.
  - La representación de prueba/respaldo del software nativo utiliza la misma lógica de rampa de glifos.
- Se agregó cobertura Rust para el análisis de metadatos de glifos nativos, diseño de representación uniforme y salida de máscara de glifos.

### Cambiado

- Los ajustes preestablecidos de ASCII tradicionales seleccionan Canvas2D para la vista previa principal, de modo que los glifos sean visibles inmediatamente en la imagen de demostración, el video de demostración, los medios personalizados y las fuentes de la cámara, mientras que el Pop Out nativo representa máscaras de glifos coincidentes.
- WTF mode ahora puede anclar objetivos aleatorios seguros en vivo alrededor de los ajustes preestablecidos tradicionales de ASCII, así como de las familias de ajustes preestablecidos extremos.
- Los menús de selección de conjunto de caracteres y familia de fuentes ahora utilizan el diseño de selección compacto utilizado por los controles de reactividad de audio.
- La salida nativa ahora conserva el estilo de texto/glifo para medios estáticos y fuentes de cámara única en lugar de aplanar los ajustes preestablecidos de glifo en bloques de celdas sólidos.
- La cobertura de humo estático ahora afirma que el grupo Glifo/Celda permanece visible y compacto mientras renderiza los nuevos ajustes preestablecidos ASCII tradicionales.
- Redacción de diagnóstico de medios reforzada para rutas locales integradas y tamaño de mensaje de diagnóstico limitado.

## [0.9.0] - 2026-06-23

### Añadido

- Se cambió el nombre y se posicionó la aplicación como ASCII VJ Remix.
- Se cambió el nombre de la identidad del repositorio/paquete a `ascii-vj-remix` y se actualizaron las referencias remotas/actualizadoras de GitHub.
- Se agregó un shell de aplicación de escritorio Tauri v2 alrededor del laboratorio de renderizado.
- Se agregó una canalización de compilación Vite para que la misma interfaz básica pueda ejecutarse en un navegador o dentro de la aplicación de escritorio empaquetada.
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
- Se agregaron controles densos de renderizado en vivo para cuadrícula, filas, dimensiones de celda, color, brillo, contraste, gamma, combinación de fondo, cuantificación, fluctuación, posición de muestra, suavizado, FPS, modo de glifo/celda y estado de rendimiento.
- Se agregaron ajustes preestablecidos visuales incorporados, que incluyen un conjunto más amplio de apariencias de extrema fluctuación, alto contraste, alta saturación, columna baja, gamma baja y gamma alta.
- Se agregaron flujos de trabajo preestablecidos para guardar, copiar, actualizar, eliminar, importar y exportar preestablecidos por el usuario.
- Se agregaron transiciones preestablecidas suaves con interpolación numérica y fundidos cruzados de la superficie del renderizador.
- Se agregó WTF mode para transiciones aleatorias continuas y seguras en vivo.
- Se agregó un Stats Overlay que muestra el ajuste preestablecido actual, la fuente, el backend, la cuadrícula, el FPS, el tiempo de transición y el estado de reactividad de audio.
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
  - Ruta de captura nativa de una sola cámara macOS a través de AVFoundation para baja latencia de cámara en Pop Out.
  - selección de pantalla de salida y pruebas de simulación de pantalla secundaria.
- Se agregó selección de medios de escritorio solo local a través de un cuadro de diálogo Tauri y un registro de medios con ámbito de sesión.
- Se agregó una política de seguridad de contenido de producción y capacidades divididas de Tauri.
- Se agregó la infraestructura del actualizador de versiones GitHub.
- Se agregó la firma de aplicaciones macOS ad-hoc como alternativa local/de versión predeterminada.
- Se agregó una estructura opcional del flujo de trabajo de certificación notarial de ID de desarrollador para uso futuro.
- Se agregó la política de creación y preparación del sidecar FFmpeg para el trabajo del motor de medios independiente.
- Se agregaron segmentos del motor multimedia Rust para sondeo/decodificación FFmpeg, preparación de fotogramas y validación de codificación de flujo adaptable.
- Se agregaron pruebas estáticas de humo del navegador, pruebas de visualización de resultados, pruebas de manifiesto del actualizador, comprobaciones de políticas de recursos FFmpeg, comprobaciones de paridad de medios y pruebas Rust.
- Se agregaron documentos de práctica de proyectos para seguridad, rendimiento, pruebas, accesibilidad e internacionalización.

### Cambiado

- La interfaz de usuario de origen normal ahora expone fuentes locales estáticas en lugar de un selector estático/transmisión visible.
- El panel Fuente ahora muestra solo entradas Demo Image, Demo Video, Cámara y archivos personalizados.
- Los controles de la cámara ahora aparecen directamente debajo de Fuente cuando la cámara está activa.
- La interfaz de usuario de solo transmisión, como el recuento de búfer y el estado de la conexión de transmisión en la parte superior derecha, está oculta del uso normal de estática, cámara o archivos.
- Los ajustes preestablecidos y WTF mode ya no alternan entre Stats Overlay a menos que el usuario cambie esa configuración directamente.
- Las transiciones preestablecidas preservan la fuente de medios activa y el tiempo de reproducción de video cuando la fuente no cambia.
- La aplicación ahora está documentada como una herramienta creativa independiente y local en lugar de solo como una bifurcación del servidor de transmisión ASCILINE.
- El tema de la interfaz de usuario ahora utiliza superficies negras y grafito con acentos activos blancos, estados listo/encendido en azul neón y estados de advertencia/WTF/actualización en rosa neón en lugar de la paleta anterior predominantemente azul, al tiempo que conserva la densidad de control compacta y los acentos de estado de alto contraste.

### Desarrollo y lanzamiento

- Node.js 24 es el tiempo de ejecución básico de JavaScript.
- La versión CI se basa en macOS, Windows y Linux.
- Las compilaciones de CI de lanzamiento revisaron los sidecars FFmpeg/ffprobe de la fuente oficial fijada FFmpeg con protocolos de red deshabilitados.
- La clave privada del actualizador es intencionalmente externa y debe proporcionarse a través de `TAURI_SIGNING_PRIVATE_KEY`.
- La clave del actualizador está protegida por contraseña; La automatización de lanzamientos ahora también requiere `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`.
- Las compilaciones locales de macOS pueden utilizar una identidad autofirmada estable para una mejor reutilización de los permisos TCC durante el desarrollo.

### Limitaciones conocidas

- El modo de transmisión existe como infraestructura heredada/de desarrollo, pero está oculto de la interfaz de usuario de origen normal hasta que el flujo de trabajo independiente esté completamente productivo.
- El control de hardware MIDI está planificado pero no se incluye en 0.9.0.
- La firma y la certificación notarial del ID de desarrollador de Apple se aplazan.
- El comportamiento de Linux WebGPU depende en gran medida de WebKitGTK, los controladores de Mesa/proveedor y el paquete de distribución; WebGL2 puede ser el recurso práctico de Linux.
- La compatibilidad con MKV depende de la ruta del decodificador de plataforma activa.
- El comportamiento de captura de audio del sistema/pantalla varía según el sistema operativo y el navegador.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
