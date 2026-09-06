---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

<a id="release-baseline"></a>

# Base de la versión

Estos documentos describen las funciones de **1.0.3**. La referencia es la entrada con fecha más reciente del registro de cambios; se excluye la sección Unreleased.

[Descarga v1.0.3 y consulta las notas de publicación y validación por plataforma](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.3). La fecha del registro de cambios corresponde a la entrada de la versión en el código fuente; GitHub Releases indica cuándo se publicaron las descargas.

<a id="103-release-notes"></a>

## 1.0.3 Notas de la versión

<a id="added"></a>

### Añadido

- Se añadió ASCII City Nightshift, un preset original inspirado en [ASCII City de tweakyourpc](https://tweakyourpc.github.io/ascii-city/). Usa la paleta compartida City Nightshift, sombras casi negras, luces ámbar y verde salvia, y caracteres densos de terminal con un jitter suave sobre la imagen, el video o la cámara seleccionados. Las imágenes fijas se animan sin audio.
- Se añadió ASCII World Mint, un preset original inspirado en [ASCII World de yeahpython](https://yeahpython.github.io/game/game.html), con glifos ASCII finos de color menta, un fondo verde azulado oscuro y jitter continuo sobre la imagen, el video o la cámara actuales.
- Se añadió captura nativa de una sola cámara para Pop Out mediante Media Foundation en Windows y la entrada V4L2 de FFmpeg incluido en Linux. Ambas rutas alimentan el renderizador nativo `wgpu` existente y evitan la lectura del canvas del WebView y el envío de cada fotograma por Tauri IPC en la ruta normal.
- Se añadieron entradas de cámara alternativas mediante DirectShow en Windows y V4L2 en Linux al FFmpeg incluido. Las comprobaciones de empaquetado exigen que FFmpeg incluya el dispositivo de entrada correspondiente antes de aceptar los artefactos de la versión.
- Se añadieron métricas acotadas de tiempos, transferencia y FPS aceptados de la duplicación de fotogramas a los informes manuales para medir su comportamiento en equipos físicos.
- Se añadió un puente de preview de cámara nativa exclusivo de Windows para dispositivos que rechazan dos clientes de captura. Un único cliente de Media Foundation alimenta tanto Pop Out nativo como un preview binario JPEG del último fotograma, limitado a 640x360 y 30 FPS, para el renderizador principal WebGPU existente.

<a id="changed"></a>

### Cambiado

- Windows abre una única sesión de cámara con Media Foundation y mantiene el preview principal en vivo mediante el puente de preview nativo; Linux conserva su flujo exclusivo V4L2. Las sesiones exclusivas esperan a que termine el hilo de trabajo nativo antes de reintentar la captura del navegador, con un número limitado de reaperturas.
- La selección de cámara en Windows acepta el identificador de modelo USB que Chromium añade al nombre cuando coincide sin ambigüedad con el nombre descriptivo de Media Foundation. Los diagnósticos manuales conservan el motivo del fallo de apertura nativa cuando se necesita recurrir a la duplicación de fotogramas.
- La duplicación de cámara alternativa en Windows/Linux usa el último fotograma, un perfil de 640x360 y una única solicitud en curso, con un máximo de 30 FPS. Las demás rutas de duplicación conservan sus dimensiones anteriores y su límite de 15 FPS.
- Los diagnósticos manuales conservan el tipo de informe y la superficie revisados al pasar por el relé e incluyen el estado de la salida nativa en las incidencias generadas en GitHub. Los informes de Windows conservan el motivo del fallo de apertura compartida, los FPS aceptados por el puente de preview, la tasa de transferencia codificada y los tiempos de lectura, codificación y decodificación.

<a id="fixed"></a>

### Corregido

- Las cargas de las tablas de paleta de WebGL2 conservan el orden de las filas independientemente de la orientación de la imagen de origen. Así, los colores oscuros y claros coinciden con el mapeo de paleta compartido al iniciar y al cambiar de paleta en vivo.
- La salida nativa de Windows usa las máscaras de glifos de cobertura máxima del renderizador principal para celdas diminutas, conservando el aspecto de píxeles de Acid Snowstorm.
- En Windows, la textura del preview, la cuadrícula y las dimensiones del canvas se actualizan juntas cuando cambia el tamaño de los fotogramas de la cámara nativa. Esto evita proporciones incorrectas y franjas sin cubrir en el borde derecho tras cambiar de preset.
- En Windows, los cambios entre imagen, video y cámara completan el traspaso del control nativo antes de cargar el siguiente preview principal. Las lecturas de cámara son asíncronas y la captura está separada de la presentación en GPU, por lo que una lectura bloqueada no impide el cierre normal del hilo de trabajo.
- Al iniciar la cámara, Windows conserva su primera sesión de captura en vez de sondear, cerrar y volver a abrir el dispositivo. La detección de controladores GPU se ejecuta fuera del hilo de la interfaz y reutiliza su instancia entre aperturas; se registran los tiempos de cada fase del inicio.
- La ruta alternativa DirectShow elimina el sufijo de modelo USB de Chromium y escapa los separadores del nombre del dispositivo. Los diagnósticos también conservan el fallo original de captura nativa.
- Se concedió a la ventana principal el permiso específico de Tauri necesario para leer fotogramas del puente de preview de cámara nativa de Windows. La comprobación de políticas de escritorio verifica que cada comando Tauri invocado por el frontend tenga un permiso generado y una concesión en las capacidades de la ventana principal. Esto evita que las aplicaciones empaquetadas rechacen silenciosamente un comando nuevo.

<a id="preserved"></a>

### Conservado

- Pop Out con una sola cámara en macOS conserva la implementación existente de AVFoundation/display-link. No se modificó el código de captura ni de presentación de macOS.
- La salida multicámara y los dispositivos que no admiten apertura nativa conservan la alternativa de duplicación de fotogramas con límites de transferencia.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
