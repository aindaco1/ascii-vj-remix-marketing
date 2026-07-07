---
title: Internacionalización
description: Documentación de internacionalización derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 5
parent: Operaciones
lang: es
---

# Internacionalización

Esta guía establece prácticas de internacionalización y localización para
ASCII VJ Remix.

El trabajo de localización aquí debería centrarse en las cadenas de aplicaciones incluidas, Tauri
metadatos, descripciones de permisos, texto del instalador, documentos y ajustes preestablecidos futuros/MIDI
perfil UX.

## Línea de base actual

Estado actual:

- El inglés es el único idioma admitido por la aplicación.
- Aún no existe un catálogo de traducción formal.
- La mayoría de las cadenas de UI se encuentran actualmente en `index.html`, `app.js` y relacionados.
módulos frontales.
- Los metadatos de la aplicación Tauri y las cadenas de uso de macOS están en inglés.
- La documentación es inglesa.
- Los nombres preestablecidos creados por el usuario y los nombres de archivos personalizados se muestran como creados.

Esto es aceptable para 0.9.0, pero el trabajo futuro de la interfaz de usuario debería evitar hacer
la localización es más difícil.

## Principios

- Mantenga las traducciones agrupadas localmente. No utilice servicios de traducción en línea en
tiempo de ejecución.
- Mantenga los identificadores internos estables separados de las cadenas de visualización.
- Trate el inglés como idioma de origen canónico hasta que exista un flujo de trabajo de traducción.
existe.
- No localice rutas de medios de usuario, nombres de archivos, nombres preestablecidos personalizados ni hardware
nombres de dispositivos.
- Localice etiquetas, texto de ayuda, mensajes de estado, errores, menús, copia del instalador,
cadenas de uso de permisos y documentos cuando se admite una configuración regional.
- Mantenga las unidades y el formato numérico conscientes de la configuración regional cuando sea práctico.
- Mantenga las etiquetas de accesibilidad localizadas con etiquetas visibles.

## Modelo de catálogo futuro

Cuando comience la localización, prefiera una estructura de catálogo pequeña, como por ejemplo:

```text
src/i18n/
  en.json
  es.json
```

o una estructura de módulo equivalente propiedad de la aplicación. Las limitaciones importantes son:

- Los catálogos se envían dentro del paquete de aplicaciones.
- Las claves que faltan vuelven al inglés.
- Las claves son estables y descriptivas.
- La copia visible no está duplicada en `index.html`, `app.js` y Tauri.
diálogos.
- Las pruebas pueden comprobar si faltan claves y si hay claves obsoletas.

No agregue un CMS remoto, un catálogo alojado en CDN ni una dependencia de traducción de red.

## Propiedad de la cadena

|Tipo de cadena|propietario|Notas|
| --- | --- | --- |
|Etiquetas de control de aplicaciones|Catálogo incluido futuro|Fuente, Presets, Cuadrícula, Color, Muestreo, Audio, Salida.|
|Mensajes de estado/error|Catálogo incluido futuro|Incluya errores de permisos, medios, backend, actualizador y fuente.|
|ID preestablecidos|Código/datos|Estable, no localizado.|
|Nombres para mostrar preestablecidos incorporados|Catálogo incluido futuro|El nombre para mostrar se puede localizar mientras que la identificación permanece estable.|
|Nombres preestablecidos de usuario|Datos de usuario|Mostrar exactamente como fue creado.|
|Nombres de dispositivos|SO/hardware|Visualización según lo dispuesto por la plataforma.|
|Nombres de archivos|SO/datos de usuario|Visualización según lo dispuesto por la plataforma.|
|Metadatos Tauri|Configuración/recursos de Tauri|El nombre del producto permanece `ASCII VJ Remix`; El texto del instalador se puede localizar más tarde.|
|Cadenas de uso macOS|`src-tauri/Info.plist`|Debe ser preciso en cada lugar de envío.|
|Documentación|Documentos de rebajas|Traducir sólo cuando haya una ruta de mantenimiento.|

## Reglas de la interfaz de usuario

Al agregar o cambiar texto visible para el usuario:

- Evite construir oraciones concatenando fragmentos.
- Mantenga la pluralización y las unidades separables.
- Evite el formato de fecha/hora/número codificado.
- Deje espacio para cadenas traducidas más largas en paneles compactos.
- No codifique la semántica solo en nombres preestablecidos o etiquetas de colores.
- Mantenga las etiquetas cerca de los controles para que el texto traducido siga siendo comprensible.
- Evite el texto integrado en imágenes.
- Mantenga los atajos de teclado y las etiquetas MIDI separados de la prosa traducida.

## Números, unidades y formatos

Los controles actuales utilizan valores como:

- artículos de segunda clase.
- FPS.
- columnas/filas.
- ancho/alto.
- porcentajes o valores del control deslizante normalizados.
- nombres de dispositivos.
- nombres de archivos.

La localización futura debería:

- formatear decimales de manera consistente.
- preservar unidades técnicas como FPS donde se esperaba.
- Evite traducir extensiones de archivos, identificadores de backend, nombres de códecs o nombres de dispositivos.
- utilice el formato numérico que tenga en cuenta la configuración regional para los valores mostrados cuando no lo haga
crear una agitación ruidosa en la interfaz de usuario.

## Presets, WTF, Audio y MIDI

Los datos visuales preestablecidos deben mantener identificadores estables.

Reglas de localización futuras:

- Los nombres para mostrar preestablecidos incorporados pueden localizarse.
- Los identificadores preestablecidos integrados no deben localizarse.
- Los nombres preestablecidos del usuario deben seguir siendo creados por el usuario.
- Los paquetes preestablecidos importados deben declarar su idioma solo para los metadatos de visualización.
- Los ID de destino de mapeo MIDI no deben localizarse.
- Las etiquetas de control MIDI que se muestran al usuario pueden localizarse.
- Los perfiles exportados no deberían requerir una configuración regional para funcionar.

## Tauri y localización del instalador

La localización de escritorio tiene piezas específicas de la plataforma:

- Descripciones de uso de macOS en `src-tauri/Info.plist`.
- Metadatos del instalador Windows y futura presentación firmada del editor.
- Metadatos de escritorio Linux.
- Tauri cadenas de diálogo/error.
- Mensajes de actualización.

Antes de enviar una nueva ubicación:

1. Confirme que las cadenas de la interfaz de usuario de la aplicación estén traducidas.
2. Confirme que las cadenas de uso de permisos estén traducidas o intencionalmente en inglés.
3. Confirme que el texto del instalador/actualización esté traducido donde la plataforma lo admita.
4. Confirme que el diseño aún se adapta a paneles compactos.
5. Confirme que las etiquetas de accesibilidad coincidan con las etiquetas visibles.
6. Confirme que los documentos indiquen a los usuarios qué idiomas son compatibles.

## Expectativas de prueba

Controles actuales:

```bash
npm run build
npm run smoke:static
```

Las comprobaciones futuras del i18n deberían incluir:

- Detección de clave faltante.
- Detección de claves no utilizadas.
- prueba de humo en cada lugar admitido.
- comprobaciones de captura de pantalla/diseño para paneles compactos con cadenas más largas.
- verificaciones de permisos/mensajes de error.
- comprobaciones de compatibilidad de importación/exportación entre configuraciones regionales.

## Límites actuales

Fuera de alcance hoy:

- Tubería de traducción automática.
- Descarga en tiempo de ejecución de catálogos de traducción.
- Sitio de documentación localizada.
- Soporte de diseño de derecha a izquierda.
- Ajustes preestablecidos específicos de la configuración regional o valores predeterminados visuales específicos de la cultura.
- Localización de nombres de dispositivos de hardware o contenido escrito por el usuario.

Estos se pueden revisar después de la aplicación de escritorio principal, el proceso de lanzamiento y
el comportamiento del renderizador se estabiliza.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/I18N.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/I18N.md)
