"""British English — reglas de naturalización.

Ortografía británica (colour, centre, organise) y vocabulario
(flat, lift, lorry, holiday, autumn, biscuit).

EXPERIMENTAL: some phrases may contain errors.
"""

from ..engine import Rule, RulePriority

RULES = [
    # ── Ortografía: -our (HIGH) ────────────────────────────────────────
    Rule(
        r"\bcolor\b",
        "colour",
        priority=RulePriority.HIGH,
        description="Spelling: 'color' → 'colour'",
    ),
    Rule(
        r"\bcolors\b",
        "colours",
        priority=RulePriority.HIGH,
        description="Spelling: 'colors' → 'colours'",
    ),
    Rule(
        r"\bfavor\b",
        "favour",
        priority=RulePriority.HIGH,
        description="Spelling: 'favor' → 'favour'",
    ),
    Rule(
        r"\bfavors\b",
        "favours",
        priority=RulePriority.HIGH,
        description="Spelling: 'favors' → 'favours'",
    ),
    Rule(
        r"\bfavorite\b",
        "favourite",
        priority=RulePriority.HIGH,
        description="Spelling: 'favorite' → 'favourite'",
    ),
    Rule(
        r"\bfavorites\b",
        "favourites",
        priority=RulePriority.HIGH,
        description="Spelling: 'favorites' → 'favourites'",
    ),
    Rule(
        r"\bhonor\b",
        "honour",
        priority=RulePriority.HIGH,
        description="Spelling: 'honor' → 'honour'",
    ),
    Rule(
        r"\bhonors\b",
        "honours",
        priority=RulePriority.HIGH,
        description="Spelling: 'honors' → 'honours'",
    ),
    Rule(
        r"\blabor\b",
        "labour",
        priority=RulePriority.HIGH,
        description="Spelling: 'labor' → 'labour'",
    ),
    Rule(
        r"\blabors\b",
        "labours",
        priority=RulePriority.HIGH,
        description="Spelling: 'labors' → 'labours'",
    ),
    Rule(
        r"\bneighbor\b",
        "neighbour",
        priority=RulePriority.HIGH,
        description="Spelling: 'neighbor' → 'neighbour'",
    ),
    Rule(
        r"\bneighbors\b",
        "neighbours",
        priority=RulePriority.HIGH,
        description="Spelling: 'neighbors' → 'neighbours'",
    ),
    Rule(
        r"\brumor\b",
        "rumour",
        priority=RulePriority.HIGH,
        description="Spelling: 'rumor' → 'rumour'",
    ),
    Rule(
        r"\brumors\b",
        "rumours",
        priority=RulePriority.HIGH,
        description="Spelling: 'rumors' → 'rumours'",
    ),
    # ── Ortografía: -re vs -er (HIGH) ──────────────────────────────────
    Rule(
        r"\bcenter\b",
        "centre",
        priority=RulePriority.HIGH,
        description="Spelling: 'center' → 'centre'",
    ),
    Rule(
        r"\bcenters\b",
        "centres",
        priority=RulePriority.HIGH,
        description="Spelling: 'centers' → 'centres'",
    ),
    Rule(
        r"\bliter\b",
        "litre",
        priority=RulePriority.HIGH,
        description="Spelling: 'liter' → 'litre'",
    ),
    Rule(
        r"\bliters\b",
        "litres",
        priority=RulePriority.HIGH,
        description="Spelling: 'liters' → 'litres'",
    ),
    Rule(
        r"\btheater\b",
        "theatre",
        priority=RulePriority.HIGH,
        description="Spelling: 'theater' → 'theatre'",
    ),
    Rule(
        r"\btheaters\b",
        "theatres",
        priority=RulePriority.HIGH,
        description="Spelling: 'theaters' → 'theatres'",
    ),
    Rule(
        r"\bcaliber\b",
        "calibre",
        priority=RulePriority.HIGH,
        description="Spelling: 'caliber' → 'calibre'",
    ),
    # ── Ortografía: -ise vs -ize (HIGH) ────────────────────────────────
    Rule(
        r"\borganize\b",
        "organise",
        priority=RulePriority.HIGH,
        description="Spelling: 'organize' → 'organise'",
    ),
    Rule(
        r"\borganizes\b",
        "organises",
        priority=RulePriority.HIGH,
        description="Spelling: 'organizes' → 'organises'",
    ),
    Rule(
        r"\borganized\b",
        "organised",
        priority=RulePriority.HIGH,
        description="Spelling: 'organized' → 'organised'",
    ),
    Rule(
        r"\brealize\b",
        "realise",
        priority=RulePriority.HIGH,
        description="Spelling: 'realize' → 'realise'",
    ),
    Rule(
        r"\brealizes\b",
        "realises",
        priority=RulePriority.HIGH,
        description="Spelling: 'realizes' → 'realises'",
    ),
    Rule(
        r"\brealized\b",
        "realised",
        priority=RulePriority.HIGH,
        description="Spelling: 'realized' → 'realised'",
    ),
    Rule(
        r"\bapologize\b",
        "apologise",
        priority=RulePriority.HIGH,
        description="Spelling: 'apologize' → 'apologise'",
    ),
    Rule(
        r"\bapologizes\b",
        "apologises",
        priority=RulePriority.HIGH,
        description="Spelling: 'apologizes' → 'apologises'",
    ),
    Rule(
        r"\bapologized\b",
        "apologised",
        priority=RulePriority.HIGH,
        description="Spelling: 'apologized' → 'apologised'",
    ),
    Rule(
        r"\brecognize\b",
        "recognise",
        priority=RulePriority.HIGH,
        description="Spelling: 'recognize' → 'recognise'",
    ),
    Rule(
        r"\brecognizes\b",
        "recognises",
        priority=RulePriority.HIGH,
        description="Spelling: 'recognizes' → 'recognises'",
    ),
    Rule(
        r"\brecognized\b",
        "recognised",
        priority=RulePriority.HIGH,
        description="Spelling: 'recognized' → 'recognised'",
    ),
    # ── Ortografía: otras (HIGH) ────────────────────────────────────────
    Rule(
        r"\btraveled\b",
        "travelled",
        priority=RulePriority.HIGH,
        description="Spelling: 'traveled' → 'travelled'",
    ),
    Rule(
        r"\btraveling\b",
        "travelling",
        priority=RulePriority.HIGH,
        description="Spelling: 'traveling' → 'travelling'",
    ),
    Rule(
        r"\btraveler\b",
        "traveller",
        priority=RulePriority.HIGH,
        description="Spelling: 'traveler' → 'traveller'",
    ),
    Rule(
        r"\bcanceled\b",
        "cancelled",
        priority=RulePriority.HIGH,
        description="Spelling: 'canceled' → 'cancelled'",
    ),
    Rule(
        r"\bcanceling\b",
        "cancelling",
        priority=RulePriority.HIGH,
        description="Spelling: 'canceling' → 'cancelling'",
    ),
    Rule(
        r"\bdefense\b",
        "defence",
        priority=RulePriority.HIGH,
        description="Spelling: 'defense' → 'defence'",
    ),
    Rule(
        r"\boffense\b",
        "offence",
        priority=RulePriority.HIGH,
        description="Spelling: 'offense' → 'offence'",
    ),
    Rule(
        r"\blicense\b",
        "licence",
        priority=RulePriority.HIGH,
        description="Spelling: 'license' → 'licence' (noun)",
    ),
    Rule(
        r"\bpractice\b",
        "practise",
        priority=RulePriority.HIGH,
        description="Spelling: 'practice' → 'practise' (verb)",
    ),
    Rule(
        r"\bcheck\b",
        "cheque",
        priority=RulePriority.HIGH,
        description="Spelling: 'check' → 'cheque' (financial)",
    ),
    Rule(
        r"\bprogram\b",
        "programme",
        priority=RulePriority.HIGH,
        description="Spelling: 'program' → 'programme'",
    ),
    Rule(
        r"\bdialog\b",
        "dialogue",
        priority=RulePriority.HIGH,
        description="Spelling: 'dialog' → 'dialogue'",
    ),
    Rule(
        r"\bcatalog\b",
        "catalogue",
        priority=RulePriority.HIGH,
        description="Spelling: 'catalog' → 'catalogue'",
    ),
    Rule(
        r"\bdisk\b",
        "disc",
        priority=RulePriority.HIGH,
        description="Spelling: 'disk' → 'disc'",
    ),
    # ── Vocabulario: vivienda (MEDIUM) ─────────────────────────────────
    Rule(
        r"\bapartment\b",
        "flat",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'apartment' → 'flat'",
    ),
    Rule(
        r"\bapartments\b",
        "flats",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'apartments' → 'flats'",
    ),
    Rule(
        r"\belevator\b",
        "lift",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'elevator' → 'lift'",
    ),
    Rule(
        r"\belevators\b",
        "lifts",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'elevators' → 'lifts'",
    ),
    Rule(
        r"\byard\b",
        "garden",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'yard' → 'garden' (residential)",
    ),
    Rule(
        r"\bdowntown\b",
        "city centre",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'downtown' → 'city centre'",
    ),
    # ── Vocabulario: transporte (MEDIUM) ───────────────────────────────
    Rule(
        r"\btruck\b",
        "lorry",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'truck' → 'lorry'",
    ),
    Rule(
        r"\btrucks\b",
        "lorries",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'trucks' → 'lorries'",
    ),
    Rule(
        r"\bsidewalk\b",
        "pavement",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'sidewalk' → 'pavement'",
    ),
    Rule(
        r"\bsidewalks\b",
        "pavements",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'sidewalks' → 'pavements'",
    ),
    Rule(
        r"\bsubway\b",
        "underground",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'subway' → 'underground'",
    ),
    Rule(
        r"\bgas station\b",
        "petrol station",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'gas station' → 'petrol station'",
    ),
    Rule(
        r"\bgas\b",
        "petrol",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'gas' → 'petrol' (fuel)",
    ),
    # ── Vocabulario: comida (MEDIUM) ───────────────────────────────────
    Rule(
        r"\bcookies\b",
        "biscuits",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'cookies' → 'biscuits'",
    ),
    Rule(
        r"\bcookie\b",
        "biscuit",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'cookie' → 'biscuit'",
    ),
    Rule(
        r"\bfrench fries\b",
        "chips",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'french fries' → 'chips'",
    ),
    Rule(
        r"\bchips\b",
        "crisps",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'chips' → 'crisps'",
    ),
    Rule(
        r"\bcandy\b",
        "sweets",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'candy' → 'sweets'",
    ),
    Rule(
        r"\bsoda\b",
        "fizzy drink",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'soda' → 'fizzy drink'",
    ),
    # ── Vocabulario: ropa (MEDIUM) ─────────────────────────────────────
    Rule(
        r"\bpants\b",
        "trousers",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'pants' → 'trousers'",
    ),
    Rule(
        r"\bsweater\b",
        "jumper",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'sweater' → 'jumper'",
    ),
    Rule(
        r"\bsneakers\b",
        "trainers",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'sneakers' → 'trainers'",
    ),
    Rule(
        r"\bvest\b",
        "waistcoat",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'vest' → 'waistcoat'",
    ),
    # ── Vocabulario: educación (MEDIUM) ────────────────────────────────
    Rule(
        r"\bvacation\b",
        "holiday",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'vacation' → 'holiday'",
    ),
    Rule(
        r"\bfall\b",
        "autumn",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'fall' → 'autumn' (season)",
    ),
    Rule(
        r"\bprincipal\b",
        "headteacher",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'principal' → 'headteacher'",
    ),
    Rule(
        r"\bgrade\b",
        "year",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'grade' → 'year' (school)",
    ),
    Rule(
        r"\bgrades\b",
        "years",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'grades' → 'years'",
    ),
    Rule(
        r"\bcollege\b",
        "university",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'college' → 'university'",
    ),
    # ── Vocabulario: expresiones (MEDIUM) ──────────────────────────────
    Rule(
        r"\bfries\b",
        "chips",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'fries' → 'chips'",
    ),
    Rule(
        r"\bhello\b",
        "hiya",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'hello' → 'hiya'",
    ),
    Rule(
        r"\bthank you\b",
        "cheers",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'thank you' → 'cheers'",
    ),
    Rule(
        r"\bthanks\b",
        "cheers",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'thanks' → 'cheers'",
    ),
    Rule(
        r"\byou are welcome\b",
        "no worries",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'you are welcome' → 'no worries'",
    ),
    Rule(
        r"\bmovie\b",
        "film",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'movie' → 'film'",
    ),
    Rule(
        r"\bmovies\b",
        "films",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'movies' → 'films'",
    ),
    Rule(
        r"\bmail\b",
        "post",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'mail' → 'post'",
    ),
    Rule(
        r"\bmailman\b",
        "postman",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'mailman' → 'postman'",
    ),
    Rule(
        r"\bcell phone\b",
        "mobile phone",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'cell phone' → 'mobile phone'",
    ),
    Rule(
        r"\bcellphone\b",
        "mobile",
        priority=RulePriority.MEDIUM,
        description="Vocab: 'cellphone' → 'mobile'",
    ),
]
