# AI_USAGE — Lab 2

## Entrada 1 — PRD

**Fecha:** 2026-09-10

**Objetivo:** Auditar `docs/prd/PRD.md` y documentar ambigüedades, riesgos de seguridad, incoherencias y otros errores en los requisitos.

**Herramienta y modelo:** Codex (GPT-5), mediante revisión asistida del documento Markdown.

**Contexto proporcionado:** PRD v1 de LegacyPay para consultar el historial de transacciones de un comercio autorizado durante los últimos 90 días, con filtros por fecha, estado y monto, paginación y uso de datos sintéticos.

**Salida obtenida:** Se añadieron comentarios de revisión en el PRD sobre codificación corrupta, autorización y aislamiento por comercio, protección de datos sensibles, semántica de filtros, ventana temporal, paginación, validación de errores, montos, prevención de abuso y requisitos no funcionales medibles.

**Problema detectado:** El documento dejaba decisiones críticas como preguntas abiertas y contenía criterios que admitían implementaciones inseguras o ambiguas, por ejemplo: confiar en un identificador de comercio del cliente, recortar en silencio períodos mayores a 90 días, paginar sin un cursor vinculado a la identidad y no definir una lista permitida de campos de respuesta. También presentaba texto con problemas de codificación.

**Cambio realizado por mí:** Incorporé comentarios accionables junto a los requisitos afectados, indicando la ambigüedad o riesgo y la definición o control que debe agregarse. No amplié el alcance funcional del PRD.

**Criterio o evidencia utilizada:** Consistencia interna entre alcance, reglas e historias de usuario; principio de mínimo privilegio y aislamiento multi-tenant; minimización de datos sensibles; validación de entradas; paginación estable; y requisitos verificables mediante criterios de aceptación.

**Pregunta todavía abierta:** ¿Cuál es el mecanismo concreto de autenticación y autorización que vincula la identidad solicitante con el comercio, y cuáles son los campos no sensibles que el contrato de respuesta permite exponer?
