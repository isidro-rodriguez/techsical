# Personalización

Cada web personaliza el tema en `[project.extra.techsical]` de su
`zensical.toml`. Para lo demás, una hoja propia en `extra_css` puede cambiar
cualquier variable.
{ .lead }

## Opciones

```toml
[project.extra.techsical]
primary = "#164e63"        # color principal (cabecera, enlaces)
accent = "#0f766e"         # acento (foco, enlaces al pasar)
primary_dark = "#66b7cc"   # principal en modo oscuro (opcional)
accent_dark = "#2cb5a5"    # acento en modo oscuro (opcional)
font_text = "'Literata', serif"   # texto y títulos (opcional)
font_ui = "'Inter', sans-serif"   # interfaz, tablas, pies (opcional)
font_code = "'Fira Code', monospace"
content_max = "720px"      # ancho del artículo
figure_max = "640px"       # ancho máximo de las imágenes
theme_color = "#164e63"    # barra del navegador (por defecto, primary)
math = true                # fórmulas LaTeX con MathJax (requiere pymdownx.arithmatex)
toc = false                # sin índice lateral en ninguna página
footer_nav = true          # «anterior / siguiente» al pie (por defecto, no)
framed = true              # el artículo en un panel sobre fondo gris
transitions = false        # sin transiciones entre páginas (por defecto, sí)
header_nav = [
    { title = "Guía", url = "guia/" },
    { title = "API", url = "api/" },
]
```

| Opción | Por defecto | Notas |
|---|---|---|
| `primary` | `#164E63` | Color principal en modo claro: cabecera, enlaces, botones. Los fondos suaves salen de él con `color-mix()` |
| `accent` | `#0F766E` | Acento en modo claro: foco, enlaces al pasar, tareas hechas |
| `primary_dark` | `#66B7CC` | Principal en modo oscuro. Si la web da `primary` y no este, se deriva: `primary` mezclado al 50 % con blanco |
| `accent_dark` | `#2CB5A5` | Acento en modo oscuro; se deriva de `accent` igual que el anterior |
| `font_text` | Source Serif 4 | Las fuentes que no trae el tema las carga la web |
| `font_ui` | Manrope | |
| `font_code` | JetBrains Mono | |
| `content_max` | `720px` | Texto, tablas y código comparten este ancho |
| `figure_max` | `640px` | Las imágenes nunca se amplían por encima de su tamaño |
| `header_nav` | — | Barra de enlaces bajo la cabecera; el menú lateral sigue igual |
| `toc` | `true` | `false` quita el índice lateral de todas las páginas y centra el artículo, como `hide: [toc]` en cada una |
| `footer_nav` | `false` | Muestra «anterior / siguiente» al pie. La portada nunca lo lleva |
| `framed` | `false` | El artículo va en un panel con fondo, borde y relleno propios sobre un fondo de página más oscuro. La portada no |
| `transitions` | `true` | Transiciones suaves entre páginas y la imagen de un enlace que «vuela» a la de la página de destino. Ver [Páginas](paginas.md#transiciones-entre-páginas) |
| `math` | `false` | Carga MathJax desde unpkg.com; activa `pymdownx.arithmatex` con `generic = true` |

!!! warning "Contraste de los colores propios"

    El tema comprueba el contraste de sus colores por defecto y de los oscuros
    que deriva de colores de marca habituales. Un color propio debe comprobarse:
    `primary` necesita un contraste de 4,5:1 sobre blanco para los enlaces y el
    texto de la cabecera, y un `primary_dark` propio, 4,5:1 sobre `#111C24`.

!!! warning "Fuentes propias"

    Si cambias una fuente, la web debe cargarla: con `@font-face` en su hoja de
    estilos (archivos en `docs/assets/fonts/`) o con un servicio externo.

## Variables CSS

La hoja propia de la web se carga después de la del tema, así que puede pisar
cualquier variable:

```css
:root {
  --tx-size-body: 18px;
  --tx-leading-body: 1.7;
}
```
