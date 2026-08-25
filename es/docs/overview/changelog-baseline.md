---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

# Base de la versión

Los documentos actuales describen el conjunto de funciones **0.9.6**.

## 0.9.6 Aspectos destacados

- El macOS Pop Out nativo carga fotogramas de origen decodificados solo cuando su versión del fotograma de origen cambia mientras la presentación y los parámetros en vivo continúan en la actualización de la pantalla.
- WebGPU reutiliza almacenamiento de respaldo uniforme, vistas de textura y grupos de enlace estables; WebGL2 almacena en caché sus 18 ubicaciones uniformes de sombreador después de la vinculación.
- Las transiciones numéricas preestablecidas y WTF actualizan los controles cambiantes durante la interpolación y luego sincronizan toda la fuente/cámara/superficie de control una vez finalizada.
- La ruta de prueba medida macOS eliminó alrededor del 60% del trabajo duplicado de conversión RGB y carga de texturas para una fuente de 24 FPS presentada cerca de 60 FPS sin cambiar las matemáticas del renderizador, la resolución de fuente/salida, el comportamiento del sombreador o los controles de calidad.
- La versión 0.9.5 agregó 23 ajustes preestablecidos de caracteres acreditados inspirados en ascii.today y UC-33e/mioXC MIDI nativo experimental con cuatro páginas, adquisición suave, aprendizaje MIDI, selección de ajustes preestablecidos numéricos y captura/restauración SysEx limitada.
- Los paquetes de desarrollo normales ahora utilizan el nombre `ASCII VJ Remix Dev` y el identificador `com.asciline.remix.dev` separados.
- El DMG macOS y la ruta del actualizador validan el diseño de arrastrar a las aplicaciones, la identidad de producción, la carga útil del actualizador firmado y el reemplazo real impulsado por la aplicación.

## Línea de base de seguridad

- Los permisos MIDI permanecen confinados a la ventana de control principal y el primer adaptador nativo acepta solo puertos con nombre mioXC.
- Las compilaciones de desarrollo no pueden reemplazar la aplicación de producción ni heredar sus concesiones de privacidad macOS.
- Los artefactos públicos macOS deben conservar el identificador del paquete de producción, el equipo de ID del desarrollador, el tiempo de ejecución reforzado y el requisito designado estable en todas las actualizaciones.

## Línea base de validación

El registro de cambios 0.9.6 registra la validación optimizada de la aplicación, verificaciones de renderizador/estático/audio/MIDI/Tauri, 47 pruebas Rust, contadores de carga de fuentes, trabajo de interfaz de usuario de transición limitada, pruebas de diseño de DMG, pruebas de identidad de aplicaciones y humo del actualizador de versiones publicadas.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
