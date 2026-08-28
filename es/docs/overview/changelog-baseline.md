---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

# Base de la versión

Los documentos actuales describen el conjunto de características **0.9.12**. La entrada más reciente del registro de cambios con fecha es la autoridad de publicación; la sección Inédita está excluida intencionalmente.

## 0.9.12 Notas de la versión

### Corregido

- Se restauró la salida visible de la vista principal para cada ajuste preestablecido Demo Image incorporado corrigiendo las cargas de páginas de glifos de WebGL y usando mips de atlas de cobertura máxima en caché para glifos representados en celdas muy pequeñas.
- Mantuvo los lienzos preestablecidos de sólidos, píxeles y glifos en la relación de aspecto de origen resolviendo los recuentos de filas estáticas a partir del ancho y alto real de la celda.
- Se agregó una matriz de pruebas de humo de vista primaria totalmente preestablecida que cubre la activación, la salida visible, los errores de WebGL, la finalización diferida de la página de glifos y el aspecto del lienzo.
- Se evitaron lienzos de glifos de vista primaria en blanco en el tiempo de ejecución de macOS Apple WebKit seleccionando allí la ruta de glifo Canvas2D limitada existente. Los ajustes preestablecidos primarios de sólidos/píxeles conservan WebGPU, los tiempos de ejecución compatibles conservan los glifos GPU y el renderizador nativo Pop Out no cambia.
- Hizo que la prueba de humo de rendimiento del escritorio empaquetado rechazara un renderizador que avanzaba cuyo lienzo principal no tiene señal de píxeles visible.
- Se agregó un barrido Apple WebKit empaquetado que activa los 69 ajustes preestablecidos de Demo Image integrados y verifica la visibilidad de la vista principal, la familia de renderizador, el estado de ejecución, los errores de GPU y el aspecto de fuente/lienzo para cada superficie final.

La versión 0.9.12 restaura todos los ajustes preestablecidos integrados en la vista principal de la aplicación mientras conserva la relación de aspecto de origen y la ruta nativa Pop Out. La versión 0.9.11 agrega paletas de proyecto con presupuesto de rendimiento, tramado ordenado, controles de glifos multilingües, rampas Unicode personalizadas, límites de densidad y paridad de renderizado/salida nativa. La versión 0.9.10 reemplaza el arte de televisión heredado con un icono canónico de la aplicación generado para cada plataforma empaquetada y incorpora la corrección de aceptación de Reports posterior a 0.9.9. La versión 0.9.9 mantiene las preferencias de informes de fallas accesibles con una cola vacía, elimina la lectura duplicada del backend de la barra superior y amplía la prueba de humo de la interfaz empaquetada para cubrir ambos controles. La versión 0.9.8 restaura el control de producción y la verificación de inicio de Update, agrega una prueba de humo de regresión de UI empaquetada y acorta las compilaciones de lanzamiento al compilar la aplicación y el tiempo de ejecución de FFmpeg simultáneamente antes de la reutilización de artefactos verificados. La versión 0.9.7 agrega el controlador de verificación de lanzamiento silencioso al tiempo que conserva la instalación aprobada por el usuario y fortalece la resiliencia del transporte de lanzamiento. La versión 0.9.6 continúa el trabajo de puesta en marcha experimental de MIDI, elimina la sobrecarga medida de la ruta activa de salida/renderizador sin cambiar las matemáticas o la calidad visual, y refuerza la ruta de lanzamiento de arrastrar a las aplicaciones de macOS. La versión 0.9.5 agrega 23 ajustes preestablecidos de caracteres inspirados en ascii.today acreditados y un control DIN MIDI nativo experimental para un Evolution/M-Audio UC-33e a través de un mioXC de iConnectivity, incluidas cuatro páginas de controlador completas, soft takeover, selección numérica de ajustes preestablecidos, aprendizaje de MIDI y captura/restauración de banco completo de SysEx. La versión 0.9.3 traslada las versiones de escritorio públicas a la distribución macOS firmada/notariada, publica Windows como una vista previa sin firmar mientras se difiere la firma y amplía la reactividad del audio con controles de mezcla densa que reducen la reacción exagerada en música ocupada. La versión 0.9.0 sigue siendo la primera base de documentación para el conjunto de funciones actual ASCII VJ Remix.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
