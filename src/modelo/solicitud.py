"""Clase base de las solicitudes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import TYPE_CHECKING

from excepciones import EstadoSolicitudInvalidaError
from modelo.estado_solicitud import EstadoSolicitud

if TYPE_CHECKING:
    from modelo.empleado import Empleado


class Solicitud(ABC):
    """Contiene el manejo comun del estado y deja como abstractos el
    calculo del monto y el tipo (polimorfismo).
    """

    def __init__(self, id_solicitud: str, empleado: "Empleado", fecha_solicitud: date) -> None:
        self.id = id_solicitud
        self.empleado = empleado
        self.fecha_solicitud = fecha_solicitud
        self._estado = EstadoSolicitud.PENDIENTE
        self._observacion = ""
        self._fecha_resolucion: datetime | None = None
        self._resuelto_por = ""

    # ------------------------------------------------------------------
    # Comportamiento comun
    # ------------------------------------------------------------------
    def aprobar(self, usuario: str) -> None:
        """Aprueba la solicitud solo si esta pendiente."""
        self._exigir_estado(EstadoSolicitud.PENDIENTE, "aprobar")
        self._estado = EstadoSolicitud.APROBADA
        self._resuelto_por = usuario
        self._fecha_resolucion = datetime.now()

    def rechazar(self, motivo: str, usuario: str) -> None:
        """Rechaza la solicitud solo si esta pendiente."""
        self._exigir_estado(EstadoSolicitud.PENDIENTE, "rechazar")
        if motivo is None or not motivo.strip():
            raise ValueError("Debe indicar el motivo del rechazo.")
        self._estado = EstadoSolicitud.RECHAZADA
        self._observacion = motivo.strip()
        self._resuelto_por = usuario
        self._fecha_resolucion = datetime.now()

    def _cambiar_estado(
        self, nuevo: EstadoSolicitud, permitido: EstadoSolicitud, accion: str, usuario: str
    ) -> None:
        """Cambia el estado validando que el estado actual sea el permitido."""
        self._exigir_estado(permitido, accion)
        self._estado = nuevo
        self._resuelto_por = usuario
        self._fecha_resolucion = datetime.now()

    def _exigir_estado(self, esperado: EstadoSolicitud, accion: str) -> None:
        if self._estado != esperado:
            raise EstadoSolicitudInvalidaError(
                f"No se puede {accion} la solicitud {self.id} porque su estado "
                f"actual es {self._estado.value} (se esperaba {esperado.value})."
            )

    def resumen(self) -> str:
        return (
            f"{self.id:<8} | {self.obtener_tipo():<24} | "
            f"{self.empleado.codigo_empleado:<6} | {self._estado.value:<10} | "
            f"S/ {self.calcular_monto():9.2f}"
        )

    # ------------------------------------------------------------------
    # Metodos abstractos (polimorfismo)
    # ------------------------------------------------------------------
    @abstractmethod
    def calcular_monto(self) -> float:
        """Monto economico asociado a la solicitud."""

    @abstractmethod
    def obtener_tipo(self) -> str:
        """Nombre del tipo de solicitud."""

    @abstractmethod
    def detalle(self) -> str:
        """Detalle propio de cada subclase."""

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        if valor is None or not str(valor).strip():
            raise ValueError("El id de la solicitud es obligatorio.")
        self._id = str(valor).strip()

    @property
    def empleado(self) -> "Empleado":
        return self._empleado

    @empleado.setter
    def empleado(self, valor: "Empleado") -> None:
        if valor is None:
            raise ValueError("La solicitud debe tener un empleado.")
        self._empleado = valor

    @property
    def fecha_solicitud(self) -> date:
        return self._fecha_solicitud

    @fecha_solicitud.setter
    def fecha_solicitud(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("La fecha de la solicitud es obligatoria.")
        self._fecha_solicitud = valor

    @property
    def estado(self) -> EstadoSolicitud:
        return self._estado

    @property
    def observacion(self) -> str:
        return self._observacion

    @property
    def fecha_resolucion(self) -> datetime | None:
        return self._fecha_resolucion

    @property
    def resuelto_por(self) -> str:
        return self._resuelto_por

    def __str__(self) -> str:
        return self.resumen()
