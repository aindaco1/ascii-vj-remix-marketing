---
title: Registro de cambios
description: Documentación de registro de cambios derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Referencia
lang: es
---

# Registro de cambios

La versión 0.9.3 traslada las versiones de escritorio públicas a macOS firmada/notariada
distribución, publica Windows como una vista previa sin firmar mientras se firma
diferido y amplía la reactividad del audio con controles de mezcla densa que reducen
reacción exagerada ante la música ocupada. La versión 0.9.0 sigue siendo la primera documentación.
línea de base para el conjunto de características actual ASCII VJ Remix.

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

- Se corrigió un modo WTF `ReferenceError` cuando los ajustes preestablecidos de sólidos/píxeles sesgaban el siguiente
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
- Se agregó representación de glifos nativos `wgpu` Pop Out para ajustes preestablecidos de `glyphMode`:
  - La salida nativa ahora acepta `glyphMode` y `charset` del formato canónico.
parámetros del renderizador.
  - La salida nativa de GPU utiliza un atlas de glifos de mapa de bits fijo y una rampa de juego de caracteres.
  - La representación de prueba/retroceso del software nativo utiliza la misma lógica de rampa de glifos.
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
