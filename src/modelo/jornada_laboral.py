"""Jornada laboral de un empleado."""

from __future__ import annotations

from datetime import time


class JornadaLaboral:
    """Define cuantas horas trabaja un empleado y con eso calcula las
    horas mensuales que se usan para obtener el valor de la hora.
    """

    def __init__(
        self,
        horas_diarias: float = 8.0,
        dias_laborables_mes: int = 30,
        hora_inicio: time | None = None,
        hora_fin: time | None = None,
    ) -> None:
        self.horas_diarias = horas_diarias
        self.dias_laborables_mes = dias_laborables_mes
        self.hora_inicio = hora_inicio if hora_inicio is not None else time(8, 0)
        self.hora_fin = hora_fin if hora_fin is not None else time(17, 0)

    @property
    def horas_diarias(self) -> float:
        return self._horas_diarias

    @horas_diarias.setter
    def horas_diarias(self, valor: float) -> None:
        if valor <= 0 or valor > 24:
            raise ValueError("Las horas diarias deben estar entre 0 y 24.")
        self._horas_diarias = float(valor)

    @property
    def dias_laborables_mes(self) -> int:
        return self._dias_laborables_mes

    @dias_laborables_mes.setter
    def dias_laborables_mes(self, valor: int) -> None:
        if valor <= 0 or valor > 31:
            raise ValueError("Los dias laborables del mes deben estar entre 1 y 31.")
        self._dias_laborables_mes = int(valor)

    @property
    def hora_inicio(self) -> time:
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, valor: time) -> None:
        if not isinstance(valor, time):
            raise ValueError("La hora de inicio es obligatoria.")
        self._hora_inicio = valor

    @property
    def hora_fin(self) -> time:
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, valor: time) -> None:
        if not isinstance(valor, time):
            raise ValueError("La hora de fin es obligatoria.")
        self._hora_fin = valor

    def calcular_horas_mensuales(self) -> float:
        """Horas que trabaja el empleado en un mes."""
        return self.horas_diarias * self.dias_laborables_mes

    def __str__(self) -> str:
        return (
            f"{self.horas_diarias:.1f} h/dia, {self.dias_laborables_mes} dias/mes "
            f"({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"
        )
