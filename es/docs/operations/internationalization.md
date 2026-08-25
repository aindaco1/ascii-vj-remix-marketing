---
title: Internacionalización
description: Documentación de internacionalización derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Operaciones
lang: es
---

# Internacionalización

Esta guía documenta los límites actuales del idioma, la propiedad de las cadenas y
reglas de localización segura para ASCII VJ Remix.

## Línea de base actual

- El inglés es el único idioma admitido para la aplicación y la documentación.
- La aplicación no tiene catálogo de traducción ni conmutador de configuración regional.
- La mayoría de las cadenas de UI viven directamente en `index.html`, `app.js` y la interfaz relacionada.
módulos.
- Metadatos de Tauri, cuadros de diálogo de escritorio, mensajes de estado/error y uso de macOS
Las descripciones están en inglés.
- Los nombres de los ajustes preestablecidos del usuario, los nombres de los archivos y los nombres de los dispositivos de hardware se muestran como
creado o reportado por el sistema operativo.
- La aplicación no descarga traducciones ni otros recursos lingüísticos en
tiempo de ejecución.

El trabajo prospectivo de catálogo, configuración regional y flujo de trabajo de traducción se rastrea únicamente en
la [Hoja de ruta](/es/docs/reference/roadmap/).

## Propiedad actual de la cadena

|Tipo de cadena|Propietario actual|Comportamiento actual|
| --- | --- | --- |
|Etiquetas de control de aplicaciones|`index.html`, `app.js` y módulos frontales|Literales en inglés.|
|Mensajes de estado y error|Módulos frontend y comandos Rust/Tauri|Literales en inglés.|
|ID preestablecidos|Código y datos preestablecidos|Estable e independiente del idioma.|
|Nombres para mostrar preestablecidos incorporados|Datos preestablecidos|Nombres ingleses.|
|Nombres preestablecidos de usuario|Datos de usuario|Se muestra exactamente como fue creado.|
|Nombres de dispositivos|SO y hardware|Se muestra según lo dispuesto por la plataforma.|
|Nombres de archivos|SO y datos de usuario|Se muestra según lo dispuesto por la plataforma.|
|Metadatos del producto|Recursos de plataforma y configuración de Tauri|El nombre del producto sigue siendo `ASCII VJ Remix`.|
|Cadenas de uso macOS|`src-tauri/Info.plist`|Descripciones en inglés de permisos activos.|
|Documentación|Archivos de rebajas|Inglés.|

## Reglas para texto visible para el usuario

- Mantenga las cadenas de tiempo de ejecución y los activos agrupados localmente.
- Mantenga los identificadores internos estables separados de las cadenas de visualización.
- No localice rutas de medios de usuario, nombres de archivos, nombres preestablecidos personalizados, hardware
nombres de dispositivos, identificadores de backend, nombres de códecs, canales MIDI, números CC, SysEx
bytes o extensiones de archivo.
- Evite construir oraciones concatenando fragmentos.
- Mantenga la pluralización y las unidades separables.
- Deje espacio para copias más largas en paneles de control compactos.
- Mantenga las etiquetas cerca de sus controles y mantenga las etiquetas accesibles alineadas con
etiquetas visibles.
- Evite el texto integrado en imágenes.
- Mantenga los atajos de teclado y los identificadores MIDI separados de la prosa.
- Conserve el nombre del producto `ASCII VJ Remix` en los metadatos de la plataforma.

## Números, unidades y formatos

Los controles actuales muestran segundos, FPS, columnas/filas, ancho/alto, porcentajes,
valores normalizados, nombres de dispositivos y nombres de archivos directamente desde la aplicación o plataforma
estado. Las unidades técnicas y los identificadores permanecen estables en toda la interfaz.

El código que agrega un valor formateado visible para el usuario mantiene el valor separado de su
etiqueta y evita fragmentos de oraciones codificadas. Formato de números según la configuración regional
Actualmente no está implementado.

## Presets, WTF, Audio y MIDI

- Los identificadores integrados y preestablecidos por el usuario permanecen estables.
- Los nombres preestablecidos del usuario siguen siendo creados por el usuario.
- Los datos preestablecidos importados y exportados no requieren una configuración regional para funcionar.
- MIDI ID de destino, ID de página, canales, números CC, bytes SysEx y valores predeterminados almacenados
Los identificadores siguen siendo independientes del idioma.
- Los nombres de dispositivos y archivos siguen siendo datos de plataforma/usuario en lugar de una copia de la aplicación.

## Tauri y texto del instalador

El texto de escritorio actualmente abarca:

- Descripciones de uso de macOS en `src-tauri/Info.plist`;
- Metadatos de los paquetes Windows y Linux;
- Cuadro de diálogo Tauri y cadenas de error; y
- mensajes de actualización.

Estas cadenas están en inglés y deben seguir siendo precisas para el comportamiento y
permisos presentes en la aplicación empaquetada.

## Validación actual

Las comprobaciones generales de construcción y humo estático utilizan la interfaz de usuario en inglés actual:

```bash
npm run build
npm run smoke:static
```

No hay ninguna clave faltante, clave no utilizada, diseño regional o configuración regional cruzada.
suite de importación/exportación porque la aplicación no tiene catálogo ni soporte adicional
local. Esta brecha se registra en [Testing](/es/docs/operations/testing/).

## Límites actuales

El producto actual no incluye traducción automática ni catálogo en tiempo de ejecución.
descargas, documentación traducida, diseño de derecha a izquierda, específico de la configuración regional
ajustes preestablecidos o localización de hardware/datos creados por el usuario. Esas son la hoja de ruta
decisiones en lugar de capacidades actuales indocumentadas.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/I18N.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/I18N.md)
