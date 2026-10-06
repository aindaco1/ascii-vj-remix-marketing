---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

<a id="release-baseline"></a>

# Base de la versión

La última entrada fechada del registro de cambios es **1.2.0**. Esta página excluye las entradas Unreleased; el [Registro de cambios](/es/docs/reference/changelog/) las conserva cuando existen. Las demás guías siguen la rama `main` y pueden incluir cambios posteriores a la etiqueta de la aplicación publicada.

[Descargue v1.2.0 y consulte sus notas de publicación y validación de plataformas](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.2.0). La fecha del registro de cambios corresponde a la entrada en el código fuente; GitHub Releases registra cuándo se publicaron las descargas.

Consulte las [Funciones](/es/docs/overview/features/) para conocer los controles actuales y los [registros de publicación del repositorio principal](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) para la validación y cobertura de plataformas de cada versión.

<a id="120-release-notes"></a>

## Notas de la versión 1.2.0

- WTF ahora selecciona Flat Media el 95% de las veces (5% en total para las escenas opcionales).
- WTF valida la visibilidad de los glifos, las tomas oscuras y la respuesta al audio, comprueba su alternativa y comparte con Pop Out nativo límites que conservan las sombras.
- Se añaden seis presets sutiles de Flat Media: Threadlight, Silver Etching, Contour Silk, Julia Glass, Chromatic Undertow y Phosphor Lace.
- Se añade Fractal Accents con Amount/Coverage independientes, ubicación en bordes, tonos medios, zonas tranquilas o estelas, escala, movimiento lento, respuesta moderada al audio, seis variaciones seleccionadas y la acción Another variation asignable mediante MIDI Learn.
- Los acentos se ven en looks de glifos y monocromáticos, se conservan al cambiar entre presets integrados normales y se aplican a todos los modos de escena opcionales. Se añade una opción Off explícita y estelas cortas automáticas cuando el eco está en cero.
- Las seis recetas de acentos se integran en WTF, con una elección independiente de 65% acento / 35% Off que se conserva durante los reintentos de seguridad. Se aumenta la intensidad de los presets manteniendo límites que conservan la visibilidad de la fuente.
- Subtle Limit empieza activado como preferencia global persistente; se conserva al cambiar, guardar o importar presets y al usar WTF. Limita los cambios de brillo, color, glifos y desplazamiento del acento sin cambiar el look Classic Camera ASCII de un perfil nuevo.
- WebGPU, WebGL2, wgpu nativo y Canvas comparten los cálculos acotados de los acentos. Se amplían las comprobaciones de paridad, continuidad de la fuente, congelación, omisión, audio, desvanecimiento de estelas y matriz de presets; el catálogo ahora tiene 96 en total / 68 acelerados / 28 explícitos de Canvas.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
