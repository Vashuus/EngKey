# EngKey - Architecture Reference

This file describes the project structure for developers and AI assistants working on EngKey.

## Project Structure

```
EngKey/
├── engkey.py              Entry point (imports from core/)
├── engkey.sh              Launch script (Linux)
├── engkey.desktop         Desktop shortcut
├── icon.svg               App icon
├── LICENSE                MIT license
├── ARCHITECTURE.md        This file - architecture reference
├── core/                  All Python source code
│   ├── translator.py      Translation facade with LRU cache
│   ├── engines.py         Pluggable translation backends (Registry pattern)
│   ├── config_store.py    JSON persistence (~/.config/engkey/)
│   ├── config.py          Visual and behavioral constants
│   ├── main_window.py     UI: input, output, buttons, threads
│   ├── settings_window.py Settings dialog
│   ├── env.py             Runtime environment detection
│   ├── debouncer.py       Typing debounce (300ms idle)
│   ├── languages.py       Language list with ISO codes
│   └── native/            Native Mode dialect rules (package)
├── tests/                 Pytest test suite
└── test_engkey.py         Legacy E2E tests (deprecated, use tests/)
```

### Key Rule

All source code lives in `core/`. The root `engkey.py` imports from `core/` via sys.path manipulation. Platform-specific files (engkey.sh, engkey.desktop, icon.svg) stay at the root level.

---

## Translation Engine System

`core/engines.py` implements a **Registry + Strategy pattern** for pluggable translation backends.

### Basic Usage

```python
from core.engines import build_engine, list_engines, ENGINE_REGISTRY

# List available engines
engines = list_engines()  # -> ["google", "deepl", "microsoft", "libre", "gpt"]

# Create engine instance
engine = build_engine("google")           # Google Translate (free, no key required)
engine = build_engine("deepl", api_key)   # DeepL (requires API key)

# Translate
result = engine.translate("Hello", source="en", target="es")  # -> "Hola"
```

### Available Engines

| ID | Class | Requires Key | Quality | Notes |
|----|-------|:-----------:|:-------:|-------|
| google | GoogleEngine | No | High | Free, rate-limited |
| deepl | DeepLEngine | Yes | Very High | Excellent quality, paid |
| microsoft | MicrosoftEngine | Yes | High | Requires Azure credentials |
| libre | LibreEngine | No | Medium | Local option (slower) |
| gpt | GPTEngine | Yes | Very High | Requires OpenAI API key |

### Engine Contract

Each engine must:
- Inherit from `BaseEngine`
- Implement `translate(text: str, source: str, target: str) -> str`
- Define class attributes: `id`, `name`, `needs_key`, `key_label`
- Implement `_setup()` to initialize the client
- Auto-register using `@register` decorator
- Handle `ImportError` gracefully if library is not installed

### Adding a New Engine

```python
from core.engines import BaseEngine, register

class MyEngine(BaseEngine):
    id = "myengine"
    name = "My Translator"
    needs_key = True
    key_label = "MyEngine API Key"

    def _setup(self):
        """Initialize the translation client."""
        import myengine  # Will raise ImportError if not installed
        self._client = myengine.Client(self.api_key)
        self._available = True

    def translate(self, text: str, source: str, target: str) -> str:
        """Translate text from source language to target language."""
        return self._client.translate(text, source, target)

register(MyEngine)  # Auto-registers in ENGINE_REGISTRY
```

The engine appears automatically in the Settings menu. **Zero UI changes required.**

### Error Handling

- If an engine's library is not installed → marked as unavailable
- If an API call fails → original text is returned (graceful degradation)
- Missing API key → engine is disabled in UI

---

## Native Mode

Post-processing system that adapts generic translation output to specific regional dialects and speech patterns.

### Example

```
Generic translation (en-US):  "I'm going to do what I want because I have to"
Native Mode (en-US):          "I'm gonna do what I wanna do cuz I gotta"
Native Mode (en-GB):          "I'm going to do what I want as I've got to"
Native Mode (es-MX):          "Voy a hacer lo que me venga en gana porque tengo que"
```

### Architecture

Implemented as a rule pipeline in `core/native/`:
1. **Contractions** — want to → wanna, going to → gonna, have to → gotta
2. **Idioms** — regional expressions (no problem → no cap, thanks → cheers)
3. **Spelling** — regional variants (color → colour, apartment → flat)
4. **Style** — formal vs. informal tone, regional slang

Each language/dialect has a rules file (e.g., `en_us.py`, `en_gb.py`). The registry in `dialects.py` maps ISO 639-1 codes with region (en-US, es-VE) to their implementations.

---

## Data Flow

```
┌─────────────────────────────────────────────────┐
│ User types text in main_window._input           │
└────────────────┬────────────────────────────────┘
                 │
                 │ <KeyRelease> event
                 v
┌─────────────────────────────────────────────────┐
│ debouncer                                       │
│ Waits 300ms idle before processing              │
└────────────────┬────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────┐
│ translator (core/translator.py)                 │
│ LRU cache (250 entries)                         │
│ Returns cached result if available              │
└────────────────┬────────────────────────────────┘
                 │
                 │ Cache miss → API call
                 v
┌─────────────────────────────────────────────────┐
│ engine.translate()                              │
│ Google / DeepL / GPT / etc. (async in thread)   │
└────────────────┬────────────────────────────────┘
                 │
                 │ Translation result
                 v
┌─────────────────────────────────────────────────┐
│ NativeMode (if dialect active)                  │
│ Post-processing rules pipeline                  │
└────────────────┬────────────────────────────────┘
                 │
                 │ Final result
                 v
┌─────────────────────────────────────────────────┐
│ queue.Queue → main_window._output               │
│ Thread-safe update (GUI thread)                 │
└─────────────────────────────────────────────────┘
```

### Thread Safety

- Translation happens in a background thread
- Results are posted to `queue.Queue` (thread-safe)
- Main GUI thread polls the queue and updates `_output` widget
- No race conditions or deadlocks

---

## Configuration & Persistence

### Config File Location

`~/.config/engkey/config.json`

### Config Structure

```json
{
  "engine": "google",
  "api_key": "",
  "source": "en",
  "target": "es",
  "native_mode": false,
  "dialect": null,
  "window_x": 100,
  "window_y": 100
}
```

### Behavior

- **Load**: At application startup via `core/config_store.py`
- **Save**: When user clicks "Apply" in settings dialog
- **Fallback**: If file is missing or corrupted, sensible defaults are used

---

## Testing

Tests are in `tests/` (Pytest suite).

### Running Tests

```bash
# All tests except E2E
python3 -m pytest tests/ -v --ignore=tests/test_e2e.py

# Only E2E tests (requires Xvfb display)
python3 -m pytest tests/test_e2e.py -v

# Specific test file
python3 -m pytest tests/test_translator.py -v

# With coverage
python3 -m pytest tests/ --cov=core --cov-report=html
```

### Testing a New Engine

1. Create `tests/test_myengine.py`
2. Mock the API client (don't call real APIs in tests)
3. Test `_setup()`, `translate()`, and error handling
4. Example:
   ```python
   import pytest
   from core.engines import build_engine
   
   def test_myengine_translate():
       engine = build_engine("myengine", api_key="test_key")
       result = engine.translate("Hello", "en", "es")
       assert result == "Hola"
   
   def test_myengine_missing_key():
       engine = build_engine("myengine")  # No key
       assert not engine.is_available()
   ```

---

## Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Single source of truth** | All code in `core/`; no duplication |
| **Plugin architecture** | Engines auto-register; no hardcoded lists |
| **Thread safety** | Background translation + `queue.Queue` for UI updates |
| **Graceful degradation** | API failures return original text; missing libs are skipped |
| **Offline-first config** | Local JSON, no server required |
| **Minimal dependencies** | Only `deep-translator` required; everything else optional |
| **Clean separation** | UI, translation logic, and config are decoupled |
| **Extensibility** | Add engines and dialects without modifying core files |

---

## Environment & Dependencies

### Runtime Environment Detection

`core/env.py` detects:
- OS (Linux, macOS, Windows)
- Desktop environment (GNOME, KDE, etc.)
- Available display server (X11, Wayland)
- Installed optional libraries (for engine availability)

### Minimal Dependencies

- `tkinter` (usually pre-installed)
- `deep-translator` (required for fallback translation)

### Optional Dependencies

- `google-translate-unofficial-api` (for Google engine)
- `deepl` (for DeepL engine)
- `azure-ai-translation` (for Microsoft engine)
- `libre-translate` (for LibreTranslate engine)
- `openai` (for GPT engine)

Engines gracefully degrade if their library is missing.

---

## Development Workflow

1. Clone and install: `git clone https://github.com/Vashuus/EngKey && cd EngKey && pip install -e .`
2. Run locally: `python3 engkey.py`
3. Run tests: `python3 -m pytest tests/ -v`
4. Add a feature:
   - Create files in `core/`
   - Write tests in `tests/`
   - Update this document if architecture changes
5. Submit PR with tests + ARCHITECTURE.md updates

---

## Troubleshooting

### API key not working
- Check `~/.config/engkey/config.json`
- Verify key in engine's web console (DeepL, OpenAI, etc.)
- Check rate limits and billing

### Engine not appearing in menu
- Verify `@register` decorator is present
- Check `ENGINE_REGISTRY.list()` in Python REPL
- Ensure library is installed (`pip list`)

### Translation slow
- Check debouncer timeout (default 300ms)
- Verify LRU cache is working (`translator.cache_info()`)
- Consider switching to faster engine (e.g., Google → DeepL)
