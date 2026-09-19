"""Paquete de excepciones personalizadas del sistema."""

from excepciones.excepciones import (
    EmpleadoDuplicadoError,
    EmpleadoNoEncontradoError,
    EstadoSolicitudInvalidaError,
    HorasInvalidasError,
    SaldoInsuficienteError,
    SolicitudNoEncontradaError,
)

__all__ = [
    "EmpleadoDuplicadoError",
    "EmpleadoNoEncontradoError",
    "EstadoSolicitudInvalidaError",
    "HorasInvalidasError",
    "SaldoInsuficienteError",
    "SolicitudNoEncontradaError",
]
