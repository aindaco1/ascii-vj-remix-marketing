---
title: Rendimiento
description: Documentación de rendimiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Operaciones
lang: es
---

# Rendimiento

Esta guía documenta el modelo de desempeño actual, el comportamiento de aceptación y
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

## Comportamiento de aceptación práctica

Estos son criterios de regresión para el hardware compatible, no garantías de velocidad de fotogramas.
en cada máquina.

|Área|Objetivo|
| --- | --- |
|Imagen de demostración|El renderizador se inicia automáticamente y permanece receptivo mientras los ajustes preestablecidos/WTF/audio cambian los parámetros.|
|Vídeo de demostración|Reproducción fluida a través de cambios de fuente y transiciones preestablecidas sin reiniciar el video a menos que cambie la fuente.|
|vista previa principal|No colapsa a FPS bajo de un solo dígito únicamente porque Pop Out está abierto en hardware compatible.|
|Pop Out|Los enfoques de salida nativa muestran la actualización de la imagen de demostración y el vídeo de demostración en versiones optimizadas.|
|Cámara Pop Out|Prefiera rutas de captura/presentación nativas del último fotograma para minimizar la latencia visible.|
|Reactividad de audio|La respuesta visual sigue siendo inmediata y al mismo tiempo conserva un análisis estable de RMS/banda/tiempo.|
|Cambio de fuente|Los interruptores de imagen/vídeo integrados están limitados y no dejan el renderizador atascado.|
|Controlar la interfaz de usuario|Los controles deslizantes, los botones preestablecidos, la selección de fuente y el conmutador WTF permanecen interactivos bajo la carga de renderizado.|
|MIDI|Los controles continuos están fusionados en marcos y siguen respondiendo sin una actualización IPC/renderizado por mensaje de hardware sin formato.|

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
modulación, sincronización de salida nativa y MIDI.
- Cambie los controles de alta frecuencia por lotes a los cuadros de animación cuando sea posible.
- No reconstruya los recursos del renderizador para cambios de control numérico que puedan ser
actualizado como uniformes/params.
- Separe los cambios de fuente de los cambios de parámetros visuales.
- Conserve el tiempo de reproducción de medios activos cuando cambien los ajustes preestablecidos visuales.
- Mantenga los cambios discretos controlados y predecibles durante las transiciones.

## 0.9.6 Pase de optimización medido

La versión 0.9.6 elimina el trabajo repetido de configuración/copia de las rutas activas medidas sin
cambio de sombreadores, muestreo, matemáticas de color, selección de glifos, fuente/salida
resolución o controles de calidad.

|Camino|antes|0.9.6 comportamiento|
| --- | --- | --- |
|Vídeo nativo macOS Pop Out|Conversión de RGB a RGBA y carga de texturas en cada presentación de enlace de pantalla|Subir sólo cuando cambie la versión decodificada del marco fuente; continuar presentando y aplicando parámetros en cada marca de visualización|
|WebGPU|Nuevo almacenamiento de respaldo uniforme, vistas de texturas y grupos de encuadernación estables ensamblados por marco|Reutilice el almacenamiento uniforme, las vistas de texturas y los grupos de vinculación estables; El enlace de textura de vídeo externo permanece por fotograma.|
|WebGL2|18 llamadas `getUniformLocation` por cuadro|Resuelve las 18 ubicaciones una vez después de vincularlas.|
|Transiciones numéricas|Sincronización completa de fuente, cámara, visibilidad, medidor y superficie de control en cada cuadro de interpolación|Sincronice los valores cambiantes durante la interpolación y realice la actualización completa del estado final una vez|

En la versión de prueba optimizada de Apple Silicon macOS, el vídeo de demostración se decodificó a aproximadamente
23.8 FPS mientras que el Pop Out nativo se presenta en 60.1 FPS. Almacenamiento en caché de la versión fuente
realizó 23,8 cargas y omitió 36,3 cargas duplicadas por segundo, eliminando
aproximadamente el 60% de la frecuencia de carga de textura/conversión RGB anterior. Un punto de referencia
la ejecución aún puede verse afectada por la carga de la máquina; comparar la misma transición fija
objetivos, backend, duración, tipo de construcción y percentiles de fase en lugar de un
mínimo único.

En el mismo host, la referencia 0.9.5 publicada optimizada midió 35,8 FPS en
la fase principal y 39.3 FPS después de abrir Pop Out. El 0.9.6 final optimizado
El candidato midió 38,6 y 39,0 FPS respectivamente, luego 35,9 FPS durante la sesión fija.
abandono de transición numérica. El arnés más antiguo usaba una tercera fase aleatoria, por lo que solo
las fases constante principal/Pop Out se utilizan para esa comparación de versiones.

El arnés de humo del navegador también implementa una transición numérica de 250 ms. eso
requiere que la sincronización del control de fuente permanezca en no más de dos llamadas y
cámara/sincronización visual completa en no más de una llamada mientras se actualiza el valor
continúa durante toda la interpolación.

## Notas de backend

### WebGPU

WebGPU es el principal objetivo de calidad visual y la primera opción en capacidad
Tiempos de ejecución de Chromium/WebView.

Esté atento a:

- Costos de importación de texturas externas en cuadros de video.
- Tamaño de la textura de almacenamiento después de cambios de cuadrícula/celda.
- cambios de sombreado que aumentan el trabajo por píxel en tamaños de salida altos.
- rutas de transición que accidentalmente crean renderizadores completos adicionales durante demasiado tiempo.

### WebGL2

WebGL2 es el respaldo integrado más importante de GPU y realiza un seguimiento visual de WebGPU como
tan de cerca como sea práctico.

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
- Mantenga limitados los recursos en modo glifo. Los cambios en el juego de caracteres actualizan el
rampa/parámetros de glifos pequeños, no activan la carga de fuentes ilimitadas ni dinámicas grandes
asignación de atlas.
- Evite bloquear la interfaz de usuario principal mientras se presenta la ventana de salida.
- Cargue texturas de origen en los cambios de versión del marco de origen en lugar de mostrarlas
actualizar; Las personas que llaman de reserva sin versión deben continuar cargando.
- Mantenga contadores/registros disponibles para adquisición de fotogramas, presentación y parámetros.
versión, versión fuente y regresiones de ritmo.

## Presupuestos de fuentes específicas

### Imágenes estáticas

La representación de imágenes estáticas es el camino más barato. Jitter, modulación de audio,
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

El análisis de audio está optimizado para una respuesta en vivo estable.

Normas:

- Mantenga las ventanas del analizador y el suavizado lo suficientemente bajos para una respuesta en vivo.
- Utilice vectores de funciones como RMS, graves, medios, agudos, flujo, pulso de ritmo y
fase en lugar de muestras crudas ilimitadas.
- Mantenga los ayudantes de mezcla densa derivados de los mismos buffers del analizador delimitados:
bandas medias-bajas/medias-altas, la presencia, el brillo y la densidad no suman
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

### Control experimental MIDI

- Rust mantiene una cola de eventos limitada y descarta el evento más antiguo cuando está lleno.
- JavaScript conserva los bordes ordenados de los botones pero fusiona eventos continuos mediante
mensaje/canal/controlador antes de aplicar un marco.
- Los parámetros seguros en vivo se actualizan a través de configuradores de renderizador existentes.
- Los parámetros estructurales mantienen el camino de reconstrucción retrasado existente en lugar de
reconstrucción por cada incremento de 7 bits.
- La adquisición suave evita saltos disruptivos después de cambios preestablecidos sin agregar un
bucle de sondeo por enlace.
- El monitoreo del puerto se ejecuta a una cadencia fija baja; las lecturas de eventos normales están limitadas.
- La captura/restauración de SysEx es una operación de configuración explícita y nunca se ejecuta en el
renderizar hilo. La restauración de paquetes tiene un ritmo para hardware más antiguo.

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

`smoke:ui-perf` parte de los valores predeterminados canónicos y utiliza dos valores fijos,
objetivos de transición numérica no estructural. Registra promedio, P10, P50 y
vista previa mínima de FPS más tasas de salida nativas y los backends del renderizador en realidad
visitado. Para comparar un paquete exacto de aplicaciones instaladas o archivadas:

```bash
ASCILINE_SOURCE_APP="/absolute/path/ASCII VJ Remix Dev.app" \
ASCILINE_UI_PERF_SMOKE_DURATION_MS=30000 \
npm run smoke:ui-perf
```

Los registros de enlace de visualización nativos incluyen `sourceUploads` y `sourceUploadSkips`. por un
24 videos FPS en una salida de 60 Hz, la forma saludable esperada es de aproximadamente 24 cargas
y 36 saltos por segundo mientras la presentación permanece cerca de 60 FPS.

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
npm run test:midi
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

Punto de referencia prospectivo, prueba de latencia, uso compartido de texturas y panel de rendimiento
el trabajo se rastrea en [Roadmap](/es/docs/reference/roadmap/).


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/PERFORMANCE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/PERFORMANCE.md)
