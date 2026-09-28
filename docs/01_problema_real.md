# ETAPA 1 — Problema Real

**Empresa (ficticia para fines académicos):** Fábrica Marsar SRL
**Proceso analizado:** Control de Horas Extras y Horas Compensadas del personal

---

## 1. Contexto

Fábrica Marsar SRL es una organización del sector servicios que cuenta
con personal administrativo, operativo y de supervisión. Por la naturaleza
de su actividad, es habitual que determinados empleados deban extender su
jornada de trabajo habitual para cumplir con entregas, picos de operación
o atención de incidentes.

Hasta la fecha, las horas trabajadas fuera de la jornada regular y las
horas compensadas se registran de manera manual —en planillas físicas y
correos internos— lo que produce retrasos, errores de cálculo y
discrepancias entre lo que el empleado reporta, lo que el supervisor
aprueba y lo que finalmente se paga o compensa.

## 2. Situación actual

El proceso actual de control de horas se realiza en tres pasos
desconectados entre sí:

1. El **empleado** completa un formulario en papel cuando realiza horas
   extras. Ese formulario queda en su escritorio hasta fin de mes.
2. El **supervisor** recoge los formularios y, según su criterio, anota
   en una planilla Excel si las aprueba o las rechaza.
3. El área de **RR. HH.** consolida la planilla, calcula manualmente lo
   que se debe pagar y, por separado, lleva un cuaderno con las horas
   compensadas.

No existe una herramienta que conecte estas tres etapas.

## 3. Problema identificado

La empresa no cuenta con un sistema que permita **registrar, controlar,
aprobar y calcular** de manera uniforme las horas extras que sus
empleados realizan fuera de su jornada habitual, ni las **horas
compensadas** que la empresa entrega como beneficio.

## 4. Problema central

> *La ausencia de un sistema único de gestión provoca que la información
> de horas extras y horas compensadas esté dispersa, sea propensa a
> errores manuales, no se pueda consultar de inmediato y no permita
> mantener un saldo confiable por empleado.*

## 5. Causas

| # | Causa |
|---|-------|
| C1 | El registro se hace en papel y se centraliza a fin de mes. |
| C2 | No hay un repositorio común entre el área usuaria y RR. HH. |
| C3 | Los cálculos del valor hora y del pago se hacen con calculadora. |
| C4 | El control de horas compensadas es un cuaderno físico. |
| C5 | No existen estados formales para las solicitudes (pendiente, aprobada, rechazada). |

## 6. Consecuencias

| # | Consecuencia |
|---|--------------|
| CO1 | Errores frecuentes al transcribir los formularios a la planilla. |
| CO2 | Retrasos en el pago de las horas extras. |
| CO3 | Conflictos entre el empleado y la empresa por horas no reconocidas. |
| CO4 | Saldo de horas compensadas desactualizado o inexistente. |
| CO5 | Imposibilidad de auditar cuántas horas extras se han pagado en el mes. |

## 7. Necesidad de solución

Se requiere una **aplicación de consola en Python** que:

- Centralice el registro de empleados, solicitudes de horas extras y horas
  compensadas.
- Permita la **aprobación o rechazo** de cada solicitud con un estado
  formal.
- Calcule de manera automática el **valor hora** y el **pago** de las
  horas extras aprobadas.
- Mantenga un **saldo** de horas compensadas por empleado y registre
  cuando el empleado las utiliza.
- Genere **reportes** que sirvan como soporte para el pago mensual y la
  auditoría interna.

## 8. Objetivo general

Desarrollar una aplicación de consola en Python que gestione y controle las
horas extras y las horas compensadas de los empleados de
Fábrica Marsar SRL, permitiendo el registro, la aprobación, el
cálculo de pago, el control de saldo y la generación de reportes.

## 9. Objetivos específicos

| # | Objetivo específico |
|---|---------------------|
| OE1 | Registrar y mantener actualizados los datos de los empleados. |
| OE2 | Registrar solicitudes de horas extras con fecha, cantidad de horas y motivo. |
| OE3 | Aprobar o rechazar solicitudes de horas extras con un estado formal. |
| OE4 | Calcular automáticamente el valor hora, el pago unitario y el pago total de horas extras aprobadas. |
| OE5 | Registrar horas compensadas otorgadas al empleado y mantener un saldo actualizado. |
| OE6 | Permitir que el empleado utilice horas compensadas respetando el saldo disponible. |
| OE7 | Generar reportes de empleados, horas extras, solicitudes pendientes y saldos. |
| OE8 | Controlar los datos de entrada con validaciones y excepciones personalizadas. |