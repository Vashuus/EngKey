"""Normalization pre-pass — expands compounds written as one word before NativeMode.

Spanish speakers often write compound expressions as a single word
(e.g. "deacuerdo" instead of "de acuerdo"). This module normalizes
these cases before the rule engine processes them.

EXPERIMENTAL: the list may not be exhaustive.
"""

import re

# (one_word_form, expanded_form, language)
# Sorted: longer entries first prevent false positives
_COMPOUNDS: list[tuple[str, str, str]] = [
    ("deacuerdo",     "de acuerdo",     "es"),
    ("deacuerdo",     "de acuerdo",     "en"),
    ("sobretodo",     "sobre todo",     "es"),
    ("enfin",         "en fin",         "es"),
    ("aveces",        "a veces",        "es"),
    ("aparte",        "a parte",        "es"),
    ("aparte",        "a parte",        "en"),
    ("adonde",        "a donde",        "es"),
    ("adonde",        "a donde",        "en"),
    ("acercade",      "acerca de",      "es"),
    ("acercade",      "acerca de",      "en"),
    ("debajode",      "debajo de",      "es"),
    ("delantede",     "delante de",     "es"),
    ("detrasde",      "detras de",      "es"),
    ("encimade",      "encima de",      "es"),
    ("dentrode",      "dentro de",      "es"),
    ("juntoa",        "junto a",        "es"),
    ("lejosde",       "lejos de",       "es"),
    ("fuerade",       "fuera de",       "es"),
]


_PATTERNS_BY_LANG: dict[str, list[tuple[re.Pattern, str]]] = {}

def _build() -> None:
    _PATTERNS_BY_LANG.clear()
    sorted_c = sorted(_COMPOUNDS, key=lambda x: -len(x[0]))
    for raw, expanded, lang in sorted_c:
        escaped = re.escape(raw)
        pat = re.compile(r"\b" + escaped + r"\b", re.IGNORECASE | re.UNICODE)
        _PATTERNS_BY_LANG.setdefault(lang, []).append((pat, expanded))


_build()


def pre_normalize(text: str, lang: str | None = None) -> str:
    """Expand compounds written as one word.

    If ``lang`` is provided, only entries for that language are applied.
    If ``None``, all entries are applied (default).
    """
    if not text:
        return text

    result = text
    patterns = _PATTERNS_BY_LANG.get(lang) if lang else None

    if patterns is None:
        for lang_pats in _PATTERNS_BY_LANG.values():
            for pat, replacement in lang_pats:
                result = pat.sub(replacement, result)
    else:
        for pat, replacement in patterns:
            result = pat.sub(replacement, result)

    return result
