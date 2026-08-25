---
title: Lanzamiento y actualizaciones
description: Documentación de versiones y actualizaciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Operaciones
lang: es
---

# Lanzamiento y actualizaciones

## Postura de liberación actual

- Los documentos fuente actuales describen el conjunto de características **0.9.6**.
- Los artefactos públicos 0.9.6 macOS están firmados con el ID del desarrollador, notariados, engrapados y validados por Gatekeeper.
- Los artefactos públicos 0.9.6 Windows son vistas previas sin firmar.
- GitHub La infraestructura del actualizador de versiones está configurada.
- Las comprobaciones de actualizaciones y versiones no deben ampliar la capacidad de la red en tiempo de ejecución.

## macOS

El CI de publicación pública trata la firma o notarización de macOS como un proceso cerrado ante fallas. Los artefactos 0.9.6 pasaron la firma, certificación notarial, grapado y validación Gatekeeper. Es posible que las compilaciones locales o de prueba aún requieran el flujo normal de clic derecho del botón Abrir o Abrir de todos modos con macOS.

## Windows

La configuración de firma Windows inactiva y los asistentes de verificación de Authenticode permanecen en el árbol de fuentes, pero el flujo de trabajo de la versión pública 0.9.6 no los utiliza. Sus artefactos Windows son vistas previas sin firmar.

## Informe de fallos

Los informes de fallas de producción se revisan/desinfectan y se enrutan a través de la capa de escritorio Rust al relé Cloudflare Worker en `https://crash.dustwave.xyz`. La vista web no tiene capacidad HTTP arbitraria. Los informes están delimitados y desinfectados: no se incluyen archivos multimedia, fotogramas, audio sin procesar, rutas completas, tokens, cookies ni valores de entorno privado.

## Validación de lanzamiento

Las comprobaciones de versión incluyen comprobaciones de escritorio, matemáticas de renderizado, pruebas de ayuda reactivas de audio, pruebas de retransmisión de fallos, comprobaciones de políticas Tauri y verificación de firma/actualización apropiada para cada plataforma.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
