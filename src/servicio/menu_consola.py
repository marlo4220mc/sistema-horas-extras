"""Menu de consola del sistema."""

from __future__ import annotations

from datetime import date, datetime

from excepciones import (
    AprobacionNoAutorizadaError,
    EmpleadoDuplicadoError,
    EmpleadoNoEncontradoError,
    EstadoSolicitudInvalidaError,
    HorasInvalidasError,
    SaldoInsuficienteError,
    SolicitudNoEncontradaError,
)
from modelo.estado_solicitud import EstadoSolicitud
from modelo.registro_hora import RegistroHora
from modelo.solicitud import Solicitud
from modelo.supervisor import Supervisor
from servicio.gestor_horas_extras import GestorHorasExtras


class MenuConsola:
    """Lee opciones del usuario, invoca al GestorHorasExtras y muestra los
    resultados. Ninguna entrada incorrecta debe terminar el programa: los
    errores se capturan y se informan.
    """

    def __init__(self, gestor: GestorHorasExtras) -> None:
        if gestor is None:
            raise ValueError("El gestor es obligatorio.")
        self._gestor = gestor
        self._continuar = True
        self._entrada_agotada = False

    # ------------------------------------------------------------------
    # Bucle principal
    # ------------------------------------------------------------------
    def iniciar(self) -> None:
        self._mostrar_bienvenida()
        while self._continuar and not self._entrada_agotada:
            self._mostrar_menu_principal()
            opcion = self._leer_entero("Seleccione una opcion: ")
            if self._entrada_agotada:
                break
            self._ejecutar_opcion(opcion)
        print("\nFin de la ejecucion. Gracias por usar el sistema.")

    def _mostrar_bienvenida(self) -> None:
        print()
        print("=" * 56)
        print("   SISTEMA DE GESTION Y CONTROL DE HORAS EXTRAS")
        print("            Y HORAS COMPENSADAS")
        print("=" * 56)
        print(" Empresa: Fábrica Marsar SRL")
        print(" Curso  : 1FIS275 - Fundamentos de Programacion 2")
        print("=" * 56)

    def _mostrar_menu_principal(self) -> None:
        print()
        print("=" * 56)
        print("                  MENU PRINCIPAL")
        print("=" * 56)
        print(" 1. Registrar empleado")
        print(" 2. Buscar empleado")
        print(" 3. Listar empleados")
        print(" 4. Registrar horas extras")
        print(" 5. Listar solicitudes")
        print(" 6. Aprobar solicitud")
        print(" 7. Rechazar solicitud")
        print(" 8. Calcular pago de horas extras")
        print(" 9. Registrar horas compensadas")
        print("10. Consultar saldo")
        print("11. Utilizar horas compensadas")
        print("12. Historial")
        print("13. Reportes")
        print(" 0. Salir")
        print("=" * 56)

    def _ejecutar_opcion(self, opcion: int) -> None:
        try:
            if opcion == 1:
                self._registrar_empleado()
            elif opcion == 2:
                self._buscar_empleado()
            elif opcion == 3:
                self._listar_empleados()
            elif opcion == 4:
                self._registrar_horas_extras()
            elif opcion == 5:
                self._listar_solicitudes()
            elif opcion == 6:
                self._aprobar_solicitud()
            elif opcion == 7:
                self._rechazar_solicitud()
            elif opcion == 8:
                self._calcular_pago()
            elif opcion == 9:
                self._registrar_horas_compensadas()
            elif opcion == 10:
                self._consultar_saldo()
            elif opcion == 11:
                self._utilizar_horas_compensadas()
            elif opcion == 12:
                self._mostrar_historial()
            elif opcion == 13:
                self._menu_reportes()
            elif opcion == 0:
                self._continuar = False
            else:
                print("  ! Opcion no valida. Ingrese un numero del 0 al 13.")
        except ValueError as error:
            print(f"  ! Dato invalido: {error}")

    # ------------------------------------------------------------------
    # Opciones del menu
    # ------------------------------------------------------------------
    def _registrar_empleado(self) -> None:
        print("\n--- REGISTRAR EMPLEADO ---")
        # El codigo y el documento se validan apenas se ingresan, para no
        # pedir todo el formulario y recien al final avisar del duplicado.
        codigo = self._leer_codigo_disponible("Codigo de empleado (ej. E006): ")
        if self._entrada_agotada:
            return
        nombres = self._leer_texto("Nombres: ")
        apellidos = self._leer_texto("Apellidos: ")
        tipo_documento = self._leer_texto("Tipo de documento (DNI/CE): ")
        numero_documento = self._leer_documento_disponible("Numero de documento: ")
        if self._entrada_agotada:
            return
        correo = self._leer_correo("Correo: ")
        salario = self._leer_salario("Salario mensual: ")
        cargo = self._leer_texto("Cargo: ")
        fecha_ingreso = self._leer_fecha_no_futura(
            "Fecha de ingreso (dd/mm/aaaa): ", "La fecha de ingreso no puede ser futura."
        )
        if self._entrada_agotada:
            return
        try:
            empleado = self._gestor.registrar_empleado(
                codigo, nombres, apellidos, tipo_documento, numero_documento, correo,
                salario, cargo, fecha_ingreso,
            )
            print(f"  OK. Empleado registrado: {empleado}")
        except EmpleadoDuplicadoError as error:
            print(f"  ! {error}")

    def _leer_codigo_disponible(self, etiqueta: str) -> str:
        """Pide el codigo y avisa de inmediato si ya esta registrado."""
        while not self._entrada_agotada:
            codigo = self._leer_texto(etiqueta)
            if self._entrada_agotada or not codigo:
                return ""
            if self._gestor.existe_empleado_con_codigo(codigo):
                print(
                    f"  ! Ya existe un empleado con el codigo {codigo.upper()}."
                    " Ingrese otro codigo."
                )
                continue
            return codigo
        return ""

    def _leer_documento_disponible(self, etiqueta: str) -> str:
        """Pide el documento y avisa de inmediato si ya esta registrado."""
        while not self._entrada_agotada:
            documento = self._leer_texto(etiqueta)
            if self._entrada_agotada or not documento:
                return ""
            if self._gestor.existe_empleado_con_documento(documento):
                print(
                    f"  ! Ya existe un empleado con el documento {documento}."
                    " Ingrese otro documento."
                )
                continue
            return documento
        return ""

    def _leer_texto_validado(self, etiqueta: str, validador, mensaje_error: str) -> str:
        """Pide un texto y lo valida de inmediato; si falla, vuelve a pedirlo."""
        while not self._entrada_agotada:
            valor = self._leer_texto(etiqueta)
            if self._entrada_agotada or not valor:
                return ""
            try:
                validador(valor)
                return valor
            except ValueError:
                print(f"  ! {mensaje_error}")
        return ""

    def _leer_numero_validado(self, etiqueta: str, validador, mensaje_error: str) -> float:
        """Pide un numero y lo valida de inmediato; si falla, vuelve a pedirlo."""
        while not self._entrada_agotada:
            valor = self._leer_float(etiqueta)
            if self._entrada_agotada:
                return 0.0
            try:
                validador(valor)
                return valor
            except ValueError:
                print(f"  ! {mensaje_error}")
        return 0.0

    def _leer_correo(self, etiqueta: str) -> str:
        def valida(valor: str) -> None:
            if "@" not in valor or "." not in valor:
                raise ValueError

        return self._leer_texto_validado(
            etiqueta, valida, "El correo no es valido (ej. nombre@empresa.com)."
        )

    def _leer_salario(self, etiqueta: str) -> float:
        def valida(valor: float) -> None:
            if valor <= 0:
                raise ValueError

        return self._leer_numero_validado(
            etiqueta, valida, "El salario debe ser mayor a cero."
        )

    def _leer_horas(self, etiqueta: str) -> float:
        def valida(valor: float) -> None:
            if valor <= 0 or valor > 24:
                raise ValueError

        return self._leer_numero_validado(
            etiqueta, valida, "Las horas deben ser mayores a 0 y como maximo 24."
        )

    def _leer_horas_dentro_del_saldo(self, etiqueta: str, codigo: str) -> float:
        """Pide las horas a utilizar y avisa de inmediato si superan el saldo."""
        saldo = self._gestor.consultar_saldo(codigo)
        while not self._entrada_agotada:
            horas = self._leer_horas(etiqueta)
            if self._entrada_agotada:
                return horas
            if horas > saldo:
                print(
                    f"  ! Saldo insuficiente: dispone de {saldo:.2f} h."
                    " Ingrese una cantidad menor."
                )
                continue
            return horas
        return 0.0

    def _leer_fecha_no_futura(self, etiqueta: str, mensaje: str) -> date:
        """Pide una fecha y rechaza de inmediato una fecha futura."""
        while not self._entrada_agotada:
            fecha = self._leer_fecha(etiqueta)
            if self._entrada_agotada:
                return fecha
            if fecha > date.today():
                print(f"  ! {mensaje}")
                continue
            return fecha
        return date.today()

    def _leer_empleado_existente(self, etiqueta: str) -> str:
        """Pide un codigo y avisa de inmediato si el empleado no existe."""
        while not self._entrada_agotada:
            codigo = self._leer_texto(etiqueta)
            if self._entrada_agotada or not codigo:
                return ""
            if not self._gestor.existe_empleado_con_codigo(codigo):
                print(f"  ! No existe el empleado con codigo {codigo}. Ingrese otro codigo.")
                continue
            return codigo
        return ""

    def _leer_solicitud_existente(self, etiqueta: str) -> str:
        """Pide un id de solicitud y avisa de inmediato si no existe."""
        while not self._entrada_agotada:
            id_solicitud = self._leer_texto(etiqueta)
            if self._entrada_agotada or not id_solicitud:
                return ""
            try:
                self._gestor.buscar_solicitud(id_solicitud)
                return id_solicitud
            except SolicitudNoEncontradaError:
                print(f"  ! No existe la solicitud {id_solicitud}. Ingrese otro id.")
        return ""

    def _leer_solicitud_pendiente(self, etiqueta: str) -> str:
        """Pide un id y avisa de inmediato si no existe o si ya fue procesada."""
        while not self._entrada_agotada:
            id_solicitud = self._leer_texto(etiqueta)
            if self._entrada_agotada or not id_solicitud:
                return ""
            try:
                solicitud = self._gestor.buscar_solicitud(id_solicitud)
            except SolicitudNoEncontradaError:
                print(f"  ! No existe la solicitud {id_solicitud}. Ingrese otro id.")
                continue
            if solicitud.estado != EstadoSolicitud.PENDIENTE:
                print(
                    f"  ! La solicitud {id_solicitud} ya esta en estado "
                    f"{solicitud.estado.value} y no se puede procesar."
                )
                continue
            return id_solicitud
        return ""

    def _mostrar_supervisores(self) -> None:
        """Muestra los supervisores registrados para facilitar la eleccion."""
        supervisores = self._gestor.listar_empleados_por_rol("Supervisor")
        if supervisores:
            lista = ", ".join(
                f"{s.codigo_empleado} ({s.nombre_completo})" for s in supervisores
            )
            print(f"  Supervisores registrados: {lista}")

    def _leer_supervisor(self, etiqueta: str) -> str:
        """Pide el codigo de quien aprueba y valida de inmediato que sea supervisor."""
        while not self._entrada_agotada:
            codigo = self._leer_texto(etiqueta)
            if self._entrada_agotada or not codigo:
                return ""
            try:
                empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            except EmpleadoNoEncontradoError:
                print(f"  ! No existe el empleado con codigo {codigo}. Ingrese otro codigo.")
                continue
            if not isinstance(empleado, Supervisor):
                print(
                    f"  ! {empleado.nombre_completo} no es supervisor "
                    f"(rol: {empleado.obtener_rol()}). Ingrese otro codigo."
                )
                continue
            return codigo
        return ""

    def _buscar_empleado(self) -> None:
        print("\n--- BUSCAR EMPLEADO ---")
        print("1. Por codigo   2. Por documento   3. Por apellido")
        criterio = self._leer_entero("Criterio: ")
        try:
            if criterio == 1:
                empleado = self._gestor.buscar_empleado_por_codigo(
                    self._leer_texto("Codigo: ")
                )
                print(f"  {empleado}")
            elif criterio == 2:
                empleado = self._gestor.buscar_empleado_por_documento(
                    self._leer_texto("Documento: ")
                )
                print(f"  {empleado}")
            elif criterio == 3:
                encontrados = self._gestor.buscar_empleados_por_apellido(
                    self._leer_texto("Apellido: ")
                )
                if not encontrados:
                    print("  No se encontraron empleados con ese apellido.")
                for empleado in encontrados:
                    print(f"  {empleado}")
            else:
                print("  ! Criterio no valido.")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _listar_empleados(self) -> None:
        print("\n--- LISTA DE EMPLEADOS ---")
        empleados = self._gestor.listar_empleados()
        if not empleados:
            print("  No hay empleados registrados.")
            return
        for empleado in empleados:
            print(f"  {empleado}")
        print(f"  Total: {len(empleados)} empleado(s).")

    def _registrar_horas_extras(self) -> None:
        print("\n--- REGISTRAR HORAS EXTRAS ---")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            fecha = self._leer_fecha_no_futura(
                "Fecha en que se trabajo (dd/mm/aaaa): ",
                "La fecha en que se trabajo no puede ser futura.",
            )
            horas = self._leer_horas("Cantidad de horas: ")
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.registrar_solicitud_hora_extra(codigo, fecha, horas, motivo)
            print(
                f"  OK. Solicitud registrada: {solicitud.id} | "
                f"Estado: {solicitud.estado.value} | "
                f"Pago calculado: S/ {solicitud.calcular_monto():.2f}"
            )
        except (EmpleadoNoEncontradoError, HorasInvalidasError) as error:
            print(f"  ! {error}")

    def _listar_solicitudes(self) -> None:
        print("\n--- LISTA DE SOLICITUDES ---")
        solicitudes = self._gestor.listar_solicitudes()
        if not solicitudes:
            print("  No hay solicitudes registradas.")
            return
        for solicitud in solicitudes:
            print(f"  {solicitud.resumen()}")

    def _aprobar_solicitud(self) -> None:
        print("\n--- APROBAR SOLICITUD ---")
        try:
            id_solicitud = self._leer_solicitud_pendiente("Id de la solicitud (ej. SOL-001): ")
            if self._entrada_agotada:
                return
            self._mostrar_supervisores()
            codigo = self._leer_supervisor("Codigo del supervisor que aprueba: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.aprobar_solicitud(id_solicitud, codigo)
            print(
                f"  OK. La solicitud {solicitud.id} quedo {solicitud.estado.value} "
                f"(aprobada por {codigo})."
            )
        except (SolicitudNoEncontradaError, EstadoSolicitudInvalidaError,
                AprobacionNoAutorizadaError) as error:
            print(f"  ! {error}")

    def _rechazar_solicitud(self) -> None:
        print("\n--- RECHAZAR SOLICITUD ---")
        try:
            id_solicitud = self._leer_solicitud_pendiente("Id de la solicitud: ")
            if self._entrada_agotada:
                return
            motivo = self._leer_texto("Motivo del rechazo: ")
            self._mostrar_supervisores()
            codigo = self._leer_supervisor("Codigo del supervisor que rechaza: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.rechazar_solicitud(id_solicitud, motivo, codigo)
            print(
                f"  OK. La solicitud {solicitud.id} quedo {solicitud.estado.value} "
                f"(rechazada por {codigo})."
            )
        except (SolicitudNoEncontradaError, EstadoSolicitudInvalidaError,
                AprobacionNoAutorizadaError) as error:
            print(f"  ! {error}")

    def _calcular_pago(self) -> None:
        print("\n--- CALCULAR PAGO DE HORAS EXTRAS ---")
        try:
            id_solicitud = self._leer_solicitud_existente("Id de la solicitud: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.buscar_solicitud(id_solicitud)
            print(f"  Empleado......: {solicitud.empleado.nombre_completo}")
            print(f"  Valor hora....: S/ {self._gestor.calculadora.valor_hora(solicitud.empleado):.2f}")
            print(f"  {solicitud.detalle()}")
            print(f"  Estado........: {solicitud.estado.value}")
            print(f"  PAGO TOTAL....: S/ {self._gestor.calcular_pago_solicitud(id_solicitud):.2f}")
        except SolicitudNoEncontradaError as error:
            print(f"  ! {error}")

    def _registrar_horas_compensadas(self) -> None:
        print("\n--- REGISTRAR HORAS COMPENSADAS ---")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            fecha = self._leer_fecha_no_futura(
                "Fecha (dd/mm/aaaa): ", "La fecha no puede ser futura."
            )
            horas = self._leer_horas("Cantidad de horas a otorgar: ")
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            self._gestor.registrar_horas_compensadas(codigo, fecha, horas, motivo)
            print(
                "  OK. Horas compensadas registradas. "
                f"Nuevo saldo: {self._gestor.consultar_saldo(codigo)} h"
            )
        except (EmpleadoNoEncontradoError, HorasInvalidasError) as error:
            print(f"  ! {error}")

    def _consultar_saldo(self) -> None:
        print("\n--- CONSULTAR SALDO ---")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            print(f"  Empleado: {empleado.nombre_completo}")
            print(f"  Saldo de horas compensadas: {self._gestor.consultar_saldo(codigo)} h")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _utilizar_horas_compensadas(self) -> None:
        print("\n--- UTILIZAR HORAS COMPENSADAS ---")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            horas = self._leer_horas_dentro_del_saldo("Horas a utilizar: ", codigo)
            if self._entrada_agotada:
                return
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.utilizar_horas_compensadas(codigo, horas, motivo)
            print(f"  OK. Uso de horas compensadas registrado en la solicitud {solicitud.id}.")
            print(f"  Nuevo saldo: {self._gestor.consultar_saldo(codigo)} h")
        except (EmpleadoNoEncontradoError, HorasInvalidasError, SaldoInsuficienteError) as error:
            print(f"  ! {error}")

    def _mostrar_historial(self) -> None:
        print("\n--- HISTORIAL POR EMPLEADO ---")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            print(f"  Empleado: {empleado.nombre_completo}")
            print("  --- Movimientos de horas ---")
            movimientos = self._gestor.historial_por_empleado(codigo)
            if not movimientos:
                print("  Sin movimientos registrados.")
            for movimiento in movimientos:
                print(f"  {movimiento.resumen()}")
            print("  --- Solicitudes ---")
            solicitudes = self._gestor.solicitudes_por_empleado(codigo)
            if not solicitudes:
                print("  Sin solicitudes registradas.")
            for solicitud in solicitudes:
                print(f"  {solicitud.resumen()}")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _menu_reportes(self) -> None:
        volver = False
        while not volver and not self._entrada_agotada:
            print("\n--- REPORTES ---")
            print("1. Reporte general")
            print("2. Horas extras por empleado")
            print("3. Horas extras (registros)")
            print("4. Horas compensadas (registros)")
            print("5. Saldo de horas compensadas")
            print("6. Solicitudes pendientes")
            print("7. Total a pagar / pagado")
            print("0. Volver al menu principal")
            opcion = self._leer_entero("Reporte: ")
            if self._entrada_agotada:
                return
            if opcion == 1:
                print(self._gestor.reporte_general())
            elif opcion == 2:
                print(self._gestor.reporte_horas_extras_por_empleado())
            elif opcion == 3:
                self._imprimir_registros(self._gestor.listar_horas_extras(), "HORAS EXTRAS")
            elif opcion == 4:
                self._imprimir_registros(
                    self._gestor.listar_horas_compensadas(), "HORAS COMPENSADAS"
                )
            elif opcion == 5:
                print(self._gestor.reporte_saldos_compensadas())
            elif opcion == 6:
                self._imprimir_solicitudes(self._gestor.listar_solicitudes_pendientes())
            elif opcion == 7:
                print(f"  Total a pagar (aprobadas): S/ {self._gestor.total_a_pagar():.2f}")
                print(f"  Total pagado: S/ {self._gestor.total_pagado():.2f}")
            elif opcion == 0:
                volver = True
            else:
                print("  ! Opcion no valida.")

    def _imprimir_registros(self, registros: list[RegistroHora], titulo: str) -> None:
        print(f"\n--- {titulo} ---")
        if not registros:
            print("  Sin registros.")
            return
        for registro in registros:
            print(f"  {registro.resumen()}")

    def _imprimir_solicitudes(self, solicitudes: list[Solicitud]) -> None:
        print("\n--- SOLICITUDES PENDIENTES ---")
        if not solicitudes:
            print("  No hay solicitudes pendientes.")
            return
        for solicitud in solicitudes:
            print(f"  {solicitud.resumen()}")
            print(f"      {solicitud.detalle()}")

    # ------------------------------------------------------------------
    # Lectura de datos con validacion
    # ------------------------------------------------------------------
    def _leer_linea(self, etiqueta: str) -> str:
        try:
            return input(etiqueta).strip()
        except (EOFError, KeyboardInterrupt):
            self._entrada_agotada = True
            print()
            return ""

    def _leer_texto(self, etiqueta: str) -> str:
        while not self._entrada_agotada:
            valor = self._leer_linea(etiqueta)
            if valor:
                return valor
            print("  ! Este dato es obligatorio.")
        return ""

    def _leer_entero(self, etiqueta: str) -> int:
        while not self._entrada_agotada:
            valor = self._leer_linea(etiqueta)
            try:
                return int(valor)
            except ValueError:
                print("  ! Debe ingresar un numero entero.")
        return 0

    def _leer_float(self, etiqueta: str) -> float:
        while not self._entrada_agotada:
            valor = self._leer_linea(etiqueta).replace(",", ".")
            try:
                return float(valor)
            except ValueError:
                print("  ! Debe ingresar un numero valido (ej. 4.5).")
        return 0.0

    def _leer_fecha(self, etiqueta: str) -> date:
        while not self._entrada_agotada:
            valor = self._leer_linea(etiqueta)
            for formato in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(valor, formato).date()
                except ValueError:
                    continue
            print("  ! Fecha invalida. Use dd/mm/aaaa (ej. 15/09/2026).")
        return date.today()
