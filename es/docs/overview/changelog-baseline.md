---
title: Base de la versión
description: Documentación básica de lanzamiento derivada del código fuente para desarrolladores que mantienen, amplían, empaquetan o contribuyen a ASCII VJ Remix.
nav_order: 3
parent: Resumen
lang: es
---

<a id="release-baseline"></a>

# Base de la versión

La versión actual es **1.3.1**. El [Registro de cambios](/es/docs/reference/changelog/) contiene el historial completo de versiones.

[Descargar v1.3.1](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.3.1).

Consulte las [Funciones](/es/docs/overview/features/) para conocer los controles actuales y los [registros de publicación del repositorio principal](https://github.com/aindaco1/ascii-vj-remix/blob/ab93bbd6b4d1634d3ee90e05dea743686b83d366/docs/releases/README.md) para la validación y cobertura de plataformas de cada versión.



<a id="131-release-notes"></a>

## Notas de la versión 1.3.1

- Se rechazan las cadenas TLS eMudhra comprometidas con rustls-webpki 0.103.16 y los paquetes de certificados raíz webpki 1.0.10.
- Se añadió una prueba TLS en vivo opcional que comprueba las 12 cadenas de certificados divulgadas y una conexión HTTPS válida como control (`npm run test:tls`).



<a id="source-material"></a>

## Material de origen

Esta página se genera a partir del material fuente de ASCII VJ Remix. Fuentes primarias:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/ab93bbd6b4d1634d3ee90e05dea743686b83d366/CHANGELOG.md)
