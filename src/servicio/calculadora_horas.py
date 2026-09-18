"""Calculos de negocio y reglas configurables del sistema."""

from __future__ import annotations

from modelo.empleado import Empleado
from modelo.redondeo import redondear


class CalculadoraHoras:
    """Concentra los calculos y las reglas configurables (factores).

    Reglas del proyecto academico::

        valor_hora        = salario_mensual / horas_mensuales
        valor_hora_extra  = valor_hora * factor_hora_extra
        pago_horas_extras = valor_hora_extra * cantidad_horas

    El factor 1.5 NO proviene de una norma legal: es una regla configurada
    para este trabajo y puede cambiarse con ``factor_hora_extra``.
    """

    FACTOR_HORA_EXTRA_DEFECTO = 1.5
    FACTOR_HORA_COMPENSADA_DEFECTO = 1.0

    def __init__(
        self,
        factor_hora_extra: float = FACTOR_HORA_EXTRA_DEFECTO,
        factor_hora_compensada: float = FACTOR_HORA_COMPENSADA_DEFECTO,
    ) -> None:
        self.factor_hora_extra = factor_hora_extra
        self.factor_hora_compensada = factor_hora_compensada

    def valor_hora(self, empleado: Empleado) -> float:
        """Valor de una hora ordinaria del empleado."""
        return redondear(empleado.calcular_valor_hora())

    def pago_horas_extras(self, empleado: Empleado, cantidad_horas: float) -> float:
        """Pago de una cantidad de horas extras."""
        return redondear(
            empleado.calcular_valor_hora() * self.factor_hora_extra * cantidad_horas
        )

    def valor_horas_compensadas(self, empleado: Empleado, cantidad_horas: float) -> float:
        """Equivalente economico de una cantidad de horas compensadas."""
        return redondear(
            empleado.calcular_valor_hora() * self.factor_hora_compensada * cantidad_horas
        )

    @staticmethod
    def redondear(valor: float) -> float:
        """Redondea a dos decimales."""
        return redondear(valor)

    @property
    def factor_hora_extra(self) -> float:
        return self._factor_hora_extra

    @factor_hora_extra.setter
    def factor_hora_extra(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El factor de hora extra debe ser mayor a cero.")
        self._factor_hora_extra = float(valor)

    @property
    def factor_hora_compensada(self) -> float:
        return self._factor_hora_compensada

    @factor_hora_compensada.setter
    def factor_hora_compensada(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El factor de hora compensada debe ser mayor a cero.")
        self._factor_hora_compensada = float(valor)
