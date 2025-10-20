"""
Sistema de preguntas de inglés para el juego Mario.
Temas: WILL y GOING TO
Niveles de dificultad: 1 (básico) a 5 (avanzado)
"""

from typing import Dict, List, Tuple
from enum import Enum

class TipoPregunta(Enum):
    GOING_TO_BASICO = "going_to_basico"
    GOING_TO_INTERMEDIO = "going_to_intermedio"
    WILL_BASICO = "will_basico"
    WILL_INTERMEDIO = "will_intermedio"
    MIXTO_AVANZADO = "mixto_avanzado"

class TipoPuerta(Enum):
    OBLIGATORIA = "obligatoria"  # Bloquea el camino principal
    OPCIONAL_SECRETA = "opcional_secreta"  # Acceso a área secreta
    OPCIONAL_BONUS = "opcional_bonus"  # Power-ups extra
    LLAVE_ESPECIAL = "llave_especial"  # Da llave para puertas especiales

# Estructura: (pregunta, [opcion_a, opcion_b, opcion_c, opcion_d], respuesta_correcta_index, explicacion)
PREGUNTAS_DATABASE = {
    # =================== GOING TO - BÁSICO (Niveles 1-2) ===================
    TipoPregunta.GOING_TO_BASICO: [
        (
            "I ___ study English tomorrow.",
            ["am going to", "will going", "going to", "am going"],
            0,
            "Usamos 'be + going to' para planes futuros."
        ),
        (
            "She ___ visit her grandmother next week.",
            ["will going to", "is going to", "going to", "are going to"],
            1,
            "Con 'she' usamos 'is going to'."
        ),
        (
            "They ___ play soccer this afternoon.",
            ["is going to", "am going to", "are going to", "will going"],
            2,
            "Con 'they' usamos 'are going to'."
        ),
        (
            "We ___ watch a movie tonight.",
            ["is going to", "are going to", "am going to", "will going"],
            1,
            "Con 'we' usamos 'are going to'."
        ),
        (
            "Maria ___ cook dinner for us.",
            ["are going to", "is going to", "am going to", "going to"],
            1,
            "Con nombres propios usamos 'is going to'."
        ),
        (
            "The children ___ go to the park.",
            ["is going to", "am going to", "are going to", "will going"],
            2,
            "Con sujetos plurales usamos 'are going to'."
        ),
        (
            "I ___ buy a new car next month.",
            ["am going to", "is going to", "are going to", "will going"],
            0,
            "Con 'I' usamos 'am going to'."
        ),
        (
            "He ___ learn to drive soon.",
            ["are going to", "am going to", "is going to", "will going"],
            2,
            "Con 'he' usamos 'is going to'."
        )
    ],
    
    # =================== GOING TO - INTERMEDIO (Nivel 2-3) ===================
    TipoPregunta.GOING_TO_INTERMEDIO: [
        (
            "Look at those clouds! It ___ rain.",
            ["will", "is going to", "are going to", "going to"],
            1,
            "Usamos 'going to' para predicciones basadas en evidencia."
        ),
        (
            "She's not ___ come to the party.",
            ["going to", "will", "go to", "going"],
            0,
            "En negativo: 'not going to'."
        ),
        (
            "Are you ___ study abroad?",
            ["will", "going to", "go to", "going"],
            1,
            "En pregunta: 'Are you going to...?'"
        ),
        (
            "The team ___ win the championship. They're very strong!",
            ["will", "is going to", "are going to", "going to"],
            2,
            "Predicción basada en evidencia actual."
        ),
        (
            "I don't think I ___ finish this project today.",
            ["am going to", "will", "going to", "am going"],
            0,
            "Con planes personales usamos 'going to'."
        ),
        (
            "What ___ you do this weekend?",
            ["will", "are going to", "is going to", "going to"],
            1,
            "Pregunta sobre planes: 'are going to'."
        )
    ],
    
    # =================== WILL - BÁSICO (Niveles 3-4) ===================
    TipoPregunta.WILL_BASICO: [
        (
            "I ___ help you with your homework.",
            ["am going to", "will", "going to", "am going"],
            1,
            "Usamos 'will' para decisiones espontáneas y ofertas."
        ),
        (
            "She ___ be here at 3 PM.",
            ["is going to", "will", "going to", "are going to"],
            1,
            "'Will' para promesas y predicciones generales."
        ),
        (
            "It ___ be sunny tomorrow.",
            ["is going to", "will", "are going to", "going to"],
            1,
            "'Will' para predicciones sin evidencia específica."
        ),
        (
            "They ___ not come to the meeting.",
            ["are going to", "will", "going to", "is going to"],
            1,
            "Negativo con will: 'will not' o 'won't'."
        ),
        (
            "___ you open the window, please?",
            ["Are going to", "Will", "Going to", "Are"],
            1,
            "'Will' para peticiones educadas."
        ),
        (
            "We ___ travel to Europe next year.",
            ["will", "are going to", "going to", "is going to"],
            0,
            "'Will' para decisiones futuras no planificadas."
        ),
        (
            "The phone is ringing. I ___ answer it.",
            ["am going to", "will", "going to", "am"],
            1,
            "'Will' para decisiones inmediatas y espontáneas."
        ),
        (
            "Don't worry, everything ___ be fine.",
            ["is going to", "will", "are going to", "going to"],
            1,
            "'Will' para tranquilizar y dar esperanza."
        )
    ],
    
    # =================== WILL - INTERMEDIO (Nivel 4) ===================
    TipoPregunta.WILL_INTERMEDIO: [
        (
            "I think robots ___ replace many jobs in the future.",
            ["are going to", "will", "going to", "is going to"],
            1,
            "'Will' para predicciones basadas en opiniones."
        ),
        (
            "If it rains, we ___ stay inside.",
            ["are going to", "will", "going to", "is going to"],
            1,
            "Usamos 'will' en frases condicionales."
        ),
        (
            "___ there be flying cars in 2050?",
            ["Are going to", "Will", "Going to", "Is going to"],
            1,
            "Preguntas sobre el futuro con 'will'."
        ),
        (
            "She probably ___ arrive late.",
            ["is going to", "will", "going to", "are going to"],
            1,
            "'Will' con adverbios de probabilidad."
        ),
        (
            "Technology ___ change our lives completely.",
            ["is going to", "will", "going to", "are going to"],
            1,
            "'Will' para predicciones generales sobre el futuro."
        ),
        (
            "When I'm older, I ___ become a doctor.",
            ["am going to", "will", "going to", "am"],
            1,
            "'Will' en frases temporales futuras."
        )
    ],
    
    # =================== MIXTO AVANZADO (Nivel 5) ===================
    TipoPregunta.MIXTO_AVANZADO: [
        (
            "Look! The vase ___! (It's falling)",
            ["will break", "is going to break", "breaks", "is breaking"],
            1,
            "Evidencia visual → 'going to' para predicciones inmediatas."
        ),
        (
            "A: 'We don't have milk.' B: 'Don't worry, I ___ buy some.'",
            ["am going to", "will", "going to", "am"],
            1,
            "Decisión espontánea en respuesta → 'will'."
        ),
        (
            "According to the weather forecast, it ___ snow tomorrow.",
            ["will", "is going to", "going to", "are going to"],
            1,
            "Plan basado en información → 'going to'."
        ),
        (
            "I believe humans ___ live on Mars someday.",
            ["are going to", "will", "going to", "is going to"],
            1,
            "Creencia/opinión personal → 'will'."
        ),
        (
            "She has saved money and ___ buy a house.",
            ["will", "is going to", "going to", "are going to"],
            1,
            "Plan preparado con evidencia → 'going to'."
        ),
        (
            "If you study hard, you ___ pass the exam.",
            ["are going to", "will", "going to", "is going to"],
            1,
            "Condicional → 'will'."
        ),
        (
            "A: 'The doorbell is ringing.' B: 'I ___ get it.'",
            ["am going to", "will", "going to", "am"],
            1,
            "Reacción inmediata → 'will'."
        ),
        (
            "Next week I ___ start my new job. (Already arranged)",
            ["will", "am going to", "going to", "am"],
            1,
            "Plan ya organizado → 'going to'."
        )
    ]
}

# Distribución de preguntas por nivel
PREGUNTAS_POR_NIVEL = {
    1: [TipoPregunta.GOING_TO_BASICO],
    2: [TipoPregunta.GOING_TO_BASICO, TipoPregunta.GOING_TO_INTERMEDIO],
    3: [TipoPregunta.GOING_TO_INTERMEDIO, TipoPregunta.WILL_BASICO],
    4: [TipoPregunta.WILL_BASICO, TipoPregunta.WILL_INTERMEDIO],
    5: [TipoPregunta.WILL_INTERMEDIO, TipoPregunta.MIXTO_AVANZADO]
}

# Configuración de puertas por nivel
CONFIGURACION_PUERTAS = {
    1: {
        "obligatorias": 1,      # 1 puerta obligatoria
        "opcionales": 2,        # 2 puertas opcionales
        "llaves_necesarias": 0  # No necesita llaves especiales
    },
    2: {
        "obligatorias": 1,
        "opcionales": 2,
        "llaves_necesarias": 0
    },
    3: {
        "obligatorias": 2,
        "opcionales": 1,
        "llaves_necesarias": 1  # Necesita 1 llave del nivel anterior
    },
    4: {
        "obligatorias": 2,
        "opcionales": 2,
        "llaves_necesarias": 2
    },
    5: {
        "obligatorias": 1,      # Solo 1 antes de la princesa
        "opcionales": 3,        # Muchas opcionales para bonus
        "llaves_necesarias": 3  # Necesita todas las llaves
    }
}

def obtener_pregunta_aleatoria(nivel: int, tipo_puerta: TipoPuerta) -> Tuple[str, List[str], int, str]:
    """
    Obtiene una pregunta aleatoria según el nivel y tipo de puerta.
    Las opciones se mezclan aleatoriamente para que la respuesta correcta no siempre esté en la misma posición.
    
    Args:
        nivel: Nivel del juego (1-5)
        tipo_puerta: Tipo de puerta que se está abriendo
    
    Returns:
        Tupla con (pregunta, opciones_mezcladas, nueva_respuesta_correcta, explicacion)
    """
    import random
    
    # Seleccionar tipos de pregunta según el nivel
    tipos_disponibles = PREGUNTAS_POR_NIVEL.get(nivel, [TipoPregunta.GOING_TO_BASICO])
    
    # Para puertas especiales, usar preguntas más difíciles
    if tipo_puerta == TipoPuerta.LLAVE_ESPECIAL and nivel > 2:
        # Usar preguntas del siguiente nivel de dificultad
        tipos_disponibles = PREGUNTAS_POR_NIVEL.get(min(5, nivel + 1), tipos_disponibles)
    
    # Seleccionar tipo de pregunta al azar
    tipo_pregunta = random.choice(tipos_disponibles)
    
    # Seleccionar pregunta específica
    preguntas = PREGUNTAS_DATABASE[tipo_pregunta]
    pregunta, opciones, respuesta_correcta_original, explicacion = random.choice(preguntas)
    
    # MEZCLAR LAS OPCIONES ALEATORIAMENTE
    # Crear lista de índices para mezclar
    indices = list(range(len(opciones)))
    random.shuffle(indices)
    
    # Mezclar las opciones según los índices aleatorios
    opciones_mezcladas = [opciones[i] for i in indices]
    
    # Encontrar la nueva posición de la respuesta correcta
    nueva_respuesta_correcta = indices.index(respuesta_correcta_original)
    
    return (pregunta, opciones_mezcladas, nueva_respuesta_correcta, explicacion)

def obtener_configuracion_nivel(nivel: int) -> Dict:
    """Obtiene la configuración de puertas para un nivel específico."""
    return CONFIGURACION_PUERTAS.get(nivel, CONFIGURACION_PUERTAS[1])

def validar_respuesta(pregunta_info: Tuple, respuesta_usuario: int) -> bool:
    """
    Valida si la respuesta del usuario es correcta.
    
    Args:
        pregunta_info: Tupla con información de la pregunta
        respuesta_usuario: Índice de la respuesta seleccionada (0-3)
    
    Returns:
        True si es correcta, False si no
    """
    _, _, respuesta_correcta, _ = pregunta_info
    return respuesta_usuario == respuesta_correcta