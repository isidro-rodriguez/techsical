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
header_nav = [
    { title = "Guía", url = "guia/" },
    { title = "API", url = "api/" },
]
```

| Opción | Por defecto | Notas |
|---|---|---|
| `primary` | `#164E63` | La escala clara y oscura se calcula con `color-mix()` |
| `accent` | `#0F766E` | |
| `font_text` | Source Serif 4 | Las fuentes que no trae el tema las carga la web |
| `font_ui` | Manrope | |
| `font_code` | JetBrains Mono | |
| `content_max` | `720px` | Texto, tablas y código comparten este ancho |
| `figure_max` | `640px` | Las imágenes nunca se amplían por encima de su tamaño |
| `header_nav` | — | Enlaces propios de la cabecera; el menú lateral sigue igual |
| `math` | `false` | Carga MathJax desde unpkg.com; activa `pymdownx.arithmatex` con `generic = true` |

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
