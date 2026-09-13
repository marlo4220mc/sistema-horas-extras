"""Empleado de la empresa."""

from __future__ import annotations

from datetime import date

from excepciones import HorasInvalidasError, SaldoInsuficienteError
from modelo.jornada_laboral import JornadaLaboral
from modelo.persona import Persona


class Empleado(Persona):
    """Hereda de Persona y agrega los datos laborales (codigo, salario,
    cargo, jornada) y el saldo de horas compensadas.
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
        jornada: JornadaLaboral | None = None,
    ) -> None:
        super().__init__(nombres, apellidos, tipo_documento, numero_documento, correo)
        self.codigo_empleado = codigo_empleado
        self.salario_mensual = salario_mensual
        self.cargo = cargo
        self.fecha_ingreso = fecha_ingreso
        self.jornada = jornada if jornada is not None else JornadaLaboral()
        self._saldo_horas_compensadas = 0.0
        self.activo = True

    # ------------------------------------------------------------------
    # Comportamiento
    # ------------------------------------------------------------------
    def obtener_rol(self) -> str:
        return "Empleado"

    def calcular_valor_hora(self) -> float:
        """Valor de una hora: salario mensual entre horas mensuales."""
        return self.salario_mensual / self.jornada.calcular_horas_mensuales()

    def agregar_horas_compensadas(self, horas: float) -> None:
        """Suma horas al saldo de horas compensadas."""
        self._validar_horas(horas)
        self._saldo_horas_compensadas += horas

    def consumir_horas_compensadas(self, horas: float) -> None:
        """Descuenta horas del saldo de horas compensadas."""
        self._validar_horas(horas)
        if horas > self._saldo_horas_compensadas:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente para {self.nombre_completo}. "
                f"Saldo disponible: {self._saldo_horas_compensadas:.2f} h, "
                f"solicitado: {horas:.2f} h."
            )
        self._saldo_horas_compensadas -= horas

    @staticmethod
    def _validar_horas(horas: float) -> None:
        if horas <= 0 or horas > 24:
            raise HorasInvalidasError(
                "La cantidad de horas debe ser mayor a 0 y como maximo 24."
            )

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def codigo_empleado(self) -> str:
        return self._codigo_empleado

    @codigo_empleado.setter
    def codigo_empleado(self, valor: str) -> None:
        self._codigo_empleado = self._validar_texto(valor, "codigo de empleado").upper()

    @property
    def salario_mensual(self) -> float:
        return self._salario_mensual

    @salario_mensual.setter
    def salario_mensual(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El salario mensual debe ser mayor a cero.")
        self._salario_mensual = float(valor)

    @property
    def cargo(self) -> str:
        return self._cargo

    @cargo.setter
    def cargo(self, valor: str) -> None:
        self._cargo = self._validar_texto(valor, "cargo")

    @property
    def fecha_ingreso(self) -> date:
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("La fecha de ingreso es obligatoria.")
        if valor > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura.")
        self._fecha_ingreso = valor

    @property
    def jornada(self) -> JornadaLaboral:
        return self._jornada

    @jornada.setter
    def jornada(self, valor: JornadaLaboral) -> None:
        if not isinstance(valor, JornadaLaboral):
            raise ValueError("La jornada laboral es obligatoria.")
        self._jornada = valor

    @property
    def saldo_horas_compensadas(self) -> float:
        return self._saldo_horas_compensadas

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        self._activo = bool(valor)

    def __str__(self) -> str:
        return (
            f"{self.codigo_empleado} | {self.nombre_completo} | "
            f"{self.tipo_documento} {self.numero_documento} | {self.cargo} | "
            f"Salario: {self.salario_mensual:.2f} | "
            f"Valor hora: {self.calcular_valor_hora():.2f} | "
            f"Saldo: {self._saldo_horas_compensadas:.2f} h"
        )
