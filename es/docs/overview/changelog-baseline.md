---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

# Base de la versión

Los documentos actuales describen el conjunto de características **0.9.3**.

## 0.9.3 Aspectos destacados

- Las versiones públicas de macOS requieren la firma y certificación notarial del ID del desarrollador.
- Los artefactos de la versión Windows se publican como vistas previas sin firmar hasta que se pruebe un backend de firma.
- La reactividad de audio tiene valores predeterminados compartidos, metadatos de control, ajustes preestablecidos, normalización de funciones, amortiguación de mezcla densa y modulación de parámetros de renderizado.
- Los nuevos controles audiorreactivos cubren la cantidad de transitorio/flujo, la cantidad de presencia, la amortiguación de densidad y el nivel de ruido.
- Los medidores de flujo y densidad están disponibles junto con un preajuste audio-reactivo de Dense Mix Control.
- La vista previa del navegador, Pop Out, las rutas de transmisión y la salida nativa consumen reglas de modulación reactivas de audio compartidas.
- Las transiciones estáticas de vídeo/cámara se funden entre familias de renderizadores sin destruir la fuente de medios compartida.
- Los ajustes preestablecidos tradicionales de Canvas2D ASCII tienen por defecto una fluctuación de imagen estática visible.

## Línea de base de seguridad

- La firma futura Windows utiliza credenciales de firma de ámbito ambiental y no confirma archivos de certificado, secretos de cliente ni material de firma privado.
- La reactividad de audio envía vectores de características acotados a través de IPC; El audio sin formato, los fotogramas, los archivos multimedia y las rutas permanecen locales.
- Las comprobaciones de firma de versiones y de firmas de actualizadores tratan la distribución pública de macOS como cerrada ante fallos.

## Línea base de validación

El registro de cambios registra comprobaciones de reactividad de audio, preparación de Authenticode Windows, puertas de liberación/escritorio, comportamiento de Pop Out de la cámara, enmascaramiento de glifos nativos, transiciones de renderizado en vivo, WTF mode, fluctuación ASCII tradicional y permisos de política Tauri.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
