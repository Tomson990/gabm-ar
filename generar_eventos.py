"""
Generador de eventos de ronda - toma un hecho crudo (real, buscado en la web)
y genera versiones "framed" según cómo llegaría por cada canal informativo,
usando el LLM para simular el sesgo/estilo de cada medio.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODELO = "claude-sonnet-4-6"

# ============================================================================
# EXPERIMENTO 1 (exploratorio, archivado) - eventos sueltos sin orden cronológico
# estricto: Adorni (jun-2026), dólar/superávit (jun-2026), derrota PBA (sep-2025).
# Resultados y código preservados en la carpeta experimento_1_exploratorio/.
# ============================================================================

# ============================================================================
# EXPERIMENTO 2 (actual) - secuencia cronológica real de eventos negativos para
# el oficialismo, pensada para testear desgaste acumulado a través de rondas.
# Orden real: Libra (feb-2025) -> ANDIS (ago-2025) -> derrota PBA (sep-2025) ->
# síntesis FT "mayor crisis" (sep-2025).
# ============================================================================

# Hecho crudo de la Ronda 1 - escándalo $LIBRA / "Criptogate" (febrero 2025)
EVENTO_CRUDO_RONDA_1 = """
HECHO (neutral, ronda 1 - 14 de febrero de 2025, primer evento de la secuencia):
El 14 de febrero de 2025, el presidente Javier Milei recomendó por su cuenta de X una
criptomoneda llamada $LIBRA, presentada como un vehículo para financiar a pequeñas
empresas argentinas. Tras la publicación de Milei, la cotización subió de forma
exponencial en minutos, pero en apenas 4 horas la moneda se desplomó y perdió el 89%
de su valor, mientras algunos funcionarios y cuentas afines a La Libertad Avanza
seguían difundiendo el mensaje. El escándalo, conocido como "Criptogate", escaló
cuando se revelaron reuniones previas del propio Milei con los responsables del
proyecto: en octubre de 2024 con Julian Peh (CEO de KIP Protocol) y en enero de 2025
con Hayden Davis (Kelsier Ventures). Se acumularon 112 denuncias penales en la
Justicia argentina, además de demandas colectivas presentadas en Estados Unidos y
España por inversores que perdieron dinero. Milei reconoció públicamente: "Obré de
buena fe y me comí un cachetazo", pero minimizó el impacto diciendo que la mayoría de
los afectados eran inversores extranjeros y que el episodio no dañaba su credibilidad.
Meses después, en mayo de 2025, el propio gobierno disolvió por decreto la unidad que
investigaba el caso, alegando que "la tarea encomendada fue cumplimentada".
"""

# Hecho crudo de la Ronda 2 - escándalo ANDIS / coimas en discapacidad (agosto 2025)
EVENTO_CRUDO_RONDA_2 = """
HECHO (neutral, ronda 2 - agosto de 2025, segundo evento de la secuencia):
En agosto de 2025 se filtraron audios de Diego Spagnuolo, hasta entonces director de
la Agencia Nacional de Discapacidad (ANDIS) y amigo/abogado personal de Milei, en los
que detallaba una presunta trama de coimas en la compra de medicamentos para personas
con discapacidad. Según los audios, una droguería (Suizo Argentina) habría pagado
sobreprecios de los que una parte se desviaba como soborno a funcionarios, con un
tramo de esos pagos señalado hacia Karina Milei, hermana del presidente y Secretaria
General de la Presidencia. Los contratos de esa droguería con el Estado habían pasado
de 3.898 millones de pesos en 2024 a 108.299 millones en 2025. El gobierno removió a
Spagnuolo de su cargo, pero sostuvo que se trataba de una "operación política" del
kirchnerismo a dos semanas de las elecciones bonaerenses. El presidente de la Cámara
de Diputados, Martín Menem, declaró públicamente: "pongo las manos en el fuego" por
Karina Milei y por su colaborador Eduardo "Lule" Menem. Milei calificó las
declaraciones de Spagnuolo como "mentira" y anunció acciones legales en su contra. El
juez federal a cargo de la causa describió a la agencia como una organización que se
convirtió en "una oportunidad de rápido enriquecimiento ilícito" del grupo que la
dirigía, a costa de fondos destinados a personas con discapacidad, adultos mayores en
situación de pobreza y madres de familias numerosas.
"""

# ============================================================================
# RAMA CONTRAFACTUAL "SIN LIBRA" - misma secuencia real, pero arrancando
# directamente en ANDIS como primer evento que el agente conoce. Pregunta que
# busca responder: ¿el factor causal era "Libra específicamente" (protagonismo
# del propio Milei, ruptura de la promesa fundacional anti-casta) o simplemente
# "el primer escándalo de corrupción que aparece en la secuencia, sea cual sea"?
# ============================================================================

EVENTO_CRUDO_RONDA_1_CONTRAFACTUAL = """
HECHO (neutral, ronda 1 de la rama CONTRAFACTUAL "sin Libra" - agosto de 2025,
PRIMER evento que este agente conoce en esta rama alternativa de la simulación):
En agosto de 2025 se filtraron audios de Diego Spagnuolo, hasta entonces director de
la Agencia Nacional de Discapacidad (ANDIS) y amigo/abogado personal de Milei, en los
que detallaba una presunta trama de coimas en la compra de medicamentos para personas
con discapacidad. Según los audios, una droguería (Suizo Argentina) habría pagado
sobreprecios de los que una parte se desviaba como soborno a funcionarios, con un
tramo de esos pagos señalado hacia Karina Milei, hermana del presidente y Secretaria
General de la Presidencia. Los contratos de esa droguería con el Estado habían pasado
de 3.898 millones de pesos en 2024 a 108.299 millones en 2025. El gobierno removió a
Spagnuolo de su cargo, pero sostuvo que se trataba de una "operación política" del
kirchnerismo a dos semanas de las elecciones bonaerenses. El presidente de la Cámara
de Diputados, Martín Menem, declaró públicamente: "pongo las manos en el fuego" por
Karina Milei y por su colaborador Eduardo "Lule" Menem. Milei calificó las
declaraciones de Spagnuolo como "mentira" y anunció acciones legales en su contra. El
juez federal a cargo de la causa describió a la agencia como una organización que se
convirtió en "una oportunidad de rápido enriquecimiento ilícito" del grupo que la
dirigía, a costa de fondos destinados a personas con discapacidad, adultos mayores en
situación de pobreza y madres de familias numerosas. (Nota: en esta rama de la
simulación, este es el primer escándalo de corrupción del mandato que el agente
conoce - no hubo ningún antecedente previo de este tipo.)
"""

# Hecho crudo de la Ronda 3 - derrota electoral PBA (septiembre 2025), tercer evento
EVENTO_CRUDO_RONDA_3 = """
HECHO (neutral, ronda 3 - 7 de septiembre de 2025, tercer evento de la secuencia,
ocurre apenas semanas después del escándalo ANDIS):
El 7 de septiembre de 2025 se realizaron elecciones legislativas provinciales en
Buenos Aires (el distrito más poblado del país, con más del 37% del padrón nacional).
La coalición peronista Fuerza Patria (que reúne a sectores de Axel Kicillof, Cristina
Kirchner y Sergio Massa) obtuvo el 47,28% de los votos, venciendo en 102 municipios y
en 6 de las 8 secciones electorales. La Libertad Avanza, alianza oficialista de
Milei, quedó segunda con 33,71%, perdiendo por más de 13 puntos en lo que era
considerado uno de los distritos clave para el oficialismo. El propio Milei reconoció
públicamente desde el búnker de campaña: "en el plano político hoy hemos tenido una
clara derrota... no han sido positivos, hemos tenido un revés, y hay que asumirlo con
responsabilidad". El resultado generó pánico financiero inmediato: el peso se
desplomó casi 10% en cuestión de horas, el riesgo país subió fuertemente, y cayeron
las acciones y bonos argentinos. Varios analistas vincularon directamente este
resultado al desgaste producido por el escándalo de ANDIS de las semanas previas.
"""

# Hecho crudo de la Ronda 4 - síntesis "mayor crisis de su presidencia" (Financial
# Times, septiembre 2025), cuarto evento: no es un hecho nuevo aislado sino un
# diagnóstico periodístico que integra los tres eventos anteriores
EVENTO_CRUDO_RONDA_4 = """
HECHO (neutral, ronda 4 - mediados de septiembre de 2025, cuarto evento de la
secuencia: una síntesis periodística que conecta explícitamente los tres eventos
anteriores como parte de un mismo proceso, no un hecho nuevo y aislado):
A mediados de septiembre de 2025, el diario británico Financial Times publicó un
análisis afirmando que Javier Milei atravesaba "la mayor crisis" de su presidencia, a
menos de dos años de haber asumido. El artículo, escrito por la periodista Ciara
Nugent, señaló que el primer año de gobierno había tenido logros visibles (baja de la
inflación, ajuste fiscal con respaldo popular), pero que ese escenario se había
invertido en los meses recientes por la combinación de: el escándalo de corrupción
que involucró a Karina Milei en la agencia de discapacidad (ANDIS), la derrota
electoral en la provincia de Buenos Aires por más de 13 puntos frente al peronismo, y
una recuperación económica estancada. El análisis agregó que el índice de aprobación
presidencial de Milei había caído por primera vez por debajo del 40%, y mencionó
también las dificultades del oficialismo para lograr consensos en el Congreso, donde
es minoría, incluyendo el rechazo a vetos presidenciales sobre la emergencia en
discapacidad y el financiamiento universitario. El artículo describió al presidente
como cada vez más "belicoso" en su respuesta pública a las críticas.
"""

# Hecho crudo de la Ronda 5 - golpe directo al bolsillo, con disputa entre el relato
# oficial y los datos de actividad real (abril 2026, evento reciente, no atribuible
# a la herencia de la gestión anterior - es deterioro bajo la gestión actual)
EVENTO_CRUDO_RONDA_5 = """
HECHO (neutral, ronda 5 - abril de 2026, quinto evento de la secuencia, distinto en
naturaleza a los anteriores: no es un escándalo político sino un dato económico
directo sobre el poder de compra, ocurrido bajo la gestión actual, sin atribución
posible a la herencia del gobierno anterior):
En abril de 2026, el presidente Milei afirmó públicamente en el AmCham Summit
"estamos en récord de consumo", y tanto el ministro de Economía Luis Caputo como su
viceministro repitieron en distintas apariciones mediáticas que el consumo se
encuentra en "niveles históricos", citando un informe del INDEC según el cual el
consumo privado creció 7,9% en 2025 y alcanzó, en términos constantes, el nivel más
alto de la serie estadística que comienza en 2004. Sin embargo, otros indicadores
del mismo período muestran un panorama distinto: en febrero de 2026 el EMAE (el
estimador de actividad mensual) cayó 2,1% interanual y 2,6% respecto al mes anterior,
borrando gran parte del avance de los meses previos, con los sectores más afectados
siendo la industria manufacturera (-8,7% interanual), el comercio (-7%) y
electricidad, gas y agua (-6%); los sectores que sí crecieron fueron minería y agro,
de baja generación de empleo. Entre febrero de 2025 y febrero de 2026, los salarios
formales tuvieron un ajuste nominal del 27,5% frente a una suba de precios del 33,1%,
es decir que el salario sigue perdiendo contra la inflación en el último año
corriente, no solo al inicio de la gestión. Un informe del centro de investigación
Cifra calculó que el salario registrado real promedio acumuló una caída cercana al
9% entre noviembre de 2023 y febrero de 2026, con los salarios estatales un 18,3% por
debajo de ese punto de partida, y que en los dos años de gestión se perdieron 265.800
empleos asalariados registrados, mientras crecieron 345.700 trabajos no asalariados
(informales o de cuenta propia, descritos como "empleos refugio").
"""

# Hecho crudo de la Ronda 6 - tarifazos combinados de energía y transporte (2026),
# pensado para el esquema CONTINUO de medición. A diferencia de Ronda 5, este evento
# no tiene "dato positivo" real que lo contrarreste - es una decisión de política
# directa y reconocida del gobierno, gradual durante todo 2026, sin escape narrativo
# fácil para el núcleo LLA.
EVENTO_CRUDO_RONDA_6 = """
HECHO (neutral, ronda 6 - evento combinado, distinto en naturaleza a los anteriores:
no es un escándalo ni una estadística discutible, es el costo de vida básico
golpeado por decisión directa de política económica, con datos verificables y sin
versión "positiva" real que lo contrarreste):
Desde enero de 2026, el gobierno de Milei implementó un nuevo esquema de subsidios
de energía que elimina la segmentación por niveles de ingreso y deja fuera del
subsidio a más de 140.000 familias de ingresos medios; el "colchón" transitorio de
cobertura (75% en luz, 25% en gas en enero) baja mes a mes hasta desaparecer por
completo en diciembre de 2026. En paralelo, la quita de subsidios al transporte
público --iniciada en 2024-- ya produjo que el boleto de subte se multiplicara más
de 17 veces (de $80 a $1.414) entre noviembre de 2023 y abril de 2026, un aumento
337% por encima de la inflación acumulada del período; el boleto de colectivo se
multiplicó hasta 16 veces en el mismo lapso. El salario mínimo, en cambio, solo
aumentó 129% nominal frente a una inflación acumulada de 303,5% en el mismo período,
lo que implicó una caída real de aproximadamente 43% en su poder de compra. El
transporte público en el AMBA consume hoy el 43% de un salario, una proporción
similar a Bogotá o Montevideo. Como referencia concreta del deterioro: la Beca
Progresar, congelada en su monto desde marzo de 2025, permitía costear 839 viajes
de colectivo en diciembre de 2023; hoy apenas alcanza para 111 boletos. El gasto de
las familias en servicios públicos saltó 561% durante la gestión, con nuevos
aumentos previstos para el resto de 2026.
"""

CANALES = [
    "TV abierta + WhatsApp familiar",
    "redes (Instagram/TikTok)",
    "redes (X/Twitter)",
    "radio + diario local",
    "streaming político (YouTube/Twitch)",
    "boca en boca, poco consumo directo",
]

SYSTEM_PROMPT_FRAMING = """Sos un simulador de medios para un experimento de \
investigación en ciencias sociales computacionales. Dado un hecho neutral, tu tarea \
es reescribirlo TAL COMO LE LLEGARÍA a una persona según un canal informativo \
específico - no dando tu propia opinión, sino simulando el estilo, tono, nivel de \
detalle y sesgo TÍPICO de ese canal en Argentina.

Pautas por canal (estas son convenciones de estilo a simular, no juicios de valor):
- "TV abierta + WhatsApp familiar": tono más institucional en la TV, pero la versión \
  que real importa es la que circula en WhatsApp - mensajes cortos, alarmistas o \
  indignados, a veces con errores o exageración, replicando lo que vio un familiar.
- "redes (Instagram/TikTok)": formato de posteo/historia breve, emocional, con lenguaje \
  coloquial, puede incluir referencia a un video viral o meme sobre el tema.
- "redes (X/Twitter)": más político y polarizado, hilos de discusión, citando posturas \
  enfrentadas de cuentas políticas/periodísticas conocidas (sin inventar tuits \
  textuales, solo describiendo el clima del debate).
- "radio + diario local": tono más sobrio, informativo, con algo de análisis político, \
  estilo nota de diario regional.
- "streaming político (YouTube/Twitch)": tono conversacional pero con codificación \
  ideológica fuerte según la línea editorial del streamer - explicá el hecho con un \
  ángulo claramente crítico O claramente defensivo del oficialismo (elegí el más \
  plausible para este hecho puntual, no siempre el mismo signo en cada ronda).
- "boca en boca, poco consumo directo": versión muy resumida, simplificada, con \
  posible pérdida de matices y detalles, tal como llegaría de tercera mano.

Para cada canal, generá un párrafo corto (3-5 oraciones) que sea la versión que ese \
canal le mostraría a la audiencia. Respondé ÚNICAMENTE en JSON válido con este formato:
{"canal_1": "...", "canal_2": "...", ...} usando como claves exactamente los nombres \
de canal que se te pasan, en el mismo orden."""


def generar_framings(evento_crudo: str, canales: list) -> dict:
    prompt = f"""HECHO NEUTRAL A ADAPTAR:
{evento_crudo}

CANALES (generá una versión para cada uno, usando estas claves exactas):
{json.dumps(canales, ensure_ascii=False)}
"""

    response = client.messages.create(
        model=MODELO,
        max_tokens=2200,
        system=SYSTEM_PROMPT_FRAMING,
        messages=[{"role": "user", "content": prompt}]
    )

    texto = response.content[0].text.strip()
    if texto.startswith("```"):
        texto = texto.strip("`").replace("json\n", "", 1)

    if response.stop_reason == "max_tokens":
        print("⚠️  ADVERTENCIA: la respuesta se cortó por límite de tokens "
              "(stop_reason='max_tokens'). Es probable que el JSON esté incompleto. "
              "Subí max_tokens en generar_eventos.py si esto se repite.")

    try:
        resultado = json.loads(texto)
    except json.JSONDecodeError:
        print("ERROR de parseo. Guardando respuesta cruda en 'framings_debug_raw.txt' "
              "para no perder el trabajo ya generado.")
        with open("framings_debug_raw.txt", "w", encoding="utf-8") as f:
            f.write(texto)
        resultado = {}

    return resultado


if __name__ == "__main__":
    import sys

    ronda = sys.argv[1] if len(sys.argv) > 1 else "1"
    # Si es un número puro (ej "3", "4"), normalizar a int para que coincida
    # con las claves int del diccionario; si tiene letras (ej "1c"), dejar como string.
    if ronda.isdigit():
        ronda = int(ronda)
    eventos_por_ronda = {
        1: EVENTO_CRUDO_RONDA_1,
        2: EVENTO_CRUDO_RONDA_2,
        3: EVENTO_CRUDO_RONDA_3,
        4: EVENTO_CRUDO_RONDA_4,
        5: EVENTO_CRUDO_RONDA_5,
        6: EVENTO_CRUDO_RONDA_6,
        # Rama contrafactual "sin Libra": usar ronda="1c" para el primer evento
        # (ANDIS como apertura), luego reutilizar las claves 3, 4 normales para
        # PBA y síntesis FT en la misma rama (no cambian, no mencionan a Libra).
        "1c": EVENTO_CRUDO_RONDA_1_CONTRAFACTUAL,
    }

    evento = eventos_por_ronda.get(ronda)
    if evento is None:
        print(f"No hay evento crudo definido para la ronda {ronda}. "
              f"Agregalo en generar_eventos.py antes de correr.")
        sys.exit(1)

    framings = generar_framings(evento, CANALES)

    with open(f"framings_ronda_{ronda}.json", "w", encoding="utf-8") as f:
        json.dump(framings, f, ensure_ascii=False, indent=2)

    for canal, texto in framings.items():
        print(f"\n--- {canal} ---")
        print(texto)
