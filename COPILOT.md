# EngKey - Architecture Reference

This file describes the project structure for developers and AI assistants working on EngKey.

## Architecture

```
EngKey/
  engkey.py             Entry point (imports from core/)
  COPILOT.md            This file - architecture reference

  core/                 All source code
    translator.py       Translation facade with LRU cache
    engines.py          Pluggable translation backends (Registry pattern)
    config_store.py     JSON persistence (~/.config/engkey/)
    config.py           Visual and behavioral constants
    main_window.py      UI: input, output, buttons, threads
    settings_window.py  Settings dialog
    debouncer.py        Typing debounce
    languages.py        Language list with ISO codes
    native.py           Native Mode core (post-processing)
    native/             Dialect rules per language

  tests/                Pytest test suite
  engkey.sh             Launch script
  engkey.desktop        Desktop shortcut
  icon.svg              App icon

  LICENSE               MIT
```

### Key rule

All source code lives in `core/`. The root `engkey.py` imports from `core/` via sys.path. Platform-specific files (engkey.sh, engkey.desktop, icon.svg) are at the root level.

## Translation Engine System

`core/engines.py` implements a Registry + Strategy pattern.

```python
from engines import build_engine, list_engines, ENGINE_REGISTRY

engine = build_engine("google")          # Google Translate (free, no key)
engine = build_engine("deepl", api_key)  # DeepL (requires key)
engine.translate("Hello", "en", "es")    # -> "Hola"
```

### Available engines

| ID | Class | Requires Key | Quality |
|----|-------|:-----------:|:-------:|
| google | GoogleEngine | No | High |
| deepl | DeepLEngine | Yes | Very high |
| microsoft | MicrosoftEngine | Yes | High |
| libre | LibreEngine | No | Medium |
| gpt | GPTEngine | Yes | Very high |

Each engine:
- Inherits from `BaseEngine`
- Implements `translate(text, source, target) -> str`
- Auto-registers with `@register`
- Handles `ImportError` if the library is not installed

### Adding a new engine

```python
from engines import BaseEngine, register

class MyEngine(BaseEngine):
    id = "myengine"
    name = "My Translator"
    needs_key = True
    key_label = "MyEngine API Key"

    def _setup(self):
        import myengine
        self._client = myengine.Client(self.api_key)
        self._available = True

    def translate(self, text, source, target):
        return self._client.translate(text, source, target)

register(MyEngine)
```

It appears automatically in the Settings menu. Zero UI changes needed.

## Native Mode

Post-processing system that adapts generic translation output to specific dialects.

```
Generic translation:  "I'm going to do what I want because I have to"
  en-US Native Mode:  "I'm gonna do what I wanna do cuz I've to"
  en-GB Native Mode:  "I like the colour of your flat in the centre"
```

Implemented as a rule pipeline:
1. Contractions (want to -> wanna, going to -> gonna)
2. Idioms (no problem -> no cap, thank you -> cheers)
3. Spelling (color -> colour, apartment -> flat)
4. Style (formal/informal, regional slang)

Each language has a file in `core/native/` with specific rules. The `dialects.py` registry maps ISO codes (en-US, es-VE) to their implementations.

## Data flow

```
User types text
       |
       v
  main_window._input
       | <KeyRelease>
       v
  debouncer           waits 300ms idle
       |
       v
  translator          facade with LRU cache (250 entries)
       |
       v
  engine (API)        Google / DeepL / GPT / etc.
       | result
       v
  NativeMode          post-processing if dialect active
       |
       v
  main_window._output updated via thread-safe queue
```

## Persistence

`core/config_store.py` saves configuration to `~/.config/engkey/config.json`:

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

Saved when settings are applied, loaded at startup.

## Project layout

```
engkey.py             Entry point (imports from core/)
engkey.sh             Launch script
engkey.desktop        Desktop shortcut
icon.svg              App icon
test_engkey.py        Legacy E2E tests
core/                 All Python source code
tests/                Pytest test suite
```

## Tests

`tests/` contains pytest tests. E2E tests use Xvfb for headless display.

```bash
python3 -m pytest tests/ -v -m "not e2e" --ignore=tests/test_e2e.py
```

## Design principles

| Principle | Implementation |
|-----------|---------------|
| Single source of truth | All code in core/, copied to platforms |
| Plugin architecture | Engines register automatically |
| Thread-safe UI | Background translation, queue.Queue for UI updates |
| Graceful degradation | API failures return original text |
| Offline-first config | Local JSON config, no server required |
| Minimal dependencies | Only deep-translator required; everything else is optional |
