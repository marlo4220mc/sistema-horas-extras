"""Utilidad de redondeo monetario del sistema."""

from decimal import Decimal, ROUND_HALF_UP

_DOS_DECIMALES = Decimal("0.01")


def redondear(valor: float) -> float:
    """Redondea un monto a dos decimales usando redondeo comercial (HALF_UP)."""
    return float(Decimal(str(valor)).quantize(_DOS_DECIMALES, rounding=ROUND_HALF_UP))
