"""Procesador NativeMode — aplica reglas de naturalización post-traducción.

Cada regla es una tupla (patrón_regex, reemplazo, [match_texto_completo]).
Si match_texto_completo es True, la regla reemplaza solo la primera ocurrencia
(sin re.sub), útil para frases enteras como "I do not know" → "idk".
"""

import re
from typing import ClassVar


class NativeMode:
    """Procesador estático de reglas lingüísticas."""

    _rules: ClassVar[dict[str, list[tuple]]] = {}

    @classmethod
    def register(cls, lang_code: str, rules: list[tuple]) -> None:
        cls._rules[lang_code] = rules

    @classmethod
    def process(cls, text: str, lang: str) -> str:
        rules = cls._rules.get(lang)
        if not rules:
            return text
        return cls._apply(text, rules)

    @classmethod
    def _apply(cls, text: str, rules: list[tuple]) -> str:
        for rule in rules:
            if len(rule) >= 3 and rule[2] is True:
                pattern, replacement = rule[0], rule[1]
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    text = text[: m.start()] + replacement + text[m.end() :]
            else:
                pattern, replacement = rule[0], rule[1]
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
