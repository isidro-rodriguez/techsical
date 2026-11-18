# Instalación

El tema es un paquete de Python. Se instala junto a Zensical y se activa con una
línea en `zensical.toml`.
{ .lead }

## Añadir el paquete

```bash
uv add --dev techsical
```

`techsical` depende de Zensical con un rango de versiones acotado: cada versión
del tema se prueba con las plantillas de una versión concreta de Zensical.

## Activar el tema

```toml
[project.theme]
name = "techsical"
```

El tema ya fija el idioma (`es`), las fuentes propias (sin Google Fonts), las
funciones habituales de navegación y los tres modos de color. Lo que la web
ponga en `[project.theme]` manda sobre esos valores.

## Estructura de la web

El tema enlaza estos archivos si existen en `docs/`:

| Archivo | Uso |
|---|---|
| `assets/favicon/favicon.ico` | Icono de la pestaña (16, 32 y 48 px) |
| `assets/favicon/favicon-16x16.png`, `favicon-32x32.png` | Iconos PNG |
| `assets/favicon/apple-touch-icon.png` | Icono de 180 px para iOS |
| `site.webmanifest` | Manifiesto web, con rutas relativas |

Si la web no los tiene, desactívalos con `favicons = false` y `manifest = false`
en `[project.extra.techsical]`.
