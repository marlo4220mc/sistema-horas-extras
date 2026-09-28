# Sistema de Gestión y Control de Horas Extras y Horas Compensadas

Trabajo Parcial del curso **1FIS275 / 1FIS0275 – Fundamentos de Programación 2**
(Ingeniería de Sistemas EPE — ciclo 2026-25).

Aplicación de **consola en Python** que registra, controla, calcula y reporta
las horas extras y las horas compensadas del personal de una empresa.

---

## Descripción

El sistema administra en memoria tres listas principales: empleados, registros
de horas y solicitudes. Permite registrar empleados, registrar horas extras,
aprobarlas o rechazarlas, calcular el pago, otorgar y utilizar horas
compensadas controlando el saldo, consultar el historial y generar reportes.
Está construido con programación orientada a objetos y usa únicamente la
biblioteca estándar de Python.

## Problema

En la empresa Fábrica Marsar SRL el control de horas extras y compensadas
se hacía en papel y planillas sueltas: la información quedaba dispersa, había
errores de cálculo, no se conocía el saldo real de horas y no se podía
auditar lo pagado en el mes. El detalle está en `docs/01_problema_real.md`.

## Objetivo

Desarrollar una aplicación de consola en Python que permita registrar,
gestionar, controlar, consultar y calcular las horas extras y las horas
compensadas de los empleados, aplicando los conceptos de POO del curso.

## Funcionalidades

| # | Funcionalidad | Menú |
|---|---------------|------|
| 1 | Registrar empleado | 1 |
| 2 | Buscar empleado (código / documento / apellido) | 2 |
| 3 | Listar empleados | 3 |
| 4 | Registrar horas extras | 4 |
| 5 | Listar y consultar solicitudes | 5 |
| 6 | Aprobar solicitud | 6 |
| 7 | Rechazar solicitud | 7 |
| 8 | Calcular pago de horas extras | 8 |
| 9 | Registrar horas compensadas | 9 |
| 10 | Consultar saldo | 10 |
| 11 | Utilizar horas compensadas | 11 |
| 12 | Consultar historial | 12 |
| 13 | Reportes | 13 |
| 0 | Salir | 0 |

## POO utilizada

- **Encapsulamiento:** atributos privados por convención (`_nombre`) con
  propiedades (`@property`) y validación en los setters.
- **Herencia:**
  - `Persona` → `Empleado` → (`Supervisor`, `ResponsableRRHH`)
  - `RegistroHora` → (`HoraExtra`, `HoraCompensada`)
  - `Solicitud` → (`SolicitudHoraExtra`, `SolicitudCompensacion`)
- **Polimorfismo:**
  - `calcular_valor()` en `RegistroHora` (redefinido por `HoraExtra` y `HoraCompensada`).
  - `calcular_monto()` en `Solicitud` (redefinido por sus dos subclases).
  - `obtener_rol()` en `Persona` (redefinido por `Empleado`, `Supervisor` y `ResponsableRRHH`).
- **Clases abstractas:** `Persona`, `RegistroHora` y `Solicitud` usan `ABC` y
  `@abstractmethod`.
- **Colecciones:** `list[Empleado]`, `list[RegistroHora]` y `list[Solicitud]`.
- **Excepciones propias:** 6 excepciones de negocio controladas por el menú.

## Estructura

```
SistemaHorasExtras/
├── src/
│   ├── modelo/         (12 archivos: 11 clases + 1 enumeración)
│   ├── servicio/       (3 clases)
│   ├── excepciones/    (6 excepciones en un módulo)
│   └── main.py
├── test/               (test_sistema.py — unittest)
├── uml/                (diagramas .puml)
├── docs/               (documentación e informe)
├── salida/             (diagramas e imágenes y salidas de ejecución)
├── scripts/            (run.sh, test.sh)
├── README.md
└── REVISION_RUBRICA.md
```

## Requisitos

- **Python 3.10 o superior** (probado con Python 3.14).
- No requiere dependencias externas: solo la biblioteca estándar
  (`unittest`, `datetime`, `enum`, `decimal`, `abc`).

## Instalación

```bash
git clone https://github.com/marlo4220mc/sistema-horas-extras
cd sistema-horas-extras
```

## Ejecución

```bash
./scripts/run.sh                 # ejecuta el menú
# o directamente:
python3 src/main.py
```

Al iniciar, el sistema carga **datos de demostración** (empleados y movimientos
ficticios) para poder probar todas las opciones de inmediato.

## Pruebas

```bash
./scripts/test.sh
# o directamente:
python3 -m unittest discover -s test -p "test_*.py" -v
```

Resultado actual: **23 pruebas ejecutadas, 23 correctas, 0 fallidas**.
Ver `docs/07_pruebas.md`.

## UML

Los diagramas están en formato **draw.io** (editables en <https://app.diagrams.net>
o con la aplicación de escritorio):

- `drawio/diagrama_clases.drawio` — diagrama de clases (imagen: `salida/diagrama_clases.png`).
- `drawio/casos_uso.drawio` — casos de uso (`salida/casos_uso.png`).
- `drawio/flujo_aplicacion.drawio` — flujo general (`salida/flujo_aplicacion.png`).
- `drawio/flujo_registro_horas_extras.drawio` — registro de horas extras.
- `drawio/flujo_aprobacion.drawio` — aprobación o rechazo.
- `drawio/flujo_horas_compensadas.drawio` — uso de horas compensadas.

Las imágenes de `salida/` son exportaciones de esos archivos. Se incluye además la
versión PlantUML (`uml/*.puml`) de los mismos diagramas.

## Gestión del proyecto

El cronograma y la asignación de actividades se gestionan en un tablero de Trello:

- Tablero: <https://trello.com/b/VRlZeBkn/sistema-de-horas-extras-tp-fp2>
- 5 listas (una por fase) y 13 tarjetas con responsable, fechas y estado.

## Documentación

- `docs/00_requisitos_enunciado.md`
- `docs/01_problema_real.md`
- `docs/02_definicion_sistema.md`
- `docs/03_historias_usuario.md`
- `docs/04_flujos.md`
- `docs/05_diseno_clases.md`
- `docs/06_uml.md`
- `docs/07_pruebas.md`
- `docs/informe_final.md`
- `docs/Trabajo_Parcial_FP2.docx`

## Autores

- Marlon James Castro Castro
- Fatima Auris Aliaga
- Victor Hugo López Sobrado
- 
**Docente:** Chahuas Rebatta, César Eduardo

## Licencia

Trabajo académico. Uso educativo.
