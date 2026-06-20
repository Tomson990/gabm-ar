"""
Ejecuta una ronda completa de la simulación: para cada uno de los 24 agentes,
toma el framing correspondiente a su canal informativo, llama al motor de
razonamiento, y guarda el resultado (intención de voto + razonamiento) tanto
en el historial del agente como en un archivo agregado de la ronda.
"""

import json
import time
from motor_agente import llamar_agente

ARCHIVO_PERFILES = "perfiles_agentes.json"
ARCHIVO_FRAMINGS = "framings_ronda_1.json"


def cargar_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ejecutar_ronda(numero_ronda: int, archivo_framings: str = ARCHIVO_FRAMINGS,
                    archivo_perfiles: str = ARCHIVO_PERFILES, pausa_seg: float = 0.5):
    agentes = cargar_json(archivo_perfiles)
    framings = cargar_json(archivo_framings)

    resultados_ronda = []

    for i, agente in enumerate(agentes, start=1):
        canal = agente["consumo_informativo"]
        evento_framed = framings.get(canal)

        if evento_framed is None:
            print(f"⚠️  {agente['id']}: no se encontró framing para el canal "
                  f"'{canal}'. Se omite este agente en esta ronda.")
            continue

        print(f"[{i}/{len(agentes)}] Procesando {agente['id']} "
              f"({agente['ocupacion']}, canal: {canal})...")

        resultado = llamar_agente(agente, evento_framed, ronda=numero_ronda)

        # Actualizar estado del agente
        agente["intencion_voto_actual"] = resultado["intencion_voto"]
        agente["historial_razonamiento"].append({
            "ronda": numero_ronda,
            "intencion_voto": resultado["intencion_voto"],
            "razonamiento": resultado["razonamiento"],
            "cambio": resultado.get("cambio_respecto_a_ronda_anterior", False)
        })

        resultados_ronda.append({
            "id": agente["id"],
            "voto_2023": agente["voto_2023"],
            "intencion_voto": resultado["intencion_voto"],
            "cambio": resultado.get("cambio_respecto_a_ronda_anterior", False),
            "razonamiento": resultado["razonamiento"]
        })

        # Guardado incremental: si algo falla más adelante, no se pierde lo ya hecho
        guardar_json(agentes, archivo_perfiles)
        guardar_json(resultados_ronda, f"resultados_ronda_{numero_ronda}.json")

        time.sleep(pausa_seg)  # evitar saturar la API

    # Guardar perfiles actualizados (con historial nuevo) y resultados de la ronda
    guardar_json(agentes, archivo_perfiles)
    guardar_json(resultados_ronda, f"resultados_ronda_{numero_ronda}.json")

    return resultados_ronda


def resumen_agregado(resultados_ronda: list):
    conteo = {}
    cambios = 0
    for r in resultados_ronda:
        conteo[r["intencion_voto"]] = conteo.get(r["intencion_voto"], 0) + 1
        if r["cambio"]:
            cambios += 1

    print("\n" + "=" * 50)
    print(f"RESUMEN DE LA RONDA — {len(resultados_ronda)} agentes procesados")
    print("=" * 50)
    for partido, cantidad in sorted(conteo.items(), key=lambda x: -x[1]):
        pct = 100 * cantidad / len(resultados_ronda)
        print(f"  {partido}: {cantidad} ({pct:.1f}%)")
    print(f"\n  Agentes que cambiaron de intención esta ronda: {cambios}")


if __name__ == "__main__":
    import sys

    numero_ronda_arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    archivo_perfiles_arg = sys.argv[2] if len(sys.argv) > 2 else ARCHIVO_PERFILES

    archivo_framings = f"framings_ronda_{numero_ronda_arg}.json"

    resultados = ejecutar_ronda(numero_ronda=numero_ronda_arg, archivo_framings=archivo_framings,
                                  archivo_perfiles=archivo_perfiles_arg)
    resumen_agregado(resultados)
