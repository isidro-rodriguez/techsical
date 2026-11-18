"""Contraste WCAG 2.2 AA de los colores del tema, en claro y en oscuro.

Lee las primitivas de techsical.css y calcula las mezclas ``color-mix(in oklab)``
igual que el navegador, para comprobar cada pareja texto/fondo que el tema usa.
"""

import re
from pathlib import Path

import pytest

CSS = (
    Path(__file__).resolve().parent.parent
    / "src/techsical/theme/assets/stylesheets/techsical.css"
).read_text(encoding="utf-8")
PRIMITIVES = dict(re.findall(r"--(tx-[\w-]+):\s*(#[0-9a-fA-F]{6});", CSS))
TEXT = 4.5  # texto normal
LARGE = 3.0  # texto grande e iconos


def hex_to_rgb(color: str) -> tuple[float, float, float]:
    value = PRIMITIVES.get(color, color).lstrip("#")
    r, g, b = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return r, g, b


def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gamma(c: float) -> float:
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _to_oklab(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_linear(c) for c in rgb)
    lms = (
        0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
        0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
        0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b,
    )
    l_, m_, s_ = (x ** (1 / 3) for x in lms)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _from_oklab(lab: tuple[float, float, float]) -> tuple[float, float, float]:
    lightness, a, b = lab
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    long_, medium, short = l_**3, m_**3, s_**3
    r = 4.0767416621 * long_ - 3.3077115913 * medium + 0.2309699292 * short
    g = -1.2684380046 * long_ + 2.6097574011 * medium - 0.3413193965 * short
    b2 = -0.0041960863 * long_ - 0.7034186147 * medium + 1.7076147010 * short
    return _gamma(r), _gamma(g), _gamma(b2)


def mix(color: str, percent: float, other: str) -> tuple[float, float, float]:
    """``color-mix(in oklab, color percent%, other)``."""
    a, b = _to_oklab(hex_to_rgb(color)), _to_oklab(hex_to_rgb(other))
    t = percent / 100
    return _from_oklab(
        (
            t * a[0] + (1 - t) * b[0],
            t * a[1] + (1 - t) * b[1],
            t * a[2] + (1 - t) * b[2],
        )
    )


def contrast(fg: str | tuple, bg: str | tuple) -> float:
    def luminance(color: str | tuple) -> float:
        rgb = hex_to_rgb(color) if isinstance(color, str) else color
        r, g, b = (_linear(c) for c in rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    high, low = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


WHITE = "#ffffff"
PRIMARY = "tx-petroleum-800"
PRIMARY_DARK = "#66b7cc"
ACCENT = "tx-teal-700"
ACCENT_DARK = "#2cb5a5"
NIGHT = "tx-night-bg"

LIGHT = [
    ("texto", "tx-slate-900", WHITE, TEXT),
    ("texto secundario", "tx-slate-700", WHITE, TEXT),
    ("texto atenuado", "tx-slate-600", WHITE, TEXT),
    ("atenuado sobre superficie", "tx-slate-600", "tx-slate-100", TEXT),
    ("enlace", PRIMARY, WHITE, TEXT),
    ("enlace al pasar", ACCENT, WHITE, TEXT),
    ("cabecera", WHITE, PRIMARY, TEXT),
    ("botón principal", WHITE, PRIMARY, TEXT),
    ("código", "tx-slate-800", "tx-slate-100", TEXT),
    ("nota info", "tx-info-900", "tx-info-100", TEXT),
    ("nota éxito", "tx-success-900", "tx-success-100", TEXT),
    ("nota aviso", "tx-warning-900", "tx-warning-100", TEXT),
    ("nota peligro", "tx-danger-900", "tx-danger-100", TEXT),
    ("icono info", "tx-info-700", "tx-info-100", LARGE),
    ("icono éxito", "tx-success-700", "tx-success-100", LARGE),
    ("icono aviso", "tx-warning-700", "tx-warning-100", LARGE),
    ("icono peligro", "tx-danger-700", "tx-danger-100", LARGE),
    ("foco", ACCENT, WHITE, LARGE),
]

DARK = [
    ("texto", "tx-night-text", NIGHT, TEXT),
    ("texto secundario", "tx-night-text-secondary", NIGHT, TEXT),
    ("texto atenuado", "tx-night-text-muted", NIGHT, TEXT),
    ("atenuado sobre superficie 2", "tx-night-text-muted", "tx-night-surface-2", TEXT),
    ("enlace", PRIMARY_DARK, NIGHT, TEXT),
    ("enlace en superficie 1", PRIMARY_DARK, "tx-night-surface-1", TEXT),
    ("cabecera", "tx-night-text", "tx-night-surface-1", TEXT),
    ("código", "tx-night-text", "tx-night-surface-2", TEXT),
    ("foco", ACCENT_DARK, NIGHT, LARGE),
]


@pytest.mark.parametrize(
    ("name", "fg", "bg", "minimum"), LIGHT, ids=[p[0] for p in LIGHT]
)
def test_contraste_claro(name: str, fg: str, bg: str, minimum: float) -> None:
    assert contrast(fg, bg) >= minimum, f"{name}: {contrast(fg, bg):.2f}"


@pytest.mark.parametrize(
    ("name", "fg", "bg", "minimum"), DARK, ids=[p[0] for p in DARK]
)
def test_contraste_oscuro(name: str, fg: str, bg: str, minimum: float) -> None:
    assert contrast(fg, bg) >= minimum, f"{name}: {contrast(fg, bg):.2f}"


def test_mezclas_del_tema() -> None:
    # Fondos derivados con color-mix(): recuadro de datos, notas y hover de tabla.
    assert contrast("tx-slate-900", mix(PRIMARY, 9, WHITE)) >= TEXT
    assert contrast(PRIMARY, mix(PRIMARY, 9, WHITE)) >= TEXT
    for state in ("info", "success", "warning", "danger"):
        bg = mix(f"tx-{state}-500", 16, NIGHT)
        assert contrast(f"tx-{state}-100", bg) >= TEXT, state
        assert contrast(f"tx-{state}-300", bg) >= LARGE, state
    assert contrast("tx-night-text", mix(PRIMARY_DARK, 18, NIGHT)) >= TEXT
    # Texto atenuado de la cabecera sobre el color principal.
    assert contrast(mix(WHITE, 78, PRIMARY), PRIMARY) >= TEXT


def test_mezcla_sin_cambio_devuelve_el_color() -> None:
    assert contrast(mix(PRIMARY, 100, WHITE), PRIMARY) == pytest.approx(1, abs=1e-3)


# Colores de marca habituales: el claro sobre blanco y el oscuro que el tema
# deriva (50 % con blanco) sobre el fondo y la superficie oscuros.
BRANDS = ["#164e63", "#3f5f4a", "#7c2d12", "#1e3a8a", "#1f3a5f", "#5b21b6", "#0f766e"]


@pytest.mark.parametrize("brand", BRANDS)
def test_marca_personalizada(brand: str) -> None:
    assert contrast(brand, WHITE) >= TEXT
    dark = mix(brand, 50, WHITE)
    assert contrast(dark, NIGHT) >= TEXT
    assert contrast(dark, "tx-night-surface-1") >= TEXT
    assert contrast("tx-night-text", mix(_hex(dark), 18, NIGHT)) >= TEXT


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)
