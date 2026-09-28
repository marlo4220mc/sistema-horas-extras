# ETAPA 2 — Definición del Sistema

---

## 1. Nombre del sistema

**Sistema de Gestión y Control de Horas Extras y Horas Compensadas**

## 2. Objetivo

Desarrollar una aplicación de consola en Python que permita registrar,
gestionar, controlar, consultar y calcular las horas extras y las horas
compensadas de los empleados de [NOMBRE DE LA EMPRESA].

## 3. Alcance

### 3.1 Dentro del alcance

- Aplicación de consola en Python 3 (solo biblioteca estándar).
- Persistencia en memoria (sin base de datos).
- Carga de datos de demostración al iniciar para que el sistema sea
  inmediatamente operable.
- Cálculos de pago y saldo con reglas configurables.

### 3.2 Fuera del alcance

- Interfaz gráfica.
- Base de datos.
- Aplicación web.
- Integración con sistemas externos de planillas.
- Notificaciones por correo o mensajería.

## 4. Usuarios del sistema

| Rol | Descripción |
|-----|-------------|
| **Responsable de RR. HH.** | Registra empleados, aprueba o rechaza solicitudes, consulta reportes. |
| **Supervisor** | Aprueba o rechaza solicitudes; solo un supervisor puede hacerlo. |
| **Empleado** | Origen de las solicitudes y de las horas compensadas. |

> Nota: el sistema identifica el rol con `obtener_rol()`, pero como el
> prototipo es académico, desde la consola se pueden usar todas las
> funcionalidades.

## 5. Funcionalidades del sistema

### 5.1 Gestión de empleados

| Código | Funcionalidad |
|--------|---------------|
| F1 | Registrar empleado. |
| F2 | Buscar empleado por código, documento o apellido. |
| F3 | Listar empleados. |

### 5.2 Gestión de horas extras

| Código | Funcionalidad |
|--------|---------------|
| F4 | Registrar solicitud de horas extras. |
| F5 | Listar y consultar solicitudes. |
| F6 | Aprobar solicitud. |
| F7 | Rechazar solicitud. |
| F8 | Calcular pago de horas extras. |
| F9 | Pagar una solicitud aprobada. |
| F10 | Convertir una solicitud aprobada en horas compensadas. |

### 5.3 Gestión de horas compensadas

| Código | Funcionalidad |
|--------|---------------|
| F11 | Registrar horas compensadas otorgadas al empleado. |
| F12 | Consultar saldo de horas compensadas. |
| F13 | Utilizar horas compensadas. |
| F14 | Listar horas compensadas. |

### 5.4 Reportes

| Código | Funcionalidad |
|--------|---------------|
| F15 | Reporte general. |
| F16 | Reporte de solicitudes pendientes. |
| F17 | Reporte de horas extras por empleado. |
| F18 | Reporte de saldos de horas compensadas. |

## 6. Reglas de negocio

| Regla | Descripción |
|-------|-------------|
| RN1 | El código de empleado es único. |
| RN2 | El documento de empleado es único. |
| RN3 | El salario mensual debe ser mayor a cero. |
| RN4 | Una solicitud de horas extras requiere fecha, cantidad de horas ( > 0 ) y motivo no vacío. |
| RN5 | Una solicitud pasa de `PENDIENTE` a `APROBADA` o `RECHAZADA`; una aprobada puede pasar a `PAGADA` o `COMPENSADA`. |
| RN6 | El valor hora se calcula como `salario_mensual / horas_mensuales` (por defecto 240). |
| RN7 | El pago de la hora extra se calcula como `valor_hora × factor_hora_extra` (factor configurable, por defecto 1.5). |
| RN8 | El pago total de una solicitud aprobada es `pago_hora × cantidad_horas`. |
| RN9 | El saldo de horas compensadas se incrementa cuando la empresa las otorga y se decrementa cuando el empleado las utiliza. |
| RN10 | No se pueden utilizar más horas compensadas que el saldo disponible. |
| RN11 | Toda entrada numérica debe validarse: no se aceptan números negativos ni cero donde la regla diga "mayor que cero". |
| RN12 | No se procesa ninguna operación si la entidad referenciada (empleado o solicitud) no existe. |
| RN13 | Solo un **supervisor registrado** puede aprobar o rechazar una solicitud; si quien lo intenta no es supervisor, la operación se rechaza. |

## 7. Arquitectura lógica

```
┌────────────────────────────┐
│  Capa de Presentación      │  main.py, MenuConsola
├────────────────────────────┤
│  Capa de Servicio          │  GestorHorasExtras (fachada con listas),
│                            │  CalculadoraHoras
├────────────────────────────┤
│  Capa de Modelo            │  Persona, Empleado, Supervisor,
│                            │  ResponsableRRHH, JornadaLaboral,
│                            │  RegistroHora, HoraExtra, HoraCompensada,
│                            │  Solicitud, SolicitudHoraExtra,
│                            │  SolicitudCompensacion, EstadoSolicitud
├────────────────────────────┤
│  Capa de Excepciones       │  Excepciones personalizadas
└────────────────────────────┘
```

## 8. Colecciones principales

| Colección | Tipo | Uso |
|-----------|------|-----|
| `list[Empleado]` | `list` | Repositorio en memoria de empleados. |
| `list[RegistroHora]` | `list` | Repositorio de movimientos (extras y compensadas). |
| `list[Solicitud]` | `list` | Repositorio de solicitudes. |
| Subconjunto de horas compensadas | Filtrado de `list[RegistroHora]` | Reportes y consulta de saldo (`listar_horas_compensadas`). |

## 9. Stack técnico

| Aspecto | Tecnología |
|---------|------------|
| Lenguaje | Python 3.10+ (probado con 3.14) |
| Ejecución | `python3 src/main.py` |
| Pruebas | `unittest` (biblioteca estándar), `python3 -m unittest` |
| Persistencia | En memoria (sin base de datos) |
| UML | PlantUML (`.puml`) e imágenes |
| Informe | Markdown y documento Word (`.docx`) |

## 10. Criterios de éxito

- El usuario puede registrar un empleado, registrar una solicitud, aprobarla y ver el cálculo de pago sin conocimientos técnicos.
- Las validaciones evitan que el sistema registre datos inválidos.
- Las horas compensadas mantienen un saldo consistente.
- El sistema no termina abruptamente cuando el usuario ingresa datos inválidos.
- Las 23 pruebas unitarias pasan.
