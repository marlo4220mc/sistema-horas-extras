# Sistema de Gestión y Control de Horas Extras y Horas Compensadas

**Trabajo Parcial — Fundamentos de Programación 2**

---

# A. CARÁTULA / MIEMBROS DEL GRUPO

<br>

<div align="center">

![Logo UPC](img/logo_upc.png)

**Universidad Peruana de Ciencias Aplicadas (UPC)**

Ingeniería de Sistemas EPE

<br><br>

**Curso:**
1FIS275 — Fundamentos de Programación 2

**Trabajo Parcial**

<br>

**"Sistema de Gestión y Control de Horas Extras y Horas Compensadas"**

<br><br>

**Integrantes:**

Marlon James Castro Castro
Fatima Auris Aliaga
Victor Hugo López Sobrado


<br>

**Docente:**
Chahuas Rebatta, César Eduardo

**Ciclo:**
2026-25

</div>

<br><br>

---

# B. ÍNDICE

1. Introducción … 3
2. Capítulo 1: Situación Actual … 4
   - 2.1 Análisis del Problema … 4
   - 2.2 Objetivo del Sistema … 5
   - 2.3 Lista de Funcionalidades / Historias de Usuario, priorizadas … 5
   - 2.4 Cronograma y Asignación de Actividades … 5
3. Capítulo 2: Propuesta de Innovación … 7
   - 3.1 Diseño de Flujo de Aplicación … 7
   - 3.2 Diagrama de Clases del Modelo … 13
4. Conclusiones … 15
5. Recomendaciones … 15
6. Objetivo del Estudiante (Student Outcome) … 16
7. Bibliografía … 16
8. Anexos … 17

---

# C. INTRODUCCIÓN

El presente trabajo se desarrolla en el marco del curso Fundamentos de
Programación 2 de Ingeniería de Sistemas EPE y tiene como finalidad aplicar
los principios de la programación orientada a objetos para plantear una
solución a un problema real identificado en un proceso de negocio de una
empresa.

El problema seleccionado corresponde al proceso de gestión y control de horas
extras y horas compensadas. Actualmente, el registro de estas horas se realiza
mediante cuadernos y archivos Excel, generando duplicidad de información
debido a que los datos registrados por los trabajadores deben ser
posteriormente trasladados a un medio digital. Esta situación puede ocasionar
errores en el registro, dificultades para realizar el seguimiento de las
solicitudes y demoras en su revisión, aprobación y posterior procesamiento.

Ante esta situación, se propone desarrollar un Sistema de Gestión y Control de
Horas Extras y Horas Compensadas, como una aplicación de consola desarrollada
en Python. El sistema permitirá registrar trabajadores y sus horas, gestionar
la aprobación o rechazo por parte del responsable del área, controlar el saldo
de horas compensadas, realizar los cálculos correspondientes y consultar el
historial de registros.

La solución será desarrollada aplicando conceptos de programación orientada a
objetos, tales como clases, objetos, encapsulamiento, herencia y polimorfismo,
además del uso de colecciones, manejo de excepciones y pruebas de los métodos
de negocio. El sistema tendrá un alcance académico y trabajará con información
almacenada en memoria, sin integración con una base de datos o sistemas
externos.

---

# D. CAPÍTULO 1: SITUACIÓN ACTUAL

## 2.1 Análisis del Problema

### Situación actual

Actualmente, el proceso de gestión de horas extras y horas compensadas se
realiza mediante el registro de información en cuadernos y archivos Excel. El
trabajador registra las horas realizadas en un cuaderno y posteriormente esta
información es trasladada a un archivo Excel para su control.

Una vez registrada la información, el responsable del área revisa las horas
reportadas y determina su aprobación o rechazo. En el caso de las horas extras
aprobadas, posteriormente se realiza el cálculo correspondiente para su
procesamiento. Por otro lado, las horas compensadas requieren llevar un
control del saldo disponible de cada trabajador y de las horas utilizadas.

Este proceso implica el manejo de información en diferentes medios y el
traslado manual de datos, lo que puede generar errores de registro, duplicidad
de información, dificultades para consultar el estado de las solicitudes y
falta de un control centralizado del saldo de horas compensadas.

### Problema

La empresa no cuenta con una herramienta única que permita registrar,
controlar, aprobar y calcular de manera uniforme las horas extras ni las horas
compensadas de sus empleados.

### Causas

| # | Causa |
|---|-------|
| C1 | El registro se hace en papel y se centraliza a fin de mes. |
| C2 | No existe un repositorio común entre el área usuaria y Recursos Humanos. |
| C3 | Los cálculos del valor hora y del pago se hacen de forma manual. |
| C4 | El control de horas compensadas es un cuaderno físico. |
| C5 | Las solicitudes no tienen un estado formal (pendiente, aprobada, rechazada). |

### Consecuencias

| # | Consecuencia |
|---|--------------|
| CO1 | Errores frecuentes al transcribir los formularios a la planilla. |
| CO2 | Retrasos en el pago de las horas extras. |
| CO3 | Conflictos entre el empleado y la empresa por horas no reconocidas. |
| CO4 | Saldo de horas compensadas desactualizado o inexistente. |
| CO5 | Imposibilidad de auditar cuántas horas extras se han pagado en el mes. |

### Necesidad

Se requiere una aplicación de consola en Python que centralice el registro, la
aprobación, el cálculo y el reporte de las horas extras y compensadas, y que
mantenga un saldo confiable por empleado.

## 2.2 Objetivo del Sistema

### Objetivo general

Desarrollar una aplicación de consola en Python que permita gestionar y
controlar las horas extras y horas compensadas de los empleados de Fábrica
Marsar SRL, mediante el registro de horas, la revisión y aprobación por parte
del responsable del área, el cálculo de las horas extras y el control del
saldo de horas compensadas.

### Objetivos específicos

| # | Objetivo específico |
|---|---------------------|
| OE1 | Registrar y mantener actualizados los datos de los empleados. |
| OE2 | Registrar solicitudes de horas extras con fecha, cantidad de horas y motivo. |
| OE3 | Permitir al responsable del área revisar, aprobar o rechazar los registros de horas extras. |
| OE4 | Calcular el valor correspondiente a las horas extras aprobadas de acuerdo con las reglas definidas para el sistema. |
| OE5 | Registrar las horas compensadas y mantener actualizado el saldo disponible de cada empleado. |
| OE6 | Permitir la utilización de horas compensadas, validando que el empleado cuente con saldo suficiente. |
| OE7 | Permitir la consulta de empleados, solicitudes, estados, historial y saldos de horas. |
| OE8 | Validar los datos ingresados y controlar las situaciones no válidas mediante el manejo de excepciones. |

## 2.3 Lista de Funcionalidades / Historias de Usuario, priorizadas

| ID | Historia de Usuario | Prioridad |
|----|---------------------|-----------|
| HU01 | Registrar empleado | Alta |
| HU02 | Buscar empleado | Media |
| HU03 | Listar empleados | Media |
| HU04 | Registrar horas extras | Alta |
| HU05 | Consultar solicitudes | Alta |
| HU06 | Aprobar solicitud de horas extras | Alta |
| HU07 | Rechazar solicitud de horas extras | Alta |
| HU08 | Calcular pago de horas extras aprobadas | Alta |
| HU09 | Registrar horas compensadas | Alta |
| HU10 | Consultar saldo de horas compensadas | Alta |
| HU11 | Utilizar horas compensadas | Alta |
| HU12 | Consultar historial | Media |
| HU13 | Generar reportes | Media |

Las prioridades se asignaron según el aporte al proceso principal: son *Alta*
las historias sin las cuales no funciona el ciclo de horas extras (registro,
aprobación o rechazo, cálculo del pago y uso de las horas compensadas), y
*Media* las que dan soporte de consulta y reporte. Cada historia se redactó en
el formato *como &lt;rol&gt;, quiero &lt;acción&gt;, para &lt;beneficio&gt;*:

- **HU01 — Registrar empleado** (Alta): como responsable de RR. HH., quiero
  registrar un empleado con su código, documento, cargo y salario, para
  mantener actualizada la información del personal; valida los datos y evita
  códigos o documentos duplicados.
- **HU02 — Buscar empleado** (Media): como responsable de RR. HH., quiero
  buscar un empleado por código, documento o apellido, para atender consultas
  sin revisar toda la lista; si no existe, se informa sin cerrar el programa.
- **HU03 — Listar empleados** (Media): como responsable de RR. HH., quiero ver
  la lista completa del personal con su cargo y su saldo de horas, para
  revisar el personal registrado.
- **HU04 — Registrar horas extras** (Alta): como empleado, quiero registrar
  las horas trabajadas fuera de mi jornada (fecha, cantidad y motivo), para que
  la empresa evalúe su reconocimiento; valida los rangos, impide fechas
  futuras y deja la solicitud en estado PENDIENTE.
- **HU05 — Consultar solicitudes** (Alta): como responsable de RR. HH., quiero
  consultar las solicitudes y su estado, para saber cuáles están pendientes y
  cuáles ya fueron procesadas.
- **HU06 — Aprobar horas extras** (Alta): como supervisor, quiero aprobar una
  solicitud pendiente, para que el pago o la compensación puedan continuar;
  solo un supervisor registrado puede hacerlo.
- **HU07 — Rechazar horas extras** (Alta): como supervisor, quiero rechazar
  una solicitud indicando el motivo, para dejar constancia de por qué no se
  reconoce.
- **HU08 — Calcular pago de horas extras** (Alta): como responsable de RR.
  HH., quiero que el sistema calcule el pago (valor de la hora, recargo y
  total), para evitar errores de cálculo manual.
- **HU09 — Registrar horas compensadas** (Alta): como responsable de RR. HH.,
  quiero otorgar horas compensadas al saldo del empleado, para que pueda
  utilizarlas después.
- **HU10 — Consultar saldo** (Alta): como empleado, quiero consultar cuántas
  horas compensadas tengo disponibles, para saber cuánto puedo utilizar.
- **HU11 — Utilizar horas compensadas** (Alta): como empleado, quiero utilizar
  horas de mi saldo para asuntos personales, sin afectar mi remuneración; no
  permite gastar más de lo disponible.
- **HU12 — Consultar historial** (Media): como responsable de RR. HH., quiero
  ver los movimientos y solicitudes de un empleado en un solo listado, para
  revisar su situación completa.
- **HU13 — Generar reportes** (Media): como responsable de RR. HH., quiero
  obtener reportes de horas, montos y saldos, para sustentar el pago y la
  auditoría interna.

El detalle completo de cada historia (criterios de aceptación y método del
programa que la implementa) está en `docs/03_historias_usuario.md`.

## 2.4 Cronograma y Asignación de Actividades

El trabajo se organizó por semanas del ciclo 2026-25. La evaluación del trabajo
parcial corresponde a la semana 4. Las actividades se distribuyeron entre los
tres integrantes.

| # | Actividad | Responsable | Inicio | Fin | Estado |
|---|-----------|-------------|--------|-----|--------|
| 1 | Análisis del enunciado y de los requisitos | Integrante 1 | 31/08/2026 | 02/09/2026 | Completado |
| 2 | Definición del problema real y del objetivo | Integrante 2 | 02/09/2026 | 04/09/2026 | Completado |
| 3 | Historias de usuario y priorización | Integrante 3 | 04/09/2026 | 07/09/2026 | Completado |
| 4 | Diseño de flujos de la aplicación | Integrante 2 | 07/09/2026 | 10/09/2026 | Completado |
| 5 | Diseño de clases, herencia y polimorfismo | Integrante 1 | 08/09/2026 | 12/09/2026 | Completado |
| 6 | Diagrama de clases UML | Integrante 3 | 12/09/2026 | 15/09/2026 | Completado |
| 7 | Implementación de las clases del modelo | Integrante 3 | 12/09/2026 | 18/09/2026 | Completado |
| 8 | Implementación de cálculos, excepciones y menú | Integrante 1 | 15/09/2026 | 21/09/2026 | Completado |
| 9 | Pruebas unitarias con unittest | Integrante 2 | 18/09/2026 | 22/09/2026 | Completado |
| 10 | Corrección de errores y reejecución de pruebas | Integrante 2 | 22/09/2026 | 23/09/2026 | Completado |
| 11 | Revisión del UML contra el código | Integrante 3 | 23/09/2026 | 24/09/2026 | Completado |
| 12 | Elaboración del informe y anexos | Integrante 1 | 23/09/2026 | 26/09/2026 | Completado |
| 13 | Revisión final contra la rúbrica | Integrante 1 | 26/09/2026 | 26/09/2026 | Completado |

Herramienta de gestión: Trello (ver Anexo 8).

---

# E. CAPÍTULO 2: PROPUESTA DE INNOVACIÓN

## 3.1 Diseño de Flujo de Aplicación

El sistema se organiza alrededor de un menú de consola que se repite hasta que
el usuario elige salir. Ante cualquier dato inválido, el programa muestra el
error y vuelve al menú, sin cerrarse.

### Diagrama de casos de uso

El sistema se representa con tres actores: el empleado, que registra horas
extras y consulta o utiliza sus horas compensadas; el supervisor, que aprueba
o rechaza solicitudes; y el responsable de RR. HH., que administra el
personal, el pago y los reportes. Cada caso de uso se ejecuta desde una opción
del menú de consola y comparte el mismo gestor.

![Diagrama de casos de uso](../salida/casos_uso.png)

### Flujo general

El flujo principal recibe al usuario en el menú y lo mantiene en un bucle
hasta que elige "Salir". Eligiendo una opción, el sistema pide los datos,
valida cada uno, muestra el resultado y regresa al menú; si algo no es válido,
muestra el error sin terminar el programa.

![Flujo general de la aplicación](../salida/flujo_aplicacion.png)

### Flujo de registro de horas extras

Comienza cuando el usuario elige la opción de registrar horas extras; el
sistema pide el código del empleado, la fecha, la cantidad de horas y el
motivo. Valida cada dato (empleado existente, horas entre 1 y 24, fecha no
futura) y, si todo es correcto, crea la solicitud en estado PENDIENTE; si
algo falla, muestra el error y vuelve al menú.

![Flujo de registro de horas extras](../salida/flujo_registro_horas_extras.png)

### Flujo de aprobación o rechazo

Después de listar las solicitudes pendientes, el usuario elige una y decide
aprobar o rechazar; en ambos casos el sistema valida el código del aprobador
y que la solicitud siga PENDIENTE. Si aprueba, la solicitud pasa a APROBADA;
si rechaza, pide el motivo y la pasa a RECHAZADA. Un aprobador que no sea
supervisor o una solicitud ya procesada genera el error correspondiente.

![Flujo de aprobación o rechazo](../salida/flujo_aprobacion.png)

### Flujo de utilización de horas compensadas

El usuario pide el código del empleado y la cantidad de horas a utilizar. El
sistema busca al empleado y compara la cantidad con su saldo: si el saldo
alcanza, descuenta las horas y registra el movimiento; si no alcanza, muestra
el error de saldo insuficiente y deja el saldo sin cambios.

![Flujo de horas compensadas](../salida/flujo_horas_compensadas.png)

Los diagramas editables están en `drawio/flujo_aplicacion.drawio`,
`drawio/flujo_registro_horas_extras.drawio`, `drawio/flujo_aprobacion.drawio` y
`drawio/flujo_horas_compensadas.drawio` (formato draw.io).

## 3.2 Diagrama de Clases del Modelo

![Diagrama de clases](../salida/diagrama_clases.png)

El diagrama editable está en `drawio/diagrama_clases.drawio`.

### Encapsulamiento

Los atributos se guardan con la convención de variable privada (`_nombre`) y
se accede a ellos mediante propiedades (`@property`) con validación en el
setter. Las listas del gestor se entregan como copias, de modo que no puedan
modificarse desde fuera de la clase.

### Herencia

El sistema tiene tres jerarquías:

```
Persona (abstracta)  →  Empleado  →  Supervisor
                                  →  ResponsableRRHH

RegistroHora (abstracta)  →  HoraExtra
                          →  HoraCompensada

Solicitud (abstracta)  →  SolicitudHoraExtra
                       →  SolicitudCompensacion
```

`Persona` agrupa los datos de identificación; `RegistroHora` agrupa id,
empleado, fecha, horas y motivo; y `Solicitud` agrupa el ciclo de vida común de
una solicitud. Cada subclase agrega solo lo que le es propio.

### Polimorfismo

El polimorfismo se ejecuta a través de referencias de la clase padre:

- `RegistroHora.calcular_valor()`: en `HoraExtra` devuelve
  `valor_hora × factor_recargo × horas`; en `HoraCompensada` devuelve
  `valor_hora × horas`. En los reportes se recorre `list[RegistroHora]` y se
  invoca `calcular_valor()` sin conocer el tipo concreto.
- `Solicitud.calcular_monto()`: en `SolicitudHoraExtra` delega en su
  `HoraExtra`; en `SolicitudCompensacion` aplica `valor_hora × cantidad_horas`.
- `Persona.obtener_rol()`: devuelve "Empleado", "Supervisor" o "Responsable de
  RR.HH." según la subclase; se usa para filtrar por rol sin `isinstance`.

### Relaciones entre clases

El diagrama usa la notación UML: la **generalización** con el triángulo hueco,
la **composición** con el rombo relleno, la **agregación** con el rombo hueco,
la **asociación** con flecha abierta (navegabilidad) y la multiplicidad en
cada extremo, y la **dependencia** con línea discontinua.

- **Composición (1–1):** `Empleado` está compuesto por una `JornadaLaboral`.
- **Agregación (1–0..*):** `GestorHorasExtras` administra `list[Empleado]`,
  `list[RegistroHora]` y `list[Solicitud]`.
- **Asociación (0..*–1):** cada `RegistroHora` y cada `Solicitud` pertenece a
  un `Empleado`; cada `SolicitudHoraExtra` incluye una `HoraExtra`; cada
  `Solicitud` tiene un `EstadoSolicitud`; `MenuConsola` usa un
  `GestorHorasExtras`.
- **Dependencia:** `GestorHorasExtras` usa `CalculadoraHoras` («utiliza») y
  lanza las excepciones de negocio («lanza»); `Main` usa `MenuConsola`
  («utiliza»).

### Colecciones

Se utilizan tres listas:

| Colección | Uso |
|-----------|-----|
| `list[Empleado]` | Registro, búsqueda y listado de empleados. |
| `list[RegistroHora]` | Movimientos de horas y cálculo de totales. |
| `list[Solicitud]` | Estados, aprobación, pago y reportes. |

### Cálculos principales

```
valor_hora       = salario_mensual / horas_mensuales        (por defecto 240 h)
valor_hora_extra = valor_hora × factor_hora_extra           (por defecto 1.5)
pago_total       = valor_hora_extra × cantidad_horas
valor_compensada = valor_hora × cantidad_horas
saldo_nuevo      = saldo − horas_utilizadas   (si horas_utilizadas ≤ saldo)
```

> El factor 1.5 no proviene de una norma legal: es una regla configurada para
> este trabajo académico y puede modificarse con `CalculadoraHoras.factor_hora_extra`.

### Excepciones

Siete excepciones propias controlan los errores de negocio:
`EmpleadoNoEncontradoError`, `EmpleadoDuplicadoError`, `HorasInvalidasError`,
`SaldoInsuficienteError`, `SolicitudNoEncontradaError`,
`EstadoSolicitudInvalidaError` y `AprobacionNoAutorizadaError`. Esta última
aplica la regla de que **solo un supervisor registrado puede aprobar o
rechazar** una solicitud: el gestor busca al empleado que intenta aprobar y, si
no es supervisor, rechaza la operación. Para los datos simples (texto vacío,
salario negativo) se usa `ValueError`. El menú captura todas ellas y continúa
funcionando.

---

# F. CONCLUSIONES

La implementación del Sistema de Gestión y Control de Horas Extras y Horas
Compensadas permitió concluir que la programación orientada a objetos es una
alternativa viable para formalizar los procesos de una empresa mediana como
Fábrica Marsar SRL, aun cuando el problema se presente en un contexto de
oficina y no en un entorno industrial.

Se comprobó que la orientación a objetos modela fielmente el dominio: las tres
jerarquías del sistema (`Persona` → `Empleado` → `Supervisor` /
`ResponsableRRHH`, `RegistroHora` → `HoraExtra` / `HoraCompensada` y
`Solicitud` → `SolicitudHoraExtra` / `SolicitudCompensacion`) permiten tratar
las diferencias entre tipos mediante herencia y reutilizar el comportamiento
común, mientras que el polimorfismo en `calcular_valor()`, `calcular_monto()`
y `obtener_rol()` evita el uso de condicionales según el tipo.

La verificación con 23 pruebas unitarias superadas demostró que los métodos de
negocio —el cálculo del pago, el control de estados y la validación del
saldo— se comportan como se especificaba en las historias de usuario.

Además, el control de excepciones demostró que el sistema puede responder a
datos inválidos sin detenerse, requisito indispensable para que una
herramienta de uso diario resulte confiable.

# G. RECOMENDACIONES

- **Para la empresa:** utilizar el sistema como registro único de horas y
  conservar los reportes exportados como respaldo ante una eventual
  auditoría.
- **Para el área de RR. HH.:** continuar el registro de horas dentro del
  sistema y evitar el uso paralelo de cuadernos u hojas de cálculo, que fue la
  causa principal del problema analizado.
- **Para futuras versiones:** extender el cálculo de horas a los conceptos de
 CTS (gratificaciones, bonificaciones y horas de CTS), permitir la carga de la
 planilla del personal y exportar los reportes en formatos PDF y Excel.
- **Para el mantenimiento del software:** conservar la disciplina de escribir
  pruebas unitarias antes de cada modificación, ya que son las que permiten
  detectar regresiones en el cálculo de pagos.
- **Para el equipo académico:** replicar la metodología de priorización de
  historias de usuario, el control de versiones con Git y la gestión de
  tareas con Trello en los siguientes trabajos del curso.

# H. OBJETIVO DEL ESTUDIANTE (STUDENT OUTCOME)

Al finalizar el trabajo, el estudiante es capaz de:

- Analizar un problema real de una organización e identificar sus causas,
  consecuencias y necesidades de información.
- Modelar un sistema mediante clases, identificando atributos, métodos,
  relaciones de herencia, asociación, agregación y composición.
- Aplicar los principios de programación orientada a objetos: abstracción,
  encapsulamiento, herencia y polimorfismo.
- Especificar funcionalidades mediante historias de usuario priorizadas y
  derivar de ellas los criterios de aceptación.
- Traducir un modelo de clases a código funcional en Python utilizando la
  biblioteca estándar.
- Verificar el comportamiento del software mediante pruebas unitarias
  automatizadas y gestionar los errores mediante excepciones propias.
- Trabajar en equipo con herramientas de control de versiones (Git),
  organización de tareas (Trello) y edición compartida de documentos.

---

# I. BIBLIOGRAFÍA

American Psychological Association. (2020). *Publication manual of the American
Psychological Association* (7.ª ed.). https://doi.org/10.1037/0000165-000

Lutz, M. (2013). *Learning Python* (5.ª ed.). O'Reilly Media.

Python Software Foundation. (2024). *The Python standard library*.
https://docs.python.org/3/library/

Python Software Foundation. (2024). *The Python tutorial*.
https://docs.python.org/3/tutorial/

Python Software Foundation. (2024). *unittest — Unit testing framework*.
https://docs.python.org/3/library/unittest.html

PlantUML. (2024). *PlantUML language reference guide*. https://plantuml.com/guide

Sommerville, I. (2016). *Software engineering* (10.ª ed.). Pearson.

Van Rossum, G., Warsaw, B., & Coghlan, N. (2001). *PEP 8 — Style guide for
Python code*. Python Software Foundation.
https://peps.python.org/pep-0008/

---

# J. ANEXOS

## ANEXO 1 — Evidencias del trabajo en equipo

Coordinaciones realizadas por cada integrante (reuniones, acuerdos y
distribución de tareas). Los números de teléfono de los participantes se
difuminaron en las capturas del grupo.

![Carpeta compartida en Google Drive](img/evidencias/anexo1_drive_archivos.jpg)

*Figura 8. Carpeta compartida en Google Drive con el enunciado, la propuesta y el documento del equipo*

![Carpeta de Drive con la estructura del proyecto](img/evidencias/anexo2_drive_test.jpg)

*Figura 9. Carpeta de Drive con la estructura de carpetas del proyecto y el documento del trabajo parcial*

![Acuerdo sobre el problema real](img/evidencias/anexo3_whatsapp_problema.jpg)

*Figura 10. Acuerdo sobre el problema real y sobre el lenguaje de programación del curso*

![Ajuste del proceso real](img/evidencias/anexo4_whatsapp_proceso.jpg)

*Figura 11. Ajuste del proceso real: registro en cuaderno y Excel, y aprobación a cargo del responsable del área*

![Revisión del código y reparto de anexos](img/evidencias/anexo5_whatsapp_codigo.jpg)

*Figura 12. Revisión del código del sistema y distribución de los anexos entre los integrantes*

![Organización del trabajo en Trello](img/evidencias/anexo6_whatsapp_trello.jpg)

*Figura 13. Organización del trabajo en el tablero de Trello a partir del cronograma del documento*

![Permisos de edición del documento](img/evidencias/anexo7_drive_acceso.jpg)

*Figura 14. Permisos de edición del documento compartido para los tres integrantes del equipo*

![Diagrama de clases y comentarios de revisión](img/evidencias/anexo8_word_diagrama.jpg)

*Figura 15. Documento del trabajo parcial con el diagrama de clases y los comentarios de revisión*

## ANEXO 2 — Evidencias de desarrollo

Capturas del código fuente y de la comparación de versiones durante el
desarrollo, junto con la ejecución del programa
(ver también `salida/pruebas_unittest.txt`).

![Estructura del proyecto y punto de entrada](img/evidencias/anexo9_codigo_main.jpg)

*Figura 16. Estructura del proyecto y punto de entrada `src/main.py`*

![Comparación de cambios entre versiones](img/evidencias/git_comparacion_cambios.png)

*Figura 17. Comparación de cambios entre dos versiones de `menu_consola.py`*

## ANEXO 3 — Capturas del sistema

Capturas del menú principal, del registro de empleados, del registro de horas
extras, de la aprobación de solicitudes y de los reportes. La salida completa
de una ejecución real está en `salida/ejecucion_menu.txt`.

![Menú principal y búsqueda de empleado](img/evidencias/anexo10_sistema_menu.jpg)

*Figura 18. Menú principal y búsqueda de empleado por código (EG04, Ana Torres)*

## ANEXO 4 — Pruebas

![Salida de la ejecución de las pruebas unitarias](img/evidencias/pruebas_unittest.png)

*Figura 19. Salida de la ejecución de las pruebas unitarias (unittest)*

Resultado de la ejecución con `unittest`: 23 pruebas ejecutadas, 23 correctas,
0 fallidas. Detalle en `docs/07_pruebas.md`.

## ANEXO 5 — UML

Diagrama de clases en `drawio/diagrama_clases.drawio` e imagen en
`salida/diagrama_clases.png`.

![Diagrama de clases del modelo](../salida/diagrama_clases.png)

*Figura 20. Diagrama de clases del modelo (véase también la Figura 6)*

## ANEXO 6 — Flujo

Los cuatro diagramas de flujo se muestran en las Figuras 2 a 5 del capítulo 2.
Los archivos editables están en `/drawio` y las imágenes en `/salida` del
repositorio *github*.

## ANEXO 7 — Git

https://github.com/marlo4220mc/sistema-horas-extras

Repositorio público con los *commits* del equipo (historia por etapas).

![Repositorio en GitHub](img/evidencias/git_repositorio_github.png)

*Figura 21. Repositorio del equipo en GitHub con el historial de commits*

![Historial de versiones de un archivo](img/evidencias/git_historial_archivo.png)

*Figura 22. Historial de versiones del archivo `hora_compensada.py`*

## ANEXO 8 — Trello

Tablero de gestión del cronograma y de las actividades del equipo:

https://trello.com/b/VRlZeBkn/sistema-de-horas-extras-tp-fp2

El tablero tiene 5 listas (una por fase del proyecto) y 13 tarjetas, una por
actividad del cronograma, con el responsable, las fechas y el estado.

![Tablero de Trello con el cronograma](img/tablero_trello.png)

*Figura 23. Tablero de Trello con el cronograma y la asignación de actividades*
