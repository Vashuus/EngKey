"""Settings dialog with Translation and Appearance tabs."""

import os
import tkinter as tk
from tkinter import ttk, font as tkfont, colorchooser, filedialog

from config import BG, SURFACE, FG, ACCENT, MUTED, SUBTEXT


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
from languages import LANG
from native.dialects import has_dialects, get_variants, LABELS
from engines import list_engines
from config_store import DEFAULT

COLOR_KEYS = ["BG", "SURFACE", "FG", "ACCENT", "MUTED", "SUBTEXT"]


class Settings(tk.Toplevel):
    """Modal settings dialog with Translation and Appearance tabs.

    Callback receives a single dict with all settings:
        source, target, dialect, engine, api_key,
        font_family, font_size, bg_image, custom_colors
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
        appearance: dict | None = None,
    ):
        super().__init__(parent)
        self._callback = callback
        self._last_tgt = target_code
        self._engine_id = engine_id
        self._appearance = appearance or {}

        self.title("EngKey - Settings")
        self.configure(bg=BG)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.geometry("420x600")

        # Notebook with tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=6, pady=6)

        # ── Tab 1: Translation ───────────────────────────────────────
        trans_frame = tk.Frame(notebook, bg=SURFACE, padx=14, pady=14)
        notebook.add(trans_frame, text="  Translation  ")
        self._build_translation_tab(trans_frame, source_code, target_code,
                                     dialect, engine_id, api_key)

        # ── Tab 2: Appearance ─────────────────────────────────────────
        appear_frame = tk.Frame(notebook, bg=SURFACE, padx=14, pady=14)
        notebook.add(appear_frame, text="  Appearance  ")
        self._build_appearance_tab(appear_frame)

        # Buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", padx=14, pady=(0, 10))

        tk.Button(btn_frame, text="Apply",
                  font=("Segoe UI", 9, "bold"),
                  bg=ACCENT, fg=BG,
                  relief="flat", padx=16, pady=3, bd=0,
                  cursor="hand2",
                  command=self._apply).pack(side="right", padx=(6, 0))

        tk.Button(btn_frame, text="Cancel",
                  font=("Segoe UI", 9),
                  bg=MUTED, fg=FG,
                  relief="flat", padx=12, pady=3, bd=0,
                  cursor="hand2",
                  command=self.destroy).pack(side="right")

    # ═══════════════════════════════════════════════════════════════════
    #  Translation tab
    # ═══════════════════════════════════════════════════════════════════

    def _build_translation_tab(self, frame, source_code, target_code,
                                dialect, engine_id, api_key):
        codes = [c for _, c in LANG]
        engines = list_engines()

        tk.Label(frame, text="Source language:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        self._src_var = tk.StringVar(value=source_code)
        ttk.Combobox(frame, textvariable=self._src_var,
                      values=codes, state="readonly", width=30).pack(
            fill="x", pady=(0, 8))

        tk.Label(frame, text="Target language:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        self._tgt_var = tk.StringVar(value=target_code)
        tgt_menu = ttk.Combobox(frame, textvariable=self._tgt_var,
                                 values=codes, state="readonly", width=30)
        tgt_menu.pack(fill="x", pady=(0, 10))

        sep = tk.Frame(frame, height=1, bg=MUTED)
        sep.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Translation API:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        engine_names = [f"{n}" for _, n in engines]
        self._eng_var = tk.StringVar(value=self._engine_name(engine_id, engines))
        eng_menu = ttk.Combobox(frame, textvariable=self._eng_var,
                                 values=engine_names, state="readonly", width=30)
        eng_menu.pack(fill="x", pady=(0, 8))
        eng_menu.bind("<<ComboboxSelected>>", self._on_engine_change)

        self._eng_id_map = {n: i for i, n in engines}

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
            show="*",
        )
        self._key_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self._key_toggle_btn = tk.Button(
            key_row,
            text="Show",
            font=("Segoe UI", 9),
            bg=MUTED, fg=FG,
            relief="flat",
            padx=4, pady=1, bd=0,
            cursor="hand2",
            command=self._toggle_key_visibility,
        )
        self._key_toggle_btn.pack(side="right")

        sep2 = tk.Frame(frame, height=1, bg=MUTED)
        sep2.pack(fill="x", pady=(0, 10))

        nat_frame = tk.Frame(frame, bg=SURFACE)
        nat_frame.pack(fill="x", pady=(0, 2))

        self._nat_var = tk.BooleanVar(value=dialect is not None)
        self._nat_cb = tk.Checkbutton(
            nat_frame,
            text="Native Mode",
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

        tk.Label(nat_frame, text="(Experimental)",
                 font=("Segoe UI", 7),
                 fg="#e06c75", bg=SURFACE).pack(side="left", padx=(4, 0))

        dial_frame = tk.Frame(frame, bg=SURFACE)
        dial_frame.pack(fill="x", pady=(0, 10))

        self._dial_label = tk.Label(
            dial_frame,
            text="Dialect:",
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
            width=20,
        )
        self._dial_menu.pack(side="left", padx=(6, 0))

        self._dial_name = tk.Label(
            dial_frame,
            text=LABELS.get(initial_dialect, ""),
            font=("Segoe UI", 8),
            fg=SUBTEXT, bg=SURFACE,
        )
        self._dial_name.pack(side="left", padx=(4, 0))

        self._dial_var.trace_add("write", self._update_dial_name)
        self._tgt_var.trace_add("write", self._on_target_change)

        self._update_dial_visibility()
        self._update_key_visibility()

    # ═══════════════════════════════════════════════════════════════════
    #  Appearance tab
    # ═══════════════════════════════════════════════════════════════════

    def _build_appearance_tab(self, frame):
        # ── Font ─────────────────────────────────────────────────────
        tk.Label(frame, text="Font:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")
        font_row = tk.Frame(frame, bg=SURFACE)
        font_row.pack(fill="x", pady=(0, 10))

        families = sorted(tkfont.families())
        current_family = self._appearance.get("font_family", DEFAULT["font_family"])
        self._font_family_var = tk.StringVar(value=current_family)
        font_menu = ttk.Combobox(
            font_row, textvariable=self._font_family_var,
            values=families, state="readonly", width=22,
        )
        font_menu.pack(side="left", padx=(0, 6))

        current_size = self._appearance.get("font_size", DEFAULT["font_size"])
        self._font_size_var = tk.StringVar(value=str(current_size))
        size_spin = tk.Spinbox(
            font_row, from_=8, to=24,
            textvariable=self._font_size_var,
            font=("Segoe UI", 9),
            width=4,
            bg=BG, fg=FG,
            buttonbackground=MUTED,
            relief="flat", bd=4,
        )
        size_spin.pack(side="left")

        # ── Colors ───────────────────────────────────────────────────
        sep1 = tk.Frame(frame, height=1, bg=MUTED)
        sep1.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Colors:", font=("Segoe UI", 9),
                 fg=SUBTEXT, bg=SURFACE, anchor="w").pack(fill="x")

        self._color_vars: dict[str, tk.StringVar] = {}
        self._color_swatches: dict[str, tk.Canvas] = {}
        custom = self._appearance.get("custom_colors", {})

        colors_frame = tk.Frame(frame, bg=SURFACE)
        colors_frame.pack(fill="x", pady=(0, 6))

        import config as cfg_mod
        for i, key in enumerate(COLOR_KEYS):
            row = tk.Frame(colors_frame, bg=SURFACE)
            row.pack(fill="x", pady=1)

            default_val = getattr(cfg_mod, key, "#000000")
            current_val = custom.get(key, default_val)
            var = tk.StringVar(value=current_val)
            self._color_vars[key] = var

            swatch = tk.Canvas(row, width=18, height=18,
                               bg=current_val, highlightthickness=1,
                               highlightbackground=MUTED, bd=0)
            swatch.pack(side="left", padx=(0, 4))
            self._color_swatches[key] = swatch

            tk.Label(row, text=key, font=("Segoe UI", 9, "bold"),
                     fg=SUBTEXT, bg=SURFACE, width=9, anchor="w").pack(side="left")

            tk.Label(row, textvariable=var, font=("Segoe UI", 8),
                     fg=MUTED, bg=SURFACE, width=10, anchor="w").pack(side="left")

            pick_btn = tk.Button(row, text="Pick",
                                 font=("Segoe UI", 8),
                                 bg=MUTED, fg=FG,
                                 relief="flat", padx=6, pady=0, bd=0,
                                 cursor="hand2",
                                 command=lambda k=key, v=var,
                                        s=self._color_swatches[key]:
                                     self._pick_color(k, v, s))
            pick_btn.pack(side="left", padx=(0, 2))

            reset_btn = tk.Button(row, text="Default",
                                  font=("Segoe UI", 8),
                                  bg=MUTED, fg=FG,
                                  relief="flat", padx=4, pady=0, bd=0,
                                  cursor="hand2",
                                  command=lambda k=key, v=var,
                                         s=self._color_swatches[key],
                                         d=default_val:
                                     self._reset_color(k, v, s, d))
            reset_btn.pack(side="left")

        sep2 = tk.Frame(frame, height=1, bg=MUTED)
        sep2.pack(fill="x", pady=(8, 8))

        current_style = self._appearance.get("button_border_style", "default")
        self._soft_borders_var = tk.BooleanVar(value=(current_style == "soft"))
        tk.Checkbutton(
            frame, text="Soft button borders",
            variable=self._soft_borders_var,
            font=("Segoe UI", 9),
            fg=FG, bg=SURFACE,
            selectcolor=BG,
            activebackground=SURFACE,
            activeforeground=FG,
            cursor="hand2",
        ).pack(anchor="w", pady=(0, 4))

    # ═══════════════════════════════════════════════════════════════════
    #  Color helpers
    # ═══════════════════════════════════════════════════════════════════

    def _pick_color(self, key, var, swatch):
        result = colorchooser.askcolor(
            title=f"Pick {key}", color=var.get(), parent=self)
        if result and result[1]:
            var.set(result[1])
            swatch.configure(bg=result[1])

    def _reset_color(self, key, var, swatch, default):
        var.set(default)
        swatch.configure(bg=default)

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Select background image",
            parent=self,
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self._bg_image_var.set(path)

    def _update_preview(self):
        """Render a thumbnail preview of the overlay as it will appear in the main window."""
        path = self._bg_image_var.get().strip()
        opacity = self._opacity_var.get()

        if not path or not os.path.isfile(path) or opacity <= 0.0:
            self._preview_label.config(
                text="No image selected" if not path else "Image not found",
                image="", fg=MUTED,
            )
            self._preview_frame.configure(bg=BG)
            return

        pw = self._preview_frame.winfo_width() or 360
        ph = self._preview_frame.winfo_height() or 100

        try:
            from PIL import Image, ImageTk
            img = Image.open(path).convert("RGBA")
            img.thumbnail((pw, ph), Image.LANCZOS)

            root_bg_hex = self._appearance.get("custom_colors", {}).get("BG", BG)
            bg_rgb = _hex_to_rgb(root_bg_hex)
            bg_layer = Image.new("RGBA", img.size, bg_rgb + (255,))
            blended = Image.blend(bg_layer, img, opacity)

            photo = ImageTk.PhotoImage(blended.convert("RGB"))
            self._preview_label.config(image=photo, text="", fg=SUBTEXT, bg=BG)
            self._preview_label.image = photo
        except ImportError:
            self._preview_label.config(
                text="Pillow required for preview",
                image="", fg="#e06c75",
            )
        except Exception:
            self._preview_label.config(
                text="Cannot load image",
                image="", fg="#e06c75",
            )

    # ═══════════════════════════════════════════════════════════════════
    #  Translation tab helpers (unchanged)
    # ═══════════════════════════════════════════════════════════════════

    @staticmethod
    def _engine_name(engine_id, engines):
        for i, n in engines:
            if i == engine_id:
                return n
        return engines[0][1] if engines else "Google Translate"

    @staticmethod
    def _get_variant_codes(lang_code):
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
            self._key_label.config(text=f"{cls.key_label}:")
        else:
            self._key_frame.pack_forget()

    def _toggle_key_visibility(self):
        if self._key_entry.cget("show") == "*":
            self._key_entry.config(show="")
            self._key_toggle_btn.config(text="Hide")
        else:
            self._key_entry.config(show="*")
            self._key_toggle_btn.config(text="Show")

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

    # ═══════════════════════════════════════════════════════════════════
    #  Apply
    # ═══════════════════════════════════════════════════════════════════

    def _apply(self):
        src = self._src_var.get()
        tgt = self._tgt_var.get()
        dialect = None
        if self._nat_var.get():
            variants = self._get_variant_codes(tgt)
            if variants:
                dialect = self._dial_var.get()

        eng_name = self._eng_var.get()
        engine_id = self._eng_id_map.get(eng_name, "google")
        api_key = self._key_var.get()

        custom_colors = {}
        for key in COLOR_KEYS:
            val = self._color_vars[key].get()
            import config as cfg_mod
            default_val = getattr(cfg_mod, key, None)
            if val != default_val:
                custom_colors[key] = val

        font_size_str = self._font_size_var.get().strip()
        try:
            font_size = int(font_size_str)
        except ValueError:
            font_size = DEFAULT["font_size"]

        bg_image = self._appearance.get("bg_image", DEFAULT["bg_image"])
        overlay_opacity = self._appearance.get("overlay_opacity", DEFAULT["overlay_opacity"])

        button_border_style = "soft" if self._soft_borders_var.get() else "default"

        cfg = {
            "source": src,
            "target": tgt,
            "dialect": dialect,
            "engine": engine_id,
            "api_key": api_key,
            "font_family": self._font_family_var.get(),
            "font_size": font_size,
            "bg_image": bg_image,
            "custom_colors": custom_colors,
            "overlay_opacity": overlay_opacity,
            "button_border_style": button_border_style,
        }

        self._callback(cfg)
        self.destroy()
