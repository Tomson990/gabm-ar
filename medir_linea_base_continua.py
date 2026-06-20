"""
Re-medición inicial: toma el estado actual de los 24 agentes (post Ronda 5 del
esquema categórico) y les pide estimar sus scores continuos de afinidad, SIN
introducir un evento nuevo todavía. Esto establece la línea de base continua
para poder medir movimiento real en rondas continuas futuras.
"""

import json
import time
from motor_agente_continuo import llamar_agente_continuo

ARCHIVO_PERFILES = "perfiles_agentes.json"
ARCHIVO_SCORES = "scores_continuos.json"

EVENTO_LINEA_BASE = (
    "Esta es una re-medición de tu estado actual con un nuevo esquema de scores "
    "continuos, después de haber vivido las rondas 1 a 5 (escándalo $LIBRA, "
    "escándalo ANDIS, derrota electoral en PBA, síntesis del Financial Times sobre "
    "la 'mayor crisis', y la disputa entre el 'récord de consumo' anunciado por el "
    "gobierno y los datos reales de caída de salarios y empleo formal). No hay un "
    "evento nuevo en esta medición - estimá tus scores de afinidad actuales tomando "
    "en cuenta todo lo que ya viviste hasta ahora."
)


def correr_linea_base():
    with open(ARCHIVO_PERFILES, encoding="utf-8") as f:
        agentes = json.load(f)

    resultados = {}
    for i, agente in enumerate(agentes, start=1):
        print(f"[{i}/{len(agentes)}] Midiendo línea de base continua: {agente['id']} "
              f"(voto 2023: {agente['voto_2023']}, intención actual: "
              f"{agente.get('intencion_voto_actual')})...")

        resultado = llamar_agente_continuo(agente, EVENTO_LINEA_BASE, ronda=0)
        resultados[agente['id']] = {
            "voto_2023": agente["voto_2023"],
            "intencion_categorica_actual": agente.get("intencion_voto_actual"),
            "scores": resultado["scores"],
            "razonamiento": resultado["razonamiento"]
        }

        # Guardado incremental
        with open(ARCHIVO_SCORES, "w", encoding="utf-8") as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)

        time.sleep(0.5)

    return resultados


def resumen_linea_base(resultados: dict):
    print("\n" + "=" * 70)
    print("LÍNEA DE BASE CONTINUA - scores promedio por categoría categórica actual")
    print("=" * 70)

    grupos = {}
    for agente_id, data in resultados.items():
        cat = data["intencion_categorica_actual"]
        grupos.setdefault(cat, []).append(data["scores"])

    for categoria, lista_scores in grupos.items():
        n = len(lista_scores)
        promedio = {
            espacio: round(sum(s.get(espacio, 0) for s in lista_scores) / n, 1)
            for espacio in ["LLA", "UxP", "JxC", "otro", "blanco"]
        }
        print(f"\nGrupo categórico '{categoria}' (n={n}):")
        for espacio, valor in promedio.items():
            print(f"    {espacio}: {valor}")


if __name__ == "__main__":
    resultados = correr_linea_base()
    resumen_linea_base(resultados)
