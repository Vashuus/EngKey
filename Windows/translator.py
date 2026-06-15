"""Traductor — wrapper sobre motor intercambiable con caché y Modo Nativo."""

import threading

from engines import build_engine
from config import MAX_CACHE
from native import NativeMode


class Translator:
    """Traductor bidireccional con motor intercambiable y caché LRU."""

    def __init__(
        self,
        source: str = "es",
        target: str = "en",
        engine_id: str = "google",
        api_key: str = "",
    ):
        self._source = source
        self._target = target
        self._engine_id = engine_id
        self._api_key = api_key
        self._dialect: str | None = None
        self._cache: dict[tuple, str] = {}
        self._lock = threading.Lock()
        self._engine = None
        self._build_engine()

    # ── configuración ─────────────────────────────────────────────────

    def _build_engine(self) -> None:
        try:
            self._engine = build_engine(self._engine_id, self._api_key)
        except Exception:
            self._engine = None

    def set_engine(self, engine_id: str, api_key: str = "") -> None:
        self._engine_id = engine_id
        self._api_key = api_key
        self._cache.clear()
        self._build_engine()

    def set_direction(self, source: str, target: str) -> None:
        self._source = source
        self._target = target
        self._cache.clear()

    def set_dialect(self, dialect: str | None) -> None:
        self._dialect = dialect

    # ── traducción ────────────────────────────────────────────────────

    def translate(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        if not self._engine:
            return text

        key = (text, self._dialect)
        with self._lock:
            cached = self._cache.get(key)
            if cached is not None:
                return cached

        try:
            result = self._engine.translate(text, self._source, self._target)
        except Exception:
            result = text

        if self._dialect:
            result = NativeMode.process(result, self._dialect)

        with self._lock:
            self._cache[key] = result
            if len(self._cache) > MAX_CACHE:
                self._cache.clear()

        return result
