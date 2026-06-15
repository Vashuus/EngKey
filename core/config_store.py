"""Simple JSON configuration persistence.

Stores in ~/.config/engkey/config.json:
  engine, api_key, source, target, dialect, native_mode
"""

import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/engkey")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT = {
    "engine": "google",
    "api_key": "",
    "source": "en",
    "target": "es",
    "native_mode": False,
    "dialect": None,
    # Appearance
    "font_family": "Segoe UI",
    "font_size": 11,
    "bg_image": None,  # path to image file, or None
    "custom_colors": {},  # override specific colors: {"BG": "#...", "ACCENT": "#...", ...}
    "overlay_opacity": 0.25,  # 0.0-1.0, image overlay transparency on top of widgets
    "button_border_style": "default",  # "default" (flat) or "soft" (groove+bd1)
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
