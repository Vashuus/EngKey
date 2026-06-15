"""British English — reglas de naturalización.

Ortografía británica (colour, centre, organise) y vocabulario
(flat, lift, lorry, holiday, autumn, biscuit).
"""

# Reglas seguras: patrón -> reemplazo (con \b para palabra completa).
# NOTA: Google Translate da por defecto inglés americano,
# así que estas reglas convierten US -> UK.
# NO se incluyen reglas de contracciones (son iguales en UK/US).

RULES = [
    # ── Ortografía: -our ─────────────────────────────────────────────
    (r"\bcolor\b",            "colour"),
    (r"\bcolors\b",           "colours"),
    (r"\bfavor\b",            "favour"),
    (r"\bfavors\b",           "favours"),
    (r"\bfavorite\b",         "favourite"),
    (r"\bfavorites\b",        "favourites"),
    (r"\bhonor\b",            "honour"),
    (r"\bhonors\b",           "honours"),
    (r"\blabor\b",            "labour"),
    (r"\blabors\b",           "labours"),
    (r"\bneighbor\b",         "neighbour"),
    (r"\bneighbors\b",        "neighbours"),
    (r"\brumor\b",            "rumour"),
    (r"\brumors\b",           "rumours"),
    # ── Ortografía: -re vs -er ────────────────────────────────────────
    (r"\bcenter\b",           "centre"),
    (r"\bcenters\b",          "centres"),
    (r"\bliter\b",            "litre"),
    (r"\bliters\b",           "litres"),
    (r"\btheater\b",          "theatre"),
    (r"\btheaters\b",         "theatres"),
    (r"\bcaliber\b",          "calibre"),
    # ── Ortografía: -ise vs -ize ──────────────────────────────────────
    (r"\borganize\b",         "organise"),
    (r"\borganizes\b",        "organises"),
    (r"\borganized\b",        "organised"),
    (r"\brealize\b",          "realise"),
    (r"\brealizes\b",         "realises"),
    (r"\brealized\b",         "realised"),
    (r"\bapologize\b",        "apologise"),
    (r"\bapologizes\b",       "apologises"),
    (r"\bapologized\b",       "apologised"),
    (r"\brecognize\b",        "recognise"),
    (r"\brecognizes\b",       "recognises"),
    (r"\brecognized\b",       "recognised"),
    # ── Ortografía: otras ─────────────────────────────────────────────
    (r"\btraveled\b",         "travelled"),
    (r"\btraveling\b",        "travelling"),
    (r"\btraveler\b",         "traveller"),
    (r"\bcanceled\b",         "cancelled"),
    (r"\bcanceling\b",        "cancelling"),
    (r"\bdefense\b",          "defence"),
    (r"\boffense\b",          "offence"),
    (r"\blicense\b",          "licence"),  # noun form
    (r"\bpractice\b",         "practise"), # verb form
    (r"\bcheck\b",            "cheque"),   # financial
    (r"\bprogram\b",          "programme"),
    (r"\bdialog\b",           "dialogue"),
    (r"\bcatalog\b",          "catalogue"),
    (r"\bdisk\b",             "disc"),
    # ── Vocabulario: vivienda ─────────────────────────────────────────
    (r"\bapartment\b",        "flat"),
    (r"\bapartments\b",       "flats"),
    (r"\belevator\b",         "lift"),
    (r"\belevators\b",        "lifts"),
    (r"\byard\b",             "garden"),   # residential
    (r"\bdowntown\b",         "city centre"),
    # ── Vocabulario: transporte ───────────────────────────────────────
    (r"\btruck\b",            "lorry"),
    (r"\btrucks\b",           "lorries"),
    (r"\bsidewalk\b",         "pavement"),
    (r"\bsidewalks\b",        "pavements"),
    (r"\bsubway\b",           "underground"),
    (r"\bgas station\b",      "petrol station"),
    (r"\bgas\b",              "petrol"),   # fuel
    # ── Vocabulario: comida ───────────────────────────────────────────
    (r"\bcookies\b",          "biscuits"),
    (r"\bcookie\b",           "biscuit"),
    (r"\bfrench fries\b",     "chips"),
    (r"\bchips\b",            "crisps"),   # potato chips
    (r"\bcandy\b",            "sweets"),
    (r"\bsoda\b",             "fizzy drink"),
    # ── Vocabulario: ropa ─────────────────────────────────────────────
    (r"\bpants\b",            "trousers"),
    (r"\bsweater\b",          "jumper"),
    (r"\bsneakers\b",         "trainers"),
    (r"\bvest\b",             "waistcoat"),
    # ── Vocabulario: educación ────────────────────────────────────────
    (r"\bvacation\b",         "holiday"),
    (r"\bfall\b",             "autumn"),   # season
    (r"\bprincipal\b",        "headteacher"),
    (r"\bgrade\b",            "year"),     # school year
    (r"\bgrades\b",           "years"),
    (r"\bcollege\b",          "university"),
    # ── Vocabulario: expresiones ──────────────────────────────────────
    (r"\bfries\b",            "chips"),
    (r"\bhello\b",            "hiya"),
    (r"\bthank you\b",        "cheers"),
    (r"\bthanks\b",           "cheers"),
    (r"\byou are welcome\b",  "no worries"),
    (r"\bmovie\b",            "film"),
    (r"\bmovies\b",           "films"),
    (r"\bmail\b",             "post"),
    (r"\bmailman\b",          "postman"),
    (r"\bcell phone\b",       "mobile phone"),
    (r"\bcellphone\b",        "mobile"),
]
