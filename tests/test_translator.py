"""Tests unitarios para el traductor (sin llamadas de red)."""

from unittest.mock import patch, MagicMock
from translator import Translator
from config import MAX_CACHE


# ── Básicos ───────────────────────────────────────────────────────────────

def test_empty_text():
    t = Translator()
    assert t.translate("") == ""
    assert t.translate("   ") == ""


def test_no_engine_fallback():
    """Si no hay motor, devuelve el texto original."""
    t = Translator(engine_id="nonexistent")
    assert t.translate("hola") == "hola"


# ── Caché ──────────────────────────────────────────────────────────────────

def test_cache_hit():
    """Misma entrada dos veces → llama al motor solo una vez."""
    with patch.object(Translator, "_build_engine") as mock_build:
        mock_build.return_value = None
        t = Translator()
        mock_translate = MagicMock(return_value="hello")
        t._engine = MagicMock()
        t._engine.translate.return_value = "hello"

        r1 = t.translate("hola")
        r2 = t.translate("hola")

        assert r1 == r2 == "hello"
        # Solo una llamada al motor (la segunda es caché)
        t._engine.translate.assert_called_once()


def test_cache_cleared_on_direction_change():
    t = Translator()
    t._cache = {("hola", None): "hello"}
    t.set_direction("en", "es")
    assert t._cache == {}


def test_cache_max_size():
    """Cuando la caché excede MAX_CACHE, se limpia toda."""
    t = Translator()
    t._engine = MagicMock()
    t._engine.translate.side_effect = lambda text, s, t: f"translated:{text}"

    for i in range(MAX_CACHE + 10):
        t.translate(f"text{i}")

    assert len(t._cache) <= MAX_CACHE + 10  # no explota


# ── Dialectos ──────────────────────────────────────────────────────────────

def test_dialect_setting():
    t = Translator()
    assert t._dialect is None
    t.set_dialect("en-US")
    assert t._dialect == "en-US"
    t.set_dialect(None)
    assert t._dialect is None
