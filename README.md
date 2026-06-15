# EngKey

**Platform: Linux** (X11/Wayland). Windows builds are available in Releases.

EngKey is a desktop translator that translates text in real time as you type. It appears as a floating overlay window. Uses Google Translate by default with support for DeepL, Microsoft Azure, LibreTranslate, and OpenAI GPT as alternative engines.

> This codebase is created with AI assistance.

## Features

- Real-time translation while typing with 300ms debounce
- Multiple pluggable translation engines: Google, DeepL, Microsoft Azure, LibreTranslate, OpenAI GPT
- Native Mode: post-processing per dialect (English contractions, British spelling, Venezuelan colloquialisms, etc.)
- LRU cache (250 entries) to avoid repeated API calls
- Persistent configuration at ~/.config/engkey/config.json
- Each engine is optional: install only the ones you use

## Installation

### Dependencies

Required: `deep-translator` (Google Translate engine, free, no API key).

Optional (install only if you use that engine):
- `deepl` for DeepL
- `requests` for Microsoft Azure or LibreTranslate
- `openai` for OpenAI GPT

### Running

```bash
git clone https://github.com/Vashuus/EngKey.git
cd EngKey

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 engkey.py
```

## Desktop environments

EngKey uses Tkinter, which is built on X11. It runs on both X11 and Wayland (via XWayland, included in most compositors). The always-on-top feature relies on X11 window manager protocols and may not work on all Wayland compositors. If you use Wayland and encounter window stacking issues, try a compositor with good XWayland support (GNOME, KDE, Sway).

## Translation engines

| Engine | Quality | API Key Required | Install |
|--------|---------|-----------------|---------|
| Google Translate (default) | High | No | pip install deep-translator |
| DeepL | Very high | Yes (free plan) | pip install deepl |
| Microsoft Azure | High | Yes (free plan) | pip install requests |
| LibreTranslate | Medium | No | pip install requests |
| OpenAI GPT | Very high | Yes | pip install openai |

To switch engines: open Settings (gear icon in the UI) -> select API -> enter API key if required.

## Native Mode

Native Mode applies linguistic rules to already-translated text to adapt it to a specific dialect. It is a post-processing step, not an alternative translation.

| Dialect | Example transformation |
|---------|----------------------|
| en-US | "I am going to" -> "I'm gonna" |
| en-GB | "color" -> "colour", "apartment" -> "flat" |
| es-VE | "de acuerdo" -> "dale", "muchas gracias" -> "gracias a ti" |

To enable: open Settings -> check Native Mode -> select a dialect. Only dialects available for the selected target language are shown.

## Configuration

Settings are saved to `~/.config/engkey/config.json`:

```json
{
  "engine": "google",
  "api_key": "",
  "source": "en",
  "target": "es",
  "native_mode": false,
  "dialect": null
}
```

## Tests

```bash
# Unit tests (no display required)
python3 -m pytest tests/ -v -m "not e2e" --ignore=tests/test_e2e.py

# E2E tests (requires Xvfb + xdotool)
Xvfb :99 -screen 0 1280x720x24 &
DISPLAY=:99 python3 -m pytest tests/test_e2e.py -v
```

## Project structure

```
EngKey/
  engkey.py             Entry point
  core/                 All Python source code
    engines.py          Translation engine registry (Strategy pattern)
    translator.py       Facade with LRU cache
    main_window.py      Tkinter UI with environment detection
    settings_window.py  Settings dialog
    env.py              Runtime environment detection (X11/Wayland/DE)
    native/             Native Mode dialect rules
    config_store.py     JSON config persistence
  tests/                Pytest test suite
  engkey.sh             Launch script
  engkey.desktop        Desktop shortcut
  icon.svg              App icon
```

### Key rule

All source code lives in `core/`. The root `engkey.py` imports from `core/` via sys.path. Platform-specific files (launch scripts, icons) are at the root level.

### Adding a new translation engine

Create a class in `core/engines.py` that inherits from `BaseEngine` and implements `translate(text, source, target) -> str`. Call `register(YourEngine)` at module level. The engine appears automatically in the Settings menu. See `COPILOT.md` for a complete example.

### Adding a new dialect

1. Create `core/native/<language>/<code>.py` with a `process(text) -> str` function
2. Register it in `core/native/dialects.py`

## Building portable binaries

Portable builds bundle Python + Tkinter + all dependencies into a single executable with PyInstaller.

### Linux

```bash
pip install pyinstaller
pyinstaller engkey.spec
# Output: dist/EngKey (ELF, ~16 MB)
```

### Windows (cross-compile from Linux)

```bash
# Install Python for Windows via wine
wget https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
wine python-3.12.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Install dependencies + pyinstaller
wine pip install deep-translator requests pyinstaller

# Build
wine pyinstaller --onefile --windowed --name EngKey ^
  --paths core ^
  --hidden-import deep_translator ^
  --hidden-import deepl ^
  --hidden-import requests ^
  --hidden-import openai ^
  --add-data "core/native;core/native" ^
  engkey.py
# Output: dist/EngKey.exe (~20 MB)
```

### Windows (native)

On a Windows machine with Python installed:

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name EngKey `
  --paths core `
  --hidden-import deep_translator `
  --hidden-import deepl `
  --hidden-import requests `
  --hidden-import openai `
  --add-data "core/native;core/native" `
  engkey.py
# Output: dist\EngKey.exe
```

### GitHub Actions (automatic)

Every time you publish a Release on GitHub, the workflow in `.github/workflows/release.yml` builds both Linux and Windows binaries and attaches them automatically.

## License

MIT - see LICENSE file.

## Contributing

Read CONTRIBUTING.md for details. Summary: fork, branch, changes, pytest, ruff, PR.
