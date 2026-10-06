---
title: Resumen
description: Descripción general para desarrolladores de ASCII VJ Remix, incluida la arquitectura derivada del código fuente, las funciones, el desarrollo, las operaciones y la documentación de referencia.
nav_order: 1
lang: es
---

<a id="overview"></a>

# Resumen

Estos documentos son para desarrolladores de software que desean bifurcar, inspeccionar, ampliar, empaquetar o contribuir a ASCII VJ Remix.

ASCII VJ Remix es un visualizador de escritorio local y un banco de trabajo de renderizado. Para los usuarios, existe para brindar a los DJ un visualizador manejable y a los VJ un control detallado de filtro de video/ASCII. Para los desarrolladores, es una aplicación de escritorio Tauri con una densa superficie de control/representación, ruta de salida nativa, adaptadores de medios locales, modulación reactiva de audio e infraestructura de lanzamiento/actualización.

Estas guías siguen los cambios integrados en `main` del repositorio principal. La [Base de la versión](/es/docs/overview/changelog-baseline/) identifica la última publicación fechada, **1.2.0**. Los cambios posteriores se indican por separado; el código fuente, CI, la publicación de la aplicación, el despliegue del relay y la aceptación en hardware son comprobaciones distintas.

<a id="start-here"></a>

## Comience aquí

1. [ASCII VJ Remix descripción general](/es/docs/overview/ascii-vj-remix/) para conocer el alcance del producto, la versión base, los requisitos de la plataforma y las capacidades actuales.
2. [Conjunto de funciones](/es/docs/overview/features/) para obtener un mapa completo derivado del código fuente de lo que puede hacer la aplicación.
3. [Quickstart](/es/docs/development/quickstart/) para configuración local y primeros comandos de verificación.
4. [Arquitectura](/es/docs/development/architecture/) y [Motor de renderizado](/es/docs/development/rendering-engine/) antes de cambiar la fuente, el renderizador, el ajuste preestablecido, el audio, la cámara o el comportamiento de Pop Out.
5. [Seguridad](/es/docs/operations/security/), [Rendimiento](/es/docs/operations/performance/), [Pruebas](/es/docs/operations/testing/), [Accesibilidad](/es/docs/operations/accessibility/) e [Internacionalización](/es/docs/operations/internationalization/) antes de publicar una bifurcación.

<a id="overview-pages"></a>

## Páginas de descripción general

- [ASCII VJ Remix](/es/docs/overview/ascii-vj-remix/): alcance, linaje, línea base de lanzamiento, requisitos de plataforma y límites del proyecto.
- [Conjunto de funciones](/es/docs/overview/features/): mapa completo de fuentes, renderizado, ajustes preestablecidos, controles en vivo, reactividad de audio, Pop Out, empaquetado, seguridad y rutas avanzadas.
- [Línea base de lanzamiento](/es/docs/overview/changelog-baseline/): línea de lanzamiento actual y cambios de comportamiento recientes del registro de cambios.

<a id="source-derived-sections"></a>

## Secciones derivadas de la fuente

- [Desarrollo](/es/docs/development/) cubre la configuración local, la arquitectura, los componentes internos de renderizado, el flujo de trabajo de contribución y la orientación del agente LLM.
- [Operaciones](/es/docs/operations/) cubre seguridad, rendimiento, pruebas, accesibilidad, i18n, empaquetado, actualizaciones e informes de fallos.
- [Referencia](/es/docs/reference/) cubre comandos, hoja de ruta, registro de cambios y mapeo de fuente a documentos.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [docs/README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md)
- [docs/USER_GUIDE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md)
- [docs/RELEASING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RELEASING.md)
- [docs/releases/README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/SHARED_DESKTOP_MIGRATION.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SHARED_DESKTOP_MIGRATION.md)
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
- [docs/PERFORMANCE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/PERFORMANCE.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
- [docs/ACCESSIBILITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ACCESSIBILITY.md)
- [docs/I18N.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/I18N.md)
- [docs/ROADMAP.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ROADMAP.md)
