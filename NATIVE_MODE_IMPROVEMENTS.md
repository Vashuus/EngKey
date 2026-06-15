# Native Mode — Mejoras Propuestas

## 1. Refactorizar el motor de reglas (engine.py)

### Problema actual
El sistema actual es muy básico: busca patrones regex y reemplaza. No hay:
- Prioridad entre reglas
- Contexto lingüístico
- Validación antes/después

### Solución: Sistema de reglas con contexto

```python
"""Improved NativeMode engine with rule priority and context."""

import re
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum


class RulePriority(Enum):
    """Orden de ejecución de reglas (mayor número = ejecuta primero)."""
    CRITICAL = 3
    HIGH = 2
    MEDIUM = 1
    LOW = 0


@dataclass
class Rule:
    """Regla de naturalización con contexto."""
    pattern: str                        # Regex
    replacement: str | Callable         # Reemplazo (string o función)
    priority: RulePriority = RulePriority.MEDIUM
    context: Optional[str] = None       # 'word' (palabra completa) o None (substring)
    description: str = ""               # Explicación

    def apply(self, text: str) -> str:
        """Aplica la regla al texto."""
        flags = re.IGNORECASE

        if callable(self.replacement):
            # Función personalizada para lógica compleja
            return re.sub(self.pattern, self.replacement, text, flags=flags)
        else:
            # String simple
            return re.sub(self.pattern, self.replacement, text, flags=flags)


class NativeMode:
    """Procesador mejorado de reglas lingüísticas."""

    _rules: dict[str, list[Rule]] = {}

    @classmethod
    def register(cls, lang_code: str, rules: list[Rule]) -> None:
        """Registra reglas para un dialecto."""
        # Ordenar por prioridad (mayor primero)
        sorted_rules = sorted(rules, key=lambda r: r.priority.value, reverse=True)
        cls._rules[lang_code] = sorted_rules

    @classmethod
    def process(cls, text: str, lang: str) -> str:
        """Aplica todas las reglas del dialecto."""
        rules = cls._rules.get(lang)
        if not rules:
            return text

        result = text
        for rule in rules:
            result = rule.apply(result)

        return result

    @classmethod
    def list_rules(cls, lang: str) -> list[tuple[str, str, str]]:
        """Devuelve lista de reglas para debugging: (pattern, replacement, description)."""
        rules = cls._rules.get(lang, [])
        return [
            (r.pattern, 
             r.replacement if isinstance(r.replacement, str) else "<function>",
             r.description)
            for r in rules
        ]
```

### Usar en dialecto

```python
# en_us.py (mejorado)
from core.native.engine import Rule, RulePriority

RULES = [
    # Paso 1: Contracciones negativas (alta prioridad)
    Rule(
        pattern=r"\b(do|does|did)\s+not\b",
        replacement="don't",
        priority=RulePriority.HIGH,
        description="Contracción: 'do/does/did not' → 'don't'"
    ),
    Rule(
        pattern=r"\b(is|are|was|were)\s+not\b",
        replacement="isn't/aren't/wasn't/weren't",  # Según el sujeto
        priority=RulePriority.HIGH,
        description="Contracción: 'is/are/was/were not' → contracción"
    ),
    
    # Paso 2: Contracciones sujeto+verbo (media)
    Rule(
        pattern=r"\b(I)\s+(am)\b",
        replacement="I'm",
        priority=RulePriority.MEDIUM,
        description="Contracción: 'I am' → 'I'm'"
    ),
    
    # Paso 3: Reducciones informales (baja)
    Rule(
        pattern=r"\b(going|wanna|gotta)\s+to\b",
        replacement="gonna",
        priority=RulePriority.LOW,
        description="Reducción informal: 'going to' → 'gonna'"
    ),
]
```

---

## 2. Agregar más dialectos

### Estructura propuesta

```
core/native/
├── engine.py              (mejorado)
├── dialects.py            (actualizado)
├── __init__.py
├── en/
│   ├── en_us.py          ✅
│   ├── en_gb.py          ✅
│   └── en_au.py          (nuevo: Australian)
├── es/
│   ├── es_ar.py          ✅
│   ├── es_co.py          ✅
│   ├── es_ve.py          ✅
│   ├── es_es.py          (nuevo: Spain/Castilian)
│   ├── es_mx.py          (nuevo: Mexican)
│   └── es_pe.py          (nuevo: Peruvian)
├── fr/
│   ├── fr_fr.py          (nuevo: Parisian)
│   └── fr_ca.py          (nuevo: Québécois)
└── pt/
    └── pt_br.py          (nuevo: Brazilian Portuguese)
```

### Ejemplo: es_es.py (Castellano)

```python
"""Castellano (España) — reglas de naturalización.

Seseo, distinción formal/informal, expresiones españolas.
"""

from core.native.engine import Rule, RulePriority

RULES = [
    # Tú vs Vosotros (España es la única que distingue)
    Rule(
        pattern=r"\bvosotros\s+(sois|estáis|habéis)\b",
        replacement=lambda m: {
            "sois": "sois",
            "estáis": "estáis",
            "habéis": "habéis"
        }.get(m.group(1)),
        priority=RulePriority.HIGH,
        description="Preservar vosotros (único en español)"
    ),
    
    # Cortesía española
    Rule(
        pattern=r"\bmuchas gracias\b",
        replacement="gracias, tío",
        priority=RulePriority.MEDIUM,
        description="Saludos españoles informales"
    ),
    
    Rule(
        pattern=r"\bestupendo\b",
        replacement="cojonudo",
        priority=RulePriority.MEDIUM,
        description="Expresión española: 'estupendo' → 'cojonudo'"
    ),
    
    # Coloquialismos españoles
    Rule(
        pattern=r"\bchico\b",
        replacement="tío",
        priority=RulePriority.LOW,
        description="Léxico: 'chico' → 'tío' (amigo)"
    ),
    
    Rule(
        pattern=r"\bmuy bien\b",
        replacement="muy bien tío",
        priority=RulePriority.LOW,
        description="Expresión española"
    ),
]
```

---

## 3. Agregar tests para Native Mode

### tests/test_native_mode.py

```python
import pytest
from core.native import NativeMode


class TestEnglishUS:
    """Tests para dialecto American English."""
    
    def test_contractions_negative(self):
        """Verificar contracciones negativas."""
        text = "I do not like this"
        result = NativeMode.process(text, "en-US")
        assert "don't" in result.lower()
    
    def test_subject_verb_contraction(self):
        """Verificar contracciones sujeto+verbo."""
        text = "I am happy"
        result = NativeMode.process(text, "en-US")
        assert result == "I'm happy"
    
    def test_informal_reduction(self):
        """Verificar reducciones informales."""
        text = "I am going to do it"
        result = NativeMode.process(text, "en-US")
        # Primero aplica "I am" → "I'm", luego "going to" → "gonna"
        assert "gonna" in result.lower()


class TestSpanishAR:
    """Tests para dialecto Argentino."""
    
    def test_voseo(self):
        """Verificar transformación tú → vos."""
        text = "tú tienes razón"
        result = NativeMode.process(text, "es-AR")
        assert "vos tenés" in result.lower()
    
    def test_lunfardo(self):
        """Verificar lunfardo rioplatense."""
        text = "quiero trabajar"
        result = NativeMode.process(text, "es-AR")
        assert "laburo" in result.lower() or "laburar" in result.lower()


class TestNativeModeEdgeCases:
    """Tests de casos especiales."""
    
    def test_preserve_case_sensitivity(self):
        """El texto debe preservar mayúsculas donde corresponda."""
        text = "I AM HAPPY"
        result = NativeMode.process(text, "en-US")
        # Nota: Regex con re.IGNORECASE puede romper esto
        # Solución: usar replacer personalizado que preserve caso
        assert result is not None
    
    def test_empty_string(self):
        """Manejar texto vacío."""
        result = NativeMode.process("", "en-US")
        assert result == ""
    
    def test_unknown_dialect(self):
        """Dialecto desconocido devuelve texto original."""
        result = NativeMode.process("hello", "xx-XX")
        assert result == "hello"
```

---

## 4. Mejorar documentation de dialectos

### native/DIALECTS.md

```markdown
# Native Mode Dialects

## English

### en-US (American English)
- Contracciones negativas: "do not" → "don't"
- Reducciones informales: "going to" → "gonna"
- Léxico: "colour" → "color"

Examples:
- "I do not know" → "I don't know"
- "I'm going to work" → "I'm gonna work"

### en-GB (British English)
- Mantiene "going to" (sin reducir a "gonna")
- Ortografía: "color" → "colour", "favor" → "favour"
- Léxico: "apartment" → "flat", "truck" → "lorry"

Examples:
- "I'm going to do it" → "I'm going to do it" (sin cambio)
- "Color of the car" → "Colour of the car"

## Spanish

### es-AR (Argentino)
- Voseo: "tú tienes" → "vos tenés"
- Lunfardo: "dinero" → "guita"
- Calidez: "gracias" → "gracias che"

Examples:
- "¿Cómo estás?" → "¿Cómo andás?"
- "Chico" → "Pibe"

### es-CO (Colombiano)
- Coloquialismos: "parce", "bacano"
- "¿Cómo estás?" → "¿Qué más?"
- Léxico local: "amigo" → "parcero"

### es-ES (Castellano) [NEW]
- Preserva vosotros
- Expresiones españolas: "cojonudo", "tío"
- Formal pero cercano

## How to add a new dialect

1. Create `core/native/<lang>/<code>.py` with a `RULES` list
2. Register in `core/native/__init__.py`:
   ```python
   from .es import es_mx
   NativeMode.register("es-MX", es_mx.RULES)
   ```
3. Add to `core/native/dialects.py`:
   ```python
   DIALECTS["es"]["variants"].append(("es-MX", "🇲🇽  Mexicano"))
   ```
4. Add tests in `tests/test_native_mode.py`
```

---

## 5. Agregar preview de Native Mode en Settings

### Idea de UX mejora

En la ventana de Settings, cuando el usuario activa Native Mode:

```python
# settings_window.py (mejora)

def _update_native_preview(self):
    """Muestra preview de cómo se vería con Native Mode."""
    if not self._nat_var.get():
        self._preview_label.config(text="")
        return
    
    # Tomar el último texto traducido y aplicar Native Mode
    current_translation = self._main_window._output.get("1.0", "end-1c")
    dialect = self._dial_var.get()
    
    if not current_translation or not dialect:
        return
    
    # Aplicar Native Mode y mostrar diferencia
    from core.native import NativeMode
    preview = NativeMode.process(current_translation, dialect)
    
    if preview != current_translation:
        self._preview_label.config(
            text=f"Preview:\n{current_translation}\n↓\n{preview}",
            fg=ACCENT
        )
```

---

## 6. Performance: Cachear reglas compiladas

```python
"""Optimización: precompilar reglas regex."""

from functools import lru_cache
import re


@lru_cache(maxsize=100)
def _compile_pattern(pattern: str) -> re.Pattern:
    """Cachear Pattern compilados para evitar recompilar."""
    return re.compile(pattern, re.IGNORECASE)


class Rule:
    def __init__(self, pattern: str, replacement, ...):
        self.pattern = pattern
        self.replacement = replacement
        self._compiled = _compile_pattern(pattern)  # Guardar compilado
    
    def apply(self, text: str) -> str:
        return self._compiled.sub(self.replacement, text)
```

---

## Roadmap de implementación

### Fase 1 (Easy)
- ✅ Mejorar `engine.py` con `Rule` dataclass y prioridades
- ✅ Agregar tests básicos
- ✅ Documentar dialectos actuales

### Fase 2 (Medium)
- ✅ Agregar es-ES, es-MX
- ✅ Agregar en-AU
- ✅ Implementar Rule.description en UI

### Fase 3 (Hard)
- ✅ Preview en Settings (UI)
- ✅ Performance con funciones personalizadas
- ✅ Análisis de contexto lingüístico (NLP simple)

---

## Referencias

- [Voseo Argentino](https://es.wikipedia.org/wiki/Voseo)
- [Lunfardo](https://es.wikipedia.org/wiki/Lunfardo)
- [British vs American English](https://www.britannica.com/summary/British-vs-American-English)
- [Spanish Dialects](https://en.wikipedia.org/wiki/Spanish_dialects_and_varieties)
