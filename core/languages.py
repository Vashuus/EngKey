"""Supported languages for translation.

Display names show both native name and English name for clarity,
e.g. \"Espanol (Spanish)\", \"Deutsch (German)\".

The translator uses language codes (en, es, de...) for actual translation,
so display names do not affect functionality.
"""

LANG = [
    ("English", "en"),
    ("Espanol (Spanish)", "es"),
    ("Deutsch (German)", "de"),
    ("Francais (French)", "fr"),
    ("Italiano (Italian)", "it"),
    ("Portugues (Portuguese)", "pt"),
    ("Russian", "ru"),
    ("Chinese simp.", "zh-CN"),
]

LANG_NAMES = {code: name for name, code in LANG}
