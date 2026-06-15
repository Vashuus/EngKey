"""NativeMode — prosesador de regles de naturalització post-traducció.

Cada regla transforma patrons regex en text natural per al dialecte.
Les regles s'ordenen automàticament per prioritat:
  - Més paraules al patró = més específica = s'aplica primer
  - A igualtat, ordre de definició

Estat: EXPERIMENTAL — algunes frases poden contenir errors.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import IntEnum
from functools import lru_cache
from typing import Callable


class RulePriority(IntEnum):
    """Ordre d'execució (valor més alt = s'executa primer)."""

    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    LOWEST = 0


@lru_cache(maxsize=256)
def _compile(pattern: str) -> re.Pattern:
    """Patró regex amb cache (evita recompilar en cada traducció)."""
    return re.compile(pattern, re.IGNORECASE | re.UNICODE)


def _count_words(pattern: str) -> int:
    """Nombre de paraules que casa el patró (per a prioritat automàtica)."""
    return len(re.findall(r"\b\w+\b", pattern))


@dataclass
class Rule:
    """Regla de naturalització amb prioritat i context opcional.

    Compatibilitat enrere: es pot crear des d'una tupla de 2 o 3 elements:
        (patró, reemplaç)                    → Rule(patró, reemplaç)
        (patró, reemplaç, full_match)        → Rule(patró, reemplaç,  match_full=full_match)
    """

    pattern: str
    replacement: str | Callable[[re.Match], str]
    match_full: bool = False
    priority: RulePriority | None = None
    description: str = ""

    # Nombre de paraules al patró (per a prioritat automàtica si no es fixa)
    _word_count: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._word_count = _count_words(self.pattern)

    @classmethod
    def from_tuple(cls, t: tuple) -> "Rule":
        """Converteix una tupla (patró, reemplaç, [full_match]) a Rule."""
        if len(t) >= 3 and t[2] is True:
            return cls(pattern=t[0], replacement=t[1], match_full=True)
        return cls(pattern=t[0], replacement=t[1])

    def apply(self, text: str) -> str:
        """Aplica la regla al text i retorna el resultat."""
        compiled = _compile(self.pattern)

        if self.match_full:
            m = compiled.search(text)
            if m:
                text = text[: m.start()] + str(self.replacement) + text[m.end() :]
            return text

        if callable(self.replacement):
            return compiled.sub(self.replacement, text)
        return compiled.sub(str(self.replacement), text)


class NativeMode:
    """Procesador estàtic de regles lingüístiques.

    L'ordre d'aplicació és:
      1. Normalització prèvia (expandir compostos: \"deacuerdo\" → \"de acuerdo\")
      2. Regles multi-paraula (més específiques primer)
      3. Regles d'una paraula
    """

    _rules: dict[str, list[Rule]] = {}

    # ── Registre ─────────────────────────────────────────────────────

    @classmethod
    def register(cls, lang_code: str, rules: list) -> None:
        """Registra regles per a un dialecte, ordenades per prioritat.

        Accepta tant objects ``Rule`` com tuples de 2/3 elements (compatibilitat enrere).
        """
        parsed: list[Rule] = []
        for r in rules:
            if isinstance(r, Rule):
                parsed.append(r)
            elif isinstance(r, tuple):
                parsed.append(Rule.from_tuple(r))
            else:
                raise TypeError(f"Expected Rule or tuple, got {type(r).__name__}")

        # Assignar prioritat automàtica si no en té
        for r in parsed:
            if r.priority is None:
                # Més paraules = més específic = prioritat més alta
                if r._word_count >= 3:
                    r.priority = RulePriority.CRITICAL
                elif r._word_count == 2:
                    r.priority = RulePriority.HIGH
                else:
                    r.priority = RulePriority.MEDIUM

        # Ordenar: prioritat descendent, després paraules descendents, després patró asc
        parsed.sort(key=lambda x: (-x.priority.value, -x._word_count, x.pattern))
        cls._rules[lang_code] = parsed

    # ── Processament ─────────────────────────────────────────────────

    @classmethod
    def process(cls, text: str, lang: str) -> str:
        """Aplica totes les regles del dialecte, amb normalització prèvia."""
        if not text:
            return text

        result = text

        # 1. Normalització prèvia (expandir compostos, etc.)
        from .normalize import pre_normalize

        result = pre_normalize(result)

        # 2. Aplicar regles del dialecte
        rules = cls._rules.get(lang)
        if rules:
            for rule in rules:
                result = rule.apply(result)

        return result

    # ── Utilitats ────────────────────────────────────────────────────

    @classmethod
    def list_rules(cls, lang: str) -> list[dict]:
        """Retorna metadades de les regles per a debugging/UI."""
        rules = cls._rules.get(lang, [])
        return [
            {
                "pattern": r.pattern,
                "replacement": (
                    r.replacement
                    if isinstance(r.replacement, str)
                    else "<function>"
                ),
                "priority": r.priority.name if r.priority else "N/A",
                "words": r._word_count,
                "match_full": r.match_full,
                "description": r.description,
            }
            for r in rules
        ]

    @classmethod
    def clear(cls, lang_code: str | None = None) -> None:
        """Neteja regles (per a tests)."""
        if lang_code:
            cls._rules.pop(lang_code, None)
        else:
            cls._rules.clear()
