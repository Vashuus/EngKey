"""Main window - floating overlay with input/output text areas."""

import os
import tkinter as tk
from tkinter import font as tkfont
import queue
import threading

from env import detect as detect_env
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
from config_store import load as load_config, save as save_config, DEFAULT


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert '#rrggbb' to (R, G, B)."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


class EngKey:
    """Floating translator application."""

    def __init__(self, debug: bool = False):
        # Detect runtime environment
        self._env = detect_env()
        self._debug = debug
        if debug:
            from env import print_summary
            print_summary(self._env)

        self.root = tk.Tk()
        self.root.title("EngKey")
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{W}x{H}+{sw-W-POS_OFFX}+{sh-H-POS_OFFY}")
        self.root.minsize(MIN_W, MIN_H)

        # Load persisted configuration
        cfg = load_config()
        self._src_code = cfg.get("source", "en")
        self._tgt_code = cfg.get("target", "es")
        self._dialect: str | None = cfg.get("dialect")
        self._engine_id = cfg.get("engine", "google")
        self._api_key = cfg.get("api_key", "")
        self._font_family = cfg.get("font_family", DEFAULT["font_family"])
        self._font_size = cfg.get("font_size", DEFAULT["font_size"])
        self._bg_image = cfg.get("bg_image", DEFAULT["bg_image"])
        self._custom_colors = cfg.get("custom_colors", DEFAULT["custom_colors"]).copy()
        self._overlay_opacity = cfg.get("overlay_opacity", DEFAULT["overlay_opacity"])
        self._button_border_style = cfg.get("button_border_style", "default")

        # Components
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
        self._overlay_label: tk.Label | None = None
        self._overlay_photo = None
        self._after_resize_id: str | None = None
        self._build_ui()
        self._apply_fonts()
        self._apply_button_style()
        self._apply_appearance(cfg)
        self._load_overlay(self._bg_image, self._overlay_opacity)
        self._poll_queue()

        # Events
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.bind("<Escape>", lambda e: self._quit())
        self.root.bind("<Configure>", self._on_window_configure)
        self.root.after(100, self._input.focus_set)

        self._refresh_labels()

        if self._env["topmost_reliable"] == "unreliable":
            self._flash("No display server detected - running in a TTY?")
        elif self._env["topmost_reliable"] == "partial":
            self._flash("Always-on-top may not work on this desktop", 3000)

    # ═══════════════════════════════════════════════════════════════════
    #  Appearance
    # ═══════════════════════════════════════════════════════════════════

    def _apply_appearance(self, cfg: dict) -> None:
        colors = cfg.get("custom_colors", {})
        self._custom_colors = colors.copy()
        self._bg_image = cfg.get("bg_image")
        if colors:
            root_bg = colors.get("BG", BG)
            self.root.configure(bg=root_bg)

    def _apply_fonts(self) -> None:
        family = self._font_family
        size = self._font_size
        self._lbl_in.config(font=(family, 9, "bold"))
        self._input.config(font=(family, size))
        self._lbl_out.config(font=(family, 9, "bold"))
        self._output.config(font=(family, size))
        for btn in (self._copy_btn, self._invert_btn,
                     self._settings_btn, self._clear_btn):
            btn.config(font=(family, 9))
        self._status.config(font=(family, 8))

    def _apply_button_style(self) -> None:
        if self._button_border_style == "soft":
            relief = "groove"
            bd = 1
        else:
            relief = "flat"
            bd = 0

        for btn in (self._copy_btn, self._invert_btn,
                     self._settings_btn, self._clear_btn):
            btn.config(relief=relief, bd=bd)

        self._copy_btn.config(bg=ACCENT, fg=BG,
                              activebackground="#7aa2f7")

    def _apply_overlay_tint(self, path: str | None, opacity: float) -> None:
        """Tint SURFACE widgets to simulate the image showing through.

        When an image is active, SURFACE widgets' bg is blended toward the
        composited overlay colour so they appear semi-transparent.
        When no image, original colours are restored.
        """
        surface_widgets = (
            self._input, self._output,
            self._invert_btn, self._settings_btn, self._clear_btn,
        )

        if not path or not os.path.isfile(path) or opacity <= 0.0:
            for w in surface_widgets:
                w.config(bg=SURFACE)
            return

        try:
            from PIL import Image
            img = Image.open(path).convert("RGBA")
            avg = img.resize((1, 1), Image.LANCZOS).getpixel((0, 0))[:3]
            bg_rgb = _hex_to_rgb(BG)

            # overlay_bg = blend(avg_img, BG, opacity)
            overlay = tuple(
                int(avg[i] * opacity + bg_rgb[i] * (1 - opacity))
                for i in range(3)
            )

            # SURFACE → blend overlay (80%) with SURFACE (20%)
            s = _hex_to_rgb(SURFACE)
            tint = tuple(min(255, int(overlay[i] * 0.8 + s[i] * 0.2))
                         for i in range(3))
            tint_hex = f"#{tint[0]:02x}{tint[1]:02x}{tint[2]:02x}"

            for w in surface_widgets:
                w.config(bg=tint_hex)
        except Exception:
            for w in surface_widgets:
                w.config(bg=SURFACE)

    # ═══════════════════════════════════════════════════════════════════
    #  Overlay
    # ═══════════════════════════════════════════════════════════════════

    def _build_overlay(self, path: str | None, opacity: float) -> None:
        """Composite a user background image onto the BG colour and place it behind widgets."""
        if self._overlay_label is not None:
            self._overlay_label.destroy()
            self._overlay_label = None
        self._overlay_photo = None

        if not path or not os.path.isfile(path) or opacity <= 0.0:
            self._apply_overlay_tint(None, 0.0)
            return

        cw = self.root.winfo_width() or W
        ch = self.root.winfo_height() or H

        try:
            from PIL import Image, ImageTk
            img = Image.open(path).convert("RGBA")
            img = img.resize((cw, ch), Image.LANCZOS)

            root_bg_hex = self._custom_colors.get("BG", BG)
            bg_rgb = _hex_to_rgb(root_bg_hex)
            bg_layer = Image.new("RGBA", img.size, bg_rgb + (255,))
            blended = Image.blend(bg_layer, img, opacity)

            self._overlay_photo = ImageTk.PhotoImage(blended.convert("RGB"))
        except ImportError:
            try:
                self._overlay_photo = tk.PhotoImage(file=path)
            except Exception:
                self._apply_overlay_tint(None, 0.0)
                return
        except Exception:
            self._apply_overlay_tint(None, 0.0)
            return

        self._overlay_label = tk.Label(self.root, image=self._overlay_photo)
        self._overlay_label.place(x=0, y=0, relwidth=1, relheight=1)
        self._overlay_label.lower()
        self._apply_overlay_tint(path, opacity)

    def _load_overlay(self, path: str | None, opacity: float | None = None) -> None:
        if opacity is None:
            opacity = self._overlay_opacity
        self._bg_image = path
        self._overlay_opacity = opacity if opacity is not None else 0.0
        self._build_overlay(path, self._overlay_opacity)

    def _on_window_configure(self, event) -> None:
        """Rebuild overlay on resize, debounced."""
        if event.widget is not self.root:
            return
        if self._after_resize_id is not None:
            self.root.after_cancel(self._after_resize_id)
        self._after_resize_id = self.root.after(
            150, lambda: self._build_overlay(self._bg_image, self._overlay_opacity)
        )

    # ═══════════════════════════════════════════════════════════════════
    #  UI
    # ═══════════════════════════════════════════════════════════════════

    def _build_ui(self):
        PX = 14

        # Input area
        self._lbl_in = tk.Label(
            self.root, text="",
            font=("Segoe UI", 9, "bold"),
            fg=SUBTEXT, bg=BG, anchor="w",
        )
        self._lbl_in.pack(fill="x", padx=PX, pady=(10, 3))

        self._input = tk.Text(
            self.root, height=3,
            font=("Segoe UI", 11),
            bg=SURFACE, fg=FG,
            insertbackground=ACCENT,
            relief="flat", bd=6,
            padx=8, pady=6,
            wrap="word",
            highlightthickness=1,
            highlightbackground=MUTED,
            highlightcolor=ACCENT,
        )
        self._input.pack(fill="both", padx=PX, pady=(0, 0), expand=True)
        self._input.bind("<KeyRelease>", lambda e: self._debouncer.poke())

        # Output area
        self._lbl_out = tk.Label(
            self.root, text="",
            font=("Segoe UI", 9, "bold"),
            fg=SUBTEXT, bg=BG, anchor="w",
        )
        self._lbl_out.pack(fill="x", padx=PX, pady=(8, 3))

        self._output = tk.Text(
            self.root, height=3,
            font=("Segoe UI", 11),
            bg=SURFACE, fg=ACCENT,
            relief="flat", bd=6,
            padx=8, pady=6,
            wrap="word",
            highlightthickness=1,
            highlightbackground=MUTED,
            highlightcolor=ACCENT,
        )
        self._output.pack(fill="both", padx=PX, pady=(0, 0), expand=True)
        self._output.configure(state="disabled")

        # Button bar
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill="x", padx=PX, pady=(8, 10))

        self._copy_btn = tk.Button(
            bar, text="",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT, fg=BG,
            relief="flat", padx=14, pady=4, bd=0,
            cursor="hand2",
            activebackground="#7aa2f7",
            command=self._copy,
        )
        self._copy_btn.pack(side="left", padx=(0, 6))

        self._invert_btn = tk.Button(
            bar, text="Swap",
            font=("Segoe UI", 9),
            bg=SURFACE, fg=FG,
            relief="flat", padx=10, pady=4, bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._invert,
        )
        self._invert_btn.pack(side="left", padx=(0, 6))

        self._settings_btn = tk.Button(
            bar, text="Settings",
            font=("Segoe UI", 9),
            bg=SURFACE, fg=FG,
            relief="flat", padx=8, pady=4, bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._open_settings,
        )
        self._settings_btn.pack(side="left")

        self._clear_btn = tk.Button(
            bar, text="Clear",
            font=("Segoe UI", 9),
            bg=SURFACE, fg=FG,
            relief="flat", padx=12, pady=4, bd=0,
            cursor="hand2",
            activebackground=MUTED,
            command=self._clear,
        )
        self._clear_btn.pack(side="left", padx=(6, 0))

        self._status = tk.Label(
            bar, text="",
            font=("Segoe UI", 8),
            fg=SUBTEXT, bg=BG,
        )
        self._status.pack(side="right")

    # ═══════════════════════════════════════════════════════════════════
    #  Configuration
    # ═══════════════════════════════════════════════════════════════════

    def _open_settings(self):
        appearance = {
            "font_family": self._font_family,
            "font_size": self._font_size,
            "bg_image": self._bg_image,
            "custom_colors": self._custom_colors,
            "overlay_opacity": self._overlay_opacity,
            "button_border_style": self._button_border_style,
        }
        Settings(
            self.root,
            self._src_code,
            self._tgt_code,
            self._dialect,
            self._engine_id,
            self._api_key,
            self._apply_settings,
            appearance=appearance,
        )

    def _apply_settings(self, cfg: dict):
        src = cfg.get("source", self._src_code)
        tgt = cfg.get("target", self._tgt_code)
        dialect = cfg.get("dialect")
        engine_id = cfg.get("engine", self._engine_id)
        api_key = cfg.get("api_key", self._api_key)
        font_family = cfg.get("font_family", self._font_family)
        font_size = cfg.get("font_size", self._font_size)
        bg_image = cfg.get("bg_image", self._bg_image)
        custom_colors = cfg.get("custom_colors", self._custom_colors)
        overlay_opacity = cfg.get("overlay_opacity", self._overlay_opacity)
        button_border_style = cfg.get("button_border_style", "default")

        engine_changed = engine_id != self._engine_id or api_key != self._api_key
        if engine_changed:
            self._engine_id = engine_id
            self._api_key = api_key
            self._translator.set_engine(engine_id, api_key)

        dir_changed = src != self._src_code or tgt != self._tgt_code
        if dir_changed:
            self._src_code = src
            self._tgt_code = tgt
            self._translator.set_direction(src, tgt)

        if dialect != self._dialect:
            self._dialect = dialect
            self._translator.set_dialect(dialect)

        font_changed = (font_family != self._font_family or
                        font_size != self._font_size)
        if font_changed:
            self._font_family = font_family
            self._font_size = font_size
            self._apply_fonts()

        if bg_image != self._bg_image or overlay_opacity != self._overlay_opacity:
            self._bg_image = bg_image
            self._overlay_opacity = overlay_opacity
            self._load_overlay(bg_image, overlay_opacity)

        if button_border_style != self._button_border_style:
            self._button_border_style = button_border_style
            self._apply_button_style()

        if custom_colors != self._custom_colors:
            self._custom_colors = custom_colors.copy()
            if "BG" in custom_colors:
                self.root.configure(bg=custom_colors["BG"])

        save_config({
            "engine": self._engine_id,
            "api_key": self._api_key,
            "source": self._src_code,
            "target": self._tgt_code,
            "native_mode": dialect is not None,
            "dialect": dialect,
            "font_family": self._font_family,
            "font_size": self._font_size,
            "bg_image": self._bg_image,
            "custom_colors": self._custom_colors,
            "overlay_opacity": self._overlay_opacity,
            "button_border_style": self._button_border_style,
        })

        self._refresh_labels()

        if dialect:
            name = DIALECT_LABELS.get(dialect, dialect)
            self._flash(f"Native: {name}")
        if engine_changed:
            eng_name = ENGINE_REGISTRY[self._engine_id].name
            self._flash(f"Engine: {eng_name}")
        if dir_changed:
            self._clear()
        if font_changed:
            self._flash(f"Font: {font_family} {font_size}")

    def _refresh_labels(self):
        src_name = LANG_NAMES.get(self._src_code, self._src_code)
        tgt_name = LANG_NAMES.get(self._tgt_code, self._tgt_code)

        self._lbl_in.config(text=src_name)
        self._lbl_out.config(text=tgt_name)
        self._copy_btn.config(text=f"Copy {tgt_name}")

        eng_name = ENGINE_REGISTRY[self._engine_id].name
        label = f"{eng_name} - {src_name} > {tgt_name}"
        if self._dialect:
            name = DIALECT_LABELS.get(self._dialect, self._dialect)
            label += f" Native: {name}"
        self.root.title(label)

    # ═══════════════════════════════════════════════════════════════════
    #  Translation
    # ═══════════════════════════════════════════════════════════════════

    def _translate(self):
        text = self._input.get("1.0", "end-1c")
        if not text.strip():
            self._set_output("")
            return
        self._status.config(text="Translating...")
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
    #  Actions
    # ═══════════════════════════════════════════════════════════════════

    def _copy(self):
        text = self._output.get("1.0", "end-1c")
        if not text.strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._flash("Copied")

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
