"""Horas trabajadas fuera de la jornada habitual."""

from __future__ import annotations

from datetime import date

from modelo.empleado import Empleado
from modelo.registro_hora import RegistroHora
from modelo.redondeo import redondear


class HoraExtra(RegistroHora):
    """Hereda de RegistroHora y redefine calcular_valor(): aplica el
    factor de recargo configurado sobre el valor hora del empleado.
    """

    def __init__(
        self,
        id_registro: str,
        empleado: Empleado,
        fecha: date,
        cantidad_horas: float,
        motivo: str,
        factor_recargo: float,
    ) -> None:
        super().__init__(id_registro, empleado, fecha, cantidad_horas, motivo)
        self.factor_recargo = factor_recargo

    def calcular_valor(self) -> float:
        return redondear(
            self.empleado.calcular_valor_hora() * self.factor_recargo * self.cantidad_horas
        )

    def obtener_tipo(self) -> str:
        return "Hora extra"

    @property
    def factor_recargo(self) -> float:
        return self._factor_recargo

    @factor_recargo.setter
    def factor_recargo(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El factor de recargo debe ser mayor a cero.")
        self._factor_recargo = float(valor)
