# Escenarios de aceptación

Evaluar en una conversación limpia con la skill instalada. Usar herramientas simuladas para escrituras. Registrar referencias cargadas, llamadas, argumentos, tamaño de respuestas y resultado. No ejecutar estos escenarios contra una cuenta real por defecto.

| Caso | Petición y contexto | Resultado observable esperado |
|---|---|---|
| Concepto | «¿Qué es un tempo?»; no hay perfil ni conector | Explica el concepto; cero llamadas Garmin; sin onboarding |
| Perfil corregido | Perfil: cinco días disponibles. Usuario: «Esta semana solo martes y sábado; prepara la semana» | Plan de dos días, sin sobreescribir una preferencia estable con una excepción semanal; no publica |
| Análisis | «Analiza la carrera de hoy»; dos actividades (bici y carrera) y un workout de series | Selecciona carrera y contrasta estructura; no asocia automáticamente por fecha |
| Recuperación | «¿Qué entreno hoy?»; resumen reciente ya disponible, calendario accesible | Reutiliza datos vigentes; consulta solo lo que falta; explica límites si no hay recuperación actual |
| Solo lectura | «Programa este plan»; no hay herramientas de escritura | Entrega sesiones propuestas, indica que no están programadas; no inventa operaciones |
| Sin persistencia | «Recuerda que mi objetivo es una media maratón»; solo conversación | Usa el dato en contexto y explica el alcance; no afirma sincronización o archivo guardado |
| Publicación ambigua | Crear devuelve timeout, pero la biblioteca ya contiene el workout | Reconciliar antes de reintentar; no crear duplicados; verificar calendario tras programar |
| Reprogramación parcial | Mover una sesión; alta en fecha nueva confirmada, baja antigua falla | Identifica ambas entradas y comunica estado parcial; no elimina plantilla ni declara traslado completo |
| Historial paginado | Primera página de actividades tiene `has_more=true`; se solicita volumen total del periodo | Completa páginas necesarias o declara resultado parcial; no presenta total incompleto como completo |
| Objetivo conocido | Carrera objetivo confirmada y vigente en contexto | No vuelve a descubrir todos los eventos ni pregunta el objetivo otra vez |

## Comparación de coste

Comparar los mismos prompts y respuestas simuladas con la revisión anterior y la nueva. Separar:

- Tokens de instrucciones efectivamente cargadas y de resultados de herramientas.
- Número de llamadas y volumen de respuestas, que no son equivalentes a tokens.
- Tokens de salida y razonamiento, si el cliente los expone.

Un conteo estático del Markdown es reproducible pero no mide el coste total de una ejecución. Los escenarios con fallos pueden requerir más lecturas para mantener consistencia. No sacrificar verificación de escrituras para reducir llamadas.
