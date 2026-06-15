"""Configuration persistence tests."""

import os
import json
import tempfile

from config_store import load, save, DEFAULT, CONFIG_DIR, CONFIG_FILE


def test_default_config():
    """Returns defaults when no config file exists."""
    cfg = load()
    assert cfg["engine"] == "google"
    assert cfg["api_key"] == ""
    assert cfg["source"] == "en"
    assert cfg["target"] == "es"


def test_save_and_load(monkeypatch, tmp_path):
    """Save and load preserves values."""
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
    """Missing values are filled with defaults."""
    test_file = tmp_path / "config.json"
    monkeypatch.setattr("config_store.CONFIG_FILE", str(test_file))
    monkeypatch.setattr("config_store.CONFIG_DIR", str(tmp_path))

    with open(test_file, "w") as f:
        json.dump({"engine": "gpt"}, f)

    cfg = load()
    assert cfg["engine"] == "gpt"
    assert cfg["source"] == "en"
    assert cfg["target"] == "es"
