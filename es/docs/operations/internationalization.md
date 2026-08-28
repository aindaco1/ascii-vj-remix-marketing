---
title: Internacionalización
description: Documentación de internacionalización derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Operaciones
lang: es
---

# Internacionalización

Esta guía documenta los límites del idioma actual, la propiedad de cadenas y las reglas de localización segura para ASCII VJ Remix.

## Línea de base actual

- El inglés es el único idioma admitido para la aplicación y la documentación.
- La aplicación no tiene catálogo de traducción ni conmutador de configuración regional.
- La mayoría de las cadenas de interfaz de usuario se encuentran directamente en `index.html`, `app.js` y módulos de interfaz relacionados.
- Los metadatos de Tauri, los cuadros de diálogo del escritorio, los mensajes de estado/error y las descripciones de uso de macOS están en inglés.
- Los nombres preestablecidos de usuario, nombres de archivos y nombres de dispositivos de hardware se muestran tal como fueron creados o informados por el sistema operativo.
- La aplicación no descarga traducciones ni otros recursos lingüísticos durante el tiempo de ejecución.
- La representación de glifos multilingüe se admite independientemente de la localización de la interfaz de usuario. El atlas neutral incluido cubre bloques seleccionados de latín, griego, cirílico, símbolo, CJK/Kana y Hangul, pero la interfaz de usuario de control sigue siendo en inglés.

El seguimiento del trabajo prospectivo de catálogo, configuración regional y flujo de trabajo de traducción se realiza únicamente en [Roadmap](/es/docs/reference/roadmap/).

## Propiedad actual de la cadena

|Tipo de cadena|Propietario actual|Comportamiento actual|
| --- | --- | --- |
|Etiquetas de control de aplicaciones|`index.html`, `app.js` y módulos frontales|Literales en inglés.|
|Mensajes de estado y error|Módulos frontend y comandos Rust/Tauri|Literales en inglés.|
|ID preestablecidos|Código y datos preestablecidos|Estable e independiente del idioma.|
|Nombres para mostrar preestablecidos incorporados|Datos preestablecidos|Nombres ingleses.|
|Identificadores de paleta y conjunto de glifos|Catálogos compartidos|Estable e independiente del idioma.|
|Rampas de glifos personalizadas escritas|Datos de usuario|Conservado como escalares Unicode admitidos, con un límite de 96.|
|Nombres preestablecidos de usuario|Datos de usuario|Se muestra exactamente como fue creado.|
|Nombres de dispositivos|SO y hardware|Se muestra según lo dispuesto por la plataforma.|
|Nombres de archivos|SO y datos de usuario|Se muestra según lo dispuesto por la plataforma.|
|Metadatos del producto|Recursos de plataforma y configuración de Tauri|El nombre del producto sigue siendo `ASCII VJ Remix`.|
|Cadenas de uso macOS|`src-tauri/Info.plist`|Descripciones en inglés de permisos activos.|
|Documentación|Archivos de rebajas|Inglés.|

## Reglas para texto visible para el usuario

- Mantenga las cadenas de tiempo de ejecución y los activos agrupados localmente.
- Mantenga los identificadores internos estables separados de las cadenas de visualización.
- No localice rutas de medios de usuario, nombres de archivos, nombres preestablecidos personalizados, nombres de dispositivos de hardware, identificadores de backend, nombres de códecs, canales MIDI, números CC, bytes SysEx ni extensiones de archivos.
- Evite construir oraciones concatenando fragmentos.
- Mantenga la pluralización y las unidades separables.
- Deje espacio para copias más largas en paneles de control compactos.
- Mantenga las etiquetas cerca de sus controles y mantenga las etiquetas accesibles alineadas con las etiquetas visibles.
- Evite el texto integrado en imágenes.
- Mantenga los atajos de teclado y los identificadores MIDI separados de la prosa.
- Conserve el nombre del producto `ASCII VJ Remix` en los metadatos de la plataforma.

## Números, unidades y formatos

Los controles actuales muestran segundos, FPS, columnas/filas, ancho/alto, porcentajes, valores normalizados, nombres de dispositivos y nombres de archivos directamente desde el estado de la aplicación o la plataforma. Las unidades técnicas y los identificadores permanecen estables en toda la interfaz.

El código que agrega un valor formateado visible para el usuario mantiene el valor separado de su etiqueta y evita fragmentos de oraciones codificadas. Actualmente, el formato de números compatible con la configuración regional no está implementado.

## Presets, WTF, Audio y MIDI

- Los identificadores integrados y preestablecidos por el usuario permanecen estables.
- Los nombres preestablecidos del usuario siguen siendo creados por el usuario.
- Los datos preestablecidos importados y exportados no requieren una configuración regional para funcionar.
- Los identificadores de destino MIDI, los identificadores de página, los canales, los números CC, los bytes SysEx y los identificadores preestablecidos almacenados siguen siendo independientes del idioma.
- Los nombres de dispositivos y archivos siguen siendo datos de plataforma/usuario en lugar de una copia de la aplicación.
- Los identificadores de paleta, los identificadores de modo de tramado, los identificadores de estilo atlas y los identificadores de conjunto de caracteres permanecen estables incluso si sus etiquetas de visualización se localizan más adelante.

## Salida de glifos multilingüe

La cobertura de glifos es una función de representación, no una afirmación de que la interfaz de usuario de la aplicación o el resultado generado estén traducidos. La versión 0.9.11 admite puntuación/radicales CJK, Hiragana, Katakana, CJK ideógrafos unificados U+4E00-U+9FFF y sílabas Hangul junto con los bloques de símbolos latinos, griegos, cirílicos y documentados.

El renderizador trata un escalar Unicode como una celda visual. No realiza segmentación de grupos de grafemas, configuración de guiones, diseño de párrafos bidireccionales, composición de secuencias de emoji ni diseño de texto legible. Los escalares no admitidos se eliminan de las rampas escritas con comentarios de texto limitados. La extensión A y los planos suplementarios CJK siguen siendo trabajos de la hoja de ruta.

## Tauri y texto del instalador

El texto de escritorio actualmente abarca:

- Descripciones de uso de macOS en `src-tauri/Info.plist`;
- Metadatos de los paquetes Windows y Linux;
- Cuadro de diálogo Tauri y cadenas de error; y
- mensajes de actualización.

Estas cadenas están en inglés y deben seguir siendo precisas para el comportamiento y los permisos presentes en la aplicación empaquetada.

## Validación actual

Las comprobaciones generales de construcción y humo estático utilizan la interfaz de usuario en inglés actual:

```bash
npm run build
npm run smoke:static
```

No hay ningún paquete de importación/exportación de claves faltantes, claves no utilizadas, diseño local o entre localidades porque la aplicación no tiene catálogo ni configuración regional compatible adicional. Esta brecha se registra en [Testing](/es/docs/operations/testing/).

## Límites actuales

El producto actual no incluye traducción automática, descargas de catálogos en tiempo de ejecución, documentación traducida, diseño de derecha a izquierda, ajustes preestablecidos específicos de la configuración regional ni localización de hardware/datos escritos por el usuario. Se trata de decisiones de hoja de ruta más que de capacidades actuales no documentadas.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/I18N.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/I18N.md)
