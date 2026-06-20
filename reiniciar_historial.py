"""
Reinicia el historial de razonamiento de los 24 agentes para empezar una nueva
secuencia de rondas (Experimento 2: desgaste acumulado, orden cronológico real).
Mantiene intactas todas las características fijas del perfil (edad, provincia,
ocupación, voto_2023, canal, rasgo) - solo borra el historial y la intención
de voto actual, que se vuelven a construir desde cero en este experimento.
"""

import json
import shutil

ARCHIVO_PERFILES = "perfiles_agentes.json"
BACKUP = "perfiles_agentes_experimento_1_backup.json"


def reiniciar_historial():
    # Backup de seguridad antes de tocar nada
    shutil.copy(ARCHIVO_PERFILES, BACKUP)
    print(f"Backup guardado en {BACKUP}")

    with open(ARCHIVO_PERFILES, encoding="utf-8") as f:
        agentes = json.load(f)

    for agente in agentes:
        agente["intencion_voto_actual"] = None
        agente["historial_razonamiento"] = []

    with open(ARCHIVO_PERFILES, "w", encoding="utf-8") as f:
        json.dump(agentes, f, ensure_ascii=False, indent=2)

    print(f"Historial reiniciado para {len(agentes)} agentes. "
          f"Características fijas (perfil) sin cambios.")


if __name__ == "__main__":
    reiniciar_historial()
