"""Pruebas de los metodos de negocio del sistema (unittest)."""

from __future__ import annotations

import os
import sys
import unittest
from datetime import date, timedelta

# Permite importar el paquete src/ al ejecutar las pruebas.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from excepciones import (  # noqa: E402
    AprobacionNoAutorizadaError,
    EmpleadoDuplicadoError,
    EmpleadoNoEncontradoError,
    EstadoSolicitudInvalidaError,
    HorasInvalidasError,
    SaldoInsuficienteError,
    SolicitudNoEncontradaError,
)
from modelo.estado_solicitud import EstadoSolicitud  # noqa: E402
from modelo.hora_compensada import HoraCompensada  # noqa: E402
from modelo.hora_extra import HoraExtra  # noqa: E402
from modelo.registro_hora import RegistroHora  # noqa: E402
from modelo.solicitud import Solicitud  # noqa: E402
from servicio.calculadora_horas import CalculadoraHoras  # noqa: E402
from servicio.gestor_horas_extras import GestorHorasExtras  # noqa: E402


class PruebasSistema(unittest.TestCase):
    """Agrupa las 23 pruebas del sistema."""

    def setUp(self) -> None:
        self.gestor = GestorHorasExtras()
        self.gestor.registrar_empleado(
            "E001", "Juan", "Perez", "DNI", "10000001",
            "juan.perez@empresa-demo.com", 3000.00, "Analista de sistemas",
            date(2023, 3, 1),
        )
        self.gestor.registrar_empleado(
            "E002", "Maria", "Lopez", "DNI", "10000002",
            "maria.lopez@empresa-demo.com", 2400.00, "Asistente administrativa",
            date(2022, 8, 15),
        )
        self.gestor.registrar_supervisor(
            "E009", "Ana", "Torres", "DNI", "10000009",
            "ana.torres@empresa-demo.com", 5200.00, "Supervisora de RR. HH.",
            date(2020, 5, 4), "Recursos Humanos", 10,
        )

    # ------------------------------------------------------------------
    # HU01 - Registrar empleado
    # ------------------------------------------------------------------
    def test_hu01_registrar_empleado_correctamente(self) -> None:
        empleado = self.gestor.buscar_empleado_por_codigo("E001")
        self.assertEqual("Perez", empleado.apellidos)
        self.assertEqual("Empleado", empleado.obtener_rol())
        self.assertEqual(3, len(self.gestor.listar_empleados()))
        self.assertAlmostEqual(0.0, empleado.saldo_horas_compensadas, places=3)

    def test_validacion_empleado_duplicado(self) -> None:
        # La disponibilidad se puede consultar apenas se ingresa el codigo.
        self.assertTrue(self.gestor.existe_empleado_con_codigo("E001"))
        self.assertTrue(self.gestor.existe_empleado_con_codigo("e001"))
        self.assertFalse(self.gestor.existe_empleado_con_codigo("E999"))
        self.assertTrue(self.gestor.existe_empleado_con_documento("10000001"))
        self.assertFalse(self.gestor.existe_empleado_con_documento("99999999"))
        with self.assertRaises(EmpleadoDuplicadoError):
            self.gestor.registrar_empleado(
                "E001", "Otro", "Empleado", "DNI", "99999999",
                "otro@empresa-demo.com", 2000.00, "Practicante", date(2024, 1, 5),
            )
        with self.assertRaises(EmpleadoDuplicadoError):
            self.gestor.registrar_empleado(
                "E030", "Otro", "Empleado", "DNI", "10000001",
                "otro@empresa-demo.com", 2000.00, "Practicante", date(2024, 1, 5),
            )

    # ------------------------------------------------------------------
    # HU02 - Buscar empleado
    # ------------------------------------------------------------------
    def test_hu02_buscar_empleado_por_codigo(self) -> None:
        empleado = self.gestor.buscar_empleado_por_codigo("e002")
        self.assertEqual("Maria Lopez", empleado.nombre_completo)

    def test_hu02_buscar_empleado_inexistente(self) -> None:
        with self.assertRaises(EmpleadoNoEncontradoError):
            self.gestor.buscar_empleado_por_codigo("E999")

    # ------------------------------------------------------------------
    # HU04 - Registrar horas extras
    # ------------------------------------------------------------------
    def test_hu04_registrar_horas_extras(self) -> None:
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.assertEqual(EstadoSolicitud.PENDIENTE, solicitud.estado)
        self.assertAlmostEqual(6, solicitud.hora_extra.cantidad_horas, places=3)

    def test_validacion_horas_invalidas(self) -> None:
        with self.assertRaises(HorasInvalidasError):
            self.gestor.registrar_solicitud_hora_extra(
                "E001", date(2026, 9, 10), 0, "Sin horas"
            )
        with self.assertRaises(HorasInvalidasError):
            self.gestor.registrar_solicitud_hora_extra(
                "E001", date(2026, 9, 10), -3, "Horas negativas"
            )

    def test_validacion_fecha_futura(self) -> None:
        manana = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError):
            self.gestor.registrar_solicitud_hora_extra("E001", manana, 4, "Trabajo futuro")
        with self.assertRaises(ValueError):
            self.gestor.registrar_horas_compensadas("E001", manana, 4, "Compensacion futura")
        # Una fecha de hoy si es valida.
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date.today(), 4, "Trabajo de hoy"
        )
        self.assertEqual(EstadoSolicitud.PENDIENTE, solicitud.estado)

    # ------------------------------------------------------------------
    # HU08 - Calculos
    # ------------------------------------------------------------------
    def test_hu08_calcular_valor_hora(self) -> None:
        # 3000 / (8 h * 30 dias) = 3000 / 240 = 12.5
        empleado = self.gestor.buscar_empleado_por_codigo("E001")
        self.assertAlmostEqual(12.5, self.gestor.calculadora.valor_hora(empleado), places=3)

    def test_hu08_calcular_pago_horas_extras(self) -> None:
        # valor hora 12.5 * factor 1.5 = 18.75 por hora; por 6 horas = 112.5
        empleado = self.gestor.buscar_empleado_por_codigo("E001")
        self.assertAlmostEqual(
            112.5, self.gestor.calculadora.pago_horas_extras(empleado, 6), places=3
        )
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.assertAlmostEqual(112.5, self.gestor.calcular_pago_solicitud(solicitud.id), places=3)

    # ------------------------------------------------------------------
    # HU06 / HU07 - Aprobar y rechazar
    # ------------------------------------------------------------------
    def test_hu06_aprobar_solicitud(self) -> None:
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.gestor.aprobar_solicitud(solicitud.id, "E009")
        self.assertEqual(EstadoSolicitud.APROBADA, solicitud.estado)
        self.assertEqual("E009", solicitud.resuelto_por)
        self.assertAlmostEqual(112.5, self.gestor.total_a_pagar(), places=3)

    def test_validacion_aprobar_dos_veces(self) -> None:
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.gestor.aprobar_solicitud(solicitud.id, "E009")
        with self.assertRaises(EstadoSolicitudInvalidaError):
            self.gestor.aprobar_solicitud(solicitud.id, "E009")

    def test_hu07_rechazar_solicitud(self) -> None:
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        self.gestor.rechazar_solicitud(solicitud.id, "No autorizado por el jefe", "E009")
        self.assertEqual(EstadoSolicitud.RECHAZADA, solicitud.estado)
        self.assertIn("No autorizado", solicitud.observacion)
        self.assertAlmostEqual(0.0, self.gestor.total_a_pagar(), places=3)

    def test_validacion_aprobador_no_supervisor(self) -> None:
        """Solo un supervisor puede aprobar o rechazar (regla de negocio)."""
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        # E001 y E002 existen, pero son empleados (no supervisores).
        with self.assertRaises(AprobacionNoAutorizadaError):
            self.gestor.aprobar_solicitud(solicitud.id, "E001")
        with self.assertRaises(AprobacionNoAutorizadaError):
            self.gestor.rechazar_solicitud(solicitud.id, "No corresponde", "E002")
        # La solicitud debe seguir pendiente.
        self.assertEqual(EstadoSolicitud.PENDIENTE, solicitud.estado)

    def test_validacion_aprobador_inexistente(self) -> None:
        solicitud = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre de inventario"
        )
        with self.assertRaises(EmpleadoNoEncontradoError):
            self.gestor.aprobar_solicitud(solicitud.id, "E999")

    def test_hu05_solicitud_inexistente(self) -> None:
        with self.assertRaises(SolicitudNoEncontradaError):
            self.gestor.buscar_solicitud("SOL-999")

    # ------------------------------------------------------------------
    # HU09 / HU10 / HU11 - Horas compensadas
    # ------------------------------------------------------------------
    def test_hu09_hu10_registrar_horas_compensadas_y_saldo(self) -> None:
        self.gestor.registrar_horas_compensadas(
            "E001", date(2026, 9, 12), 8, "Compensacion por horas extras"
        )
        self.assertAlmostEqual(8.0, self.gestor.consultar_saldo("E001"), places=3)
        self.assertAlmostEqual(8.0, self.gestor.total_horas_compensadas_otorgadas(), places=3)

    def test_hu11_utilizar_horas_compensadas(self) -> None:
        self.gestor.registrar_horas_compensadas(
            "E001", date(2026, 9, 12), 8, "Compensacion por horas extras"
        )
        solicitud = self.gestor.utilizar_horas_compensadas(
            "E001", 3, "Tramite personal autorizado"
        )
        self.assertEqual(EstadoSolicitud.APROBADA, solicitud.estado)
        self.assertAlmostEqual(5.0, self.gestor.consultar_saldo("E001"), places=3)
        self.assertAlmostEqual(3.0, self.gestor.total_horas_compensadas_utilizadas(), places=3)

    def test_validacion_saldo_insuficiente(self) -> None:
        self.gestor.registrar_horas_compensadas(
            "E001", date(2026, 9, 12), 8, "Compensacion por horas extras"
        )
        with self.assertRaises(SaldoInsuficienteError):
            self.gestor.utilizar_horas_compensadas("E001", 9, "Excede el saldo")
        # El saldo no debe cambiar luego del intento fallido.
        self.assertAlmostEqual(8.0, self.gestor.consultar_saldo("E001"), places=3)

    # ------------------------------------------------------------------
    # Polimorfismo
    # ------------------------------------------------------------------
    def test_polimorfismo_calcular_valor(self) -> None:
        empleado = self.gestor.buscar_empleado_por_codigo("E001")
        movimientos: list[RegistroHora] = [
            HoraExtra(
                "RH-X1", empleado, date(2026, 9, 10), 2, "Hora extra de prueba",
                CalculadoraHoras.FACTOR_HORA_EXTRA_DEFECTO,
            ),
            HoraCompensada(
                "RH-X2", empleado, date(2026, 9, 11), 2, "Hora compensada de prueba", False
            ),
        ]
        # Misma referencia de tipo padre, distinto comportamiento.
        self.assertAlmostEqual(12.5 * 1.5 * 2, movimientos[0].calcular_valor(), places=3)  # 37.5
        self.assertAlmostEqual(12.5 * 2, movimientos[1].calcular_valor(), places=3)        # 25.0
        self.assertEqual("Hora extra", movimientos[0].obtener_tipo())
        self.assertEqual("Hora comp. otorg.", movimientos[1].obtener_tipo())

    def test_polimorfismo_obtener_rol(self) -> None:
        supervisor = self.gestor.buscar_empleado_por_codigo("E009")
        por_rol = self.gestor.listar_empleados_por_rol("Supervisor")
        self.assertEqual(1, len(por_rol))
        self.assertEqual("Supervisor", por_rol[0].obtener_rol())
        self.assertTrue(supervisor.puede_aprobar(8))
        self.assertFalse(supervisor.puede_aprobar(12))

    def test_polimorfismo_calcular_monto(self) -> None:
        hora_extra = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 4, "Soporte nocturno"
        )
        self.gestor.registrar_horas_compensadas("E001", date(2026, 9, 12), 8, "Otorgadas")
        compensacion = self.gestor.utilizar_horas_compensadas("E001", 2, "Uso")

        solicitudes: list[Solicitud] = [hora_extra, compensacion]
        self.assertAlmostEqual(12.5 * 1.5 * 4, solicitudes[0].calcular_monto(), places=3)  # 75.0
        self.assertAlmostEqual(12.5 * 2, solicitudes[1].calcular_monto(), places=3)        # 25.0
        self.assertEqual("Solicitud hora extra", solicitudes[0].obtener_tipo())
        self.assertEqual("Solicitud compensacion", solicitudes[1].obtener_tipo())

    # ------------------------------------------------------------------
    # Validaciones generales
    # ------------------------------------------------------------------
    def test_validacion_datos_empleado(self) -> None:
        with self.assertRaises(ValueError):
            self.gestor.registrar_empleado(
                "E020", "Sin", "Nombre", "DNI", "20000020",
                "x@empresa-demo.com", -100, "Cargo", date(2024, 1, 1),
            )
        with self.assertRaises(ValueError):
            self.gestor.registrar_empleado(
                "E021", "   ", "Apellido", "DNI", "20000021",
                "y@empresa-demo.com", 2000, "Cargo", date(2024, 1, 1),
            )

    # ------------------------------------------------------------------
    # Flujo completo
    # ------------------------------------------------------------------
    def test_flujo_pagar_y_compensar(self) -> None:
        pagar = self.gestor.registrar_solicitud_hora_extra(
            "E001", date(2026, 9, 10), 6, "Cierre"
        )
        self.gestor.aprobar_solicitud(pagar.id, "E009")
        self.gestor.pagar_solicitud(pagar.id, "E005")
        self.assertEqual(EstadoSolicitud.PAGADA, pagar.estado)
        self.assertAlmostEqual(112.5, self.gestor.total_pagado(), places=3)
        self.assertAlmostEqual(0.0, self.gestor.total_a_pagar(), places=3)

        compensar = self.gestor.registrar_solicitud_hora_extra(
            "E002", date(2026, 9, 14), 4, "Mantenimiento"
        )
        self.gestor.aprobar_solicitud(compensar.id, "E009")
        self.gestor.compensar_solicitud_hora_extra(compensar.id, "E005")
        self.assertEqual(EstadoSolicitud.COMPENSADA, compensar.estado)
        self.assertAlmostEqual(4.0, self.gestor.consultar_saldo("E002"), places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
