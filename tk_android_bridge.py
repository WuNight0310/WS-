# -*- coding: utf-8 -*-
"""
tk_android_bridge.py
====================
Pure-Python Cross-Platform & Android Rendering Bridge for main.py (1600x950).
Provides a 100% compatible drop-in implementation of:
  - tkinter (tk)
  - tkinter.ttk (ttk)
  - tkinter.scrolledtext (scrolledtext)
  - tkinter.filedialog (filedialog)
  - tkinter.messagebox (messagebox)
  - PIL.ImageTk (ImageTk)

Supports:
  - Full pack(), place(), and grid() geometry managers with lookahead cavity layout
  - Re-entrant event loop: after(), after_cancel(), update_idletasks(), update(), wait_variable()
  - Complete Canvas API: create_image, create_rectangle, create_oval, create_line, create_text,
    create_window, coords, itemconfig, delete, bbox, xview_scroll, yview_scroll, yview_moveto
  - Full PIL 1600x950 software compositor (for VM testing & Kivy OpenGL texture streaming on Android)
"""

import os
import sys
import time
import math
import threading
from PIL import Image, ImageDraw, ImageFont

# Pillow < 9.1.0 (e.g. p4a Pillow 8.4.0 on Android) compatibility shims
if not hasattr(Image, "Resampling"):
    class _PillowResamplingShim:
        NEAREST = getattr(Image, "NEAREST", 0)
        BOX = getattr(Image, "BOX", 4)
        BILINEAR = getattr(Image, "BILINEAR", 2)
        HAMMING = getattr(Image, "HAMMING", 5)
        BICUBIC = getattr(Image, "BICUBIC", 3)
        LANCZOS = getattr(Image, "LANCZOS", getattr(Image, "ANTIALIAS", 1))
    Image.Resampling = _PillowResamplingShim

if not hasattr(Image, "Transpose"):
    class _PillowTransposeShim:
        FLIP_LEFT_RIGHT = getattr(Image, "FLIP_LEFT_RIGHT", 0)
        FLIP_TOP_BOTTOM = getattr(Image, "FLIP_TOP_BOTTOM", 1)
        ROTATE_90 = getattr(Image, "ROTATE_90", 2)
        ROTATE_180 = getattr(Image, "ROTATE_180", 3)
        ROTATE_270 = getattr(Image, "ROTATE_270", 4)
        TRANSPOSE = getattr(Image, "TRANSPOSE", 5)
        TRANSVERSE = getattr(Image, "TRANSVERSE", 6)
    Image.Transpose = _PillowTransposeShim

# ==========================================
# Tkinter Constants
# ==========================================
TOP = "top"
BOTTOM = "bottom"
LEFT = "left"
RIGHT = "right"
CENTER = "center"

N = "n"
S = "s"
E = "e"
W = "w"
NW = "nw"
NE = "ne"
SW = "sw"
SE = "se"

BOTH = "both"
X = "x"
Y = "y"
NONE = "none"

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

NORMAL = "normal"
DISABLED = "disabled"
ACTIVE = "active"
HIDDEN = "hidden"

END = "end"
INSERT = "insert"
CURRENT = "current"

WORD = "word"
CHAR = "char"

FLAT = "flat"
RAISED = "raised"
SUNKEN = "sunken"
GROOVE = "groove"
RIDGE = "ridge"
SOLID = "solid"

SINGLE = "single"
BROWSE = "browse"
MULTIPLE = "multiple"
EXTENDED = "extended"

# ==========================================
# Font Loader & Text Measurement Cache
# ==========================================
_FONT_CACHE = {}
_TEXT_SIZE_CACHE = {}
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CJK_FONT_PATHS = [
    os.path.join(_BASE_DIR, "ws_font.ttf"),
    os.path.join(_BASE_DIR, "ws_font.ttc"),
    # Android system CJK fonts
    "/system/fonts/NotoSansCJK-Bold.ttc",
    "/system/fonts/NotoSansCJK-Regular.ttc",
    "/system/fonts/NotoSansTC-Bold.otf",
    "/system/fonts/NotoSansTC-Regular.otf",
    "/system/fonts/NotoSansSC-Regular.otf",
    "/system/fonts/DroidSansFallback.ttf",
    # Linux / VM CJK fonts
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    # Windows fonts
    "C:/Windows/Fonts/msjhbd.ttc",
    "C:/Windows/Fonts/msjh.ttc",
    "msjhbd.ttc",
    "msjh.ttc",
]
if os.path.isdir("/system/fonts"):
    try:
        for _fn in sorted(os.listdir("/system/fonts")):
            if any(k in _fn for k in ("CJK", "TC", "SC", "Fallback", "DroidSans")):
                _fp = os.path.join("/system/fonts", _fn)
                if _fp not in _CJK_FONT_PATHS:
                    _CJK_FONT_PATHS.append(_fp)
    except Exception:
        pass


def get_pil_font(font_spec):
    if not font_spec:
        size = 11
        bold = False
    elif isinstance(font_spec, (tuple, list)):
        size = int(font_spec[1]) if len(font_spec) > 1 else 11
        bold = any("bold" in str(x).lower() for x in font_spec[2:])
    elif isinstance(font_spec, int):
        size = font_spec
        bold = False
    else:
        size = 11
        bold = False

    # Convert Tk point size to pixel size (1pt ~= 1.25px on 96dpi, keep compact so 1600x950 fits cleanly)
    px_size = max(9, int(round(size * 1.18)))
    key = (px_size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    fallback_f = None
    for p in _CJK_FONT_PATHS:
        if os.path.exists(p):
            try:
                f = ImageFont.truetype(p, px_size)
                if fallback_f is None:
                    fallback_f = f
                # Verify font has BOTH ASCII ("A", "0") AND CJK ("卡") glyphs (rejects DroidSansFallbackFull.ttf)
                notdef = list(f.getmask("\ufffd"))
                if (
                    list(f.getmask("A")) != notdef
                    and list(f.getmask("0")) != notdef
                    and list(f.getmask("卡")) != notdef
                ):
                    _FONT_CACHE[key] = f
                    return f
            except Exception:
                pass
    if fallback_f is not None:
        _FONT_CACHE[key] = fallback_f
        return fallback_f
    f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


_EMOJI_MAP = {
    "⚔️": "★",
    "⚔": "★",
    "🛡️": "◆",
    "🛡": "◆",
    "🎴": "◆",
    "🃏": "◆",
    "📋": "■",
    "🏠": "▲",
    "🌐": "●",
    "✨": "★",
    "🌟": "★",
    "👑": "★",
    "🔥": "◆",
    "⚡": "★",
    "🔄": "▶",
    "↻": "▶",
    "↺": "◀",
    "⏰": "●",
    "⏱": "●",
    "⏳": "…",
    "💡": "●",
    "👁️": "●",
    "👁": "●",
    "🔙": "◀",
    "➕": "+",
    "✏️": "※",
    "✏": "※",
    "✎": "※",
    "🗑️": "×",
    "🗑": "×",
    "✖": "×",
    "❌": "×",
    "✔": "✓",
    "✅": "✓",
    "☑": "■",
    "☐": "□",
    "➔": "→",
    "⏩": "▶▶",
    "⚙": "◆",
    "⌨": "■",
    "💾": "■",
    "🧹": "◀",
    "🤖": "◆",
    "🎯": "◎",
    "🎉": "★",
    "🏆": "★",
    "💀": "×",
}


def sanitize_cjk_text(text: str) -> str:
    if not text:
        return ""
    s = str(text)
    for k, v in _EMOJI_MAP.items():
        if k in s:
            s = s.replace(k, v)
    # Strip remaining supplementary plane emojis / variation selectors not in CJK font
    out = []
    for ch in s:
        code = ord(ch)
        if code in (0xFE0E, 0xFE0F, 0x200D):
            continue
        if code > 0xFFFF:
            continue
        out.append(ch)
    return "".join(out)


def measure_text_block(text: str, font_spec, wraplength: int = 0):
    text = sanitize_cjk_text(text)
    if not text:
        return (0, 0, [])
    cache_key = (text, str(font_spec), int(wraplength or 0))
    if cache_key in _TEXT_SIZE_CACHE:
        return _TEXT_SIZE_CACHE[cache_key]

    pil_font = get_pil_font(font_spec)
    raw_lines = text.split("\n")
    wrapped_lines = []

    for rline in raw_lines:
        if not rline:
            wrapped_lines.append("")
            continue
        if wraplength and wraplength > 20:
            cur = ""
            for ch in rline:
                test = cur + ch
                try:
                    bbox = pil_font.getbbox(test)
                    w = bbox[2] - bbox[0]
                except Exception:
                    w = len(test) * 12
                if w > wraplength and cur:
                    wrapped_lines.append(cur)
                    cur = ch
                else:
                    cur = test
            if cur:
                wrapped_lines.append(cur)
        else:
            wrapped_lines.append(rline)

    max_w = 0
    try:
        sample_bbox = pil_font.getbbox("測試Ag")
        line_h = max(12, (sample_bbox[3] - sample_bbox[1]) + 4)
    except Exception:
        line_h = 16

    for wl in wrapped_lines:
        if not wl:
            continue
        try:
            bbox = pil_font.getbbox(wl)
            lw = bbox[2] - bbox[0]
        except Exception:
            lw = len(wl) * 12
        if lw > max_w:
            max_w = lw

    total_h = max(line_h, len(wrapped_lines) * line_h)
    res = (max_w, total_h, wrapped_lines)
    if len(_TEXT_SIZE_CACHE) > 8000:
        _TEXT_SIZE_CACHE.clear()
    _TEXT_SIZE_CACHE[cache_key] = res
    return res


def _parse_pad(val):
    """Parse Tk padx/pady (either int or 2-tuple) into (pad_start, pad_end)."""
    if val is None:
        return (0, 0)
    if isinstance(val, (tuple, list)):
        if len(val) >= 2:
            return (int(val[0]), int(val[1]))
        elif len(val) == 1:
            return (int(val[0]), int(val[0]))
        return (0, 0)
    try:
        v = int(float(val))
        return (v, v)
    except Exception:
        return (0, 0)


# ==========================================
# ImageTk.PhotoImage Drop-In
# ==========================================
class PhotoImage:
    def __init__(self, image=None, file=None, **kw):
        if image is not None and isinstance(image, Image.Image):
            self._pil = image.convert("RGBA")
        elif file is not None and os.path.exists(file):
            self._pil = Image.open(file).convert("RGBA")
        else:
            self._pil = Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    def width(self):
        return self._pil.width

    def height(self):
        return self._pil.height


class ImageTkModule:
    PhotoImage = PhotoImage


ImageTk = ImageTkModule()


# ==========================================
# Variable Classes (StringVar, IntVar, etc.)
# ==========================================
class Variable:
    def __init__(self, master=None, value=None, name=None):
        self._value = value
        self._traces = []
        self._cond = threading.Condition()

    def set(self, value):
        with self._cond:
            self._value = value
            self._cond.notify_all()
        for mode, cb in list(self._traces):
            try:
                cb("", "", mode)
            except TypeError:
                try:
                    cb()
                except Exception:
                    pass
            except Exception:
                pass

    def get(self):
        return self._value

    def trace_add(self, mode, callback):
        self._traces.append((mode, callback))
        return str(len(self._traces))

    def trace(self, mode, callback):
        return self.trace_add(mode, callback)


class StringVar(Variable):
    def __init__(self, master=None, value="", name=None):
        super().__init__(master, str(value if value is not None else ""), name)

    def get(self):
        return str(self._value if self._value is not None else "")


class IntVar(Variable):
    def __init__(self, master=None, value=0, name=None):
        super().__init__(master, int(value if value is not None else 0), name)

    def get(self):
        try:
            return int(self._value)
        except Exception:
            return 0


class DoubleVar(Variable):
    def __init__(self, master=None, value=0.0, name=None):
        super().__init__(master, float(value if value is not None else 0.0), name)

    def get(self):
        try:
            return float(self._value)
        except Exception:
            return 0.0


class BooleanVar(Variable):
    def __init__(self, master=None, value=False, name=None):
        super().__init__(master, bool(value), name)

    def get(self):
        return bool(self._value)


# ==========================================
# Event Object
# ==========================================
class Event:
    def __init__(self, widget=None, x=0, y=0, x_root=0, y_root=0, delta=0, keysym="", char="", num=1):
        self.widget = widget
        self.x = int(x)
        self.y = int(y)
        self.x_root = int(x_root)
        self.y_root = int(y_root)
        self.delta = int(delta)
        self.keysym = keysym
        self.char = char
        self.num = num
        self.width = widget._w if widget else 0
        self.height = widget._h if widget else 0


# ==========================================
# Base Widget & Geometry Engine
# ==========================================
class Widget:
    _next_id = 1

    def __init__(self, master=None, **kw):
        self.master = master
        self._id = Widget._next_id
        Widget._next_id += 1
        self._children = []
        self._exists = True
        self._mapped = False
        self._geom_mgr = None  # "pack", "place", "grid"
        self._geom_opts = {}
        self._pack_propagate = True
        self._grid_propagate = True
        self._grid_col_weights = {}
        self._grid_row_weights = {}
        self._bindings = {}

        # Computed geometry relative to root and parent
        self._x = 0
        self._y = 0
        self._w = 1
        self._h = 1
        self._rootx = 0
        self._rooty = 0
        self._reqw = 1
        self._reqh = 1
        self._last_cfg_size = (0, 0)

        # Default options
        self._opts = {
            "bg": "#151b29",
            "fg": "#ffffff",
            "font": ("Microsoft JhengHei", 11),
            "text": "",
            "image": None,
            "compound": NONE,
            "width": None,
            "height": None,
            "padx": 0,
            "pady": 0,
            "bd": 0,
            "relief": FLAT,
            "highlightthickness": 0,
            "highlightbackground": "#2b3348",
            "highlightcolor": "#ffd166",
            "anchor": CENTER,
            "justify": CENTER,
            "wraplength": 0,
            "state": NORMAL,
            "command": None,
            "cursor": "",
            "textvariable": None,
            "variable": None,
            "values": [],
            "from_": 0,
            "to": 100,
            "resolution": 1,
            "orient": HORIZONTAL,
            "yscrollcommand": None,
            "xscrollcommand": None,
            "activebackground": None,
            "activeforeground": None,
            "disabledforeground": "#8890a8",
            "selectbackground": "#118ab2",
            "selectforeground": "#ffffff",
        }
        if master is not None and hasattr(master, "_opts"):
            # Default Frame/Label bg inherits or defaults cleanly
            pass
        self.configure(**kw)
        if master is not None and hasattr(master, "_children"):
            master._children.append(self)

    @property
    def _root(self):
        cur = self
        while cur.master is not None:
            cur = cur.master
        return cur

    def winfo_class(self):
        cls_name = self.__class__.__name__
        if cls_name == "Combobox":
            return "TCombobox"
        if cls_name == "ScrolledText":
            return "Text"
        return cls_name

    def winfo_exists(self):
        return bool(self._exists)

    def winfo_ismapped(self):
        if not self._exists:
            return False
        if isinstance(self, (Tk, Toplevel)):
            return True
        if self._geom_mgr is None:
            # Check if embedded via Canvas create_window
            if isinstance(self.master, Canvas):
                for item in self.master._items.values():
                    if item.get("type") == "window" and item.get("window") is self:
                        return self.master.winfo_ismapped()
            return False
        if self.master is not None:
            return self.master.winfo_ismapped()
        return self._mapped

    def winfo_children(self):
        return [c for c in self._children if c._exists]

    def winfo_width(self):
        return max(1, int(self._w))

    def winfo_height(self):
        return max(1, int(self._h))

    def winfo_reqwidth(self):
        return max(1, int(self._reqw))

    def winfo_reqheight(self):
        return max(1, int(self._reqh))

    def winfo_rootx(self):
        return int(self._rootx)

    def winfo_rooty(self):
        return int(self._rooty)

    def winfo_x(self):
        return int(self._x)

    def winfo_y(self):
        return int(self._y)

    def configure(self, cnf=None, **kw):
        if isinstance(cnf, dict):
            kw.update(cnf)
        for k, v in kw.items():
            if k == "background":
                k = "bg"
            elif k == "foreground":
                k = "fg"
            elif k == "borderwidth":
                k = "bd"
            self._opts[k] = v
            if k == "textvariable" and isinstance(v, Variable):
                v.trace_add("write", lambda *a: self._on_textvar_change())
        root = self._root
        if hasattr(root, "_dirty"):
            root._dirty = True

    config = configure

    def _on_textvar_change(self):
        root = self._root
        if hasattr(root, "_dirty"):
            root._dirty = True

    def cget(self, key):
        if key == "background":
            key = "bg"
        elif key == "foreground":
            key = "fg"
        elif key == "borderwidth":
            key = "bd"
        if key == "text" and self._opts.get("textvariable") is not None:
            return self._opts["textvariable"].get()
        return self._opts.get(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    # Geometry Managers
    def pack(self, **kw):
        self._geom_mgr = "pack"
        opts = {
            "side": TOP,
            "fill": NONE,
            "expand": False,
            "padx": 0,
            "pady": 0,
            "ipadx": 0,
            "ipady": 0,
            "anchor": CENTER,
        }
        opts.update(kw)
        self._geom_opts = opts
        self._mapped = True
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def pack_forget(self):
        if self._geom_mgr == "pack":
            self._geom_mgr = None
            self._mapped = False
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    def pack_propagate(self, flag=True):
        self._pack_propagate = bool(flag)

    def place(self, **kw):
        was_placed = (self._geom_mgr == "place" and self._mapped)
        self._geom_mgr = "place"
        if not hasattr(self, "_place_opts"):
            self._place_opts = {}
        self._place_opts.update(kw)
        self._geom_opts = dict(self._place_opts)
        self._mapped = True
        root = self._root
        if hasattr(root, "_dirty"):
            txt_val = str(self._opts.get("text") or "")
            if was_placed and txt_val.startswith("拖移：") and "x" in kw and "y" in kw and self.master is not None:
                self._x = int(float(kw["x"]))
                self._y = int(float(kw["y"]))
                self._rootx = self.master._rootx + self._x
                self._rooty = self.master._rooty + self._y
                root._ghost_widget = self
                root._ghost_only_dirty = True
            else:
                root._dirty = True
                root._bg_without_ghost_pil = None

    def place_forget(self):
        if self._geom_mgr == "place":
            self._geom_mgr = None
            self._place_opts = {}
            self._mapped = False
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    def grid(self, **kw):
        self._geom_mgr = "grid"
        opts = {
            "row": 0,
            "column": 0,
            "rowspan": 1,
            "columnspan": 1,
            "padx": 0,
            "pady": 0,
            "ipadx": 0,
            "ipady": 0,
            "sticky": "",
        }
        opts.update(kw)
        self._geom_opts = opts
        self._mapped = True
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def grid_forget(self):
        if self._geom_mgr == "grid":
            self._geom_mgr = None
            self._mapped = False
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    def grid_columnconfigure(self, index, **kw):
        if "weight" in kw:
            self._grid_col_weights[int(index)] = int(kw["weight"])

    def grid_rowconfigure(self, index, **kw):
        if "weight" in kw:
            self._grid_row_weights[int(index)] = int(kw["weight"])

    def lift(self, aboveThis=None):
        if self.master and self in self.master._children:
            self.master._children.remove(self)
            self.master._children.append(self)
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    def lower(self, belowThis=None):
        if self.master and self in self.master._children:
            self.master._children.remove(self)
            self.master._children.insert(0, self)
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    def destroy(self):
        self._exists = False
        self._mapped = False
        self._geom_mgr = None
        for c in list(self._children):
            c.destroy()
        self._children.clear()
        if self.master and self in self.master._children:
            self.master._children.remove(self)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def bind(self, sequence, func, add=None):
        if add == "+" and sequence in self._bindings:
            self._bindings[sequence].append(func)
        else:
            self._bindings[sequence] = [func]

    def bind_all(self, sequence, func, add=None):
        root = self._root
        if hasattr(root, "_global_bindings"):
            if add == "+" and sequence in root._global_bindings:
                root._global_bindings[sequence].append(func)
            else:
                root._global_bindings[sequence] = [func]

    def _fire_event(self, sequence, event=None):
        if not self._exists:
            return
        if event is None:
            event = Event(widget=self)
        for fn in list(self._bindings.get(sequence, [])):
            try:
                fn(event)
            except Exception as e:
                pass

    def focus_set(self):
        root = self._root
        if hasattr(root, "_focused_widget"):
            root._focused_widget = self

    def grab_set(self):
        pass

    def after(self, ms, func=None, *args):
        return self._root.after(ms, func, *args)

    def after_cancel(self, ident):
        return self._root.after_cancel(ident)

    def update_idletasks(self):
        return self._root.update_idletasks()

    def update(self):
        return self._root.update()

    def wait_variable(self, var):
        return self._root.wait_variable(var)


# ==========================================
# Concrete Widget Classes
# ==========================================
class Frame(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


class LabelFrame(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


class Label(Widget):
    def __init__(self, master=None, **kw):
        if "anchor" not in kw:
            kw["anchor"] = CENTER
        super().__init__(master, **kw)


class Button(Widget):
    def __init__(self, master=None, **kw):
        if "relief" not in kw:
            kw["relief"] = RAISED
        if "bd" not in kw and "borderwidth" not in kw:
            kw["bd"] = 2
        if "padx" not in kw:
            kw["padx"] = 8
        if "pady" not in kw:
            kw["pady"] = 4
        super().__init__(master, **kw)

    def invoke(self):
        if self.cget("state") == DISABLED:
            return
        cmd = self.cget("command")
        if callable(cmd):
            cmd()


class Checkbutton(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def invoke(self):
        if self.cget("state") == DISABLED:
            return
        var = self.cget("variable")
        if isinstance(var, Variable):
            var.set(not bool(var.get()))
        cmd = self.cget("command")
        if callable(cmd):
            cmd()


class Entry(Widget):
    def __init__(self, master=None, **kw):
        if "bg" not in kw and "background" not in kw:
            kw["bg"] = "#0d111a"
        if "fg" not in kw and "foreground" not in kw:
            kw["fg"] = "#ffffff"
        super().__init__(master, **kw)
        self._text_buf = ""
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            self._text_buf = str(tv.get())

    def get(self):
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            return str(tv.get())
        return self._text_buf

    def insert(self, index, string):
        s = str(string)
        cur = self.get()
        if index == END or index == "end":
            new_s = cur + s
        else:
            try:
                idx = int(index)
                new_s = cur[:idx] + s + cur[idx:]
            except Exception:
                new_s = cur + s
        self._text_buf = new_s
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            tv.set(new_s)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def delete(self, first, last=None):
        cur = self.get()
        if first == 0 and (last == END or last == "end"):
            new_s = ""
        else:
            new_s = ""
        self._text_buf = new_s
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            tv.set(new_s)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def select_range(self, start, end):
        pass


class Spinbox(Entry):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


class Text(Widget):
    def __init__(self, master=None, **kw):
        if "anchor" not in kw:
            kw["anchor"] = NW
        if "justify" not in kw:
            kw["justify"] = LEFT
        super().__init__(master, **kw)
        self._content = ""
        self._scroll_y = 0

    def get(self, index1="1.0", index2=END):
        return self._content

    def insert(self, index, chars, *tags):
        s = str(chars)
        if index in (END, "end"):
            self._content += s
        else:
            self._content = s + self._content
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def delete(self, index1, index2=None):
        self._content = ""
        self._scroll_y = 0
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def see(self, index):
        if index in (END, "end"):
            self._scroll_y = 999999
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def yview(self, *args):
        pass

    def yview_scroll(self, number, what):
        self._scroll_y = max(0, self._scroll_y + int(number) * 24)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True


class ScrolledText(Text):
    pass


class Listbox(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._items = []
        self._selected = []
        self._scroll_idx = 0

    def insert(self, index, *elements):
        for el in elements:
            if index in (END, "end"):
                self._items.append(str(el))
            else:
                try:
                    self._items.insert(int(index), str(el))
                except Exception:
                    self._items.append(str(el))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def delete(self, first, last=None):
        if first == 0 and last in (END, "end"):
            self._items.clear()
            self._selected.clear()
            self._scroll_idx = 0
        elif last is None:
            try:
                self._items.pop(int(first))
            except Exception:
                pass
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def curselection(self):
        return tuple(self._selected)

    def selection_clear(self, first, last=None):
        self._selected.clear()

    def selection_set(self, first, last=None):
        try:
            idx = int(first)
            if 0 <= idx < len(self._items):
                self._selected = [idx]
        except Exception:
            pass

    def get(self, first, last=None):
        try:
            return self._items[int(first)]
        except Exception:
            return ""

    def size(self):
        return len(self._items)

    def yview(self, *args):
        pass

    def yview_scroll(self, number, what):
        self._scroll_idx = max(0, min(max(0, len(self._items) - 1), self._scroll_idx + int(number)))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True


class Scrollbar(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def set(self, first, last):
        pass


class Scale(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._val = float(kw.get("from_", 0))

    def get(self):
        var = self.cget("variable")
        if isinstance(var, Variable):
            return var.get()
        res = float(self.cget("resolution") or 1)
        if res >= 1 and float(res).is_integer():
            return int(round(self._val))
        return round(self._val, 2)

    def set(self, value):
        try:
            v = float(value)
        except Exception:
            v = 0.0
        lo = float(self.cget("from_") or 0)
        hi = float(self.cget("to") or 100)
        if lo > hi:
            lo, hi = hi, lo
        self._val = max(lo, min(hi, v))
        var = self.cget("variable")
        if isinstance(var, Variable):
            var.set(self.get())
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True


class Combobox(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._val = ""
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            self._val = str(tv.get())

    def get(self):
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            return str(tv.get())
        return self._val

    def set(self, value):
        self._val = str(value)
        tv = self.cget("textvariable")
        if isinstance(tv, Variable):
            tv.set(self._val)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def current(self, newindex=None):
        vals = list(self.cget("values") or [])
        if newindex is not None and 0 <= int(newindex) < len(vals):
            self.set(vals[int(newindex)])
        cur = self.get()
        return vals.index(cur) if cur in vals else -1


class OptionMenu(Combobox):
    def __init__(self, master, variable, value, *values, **kw):
        all_vals = [value] + list(values)
        super().__init__(master, textvariable=variable, values=all_vals, **kw)
        if isinstance(variable, Variable) and not variable.get():
            variable.set(value)


# ==========================================
# Canvas Implementation
# ==========================================
class Canvas(Widget):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._items = {}
        self._item_order = []
        self._next_item_id = 1
        self._scroll_x = 0.0
        self._scroll_y = 0.0
        self._scrollregion = None

    def _add_item(self, item_dict):
        cid = self._next_item_id
        self._next_item_id += 1
        self._items[cid] = item_dict
        self._item_order.append(cid)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True
        return cid

    def create_image(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]
        return self._add_item({
            "type": "image",
            "coords": [float(x), float(y)],
            "image": kw.get("image"),
            "anchor": kw.get("anchor", CENTER),
            "tags": kw.get("tags", ()),
        })

    def create_rectangle(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
             coords = [float(v) for v in args[0]]
        else:
            coords = [float(v) for v in args[:4]]
        return self._add_item({
            "type": "rectangle",
            "coords": coords,
            "fill": kw.get("fill", ""),
            "outline": kw.get("outline", "#ffffff"),
            "width": int(kw.get("width", 1)),
            "tags": kw.get("tags", ()),
        })

    def create_oval(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            coords = [float(v) for v in args[0]]
        else:
            coords = [float(v) for v in args[:4]]
        return self._add_item({
            "type": "oval",
            "coords": coords,
            "fill": kw.get("fill", ""),
            "outline": kw.get("outline", "#ffffff"),
            "width": int(kw.get("width", 1)),
            "tags": kw.get("tags", ()),
        })

    def create_line(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            coords = [float(v) for v in args[0]]
        else:
            coords = [float(v) for v in args]
        return self._add_item({
            "type": "line",
            "coords": coords,
            "fill": kw.get("fill", "#ffffff"),
            "width": int(kw.get("width", 1)),
            "tags": kw.get("tags", ()),
        })

    def create_text(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]
        return self._add_item({
            "type": "text",
            "coords": [float(x), float(y)],
            "text": str(kw.get("text", "")),
            "fill": kw.get("fill", "#ffffff"),
            "font": kw.get("font", ("Microsoft JhengHei", 11)),
            "anchor": kw.get("anchor", CENTER),
            "width": int(kw.get("width", 0)),
            "tags": kw.get("tags", ()),
        })

    def create_window(self, *args, **kw):
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]
        win = kw.get("window")
        if win is not None:
            win._mapped = True
        return self._add_item({
            "type": "window",
            "coords": [float(x), float(y)],
            "window": win,
            "anchor": kw.get("anchor", NW),
            "width": kw.get("width"),
            "height": kw.get("height"),
            "tags": kw.get("tags", ()),
        })

    def coords(self, item_id, *new_coords):
        if item_id in self._items:
            if new_coords:
                if len(new_coords) == 1 and isinstance(new_coords[0], (tuple, list)):
                    self._items[item_id]["coords"] = [float(v) for v in new_coords[0]]
                else:
                    self._items[item_id]["coords"] = [float(v) for v in new_coords]
                if hasattr(self._root, "_dirty"):
                    self._root._dirty = True
            return self._items[item_id]["coords"]
        return []

    def itemconfig(self, item_id, **kw):
        if item_id in self._items:
            self._items[item_id].update(kw)
            if hasattr(self._root, "_dirty"):
                self._root._dirty = True

    itemconfigure = itemconfig

    def delete(self, tag_or_id):
        if tag_or_id == "all":
            self._items.clear()
            self._item_order.clear()
        elif tag_or_id in self._items:
            self._items.pop(tag_or_id, None)
            if tag_or_id in self._item_order:
                self._item_order.remove(tag_or_id)
        else:
            to_del = [
                cid for cid, it in self._items.items()
                if tag_or_id == it.get("tags") or (isinstance(it.get("tags"), (tuple, list)) and tag_or_id in it.get("tags"))
            ]
            for cid in to_del:
                self._items.pop(cid, None)
                if cid in self._item_order:
                    self._item_order.remove(cid)
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def bbox(self, tag_or_id="all"):
        max_x, max_y = self._w, self._h
        for cid in self._item_order:
            it = self._items[cid]
            if it["type"] == "window" and it.get("window") is not None:
                win = it["window"]
                max_x = max(max_x, int(it["coords"][0]) + win._reqw)
                max_y = max(max_y, int(it["coords"][1]) + win._reqh)
            elif it["coords"]:
                xs = it["coords"][0::2]
                ys = it["coords"][1::2]
                if xs:
                    max_x = max(max_x, int(max(xs)) + 40)
                if ys:
                    max_y = max(max_y, int(max(ys)) + 40)
        return (0, 0, max_x, max_y)

    def xview(self, *args):
        if not args:
            return (0.0, 1.0)
        if args[0] == "moveto":
            self.xview_moveto(float(args[1]))
        elif args[0] == "scroll":
            self.xview_scroll(int(args[1]), args[2] if len(args) > 2 else "units")

    def yview(self, *args):
        if not args:
            return (0.0, 1.0)
        if args[0] == "moveto":
            self.yview_moveto(float(args[1]))
        elif args[0] == "scroll":
            self.yview_scroll(int(args[1]), args[2] if len(args) > 2 else "units")

    def xview_moveto(self, fraction):
        bbox = self.bbox("all")
        total_w = max(self._w, bbox[2] - bbox[0])
        self._scroll_x = max(0.0, min(float(total_w - self._w), float(fraction) * total_w))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def yview_moveto(self, fraction):
        bbox = self.bbox("all")
        total_h = max(self._h, bbox[3] - bbox[1])
        self._scroll_y = max(0.0, min(float(total_h - self._h), float(fraction) * total_h))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def xview_scroll(self, number, what="units"):
        bbox = self.bbox("all")
        total_w = max(self._w, bbox[2] - bbox[0])
        self._scroll_x = max(0.0, min(float(total_w - self._w), self._scroll_x + int(number) * 48.0))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True

    def yview_scroll(self, number, what="units"):
        bbox = self.bbox("all")
        total_h = max(self._h, bbox[3] - bbox[1])
        self._scroll_y = max(0.0, min(float(total_h - self._h), self._scroll_y + int(number) * 48.0))
        if hasattr(self._root, "_dirty"):
            self._root._dirty = True


# ==========================================
# Root Window (Tk) & Toplevel
# ==========================================
class Toplevel(Frame):
    def __init__(self, master=None, **kw):
        root = master._root if master is not None else None
        super().__init__(root, **kw)
        self._title = "視窗"
        self._w = 500
        self._h = 320
        # Place Toplevel centered on root
        self.place(relx=0.5, rely=0.5, anchor="center", width=500, height=320)
        self.lift()

    def title(self, text=None):
        if text is not None:
            self._title = str(text)
        return self._title

    def geometry(self, geom_str=None):
        if geom_str:
            try:
                size_part = geom_str.split("+")[0]
                w_s, h_s = size_part.lower().split("x")
                self._w = int(w_s)
                self._h = int(h_s)
                self.place(relx=0.5, rely=0.5, anchor="center", width=self._w, height=self._h)
                self.lift()
            except Exception:
                pass
        return f"{self._w}x{self._h}"

    def transient(self, master=None):
        pass

    def resizable(self, w=True, h=True):
        pass

    def protocol(self, name, func):
        pass


class Tk(Frame):
    _active_instance = None

    def __init__(self, **kw):
        super().__init__(None, **kw)
        Tk._active_instance = self
        self._title = "Weiß Schwarz"
        self._portrait_mode = (os.environ.get("WS_PORTRAIT") == "1")
        self._target_w = 1000 if self._portrait_mode else 1600
        self._target_h = 1340 if self._portrait_mode else 950
        self._w = self._target_w
        self._h = self._target_h
        self._reqw = self._w
        self._reqh = self._h
        self._x = 0
        self._y = 0
        self._rootx = 0
        self._rooty = 0
        self._mapped = True
        self._dirty = True
        self._ghost_only_dirty = False
        self._ghost_widget = None
        self._bg_without_ghost_pil = None
        self._pending_move_xy = None
        self._running = True
        self._timers = {}
        self._next_timer_id = 1
        self._timer_lock = threading.Lock()
        self._event_queue = []
        self._event_cond = threading.Condition()
        self._global_bindings = {}
        self._focused_widget = None
        self._active_dropdown = None  # (combobox_widget, rect_list)
        self._drag_widget = None
        self._last_frame_pil = None

    def title(self, text=None):
        if text is not None:
            self._title = str(text)
        return self._title

    def set_adaptive_surface_size(self, target_w: int, target_h: int, portrait: bool = False):
        target_w = max(800, int(target_w))
        target_h = max(600, int(target_h))
        if (self._target_w, self._target_h, self._portrait_mode) != (target_w, target_h, bool(portrait)):
            self._portrait_mode = bool(portrait)
            self._target_w = target_w
            self._target_h = target_h
            self._w = target_w
            self._h = target_h
            self._reqw = target_w
            self._reqh = target_h
            self._bg_without_ghost_pil = None
            self._dirty = True

    def set_orientation_mode(self, portrait: bool, manual: bool = False):
        portrait = bool(portrait)
        if getattr(self, "_portrait_mode", False) != portrait:
            tw = 1000 if portrait else max(1600, self._target_w)
            th = 1340 if portrait else 950
            self.set_adaptive_surface_size(tw, th, portrait=portrait)

    def geometry(self, geom_str=None):
        if geom_str and not getattr(self, "_portrait_mode", False):
            try:
                size_part = geom_str.split("+")[0]
                w_s, h_s = size_part.lower().split("x")
                self._w = int(w_s)
                self._h = int(h_s)
                self._reqw = self._w
                self._reqh = self._h
            except Exception:
                pass
        return f"{self._w}x{self._h}" 

    def iconbitmap(self, default=None):
        pass

    def iconphoto(self, default, *images):
        pass

    def resizable(self, w=True, h=True):
        pass

    def protocol(self, name, func):
        pass

    def after(self, ms, func=None, *args):
        if func is None:
            time.sleep(max(0.0, float(ms) / 1000.0))
            return None
        due = time.monotonic() + max(0.0, float(ms) / 1000.0)
        with self._timer_lock:
            tid = f"after#{self._next_timer_id}"
            self._next_timer_id += 1
            self._timers[tid] = (due, func, args)
        with self._event_cond:
            self._event_cond.notify_all()
        return tid

    def after_cancel(self, ident):
        with self._timer_lock:
            self._timers.pop(ident, None)

    def post_ui_event(self, fn):
        with self._event_cond:
            self._event_queue.append(fn)
            self._event_cond.notify_all()

    def post_move_event(self, rx: int, ry: int):
        """Coalesces high-frequency touch move samples so dragging stays at 60 FPS with zero backlog."""
        with self._event_cond:
            self._pending_move_xy = (int(rx), int(ry))
            self._event_cond.notify_all()

    def _process_pending_events(self):
        # 1. Process queued UI touch/mouse events
        while True:
            with self._event_cond:
                if not self._event_queue:
                    break
                ev_fn = self._event_queue.pop(0)
            try:
                ev_fn()
            except Exception:
                pass

        # 1b. Process coalesced pointer move event (at most once per frame!)
        move_xy = None
        with self._event_cond:
            if self._pending_move_xy is not None:
                move_xy = self._pending_move_xy
                self._pending_move_xy = None
        if move_xy is not None:
            try:
                dispatch_pointer_move(self, move_xy[0], move_xy[1], is_dragging=True)
            except Exception:
                pass

        # 2. Process due after() timers
        now = time.monotonic()
        due_list = []
        with self._timer_lock:
            for tid, (due_t, fn, args) in list(self._timers.items()):
                if now >= due_t:
                    due_list.append((tid, fn, args))
                    self._timers.pop(tid, None)
        for tid, fn, args in due_list:
            try:
                fn(*args)
            except Exception:
                pass

        # 3. Recompute layout if dirty
        if self._dirty:
            self.update_idletasks()

    def update_idletasks(self):
        self._dirty = False
        self._bg_without_ghost_pil = None
        _compute_req_size(self)
        self._w = int(getattr(self, "_target_w", 1600))
        self._h = int(getattr(self, "_target_h", 950))
        self._x = 0
        self._y = 0
        self._rootx = 0
        self._rooty = 0
        _layout_children(self)

    def update(self):
        self._process_pending_events()
        self.update_idletasks()

    def wait_variable(self, var: Variable):
        """Re-entrant event loop wait! Processes timers & input events until var is modified."""
        initial_val = var.get()
        while self._running and self._exists:
            self._process_pending_events()
            if var.get() != initial_val and var.get() != 0:
                break
            # Wait briefly for next timer or input event
            with self._event_cond:
                if not self._event_queue:
                    self._event_cond.wait(timeout=0.004)

    def mainloop(self):
        self.update_idletasks()
        while self._running and self._exists:
            self._process_pending_events()
            with self._event_cond:
                if not self._event_queue:
                    self._event_cond.wait(timeout=0.004)


# ==========================================
# Layout Engine (Bottom-Up + Top-Down)
# ==========================================
def _compute_leaf_req_size(w: Widget):
    opts = w._opts
    bd = int(opts.get("bd") or 0) + int(opts.get("highlightthickness") or 0)
    px1, px2 = _parse_pad(opts.get("padx", 0))
    py1, py2 = _parse_pad(opts.get("pady", 0))
    pad_w = px1 + px2 + bd * 2
    pad_h = py1 + py2 + bd * 2

    img = opts.get("image")
    txt = str(w.cget("text") or "")
    font_spec = opts.get("font")
    wrap = int(opts.get("wraplength") or 0)
    explicit_w = opts.get("width")
    explicit_h = opts.get("height")

    if isinstance(w, Canvas):
        cw = int(explicit_w) if explicit_w is not None else 400
        ch = int(explicit_h) if explicit_h is not None else 240
        return (cw + bd * 2, ch + bd * 2)

    if isinstance(w, Scrollbar):
        if opts.get("orient") == HORIZONTAL:
            return (120, 16)
        return (16, 120)

    if isinstance(w, Scale):
        if opts.get("orient") == HORIZONTAL:
            sw = int(opts.get("length") or 180)
            return (sw, 38)
        return (44, int(opts.get("length") or 140))

    if isinstance(w, (Entry, Spinbox, Combobox)):
        char_cnt = int(explicit_w) if explicit_w is not None else 18
        _, th, _ = measure_text_block("測試Ag", font_spec)
        return (max(60, int(char_cnt * 10.5) + 18), max(28, th + 10))

    if isinstance(w, (Text, ScrolledText)):
        char_w = int(explicit_w) if explicit_w is not None else 36
        line_cnt = int(explicit_h) if explicit_h is not None else 8
        return (char_w * 9 + pad_w, line_cnt * 18 + pad_h)

    if isinstance(w, Listbox):
        char_w = int(explicit_w) if explicit_w is not None else 28
        line_cnt = int(explicit_h) if explicit_h is not None else 10
        return (char_w * 9 + pad_w, line_cnt * 20 + pad_h)

    # Label / Button / Checkbutton
    tw, th, _ = measure_text_block(txt, font_spec, wrap)
    if isinstance(w, Checkbutton):
        tw += 24
        th = max(th, 22)

    if img is not None and hasattr(img, "width"):
        iw, ih = img.width(), img.height()
        comp = opts.get("compound", NONE)
        if comp in (TOP, BOTTOM) and txt:
            nat_w = max(iw, tw) + pad_w
            nat_h = ih + th + 4 + pad_h
        elif comp in (LEFT, RIGHT) and txt:
            nat_w = iw + tw + 6 + pad_w
            nat_h = max(ih, th) + pad_h
        else:
            nat_w = iw + pad_w
            nat_h = ih + pad_h
        # In Tk, when image is set, explicit width/height are in pixels!
        rw = int(explicit_w) if explicit_w is not None else nat_w
        rh = int(int(explicit_h) * 0.93) if explicit_h is not None else nat_h
        return (max(16, rw), max(16, rh))
    else:
        # Without image: check if large pixel dimensions were passed (e.g. card preview placeholder 165x230)
        if isinstance(w, Label) and not txt and explicit_w and explicit_h and int(explicit_w) >= 60 and int(explicit_h) >= 60:
            return (int(explicit_w) + bd * 2, int(explicit_h) + bd * 2)
        if explicit_w is not None:
            # Character width
            px_size = int(font_spec[1]) if isinstance(font_spec, (tuple, list)) and len(font_spec) > 1 else 11
            char_unit = max(7.5, px_size * 0.72)
            rw = max(tw + pad_w, int(int(explicit_w) * char_unit) + pad_w)
        else:
            rw = tw + pad_w
        if explicit_h is not None:
            line_unit = max(18, th)
            rh = max(th + pad_h, int(int(explicit_h) * line_unit) + pad_h)
        else:
            rh = th + pad_h
        return (max(12, rw), max(12, rh))


def _compute_req_size(w: Widget):
    if not w._exists:
        return (1, 1)

    # First compute for all children
    for c in w._children:
        if c._exists:
            _compute_req_size(c)

    if isinstance(w, Canvas):
        for it in w._items.values():
            if it["type"] == "window" and it.get("window") is not None:
                _compute_req_size(it["window"])

    if not isinstance(w, (Frame, LabelFrame, Tk, Toplevel)):
        w._reqw, w._reqh = _compute_leaf_req_size(w)
        return (w._reqw, w._reqh)

    # Container (Frame / LabelFrame)
    opts = w._opts
    bd = int(opts.get("bd") or 0) + int(opts.get("highlightthickness") or 0)
    px1, px2 = _parse_pad(opts.get("padx", 0))
    py1, py2 = _parse_pad(opts.get("pady", 0))
    title_h = 20 if isinstance(w, LabelFrame) and opts.get("text") else 0
    pad_w = px1 + px2 + bd * 2
    pad_h = py1 + py2 + bd * 2 + title_h

    pack_kids = [c for c in w._children if c._exists and c._geom_mgr == "pack"]
    grid_kids = [c for c in w._children if c._exists and c._geom_mgr == "grid"]

    is_portrait = getattr(w._root, "_portrait_mode", False)
    if pack_kids and w._pack_propagate:
        # Check special Portrait 2-tier board row (left_zones + center_stage + right_zones)
        if (
            is_portrait
            and len(pack_kids) == 3
            and all(c._geom_opts.get("side", TOP) == LEFT for c in pack_kids)
            and sum(c._reqw for c in pack_kids) > 960
        ):
            c0, c1, c2 = pack_kids
            row_zones_w = c0._reqw + c2._reqw + 24
            row_zones_h = max(c0._reqh, c2._reqh) + 6
            stage_w = c1._reqw + 16
            stage_h = c1._reqh + 6
            req_w = max(row_zones_w, stage_w) + pad_w
            req_h = row_zones_h + stage_h + pad_h
        # Check special Portrait hand_outer (p_hud LEFT, br_hud RIGHT, hand_canvas LEFT expand)
        elif (
            is_portrait
            and len(pack_kids) == 3
            and isinstance(pack_kids[2], Canvas)
            and pack_kids[0]._geom_opts.get("side") == LEFT
            and pack_kids[1]._geom_opts.get("side") == RIGHT
        ):
            c_hud, c_br, c_canv = pack_kids
            req_w = 980
            req_h = c_canv._reqh + max(c_hud._reqh, c_br._reqh) + 24 + pad_h
        else:
            acc_w, acc_h = 0, 0
            for c in reversed(pack_kids):
                g = c._geom_opts
                cpx1, cpx2 = _parse_pad(g.get("padx", 0))
                cpy1, cpy2 = _parse_pad(g.get("pady", 0))
                cw = c._reqw + cpx1 + cpx2 + int(g.get("ipadx", 0)) * 2
                ch = c._reqh + cpy1 + cpy2 + int(g.get("ipady", 0)) * 2
                side = g.get("side", TOP)
                if side in (TOP, BOTTOM):
                    acc_h += ch
                    acc_w = max(acc_w, cw)
                else:
                    acc_w += cw
                    acc_h = max(acc_h, ch)
            req_w = acc_w + pad_w
            req_h = acc_h + pad_h
    elif grid_kids and w._grid_propagate:
        col_w = {}
        row_h = {}
        for c in grid_kids:
            g = c._geom_opts
            r = int(g.get("row", 0))
            col = int(g.get("column", 0))
            cpx1, cpx2 = _parse_pad(g.get("padx", 0))
            cpy1, cpy2 = _parse_pad(g.get("pady", 0))
            cw = c._reqw + cpx1 + cpx2 + int(g.get("ipadx", 0)) * 2
            ch = c._reqh + cpy1 + cpy2 + int(g.get("ipady", 0)) * 2
            col_w[col] = max(col_w.get(col, 0), cw)
            row_h[r] = max(row_h.get(r, 0), ch)
        req_w = sum(col_w.values()) + pad_w
        req_h = sum(row_h.values()) + pad_h
    else:
        req_w = pad_w
        req_h = pad_h

    if opts.get("width") is not None and (not pack_kids or not w._pack_propagate):
        req_w = int(opts["width"])
    elif opts.get("width") is not None:
        req_w = max(req_w, int(opts["width"]))

    if opts.get("height") is not None and (not pack_kids or not w._pack_propagate):
        req_h = int(opts["height"])
    elif opts.get("height") is not None:
        req_h = max(req_h, int(opts["height"]))

    w._reqw = max(1, req_w)
    w._reqh = max(1, req_h)
    return (w._reqw, w._reqh)


def _anchor_offset(anchor, box_w, box_h, item_w, item_h):
    anchor = str(anchor or CENTER).lower()
    if anchor in ("nw", "w", "sw"):
        dx = 0
    elif anchor in ("ne", "e", "se"):
        dx = box_w - item_w
    else:
        dx = (box_w - item_w) // 2

    if anchor in ("nw", "n", "ne"):
        dy = 0
    elif anchor in ("sw", "s", "se"):
        dy = box_h - item_h
    else:
        dy = (box_h - item_h) // 2
    return (dx, dy)


def _layout_children(w: Widget):
    if not w._exists:
        return

    # Fire <Configure> if size changed
    cur_sz = (int(w._w), int(w._h))
    if cur_sz != w._last_cfg_size and cur_sz[0] > 1 and cur_sz[1] > 1:
        w._last_cfg_size = cur_sz
        if "<Configure>" in w._bindings:
            w._fire_event("<Configure>", Event(widget=w, x=0, y=0))

    opts = w._opts
    bd = int(opts.get("bd") or 0) + int(opts.get("highlightthickness") or 0)
    px1, px2 = _parse_pad(opts.get("padx", 0))
    py1, py2 = _parse_pad(opts.get("pady", 0))
    title_h = 20 if isinstance(w, LabelFrame) and opts.get("text") else 0

    cav_x = bd + px1
    cav_y = bd + py1 + title_h
    cav_w = max(0, w._w - (bd * 2 + px1 + px2))
    cav_h = max(0, w._h - (bd * 2 + py1 + py2 + title_h))

    # 1. Pack Children (with lookahead for expand=True and Portrait auto-stacking)
    is_portrait = getattr(w._root, "_portrait_mode", False)
    pack_kids = [c for c in w._children if c._exists and c._geom_mgr == "pack"]

    # Special Portrait layout A: 3-column battle board row (left_zones, center_stage, right_zones)
    if (
        is_portrait
        and len(pack_kids) == 3
        and all(c._geom_opts.get("side", TOP) == LEFT for c in pack_kids)
        and sum(c._reqw for c in pack_kids) > 960
    ):
        c0, c1, c2 = pack_kids
        zones_h = max(c0._reqh, c2._reqh)
        stage_h = c1._reqh
        # Determine if this is AI mat (#211620) or Player mat (#141e2b):
        # AI mat puts back-zones on top and stage on bottom (facing center);
        # Player mat puts stage on top (facing center) and back-zones on bottom!
        is_ai_row = str(w._opts.get("bg", "")).lower() in ("#211620", "#291926")
        if is_ai_row:
            zy = cav_y + 2
            sy = zy + zones_h + 6
        else:
            sy = cav_y + 2
            zy = sy + stage_h + 6

        # Center the two zone groups [c0, c2]
        tot_zw = c0._reqw + c2._reqw + 24
        zx0 = cav_x + max(0, (cav_w - tot_zw) // 2)
        c0._x, c0._y, c0._w, c0._h = zx0, zy, c0._reqw, zones_h
        c0._rootx, c0._rooty = w._rootx + c0._x, w._rooty + c0._y
        _layout_children(c0)

        c2._x, c2._y, c2._w, c2._h = zx0 + c0._reqw + 24, zy, c2._reqw, zones_h
        c2._rootx, c2._rooty = w._rootx + c2._x, w._rooty + c2._y
        _layout_children(c2)

        # Center the stage group [c1]
        sx0 = cav_x + max(0, (cav_w - c1._reqw) // 2)
        c1._x, c1._y, c1._w, c1._h = sx0, sy, c1._reqw, stage_h
        c1._rootx, c1._rooty = w._rootx + c1._x, w._rooty + c1._y
        _layout_children(c1)
        pack_kids = []

    # Special Portrait layout B: hand_outer (p_hud + br_hud on top row, hand_canvas full width at bottom)
    elif (
        is_portrait
        and len(pack_kids) == 3
        and isinstance(pack_kids[2], Canvas)
        and pack_kids[0]._geom_opts.get("side") == LEFT
        and pack_kids[1]._geom_opts.get("side") == RIGHT
    ):
        c_hud, c_br, c_canv = pack_kids
        top_h = max(c_hud._reqh, c_br._reqh)
        ty = cav_y + 4
        c_hud._x, c_hud._y, c_hud._w, c_hud._h = cav_x + 8, ty, c_hud._reqw, top_h
        c_hud._rootx, c_hud._rooty = w._rootx + c_hud._x, w._rooty + c_hud._y
        _layout_children(c_hud)

        c_br._x, c_br._y, c_br._w, c_br._h = max(cav_x + c_hud._reqw + 16, cav_x + cav_w - c_br._reqw - 8), ty, c_br._reqw, top_h
        c_br._rootx, c_br._rooty = w._rootx + c_br._x, w._rooty + c_br._y
        _layout_children(c_br)

        cy = ty + top_h + 4
        canv_h = max(195, cav_h - (top_h + 10))
        c_canv._x, c_canv._y, c_canv._w, c_canv._h = cav_x, cy, cav_w, canv_h
        c_canv._rootx, c_canv._rooty = w._rootx + c_canv._x, w._rooty + c_canv._y
        _layout_children(c_canv)
        pack_kids = []

    # Special Portrait layout C: top_hud_bar (Label LEFT, ai_hand_canvas LEFT expand, ai_hud RIGHT)
    elif (
        is_portrait
        and len(pack_kids) == 3
        and isinstance(pack_kids[0], Label)
        and isinstance(pack_kids[1], Canvas)
        and pack_kids[2]._geom_opts.get("side") == RIGHT
    ):
        c_lbl, c_fan, c_aihud = pack_kids
        # Hide long tip label on narrow portrait top bar so AI hand fan + AI HUD fit side by side
        c_lbl._x, c_lbl._y, c_lbl._w, c_lbl._h = 0, 0, 1, 1
        c_lbl._rootx, c_lbl._rooty = w._rootx, w._rooty
        hud_w = c_aihud._reqw
        fan_w = max(320, cav_w - hud_w - 16)
        c_fan._x, c_fan._y, c_fan._w, c_fan._h = cav_x + 4, cav_y + 4, fan_w, max(70, cav_h - 8)
        c_fan._rootx, c_fan._rooty = w._rootx + c_fan._x, w._rooty + c_fan._y
        _layout_children(c_fan)

        c_aihud._x, c_aihud._y, c_aihud._w, c_aihud._h = cav_x + cav_w - hud_w - 4, cav_y + 4, hud_w, c_aihud._reqh
        c_aihud._rootx, c_aihud._rooty = w._rootx + c_aihud._x, w._rooty + c_aihud._y
        _layout_children(c_aihud)
        pack_kids = []

    for idx, c in enumerate(pack_kids):
        g = c._geom_opts
        side = g.get("side", TOP)
        fill = g.get("fill", NONE)
        expand = bool(g.get("expand", False))
        anchor = g.get("anchor", CENTER)
        cpx1, cpx2 = _parse_pad(g.get("padx", 0))
        cpy1, cpy2 = _parse_pad(g.get("pady", 0))
        ipadx = int(g.get("ipadx", 0))
        ipady = int(g.get("ipady", 0))

        req_cw = c._reqw + ipadx * 2
        req_ch = c._reqh + ipady * 2
        tot_cw = req_cw + cpx1 + cpx2
        tot_ch = req_ch + cpy1 + cpy2

        if side in (TOP, BOTTOM):
            slice_w = cav_w
            if expand:
                # Calculate remaining required vertical space of subsequent siblings
                rem_h = 0
                exp_cnt = 1
                for rem_c in pack_kids[idx + 1:]:
                    rg = rem_c._geom_opts
                    rcpy1, rcpy2 = _parse_pad(rg.get("pady", 0))
                    rch = rem_c._reqh + int(rg.get("ipady", 0)) * 2 + rcpy1 + rcpy2
                    if rg.get("side", TOP) in (TOP, BOTTOM):
                        rem_h += rch
                        if rg.get("expand"):
                            exp_cnt += 1
                    else:
                        rem_h = max(rem_h, rch)
                if cav_h >= tot_ch + rem_h:
                    extra_h = cav_h - (tot_ch + rem_h)
                    slice_h = tot_ch + (extra_h // exp_cnt)
                else:
                    slice_h = max(1, cav_h - rem_h)
            else:
                slice_h = min(cav_h, tot_ch) if cav_h > 0 else tot_ch

            if side == TOP:
                sx, sy = cav_x, cav_y
                cav_y += slice_h
                cav_h = max(0, cav_h - slice_h)
            else:
                sx, sy = cav_x, cav_y + cav_h - slice_h
                cav_h = max(0, cav_h - slice_h)
        else:
            slice_h = cav_h
            if expand:
                rem_w = 0
                exp_cnt = 1
                for rem_c in pack_kids[idx + 1:]:
                    rg = rem_c._geom_opts
                    rcpx1, rcpx2 = _parse_pad(rg.get("padx", 0))
                    rcw = rem_c._reqw + int(rg.get("ipadx", 0)) * 2 + rcpx1 + rcpx2
                    if rg.get("side", TOP) in (LEFT, RIGHT):
                        rem_w += rcw
                        if rg.get("expand"):
                            exp_cnt += 1
                    else:
                        rem_w = max(rem_w, rcw)
                if cav_w >= tot_cw + rem_w:
                    extra_w = cav_w - (tot_cw + rem_w)
                    slice_w = tot_cw + (extra_w // exp_cnt)
                else:
                    slice_w = max(1, cav_w - rem_w)
            else:
                slice_w = min(cav_w, tot_cw) if cav_w > 0 else tot_cw

            if side == LEFT:
                sx, sy = cav_x, cav_y
                cav_x += slice_w
                cav_w = max(0, cav_w - slice_w)
            else:
                sx, sy = cav_x + cav_w - slice_w, cav_y
                cav_w = max(0, cav_w - slice_w)

        avail_w = max(1, slice_w - (cpx1 + cpx2))
        avail_h = max(1, slice_h - (cpy1 + cpy2))

        final_w = avail_w if fill in (X, BOTH) else min(avail_w, req_cw)
        final_h = avail_h if fill in (Y, BOTH) else min(avail_h, req_ch)
        dx, dy = _anchor_offset(anchor, avail_w, avail_h, final_w, final_h)

        c._x = sx + cpx1 + dx
        c._y = sy + cpy1 + dy
        c._w = max(1, final_w)
        c._h = max(1, final_h)
        c._rootx = w._rootx + c._x
        c._rooty = w._rooty + c._y
        _layout_children(c)

    # 2. Grid Children
    grid_kids = [c for c in w._children if c._exists and c._geom_mgr == "grid"]
    if grid_kids:
        col_w = {}
        row_h = {}
        for c in grid_kids:
            g = c._geom_opts
            r = int(g.get("row", 0))
            col = int(g.get("column", 0))
            cpx1, cpx2 = _parse_pad(g.get("padx", 0))
            cpy1, cpy2 = _parse_pad(g.get("pady", 0))
            cw = c._reqw + cpx1 + cpx2 + int(g.get("ipadx", 0)) * 2
            ch = c._reqh + cpy1 + cpy2 + int(g.get("ipady", 0)) * 2
            col_w[col] = max(col_w.get(col, 0), cw)
            row_h[r] = max(row_h.get(r, 0), ch)

        total_grid_w = sum(col_w.values())
        total_weight = sum(w._grid_col_weights.get(col, 0) for col in col_w)
        if total_weight > 0 and cav_w > total_grid_w:
            extra = cav_w - total_grid_w
            for col in col_w:
                wt = w._grid_col_weights.get(col, 0)
                if wt > 0:
                    col_w[col] += int(extra * (wt / total_weight))

        col_x = {}
        cur_x = cav_x
        for col in sorted(col_w.keys()):
            col_x[col] = cur_x
            cur_x += col_w[col]

        row_y = {}
        cur_y = cav_y
        for r in sorted(row_h.keys()):
            row_y[r] = cur_y
            cur_y += row_h[r]

        for c in grid_kids:
            g = c._geom_opts
            r = int(g.get("row", 0))
            col = int(g.get("column", 0))
            cpx1, cpx2 = _parse_pad(g.get("padx", 0))
            cpy1, cpy2 = _parse_pad(g.get("pady", 0))
            sticky = str(g.get("sticky", "")).lower()
            cell_w = max(1, col_w.get(col, c._reqw) - (cpx1 + cpx2))
            cell_h = max(1, row_h.get(r, c._reqh) - (cpy1 + cpy2))

            fw = cell_w if ("e" in sticky and "w" in sticky) else min(cell_w, c._reqw)
            fh = cell_h if ("n" in sticky and "s" in sticky) else min(cell_h, c._reqh)
            dx, dy = _anchor_offset(sticky or CENTER, cell_w, cell_h, fw, fh)

            c._x = col_x.get(col, cav_x) + cpx1 + dx
            c._y = row_y.get(r, cav_y) + cpy1 + dy
            c._w = max(1, fw)
            c._h = max(1, fh)
            c._rootx = w._rootx + c._x
            c._rooty = w._rooty + c._y
            _layout_children(c)

    # 3. Place Children
    place_kids = [c for c in w._children if c._exists and c._geom_mgr == "place"]
    for c in place_kids:
        g = c._geom_opts
        relx = float(g.get("relx", 0.0))
        rely = float(g.get("rely", 0.0))
        ox = int(float(g.get("x", 0)))
        oy = int(float(g.get("y", 0)))
        anchor = str(g.get("anchor", NW)).lower()

        if "relwidth" in g and g["relwidth"] is not None:
            pw = int(round(w._w * float(g["relwidth"])))
        elif "width" in g and g["width"] is not None:
            pw = int(float(g["width"]))
        else:
            pw = c._reqw

        if "relheight" in g and g["relheight"] is not None:
            ph = int(round(w._h * float(g["relheight"])))
        elif "height" in g and g["height"] is not None:
            ph = int(float(g["height"]))
        else:
            ph = c._reqh

        base_x = int(round(w._w * relx)) + ox
        base_y = int(round(w._h * rely)) + oy

        if anchor in ("ne", "e", "se"):
            px = base_x - pw
        elif anchor in ("n", "s", "center"):
            px = base_x - pw // 2
        else:
            px = base_x

        if anchor in ("sw", "s", "se"):
            py = base_y - ph
        elif anchor in ("w", "e", "center"):
            py = base_y - ph // 2
        else:
            py = base_y

        if is_portrait and pw > w._w - 16 and w is w._root or (is_portrait and pw > w._w - 16 and "relwidth" not in g):
            pw = w._w - 16
            px = (w._w - pw) // 2
        c._x = px
        c._y = py
        c._w = max(1, pw)
        c._h = max(1, ph)
        c._rootx = w._rootx + c._x
        c._rooty = w._rooty + c._y
        _layout_children(c)

    # 4. Canvas embedded windows (create_window)
    if isinstance(w, Canvas):
        for cid in w._item_order:
            it = w._items[cid]
            if it["type"] == "window" and it.get("window") is not None:
                win = it["window"]
                if not win._exists:
                    continue
                wx = int(it["coords"][0] - w._scroll_x)
                wy = int(it["coords"][1] - w._scroll_y)
                ww = int(it["width"]) if it.get("width") else win._reqw
                wh = int(it["height"]) if it.get("height") else win._reqh
                win._x = wx
                win._y = wy
                win._w = max(1, ww)
                win._h = max(1, wh)
                win._rootx = w._rootx + wx
                win._rooty = w._rooty + wy
                _layout_children(win)


# ==========================================
# High-Fidelity 1600x950 PIL Renderer
# ==========================================
def _parse_color(col, default=None):
    if not col:
        return default
    col = str(col).strip()
    if col.lower() == "white":
        return "#ffffff"
    if col.lower() == "black":
        return "#000000"
    return col


def _paste_photo_image(surface: Image.Image, photo: PhotoImage, dst_x: int, dst_y: int, clip_box=None):
    if photo is None or not hasattr(photo, "_pil"):
        return
    src = photo._pil
    if clip_box:
        cx1, cy1, cx2, cy2 = clip_box
        ix1 = max(dst_x, cx1)
        iy1 = max(dst_y, cy1)
        ix2 = min(dst_x + src.width, cx2)
        iy2 = min(dst_y + src.height, cy2)
        if ix2 <= ix1 or iy2 <= iy1:
            return
        crop_src = src.crop((ix1 - dst_x, iy1 - dst_y, ix2 - dst_x, iy2 - dst_y))
        surface.paste(crop_src, (ix1, iy1), crop_src)
    else:
        surface.paste(src, (dst_x, dst_y), src)


def _draw_widget_tree(surface: Image.Image, draw: ImageDraw.ImageDraw, w: Widget, clip_box=(0, 0, 1600, 950)):
    if not w._exists or not w.winfo_ismapped():
        return

    wx1, wy1 = w._rootx, w._rooty
    wx2, wy2 = wx1 + w._w, wy1 + w._h
    cx1 = max(clip_box[0], wx1)
    cy1 = max(clip_box[1], wy1)
    cx2 = min(clip_box[2], wx2)
    cy2 = min(clip_box[3], wy2)
    if cx2 <= cx1 or cy2 <= cy1:
        return

    my_clip = (cx1, cy1, cx2, cy2)
    opts = w._opts
    bg = _parse_color(opts.get("bg"), "#151b29")
    fg = _parse_color(opts.get("fg"), "#ffffff")
    if opts.get("state") == DISABLED:
        fg = _parse_color(opts.get("disabledforeground"), "#8890a8")
    bd = int(opts.get("bd") or 0)
    ht = int(opts.get("highlightthickness") or 0)
    relief = opts.get("relief", FLAT)

    # 1. Background fill
    if bg:
        draw.rectangle([cx1, cy1, cx2 - 1, cy2 - 1], fill=bg)

    # 2. Widget-specific content
    if isinstance(w, Canvas):
        for cid in w._item_order:
            it = w._items[cid]
            itype = it["type"]
            coords = it["coords"]
            ox = wx1 - int(w._scroll_x)
            oy = wy1 - int(w._scroll_y)

            if itype == "image":
                im = it.get("image")
                if im and hasattr(im, "_pil"):
                    ix = int(coords[0]) + ox
                    iy = int(coords[1]) + oy
                    anc = str(it.get("anchor", CENTER)).lower()
                    if anc in ("ne", "e", "se"):
                        ix -= im.width()
                    elif anc in ("n", "s", "center"):
                        ix -= im.width() // 2
                    if anc in ("sw", "s", "se"):
                        iy -= im.height()
                    elif anc in ("w", "e", "center"):
                        iy -= im.height() // 2
                    _paste_photo_image(surface, im, ix, iy, my_clip)

            elif itype == "rectangle" and len(coords) >= 4:
                rx1 = max(cx1, int(coords[0]) + ox)
                ry1 = max(cy1, int(coords[1]) + oy)
                rx2 = min(cx2 - 1, int(coords[2]) + ox)
                ry2 = min(cy2 - 1, int(coords[3]) + oy)
                if rx2 > rx1 and ry2 > ry1:
                    rfill = _parse_color(it.get("fill"), None)
                    rout = _parse_color(it.get("outline"), None)
                    draw.rectangle([rx1, ry1, rx2, ry2], fill=rfill, outline=rout, width=int(it.get("width", 1)))

            elif itype == "oval" and len(coords) >= 4:
                ox1 = int(coords[0]) + ox
                oy1 = int(coords[1]) + oy
                ox2 = int(coords[2]) + ox
                oy2 = int(coords[3]) + oy
                rfill = _parse_color(it.get("fill"), None)
                rout = _parse_color(it.get("outline"), None)
                draw.ellipse([ox1, oy1, ox2, oy2], fill=rfill, outline=rout, width=int(it.get("width", 1)))

            elif itype == "line" and len(coords) >= 4:
                pts = [(int(coords[i]) + ox, int(coords[i + 1]) + oy) for i in range(0, len(coords) - 1, 2)]
                lfill = _parse_color(it.get("fill"), "#ffffff")
                draw.line(pts, fill=lfill, width=int(it.get("width", 1)))

            elif itype == "text":
                tx = int(coords[0]) + ox
                ty = int(coords[1]) + oy
                ttxt = str(it.get("text", ""))
                tfont = it.get("font", ("Microsoft JhengHei", 11))
                tfill = _parse_color(it.get("fill"), "#ffffff")
                tw, th, tlines = measure_text_block(ttxt, tfont, int(it.get("width", 0)))
                anc = str(it.get("anchor", CENTER)).lower()
                if anc in ("ne", "e", "se"):
                    tx -= tw
                elif anc in ("n", "s", "center"):
                    tx -= tw // 2
                if anc in ("sw", "s", "se"):
                    ty -= th
                elif anc in ("w", "e", "center"):
                    ty -= th // 2
                pil_f = get_pil_font(tfont)
                lh = max(12, th // max(1, len(tlines)))
                for l_i, ln in enumerate(tlines):
                    ly = ty + l_i * lh
                    if cy1 - 10 <= ly <= cy2:
                        draw.text((tx, ly), ln, fill=tfill, font=pil_f)

            elif itype == "window" and it.get("window") is not None:
                _draw_widget_tree(surface, draw, it["window"], my_clip)

    elif isinstance(w, (Label, Button, Checkbutton)):
        img = opts.get("image")
        txt = str(w.cget("text") or "")
        if isinstance(w, Checkbutton):
            var = w.cget("variable")
            checked = bool(var.get()) if isinstance(var, Variable) else False
            txt = f"{'☑' if checked else '☐'} {txt}"
        font_spec = opts.get("font")
        pil_f = get_pil_font(font_spec)
        wrap = int(opts.get("wraplength") or 0)
        comp = opts.get("compound", NONE)
        anc = opts.get("anchor", CENTER)
        px1, px2 = _parse_pad(opts.get("padx", 0))
        py1, py2 = _parse_pad(opts.get("pady", 0))

        inner_x = wx1 + bd + px1
        inner_y = wy1 + bd + py1
        inner_w = max(1, w._w - (bd * 2 + px1 + px2))
        inner_h = max(1, w._h - (bd * 2 + py1 + py2))

        if img is not None and hasattr(img, "_pil"):
            iw, ih = img.width(), img.height()
            if txt and comp in (TOP, BOTTOM):
                tw, th, lines = measure_text_block(txt, font_spec, wrap)
                tot_h = ih + th + 2
                start_y = wy1 + max(2, (w._h - tot_h) // 2)
                if comp == TOP:
                    ix = wx1 + (w._w - iw) // 2
                    _paste_photo_image(surface, img, ix, start_y, my_clip)
                    ty = start_y + ih + 2
                else:
                    ty = start_y
                    ix = wx1 + (w._w - iw) // 2
                    _paste_photo_image(surface, img, ix, start_y + th + 2, my_clip)
                lh = max(11, th // max(1, len(lines)))
                for li, ln in enumerate(lines):
                    lw, _, _ = measure_text_block(ln, font_spec)
                    tx = wx1 + (w._w - lw) // 2
                    if cy1 <= ty + li * lh <= cy2 - 8:
                        draw.text((tx, ty + li * lh), ln, fill=fg, font=pil_f)
            else:
                if (
                    isinstance(w, Label)
                    and not txt
                    and w._w >= 850
                    and w._h >= 550
                    and (iw != w._w or ih != w._h)
                    and getattr(img, "_pil", None) is not None
                ):
                    cached_stretch = getattr(img, "_stretched_photo", None)
                    if cached_stretch is None or cached_stretch[0] != (w._w, w._h):
                        s_pil = img._pil.resize((w._w, w._h), Image.Resampling.BILINEAR)
                        s_photo = PhotoImage(s_pil)
                        img._stretched_photo = ((w._w, w._h), s_photo)
                    else:
                        s_photo = cached_stretch[1]
                    _paste_photo_image(surface, s_photo, wx1, wy1, my_clip)
                else:
                    ix = wx1 + (w._w - iw) // 2
                    iy = wy1 + (w._h - ih) // 2
                    _paste_photo_image(surface, img, ix, iy, my_clip)
        elif txt:
            tw, th, lines = measure_text_block(txt, font_spec, wrap)
            dx, dy = _anchor_offset(anc, inner_w, inner_h, tw, th)
            tx0 = inner_x + max(0, dx)
            ty0 = inner_y + max(0, dy)
            lh = max(12, th // max(1, len(lines)))
            just = str(opts.get("justify", CENTER)).lower()
            for li, ln in enumerate(lines):
                ly = ty0 + li * lh
                if ly < cy1 - 8 or ly > cy2 - 6:
                    continue
                lw, _, _ = measure_text_block(ln, font_spec)
                if just == "center":
                    lx = tx0 + max(0, (tw - lw) // 2)
                elif just == "right":
                    lx = tx0 + max(0, tw - lw)
                else:
                    lx = tx0
                draw.text((lx, ly), ln, fill=fg, font=pil_f)

    elif isinstance(w, (Entry, Spinbox, Combobox)):
        draw.rectangle([wx1, wy1, wx2 - 1, wy2 - 1], fill=_parse_color(opts.get("bg"), "#0d111a"), outline="#4cc9f0", width=1)
        val_txt = sanitize_cjk_text(w.get())
        font_spec = opts.get("font")
        pil_f = get_pil_font(font_spec)
        _, th, _ = measure_text_block(val_txt or "Ag", font_spec)
        ty = wy1 + max(2, (w._h - th) // 2)
        draw.text((wx1 + 8, ty), val_txt, fill=_parse_color(opts.get("fg"), "#06d6a0"), font=pil_f)
        if isinstance(w, Combobox):
            # Dropdown arrow box
            ax1 = wx2 - 24
            draw.rectangle([ax1, wy1 + 1, wx2 - 2, wy2 - 2], fill="#252c42", outline="#4cc9f0", width=1)
            draw.text((ax1 + 5, ty), "▼", fill="#ffd166", font=pil_f)

    elif isinstance(w, (Text, ScrolledText)):
        font_spec = opts.get("font")
        pil_f = get_pil_font(font_spec)
        px1, px2 = _parse_pad(opts.get("padx", 8))
        py1, py2 = _parse_pad(opts.get("pady", 6))
        wrap_w = max(60, w._w - (px1 + px2 + 16))
        _, th, lines = measure_text_block(w._content, font_spec, wrap_w)
        lh = max(15, th // max(1, len(lines))) if lines else 16
        vis_lines = max(1, (w._h - (py1 + py2)) // lh)
        if w._scroll_y > 90000:
            start_line = max(0, len(lines) - vis_lines)
        else:
            start_line = max(0, min(max(0, len(lines) - vis_lines), w._scroll_y // lh))
        for idx_l, ln in enumerate(lines[start_line : start_line + vis_lines]):
            ly = wy1 + py1 + idx_l * lh
            if ly + lh <= cy2:
                draw.text((wx1 + px1, ly), ln, fill=fg, font=pil_f)

    elif isinstance(w, Listbox):
        font_spec = opts.get("font")
        pil_f = get_pil_font(font_spec)
        lh = 22
        vis_cnt = max(1, (w._h - 8) // lh)
        for i in range(w._scroll_idx, min(len(w._items), w._scroll_idx + vis_cnt)):
            ry1 = wy1 + 4 + (i - w._scroll_idx) * lh
            ry2 = ry1 + lh - 1
            is_sel = i in w._selected
            if is_sel:
                draw.rectangle([wx1 + 2, ry1, wx2 - 3, ry2], fill="#06d6a0")
            draw.text(
                (wx1 + 8, ry1 + 2),
                sanitize_cjk_text(w._items[i])[:42],
                fill="#000000" if is_sel else fg,
                font=pil_f,
            )

    elif isinstance(w, Scale):
        val = w.get()
        lo = float(opts.get("from_") or 0)
        hi = float(opts.get("to") or 100)
        ratio = (float(val) - lo) / max(0.0001, hi - lo)
        ratio = max(0.0, min(1.0, ratio))
        pil_f = get_pil_font(("Consolas", 9, "bold"))
        draw.text((wx1 + 4, wy1 + 1), str(val), fill="#ffd166", font=pil_f)
        ty = wy1 + w._h - 12
        tx1, tx2 = wx1 + 8, wx2 - 8
        draw.line([(tx1, ty), (tx2, ty)], fill="#3a3f58", width=4)
        kx = int(tx1 + ratio * max(1, tx2 - tx1))
        draw.ellipse([kx - 7, ty - 7, kx + 7, ty + 7], fill="#06d6a0", outline="#ffffff", width=1)

    elif isinstance(w, Scrollbar):
        draw.rectangle([cx1, cy1, cx2 - 1, cy2 - 1], fill="#10141f", outline="#2b3348", width=1)

    # 3. Recurse into normal children (pack / grid / place)
    if not isinstance(w, Canvas):
        for c in w._children:
            if c._exists and c._geom_mgr is not None:
                _draw_widget_tree(surface, draw, c, my_clip)

    # 4. Draw border / LabelFrame title on top
    if isinstance(w, LabelFrame):
        draw.rectangle([wx1 + 2, wy1 + 8, wx2 - 3, wy2 - 3], outline="#3a4460", width=1)
        lf_txt = sanitize_cjk_text(opts.get("text") or "")
        if lf_txt:
            pil_f = get_pil_font(opts.get("font"))
            tw, th, _ = measure_text_block(lf_txt, opts.get("font"))
            draw.rectangle([wx1 + 10, wy1, wx1 + 18 + tw, wy1 + th], fill=bg)
            draw.text((wx1 + 14, wy1), lf_txt, fill=fg, font=pil_f)
    elif ht > 0:
        hcol = _parse_color(opts.get("highlightbackground") or opts.get("highlightcolor"), "#ffd166")
        draw.rectangle([wx1, wy1, wx2 - 1, wy2 - 1], outline=hcol, width=min(3, ht))
    elif bd > 0 and relief != FLAT:
        bcol = "#3a4562" if relief in (RAISED, RIDGE, GROOVE) else "#252c42"
        draw.rectangle([wx1, wy1, wx2 - 1, wy2 - 1], outline=bcol, width=1)


def render_root_to_pil(root: Tk) -> Image.Image:
    gw = getattr(root, "_ghost_widget", None)
    if (
        getattr(root, "_ghost_only_dirty", False)
        and not root._dirty
        and root._bg_without_ghost_pil is not None
        and gw is not None
        and gw._exists
        and gw.winfo_ismapped()
    ):
        root._ghost_only_dirty = False
        surface = root._bg_without_ghost_pil.copy()
        draw = ImageDraw.Draw(surface)
        _draw_widget_tree(surface, draw, gw, (0, 0, int(root._w), int(root._h)))
        root._last_frame_pil = surface
        return surface

    if root._dirty:
        root.update_idletasks()
    root._ghost_only_dirty = False
    rw, rh = int(root._w), int(root._h)
    surface = Image.new("RGB", (rw, rh), color=_parse_color(root.cget("bg"), "#0d111a"))
    draw = ImageDraw.Draw(surface)

    # Temporarily hide ghost while capturing clean base board so drag frames take ~1.5ms
    gw_was_mapped = False
    if gw is not None and gw._exists and gw._mapped:
        gw_was_mapped = True
        gw._mapped = False

    _draw_widget_tree(surface, draw, root, (0, 0, rw, rh))

    if gw_was_mapped:
        root._bg_without_ghost_pil = surface.copy()
        gw._mapped = True
        _draw_widget_tree(surface, draw, gw, (0, 0, rw, rh))
    else:
        root._bg_without_ghost_pil = surface

    # Draw active Combobox dropdown overlay if open
    if root._active_dropdown is not None:
        cmb, item_rects = root._active_dropdown
        if cmb._exists and cmb.winfo_ismapped():
            pil_f = get_pil_font(cmb.cget("font"))
            for val_str, (rx1, ry1, rx2, ry2) in item_rects:
                is_cur = (val_str == cmb.get())
                draw.rectangle(
                    [rx1, ry1, rx2, ry2],
                    fill="#ffd166" if is_cur else "#1b2234",
                    outline="#4cc9f0",
                    width=1,
                )
                draw.text(
                    (rx1 + 8, ry1 + 4),
                    str(val_str),
                    fill="#000000" if is_cur else "#ffffff",
                    font=pil_f,
                )

    # Draw floating touch helper bar when an Entry/Spinbox is focused
    fw = getattr(root, "_focused_widget", None)
    if fw is not None and isinstance(fw, (Entry, Spinbox)) and fw._exists and fw.winfo_ismapped():
        pil_f = get_pil_font(("Microsoft JhengHei", 10, "bold"))
        bx1 = max(8, min(rw - 540, fw._rootx))
        by1 = fw._rooty + fw._h + 4
        if by1 + 36 > rh - 5:
            by1 = max(4, fw._rooty - 40)
        btns = [
            ("PASTE", "■ 貼上剪貼簿", "#06d6a0", "#000000", 106),
            ("COLON", "：冒號", "#4cc9f0", "#000000", 64),
            ("TCP", "tcp://", "#9b5de5", "#ffffff", 60),
            ("BACK", "◀ 退格", "#2b3348", "#ffffff", 70),
            ("CLEAR", "↺ 清空", "#e63946", "#ffffff", 70),
            ("KB", "⌨ 鍵盤", "#ffd166", "#000000", 78),
            ("CLOSE", "✖", "#3a3f58", "#ffffff", 36),
        ]
        root._entry_helper_rects = []
        cx = bx1
        for act_k, b_txt, b_bg, b_fg, bw in btns:
            rbox = (cx, by1, cx + bw, by1 + 32)
            draw.rectangle(rbox, fill=b_bg, outline="#ffffff", width=1)
            draw.text((cx + 6, by1 + 6), sanitize_cjk_text(b_txt), fill=b_fg, font=pil_f)
            root._entry_helper_rects.append((act_k, fw, rbox))
            cx += bw + 4
    else:
        root._entry_helper_rects = []

    root._last_frame_pil = surface
    return surface


# ==========================================
# Hit-Testing & Pointer/Touch Event Dispatch
# ==========================================
def hit_test_widget(w: Widget, rx: int, ry: int):
    if not w._exists or not w.winfo_ismapped():
        return None
    if not (w._rootx <= rx <= w._rootx + w._w and w._rooty <= ry <= w._rooty + w._h):
        return None

    # Check Canvas embedded windows first (in reverse order)
    if isinstance(w, Canvas):
        for cid in reversed(w._item_order):
            it = w._items[cid]
            if it["type"] == "window" and it.get("window") is not None:
                hit = hit_test_widget(it["window"], rx, ry)
                if hit is not None:
                    return hit
        return w

    # Check children in reverse z-order (place/pack/grid)
    for c in reversed(w._children):
        if c._exists and c._geom_mgr is not None:
            hit = hit_test_widget(c, rx, ry)
            if hit is not None:
                return hit
    return w


def _find_scrollable_ancestor(w: Widget):
    cur = w
    while cur is not None:
        if isinstance(cur, (Canvas, Text, ScrolledText, Listbox)):
            return cur
        # Also check if inside a Canvas create_window
        if cur.master is not None and isinstance(cur.master, Canvas):
            return cur.master
        cur = cur.master
    return None


def dispatch_pointer_down(root: Tk, rx: int, ry: int, double_click: bool = False):
    rx, ry = int(rx), int(ry)

    # 0. Check if clicking inside the floating Entry helper bar
    for act_k, fw, (x1, y1, x2, y2) in list(getattr(root, "_entry_helper_rects", []) or []):
        if x1 <= rx <= x2 and y1 <= ry <= y2:
            if act_k == "PASTE":
                clip_txt = ""
                try:
                    from kivy.core.clipboard import Clipboard
                    clip_txt = Clipboard.paste() or ""
                except Exception:
                    pass
                if clip_txt:
                    fw.delete(0, END)
                    fw.insert(0, clip_txt.strip())
            elif act_k == "COLON":
                fw.insert(END, ":")
            elif act_k == "TCP":
                cur_s = fw.get()
                if not cur_s.startswith("tcp://"):
                    fw.delete(0, END)
                    fw.insert(0, "tcp://" + cur_s)
            elif act_k == "BACK":
                cur_s = fw.get()
                if cur_s:
                    fw.delete(0, END)
                    fw.insert(0, cur_s[:-1])
            elif act_k == "CLEAR":
                fw.delete(0, END)
            elif act_k == "KB":
                cb_kb = getattr(root, "_request_android_kb_fn", None)
                if callable(cb_kb):
                    cb_kb(fw)
            elif act_k == "CLOSE":
                root._focused_widget = None
            root._dirty = True
            return

    # 1. Check if clicking inside an open Combobox dropdown menu
    if root._active_dropdown is not None:
        cmb, item_rects = root._active_dropdown
        root._active_dropdown = None
        root._dirty = True
        for val_str, (x1, y1, x2, y2) in item_rects:
            if x1 <= rx <= x2 and y1 <= ry <= y2:
                cmb.set(val_str)
                cmb._fire_event("<<ComboboxSelected>>", Event(widget=cmb))
                return

    target = hit_test_widget(root, rx, ry)
    if target is None:
        return

    lx = rx - target._rootx
    ly = ry - target._rooty
    ev = Event(widget=target, x=lx, y=ly, x_root=rx, y_root=ry)

    # 2. Fire global bind_all("<ButtonPress-1>")
    for fn in list(root._global_bindings.get("<ButtonPress-1>", [])):
        try:
            fn(ev)
        except Exception:
            pass

    # 3. Widget-specific interactions
    if isinstance(target, (Entry, Spinbox)):
        root._focused_widget = target
        root._dirty = True
        cb_kb = getattr(root, "_request_android_kb_fn", None)
        if callable(cb_kb):
            cb_kb(target)
        return

    if isinstance(target, Combobox):
        vals = list(target.cget("values") or [])
        if vals:
            rects = []
            item_h = 28
            start_y = min(950 - len(vals[:12]) * item_h - 4, target._rooty + target._h)
            start_y = max(4, start_y)
            for idx, v in enumerate(vals[:12]):
                iy1 = start_y + idx * item_h
                rects.append((v, (target._rootx, iy1, target._rootx + max(240, target._w), iy1 + item_h)))
            root._active_dropdown = (target, rects)
            root._dirty = True
        return

    if isinstance(target, Scale):
        lo = float(target.cget("from_") or 0)
        hi = float(target.cget("to") or 100)
        ratio = max(0.0, min(1.0, (lx - 8) / max(1.0, target._w - 16)))
        target.set(lo + ratio * (hi - lo))
        cmd = target.cget("command")
        if callable(cmd):
            try:
                cmd(str(target.get()))
            except Exception:
                pass
        return

    if isinstance(target, Listbox):
        idx = target._scroll_idx + max(0, (ly - 4) // 22)
        if 0 <= idx < len(target._items):
            target._selected = [idx]
            target._fire_event("<<ListboxSelect>>", ev)
            root._dirty = True
        return

    root._drag_widget = target
    if double_click and "<Double-Button-1>" in target._bindings:
        target._fire_event("<Double-Button-1>", ev)
        return

    if "<ButtonPress-1>" in target._bindings:
        target._fire_event("<ButtonPress-1>", ev)
    if "<Button-1>" in target._bindings:
        target._fire_event("<Button-1>", ev)


def dispatch_pointer_move(root: Tk, rx: int, ry: int, is_dragging: bool = False):
    rx, ry = int(rx), int(ry)
    target = hit_test_widget(root, rx, ry)
    w = root._drag_widget if (is_dragging and root._drag_widget is not None) else target
    if w is None:
        return
    lx = rx - w._rootx
    ly = ry - w._rooty
    ev = Event(widget=w, x=lx, y=ly, x_root=rx, y_root=ry)

    for fn in list(root._global_bindings.get("<Motion>", [])):
        try:
            fn(ev)
        except Exception:
            pass

    if is_dragging and "<B1-Motion>" in w._bindings:
        w._fire_event("<B1-Motion>", ev)
    elif "<Motion>" in w._bindings:
        w._fire_event("<Motion>", ev)


def dispatch_pointer_up(root: Tk, rx: int, ry: int):
    rx, ry = int(rx), int(ry)
    drag_w = root._drag_widget
    root._drag_widget = None
    target = hit_test_widget(root, rx, ry)

    w = drag_w if drag_w is not None else target
    if w is None:
        return
    lx = rx - w._rootx
    ly = ry - w._rooty
    ev = Event(widget=w, x=lx, y=ly, x_root=rx, y_root=ry)

    if "<ButtonRelease-1>" in w._bindings:
        w._fire_event("<ButtonRelease-1>", ev)

    if isinstance(w, (Button, Checkbutton)) and target is w:
        w.invoke()


def dispatch_mousewheel(root: Tk, rx: int, ry: int, delta: int):
    target = hit_test_widget(root, int(rx), int(ry))
    if target is None:
        return
    ev = Event(widget=target, x=int(rx) - target._rootx, y=int(ry) - target._rooty, x_root=int(rx), y_root=int(ry), delta=int(delta))
    if "<MouseWheel>" in target._bindings:
        target._fire_event("<MouseWheel>", ev)
        return
    sc_anc = _find_scrollable_ancestor(target)
    if sc_anc is not None:
        if "<MouseWheel>" in sc_anc._bindings:
            sc_anc._fire_event("<MouseWheel>", ev)
        else:
            sc_anc.yview_scroll(-1 if delta > 0 else 1, "units")


# ==========================================
# Submodules (ttk, scrolledtext, filedialog, messagebox)
# ==========================================
class _TtkModule:
    Combobox = Combobox
    Button = Button
    Frame = Frame
    Label = Label
    Scale = Scale
    Scrollbar = Scrollbar


class _ScrolledTextModule:
    ScrolledText = ScrolledText


class _FileDialogModule:
    @staticmethod
    def askopenfilename(**kw):
        return ""

    @staticmethod
    def asksaveasfilename(**kw):
        return ""


class _MessageBoxModule:
    @staticmethod
    def showinfo(title="", message="", **kw):
        return "ok"

    @staticmethod
    def showwarning(title="", message="", **kw):
        return "ok"

    @staticmethod
    def showerror(title="", message="", **kw):
        return "ok"

    @staticmethod
    def askyesno(title="", message="", **kw):
        return True


ttk = _TtkModule()
scrolledtext = _ScrolledTextModule()
filedialog = _FileDialogModule()
messagebox = _MessageBoxModule()


# ==========================================
# Kivy OpenGL Fullscreen Host for Android APK
# ==========================================
def run_kivy_android_host(main_app_cls):
    """
    Launches main.py (MainApp) inside a hardware-accelerated Kivy OpenGL surface on Android.
    Runs the Tkinter event loop + wait_variable() on a dedicated game thread so nested
    modal waits (Ace flip, Mulligan, Trigger/Damage interactive flip, Counter step) never
    block the Android OpenGL touch/render thread.
    """
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.graphics import Color, Rectangle
    from kivy.graphics.texture import Texture
    from kivy.uix.widget import Widget as KivyWidget

    class WSMasterDuelSurface(KivyWidget):
        def __init__(self, tk_root: Tk, **kwargs):
            super().__init__(**kwargs)
            self.tk_root = tk_root
            self.tex = Texture.create(size=(1600, 950), colorfmt="rgb")
            self.tex.flip_vertical()
            self._frame_lock = threading.Lock()
            self._latest_bytes = None
            self._viewport = (0, 0, 1600, 950)
            self._touch_start_xy = None
            self._touch_scrolled = False
            self._kb = None
            self.tk_root._request_android_kb_fn = lambda fw: Clock.schedule_once(lambda dt: self._open_kb(fw), 0)

            with self.canvas:
                Color(0.05, 0.07, 0.10, 1.0)
                self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                Color(1.0, 1.0, 1.0, 1.0)
                self.fg_rect = Rectangle(texture=self.tex, pos=self.pos, size=self.size)

            self.bind(pos=self._update_rects, size=self._update_rects)
            try:
                Window.bind(on_textinput=self._on_window_textinput)
            except Exception:
                pass

        def _update_rects(self, *args):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
            ww, wh = max(1, float(self.width)), max(1, float(self.height))
            is_port = wh > ww
            if is_port:
                # 自動豎屏模式：固定邏輯寬度 1000，高度依手機螢幕長寬比自適應延展，100% 滿版無黑邊
                tw = 1000
                th = max(1340, min(2240, int(round(1000.0 * wh / ww))))
            else:
                # 自動橫屏模式：固定邏輯高度 950，寬度依手機螢幕長寬比 (如 20:9) 自適應延展，100% 滿版無黑邊
                if ww / wh >= 1600.0 / 950.0:
                    th = 950
                    tw = max(1600, min(2240, int(round(950.0 * ww / wh))))
                else:
                    tw = 1600
                    th = max(950, min(1400, int(round(1600.0 * wh / ww))))
            self.tk_root.set_adaptive_surface_size(tw, th, portrait=is_port)
            self._viewport = (int(self.x), int(self.y), int(ww), int(wh))
            self.fg_rect.pos = self.pos
            self.fg_rect.size = self.size

        def _screen_to_tk(self, sx, sy):
            vx, vy, vw, vh = self._viewport
            if vw <= 0 or vh <= 0:
                return (0, 0)
            tw = float(self.tk_root._w)
            th = float(self.tk_root._h)
            rx = int((sx - vx) * tw / vw)
            # Kivy y=0 is bottom, Tk y=0 is top
            ry = int((vh - (sy - vy)) * th / vh)
            rx = max(0, min(int(tw) - 1, rx))
            ry = max(0, min(int(th) - 1, ry))
            return (rx, ry)

        def on_touch_down(self, touch):
            rx, ry = self._screen_to_tk(touch.x, touch.y)
            self._touch_start_xy = (rx, ry)
            self._touch_scrolled = False
            is_dbl = bool(getattr(touch, "is_double_tap", False))
            self.tk_root.post_ui_event(
                lambda r=rx, c=ry, d=is_dbl: (
                    dispatch_pointer_move(self.tk_root, r, c, is_dragging=False),
                    dispatch_pointer_down(self.tk_root, r, c, double_click=d),
                )
            )
            return True

        def on_touch_move(self, touch):
            rx, ry = self._screen_to_tk(touch.x, touch.y)
            if self._touch_start_xy is not None:
                sx, sy = self._touch_start_xy
                dy = ry - sy
                # Check if user is swiping inside a scrollable Canvas / Text / Listbox
                hit_w = hit_test_widget(self.tk_root, rx, ry)
                sc_anc = _find_scrollable_ancestor(hit_w) if hit_w else None
                if sc_anc is not None and hit_w != getattr(self.tk_root, "_drag_widget", None):
                    if abs(dy) >= 36:
                        steps = int(-dy // 36)
                        self._touch_start_xy = (rx, ry)
                        self._touch_scrolled = True
                        self.tk_root.post_ui_event(
                            lambda a=sc_anc, s=steps: a.yview_scroll(s, "units")
                        )
                        return True
            self.tk_root.post_move_event(rx, ry)
            return True

        def on_touch_up(self, touch):
            rx, ry = self._screen_to_tk(touch.x, touch.y)
            self._touch_start_xy = None
            if not self._touch_scrolled:
                self.tk_root.post_ui_event(
                    lambda r=rx, c=ry: dispatch_pointer_up(self.tk_root, r, c)
                )
            return True

        def _open_kb(self, fw):
            try:
                if self._kb is not None:
                    self._kb.unbind(on_key_down=self._on_kb_down)
                self._kb = Window.request_keyboard(self._kb_closed, self)
                if self._kb:
                    self._kb.bind(on_key_down=self._on_kb_down)
            except Exception:
                pass

        def _kb_closed(self):
            if self._kb is not None:
                try:
                    self._kb.unbind(on_key_down=self._on_kb_down)
                except Exception:
                    pass
                self._kb = None

        def _on_window_textinput(self, window, text):
            """使用 SDL2/Kivy 合成後之 on_textinput 接收字元，徹底解決 Shift 大寫或特殊符號 (如 :) 產生 !;! 亂碼問題"""
            fw = getattr(self.tk_root, "_focused_widget", None)
            if fw is None or not isinstance(fw, (Entry, Spinbox)):
                return
            if text and text not in ("\r", "\n"):
                fw.insert(END, text)
                self.tk_root._dirty = True

        def _on_kb_down(self, keyboard, keycode, text, modifiers):
            fw = getattr(self.tk_root, "_focused_widget", None)
            if fw is None or not isinstance(fw, (Entry, Spinbox)):
                return False
            k_name = keycode[1] if isinstance(keycode, (tuple, list)) and len(keycode) > 1 else ""
            if k_name == "backspace":
                cur_s = fw.get()
                if cur_s:
                    fw.delete(0, END)
                    fw.insert(0, cur_s[:-1])
                self.tk_root._dirty = True
                return True
            if k_name in ("enter", "numpadenter", "escape"):
                fw._fire_event("<Return>", Event(widget=fw))
                self.tk_root._focused_widget = None
                self._kb_closed()
                self.tk_root._dirty = True
                return True
            return False

        def push_frame_bytes(self, raw_bytes: bytes, size_wh=(1600, 950)):
            with self._frame_lock:
                self._latest_bytes = (raw_bytes, size_wh)

        def sync_texture(self, dt):
            item = None
            with self._frame_lock:
                if self._latest_bytes is not None:
                    item = self._latest_bytes
                    self._latest_bytes = None
            if item is not None:
                raw, (fw, fh) = item
                if tuple(self.tex.size) != (fw, fh):
                    self.tex = Texture.create(size=(fw, fh), colorfmt="rgb")
                    self.tex.flip_vertical()
                    self.fg_rect.texture = self.tex
                self.tex.blit_buffer(raw, colorfmt="rgb", bufferfmt="ubyte")
                self.canvas.ask_update()

    class WSMasterDuelAndroidApp(App):
        def build(self):
            try:
                Window.fullscreen = "auto"
            except Exception:
                pass
            # 啟用 Android 硬體重力感應自動翻轉 (SCREEN_ORIENTATION_FULL_SENSOR = 10)
            try:
                from jnius import autoclass
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                act = PythonActivity.mActivity
                if act is not None:
                    act.setRequestedOrientation(10)
            except Exception:
                pass
            self.tk_root = Tk()
            self.surface_widget = WSMasterDuelSurface(self.tk_root)
            Clock.schedule_interval(self.surface_widget.sync_texture, 1.0 / 60.0)
            threading.Thread(target=self._game_loop_worker, daemon=True).start()
            return self.surface_widget

        def _game_loop_worker(self):
            orig_process = self.tk_root._process_pending_events
            last_render_t = [0.0]

            def _hooked_process():
                was_dirty = self.tk_root._dirty or getattr(self.tk_root, "_ghost_only_dirty", False)
                orig_process()
                now = time.monotonic()
                if was_dirty or (now - last_render_t[0] >= 0.033):
                    img = render_root_to_pil(self.tk_root)
                    self.surface_widget.push_frame_bytes(img.tobytes(), img.size)
                    last_render_t[0] = now

            self.tk_root._process_pending_events = _hooked_process
            app = main_app_cls(self.tk_root)
            img = render_root_to_pil(self.tk_root)
            self.surface_widget.push_frame_bytes(img.tobytes(), img.size)
            self.tk_root.mainloop()

    WSMasterDuelAndroidApp().run()
