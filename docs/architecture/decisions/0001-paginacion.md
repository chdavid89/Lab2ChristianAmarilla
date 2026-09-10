# ADR: Estrategia de paginación para el historial de transacciones

## Contexto

La consulta de historial de transacciones de LegacyPay debe ser paginada porque la cantidad de datos puede crecer significativamente por comercio.

El endpoint debe ser auditable. La estrategia elegida debe permitir identificar de forma consistente qué resultados fueron consultados, con qué filtros y en qué orden.

No se cuenta todavía con benchmarks, volúmenes máximos, SLA ni una decisión sobre el contrato definitivo de la API.

## Alternativas

### 1. Paginación por offset

El cliente solicita una página y una cantidad de elementos mediante parámetros como `offset` y `limit`.

**Ventajas:**

- Implementación sencilla.
- Fácil comprensión para consumidores del endpoint.
- Permite navegar directamente a una posición aproximada.

**Desventajas:**

- Puede requerir recorrer o descartar muchos registros cuando el offset crece.
- Los cambios en los datos entre consultas pueden producir duplicados u omisiones.
- La auditoría de una consulta puede ser menos precisa si no se conserva el estado del conjunto consultado.

### 2. Paginación por cursor

La primera consulta devuelve un cursor que el cliente utiliza para solicitar la página siguiente.

**Ventajas:**

- Evita depender de offsets grandes.
- Se adapta mejor al crecimiento de datos.
- Puede asociar el cursor con el comercio, los filtros y el orden utilizados.
- Favorece una navegación consistente y auditable.

**Desventajas:**

- Es más compleja de implementar.
- No facilita saltar directamente a una página arbitraria.
- Requiere definir el formato, expiración y validación del cursor.

### 3. Paginación por clave estable

La página siguiente se obtiene usando los valores del último registro recibido, junto con un orden determinista.

**Ventajas:**

- Puede funcionar bien con grandes volúmenes.
- Reduce la dependencia de posiciones calculadas.
- Facilita evitar duplicados cuando existe una clave de orden estable.

**Desventajas:**

- Requiere definir una combinación de campos con orden total y estable.
- Puede ser menos familiar para consumidores del endpoint.
- Cambios en los filtros o en el orden invalidan la posición anterior.
- El contrato de la API puede terminar teniendo responsabilidades similares a un cursor.

## Decisión propuesta

Adoptar **paginación por cursor**, condicionada a validar que el contrato de datos permita definir un orden estable y reproducible.

Como propuesta de contrato:

- La primera consulta utiliza los filtros permitidos y un tamaño de página.
- La respuesta incluye los resultados y, si corresponde, un cursor para continuar.
- Las solicitudes posteriores utilizan el cursor sin modificar los filtros ni el orden originales.
- El cursor debe estar asociado al comercio autorizado, los filtros y el orden de la consulta.
- La respuesta no debe incluir datos completos de tarjeta ni datos de autenticación.
- El orden de los resultados debe ser determinista.
- El tamaño de página y cualquier límite máximo quedan pendientes de definición.

Esta decisión es una propuesta para el ADR. Debe confirmarse después de validar el modelo de datos, el contrato del endpoint y la evidencia de uso esperada.

## Consecuencias positivas

- Mejor comportamiento esperado frente al crecimiento de transacciones por comercio.
- Menor dependencia de offsets grandes.
- Mayor posibilidad de reproducir y auditar la navegación de resultados.
- Reduce el riesgo de inconsistencias al insertar nuevos registros entre consultas, siempre que se defina correctamente el orden.
- Mantiene el alcance de cada consulta ligado a los filtros y al comercio autorizado.

## Consecuencias negativas

- Mayor complejidad de implementación que la paginación por offset.
- No permite navegar directamente a una página arbitraria.
- Requiere definir reglas para cursores inválidos, expirados o reutilizados con otros filtros.
- Requiere un orden estable basado en campos que todavía no están confirmados.
- Puede requerir cambios posteriores si el contrato de datos no soporta una clave de orden adecuada.

## Evidencia pendiente

- Volumen actual y crecimiento esperado de transacciones por comercio.
- Distribución de tamaños de consulta.
- Consultas esperadas con y sin filtros.
- Necesidad real de saltar a una página específica.
- Campos disponibles para establecer un orden estable.
- Comportamiento esperado cuando se insertan nuevas transacciones entre páginas.
- Tamaño predeterminado y máximo de página.
- Expiración y reutilización permitida de los cursores.
- Requisitos de auditoría para reconstruir una consulta.
- Pruebas comparativas de costo y tiempo entre offset y cursor.
- Restricciones del motor de persistencia utilizado.
- Requisitos de compatibilidad con consumidores existentes, si los hubiera.

## Condición de revisión

Revisar esta decisión cuando se disponga de evidencia sobre volumen, crecimiento, patrones de uso y capacidades del almacenamiento.

También debe revisarse si:

- El endpoint necesita navegación directa a páginas arbitrarias.
- El orden estable requerido no puede implementarse de forma confiable.
- Los consumidores requieren compatibilidad con paginación por offset.
- Las pruebas muestran que la estrategia elegida no satisface el crecimiento esperado.
- Cambian los requisitos de auditoría o del contrato del endpoint.