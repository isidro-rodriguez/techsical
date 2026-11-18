"""Cálculos sencillos de obra (paquete de ejemplo para la referencia de la API).

No forma parte del tema: sirve para ver cómo pinta techsical las páginas que
mkdocstrings genera a partir de los docstrings.
"""

from obra.hormigon import Amasada, Hormigon, ResistenciaError, volumen_zapata

__all__ = ["Amasada", "Hormigon", "ResistenciaError", "volumen_zapata"]
