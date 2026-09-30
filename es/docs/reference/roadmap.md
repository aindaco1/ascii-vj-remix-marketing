---
title: Hoja de ruta
description: Documentación de hoja de ruta derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Referencia
lang: es
---

<a id="roadmap"></a>

# Hoja de ruta

Este documento contiene únicamente trabajos prospectivos. No es una descripción del producto actual y no promete una fecha o versión de lanzamiento. El comportamiento actual pertenece a la [Guía del usuario](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/USER_GUIDE.md) y guías de práctica; El trabajo completado y el historial de lanzamientos pertenecen al [Changelog](/es/docs/reference/changelog/).

<a id="distribution-and-platform-validation"></a>

## Distribución y Validación de Plataforma

- Complete las comprobaciones físicas pendientes de la [versión 1.1.0 Spatial ASCII aprobada por el responsable](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md#release-decision--2026-09-29): rendimiento en el hardware mínimo de referencia, cámaras, audio y GPU en Windows/Linux, alineación de pantallas externas, MIDI físico y latencia del sonido a la pantalla.

- Completar la aceptación de [macOS 27 (#30)](https://github.com/aindaco1/ascii-vj-remix/issues/30), incluida la regresión en tiempo de ejecución de macOS 13, captura física/MIDI/permisos y comprobaciones de visualización externa, y promoción de cadena de herramientas/artefactos Xcode 27 firmados. La evidencia publicada actual y los límites restantes se encuentran en el registro [1.0.4](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.0.4.md#issue-review--2026-09-16).

- Agregue firma Authenticode y marca de tiempo para los instaladores Windows cuando exista un proveedor de firma sostenible y una política de lanzamiento.
- Valide el comportamiento de Windows SmartScreen en máquinas limpias después de que comience la distribución firmada.
- Ejecute pruebas de humo de instalación, lanzamiento y actualización en máquinas Windows y Linux físicas o virtuales representativas.
- Valide los paquetes Linux AppImage, deb y rpm en una matriz de distribución mantenida. Complete las pruebas de la cámara física de Ubuntu/Fedora aplazadas en la [decisión de lanzamiento 1.0.3](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.0.3.md#release-decision--2026-09-04), utilizando las [verificaciones de hardware](/es/docs/operations/testing/#hardware-and-platform-checks).
- Confirme que las concesiones de privacidad de macOS sobrevivan a un actualizador público de identidad estable en una máquina limpia.
- Decida si las versiones de Windows necesitan un tiempo de ejecución fijo de WebView2 para la instalación sin conexión.

<a id="midi-controllers-and-profiles"></a>

## Controladores y perfiles MIDI

- Valide el perfil DIN UC-33e/mioXC existente en el hardware Windows y Linux.
- Evalúe la compatibilidad directa con USB UC-33e por separado de la ruta DIN/mioXC documentada.
- Agregue un formato de importación/exportación de perfil de mapeo que el usuario pueda compartir con validación de esquema limitada y sin rutas de medios.
- Evaluar perfiles de controlador adicionales después de que los contratos existentes de mapeo, soft takeover, reconexión y seguridad SysEx sigan cubiertos.
- Evalúe los controles de suavizado y banda muerta por enlace.
- Evalúe la edición segura de UC-33e SysEx sin necesidad de un volcado de banco completo capturado previamente.

<a id="productized-stream-mode"></a>

## Modo de transmisión productizado

- Decida si una fuente de transmisión de usuario normal utiliza la ruta de sesión Rust/FFmpeg, un sidecar incluido, un conector externo o una combinación revisada.
- Mantenga Python/FastAPI como infraestructura de desarrollo/referencia a menos que se convierta en un componente empaquetado explícitamente.
- Diseñe un flujo de trabajo de origen de Stream claro que no complique el panel de origen local predeterminado.
- Restaure las métricas específicas de la transmisión solo cuando ayuden a los usuarios a diagnosticar el comportamiento del búfer, el códec, el ancho de banda o la latencia.
- Conserve la salida nativa, las transiciones preestablecidas y el comportamiento de los mensajes de control limitados en la ruta de la transmisión.
- Agregue pruebas de transmisión de un extremo a otro antes de exponer el modo en la interfaz de usuario normal.

<a id="native-audio-capture"></a>

## Captura de audio nativa

- Evalúe Core Audio Taps en macOS para capturar audio del sistema con una superficie de permiso más estrecha.
- Agregue bucle invertido WASAPI en Windows.
- Agregue proveedores de audio del sistema PipeWire o PulseAudio en Linux.
- Mantenga el procesamiento de audio local y pase cuadros de funciones limitados en lugar de muestras sin procesar ilimitadas a través de Tauri IPC.

<a id="camera-and-native-texture-paths"></a>

## Rutas de cámara y textura nativa

- Evalúe el intercambio de texturas AVFoundation/CVPixelBuffer-to-Metal en macOS.
- Evalúe el intercambio de texturas de copia cero de Media Foundation a D3D más allá de la ruta de fotograma RGB nativa 1.0.3 en Windows.
- Evalúe la interoperabilidad de PipeWire o copia cero de V4L2 a Vulkan/GLES más allá de la ruta 1.0.3 incluida-FFmpeg V4L2 en Linux.
- Agregue una composición nativa multicámara sin forzar cada ruta a través de la lectura del lienzo de WebView.
- Conserve el comportamiento del último fotograma para que la salida en vivo no acumule fotogramas de cámara obsoletos.

<a id="renderer-consistency-and-performance"></a>

## Consistencia y rendimiento del renderizador

- Defina un esquema de parámetros de renderizado compartido por controles de UI, ajustes preestablecidos, audio, WTF, MIDI, renderizadores de navegador, renderizadores de secuencias y salida nativa.
- Reduzca el color duplicado restante y el comportamiento de cuantización en las rutas WebGPU, WebGL2, Canvas, stream y `wgpu` nativas.
- Agregue pruebas visuales limitadas o de salida dorada para ajustes preestablecidos representativos.
- Agregue un indicador de respaldo persistente en el lienzo más allá del diagnóstico actual Stats Overlay y limitado Reports.
- Agregue puntos de referencia repetibles de compilación optimizada para la vista previa principal y Pop Out.
- Agregue pruebas sintéticas de latencia de cámara y respuesta de audio con marca de tiempo.
- Realice un seguimiento de la velocidad de fotogramas, las caídas de fotogramas, los recuentos de carga/salto y la propagación de parámetros con resultados de referencia comparables.
- Repita la carga de trabajo 0.9.11 1080p/audio/salida nativa en el piso de referencia Apple M1/16 GB y una máquina física comparable Windows integrada-GPU; retenga la compilación automatizada de Windows/Linux y el renderizador humea entre comprobaciones físicas.
- Después de que se envíe el primer estilo de atlas Unicode neutral incluido, agregue estilos de atlas opcionales propiedad del proyecto sin cambiar los identificadores de conjunto de glifos, la cobertura de Unicode, la semántica de rampa personalizada ni los enlaces de renderizado. Mantenga los estilos generados en tiempo de compilación, agrupados localmente, cargados de forma diferida y sujetos a presupuestos explícitos de paquete/memoria GPU en lugar de introducir la búsqueda de fuentes del sistema en tiempo de ejecución.
- Evalúe la extensión A de CJK y la compatibilidad con el atlas de plano suplementario solo con un presupuesto explícito de paquete/GPU/caché. El contrato de identificación escalar BMP directo actual debe versionarse en lugar de ampliarse silenciosamente.
- Evalúe los grupos de grafemas, la configuración de guiones, el diseño bidireccional y las secuencias de emoji por separado de las rampas visuales de un solo escalar. Nadie debería entrar en el camino de la telefonía móvil sin un rendimiento medido y un comportamiento creativo claro.

<a id="presets-and-user-profiles"></a>

## Presets y perfiles de usuario

- Agregue cambio de nombre preestablecido por el usuario, comportamiento de inicio opcional seleccionado por el usuario y carpetas/etiquetas.
- Separe los paquetes visuales preestablecidos de los perfiles de mapeo MIDI.
- Mejore la validación de importaciones con errores localizados y legibles.
- Evalúe paquetes de exportación que contengan ajustes preestablecidos visuales, configuraciones reactivas de audio y perfiles de mapeo sin rutas de medios privadas.

<a id="accessibility"></a>

## Accesibilidad

- Complete auditorías de teclado y lector de pantalla de la superficie de control.
- Agregue controles automatizados de teclado, orden de enfoque, ARIA y contraste.
- Evalúe el comportamiento de movimiento reducido para las transiciones de la superficie de control.
- Evalúe una opción de fotosensibilidad que limite el parpadeo o la inquietud extrema en modos aleatorios.
- Evalúe advertencias y exclusiones preestablecidas para resultados WTF intencionalmente intensos.

<a id="internationalization"></a>

## Internacionalización

- Introduzca un catálogo de cadenas empaquetado solo cuando exista un flujo de trabajo de traducción mantenido.
- Mantenga los identificadores estables, los nombres de dispositivos, los nombres de archivos, los bytes MIDI y los nombres escritos por el usuario independientes de las cadenas de visualización localizadas.
- Agregue comprobaciones de clave faltante, clave no utilizada, humo de configuración regional y diseño compacto con la primera configuración regional de la aplicación compatible.
- Localice el texto de permisos, instalador, actualizador, error y accesibilidad como parte de cada configuración regional admitida.
- Mantenga los catálogos de traducción empaquetados localmente sin servicio de traducción en tiempo de ejecución ni dependencia de CDN.

<a id="documentation-and-examples"></a>

## Documentación y ejemplos

- Agregue capturas de pantalla mantenidas para la configuración, los permisos, la superficie de control y Pop Out.
- Agregue guías de configuración de hardware para cámaras, interfaces de audio, proyectores y el equipo UC-33e/mioXC.
- Mantenga una matriz de solución de problemas para permisos, respaldo de GPU, códecs y problemas de ventanas de salida.
- Mantenga el [índice de documentación](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/README.md), las guías de usuario/desarrollador y las guías de práctica alineados con el comportamiento verificado.

<a id="planning-constraints"></a>

## Restricciones de planificación

- La compatibilidad con WebGPU varía según las vistas web y plataformas de Tauri.
- Linux GPU, el comportamiento de la cámara, el audio y el paquete varían según la distribución y la pila de controladores.
- La captura multicámara depende del firmware de la cámara, la topología del USB y el comportamiento del sistema operativo.
- Las concesiones de privacidad macOS siguen siendo sensibles a la identidad y firma del paquete.
- Las licencias y la configuración de FFmpeg siguen siendo puertas de lanzamiento.
- La decodificación de medios nativos y la interoperabilidad de GPU difieren sustancialmente entre plataformas.
- Las asignaciones estructurales de alta velocidad MIDI pueden crear una rotación del renderizador a pesar de los límites de velocidad y fusión.
- El modo Transmisión requiere un flujo de trabajo de usuario completo antes de poder regresar al panel Fuente normal.


<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/ROADMAP.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ROADMAP.md)
