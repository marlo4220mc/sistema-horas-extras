# ETAPA 0 — Requisitos del Enunciado Oficial

**Curso:** 1FIS275 — Fundamentos de Programación 2
**Ciclo:** 2026-25
**Trabajo Parcial:** Sistema de Gestión y Control de Horas Extras y Horas Compensadas
**Lenguaje:** Python 3
**Fuente oficial:** `enunciado_oficial.docx` (`1FIS0275_Enunciado del Trabajo Parcial_vf_AV - 202625`)

---

## 1. Objetivo del trabajo

Seleccionar una empresa donde labore algún integrante del grupo, identificar
un **problema real** de uno de sus procesos de negocio y resolverlo mediante
un **programa orientado a objetos** que aplique los conceptos del curso.

## 2. Logro del curso

Al finalizar el curso, el estudiante resuelve problemas de computación de
alta complejidad a través de la programación orientada a objetos. El trabajo
contribuye al ABET – Student Outcome 2 (diseño de ingeniería para producir
soluciones que satisfagan necesidades específicas).

## 3. Consideraciones mínimas del enunciado

| # | Consideración del enunciado |
|---|------------------------------|
| 1 | El sistema debe tener un menú de ejecución de las opciones de funcionalidad. |
| 2 | El sistema debe contemplar funcionalidades de control y de cálculos. |
| 3 | Presentar el diagrama de clases UML de la solución propuesta. |
| 4 | POO con clase, relaciones entre clases, herencia y polimorfismo. |
| 5 | Aplicar pruebas a los métodos de negocio o comportamiento de las clases. |
| 6 | Controlar excepciones en los datos a ingresar, entre otros. |

## 4. Matriz de requisitos

| Requisito | Qué exige | Cómo lo cumplirá el proyecto |
|-----------|-----------|------------------------------|
| **Empresa real (problema real)** | Problema identificable en un proceso de negocio. | Empresa `[NOMBRE DE LA EMPRESA]` con el problema de control de horas extras y compensadas. |
| **Programa orientado a objetos** | Clases, objetos, herencia, polimorfismo. | 14 clases en los paquetes `modelo` y `servicio`. |
| **10 a 15 clases** | Mínimo 10 y máximo 15 clases. | **14 clases principales** (11 de `modelo` + 3 de `servicio`), más `Main`, la enumeración `EstadoSolicitud` y 7 excepciones personalizadas. |
| **Colecciones tipo lista** | Uso real de listas. | `list[Empleado]`, `list[RegistroHora]` y `list[Solicitud]`. |
| **Registro** | Dar de alta entidades. | `registrar_empleado`, `registrar_solicitud_hora_extra`, `registrar_horas_compensadas`. |
| **Búsqueda** | Localizar entidades. | `buscar_empleado_por_codigo`, `buscar_empleado_por_documento`, `buscar_solicitud`. |
| **Listado** | Mostrar todas las entidades. | `listar_empleados`, `listar_solicitudes`, `listar_horas_extras`. |
| **Cálculos** | Cálculos de negocio. | `valor_hora`, `pago_horas_extras`, `calcular_monto`, totales de reporte. |
| **Menú** | Menú en consola. | `MenuConsola` con 13 opciones + salir y submenú de reportes. |
| **UML** | Diagrama de clases. | `uml/diagrama_clases.puml` e imagen en `salida/`. |
| **Relaciones entre clases** | Asociación, agregación, composición, herencia. | Documentadas en `docs/05_diseno_clases.md` y reflejadas en el UML. |
| **Herencia** | Jerarquía real. | `Persona → Empleado / Supervisor / ResponsableRRHH`; `RegistroHora → HoraExtra / HoraCompensada`; `Solicitud → SolicitudHoraExtra / SolicitudCompensacion`. |
| **Polimorfismo** | Comportamiento polimórfico. | `calcular_valor()` en `RegistroHora`; `calcular_monto()` y `detalle()` en `Solicitud`; `obtener_rol()` en `Persona`. |
| **Encapsulamiento** | Atributos privados con acceso controlado. | Atributos con `_nombre` y `@property` con validación. |
| **Pruebas** | Pruebas de métodos de negocio. | `unittest` (biblioteca estándar) — `test/test_sistema.py` con 23 pruebas. |
| **Excepciones** | Control de excepciones de ingreso. | 7 excepciones personalizadas en `src/excepciones/` (incluye `AprobacionNoAutorizadaError`). |
| **Informe** | Documento Word con las secciones. | `docs/informe_final.md` y `docs/Trabajo_Parcial_FP2.docx`. |
| **APA** | Bibliografía en formato APA. | Sección de Bibliografía con fuentes reales. |
| **Anexos** | Evidencias del equipo, Git, Trello. | Anexos 1 a 8 con placeholders. |
| **Cronograma** | Asignación de actividades. | Tabla de 13 actividades en el Capítulo 1.4. |
| **Estructura del informe** | Carátula, índice, introducción, capítulos, bibliografía, anexos. | `docs/informe_final.md` sigue esa estructura. |

## 5. Estructura del informe exigida

- Carátula / Miembros del Grupo
- Índice
- Introducción
- Capítulo 1: Situación Actual
  - Análisis del Problema
  - Objetivo del Sistema
  - Lista de Funcionalidades o Historias de Usuario, priorizadas
  - Cronograma y Asignación de Actividades
- Capítulo 2: Propuesta de Innovación
  - Diseño de Flujo de aplicación
  - Diagrama de Clases del Modelo
- Bibliografía (formato APA)
- Anexos
  - Evidencias del Trabajo en Equipo
  - URL de GIT con commits por rol
  - URL de Trello

## 6. Forma de entrega exigida

Archivo comprimido con nombre `GRUPO_XX_TP_FP2_Ciclo` que contenga los
fuentes y el documento Word del proyecto.

---

> **Conclusión:** El proyecto cumple las 6 consideraciones mínimas del enunciado
> y los requisitos técnicos extraídos de él. Esta matriz es la base de la
> auto-revisión `REVISION_RUBRICA.md` al final del trabajo.
