# REVISIÓN FINAL CONTRA LA RÚBRICA

**Proyecto:** Sistema de Gestión y Control de Horas Extras y Horas Compensadas
**Curso:** 1FIS275 — Fundamentos de Programación 2 (ciclo 2026-25)
**Lenguaje:** Python 3
**Fecha de revisión:** 27/09/2026

---

## 1. Matriz de cumplimiento

| Requisito | Cumplido | Evidencia | Archivo |
|-----------|----------|-----------|---------|
| Problema real de una empresa | Sí | Situación, causas y consecuencias documentadas | `docs/01_problema_real.md` |
| Solución orientada a objetos | Sí | 14 clases principales con encapsulamiento, herencia y polimorfismo | `src/` |
| Entre 10 y 15 clases | Sí | 14 clases principales (11 modelo + 3 servicio) | `docs/05_diseno_clases.md` |
| Colecciones tipo lista | Sí | `list[Empleado]`, `list[RegistroHora]`, `list[Solicitud]` | `src/servicio/gestor_horas_extras.py` |
| Funcionalidad de registro | Sí | `registrar_empleado`, `registrar_solicitud_hora_extra`, `registrar_horas_compensadas` | `src/servicio/gestor_horas_extras.py` |
| Funcionalidad de búsqueda | Sí | `buscar_empleado_por_codigo/documento/apellido`, `buscar_solicitud` | `src/servicio/gestor_horas_extras.py` |
| Funcionalidad de listado | Sí | `listar_empleados`, `listar_solicitudes`, `listar_horas_extras`, `listar_horas_compensadas` | `src/servicio/gestor_horas_extras.py` |
| Funcionalidades de control | Sí | Aprobar, rechazar, pagar, compensar, control de saldo | `src/modelo/solicitud.py`, `src/modelo/empleado.py` |
| Cálculos específicos | Sí | `valor_hora`, `pago_horas_extras`, `valor_horas_compensadas`, totales | `src/servicio/calculadora_horas.py` |
| Menú de ejecución | Sí | Menú de 13 opciones + salir y submenú de reportes | `src/servicio/menu_consola.py` |
| Diagrama de clases UML | Sí | `.drawio` editable + imagen exportada | `drawio/diagrama_clases.drawio`, `salida/diagrama_clases.png` |
| Relaciones entre clases | Sí | Herencia, composición, agregación, asociación y dependencia | `docs/06_uml.md` |
| Herencia | Sí | 3 jerarquías reales | `docs/05_diseno_clases.md` |
| Polimorfismo | Sí | `calcular_valor()`, `calcular_monto()`, `obtener_rol()` | `src/modelo/`, `docs/06_uml.md` |
| Encapsulamiento | Sí | Atributos `_privados` + `@property` con validación | `src/modelo/*.py` |
| Pruebas de métodos de negocio | Sí | 23 pruebas con `unittest`, 23 correctas | `test/test_sistema.py`, `salida/pruebas_unittest.txt` |
| Control de excepciones | Sí | 7 excepciones propias + `ValueError` | `src/excepciones/excepciones.py` |
| Validaciones | Sí | Texto, números, salario, horas, duplicados, saldo, estados, fechas | `docs/05_diseno_clases.md` §7 |
| Informe con la estructura oficial | Sí | Carátula (con logo UPC), índice, introducción, capítulos, bibliografía, anexos; encabezado, numeración de páginas y figuras numeradas | `docs/informe_final.md`, `docs/Trabajo_Parcial_FP2.docx` |
| Bibliografía en formato APA | Sí | 8 fuentes reales en APA 7 | `docs/informe_final.md` §F |
| Anexos preparados | Sí | Anexos 1 a 8 con placeholders | `docs/informe_final.md` §G |
| Cronograma y asignación | Sí | Tabla de 13 actividades con responsables | `docs/informe_final.md` §2.4 |
| Evidencias del trabajo en equipo | Preparado | Placeholders `[INSERTAR CAPTURA]` | `docs/informe_final.md` §G |
| URL de Git | Sí | Repositorio privado con 17 commits por etapas | https://github.com/marlo4220mc/sistema-horas-extras |
| URL de Trello | Sí | Tablero con 5 listas y 13 tarjetas (responsable, fechas y estado) | https://trello.com/b/VRlZeBkn/sistema-de-horas-extras-tp-fp2 |

---

## 2. Lista de verificación (checklist)

- [x] Problema real
- [x] Solución orientada a objetos
- [x] 10–15 clases (14 clases principales)
- [x] Colecciones (`list`)
- [x] Registro
- [x] Búsqueda
- [x] Listado
- [x] Cálculos
- [x] Menú
- [x] UML
- [x] Relaciones entre clases
- [x] Herencia
- [x] Polimorfismo
- [x] Encapsulamiento
- [x] Pruebas (ejecutadas con `unittest`)
- [x] Excepciones
- [x] Validaciones
- [x] Informe
- [x] APA
- [x] Anexos
- [x] Evidencias (placeholders listos)
- [x] Git / Trello (repositorio y tablero listos)

---

## 3. Consideraciones mínimas del enunciado oficial

| # | Consideración del enunciado | Cumplido | Evidencia |
|---|------------------------------|----------|-----------|
| 1 | Menú de ejecución de las opciones | Sí | `MenuConsola` — 13 opciones + 0 |
| 2 | Funcionalidades de control y cálculos | Sí | Aprobación, saldo, `CalculadoraHoras` |
| 3 | Diagrama de clases UML | Sí | `drawio/diagrama_clases.drawio` |
| 4 | POO: clase, relaciones, herencia, polimorfismo | Sí | `docs/05_diseno_clases.md` |
| 5 | Pruebas de métodos de negocio | Sí | `unittest` — 23/23 |
| 6 | Control de excepciones de los datos | Sí | `src/excepciones/` + `try/except` en el menú |

---

## 4. Verificación de ejecución real

| Verificación | Comando | Resultado |
|--------------|---------|-----------|
| Pruebas unitarias | `./scripts/test.sh` | `Ran 23 tests`, `OK` (0 fallos) |
| Ejecución del menú | `python3 src/main.py` | Ejecución completa sin cierres inesperados — `salida/ejecucion_menu.txt` |
| Robustez ante errores | Entradas inválidas en el menú | Se muestran mensajes de error y el programa continúa |

---

## 5. Verificación de consistencia cruzada

```
PROBLEMA        → docs/01_problema_real.md
   ↓
OBJETIVO        → docs/02_definicion_sistema.md  (OE1..OE8)
   ↓
HISTORIAS       → docs/03_historias_usuario.md   (HU01..HU13)
   ↓
FUNCIONALIDADES → menú de 13 opciones
   ↓
CLASES          → 14 clases principales
   ↓
CÓDIGO          → src/ (módulos .py)
   ↓
UML             → drawio/diagrama_clases.drawio (coincide con el código)
   ↓
INFORME         → docs/informe_final.md + docs/Trabajo_Parcial_FP2.docx
```

**Resultado de la revisión cruzada:** cada historia de usuario tiene una opción
de menú, cada opción de menú existe en el código, y cada clase del UML existe
en `src/`. No se detectaron funcionalidades documentadas que no existan en el
programa, ni clases en el UML que no estén implementadas.

Detalle de la trazabilidad:

| HU | Opción de menú | Método | Prueba |
|----|----------------|--------|--------|
| HU01 | 1 | `registrar_empleado` | #1, #2, #19 |
| HU02 | 2 | `buscar_empleado_*` | #3, #4 |
| HU03 | 3 | `listar_empleados` | #1 |
| HU04 | 4 | `registrar_solicitud_hora_extra` | #5, #6 |
| HU05 | 5 | `listar_solicitudes` / `buscar_solicitud` | #12 |
| HU06 | 6 | `aprobar_solicitud` | #9, #10 |
| HU07 | 7 | `rechazar_solicitud` | #11 |
| HU08 | 8 | `CalculadoraHoras` / `calcular_monto` | #7, #8 |
| HU09 | 9 | `registrar_horas_compensadas` | #13 |
| HU10 | 10 | `consultar_saldo` | #13 |
| HU11 | 11 | `utilizar_horas_compensadas` | #14, #15 |
| HU12 | 12 | `historial_por_empleado` | (uso en menú) |
| HU13 | 13 | reportes | #20 |

---

## 6. Pendientes que dependen de información del grupo

Estos puntos **no pueden completarse sin datos reales del equipo** y quedaron
con placeholders. No se inventó información:

| Pendiente | Dónde | Qué falta |
|-----------|-------|-----------|
| Capturas del sistema y de las pruebas | Anexos 2, 3, 4 y 7 | Faltan esas capturas de pantalla |
| Nombre del archivo de entrega | — | `GRUPO_XX_TP_FP2_Ciclo` (definido por el grupo) |

> El Anexo 1 ya tiene las 8 capturas de coordinación (Drive y WhatsApp).
> El índice quedó escrito en texto plano con los números de página (17 en total),
> sin campos que haya que actualizar.
>
> Los integrantes (3), el docente y la empresa (**Fábrica Marsar SRL**) ya están
> completados en la carátula, el informe y el código.
>
> El nombre de la universidad (**UPC**) y su logo se tomaron del enunciado
> oficial `docs/enunciado_oficial.docx` (logo con descripción "upc logo" y
> propiedad `Company = UPC`), por lo que ya no son un placeholder.
