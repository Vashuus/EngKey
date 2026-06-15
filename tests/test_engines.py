"""Tests para el registro de motores de traducción."""

import pytest
from engines import (
    ENGINE_REGISTRY,
    list_engines,
    build_engine,
    GoogleEngine,
    DeepLEngine,
    MicrosoftEngine,
    LibreEngine,
    GPTEngine,
)


def test_registry_contains_all_engines():
    ids = [e.id for e in ENGINE_REGISTRY.values()]
    assert "google" in ids
    assert "deepl" in ids
    assert "microsoft" in ids
    assert "libre" in ids
    assert "gpt" in ids


def test_list_engines_returns_tuples():
    engines = list_engines()
    assert len(engines) == 5
    for eid, name in engines:
        assert isinstance(eid, str)
        assert isinstance(name, str)
        assert len(eid) > 0
        assert len(name) > 0


def test_build_google():
    engine = build_engine("google")
    assert isinstance(engine, GoogleEngine)
    assert not engine.needs_key


def test_build_deepl():
    engine = build_engine("deepl", api_key="test-key")
    assert isinstance(engine, DeepLEngine)
    assert engine.needs_key
    assert engine.api_key == "test-key"


def test_build_microsoft():
    engine = build_engine("microsoft", api_key="test-key")
    assert isinstance(engine, MicrosoftEngine)
    assert engine.needs_key


def test_build_libre():
    engine = build_engine("libre")
    assert isinstance(engine, LibreEngine)
    assert not engine.needs_key


def test_build_gpt():
    engine = build_engine("gpt", api_key="test-key")
    assert isinstance(engine, GPTEngine)
    assert engine.needs_key


def test_build_unknown_engine():
    with pytest.raises(ValueError, match="Motor desconocido"):
        build_engine("nonexistent")


def test_google_engine_name():
    engine = build_engine("google")
    assert engine.name == "Google Translate"
