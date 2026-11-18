# techsical

Tema editorial técnico para [Zensical](https://zensical.org/): texto y títulos en
serif para leer con calma, interfaz, tablas y pies en sans, código en monoespaciada,
y un tema oscuro propio. Cada web personaliza colores y fuentes en su `zensical.toml`.

- Guía y demostración: <https://isidro-rodriguez.github.io/techsical/>
- Cambios: [CHANGELOG.md](https://github.com/isidro-rodriguez/techsical/blob/main/CHANGELOG.md)

## Instalación

```bash
uv add --dev techsical
```

```toml
# zensical.toml
[project.theme]
name = "techsical"

[project.extra.techsical]
primary = "#164e63"   # opcional: color principal
accent = "#0f766e"    # opcional: acento
header_nav = [        # opcional: barra de enlaces bajo la cabecera
    { title = "Guía", url = "guia/" },
]
toc = false           # opcional: sin índice lateral en ninguna página
framed = true         # opcional: el artículo en un panel
footer_nav = true     # opcional: «anterior / siguiente» al pie
transitions = false   # opcional: sin transiciones entre páginas
```

Todas las opciones, la portada (`template: home.html`) y los tipos de página están en
la [guía](https://isidro-rodriguez.github.io/techsical/guia/).

## Desarrollo

```bash
uv sync
uv run ruff format --check . && uv run ruff check . && uv run ty check && uv run pytest
uv run zensical serve                                   # web de demostración
uv run --with playwright python scripts/capturas.py     # capturas en capturas/
```

Las fuentes (Source Serif 4, Manrope y JetBrains Mono) se distribuyen con la
[SIL Open Font License 1.1](https://openfontlicense.org/); el código, con licencia MIT.
