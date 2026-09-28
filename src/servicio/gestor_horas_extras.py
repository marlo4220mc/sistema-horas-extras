"""Fachada del sistema: colecciones y funcionalidades de control."""

from __future__ import annotations

from datetime import date

from excepciones import (
    AprobacionNoAutorizadaError,
    EmpleadoDuplicadoError,
    EmpleadoNoEncontradoError,
    HorasInvalidasError,
    SaldoInsuficienteError,
    SolicitudNoEncontradaError,
)
from modelo.empleado import Empleado
from modelo.estado_solicitud import EstadoSolicitud
from modelo.hora_compensada import HoraCompensada
from modelo.hora_extra import HoraExtra
from modelo.jornada_laboral import JornadaLaboral
from modelo.registro_hora import RegistroHora
from modelo.responsable_rrhh import ResponsableRRHH
from modelo.solicitud import Solicitud
from modelo.solicitud_compensacion import SolicitudCompensacion
from modelo.solicitud_hora_extra import SolicitudHoraExtra
from modelo.supervisor import Supervisor
from servicio.calculadora_horas import CalculadoraHoras


class GestorHorasExtras:
    """Guarda las colecciones en memoria y concentra las funcionalidades
    de control: registro, busqueda, listado, aprobacion, calculo y reportes.
    """

    USUARIO_SISTEMA = "usuario.consola"

    def __init__(self, calculadora: CalculadoraHoras | None = None) -> None:
        self._empleados: list[Empleado] = []
        self._registros: list[RegistroHora] = []
        self._solicitudes: list[Solicitud] = []
        self._calculadora = calculadora if calculadora is not None else CalculadoraHoras()
        self._secuencia_registros = 0
        self._secuencia_solicitudes = 0

    # ==================================================================
    # Gestion de empleados
    # ==================================================================
    def registrar_empleado(
        self,
        codigo: str,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        correo: str,
        salario_mensual: float,
        cargo: str,
        fecha_ingreso: date,
    ) -> Empleado:
        """Registra un empleado. Lanza EmpleadoDuplicadoError si repite codigo o documento."""
        self._validar_empleado_no_duplicado(codigo, numero_documento)
        empleado = Empleado(
            codigo, nombres, apellidos, tipo_documento, numero_documento, correo,
            salario_mensual, cargo, fecha_ingreso, JornadaLaboral(),
        )
        self._empleados.append(empleado)
        return empleado

    def registrar_supervisor(
        self,
        codigo: str,
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
    ) -> Supervisor:
        self._validar_empleado_no_duplicado(codigo, numero_documento)
        supervisor = Supervisor(
            codigo, nombres, apellidos, tipo_documento, numero_documento, correo,
            salario_mensual, cargo, fecha_ingreso, area_a_cargo,
            limite_horas_aprobables, JornadaLaboral(),
        )
        self._empleados.append(supervisor)
        return supervisor

    def registrar_responsable_rrhh(
        self,
        codigo: str,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        correo: str,
        salario_mensual: float,
        cargo: str,
        fecha_ingreso: date,
        responsabilidad: str,
    ) -> ResponsableRRHH:
        self._validar_empleado_no_duplicado(codigo, numero_documento)
        responsable = ResponsableRRHH(
            codigo, nombres, apellidos, tipo_documento, numero_documento, correo,
            salario_mensual, cargo, fecha_ingreso, responsabilidad, JornadaLaboral(),
        )
        self._empleados.append(responsable)
        return responsable

    def _validar_empleado_no_duplicado(self, codigo: str, numero_documento: str) -> None:
        """Valida de una sola vez que el codigo y el documento esten libres."""
        if self.existe_empleado_con_codigo(codigo):
            raise EmpleadoDuplicadoError(f"Ya existe un empleado con el codigo {codigo}.")
        if self.existe_empleado_con_documento(numero_documento):
            raise EmpleadoDuplicadoError(
                f"Ya existe un empleado con el documento {numero_documento}."
            )

    def existe_empleado_con_codigo(self, codigo: str) -> bool:
        """Indica si ya hay un empleado registrado con ese codigo.

        Permite avisar del duplicado apenas se ingresa el codigo, sin
        esperar a que el usuario complete el resto de los datos.
        """
        codigo_normalizado = str(codigo).strip().lower()
        return any(
            empleado.codigo_empleado.lower() == codigo_normalizado
            for empleado in self._empleados
        )

    def existe_empleado_con_documento(self, numero_documento: str) -> bool:
        """Indica si ya hay un empleado registrado con ese documento."""
        documento_normalizado = str(numero_documento).strip()
        return any(
            empleado.numero_documento == documento_normalizado
            for empleado in self._empleados
        )

    def buscar_empleado_por_codigo(self, codigo: str) -> Empleado:
        for empleado in self._empleados:
            if empleado.codigo_empleado.lower() == str(codigo).strip().lower():
                return empleado
        raise EmpleadoNoEncontradoError(f"No existe el empleado con codigo {codigo}.")

    def buscar_empleado_por_documento(self, numero_documento: str) -> Empleado:
        for empleado in self._empleados:
            if empleado.numero_documento == str(numero_documento).strip():
                return empleado
        raise EmpleadoNoEncontradoError(
            f"No existe el empleado con documento {numero_documento}."
        )

    def buscar_empleados_por_apellido(self, texto: str) -> list[Empleado]:
        filtro = "" if texto is None else str(texto).strip().lower()
        return [e for e in self._empleados if filtro in e.apellidos.lower()]

    def listar_empleados(self) -> list[Empleado]:
        return list(self._empleados)

    def listar_empleados_por_rol(self, rol: str) -> list[Empleado]:
        """Lista empleados filtrando por el rol que devuelve obtener_rol() (polimorfismo)."""
        return [e for e in self._empleados if e.obtener_rol().lower() == str(rol).strip().lower()]

    # ==================================================================
    # Horas extras y solicitudes
    # ==================================================================
    def registrar_solicitud_hora_extra(
        self, codigo_empleado: str, fecha: date, cantidad_horas: float, motivo: str
    ) -> SolicitudHoraExtra:
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        hora_extra = HoraExtra(
            self._siguiente_id_registro(), empleado, fecha, cantidad_horas, motivo,
            self._calculadora.factor_hora_extra,
        )
        self._registros.append(hora_extra)
        solicitud = SolicitudHoraExtra(self._siguiente_id_solicitud(), date.today(), hora_extra)
        self._solicitudes.append(solicitud)
        return solicitud

    def listar_solicitudes(self) -> list[Solicitud]:
        return list(self._solicitudes)

    def listar_solicitudes_pendientes(self) -> list[Solicitud]:
        return self._filtrar_solicitudes(EstadoSolicitud.PENDIENTE)

    def _filtrar_solicitudes(self, estado: EstadoSolicitud) -> list[Solicitud]:
        return [s for s in self._solicitudes if s.estado == estado]

    def solicitudes_por_empleado(self, codigo_empleado: str) -> list[Solicitud]:
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        return [s for s in self._solicitudes if s.empleado is empleado]

    def buscar_solicitud(self, id_solicitud: str) -> Solicitud:
        for solicitud in self._solicitudes:
            if solicitud.id.lower() == str(id_solicitud).strip().lower():
                return solicitud
        raise SolicitudNoEncontradaError(f"No existe la solicitud {id_solicitud}.")

    def aprobar_solicitud(self, id_solicitud: str, codigo_aprobador: str) -> Solicitud:
        """Aprueba una solicitud. Solo un supervisor registrado puede hacerlo."""
        solicitud = self.buscar_solicitud(id_solicitud)
        self._validar_supervisor(codigo_aprobador)
        solicitud.aprobar(codigo_aprobador)
        return solicitud

    def rechazar_solicitud(self, id_solicitud: str, motivo: str, codigo_aprobador: str) -> Solicitud:
        """Rechaza una solicitud. Solo un supervisor registrado puede hacerlo."""
        solicitud = self.buscar_solicitud(id_solicitud)
        self._validar_supervisor(codigo_aprobador)
        solicitud.rechazar(motivo, codigo_aprobador)
        return solicitud

    def _validar_supervisor(self, codigo_aprobador: str) -> Supervisor:
        """Busca al empleado que intenta aprobar y verifica que sea supervisor.

        Si el empleado no existe lanza EmpleadoNoEncontradoError; si existe
        pero no es supervisor lanza AprobacionNoAutorizadaError.
        """
        empleado = self.buscar_empleado_por_codigo(codigo_aprobador)
        if not isinstance(empleado, Supervisor):
            raise AprobacionNoAutorizadaError(
                f"Solo un supervisor puede aprobar o rechazar solicitudes. "
                f"{empleado.codigo_empleado} ({empleado.obtener_rol()}) no es supervisor."
            )
        return empleado

    def pagar_solicitud(self, id_solicitud: str, usuario: str) -> SolicitudHoraExtra:
        """Paga una solicitud de horas extras ya aprobada."""
        solicitud = self._obtener_solicitud_hora_extra(id_solicitud)
        solicitud.pagar(usuario)
        return solicitud

    def compensar_solicitud_hora_extra(self, id_solicitud: str, usuario: str) -> SolicitudHoraExtra:
        """Convierte una solicitud de horas extras aprobada en horas compensadas:
        cambia el estado a COMPENSADA y suma las horas al saldo del empleado.
        """
        solicitud = self._obtener_solicitud_hora_extra(id_solicitud)
        solicitud.compensar(usuario)
        hora_extra = solicitud.hora_extra
        movimiento = HoraCompensada(
            self._siguiente_id_registro(), hora_extra.empleado, date.today(),
            hora_extra.cantidad_horas,
            f"Compensacion de la solicitud {solicitud.id}", False,
        )
        self._registros.append(movimiento)
        hora_extra.empleado.agregar_horas_compensadas(hora_extra.cantidad_horas)
        return solicitud

    def _obtener_solicitud_hora_extra(self, id_solicitud: str) -> SolicitudHoraExtra:
        solicitud = self.buscar_solicitud(id_solicitud)
        if not isinstance(solicitud, SolicitudHoraExtra):
            raise SolicitudNoEncontradaError(
                f"La solicitud {id_solicitud} no es una solicitud de horas extras."
            )
        return solicitud

    def calcular_pago_solicitud(self, id_solicitud: str) -> float:
        """Pago calculado de la solicitud (usa calcular_monto() de forma polimorfica)."""
        return CalculadoraHoras.redondear(self.buscar_solicitud(id_solicitud).calcular_monto())

    def listar_horas_extras(self) -> list[RegistroHora]:
        return [r for r in self._registros if isinstance(r, HoraExtra)]

    def listar_horas_compensadas(self) -> list[RegistroHora]:
        return [r for r in self._registros if isinstance(r, HoraCompensada)]

    # ==================================================================
    # Horas compensadas
    # ==================================================================
    def registrar_horas_compensadas(
        self, codigo_empleado: str, fecha: date, cantidad_horas: float, motivo: str
    ) -> HoraCompensada:
        """Otorga horas compensadas al empleado (HU09)."""
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        movimiento = HoraCompensada(
            self._siguiente_id_registro(), empleado, fecha, cantidad_horas, motivo, False
        )
        self._registros.append(movimiento)
        empleado.agregar_horas_compensadas(cantidad_horas)
        return movimiento

    def consultar_saldo(self, codigo_empleado: str) -> float:
        return CalculadoraHoras.redondear(
            self.buscar_empleado_por_codigo(codigo_empleado).saldo_horas_compensadas
        )

    def utilizar_horas_compensadas(
        self, codigo_empleado: str, cantidad_horas: float, motivo: str
    ) -> SolicitudCompensacion:
        """Utiliza horas compensadas del saldo (HU11). Valida el saldo antes de
        descontar y deja una solicitud de compensacion aprobada como respaldo.
        """
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        if cantidad_horas <= 0 or cantidad_horas > 24:
            raise HorasInvalidasError(
                "La cantidad de horas debe ser mayor a 0 y como maximo 24."
            )
        if cantidad_horas > empleado.saldo_horas_compensadas:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente para {empleado.nombre_completo}. "
                f"Saldo disponible: {empleado.saldo_horas_compensadas:.2f} h, "
                f"solicitado: {cantidad_horas:.2f} h."
            )
        empleado.consumir_horas_compensadas(cantidad_horas)
        movimiento = HoraCompensada(
            self._siguiente_id_registro(), empleado, date.today(),
            cantidad_horas, motivo, True,
        )
        self._registros.append(movimiento)
        solicitud = SolicitudCompensacion(
            self._siguiente_id_solicitud(), date.today(), empleado, cantidad_horas, motivo
        )
        solicitud.aprobar(self.USUARIO_SISTEMA)
        self._solicitudes.append(solicitud)
        return solicitud

    # ==================================================================
    # Historial y reportes
    # ==================================================================
    def historial_por_empleado(self, codigo_empleado: str) -> list[RegistroHora]:
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        return [r for r in self._registros if r.empleado is empleado]

    def total_horas_extras(self) -> float:
        """Suma las horas de todos los registros de tipo HoraExtra."""
        return CalculadoraHoras.redondear(
            sum(r.cantidad_horas for r in self._registros if isinstance(r, HoraExtra))
        )

    def total_horas_extras_por_empleado(self, codigo_empleado: str) -> float:
        empleado = self.buscar_empleado_por_codigo(codigo_empleado)
        return CalculadoraHoras.redondear(
            sum(
                r.cantidad_horas
                for r in self._registros
                if isinstance(r, HoraExtra) and r.empleado is empleado
            )
        )

    def total_a_pagar(self) -> float:
        """Total a pagar: monto de las solicitudes de horas extras aprobadas."""
        return CalculadoraHoras.redondear(
            sum(
                s.calcular_monto()
                for s in self._solicitudes
                if isinstance(s, SolicitudHoraExtra) and s.estado == EstadoSolicitud.APROBADA
            )
        )

    def total_pagado(self) -> float:
        """Total ya pagado: monto de las solicitudes en estado PAGADA."""
        return CalculadoraHoras.redondear(
            sum(
                s.calcular_monto()
                for s in self._solicitudes
                if isinstance(s, SolicitudHoraExtra) and s.estado == EstadoSolicitud.PAGADA
            )
        )

    def total_horas_compensadas_otorgadas(self) -> float:
        return self._total_horas_compensadas(consumo=False)

    def total_horas_compensadas_utilizadas(self) -> float:
        return self._total_horas_compensadas(consumo=True)

    def _total_horas_compensadas(self, consumo: bool) -> float:
        return CalculadoraHoras.redondear(
            sum(
                r.cantidad_horas
                for r in self._registros
                if isinstance(r, HoraCompensada) and r.es_consumo == consumo
            )
        )

    def reporte_general(self) -> str:
        """Reporte de texto con el resumen general del sistema."""
        lineas = [
            "================ REPORTE GENERAL ================",
            f"Empleados registrados......: {len(self._empleados)}",
            f"Solicitudes registradas....: {len(self._solicitudes)}",
            f"Solicitudes pendientes.....: {len(self.listar_solicitudes_pendientes())}",
            f"Total de horas extras......: {self.total_horas_extras():.2f} h",
            f"Total a pagar (aprobadas)..: S/ {self.total_a_pagar():.2f}",
            f"Total pagado...............: S/ {self.total_pagado():.2f}",
            f"Horas comp. otorgadas......: {self.total_horas_compensadas_otorgadas():.2f} h",
            f"Horas comp. utilizadas.....: {self.total_horas_compensadas_utilizadas():.2f} h",
            "",
            "--- Solicitudes ---",
        ]
        lineas += [s.resumen() for s in self._solicitudes]
        return "\n".join(lineas)

    def reporte_horas_extras_por_empleado(self) -> str:
        """Reporte de horas extras agrupadas por empleado."""
        lineas = ["========= HORAS EXTRAS POR EMPLEADO ========="]
        for empleado in self._empleados:
            registros = [
                r for r in self._registros
                if isinstance(r, HoraExtra) and r.empleado is empleado
            ]
            if registros:
                horas = sum(r.cantidad_horas for r in registros)
                monto = sum(r.calcular_valor() for r in registros)
                lineas.append(
                    f"{empleado.codigo_empleado:<6} {empleado.nombre_completo:<25} "
                    f"{horas:6.2f} h  S/ {CalculadoraHoras.redondear(monto):9.2f}"
                )
        return "\n".join(lineas)

    def reporte_saldos_compensadas(self) -> str:
        """Reporte de saldos de horas compensadas por empleado."""
        lineas = ["===== SALDO DE HORAS COMPENSADAS ====="]
        for empleado in self._empleados:
            lineas.append(
                f"{empleado.codigo_empleado:<6} {empleado.nombre_completo:<25} "
                f"Saldo: {empleado.saldo_horas_compensadas:6.2f} h"
            )
        return "\n".join(lineas)

    # ==================================================================
    # Utilidades internas
    # ==================================================================
    def _siguiente_id_registro(self) -> str:
        self._secuencia_registros += 1
        return f"RH-{self._secuencia_registros:03d}"

    def _siguiente_id_solicitud(self) -> str:
        self._secuencia_solicitudes += 1
        return f"SOL-{self._secuencia_solicitudes:03d}"

    @property
    def calculadora(self) -> CalculadoraHoras:
        return self._calculadora

    def cargar_datos_demo(self) -> None:
        """Carga empleados y movimientos de demostracion para que el sistema
        sea operable desde el primer inicio. Todos los datos son ficticios.
        """
        self.registrar_empleado(
            "E001", "Juan", "Perez", "DNI", "10000001",
            "juan.perez@empresa-demo.com", 3000.00, "Analista de sistemas",
            date(2023, 3, 1),
        )
        self.registrar_empleado(
            "E002", "Maria", "Lopez", "DNI", "10000002",
            "maria.lopez@empresa-demo.com", 2500.00, "Asistente administrativa",
            date(2022, 8, 15),
        )
        self.registrar_empleado(
            "E003", "Carlos", "Ramirez", "DNI", "10000003",
            "carlos.ramirez@empresa-demo.com", 4200.00, "Jefe de operaciones",
            date(2021, 1, 10),
        )
        self.registrar_supervisor(
            "E004", "Ana", "Torres", "DNI", "10000004",
            "ana.torres@empresa-demo.com", 5200.00, "Supervisora de RR. HH.",
            date(2020, 5, 4), "Recursos Humanos", 10,
        )
        self.registrar_responsable_rrhh(
            "E005", "Luis", "Gomez", "DNI", "10000005",
            "luis.gomez@empresa-demo.com", 6000.00, "Responsable de RR. HH.",
            date(2019, 11, 2), "Gestion de personal",
        )

        aprobada = self.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.aprobar_solicitud(aprobada.id, "E004")

        self.registrar_solicitud_hora_extra(
            "E002", date(2026, 9, 18), 4, "Atencion de incidente en el sistema"
        )  # se deja pendiente a proposito

        rechazada = self.registrar_solicitud_hora_extra(
            "E003", date(2026, 9, 20), 3, "Trabajo no autorizado por el jefe directo"
        )
        self.rechazar_solicitud(rechazada.id, "No contaba con autorizacion previa", "E004")

        self.registrar_horas_compensadas(
            "E001", date(2026, 9, 12), 8, "Compensacion por horas extras de la semana"
        )
        self.utilizar_horas_compensadas("E001", 3, "Tramite personal autorizado")
