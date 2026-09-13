"""Supervisor: empleado con responsabilidad de supervision."""

from __future__ import annotations

from datetime import date

from modelo.empleado import Empleado
from modelo.jornada_laboral import JornadaLaboral


class Supervisor(Empleado):
    """Hereda de Empleado y agrega el area a cargo y el limite de horas
    que puede aprobar en una sola solicitud.
    """

    def __init__(
        self,
        codigo_empleado: str,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        correo: str,
        salario_mensual: float,
        cargo: str,
        fecha_ingreso: date,
        area_a_cargo: str,
        limite_horas_aprobables: float,
        jornada: JornadaLaboral | None = None,
    ) -> None:
        super().__init__(
            codigo_empleado, nombres, apellidos, tipo_documento, numero_documento,
            correo, salario_mensual, cargo, fecha_ingreso, jornada,
        )
        self.area_a_cargo = area_a_cargo
        self.limite_horas_aprobables = limite_horas_aprobables

    def obtener_rol(self) -> str:
        return "Supervisor"

    def puede_aprobar(self, horas: float) -> bool:
        """Indica si el supervisor puede aprobar la cantidad de horas indicada."""
        return 0 < horas <= self.limite_horas_aprobables

    @property
    def area_a_cargo(self) -> str:
        return self._area_a_cargo

    @area_a_cargo.setter
    def area_a_cargo(self, valor: str) -> None:
        self._area_a_cargo = self._validar_texto(valor, "area a cargo")

    @property
    def limite_horas_aprobables(self) -> float:
        return self._limite_horas_aprobables

    @limite_horas_aprobables.setter
    def limite_horas_aprobables(self, valor: float) -> None:
        if valor <= 0 or valor > 24:
            raise ValueError("El limite de horas aprobables debe estar entre 0 y 24.")
        self._limite_horas_aprobables = float(valor)

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | Rol: Supervisor | Area: {self.area_a_cargo} | "
            f"Limite: {self.limite_horas_aprobables:.1f} h"
        )
