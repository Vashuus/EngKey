"""Motores de traducción intercambiables.

Cada motor implementa translate(text, source, target) -> str.
Se registran en ENGINE_REGISTRY para selección en Settings.
"""

import html


# ── Registry ───────────────────────────────────────────────────────────────

ENGINE_REGISTRY: dict[str, type["BaseEngine"]] = {}


def register(cls: type["BaseEngine"]):
    ENGINE_REGISTRY[cls.id] = cls


def list_engines() -> list[tuple[str, str]]:
    return [(e.id, e.name) for e in ENGINE_REGISTRY.values()]


def build_engine(engine_id: str, api_key: str = ""):
    cls = ENGINE_REGISTRY.get(engine_id)
    if not cls:
        raise ValueError(f"Motor desconocido: {engine_id}")
    return cls(api_key)


# ── Base ───────────────────────────────────────────────────────────────────

class BaseEngine:
    id = ""
    name = ""
    needs_key = False
    key_label = "API Key"
    help_url = ""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self._available = False
        self._setup()

    def _setup(self):
        raise NotImplementedError

    def translate(self, text: str, source: str, target: str) -> str:
        raise NotImplementedError


# ── Google Translate (vía deep-translator) ────────────────────────────────

class GoogleEngine(BaseEngine):
    id = "google"
    name = "Google Translate"
    needs_key = False

    def _setup(self):
        try:
            from deep_translator import GoogleTranslator
            self._gt = GoogleTranslator
            self._available = True
        except ImportError:
            self._available = False

    def translate(self, text: str, source: str, target: str) -> str:
        if not self._available:
            raise RuntimeError("deep-translator no instalado: pip install deep-translator")
        result = self._gt(source=source, target=target).translate(text)
        return html.unescape(result)

register(GoogleEngine)


# ── DeepL ──────────────────────────────────────────────────────────────────

class DeepLEngine(BaseEngine):
    id = "deepl"
    name = "DeepL"
    needs_key = True
    key_label = "DeepL API Key (deepl.com/pro)"
    help_url = "https://www.deepl.com/pro"

    def _setup(self):
        try:
            import deepl
            self._deepl = deepl
            self._available = True
        except ImportError:
            self._available = False

    def translate(self, text: str, source: str, target: str) -> str:
        if not self._available:
            raise RuntimeError("deepl no instalado: pip install deepl")
        if not self.api_key:
            raise RuntimeError("DeepL API Key no configurada")
        client = self._deepl.Translator(self.api_key)
        lang = target.upper()
        if lang == "EN":
            lang = "EN-US"
        result = client.translate_text(text, source_lang=source.upper() if source else None, target_lang=lang)
        return result.text

register(DeepLEngine)


# ── Microsoft Azure Translator ─────────────────────────────────────────────

class MicrosoftEngine(BaseEngine):
    id = "microsoft"
    name = "Microsoft Azure Translator"
    needs_key = True
    key_label = "Azure Translator Key (portal.azure.com)"
    help_url = "https://portal.azure.com"

    def _setup(self):
        try:
            import requests
            self._requests = requests
            self._available = True
        except ImportError:
            self._available = False

    def translate(self, text: str, source: str, target: str) -> str:
        if not self._available:
            raise RuntimeError("requests no instalado: pip install requests")
        if not self.api_key:
            raise RuntimeError("Azure Key no configurada")
        import uuid
        endpoint = "https://api.cognitive.microsofttranslator.com"
        path = "/translate?api-version=3.0"
        params = f"&from={source}&to={target}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        body = [{"text": text}]
        r = self._requests.post(endpoint + path + params, headers=headers, json=body, timeout=10)
        r.raise_for_status()
        return r.json()[0]["translations"][0]["text"]

register(MicrosoftEngine)


# ── LibreTranslate ─────────────────────────────────────────────────────────

class LibreEngine(BaseEngine):
    id = "libre"
    name = "LibreTranslate"
    needs_key = False
    key_label = "API URL (default: libretranslate.com)"

    def __init__(self, api_key: str = ""):
        self._instance = "https://libretranslate.com"
        if api_key and api_key.startswith("http"):
            self._instance = api_key.rstrip("/")
            api_key = ""
        super().__init__(api_key)

    def _setup(self):
        try:
            import requests
            self._requests = requests
            self._available = True
        except ImportError:
            self._available = False

    def translate(self, text: str, source: str, target: str) -> str:
        if not self._available:
            raise RuntimeError("requests no instalado: pip install requests")
        payload = {"q": text, "source": source, "target": target}
        if self.api_key:
            payload["api_key"] = self.api_key
        r = self._requests.post(f"{self._instance}/translate", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["translatedText"]

register(LibreEngine)


# ── OpenAI GPT ─────────────────────────────────────────────────────────────

class GPTEngine(BaseEngine):
    id = "gpt"
    name = "OpenAI GPT"
    needs_key = True
    key_label = "OpenAI API Key (platform.openai.com)"
    help_url = "https://platform.openai.com/api-keys"

    def _setup(self):
        try:
            from openai import OpenAI
            self._OpenAI = OpenAI
            self._available = True
        except ImportError:
            self._available = False

    def translate(self, text: str, source: str, target: str) -> str:
        if not self._available:
            raise RuntimeError("openai no instalado: pip install openai")
        if not self.api_key:
            raise RuntimeError("OpenAI API Key no configurada")
        client = self._OpenAI(api_key=self.api_key)
        prompt = (
            f"Translate the following text from {source} to {target}. "
            f"Respond with ONLY the translation, no explanations, no quotes.\n\n{text}"
        )
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return r.choices[0].message.content.strip()

register(GPTEngine)
