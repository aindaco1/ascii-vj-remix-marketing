---
title: Mapa de fuentes
description: Documentación de Source Map derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Referencia
lang: es
---

# Mapa de fuentes

El script de sincronización utiliza los siguientes archivos fuente del repositorio ASCII VJ Remix.

|Fuente|Destino / uso|
| --- | --- |
|`README.md`|Alcance del producto, conjunto de funciones, requisitos, embalaje, soporte/contacto y punto de entrada del desarrollador.|
|`CHANGELOG.md`|Línea de base de la versión actual, cambios de comportamiento recientes, notas de seguridad y expectativas de validación.|
|`docs/RENDERING_ENGINE.md`|Flujo de origen, modelo de parámetros, backends de renderizado, parámetros efectivos, Pop Out, audio y rutas de transmisión.|
|`docs/CONTRIBUTORS.md`|Configuración, flujo de trabajo de contribución, notas de versión/actualización, política complementaria FFmpeg.|
|`docs/AGENTS.md`|Orden de carga de contexto del agente, restricciones, mapa de propiedad y orientación para trabajar de forma segura.|
|`docs/SECURITY.md`|Límite local primero, capacidades Tauri, informes de fallas, actualizador, medios y manejo de secretos.|
|`docs/PERFORMANCE.md`|Latencia de renderizado/salida, cámara, FPS y validación de rendimiento.|
|`docs/TESTING.md`|Matriz de verificación derivada de la fuente.|
|`docs/ACCESSIBILITY.md`|Reglas de accesibilidad de la superficie de control.|
|`docs/I18N.md`|Expectativas de internacionalización y localización.|
|`docs/ROADMAP.md`|Dirección planificada, diferida y actual.|
|`package.json`|Referencia del comando NPM.|

## Regenerar documentos

```bash
ruby scripts/sync_ascii_docs.rb
```

## Reconstruir documentos en español

```bash
python3 scripts/build_spanish_docs.py
```
