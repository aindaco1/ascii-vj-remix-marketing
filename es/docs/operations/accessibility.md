---
title: Accesibilidad
description: Documentación de accesibilidad derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 4
parent: Operaciones
lang: es
---

# Accesibilidad

Esta guía establece las mejores prácticas de accesibilidad para ASCII VJ Remix y
rastrea la línea de base actual.

Los controles aún deben ser accesibles, pero la salida del renderizador en sí es
medios creativos que pueden ser intencionalmente de alto contraste, animados, nerviosos y
visualmente intenso.

## Línea de base actual

La accesibilidad es temprana para este proyecto. La aplicación actual se beneficia de:

- colores de interfaz de usuario negro, blanco, gris, rosa neón y azul neón de alto contraste.
- en su mayoría botones HTML estándar, controles deslizantes, controles de selección, casillas de verificación y archivos
flujos del selector.
- grupo de control compacto pero visible.
- Superposición de estadísticas persistente para el estado del renderizador.
- Solicitudes de permisos nativas de la plataforma para la cámara, el micrófono y el audio del sistema.

Limitaciones conocidas:

- No se ha completado ninguna auditoría integral solo del teclado.
- No se ha completado ningún pase de lector de pantalla.
- Aún no existe ningún conjunto de instantáneas automatizadas de axe/ARIA.
- La densa superficie de control de VJ tiene muchos controles deslizantes y botones que necesitan más fuerza.
enfoque y etiquetado de cobertura a lo largo del tiempo.
- La salida visual puede incluir movimiento rápido, alto contraste, fluctuación y color.
cambios por diseño.

## Principios de accesibilidad

- Preservar la densidad de control sin sacrificar la visibilidad del enfoque o la legibilidad
etiquetas.
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
4. Controles deslizantes y numéricos en cuadrícula, color, muestreo, reactividad de audio,
y futuro MIDI.
5. WTF mode estado activo/inactivo.
6. Fuente de reactividad de audio/dispositivo/controles preestablecidos y estados de permiso.
7. Pop Out y controles de pantalla completa/visualización de salida.
8. Contenido de superposición de estadísticas.
9. Recuperación de permisos y mensajes de error.

## Reglas de control de la interfaz de usuario

Utilice estas reglas para el nuevo trabajo de UI:

- Los botones necesitan nombres accesibles que coincidan con su acción.
- Los controles de solo iconos necesitan una etiqueta mediante `aria-label` o texto visible equivalente.
- Los botones de alternancia deben exponer el estado presionado/encendido.
- Los controles deslizantes necesitan etiquetas visibles, etiquetas accesibles, valores mínimo/máximo/actual y
soporte de teclado.
- Las opciones mutuamente excluyentes deben utilizar botones de opción, una selección o un ARIA.
patrón que se prueba con la entrada del teclado.
- Los grupos de casillas de verificación necesitan una etiqueta de grupo.
- Los controles del selector de archivos deben anunciar el nombre del archivo seleccionado/estado de presencia.
- Los menús y controles adicionales deben cerrarse con Escape y restaurar el foco.
- El texto de estado/error debe aparecer cerca del control de activación y utilizar un
estado apropiado o región de alerta cuando sea dinámico.
- Los controles deshabilitados o irrelevantes deben ocultarse o deshabilitarse de manera consistente,
que coincide con el modelo de perilla condicional.

## Expectativas del teclado

Comportamiento mínimo del teclado:

- La pestaña se mueve a través de los controles en un orden útil.
- Shift+Tab invierte el mismo orden.
- Enter/Space activa botones y alterna.
- Las teclas de flecha operan controles deslizantes y selecciones nativas.
- Escape cierra menús transitorios, ventanas emergentes y cuadros de diálogo.
- El foco no queda atrapado en el lienzo de vista previa/salida.
- Abrir y cerrar Pop Out no roba el foco permanentemente del principal
controles.

Para futuros cuadros de diálogo de aprendizaje y mapeo de MIDI:

- las asignaciones deben poder crearse sin entrada de puntero.
- Se deben anunciar los estados en espera de entrada.
- Las acciones de cancelar/borrar/restablecer deben ser accesibles mediante el teclado.

## Movimiento, parpadeo e intensidad visual

ASCII VJ Remix está diseñado para imágenes extremas, pero la interfaz de usuario de control aún debería
respetar las necesidades de accesibilidad.

Regla actual:

- La aplicación puede generar imágenes intensas cuando el usuario selecciona ajustes preestablecidos extremos o
WTF mode, pero los controles deben permanecer legibles y operables.

Futuros candidatos:

- Una preferencia de movimiento reducido para las transiciones de la interfaz de usuario.
- Una opción de seguridad de fotosensibilidad que limita el parpadeo/nerviosismo extremo en
modos aleatorios.
- Advertencias claras para el usuario para conjuntos de rendimiento que utilizan intencionalmente rapidez
destellos o cambios de alto contraste.
- Una forma de excluir ajustes preestablecidos específicos del modo WTF/aleatorio.

## Color y contraste

El tema actual debería mantener:

- Superficies negras/grafito para estructura.
- el blanco como color principal activo/enfoque.
- Azul neón para estados listo/encendido/positivo.
- rosa neón para estados de advertencia/actualización/WTF.
- rojo para errores.

Normas:

- Los estados al pasar el mouse deben mantener el texto legible. Un fondo claro necesita oscuridad
texto.
- Los anillos de enfoque deben ser visibles contra los paneles negros y grises.
- Los estados de error y advertencia necesitan diferencias de texto/icono/estado, no solo color.
- El logotipo/color heredado azul claro no debe usarse como acento principal de la interfaz de usuario.
a menos que el tema cambie intencionalmente.

## Objetivos de cobertura automatizados

Los controles actuales son indirectos:

```bash
npm run build
npm run smoke:static
```

Comprobaciones de accesibilidad a corto plazo para agregar:

- Humo de teclado de dramaturgo para fuente, ajustes preestablecidos, WTF, reactividad de audio y pop
Fuera de los controles.
- Ax busca la ventana de control principal.
- Instantáneas de ARIA para paneles principales.
- Afirmaciones de orden de enfoque para paneles compactos.
- El comportamiento de movimiento reducido se comprueba una vez que existe la preferencia.
- El contraste de color al pasar el cursor/enfoque comprueba el tema negro/neón.

## Lista de verificación de accesibilidad manual

Antes de enviar cambios significativos en la interfaz de usuario:

- Inicie la aplicación y use Tab en la barra lateral completa.
- Las entradas de Confirmar origen se pueden seleccionar sin puntero.
- Confirme que los botones preestablecidos sean accesibles y tengan nombres útiles.
- Confirme que el desbordamiento de Importación/Exportación se abre, cierra y restaura el foco.
- Confirme que todos los controles deslizantes se puedan ajustar desde el teclado.
- Confirme que WTF mode expone el estado activo/inactivo.
- Confirme que los errores de permisos de audio sean legibles y procesables.
- Confirme que los errores de permisos de la cámara sean legibles y procesables.
- Confirme que Pop Out se puede abrir y cerrar sin perder el control de la ventana principal.
- Confirme que el texto flotante permanezca legible en las entradas de Fuente no seleccionadas.
- Confirmar que la superposición de estadísticas no bloquea los controles esenciales.

## Límites aceptados

- La salida de vídeo/ASCII renderizada es un medio artístico y puede no ser adecuada para
cada espectador en cada modo.
- Algunos cuadros de diálogo de permisos de plataforma son propiedad de macOS, Windows, Linux o el
Vista web integrada.
- Los nombres de la cámara y del dispositivo de audio provienen del sistema operativo y es posible que no estén
localizado o compatible con lectores de pantalla.

Estos límites no eximen a los controles de la aplicación de teclado, contraste, etiquetado,
y requisitos de enfoque.


## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [docs/ACCESIBILIDAD.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ACCESSIBILITY.md)
