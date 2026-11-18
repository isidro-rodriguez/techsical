# Referencia de la API

El tema da estilo a las páginas que [mkdocstrings](https://mkdocstrings.github.io/)
genera a partir de los docstrings: nombres en monoespaciada, etiquetas pequeñas,
títulos de sección como rótulos y tablas de parámetros con el estilo del tema.
Ver el [ejemplo](../api/obra/hormigon.md).
{ .lead }

## Configuración

```bash
uv add --dev mkdocstrings-python mkdocs-api-autonav
```

```toml
[project.plugins.api-autonav]
modules = ["src/mi_paquete"]
api_root_uri = "api"
nav_section_title = "API"

[project.plugins.mkdocstrings]
locale = "es"
custom_templates = "docs_templates"

[project.plugins.mkdocstrings.handlers.python]
paths = ["src"]

[project.plugins.mkdocstrings.handlers.python.options]
docstring_style = "google"
members_order = "source"
merge_init_into_class = true
separate_signature = true
show_signature_annotations = true
show_source = true
```

## Traducción al español

Los títulos de sección («Parámetros», «Devuelve», «Lanza»…) salen de las
plantillas de mkdocstrings, que solo traen el inglés. La traducción va en
`docs_templates/python/material/languages/es.html.jinja` de la web (este
repositorio la tiene como ejemplo). `custom_templates` debe apuntar a esa
carpeta.

## Qué pinta el tema

| Elemento | Estilo |
|---|---|
| Nombre del objeto | Monoespaciada; cada objeto de primer nivel se separa con una línea |
| Etiquetas (`dataclass`, `property`…) | Rótulo pequeño en mayúsculas con borde |
| Títulos de sección | Rótulo de interfaz (Manrope, mayúsculas) |
| Parámetros, atributos, excepciones | Tablas del tema |
| Miembros de una clase | Sangrados con una línea a la izquierda |
| Símbolos del menú (`mod`, `class`, `func`) | Colores del tema |
