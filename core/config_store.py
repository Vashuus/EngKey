"""Persistencia simple de configuración en JSON.

Guarda en ~/.config/engkey/config.json:
  engine, api_key, source, target, dialect, native_mode
"""

import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/engkey")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT = {
    "engine": "google",
    "api_key": "",
    "source": "es",
    "target": "en",
    "native_mode": False,
    "dialect": None,
}


def load() -> dict:
    try:
        with open(CONFIG_FILE) as f:
            return {**DEFAULT, **json.load(f)}
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULT)


def save(cfg: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
