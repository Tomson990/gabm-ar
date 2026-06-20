"""
Motor de razonamiento de agentes - VERSIÓN CONTINUA. En vez de pedir una única
categoría discreta de intención de voto, pide un score de afinidad 0-100 para
cada espacio político (LLA, UxP, JxC, otro/provincial) más una probabilidad de
no-voto, todos sumando 100. Esto permite detectar erosión interna del núcleo que
el esquema categórico no deja ver (ej: un agente puede bajar de LLA=85 a LLA=60
sin que la categoría dominante cambie).

Pensado para re-medir el estado actual de los agentes (post Ronda 5 del esquema
categórico) y ver si hay movimiento oculto, sin descartar el historial ya
construido en motor_agente.py.

Requiere variable de entorno ANTHROPIC_API_KEY.
"""

import os
import json
import time
import anthropic
from memoria_base import MEMORIA_BASE_HISTORICA

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODELO = "claude-sonnet-4-6"

SYSTEM_PROMPT_CONTINUO = """Sos un simulador de razonamiento ciudadano para un \
experimento de investigación en ciencias sociales computacionales (GABM - \
Generative Agent-Based Modeling). Tu tarea es encarnar a UN agente sintético con el \
perfil exacto que se te da, y razonar COMO ESA PERSONA razonaría ante la información \
que recibe - no como un analista neutral, no como un asistente. El agente puede \
tener sesgos, puede razonar de forma motivada, puede ignorar evidencia que no le \
convenga - así razona la gente real.

A DIFERENCIA de una intención de voto única, ahora tenés que estimar un SCORE DE \
AFINIDAD (0 a 100) para cada uno de estos cuatro espacios políticos, MÁS una \
probabilidad de no-voto/blanco, de forma que los cinco valores SUMEN EXACTAMENTE 100:
- LLA (La Libertad Avanza)
- UxP (Unión por la Patria)
- JxC (Juntos por el Cambio)
- otro/provincial
- voto en blanco/no vota

Esto permite capturar erosión o fortalecimiento GRADUAL, no solo saltos completos \
de categoría. Por ejemplo: un agente que viene sosteniendo LLA con convicción puede \
pasar de {"LLA": 85, "UxP": 5, "JxC": 0, "otro": 0, "blanco": 10} a \
{"LLA": 65, "UxP": 5, "JxC": 0, "otro": 0, "blanco": 30} si el evento de esta ronda \
le generó dudas reales, AUNQUE LLA siga siendo su valor más alto (su "categoría \
dominante" no cambiaría, pero el score interno sí refleja el desgaste).

Reglas importantes:
- Nunca rompas el personaje para dar una opinión "balanceada" ajena al perfil.
- El razonamiento debe ser corto (3-5 oraciones), mostrando el POR QUÉ de los \
  scores que asignás, no solo enumerarlos.
- CRÍTICO: el agente solo conoce el mundo a través de su "consumo informativo \
  principal" indicado en el perfil. NUNCA menciones ni asumas un canal informativo \
  distinto al que figura textualmente en el perfil.
- CRÍTICO sobre los scores: deben reflejar fielmente el grado de convicción o duda \
  del agente, no solo repetir mecánicamente el score anterior. Si el evento de esta \
  ronda genuinamente no le afecta, los scores pueden quedar casi iguales a los \
  anteriores (variación de pocos puntos) - eso es válido y esperable. Pero si el \
  agente reconoce en su razonamiento alguna duda, tensión o condición que lo \
  acercaría a otro espacio, el score debe moverse de forma perceptible (no \
  simbólica) para reflejar eso, aunque no alcance a cambiar cuál es su valor más alto.
- Los cinco valores deben ser números enteros que sumen exactamente 100.
- Respondé ÚNICAMENTE en JSON válido, sin texto adicional, sin markdown, con este \
  formato exacto:
{"scores": {"LLA": 0, "UxP": 0, "JxC": 0, "otro": 0, "blanco": 0}, "razonamiento": "..."}
"""


def construir_prompt_usuario_continuo(agente: dict, evento_framed: str, ronda: int,
                                        scores_previos: dict = None) -> str:
    historial = agente.get("historial_razonamiento", [])
    historial_texto = "\n".join(
        f"  Ronda {h['ronda']}: votaría {h['intencion_voto']} — \"{h['razonamiento']}\""
        for h in historial[-3:]
    ) or "  (sin rondas previas registradas en el esquema categórico)"

    if scores_previos:
        scores_texto = (f"Tus scores de la medición anterior fueron: {json.dumps(scores_previos, ensure_ascii=False)}. "
                         f"Partí de ahí y ajustá según el evento de esta ronda, no reinicies desde cero.")
    else:
        scores_texto = ("Esta es tu primera medición con el esquema de scores continuos. "
                         "Basate en tu voto_2023 y en tu historial categórico previo para "
                         "estimar un punto de partida razonable antes de aplicar el ajuste "
                         "por el evento de esta ronda.")

    return f"""PERFIL DEL AGENTE:
- ID: {agente['id']}
- Edad: {agente['edad']} años
- Provincia: {agente['provincia']}
- Educación: {agente['educacion']}
- Ocupación: {agente['ocupacion']}
- Nivel de ingreso: {agente['nivel_ingreso']}
- Voto en 2023: {agente['voto_2023']}
- Consumo informativo principal: {agente['consumo_informativo']}
- Rasgo de personalidad: {agente['rasgo_personalidad']}

CONTEXTO HISTÓRICO COMPARTIDO:
{MEMORIA_BASE_HISTORICA}

HISTORIAL DE RAZONAMIENTO PREVIO (esquema categórico, rondas 1-5 ya corridas):
{historial_texto}

{scores_texto}

EVENTO DE ESTA RONDA (ronda {ronda}), tal como le llegó a este agente según su canal \
informativo ({agente['consumo_informativo']}):
\"\"\"{evento_framed}\"\"\"

Recordá: tu único canal de información es "{agente['consumo_informativo']}". No \
menciones ni asumas ningún otro canal en tu razonamiento.

Dado todo esto, asigná los scores de afinidad (0-100, sumando exactamente 100 entre \
los cinco) y explicá por qué. Respondé en el formato JSON indicado."""


def llamar_agente_continuo(agente: dict, evento_framed: str, ronda: int,
                            scores_previos: dict = None, max_reintentos: int = 3) -> dict:
    prompt = construir_prompt_usuario_continuo(agente, evento_framed, ronda, scores_previos)

    response = None
    ultimo_error = None
    for intento in range(1, max_reintentos + 1):
        try:
            response = client.messages.create(
                model=MODELO,
                max_tokens=500,
                system=SYSTEM_PROMPT_CONTINUO,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except (anthropic.InternalServerError, anthropic.APIConnectionError,
                anthropic.RateLimitError) as e:
            ultimo_error = e
            espera = 2 ** intento
            print(f"  ⚠️  Error transitorio de API en {agente['id']} "
                  f"(intento {intento}/{max_reintentos}): {type(e).__name__}. "
                  f"Reintentando en {espera}s...")
            time.sleep(espera)

    if response is None:
        print(f"  ❌ {agente['id']}: falló tras {max_reintentos} intentos.")
        return {
            "scores": scores_previos or {"LLA": 0, "UxP": 0, "JxC": 0, "otro": 0, "blanco": 100},
            "razonamiento": f"[ERROR: API no respondió tras {max_reintentos} intentos. "
                            f"Último error: {ultimo_error}]"
        }

    texto_respuesta = response.content[0].text.strip()
    if texto_respuesta.startswith("```"):
        texto_respuesta = texto_respuesta.strip("`").replace("json\n", "", 1)

    try:
        resultado = json.loads(texto_respuesta)
    except json.JSONDecodeError:
        resultado = {
            "scores": scores_previos or {"LLA": 0, "UxP": 0, "JxC": 0, "otro": 0, "blanco": 100},
            "razonamiento": f"[ERROR de parseo JSON, respuesta cruda: {texto_respuesta[:200]}]"
        }

    return resultado


if __name__ == "__main__":
    with open("perfiles_agentes.json", encoding="utf-8") as f:
        agentes = json.load(f)

    agente_prueba = agentes[8]  # agente_09, uno de los LLA que mostró duda en Ronda 5
    evento_prueba = (
        "Vos ya viviste las rondas 1 a 5 (Libra, ANDIS, derrota PBA, síntesis FT, "
        "récord de consumo vs datos reales). Esta es solo una re-medición de tu "
        "estado actual con el nuevo esquema de scores, sin un evento nuevo todavía."
    )

    print(f"Probando con: {agente_prueba['id']} ({agente_prueba['ocupacion']}, "
          f"voto 2023: {agente_prueba['voto_2023']})\n")

    resultado = llamar_agente_continuo(agente_prueba, evento_prueba, ronda=0)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
