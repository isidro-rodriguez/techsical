---
hide:
  - toc
---

# Páginas

La portada, los artículos y cómo se comportan imágenes y tablas. Esta página
oculta el índice lateral: el artículo queda centrado.
{ .lead }

## Portada

`template: home.html` en el front matter de `docs/index.md`. El título, la
entradilla, los botones y hasta dos imágenes van en el front matter; el resto
del Markdown aparece debajo. Ver el ejemplo en el [inicio](../index.md).

## Artículos

- **Entradilla**: el primer párrafo con `{ .lead }` (requiere `attr_list`).
- **Índice lateral**: se oculta por página con `hide: [toc]`.
- **Antetítulo**: las migas de pan (`navigation.path`) hacen de antetítulo.
- **Recuadro de datos**: las notas `abstract`, `example` y `quote` usan el
  color principal suave.

## Imágenes y tablas

Las imágenes solas en su párrafo, o dentro de `<figure>`, se centran y nunca se
amplían; su ancho máximo es `figure_max`. Las tablas ocupan todo el ancho del
artículo y se desplazan en horizontal en pantallas estrechas.
