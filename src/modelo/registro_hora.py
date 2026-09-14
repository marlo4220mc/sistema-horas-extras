"""Clase base de todo movimiento de horas (extras o compensadas)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

from excepciones import HorasInvalidasError

if TYPE_CHECKING:  # evita import circular en tiempo de ejecucion
    from modelo.empleado import Empleado


class RegistroHora(ABC):
    """Define el comportamiento comun de un movimiento de horas y deja
    como abstracto el calculo del valor, que cada subclase implementa
    con su propia formula (polimorfismo).
    """

    def __init__(
        self,
        id_registro: str,
        empleado: "Empleado",
        fecha: date,
        cantidad_horas: float,
        motivo: str,
    ) -> None:
        self.id = id_registro
        self.empleado = empleado
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.motivo = motivo

    @abstractmethod
    def calcular_valor(self) -> float:
        """Valor monetario del registro, calculado por cada subclase."""

    @abstractmethod
    def obtener_tipo(self) -> str:
        """Tipo de registro: 'Hora extra' o 'Hora compensada'."""

    def resumen(self) -> str:
        """Texto listo para mostrar en consola."""
        return (
            f"{self.id:<8} | {self.empleado.codigo_empleado:<6} | {self.fecha} | "
            f"{self.cantidad_horas:5.2f} h | {self.obtener_tipo():<16} | "
            f"S/ {self.calcular_valor():8.2f} | {self.motivo}"
        )

    # ------------------------------------------------------------------
    # Propiedades con validacion
    # ------------------------------------------------------------------
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        self._id = self._validar_texto(valor, "id del registro")

    @property
    def empleado(self) -> "Empleado":
        return self._empleado

    @empleado.setter
    def empleado(self, valor: "Empleado") -> None:
        if valor is None:
            raise ValueError("El registro debe estar asociado a un empleado.")
        self._empleado = valor

    @property
    def fecha(self) -> date:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("La fecha del registro es obligatoria.")
        if valor > date.today():
            raise ValueError("La fecha del registro no puede ser futura.")
        self._fecha = valor

    @property
    def cantidad_horas(self) -> float:
        return self._cantidad_horas

    @cantidad_horas.setter
    def cantidad_horas(self, valor: float) -> None:
        if valor <= 0 or valor > 24:
            raise HorasInvalidasError(
                "La cantidad de horas debe ser mayor a 0 y como maximo 24."
            )
        self._cantidad_horas = float(valor)

    @property
    def motivo(self) -> str:
        return self._motivo

    @motivo.setter
    def motivo(self, valor: str) -> None:
        self._motivo = self._validar_texto(valor, "motivo")

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if valor is None or not str(valor).strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")
        return str(valor).strip()

    def __str__(self) -> str:
        return self.resumen()
