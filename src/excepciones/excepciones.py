"""Excepciones personalizadas del sistema.

Todas heredan de Exception y representan errores de negocio controlables
(no errores de programacion). Se sigue la convencion de Python de
terminar el nombre en "Error".
"""


class EmpleadoNoEncontradoError(Exception):
    """Se lanza cuando se busca un empleado que no existe."""


class EmpleadoDuplicadoError(Exception):
    """Se lanza cuando el codigo o el documento ya pertenecen a otro empleado."""


class HorasInvalidasError(Exception):
    """Se lanza cuando la cantidad de horas no es valida (<= 0 o > 24)."""


class SaldoInsuficienteError(Exception):
    """Se lanza cuando se usan mas horas compensadas que el saldo disponible."""


class SolicitudNoEncontradaError(Exception):
    """Se lanza cuando se opera sobre una solicitud que no existe."""


class EstadoSolicitudInvalidaError(Exception):
    """Se lanza cuando el cambio de estado de una solicitud no esta permitido."""
