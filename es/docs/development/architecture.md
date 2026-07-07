---
title: Arquitectura
description: Documentación de arquitectura derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Desarrollo
lang: es
---

# Arquitectura

## Forma del producto

ASCII VJ Remix es una aplicación de escritorio Tauri v2 con una interfaz de usuario de renderizado básica/Vite, rutas de renderizado GPU/Canvas, trabajo de salida nativo y adaptadores de audio/medios locales.

La aplicación debe entenderse como una herramienta de escritorio, no como una aplicación SaaS alojada. El modo de navegador ayuda al desarrollo y la portabilidad, pero la aplicación de escritorio empaquetada es el producto.

## Flujo de alto nivel

```text
source selection
  -> source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

## Mapa de propiedad

|Área|Ubicaciones de fuentes primarias|
| --- | --- |
|UI principal, parámetros, ajustes preestablecidos, controles de fuente, WTF, UI de audio|`app.js`, `index.html`, `style.css`|
|Abstracción de fuente de medios y renderizador GPU|`renderers/gpu/`|
|Adaptador Tauri y ayudantes de visualización de salida|`renderers/desktop/`|
|Shell Tauri, comandos, permisos, actualizador, audio nativo, salida nativa|`src-tauri/`|
|Renderizador nativo Pop Out|`src-tauri/src/native_output.rs`, `src-tauri/src/native_output/gpu.rs`|
|Ruta de latencia de cámara nativa macOS|`src-tauri/src/native_output/native_camera.rs`|
|Motor de medios Rust y sesiones FFmpeg|`src-tauri/src/media_engine/`|
|Construir, fumar, liberar, Podman, scripts FFmpeg|`scripts/`|
|Documentos de usuario/desarrollador|`docs/`, `README.md`, `CHANGELOG.md`|

## Restricciones no negociables

- Conserve el nombre de la aplicación y la dirección nativa del escritorio.
- Mantenga el tiempo de ejecución normal local primero y fuera de línea de forma predeterminada.
- Mantenga alta la calidad del renderizado; La salida WebGPU/WebGL es el objetivo de calidad visual.
- Conserve las rutas alternativas a menos que se implemente y pruebe un reemplazo.
- Trate el rendimiento y la latencia de Pop Out como un comportamiento crítico de cara al usuario.
- Mantenga locales los medios locales seleccionados.
- Mantenga la superposición de estadísticas como propiedad del usuario.
- Mantenga oculta la infraestructura de transmisión hasta que el flujo de trabajo de transmisión se produzca de extremo a extremo.
- No reduzca la densidad de control de la superficie VJ al rediseñar.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
