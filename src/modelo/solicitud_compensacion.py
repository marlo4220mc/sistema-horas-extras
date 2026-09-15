"""Solicitud para utilizar horas compensadas."""

from __future__ import annotations

from datetime import date

from modelo.empleado import Empleado
from modelo.solicitud import Solicitud


class SolicitudCompensacion(Solicitud):
    """Hereda de Solicitud y redefine calcular_monto() como el equivalente
    economico de las horas que el empleado deja de trabajar.
    """

    def __init__(
        self,
        id_solicitud: str,
        fecha_solicitud: date,
        empleado: Empleado,
        cantidad_horas: float,
        motivo_uso: str,
    ) -> None:
        super().__init__(id_solicitud, empleado, fecha_solicitud)
        if cantidad_horas <= 0:
            raise ValueError("La cantidad de horas a compensar debe ser mayor a cero.")
        if motivo_uso is None or not motivo_uso.strip():
            raise ValueError("Debe indicar el motivo del uso de horas compensadas.")
        self._cantidad_horas = float(cantidad_horas)
        self._motivo_uso = motivo_uso.strip()

    @property
    def cantidad_horas(self) -> float:
        return self._cantidad_horas

    @property
    def motivo_uso(self) -> str:
        return self._motivo_uso

    def calcular_monto(self) -> float:
        return self.empleado.calcular_valor_hora() * self._cantidad_horas

    def obtener_tipo(self) -> str:
        return "Solicitud compensacion"

    def detalle(self) -> str:
        return f"Horas a compensar: {self._cantidad_horas:.2f} | Motivo: {self._motivo_uso}"
