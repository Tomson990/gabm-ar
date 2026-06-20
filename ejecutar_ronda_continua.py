"""
Ejecuta una ronda con el esquema CONTINUO: cada agente parte de sus scores
previos (guardados en scores_continuos.json) y los ajusta según el evento nuevo
de esta ronda. Permite ver movimiento gradual que el esquema categórico no capta.
"""

import json
import time
import sys
from motor_agente_continuo import llamar_agente_continuo

ARCHIVO_PERFILES = "perfiles_agentes.json"
ARCHIVO_SCORES = "scores_continuos.json"
ARCHIVO_FRAMINGS_TEMPLATE = "framings_ronda_{}.json"


def cargar_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ejecutar_ronda_continua(numero_ronda: int, pausa_seg: float = 0.5):
    agentes = {a["id"]: a for a in cargar_json(ARCHIVO_PERFILES)}
    scores_actuales = cargar_json(ARCHIVO_SCORES)
    framings = cargar_json(ARCHIVO_FRAMINGS_TEMPLATE.format(numero_ronda))

    nuevos_scores = {}
    historico_movimiento = []

    ids_ordenados = list(scores_actuales.keys())
    for i, agente_id in enumerate(ids_ordenados, start=1):
        agente = agentes[agente_id]
        canal = agente["consumo_informativo"]
        evento_framed = framings.get(canal)

        if evento_framed is None:
            print(f"⚠️  {agente_id}: no se encontró framing para el canal '{canal}'.")
            continue

        scores_previos = scores_actuales[agente_id]["scores"]

        print(f"[{i}/{len(ids_ordenados)}] {agente_id} (canal: {canal}) — "
              f"scores previos: {scores_previos}")

        resultado = llamar_agente_continuo(agente, evento_framed, numero_ronda, scores_previos)

        nuevos_scores[agente_id] = {
            "voto_2023": agente["voto_2023"],
            "intencion_categorica_actual": scores_actuales[agente_id]["intencion_categorica_actual"],
            "scores": resultado["scores"],
            "razonamiento": resultado["razonamiento"]
        }

        # Calcular movimiento respecto a la medición previa
        movimiento = {
            espacio: resultado["scores"].get(espacio, 0) - scores_previos.get(espacio, 0)
            for espacio in ["LLA", "UxP", "JxC", "otro", "blanco"]
        }
        historico_movimiento.append({"id": agente_id, "movimiento": movimiento})

        guardar_json(nuevos_scores, ARCHIVO_SCORES.replace(".json", f"_ronda_{numero_ronda}.json"))
        time.sleep(pausa_seg)

    return nuevos_scores, historico_movimiento


def resumen_movimiento(historico_movimiento: list):
    print("\n" + "=" * 70)
    print(f"MOVIMIENTO DE SCORES (delta respecto a medición previa)")
    print("=" * 70)

    promedio_abs = {espacio: 0 for espacio in ["LLA", "UxP", "JxC", "otro", "blanco"]}
    movimientos_significativos = []

    for entry in historico_movimiento:
        for espacio, delta in entry["movimiento"].items():
            promedio_abs[espacio] += abs(delta)
        max_delta = max(entry["movimiento"].values(), key=abs)
        if abs(max_delta) >= 10:
            movimientos_significativos.append((entry["id"], entry["movimiento"]))

    n = len(historico_movimiento)
    print("\nMovimiento absoluto promedio por espacio (cuánto se mueven los scores, "
          "sin importar dirección):")
    for espacio, total in promedio_abs.items():
        print(f"    {espacio}: {round(total / n, 1)}")

    print(f"\nAgentes con movimiento significativo (≥10 puntos en algún espacio): "
          f"{len(movimientos_significativos)} de {n}")
    for agente_id, mov in movimientos_significativos:
        print(f"    {agente_id}: {mov}")


if __name__ == "__main__":
    ronda = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    nuevos_scores, historico = ejecutar_ronda_continua(ronda)
    resumen_movimiento(historico)
