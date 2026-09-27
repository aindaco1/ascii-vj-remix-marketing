---
title: Servicios de escritorio compartidos
description: Documentación de servicios de escritorio compartidos derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 6
parent: Desarrollo
lang: es
---

<a id="shared-desktop-services"></a>

# Servicios de escritorio compartidos

La migración a servicios de escritorio compartidos se publicó en [v1.0.6](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.6). Esta guía documenta quién mantiene cada componente y las verificaciones de la migración; el despliegue del relay y la validación de la app instalada se comprueban por separado.

- Revisión inicial del repositorio consumidor: `a11e7f0c90f22d9ab1ebbaa4a502c0fc3771e534`.
- Revisión anterior de Platform: `60d439b887f1244f82ff232c849d74152b28c776`.
- Commit inmutable actual y versiones exactas: [platform-desktop.json](https://github.com/aindaco1/ascii-vj-remix/blob/main/platform-desktop.json).
- Componentes compartidos: helpers de progreso y manifiestos de Tauri, envío de informes revisados, agregación serializada y conciliación de incidencias de GitHub.

Las rutas del relay, los esquemas de cada producto, las huellas de diagnóstico, la autenticación, el texto de las incidencias, los bindings, las claves de almacenamiento, las clases de migración, los límites de solicitudes y los controles del operador siguen siendo responsabilidad de este repositorio. Se conserva el enrutamiento de Road Notice. El arranque de la app y la interfaz de instalación y reinicio también permanecen aquí.

<a id="shared-service-maintenance"></a>

## Mantenimiento de servicios compartidos

La documentación de mantenimiento de 1.0.6 también incluye estos cambios integrados el 25 de septiembre de 2026, después de crear la etiqueta de la versión de escritorio. No añaden funciones a la app ASCII VJ:

- El [adaptador de Record](https://github.com/aindaco1/ascii-vj-remix/blob/main/crash-relay/README.md#record-adapter) añade diagnósticos revisados y acotados mediante la ruta de agregación existente del relay.
- La dependencia de Platform pasa de Desktop Core 0.1.0 a 0.2.0 para mantener la compatibilidad con adaptadores anteriores. El [manifiesto del consumidor](https://github.com/aindaco1/ascii-vj-remix/blob/main/platform-desktop.json) sigue siendo la fuente de la revisión actual y las versiones exactas de los paquetes.

Los paquetes de escritorio publicados de 1.0.6 conservan la revisión de dependencias de su etiqueta; estos commits posteriores no modifican los instaladores. El despliegue del relay y la entrega a GitHub con datos sintéticos tienen sus propias comprobaciones en la [guía del relay](https://github.com/aindaco1/ascii-vj-remix/blob/main/crash-relay/README.md). Un commit integrado o una versión de escritorio publicada no demuestra ninguno de esos resultados.

<a id="validation"></a>

## Validación

Antes y después de la migración pasaron las 53 pruebas del relay y las pruebas de caracterización del actualizador y los manifiestos. Después también pasaron el empaquetado de Vite sin conexión, las pruebas de Jev, los controles de políticas de Tauri y la simulación de despliegue del Worker. En esa validación no se desplegó el relay ni se crearon incidencias reales.

Esta comprobación valida los gitlinks de los consumidores, las versiones exactas de los paquetes y las revisiones de Sparkle conservadas en los archivos de dependencias:

```sh
node shared/dust-wave-platform/scripts/check-desktop-consumer.mjs
```

Platform supera su suite de JavaScript y las pruebas de las recetas en una copia limpia del repositorio. Sus siete pruebas de escritorio en Swift pasan por separado con Sparkle 2.9.5, 2.9.6 y 2.10.0. Los manifiestos de las apps conservan sus revisiones exactas de Sparkle. Al avanzar el gitlink completo también se incorporan parches existentes de Platform; las pruebas de cada producto cubren esas dependencias.

<a id="independent-rollback"></a>

## Reversión independiente

Revierte el commit de migración de este repositorio y ejecuta `git submodule update --init --recursive`. Así se restauran conjuntamente los adaptadores, la declaración de dependencias, el gitlink y la configuración de compilación y CI anteriores. Si el submódulo de Platform se añadió en la migración, Git puede dejar su directorio como no seguido; después de la reversión ya no se usa para compilar.

No es necesario migrar datos de usuario ni almacenamiento del relay. Las demás aplicaciones pueden conservar sus revisiones de Platform. Una comprobación del parche inverso de la migración completa permite verificar si la reversión del código se aplica sin conflictos.

Las comprobaciones locales de código y compilación no demuestran notarización, sustitución mediante un actualizador firmado, funcionamiento en hardware físico ni entrega a GitHub desde el despliegue. Sigue el procedimiento de publicación existente antes de distribuir la app.

<a id="relay-provenance"></a>

## Procedencia del relay

Los mecanismos extraídos del relay son aportaciones originales de Alonso para Dust Wave. El autor autorizó su uso bajo la licencia MIT de Platform el 25 de septiembre de 2026; el archivo NOTICE de Desktop Core registra ese permiso. Se excluye el código de ASCILINE original y se conserva la licencia de este repositorio.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/SHARED_DESKTOP_MIGRATION.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SHARED_DESKTOP_MIGRATION.md)
