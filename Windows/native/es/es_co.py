"""Colombiano — reglas de naturalización.

Coloquialismos y expresiones típicas de Colombia.
"""

RULES = [
    # ── Saludos y cortesía ───────────────────────────────────────────
    (r"\bmuchas gracias\b",   "gracias parce"),
    (r"\b¿cómo estás\??\b",   "¿qué más?"),
    (r"\b¿cómo está\??\b",    "¿qué más?"),
    (r"\bmucho gusto\b",      "un placer parce"),
    (r"\bpor favor\b",        "porfa"),
    # ── Afirmaciones / acuerdo ───────────────────────────────────────
    (r"\bestá bien\b",        "listo"),
    (r"\bde acuerdo\b",       "listo"),
    (r"\bno importa\b",       "no pasa nada"),
    (r"\bpor supuesto\b",     "claro que sí"),
    (r"\bexacto\b",           "exacto parce"),
    # ── Coloquialismos léxicos ────────────────────────────────────────
    (r"\bamigo\b",            "parcero"),
    (r"\bamiga\b",            "parcera"),
    (r"\bamigos\b",           "parceros"),
    (r"\bchico\b",            "parce"),
    (r"\bchicos\b",           "parceros"),
    (r"\bgenial\b",           "bacano"),
    (r"\bdivertido\b",        "bacano"),
    (r"\bdivertida\b",        "bacana"),
    (r"\bdinero\b",           "plata"),
    (r"\bniño\b",             "chino"),
    (r"\bniña\b",             "china"),
    (r"\bniños\b",            "chinos"),
    (r"\btonto\b",            "huevón"),
    (r"\btonta\b",            "huevona"),
    # ── Expresiones ───────────────────────────────────────────────────
    (r"\bestoy de acuerdo\b", "listo"),
    (r"\bno me gusta\b",      "no me cuadra"),
    (r"\bme alegro\b",        "qué chévere"),
    (r"\bten cuidado\b",      "pilas"),
    (r"\btenga cuidado\b",    "pilas"),
    (r"\bcuídate\b",          "cuídate parce"),
]
