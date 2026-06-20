# Hallazgo: Sesgo de confirmación motivado en agentes GABM
## Proyecto: Simulación de intención de voto — Argentina 2027
## Rondas analizadas: 1 (caso Adorni) y 2 (dólar / superávit comercial)

---

## Resumen del hallazgo

En dos rondas consecutivas con eventos reales de naturaleza distinta (un escándalo
político de corrupción en la Ronda 1, un evento económico con señales mixtas en la
Ronda 2), **0 de 24 agentes cambiaron su intención de voto respecto a la ronda
anterior**. Sin embargo, la lectura de los razonamientos individuales descarta que
esto sea un artefacto técnico (el modelo "ignorando" el evento nuevo): cada agente
incorpora detalles específicos y verificables del evento de su ronda en su
razonamiento. El patrón no es ausencia de procesamiento, sino **procesamiento
motivado**: el mismo evento, con información objetivamente mixta, es leído de forma
sistemáticamente distinta según la identidad política previa del agente.

## El mecanismo observado: selección asimétrica del dato confirmatorio

La Ronda 2 es el caso más claro porque el evento real combinaba dos señales de signo
opuesto en la misma noticia: el dólar subiendo más que la inflación (señal negativa
para la narrativa oficialista) y un superávit comercial récord (señal positiva). Esto
permite observar, agente por agente, qué dato cada uno elige ponderar:

**Agentes con voto previo LLA:**
- agente_09: *"las cuentas oficialistas que sigo tienen más peso en mi timeline...
  la advertencia del dólar me genera algo de intranquilidad, pero la oposición tampoco
  ofrece una propuesta alternativa concreta"* → retiene el superávit, descarta la
  alarma cambiaria.
- agente_17: *"el superávit comercial récord... son números concretos que le suenan a
  resultados reales. La advertencia sobre el dólar... es técnica y abstracta, no se
  traduce todavía en algo que golpee su bolsillo"* → mismo patrón.
- agente_03: los audios alarmistas de WhatsApp se clasifican explícitamente como
  *"el tipo de cadena alarmista que siempre circula cuando quieren desestabilizar a
  un gobierno que está haciendo las cosas bien"* — el dato negativo no se pondera,
  se invalida como ilegítimo en origen.

**Agentes con voto previo UxP:**
- agente_19: *"el superávit comercial que mencionó el noticiero quedó completamente
  aplastado por la versión del WhatsApp familiar, que es la que pesa emocionalmente"*
  → exactamente el patrón inverso: retiene la alarma cambiaria, descarta el superávit.
- agente_16: *"el superávit comercial récord que mencionaron en el noticiero no se
  siente en el bolsillo de nadie conocido"* — el dato positivo se reconoce pero se
  declara irrelevante por no tener correlato experiencial directo.
- agente_01: clasifica directamente el superávit como *"humo, porque viene de que
  nadie puede comprar nada, no de que la economía anda bien"* — reinterpreta el
  significado del dato positivo en lugar de ignorarlo, convirtiéndolo en evidencia
  en contra.

## Por qué esto no es un bug sino el fenómeno de interés

Es tentador leer el "0 cambios" como una falla del harness (el modelo siendo
demasiado conservador, o no habiendo suficiente "fuerza" en el evento para mover
intención). La revisión cualitativa sugiere lo contrario: los agentes SÍ están
procesando el evento con atención al detalle (citan cifras exactas, fechas,
mecanismos causales), pero el procesamiento está mediado por una identidad política
previa que actúa como filtro de relevancia, no de contenido. Esto reproduce un
fenómeno bien documentado en ciencia política real (motivated reasoning /
confirmation bias en cognición política), lo cual es evidencia a favor de que el
GABM está capturando una dinámica psicológica plausible, no solo generando texto
genérico.

## Limitación importante para no sobre-interpretar

Con apenas 2 rondas y 24 agentes sintéticos, este patrón es sugerente pero no
concluyente. Quedan sin resolver dos preguntas abiertas:

1. **¿Es esto un techo del diseño (los agentes nunca cambiarían con ningún evento
   ambiguo) o una característica realista (la gente real tampoco cambia con
   eventos ambiguos)?** Para distinguirlo, hace falta un evento de Ronda 3 que sea
   difícil de racionalizar en cualquier dirección — algo inequívocamente negativo
   (o positivo) sin lectura alternativa disponible, y ver si ahí sí aparece algún
   cruce de intención.

2. **¿El umbral de cambio requiere acumulación, no un solo evento?** Es posible que
   el mecanismo realista no sea "un evento fuerte cambia el voto" sino "una serie de
   eventos en la misma dirección erosiona gradualmente la identidad hasta un punto
   de quiebre". Esto solo se puede observar con más rondas, no con dos.

## Próximo paso definido

Ronda 3 con un evento deliberadamente "difícil de racionalizar" — elegido entre los
hitos ya identificados en la memoria histórica (dic-2023 a jun-2026) o uno nuevo,
buscando maximizar la dificultad de selección motivada del dato. El objetivo no es
"lograr que cambien" sino testear los límites del modelo de identidad-como-filtro.

---

## Actualización — Ronda 3: derrota electoral PBA (septiembre 2025)

Se eligió deliberadamente un evento sin ambigüedad factual: una derrota electoral de
13 puntos, admitida públicamente por el propio Milei ("hemos tenido una clara
derrota"), con pánico financiero inmediato y verificable (caída del peso ~10%, suba
del riesgo país). A diferencia del evento de Ronda 2 (que mezclaba señales positivas y
negativas en el mismo dato), acá no había forma de negar el hecho central.

**Resultado: 0 de 24 agentes cambiaron de intención, el tercer cero consecutivo.**
Se verificó primero que esto no fuera un artefacto de diseño (el evento siendo tratado
como "noticia vieja" por estar resumido en la memoria histórica base) — la revisión
de razonamientos descarta esa hipótesis: los agentes procesan el shock con intensidad
y detalle propios de un evento que viven en tiempo real, no como dato archivado.

### El mecanismo es más sofisticado que en Ronda 1-2: reinterpretación, no solo descarte

En las rondas anteriores el patrón dominante era *seleccionar* qué dato del evento
ponderar (uno ignora el dato incómodo, retiene el favorable). En Ronda 3, frente a un
hecho que no admite esa salida (no hay "otro dato" que contrarreste una derrota de 13
puntos), el mecanismo que aparece es distinto: **cada bloque identitario reinterpreta
el significado del mismo hecho de forma que termina confirmando su posición previa**:

- Votantes UxP (agente_01, agente_19, agente_22): la derrota se lee como prueba de que
  *"el modelo de Milei es frágil"* — el hecho se absorbe como validación retrospectiva
  de su propio voto opositor.
- Votantes LLA (agente_03, agente_07, agente_09): la derrota se restringe de alcance
  — *"es una elección provincial, no el fin del mundo"*, *"el kirchnerismo siempre
  gana ahí"* — separando lo electoral provincial de "el proyecto nacional", que queda
  indemne.
- Votantes JxC (agente_06, agente_24): la debilidad de ambos polos grandes (oficialismo
  derrotado, pero por un kirchnerismo que tampoco entusiasma) se lee como apertura de
  espacio para "el centro" que JxC dice representar — el evento reafirma su lugar en
  lugar de desplazarlo.
- Indecisos / voto en blanco (agente_02, agente_05, agente_20, agente_21): el festejo
  simétrico de ambos bandos (unos celebran el revés de Milei, otros el triunfo de
  Kicillof) se lee como evidencia de que *"son todos iguales"* — paradójicamente, el
  mismo evento que más debería movilizar a alguien indeciso termina reforzando la
  abstención.

### Por qué esto es un hallazgo más fuerte que el de Ronda 1-2

No es solo que los agentes ignoren información incómoda (sesgo de confirmación
clásico). Es que **no existe, dentro del espacio de eventos probado hasta ahora, un
hecho lo bastante duro como para no ser absorbido por la narrativa identitaria
previa.** Cada bloque tiene una historia ya armada que tiene espacio para metabolizar
tanto buenas como malas noticias sin tensionarse. Esto sugiere que el "filtro de
identidad" en este diseño no opera seleccionando inputs, sino reconstruyendo el
significado de cualquier input — un mecanismo más parecido a un sistema de creencias
auto-sellante que a un simple sesgo de atención.

### Pregunta abierta que esto deja planteada

Si ni un escándalo de corrupción (Ronda 1), ni un dato económico mixto (Ronda 2), ni
una derrota electoral con pánico financiero (Ronda 3) perforan el modelo, la pregunta
relevante para una Ronda 4 ya no es "qué evento sería más fuerte" sino: **¿hay algún
evento, dado este diseño de agente, capaz de moverlos? ¿O el diseño tiene un techo
estructural de inmovilidad que ningún evento individual puede atravesar, y el cambio
solo sería visible con acumulación de muchas rondas, no con un evento puntual por
disruptivo que sea?** Esa es la hipótesis que queda pendiente de testear.

---

## Experimento 2: secuencia cronológica real para testear desgaste acumulado

Tras los resultados del Experimento 1, se decidió reiniciar la simulación (mismos 24
agentes, mismo diseño, historial limpio) con una secuencia de 4 eventos reales del
mandato, todos de signo negativo para el oficialismo y en su orden cronológico real:
(1) escándalo $LIBRA / "Criptogate" (feb-2025), (2) escándalo ANDIS / coimas en
discapacidad (ago-2025), (3) derrota electoral en PBA (sep-2025), (4) síntesis del
Financial Times sobre "la mayor crisis" de la presidencia (sep-2025). El objetivo:
ver si la acumulación de shocks del mismo signo logra lo que un evento aislado no
logró en el Experimento 1.

### Ronda 1 (Libra): primer movimiento real — pero solo hacia el voto en blanco

A diferencia de las 3 rondas del Experimento 1, esta vez **6 de 24 agentes (25%)
cambiaron de intención**. El movimiento agregado: voto en blanco subió de 7 a 9,
mientras LLA, UxP y JxC perdieron un agente cada uno. Examinando quién cambió: los 6
eran **todos ex-votantes de UxP o JxC — ningún ex-votante de LLA cruzó**. Y los 6
migraron **al voto en blanco, no a un partido rival**. El razonamiento típico:
*"UxP tampoco me cierra como opción"*, *"no voy a volver al kirchnerismo"* — Libra
deslegitimó al oficialismo, pero quienes ya tenían dudas sobre su propia opción previa
usaron ese empujón para soltarla también, sin tener adónde ir. El núcleo LLA, en
cambio, sostuvo exactamente el mismo mecanismo de descarte motivado documentado en el
Experimento 1 ("operación política", "ruido de WhatsApp", pesan más los resultados
económicos).

**Primera hipótesis que esto sugiere:** el desgaste acumulado no erosiona parejo —
ataca primero la periferia blanda (votantes no identitarios de cualquier signo) antes
de tocar los núcleos duros de cada espacio.

### Ronda 2 (ANDIS): cero cambios — pero por saturación, no por indiferencia

ANDIS es, en varios sentidos objetivos, un escándalo más grave que Libra (involucra
directamente a Karina Milei, afecta a personas con discapacidad, un juez federal lo
califica de "organización de enriquecimiento ilícito"). Sin embargo, **0 de 24
agentes cambiaron esta ronda**. La revisión de razonamientos descarta que esto sea
indiferencia: los agentes que ya estaban en blanco describen explícitamente el
mecanismo - agente_18: *"con dos casos graves en dos rondas consecutivas la
desconfianza se profundiza, pero no alcanza [para cambiar]"*. El problema no es que
ANDIS no impacte, es que **el voto en blanco es una categoría terminal dentro de este
diseño**: una vez que un agente llega ahí, no existe ningún paso "más allá" al que
moverse. Es una trampa absorbente, no un techo de indiferencia.

Llamativamente, dos agentes del núcleo LLA (agente_09, agente_17) **verbalizan
explícitamente que están aplicando el mismo mecanismo de descarte que usaron con
Libra** ("el mismo patrón que con el Criptogate"), lo cual sugiere que el modelo está
representando una defensa identitaria que se reconoce a sí misma como reiterativa,
no solo una reacción ingenua repetida por casualidad.

### Implicancia metodológica importante

El diseño actual usa una variable categórica discreta de 5 valores (LLA/UxP/JxC/
blanco/otro) para intención de voto. Esto introduce una limitación estructural: el
voto en blanco funciona como absorbente (se puede entrar, no se puede salir dentro
del rango de eventos probado), lo cual podría estar exagerando artificialmente la
estabilidad observada en Ronda 2. Una variable continua (ej. "probabilidad de votar a
cada espacio", o un score de afinidad 0-100 por partido) podría capturar mejor
gradientes de erosión que el esquema categórico no deja ver. Esto queda como mejora
de diseño a considerar si se continúa el experimento.

### Próximos pasos

Quedan dos eventos en la secuencia (derrota PBA, síntesis FT) que ya se sabe, por el
Experimento 1, que probablemente no muevan al núcleo duro. El valor de correrlos
ahora es ver si **erosionan aún más la periferia ya debilitada** (por ejemplo, si
algún agente de LLA empieza a aflojar) o si el patrón de saturación observado en
ANDIS se repite también para ellos.

### Ronda 3 (derrota PBA) y Ronda 4 (síntesis Financial Times): el patrón se sostiene

Ambas rondas confirmaron la hipótesis de saturación: **0 cambios en cada una**,
exactamente en el mismo equilibrio alcanzado tras Libra (9 blanco / 6 UxP / 6 LLA /
2 JxC / 1 otro). Esto incluye el evento de cierre, que no era un hecho aislado más
sino una síntesis periodística internacional (Financial Times) que conectaba
explícitamente los tres eventos previos como una sola "mayor crisis" — ni siquiera
ese marco interpretativo de alto estatus (un medio descrito como parte del
establishment financiero que antes elogiaba a Milei) logró abrir una grieta nueva.

Un detalle destacable del framing de streaming en Ronda 4: el conductor señaló
explícitamente que el análisis del FT *"conecta todo lo que venimos contando acá hace
meses: no son hechos aislados, es un patrón"* — el modelo está representando que los
propios agentes mediáticos narran la acumulación como tal, y aun así eso no traduce
en movimiento adicional de intención de voto. La saturación no es por falta de
narrativa conectiva disponible; el techo persiste incluso cuando la conexión causal
entre eventos se vuelve explícita y viene avalada por una fuente que el propio núcleo
LLA reconocería como creíble en otro contexto.

---

## Conclusión consolidada del Experimento 2

| Ronda | Evento | Cambios | Equilibrio resultante |
|-------|--------|---------|------------------------|
| 1 | $LIBRA (feb-2025) | 6 de 24 (25%) | 9 blanco / 6 UxP / 6 LLA / 2 JxC / 1 otro |
| 2 | ANDIS (ago-2025) | 0 | sin cambios |
| 3 | Derrota PBA (sep-2025) | 0 | sin cambios |
| 4 | Síntesis FT (sep-2025) | 0 | sin cambios |

**El hallazgo central, en una frase:** dado este diseño de agente (24 perfiles
sintéticos, identidad política previa + rasgo de personalidad + canal informativo,
clasificación discreta de intención en 5 categorías), **todo el movimiento observable
ocurrió en el primer evento de la secuencia y consistió exclusivamente en erosión de
la periferia blanda hacia el voto en blanco — el núcleo duro de cada espacio
político permaneció completamente estable a través de cuatro eventos reales de
severidad creciente**, incluyendo uno (ANDIS) que involucra directamente a la
hermana del presidente y uno (síntesis FT) diseñado específicamente para presentar
los hechos anteriores como un patrón acumulativo e innegable.

**Limitaciones a tener en cuenta antes de generalizar:**
1. Es una muestra sintética de 24 agentes, no una encuesta representativa — los
   porcentajes no deben leerse como proyección electoral real.
2. La clasificación categórica (5 valores discretos) probablemente exagera la
   estabilidad observada al convertir el voto en blanco en una trampa absorbente;
   una métrica continua de afinidad partidaria mostraría con más matiz si hay
   erosión interna del núcleo aunque no alcance a cruzar de categoría.
3. Cuatro eventos es una secuencia corta. No puede descartarse que el núcleo LLA
   tenga un punto de quiebre real que simplemente no se alcanzó con esta cantidad
   de shocks - la pregunta "¿existe un techo absoluto o solo uno que requiere más
   acumulación?" queda abierta.

**Lo que sí puede afirmarse con razonable solidez dentro de los límites de este
diseño:** la identidad política previa funciona como filtro interpretativo mucho más
potente que la severidad objetiva de un evento dado. Una vez establecida una postura
(incluso la "postura" de no tener ninguna, el voto en blanco), nuevos eventos del
mismo signo tienden a reforzarla retóricamente sin alterarla en la práctica, dentro
del rango de severidad y cantidad de eventos aquí explorado.

---

## Experimento 3: esquema continuo — ¿hay erosión oculta bajo la categoría estable?

Para resolver la limitación señalada (la categórica puede estar ocultando movimiento
gradual), se rediseñó el motor para pedir un score de afinidad 0-100 por cada espacio
político (LLA/UxP/JxC/otro/blanco, sumando 100) en vez de una única etiqueta. Se
midió una línea de base sobre el estado post-Ronda 5, y luego se corrió un evento
nuevo (Ronda 6: tarifazos combinados de energía y transporte, abril-2026, elegido
específicamente para testear la hipótesis "la gente cambia cuando le tocan el
bolsillo", con datos sin ambigüedad ni contraargumento macro disponible).

### La línea de base ya reveló algo que la categoría ocultaba

Antes de aplicar ningún evento nuevo, la medición continua del estado post-Ronda 5
mostró que **el núcleo LLA es, en promedio, más blando que UxP y JxC** (afinidad
promedio LLA: 73.3, frente a UxP: 82.7 y JxC: 78.5) — una diferencia invisible en el
esquema categórico, donde los tres aparecían igual de "100% sólidos" simplemente
porque ninguno había cruzado de categoría.

### Ronda 6 (tarifazos): hay movimiento real, pero pequeño y consistente

El resumen agregado mostró un movimiento absoluto promedio bajo (2.2 puntos en LLA y
en blanco, menos en los demás) y 0 agentes con cambio ≥10 puntos en un solo evento.
Antes de interpretar esto como "tampoco se mueve nada", se descartó explícitamente
la hipótesis de que el modelo estuviera anclando mecánicamente al score previo sin
razonar: la revisión de los razonamientos individuales muestra lo contrario — varios
agentes del núcleo LLA (agente_03, 07, 09, 17, 19) describen explícitamente *"el
bolsillo empieza a tensionar la convicción, pero no la rompe"*, *"esto le genera una
duda genuina... pero no lo hace cambiar de bando"*, *"el desgaste hacia LLA es cada
vez más evidente"* — y ajustan sus scores en consecuencia, con razones específicas y
verificables (mencionan si su perfil de ingreso los pone o no en la franja afectada
por la quita de subsidios).

**La conclusión más precisa, entonces, no es "el bolsillo no mueve nada" sino algo
más matizado:** hay erosión gradual real, mensurable, y motivada por el contenido
específico del evento — pero su magnitud por evento (3-7 puntos en los casos del
núcleo LLA) es pequeña en relación a la base (70-80 puntos), lo que implica que, a
ese ritmo, se necesitaría una cantidad considerable de eventos de esta intensidad
(no solo dos, como en este experimento) para que el score cruce el punto en que la
categoría dominante cambiaría. Dicho de otra forma: **el modelo está representando
la erosión de la identidad política como un proceso lento de desgaste acumulativo,
no como un interruptor que se activa con un evento (ni siquiera dos) por más
contundente que sea el dato de bolsillo** — lo cual es, en sí mismo, una hipótesis
plausible sobre cómo funciona el realineamiento electoral real, aunque con solo dos
mediciones continuas no se puede afirmar con la misma solidez que las conclusiones
del Experimento 2.

### Limitación honesta de esta tercera fase

Con una sola ronda continua ya aplicada, no hay todavía suficientes puntos para
trazar una "curva de desgaste" real - solo se puede decir que el primer paso fue
chico. Para una conclusión robusta sobre la velocidad de erosión haría falta correr
varias rondas continuas más con eventos del mismo signo y ver si el desgaste se
acelera, se mantiene lineal, o se estabiliza en un nuevo equilibrio sin llegar nunca
al cruce categórico - tres dinámicas posibles que con los datos actuales no se
pueden distinguir entre sí.
