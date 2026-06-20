"""
Recalcula el flag "cambio" de un archivo de resultados ya generado, comparando
contra voto_2023 (si es ronda 1) o contra la ronda anterior registrada en el
historial del agente. No vuelve a llamar a la API - es solo corrección local.
"""

import json
import sys


def recalcular_cambios(archivo_resultados: str, archivo_perfiles: str = "perfiles_agentes.json"):
    with open(archivo_resultados, encoding="utf-8") as f:
        resultados = json.load(f)

    with open(archivo_perfiles, encoding="utf-8") as f:
        agentes = {a["id"]: a for a in json.load(f)}

    corregidos = 0
    for r in resultados:
        agente = agentes.get(r["id"])
        referencia = r["voto_2023"] if agente is None else r["voto_2023"]
        nuevo_cambio = (r["intencion_voto"] != referencia)
        if nuevo_cambio != r["cambio"]:
            corregidos += 1
        r["cambio"] = nuevo_cambio

    with open(archivo_resultados, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"Recalculado. {corregidos} registros corregidos sobre {len(resultados)} totales.\n")

    conteo = {}
    cambios = 0
    for r in resultados:
        conteo[r["intencion_voto"]] = conteo.get(r["intencion_voto"], 0) + 1
        if r["cambio"]:
            cambios += 1

    print("Resumen corregido:")
    for partido, cantidad in sorted(conteo.items(), key=lambda x: -x[1]):
        pct = 100 * cantidad / len(resultados)
        print(f"  {partido}: {cantidad} ({pct:.1f}%)")
    print(f"\n  Agentes con intención distinta a su voto_2023: {cambios}")


if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "resultados_ronda_1.json"
    recalcular_cambios(archivo)
