"""Paquete de excepciones personalizadas del sistema."""

from excepciones.excepciones import (
    AprobacionNoAutorizadaError,
    EmpleadoDuplicadoError,
    EmpleadoNoEncontradoError,
    EstadoSolicitudInvalidaError,
    HorasInvalidasError,
    SaldoInsuficienteError,
    SolicitudNoEncontradaError,
)

__all__ = [
    "AprobacionNoAutorizadaError",
    "EmpleadoDuplicadoError",
    "EmpleadoNoEncontradoError",
    "EstadoSolicitudInvalidaError",
    "HorasInvalidasError",
    "SaldoInsuficienteError",
    "SolicitudNoEncontradaError",
]
