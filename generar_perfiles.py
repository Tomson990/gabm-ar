"""
Generador de perfiles de agentes para simulación GABM - Elecciones Argentina 2027
Distribución pensada para reflejar heterogeneidad real (no exacta, sino plausible)
sin pretender ser una muestra censalmente representativa.
"""

import json
import random

random.seed(42)

PROVINCIAS = [
    ("Buenos Aires (GBA)", 0.32),
    ("Buenos Aires (interior)", 0.10),
    ("CABA", 0.08),
    ("Córdoba", 0.09),
    ("Santa Fe", 0.08),
    ("Mendoza", 0.05),
    ("Tucumán", 0.04),
    ("Salta", 0.03),
    ("Entre Ríos", 0.03),
    ("Chaco", 0.03),
    ("Otras provincias", 0.15),
]

EDUCACION = ["primario incompleto", "secundario incompleto", "secundario completo",
             "terciario/universitario incompleto", "universitario completo"]

OCUPACION = ["comercio informal", "empleado privado formal", "empleado público",
             "profesional independiente", "desempleado", "jubilado",
             "cuentapropista/monotributista", "estudiante"]

CONSUMO_INFO = ["TV abierta + WhatsApp familiar", "redes (Instagram/TikTok)",
                "redes (X/Twitter)", "radio + diario local", "streaming político (YouTube/Twitch)",
                "boca en boca, poco consumo directo"]

VOTO_2023 = ["LLA", "UxP", "JxC", "voto en blanco/no votó", "otro/provincial"]

RASGOS = ["arraigado a identidad de voto, baja apertura al cambio",
          "persuadible, prioriza resultados económicos concretos",
          "alta apertura al cambio, vota castigo al oficialismo",
          "desconfiado de la política en general, voto errático",
          "ideológicamente consistente, vota por convicción más que coyuntura"]

def elegir_ponderado(opciones_pesos):
    opciones, pesos = zip(*opciones_pesos)
    return random.choices(opciones, weights=pesos, k=1)[0]

def generar_agente(idx):
    edad = random.choices(
        [random.randint(18, 29), random.randint(30, 44), random.randint(45, 59), random.randint(60, 80)],
        weights=[0.25, 0.30, 0.25, 0.20], k=1
    )[0]

    provincia = elegir_ponderado(PROVINCIAS)
    educacion = random.choices(EDUCACION, weights=[0.05, 0.15, 0.35, 0.20, 0.25], k=1)[0]
    ocupacion = random.choice(OCUPACION)
    consumo = random.choice(CONSUMO_INFO)
    voto_2023 = elegir_ponderado([("LLA", 0.30), ("UxP", 0.28), ("JxC", 0.18),
                                    ("voto en blanco/no votó", 0.14), ("otro/provincial", 0.10)])
    rasgo = random.choice(RASGOS)

    nivel_ingreso = random.choices(
        ["bajo", "medio-bajo", "medio", "medio-alto", "alto"],
        weights=[0.20, 0.25, 0.30, 0.18, 0.07], k=1
    )[0]

    return {
        "id": f"agente_{idx:02d}",
        "edad": edad,
        "provincia": provincia,
        "educacion": educacion,
        "ocupacion": ocupacion,
        "nivel_ingreso": nivel_ingreso,
        "voto_2023": voto_2023,
        "consumo_informativo": consumo,
        "rasgo_personalidad": rasgo,
        "intencion_voto_actual": None,  # se completa en la simulación
        "historial_razonamiento": []
    }

agentes = [generar_agente(i) for i in range(1, 25)]

with open("perfiles_agentes.json", "w", encoding="utf-8") as f:
    json.dump(agentes, f, ensure_ascii=False, indent=2)

print(f"Generados {len(agentes)} perfiles.\n")
for a in agentes[:5]:
    print(f"{a['id']}: {a['edad']} años, {a['provincia']}, {a['ocupacion']}, "
          f"voto 2023={a['voto_2023']}, rasgo={a['rasgo_personalidad']}")
print("...")
