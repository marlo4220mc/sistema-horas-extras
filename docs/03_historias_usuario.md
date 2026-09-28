# ETAPA 3 — Historias de Usuario

**Proyecto:** Sistema de Gestión y Control de Horas Extras y Horas Compensadas
**Empresa:** Fábrica Marsar SRL
**Curso:** 1FIS275 — Fundamentos de Programación 2

Las historias de usuario se redactaron en el formato *Como &lt;rol&gt;, quiero
&lt;acción&gt;, para &lt;beneficio&gt;*. Cada historia corresponde a una
funcionalidad que **existe realmente** en el programa y se puede ubicar en el
menú de consola.

---

## HU01 — Registrar empleado

**Prioridad:** Alta

Como responsable de RR. HH.,
quiero registrar un empleado,
para mantener actualizada la información del personal.

**Criterios de aceptación**

- El código de empleado y el número de documento deben ser únicos.
- Si el código o el documento ya existen, el sistema lo avisa **apenas se
  ingresa el dato**, sin pedir el resto del formulario.
- No se aceptan nombres vacíos, salario menor o igual a cero ni correo inválido.
- Al registrar, el saldo de horas compensadas inicia en 0.

**Implementación:** `GestorHorasExtras.registrar_empleado(...)` · Menú opción 1

---

## HU02 — Buscar empleado

**Prioridad:** Media

Como responsable de RR. HH.,
quiero buscar un empleado por código, documento o apellido,
para atender consultas sin revisar toda la lista.

**Criterios de aceptación**

- Si el empleado no existe, se informa el problema sin cerrar el programa.
- La búsqueda por apellido puede devolver más de un resultado.

**Implementación:** `buscar_empleado_por_codigo`, `buscar_empleado_por_documento`,
`buscar_empleados_por_apellido` · Menú opción 2

---

## HU03 — Listar empleados

**Prioridad:** Media

Como responsable de RR. HH.,
quiero ver la lista completa de empleados,
para revisar el personal registrado y su saldo de horas.

**Implementación:** `GestorHorasExtras.listar_empleados()` · Menú opción 3

---

## HU04 — Registrar horas extras

**Prioridad:** Alta

Como empleado,
quiero registrar las horas que trabajé fuera de mi jornada,
para que la empresa evalúe su reconocimiento.

**Criterios de aceptación**

- Se registra fecha, cantidad de horas y motivo.
- La cantidad de horas debe ser mayor a 0 y como máximo 24.
- El empleado debe existir en el sistema.
- La fecha en que se trabajó no puede ser futura.
- La solicitud queda en estado `PENDIENTE`.

**Implementación:** `registrar_solicitud_hora_extra(...)` · Menú opción 4

---

## HU05 — Consultar solicitudes

**Prioridad:** Alta

Como responsable de RR. HH.,
quiero consultar las solicitudes registradas y su estado,
para saber cuáles están pendientes y cuáles ya fueron procesadas.

**Implementación:** `listar_solicitudes()`, `buscar_solicitud(id)`,
`listar_solicitudes_pendientes()` · Menú opción 5

---

## HU06 — Aprobar horas extras

**Prioridad:** Alta

Como supervisor,
quiero aprobar una solicitud de horas extras,
para que el pago o la compensación puedan continuar.

**Criterios de aceptación**

- Solo se pueden aprobar solicitudes en estado `PENDIENTE`.
- Una solicitud ya procesada no se puede aprobar otra vez.
- Solo un **supervisor registrado** puede aprobar: el sistema valida el código de quien aprueba.

**Implementación:** `aprobar_solicitud(id, codigo_aprobador)` · Menú opción 6

---

## HU07 — Rechazar horas extras

**Prioridad:** Alta

Como supervisor,
quiero rechazar una solicitud de horas extras indicando el motivo,
para dejar constancia de por qué no se reconoce.

**Criterios de aceptación**

- El motivo es obligatorio.
- Solo se rechazan solicitudes en estado `PENDIENTE`.
- Solo un **supervisor registrado** puede rechazar.

**Implementación:** `rechazar_solicitud(id, motivo, codigo_aprobador)` · Menú opción 7

---

## HU08 — Calcular pago de horas extras

**Prioridad:** Alta

Como responsable de RR. HH.,
quiero que el sistema calcule el pago de las horas extras,
para evitar errores de cálculo manual.

**Regla usada (configurable en el proyecto académico)**

```
valor_hora       = salario_mensual / horas_mensuales
valor_hora_extra = valor_hora × factor_hora_extra   (por defecto 1.5)
pago_total       = valor_hora_extra × cantidad_horas
```

> El factor 1.5 **no** proviene de una norma legal: es una regla configurada
> para este trabajo y se puede cambiar con `CalculadoraHoras.factor_hora_extra`.

**Implementación:** `CalculadoraHoras` y `SolicitudHoraExtra.calcular_monto()` ·
Menú opción 8

---

## HU09 — Registrar horas compensadas

**Prioridad:** Alta

Como responsable de RR. HH.,
quiero registrar las horas compensadas que se otorgan a un empleado,
para que pueda utilizarlas después.

**Criterios de aceptación**

- Las horas otorgadas se suman al saldo del empleado.
- No se aceptan cantidades menores o iguales a cero.

**Implementación:** `registrar_horas_compensadas(...)` · Menú opción 9

---

## HU10 — Consultar saldo

**Prioridad:** Alta

Como empleado,
quiero consultar mi saldo de horas compensadas,
para saber cuántas horas puedo utilizar.

**Implementación:** `consultar_saldo(codigo)` · Menú opción 10

---

## HU11 — Utilizar horas compensadas

**Prioridad:** Alta

Como empleado,
quiero utilizar horas de mi saldo,
para atender mis asuntos personales sin afectar mi remuneración.

**Criterios de aceptación**

- No se pueden utilizar más horas que el saldo disponible.
- Si el saldo es insuficiente, el saldo no cambia y se informa el error.

**Implementación:** `utilizar_horas_compensadas(...)` · Menú opción 11

---

## HU12 — Consultar historial

**Prioridad:** Media

Como responsable de RR. HH.,
quiero ver el historial de movimientos y solicitudes de un empleado,
para revisar su situación completa en un solo listado.

**Implementación:** `historial_por_empleado(codigo)` y `solicitudes_por_empleado(codigo)` ·
Menú opción 12

---

## HU13 — Generar reportes

**Prioridad:** Media

Como responsable de RR. HH.,
quiero obtener reportes de horas extras, montos y saldos,
para sustentar el pago y la auditoría interna.

**Reportes incluidos**

1. Reporte general.
2. Horas extras por empleado.
3. Horas extras (registros).
4. Horas compensadas (registros).
5. Saldo de horas compensadas.
6. Solicitudes pendientes.
7. Total a pagar / pagado.
8. Lista de empleados.

**Implementación:** `reporte_general()`, `reporte_horas_extras_por_empleado()`,
`reporte_saldos_compensadas()`, `total_a_pagar()`, `total_pagado()` · Menú opción 13

---

## Resumen y trazabilidad

| ID | Historia | Prioridad | Método principal | Opción de menú |
|----|----------|-----------|------------------|----------------|
| HU01 | Registrar empleado | Alta | `registrar_empleado` | 1 |
| HU02 | Buscar empleado | Media | `buscar_empleado_por_codigo` / `_por_documento` / `_por_apellido` | 2 |
| HU03 | Listar empleados | Media | `listar_empleados` | 3 |
| HU04 | Registrar horas extras | Alta | `registrar_solicitud_hora_extra` | 4 |
| HU05 | Consultar solicitudes | Alta | `listar_solicitudes` | 5 |
| HU06 | Aprobar horas extras | Alta | `aprobar_solicitud` | 6 |
| HU07 | Rechazar horas extras | Alta | `rechazar_solicitud` | 7 |
| HU08 | Calcular pago | Alta | `CalculadoraHoras` / `calcular_monto` | 8 |
| HU09 | Registrar horas compensadas | Alta | `registrar_horas_compensadas` | 9 |
| HU10 | Consultar saldo | Alta | `consultar_saldo` | 10 |
| HU11 | Utilizar horas compensadas | Alta | `utilizar_horas_compensadas` | 11 |
| HU12 | Consultar historial | Media | `historial_por_empleado` | 12 |
| HU13 | Generar reportes | Media | `reporte_general` y otros | 13 |
