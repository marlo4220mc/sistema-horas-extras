# ETAPA 5 — Diseño de Clases

**Proyecto:** Sistema de Gestión y Control de Horas Extras y Horas Compensadas
**Lenguaje:** Python 3 (aplicación de consola)

---

## 1. Criterio del diseño

El sistema se organizó en tres paquetes:

| Paquete | Contenido | Rol |
|---------|-----------|-----|
| `modelo` | Entidades y reglas propias de los datos | Qué es el negocio |
| `servicio` | Cálculos, fachada con listas y menú | Cómo se opera el negocio |
| `excepciones` | Errores de negocio controlados | Qué puede fallar |

**Número de clases: 14 clases principales** (11 de modelo + 3 de servicio),
dentro del rango de 10 a 15 pedido por el enunciado. A ellas se suman:

- 1 punto de entrada: `main.py` (función `main`).
- 1 enumeración: `EstadoSolicitud`.
- 7 excepciones personalizadas (requisito explícito del enunciado).

Ninguna clase se creó solo para aumentar el conteo: cada una tiene una
responsabilidad distinta y se usa en la lógica real.

---

## 2. Jerarquías de herencia (reales)

```
Persona (abstracta, ABC)
   └── Empleado
         ├── Supervisor          (agrega área a cargo y límite de aprobación)
         └── ResponsableRRHH     (agrega responsabilidad principal)

RegistroHora (abstracta, ABC)
   ├── HoraExtra                (redefine calcular_valor con recargo)
   └── HoraCompensada           (redefine calcular_valor sin recargo)

Solicitud (abstracta, ABC)
   ├── SolicitudHoraExtra       (redefine calcular_monto y detalle)
   └── SolicitudCompensacion    (redefine calcular_monto y detalle)
```

**¿Por qué son jerarquías apropiadas y no artificiales?**

- `Supervisor` y `ResponsableRRHH` son empleados en la realidad: comparten
  código, salario, cargo, jornada y saldo, y se diferencian por datos extra.
- `HoraExtra` y `HoraCompensada` comparten id, empleado, fecha, horas y motivo,
  pero **se valorizan distinto**: la hora extra tiene recargo y la compensada
  no. Ese comportamiento distinto da sentido a la clase base `RegistroHora`.
- `SolicitudHoraExtra` y `SolicitudCompensacion` comparten el ciclo de vida
  (pendiente → aprobada/rechazada) pero calculan su monto de forma diferente.

---

## 3. Encapsulamiento

Regla aplicada en todo el proyecto:

- Los atributos se guardan en variables **privadas por convención** (`_nombre`).
- El acceso se hace con propiedades (`@property`) y validadores
  (`@nombre.setter`), que lanzan `ValueError` si el dato no es correcto.
- Las listas del gestor se entregan como copias (`list(self._empleados)`),
  para que nadie las modifique desde fuera.

Ejemplo (módulo `modelo/empleado.py`):

```python
@property
def salario_mensual(self) -> float:
    return self._salario_mensual

@salario_mensual.setter
def salario_mensual(self, valor: float) -> None:
    if valor <= 0:
        raise ValueError("El salario mensual debe ser mayor a cero.")
    self._salario_mensual = float(valor)
```

---

## 4. Polimorfismo (dónde está y cómo se usa)

El polimorfismo es **real**: se ejecuta a través de referencias de la clase
padre.

### 4.1 `RegistroHora.calcular_valor()`

```
RegistroHora (ABC)     calcular_valor() @abstractmethod
   ├── HoraExtra        valor_hora × factor_recargo × horas
   └── HoraCompensada   valor_hora × horas
```

Uso real en los reportes y en la prueba unitaria:

```python
movimientos: list[RegistroHora] = [HoraExtra(...), HoraCompensada(...)]
movimientos[0].calcular_valor()   # 12.5 * 1.5 * 2 = 37.50  (HoraExtra)
movimientos[1].calcular_valor()   # 12.5 * 2       = 25.00  (HoraCompensada)
```

### 4.2 `Solicitud.calcular_monto()` y `Solicitud.detalle()`

```
Solicitud (ABC)              calcular_monto() / detalle() @abstractmethod
   ├── SolicitudHoraExtra        delega en la HoraExtra
   └── SolicitudCompensacion     valor_hora × cantidad_horas
```

En `GestorHorasExtras.total_a_pagar()` se recorre `list[Solicitud]` y se
invoca `calcular_monto()` sin saber de qué subclase se trata.

### 4.3 `Persona.obtener_rol()`

```
Persona (ABC)        obtener_rol() @abstractmethod
   ├── Empleado           "Empleado"
   ├── Supervisor         "Supervisor"
   └── ResponsableRRHH    "Responsable de RR.HH."
```

`GestorHorasExtras.listar_empleados_por_rol(rol)` recorre `list[Empleado]` y
usa `obtener_rol()` para filtrar, sin usar `isinstance`.

---

## 5. Descripción de cada clase

### 5.1 `Persona` (abstracta) — modelo

- **Responsabilidad:** datos comunes de identificación.
- **Atributos:** `_nombres`, `_apellidos`, `_tipo_documento`,
  `_numero_documento`, `_correo`.
- **Métodos:** `nombre_completo` (propiedad), propiedades con validación,
  `obtener_rol()` (abstracto), `_validar_texto(...)` (estático, de apoyo).

### 5.2 `Empleado` — modelo

- **Responsabilidad:** trabajador con su información laboral y su saldo.
- **Atributos:** `_codigo_empleado`, `_salario_mensual`, `_cargo`,
  `_fecha_ingreso`, `_jornada`, `_saldo_horas_compensadas`, `_activo`.
- **Métodos de negocio:**
  - `calcular_valor_hora()` = `salario_mensual / jornada.calcular_horas_mensuales()`
  - `agregar_horas_compensadas(horas)`
  - `consumir_horas_compensadas(horas)`
  - `obtener_rol()` → `"Empleado"`
- **Relaciones:** hereda de `Persona`; **compone** una `JornadaLaboral`.
- **Excepciones:** `HorasInvalidasError`, `SaldoInsuficienteError`, `ValueError`.

### 5.3 `Supervisor` — modelo

- **Atributos:** `_area_a_cargo`, `_limite_horas_aprobables`.
- **Métodos:** `puede_aprobar(horas)`, `obtener_rol()` → `"Supervisor"`.
- **Herencia:** extiende `Empleado`.

### 5.4 `ResponsableRRHH` — modelo

- **Atributos:** `_responsabilidad_principal`.
- **Métodos:** `obtener_rol()` → `"Responsable de RR.HH."`.
- **Herencia:** extiende `Empleado`.

### 5.5 `JornadaLaboral` — modelo

- **Responsabilidad:** definir la jornada y calcular las horas mensuales.
- **Atributos:** `_horas_diarias`, `_dias_laborables_mes`, `_hora_inicio`, `_hora_fin`.
- **Métodos:** `calcular_horas_mensuales()` = `horas_diarias × dias_laborables_mes`.
- **Relación:** es parte de `Empleado` (composición, multiplicidad 1).
- **Valor por defecto:** 8 h/día y 30 días/mes → 240 horas mensuales.

### 5.6 `RegistroHora` (abstracta) — modelo

- **Atributos:** `_id`, `_empleado`, `_fecha`, `_cantidad_horas`, `_motivo`.
- **Métodos:** `calcular_valor()` y `obtener_tipo()` (abstractos), `resumen()`
  (implementación común).
- **Relaciones:** asociación con `Empleado`; base de las horas.
- **Excepciones:** el setter de `cantidad_horas` lanza `HorasInvalidasError`.

### 5.7 `HoraExtra` — modelo

- **Atributos:** `_factor_recargo` (regla configurable).
- **Métodos:** `calcular_valor()` (redefinido), `obtener_tipo()` → `"Hora extra"`.

### 5.8 `HoraCompensada` — modelo

- **Atributos:** `_es_consumo` (True = utilizada, False = otorgada).
- **Métodos:** `calcular_valor()` (redefinido, sin recargo), `obtener_tipo()`.

### 5.9 `Solicitud` (abstracta) — modelo

- **Atributos:** `_id`, `_empleado`, `_fecha_solicitud`, `_estado`
  (`EstadoSolicitud`), `_observacion`, `_fecha_resolucion`, `_resuelto_por`.
- **Métodos:** `aprobar(usuario)`, `rechazar(motivo, usuario)`,
  `calcular_monto()` (abstracto), `obtener_tipo()` (abstracto),
  `detalle()` (abstracto), `resumen()`.
- **Reglas:** solo se aprueba o rechaza si el estado es `PENDIENTE`.
- **Excepciones:** `EstadoSolicitudInvalidaError`.

### 5.10 `SolicitudHoraExtra` — modelo

- **Atributos:** `_hora_extra` (`HoraExtra`).
- **Métodos:** `calcular_monto()`, `detalle()`, `pagar(usuario)`, `compensar(usuario)`.

### 5.11 `SolicitudCompensacion` — modelo

- **Atributos:** `_cantidad_horas`, `_motivo_uso`.
- **Métodos:** `calcular_monto()`, `detalle()`.

### 5.12 `EstadoSolicitud` (enumeración) — modelo

- **Valores:** `PENDIENTE`, `APROBADA`, `RECHAZADA`, `PAGADA`, `COMPENSADA`.

### 5.13 `CalculadoraHoras` — servicio

- **Atributos:** `_factor_hora_extra` (1.5 por defecto),
  `_factor_hora_compensada` (1.0 por defecto).
- **Métodos:** `valor_hora(empleado)`, `pago_horas_extras(empleado, horas)`,
  `valor_horas_compensadas(empleado, horas)`, `redondear(valor)`.

### 5.14 `GestorHorasExtras` — servicio

- **Responsabilidad:** fachada del sistema; administra las listas y ejecuta
  las funcionalidades de control.
- **Atributos:** `_empleados: list[Empleado]`, `_registros: list[RegistroHora]`,
  `_solicitudes: list[Solicitud]`, `_calculadora: CalculadoraHoras`.
- **Métodos:** registro, búsqueda, listado, aprobación, pago, compensación,
  consulta de saldo, historial y reportes (ver UML).
- **Regla de aprobación:** antes de aprobar o rechazar valida, con
  `_validar_supervisor(codigo)`, que el empleado indicado exista y sea un
  `Supervisor`; si no lo es, lanza `AprobacionNoAutorizadaError`.

### 5.15 `MenuConsola` — servicio

- **Métodos:** `iniciar()`, `_ejecutar_opcion(opcion)`, `_menu_reportes()` y
  lectores validados (`_leer_entero`, `_leer_float`, `_leer_fecha`).
- **Manejo de errores:** captura las excepciones de negocio y sigue funcionando.

### 5.16 Clases de apoyo

| Clase | Responsabilidad |
|-------|-----------------|
| `Main` (`main.py`) | Arranca el sistema y carga los datos de demostración. |
| `EmpleadoNoEncontradoError` | Empleado inexistente. |
| `EmpleadoDuplicadoError` | Código o documento repetido. |
| `HorasInvalidasError` | Horas ≤ 0 o > 24. |
| `SaldoInsuficienteError` | Se piden más horas de las disponibles. |
| `SolicitudNoEncontradaError` | Solicitud inexistente. |
| `EstadoSolicitudInvalidaError` | Transición de estado no permitida. |
| `AprobacionNoAutorizadaError` | Quien intenta aprobar o rechazar no es un supervisor. |

> Las 7 excepciones se agrupan en el módulo `src/excepciones/excepciones.py`.
> Se usa el sufijo `Error` porque es la convención de nombres de Python
> (PEP 8) para las excepciones.

---

## 6. Colecciones

| Colección | Tipo real | Uso en la lógica |
|-----------|-----------|------------------|
| `list[Empleado]` | `list` | Repositorio de empleados; búsquedas y listados. |
| `list[RegistroHora]` | `list` | Movimientos de horas; totales y reportes. |
| `list[Solicitud]` | `list` | Solicitudes; estados, aprobación y pago. |

Las listas no existen solo para cumplir la rúbrica: **toda** la lógica de
registro, búsqueda y reportes recorre estas colecciones.

---

## 7. Excepciones

| Excepción | Se lanza desde | Se captura en |
|-----------|----------------|---------------|
| `EmpleadoNoEncontradoError` | `buscar_empleado_por_codigo/documento` | Menú |
| `EmpleadoDuplicadoError` | `registrar_empleado` | Menú |
| `HorasInvalidasError` | setters de horas | Menú |
| `SaldoInsuficienteError` | `consumir_horas_compensadas`, `utilizar_horas_compensadas` | Menú |
| `SolicitudNoEncontradaError` | `buscar_solicitud` | Menú |
| `EstadoSolicitudInvalidaError` | `aprobar`, `rechazar`, `pagar`, `compensar` | Menú |
| `AprobacionNoAutorizadaError` | `_validar_supervisor` (desde `aprobar_solicitud` y `rechazar_solicitud`) | Menú |

Además se usa `ValueError` para validar datos simples (textos vacíos, salario
negativo, fechas futuras), de modo que no se crean excepciones personalizadas
innecesarias.

### 7.1 Validación temprana en el menú

El menú valida cada dato **en el momento en que se ingresa**, antes de pedir el
resto del formulario. Por ejemplo:

- al registrar un empleado, avisa si el **código** o el **documento** ya
  existen, si el correo es inválido, si el salario no es mayor a cero o si la
  fecha de ingreso es futura;
- al registrar horas, avisa si el **empleado no existe**, si la **fecha es
  futura** o si las horas están fuera del rango `0 < h ≤ 24`;
- al aprobar o rechazar, avisa si la solicitud **no existe**, si **ya fue
  procesada** o si quien aprueba **no es un supervisor**;
- al utilizar horas compensadas, avisa si el saldo es insuficiente al ingresar
  la cantidad (no al final del formulario).

Las validaciones del modelo **se mantienen como respaldo** (defensa en
profundidad): aunque se invoque al gestor directamente —por ejemplo desde una
prueba unitaria— nunca se registran datos inválidos.
