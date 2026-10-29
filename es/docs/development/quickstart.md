---
title: Inicio rápido
description: Documentación de inicio rápido derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 1
parent: Desarrollo
lang: es
---

<a id="quickstart"></a>

# Inicio rápido

Utilice el repositorio de origen como árbol de trabajo:

```bash
git clone https://github.com/aindaco1/ascii-vj-remix.git
cd ascii-vj-remix
git checkout eebf5bdca6c88c66a04cacd9a2a8256112880fdb
```

<a id="prerequisites"></a>

## Requisitos previos

Herramientas mínimas de desarrollo:

- Node.js 24 o posterior.
- npm.
- Cadena de herramientas estable Rust con Cargo.
- Git.
- Un navegador actualizado. Se recomienda Chromium para las pruebas de WebGPU.

Requisitos previos de escritorio específicos de la plataforma:

- macOS: Xcode completo y sus herramientas Metal para Syphon.
- Windows: Herramientas de compilación de Visual Studio con la carga de trabajo C++ y el tiempo de ejecución WebView2.
- Linux: paquetes de desarrollo de WebKitGTK 4.1, appindicator, cabeceras de desarrollo de ALSA, librsvg, OpenSSL, patchelf y herramientas de compilación. El descubrimiento NDI nativo también requiere las bibliotecas client/common de Avahi y el servicio `avahi-daemon` en ejecución.

Opcional pero útil:

- Podman para el shell de desarrollo reproducible Linux y experimentos de Python/OpenCV.
- FFmpeg/ffprobe para el desarrollo de motores de medios.
- Dependencias de Playwright para las pruebas de humo en el navegador.
- GitHub CLI para la gestión de secretos de lanzamiento.

<a id="first-time-setup"></a>

## Configuración por primera vez

Instale las dependencias JavaScript:

```bash
git submodule update --init shared/dust-wave-platform
npm ci
npm run video-io:stage
```

La preparación de los SDK descarga dependencias de compilación con versiones fijadas desde fuentes oficiales. Es compatible con macOS arm64 y Windows/Linux x64, y debe ejecutarse antes de compilar o verificar la app de escritorio. El desarrollo solo para navegador no utiliza transportes nativos. Consulta el [empaquetado de bibliotecas de video nativo](/es/docs/operations/release/#native-video-runtime-packaging).

Ejecute el servidor de desarrollo del navegador:

```bash
npm run dev
```

Abierto:

```text
http://127.0.0.1:8010/
```

Ejecute la prueba de humo estático:

```bash
npm run smoke:static
```

Ejecute la aplicación de escritorio en modo de desarrollo:

```bash
npm run tauri:dev
```

Ejecute las comprobaciones principales de la aplicación de escritorio:

```bash
npm run check:desktop
```

Usa `npm test` como entrada habitual de pruebas de desarrollo: ejecuta las comprobaciones de escritorio existentes, las pruebas de humo estáticas en navegador y la evaluación de Jev sobre evidencia sintética de comportamiento. `npm test -- --offline` omite expresamente la evaluación alojada. Consulta [Pruebas de desarrollo con Jev](/es/docs/operations/testing/#jev-development-testing) para la configuración local.

En los espacios de trabajo macOS almacenados en iCloud Drive, el asistente de compilación Tauri redirige la salida de destino a `/private/tmp/ascii-vj-remix-tauri-target` para que los atributos extendidos de iCloud no interrumpan la firma de la aplicación. Puede anular el directorio de compilación con `ASCILINE_TAURI_TARGET_DIR` o `CARGO_TARGET_DIR`.

<a id="first-verification-path"></a>

## Primera ruta de verificación

Elija el [conjunto de comprobaciones recomendado](/es/docs/operations/testing/#recommended-check-sets) para el cambio. Consulte [Cómo contribuir](/es/docs/development/contributing/) para la identidad de desarrollo, la firma local, FFmpeg y Podman, y [Comandos](/es/docs/reference/commands/) para el catálogo completo de scripts npm.

Para tareas de empaquetado, firma, publicación o actualización, siga [Lanzamiento y actualizaciones](/es/docs/operations/release/).

<a id="development-boundary"></a>

## Límite de desarrollo

No añadas fuentes alojadas en línea, CDN, decodificadores en línea, telemetría ni dependencias de ejecución alojadas. Incluye los recursos de ejecución localmente. Los archivos multimedia permanecen locales salvo que el usuario active una salida de video compartida: NDI usa la LAN; Syphon comparte con apps en la misma Mac. No se admite audio en los transportes.



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/CONTRIBUTORS.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/TESTING.md)
- [docs/RELEASING.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/RELEASING.md)
