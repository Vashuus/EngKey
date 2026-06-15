# EngKey — Traductor Flotante en Tiempo Real

EngKey es un traductor de escritorio que traduce **mientras escribes**, sin cambiar de ventana. Aparece como overlay flotante, compatible con **Linux, Windows y macOS**.

```
┌──────────────────────────────────┐
│  Español                         │ ← input: escribe en tu idioma
│  ┌────────────────────────────┐  │
│  │ Hola, como estas?          │  │
│  └────────────────────────────┘  │
│  English                         │ ← output: traducido al instante
│  ┌────────────────────────────┐  │
│  │ Hello, how are you?        │  │
│  └────────────────────────────┘  │
│  [📋 Copiar] [🔄 Invertir] ⚙️ 🗑 │
└──────────────────────────────────┘
```

---

## ✨ Características

| Característica | Descripción |
|---------------|-------------|
| **Multi-API** | Google (default), DeepL, Microsoft Azure, LibreTranslate, OpenAI GPT |
| **Modo Nativo** | Post-procesado por dialecto: contracciones (`gonna`), ortografía GB (`colour`), modismos VE (`dale`) |
| **Seleccionable** | Elige motor y API key desde la UI de Configuración |
| **Overlay flotante** | Siempre al frente, accesible con hotkey global |
| **Caché LRU** | 250 entradas en memoria, sin llamadas repetidas |
| **Persistencia local** | Config en `~/.config/engkey/config.json` |
| **Offline-friendly** | Sin dependencias pesadas, cada motor es opcional |

---

## 🚀 Instalación

### Linux

```bash
# 1. Clonar
git clone https://github.com/vashuus/EngKey.git
cd EngKey

# 2. Entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Ejecutar
python3 Linux/engkey.py
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Windows\engkey.py
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./macOS/EngKey.app/Contents/MacOS/EngKey
```

---

## ⚙️ Motores de Traducción

| Motor | Calidad | Requiere API Key | Instalación |
|-------|:-------:|:----------------:|-------------|
| **Google Translate** (default) | ⭐⭐⭐⭐ | ❌ | `pip install deep-translator` |
| **DeepL** | ⭐⭐⭐⭐⭐ | ✅ (gratis) | `pip install deepl` |
| **Microsoft Azure** | ⭐⭐⭐⭐ | ✅ (gratis) | `pip install requests` |
| **LibreTranslate** | ⭐⭐⭐ | ❌ | `pip install requests` |
| **OpenAI GPT** | ⭐⭐⭐⭐⭐ | ✅ | `pip install openai` |

Para cambiar de motor: abre **Configuración** (⚙️) → selecciona API → ingresa key (si aplica).

---

## 🌿 Modo Nativo

Post-procesado que adapta la traducción genérica al dialecto real:

| Dialecto | Ejemplo |
|----------|---------|
| **en-US** | `"I am going to do what I want to do"` → `"I'm gonna do what I wanna do"` |
| **en-GB** | `"color"` → `"colour"`, `"apartment"` → `"flat"`, `"center"` → `"centre"` |
| **es-VE** | `"Thank you, I agree"` → `"Gracias, estoy dale"` |

Actívalo en Configuración → check **Modo Nativo** → selecciona dialecto.

---

## 🧪 Tests

```bash
# Unit tests (sin display)
python3 -m pytest tests/ -v -m "not e2e" --ignore=tests/test_e2e.py

# E2E tests (requiere Xvfb + xdotool en Linux)
Xvfb :99 -screen 0 1280x720x24 &
DISPLAY=:99 python3 -m pytest tests/test_e2e.py -v

# Todo junto
python3 -m pytest tests/ -v
```

---

## 🏗️ Arquitectura

```
EngKey/
├── core/                    ★ Código fuente único
│   ├── engines.py           Registro de motores (Registry pattern)
│   ├── translator.py        Facade con caché LRU
│   ├── main_window.py       UI con Tkinter
│   ├── settings_window.py   Diálogo de configuración
│   ├── native/              Pipeline de Modo Nativo
│   └── config_store.py      Persistencia JSON local
│
├── Linux/  Windows/  macOS/ Copias + scripts de plataforma
├── tests/                   Tests pytest
├── sync.sh                  Sincroniza core/ → plataformas
├── COPILOT.md               Contexto para asistentes AI
└── OPENCODE.md              Auditoría de publicación
```

---

## 📝 Licencia

MIT — ver [LICENSE](LICENSE).

---

## 🤝 Contribuir

1. Fork → branch → PR
2. Tests pasan: `pytest -q`
3. Ruff clean: `ruff check .`
4. Lee [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

*Parte del stack de productividad de [@vashuus](https://github.com/vashuus).*
