---
title: Rendimiento
description: Documentación de rendimiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Operaciones
lang: es
---

# Rendimiento

Esta guía documenta el modelo de desempeño actual, los comportamientos objetivo y
prácticas de validación para ASCII VJ Remix.

El trabajo de interpretación tiene que ver con el ritmo del cuadro, GPU
salida, decodificación de medios, latencia de la cámara, respuesta audio reactiva, Pop Out nativo,
y mantener la interfaz de usuario de control densa respondiendo mientras el renderizador está bajo carga.

## Principios de desempeño

- Pruebe el rendimiento con compilaciones optimizadas al realizar afirmaciones de rendimiento.
- Conserve la calidad del renderizador antes de aceptar una ruta más rápida pero visiblemente peor.
- Evite reinicios del renderizador para realizar cambios de control seguros en vivo.
- Prefiere la semántica del último fotograma para la cámara en vivo y las rutas de salida.
- Mantenga la vista previa principal y Pop Out FPS medidas por separado.
- Mantenga la capacidad de respuesta del análisis de audio sin enviar buffers de audio sin procesar e ilimitados
a través de IPC.
- Mantenga la aleatorización, los ajustes preestablecidos, la reactividad de audio y MIDI en el mismo conjunto
ruta de control en vivo.
- Mantenga todos los activos de tiempo de ejecución locales para que el rendimiento no dependa de la red.
disponibilidad.
- Mantenga los informes de fallos fuera de la ruta de renderizado. Captura, colas, desinfección y
La presentación debe estar limitada y no debe bloquear la presentación del marco o la presentación en vivo.
controles.
- Vigila térmicas y batería. Esta aplicación puede mantener intencionalmente CPU, GPU, cámara,
decodificación de medios y análisis de audio activos.

## Objetivos prácticos

Estos son objetivos prácticos, no garantías estrictas para todo el hardware.

|Área|Objetivo|
| --- | --- |
|Imagen de demostración|El renderizador se inicia automáticamente y permanece receptivo mientras los ajustes preestablecidos/WTF/audio cambian los parámetros.|
|Vídeo de demostración|Reproducción fluida a través de cambios de fuente y transiciones preestablecidas sin reiniciar el video a menos que cambie la fuente.|
|Vista previa principal|No debe colapsar a FPS bajo de un solo dígito cuando Pop Out está abierto en hardware compatible.|
|Pop Out|La salida nativa debe acercarse a la actualización de la pantalla en la imagen de demostración y el vídeo de demostración en versiones optimizadas.|
|Cámara Pop Out|Prefiera rutas de captura/presentación nativas del último fotograma para minimizar la latencia visible.|
|Reactividad de audio|La respuesta visual debe ser inmediata y al mismo tiempo preservar un análisis estable de RMS/banda/tiempo.|
|Cambio de fuente|Los interruptores de imagen/vídeo integrados deben estar limitados y no deben dejar el renderizador atascado.|
|Controlar la interfaz de usuario|Los controles deslizantes, los botones preestablecidos, la selección de fuente y el conmutador WTF deben permanecer interactivos bajo la carga de renderizado.|

## Modelo de rendimiento del renderizador

El renderizador sigue este flujo:

```text
source adapter
  -> canonical params
  -> optional live modulation
  -> effective params
  -> renderer runtime
  -> main preview
  -> optional native/browser Pop Out
```

Las regresiones de rendimiento suelen ocurrir cuando una capa pasa por alto este modelo.

Normas:

- Utilice el modelo de parámetros canónicos para controles de interfaz de usuario, ajustes preestablecidos, WTF mode y audio.
modulación, sincronización de salida nativa y futuro MIDI.
- Cambie los controles de alta frecuencia por lotes a los cuadros de animación cuando sea posible.
- No reconstruya los recursos del renderizador para cambios de control numérico que puedan ser
actualizado como uniformes/params.
- Separe los cambios de fuente de los cambios de parámetros visuales.
- Conserve el tiempo de reproducción de medios activos cuando cambien los ajustes preestablecidos visuales.
- Mantenga los cambios discretos controlados y predecibles durante las transiciones.

## Notas de backend

### WebGPU

WebGPU es el principal objetivo de calidad visual. Debería seguir siendo la primera opción
tiempos de ejecución compatibles con Chromium/WebView.

Esté atento a:

- Costos de importación de texturas externas en cuadros de video.
- Tamaño de la textura de almacenamiento después de cambios de cuadrícula/celda.
- cambios de sombreado que aumentan el trabajo por píxel en tamaños de salida altos.
- rutas de transición que accidentalmente crean renderizadores completos adicionales durante demasiado tiempo.

### WebGL2

WebGL2 es el respaldo integrado más importante de GPU. Debería realizar un seguimiento visual
WebGPU lo más fielmente posible.

Esté atento a:

- Costo de carga de textura por cuadro.
- Manejo de pérdida de contexto.
- lecturas de lienzo adicionales.
- diferencias de precisión en gamma, cuantificación y saturación.

### Canvas2D y Pixel Canvas

Las rutas de lienzo preservan la compatibilidad y el linaje ASCILINE. Ellos no son los
camino de la más alta calidad, pero deben seguir siendo funcionales.

Esté atento a:

- Costo de representación de texto/glifo en un alto número de columnas.
- bucles por celda en el objetivo alto FPS.
- regresiones de compatibilidad de flujos.

### Nativo Pop Out

La ruta de salida nativa existe porque se creó un segundo renderizador de lienzo/vista web completo.
no lo suficientemente rápido para el objetivo del producto.

Normas:

- Utilice la salida nativa `wgpu` cuando esté disponible.
- Mantenga los permisos de la ventana de salida al mínimo.
- Prefiere la transferencia directa de fotogramas o rutas de captura nativas del último fotograma.
- Mantenga limitados los recursos en modo glifo. Los cambios en el juego de caracteres deberían actualizar el
rampa/parámetros de glifos pequeños, no activan la carga de fuentes ilimitadas ni dinámicas grandes
asignación de atlas.
- Evite bloquear la interfaz de usuario principal mientras se presenta la ventana de salida.
- Mantenga contadores/registros disponibles para adquisición de fotogramas, presentación y parámetros.
versión, versión fuente y regresiones de ritmo.

## Presupuestos de fuentes específicas

### Imágenes estáticas

La representación de imágenes estáticas debería ser la opción más económica. Jitter, modulación de audio,
y las transiciones WTF pueden animar la salida sin recargar la imagen.

Evitar:

- volver a decodificar o volver a cargar la misma imagen para cada ajuste preestablecido.
- restablecer la identidad de la fuente durante las transiciones preestablecidas.

### Archivos de vídeo

Los cambios de fuente de vídeo son estructurales; los cambios preestablecidos no lo son.

Evitar:

- reiniciar el vídeo en cambios preestablecidos.
- esperando un punto medio de transición antes de aplicar parámetros numéricos continuos.
- haciendo relecturas innecesarias del lienzo del video.

### Cámaras

La latencia de la cámara importa más que la fluidez del almacenamiento en búfer.

Normas:

- Prefiere la semántica del último fotograma.
- Mantenga la resolución de la cámara/FPS ajustable.
- No ponga en cola fotogramas antiguos de la cámara cuando el renderizador se quede atrás.
- Utilice rutas de captura/textura nativas de la plataforma donde produzcan resultados significativos.
reducciones de latencia.
- Para multicámara, sea explícito sobre el costo de la mezcla y el diseño seleccionado.

### Reactividad de audio

El análisis de audio debe ser estable pero no lento.

Normas:

- Mantenga las ventanas del analizador y el suavizado lo suficientemente bajos para una respuesta en vivo.
- Utilice vectores de funciones como RMS, graves, medios, agudos, flujo, pulso de ritmo y
fase en lugar de muestras crudas ilimitadas.
- Mantenga los ayudantes de mezcla densa derivados de los mismos buffers del analizador delimitados:
bandas medias-bajas/medias-altas, la presencia, el brillo y la densidad no deberían sumar
Historia ilimitada o audio sin formato IPC.
- Modulación de abrazadera para que la alta sensibilidad no pueda generar negro puro o blanco puro
pantallas.
- Reinicie la captura automáticamente cuando cambie el dispositivo de entrada seleccionado.

### Informe de fallos

Los informes de fallos deben ser oportunistas y de bajo costo.

Normas:

- Capture únicamente pequeños informes estructurados; no adjunte marcos, capturas de pantalla,
archivos multimedia, audio sin procesar o registros largos.
- Mantenga las colas locales delimitadas por el recuento de informes y el tamaño de bytes.
- Envíe de forma asincrónica desde Rust con tiempos de espera de red cortos.
- Nunca espere el envío del informe de fallas antes de iniciar los renderizadores, cambiar
fuentes, abriendo Pop Out o aplicando controles en vivo.
- En compilaciones de depuración/desarrollo, capture localmente pero rechace el envío de red.

## Guía térmica y de batería

La aplicación puede resultar pesada por diseño.

Para uso portátil:

- Utilice alimentación de CA para las actuaciones.
- Columnas inferiores, FPS, resolución de la cámara y fluctuación cuando suben las térmicas.
- Cierre Pop Out cuando no sea necesario.
- Evite varias cámaras con batería a menos que sea necesario.
- Trate los ventiladores y la regulación térmica como señales de rendimiento, no sólo como ruido.

## Comandos de validación

Comprobaciones generales de compilación/fuera de línea:

```bash
npm run build
npm run check:offline
```

Arnés estático/navegador:

```bash
npm run smoke:static
```

Ayudantes de rendimiento de interfaz de usuario y salida nativa:

```bash
npm run smoke:native-output
npm run smoke:ui-perf
npm run test:native-output-log
```

Puertas de escritorio y de liberación:

```bash
npm run check:desktop
npm run check:release
```

Tubería de medios:

```bash
npm run check:media
npm run test:rust
```

Simulación de pantalla secundaria:

```bash
npm run test:output-display
```

## Comprobaciones manuales de rendimiento

Antes de enviar cambios de renderizador, fuente, salida o audio, verifique manualmente:

- La imagen de demostración comienza al cargarse.
- El vídeo de demostración se reproduce sin iniciar manualmente el renderizador.
- Cambiar la imagen de demostración y el vídeo de demostración es rápido.
- Las transiciones preestablecidas son suaves y no muestran fotogramas multimedia originales.
- Al menos un ajuste preestablecido ASCII tradicional, como Classic Camera ASCII, representa
correctamente en la vista previa principal y Pop Out.
- WTF mode se ejecuta indefinidamente y el cambio de fuente no afecta al renderizador.
- La reactividad del audio cambia visiblemente la salida con el micrófono/entrada seleccionado.
- Pop Out mantiene la vista previa principal receptiva.
- Pop Out refleja WTF y cambios audio-reactivos mientras es completamente visible.
- La cámara Pop Out no se congela en el primer fotograma.
- La superposición de estadísticas informa datos FPS/cuadrícula/fuente/preestablecidos creíbles.

Para afirmaciones de rendimiento de compilación optimizada, use la aplicación compilada en lugar del desarrollador
servidor o paquete de depuración.

## Señales de regresión

Investigue inmediatamente cuando:

- La vista previa principal se limita a un nivel bajo de FPS solo mientras Pop Out está abierto.
- Pop Out solo se actualiza correctamente cuando se arrastra parcialmente fuera de la pantalla.
- las transiciones preestablecidas se detienen antes de que los parámetros numéricos comiencen a cambiar.
- El vídeo se reinicia al cambiar el preset.
- El cambio de fuente lleva varios segundos para los medios integrados.
- La reactividad del audio tiene un retraso visual obvio después de cambios de ritmo/transitorios.
- la salida de la cámara se congela o acumula fotogramas obsoletos.
- El uso de CPU/GPU aumenta después de cerrar Pop Out.

## Trabajo de desempeño futuro

- Conjunto de pruebas comparativas de compilación optimizada y repetible.
- Pruebas sintéticas de latencia de cámara con marca de tiempo.
- Pruebas de tiempo de respuesta de audio-reactividad.
- Pruebas visuales limitadas o de salida dorada para ajustes preestablecidos representativos.
- Rutas nativas para compartir texturas en Windows y Linux comparables a macOS
trabajo de cámara/salida.
- Paneles de rendimiento para la vista previa principal FPS, salida FPS, caídas de fotogramas y
propagación de la versión del parámetro.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/PERFORMANCE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/PERFORMANCE.md)
