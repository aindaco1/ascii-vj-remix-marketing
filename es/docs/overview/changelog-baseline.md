---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

<a id="release-baseline"></a>

# Base de la versión

La última entrada fechada del registro de cambios es **1.1.0**. Esta página excluye las entradas Unreleased; el [Registro de cambios](/es/docs/reference/changelog/) las conserva cuando existen. Las demás guías siguen la rama `main` y pueden incluir cambios posteriores a la etiqueta de la aplicación publicada.

[Descargue v1.1.0 y consulte sus notas de publicación y validación de plataformas](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.1.0). La fecha del registro de cambios corresponde a la entrada en el código fuente; GitHub Releases registra cuándo se publicaron las descargas.

Consulte las [Funciones](/es/docs/overview/features/) para conocer los controles actuales y los [registros de publicación del repositorio principal](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) para la validación y cobertura de plataformas de cada versión.

<a id="110-release-notes"></a>

## Notas de la versión 1.1.0

- Se admiten finales de línea de Windows y Unix al cargar los sombreadores nativos compartidos, evitando un fallo de inicialización del sombreador de Pop Out en Windows.
- Se conservan los fotogramas de video decodificados hasta completar el envío a WebGPU para evitar fallos transitorios al vincular texturas externas. El bucle de renderizado puede recuperarse de errores y solo contabiliza los fotogramas enviados.
- Stop en Audio Reactivity cancela las solicitudes de captura pendientes y serializa la parada y el inicio nativos. Seleccionar un preset de audio restaura todos sus controles deslizantes, los ajustes personalizados se muestran explícitamente y los cambios de audio se aplican durante las transiciones de Pop Out.
- Se añaden once presets originales: Neon Night Drive, Media Corridor, Wet Coast, Neon Cathedral, Orbital Chamber, Ashen Ruins, Fractal Dive, Mandelbulb Bloom, Mandelbox Passage, Edge Etching y Phosphor Echo. Brightness Relief se retira del catálogo integrado; su modo visual sigue siendo compatible con los looks guardados. Orbital Chamber deja de llevar la etiqueta Experimental.
- Todos los presets integrados, incluido Ashen Ruins, empiezan en Flat Media. Las configuraciones de escena siguen disponibles al elegirlas manualmente en Space / Motion y en los looks personalizados guardados. WTF elige Flat Media de forma independiente con una probabilidad del 80 % y reparte el 20 % restante por igual entre los diez modos espaciales. Los presets de referencia, los reintentos de seguridad y la alternativa final conservan esa elección.
- Se reduce el retraso de respuesta al audio con consultas de características a 120 Hz, búferes nativos menores cuando el dispositivo los admite, ataques inmediatos y una envolvente de caída compartida basada en el tiempo. Smoothing en cero desactiva completamente el suavizado. Se ignoran respuestas de capturas antiguas y se evita modular el audio dos veces en Pop Out.
- Se añade un sombreador de escena GPU compartido por WebGPU, WebGL2 y Pop Out nativo: geometría de cuadrícula con alturas variables, cubiertas visibles, suelos y techos, texturas de fachada estables, niebla, sombreado direccional y de contacto, ventanas emisivas, reflejos sobre superficies mojadas y lluvia con comprobación de profundidad. Canvas dispone de una implementación de referencia por software con límites de trabajo.
- Se proyecta la imagen, el video en reproducción o la cámara sobre superficies de escena más grandes, con repetición, ajuste o recorte que respetan la proporción. Las configuraciones opcionales de escena usan entre un 80 y un 95 % del material de entrada y atenúan los glifos de materiales para conservar las formas de la fuente. Los presets mantienen la identidad de la fuente y su reproducción.
- Se añaden velocidad de desplazamiento con signo, congelación y reinicio, selección de ruta, glifos de materiales, ASCII orientado por bordes con histéresis e historial reutilizable en coma flotante con desvanecimiento según el tiempo transcurrido, zoom y rotación.
- Se reutilizan el sistema de movimiento compartido y las características de audio acotadas para modular escenas. Los controles visuales y las acciones de movimiento se exponen a MIDI sin añadir acciones de fuente, captura ni salida.
- Se añade Bright output como preferencia global, desactivada inicialmente. Ilumina el material oscuro antes de seleccionar colores y glifos y conserva su valor entre presets y sesiones. Al desactivarla se mantiene la respuesta de color anterior.
- Las configuraciones opcionales de escena tienen alturas e inclinaciones de cámara, velocidades y encuadres distintos, además de un corredor estrecho, un techo inclinado de catedral, una costa baja y una vista orbital giratoria. Se añaden escenas compartidas y acotadas de ruinas recursivas, Mandelbrot, Mandelbulb y Mandelbox, con controles de zoom, detalle y forma.
- Se conservan las ediciones visuales manuales y MIDI realizadas durante una transición de preset, evitando que la transición las sobrescriba. Se mantiene el look Custom actual y la reproducción del material.
- Se conservan Classic Camera ASCII como selección predeterminada, Auto como preferencia de backend y los límites de densidad. El contrato de asignación de presets pasa a ser de 90 en total: 62 acelerados y 28 asignados explícitamente a Canvas.
- Se añaden comprobaciones de geometría, movimiento, paridad de píxeles entre CPU y GPU, desvanecimiento de estelas y continuidad del video. Consulte el [alcance y la aceptación de la versión](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md).



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
