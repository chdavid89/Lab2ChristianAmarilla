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


## Auditoría del ERD

- **¿Cada entidad está justificada por el PRD?**  
  **Sí, parcialmente.** `COMERCIO` y `TRANSACCION` se desprenden del requisito de que un comercio autorizado consulte sus propias transacciones. La relación entre ambas también es coherente con el aislamiento por comercio.

- **¿La IA convirtió un atributo o estado en tabla?**  
  **No.** `estado` está modelado correctamente como atributo de `TRANSACCION`, no como entidad independiente. Lo mismo ocurre con fecha, monto y moneda.

- **¿Las cardinalidades coinciden con las reglas conocidas?**  
  **Son compatibles, pero no están confirmadas explícitamente.**  
  `COMERCIO ||--o{ TRANSACCION` significa que un comercio puede tener cero o muchas transacciones y que cada transacción pertenece a un comercio. El PRD exige aislamiento por comercio, pero no define formalmente estas cardinalidades; deben considerarse una propuesta.

- **¿Se agregaron entidades o campos no confirmados?**  
  **Sí, como propuestas explícitas.** El ERD agrega:
  - `comercio_id`
  - `transaccion_id`
  - `fecha`
  - `estado`
  - `monto`
  - `moneda`

  Todos están marcados como `Propuesto`, por lo que no se presentan como hechos confirmados. Son razonables para soportar filtros, orden y aislamiento, pero requieren validación.

- **¿Aparecen datos sensibles innecesarios?**  
  **No.** El ERD no incluye número completo de tarjeta, CVV/CVC, PIN, credenciales ni datos de autenticación. `transaccion_id` y `comercio_id` no son sensibles por sí mismos, aunque su exposición y uso deben controlarse.

- **¿El diagrama renderiza correctamente?**  
  **La sintaxis Mermaid es válida y debería renderizar correctamente.** Usa `erDiagram`, entidades, atributos, claves y cardinalidad con una sintaxis compatible. No se observan errores estructurales evidentes.

- **¿Los supuestos y preguntas abiertas están visibles?**  
  **Sí.** Aparecen inmediatamente debajo del diagrama en `erd.md`, incluyendo:
  - El carácter derivado de la relación.
  - El carácter propuesto de los campos.
  - Los estados válidos.
  - El significado y zona horaria de la fecha.
  - La moneda y precisión del monto.
  - Los campos adicionales permitidos.
  - La vinculación entre identidad autenticada y comercio.

## Conclusión

El ERD es prudente: contiene solo dos entidades y no incorpora datos sensibles. Su principal riesgo es que varios campos y la cardinalidad son propuestas, no decisiones confirmadas del PRD. Deben mantenerse claramente etiquetados como tales hasta resolver las preguntas abiertas.

Voy a localizar el diagrama de secuencia, el ERD y el PRD para contrastar el flujo real con los criterios de auditoría, y después revisaré la sintaxis del diagrama para detectar problemas de renderizado.

Searched for files matching `**/*.{md,mmd,mermaid,drawio}`, 22 matches

Searched for regex `sequenceDiagram|erDiagram|autoriz|transaccion|transacción` (`**/*.{md,mmd,mermaid}`), 125 results

Encontré un diagrama de secuencia dedicado y un ERD separado; además, el PRD vigente contiene advertencias sobre autorización y campos faltantes. Ahora los voy a leer completos en conjunto para distinguir incumplimientos reales de decisiones que siguen marcadas como abiertas.

Read 

Read 

Read 

Read 

## Auditoría de la secuencia

- **¿La autorización ocurre antes de consultar datos?**  
  **Sí.** La API valida identidad y comercio antes de invocar al servicio y al repositorio. El acceso al repositorio ocurre únicamente dentro de la rama autorizada en `secuence_historial.md`.

- **¿Cada participante está justificado?**  
  **Sí, con una observación.**
  - `Comercio`: inicia la consulta.
  - `API`: recibe la solicitud y devuelve la respuesta.
  - `Autorizacion`: valida identidad y alcance del comercio.
  - `Servicio`: valida filtros y regla de 90 días.
  - `Repositorio`: recupera las transacciones.
  
  La autorización aparece como componente conceptual, pero el PRD todavía deja abierta la forma concreta de autenticación y autorización.

- **¿El orden de mensajes es coherente?**  
  **Sí.** El flujo es coherente:
  1. El comercio solicita el historial.
  2. La API valida identidad y comercio.
  3. Se rechaza o continúa según el resultado.
  4. Se validan filtros y límite temporal.
  5. Se consultan datos paginados.
  6. La respuesta vuelve al comercio.

- **¿Existe al menos un flujo de error?**  
  **Sí.** Hay dos:
  - Identidad o comercio inválidos.
  - Filtros inválidos o fuera del límite de 90 días.

  Falta explicitar si corresponden a errores `401`, `403` u otro contrato, pero eso está correctamente marcado como pregunta abierta en `PRD.md`.

- **¿Coincide con el PRD y el ERD?**  
  **Coincide parcialmente.**
  - Coincide con el PRD en autorización previa, filtros, límite de 90 días, paginación y aislamiento por comercio.
  - Coincide con el ERD en la relación `COMERCIO`–`TRANSACCION` y en los campos propuestos para fecha, estado, monto y moneda.
  - La secuencia introduce `credencial`, identidad, autorización y alcance de comercio, pero esos mecanismos siguen abiertos en el PRD y no están representados en el ERD.
  - El ERD incluye `moneda`, mientras que el PRD aún no define formalmente moneda, precisión ni operadores del filtro de monto.
  - La secuencia no muestra explícitamente la protección de datos sensibles en la respuesta. Debería quedar indicado que el servicio devuelve únicamente campos permitidos, sin datos completos de tarjeta ni autenticación.

- **¿El diagrama renderiza?**  
  **Sí, la sintaxis Mermaid presentada es válida y debería renderizarse.** Usa correctamente `sequenceDiagram`, `actor`, `participant`, `alt`, mensajes y cierres de bloques. La única verificación pendiente es visual en el visor Mermaid concreto utilizado por el repositorio; no se detectan errores sintácticos evidentes.

## Conclusión

La secuencia es coherente como primer borrador y cumple los controles principales. Antes de considerarla alineada por completo, conviene agregar explícitamente la respuesta sin datos sensibles y resolver el contrato de autenticación/autorización, los códigos de error y la definición de los campos expuestos.


Voy a auditar el ADR que está abierto, verificando cada criterio contra el texto real y señalando cualquier ambigüedad entre alternativas, decisión y evidencia.

Read 

## Auditoría del ADR

- **¿Las alternativas son realmente diferentes?**  
  **Sí, aunque la alternativa 3 se solapa parcialmente con la 2.**
  - `offset` depende de una posición numérica.
  - `cursor` encapsula la posición y puede asociarse a filtros, comercio y orden.
  - `clave estable` usa directamente los valores del último registro para continuar.

  La paginación por cursor puede implementarse internamente mediante una clave estable, por lo que convendría aclarar que son estrategias de contrato distintas, aunque técnicamente puedan combinarse.

- **¿La decisión se relaciona con los criterios?**  
  **Sí.**
  - Rendimiento ante crecimiento: evita offsets grandes.
  - Facilidad de implementación: reconoce que es más compleja.
  - Experiencia de usuario: acepta que no permite saltar fácilmente a una página arbitraria.
  - Costo de cambio: identifica la necesidad de validar el contrato y el modelo de datos.
  - Evidencia pendiente: incluye volumen, patrones de uso, persistencia y pruebas comparativas.

  La relación está presente de forma cualitativa, sin convertirla en una matriz de puntuación no respaldada por evidencia.

- **¿Se inventaron benchmarks o tiempos?**  
  **No.** El ADR declara explícitamente que no existen benchmarks, volúmenes máximos ni SLA aprobados. Las afirmaciones de rendimiento están expresadas como consecuencias esperadas, no como cifras.

- **¿Incluye consecuencias negativas honestas?**  
  **Sí.** Reconoce:
  - Mayor complejidad.
  - Imposibilidad práctica de saltar a páginas arbitrarias.
  - Necesidad de validar cursores.
  - Dependencia de un orden estable aún no confirmado.
  - Posibles cambios posteriores del contrato.

- **¿Se indica qué evidencia falta?**  
  **Sí, de forma suficiente.** Se enumeran datos de volumen, crecimiento, patrones de consulta, necesidad de navegación directa, campos para el orden, comportamiento ante inserciones, límites de página, auditoría, persistencia y compatibilidad.

- **¿Existe una condición concreta de revisión?**  
  **Sí, aunque puede hacerse más operativa.** El ADR define revisión cuando:
  - Aparezca la necesidad de saltar a páginas arbitrarias.
  - No pueda garantizarse un orden estable.
  - Se requiera compatibilidad con offset.
  - Las pruebas contradigan el comportamiento esperado.
  - Cambien los requisitos de auditoría o del contrato.

  No establece umbrales numéricos, pero eso es correcto porque todavía no existen SLA ni benchmarks aprobados.

## Conclusión

El ADR cumple los criterios y evita inventar evidencia. La única mejora recomendable es aclarar que `cursor` y `clave estable` pueden ser mecanismos relacionados, y convertir la revisión en un punto formal de decisión después de obtener la evidencia pendiente.