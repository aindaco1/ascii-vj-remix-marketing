---
title: Hoja de ruta
description: Documentación de hoja de ruta derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 2
parent: Referencia
lang: es
---

# Hoja de ruta

Este documento contiene únicamente trabajos prospectivos. No es una descripción del
producto actual y no promete una fecha de lanzamiento o versión. Actual
el comportamiento pertenece a [README](/es/docs/overview/ascii-vj-remix/) y guías de práctica; completado
El historial de trabajos y lanzamientos pertenece a [Changelog](/es/docs/reference/changelog/).

## Distribución y Validación de Plataforma

- Agregue firma Authenticode y marca de tiempo para los instaladores Windows cuando
Se cuenta con un proveedor de firmas sustentable y una política de liberación.
- Validar el comportamiento de Windows SmartScreen en máquinas limpias después de firmar
comienza la distribución.
- Ejecute pruebas de humo de instalación, lanzamiento y actualización en sitios físicos o representativos.
máquinas virtuales Windows y Linux.
- Validar los paquetes Linux AppImage, deb y rpm en una distribución mantenida
matriz.
- Confirme que las concesiones de privacidad de macOS sobrevivan a un actualizador público de identidad estable.
una máquina limpia.
- Decida si las versiones de Windows necesitan un tiempo de ejecución fijo de WebView2 sin conexión
instalación.

## Controladores y perfiles MIDI

- Valide el perfil DIN UC-33e/mioXC existente en el hardware Windows y Linux.
- Evalúe la compatibilidad directa con USB UC-33e por separado del DIN/mioXC documentado
camino.
- Agregue un formato de importación/exportación de perfil de mapeo que el usuario pueda compartir con un esquema delimitado
validación y sin rutas de medios.
- Evaluar perfiles de controlador adicionales después del mapeo existente, software
Los contratos de adquisición, reconexión y seguridad SysEx siguen estando cubiertos.
- Evalúe los controles de suavizado y banda muerta por enlace.
- Evalúe la edición segura de UC-33e SysEx sin necesidad de una captura previa
volcado de banco completo.

## Modo de transmisión productizado

- Decida si una fuente de transmisión de usuario normal utiliza la ruta de sesión Rust/FFmpeg,
un sidecar incluido, un conector externo o una combinación revisada.
- Mantenga Python/FastAPI como infraestructura de desarrollo/referencia a menos que se convierta en
un componente empaquetado explícitamente.
- Diseñe un flujo de trabajo de origen de Stream claro que no complique el valor predeterminado
Panel de fuente local.
- Restaure las métricas específicas de la transmisión solo cuando ayuden a los usuarios a diagnosticar el búfer,
códec, ancho de banda o comportamiento de latencia.
- Preservar la salida nativa, las transiciones preestablecidas y el mensaje de control limitado
Comportamiento en el recorrido del arroyo.
- Agregue pruebas de transmisión de un extremo a otro antes de exponer el modo en la interfaz de usuario normal.

## Captura de audio nativa

- Evalúe Core Audio Taps en macOS para la captura de audio del sistema con un alcance más estrecho
superficie de permiso.
- Agregue bucle invertido WASAPI en Windows.
- Agregue proveedores de audio del sistema PipeWire o PulseAudio en Linux.
- Mantenga el procesamiento de audio local y pase fotogramas de características acotadas en lugar de
muestras sin procesar ilimitadas en Tauri IPC.

## Rutas de cámara y textura nativa

- Evalúe el intercambio de texturas AVFoundation/CVPixelBuffer-to-Metal en macOS.
- Evalúe el intercambio de texturas de Media Foundation a D3D en Windows.
- Evalúe la interoperabilidad PipeWire/V4L2-to-Vulkan o GLES en Linux cuando sea práctico.
- Agregue composición multicámara nativa sin forzar todos los caminos
Lectura del lienzo de WebView.
- Preservar el comportamiento del último fotograma para que la salida en vivo no se quede obsoleta
marcos de cámara.

## Consistencia y rendimiento del renderizador

- Defina un esquema de parámetros de renderizado compartido por controles de UI, ajustes preestablecidos, audio,
WTF, MIDI, renderizadores de navegador, renderizadores de secuencias y salida nativa.
- Reducir el color duplicado restante y el comportamiento de cuantización en WebGPU,
WebGL2, lienzo, secuencia y rutas nativas `wgpu`.
- Agregue pruebas visuales limitadas o de salida dorada para ajustes preestablecidos representativos.
- Haga que las reservas de backend sean visibles y diagnosticables.
- Agregue puntos de referencia repetibles de compilación optimizada para la vista previa principal y Pop Out.
- Agregue pruebas sintéticas de latencia de cámara y respuesta de audio con marca de tiempo.
- Realice un seguimiento de la velocidad de fotogramas, las caídas de fotogramas, los recuentos de carga/salto y la propagación de parámetros
con una producción de referencia comparable.

## Presets y perfiles de usuario

- Agregue cambio de nombre preestablecido por el usuario, selección de inicio, carpetas/etiquetas y búsqueda/filtro.
- Separe los paquetes visuales preestablecidos de los perfiles de mapeo MIDI.
- Mejore la validación de importaciones con errores localizados y legibles.
- Evalúe paquetes de exportación que contengan ajustes preestablecidos visuales, configuraciones reactivas de audio,
y mapeo de perfiles sin rutas de medios privados.

## Accesibilidad

- Complete auditorías de teclado y lector de pantalla de la superficie de control.
- Agregue controles automatizados de teclado, orden de enfoque, ARIA y contraste.
- Evalúe el comportamiento de movimiento reducido para las transiciones de la superficie de control.
- Evalúe una opción de fotosensibilidad que limite el parpadeo o la vibración extrema en
modos aleatorios.
- Evalúe advertencias y exclusiones preestablecidas para resultados WTF intencionalmente intensos.

## Internacionalización

- Introduzca un catálogo de cadenas agrupadas sólo cuando exista un mantenimiento
flujo de trabajo de traducción.
- Mantenga identificadores estables, nombres de dispositivos, nombres de archivos, bytes MIDI y nombres escritos por el usuario.
independiente de las cadenas de visualización localizadas.
- Agregue comprobaciones de clave faltante, clave no utilizada, humo local y diseño compacto con el
primera configuración regional de aplicación compatible.
- Localice el texto de permiso, instalador, actualizador, error y accesibilidad como parte
de cada localidad admitida.
- Mantenga los catálogos de traducción agrupados localmente sin servicio de traducción en tiempo de ejecución
o dependencia de CDN.

## Documentación y ejemplos

- Agregue capturas de pantalla mantenidas para la configuración, los permisos, la superficie de control y
Pop Out.
- Agregue guías de configuración de hardware para cámaras, interfaces de audio, proyectores y el
Equipo UC-33e/mioXC.
- Mantenga una matriz de resolución de problemas para permisos, respaldo de GPU, códecs y
Problemas con la ventana de salida.
- Mantenga README, renderizador, seguridad, rendimiento, pruebas, accesibilidad y
Documentación de internacionalización alineada con comportamientos verificados.

## Restricciones de planificación

- La compatibilidad con WebGPU varía según las vistas web y plataformas de Tauri.
- Linux GPU, el comportamiento de la cámara, el audio y el paquete varía según la distribución y
pila de controladores.
- La captura multicámara depende del firmware de la cámara, la topología USB y el funcionamiento.
comportamiento del sistema.
- Las concesiones de privacidad macOS siguen siendo sensibles a la identidad y firma del paquete.
- Las licencias y la configuración de FFmpeg siguen siendo puertas de lanzamiento.
- La decodificación de medios nativos y la interoperabilidad de GPU difieren sustancialmente entre plataformas.
- Las asignaciones estructurales de MIDI de alta velocidad pueden crear una rotación del renderizador a pesar de
coalescencia y límites de tarifas.
- El modo Stream requiere un flujo de trabajo completo del usuario antes de poder regresar al
panel Fuente normal.

## 1.0 Dirección

- Paquetes documentados e instalables para macOS, Windows y Linux.
- Operación de escritorio sin conexión, excepto para verificaciones y revisiones de actualización deliberadas,
informes de fallos de suscripción.
- Imagen de demostración confiable, video de demostración, archivo personalizado, cámara, preajuste, WTF, audio y
Flujos de trabajo Pop Out desde el primer lanzamiento.
- Comportamiento estable de MIDI en el equipo UC-33e/mioXC documentado.
- El modo de transmisión ya sea producido y probado o ausente de la interfaz de usuario del usuario normal.
- Los artefactos públicos macOS conservan la firma, la certificación notarial, el grapado y la identificación del desarrollador.
Aceptación del gatekeeper e identidad del actualizador.
- Los artefactos Windows utilizan una postura de distribución claramente documentada, con firmas
los instaladores prefieren una vez que la ruta de firma esté operativa.
- Los documentos y notas de la versión actuales coinciden con el producto enviado.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/ROADMAP.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ROADMAP.md)
