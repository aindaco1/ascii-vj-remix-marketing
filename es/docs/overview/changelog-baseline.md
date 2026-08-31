---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

# Base de la versión

Los documentos actuales describen el conjunto de características **1.0.0**. La entrada más reciente del registro de cambios con fecha es la autoridad de publicación; la sección Inédito está excluida intencionalmente.

## Notas de la versión 1.0.0

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



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
