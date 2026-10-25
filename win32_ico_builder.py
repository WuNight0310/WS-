# -*- coding: utf-8 -*-
"""
標準 Win32 PE 圖標 (BITMAPINFOHEADER DIB + 256px PNG) 產生器
解決 Python Pillow 預設輸出全 PNG 壓縮 ICO 導致 Windows 檔案總管「詳細資料 (16x16)」檢視下無法顯示 EXE 小圖標的問題。
"""
import io
import os
import struct
from PIL import Image


def save_win32_dib_ico(img: Image.Image, out_path: str):
    rgba = img.convert("RGBA")
    dib_sizes = [16, 20, 24, 32, 48, 64]
    entries = []
    payloads = []

    for sz in dib_sizes:
        im_s = rgba.resize((sz, sz), Image.Resampling.LANCZOS)
        raw_rgba = im_s.tobytes()
        xor_rows = []
        and_rows = []
        and_row_bytes = ((sz + 31) // 32) * 4

        for y in range(sz - 1, -1, -1):
            row_bgra = bytearray()
            and_row = bytearray(and_row_bytes)
            for x in range(sz):
                idx = (y * sz + x) * 4
                r, g, b, a = raw_rgba[idx], raw_rgba[idx + 1], raw_rgba[idx + 2], raw_rgba[idx + 3]
                row_bgra.extend((b, g, r, a))
                if a == 0:
                    byte_i = x // 8
                    bit_i = 7 - (x % 8)
                    and_row[byte_i] |= (1 << bit_i)
            xor_rows.append(bytes(row_bgra))
            and_rows.append(bytes(and_row))

        xor_data = b"".join(xor_rows)
        and_data = b"".join(and_rows)
        bih = struct.pack(
            "<IIIHHIIIIII",
            40,
            sz,
            sz * 2,
            1,
            32,
            0,
            len(xor_data) + len(and_data),
            0, 0, 0, 0
        )
        block = bih + xor_data + and_data
        entries.append((sz, sz, 32, len(block)))
        payloads.append(block)

    im_256 = rgba.resize((256, 256), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im_256.save(buf, format="PNG")
    png_256 = buf.getvalue()
    entries.append((0, 0, 32, len(png_256)))
    payloads.append(png_256)

    header = struct.pack("<HHH", 0, 1, len(entries))
    dir_offset = 6 + 16 * len(entries)
    dir_bytes = bytearray()
    for (w, h, bpp, length) in entries:
        dir_bytes.extend(struct.pack("<BBBBHHII", w, h, 0, 0, 1, bpp, length, dir_offset))
        dir_offset += length

    with open(out_path, "wb") as f:
        f.write(header)
        f.write(dir_bytes)
        for p in payloads:
            f.write(p)


if __name__ == "__main__":
    for cand in ("maple_icon.png", "maple_angel_icon.png"):
        if os.path.exists(cand):
            im = Image.open(cand)
            save_win32_dib_ico(im, "maple_icon.ico")
            print(f"✔ 已由 {cand} 建立真實 Win32 DIB 格式的 maple_icon.ico (含 16/20/24/32/48/64px DIB 與 256px PNG)！")
            break
