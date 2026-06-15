"""Ventana emergente de configuración — idiomas, motor de traducción y dialecto."""

import tkinter as tk
from tkinter import ttk

from config import BG, SURFACE, FG, ACCENT, MUTED, SUBTEXT
from languages import LANG
from native.dialects import has_dialects, get_variants, LABELS
from engines import list_engines


class Settings(tk.Toplevel):
    """Diálogo modal de configuración.

    Callback recibe: (source_code, target_code, dialect_code | None,
                       engine_id, api_key)
    """

    def __init__(
        self,
        parent: tk.Tk,
        source_code: str,
        target_code: str,
        dialect: str | None,
        engine_id: str,
        api_key: str,
        callback,
    ):
        super().__init__(parent)
        self._callback = callback
        self._last_tgt = target_code
        self._engine_id = engine_id  # guardar para detección de cambio

        self.title("EngKey — Configuración")
        self.configure(bg=BG)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.geometry("360x420")

        frame = tk.Frame(self, bg=SURFACE, padx=14, pady=14)
        frame.pack(fill="both", expand=True)

        codes = [c for _, c in LANG]
        engines = list_engines()  # [(id, name), ...]

        # ── Idioma de origen ──────────────────────────────────────────
        tk.Label(frame, text="Idioma de origen:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        self._src_var = tk.StringVar(value=source_code)
        ttk.Combobox(frame, textvariable=self._src_var,
                      values=codes, state="readonly", width=30).pack(
            fill="x", pady=(0, 8))

        # ── Idioma de destino ─────────────────────────────────────────
        tk.Label(frame, text="Idioma de destino:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        self._tgt_var = tk.StringVar(value=target_code)
        tgt_menu = ttk.Combobox(frame, textvariable=self._tgt_var,
                                 values=codes, state="readonly", width=30)
        tgt_menu.pack(fill="x", pady=(0, 10))

        # ── Separador ─────────────────────────────────────────────────
        sep = tk.Frame(frame, height=1, bg=MUTED)
        sep.pack(fill="x", pady=(0, 10))

        # ── Motor de traducción ────────────────────────────────────────
        tk.Label(frame, text="API de traducción:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        engine_names = [f"{n}" for _, n in engines]
        engine_ids = [i for i, _ in engines]
        self._eng_var = tk.StringVar(value=self._engine_name(engine_id, engines))
        eng_menu = ttk.Combobox(frame, textvariable=self._eng_var,
                                 values=engine_names, state="readonly", width=30)
        eng_menu.pack(fill="x", pady=(0, 8))
        eng_menu.bind("<<ComboboxSelected>>", self._on_engine_change)

        # guardar mapa id→name y name→id
        self._eng_id_map = {n: i for i, n in engines}
        self._eng_name_map = {i: n for i, n in engines}

        # ── API Key ────────────────────────────────────────────────────
        self._key_frame = tk.Frame(frame, bg=SURFACE)
        self._key_frame.pack(fill="x", pady=(0, 10))

        self._key_label = tk.Label(
            self._key_frame,
            text="API Key:",
            font=("Segoe UI", 9),
            fg=SUBTEXT, bg=SURFACE, anchor="w",
        )
        self._key_label.pack(fill="x")

        key_row = tk.Frame(self._key_frame, bg=SURFACE)
        key_row.pack(fill="x")

        self._key_var = tk.StringVar(value=api_key)
        self._key_entry = tk.Entry(
            key_row,
            textvariable=self._key_var,
            font=("Segoe UI", 9),
            bg=BG, fg=FG,
            insertbackground=ACCENT,
            relief="flat",
            bd=4,
            show="*",  # oculta caracteres por seguridad
        )
        self._key_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self._key_toggle_btn = tk.Button(
            key_row,
            text="👁",
            font=("Segoe UI", 9),
            bg=MUTED, fg=FG,
            relief="flat",
            padx=4, pady=1, bd=0,
            cursor="hand2",
            command=self._toggle_key_visibility,
        )
        self._key_toggle_btn.pack(side="right")

        # ── Separador ─────────────────────────────────────────────────
        sep2 = tk.Frame(frame, height=1, bg=MUTED)
        sep2.pack(fill="x", pady=(0, 10))

        # ── Modo Nativo ───────────────────────────────────────────────
        nat_frame = tk.Frame(frame, bg=SURFACE)
        nat_frame.pack(fill="x", pady=(0, 2))

        self._nat_var = tk.BooleanVar(value=dialect is not None)
        self._nat_cb = tk.Checkbutton(
            nat_frame,
            text="🌿  Modo Nativo",
            variable=self._nat_var,
            font=("Segoe UI", 9),
            fg=FG, bg=SURFACE,
            selectcolor=BG,
            activebackground=SURFACE,
            activeforeground=FG,
            cursor="hand2",
            command=self._toggle_native,
        )
        self._nat_cb.pack(side="left")

        # ── Dialecto ──────────────────────────────────────────────────
        dial_frame = tk.Frame(frame, bg=SURFACE)
        dial_frame.pack(fill="x", pady=(0, 10))

        self._dial_label = tk.Label(
            dial_frame,
            text="Dialecto:",
            font=("Segoe UI", 9),
            fg=SUBTEXT, bg=SURFACE,
        )
        self._dial_label.pack(side="left")

        variant_codes = self._get_variant_codes(target_code)
        initial_dialect = dialect if dialect in variant_codes else (
            variant_codes[0] if variant_codes else ""
        )
        self._dial_var = tk.StringVar(value=initial_dialect)
        self._dial_menu = ttk.Combobox(
            dial_frame,
            textvariable=self._dial_var,
            values=variant_codes,
            state="readonly" if variant_codes else "disabled",
            width=26,
        )
        self._dial_menu.pack(side="left", padx=(6, 0))

        # Mostrar nombre legible del dialecto actual
        self._dial_name = tk.Label(
            dial_frame,
            text=LABELS.get(initial_dialect, ""),
            font=("Segoe UI", 8),
            fg=SUBTEXT, bg=SURFACE,
        )
        self._dial_name.pack(side="left", padx=(4, 0))

        # Sincronizar nombre legible al cambiar selección
        self._dial_var.trace_add("write", self._update_dial_name)
        # Reconstruir dialectos si cambia el idioma destino
        self._tgt_var.trace_add("write", self._on_target_change)

        # Mostrar/ocultar según estado inicial
        self._update_dial_visibility()
        self._update_key_visibility()

        # ── Botones ───────────────────────────────────────────────────
        btn_frame = tk.Frame(frame, bg=SURFACE)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Aplicar",
                  font=("Segoe UI", 9, "bold"),
                  bg=ACCENT, fg=BG,
                  relief="flat", padx=16, pady=3, bd=0,
                  cursor="hand2",
                  command=self._apply).pack(side="right", padx=(6, 0))

        tk.Button(btn_frame, text="Cancelar",
                  font=("Segoe UI", 9),
                  bg=MUTED, fg=FG,
                  relief="flat", padx=12, pady=3, bd=0,
                  cursor="hand2",
                  command=self.destroy).pack(side="right")

    # ── helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _engine_name(engine_id: str, engines: list[tuple[str, str]]) -> str:
        for i, n in engines:
            if i == engine_id:
                return n
        return engines[0][1] if engines else "Google Translate"

    @staticmethod
    def _get_variant_codes(lang_code: str) -> list[str]:
        return [c for c, _ in get_variants(lang_code)]

    def _on_engine_change(self, *args):
        self._update_key_visibility()

    def _update_key_visibility(self):
        name = self._eng_var.get()
        eng_id = self._eng_id_map.get(name, "google")
        from engines import ENGINE_REGISTRY
        cls = ENGINE_REGISTRY.get(eng_id)
        needs_key = cls.needs_key if cls else False

        if needs_key:
            self._key_frame.pack(fill="x", pady=(0, 10))
            # Mostrar label de ayuda
            self._key_label.config(text=f"{cls.key_label}:")
        else:
            self._key_frame.pack_forget()

    def _toggle_key_visibility(self):
        if self._key_entry.cget("show") == "*":
            self._key_entry.config(show="")
            self._key_toggle_btn.config(text="🙈")
        else:
            self._key_entry.config(show="*")
            self._key_toggle_btn.config(text="👁")

    def _toggle_native(self):
        self._update_dial_visibility()

    def _update_dial_visibility(self):
        enabled = self._nat_var.get()
        tgt = self._tgt_var.get()
        variants = self._get_variant_codes(tgt) if enabled else []

        show = bool(enabled and variants)
        for w in (self._dial_label, self._dial_menu, self._dial_name):
            w.pack_forget()
        if show:
            self._dial_label.pack(side="left")
            self._dial_menu.pack(side="left", padx=(6, 0))
            self._dial_name.pack(side="left", padx=(4, 0))
            self._dial_menu.config(state="readonly", values=variants)
            if self._dial_var.get() not in variants:
                self._dial_var.set(variants[0])
                self._update_dial_name()
        else:
            self._dial_menu.config(state="disabled", values=[])

    def _on_target_change(self, *args):
        tgt = self._tgt_var.get()
        if tgt == self._last_tgt:
            return
        self._last_tgt = tgt
        self._update_dial_visibility()

    def _update_dial_name(self, *args):
        code = self._dial_var.get()
        self._dial_name.config(text=LABELS.get(code, ""))

    def _apply(self) -> None:
        src = self._src_var.get()
        tgt = self._tgt_var.get()
        dialect: str | None = None
        if self._nat_var.get():
            variants = self._get_variant_codes(tgt)
            if variants:
                dialect = self._dial_var.get()

        eng_name = self._eng_var.get()
        engine_id = self._eng_id_map.get(eng_name, "google")
        api_key = self._key_var.get()

        self._callback(src, tgt, dialect, engine_id, api_key)
        self.destroy()
