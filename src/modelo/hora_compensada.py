"""Movimiento de horas compensadas."""

from __future__ import annotations

from datetime import date

from modelo.empleado import Empleado
from modelo.registro_hora import RegistroHora
from modelo.redondeo import redondear


class HoraCompensada(RegistroHora):
    """Hereda de RegistroHora y redefine calcular_valor() como el valor
    hora simple (sin recargo), porque la hora compensada no se paga: se
    cambia por tiempo libre.

    Si ``es_consumo`` es True, el registro representa horas que el
    empleado utilizo; si es False, horas que la empresa le otorgo.
    """

    def __init__(
        self,
        id_registro: str,
        empleado: Empleado,
        fecha: date,
        cantidad_horas: float,
        motivo: str,
        es_consumo: bool = False,
    ) -> None:
        super().__init__(id_registro, empleado, fecha, cantidad_horas, motivo)
        self.es_consumo = es_consumo

    def calcular_valor(self) -> float:
        return redondear(self.empleado.calcular_valor_hora() * self.cantidad_horas)

    def obtener_tipo(self) -> str:
        return "Hora comp. usada" if self.es_consumo else "Hora comp. otorg."

    @property
    def es_consumo(self) -> bool:
        return self._es_consumo

    @es_consumo.setter
    def es_consumo(self, valor: bool) -> None:
        self._es_consumo = bool(valor)
