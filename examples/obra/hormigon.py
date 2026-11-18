"""Hormigón: tipificación, volúmenes y amasadas."""

from dataclasses import dataclass
from enum import Enum

DENSIDAD_HA = 2500.0
"""Densidad del hormigón armado en kg/m³."""


class Exposicion(Enum):
    """Clases de exposición ambiental (simplificadas)."""

    INTERIOR = "XC1"
    EXTERIOR = "XC4"
    MARINA = "XS1"


class ResistenciaError(ValueError):
    """La resistencia característica no es una de las tipificadas."""


@dataclass(frozen=True)
class Hormigon:
    """Hormigón tipificado.

    Attributes:
        resistencia: Resistencia característica f_ck en MPa.
        consistencia: Consistencia (``"B"`` blanda, ``"F"`` fluida).
        exposicion: Clase de exposición.

    Examples:
        >>> Hormigon(30).designacion
        'HA-30/B/20/XC1'
    """

    resistencia: int
    consistencia: str = "B"
    exposicion: Exposicion = Exposicion.INTERIOR

    def __post_init__(self) -> None:
        """Comprueba que la resistencia esté tipificada."""
        if self.resistencia not in (25, 30, 35, 40, 45, 50):
            raise ResistenciaError(f"f_ck = {self.resistencia} MPa no está tipificada.")

    @property
    def designacion(self) -> str:
        """Designación según la instrucción, como ``HA-30/B/20/XC1``."""
        return f"HA-{self.resistencia}/{self.consistencia}/20/{self.exposicion.value}"

    def peso(self, volumen: float) -> float:
        """Peso de un volumen de hormigón armado.

        Args:
            volumen: Volumen en m³; no puede ser negativo.

        Returns:
            Peso en kg.

        Raises:
            ValueError: Si el volumen es negativo.
        """
        if volumen < 0:
            raise ValueError("El volumen no puede ser negativo.")
        return volumen * DENSIDAD_HA


@dataclass
class Amasada:
    """Una amasada de hormigón recibida en obra.

    Attributes:
        hormigon: Hormigón pedido.
        volumen: Volumen en m³.
        albaran: Número del albarán de entrega.
    """

    hormigon: Hormigon
    volumen: float
    albaran: str = ""


def volumen_zapata(
    largo: float, ancho: float, canto: float, *, cantidad: int = 1
) -> float:
    """Volumen de hormigón de una o varias zapatas iguales.

    Args:
        largo: Largo de la zapata en m.
        ancho: Ancho de la zapata en m.
        canto: Canto de la zapata en m.
        cantidad: Número de zapatas iguales.

    Returns:
        Volumen total en m³, redondeado a dos decimales.

    Raises:
        ValueError: Si alguna dimensión no es positiva.

    Examples:
        >>> volumen_zapata(2.0, 2.0, 0.6, cantidad=3)
        7.2
    """
    if min(largo, ancho, canto) <= 0:
        raise ValueError("Las dimensiones deben ser positivas.")
    return round(largo * ancho * canto * cantidad, 2)
