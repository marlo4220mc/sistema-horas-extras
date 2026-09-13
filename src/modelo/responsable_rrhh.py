"""Responsable del area de Recursos Humanos."""

from __future__ import annotations

from datetime import date

from modelo.empleado import Empleado
from modelo.jornada_laboral import JornadaLaboral


class ResponsableRRHH(Empleado):
    """Hereda de Empleado y agrega la responsabilidad principal asignada."""

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
        responsabilidad_principal: str,
        jornada: JornadaLaboral | None = None,
    ) -> None:
        super().__init__(
            codigo_empleado, nombres, apellidos, tipo_documento, numero_documento,
            correo, salario_mensual, cargo, fecha_ingreso, jornada,
        )
        self.responsabilidad_principal = responsabilidad_principal

    def obtener_rol(self) -> str:
        return "Responsable de RR.HH."

    @property
    def responsabilidad_principal(self) -> str:
        return self._responsabilidad_principal

    @responsabilidad_principal.setter
    def responsabilidad_principal(self, valor: str) -> None:
        self._responsabilidad_principal = self._validar_texto(
            valor, "responsabilidad principal"
        )

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | Rol: Responsable de RR.HH. | "
            f"Responsabilidad: {self.responsabilidad_principal}"
        )
