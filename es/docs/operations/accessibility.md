---
title: Accesibilidad
description: Documentación de accesibilidad derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Operaciones
lang: es
---

# Accesibilidad

Esta guía documenta la línea base de accesibilidad actual y las reglas aplicadas a los cambios en la superficie de control.

La interfaz de usuario de control sigue sujeta a los requisitos de teclado, etiquetado, contraste y enfoque. El resultado renderizado son medios creativos que pueden ser intencionalmente de alto contraste, animados, nerviosos y visualmente intensos.

## Línea de base actual

La accesibilidad es temprana para este proyecto. La aplicación actual se beneficia de:

- colores de interfaz de usuario negro, blanco, gris, rosa neón y azul neón de alto contraste.
- en su mayoría botones HTML estándar, controles deslizantes, controles de selección, casillas de verificación y flujos de selección de archivos.
- grupo de control compacto pero visible.
- Superposición de estadísticas persistente para el estado del renderizador.
- estado en vivo cortés para verificaciones de actualización activadas por el usuario y versiones disponibles; Las comprobaciones de inicio silenciosas no anuncian resultados actuales/fuera de línea.
- un control persistente Reports que mantiene accesibles las preferencias de informes de fallas antes de que cualquier informe esté pendiente.
- Solicitudes de permisos nativas de la plataforma para la cámara, el micrófono y el audio del sistema.

Limitaciones conocidas:

- No se ha completado ninguna auditoría integral solo del teclado.
- No se ha completado ningún pase de lector de pantalla.
- No existe ningún conjunto de instantáneas automatizadas de Axe/ARIA.
- La densa superficie de control de VJ tiene muchos controles deslizantes y botones que necesitan un mayor enfoque y cobertura de etiquetado con el tiempo.
- La salida visual puede incluir movimientos rápidos, alto contraste, fluctuaciones y cambios de color por diseño.

## Principios de accesibilidad

- Conserve la densidad del control sin sacrificar la visibilidad del enfoque ni las etiquetas legibles.
- Prefiere controles nativos antes que widgets personalizados.
- Haga que todos los teclados de control interactivos sean accesibles.
- Mantenga el orden de enfoque alineado con el orden visual.
- No confíe únicamente en el color para determinar el estado crítico.
- Mantenga fuertes los estados de enfoque visibles frente al tema negro de la interfaz de usuario.
- Utilice ARIA sólo cuando la semántica nativa sea insuficiente.
- Mantenga educadas las actualizaciones de estado en vivo a menos que el usuario deba actuar de inmediato.
- No permita que los cambios estéticos reduzcan el contraste o el tamaño objetivo.
- Mantenga los controles de la ventana de salida mínimos y predecibles.

## Superficies de interacción críticas

Las superficies de accesibilidad de mayor riesgo son:

1. Selección de fuente, selección de archivo personalizado y estado de fuente.
2. Lista de dispositivos de cámara y selección multicámara.
3. Botones preestablecidos, acciones preestablecidas por el usuario y menú adicional de importación/exportación.
4. Controles deslizantes y numéricos en Cuadrícula, Color, Muestreo, Reactividad de audio y MIDI.
5. WTF mode estado activo/inactivo.
6. Fuente de reactividad de audio/dispositivo/controles preestablecidos y estados de permiso.
7. Pop Out y controles de pantalla completa/visualización de salida.
8. Contenido de superposición de estadísticas.
9. Recuperación de permisos y mensajes de error.
10. Estado del dispositivo MIDI, estado de toma de control suave, acciones SysEx y aprendizaje MIDI.
11. Preferencia de diálogo de informes, recuento pendiente, acciones de envío y descarte.
12. Controles de paleta, mapeo, tramado ordenado, modo de densidad, conjunto de caracteres, rampa escrita y color de glifo.

## Reglas de control de la interfaz de usuario

Utilice estas reglas para el nuevo trabajo de UI:

- Los botones necesitan nombres accesibles que coincidan con su acción.
- Los controles de solo iconos necesitan una etiqueta mediante `aria-label` o texto visible equivalente.
- Los botones de alternancia deben exponer el estado presionado/encendido.
- Los controles deslizantes necesitan etiquetas visibles, etiquetas accesibles, valores mínimos/máximos/actuales y soporte para teclado.
- Las opciones de paleta y conjunto de caracteres necesitan etiquetas de texto legibles; las muestras o las formas de glifos renderizados no pueden ser el único identificador.
- La longitud de la rampa personalizada y los comentarios escalares eliminados/no admitidos deben estar disponibles como texto, no transmitidos únicamente mediante una vista previa modificada.
- Advanced Density debe identificar que elimina la garantía de rendimiento normal y debe permanecer operativo independientemente de los ajustes preestablecidos visuales.
- Las opciones mutuamente excluyentes utilizan botones de opción, una selección o un patrón ARIA que se prueba con la entrada del teclado.
- Los grupos de casillas de verificación necesitan una etiqueta de grupo.
- Los controles del selector de archivos anuncian el nombre del archivo seleccionado/estado de presencia.
- Los menús y controles adicionales deben cerrarse con Escape y restaurar el foco.
- El texto de estado/error aparece cerca del control de activación y utiliza un estado apropiado o una región de alerta cuando es dinámico.
- Los diálogos se cierran con Escape y restablecen el foco en su control de activación.
- Los controles deshabilitados o irrelevantes se ocultan o deshabilitan constantemente, coincidiendo con el modelo de perilla condicional.

## Expectativas del teclado

Comportamiento mínimo del teclado:

- La pestaña se mueve a través de los controles en un orden útil.
- Shift+Tab invierte el mismo orden.
- Enter/Space activa botones y alterna.
- Las teclas de flecha operan controles deslizantes y selecciones nativas.
- Escape cierra menús transitorios, ventanas emergentes y cuadros de diálogo.
- El foco no queda atrapado en el lienzo de vista previa/salida.
- Abrir y cerrar Pop Out no roba el foco permanentemente de los controles principales.

Para controles de aprendizaje y mapeo MIDI:

- las asignaciones deben poder crearse sin entrada de puntero.
- Se deben anunciar los estados en espera de entrada.
- Las acciones de cancelar/borrar/restablecer deben ser accesibles mediante el teclado.
- Los estados de conexión, página activa, último mensaje, captura, restauración y verificación deben exponerse a través de un texto de estado en vivo legible.
- La instalación/restauración debe identificar que se sobrescriben las 33 memorias del UC-33e.
- No se debe requerir el uso del controlador físico para desconectar MIDI, cancelar el aprendizaje, eliminar una anulación o restablecer el mapa integrado.

## Movimiento, parpadeo e intensidad visual

ASCII VJ Remix está diseñado para imágenes extremas, mientras que la interfaz de usuario de control sigue siendo legible y operable.

Regla actual:

- La aplicación puede generar imágenes intensas cuando el usuario selecciona ajustes preestablecidos extremos o WTF mode, pero los controles deben permanecer legibles y operables.

## Color y contraste

El tema actual utiliza:

- Superficies negras/grafito para estructura.
- el blanco como color principal activo/enfoque.
- Azul neón para estados listo/encendido/positivo.
- rosa neón para estados de advertencia/actualización/WTF.
- rojo para errores.

Normas:

- Los estados al pasar el mouse deben mantener el texto legible. Un fondo claro necesita texto oscuro.
- Los anillos de enfoque deben ser visibles contra los paneles negros y grises.
- Los estados de error y advertencia necesitan diferencias de texto/icono/estado, no solo color.
- El logotipo/color heredado azul claro no es el acento principal de la interfaz de usuario.

## Cobertura automatizada actual

Los controles actuales son indirectos:

```bash
npm run build
npm run smoke:static
```

No hay un teclado dedicado, un hacha, una instantánea ARIA, un orden de enfoque, un movimiento reducido o un conjunto de contraste automatizado. Esas lagunas también se resumen en [Testing](/es/docs/operations/testing/); El trabajo prospectivo de accesibilidad vive en el [Roadmap](/es/docs/reference/roadmap/).

## Lista de verificación de accesibilidad manual

Antes de enviar cambios significativos en la interfaz de usuario:

- Inicie la aplicación y use Tab en la barra lateral completa.
- Las entradas de Confirmar fuente se pueden seleccionar sin un puntero.
- Confirme que los botones preestablecidos sean accesibles y tengan nombres útiles.
- Confirme que el desbordamiento de Importación/Exportación se abre, cierra y restaura el foco.
- Confirme que todos los controles deslizantes se puedan ajustar desde el teclado.
- Confirme que la paleta, la asignación, el tramado ordenado, el conjunto de caracteres y la rampa personalizada sean accesibles mediante el teclado y sus valores actuales se anuncien como texto.
- Confirme que el contador de rampa personalizada informe el límite de 96 escalares y las eliminaciones no admitidas sin depender del color.
- Confirme que WTF mode expone el estado activo/inactivo.
- Confirme que los errores de permisos de audio sean legibles y procesables.
- Confirme que los errores de permisos de la cámara sean legibles y procesables.
- Confirme que Pop Out se puede abrir y cerrar sin perder el control de la ventana principal.
- Confirme que el texto flotante permanezca legible en las entradas de Fuente no seleccionadas.
- Confirmar que la superposición de estadísticas no bloquea los controles esenciales.
- Confirme que se puede acceder al panel MIDI mediante el teclado en la aplicación de escritorio, Learn expone el estado presionado y que el cambio de opciones de dispositivo/perfil no atrapa el foco.

## Límites aceptados

- La salida de vídeo/ASCII renderizada es un medio artístico y puede no ser adecuada para todos los espectadores en todos los modos.
- Algunos cuadros de diálogo de permisos de plataforma son propiedad de macOS, Windows, Linux o la vista web integrada.
- Los nombres de las cámaras y los dispositivos de audio provienen del sistema operativo y es posible que no estén localizados o no sean fáciles de leer para los lectores de pantalla.

Estos límites no eximen a los controles de la aplicación de los requisitos de teclado, contraste, etiquetado y enfoque.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/ACCESSIBILITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ACCESSIBILITY.md)
