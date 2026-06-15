"""Tests para el Modo Nativo (post-procesado por dialecto)."""

from native import NativeMode


# ── Inglés ─────────────────────────────────────────────────────────────────

def test_en_us_contractions():
    result = NativeMode.process("I am going to do what I want to do", "en-US")
    assert "gonna" in result.lower() or "wanna" in result.lower()


def test_en_gb_spelling():
    result = NativeMode.process("I like the color of your apartment", "en-GB")
    assert "colour" in result or "flat" in result.lower()


# ── Español ────────────────────────────────────────────────────────────────

def test_es_ve_colloquial():
    # NativeMode es post-procesado: el input ya debe estar en español
    result = NativeMode.process("Muchas gracias, estoy de acuerdo, no hay problema", "es-VE")
    assert any(x in result.lower() for x in ["gracias a ti", "dale", "da igual"])


def test_unknown_dialect_noop():
    """Dialecto desconocido no debe romper."""
    result = NativeMode.process("hello world", "xx-XX")
    assert result == "hello world"


def test_no_dialect():
    """Sin dialecto, no modifica el texto."""
    result = NativeMode.process("hello world", None)
    assert result == "hello world"
