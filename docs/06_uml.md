# ETAPA 6 — UML

**Archivo PlantUML:** `uml/diagrama_clases.puml`
**Imagen:** `salida/diagrama_clases.png`
**Diagrama de casos de uso:** `salida/casos_uso.png`

El diagrama de clases se revisó **después** de programar y coincide con el
código: los nombres de clases, atributos y métodos del `.puml` son los mismos
que están en `src/`.

---

## 1. Clases incluidas

| # | Clase | Paquete | Tipo |
|---|-------|---------|------|
| 1 | `Persona` | modelo | abstracta |
| 2 | `Empleado` | modelo | concreta |
| 3 | `Supervisor` | modelo | concreta |
| 4 | `ResponsableRRHH` | modelo | concreta |
| 5 | `JornadaLaboral` | modelo | concreta |
| 6 | `RegistroHora` | modelo | abstracta |
| 7 | `HoraExtra` | modelo | concreta |
| 8 | `HoraCompensada` | modelo | concreta |
| 9 | `Solicitud` | modelo | abstracta |
| 10 | `SolicitudHoraExtra` | modelo | concreta |
| 11 | `SolicitudCompensacion` | modelo | concreta |
| 12 | `CalculadoraHoras` | servicio | concreta |
| 13 | `GestorHorasExtras` | servicio | concreta |
| 14 | `MenuConsola` | servicio | concreta |
| — | `EstadoSolicitud` | modelo | enumeración |
| — | `Main` | — | punto de entrada |
| — | 6 excepciones | excepciones | heredan de `Exception` |

**Total: 14 clases principales**, dentro del rango de 10 a 15 clases exigido.

---

## 2. Herencia representada

Flecha con triángulo (hijo → padre):

```
Persona  ←── Empleado  ←── Supervisor
                       ←── ResponsableRRHH

RegistroHora ←── HoraExtra
             ←── HoraCompensada

Solicitud ←── SolicitudHoraExtra
          ←── SolicitudCompensacion
```

---

## 3. Asociaciones, agregación y composición

| Relación | Multiplicidad | Tipo | Explicación |
|----------|---------------|------|-------------|
| `Empleado` — `JornadaLaboral` | 1 → 1 | composición (`*--`) | Todo empleado tiene una jornada. |
| `GestorHorasExtras` — `Empleado` | 1 → 0..* | agregación (`o--`) | El gestor administra la lista de empleados. |
| `GestorHorasExtras` — `RegistroHora` | 1 → 0..* | agregación | Administra los movimientos de horas. |
| `GestorHorasExtras` — `Solicitud` | 1 → 0..* | agregación | Administra las solicitudes. |
| `RegistroHora` — `Empleado` | * → 1 | asociación | Cada movimiento pertenece a un empleado. |
| `Solicitud` — `Empleado` | * → 1 | asociación | Cada solicitud pertenece a un empleado. |
| `SolicitudHoraExtra` — `HoraExtra` | 1 → 1 | asociación | La solicitud referencia las horas pedidas. |
| `Solicitud` — `EstadoSolicitud` | * → 1 | dependencia | Usa la enumeración de estados. |
| `GestorHorasExtras` — `CalculadoraHoras` | 1 → 1 | asociación | Usa la calculadora para los montos. |
| `MenuConsola` — `GestorHorasExtras` | 1 → 1 | asociación | El menú invoca al gestor. |
| `Main` — `MenuConsola` | 1 → 1 | asociación | `main` inicia el menú. |
| `GestorHorasExtras` — excepciones | — | dependencia | Lanza las excepciones de negocio. |

---

## 4. Métodos polimórficos marcados en el UML

| Método | Clase base | Redefinido en |
|--------|-----------|----------------|
| `calcular_valor()` | `RegistroHora` | `HoraExtra`, `HoraCompensada` |
| `obtener_tipo()` | `RegistroHora` | `HoraExtra`, `HoraCompensada` |
| `calcular_monto()` | `Solicitud` | `SolicitudHoraExtra`, `SolicitudCompensacion` |
| `detalle()` | `Solicitud` | `SolicitudHoraExtra`, `SolicitudCompensacion` |
| `obtener_rol()` | `Persona` | `Empleado`, `Supervisor`, `ResponsableRRHH` |

---

## 5. Cómo se lee el diagrama

- `-` atributo privado (en Python, atributo con `_`), `+` método público,
  `#` método protegido.
- `«abstract»` indica una clase o método que no se implementa directamente
  (`ABC` + `@abstractmethod`).
- `«override»` indica que el método redefine a uno de la clase padre.
- Triángulo = herencia · `o--` = agregación · línea discontinua = dependencia.

---

## 6. Verificación código ↔ UML

| Elemento del UML | Archivo en el código |
|------------------|----------------------|
| `Persona` | `src/modelo/persona.py` |
| `Empleado` | `src/modelo/empleado.py` |
| `Supervisor` | `src/modelo/supervisor.py` |
| `ResponsableRRHH` | `src/modelo/responsable_rrhh.py` |
| `JornadaLaboral` | `src/modelo/jornada_laboral.py` |
| `RegistroHora` | `src/modelo/registro_hora.py` |
| `HoraExtra` | `src/modelo/hora_extra.py` |
| `HoraCompensada` | `src/modelo/hora_compensada.py` |
| `Solicitud` | `src/modelo/solicitud.py` |
| `SolicitudHoraExtra` | `src/modelo/solicitud_hora_extra.py` |
| `SolicitudCompensacion` | `src/modelo/solicitud_compensacion.py` |
| `EstadoSolicitud` | `src/modelo/estado_solicitud.py` |
| `CalculadoraHoras` | `src/servicio/calculadora_horas.py` |
| `GestorHorasExtras` | `src/servicio/gestor_horas_extras.py` |
| `MenuConsola` | `src/servicio/menu_consola.py` |
| `Main` | `src/main.py` |
| Excepciones | `src/excepciones/excepciones.py` |
