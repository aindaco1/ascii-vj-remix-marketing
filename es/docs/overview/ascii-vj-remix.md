---
title: ASCII VJ Remix
description: Documentación de ASCII VJ Remix derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Resumen
lang: es
---

# ASCII VJ Remix

Los documentos fuente actuales describen las funciones de **1.0.3**. Las secciones siguientes proceden directamente del repositorio principal para mantener una sola referencia sobre el producto, los requisitos y las recomendaciones de hardware.

<a id="what-this-project-is"></a>

## ¿Qué es este proyecto?

ASCII VJ Remix combina varias ideas de herramientas de escritorio y renderizador:

- Comenzó con [ASCILINE](https://github.com/YusufB5/ASCILINE), que proporciona una canalización de transmisión de video ASCII de alto rendimiento, código de servidor Python/FastAPI, preparación de cuadros OpenCV, codificación de cuadros WebSocket adaptable, experimentos de reproducción de terminal y respaldos de renderizado de Canvas.
- Incluye renderizado WebGPU/WebGL de alta calidad junto con rutas de compatibilidad de Canvas.
- Mantiene el espíritu local de una herramienta creativa independiente. La aplicación Tauri incluye el renderizador, los medios de demostración, las fuentes, la ruta de salida nativa y los adaptadores de medios locales para que el uso diario no requiera servicios en línea.
- Utiliza una superficie de control VJ extremadamente negra, blanca, gris, rosa neón y azul neón con tipografía compacta estilo VCR y controles rectangulares nítidos.

El resultado es un banco de trabajo de renderizado en vivo para salida de video celular/ASCII estilizada.

<a id="system-requirements"></a>

## Requisitos del sistema

Estos requisitos son una guía práctica para el renderizador actual, no un contrato. Los tamaños de cuadrícula más altos, las cámaras múltiples, la reactividad de audio y las ventanas de salida nativas aumentan la carga.

### macOS

|Nivel|Requisito|
| --- | --- |
|Mínimo|Apple M1 o posterior, macOS 13 Ventura o posterior, 16 GB de RAM, GPU compatible con Metal, 2 GB de espacio libre en disco. Las compilaciones oficiales de macOS son las primeras de Apple Silicon.|
|Óptimo|M1 Pro/Max, M2 Pro/Max, M3 Pro/Max o más reciente; 16 GB de RAM o más; macOS 14 Sonoma, macOS 15 Sequoia o más reciente; Pantalla/proyector externo para Pop Out.|

Notas:

- La compatibilidad con Intel Mac no es el objetivo de lanzamiento actual. Puede funcionar desde el código fuente si usted mismo crea un paquete compatible, pero no es la ruta probada.
- La cámara, el micrófono y la captura de audio requieren concesiones de privacidad explícitas macOS.
- Las versiones públicas de macOS están firmadas con el ID del desarrollador, certificadas ante notario, grapadas y aceptadas por Gatekeeper. Las compilaciones locales o de prueba pueden requerir el flujo normal de macOS, hacer clic con el botón derecho en Abrir o Abrir de todos modos.

### Windows

|Nivel|Requisito|
| --- | --- |
|Mínimo|Windows 10 22H2 o Windows 11, x64 CPU, tiempo de ejecución WebView2, GPU integrado ampliamente comparable a los gráficos Apple M1 con soporte D3D12 o WebGL2, 16 GB de RAM, 2 GB de espacio libre en disco.|
|Óptimo|Windows 11, Intel/AMD/NVIDIA GPU reciente con controladores actuales, 16 GB de RAM o más, decodificación de medios de hardware, pantalla de salida dedicada.|

Notas:

- La mayoría de los sistemas Windows 10/11 actuales ya incluyen WebView2. Si un instalador informa que falta WebView2, instale Microsoft WebView2 Runtime una vez.
- Pop Out con una sola cámara usa Media Foundation y el renderizador nativo D3D12 en Windows cuando están disponibles; conserva la duplicación acotada como alternativa ante incompatibilidades del dispositivo o controlador. Un único cliente nativo captura para ambas vistas, evitando intentos fallidos de apertura simultánea y nuevas aperturas al cambiar de preset. También envía el último fotograma como JPEG binario de tamaño reducido al renderizador principal WebGPU, evitando que dos clientes compitan por la cámara y la serialización de RGBA sin comprimir. La captura del navegador se restaura después de que el hilo nativo libere por completo el dispositivo. Los cambios de fuente completan este traspaso antes de iniciar el siguiente preview.
- El loopback de audio del sistema WASAPI nativo no está implementado. El comportamiento actual del audio del sistema/pantalla depende de la ruta de captura expuesta por el tiempo de ejecución; verifíquelo en la máquina de destino antes de una sesión en vivo.

### Linux

|Nivel|Requisito|
| --- | --- |
|Mínimo|Distribución moderna x86_64 Linux, tiempo de ejecución WebKitGTK 4.1, controladores Mesa o GPU del proveedor con WebGL2, 8 GB de RAM, 2 GB de espacio libre en disco.|
|Óptimo|Ubuntu 24.04, Fedora 44, Arch o distribución actual comparable; Wayland o X11 bien configurado; controladores recientes de Mesa/NVIDIA; GPU compatible con Vulkan.|

Notas:

- Linux Tauri utiliza la pila del sistema WebKitGTK, por lo que la compatibilidad con la función GPU varía según la distribución, la versión de WebKitGTK y el controlador de gráficos.
- WebGL2 puede ser el recurso práctico de Linux incluso cuando WebGPU no esté disponible.
- Pop Out con una sola cámara usa captura V4L2 mediante FFmpeg local incluido y renderizado nativo Vulkan/GLES. Como muchos dispositivos V4L2 son exclusivos, el preview principal de la cámara se pausa mientras Pop Out nativo está activo y se recupera al cerrarlo.
- El comportamiento nativo de cámara/audio/salida Linux varía según la distribución y el hardware; La aceptación de paquetes de Ubuntu y Fedora sigue siendo una prueba física.

<a id="hardware-guidance"></a>

## Guía de hardware

|Nivel|Hardware|
| --- | --- |
|Mínimo|Apple M1-class o CPU integrado de 4 núcleos más/GPU integrado, 16 GB de RAM, compatibilidad con WebGL2/Metal/D3D12/Vulkan/GLES, pantalla de 1080p, una cámara o una fuente de medios local a la vez.|
|Óptimo|8 o más núcleos de rendimiento, 16 a 32 GB de RAM, Apple Silicon Pro/Max o un GPU discreto reciente, decodificación de video por hardware, almacenamiento SSD, pantalla/proyector externo, hardware de captura USB o HDMI, interfaz de audio compatible con su clase.|

Para el trabajo con cámara en vivo, la mejor actualización a menudo no es CPU sin formato. Utilice cámaras USB estables, puertos USB directos o un concentrador con alimentación, buena iluminación y una máquina con alimentación de CA.

<a id="battery-and-heat-warning"></a>

## Advertencia de batería y calor

ASCII VJ Remix puede ser exigente. La renderización de WebGPU/WebGL, un alto número de columnas, múltiples cámaras, análisis de audio y ventanas de salida nativas pueden mantener activos continuamente el CPU, el GPU, la cámara y el decodificador de medios.

En portátiles:

- Espere un mayor consumo de batería que un reproductor multimedia normal.
- Utilice alimentación de CA para actuaciones o sesiones largas.
- Columnas inferiores, FPS, resolución de la cámara y fluctuación si la máquina se calienta.
- Deje Advanced Density desactivado para el rango protegido por rendimiento; un recuento elevado de columnas puede aumentar drásticamente el total de celdas cuando las filas automáticas están activas.
- Cierre Pop Out cuando no necesite una segunda superficie de salida.
- Prefiera la imagen de demostración incorporada o un solo video cuando realice pruebas con batería.

Para instalación, permisos, privacidad y solución de problemas, utilice la [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md).



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [docs/USER_GUIDE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
