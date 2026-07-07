---
title: Conjunto de funciones
description: Documentación del conjunto de funciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Resumen
lang: es
---

# Conjunto de funciones

Esta página describe la línea base de funciones ASCII VJ Remix actual para desarrolladores que planean bifurcaciones, puertos, integraciones o trabajo de funciones.

## Entradas de origen

- Archivos de imágenes locales.
- Archivos de vídeo locales.
- Selección de archivos MKV donde la ruta del decodificador de plataforma activa puede manejar la reproducción.
- Entrada de cámara/webcam.
- Múltiples cámaras simultáneas cuando el sistema operativo y el tiempo de ejecución permiten la captura simultánea.
- Diseños del mezclador de cámaras: cuadrícula, fila dividida, pila e imagen en imagen.
- Controles de cámara para selección de dispositivo, tamaño de captura, FPS, diseño, encuadre y espejo.
- Entradas de análisis de audio: micrófono/entrada, archivos de audio locales y audio del sistema/pantalla donde el sistema operativo lo expone a la aplicación de escritorio.

Los medios y marcos de cámara seleccionados permanecen locales. El renderizador recibe URL de medios reproducibles o identificadores registrados de sesión local; no recibe acceso amplio al sistema de archivos.

## Representación de backends

- WebGPU es el principal objetivo de calidad en tiempos de ejecución de escritorio capaces.
- WebGL2 es el principal respaldo integrado de GPU.
- Canvas2D sigue siendo la ruta de compatibilidad para la salida ASCII de estilo glifo tradicional.
- Pixel Canvas sigue estando disponible como alternativa de compatibilidad.
- El Tauri Pop Out nativo utiliza un presentador `wgpu` cuando esté disponible:
  - Metal en macOS.
  - D3D12 en Windows.
  - Vulkan/GLES en Linux.
- El Pop Out nativo conserva el modo de glifo y los parámetros del conjunto de caracteres para los ajustes preestablecidos de ASCII tradicionales en lugar de aplanarlos en celdas sólidas.

## Controles de renderizado en vivo

La aplicación mantiene la selección de fuente, ajustes preestablecidos, WTF mode, modulación de audio, salida nativa y trabajo futuro de MIDI dirigidos a través de un modelo de parámetro canónico.

Los principales grupos de control incluyen:

- Modo de fuente, ID/URL del medio, tipo de medio y nombre de la fuente.
- Identificadores de dispositivos de cámara, resolución, FPS, diseño, encuadre y espejo.
- Selección de backend: automático, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- Cuadrícula: columnas, filas, filas automáticas, dimensiones de celda y corrección de aspecto.
- Color: saturación, contraste, brillo, gamma, combinación de fondo y cuantización.
- Muestreo: FPS, cantidad de fluctuación, velocidad de fluctuación, posición de muestra y suavizado.
- Comportamiento de glifos/celdas: modo glifo, modo sólido, juego de caracteres compacto, menú de familia de fuentes e intensidad mínima de glifo.
- UI/rendimiento: superposición de estadísticas y tiempo de transición.

Las transiciones estáticas entre familias de renderizadores mantienen la propiedad de los medios en la capa de tiempo de ejecución compartida. Los renderizadores Canvas2D, pixel Canvas, WebGL y WebGPU pueden realizar fundidos cruzados sobre la misma fuente en vivo en lugar de destruir y recargar medios cuando cambia el comportamiento del backend, glifo o celda sólida.

## Preajustes

ASCII VJ Remix incluye ajustes preestablecidos visuales integrados de solo lectura y ajustes preestablecidos administrados por el usuario.

Las familias visuales integradas incluyen apariencias extremas como Neon Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder, Cyberdelic Riot, Acid Snowstorm, Terminal Collapse y Neon Razorstorm.

Los ajustes preestablecidos de ASCII tradicionales incluyen Classic Camera ASCII, ANSI Newsprint, Terminal Mono y Dense Typewriter.

Los ajustes preestablecidos del usuario se pueden guardar, duplicar, actualizar, eliminar, importar y exportar. Los ajustes preestablecidos conservan la fuente de medios activa a menos que el usuario la cambie explícitamente.

## Transiciones y modo WTF

- Las transiciones preestablecidas se funden en lugar de fundirse en negro.
- El tiempo de transición es configurable.
- Las transiciones estáticas de vídeo/cámara pueden moverse entre los renderizadores de glifos GPU, sólido/píxel y Canvas2D mientras se mantiene la reproducción en vivo.
- WTF mode cambia continuamente a través de configuraciones aleatorias de seguridad en vivo.
- WTF mode puede anclar la aleatorización tanto en familias de ajustes preestablecidos extremos como en ajustes preestablecidos ASCII tradicionales.
- Las abrazaderas seguras evitan la salida de negro puro o blanco puro durante estados aleatorios o controlados por audio.

## Reactividad de audio

La reactividad de audio está habilitada de forma predeterminada y comienza desde Mic/Entrada de forma predeterminada.

Analiza características limitadas en lugar de buffers de audio sin formato:

- RMS.
- Bajo.
- Medio-bajo.
- Medio.
- Medio-alto.
- Agudos.
- Presencia.
- Brillo.
- Densidad.
- Energía transitoria y flujo.
- Batir el pulso.
- Movimiento espectral.

Los controles de amortiguación de mezcla densa y ruido de fondo ayudan a que las pistas ocupadas se mantengan reactivas sin fijar la vibración y la respuesta de ritmo al máximo. La modulación de audio afecta los parámetros de renderizado efectivos en vivo sin reescribir los ajustes preestablecidos guardados.

## Pop Out y pantallas externas

Pop Out crea una ventana de salida separada para un proyector, una tarjeta de captura o una pantalla secundaria. La ventana de control principal permanece disponible para la sintonización en vivo.

La ventana de salida está centrada en la presentación y tiene una superficie de comando mínima. Cuando Tauri puede enumerar pantallas, la selección de pantalla de salida persiste.

## Embalaje y actualizaciones

- Construido con Tauri v2.
- El tiempo de ejecución de producción es solo local de forma predeterminada.
- GitHub La infraestructura del actualizador de versiones está configurada.
- El CI de versión pública macOS requiere artefactos firmados y notariados con el ID del desarrollador.
- Los artefactos Windows 0.9.3 son compilaciones de vista previa explícitamente sin firmar.
- El envío de informes de fallos es solo de producción, se revisa/desinfecta y se enruta a través de la capa de escritorio Rust al relé Cloudflare Worker.

## Rutas avanzadas

- El trabajo de transmisión heredado ASCILINE y las sesiones de transmisión Rust/FFmpeg más nuevas existen, pero están ocultas de la interfaz de usuario de origen normal.
- La política complementaria FFmpeg y la compatibilidad con códecs se encuentran en el trabajo del colaborador/lanzamiento.
- Está previsto el control del hardware MIDI, con un Evolution/M-Audio UC33e a través de iConnectivity mioXC nombrado como primer objetivo de validación.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
