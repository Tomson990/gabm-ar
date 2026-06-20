"""
Crea la rama contrafactual "sin Libra": una copia de los 24 perfiles base, con
historial limpio, guardada en un archivo SEPARADO para no pisar el experimento
original. Esta rama va a correr: ANDIS (como primer evento) -> PBA -> síntesis FT
-> tarifas, en ese orden, SIN el evento $LIBRA.

Objetivo: distinguir si el factor causal era "Libra específicamente" (protagonismo
del propio Milei, ruptura de la promesa fundacional anti-casta) o simplemente
"el primer escándalo de corrupción que aparece en la secuencia, sea cual sea".
"""

import json
import shutil

ARCHIVO_ORIGINAL = "perfiles_agentes.json"
ARCHIVO_CONTRAFACTUAL = "perfiles_agentes_CONTRAFACTUAL_sin_libra.json"


def crear_rama_contrafactual():
    with open(ARCHIVO_ORIGINAL, encoding="utf-8") as f:
        agentes = json.load(f)

    for agente in agentes:
        agente["intencion_voto_actual"] = None
        agente["historial_razonamiento"] = []

    with open(ARCHIVO_CONTRAFACTUAL, "w", encoding="utf-8") as f:
        json.dump(agentes, f, ensure_ascii=False, indent=2)

    print(f"Rama contrafactual creada: {ARCHIVO_CONTRAFACTUAL}")
    print(f"{len(agentes)} agentes, historial limpio, listos para correr "
          f"ANDIS -> PBA -> síntesis FT -> tarifas (sin Libra).")


if __name__ == "__main__":
    crear_rama_contrafactual()
