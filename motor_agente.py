"""
Motor de razonamiento de agentes - llama a la API de Claude para que cada
agente, dado su perfil + memoria base + evento de la ronda, actualice su
intención de voto con razonamiento explícito.

Requiere variable de entorno ANTHROPIC_API_KEY.
"""

import os
import json
import time
import anthropic
from memoria_base import MEMORIA_BASE_HISTORICA

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODELO = "claude-sonnet-4-6"

SYSTEM_PROMPT = """Sos un simulador de razonamiento ciudadano para un experimento de \
investigación en ciencias sociales computacionales (GABM - Generative Agent-Based \
Modeling). Tu tarea es encarnar a UN agente sintético con el perfil exacto que se te \
da, y razonar COMO ESA PERSONA razonaría ante la información que recibe - no como un \
analista neutral, no como un asistente. El agente puede tener sesgos, puede razonar de \
forma motivada, puede ignorar evidencia que no le convenga - así razona la gente real.

Reglas importantes:
- Nunca rompas el personaje para dar una opinión "balanceada" ajena al perfil.
- El razonamiento debe ser corto (3-5 oraciones), en primera persona implícita o \
  tercera persona del agente, mostrando el POR QUÉ de su decisión, no solo el qué.
- La intención de voto debe ser una de: LLA, UxP, JxC, voto en blanco/no vota, otro/provincial.
- Es coherente que el agente NO cambie de intención si el evento no le afecta lo \
  suficiente según su rasgo de personalidad y su historial.
- CRÍTICO: el agente solo conoce el mundo a través de su "consumo informativo principal" \
  indicado en el perfil. NUNCA menciones ni asumas un canal informativo distinto al que \
  figura textualmente en el perfil (por ejemplo, si el perfil dice "TV abierta + WhatsApp \
  familiar", el agente NO puede mencionar streaming, X/Twitter, ni ningún otro canal que \
  no esté en ese campo exacto). Si necesitás referirte a cómo le llegó la información, \
  usá exactamente las palabras del campo consumo_informativo del perfil.
- CRÍTICO sobre el campo "cambio_respecto_a_ronda_anterior": debe ser `true` si la \
  intención de voto que estás dando AHORA es DISTINTA de la referencia anterior, y \
  `false` si es IGUAL. La referencia anterior es: (a) la intención de voto de la última \
  ronda registrada en el historial, si existe al menos una ronda previa; o (b) el \
  "voto_2023" del perfil, si esta es la ronda 1 y no hay historial previo. Compará texto \
  exacto contra esa referencia - no asumas `false` solo porque es la ronda 1. Por \
  ejemplo: si voto_2023="UxP" y ahora decidís "voto en blanco/no vota", eso ES un cambio \
  (`true`), aunque sea la ronda 1.
- Respondé ÚNICAMENTE en JSON válido, sin texto adicional, sin markdown, con este \
  formato exacto:
{"intencion_voto": "...", "razonamiento": "...", "cambio_respecto_a_ronda_anterior": true/false}
"""

def construir_prompt_usuario(agente: dict, evento_framed: str, ronda: int) -> str:
    historial = agente.get("historial_razonamiento", [])
    historial_texto = "\n".join(
        f"  Ronda {h['ronda']}: votaría {h['intencion_voto']} — \"{h['razonamiento']}\""
        for h in historial[-3:]  # solo las últimas 3 rondas para no inflar el prompt
    ) or "  (sin rondas previas, esta es la ronda 1)"

    if historial:
        referencia_cambio = historial[-1]["intencion_voto"]
        origen_referencia = f"su intención de voto en la ronda {historial[-1]['ronda']}"
    else:
        referencia_cambio = agente["voto_2023"]
        origen_referencia = "su voto_2023 (no hay rondas previas todavía)"

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

HISTORIAL DE RAZONAMIENTO PREVIO DE ESTE AGENTE:
{historial_texto}

EVENTO DE ESTA RONDA (ronda {ronda}), tal como le llegó a este agente según su canal \
informativo ({agente['consumo_informativo']}):
\"\"\"{evento_framed}\"\"\"

Recordá: tu único canal de información es "{agente['consumo_informativo']}". No \
menciones ni asumas ningún otro canal en tu razonamiento.

REFERENCIA PARA EL CAMPO "cambio_respecto_a_ronda_anterior": comparar tu nueva \
intención de voto contra {origen_referencia}, que es "{referencia_cambio}". Si tu \
respuesta de ahora es igual a "{referencia_cambio}", el campo debe ser `false`. Si es \
distinta, debe ser `true`.

Dado todo esto, ¿cuál es la intención de voto actual de este agente, y por qué? \
Respondé en el formato JSON indicado."""


def llamar_agente(agente: dict, evento_framed: str, ronda: int, max_reintentos: int = 5) -> dict:
    prompt = construir_prompt_usuario(agente, evento_framed, ronda)

    response = None
    ultimo_error = None
    for intento in range(1, max_reintentos + 1):
        try:
            response = client.messages.create(
                model=MODELO,
                max_tokens=400,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            break  # éxito, salimos del loop de reintentos
        except anthropic.APIStatusError as e:
            codigos_reintentables = {429, 500, 502, 503, 529}
            if e.status_code not in codigos_reintentables:
                raise  # error no transitorio (ej: 400, 401) - no tiene sentido reintentar
            ultimo_error = e
            espera = 2 ** intento  # backoff exponencial: 2, 4, 8 segundos
            print(f"  ⚠️  Error transitorio de API en {agente['id']} "
                  f"(intento {intento}/{max_reintentos}): {type(e).__name__} "
                  f"(status {e.status_code}). Reintentando en {espera}s...")
            time.sleep(espera)
        except anthropic.APIConnectionError as e:
            ultimo_error = e
            espera = 2 ** intento
            print(f"  ⚠️  Error de conexión en {agente['id']} "
                  f"(intento {intento}/{max_reintentos}): {type(e).__name__}. "
                  f"Reintentando en {espera}s...")
            time.sleep(espera)

    if response is None:
        print(f"  ❌ {agente['id']}: falló tras {max_reintentos} intentos. "
              f"Se mantiene su intención previa sin cambios.")
        return {
            "intencion_voto": agente.get("intencion_voto_actual") or agente["voto_2023"],
            "razonamiento": f"[ERROR: API no respondió tras {max_reintentos} intentos. "
                            f"Último error: {ultimo_error}]",
            "cambio_respecto_a_ronda_anterior": False
        }

    texto_respuesta = response.content[0].text.strip()

    # Limpieza defensiva por si el modelo agrega fences de markdown
    if texto_respuesta.startswith("```"):
        texto_respuesta = texto_respuesta.strip("`").replace("json\n", "", 1)

    try:
        resultado = json.loads(texto_respuesta)
    except json.JSONDecodeError:
        resultado = {
            "intencion_voto": agente.get("intencion_voto_actual") or agente["voto_2023"],
            "razonamiento": f"[ERROR de parseo JSON, respuesta cruda: {texto_respuesta[:200]}]",
            "cambio_respecto_a_ronda_anterior": False
        }

    return resultado


if __name__ == "__main__":
    # Prueba con un solo agente para validar el formato antes de escalar
    with open("perfiles_agentes.json", encoding="utf-8") as f:
        agentes = json.load(f)

    agente_prueba = agentes[0]
    evento_prueba = (
        "En el noticiero de la tarde anunciaron que la inflación de mayo fue más alta "
        "de lo esperado por el aumento de la carne y los combustibles. El ministro de "
        "Economía salió a decir que en junio va a bajar."
    )

    print(f"Probando con: {agente_prueba['id']} ({agente_prueba['ocupacion']}, "
          f"voto 2023: {agente_prueba['voto_2023']})\n")

    resultado = llamar_agente(agente_prueba, evento_prueba, ronda=1)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
