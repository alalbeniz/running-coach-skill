# Running Coach

Skill de running y trail para planificar, analizar sesiones y ajustar entrenamiento usando Garmin mediante [MissingMCP](https://missingmcp.com/garmin). Fuerza, ciclismo y natación se consultan cuando apoyan el objetivo de carrera.

Una sola fuente de instrucciones sirve para ChatGPT Chat, Work, Codex y otros clientes capaces de cargar skills y usar MCP. La instalación disponible depende del cliente. La fase 1 no sincroniza memoria entre aplicaciones. El conector puede llamarse `@Garmin` o tener cualquier alias elegido por ti.

## Qué cambia en la fase 1

- Acceso directo al conector: sin Coach Memory MCP, skill Garmin intermedia, librería `garminconnect` local ni servidor propio.
- Primero se interpreta la petición. Una consulta conceptual no dispara lecturas de Garmin ni onboarding.
- Resúmenes antes que datos detallados; fechas acotadas, paginación y reutilización de contexto vigente.
- Perfil portable para objetivos y restricciones; Garmin conserva actividades, métricas y sesiones publicadas.
- Plan, workout, entrada de calendario y actividad son conceptos distintos. Crear un borrador no lo publica.
- La metodología se carga por temas, sin exigir shell, Python, archivos locales o subagentes al entrenador.

## Conectar Garmin

1. Conecta `https://missingmcp.com/garmin/mcp` desde la configuración de conectores/MCP de tu cliente y autentícate con el proveedor. [Guía de MissingMCP para ChatGPT](https://missingmcp.com/garmin/chatgpt).
2. Comprueba que el cliente expone las herramientas de lectura. Para publicar o reprogramar necesitas además las operaciones y permisos de escritura correspondientes.
3. Si ya tienes el conector Garmin de MissingMCP, reutilízalo. Selecciona tu complemento (por ejemplo `@Garmin`) en el chat. La skill identifica sus capacidades y utiliza sus herramientas reales; no fija su nombre técnico, URL, ID o prefijo ni crea otra conexión. `agents/openai.yaml` contiene solo metadatos de presentación.

Sin conector, el coach puede explicar conceptos y trabajar con los datos que aportes. Sin escritura, entrega un plan y explica que no lo ha programado.

## Instalar la skill y el plugin

### Codex y clientes con skills locales

Usa el directorio fuente que contiene `SKILL.md`, `references/` y `agents/`, o extrae `coach-skill.zip`. Instala la carpeta `coach` en la ubicación de skills que admite tu cliente. En Codex puede utilizarse `~/.agents/skills/coach/` o `.agents/skills/coach/` dentro de un proyecto. No hace falta ejecutar scripts para usarla.

Invócala como `$coach` en Codex. Si aparece en el selector de ChatGPT, puedes seleccionarla con `@`. Evita instalar simultáneamente la skill local y el plugin si eso produce dos entradas del mismo coach.

### Un Markdown para toda la conversación

Descarga [running-coach-chat.md](docs/running-coach-chat.md) y adjúntalo al comenzar un chat. Selecciona tu complemento, por ejemplo `@Garmin`, y escribe:

> Usa el documento adjunto como guía de coaching durante esta conversación. Mi conector es @Garmin.

Después puedes pedir planes, análisis o ajustes sin reenviar las instrucciones en cada mensaje mientras sigan disponibles en el contexto. El archivo contiene la skill y todas las referencias de coaching, con enlaces internos; no necesita otros archivos del repositorio. No instala una skill ni un conector y no garantiza memoria entre conversaciones o retención ilimitada del contexto.

La versión autocontenida carga más texto inicial que la modular. Para ahorrar contexto cuando el cliente admite instalación de skills, usa la versión modular. El Markdown se genera desde la misma fuente, no se mantiene a mano.

### ChatGPT Chat y Work

Para distribución entre superficies, utiliza el plugin generado `running-coach-plugin.zip`. Contiene `plugin.json`, la skill en `skills/coach/` y el manifiesto de compatibilidad `.codex-plugin/plugin.json`.

En escritorio, un plugin local se puede registrar en una fuente personal mediante `@plugin-creator` en Work o `$plugin-creator` en Codex, indicando la carpeta extraída `running-coach`. Después se instala desde esa fuente y se prueba en un chat nuevo. Este repositorio no modifica automáticamente tu marketplace.

El ZIP es un paquete de distribución, no una promesa de que cualquier ChatGPT admita importarlo directamente. La disponibilidad de fuentes locales varía por superficie; para distribución general en web/móvil se requiere el canal de plugins admitido por OpenAI. No se ha publicado este plugin en el directorio universal. Consulta [skills](https://learn.chatgpt.com/docs/build-skills) y [empaquetado de plugins](https://developers.openai.com/plugins/build/plugins).

En una sesión sin instalación de skills, usa el Markdown autocontenido descrito arriba. No activa descubrimiento automático ni equivale a una instalación del plugin.

## Perfil y continuidad

Empieza en un chat/proyecto de coaching y aporta el objetivo, disponibilidad y restricciones que no estén ya disponibles. El esquema está en [athlete-profile.md](references/athlete-profile.md). No hace falta completar todos sus campos ni crear un archivo local.

La indicación reciente del usuario prevalece para sus preferencias y disponibilidad. Las mediciones conservan fuente y fecha. El coach reutiliza el contexto visible, pero no presupone acceso a otros chats ni persistencia automática. Puedes llevar un resumen compacto a otra conversación. Solo afirma haber guardado un perfil cuando una herramienta confirma la escritura en un destino disponible y autorizado.

## Ejemplos

- «¿Qué es un tempo?»
- «Analiza mi última carrera y compárala con lo previsto».
- «Prepara la semana que viene; solo puedo correr martes, jueves y domingo».
- «Programa en Garmin las sesiones de este plan».
- «Mueve el entrenamiento del jueves al viernes».

El coach comprueba las escrituras y comunica resultados parciales. No interpreta una actividad del mismo día como prueba suficiente de haber completado una sesión prevista.

## Desarrollo y paquetes

La fuente editable es `SKILL.md` en la raíz junto con `references/` y `agents/`. No edites las copias generadas.

```sh
python3 scripts/build_packages.py
# Tras editar la fuente, actualiza también el documento versionado:
cp dist/running-coach-chat.md docs/running-coach-chat.md
python3 -m unittest discover -s tests -v
```

Python solo se usa para construir/verificar los paquetes, no durante el coaching. El constructor usa la biblioteca estándar, incluye la licencia y produce ZIP reproducibles y `running-coach-chat.md` en `dist/`. El manifiesto se mantiene en `packaging/plugin.json`; la copia compatible se genera a partir de él.

Las pruebas automáticas verifican el contenido y consistencia de los archivos instalables. Los escenarios de [validación](tests/scenarios.md) permiten evaluar decisiones del coach sin escribir en Garmin. Un paquete válido no prueba por sí solo la instalación en ChatGPT ni una escritura real en Garmin.

## Licencia y origen

Fork de [barcia/running-coach-skill](https://github.com/barcia/running-coach-skill), por Ivan Barcia. Se conserva [LICENSE](LICENSE), GPL-3.0. Se corrige el antiguo campo MIT del manifiesto de la skill para alinearlo con la licencia del repositorio.
