---
title: ASCII VJ Remix
description: Documentación de ASCII VJ Remix derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Resumen
lang: es
---

# ASCII VJ Remix

ASCII VJ Remix es un laboratorio de renderizado de escritorio nativo local para convertir imágenes, videos, cámaras y señales reactivas de audio en imágenes ASCII y basadas en celdas de alto rendimiento.

Está diseñado para la experimentación al estilo VJ: elija una fuente, elija o cree un ajuste preestablecido, presione con fuerza el renderizador, muestre la salida en otra pantalla y siga ajustando la apariencia en vivo mientras los medios siguen ejecutándose.

Los documentos fuente actuales describen el conjunto de características **0.9.3**.

## Límite del producto

- El producto previsto es la aplicación de escritorio empaquetada para macOS, Windows y Linux.
- El modo Navegador/Vite es útil para el desarrollo, las pruebas de humo y la portabilidad del renderizador, pero no es el marco principal del producto.
- El tiempo de ejecución es local primero y sin conexión de forma predeterminada.
- Los medios, los fotogramas de la cámara y el audio seleccionados por el usuario siguen siendo locales.
- Las rutas en línea intencionales se limitan al actualizador de versiones GitHub y al envío de informes de fallas revisados/desinfectados solo de producción.
- La infraestructura de transmisión existe, pero la interfaz de usuario de origen normal oculta el modo de transmisión hasta que esté listo como una función de usuario independiente.
- El control de hardware MIDI está planificado, pero no forma parte del conjunto de funciones actual para el usuario normal.

## Linaje del proyecto

ASCII VJ Remix combina tres linajes de origen:

- **ASCILINE**: transmisión de video ASCII de alto rendimiento, codificación de fotogramas adaptable, experimentos de Python/OpenCV, ideas de terminales y linaje alternativo de Canvas.
- **ascii-point-and-click**: salida visual WebGPU/WebGL de alta calidad y arquitectura de fuente de medios del navegador local.
- **Trabajo de escritorio ASCII VJ Remix**: empaquetado Tauri, adaptadores de audio/medios nativos, salida Pop Out nativa, infraestructura de lanzamiento/actualización local, informes de fallas y la densa superficie de control de VJ.

## Requisitos del sistema

### macOS

- Mínimo: Apple Silicon Mac, macOS 13 Ventura o posterior, 8 GB de RAM, GPU compatible con Metal y aproximadamente 2 GB de espacio libre en disco.
- Óptimo: M1 Pro/Max, M2 Pro/Max, M3 Pro/Max o más reciente; 16 GB de RAM o más; macOS 14 Sonoma, macOS 15 Sequoia o más reciente; Pantalla/proyector externo para Pop Out.
- La compatibilidad con Intel Mac no es el objetivo de lanzamiento actual.
- La cámara, el micrófono y la captura de audio requieren concesiones de privacidad explícitas macOS.
- Las compilaciones de lanzamiento públicas de macOS deben estar firmadas con el ID del desarrollador y certificadas ante notario.

### Windows

- Mínimo: Windows 10 22H2 o Windows 11, x64 CPU, tiempo de ejecución WebView2, D3D12 o WebGL2 compatible con GPU, 8 GB de RAM y aproximadamente 2 GB de espacio libre en disco.
- Óptimo: Windows 11, Intel/AMD/NVIDIA GPU reciente con controladores actuales, 16 GB de RAM o más, decodificación de medios de hardware y pantalla de salida dedicada.
- Los artefactos Windows 0.9.3 se publican como vistas previas sin firmar hasta que se pruebe un backend de firma.

### Linux

- Mínimo: distribución moderna x86_64 Linux, tiempo de ejecución WebKitGTK 4.1, controladores Mesa o GPU del proveedor con WebGL2, 8 GB de RAM y aproximadamente 2 GB de espacio libre en disco.
- Óptimo: Ubuntu 24.04, Fedora 40, Arch o distribución actual comparable; Wayland o X11 bien configurado; controladores recientes de Mesa/NVIDIA; GPU compatible con Vulkan; PipeWire para futuros trabajos de captura.
- El comportamiento de GPU varía según la distribución, la versión de WebKitGTK y el controlador de gráficos.

## Guía práctica de hardware

El renderizador puede ser exigente. Los tamaños de cuadrícula más altos, las cámaras múltiples, la reactividad de audio y las ventanas de salida nativas aumentan la carga.

Para el trabajo con cámara en vivo, las cámaras USB estables, los puertos USB directos o un concentrador con alimentación, una buena iluminación, alimentación de CA y una pantalla de salida dedicada a menudo son más importantes que CPU sin procesar por sí solo.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
