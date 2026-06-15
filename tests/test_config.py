"""Tests para persistencia de configuración."""

import os
import json
import tempfile

from config_store import load, save, DEFAULT, CONFIG_DIR, CONFIG_FILE


def test_default_config():
    """load() devuelve defaults si no hay archivo."""
    cfg = load()
    assert cfg["engine"] == "google"
    assert cfg["api_key"] == ""
    assert cfg["source"] == "es"
    assert cfg["target"] == "en"


def test_save_and_load(monkeypatch, tmp_path):
    """Guardar y cargar preserva valores."""
    test_file = tmp_path / "config.json"
    monkeypatch.setattr("config_store.CONFIG_FILE", str(test_file))
    monkeypatch.setattr("config_store.CONFIG_DIR", str(tmp_path))

    save({
        "engine": "deepl",
        "api_key": "sk-test",
        "source": "en",
        "target": "de",
        "native_mode": True,
        "dialect": "en-US",
    })

    cfg = load()
    assert cfg["engine"] == "deepl"
    assert cfg["api_key"] == "sk-test"
    assert cfg["source"] == "en"
    assert cfg["target"] == "de"
    assert cfg["dialect"] == "en-US"


def test_save_merges_with_defaults(monkeypatch, tmp_path):
    """Valores faltantes se llenan con defaults."""
    test_file = tmp_path / "config.json"
    monkeypatch.setattr("config_store.CONFIG_FILE", str(test_file))
    monkeypatch.setattr("config_store.CONFIG_DIR", str(tmp_path))

    # Guardar solo engine
    with open(test_file, "w") as f:
        json.dump({"engine": "gpt"}, f)

    cfg = load()
    assert cfg["engine"] == "gpt"
    assert cfg["source"] == "es"  # default
    assert cfg["target"] == "en"  # default
