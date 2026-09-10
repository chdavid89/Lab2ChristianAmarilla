Voy a revisar el borrador actual para conservar su contexto y luego entregar únicamente el PRD en Markdown, separando hechos, propuestas y preguntas abiertas.

Read 

# PRD v1: Historial de transacciones de LegacyPay

## 1. Visión y problema

### Hechos proporcionados

LegacyPay es una pasarela de pagos B2B. Un comercio autorizado necesita consultar el historial de sus transacciones correspondientes a los últimos 90 días.

La consulta debe permitir filtrar por:

- Fecha.
- Estado.
- Monto.

Los resultados deben presentarse de forma paginada y no deben exponer datos completos de tarjeta ni datos de autenticación. Para este caso se utilizarán únicamente datos sintéticos.

### Problema

Los comercios autorizados necesitan consultar y revisar sus transacciones recientes mediante una búsqueda acotada por período, estado y monto, sin acceder a información sensible.

### Propuesta

Proporcionar una consulta de historial que permita aplicar los filtros mínimos definidos y navegar los resultados mediante paginación, respetando el límite de 90 días y la protección de datos sensibles.

## 2. Alcance incluido y fuera de alcance

### Incluido

- Consulta del historial de transacciones de un comercio autorizado.
- Consulta limitada a los últimos 90 días.
- Filtro por fecha.
- Filtro por estado.
- Filtro por monto.
- Resultados paginados.
- Exclusión de datos completos de tarjeta.
- Exclusión de datos de autenticación.
- Uso de datos sintéticos para el caso.
- Validación de que quien consulta sea un comercio autorizado.

### Fuera de alcance

- Consulta de transacciones con una antigüedad superior a 90 días.
- Creación, edición o eliminación de transacciones.
- Procesamiento de nuevos pagos.
- Reembolsos, cancelaciones o disputas.
- Exportación de resultados.
- Reportes o análisis agregados.
- Exposición de datos completos de tarjeta.
- Exposición de datos de autenticación.
- Integraciones con sistemas externos no definidos.
- Definición de políticas regulatorias o internas no proporcionadas.

### PREGUNTA ABIERTA

- ¿La exportación de resultados debe incluirse en una versión futura?

## 3. Usuarios, entidades y reglas de negocio

### Usuarios

#### Comercio autorizado

Usuario que puede consultar el historial de transacciones asociado a su comercio.

### Entidades conceptuales

#### Comercio autorizado

Representa al comercio que realiza la consulta y tiene permiso para acceder al historial correspondiente.

#### Transacción

Representa una operación registrada en LegacyPay que puede ser consultada mediante fecha, estado y monto.

No se definen otros atributos de estas entidades en este borrador.

### Hechos y reglas de negocio

- Solo un comercio autorizado puede consultar transacciones.
- La consulta debe limitarse a los últimos 90 días.
- La consulta debe admitir filtros por fecha, estado y monto.
- Los resultados deben estar paginados.
- No deben mostrarse datos completos de tarjeta.
- No deben mostrarse datos de autenticación.
- Los datos utilizados en este caso deben ser sintéticos.
- El comercio no debe acceder a transacciones de otro comercio.

### PREGUNTAS ABIERTAS

- ¿Cómo se determina que un comercio está autorizado?
- ¿El período de 90 días se calcula desde la fecha actual de la consulta?
- ¿La fecha debe admitir un rango, una fecha exacta o ambas opciones?
- ¿Qué estados de transacción deben estar disponibles?
- ¿El filtro de monto debe admitir un valor exacto, un rango o ambas opciones?
- ¿Qué ocurre cuando no se proporcionan filtros?
- ¿Cuál es el tamaño de cada página?
- ¿Qué mecanismo de navegación debe utilizarse para la paginación?
- ¿Cuál debe ser el orden de los resultados?
- ¿Qué información no sensible de la transacción puede mostrarse?
- ¿Debe registrarse la consulta realizada por el comercio?

## 4. Historias de usuario con criterios de aceptación

### Historia 1: Consultar el historial

**Como** comercio autorizado,  
**quiero** consultar el historial de transacciones de mi comercio,  
**para** revisar operaciones realizadas durante los últimos 90 días.

#### Criterios de aceptación

- Dado un comercio autorizado, cuando realiza una consulta, entonces recibe transacciones correspondientes únicamente a su comercio.
- Dado un período de consulta, cuando está dentro de los últimos 90 días, entonces puede utilizarse para buscar transacciones.
- Cuando el período solicitado excede los últimos 90 días, entonces la consulta no debe devolver transacciones fuera de ese límite.
- Cuando no existen transacciones que coincidan con la consulta, entonces el resultado debe indicar que no hay resultados.

### Historia 2: Filtrar por fecha

**Como** comercio autorizado,  
**quiero** filtrar transacciones por fecha,  
**para** consultar un período específico dentro de los últimos 90 días.

#### Criterios de aceptación

- El comercio puede aplicar un filtro de fecha.
- El resultado solo incluye transacciones que cumplen el filtro de fecha.
- El filtro no permite consultar transacciones anteriores al límite de 90 días.

### Historia 3: Filtrar por estado

**Como** comercio autorizado,  
**quiero** filtrar transacciones por estado,  
**para** revisar únicamente las operaciones que me interesan.

#### Criterios de aceptación

- El comercio puede aplicar un filtro de estado.
- El resultado solo incluye transacciones que cumplen el estado seleccionado.
- Los estados disponibles deben corresponder a los estados definidos para el caso.

### PREGUNTA ABIERTA

- ¿Cuáles son los estados válidos para una transacción?

### Historia 4: Filtrar por monto

**Como** comercio autorizado,  
**quiero** filtrar transacciones por monto,  
**para** encontrar operaciones según su importe.

#### Criterios de aceptación

- El comercio puede aplicar un filtro de monto.
- El resultado solo incluye transacciones que cumplen el criterio de monto.
- Los valores inválidos para el filtro deben rechazarse.

### PREGUNTAS ABIERTAS

- ¿Qué formato y moneda debe utilizar el monto?
- ¿El filtro acepta montos exactos, mínimos, máximos o rangos?
- ¿Cuál es el comportamiento esperado para montos negativos o cero?

### Historia 5: Combinar filtros

**Como** comercio autorizado,  
**quiero** combinar filtros de fecha, estado y monto,  
**para** acotar la búsqueda de transacciones.

#### Criterios de aceptación

- El comercio puede utilizar más de un filtro en una misma consulta.
- El resultado cumple simultáneamente todos los filtros proporcionados.
- La consulta continúa limitada a los últimos 90 días.

### Historia 6: Navegar resultados paginados

**Como** comercio autorizado,  
**quiero** recibir los resultados paginados,  
**para** consultar el historial sin cargar todos los resultados a la vez.

#### Criterios de aceptación

- Los resultados se entregan en páginas.
- El comercio puede solicitar otra página cuando existan más resultados.
- La respuesta indica si existen resultados adicionales.
- La paginación conserva los filtros aplicados.

### PREGUNTAS ABIERTAS

- ¿Cuál es el tamaño predeterminado y máximo de página?
- ¿Debe permitirse que el comercio solicite un tamaño de página?
- ¿Qué formato debe tener la información de paginación?

### Historia 7: Proteger información sensible

**Como** comercio autorizado,  
**quiero** consultar transacciones sin acceder a datos sensibles,  
**para** revisar el historial sin exponer información completa de tarjeta ni datos de autenticación.

#### Criterios de aceptación

- La respuesta no contiene datos completos de tarjeta.
- La respuesta no contiene datos de autenticación.
- La consulta no permite recuperar esos datos mediante filtros o paginación.
- Los datos utilizados para validar este comportamiento son sintéticos.

## 5. Restricciones no funcionales

### Hechos proporcionados

- No deben exponerse datos completos de tarjeta.
- No deben exponerse datos de autenticación.
- Deben utilizarse únicamente datos sintéticos para este caso.
- La consulta debe estar limitada a los últimos 90 días.
- La consulta debe ser paginada.
- El acceso está restringido a comercios autorizados.

### PREGUNTAS ABIERTAS

- ¿Qué requisitos de autenticación debe cumplir el usuario?
- ¿Qué requisitos de autorización deben aplicarse?
- ¿Qué tiempo máximo de respuesta se espera?
- ¿Qué volumen de transacciones debe soportarse?
- ¿Qué disponibilidad se requiere?
- ¿Qué nivel de auditoría o trazabilidad se necesita?
- ¿Qué formato de fecha debe utilizarse?
- ¿Qué zona horaria debe aplicarse?
- ¿Qué formato debe tener la respuesta?
- ¿Qué comportamiento debe presentarse ante errores o consultas inválidas?
- ¿Qué requisitos de accesibilidad son necesarios?
- ¿Qué políticas internas o regulatorias aplican?

## 6. Preguntas abiertas

- ¿Cómo se identifica y valida a un comercio autorizado?
- ¿Cómo se calcula exactamente la ventana de 90 días?
- ¿Qué formato debe tener el filtro de fecha?
- ¿Qué estados de transacción existen?
- ¿Qué formato, moneda y operadores debe admitir el filtro de monto?
- ¿Qué campos no sensibles de una transacción deben mostrarse?
- ¿Cuál debe ser el orden de los resultados?
- ¿Cuál es el tamaño de página?
- ¿Qué mecanismo de paginación debe utilizarse?
- ¿Se permiten consultas sin filtros?
- ¿Qué mensajes deben mostrarse cuando no hay resultados?
- ¿Qué requisitos de autenticación y autorización aplican?
- ¿Debe registrarse la actividad de consulta?
- ¿Qué volumen, tiempo de respuesta, disponibilidad y formato de respuesta se esperan?
- ¿Qué políticas internas o regulatorias deben considerarse?
- ¿La exportación o generación de reportes será parte de una versión futura?