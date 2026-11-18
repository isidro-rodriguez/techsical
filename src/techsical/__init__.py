"""Tema editorial técnico para Zensical.

Zensical (como MkDocs) localiza los temas instalables por el grupo de entry
points ``mkdocs.themes`` y toma como carpeta del tema la del ``__file__`` del
objeto registrado. El entry point apunta a :data:`theme`, cuyo ``__file__`` está
dentro de ``theme/``: así la carpeta del tema solo contiene plantillas, hojas de
estilo y fuentes, y ningún archivo de Python acaba copiado en la web.
"""

from importlib.metadata import version
from pathlib import Path
from types import SimpleNamespace

__all__ = ["THEME_DIR", "__version__", "theme"]

__version__ = version("techsical")

THEME_DIR = Path(__file__).resolve().parent / "theme"
"""Carpeta del tema: ``mkdocs_theme.yml``, plantillas y ``assets/``."""

theme = SimpleNamespace(__file__=str(THEME_DIR / "mkdocs_theme.yml"))
"""Objeto que registra el entry point ``mkdocs.themes``."""
