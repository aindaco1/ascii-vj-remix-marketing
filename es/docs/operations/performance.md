---
title: Rendimiento
description: Documentación de rendimiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Operaciones
lang: es
---

<a id="performance"></a>

# Rendimiento

Esta guía documenta el modelo de rendimiento actual, el comportamiento de aceptación y las prácticas de validación para ASCII VJ Remix.

El trabajo de rendimiento consiste en el ritmo de fotogramas, la salida GPU, la decodificación de medios, la latencia de la cámara, la respuesta reactiva al audio, el Pop Out nativo y el mantenimiento de la capacidad de respuesta de la interfaz de usuario de control denso mientras el renderizador está bajo carga.

<a id="performance-principles"></a>

## Principios de desempeño

- Pruebe el rendimiento con compilaciones optimizadas al realizar afirmaciones de rendimiento.
- Conserve la calidad del renderizador antes de aceptar una ruta más rápida pero visiblemente peor.
- Evite reinicios del renderizador para realizar cambios de control seguros en vivo.
- Prefiere la semántica del último fotograma para la cámara en vivo y las rutas de salida.
- Mantenga la vista previa principal y Pop Out FPS medidas por separado.
- Mantenga el análisis de audio receptivo sin enviar búferes de audio sin procesar e ilimitados a través de IPC.
- Mantenga la aleatorización, los ajustes preestablecidos, la reactividad de audio y MIDI en la misma ruta fusionada de control en vivo.
- Mantenga todos los activos de tiempo de ejecución locales para que el rendimiento no dependa de la disponibilidad de la red.
- Resuelva la densidad a través de la política de columnas compartidas/celdas totales. Advanced Density es una preferencia global explícita, no una trampilla de escape visual preestablecida.
- Reconstruir tablas de búsqueda de paletas y rampas/páginas de glifos solo cuando cambien sus entradas discretas; Los fotogramas de audio y transición deben permanecer uniformes/actualizados en parámetros.
- Inicie la verificación de actualización de lanzamiento de producción de forma asincrónica. Un punto final de lanzamiento lento o no disponible no debe retrasar el inicio del renderizador, la fuente, el audio o el control.
- Mantenga los informes de fallos fuera de la ruta de renderizado. La captura, la puesta en cola, la desinfección y el envío deben estar delimitados y no deben bloquear la presentación del fotograma ni los controles en vivo.
- Vigila térmicas y batería. Esta aplicación puede mantener activos intencionalmente CPU, GPU, la cámara, la decodificación de medios y el análisis de audio.

<a id="practical-acceptance-behavior"></a>

## Comportamiento de aceptación práctica

Estos son criterios de regresión para el hardware compatible, no garantías de velocidad de fotogramas en cada máquina.

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

<a id="renderer-performance-model"></a>

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

- Utilice el modelo de parámetros canónicos para controles de interfaz de usuario, ajustes preestablecidos, WTF mode, modulación de audio, sincronización de salida nativa y MIDI.
- Cambie los controles de alta frecuencia por lotes a los cuadros de animación cuando sea posible.
- No reconstruya los recursos del procesador para cambios de control numérico que puedan actualizarse como uniformes/parámetros.
- Separe los cambios de fuente de los cambios de parámetros visuales.
- Conserve el tiempo de reproducción de medios activos cuando cambien los ajustes preestablecidos visuales.
- Mantenga los cambios discretos controlados y predecibles durante las transiciones.

<a id="110-local-spatial-baseline"></a>

## Mediciones espaciales locales de 1.1.0

La etapa espacial conserva los límites de densidad existentes. La geometría se calcula una vez por celda, con hasta 64 pasos de cuadrícula (48 de trazado de esferas para Orbitals); los reflejos añaden un rayo acotado. La realimentación reutiliza dos texturas de historial en coma flotante y la salida nativa conserva la caché de cargas por versión de la fuente. La caché compartida de visibilidad por columna sigue siendo una optimización futura.

La carga optimizada de ciudad, video y audio sintético a 640 columnas midió 39,1 FPS y 33,15 ms P95 en el preview con Pop Out abierto, y 60,1 FPS en la presentación nativa, en un M1 Max/64 GB con un 85 % de material de entrada. La prueba por fases superó los umbrales existentes, aunque persisten picos ocasionales. El alcance exacto, los fotogramas más lentos y los límites de la validación manual y del hardware mínimo constan en el [registro de la versión 1.1.0](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md#earlier-local-validation-before-fractal-follow-up).

<a id="096-measured-optimization-pass"></a>

## 0.9.6 Pase de optimización medido

La versión 0.9.6 elimina el trabajo repetido de configuración/copia de las rutas activas medidas sin cambiar los sombreadores, el muestreo, las matemáticas de color, la selección de glifos, la resolución de fuente/salida o los controles de calidad.

|Camino|antes|0.9.6 comportamiento|
| --- | --- | --- |
|Vídeo nativo macOS Pop Out|Conversión de RGB a RGBA y carga de texturas en cada presentación de enlace de pantalla|Subir sólo cuando cambie la versión decodificada del marco fuente; continuar presentando y aplicando parámetros en cada marca de visualización|
|WebGPU|Nuevo almacenamiento de respaldo uniforme, vistas de texturas y grupos de encuadernación estables ensamblados por marco|Reutilice el almacenamiento uniforme, las vistas de texturas y los grupos de vinculación estables; El enlace de textura de vídeo externo permanece por fotograma.|
|WebGL2|18 llamadas `getUniformLocation` por cuadro|Resuelve las 18 ubicaciones una vez después de vincularlas.|
|Transiciones numéricas|Sincronización completa de fuente, cámara, visibilidad, medidor y superficie de control en cada cuadro de interpolación|Sincronice los valores cambiantes durante la interpolación y realice la actualización completa del estado final una vez|

En la versión de prueba optimizada de Apple Silicon macOS, Demo Video se decodificó en aproximadamente 23,8 FPS, mientras que el Pop Out nativo se presentó en 60,1 FPS. El almacenamiento en caché de la versión fuente realizó 23,8 cargas y omitió 36,3 cargas duplicadas por segundo, eliminando aproximadamente el 60% de la frecuencia de carga de textura/conversión RGB anterior. Una ejecución de referencia aún puede verse afectada por la carga de la máquina; compare los mismos objetivos de transición fijos, backend, duración, tipo de compilación y percentiles de fase en lugar de un único mínimo.

En el mismo host, la referencia optimizada publicada 0.9.5 midió 35,8 FPS en la fase principal y 39,3 FPS después de abrir Pop Out. El candidato final optimizado 0.9.6 midió 38,6 y 39,0 FPS respectivamente, luego 35,9 FPS durante la rotación de transición numérica fija. El arnés más antiguo usaba una tercera fase aleatoria, por lo que solo se usan las fases principal constante/Pop Out para esa comparación de lanzamiento.

El arnés de humo del navegador también implementa una transición numérica de 250 ms. Requiere que la sincronización del control de fuente permanezca en no más de dos llamadas y la sincronización de cámara/visual completa en no más de una llamada mientras las actualizaciones de valores continúan durante la interpolación.

<a id="098-release-build-optimization"></a>

## 0.9.8 Optimización de compilación de lanzamiento

El trabajo de empaquetado Windows más lento de la versión 0.9.7 tomó aproximadamente 31 minutos. La compilación del código fuente FFmpeg tomó aproximadamente 12,5 minutos, la verificación de lanzamiento repetida aproximadamente 5,5 minutos y la compilación y empaquetado de la aplicación aproximadamente 10 minutos; esas etapas independientes fueron en su mayoría serializadas.

La versión 0.9.8 adapta el patrón de reutilización de compilación verificada utilizado por MKV Magic. La versión CI resuelve una confirmación de etiqueta inmutable y ejecuta la compilación del código fuente FFmpeg y la compilación de la aplicación Tauri `--no-bundle` simultáneamente. También espera el CI `Desktop` normal del compromiso exacto en lugar de repetir ese conjunto dentro de cada trabajo de empaquetado. Los trabajos de paquete aceptan solo los artefactos de flujo de trabajo de corta duración coincidentes, vuelven a verificar los recursos FFmpeg y verifican la confirmación, la plataforma, la versión, el tamaño y SHA-256 del binario de la aplicación antes de que `tauri bundle` la empaquete sin una segunda compilación. La firma, las firmas de actualizadores, la certificación notarial, la inspección de paquetes, las verificaciones de activos publicados y las instalaciones/actualizaciones reales siguen siendo puertas de liberación.

Esto cambia la ruta crítica de la suma de la compilación de la aplicación FFmpeg más a aproximadamente la más lenta de las dos, sin cambiar el código del procesador, los recursos enviados, las plataformas de destino, la política de firma o los formatos de salida.

<a id="0911-palette-dither-unicode-and-density-pass"></a>

## 0.9.11 Paleta, tramado, Unicode y paso de densidad

La base de referencia 0.9.11 es Apple M1/16 GB o un dispositivo similar Windows x64 integrado-GPU. Intel macOS no es un objetivo de lanzamiento. La carga de trabajo principal optimizada es video local de 1080p con reactividad de audio y una ventana de salida nativa visible; el objetivo de liberación es 30 FPS con un tiempo de cuadro P95 igual o inferior a 33,3 ms en el piso de referencia.

Los límites de densidad compartida son:

|Modo|columnas|Celdas totales|Promesa|
| --- | ---: | ---: | --- |
|Normal acelerada|640|160.000|Gama protegida por el rendimiento; Los ajustes preestablecidos permanecen aquí.|
|Software normal|120|6.000|Barandilla Lona Inferior/CPU.|
|Advanced Density|900|500.000|Preferencia global explícita; sin garantía de 30 FPS.|

El host de desarrollo M1 Max/64 GB es más rápido que el piso de referencia, por lo que sus resultados son evidencia de regresión local en lugar de aceptación del piso. En 640 columnas, la función WebGL2 midió 39,1 FPS principal, 39,9 FPS con salida nativa y 35,4 FPS durante la rotación de transición; El RSS máximo fue de aproximadamente 444 MB. Signal Court + Bayer 4 + la rampa unificada CJK midió 37,9, 40,1 y 37,0 FPS con aproximadamente 446 MB de pico RSS. Los valores principales/Pop Out/transición P95 fueron 29,6/29,4/31,6 ms, dentro del diez por ciento de las fases de funciones coincidentes. La salida nativa se mantuvo cerca de 60 FPS sin fallas en GPU.

Evidencia legible por máquina:

- `docs/performance/0.9.10-phase-zero-baseline.md`
- `docs/performance/0.9.11-density-feature-off-m1-max-webgl2.json`
- `docs/performance/0.9.11-density-feature-on-m1-max-webgl2.json`
- `docs/performance/0.9.11-pre-fix-occluded-output-soak-m1-max-webgl2.json`
- `docs/performance/0.9.11-background-memory-soak-m1-max-webgl2.json`

La primera inmersión desatendida de 15 minutos expuso un error de retención de recursos de salida nativa ocluidos: el RSS constante subió de 156,5 MB a 9411,9 MB porque los fotogramas de origen se cargaron antes de que hubiera una superficie de salida disponible para enviarlos. La salida nativa ahora adquiere la superficie antes de que se escriba en la cola, omite las cargas mientras está ocluida, drena el grupo de liberación automática del hilo de visualización por tick y las encuestas completadas GPU funcionan sin bloqueo. La ejecución repetida de 15 minutos comenzó con 156,1 MB de RSS constante y finalizó con 155,5 MB, una desviación de -0,6 MB, con un pico de inicio de 446,1 MB y sin fallas de sincronización nativa.

La repetición se ejecutó mientras la sesión desatendida de macOS mantenía la aplicación en segundo plano, por lo que WebKit limitó requestAnimationFrame y IPC nativo a aproximadamente 1 Hz. Esa ejecución es sólo evidencia de la duración de la memoria, no de aceptación de la velocidad de fotogramas. Las cifras de 640 columnas de la ventana visible de arriba siguen siendo la evidencia local FPS; El piso de referencia físico y la aceptación del desempeño Windows permanecen separados.

El atlas fuente Unicode está dividido en dieciséis páginas en escala de grises de 1024px. Solo se decodifican las páginas requeridas por la rampa activa de hasta 96 escalares de 96, y el caché del navegador compartido retiene como máximo cuatro páginas base más los mips de cobertura máxima generados. WebGPU compacta las máscaras activas y los cinco niveles de cobertura en una textura RGBA de 768x62, aproximadamente 186 KB de almacenamiento GPU. WebGL2 conserva la matriz R8 de 16 capas limitada y sus mips, mientras que el Pop Out nativo conserva la asignación de página base de 16 MB. Esto evita las paradas de página CJK de varios segundos que se observan con cuatro páginas de 2048 px y, al mismo tiempo, mantiene limitados los bytes del paquete, la caché CPU y la asignación WebGPU.

Las mediciones de funciones locales originales seleccionaron WebGL2 y siguen siendo evidencia de regresión GPU del navegador, no evidencia de aceptación para la vista previa del glifo Apple WebKit instalada.

En la vista principal de macOS con Apple WebKit, los presets de glifos aptos para aceleración usan la textura compacta de la rampa WebGPU. Los presets asignados explícitamente a Canvas2D conservan el límite de densidad por software. Una prueba histórica de 71 presets instalados asignó 43 a WebGPU y 28 a Canvas2D, mantuvo los 71 visibles y confirmó que todos los aptos para GPU estaban acelerados. Son mediciones históricas; el contrato actual 96/68/28 se define en [Pruebas](/es/docs/operations/testing/#renderer-backend-changes). Pop Out nativo sigue renderizándose de forma independiente en GPU. Una ejecución estructural anterior de 30 segundos mantuvo la vista principal a 30,0 FPS, la presentación nativa a 60,0 FPS y las cargas de la fuente a 23,5 FPS para el video de prueba de 24 FPS; completó 16 transiciones sincronizadas sin fallos de GPU ni de transición. Son resultados de regresión en un equipo de desarrollo M1 Max, no una certificación del mínimo M1/16 GB.

<a id="backend-notes"></a>

## Notas de backend

### WebGPU

WebGPU es el principal objetivo de calidad visual y la primera opción en tiempos de ejecución compatibles con Chromium y macOS Apple WebKit empaquetados.

El ajuste preestablecido de perfil limpio no debe poseer la preferencia de renderizado global. El backend predeterminado es Automático y se espera que las funciones integradas sin un backend de compatibilidad explícito se resuelvan primero en WebGPU y en segundo lugar en WebGL2.

Esté atento a:

- Costos de importación de texturas externas en cuadros de video.
- Tamaño de la textura de almacenamiento después de cambios de cuadrícula/celda.
- cambios de sombreado que aumentan el trabajo por píxel en tamaños de salida altos.
- rutas de transición que accidentalmente crean renderizadores completos adicionales durante demasiado tiempo.

### WebGL2

WebGL2 es el respaldo integrado más importante de GPU y realiza un seguimiento visual de WebGPU tan de cerca como sea práctico.

Esté atento a:

- Costo de carga de textura por cuadro.
- Manejo de pérdida de contexto.
- lecturas de lienzo adicionales.
- diferencias de precisión en gamma, cuantificación y saturación.

<a id="canvas2d-and-pixel-canvas"></a>

### Canvas2D y Pixel Canvas

Las rutas de lienzo preservan la compatibilidad y el linaje ASCILINE. No son el camino de mayor calidad, pero deben seguir siendo funcionales.

Esté atento a:

- Costo de representación de texto/glifo en un alto número de columnas.
- bucles por celda en el objetivo alto FPS.
- regresiones de compatibilidad de flujos.

<a id="native-pop-out"></a>

### Nativo Pop Out

La ruta de salida nativa existe porque un segundo renderizador de lienzo/vista web completo no fue lo suficientemente rápido para el objetivo del producto.

Normas:

- Utilice la salida nativa `wgpu` cuando esté disponible.
- Mantenga los permisos de la ventana de salida al mínimo.
- Prefiere la transferencia directa de fotogramas o rutas de captura nativas del último fotograma.
- Mantenga limitados los recursos en modo glifo. Los cambios en el conjunto de caracteres actualizan los parámetros/la rampa de glifos pequeños, no activan la carga de fuentes ilimitadas ni la asignación de atlas dinámicos grandes.
- Evite bloquear la interfaz de usuario principal mientras se presenta la ventana de salida.
- Arma las transiciones preestablecidas una vez con una marca de tiempo compartida. No serialice una actualización de parámetro de solicitud/respuesta por cuadro de animación mientras una interpolación nativa o un fundido cruzado puedan avanzar en el enlace de visualización.
- Mantenga la superficie nativa con la latencia de fotogramas mínima admitida para que el almacenamiento en búfer de la cadena de intercambio no agregue un retraso evitable entre la salida principal y la salida.
- Prefiera un formato de superficie nativo que no sea sRGB para que la cadena de intercambio no transforme las matemáticas de color del renderizador de espacio de bytes compartido por segunda vez.
- Cargue texturas de origen en los cambios de versión del marco de origen en lugar de actualizar la pantalla; Las personas que llaman de reserva sin versión deben continuar cargando.
- Mantenga contadores/registros disponibles para la adquisición de fotogramas, la presentación, la versión de parámetros, la versión de origen y las regresiones de ritmo.

<a id="source-specific-budgets"></a>

## Presupuestos de fuentes específicas

<a id="static-images"></a>

### Imágenes estáticas

La representación de imágenes estáticas es el camino más barato. La fluctuación, la modulación de audio y las transiciones WTF pueden animar la salida sin recargar la imagen.

Evitar:

- volver a decodificar o volver a cargar la misma imagen para cada ajuste preestablecido.
- restablecer la identidad de la fuente durante las transiciones preestablecidas.

<a id="video-files"></a>

### Archivos de vídeo

Los cambios de fuente de vídeo son estructurales; los cambios preestablecidos no lo son.

Evitar:

- reiniciar el vídeo en cambios preestablecidos.
- esperando un punto medio de transición antes de aplicar parámetros numéricos continuos.
- haciendo relecturas innecesarias del lienzo del video.

<a id="cameras"></a>

### Cámaras

La latencia de la cámara importa más que la fluidez del almacenamiento en búfer.

Normas:

- Prefiere la semántica del último fotograma.
- Mantenga la resolución de la cámara/FPS ajustable.
- No ponga en cola fotogramas antiguos de la cámara cuando el renderizador se quede atrás.
- Utilice rutas de captura/textura nativas de la plataforma donde produzcan reducciones de latencia significativas.
- Windows Media Foundation y Linux V4L2 de cámara única Pop Out alimentan al presentador nativo `wgpu` sin lectura de WebView o IPC por cuadro. Si falla la apertura nativa, el espejo limitado de 640x360 mantiene solo una solicitud en curso y tiene un límite de 30 FPS; Los diagnósticos informan el motivo de apertura nativa, FPS aceptado y tiempos de transferencia.
- Windows mantiene una sesión de captura Media Foundation para ambas vistas, sin un intento fallido de apertura compartida ni un segundo dispositivo abierto después de la verificación previa. La captura se ejecuta independientemente de la presentación de GPU y utiliza devoluciones de llamadas de muestra asincrónicas. Su último fotograma se reduce a un máximo de 640x360, se codifica en JPEG un máximo de 30 veces por segundo y se devuelve como IPC binario para la vista previa WebGPU existente. Este puente de origen limitado evita la antigua ruta de serialización JSON sin formato RGBA; Los diagnósticos exponen FPS aceptado, KiB/s codificados y latencia de lectura/codificación/decodificación.
- En Windows, la detección de controladores GPU nativos se ejecuta fuera del hilo de la interfaz y reutiliza su instancia entre aperturas. Los registros locales `NativeOutputStartup` separan el tiempo hasta el primer fotograma de cámara, la creación de la superficie y la preparación del dispositivo y pipeline. Los diagnósticos manuales incluyen la latencia del comando de apertura nativa; no miden el tiempo hasta el primer fotograma presentado.
- Para multicámara, sea explícito sobre el costo de la mezcla y el diseño seleccionado.

<a id="audio-reactivity"></a>

### Reactividad de audio

El análisis de audio está optimizado para una respuesta en vivo estable.

Las lecturas de características tienen una frecuencia objetivo de 120 Hz sin acumular solicitudes nativas simultáneas. La captura solicita búferes de 128 muestras por canal dentro de los límites del dispositivo (2,67 ms a 48 kHz) y recurre a su valor predeterminado si no los admite. Es una solicitud de tamaño de búfer, no una garantía de latencia del hardware. Los ataques son inmediatos al recibir los datos; Smoothing controla una caída basada en el tiempo y cero la omite. El valor predeterminado de 0,36 tiene una constante de caída de 25,92 ms. El historial y la caída de los pulsos también usan el tiempo transcurrido para que los búferes menores no acorten los pulsos.

`npm run test:audio-reactive` incluye una comparación determinista de muestreo y envolvente ante un cambio brusco: alcanzar el 90 % de un ataque tarda 8,33 ms con el modelo de 120 Hz, frente a 33,33 ms antes; caer al 10 % tarda 66,67 ms frente a 150 ms con el suavizado predeterminado. Son resultados del modelo de software y excluyen dispositivo, controlador, IPC, planificación del renderizado y latencia de pantalla. Para medir la captura real bajo carga, use la prueba de entrada nativa de [Pruebas](/es/docs/operations/testing/#audio-response).

Normas:

- Mantenga las ventanas del analizador y el suavizado lo suficientemente bajos para una respuesta en vivo.
- Utilice vectores de funciones como RMS, graves, medios, agudos, flujo, pulso de ritmo y fase en lugar de muestras sin procesar ilimitadas.
- Mantenga los ayudantes de mezcla densa derivados de los mismos buffers del analizador limitados: las bandas medias bajas/medias altas, la presencia, el brillo y la densidad no agregan historial ilimitado ni audio sin formato IPC.
- Modulación de abrazadera para que la alta sensibilidad no pueda generar pantallas en blanco o negro puro.
- Reinicie la captura automáticamente cuando cambie el dispositivo de entrada seleccionado.

<a id="crash-reporting"></a>

### Informe de fallos

Los informes de fallos deben ser oportunistas y de bajo costo.

Normas:

- Capture únicamente pequeños informes estructurados; no adjunte marcos, capturas de pantalla, archivos multimedia, audio sin formato ni registros largos.
- Las fallas del renderizador pueden vincular como máximo los ocho eventos de renderizador desinfectados más recientes; mantenga la colección delimitada y fuera del marco del trabajo.
- Mantenga las colas locales delimitadas por el recuento de informes y el tamaño de bytes.
- Envíe de forma asincrónica desde Rust con tiempos de espera de red cortos.
- Nunca espere a que se envíe el informe de fallos antes de iniciar los renderizadores, cambiar de fuente, abrir Pop Out o aplicar controles en vivo.
- Intente recurrir a Canvas inmediatamente después de un error de construcción de GPU; poner en cola su diagnóstico de forma asincrónica después de que el renderizador de reemplazo esté activo.
- En compilaciones de depuración/desarrollo, capture localmente pero rechace el envío de red.

<a id="experimental-midi-control"></a>

### Control experimental MIDI

- Rust mantiene una cola de eventos limitada y descarta el evento más antiguo cuando está lleno.
- JavaScript conserva los bordes ordenados de los botones pero fusiona eventos continuos por mensaje/canal/controlador antes de aplicar un marco.
- Los parámetros seguros en vivo se actualizan a través de configuradores de renderizador existentes.
- Los parámetros estructurales mantienen la ruta de reconstrucción retrasada existente en lugar de reconstruir cada incremento de 7 bits.
- La soft takeover evita saltos disruptivos después de cambios preestablecidos sin agregar un bucle de sondeo por enlace.
- El monitoreo del puerto se ejecuta a una cadencia fija baja; las lecturas de eventos normales están limitadas.
- La captura/restauración de SysEx es una operación de configuración explícita y nunca se ejecuta en el subproceso de renderizado. La restauración de paquetes tiene un ritmo para hardware más antiguo.

<a id="battery-and-thermal-guidance"></a>

## Guía térmica y de batería

La aplicación puede resultar pesada por diseño.

Para uso portátil:

- Utilice alimentación de CA para las actuaciones.
- Columnas inferiores, FPS, resolución de la cámara y fluctuación cuando suben las térmicas.
- Cierre Pop Out cuando no sea necesario.
- Evite varias cámaras con batería a menos que sea necesario.
- Trate los ventiladores y la regulación térmica como señales de rendimiento, no sólo como ruido.

<a id="validation-commands"></a>

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
npm run smoke:primary-presets
npm run test:native-output-log
npm run bench:density
```

`smoke:ui-perf` parte de valores predeterminados canónicos y utiliza dos objetivos de transición numéricos fijos y no estructurales. Registra promedio, P10, P50 y vista previa mínima FPS más tasas de salida nativas y los backends del renderizador realmente visitados, paleta/difuminado/conjunto de caracteres solicitados, reemplazos del renderizador, restablecimientos de fotogramas y una señal de píxeles del lienzo primario posterior a la ejecución. Un renderizador con marcos que avanzan pero un lienzo vacío falla el humo. Para comparar un paquete exacto de aplicaciones instaladas o archivadas:

```bash
ASCILINE_SOURCE_APP="/absolute/path/ASCII VJ Remix Dev.app" \
ASCILINE_UI_PERF_SMOKE_DURATION_MS=30000 \
npm run smoke:ui-perf
```

Agregue `ASCILINE_UI_PERF_SMOKE_STRUCTURAL=1` para alternar familias de renderizadores de glifos y sólidos durante la fase de transición. Esto ejercita el fundido cruzado nativo de dos pasadas e informa la cadencia de cuadros del enlace de visualización `transitioned` además de la cadencia de parámetros y modulación de audio.

`smoke:primary-presets` activa por separado todos los ajustes preestablecidos de Demo Image integrados dentro de la aplicación Apple WebKit instalada. Verifica el lienzo principal final para cada ajuste preestablecido, de modo que la salida Pop Out, una instantánea de transición intermedia o un recurso de renderizado posterior no puedan satisfacer la verificación de aceptación de la vista principal.

Ejemplo de comparación de funciones activas:

```bash
ASCILINE_UI_PERF_SMOKE_BACKEND=webgl2 \
ASCILINE_UI_PERF_SMOKE_PALETTE=signal-court \
ASCILINE_UI_PERF_SMOKE_DITHER=bayer4 \
ASCILINE_UI_PERF_SMOKE_CHARSET=cjk-basic \
ASCILINE_DENSITY_BENCH_COLUMNS=640 \
npm run bench:density
```

Los registros de enlace de visualización nativos incluyen `sourceUploads` y `sourceUploadSkips`. Para un vídeo de 24 FPS con una salida de 60 Hz, la forma saludable esperada es de aproximadamente 24 cargas y 36 saltos por segundo, mientras que la presentación permanece cerca de 60 FPS.

Puertas de escritorio y de liberación:

```bash
npm run test:desktop-updater
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

<a id="manual-performance-checks"></a>

## Comprobaciones manuales de rendimiento

Antes de enviar cambios de renderizador, fuente, salida o audio, verifique manualmente:

- La imagen de demostración comienza al cargarse.
- El vídeo de demostración se reproduce sin iniciar manualmente el renderizador.
- Cambiar la imagen de demostración y el vídeo de demostración es rápido.
- Las transiciones preestablecidas son suaves y no muestran fotogramas multimedia originales.
- Al menos un ajuste preestablecido ASCII tradicional, como Classic Camera ASCII, se representa correctamente en la vista previa principal y Pop Out.
- WTF mode se ejecuta indefinidamente y el cambio de fuente no afecta al renderizador.
- La reactividad del audio cambia visiblemente la salida con el micrófono/entrada seleccionado.
- Pop Out mantiene la vista previa principal receptiva.
- Pop Out refleja WTF y cambios audio-reactivos mientras es completamente visible.
- La paleta Pop Out, el brillo, el contraste y los colores de fondo coinciden con la vista previa principal del mismo ajuste preestablecido.
- La cámara Pop Out no se congela en el primer fotograma.
- La superposición de estadísticas informa datos FPS/cuadrícula/fuente/preestablecidos creíbles.

Para afirmaciones de rendimiento de compilación optimizada, utilice la aplicación creada en lugar del servidor de desarrollo o el paquete de depuración.

<a id="regression-signals"></a>

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

En [Roadmap](/es/docs/reference/roadmap/).] se realiza un seguimiento del trabajo prospectivo de referencia, prueba de latencia, uso compartido de texturas y panel de rendimiento.

<a id="104-resource-and-startup-work"></a>

## 1.0.4 Recursos y trabajo inicial

La primera vista previa ya no espera a la enumeración independiente de MIDI/dispositivo ni al envío del informe de fallos. El sondeo de la capacidad del renderizador se superpone a la carga de origen y las solicitudes simultáneas comparten un sondeo pendiente. El calentamiento nativo de GPU comienza después de la primera configuración de vista previa, en un trabajador, por lo que no compite con la selección inicial del controlador en el subproceso de la interfaz de usuario.

Las canalizaciones WebGPU se compilan de forma asincrónica y se comparten por dispositivo/tipo de fuente y formato de lienzo. La salida nativa comparte un adaptador/dispositivo/cola compatible y canalizaciones inmutables entre aperturas; la pérdida del dispositivo invalida ese caché y una superficie no compatible solicita un adaptador compatible. La creación de la superficie Windows aún se envía al subproceso de interfaz de usuario requerido. La ventana/superficie, la cámara, las texturas, las cargas y los buffers de fotogramas siguen siendo propiedad de cada presentador y se liberan al cerrar. Las salvaguardas existentes de adquisición antes de carga y de último fotograma permanecen activas.

La reutilización de la búsqueda de la paleta del navegador tiene un límite de 16 tablas (512 KiB); La reutilización nativa tiene un límite de 16 tablas (2 MiB más claves pequeñas). El orden de luminancia nativo se calcula una vez por instantánea de parámetro y el inicio del vídeo utiliza una sonda para geometría/FPS. Las actualizaciones en vivo de la tabla de visualización reutilizan los buffers y nunca reconstruyen estos recursos. La inicialización fallida del renderizador ahora destruye recursos parciales y WebGL2 también libera su búfer cuádruple/VAO.

La prueba de humo de rendimiento de la interfaz de usuario ahora informa la finalización/fallo real de la interfaz de usuario con un tiempo de espera limitado. La expiración del temporizador por sí sola nunca es una medida pasajera. Los resultados locales exactos y las limitaciones de la plataforma pertenecen al registro de versión [1.0.4](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.0.4.md).


Los acentos fractales añaden un bucle de Julia acotado con salida anticipada (máximo de 24 iteraciones) a la pasada de celdas existente cuando están activados en cualquier modo visual. Off, Amount en cero o Coverage en cero omiten el bucle. El vidrio espacial deforma el rayo principal de la escena sin trazados adicionales. Canvas reutiliza la memoria del campo y lo mantiene en caché cuando el reloj no cambia. Los límites de cuadrícula y la resolución existentes se conservan. Usa el barrido de presets de la vista principal instalada y una prueba de humo optimizada de interfaz y salida nativa con `ASCILINE_UI_PERF_SMOKE_SPATIAL='{"accentAmount":0.5,"accentCoverage":1}'` para medir la función en el dispositivo objetivo; el hardware de gama baja necesita su propia ejecución.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/PERFORMANCE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/PERFORMANCE.md)
