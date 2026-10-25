# -*- coding: utf-8 -*-
"""
✂️ 圓框去背頭貼圖標 (.ico / .png) 裁切轉換小工具
功能：
  1. 可選擇電腦中任意圖片 (.png / .jpg / .webp) 或直接挑選 ws_card_images 內的卡片圖檔。
  2. 滑鼠左鍵拖曳圓框位置、滑鼠滾輪調整放大倍率，並可自由選擇外圈金屬光環顏色。
  3. 一鍵匯出為「四角完全透明去背」的 Windows 多尺寸圖標檔 (.ico，含 256/128/64/48/32/16px) 與高解析度去背 .png！
"""
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from win32_ico_builder import save_win32_dib_ico

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def render_circular_transparent_icon(
    src_img: Image.Image,
    cx_ratio: float = 0.50,
    cy_ratio: float = 0.25,
    zoom: float = 1.95,
    ring_color: str = "#ffd166",
    inner_ring: str = "#06d6a0",
    out_size: int = 512,
) -> Image.Image:
    src_rgba = src_img.convert("RGBA")
    w, h = src_rgba.size
    base_dim = min(w, h)
    crop_s = max(24, min(base_dim, int(base_dim / max(0.6, zoom))))
    cx = int(w * cx_ratio)
    cy = int(h * cy_ratio)
    x0 = max(0, min(w - crop_s, cx - crop_s // 2))
    y0 = max(0, min(h - crop_s, cy - crop_s // 2))

    ss = 1024
    cropped = src_rgba.crop((x0, y0, x0 + crop_s, y0 + crop_s)).resize((ss, ss), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    pad = 44
    mask = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(mask).ellipse([pad, pad, ss - pad - 1, ss - pad - 1], fill=255)

    shadow = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([pad - 12, pad - 12, ss - pad + 12, ss - pad + 12], fill=(0, 0, 0, 175))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)

    char_layer = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    char_layer.paste(cropped, (0, 0), mask)
    canvas = Image.alpha_composite(canvas, char_layer)

    r_draw = ImageDraw.Draw(canvas)
    r_draw.ellipse([pad - 10, pad - 10, ss - pad + 9, ss - pad + 9], outline="#10141f", width=22)
    r_draw.ellipse([pad - 6, pad - 6, ss - pad + 5, ss - pad + 5], outline=ring_color, width=14)
    r_draw.ellipse([pad + 8, pad + 8, ss - pad - 9, ss - pad - 9], outline=inner_ring, width=6)
    return canvas.resize((out_size, out_size), Image.Resampling.LANCZOS)


class IconMakerApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✂️ 圓框去背頭貼圖標 (.ico / .png) 裁切轉換小工具")
        self.root.geometry("880x600")
        self.root.configure(bg="#131926")

        default_img_path = os.path.join(BASE_DIR, "ws_card_images", "BFR_S78_082SP.webp")
        if not os.path.exists(default_img_path):
            default_img_path = os.path.join(BASE_DIR, "ws_card_images", "BFR_S78_057.webp")

        self.src_img = Image.open(default_img_path).convert("RGBA") if os.path.exists(default_img_path) else Image.new("RGBA", (400, 560), (30, 40, 60, 255))
        self.cx = 0.64
        self.cy = 0.36
        self.zoom = 2.15
        self.ring_color = "#ffd166"
        self.inner_color = "#ff6b6b"

        self._build_ui()
        self._redraw()

    def _build_ui(self):
        ff = "Microsoft JhengHei"
        top = tk.Frame(self.root, bg="#1b2234", padx=16, pady=10, bd=1, relief=tk.SOLID)
        top.pack(fill=tk.X, padx=14, pady=10)

        tk.Label(
            top,
            text="✂️ 圓框去背圖標 (.ico) 裁切器 — 支援左鍵拖曳圓框、滾輪縮放、一鍵輸出桌面與打包圖標",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            top,
            text="📂 選擇任意圖片 (.png/.jpg/.webp)",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.pick_image,
        ).pack(side=tk.RIGHT)

        body = tk.Frame(self.root, bg="#131926")
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

        left_f = tk.Frame(body, bg="#1b2234", padx=14, pady=12, bd=1, relief=tk.SOLID)
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        tk.Label(left_f, text="1. 在下方圖片按住左鍵移動圓框・滾輪縮放：", bg="#1b2234", fg="#8ecae6", font=(ff, 10, "bold")).pack(anchor="w", pady=(0, 6))

        self.cw, self.ch = 320, 448
        self.canvas = tk.Canvas(left_f, width=self.cw, height=self.ch, bg="#0d111a", highlightthickness=2, highlightbackground="#ffd166", cursor="fleur")
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self._on_drag)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<MouseWheel>", self._on_wheel)

        right_f = tk.Frame(body, bg="#1b2234", padx=18, pady=12, bd=1, relief=tk.SOLID, width=380)
        right_f.pack(side=tk.LEFT, fill=tk.Y)
        right_f.pack_propagate(False)

        tk.Label(right_f, text="2. 去背圓框圖標即時預覽（棋盤格代表透明背景）：", bg="#1b2234", fg="#06d6a0", font=(ff, 10, "bold")).pack(anchor="w", pady=(0, 8))

        self.lbl_preview = tk.Label(right_f, bg="#1b2234")
        self.lbl_preview.pack(pady=6)

        self.lbl_zoom = tk.Label(right_f, text="縮放倍率：2.15x", bg="#1b2234", fg="#ffd166", font=(ff, 10, "bold"))
        self.lbl_zoom.pack(pady=(6, 2))

        self.sc_zoom = tk.Scale(
            right_f, from_=1.0, to=4.0, resolution=0.05, orient=tk.HORIZONTAL,
            bg="#141824", fg="#ffd166", highlightthickness=0, length=260,
            command=self._on_scale_zoom
        )
        self.sc_zoom.set(self.zoom)
        self.sc_zoom.pack(pady=4)

        col_row = tk.Frame(right_f, bg="#1b2234")
        col_row.pack(fill=tk.X, pady=8)
        tk.Button(col_row, text="🎨 更換外圈金環顏色", bg="#2b3348", fg="#ffd166", font=(ff, 9, "bold"), padx=10, pady=3, command=self.pick_outer_color).pack(side=tk.LEFT, padx=4)
        tk.Button(col_row, text="🎨 更換內圈光環顏色", bg="#2b3348", fg="#06d6a0", font=(ff, 9, "bold"), padx=10, pady=3, command=self.pick_inner_color).pack(side=tk.LEFT, padx=4)

        tk.Button(
            right_f,
            text="💾 另存為 .ico 圖標檔 ＆ 去背 .png",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 12, "bold"),
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.save_icon_files,
        ).pack(fill=tk.X, pady=(16, 6))

        tk.Button(
            right_f,
            text="⚡ 直接覆蓋設為本遊戲預設圖標 (maple_icon.ico)",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.overwrite_game_icon,
        ).pack(fill=tk.X, pady=4)

        self.lbl_status = tk.Label(right_f, text="💡 支援多尺寸 ICO，可直接用於桌面捷徑與 PyInstaller --icon 打包！", bg="#1b2234", fg="#8ecae6", font=(ff, 9), wraplength=330)
        self.lbl_status.pack(pady=8)

    def pick_image(self):
        init_dir = os.path.join(BASE_DIR, "ws_card_images")
        p = filedialog.askopenfilename(
            initialdir=init_dir if os.path.exists(init_dir) else BASE_DIR,
            title="選擇要做為圖標的圖片",
            filetypes=[("Image Files", "*.webp;*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")],
        )
        if p and os.path.exists(p):
            self.src_img = Image.open(p).convert("RGBA")
            self.cx, self.cy, self.zoom = 0.50, 0.28, 1.95
            self.sc_zoom.set(self.zoom)
            self._redraw()

    def pick_outer_color(self):
        c = colorchooser.askcolor(color=self.ring_color, title="選擇外圈光環顏色")[1]
        if c:
            self.ring_color = c
            self._redraw()

    def pick_inner_color(self):
        c = colorchooser.askcolor(color=self.inner_color, title="選擇內圈光環顏色")[1]
        if c:
            self.inner_color = c
            self._redraw()

    def _on_drag(self, event):
        self.cx = max(0.05, min(0.95, event.x / float(self.cw)))
        self.cy = max(0.05, min(0.95, event.y / float(self.ch)))
        self._redraw()

    def _on_wheel(self, event):
        delta = 0.12 if event.delta > 0 else -0.12
        self.zoom = max(1.0, min(4.0, round(self.zoom + delta, 2)))
        self.sc_zoom.set(self.zoom)
        self._redraw()

    def _on_scale_zoom(self, val):
        self.zoom = float(val)
        self._redraw()

    def _redraw(self):
        disp = self.src_img.resize((self.cw, self.ch), Image.Resampling.LANCZOS).convert("RGBA")
        base_d = min(self.cw, self.ch)
        rad = max(16, int((base_d / max(0.6, self.zoom)) / 2))
        cx_px = max(rad, min(self.cw - rad, int(self.cw * self.cx)))
        cy_px = max(rad, min(self.ch - rad, int(self.ch * self.cy)))
        self.cx = cx_px / float(self.cw)
        self.cy = cy_px / float(self.ch)

        dim = Image.new("RGBA", (self.cw, self.ch), (10, 14, 24, 155))
        mask = Image.new("L", (self.cw, self.ch), 255)
        ImageDraw.Draw(mask).ellipse([cx_px - rad, cy_px - rad, cx_px + rad, cy_px + rad], fill=0)
        comp = Image.composite(dim, Image.new("RGBA", (self.cw, self.ch), (0, 0, 0, 0)), mask)
        merged = Image.alpha_composite(disp, comp).convert("RGB")
        d = ImageDraw.Draw(merged)
        d.ellipse([cx_px - rad, cy_px - rad, cx_px + rad, cy_px + rad], outline=self.ring_color, width=3)

        self.tk_canvas_img = ImageTk.PhotoImage(merged)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_canvas_img)

        # 右側棋盤格透明背景預覽
        p_sz = 180
        checker = Image.new("RGBA", (p_sz, p_sz), (255, 255, 255, 255))
        cd = ImageDraw.Draw(checker)
        step = 12
        for y in range(0, p_sz, step):
            for x in range(0, p_sz, step):
                col = (42, 48, 66, 255) if ((x // step + y // step) % 2 == 0) else (26, 30, 44, 255)
                cd.rectangle([x, y, x + step, y + step], fill=col)

        icon_pil = render_circular_transparent_icon(self.src_img, self.cx, self.cy, self.zoom, self.ring_color, self.inner_color, out_size=p_sz)
        preview_comp = Image.alpha_composite(checker, icon_pil).convert("RGB")
        self.tk_prev_img = ImageTk.PhotoImage(preview_comp)
        self.lbl_preview.config(image=self.tk_prev_img)
        self.lbl_zoom.config(text=f"縮放倍率：{self.zoom:.2f}x")

    def save_icon_files(self):
        out_ico = filedialog.asksaveasfilename(
            initialdir=BASE_DIR,
            initialfile="my_custom_icon.ico",
            title="儲存 .ico 圖標檔",
            defaultextension=".ico",
            filetypes=[("Windows Icon (.ico)", "*.ico")],
        )
        if not out_ico:
            return
        hi_icon = render_circular_transparent_icon(self.src_img, self.cx, self.cy, self.zoom, self.ring_color, self.inner_color, out_size=512)
        save_win32_dib_ico(hi_icon, out_ico)
        png_path = os.path.splitext(out_ico)[0] + ".png"
        hi_icon.save(png_path, format="PNG")
        self.lbl_status.config(text=f"✔ 已成功匯出圖標：{os.path.basename(out_ico)} 與去背 {os.path.basename(png_path)}！", fg="#06d6a0")

    def overwrite_game_icon(self):
        hi_icon = render_circular_transparent_icon(self.src_img, self.cx, self.cy, self.zoom, self.ring_color, self.inner_color, out_size=512)
        ico_p = os.path.join(BASE_DIR, "maple_icon.ico")
        png_p = os.path.join(BASE_DIR, "maple_icon.png")
        save_win32_dib_ico(hi_icon, ico_p)
        hi_icon.save(png_p, format="PNG")
        self.lbl_status.config(text="✔ 已成功更新遊戲預設圖標 maple_icon.ico 與 maple_icon.png！", fg="#06d6a0")


if __name__ == "__main__":
    r = tk.Tk()
    app = IconMakerApp(r)
    r.mainloop()
