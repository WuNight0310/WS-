# -*- coding: utf-8 -*-
"""
🌐 貓罐子 (BottleNeko) 全系列免組牌抓取 ／ 每次 20 張分批匯入 ＆ 萬用效果 AST 編譯工具
執行方式：
  1. 直接雙擊執行本檔案，或在終端機輸入：
     - 抓整個系列：python 匯入貓罐子牌組工具.py https://bottleneko.app/ws/series/172
     - 每次抓 20 張：python 匯入貓罐子牌組工具.py https://bottleneko.app/ws/series/172 --batch 20 --offset 0
  2. 也可直接從遊戲主選單點擊【🌐 貓罐子匯入 ＆ 萬用效果除錯】按鈕，在視窗內直接搜尋貓罐子全部 170+ 個系列並點選【📦 分批抓取 20 張】或【🚀 一次抓完整個系列】！
"""
import sys
from engine import BottleNekoImporter


def main():
    print("=" * 72)
    print("  🌐 Weiß Schwarz 貓罐子 (BottleNeko) 全系列免組牌 ／ 20張分批匯入工具")
    print("=" * 72)
    args = sys.argv[1:]
    if not args:
        print("請選擇操作模式：")
        print("  [1] 列出／搜尋貓罐子全部系列清單 (免組牌直接挑系列)")
        print("  [2] 輸入貓罐子系列網址 (例 https://bottleneko.app/ws/series/172) 或系列編號")
        print("  [3] 輸入貓罐子牌組網址 (例 https://bottleneko.app/ws/deck/wMI7n)")
        mode = input("> ").strip()
        if mode == "1":
            kw = input("請輸入系列關鍵字（直接按 Enter 列出前 30 個）：").strip().lower()
            cats = BottleNekoImporter.fetch_all_series_catalog()
            matches = [c for c in cats if not kw or kw in c["display"].lower() or kw in c["jp_name"].lower()]
            for c in matches[:40]:
                print(" ", c["display"])
            sid = input("\n請輸入要匯入的系列編號 (例如 172)：").strip()
            if not sid:
                return
            b_mode = input("要 [A] 一次抓完整個系列，還是 [B] 每次 20 張分批抓？(輸入 A 或 B，預設 A)：").strip().upper()
            if b_mode == "B":
                off = 0
                while True:
                    res = BottleNekoImporter.import_series_by_id(sid, batch_offset=off, batch_limit=20)
                    off = res["next_offset"]
                    if off >= res["total_available"]:
                        print("🎉 全系列已全數抓取完畢！")
                        break
                    cont = input(f"目前已抓到 {off}/{res['total_available']} 張，繼續抓下 20 張嗎？(Y/n)：").strip().lower()
                    if cont == "n":
                        break
            else:
                BottleNekoImporter.import_series_by_id(sid, batch_offset=0, batch_limit=0)
            return
        target = input("請貼上貓罐子系列網址、系列編號或牌組網址：\n> ").strip()
    else:
        target = args[0]

    if not target:
        return
    try:
        res = BottleNekoImporter.import_from_url_or_json(target, sets_dir="sets")
        print("\n🎉 匯入與萬用效果編譯成功！")
        print(f"  - 系列代碼：{res['series_code']}")
        print(f"  - 名稱：{res['deck_name']}")
        print(f"  - 本次匯入張數：{res['card_count']} 張")
        print(f"  - 儲存路徑：{res['file_path']}")
    except Exception as e:
        print(f"\n❌ 匯入失敗：{e}")


if __name__ == "__main__":
    main()
