"""
Memoria de base histórica - Mandato de Javier Milei (dic 2023 - jun 2026)
Redactado en tono neutral/descriptivo, combinando fuentes de distinto signo,
para servir como contexto compartido inicial de todos los agentes de la simulación.
NO es un evento de ronda - es el "punto de partida" de conocimiento común.
"""

MEMORIA_BASE_HISTORICA = """
CONTEXTO HISTÓRICO COMPARTIDO (diciembre 2023 - junio 2026):

- Diciembre 2023: Javier Milei asume la presidencia. A los pocos días, devalúa el peso
  oficial un 118% y lanza un fuerte ajuste fiscal. La inflación mensual salta de 12,8% a
  25,5% en el primer mes, con caída de salarios reales y consumo.

- 2024: Se aprueba la Ley de Bases tras meses de negociación en el Congreso, otorgando
  facultades delegadas amplias al Poder Ejecutivo (privatizaciones, desregulación,
  reforma del Estado). El gobierno sostiene el ajuste fiscal como eje central ("no hay
  plata"). La actividad económica cae, especialmente construcción e industria.
  El riesgo país desciende de forma sostenida durante el año.

- 2025: Continúa el proceso de desregulación vía DNUs y decretos delegados (más de 150
  normas con rango de ley entre dic-2023 y mediados de 2025). El gobierno sufre una
  derrota electoral en las elecciones provinciales de Buenos Aires en septiembre, pero
  en las elecciones legislativas nacionales de octubre 2025 obtiene una victoria decisiva,
  ampliando su bloque en el Congreso. Mejora la relación con EE.UU., con apoyo del Tesoro
  estadounidense para sostener el esquema cambiario. La pobreza, que había llegado a un
  pico tras el ajuste inicial, desciende en el primer semestre de 2025 a 31,6% según
  INDEC. El dólar oficial pasa de 185 a más de 1.460 pesos en dos años.

- Diciembre 2025: El Congreso aprueba el Presupuesto 2026 con amplio respaldo
  legislativo, reflejando el nuevo capital político del oficialismo tras octubre.

- Primer cuatrimestre de 2026: La inflación se acelera (12,3% acumulado), atribuida al
  aumento internacional del precio de la carne, suba de combustibles por la escalada del
  conflicto en Irán, y actualización de tarifas energéticas. El ministro de Economía,
  Luis Caputo, anticipa una desaceleración desde junio.

- Lecturas en disputa sobre el balance económico a mediados de 2026: sectores oficialistas
  y bancos de inversión destacan la baja del riesgo país, la mejora en precios agrícolas y
  el repunte del crédito hipotecario como señales de estabilización. Sectores críticos
  señalan caídas interanuales consecutivas en la industria y advierten sobre fragilidad
  estructural pese a los indicadores macro.

- Hacia 2027: Con el calendario electoral despejado hasta las elecciones presidenciales,
  el gobierno impulsa una "segunda fase" de reformas (tributaria, laboral, previsional),
  en versiones que buscan consensos legislativos más amplios que en el primer mandato.
"""

if __name__ == "__main__":
    print(MEMORIA_BASE_HISTORICA)
    print(f"\nLongitud aproximada: {len(MEMORIA_BASE_HISTORICA.split())} palabras")
