# OPENCODE — Auditoría y lista de preparación para publicación

Resumen: auditoría del repositorio EngKey para preparar su publicación pública en GitHub. Incluye problemas detectados, puntos fuertes, recomendaciones concretas y una checklist accionable para hacer el proyecto escalable y seguro.

---

**Alcance de la revisión**
- Proyecto raíz: estructura multi-plataforma con `core/` como fuente única.
- Archivos analizados: código Python en `core/`, `Linux/`, `Windows/`, `macOS/` y utilidad `COPILOT.md`.
- Búsquedas realizadas: patrones `TODO|FIXME|print|assert`, tokens sensibles (`api_key|SECRET|token|password`), dependencias (`openai`, `deep-translator`, `requests`, `tkinter`).

---

**Resumen ejecutivo**
- El proyecto está bien pensado: arquitectura `core/` + adaptadores por plataforma, motor pluggable de traducción y pipeline de post-procesado (Modo Nativo).
- Principales ventajas: diseño modular, sistema de motores (Registry/Strategy), pruebas E2E (script `test_engkey.py`), enfoque multi-API y persistencia local de configuración.
- Obstáculos para publicar tal cual: falta de archivos de repo estándar (LICENSE en raíz, README con instrucciones públicas, .gitignore, manifest de dependencias), duplicación por plataforma sin un proceso de packaging claro, y ausencia de CI/configuración de release.

---

**Hallazgos concretos (evidencia)**
- Dependencias detectadas en el código: `deep-translator`, `requests`, `openai`, uso de `tkinter` (stdlib).
- Variables de API: la app usa `api_key` en varios módulos y la configuración por defecto guarda `"api_key": ""` (no aparece ninguna API key comprometida en el repo).
- Tests: `Linux/test_engkey.py` existe y ejecuta la app real (Tkinter/Xvfb). Contiene `print` y `assert` para aserciones E2E.
- Licencia: `COPILOT.md` menciona `core/LICENSE (GPLv3)`.
- Packaging/CI: no existe `requirements.txt`, `pyproject.toml` ni `setup.py`; tampoco `.gitignore` ni workflows CI bajo `.github/`.

---

**Problemas (prioridad alta)**
1. Falta de `LICENSE` en la raíz o comprobación de la licencia real — imprescindible antes de publicar.
2. No hay fichero de dependencias (`requirements.txt` / `pyproject.toml`) — dificulta reproducibilidad e instalación.
3. Ausencia de `.gitignore` — riesgo de subir archivos de entorno/keys/artefactos por accidente.
4. Duplicación de código entre `core/` y carpetas por plataforma — complica mantenimiento y provoca regresiones.
5. Tests E2E no automatizados con `pytest` y sin integración CI — hay que adaptar para CI (usar Xvfb en Linux CI).
6. Falta de documentación pública: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.

**Problemas (prioridad media/low)**
- Falta de linters/formatters y tipado (mypy/ruff/black) — mejora calidad e integrabilidad.
- No existe mecanismo de gestión de secretos (usar `.env` o keyring), aunque por ahora no hay secretos en el repo.
- Scripts de sincronización (`sync.sh`) que copian `core/` a carpetas puede ocultar cambios y dificultar diffs en PRs.

---

**Lo que está bien (fortalezas)**
- `core/` como fuente única: diseño pensado para evitar divergencia funcional.
- Arquitectura de motores (registry pattern) — facilita añadir nuevos backends sin tocar UI.
- Modo Nativo: pipeline de post-procesado con reglas por dialecto — valor diferencial claro.
- Pruebas funcionales existentes que ejercitan la app completa.
- Manejo de dependencias opcional en tiempo de ejecución (try/except con mensajes instructivos).

---

**Recomendaciones concretas (por pasos y prioridades)**
Prioridad Inmediata (publicación segura):
- Añadir un `LICENSE` en la raíz (por ejemplo MIT si corresponde). Verificar la propiedad intelectual y que todos los colaboradores acepten la licencia.
- Crear un `README.md` público con descripción, instalación mínima, ejemplos y permisos.
- Añadir `.gitignore` con patrones comunes (venv, __pycache__, .env, .DS_Store, .vscode, build/).
- Añadir un fichero de dependencias: `requirements.txt` (lista mínima: `deep-translator`, `requests`, `openai` — marcar `openai` como opcional) o crear `pyproject.toml` y configurar `poetry`/`pip-tools`.
- Añadir `SECURITY.md` y `CONTRIBUTING.md` básicos.

Prioridad Alta (calidad y CI):
- Añadir workflow de CI en `.github/workflows/ci.yml` que haga: instalar deps, ejecutar linters (`ruff`/`flake8`), formateo (`black`), ejecutar tests (`pytest` con Xvfb para pruebas UI en Linux).
- Convertir `Linux/test_engkey.py` en tests `pytest` (modularizar, usar fixtures y marks para E2E) y añadir pequeños tests unitarios para `core/translator.py`, `core/engines.py`.
- Añadir `requirements-dev.txt` con `pytest`, `pytest-xvfb`, `ruff`, `black`, `mypy`.

Prioridad Media (arquitectura y mantenimiento):
- Evitar duplicar TODO el código por plataforma; en su lugar empaquetar `core/` como un paquete Python instalable y crear ligeros wrappers por plataforma con solo scripts/recursos específicos. Esto facilita publicar `core` como pip package interno.
- Reemplazar `sync.sh` por un proceso reproducible: packaging + entry points o un submodule/subpackage si se necesita mantener copias.
- Añadir tipado gradual (mypy) y cobertura básica de tests.

Prioridad Baja (escalabilidad y comunidad):
- Documentar cómo agregar nuevos motores con ejemplos; añadir tests de integración de motores con mocks.
- Añadir métricas y telemetría opt-in (si aplica), y consideraciones de privacidad.
- Añadir `CHANGELOG.md` y práctica de versionado semántico.

---

**Checklist de publicación (acción rápida)**
- [ ] Confirmar licencia y añadir `LICENSE` en la raíz.
- [ ] Crear `README.md` con instalación básica y ejecución de ejemplo.
- [ ] Añadir `.gitignore` y `SECURITY.md`.
- [ ] Crear `requirements.txt` y `requirements-dev.txt`.
- [ ] Añadir workflow CI (`.github/workflows/ci.yml`) para linter + tests.
- [ ] Convertir tests E2E a `pytest` y añadir tests unitarios mínimos.
- [ ] Revisar que no haya secretos en el repo (hacer `git-secrets` scan si procede).
- [ ] Consolidar `core/` en paquete instalable y reducir duplicación de plataforma.

---

**Sugerencias de comandos útiles**
```bash
# Rápido: crear requirements (manualmente) y entorno virtual
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install deep-translator requests
pip freeze > requirements.txt

# Instalar dev deps
pip install pytest pytest-xvfb ruff black mypy
pip freeze > requirements-dev.txt

# Ejecutar tests (Linux) con Xvfb
pytest -q

# Ejecutar linter y formato
ruff check .
black --check .
```

---

**Checklist de seguridad rápido**
- No subir keys en texto claro: usar `~/.config/engkey/config.json` para guardar `api_key` localmente (ya sugerido por el proyecto). No incluir este archivo en VCS.
- Añadir `.env.example` y documentar cómo configurar keys en `README.md`.

---

Si quieres, lo recreo ahora en la raíz como `OPENCODE.md` para que puedas verlo desde tu explorador y luego genero `README.md` y `LICENSE` básicos. ¿Lo hago?