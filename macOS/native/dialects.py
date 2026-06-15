"""Metadatos de dialectos para el Modo Nativo.

Cada idioma puede tener múltiples variantes dialectales con sus propias
reglas de naturalización (slang, coloquialismos, ortografía regional).

Para agregar un dialecto nuevo:
  1. Crear native/<lang>/<dialect>.py con una lista `RULES`
  2. Agregar el código aquí en `DIALECTS`
  3. Importar y registrar en native/__init__.py
"""

DIALECTS: dict[str, dict] = {
    "en": {
        "name": "English",
        "default": "en-US",
        "variants": [
            ("en-US", "🇺🇸  American English"),
            ("en-GB", "🇬🇧  British English"),
        ],
    },
    "es": {
        "name": "Español",
        "default": "es-VE",
        "variants": [
            ("es-VE", "🇻🇪  Venezolano"),
            ("es-CO", "🇨🇴  Colombiano"),
            ("es-AR", "🇦🇷  Argentino"),
        ],
    },
}

# Reverse map: dialect_code -> display label
LABELS: dict[str, str] = {}
for _lang, info in DIALECTS.items():
    for code, label in info["variants"]:
        LABELS[code] = label


def has_dialects(lang_code: str) -> bool:
    """True si el idioma tiene dialectos definidos."""
    return lang_code in DIALECTS


def get_variants(lang_code: str) -> list[tuple[str, str]]:
    """Lista de (código, etiqueta) para los dialectos de un idioma."""
    info = DIALECTS.get(lang_code)
    return info["variants"] if info else []


def get_default(lang_code: str) -> str:
    """Código del dialecto por defecto para un idioma."""
    info = DIALECTS.get(lang_code)
    return info["default"] if info else lang_code
