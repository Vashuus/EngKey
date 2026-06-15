"""Argentino — reglas de naturalización.

Voseo (vos, tenés, sos, podés), lunfardo y coloquialismos rioplatenses.
"""

RULES = [
    # ── Voseo: pronombre ─────────────────────────────────────────────
    (r"\btú tienes\b",        "vos tenés"),
    (r"\btú eres\b",          "vos sos"),
    (r"\btú puedes\b",        "vos podés"),
    (r"\btú quieres\b",       "vos querés"),
    (r"\btú sabes\b",         "vos sabés"),
    (r"\btú dices\b",         "vos decís"),
    (r"\btú haces\b",         "vos hacés"),
    (r"\btú vienes\b",        "vos venís"),
    (r"\btú piensas\b",       "vos pensás"),
    (r"\btú entiendes\b",     "vos entendés"),
    (r"\btú necesitas\b",     "vos necesitás"),
    (r"\btú tienes que\b",    "vos tenés que"),
    (r"\btú puedes\b",        "vos podés"),
    (r"\btú estás\b",         "vos estás"),
    (r"\btú andas\b",         "vos andás"),
    (r"\btú eres\b",          "vos sos"),
    # ── Saludos y cortesía ───────────────────────────────────────────
    (r"\bmuchas gracias\b",   "gracias che"),
    (r"\b¿cómo estás\??\b",   "¿cómo andás?"),
    (r"\b¿cómo está\??\b",    "¿cómo anda?"),
    (r"\bmucho gusto\b",      "un placer che"),
    (r"\bpor favor\b",        "porfa"),
    (r"\bhasta luego\b",      "chau"),
    (r"\badiós\b",            "chau"),
    # ── Afirmaciones / acuerdo ───────────────────────────────────────
    (r"\bestá bien\b",        "dale"),
    (r"\bde acuerdo\b",       "dale"),
    (r"\bno importa\b",       "no pasa nada"),
    (r"\bpor supuesto\b",     "obvio"),
    (r"\bexacto\b",           "obvio"),
    # ── Lunfardo / coloquialismos ────────────────────────────────────
    (r"\bchico\b",            "pibe"),
    (r"\bchica\b",            "piba"),
    (r"\bchicos\b",           "pibes"),
    (r"\bamigo\b",            "boludo"),   # entre amigos
    (r"\bamiga\b",            "boluda"),
    (r"\bamigos\b",           "boludos"),
    (r"\bgenial\b",           "copado"),
    (r"\bdivertido\b",        "copado"),
    (r"\bdivertida\b",        "copada"),
    (r"\bdinero\b",           "guita"),
    (r"\btrabajar\b",         "laburar"),
    (r"\btrabajo\b",          "laburo"),
    (r"\btrabaja\b",          "labura"),
    (r"\bestúpido\b",         "boludo"),
    (r"\bestúpida\b",         "boluda"),
    (r"\bautobús\b",          "bondi"),
    (r"\bcolectivo\b",        "bondi"),
    (r"\bdesorden\b",         "quilombo"),
    (r"\blío\b",              "quilombo"),
    (r"\bproblema\b",         "quilombo"),
    (r"\bmujer\b",            "mina"),     # informal
    (r"\bchica\b",            "mina"),
    (r"\bbueno\b",            "bue"),       # informal "bueno" -> "bue"
    # ── Expresiones ───────────────────────────────────────────────────
    (r"\bno me gusta\b",      "no me copa"),
    (r"\bme alegro\b",        "qué bueno che"),
    (r"\bqué bueno\b",        "qué bueno che"),
    (r"\bcuídate\b",          "cuidate che"),
    (r"\bestoy cansado\b",    "estoy re quemado"),
    (r"\bestá cansado\b",     "está re quemado"),
    (r"\bhace calor\b",       "calor del orto"),
    (r"\bhace frío\b",        "frío del orto"),
]
