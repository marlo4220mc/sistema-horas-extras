"""Estados por los que pasa una solicitud dentro del sistema."""

from enum import Enum


class EstadoSolicitud(Enum):
    """Estados validos de una solicitud.

    - PENDIENTE: registrada y a la espera de decision.
    - APROBADA: aceptada por el supervisor o por RR. HH.
    - RECHAZADA: no aceptada.
    - PAGADA: horas extras aprobadas que ya fueron pagadas.
    - COMPENSADA: horas extras aprobadas que se cambiaron por horas compensadas.
    """

    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"
    PAGADA = "PAGADA"
    COMPENSADA = "COMPENSADA"

    def __str__(self) -> str:  # para imprimir el nombre y no el objeto
        return self.value
