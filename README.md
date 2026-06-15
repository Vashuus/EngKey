# EngKey

EngKey es un traductor flotante multiplataforma (Linux, Windows, macOS) que traduce texto en tiempo real mientras escribes en cualquier aplicación.

Características principales:
- Arquitectura centralizada en `core/` con wrappers por plataforma.
- Motores de traducción plugin (`google`, `deepl`, `microsoft`, `libre`, `gpt`).
- Modo Nativo: post-procesado por dialecto (contracciones, modismos, ortografía).
- Persistencia local en `~/.config/engkey/config.json`.

Instalación rápida (Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 Linux/engkey.py
```

Configuración:
- Configuración y API keys se guardan en `~/.config/engkey/config.json`.
- Abre Settings desde la UI para seleccionar motor y clave (si aplica).

Tests:
- `Linux/test_engkey.py` contiene pruebas E2E.
- Para CI se recomienda usar `pytest` con `pytest-xvfb`.

Contribuir:
- Añadir issues o PRs al repositorio.
- Antes de publicar, añadir `LICENSE`, `CONTRIBUTING.md` y configurar CI.

---

(Documento generado automáticamente por la auditoría OPENCODE).