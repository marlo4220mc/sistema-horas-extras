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
from modelo.empleado import Empleado
from modelo.estado_solicitud import EstadoSolicitud
from modelo.hora_compensada import HoraCompensada
from modelo.registro_hora import RegistroHora
from modelo.responsable_rrhh import ResponsableRRHH
from modelo.solicitud import Solicitud
from modelo.solicitud_hora_extra import SolicitudHoraExtra
from modelo.supervisor import Supervisor
from servicio.gestor_horas_extras import GestorHorasExtras


class MenuConsola:
    """Lee opciones del usuario, invoca al GestorHorasExtras y muestra los
    resultados. Ninguna entrada incorrecta debe terminar el programa: los
    errores se capturan y se informan.
    """

    ANCHO_PANTALLA = 56
    COLUMNAS_EMPLEADOS = [
        ("Cod.", "<"), ("Nombre", "<"), ("Cargo", "<"),
        ("Rol", "<"), ("Salario S/", ">"), ("Saldo h", ">"),
    ]
    COLUMNAS_SOLICITUDES = [
        ("Id", "<"), ("Tipo", "<"), ("Cod.", "<"), ("Empleado", "<"),
        ("Fecha", "<"), ("Estado", "<"), ("Monto S/", ">"),
    ]
    COLUMNAS_REGISTROS = [
        ("Id", "<"), ("Cod.", "<"), ("Fecha", "<"), ("Tipo", "<"),
        ("Horas", ">"), ("Valor S/", ">"), ("Motivo", "<"),
    ]

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
        ancho = self.ANCHO_PANTALLA
        print()
        print("=" * ancho)
        print("SISTEMA DE GESTION Y CONTROL DE HORAS EXTRAS".center(ancho))
        print("Y HORAS COMPENSADAS".center(ancho))
        print("=" * ancho)
        print(" Empresa: Fábrica Marsar SRL")
        print(" Curso  : 1FIS275 - Fundamentos de Programacion 2")
        print("=" * ancho)

    def _mostrar_menu_principal(self) -> None:
        ancho = self.ANCHO_PANTALLA
        hoy = date.today().strftime("%d/%m/%Y")
        total_empleados = len(self._gestor.listar_empleados())
        pendientes = len(self._gestor.listar_solicitudes_pendientes())
        secciones = [
            ("EMPLEADOS", [
                (1, "Registrar empleado"),
                (2, "Buscar empleado"),
                (3, "Listar empleados"),
            ]),
            ("HORAS EXTRAS", [
                (4, "Registrar horas extras"),
                (5, "Listar solicitudes"),
                (6, "Aprobar solicitud"),
                (7, "Rechazar solicitud"),
                (8, "Calcular pago de horas extras"),
            ]),
            ("HORAS COMPENSADAS", [
                (9, "Registrar horas compensadas"),
                (10, "Consultar saldo"),
                (11, "Utilizar horas compensadas"),
            ]),
            ("CONSULTAS E INFORMES", [
                (12, "Historial"),
                (13, "Reportes"),
            ]),
        ]
        print()
        print("=" * ancho)
        print("MENU PRINCIPAL".center(ancho))
        print("=" * ancho)
        print(f" Fecha: {hoy} | Empleados: {total_empleados} | Pendientes: {pendientes}")
        print("-" * ancho)
        for titulo, opciones in secciones:
            print(f" {titulo}")
            for numero, texto in opciones:
                print(f"  {numero:>2}. {texto}")
        print("-" * ancho)
        print(f"  {0:>2}. Salir")
        print("=" * ancho)

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
        self._encabezado_pantalla("REGISTRAR EMPLEADO")
        print(" Complete los datos del nuevo empleado.")
        self._linea()
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
            self._linea()
            print(" OK. Empleado registrado correctamente.")
            self._imprimir_ficha_empleado(empleado)
            self._linea("=")
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
        self._encabezado_pantalla("BUSCAR EMPLEADO")
        print(" Criterios de busqueda:")
        print("   1. Por codigo")
        print("   2. Por documento")
        print("   3. Por apellido")
        self._linea()
        criterio = self._leer_entero("Criterio: ")
        try:
            if criterio == 1:
                empleado = self._gestor.buscar_empleado_por_codigo(
                    self._leer_texto("Codigo: ")
                )
                self._linea()
                self._imprimir_ficha_empleado(empleado)
                self._linea("=")
            elif criterio == 2:
                empleado = self._gestor.buscar_empleado_por_documento(
                    self._leer_texto("Documento: ")
                )
                self._linea()
                self._imprimir_ficha_empleado(empleado)
                self._linea("=")
            elif criterio == 3:
                encontrados = self._gestor.buscar_empleados_por_apellido(
                    self._leer_texto("Apellido: ")
                )
                if not encontrados:
                    self._linea()
                    print("  No se encontraron empleados con ese apellido.")
                else:
                    self._imprimir_tabla(
                        "RESULTADOS DE LA BUSQUEDA", self.COLUMNAS_EMPLEADOS,
                        self._filas_empleados(encontrados),
                        f"Coincidencias: {len(encontrados)} empleado(s).",
                    )
            else:
                print("  ! Criterio no valido.")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _listar_empleados(self) -> None:
        empleados = self._gestor.listar_empleados()
        if not empleados:
            self._encabezado_pantalla("LISTA DE EMPLEADOS")
            print("  No hay empleados registrados.")
            return
        self._imprimir_tabla(
            "LISTA DE EMPLEADOS", self.COLUMNAS_EMPLEADOS,
            self._filas_empleados(empleados),
            f"Total: {len(empleados)} empleado(s).",
        )

    def _registrar_horas_extras(self) -> None:
        self._encabezado_pantalla("REGISTRAR HORAS EXTRAS")
        print(" Ingrese los datos de las horas extras trabajadas.")
        self._linea()
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            print(f"  Empleado: {empleado.nombre_completo} | {empleado.cargo}")
            fecha = self._leer_fecha_no_futura(
                "Fecha en que se trabajo (dd/mm/aaaa): ",
                "La fecha en que se trabajo no puede ser futura.",
            )
            horas = self._leer_horas("Cantidad de horas: ")
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.registrar_solicitud_hora_extra(codigo, fecha, horas, motivo)
            hora_extra = solicitud.hora_extra
            valor_hora = self._gestor.calculadora.valor_hora(empleado)
            self._linea()
            print(" OK. Solicitud de horas extras registrada.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
                ("Fecha trabajada", hora_extra.fecha.strftime("%d/%m/%Y")),
                ("Horas", f"{hora_extra.cantidad_horas:.2f} h"),
                ("Motivo", hora_extra.motivo),
                ("Valor hora", f"S/ {valor_hora:.2f}"),
                ("Factor de recargo", f"{hora_extra.factor_recargo:.2f}"),
                ("Pago calculado", f"S/ {solicitud.calcular_monto():.2f}"),
                ("Estado", solicitud.estado.value),
            ])
            print(" La solicitud queda PENDIENTE hasta que un supervisor la apruebe.")
            self._linea("=")
        except (EmpleadoNoEncontradoError, HorasInvalidasError) as error:
            print(f"  ! {error}")

    def _listar_solicitudes(self) -> None:
        solicitudes = self._gestor.listar_solicitudes()
        if not solicitudes:
            self._encabezado_pantalla("LISTA DE SOLICITUDES")
            print("  No hay solicitudes registradas.")
            return
        por_estado = []
        for estado in EstadoSolicitud:
            cantidad = sum(1 for s in solicitudes if s.estado == estado)
            if cantidad:
                por_estado.append(f"{estado.value}: {cantidad}")
        self._imprimir_tabla(
            "LISTA DE SOLICITUDES", self.COLUMNAS_SOLICITUDES,
            self._filas_solicitudes(solicitudes),
            f"Total: {len(solicitudes)} solicitud(es) | " + " | ".join(por_estado),
        )

    def _aprobar_solicitud(self) -> None:
        self._encabezado_pantalla("APROBAR SOLICITUD")
        if not self._mostrar_pendientes_para_decidir():
            return
        try:
            id_solicitud = self._leer_solicitud_pendiente("Id de la solicitud (ej. SOL-001): ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.buscar_solicitud(id_solicitud)
            self._linea()
            self._imprimir_campos(self._campos_solicitud(solicitud))
            self._linea()
            self._mostrar_supervisores()
            codigo = self._leer_supervisor("Codigo del supervisor que aprueba: ")
            if self._entrada_agotada:
                return
            supervisor = self._gestor.buscar_empleado_por_codigo(codigo)
            solicitud = self._gestor.aprobar_solicitud(id_solicitud, codigo)
            self._linea()
            print(" OK. Solicitud aprobada.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Estado", solicitud.estado.value),
                ("Aprobada por", f"{supervisor.codigo_empleado} - {supervisor.nombre_completo}"),
                ("Fecha de decision", solicitud.fecha_resolucion.strftime("%d/%m/%Y %H:%M")),
            ])
            self._linea("=")
        except (SolicitudNoEncontradaError, EstadoSolicitudInvalidaError,
                AprobacionNoAutorizadaError) as error:
            print(f"  ! {error}")

    def _rechazar_solicitud(self) -> None:
        self._encabezado_pantalla("RECHAZAR SOLICITUD")
        if not self._mostrar_pendientes_para_decidir():
            return
        try:
            id_solicitud = self._leer_solicitud_pendiente("Id de la solicitud: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.buscar_solicitud(id_solicitud)
            self._linea()
            self._imprimir_campos(self._campos_solicitud(solicitud))
            self._linea()
            motivo = self._leer_texto("Motivo del rechazo: ")
            self._mostrar_supervisores()
            codigo = self._leer_supervisor("Codigo del supervisor que rechaza: ")
            if self._entrada_agotada:
                return
            supervisor = self._gestor.buscar_empleado_por_codigo(codigo)
            solicitud = self._gestor.rechazar_solicitud(id_solicitud, motivo, codigo)
            self._linea()
            print(" OK. Solicitud rechazada.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Estado", solicitud.estado.value),
                ("Rechazada por", f"{supervisor.codigo_empleado} - {supervisor.nombre_completo}"),
                ("Motivo del rechazo", solicitud.observacion),
                ("Fecha de decision", solicitud.fecha_resolucion.strftime("%d/%m/%Y %H:%M")),
            ])
            self._linea("=")
        except (SolicitudNoEncontradaError, EstadoSolicitudInvalidaError,
                AprobacionNoAutorizadaError) as error:
            print(f"  ! {error}")

    def _calcular_pago(self) -> None:
        self._encabezado_pantalla("CALCULAR PAGO DE HORAS EXTRAS")
        try:
            id_solicitud = self._leer_solicitud_existente("Id de la solicitud (ej. SOL-001): ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.buscar_solicitud(id_solicitud)
            empleado = solicitud.empleado
            self._linea()
            self._imprimir_campos(
                [c for c in self._campos_solicitud(solicitud) if c[0] != "Pago calculado"]
            )
            self._linea()
            print(" CALCULO DEL PAGO")
            etiqueta_total = "PAGO TOTAL"
            if isinstance(solicitud, SolicitudHoraExtra):
                hora_extra = solicitud.hora_extra
                self._imprimir_campos([
                    ("Salario mensual", f"S/ {empleado.salario_mensual:,.2f}"),
                    ("Horas al mes", f"{empleado.jornada.calcular_horas_mensuales():.0f}"),
                    ("Valor hora", f"S/ {self._gestor.calculadora.valor_hora(empleado):.2f}"),
                    ("Factor de recargo", f"{hora_extra.factor_recargo:.2f}"),
                    ("Horas trabajadas", f"{hora_extra.cantidad_horas:.2f} h"),
                ])
                print(" Formula: (salario / horas al mes) x factor x horas")
            else:
                print(" Equivalente economico de las horas de la solicitud.")
                etiqueta_total = "EQUIVALENTE"
            pago = self._gestor.calcular_pago_solicitud(id_solicitud)
            self._imprimir_campos([(etiqueta_total, f"S/ {pago:.2f}")])
            self._linea()
            if isinstance(solicitud, SolicitudHoraExtra):
                self._ofrecer_acciones_pago(solicitud)
            self._linea("=")
        except (SolicitudNoEncontradaError, EstadoSolicitudInvalidaError) as error:
            print(f"  ! {error}")

    def _ofrecer_acciones_pago(self, solicitud: SolicitudHoraExtra) -> None:
        """Segun el flujo de pago documentado: una solicitud APROBADA puede
        pagarse (PAGADA) o convertirse en horas compensadas (COMPENSADA).
        """
        estado = solicitud.estado
        if estado != EstadoSolicitud.APROBADA:
            if estado in (EstadoSolicitud.PAGADA, EstadoSolicitud.COMPENSADA):
                print(f" La solicitud ya fue {estado.value}.")
            else:
                print(" Solo una solicitud APROBADA puede pagarse o compensarse.")
            return
        print(" Acciones para esta solicitud aprobada:")
        print("   1. Registrar el pago (estado PAGADA)")
        print("   2. Convertir en horas compensadas (estado COMPENSADA)")
        print("   0. No realizar ninguna accion")
        accion = -1
        while accion not in (0, 1, 2) and not self._entrada_agotada:
            accion = self._leer_entero("Accion: ")
            if accion not in (0, 1, 2) and not self._entrada_agotada:
                print("  ! Ingrese 0, 1 o 2.")
        if self._entrada_agotada or accion == 0:
            return
        usuario = self._gestor.USUARIO_SISTEMA
        self._linea()
        if accion == 1:
            self._gestor.pagar_solicitud(solicitud.id, usuario)
            print(" OK. Pago registrado.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Estado", solicitud.estado.value),
                ("Monto pagado", f"S/ {self._gestor.calcular_pago_solicitud(solicitud.id):.2f}"),
                ("Fecha de registro", solicitud.fecha_resolucion.strftime("%d/%m/%Y %H:%M")),
            ])
        else:
            self._gestor.compensar_solicitud_hora_extra(solicitud.id, usuario)
            codigo = solicitud.empleado.codigo_empleado
            print(" OK. Solicitud convertida en horas compensadas.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Estado", solicitud.estado.value),
                ("Horas acreditadas", f"{solicitud.hora_extra.cantidad_horas:.2f} h"),
                ("Nuevo saldo", f"{self._gestor.consultar_saldo(codigo):.2f} h"),
            ])

    def _registrar_horas_compensadas(self) -> None:
        self._encabezado_pantalla("REGISTRAR HORAS COMPENSADAS")
        print(" Ingrese los datos de las horas compensadas a otorgar.")
        self._linea()
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            saldo_anterior = self._gestor.consultar_saldo(codigo)
            print(
                f"  Empleado: {empleado.nombre_completo} | "
                f"Saldo actual: {saldo_anterior:.2f} h"
            )
            fecha = self._leer_fecha_no_futura(
                "Fecha (dd/mm/aaaa): ", "La fecha no puede ser futura."
            )
            horas = self._leer_horas("Cantidad de horas a otorgar: ")
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            movimiento = self._gestor.registrar_horas_compensadas(codigo, fecha, horas, motivo)
            self._linea()
            print(" OK. Horas compensadas registradas.")
            self._imprimir_campos([
                ("Registro", movimiento.id),
                ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
                ("Fecha", movimiento.fecha.strftime("%d/%m/%Y")),
                ("Horas otorgadas", f"{movimiento.cantidad_horas:.2f} h"),
                ("Motivo", movimiento.motivo),
                ("Saldo anterior", f"{saldo_anterior:.2f} h"),
                ("Nuevo saldo", f"{self._gestor.consultar_saldo(codigo):.2f} h"),
            ])
            self._linea("=")
        except (EmpleadoNoEncontradoError, HorasInvalidasError) as error:
            print(f"  ! {error}")

    def _consultar_saldo(self) -> None:
        self._encabezado_pantalla("CONSULTAR SALDO")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            otorgadas, utilizadas = self._horas_compensadas_por_empleado(codigo)
            self._linea()
            self._imprimir_campos([
                ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
                ("Cargo", empleado.cargo),
                ("Horas otorgadas", f"{otorgadas:.2f} h"),
                ("Horas utilizadas", f"{utilizadas:.2f} h"),
                ("SALDO DISPONIBLE", f"{self._gestor.consultar_saldo(codigo):.2f} h"),
            ])
            self._linea("=")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _utilizar_horas_compensadas(self) -> None:
        self._encabezado_pantalla("UTILIZAR HORAS COMPENSADAS")
        print(" Descuente horas del saldo compensado del empleado.")
        self._linea()
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            saldo_anterior = self._gestor.consultar_saldo(codigo)
            print(
                f"  Empleado: {empleado.nombre_completo} | "
                f"Saldo disponible: {saldo_anterior:.2f} h"
            )
            if saldo_anterior <= 0:
                print("  ! El empleado no tiene horas compensadas disponibles.")
                self._linea("=")
                return
            horas = self._leer_horas_dentro_del_saldo("Horas a utilizar: ", codigo)
            if self._entrada_agotada:
                return
            motivo = self._leer_texto("Motivo: ")
            if self._entrada_agotada:
                return
            solicitud = self._gestor.utilizar_horas_compensadas(codigo, horas, motivo)
            self._linea()
            print(" OK. Uso de horas compensadas registrado.")
            self._imprimir_campos([
                ("Solicitud", solicitud.id),
                ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
                ("Horas utilizadas", f"{solicitud.cantidad_horas:.2f} h"),
                ("Motivo", solicitud.motivo_uso),
                ("Saldo anterior", f"{saldo_anterior:.2f} h"),
                ("Nuevo saldo", f"{self._gestor.consultar_saldo(codigo):.2f} h"),
                ("Estado", solicitud.estado.value),
            ])
            self._linea("=")
        except (EmpleadoNoEncontradoError, HorasInvalidasError, SaldoInsuficienteError) as error:
            print(f"  ! {error}")

    def _mostrar_historial(self) -> None:
        self._encabezado_pantalla("HISTORIAL POR EMPLEADO")
        try:
            codigo = self._leer_empleado_existente("Codigo del empleado: ")
            if self._entrada_agotada:
                return
            empleado = self._gestor.buscar_empleado_por_codigo(codigo)
            self._linea()
            self._imprimir_campos([
                ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
                ("Cargo", empleado.cargo),
                ("Saldo compensado", f"{self._gestor.consultar_saldo(codigo):.2f} h"),
            ])
            self._linea("=")
            movimientos = self._gestor.historial_por_empleado(codigo)
            if movimientos:
                self._imprimir_tabla(
                    "MOVIMIENTOS DE HORAS", self.COLUMNAS_REGISTROS,
                    self._filas_registros(movimientos),
                    f"Total: {len(movimientos)} movimiento(s).",
                )
            else:
                self._imprimir_seccion_vacia("MOVIMIENTOS DE HORAS", "Sin movimientos registrados.")
            solicitudes = self._gestor.solicitudes_por_empleado(codigo)
            if solicitudes:
                self._imprimir_tabla(
                    "SOLICITUDES DEL EMPLEADO", self.COLUMNAS_SOLICITUDES,
                    self._filas_solicitudes(solicitudes),
                    f"Total: {len(solicitudes)} solicitud(es).",
                )
            else:
                self._imprimir_seccion_vacia("SOLICITUDES DEL EMPLEADO", "Sin solicitudes registradas.")
        except EmpleadoNoEncontradoError as error:
            print(f"  ! {error}")

    def _menu_reportes(self) -> None:
        opciones = [
            (1, "Reporte general"),
            (2, "Horas extras por empleado"),
            (3, "Horas extras (registros)"),
            (4, "Horas compensadas (registros)"),
            (5, "Saldo de horas compensadas"),
            (6, "Solicitudes pendientes"),
            (7, "Total a pagar / pagado"),
        ]
        volver = False
        while not volver and not self._entrada_agotada:
            self._encabezado_pantalla("REPORTES")
            for numero, texto in opciones:
                print(f"  {numero:>2}. {texto}")
            self._linea()
            print(f"  {0:>2}. Volver al menu principal")
            self._linea("=")
            opcion = self._leer_entero("Reporte: ")
            if self._entrada_agotada:
                return
            if opcion == 1:
                self._reporte_general()
            elif opcion == 2:
                self._reporte_horas_extras_por_empleado()
            elif opcion == 3:
                self._imprimir_registros(
                    self._gestor.listar_horas_extras(), "HORAS EXTRAS (REGISTROS)"
                )
            elif opcion == 4:
                self._imprimir_registros(
                    self._gestor.listar_horas_compensadas(), "HORAS COMPENSADAS (REGISTROS)"
                )
            elif opcion == 5:
                self._reporte_saldos_compensadas()
            elif opcion == 6:
                self._imprimir_solicitudes(self._gestor.listar_solicitudes_pendientes())
            elif opcion == 7:
                self._reporte_totales_pago()
            elif opcion == 0:
                volver = True
            else:
                print("  ! Opcion no valida.")

    def _reporte_general(self) -> None:
        gestor = self._gestor
        self._encabezado_pantalla("REPORTE GENERAL")
        self._imprimir_campos([
            ("Empleados registrados", str(len(gestor.listar_empleados()))),
            ("Solicitudes registradas", str(len(gestor.listar_solicitudes()))),
            ("Solicitudes pendientes", str(len(gestor.listar_solicitudes_pendientes()))),
            ("Total de horas extras", f"{gestor.total_horas_extras():.2f} h"),
            ("Total a pagar (aprobadas)", f"S/ {gestor.total_a_pagar():.2f}"),
            ("Total pagado", f"S/ {gestor.total_pagado():.2f}"),
            ("Horas comp. otorgadas", f"{gestor.total_horas_compensadas_otorgadas():.2f} h"),
            ("Horas comp. utilizadas", f"{gestor.total_horas_compensadas_utilizadas():.2f} h"),
        ], 26)
        self._linea("=")
        solicitudes = gestor.listar_solicitudes()
        if solicitudes:
            self._imprimir_tabla(
                "DETALLE DE SOLICITUDES", self.COLUMNAS_SOLICITUDES,
                self._filas_solicitudes(solicitudes),
                f"Total: {len(solicitudes)} solicitud(es).",
            )

    def _reporte_horas_extras_por_empleado(self) -> None:
        horas_extras = self._gestor.listar_horas_extras()
        filas = []
        total_horas = 0.0
        total_monto = 0.0
        for empleado in self._gestor.listar_empleados():
            registros = [r for r in horas_extras if r.empleado is empleado]
            if not registros:
                continue
            horas = sum(r.cantidad_horas for r in registros)
            monto = sum(r.calcular_valor() for r in registros)
            total_horas += horas
            total_monto += monto
            filas.append((
                empleado.codigo_empleado, empleado.nombre_completo, str(len(registros)),
                f"{horas:.2f}", f"{monto:,.2f}",
            ))
        if not filas:
            self._imprimir_seccion_vacia("HORAS EXTRAS POR EMPLEADO", "Sin registros.")
            return
        self._imprimir_tabla(
            "HORAS EXTRAS POR EMPLEADO",
            [("Cod.", "<"), ("Empleado", "<"), ("Registros", ">"),
             ("Horas", ">"), ("Monto S/", ">")],
            filas,
            f"Total: {total_horas:.2f} h | S/ {total_monto:,.2f}",
        )

    def _reporte_saldos_compensadas(self) -> None:
        filas = []
        total_saldo = 0.0
        for empleado in self._gestor.listar_empleados():
            otorgadas, utilizadas = self._horas_compensadas_por_empleado(empleado.codigo_empleado)
            saldo = empleado.saldo_horas_compensadas
            total_saldo += saldo
            filas.append((
                empleado.codigo_empleado, empleado.nombre_completo,
                f"{otorgadas:.2f}", f"{utilizadas:.2f}", f"{saldo:.2f}",
            ))
        if not filas:
            self._imprimir_seccion_vacia("SALDO DE HORAS COMPENSADAS", "No hay empleados registrados.")
            return
        self._imprimir_tabla(
            "SALDO DE HORAS COMPENSADAS",
            [("Cod.", "<"), ("Empleado", "<"), ("Otorgadas h", ">"),
             ("Utilizadas h", ">"), ("Saldo h", ">")],
            filas,
            f"Saldo total: {total_saldo:.2f} h",
        )

    def _reporte_totales_pago(self) -> None:
        gestor = self._gestor
        extras = [s for s in gestor.listar_solicitudes() if isinstance(s, SolicitudHoraExtra)]
        aprobadas = sum(1 for s in extras if s.estado == EstadoSolicitud.APROBADA)
        pagadas = sum(1 for s in extras if s.estado == EstadoSolicitud.PAGADA)
        self._encabezado_pantalla("TOTAL A PAGAR / PAGADO")
        self._imprimir_campos([
            ("Aprobadas por pagar", str(aprobadas)),
            ("Total a pagar", f"S/ {gestor.total_a_pagar():.2f}"),
            ("Solicitudes pagadas", str(pagadas)),
            ("Total pagado", f"S/ {gestor.total_pagado():.2f}"),
        ], 22)
        self._linea("=")

    def _imprimir_registros(self, registros: list[RegistroHora], titulo: str) -> None:
        if not registros:
            self._imprimir_seccion_vacia(titulo, "Sin registros.")
            return
        total_horas = sum(r.cantidad_horas for r in registros)
        self._imprimir_tabla(
            titulo, self.COLUMNAS_REGISTROS, self._filas_registros(registros),
            f"Total: {len(registros)} registro(s) | {total_horas:.2f} h",
        )

    def _imprimir_solicitudes(self, solicitudes: list[Solicitud]) -> None:
        if not solicitudes:
            self._imprimir_seccion_vacia("SOLICITUDES PENDIENTES", "No hay solicitudes pendientes.")
            return
        self._imprimir_tabla(
            "SOLICITUDES PENDIENTES", self.COLUMNAS_SOLICITUDES,
            self._filas_solicitudes(solicitudes),
            f"Total: {len(solicitudes)} solicitud(es) pendiente(s).",
        )

    # ------------------------------------------------------------------
    # Presentacion de pantallas (helpers visuales)
    # ------------------------------------------------------------------
    def _encabezado_pantalla(self, titulo: str, ancho: int | None = None) -> None:
        """Imprime el titulo de una pantalla entre dos lineas de '='."""
        ancho = ancho or self.ANCHO_PANTALLA
        print()
        print("=" * ancho)
        print(titulo.center(ancho).rstrip())
        print("=" * ancho)

    def _linea(self, caracter: str = "-", ancho: int | None = None) -> None:
        """Imprime una linea separadora con el ancho de pantalla."""
        print(caracter * (ancho or self.ANCHO_PANTALLA))

    def _imprimir_tabla(
        self,
        titulo: str,
        columnas: list[tuple[str, str]],
        filas: list[tuple],
        pie: str | None = None,
    ) -> None:
        """Imprime una pantalla con una tabla. 'columnas' es una lista de
        (nombre, alineacion) con alineacion '<' (izquierda) o '>' (derecha).
        El ancho de cada columna se ajusta al contenido.
        """
        textos = [tuple(str(celda) for celda in fila) for fila in filas]
        anchos = [
            max([len(nombre)] + [len(fila[i]) for fila in textos])
            for i, (nombre, _) in enumerate(columnas)
        ]
        ancho_total = max(
            self.ANCHO_PANTALLA, 1 + sum(anchos) + 3 * (len(anchos) - 1)
        )

        def formatear(celdas: tuple) -> str:
            partes = [
                f"{celda:{alineacion}{ancho}}"
                for celda, (_, alineacion), ancho in zip(celdas, columnas, anchos)
            ]
            return (" " + " | ".join(partes)).rstrip()

        self._encabezado_pantalla(titulo, ancho_total)
        print(formatear(tuple(nombre for nombre, _ in columnas)))
        self._linea("-", ancho_total)
        for fila in textos:
            print(formatear(fila))
        self._linea("-", ancho_total)
        if pie:
            print(f" {pie}")
        self._linea("=", ancho_total)

    def _filas_empleados(self, empleados: list[Empleado]) -> list[tuple]:
        """Convierte empleados en filas para COLUMNAS_EMPLEADOS."""
        return [
            (
                e.codigo_empleado, e.nombre_completo, e.cargo, e.obtener_rol(),
                f"{e.salario_mensual:,.2f}", f"{e.saldo_horas_compensadas:.2f}",
            )
            for e in empleados
        ]

    def _filas_solicitudes(self, solicitudes: list[Solicitud]) -> list[tuple]:
        """Convierte solicitudes en filas para COLUMNAS_SOLICITUDES."""
        return [
            (
                s.id, s.obtener_tipo(), s.empleado.codigo_empleado,
                s.empleado.nombre_completo, s.fecha_solicitud.strftime("%d/%m/%Y"),
                s.estado.value, f"{s.calcular_monto():,.2f}",
            )
            for s in solicitudes
        ]

    def _imprimir_campos(self, campos: list[tuple[str, str]], ancho: int = 18) -> None:
        """Imprime pares (etiqueta, valor), uno por linea, con puntos de relleno."""
        for etiqueta, valor in campos:
            print(f" {etiqueta:.<{ancho}}: {valor}")

    def _imprimir_seccion_vacia(self, titulo: str, mensaje: str) -> None:
        """Pantalla de una sola linea para cuando no hay datos que mostrar."""
        self._encabezado_pantalla(titulo)
        print(f" {mensaje}")
        self._linea("=")

    def _filas_registros(self, registros: list[RegistroHora]) -> list[tuple]:
        """Convierte movimientos de horas en filas para COLUMNAS_REGISTROS."""
        return [
            (
                r.id, r.empleado.codigo_empleado, r.fecha.strftime("%d/%m/%Y"),
                r.obtener_tipo(), f"{r.cantidad_horas:.2f}",
                f"{r.calcular_valor():,.2f}", r.motivo,
            )
            for r in registros
        ]

    def _horas_compensadas_por_empleado(self, codigo: str) -> tuple[float, float]:
        """Devuelve (horas otorgadas, horas utilizadas) de un empleado."""
        movimientos = [
            m for m in self._gestor.historial_por_empleado(codigo)
            if isinstance(m, HoraCompensada)
        ]
        otorgadas = sum(m.cantidad_horas for m in movimientos if not m.es_consumo)
        utilizadas = sum(m.cantidad_horas for m in movimientos if m.es_consumo)
        return otorgadas, utilizadas

    def _mostrar_pendientes_para_decidir(self) -> bool:
        """Lista las solicitudes pendientes. Devuelve False si no hay ninguna,
        para que la pantalla termine en vez de pedir un id que no existe.
        """
        pendientes = self._gestor.listar_solicitudes_pendientes()
        if not pendientes:
            print(" No hay solicitudes pendientes.")
            self._linea("=")
            return False
        print(" Solicitudes pendientes de decision:")
        for solicitud in pendientes:
            print(
                f"   {solicitud.id} | {solicitud.empleado.nombre_completo} "
                f"({solicitud.empleado.codigo_empleado}) | "
                f"S/ {solicitud.calcular_monto():.2f}"
            )
        self._linea()
        return True

    def _campos_solicitud(self, solicitud: Solicitud) -> list[tuple[str, str]]:
        """Datos de una solicitud listos para _imprimir_campos."""
        empleado = solicitud.empleado
        campos = [
            ("Solicitud", solicitud.id),
            ("Tipo", solicitud.obtener_tipo()),
            ("Empleado", f"{empleado.codigo_empleado} - {empleado.nombre_completo}"),
        ]
        if isinstance(solicitud, SolicitudHoraExtra):
            hora_extra = solicitud.hora_extra
            campos += [
                ("Fecha trabajada", hora_extra.fecha.strftime("%d/%m/%Y")),
                ("Horas", f"{hora_extra.cantidad_horas:.2f} h"),
                ("Motivo", hora_extra.motivo),
            ]
        else:
            campos.append(("Detalle", solicitud.detalle()))
        campos += [
            ("Pago calculado", f"S/ {solicitud.calcular_monto():.2f}"),
            ("Estado actual", solicitud.estado.value),
        ]
        return campos

    def _imprimir_ficha_empleado(self, empleado: Empleado) -> None:
        """Muestra todos los datos de un empleado, uno por linea."""
        campos = [
            ("Codigo", empleado.codigo_empleado),
            ("Nombre", empleado.nombre_completo),
            ("Documento", f"{empleado.tipo_documento} {empleado.numero_documento}"),
            ("Correo", empleado.correo),
            ("Cargo", empleado.cargo),
            ("Rol", empleado.obtener_rol()),
            ("Fecha de ingreso", empleado.fecha_ingreso.strftime("%d/%m/%Y")),
            ("Salario mensual", f"S/ {empleado.salario_mensual:,.2f}"),
            ("Valor hora", f"S/ {self._gestor.calculadora.valor_hora(empleado):.2f}"),
            ("Saldo compensado", f"{empleado.saldo_horas_compensadas:.2f} h"),
        ]
        if isinstance(empleado, Supervisor):
            campos.append(("Area a cargo", empleado.area_a_cargo))
            campos.append(
                ("Limite aprobable", f"{empleado.limite_horas_aprobables:.1f} h")
            )
        elif isinstance(empleado, ResponsableRRHH):
            campos.append(("Responsabilidad", empleado.responsabilidad_principal))
        self._imprimir_campos(campos)

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