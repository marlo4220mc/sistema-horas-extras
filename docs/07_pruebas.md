# ETAPA 8 — Pruebas

**Framework:** `unittest` (biblioteca estándar de Python, sin dependencias externas)
**Archivo de pruebas:** `test/test_sistema.py`
**Comando:** `./scripts/test.sh` (o `python3 -m unittest discover -s test -v`)
**Salida completa:** `salida/pruebas_unittest.txt`
**Fecha de ejecución:** 27/09/2026

## Resultado real de la ejecución

```
----------------------------------------------------------------------
Ran 23 tests in 0.001s

OK
```

**23 pruebas ejecutadas, 23 correctas, 0 fallidas.**

---

## Detalle de las pruebas

| # | Prueba | Objetivo | Entrada | Resultado esperado | Resultado obtenido | Estado |
|---|--------|----------|---------|--------------------|--------------------|--------|
| 1 | `test_hu01_registrar_empleado_correctamente` | Verificar el alta de un empleado | E001 Juan Pérez, DNI 10000001, S/ 3000, jornada 8×30 | Empleado creado, saldo 0, 2 empleados | Apellido "Perez", rol "Empleado", saldo 0.00, 2 empleados | OK |
| 2 | `test_validacion_empleado_duplicado` | Impedir códigos y documentos repetidos (aviso temprano) | Código "E001" y documento "10000001" repetidos | `EmpleadoDuplicadoError`; `existe_empleado_con_codigo/documento` = True | Excepciones lanzadas y consultas previas correctas | OK |
| 3 | `test_hu02_buscar_empleado_por_codigo` | Búsqueda por código sin distinguir mayúsculas | Código "e002" | Nombre "Maria Lopez" | "Maria Lopez" | OK |
| 4 | `test_hu02_buscar_empleado_inexistente` | Controlar la ausencia | Código "E999" | `EmpleadoNoEncontradoError` | Excepción lanzada | OK |
| 5 | `test_hu04_registrar_horas_extras` | Crear solicitud de 6 h | E001, 10/09/2026, 6 h | Estado `PENDIENTE`, 6.00 h | `PENDIENTE`, 6.00 h | OK |
| 6 | `test_validacion_horas_invalidas` | Rechazar 0 y −3 horas | 0 h y −3 h | `HorasInvalidasError` (2 casos) | Excepción en ambos casos | OK |
| 7 | `test_hu08_calcular_valor_hora` | `3000 / 240` | E001, salario 3000 | 12.50 | 12.50 | OK |
| 8 | `test_hu08_calcular_pago_horas_extras` | `12.50 × 1.5 × 6` | E001, 6 h | 112.50 | 112.50 (calculadora y solicitud) | OK |
| 9 | `test_hu06_aprobar_solicitud` | Pasar de PENDIENTE a APROBADA (aprueba un supervisor) | SOL-001, supervisor E009 | `APROBADA`, resuelto por E009, total a pagar 112.50 | `APROBADA`, E009, S/ 112.50 | OK |
| 10 | `test_validacion_aprobar_dos_veces` | No aprobar dos veces | Misma solicitud | `EstadoSolicitudInvalidaError` | Excepción lanzada | OK |
| 11 | `test_hu07_rechazar_solicitud` | Pasar de PENDIENTE a RECHAZADA | Motivo obligatorio | `RECHAZADA`, observación guardada, total a pagar 0 | `RECHAZADA`, observación correcta, S/ 0.00 | OK |
| 12 | `test_hu05_solicitud_inexistente` | Controlar la ausencia | "SOL-999" | `SolicitudNoEncontradaError` | Excepción lanzada | OK |
| 13 | `test_hu09_hu10_registrar_horas_compensadas_y_saldo` | Sumar al saldo | E001, 8 h otorgadas | Saldo 8.00 h | 8.00 h | OK |
| 14 | `test_hu11_utilizar_horas_compensadas` | Descontar del saldo | Saldo 8 h, usa 3 h | Saldo 5.00 h, solicitud APROBADA | 5.00 h, `APROBADA`, 3.00 h usadas | OK |
| 15 | `test_validacion_saldo_insuficiente` | Rechazar el exceso | Saldo 8 h, usa 9 h | `SaldoInsuficienteError` y saldo intacto | Excepción lanzada, saldo 8.00 h | OK |
| 16 | `test_polimorfismo_calcular_valor` | Misma referencia padre, distinto cálculo | `list[RegistroHora]` con 2 h extra y 2 h compensadas | 37.50 y 25.00 | 37.50 y 25.00 | OK |
| 17 | `test_polimorfismo_obtener_rol` | Rol distinto por subclase | Supervisor con límite 10 h | "Supervisor", puede 8 h, no puede 12 h | Coincide | OK |
| 18 | `test_polimorfismo_calcular_monto` | Monto distinto por tipo de solicitud | 4 h extras y 2 h compensadas | 75.00 y 25.00 | 75.00 y 25.00 | OK |
| 19 | `test_validacion_datos_empleado` | Salario negativo y nombre vacío | −100 y "   " | `ValueError` (2 casos) | Excepción en ambos casos | OK |
| 20 | `test_flujo_pagar_y_compensar` | Cambio de estados y efecto en el saldo | Solicitud aprobada | `PAGADA`, total pagado 112.50; otra `COMPENSADA` con saldo 4.00 h | Coincide | OK |
| 21 | `test_validacion_fecha_futura` | Rechazar fechas futuras en los registros de horas | Fecha de mañana para horas extras y para compensadas | `ValueError`; la fecha de hoy sí es válida | Excepción en ambos casos; hoy aceptado | OK |
| 22 | `test_validacion_aprobador_no_supervisor` | Solo un supervisor puede aprobar o rechazar | Aprobar con E001 y rechazar con E002 (empleados) | `AprobacionNoAutorizadaError`; la solicitud sigue PENDIENTE | Excepción en ambos casos; estado PENDIENTE | OK |
| 23 | `test_validacion_aprobador_inexistente` | Controlar un aprobador inexistente | Aprobar con código "E999" | `EmpleadoNoEncontradoError` | Excepción lanzada | OK |

---

## Cómo ejecutar las pruebas

```bash
cd SistemaHorasExtras
./scripts/test.sh
```

También se pueden ejecutar de forma directa:

```bash
python3 test/test_sistema.py
```

Salida esperada (resumen):

```
Ran 23 tests in 0.001s

OK
```

---

## Nota sobre la veracidad

Los resultados de la tabla se copiaron de la ejecución real registrada en
`salida/pruebas_unittest.txt`. No se han inventado resultados: las 23 pruebas
se ejecutaron con `unittest` sobre el código incluido en el proyecto.
