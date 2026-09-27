# Perfil lógico del atleta

Usa este esquema solo cuando personalizar, planificar o mantener continuidad lo requiera. Puede existir en el contexto de la conversación, en una función de memoria del host o en un documento que el usuario elija. No presupongas una ruta ni una memoria compartida entre ChatGPT Chat, Work y Codex.

## Reglas de verdad

- La indicación explícita más reciente del usuario sobre objetivo, disponibilidad, salud o preferencias prevalece sobre lo guardado. Conserva la fecha y la fuente si se conocen.
- Los datos Garmin son hechos medidos con fecha y procedencia, no identidad permanente del atleta. Resume tendencias estables; evita guardar snapshots efímeros como si siguieran vigentes.
- Marca desconocidos como `desconocido`. No rellenes huecos con promedios, defaults o inferencias no declaradas.
- Distingue valores **medidos**, **estimados** y **declarados por el usuario**. Las zonas estimadas nunca sustituyen en silencio unas zonas medidas.
- Solo di que el perfil fue guardado o actualizado cuando una escritura se haya confirmado.

## Esquema

### Identidad y contexto

- Nombre o forma de dirigirse al atleta, idioma y zona horaria, si son útiles.
- Edad o año de nacimiento, altura y peso, solo si el usuario los aporta y resultan pertinentes.
- Condiciones médicas activas, dolor o limitaciones; historial de lesiones relevante.

### Objetivos vigentes

- Objetivo principal, fecha, distancia, desnivel o marca deseada.
- Carreras de preparación y prioridad A/B/C.
- Fecha y fuente de cada cambio de objetivo.

### Disponibilidad

- Días, horarios y duración real disponibles.
- Restricciones fijas, viajes y otras cargas vitales.
- Preferencias: tirada larga, descanso, superficie y horario.
- Fuerza, ciclismo, natación u otros deportes ya comprometidos.

### Historial y capacidad

- Experiencia, volumen reciente, frecuencia y terreno habitual.
- Marcas o tests relevantes con fecha.
- Ritmos conversacionales, RPE calibrado y potencia, si existen.
- Zonas de FC, FC máxima, umbral, VO2max o FTP con fecha, fuente y método.
- Dispositivo y equipamiento que afecten al plan.

### Recuperación y tolerancia

- Baselines estables de HRV, FC en reposo y sueño, con intervalo usado para estimarlos.
- Respuesta conocida a carga, calor, altitud y fuerza.
- Preferencias y tolerancias de nutrición e hidratación relevantes.
- Patrones observados con fecha y evidencia; retira los que hayan dejado de aplicar.

### Preferencias de trabajo

- Estilo de feedback y nivel de detalle.
- Prioridad entre datos y sensaciones.
- Reglas expresas para publicar o programar workouts. La autorización explícita puede mantenerse durante el flujo y sus turnos relacionados; no la extiendas a planes futuros no solicitados.

## Estado temporal opcional

Si ayuda al trabajo actual, mantén fase, foco del bloque, carga reciente, fatiga y próxima carrera. Fecha siempre este estado y no lo trates como perfil permanente. Registra la disponibilidad temporal con inicio y caducidad para que no reemplace las preferencias estables una vez vencida.
