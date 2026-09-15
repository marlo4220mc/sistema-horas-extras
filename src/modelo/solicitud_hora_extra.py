"""Solicitud de horas extras."""

from __future__ import annotations

from datetime import date

from modelo.estado_solicitud import EstadoSolicitud
from modelo.hora_extra import HoraExtra
from modelo.solicitud import Solicitud


class SolicitudHoraExtra(Solicitud):
    """Hereda de Solicitud, guarda la HoraExtra solicitada y redefine
    calcular_monto() para devolver el pago calculado por la HoraExtra.
    """

    def __init__(self, id_solicitud: str, fecha_solicitud: date, hora_extra: HoraExtra) -> None:
        super().__init__(id_solicitud, hora_extra.empleado, fecha_solicitud)
        if not isinstance(hora_extra, HoraExtra):
            raise ValueError("La solicitud requiere una HoraExtra.")
        self._hora_extra = hora_extra

    @property
    def hora_extra(self) -> HoraExtra:
        return self._hora_extra

    def calcular_monto(self) -> float:
        return self._hora_extra.calcular_valor()

    def obtener_tipo(self) -> str:
        return "Solicitud hora extra"

    def detalle(self) -> str:
        return (
            f"Fecha trabajada: {self._hora_extra.fecha} | "
            f"Horas: {self._hora_extra.cantidad_horas:.2f} | "
            f"Motivo: {self._hora_extra.motivo} | "
            f"Factor: {self._hora_extra.factor_recargo:.2f}"
        )

    def pagar(self, usuario: str) -> None:
        """Marca la solicitud aprobada como pagada."""
        self._cambiar_estado(EstadoSolicitud.PAGADA, EstadoSolicitud.APROBADA, "pagar", usuario)

    def compensar(self, usuario: str) -> None:
        """Marca la solicitud aprobada como compensada con horas compensadas."""
        self._cambiar_estado(
            EstadoSolicitud.COMPENSADA, EstadoSolicitud.APROBADA, "compensar", usuario
        )
