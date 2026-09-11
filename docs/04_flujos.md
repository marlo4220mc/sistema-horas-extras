# ETAPA 4 — Diseño de Flujos

Los diagramas se encuentran en formato PlantUML (`.puml`) en la carpeta `uml/`
y también como imagen en `salida/`.

| Flujo | PlantUML | Imagen |
|-------|----------|--------|
| Flujo general | `uml/flujo_aplicacion.puml` | `salida/flujo_aplicacion.png` |
| Registro de horas extras | `uml/flujo_registro_horas_extras.puml` | `salida/flujo_registro_horas_extras.png` |
| Aprobación / rechazo | `uml/flujo_aprobacion.puml` | `salida/flujo_aprobacion.png` |
| Horas compensadas | `uml/flujo_horas_compensadas.puml` | `salida/flujo_horas_compensadas.png` |

---

## A. Flujo general

```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓
SELECCIONAR OPCIÓN
  ↓
VALIDAR DATOS
  ↓
EJECUTAR OPERACIÓN
  ↓
MOSTRAR RESULTADO
  ↓
VOLVER AL MENÚ
  ↓
¿SALIR?
 ├── NO → MENÚ
 └── SÍ → FIN
```

El programa repite el ciclo hasta que el usuario elige la opción `0`. Si el
usuario ingresa datos inválidos, se muestra el mensaje de error y se vuelve al
menú (nunca se cierra la aplicación).

---

## B. Flujo de registro de empleado

```
INICIO
  ↓
Leer código, nombres, apellidos, documento, correo, salario, cargo, fecha
  ↓
¿Datos de texto no vacíos? ── NO ─→ Mensaje de error → FIN
  ↓ SÍ
¿Salario > 0? ── NO ─→ Mensaje de error → FIN
  ↓ SÍ
¿Código y documento únicos? ── NO ─→ EmpleadoDuplicadoError → FIN
  ↓ SÍ
Crear Empleado (saldo = 0) y agregarlo a List<Empleado>
  ↓
Mostrar confirmación
  ↓
FIN
```

Validaciones del flujo (clase `Persona` y `Empleado`):

- `nombres`, `apellidos`, `cargo`, `correo` no vacíos y con formato válido.
- `numeroDocumento` con al menos 6 caracteres.
- `salarioMensual > 0`.
- `fechaIngreso` no futura.
- Código de empleado y documento únicos (`EmpleadoDuplicadoError`).

---

## C. Flujo de registro de horas extras

```
INICIO
  ↓
Leer código de empleado
  ↓
Buscar en List<Empleado>
  ↓
¿Existe? ── NO ─→ EmpleadoNoEncontradoError → FIN
  ↓ SÍ
Leer fecha, horas y motivo
  ↓
¿0 < horas ≤ 24? ── NO ─→ HorasInvalidasError → FIN
  ↓ SÍ
Crear HoraExtra (id RH-XXX) con el factor de recargo configurado
  ↓
Crear SolicitudHoraExtra (id SOL-XXX) en estado PENDIENTE
  ↓
Agregar a List<RegistroHora> y List<Solicitud>
  ↓
Mostrar pago calculado
  ↓
FIN
```

---

## D. Flujo de aprobación

```
INICIO
  ↓
Leer id de solicitud (SOL-XXX)
  ↓
Buscar en List<Solicitud>
  ↓
¿Existe? ── NO ─→ SolicitudNoEncontradaError → FIN
  ↓ SÍ
¿Estado = PENDIENTE? ── NO ─→ EstadoSolicitudInvalidaError → FIN
  ↓ SÍ
¿APROBAR o RECHAZAR?
  ├── APROBAR  → estado = APROBADA
  └── RECHAZAR → leer motivo → estado = RECHAZADA
  ↓
Registrar usuario y fecha de resolución
  ↓
Mostrar confirmación
  ↓
FIN
```

Estados posibles: `PENDIENTE`, `APROBADA`, `RECHAZADA`, `PAGADA`, `COMPENSADA`.

Transiciones permitidas:

```
PENDIENTE ──→ APROBADA ──→ PAGADA
    │              └─────→ COMPENSADA
    └────────→ RECHAZADA
```

---

## E. Flujo de pago de horas extras

```
INICIO
  ↓
Leer id de solicitud
  ↓
Buscar solicitud y su HoraExtra
  ↓
valor_hora = salario_mensual / horas_mensuales
pago_hora  = valor_hora × factor_hora_extra (1.5 por defecto)
pago_total = pago_hora × cantidad_horas
  ↓
Mostrar valor hora, detalle y pago total
  ↓
Si el usuario confirma el pago:
  ¿Solicitud APROBADA? ── NO ─→ EstadoSolicitudInvalidaError → FIN
  ↓ SÍ
Estado = PAGADA · registrar usuario y fecha
  ↓
FIN
```

---

## F. Flujo de horas compensadas

```
INICIO
  ↓
Leer código de empleado, fecha, horas y motivo
  ↓
¿0 < horas ≤ 24? ── NO ─→ HorasInvalidasError → FIN
  ↓ SÍ
Crear HoraCompensada (esConsumo = false)
  ↓
saldo += horas   (Empleado.agregar_horas_compensadas)
  ↓
Agregar a List<RegistroHora>
  ↓
Mostrar nuevo saldo
  ↓
FIN
```

Además, una solicitud de horas extras **aprobada** puede convertirse en horas
compensadas con `compensar_solicitud_hora_extra(id, usuario)`: la solicitud pasa a
`COMPENSADA` y se suma su cantidad de horas al saldo del empleado.

---

## G. Flujo de utilización de horas compensadas

```
INICIO
  ↓
Leer código de empleado y horas a utilizar
  ↓
Buscar empleado y su saldo
  ↓
¿0 < horas ≤ 24? ── NO ─→ HorasInvalidasError → FIN
  ↓ SÍ
¿horas ≤ saldo? ── NO ─→ SaldoInsuficienteError (el saldo no cambia) → FIN
  ↓ SÍ
saldo -= horas   (Empleado.consumir_horas_compensadas)
  ↓
Crear HoraCompensada (esConsumo = true) y SolicitudCompensacion APROBADA
  ↓
Mostrar nuevo saldo
  ↓
FIN
```

Ejemplo verificable:

```
Empleado E001: saldo = 8 h
Utiliza       3 h
Nuevo saldo   5 h
Intenta usar  6 h  →  SaldoInsuficienteError (el saldo sigue en 5 h)
```
