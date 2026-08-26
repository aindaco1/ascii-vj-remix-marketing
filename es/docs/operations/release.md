---
title: Lanzamiento y actualizaciones
description: Documentación de versiones y actualizaciones derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Operaciones
lang: es
---

# Lanzamiento y actualizaciones

## Postura de lanzamiento actual

- Los documentos fuente actuales describen el conjunto de características **0.9.9**.
- Los artefactos públicos 0.9.9 macOS están firmados con el ID del desarrollador, notariados, engrapados y validados por Gatekeeper.
- Los artefactos públicos 0.9.9 Windows son vistas previas sin firmar.
- Las compilaciones de producción comprueban una vez por inicio los metadatos de GitHub Releases sin bloquear el arranque; las versiones firmadas más recientes aparecen en el control Actualizar existente.
- Las comprobaciones manuales siguen estando disponibles, mientras que la descarga, instalación y reinicio requieren una acción explícita del usuario.
- Las comprobaciones de actualizaciones y versiones no deben ampliar la capacidad de la red en tiempo de ejecución.

## macOS

El CI de publicación pública trata la firma o notarización de macOS como un proceso cerrado ante fallas. Los artefactos 0.9.9 pasaron la firma, certificación notarial, grapado y validación Gatekeeper. Las versiones 0.9.6 y 0.9.7 requieren una actualización manual única de DMG a 0.9.9 porque su conjunto de capacidades de producción ocultaba el control de Actualización. Es posible que las compilaciones locales o de prueba aún requieran el flujo normal de macOS, hacer clic con el botón derecho en Abrir o Abrir de todos modos.

## Windows

La configuración de firma Windows inactiva y los asistentes de verificación de Authenticode permanecen en el árbol de fuentes, pero el flujo de trabajo de la versión pública 0.9.9 no los utiliza. Sus artefactos Windows son vistas previas sin firmar.

## Informes de fallos

Los informes de fallos de producción se revisan y sanitizan, y se envían mediante la capa de escritorio Rust al relay de Cloudflare Worker en `https://crash.dustwave.xyz`. La vista web no tiene capacidad HTTP arbitraria. Los informes están limitados y sanitizados: no incluyen archivos multimedia, fotogramas, audio sin procesar, rutas completas, tokens, cookies, valores privados del entorno ni registros de diagnóstico arbitrarios. El control Informes permanece visible con una cola vacía para que la preferencia pueda revisarse sin crear ni enviar ningún informe.

## Validación de lanzamiento

El CI de lanzamiento resuelve un commit de etiqueta inmutable, exige que el flujo Desktop del commit exacto haya finalizado correctamente, compila la app y el entorno FFmpeg fijado en paralelo y verifica los artefactos restaurados antes del empaquetado. La prueba de humo de la versión publicada abre después la app empaquetada en macOS, Windows y Linux, exige que Actualizar e Informes permanezcan visibles y que la lectura duplicada del backend siga ausente, y conserva las comprobaciones de instalador, firma, notarización, firma del actualizador y reemplazo real adecuadas para cada plataforma.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
