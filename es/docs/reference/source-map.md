---
title: Mapa de fuentes
description: Documentación de Source Map derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Referencia
lang: es
---

<a id="source-map"></a>

# Mapa de fuentes

El script de sincronización utiliza los siguientes archivos fuente del repositorio ASCII VJ Remix.

|Fuente|Destino / uso|
| --- | --- |
|`README.md`|Alcance y linaje del producto; instalación aguas arriba y punto de entrada de primera ejecución.|
|`docs/README.md`|Propiedad y navegación de la documentación ascendente.|
|`docs/USER_GUIDE.md`|Conjunto detallado de funciones, requisitos del sistema, hardware y guía térmica. El uso completo, los permisos y la solución de problemas permanecen vinculados en sentido ascendente.|
|`CHANGELOG.md`|Línea de base de la versión actual, cambios de comportamiento recientes, notas de seguridad y expectativas de validación.|
|`docs/RENDERING_ENGINE.md`|Flujo de origen, modelo de parámetros, backends de renderizado, parámetros efectivos, Pop Out, audio y rutas de transmisión.|
|`docs/CONTRIBUTORS.md`|Inicio rápido, identidad de la aplicación local, flujo de trabajo de contribución, FFmpeg y Podman.|
|`docs/RELEASING.md`|Procedimiento mantenido de empaquetado, firma, publicación, actualización y aceptación de artefactos.|
|`docs/releases/README.md`|Índice vinculado de registros históricos de publicaciones; procedimiento no actual o estado de aceptación en vivo.|
|`docs/AGENTS.md`|Orden de carga de contexto del agente, restricciones, mapa de propiedad y orientación para trabajar de forma segura.|
|`docs/SECURITY.md`|Límite local primero, capacidades Tauri, informes de fallas, actualizador, medios y manejo de secretos.|
|`docs/PERFORMANCE.md`|Latencia de renderizado/salida, cámara, FPS y validación de rendimiento.|
|`docs/TESTING.md`|Matriz de verificación derivada de la fuente.|
|`docs/ACCESSIBILITY.md`|Reglas de accesibilidad de la superficie de control.|
|`docs/I18N.md`|Expectativas de internacionalización y localización.|
|`docs/ROADMAP.md`|Sólo dirección prospectiva.|
|`package.json`|Referencia del comando NPM.|
|`src-tauri/icons/icon.png`|Icono de aplicación canónica aprobada copiado en el sitio de marketing.|

<a id="guide-ownership"></a>

## Propiedad de la guía

El [índice de documentación ascendente](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md) posee el mapa de guía completo, incluido MIDI, créditos de caracteres preestablecidos, control de calidad de VM Linux, documentos de componentes y evidencia de referencia. Estas guías especializadas permanecen vinculadas a sus archivos fuente canónicos.

Los [registros de versiones](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) conservan decisiones y evidencia fechadas. Consulte [Lanzamiento y actualizaciones](/es/docs/operations/release/) para el procedimiento actual, [Pruebas](/es/docs/operations/testing/) para la verificación y la [Hoja de ruta](/es/docs/reference/roadmap/) para el trabajo futuro.

<a id="regenerate-docs"></a>

## Regenerar documentos

```bash
ruby scripts/sync_ascii_docs.rb
```

<a id="rebuild-spanish-docs"></a>

## Reconstruir documentos en español

```bash
python3 scripts/build_spanish_docs.py
```
