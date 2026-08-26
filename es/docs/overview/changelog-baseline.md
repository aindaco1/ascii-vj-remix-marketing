---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

# Base de la versión

Los documentos actuales describen el conjunto de funciones **0.9.9**.

## Aspectos destacados de 0.9.9

- El control Informes permanece visible con una cola vacía para que los usuarios puedan revisar las preferencias `ask`, `always` y `off` antes de que ocurra un error. Los informes pendientes todavía añaden un contador y un estado de advertencia.
- Se eliminó la lectura duplicada del backend del lado derecho. El selector Backend central sigue siendo el control canónico y la superposición Estadísticas conserva los diagnósticos del backend resuelto en tiempo de ejecución.
- Los listeners de la prueba de humo de la interfaz del actualizador empaquetado se registran antes de inicializar los dispositivos, para que el arranque de la cámara o el audio no compita con una solicitud temprana.
- La prueba de humo de la versión publicada abre las apps empaquetadas para macOS, Windows y Linux, exige que Actualizar e Informes permanezcan visibles y que la lectura duplicada del backend siga ausente.
- La línea de versiones reciente también incluye las correcciones del actualizador y del pipeline de lanzamiento de 0.9.8, las optimizaciones del renderizador y la salida nativa de 0.9.6, y los presets y el MIDI UC-33e/mioXC experimental introducidos en 0.9.5.

## Línea de base de seguridad

- Los informes siguen conteniendo únicamente datos de fallos limitados y sanitizados. Los diagnósticos de medios locales y los registros arbitrarios no se adjuntan ni se envían.
- El canario opcional de aceptación de producción se niega a ejecutarse cuando ya hay un informe de usuario pendiente y solo envía una carga sintética fija.
- La comprobación de actualización al inicio no envía datos multimedia, de cámara, de audio, presets, MIDI, informes de fallos ni rutas locales, y no bloquea el arranque cuando la red no está disponible.
- Los paquetes de actualización permanecen firmados y la instalación nunca comienza sin una acción del usuario.
- Las compilaciones de desarrollo no pueden reemplazar la aplicación de producción, heredar sus concesiones de privacidad macOS ni utilizar el punto final del actualizador de producción.
- Los artefactos públicos macOS deben conservar el identificador del paquete de producción, el equipo de ID del desarrollador, el tiempo de ejecución reforzado y el requisito designado estable en todas las actualizaciones; Los artefactos Windows actuales siguen siendo vistas previas sin firmar.

## Línea base de validación

El registro de cambios 0.9.9 documenta pruebas deterministas de la interfaz de informes de fallos, además de comprobaciones empaquetadas de Actualizar, Informes y el único control Backend en macOS, Windows y Linux. La puerta de lanzamiento más amplia conserva las comprobaciones del renderizador, audio, MIDI, política de Tauri, firma, notarización, instaladores y reemplazo mediante el actualizador.



## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
