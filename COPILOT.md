# EngKey — Traductor Flotante Multisistema

Aplicación de escritorio que traduce texto en **tiempo real** mientras escribes en cualquier app. Overlay flotante con hotkey global y soporte multi-API. Compatible con **Linux, Windows y macOS** desde un mismo código base.

---

##  Arquitectura

```
EngKey/
├── COPILOT.md            ← este archivo
├── engkey.py             ← entry point raíz (delega a core/)
├── sync.sh               ← copia core/ → Linux/ Windows/ macOS/
│
├── core/                 ← ★ FUENTE ÚNICA de todo el código
│   ├── engkey.py         ← entry point de desarrollo
│   ├── translator.py     ← facade de traducción con caché LRU
│   ├── engines.py        ← ★ backends de traducción intercambiables
│   ├── config_store.py   ← persistencia JSON (~/.config/engkey/)
│   ├── config.py         ← constantes visuales y de comportamiento
│   ├── main_window.py    ← UI: input, output, botones, hilos
│   ├── settings_window.py← diálogo de configuración
│   ├── debouncer.py      ← debounce para escribir
│   ├── languages.py      ← lista de idiomas con códigos ISO
│   ├── native.py         ← core del Modo Nativo (post-procesado)
│   ├── native/           ← reglas de dialecto por idioma
│   │   ├── dialects.py   ← registro de dialectos
│   │   ├── en.py         ← inglés (US, GB, slang, etc.)
│   │   └── es.py         ← español (VE, MX, AR, ES, etc.)
│   └── test_engkey.py    ← pruebas automatizadas con Tkinter real
│
├── Linux/   Windows/   macOS/   ← copias independientes (cada una tiene
│   └── ...                        su propio entry point, script .sh/.bat,
│                                  icono .desktop, etc.)
│
└── core/LICENSE          ← GPLv3
```

### Regla fundamental

> **Todo el código vive en `core/`.** Las carpetas `Linux/`, `Windows/`, `macOS/` son copias exactas más sus propios scripts de lanzamiento, iconos y configuraciones de plataforma. `sync.sh` copia `core/` → todas las plataformas.

---

##  Sistema de Motores de Traducción

El archivo `core/engines.py` implementa un **patrón Registry + Strategy**.

```python
from engines import build_engine, list_engines, ENGINE_REGISTRY

engine = build_engine("google")          # Google Translate (gratis, sin key)
engine = build_engine("deepl", api_key)  # DeepL (requiere key)
engine.translate("Hola", "es", "en")     # → "Hello"
```

### Motores disponibles

| ID | Clase | Requiere Key | Calidad | Status |
|----|-------|:-----------:|:-------:|:------:|
| `google` | `GoogleEngine` | ❌ | ⭐⭐⭐⭐ | ✅ Default |
| `deepl` | `DeepLEngine` | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| `microsoft` | `MicrosoftEngine` | ✅ | ⭐⭐⭐⭐ | ✅ |
| `libre` | `LibreEngine` | ❌ | ⭐⭐⭐ | ✅ |
| `gpt` | `OpenAI GPT` | ✅ | ⭐⭐⭐⭐⭐ | ✅ |

**Cada motor:**
- Hereda de `BaseEngine`
- Implementa `translate(text, source, target) → str`
- Se auto-registra con `@register`
- Maneja `ImportError` si la librería no está instalada

### Agregar un motor nuevo

```python
from engines import BaseEngine, register

class MiMotor(BaseEngine):
    id = "mimoto"
    name = "Mi Traductor"
    needs_key = True
    key_label = "API Key de MiMotor"

    def _setup(self):
        import mimoto
        self._client = mimoto.Client(self.api_key)
        self._available = True

    def translate(self, text, source, target):
        return self._client.translate(text, source, target)

register(MiMotor)
```

Aparece automáticamente en el menú de Configuración. **Sin Toque de manos.**

---

##  Modo Nativo

Sistema de post-procesado que adapta la traducción genérica a dialectos específicos.

```
Traducción genérica:    "I'm going to do what I want because I have to"
  ↓ Modo Nativo en-US   "I'm gonna do what I wanna do cuz I've to"
  ↓ Modo Nativo en-GB   "I like the colour of your flat in the centre"
```

Implementado como un pipeline de reglas:
1. **Contracciones** (`want to` → `wanna`, `going to` → `gonna`)
2. **Modismos** (`no problem` → `no cap`, `thank you` → `cheers`)
3. **Ortografía** (`color` → `colour`, `apartment` → `flat`)
4. **Estilo** (formal ↔ informal, argot regional)

Cada idioma tiene su archivo en `core/native/` con reglas específicas. El registro `dialects.py` mapea códigos ISO (`en-US`, `es-VE`) a sus implementaciones.

---

##  Flujo de datos

```
Usuario escribe texto
        │
        ▼
┌────────────────┐
│  main_window   │
│  ._input       │
└────┬───────────┘
     │ <KeyRelease>
     ▼
┌────────────────┐
│  debouncer     │  ← espera 300ms sin escribir
└────┬───────────┘
     │
     ▼
┌────────────────┐
│  translator    │  ← facade con caché LRU (250 entradas)
│  .translate()  │
└────┬───────────┘
     │
     ▼
┌────────────────┐
│  engine (API)  │  ← Google / DeepL / GPT / etc.
│  .translate()  │
└────┬───────────┘
     │ resultado
     ▼
┌────────────────┐
│  NativeMode    │  ← post-procesado si hay dialecto activo
│  .process()    │
└────┬───────────┘
     │
     ▼
┌────────────────┐
│  main_window   │
│  ._output      │  ← actualizado vía cola thread-safe
└────────────────┘
```

---

##  Persistencia

`core/config_store.py` guarda configuración en `~/.config/engkey/config.json`:

```json
{
  "engine": "google",
  "api_key": "",
  "source": "es",
  "target": "en",
  "native_mode": false,
  "dialect": null
}
```

Se guarda al aplicar cambios en Settings y se carga al iniciar.

---

##  Estructura de una plataforma (ej. Linux)

```
Linux/
├── engkey.py          ← entry point (mismo que core/engkey.py)
├── engkey.sh          ← script bash para lanzar
├── engkey.desktop     ← acceso directo .desktop
├── icon.svg           ← ícono de la app
├── test_engkey.py     ← tests
├── native/            ← reglas de dialecto
│   ├── __init__.py
│   ├── dialects.py
│   ├── en.py
│   └── es.py
└── *.py               ← copia exacta de core/
```

Windows tiene `engkey.bat` y `engkey.ps1`. macOS tiene `EngKey.app/`.

---

##  Pruebas

`test_engkey.py` lanza la app real con Tkinter, escribe texto, verifica salida, prueba APIs, botones, cierre con Escape. Corre en CI sin pantalla (usando `Xvfb` en Linux).

```bash
python3 Linux/test_engkey.py
# → 7/7 tests pasan
```

---

## Principios de diseño

| Principio | Cómo se aplica |
|-----------|---------------|
| **Single source of truth** | Todo el código en `core/`, se copia a plataformas |
| **Plugin architecture** | Motores de traducción se registran automáticamente |
| **Thread-safe UI** | Traducción en background thread, cola `queue.Queue` para UI |
| **Graceful degradation** | Si falla la API, devuelve el texto original |
| **Offline-first config** | Config local JSON, sin servidor |
| **Sin dependencias pesadas** | Solo `deep-translator` (default), el resto es opcional |
