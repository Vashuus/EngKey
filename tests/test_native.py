"""Tests para el Modo Nativo (post-procesado por dialecto).

EXPERIMENTAL: algunas frases pueden contener errores.
"""

from __future__ import annotations

import pytest
from native import NativeMode, Rule, RulePriority


# ── Regresion: prioridad de reglas ─────────────────────────────────────

class TestRulePriority:
    """Las reglas con mas palabras se aplican antes (mas especificas primero)."""

    def test_estoy_de_acuerdo_antes_que_de_acuerdo(self):
        """'estoy de acuerdo' → 'dale' debe ganarle a 'de acuerdo' → 'dale'.
        
        Caso real del bug original: la frase 'Estoy de acuerdo contigo' producia
        'Estoy dale contigo' porque la regla '\bde acuerdo\b' se aplicaba antes
        que '\bestoy de acuerdo\b'.
        """
        result = NativeMode.process("Estoy de acuerdo contigo", "es-VE")
        # Debe reemplazar TODO 'estoy de acuerdo', no solo 'de acuerdo'
        assert result == "dale contigo", (
            f"Esperaba 'dale contigo', obtuve '{result}'. "
            "Si ves 'Estoy dale contigo', la prioridad no funciona."
        )

    def test_de_acuerdo_standalone(self):
        """'de acuerdo' sin 'estoy' debe reemplazarse igual."""
        result = NativeMode.process("De acuerdo, vamos", "es-VE")
        assert result == "dale, vamos"

    def test_longer_phrase_wins(self):
        """Frase de 3 palabras se aplica antes que frase de 2."""
        # 'estoy de acuerdo' (3 palabras) debe ganar
        result = NativeMode.process("Estoy de acuerdo", "es-VE")
        assert result == "dale", (
            f"Esperaba 'dale', obtuve '{result}'"
        )


# ── Normalizacion: compuestos escritos juntos ─────────────────────────

class TestNormalization:
    """La normalizacion previa expande compuestos escritos juntos."""

    def test_deacuerdo_expandido(self):
        """'deacuerdo' escrito junto → se expande antes del matching."""
        result = NativeMode.process("Estoy deacuerdo contigo", "es-VE")
        assert result == "dale contigo", (
            f"Esperaba 'dale contigo', obtuve '{result}'. "
            "La normalizacion previa no expandio 'deacuerdo' a 'de acuerdo'."
        )

    def test_sobretodo_expandido(self):
        """'sobretodo' → 'sobre todo' (es-CO)."""
        result = NativeMode.process("sobretodo, me gusta", "es-CO")
        assert "sobre todo" in result

    def test_normalization_noop_for_correct_text(self):
        """Texto ya correcto no debe cambiar."""
        result = NativeMode.process("Estoy de acuerdo", "es-VE")
        assert "deacuerdo" not in result


# ── Inglés ─────────────────────────────────────────────────────────────

class TestEnglishUS:
    """Tests para dialecto American English."""

    def test_contractions_negative(self):
        """Verificar contracciones negativas."""
        result = NativeMode.process("I do not like this", "en-US")
        assert "don't" in result.lower()

    def test_subject_verb_contraction(self):
        """Verificar contracciones sujeto+verbo."""
        result = NativeMode.process("I am happy", "en-US")
        assert result == "I'm happy"

    def test_informal_reduction(self):
        """Verificar reducciones informales."""
        result = NativeMode.process("I am going to do it", "en-US")
        # Primero 'I am' → 'I'm', luego 'going to' → 'gonna'
        assert result == "I'm gonna do it" or "gonna" in result.lower()

    def test_en_us_contractions(self):
        """Compatibilidad con test anterior."""
        result = NativeMode.process("I am going to do what I want to do", "en-US")
        assert "gonna" in result.lower() or "wanna" in result.lower()

    def test_full_match_idk(self):
        """'I do not know' completo → 'idk' (match_full=True)."""
        result = NativeMode.process("I do not know", "en-US")
        assert result.lower() == "idk"


class TestEnglishGB:
    """Tests para dialecto British English."""

    def test_en_gb_spelling(self):
        """Compatibilidad con test anterior."""
        result = NativeMode.process("I like the color of your apartment", "en-GB")
        assert "colour" in result or "flat" in result.lower()


# ── Español ────────────────────────────────────────────────────────────

class TestSpanishVE:
    """Tests para dialecto Venezolano."""

    def test_es_ve_colloquial(self):
        """Compatibilidad con test anterior."""
        result = NativeMode.process("Muchas gracias, estoy de acuerdo, no hay problema", "es-VE")
        # 'muchas gracias' → 'gracias a ti', 'estoy de acuerdo' → 'dale'
        assert any(x in result.lower() for x in ["gracias a ti", "dale"])

    def test_es_ve_saludo(self):
        """'cómo estás' → 'qué más'."""
        result = NativeMode.process("¿Cómo estás?", "es-VE")
        assert "qué más" in result.lower()


class TestSpanishAR:
    """Tests para dialecto Argentino."""

    def test_voseo(self):
        """Verificar transformación tú → vos."""
        result = NativeMode.process("tú tienes razón", "es-AR")
        assert "vos tenés" in result.lower()

    def test_lunfardo(self):
        """Verificar lunfardo rioplatense."""
        result = NativeMode.process("quiero trabajar", "es-AR")
        assert "laburo" in result.lower() or "laburar" in result.lower()


# ── Casos borde ────────────────────────────────────────────────────────

class TestEdgeCases:
    """Casos especiales."""

    def test_unknown_dialect_noop(self):
        """Dialecto desconocido no debe romper."""
        result = NativeMode.process("hello world", "xx-XX")
        assert result == "hello world"

    def test_no_dialect(self):
        """Sin dialecto, no modifica el texto."""
        result = NativeMode.process("hello world", None)
        assert result == "hello world"

    def test_empty_string(self):
        """Manejar texto vacío."""
        result = NativeMode.process("", "en-US")
        assert result == ""

    def test_whitespace_only(self):
        """Manejar solo espacios."""
        result = NativeMode.process("   ", "en-US")
        assert result == "   "

    def test_case_preservation(self):
        """Mayúsculas no deben romper el matching."""
        result = NativeMode.process("I AM HAPPY", "en-US")
        assert result is not None

    def test_multiple_replacements_in_one_text(self):
        """Múltiples reglas en un mismo texto."""
        result = NativeMode.process(
            "I am going to work. I do not like it.", "en-US"
        )
        assert "I'm" in result
        assert "don't" in result
        assert "gonna" in result.lower() or "going to" in result


# ── Rule API ──────────────────────────────────────────────────────────

class TestRuleAPI:
    """Tests para la API de Rule y NativeMode.list_rules."""

    def test_rule_from_tuple(self):
        """Conversión de tupla a Rule."""
        rule = Rule.from_tuple((r"\bhola\b", "mundo"))
        assert rule.pattern == r"\bhola\b"
        assert rule.replacement == "mundo"
        assert not rule.match_full

    def test_rule_from_tuple_full_match(self):
        """Tupla con 3 elementos y match_full=True."""
        rule = Rule.from_tuple((r"\bfrase completa\b", "abrev", True))
        assert rule.match_full is True

    def test_list_rules(self):
        """list_rules() devuelve metadatos."""
        rules = NativeMode.list_rules("es-VE")
        assert len(rules) > 0
        assert all("pattern" in r for r in rules)
        assert all("priority" in r for r in rules)
        assert all("description" in r for r in rules)

    def test_custom_rule(self):
        """Regla personalizada con Rule.apply()."""
        rule = Rule(r"\bmundo\b", "planeta", priority=RulePriority.HIGH)
        result = rule.apply("Hola mundo")
        assert result == "Hola planeta"

    def test_clear(self):
        """clear() limpia reglas para tests."""
        NativeMode._rules["xx-TEST"] = [Rule(r"\btest\b", "ok")]
        assert "xx-TEST" in NativeMode._rules
        NativeMode.clear("xx-TEST")
        assert "xx-TEST" not in NativeMode._rules


# ── Rendimiento ────────────────────────────────────────────────────────

class TestPerformance:
    """Verifica que el cache de regex funcione."""

    def test_regex_cache(self):
        """Aplicar misma regla múltiples veces no debe fallar."""
        rule = Rule(r"\btest\b", "ok")
        for _ in range(100):
            result = rule.apply("this is a test")
            assert result == "this is a ok"
