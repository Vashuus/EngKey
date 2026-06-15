"""Ventana principal de EngKey — overlay flotante con entrada/salida de texto."""

import tkinter as tk
import queue
import threading

from config import (
    BG, SURFACE, FG, ACCENT, MUTED, SUBTEXT,
    W, H, MIN_W, MIN_H, POS_OFFX, POS_OFFY, DEBOUNCE_MS,
)
from languages import LANG_NAMES
from debouncer import Debouncer
from translator import Translator
from settings_window import Settings
from native.dialects import LABELS as DIALECT_LABELS
from engines import list_engines, ENGINE_REGISTRY
from config_store import load as load_config, save as save_config


class EngKey:
    """Aplicación traductor flotante."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EngKey")
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{W}x{H}+{sw-W-POS_OFFX}+{sh-H-POS_OFFY}")
        self.root.minsize(MIN_W, MIN_H)

        # Cargar configuración persistente
        cfg = load_config()
        self._src_code = cfg.get("source", "es")
        self._tgt_code = cfg.get("target", "en")
        self._dialect: str | None = cfg.get("dialect")
        self._engine_id = cfg.get("engine", "google")
        self._api_key = cfg.get("api_key", "")

        # Componentes
        self._translator = Translator(
            source=self._src_code,
            target=self._tgt_code,
            engine_id=self._engine_id,
            api_key=self._api_key,
        )
        if self._dialect:
            self._translator.set_dialect(self._dialect)

        self._debouncer = Debouncer(DEBOUNCE_MS, self._translate)
        self._update_queue: queue.Queue = queue.Queue()

        # UI
        self._build_ui()
        self._poll_queue()

        # Eventos
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.bind("<Escape>", lambda e: self._quit())
        self.root.after(100, self._input.focus_set)

    # ═══════════════════════════════════════════════════════════════════
    #  UI
    # ═══════════════════════════════════════════════════════════════════

    def _build_ui(self):
        # ── Entrada ───────────────────────────────────────────────────
        self._lbl_in = tk.Label(
            self.root,
            text="Español",
            font=("Segoe UI", 9, "bold"),
            fg=SUBTEXT,
            bg=BG,
            anchor="w",
        )
        self._lbl_in.pack(fill="x", padx=10, pady=(8, 2))

        self._input = tk.Text(
            self.root,
            height=3,
            font=("Segoe UI", 11),
            bg=SURFACE,
            fg=FG,
            insertbackground=ACCENT,
            relief="flat",
            bd=6,
            padx=6,
            pady=4,
            wrap="word",
        )
        self._input.pack(fill="both", padx=10, pady=(0, 0), expand=True)
        self._input.bind("<KeyRelease>", lambda e: self._debouncer.poke())

        # ── Salida ────────────────────────────────────────────────────
        self._lbl_out = tk.Label(
            self.root,
            text="English",
            font=("Segoe UI", 9, "bold"),
            fg=SUBTEXT,
            bg=BG,
            anchor="w",
        )
        self._lbl_out.pack(fill="x", padx=10, pady=(6, 2))

        self._output = tk.Text(
            self.root,
            height=3,
            font=("Segoe UI", 11),
            bg=SURFACE,
            fg=ACCENT,
            relief="flat",
            bd=6,
            padx=6,
            pady=4,
            wrap="word",
        )
        self._output.pack(fill="both", padx=10, pady=(0, 0), expand=True)
        self._output.configure(state="disabled")

        # ── Barra de botones ──────────────────────────────────────────
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill="x", padx=10, pady=(6, 8))

        self._copy_btn = tk.Button(
            bar,
            text="📋  Copiar inglés",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT,
            fg=BG,
            relief="flat",
            padx=12,
            pady=3,
            bd=0,
            cursor="hand2",
            activebackground="#7aa2f7",
            command=self._copy,
        )
        self._copy_btn.pack(side="left", padx=(0, 6))

        self._invert_btn = tk.Button(
            bar,
            text="🔄  Invertir",
            font=("Segoe UI", 9),
            bg=SURFACE,
            fg=FG,
            relief="flat",
            padx=10,
            pady=3,
            bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._invert,
        )
        self._invert_btn.pack(side="left", padx=(0, 6))

        self._settings_btn = tk.Button(
            bar,
            text="⚙️",
            font=("Segoe UI", 10),
            bg=SURFACE,
            fg=SUBTEXT,
            relief="flat",
            padx=6,
            pady=3,
            bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._open_settings,
        )
        self._settings_btn.pack(side="left")

        self._clear_btn = tk.Button(
            bar,
            text="🗑  Limpiar",
            font=("Segoe UI", 9),
            bg=SURFACE,
            fg=FG,
            relief="flat",
            padx=12,
            pady=3,
            bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._clear,
        )
        self._clear_btn.pack(side="left", padx=(6, 0))

        self._status = tk.Label(
            bar,
            text="",
            font=("Segoe UI", 8),
            fg=SUBTEXT,
            bg=BG,
        )
        self._status.pack(side="right")

    # ═══════════════════════════════════════════════════════════════════
    #  Configuración
    # ═══════════════════════════════════════════════════════════════════

    def _open_settings(self):
        Settings(
            self.root,
            self._src_code,
            self._tgt_code,
            self._dialect,
            self._engine_id,
            self._api_key,
            self._apply_settings,
        )

    def _apply_settings(
        self,
        src: str,
        tgt: str,
        dialect: str | None,
        engine_id: str,
        api_key: str,
    ):
        # Motor
        engine_changed = engine_id != self._engine_id or api_key != self._api_key
        if engine_changed:
            self._engine_id = engine_id
            self._api_key = api_key
            self._translator.set_engine(engine_id, api_key)

        # Dirección
        dir_changed = src != self._src_code or tgt != self._tgt_code
        if dir_changed:
            self._src_code = src
            self._tgt_code = tgt
            self._translator.set_direction(src, tgt)

        # Dialecto
        if dialect != self._dialect:
            self._dialect = dialect
            self._translator.set_dialect(dialect)

        # Persistir
        save_config({
            "engine": self._engine_id,
            "api_key": self._api_key,
            "source": self._src_code,
            "target": self._tgt_code,
            "native_mode": dialect is not None,
            "dialect": dialect,
        })

        self._refresh_labels()

        if dialect:
            name = DIALECT_LABELS.get(dialect, dialect)
            self._flash(f"🌿  {name}")
        if engine_changed:
            eng_name = ENGINE_REGISTRY[self._engine_id].name
            self._flash(f"⚡ {eng_name}")
        if dir_changed:
            self._clear()

    def _refresh_labels(self):
        src_name = LANG_NAMES.get(self._src_code, self._src_code)
        tgt_name = LANG_NAMES.get(self._tgt_code, self._tgt_code)

        self._lbl_in.config(text=src_name)
        self._lbl_out.config(text=tgt_name)
        self._copy_btn.config(text=f"📋  Copiar {tgt_name.lower()}")

        eng_name = ENGINE_REGISTRY[self._engine_id].name
        label = f"⚡ {eng_name} — {src_name} → {tgt_name}"
        if self._dialect:
            name = DIALECT_LABELS.get(self._dialect, self._dialect)
            label += f" 🌿  {name}"
        self.root.title(label)

    # ═══════════════════════════════════════════════════════════════════
    #  Traducción
    # ═══════════════════════════════════════════════════════════════════

    def _translate(self):
        text = self._input.get("1.0", "end-1c")
        if not text.strip():
            self._set_output("")
            return
        self._status.config(text="✍️  traduciendo…")
        threading.Thread(target=self._translate_worker, args=(text,), daemon=True).start()

    def _translate_worker(self, text: str):
        result = self._translator.translate(text)
        self._update_queue.put(("result", result))

    def _set_output(self, text: str):
        self._output.configure(state="normal")
        self._output.delete("1.0", "end")
        self._output.insert("1.0", text)
        self._output.configure(state="disabled")

    def _poll_queue(self):
        try:
            while True:
                kind, val = self._update_queue.get_nowait()
                if kind == "result":
                    self._set_output(val)
                    self._status.config(text="")
        except queue.Empty:
            pass
        self.root.after(80, self._poll_queue)

    # ═══════════════════════════════════════════════════════════════════
    #  Acciones
    # ═══════════════════════════════════════════════════════════════════

    def _copy(self):
        text = self._output.get("1.0", "end-1c")
        if not text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._flash("✅  Copiado")

    def _clear(self):
        self._input.delete("1.0", "end")
        self._output.configure(state="normal")
        self._output.delete("1.0", "end")
        self._output.configure(state="disabled")
        self._status.config(text="")

    def _invert(self):
        self._src_code, self._tgt_code = self._tgt_code, self._src_code
        self._translator.set_direction(self._src_code, self._tgt_code)
        self._dialect = None
        self._translator.set_dialect(None)
        self._refresh_labels()
        self._clear()

    def _flash(self, msg: str, duration_ms: int = 2000):
        self._status.config(text=msg)
        self.root.after(duration_ms, lambda: self._status.config(text=""))

    def _quit(self):
        self._debouncer.cancel()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
