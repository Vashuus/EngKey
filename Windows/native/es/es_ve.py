"""Venezolano — reglas de naturalización.

Coloquialismos y expresiones típicas de Venezuela.
"""

RULES = [
    # ── Saludos y cortesía ───────────────────────────────────────────
    (r"\bmuchas gracias\b",   "gracias a ti"),
    (r"\b¿cómo estás\??\b",   "¿qué más?"),
    (r"\b¿cómo está\??\b",    "¿qué más?"),
    (r"\bmucho gusto\b",      "un placer"),
    (r"\bpor favor\b",        "porfa"),
    # ── Afirmaciones / acuerdo ───────────────────────────────────────
    (r"\bestá bien\b",        "vale"),
    (r"\bde acuerdo\b",       "dale"),
    (r"\bno importa\b",       "da igual"),
    (r"\bpor supuesto\b",     "claro que sí"),
    # ── Coloquialismos léxicos ────────────────────────────────────────
    (r"\bchico\b",            "pana"),       # guy / friend
    (r"\bchicos\b",           "panas"),
    (r"\bamigo\b",            "pana"),
    (r"\bamigos\b",           "panas"),
    (r"\bgenial\b",           "chévere"),
    (r"\bmuy bueno\b",        "chévere"),
    (r"\bexcelente\b",        "chévere"),
    (r"\bdinero\b",           "plata"),
    (r"\bcosa\b",             "vaina"),      # thing
    (r"\bcosas\b",            "vainas"),
    (r"\bniño\b",             "chamo"),
    (r"\bniña\b",             "chama"),
    (r"\bniños\b",            "chamos"),
    (r"\bdivertido\b",        "chévere"),
    (r"\bdivertida\b",        "chévere"),
    (r"\bestúpido\b",         "güevón"),
    (r"\bestá bromeando\b",   "está echando broma"),
    (r"\bbroma\b",            "echar broma"),
    # ── Expresiones ───────────────────────────────────────────────────
    (r"\bestoy de acuerdo\b", "dale"),
    (r"\bno me gusta\b",     "no me cuadra"),
    (r"\bestoy cansado\b",   "estoy molido"),
    (r"\bestá cansado\b",    "está molido"),
    (r"\bhace calor\b",      "está candela"),
    (r"\bhace frío\b",       "está fresco"),
    (r"\bme alegro\b",       "qué bien"),
    (r"\bcuídate\b",         "cuídate mucho"),
]
