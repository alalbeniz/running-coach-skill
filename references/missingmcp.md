# Garmin mediante MissingMCP

Usa las herramientas Garmin disponibles directamente en el host. Los nombres estables de esta guía son los sufijos sin prefijo; el host puede exponerlos con un namespace distinto. Descubre la herramienta y su esquema real en el entorno actual. No inventes parámetros, enums ni estructuras JSON a partir de esta referencia.

## Selección por necesidad

| Necesidad | Herramienta estable | Uso eficiente |
|---|---|---|
| Actividades de un intervalo | `get_activities_by_date` | Rango acotado, filtro de deporte y página pequeña. Continúa solo mientras `has_more` y la pregunta lo exija. |
| Detalle de una actividad | `get_activity` | Después de identificar el `activity_id`. |
| Vueltas resumidas o completas | `get_activity_split_summaries`, `get_activity_splits` | Empieza por resumen; carga splits completos solo para pacing o estructura. |
| Estado y carga | `get_training_status` | Fecha concreta pertinente. |
| Readiness | `get_training_readiness` | Complemento, nunca única base de decisión. |
| Sueño diario o tendencia | `get_sleep_summary`, `get_sleep_summary_range` | Diario para hoy; rango corto para tendencia. |
| HRV diario o tendencia | `get_hrv_data`, `get_hrv_trend` | En `get_hrv_data`, usa `return_timeseries=false` salvo que la serie sea imprescindible. |
| Carreras y eventos | `get_calendar_events` | Intervalo futuro relevante. No confundir con workouts. |
| Sesiones programadas | `get_scheduled_workouts` | Intervalo exacto que se revisa o modifica. |
| Biblioteca de workouts | `get_workouts`, `get_workout_by_id` | Lista resumida primero; detalle solo del candidato. |
| Crear una carrera continua simple | `create_run_workout` | Cuando su estructura cubra exactamente la sesión. Ya sube la plantilla. |
| Subir plantillas | `upload_workout`, `upload_workouts` | Solo tras petición explícita de publicación. |
| Programar plantillas | `schedule_workout`, `schedule_workouts` | Usa `workout_id`; verifica después en un rango corto. |
| Quitar del calendario | `unschedule_workout`, `unschedule_workouts` | Usa `scheduled_workout_id`; conserva la plantilla de biblioteca. |

## Lectura y reutilización

Empieza por respuestas resumidas y rangos de fechas mínimos. Reutiliza datos frescos obtenidos en la misma interacción cuando cubran la misma fecha y necesidad. Amplía el rango, pagina o abre detalle únicamente si la respuesta depende de ello.

Para vincular plan y actividad, prefiere un identificador explícito. Si no existe, exige coherencia suficiente de deporte, hora, duración y estructura. La misma fecha no demuestra la relación. Un hueco en Garmin tampoco prueba que el atleta se saltó la sesión.

## Escrituras y verificación

Crear un plan o borrador no autoriza a escribir en Garmin. Una petición explícita de subir, programar, reprogramar o retirar sí autoriza la operación necesaria y sus verificaciones; no repitas solicitudes de permiso.

Antes de crear, consulta la biblioteca y reutiliza una plantilla equivalente. Tras cada escritura, lee un intervalo acotado o el workout concreto para confirmar el estado real.

- `workout_id` identifica la plantilla de biblioteca.
- `scheduled_workout_id` identifica una entrada del calendario y es el valor requerido para desprogramar.
- `activity_id` identifica una actividad realizada.

No reintentes a ciegas una subida o programación cuyo resultado sea ambiguo: primero reconcilia biblioteca y calendario para evitar duplicados. Haz como máximo una nueva lectura acotada si la primera verificación sigue sin resolver el resultado; después detente, informa de la ambigüedad y no vuelvas a escribir. En operaciones por lotes, inspecciona el resultado por elemento, verifica lo creado y reintenta solo los fallidos confirmados.

## Mover una sesión

Si el host ofrece una operación nativa de mover, úsala y verifica. Si no:

Si origen y destino son la misma fecha, trátalo como ya programado y no desprogrames nada. Identifica la entrada exacta que se mueve; no retires otras sesiones aunque compartan fecha o plantilla.

1. identifica la plantilla y el `scheduled_workout_id` originales;
2. programa el mismo `workout_id` en la fecha destino;
3. verifica que la entrada destino existe;
4. desprograma la entrada antigua con su `scheduled_workout_id`;
5. verifica ambas fechas.

Si el alta destino funciona y la retirada antigua falla, reconcilia una vez bajo la autorización ya concedida. Reintenta la retirada solo si el fallo está confirmado y la entrada exacta sigue vigente; que su ID aparezca en un índice posiblemente retrasado no basta. Si el estado sigue ambiguo, detente e informa del resultado parcial. No borres la plantilla de la biblioteca para moverla.

## Workout estructurado

Obtén el esquema de la descripción de la herramienta o de los recursos que exponga el host. Conserva la intención del plan: calentamiento, bloques, recuperaciones, repeticiones, enfriamiento y objetivo de intensidad. Tras subir, abre el workout y comprueba nombre, deporte, pasos, repeticiones, duraciones o distancias y targets; después prográmalo y verifica el calendario.
