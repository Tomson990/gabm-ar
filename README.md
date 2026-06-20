# GABM-AR: Simulación de identidad política con agentes generativos

**TL;DR:** Un experimento de Generative Agent-Based Modeling (GABM) — 24 agentes
sintéticos impulsados por LLM, con identidad política e historial propios, expuestos
secuencialmente a eventos reales del mandato de Javier Milei (2023-2026). El objeto
de estudio **no es predecir el resultado de ninguna elección** — es observar, en un
laboratorio controlado, cómo un modelo de lenguaje representa el sesgo de
confirmación y la resistencia identitaria al cambio de opinión política, y qué
limitaciones metodológicas aparecen al intentar medir eso.

---

## ⚠️ Qué es esto y qué NO es

- **Es:** una exploración metodológica sobre cómo simular dinámicas de opinión con
  agentes generativos, usando un caso real como banco de pruebas.
- **No es:** una encuesta, un sondeo, ni una predicción electoral. 24 agentes
  sintéticos no son una muestra representativa de la población argentina.
- **No es:** una toma de posición política propia. Los nombres de figuras y partidos
  reales (Milei, LLA, UxP, JxC) se usan porque dan anclaje verificable a los eventos
  --no como juicio sobre ellos. El objeto de análisis es el comportamiento del modelo,
  no la política argentina en sí.

## El problema que esto explora

¿Qué hace falta para que un modelo de lenguaje, actuando como agente con una
identidad política previa, cambie de "opinión" frente a evidencia nueva? Y más
interesante todavía: ¿ese cambio se parece a cómo cambian (o no cambian) las personas
reales?

## Diseño del experimento

### Los agentes
24 perfiles sintéticos con variables demográficas (edad, provincia, educación,
ocupación, nivel de ingreso), político-electorales (voto 2023, rasgo de personalidad
respecto al cambio de opinión) y de consumo informativo (TV+WhatsApp, redes
segmentadas por plataforma, streaming político, radio/diario, boca en boca) —
generadas con distribución aleatoria ponderada, no representativa.

### La memoria histórica compartida
Un resumen de ~380 palabras de los hitos del mandato (dic-2023 a jun-2026), inyectado
como contexto común a todos los agentes — el "punto de partida" de lo que cualquier
ciudadano informado ya sabría.

### El mecanismo de "framing" por canal
Cada evento real se adapta, vía LLM, a 6 versiones distintas según cómo llegaría por
cada canal informativo — no es el mismo texto para todos los agentes, sino una
simulación de cómo el mismo hecho se deforma/enfatiza distinto según el medio.

### Las rondas
Cada ronda introduce un evento real verificado por búsqueda web (no inventado), y
cada agente actualiza su intención de voto/score de afinidad con un razonamiento
explícito de por qué cambia o no cambia.

## Hallazgos (resumen — ver `HALLAZGOS.md` para el detalle completo con evidencia)

1. **Sesgo de confirmación motivado:** ante el mismo evento con señales mixtas, cada
   bloque identitario selecciona el dato que confirma su postura previa y descarta o
   reinterpreta el resto.
2. **Saturación categórica:** con un esquema de clasificación discreta (LLA/UxP/JxC/
   blanco/otro), el voto en blanco actúa como una "trampa absorbente" — una vez
   alcanzado, ningún evento nuevo, sin importar su severidad, logra sacar a un agente
   de ahí, simplemente porque no hay categoría "más allá".
3. **Erosión gradual real pero lenta:** cambiando a un esquema de scores continuos
   (afinidad 0-100 por espacio), se detecta desgaste genuino y motivado en el núcleo
   más "duro" de cada espacio — pero de magnitud pequeña por evento, sugiriendo que
   el modelo representa el cambio de identidad política como proceso acumulativo
   lento, no como un interruptor que un solo evento (por contundente que sea) activa.

## Stack

- Python 3 + API de Anthropic (Claude Sonnet)
- Sin frameworks de agentes (LangGraph, CrewAI, etc.) — loop propio simple,
  deliberadamente, para mantener visibilidad total sobre cada paso del razonamiento.
- Búsqueda web para verificar cada evento antes de inyectarlo (no se inventó ningún
  hecho político o económico — todos están sourceados).

## Estructura del repo

```
generar_perfiles.py       # genera los 24 agentes sintéticos
memoria_base.py           # contexto histórico compartido
generar_eventos.py        # adapta cada evento real a 6 framings por canal
motor_agente.py           # esquema categórico (intención de voto discreta)
motor_agente_continuo.py  # esquema continuo (scores de afinidad 0-100)
ejecutar_ronda.py         # corre una ronda categórica completa
ejecutar_ronda_continua.py # corre una ronda continua completa
HALLAZGOS.md              # documento completo de hallazgos con evidencia citada
```

## Limitaciones explícitas

- Muestra sintética de 24 agentes — no representativa, no proyectable.
- El esquema categórico tiene un sesgo estructural hacia la estabilidad aparente
  (ver hallazgo #2) — cualquier conclusión sobre "estabilidad" debe leerse con esa
  salvedad.
- Solo 6 rondas categóricas + 1 ronda continua — insuficiente para trazar una curva
  de desgaste real; el Experimento 3 abre más preguntas de las que cierra.
- Un solo modelo de lenguaje (Claude Sonnet) - no se comparó contra otros LLMs para
  ver si el patrón es propio del modelo o generalizable.

## Por qué este proyecto

Nace de una pregunta más amplia: ¿puede usarse IA generativa para modelar dinámicas
sociales colectivas con algo del espíritu de la "psicohistoria" de Asimov — no para
predecir el futuro con precisión, sino para encontrar patrones de comportamiento
colectivo que no son obvios mirando el sistema desde arriba? Este repo es un primer
paso modesto y honesto sobre sus propios límites en esa dirección.
