"""Construye webs de prueba con el tema y comprueba el HTML generado."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _build(project: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--clean"],
        cwd=project,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No issues found" in result.stdout + result.stderr


@pytest.fixture(scope="module")
def demo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """La web de demostración del repositorio, construida en una carpeta temporal."""
    project = tmp_path_factory.mktemp("demo")
    shutil.copytree(ROOT / "docs", project / "docs")
    shutil.copy(ROOT / "zensical.toml", project / "zensical.toml")
    _build(project)
    return project / "site"


def _html(site: Path, rel: str) -> str:
    return (site / rel / "index.html").read_text(encoding="utf-8")


def test_carga_hojas_del_tema_antes_que_las_de_la_web(demo: Path) -> None:
    html = _html(demo, "")
    fonts = html.index("assets/stylesheets/fonts.css")
    theme = html.index("assets/stylesheets/techsical.css")
    assert fonts < theme
    assert "fonts.googleapis.com" not in html


def test_assets_del_tema_en_la_web(demo: Path) -> None:
    assert (demo / "assets/stylesheets/techsical.css").is_file()
    assert any((demo / "assets/fonts").glob("source-serif-4-latin-*.woff2"))
    # La carpeta del tema no lleva Python: nada de eso debe acabar publicado.
    assert not list(demo.rglob("*.py"))
    assert not (demo / "__pycache__").exists()


def test_cabecera_enlaza_favicons_manifiesto_y_color(demo: Path) -> None:
    html = _html(demo, "guia/instalacion")
    assert 'href="../../assets/favicon/favicon.ico"' in html
    assert 'href="../../site.webmanifest"' in html
    assert '<meta name="theme-color" content="#164e63">' in html


def test_marca_y_barra_de_navegacion_bajo_la_cabecera(demo: Path) -> None:
    html = _html(demo, "guia/instalacion")
    assert 'class="tx-brand__name">techsical<' in html
    assert "Tema editorial técnico para Zensical" in html
    active = re.search(
        r'tx-subnav__link tx-subnav__link--active"\s+href="([^"]+)"', html
    )
    assert active is not None
    assert active.group(1) == "../"
    # La barra va fuera de la banda de la cabecera, justo después.
    assert html.index("</header>") < html.index('class="tx-subnav"')


def test_portada_con_hero_e_imagenes(demo: Path) -> None:
    html = _html(demo, "")
    assert 'class="tx-hero tx-hero--media"' in html
    assert html.count('class="tx-hero__figure"') == 2
    assert 'class="md-button md-button--primary"' in html


def test_indice_lateral_oculto_por_pagina(demo: Path) -> None:
    hidden = re.compile(r'md-sidebar--secondary"[^>]*data-md-type="toc"\s+hidden')
    assert hidden.search(_html(demo, "guia/paginas"))
    assert not hidden.search(_html(demo, "guia/instalacion"))


def test_entradilla_con_attr_list(demo: Path) -> None:
    assert '<p class="lead">' in _html(demo, "guia/instalacion")


def _site(tmp_path: Path, extra: str, files: dict[str, str] | None = None) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/index.md").write_text("# Hola\n\nTexto.\n", encoding="utf-8")
    for rel, text in (files or {}).items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    (tmp_path / "zensical.toml").write_text(
        '[project]\nsite_name = "Prueba"\n\n[project.theme]\nname = "techsical"\n'
        + extra,
        encoding="utf-8",
    )
    _build(tmp_path)
    return tmp_path / "site"


def test_colores_y_fuentes_de_la_web(tmp_path: Path) -> None:
    site = _site(
        tmp_path,
        '\n[project.extra.techsical]\nprimary = "#7c2d12"\n'
        "font_text = \"'Literata', serif\"\nfavicons = false\nmanifest = false\n",
    )
    html = _html(site, "")
    assert "--tx-brand-primary:#7c2d12;" in html
    assert "--tx-font-text:'Literata', serif;" in html
    assert '<meta name="theme-color" content="#7c2d12">' in html
    assert "favicon.ico" not in html
    assert "site.webmanifest" not in html


def test_main_html_propio_no_pierde_la_cabecera_del_tema(tmp_path: Path) -> None:
    # Una web con su propio main.html (como reCocina) sigue recibiendo el tema.
    main = '{% extends "base.html" %}\n{% block content %}PROPIO{% endblock %}\n'
    site = _site(
        tmp_path,
        'custom_dir = "overrides"\n',
        {"overrides/main.html": main},
    )
    html = _html(site, "")
    assert "PROPIO" in html
    assert "assets/stylesheets/techsical.css" in html
    assert 'class="tx-brand__name">Prueba<' in html


def test_formulas_con_math(demo: Path) -> None:
    html = _html(demo, "formulas")
    assert 'src="../assets/javascripts/math.js"' in html
    assert "mathjax@3" in html
    assert (demo / "assets/javascripts/math.js").is_file()


def test_sin_math_no_carga_mathjax(tmp_path: Path) -> None:
    assert "mathjax" not in _html(_site(tmp_path, ""), "")


def test_opciones_de_maquetacion_por_defecto(demo: Path) -> None:
    html = _html(demo, "guia/instalacion")
    # Sin «anterior / siguiente» al pie; con índice lateral y sin panel.
    assert "options/no-footer-nav.css" in html
    assert "options/no-toc.css" not in html
    assert "options/framed.css" not in html
    # Transiciones entre páginas activas y sin navegación instantánea.
    assert "options/transitions.css" in html
    assert 'src="../../assets/javascripts/transitions.js"' in html
    assert '"navigation.instant"' not in html


def test_opciones_sin_indice_con_panel_y_paso_de_pagina(tmp_path: Path) -> None:
    site = _site(
        tmp_path,
        "\n[project.extra.techsical]\ntoc = false\nframed = true\nfooter_nav = true\n",
    )
    html = _html(site, "")
    assert "options/no-toc.css" in html
    assert "options/framed.css" in html
    assert "options/no-footer-nav.css" not in html
    for name in ("no-toc", "framed", "no-footer-nav", "transitions"):
        assert (site / f"assets/stylesheets/options/{name}.css").is_file()


def test_sin_transiciones(tmp_path: Path) -> None:
    html = _html(
        _site(tmp_path, "\n[project.extra.techsical]\ntransitions = false\n"), ""
    )
    assert "transitions.css" not in html
    assert "transitions.js" not in html


def test_portada_carga_la_primera_imagen_con_prioridad(demo: Path) -> None:
    hero = re.findall(r'tx-hero__figure">\s*<img([^>]*)>', _html(demo, ""))
    assert len(hero) == 2
    assert 'fetchpriority="high"' in hero[0]
    assert 'loading="lazy"' not in hero[0]
    assert 'loading="lazy"' in hero[1]


def test_oscuro_derivado_del_color_de_la_web(tmp_path: Path) -> None:
    html = _html(
        _site(tmp_path, '\n[project.extra.techsical]\nprimary = "#3f5f4a"\n'), ""
    )
    assert "--tx-brand-primary-dark:color-mix(in oklab, #3f5f4a 50%, white);" in html
    assert "--tx-brand-accent-dark" not in html


def test_oscuro_propio_manda_sobre_el_derivado(tmp_path: Path) -> None:
    extra = (
        '\n[project.extra.techsical]\nprimary = "#3f5f4a"\nprimary_dark = "#9ccfa8"\n'
    )
    html = _html(_site(tmp_path, extra), "")
    assert "--tx-brand-primary-dark:#9ccfa8;" in html
    assert "color-mix(in oklab, #3f5f4a" not in html
