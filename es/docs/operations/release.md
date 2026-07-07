---
title: Lanzamiento y actualizaciones
description: Documentación de versiones y actualizaciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Operaciones
lang: es
---

# Lanzamiento y actualizaciones

## Postura de liberación actual

- Los documentos fuente actuales describen el conjunto de características **0.9.3**.
- Las compilaciones de lanzamiento público de macOS requieren la firma y certificación notarial del ID del desarrollador.
- Los artefactos Windows 0.9.3 son vistas previas sin firmar hasta que se pruebe SignPath Foundation, Azure Artifact Signing u otro backend de firma.
- GitHub La infraestructura del actualizador de versiones está configurada.
- Las comprobaciones de actualizaciones y versiones no deben ampliar la capacidad de la red en tiempo de ejecución.

## macOS

El CI de publicación pública trata la firma o notarización de macOS como un proceso cerrado ante fallos. Es posible que las compilaciones locales o de prueba aún requieran el flujo normal de macOS, hacer clic con el botón derecho en Abrir o Abrir de todos modos.

## Windows

Las herramientas de firma Windows existen para futuros trabajos de versión firmada, incluidos Azure Artifact Signing, Tauri `signCommand` y los asistentes de verificación de Authenticode. La versión activa 0.9.3 sigue siendo artefactos de vista previa sin firmar.

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
