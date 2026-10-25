import io
import json
import os
import random
import re
import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import urllib.request
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageTk

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != BASE_DIR:
    os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def _ensure_assets_from_zip():
    need_extract = (
        (not getattr(sys, "frozen", False) and not os.path.exists(os.path.join(BASE_DIR, "main.py")))
        or not os.path.exists(os.path.join(BASE_DIR, "sets", "GA_S131.json"))
        or not os.path.exists(os.path.join(BASE_DIR, "sets", "BTR_W107.json"))
    )
    if not need_extract:
        return
    import zipfile
    search_dirs = [
        BASE_DIR,
        os.path.dirname(BASE_DIR),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
    ]
    for sdir in search_dirs:
        if not sdir or not os.path.exists(sdir):
            continue
        try:
            for fname in os.listdir(sdir):
                if fname.lower().endswith(".zip"):
                    zpath = os.path.join(sdir, fname)
                    try:
                        with zipfile.ZipFile(zpath, "r") as zf:
                            names = zf.namelist()
                            if any(n.endswith("BTR_W107.json") or n.endswith("GA_S131.json") or n.endswith("BFR_S78.json") for n in names):
                                zf.extractall(BASE_DIR)
                                return
                    except Exception:
                        pass
        except Exception:
            pass

_ensure_assets_from_zip()


try:
    import requests
except ImportError:
    requests = None

try:
    from engine import (
    ChineseEffectParser,
    BottleNekoImporter,
        CARD_DB,
        DEFAULT_DECK_RECIPE,
        SERIES_DB,
        SERIES_DEFAULT_DECKS,
        SERIES_LABELS,
        CardInstance,
        PlayerState,
        RuleEngine,
        load_all_card_sets,
    )
except ImportError:
    import glob
    import json
    import os
    import random
    import sys

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != BASE_DIR:
        os.chdir(BASE_DIR)
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    def _ensure_assets_from_zip():
        need_extract = (
            (not getattr(sys, "frozen", False) and not os.path.exists(os.path.join(BASE_DIR, "main.py")))
            or not os.path.exists(os.path.join(BASE_DIR, "sets", "GA_S131.json"))
        or not os.path.exists(os.path.join(BASE_DIR, "sets", "BTR_W107.json"))
            or not os.path.exists(os.path.join(BASE_DIR, "sets", "BTR_W107.json"))
        )
        if not need_extract:
            return
        import zipfile
        search_dirs = [
            BASE_DIR,
            os.path.dirname(BASE_DIR),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
        ]
        for sdir in search_dirs:
            if not sdir or not os.path.exists(sdir):
                continue
            try:
                for fname in os.listdir(sdir):
                    if fname.lower().endswith(".zip"):
                        zpath = os.path.join(sdir, fname)
                        try:
                            with zipfile.ZipFile(zpath, "r") as zf:
                                names = zf.namelist()
                                if any(n.endswith("BTR_W107.json") or n.endswith("GA_S131.json") or n.endswith("BFR_S78.json") for n in names):
                                    zf.extractall(BASE_DIR)
                                    return
                        except Exception:
                            pass
            except Exception:
                pass

    _ensure_assets_from_zip()
    FALLBACK_CARD_DB = {'BFR/S78-076': {'id': 'BFR/S78-076', 'name': '公會長之間的對決', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 2, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-076', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-076R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076.png', 'https://img.bottleneko.app/BFR_S78_076.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076.png']}, 'BFR/S78-076R': {'id': 'BFR/S78-076R', 'name': '公會長之間的對決', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-076', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-076R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076R.png', 'https://img.bottleneko.app/BFR_S78_076R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_076R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076r.gif']}, 'BFR/S78-077': {'id': 'BFR/S78-077', 'name': 'Boss級怪物', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 2, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-077', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-077R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077.png', 'https://img.bottleneko.app/BFR_S78_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077.png']}, 'BFR/S78-077R': {'id': 'BFR/S78-077R', 'name': 'Boss級怪物', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-077', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-077R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077R.png', 'https://img.bottleneko.app/BFR_S78_077R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_077R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077r.gif']}, 'BFR/S78-078': {'id': 'BFR/S78-078', 'name': '炎帝之國的公會長', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 2, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-078', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-078R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078.png', 'https://img.bottleneko.app/BFR_S78_078.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078.png']}, 'BFR/S78-078R': {'id': 'BFR/S78-078R', 'name': '炎帝之國的公會長', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-078', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-078R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078R.png', 'https://img.bottleneko.app/BFR_S78_078R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_078R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078r.gif']}, 'BFR/S78-107': {'id': 'BFR/S78-107', 'name': '展開．左手', 'type': 'CX', 'color': '藍', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'GATE', 'traits': [], 'default_count': 2, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n城門：當你判定出此卡時，你可以選擇自己休息室的1張名場面，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-107', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-107R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107.png', 'https://img.bottleneko.app/BFR_S78_107.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107.png']}, 'BFR/S78-107R': {'id': 'BFR/S78-107R', 'name': '展開．左手', 'type': 'CX', 'color': '藍', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'GATE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n城門：當你判定出此卡時，你可以選擇自己休息室的1張名場面，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-107', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-107R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107R.png', 'https://img.bottleneko.app/BFR_S78_107R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_107R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107r.gif']}, 'BFR/S78-075': {'id': 'BFR/S78-075', 'name': '獨有系列', 'type': 'EVENT', 'color': '紅', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 2, 'effects': ['EVENT_COUNTER_2500_MEMORY', 'MEMORY_MAIN_START_RETURN'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_075.png', 'text': '【反擊】你選擇自己的《遊戲》的角色1張，在那個回合中，攻擊力+2500。將此卡放到回憶區。\n【自】記憶 ［手牌的《遊戲》的角色1張放到休息室］ 在你的主要階段開始時，回憶區有此卡存在的話，你可以支付代價。支付代價的話，將此卡返回手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-075', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_075.png', 'https://img.bottleneko.app/BFR_S78_075.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_075.png']}, 'BFR/S78-015': {'id': 'BFR/S78-015', 'name': '雙胞胎的妹妹 結衣', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 3000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '雙胞胎'], 'default_count': 2, 'effects': ['CONT_CANNOT_SIDE_ATTACK', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_015.png', 'text': '【永】此卡不能側打。\n【自】［(1) 手牌1張名場面放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-015', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_015.png', 'https://img.bottleneko.app/BFR_S78_015.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_015.png']}, 'BFR/S78-001': {'id': 'BFR/S78-001', 'name': '戰鬥的工匠 伊茲', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '鍛造'], 'default_count': 3, 'effects': ['AUTO_ON_PLAY_CLOCK_SEARCH_LV1', 'AUTO_OTHER_REVERSE_BUFF_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇等級1以下的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。\n【自】其他的你的角色的戰鬥對手【倒置】時，在那個回合中，此卡的攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-001', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-001SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001.png', 'https://img.bottleneko.app/BFR_S78_001.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001.png']}, 'BFR/S78-001SP': {'id': 'BFR/S78-001SP', 'name': '戰鬥的工匠 伊茲', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '鍛造'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_CLOCK_SEARCH_LV1', 'AUTO_OTHER_REVERSE_BUFF_1000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001SP.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇等級1以下的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。\n【自】其他的你的角色的戰鬥對手【倒置】時，在那個回合中，此卡的攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-001', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-001SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001SP.png', 'https://img.bottleneko.app/BFR_S78_001SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_001SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001S.png', 'https://img.bottleneko.app/BFR_S78_001S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_001S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001s.gif']}, 'BFR/S78-031': {'id': 'BFR/S78-031', 'name': '多彩多樣 莎莉', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 3, 'effects': ['CONT_IGNORE_CX_COLOR', 'AUTO_ON_CX_LOOT', 'ACT_CONCENTRATE_SINGLE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031.png', 'text': '【永】你的名場面可以無需滿足顏色條件從手牌使用。\n【自】［手牌1張放到休息室］ 當你的名場面被放置到名場面區時，你可以支付代價。支付代價的話，你抽1張牌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻4張，放到休息室。那些卡片中每有1張名場面，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-031', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-031SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031.png', 'https://img.bottleneko.app/BFR_S78_031.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031.png']}, 'BFR/S78-031SP': {'id': 'BFR/S78-031SP', 'name': '多彩多樣 莎莉', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 0, 'effects': ['CONT_IGNORE_CX_COLOR', 'AUTO_ON_CX_LOOT', 'ACT_CONCENTRATE_SINGLE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031SP.png', 'text': '【永】你的名場面可以無需滿足顏色條件從手牌使用。\n【自】［手牌1張放到休息室］ 當你的名場面被放置到名場面區時，你可以支付代價。支付代價的話，你抽1張牌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻4張，放到休息室。那些卡片中每有1張名場面，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-031', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-031SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031SP.png', 'https://img.bottleneko.app/BFR_S78_031SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_031SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031S.png', 'https://img.bottleneko.app/BFR_S78_031S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_031S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031s.gif']}, 'BFR/S78-062': {'id': 'BFR/S78-062', 'name': '咬咬 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 3, 'effects': ['AUTO_STAGE_TO_WR_LOOK4_STEPWISE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062.png', 'text': '【自】［手牌1張放到休息室］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-062', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-062S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062.png', 'https://img.bottleneko.app/BFR_S78_062.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062.png']}, 'BFR/S78-062S': {'id': 'BFR/S78-062S', 'name': '咬咬 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_STAGE_TO_WR_LOOK4_STEPWISE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062S.png', 'text': '【自】［手牌1張放到休息室］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-062', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-062S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062S.png', 'https://img.bottleneko.app/BFR_S78_062S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_062S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062s.gif']}, 'BFR/S78-061': {'id': 'BFR/S78-061', 'name': '作戰變更 米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['ACT_MARKER_OR_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_061.png', 'text': '【起】［將此卡【橫置】］ 此卡下方沒有標記的話，你將自己的牌組上方1張公開。那張卡片的等級是1以上的話作為標記以裏側表示放到此卡下方。名場面的等級視為0。如果不是的話放回原位。\n【起】［將此卡【橫置】］ 你將此卡下方的標記1張放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-061', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_061.png', 'https://img.bottleneko.app/BFR_S78_061.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_061.png']}, 'BFR/S78-060': {'id': 'BFR/S78-060', 'name': '焰火飛馳 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 3, 'effects': ['AUTO_ON_PLAY_DEBUFF_AND_SEARCH'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手前列的角色1張，在那個回合中，攻擊力-1000。\n【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-060', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-060S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060.png', 'https://img.bottleneko.app/BFR_S78_060.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060.png']}, 'BFR/S78-060S': {'id': 'BFR/S78-060S', 'name': '焰火飛馳 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DEBUFF_AND_SEARCH'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060S.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手前列的角色1張，在那個回合中，攻擊力-1000。\n【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-060', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-060S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060S.png', 'https://img.bottleneko.app/BFR_S78_060S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_060S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060s.gif']}, 'BFR/S78-083': {'id': 'BFR/S78-083', 'name': '情報戰 莎莉', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_SCRY2_AND_GUESS_DRAW'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_083.png', 'text': '【自】此卡從手牌被放置到舞台時，你看自己的牌組上方最多2張，以任意順序放回牌組上方。\n【自】此卡從手牌被放置到舞台時，對手宣言0或1或2或3。你將自己的牌組上方1張，放到休息室，那張卡片是對手宣言的等級的卡片的話，你抽最多X張牌。X等於對手宣言的數字+1。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-083', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_083.png', 'https://img.bottleneko.app/BFR_S78_083.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_083.png']}, 'BFR/S78-073': {'id': 'BFR/S78-073', 'name': '不屈的守護者 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 3, 'effects': ['CONT_OTHER_2GAME_BUFF_2000', 'AUTO_HAND_ENCORE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_073.png', 'text': '【永】其他的你的《遊戲》的角色存在2張以上的話，此卡的攻擊力+2000。\n【自】安可 ［手牌的角色1張放到休息室］', 'series': 'BFR/S78', 'base_id': 'BFR/S78-073', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_073.png', 'https://img.bottleneko.app/BFR_S78_073.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_073.png']}, 'BFR/S78-057': {'id': 'BFR/S78-057', 'name': '移動要塞 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 4, 'effects': ['AUTO_ON_PLAY_BUFF_1500', 'CX_COMBO_ATK_START_STAND_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】【CX連動】 ［手牌的「移動要塞 梅普露」1張放到休息室，你的名場面區的「公會長之間的對決」1張放到休息室］ 在你的攻擊階段開始時，此卡存在於前列的話，你可以支付代價。支付代價的話，你選擇其他的自己的《遊戲》的角色最多1張，【正置】，選擇自己休息室的《遊戲》的角色最多1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-057', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-057SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057.png', 'https://img.bottleneko.app/BFR_S78_057.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057.png']}, 'BFR/S78-057SP': {'id': 'BFR/S78-057SP', 'name': '移動要塞 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_BUFF_1500', 'CX_COMBO_ATK_START_STAND_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057SP.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】【CX連動】 ［手牌的「移動要塞 梅普露」1張放到休息室，你的名場面區的「公會長之間的對決」1張放到休息室］ 在你的攻擊階段開始時，此卡存在於前列的話，你可以支付代價。支付代價的話，你選擇其他的自己的《遊戲》的角色最多1張，【正置】，選擇自己休息室的《遊戲》的角色最多1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-057', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-057SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057SP.png', 'https://img.bottleneko.app/BFR_S78_057SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_057SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057S.png', 'https://img.bottleneko.app/BFR_S78_057S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_057S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057s.gif']}, 'BFR/S78-102': {'id': 'BFR/S78-102', 'name': '通往勝利的方程式 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 1, 'cost': 1, 'power': 3000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['CONT_LEVEL_ASSIST', 'AUTO_ON_ACT_BUFF_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_102.png', 'text': '【永】應援 此卡前面的你的《遊戲》的角色全部，攻擊力+X。X等於那張角色的等級×500。\n【自】此能力每1回合最多發動1次。當你使用【起】的時候，你選擇自己的角色1張，在那個回合中，攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-102', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_102.png', 'https://img.bottleneko.app/BFR_S78_102.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_102.png']}, 'BFR/S78-087': {'id': 'BFR/S78-087', 'name': '盾與盾 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_FORCE_OPP_SWAP'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_087.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇對手的等級1以上的角色1張，對手選擇自己休息室的等級X以下的角色1張，交換位置。X等於你選擇的角色的等級-1。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-087', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_087.png', 'https://img.bottleneko.app/BFR_S78_087.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_087.png']}, 'BFR/S78-072': {'id': 'BFR/S78-072', 'name': '火炎牢 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_SCALING_BUFF_AND_LOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_072.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於你的《遊戲》的角色張數×500。\n【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，在那個回合中，給予以下能力。『【永】此卡不能回到手牌，不能放到回憶區。』', 'series': 'BFR/S78', 'base_id': 'BFR/S78-072', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_072.png', 'https://img.bottleneko.app/BFR_S78_072.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_072.png']}, 'BFR/S78-058': {'id': 'BFR/S78-058', 'name': '聖女米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 1, 'effects': ['CONT_ALL_GAME_BUFF_3000', 'AUTO_DIRECT_ATK_STOCK_CHARGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058.png', 'text': '【永】你的角色全部都是《遊戲》的話，此卡的攻擊力+3000。\n【自】此卡直接攻擊時，你可以選擇自己休息室的《遊戲》的角色1張，放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-058', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-058SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058.png', 'https://img.bottleneko.app/BFR_S78_058.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058.png']}, 'BFR/S78-058SP': {'id': 'BFR/S78-058SP', 'name': '聖女米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['CONT_ALL_GAME_BUFF_3000', 'AUTO_DIRECT_ATK_STOCK_CHARGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058SP.png', 'text': '【永】你的角色全部都是《遊戲》的話，此卡的攻擊力+3000。\n【自】此卡直接攻擊時，你可以選擇自己休息室的《遊戲》的角色1張，放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-058', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-058SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058SP.png', 'https://img.bottleneko.app/BFR_S78_058SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_058SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058S.png', 'https://img.bottleneko.app/BFR_S78_058S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_058S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058s.gif']}, 'BFR/S78-069': {'id': 'BFR/S78-069', 'name': '被託付的生命 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 1, 'effects': ['AUTO_FRONT_ATK_LOWER_LEVEL', 'AUTO_REVERSE_BOMB_LV2'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_069.png', 'text': '【自】［(1)］ 此卡正打時，你可以支付代價。支付代價的話，你選擇對手的角色1張，在那個回合中，等級-1。\n【自】此卡【倒置】時，此卡的戰鬥對手是等級2以下的話，你可以將那張角色【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-069', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_069.png', 'https://img.bottleneko.app/BFR_S78_069.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_069.png']}, 'BFR/S78-089': {'id': 'BFR/S78-089', 'name': '大摯友 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 1, 'effects': ['CONT_OPP_BACKROW_BUFF_1500', 'AUTO_DEFEND_IMMUNE_REVERSE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089.png', 'text': '【永】對手的後列的角色每有1張，此卡的攻擊力+1500。\n【自】［(1) 手牌的《遊戲》的角色1張放到休息室］ 此卡被正打時，你可以支付代價。支付代價的話，在那個回合中，此卡不會【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-089', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-089S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089.png', 'https://img.bottleneko.app/BFR_S78_089.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089.png']}, 'BFR/S78-089S': {'id': 'BFR/S78-089S', 'name': '大摯友 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['CONT_OPP_BACKROW_BUFF_1500', 'AUTO_DEFEND_IMMUNE_REVERSE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089S.png', 'text': '【永】對手的後列的角色每有1張，此卡的攻擊力+1500。\n【自】［(1) 手牌的《遊戲》的角色1張放到休息室］ 此卡被正打時，你可以支付代價。支付代價的話，在那個回合中，此卡不會【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-089', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-089S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089S.png', 'https://img.bottleneko.app/BFR_S78_089S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_089S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089s.gif']}, 'BFR/S78-063': {'id': 'BFR/S78-063', 'name': '暴虐 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_3000_AND_SALVAGE_CX', 'CX_COMBO_REVERSE_BURN_1_2_3'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。\n【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。\n【自】【CX連動】 ［(6) 手牌2張放到休息室，你的名場面區的「Boss級怪物」1張放到休息室］ 此卡的戰鬥對手【倒置】時，你可以支付代價。支付代價的話，給對手1點傷害，給對手2點傷害，給對手3點傷害。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-063', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-063S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063.png', 'https://img.bottleneko.app/BFR_S78_063.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063.png']}, 'BFR/S78-063S': {'id': 'BFR/S78-063S', 'name': '暴虐 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_3000_AND_SALVAGE_CX', 'CX_COMBO_REVERSE_BURN_1_2_3'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063S.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。\n【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。\n【自】【CX連動】 ［(6) 手牌2張放到休息室，你的名場面區的「Boss級怪物」1張放到休息室］ 此卡的戰鬥對手【倒置】時，你可以支付代價。支付代價的話，給對手1點傷害，給對手2點傷害，給對手3點傷害。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-063', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-063S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063S.png', 'https://img.bottleneko.app/BFR_S78_063S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063SEC.png', 'https://img.bottleneko.app/BFR_S78_063SEC.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063SEC.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sec.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sec.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063SP.png', 'https://img.bottleneko.app/BFR_S78_063SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sp.gif']}, 'BFR/S78-064': {'id': 'BFR/S78-064', 'name': '炎帝 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_HEAL', 'CX_COMBO_STANDBY_STAND'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064.png', 'text': '【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】【CX連動】 ［手牌的《遊戲》的角色3張放到休息室］ 此卡因為「炎帝之國的公會長」的效果被放到舞台時，你可以支付代價。支付代價的話，將此卡【正置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-064', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-064S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064.png', 'https://img.bottleneko.app/BFR_S78_064.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064.png']}, 'BFR/S78-064S': {'id': 'BFR/S78-064S', 'name': '炎帝 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_HEAL', 'CX_COMBO_STANDBY_STAND'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064S.png', 'text': '【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】【CX連動】 ［手牌的《遊戲》的角色3張放到休息室］ 此卡因為「炎帝之國的公會長」的效果被放到舞台時，你可以支付代價。支付代價的話，將此卡【正置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-064', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-064S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064S.png', 'https://img.bottleneko.app/BFR_S78_064S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_064S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064SP.png', 'https://img.bottleneko.app/BFR_S78_064SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_064SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064sp.gif']}, 'BFR/S78-081': {'id': 'BFR/S78-081', 'name': '天才少年 奏', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '武器'], 'default_count': 1, 'effects': ['CONT_EARLY_PLAY_4GAME', 'AUTO_ON_PLAY_HEAL', 'AUTO_ON_PLAY_OTHER_GAME_2000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081.png', 'text': '【永】你的《遊戲》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，有其他的你的《遊戲》的角色存在的話，在那個回合中，此卡的攻擊力+2000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-081', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-081SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081.png', 'https://img.bottleneko.app/BFR_S78_081.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081.png']}, 'BFR/S78-081SP': {'id': 'BFR/S78-081SP', 'name': '天才少年 奏', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '武器'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4GAME', 'AUTO_ON_PLAY_HEAL', 'AUTO_ON_PLAY_OTHER_GAME_2000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081SP.png', 'text': '【永】你的《遊戲》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，有其他的你的《遊戲》的角色存在的話，在那個回合中，此卡的攻擊力+2000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-081', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-081SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081SP.png', 'https://img.bottleneko.app/BFR_S78_081SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_081SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081S.png', 'https://img.bottleneko.app/BFR_S78_081S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_081S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081s.gif']}, 'BFR/S78-082': {'id': 'BFR/S78-082', 'name': '機械神 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_RESHUFFLE_OPP_STOCK', 'CX_COMBO_ATK_BOTTOM_MILL4_BURN'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082.png', 'text': '【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手將自己的能量區全部，放到休息室，從自己的牌組上方將相同張數放到能量區。\n【自】【CX連動】 此卡攻擊時，名場面區有「展開．左手」的話，你將對手的牌組下方4張，放到休息室，給對手X點傷害。X等於那些卡片中的名場面張數。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-082', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-082SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082.png', 'https://img.bottleneko.app/BFR_S78_082.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082.png']}, 'BFR/S78-082SP': {'id': 'BFR/S78-082SP', 'name': '機械神 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_RESHUFFLE_OPP_STOCK', 'CX_COMBO_ATK_BOTTOM_MILL4_BURN'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082SP.png', 'text': '【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手將自己的能量區全部，放到休息室，從自己的牌組上方將相同張數放到能量區。\n【自】【CX連動】 此卡攻擊時，名場面區有「展開．左手」的話，你將對手的牌組下方4張，放到休息室，給對手X點傷害。X等於那些卡片中的名場面張數。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-082', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-082SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082SP.png', 'https://img.bottleneko.app/BFR_S78_082SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_082SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082S.png', 'https://img.bottleneko.app/BFR_S78_082S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_082S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082s.gif']}, 'GA10/S131-030': {'id': 'GA10/S131-030', 'series': 'GA/S131', 'name': '時隔五年的【能力值】更新', 'jp_name': '五年振りの【ステイタス】更新', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 4, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA10/S131-030', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'GA10/S131-030R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030.png', 'https://img.bottleneko.app/GA10_S131_030.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030.png']}, 'GA10/S131-030R': {'id': 'GA10/S131-030R', 'series': 'GA/S131', 'name': '時隔五年的【能力值】更新', 'jp_name': '五年振りの【ステイタス】更新', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA10/S131-030', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'GA10/S131-030R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030R.png', 'https://img.bottleneko.app/GA10_S131_030R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_030R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030r.gif']}, 'GA17/S131-033': {'id': 'GA17/S131-033', 'series': 'GA/S131', 'name': '灰之魔女', 'jp_name': '灰の魔女', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 4, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA17/S131-033', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'GA17/S131-033R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033.png', 'https://img.bottleneko.app/GA17_S131_033.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033.png']}, 'GA17/S131-033R': {'id': 'GA17/S131-033R', 'series': 'GA/S131', 'name': '灰之魔女', 'jp_name': '灰の魔女', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA17/S131-033', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'GA17/S131-033R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033R.png', 'https://img.bottleneko.app/GA17_S131_033R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_033R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033r.gif']}, 'GA05/S131-007': {'id': 'GA05/S131-007', 'series': 'GA/S131', 'name': '〈迪亞馬特〉的使用者 莉姿夏爾蒂·亞提司瑪特', 'jp_name': '《ティアマト》の使い手 リーズシャルテ・アティスマータ', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '王族', '機龍'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_LOCK_MOVE', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，到下次的對手回合結束前，給予以下能力。『【永】此卡不能移動到其他格子。』\n【自】［(1) 手牌的CX1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA05/S131-007', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA05/S131-007SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007.png', 'https://img.bottleneko.app/GA05_S131_007.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007.png']}, 'GA05/S131-007SP': {'id': 'GA05/S131-007SP', 'series': 'GA/S131', 'name': '〈迪亞馬特〉的使用者 莉姿夏爾蒂·亞提司瑪特', 'jp_name': '《ティアマト》の使い手 リーズシャルテ・アティスマータ', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '王族', '機龍'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_LOCK_MOVE', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007SP.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，到下次的對手回合結束前，給予以下能力。『【永】此卡不能移動到其他格子。』\n【自】［(1) 手牌的CX1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA05/S131-007', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA05/S131-007SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007SP.png', 'https://img.bottleneko.app/GA05_S131_007SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA05_S131_007SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga05_s131/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007S.png', 'https://img.bottleneko.app/GA05_S131_007S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA05_S131_007S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga05_s131/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007s.gif']}, 'GA08/S131-038': {'id': 'GA08/S131-038', 'series': 'GA/S131', 'name': '魔族農業大臣 別西卜', 'jp_name': '魔族の農相 ベルゼブブ', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔族', '農家'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_DOKITEMA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA08/S131-038', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA08/S131-038SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038.png', 'https://img.bottleneko.app/GA08_S131_038.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038.png']}, 'GA08/S131-038SP': {'id': 'GA08/S131-038SP', 'series': 'GA/S131', 'name': '魔族農業大臣 別西卜', 'jp_name': '魔族の農相 ベルゼブブ', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔族', '農家'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DOKITEMA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038SP.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA08/S131-038', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA08/S131-038SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038SP.png', 'https://img.bottleneko.app/GA08_S131_038SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA08_S131_038SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga08_s131/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038S.png', 'https://img.bottleneko.app/GA08_S131_038S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA08_S131_038S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga08_s131/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038s.gif']}, 'GA10/S131-012': {'id': 'GA10/S131-012', 'series': 'GA/S131', 'name': '奇怪的妖精 琉', 'jp_name': '変り種のエルフ リュー', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 3, 'effects': ['CONT_CHOICE_CX_GIVES_WIND', 'ACT_CONCENTRATE_5_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，給予你的所有的領域的黃色的CX風的判定標誌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻出5張，放到休息室。那些卡片中每有1張判定標誌是箭頭的CX，你選擇自己休息室的角色最多1張，回到手牌。', 'base_id': 'GA10/S131-012', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-012GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012.png', 'https://img.bottleneko.app/GA10_S131_012.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012.png']}, 'GA10/S131-012GA': {'id': 'GA10/S131-012GA', 'series': 'GA/S131', 'name': '奇怪的妖精 琉', 'jp_name': '変り種のエルフ リュー', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 0, 'effects': ['CONT_CHOICE_CX_GIVES_WIND', 'ACT_CONCENTRATE_5_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012GA.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，給予你的所有的領域的黃色的CX風的判定標誌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻出5張，放到休息室。那些卡片中每有1張判定標誌是箭頭的CX，你選擇自己休息室的角色最多1張，回到手牌。', 'base_id': 'GA10/S131-012', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA10/S131-012GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012GA.png', 'https://img.bottleneko.app/GA10_S131_012GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_012GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012S.png', 'https://img.bottleneko.app/GA10_S131_012S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_012S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012s.gif']}, 'GA10/S131-T09': {'id': 'GA10/S131-T09', 'series': 'GA/S131', 'name': '女神之鐘 赫斯緹雅', 'jp_name': '女神のカンパネラ ヘスティア', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '眷族', '神'], 'default_count': 3, 'effects': ['CONT_HAND5_BUFF_2000', 'AUTO_ATK_TWIN_DRIVE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09.png', 'text': '【永】在你的回合中，你的手牌有5張以上的話，此卡的攻擊力+2000。\n【自】［(1)］ 此卡攻擊時，你可以支付代價。支付代價的話，在那次攻擊中，你在判定階段執行2次判定。', 'base_id': 'GA10/S131-T09', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-T09TDP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09.png', 'https://img.bottleneko.app/GA10_S131_T09.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09.png']}, 'GA10/S131-T09TDP': {'id': 'GA10/S131-T09TDP', 'series': 'GA/S131', 'name': '女神之鐘 赫斯緹雅', 'jp_name': '女神のカンパネラ ヘスティア', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '眷族', '神'], 'default_count': 0, 'effects': ['CONT_HAND5_BUFF_2000', 'AUTO_ATK_TWIN_DRIVE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09TDP.png', 'text': '【永】在你的回合中，你的手牌有5張以上的話，此卡的攻擊力+2000。\n【自】［(1)］ 此卡攻擊時，你可以支付代價。支付代價的話，在那次攻擊中，你在判定階段執行2次判定。', 'base_id': 'GA10/S131-T09', 'is_high_rarity': True, 'rarity': 'TDP', 'high_rarity_id': 'GA10/S131-T09TDP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09TDP.png', 'https://img.bottleneko.app/GA10_S131_T09TDP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09TDP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09tdp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09SP.png', 'https://img.bottleneko.app/GA10_S131_T09SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09R.png', 'https://img.bottleneko.app/GA10_S131_T09R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09S.png', 'https://img.bottleneko.app/GA10_S131_T09S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09s.gif']}, 'GA12/S131-013': {'id': 'GA12/S131-013', 'series': 'GA/S131', 'name': '朋友的話是當然的 月之森真白', 'jp_name': '友達ならトーゼン 月ノ森真白', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '學生'], 'default_count': 4, 'effects': ['CONT_GAIN_CHOICE_TRIGGER', 'AUTO_ON_PLAY_BUFF_3000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，所有的領域的此卡獲得箭頭的判定標誌。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。', 'base_id': 'GA12/S131-013', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA12/S131-013GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013.png', 'https://img.bottleneko.app/GA12_S131_013.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013.png']}, 'GA12/S131-013GA': {'id': 'GA12/S131-013GA', 'series': 'GA/S131', 'name': '朋友的話是當然的 月之森真白', 'jp_name': '友達ならトーゼン 月ノ森真白', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '學生'], 'default_count': 0, 'effects': ['CONT_GAIN_CHOICE_TRIGGER', 'AUTO_ON_PLAY_BUFF_3000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013GA.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，所有的領域的此卡獲得箭頭的判定標誌。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。', 'base_id': 'GA12/S131-013', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA12/S131-013GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013GA.png', 'https://img.bottleneko.app/GA12_S131_013GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA12_S131_013GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga12_s131/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013S.png', 'https://img.bottleneko.app/GA12_S131_013S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA12_S131_013S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga12_s131/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013s.gif']}, 'GA13/S131-077': {'id': 'GA13/S131-077', 'series': 'GA/S131', 'name': '我的女神 草壁由佳', 'jp_name': 'ぼくの女神 草壁ゆか', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '農業'], 'default_count': 4, 'effects': ['AUTO_STAGE_TO_WR_CLOCK_LOOK2_GA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多2張，選擇《GA文庫》的角色最多2張給對手確認，加到手牌，剩下的卡片放到休息室。', 'base_id': 'GA13/S131-077', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA13/S131-077GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077.png', 'https://img.bottleneko.app/GA13_S131_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077.png']}, 'GA13/S131-077GA': {'id': 'GA13/S131-077GA', 'series': 'GA/S131', 'name': '我的女神 草壁由佳', 'jp_name': 'ぼくの女神 草壁ゆか', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '農業'], 'default_count': 0, 'effects': ['AUTO_STAGE_TO_WR_CLOCK_LOOK2_GA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077GA.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多2張，選擇《GA文庫》的角色最多2張給對手確認，加到手牌，剩下的卡片放到休息室。', 'base_id': 'GA13/S131-077', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA13/S131-077GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077GA.png', 'https://img.bottleneko.app/GA13_S131_077GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA13_S131_077GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga13_s131/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077S.png', 'https://img.bottleneko.app/GA13_S131_077S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA13_S131_077S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga13_s131/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077s.gif']}, 'GA10/S131-002': {'id': 'GA10/S131-002', 'series': 'GA/S131', 'name': '跨越復仇 琉', 'jp_name': '復讐を越えて リュー', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 4, 'effects': ['AUTO_ON_PLAY_OPP_COUNT_BUFF_1000', 'CX_COMBO_RYU_ATK_SCRY2_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於對手的角色張數×1000。\n【自】【CX連動】此卡攻擊時，CX區有「時隔五年的【能力值】更新」的話，你看自己牌組上方最多2張，選擇卡片最多2張，以任意順序放到牌組上方，剩下的卡片放到休息室，將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA10/S131-002', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-002SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002.png', 'https://img.bottleneko.app/GA10_S131_002.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002.png']}, 'GA10/S131-002SSP': {'id': 'GA10/S131-002SSP', 'series': 'GA/S131', 'name': '跨越復仇 琉', 'jp_name': '復讐を越えて リュー', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_OPP_COUNT_BUFF_1000', 'CX_COMBO_RYU_ATK_SCRY2_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002SSP.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於對手的角色張數×1000。\n【自】【CX連動】此卡攻擊時，CX區有「時隔五年的【能力值】更新」的話，你看自己牌組上方最多2張，選擇卡片最多2張，以任意順序放到牌組上方，剩下的卡片放到休息室，將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA10/S131-002', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA10/S131-002SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002SSP.png', 'https://img.bottleneko.app/GA10_S131_002SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_002SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002S.png', 'https://img.bottleneko.app/GA10_S131_002S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_002S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002s.gif']}, 'GA17/S131-014': {'id': 'GA17/S131-014', 'series': 'GA/S131', 'name': '我的旅路 伊蕾娜', 'jp_name': '私の旅路 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔法'], 'default_count': 1, 'effects': ['AUTO_MEMORY_DEF_DIRECT_MINUS_SOUL', 'ACT_MILL_ELAINA_BUFF_2000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014.png', 'text': '【自】回合1次 記憶 對手的角色直接攻擊時，你的回憶區有卡名包含「伊蕾娜」的角色，沒有其他的你的「我的旅路 伊蕾娜」存在的話，你選擇攻擊中的角色最多1張，在那個回合中，魂傷-1。\n【起】［將此卡【橫置】］ 你從自己的牌組選擇「第二章 伊蕾娜」或「第三章 伊蕾娜」最多1張，放到休息室，將那個牌組洗牌，你選擇自己的《GA文庫》的角色1張，在那個回合中，攻擊力+2000。', 'base_id': 'GA17/S131-014', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-014GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014.png', 'https://img.bottleneko.app/GA17_S131_014.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014.png']}, 'GA17/S131-014GA': {'id': 'GA17/S131-014GA', 'series': 'GA/S131', 'name': '我的旅路 伊蕾娜', 'jp_name': '私の旅路 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['AUTO_MEMORY_DEF_DIRECT_MINUS_SOUL', 'ACT_MILL_ELAINA_BUFF_2000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014GA.png', 'text': '【自】回合1次 記憶 對手的角色直接攻擊時，你的回憶區有卡名包含「伊蕾娜」的角色，沒有其他的你的「我的旅路 伊蕾娜」存在的話，你選擇攻擊中的角色最多1張，在那個回合中，魂傷-1。\n【起】［將此卡【橫置】］ 你從自己的牌組選擇「第二章 伊蕾娜」或「第三章 伊蕾娜」最多1張，放到休息室，將那個牌組洗牌，你選擇自己的《GA文庫》的角色1張，在那個回合中，攻擊力+2000。', 'base_id': 'GA17/S131-014', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA17/S131-014GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014GA.png', 'https://img.bottleneko.app/GA17_S131_014GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_014GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014S.png', 'https://img.bottleneko.app/GA17_S131_014S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_014S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014s.gif']}, 'GA17/S131-015': {'id': 'GA17/S131-015', 'series': 'GA/S131', 'name': '第一章 伊蕾娜', 'jp_name': '第一章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 3, 'effects': ['CONT_YOUR_TURN_6000', 'AUTO_REVERSE_CHAIN_CH2_ELAINA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015.png', 'text': '【永】在你的回合中，此卡的攻擊力+6000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，其他的你的《GA文庫》的角色存在2張以上的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第二章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方最多3張，以任意順序放到牌組上方，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第二章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-015', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-015S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015.png', 'https://img.bottleneko.app/GA17_S131_015.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015.png']}, 'GA17/S131-015S': {'id': 'GA17/S131-015S', 'series': 'GA/S131', 'name': '第一章 伊蕾娜', 'jp_name': '第一章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['CONT_YOUR_TURN_6000', 'AUTO_REVERSE_CHAIN_CH2_ELAINA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015S.png', 'text': '【永】在你的回合中，此卡的攻擊力+6000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，其他的你的《GA文庫》的角色存在2張以上的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第二章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方最多3張，以任意順序放到牌組上方，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第二章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-015', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA17/S131-015S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015S.png', 'https://img.bottleneko.app/GA17_S131_015S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_015S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015GA.png', 'https://img.bottleneko.app/GA17_S131_015GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_015GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015ga.gif']}, 'GA02/S131-009': {'id': 'GA02/S131-009', 'series': 'GA/S131', 'name': '告別膽小的自己 椎名真晝', 'jp_name': '臆病だった自分にさよならを 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 1, 'effects': ['COUNTER_BACKUP_2500_LV2', 'AUTO_ON_BACKUP_REFRESH_WR'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009.png', 'text': '【自】［(2)］ 當你使用此卡的『助太刀』時，你可以支付代價。支付代價的話，你將自己休息室的卡片全部，返回牌組，將那個牌組洗牌。\n【起】【反擊】 助太刀2500 等級2 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那個回合中，攻擊力+2500。', 'base_id': 'GA02/S131-009', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA02/S131-009SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009.png', 'https://img.bottleneko.app/GA02_S131_009.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009.png']}, 'GA02/S131-009SP': {'id': 'GA02/S131-009SP', 'series': 'GA/S131', 'name': '告別膽小的自己 椎名真晝', 'jp_name': '臆病だった自分にさよならを 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 0, 'effects': ['COUNTER_BACKUP_2500_LV2', 'AUTO_ON_BACKUP_REFRESH_WR'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009SP.png', 'text': '【自】［(2)］ 當你使用此卡的『助太刀』時，你可以支付代價。支付代價的話，你將自己休息室的卡片全部，返回牌組，將那個牌組洗牌。\n【起】【反擊】 助太刀2500 等級2 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那個回合中，攻擊力+2500。', 'base_id': 'GA02/S131-009', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA02/S131-009SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009SP.png', 'https://img.bottleneko.app/GA02_S131_009SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_009SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009S.png', 'https://img.bottleneko.app/GA02_S131_009S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_009S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009s.gif']}, 'GA10/S131-019': {'id': 'GA10/S131-019', 'series': 'GA/S131', 'name': '炸薯球 艾絲', 'jp_name': 'ジャガ丸くん アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 7000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_OPP_REVERSE_COMPRESS', 'AUTO_DIRECT_ATK_YELLOW_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019.png', 'text': '【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手選擇自己休息室的CX1張，除那張卡片以外的休息室的卡片全部，回到牌組，將那個牌組洗牌。\n【自】此卡直接攻擊時，你可以選擇自己休息室的黃色的卡片1張，放到能量區。', 'base_id': 'GA10/S131-019', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-019S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019.png', 'https://img.bottleneko.app/GA10_S131_019.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019.png']}, 'GA10/S131-019S': {'id': 'GA10/S131-019S', 'series': 'GA/S131', 'name': '炸薯球 艾絲', 'jp_name': 'ジャガ丸くん アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 7000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_OPP_REVERSE_COMPRESS', 'AUTO_DIRECT_ATK_YELLOW_STOCK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019S.png', 'text': '【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手選擇自己休息室的CX1張，除那張卡片以外的休息室的卡片全部，回到牌組，將那個牌組洗牌。\n【自】此卡直接攻擊時，你可以選擇自己休息室的黃色的卡片1張，放到能量區。', 'base_id': 'GA10/S131-019', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA10/S131-019S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019S.png', 'https://img.bottleneko.app/GA10_S131_019S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_019S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019GA.png', 'https://img.bottleneko.app/GA10_S131_019GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_019GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019ga.gif']}, 'GA10/S131-029': {'id': 'GA10/S131-029', 'series': 'GA/S131', 'name': '蕾菲亞&艾絲', 'jp_name': 'レフィーヤ＆アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_GRANT_ANTI_EARLY_PLAY_BOMB'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇自己的角色最多2張，在那個回合中，給予以下能力。『【自】此卡【倒置】時，此卡的戰鬥對手的等級比對手玩家等級還要高的話，你可以將那張角色放到能量區。放到能量區的話，你將對手的能量區下方1張，放到休息室。』', 'base_id': 'GA10/S131-029', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-029GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029.png', 'https://img.bottleneko.app/GA10_S131_029.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029.png']}, 'GA10/S131-029GA': {'id': 'GA10/S131-029GA', 'series': 'GA/S131', 'name': '蕾菲亞&艾絲', 'jp_name': 'レフィーヤ＆アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_GRANT_ANTI_EARLY_PLAY_BOMB'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029GA.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇自己的角色最多2張，在那個回合中，給予以下能力。『【自】此卡【倒置】時，此卡的戰鬥對手的等級比對手玩家等級還要高的話，你可以將那張角色放到能量區。放到能量區的話，你將對手的能量區下方1張，放到休息室。』', 'base_id': 'GA10/S131-029', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA10/S131-029GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029GA.png', 'https://img.bottleneko.app/GA10_S131_029GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_029GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029S.png', 'https://img.bottleneko.app/GA10_S131_029S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_029S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029s.gif']}, 'GA17/S131-017': {'id': 'GA17/S131-017', 'series': 'GA/S131', 'name': '第二章 伊蕾娜', 'jp_name': '第二章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 1500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 4, 'effects': ['CONT_YOUR_TURN_11000', 'AUTO_REVERSE_CHAIN_CH3_ELAINA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017.png', 'text': '【永】在你的回合中，此卡的攻擊力+11000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第三章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方1張，放到牌組上方或下方或休息室，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第三章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-017', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-017S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017.png', 'https://img.bottleneko.app/GA17_S131_017.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017.png']}, 'GA17/S131-017S': {'id': 'GA17/S131-017S', 'series': 'GA/S131', 'name': '第二章 伊蕾娜', 'jp_name': '第二章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 1500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['CONT_YOUR_TURN_11000', 'AUTO_REVERSE_CHAIN_CH3_ELAINA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017S.png', 'text': '【永】在你的回合中，此卡的攻擊力+11000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第三章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方1張，放到牌組上方或下方或休息室，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第三章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-017', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA17/S131-017S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017S.png', 'https://img.bottleneko.app/GA17_S131_017S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_017S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017GA.png', 'https://img.bottleneko.app/GA17_S131_017GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_017GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017ga.gif']}, 'GA01/S131-115': {'id': 'GA01/S131-115', 'series': 'GA/S131', 'name': '《五帝》櫛川鳩子', 'jp_name': '《五帝》櫛川鳩子', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '文藝部'], 'default_count': 1, 'effects': ['CONT_IGNORE_SELF_COLOR', 'AUTO_ON_PLAY_SAC_STAGE_SALVAGE_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115.png', 'text': '【永】此卡可以無需滿足顏色條件從手牌使用。\n【自】［其他的你的舞台的角色1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA01/S131-115', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA01/S131-115GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115.png', 'https://img.bottleneko.app/GA01_S131_115.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115.png']}, 'GA01/S131-115GA': {'id': 'GA01/S131-115GA', 'series': 'GA/S131', 'name': '《五帝》櫛川鳩子', 'jp_name': '《五帝》櫛川鳩子', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '文藝部'], 'default_count': 0, 'effects': ['CONT_IGNORE_SELF_COLOR', 'AUTO_ON_PLAY_SAC_STAGE_SALVAGE_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115GA.png', 'text': '【永】此卡可以無需滿足顏色條件從手牌使用。\n【自】［其他的你的舞台的角色1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA01/S131-115', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA01/S131-115GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115GA.png', 'https://img.bottleneko.app/GA01_S131_115GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA01_S131_115GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga01_s131/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115S.png', 'https://img.bottleneko.app/GA01_S131_115S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA01_S131_115S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga01_s131/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115s.gif']}, 'GA02/S131-003': {'id': 'GA02/S131-003', 'series': 'GA/S131', 'name': '隔壁的天使 椎名真晝', 'jp_name': 'お隣の天使様 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 2, 'effects': ['CONT_EARLY_PLAY_4GA', 'AUTO_ON_PLAY_BUFF_1500', 'AUTO_ON_PLAY_DISCARD_HEAL_AND_SALVAGE_GA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003.png', 'text': '【永】你的《GA文庫》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你將自己的傷害區上方最多1張，放到休息室，選擇自己休息室的《GA文庫》的角色1張，回到手牌。', 'base_id': 'GA02/S131-003', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA02/S131-003SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003.png', 'https://img.bottleneko.app/GA02_S131_003.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003.png']}, 'GA02/S131-003SSP': {'id': 'GA02/S131-003SSP', 'series': 'GA/S131', 'name': '隔壁的天使 椎名真晝', 'jp_name': 'お隣の天使様 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4GA', 'AUTO_ON_PLAY_BUFF_1500', 'AUTO_ON_PLAY_DISCARD_HEAL_AND_SALVAGE_GA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SSP.png', 'text': '【永】你的《GA文庫》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你將自己的傷害區上方最多1張，放到休息室，選擇自己休息室的《GA文庫》的角色1張，回到手牌。', 'base_id': 'GA02/S131-003', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA02/S131-003SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SSP.png', 'https://img.bottleneko.app/GA02_S131_003SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SP.png', 'https://img.bottleneko.app/GA02_S131_003SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003S.png', 'https://img.bottleneko.app/GA02_S131_003S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003s.gif']}, 'GA04/S131-100': {'id': 'GA04/S131-100', 'series': 'GA/S131', 'name': '新的黎明 女神官', 'jp_name': '新しい夜明け 女神官', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '神官'], 'default_count': 2, 'effects': ['CONT_EARLY_PLAY_WR_CX_2OR6', 'CONT_YOUR_TURN_1000', 'AUTO_ON_PLAY_CHOOSE_HEAL_OR_RESHUFFLE_OPP_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100.png', 'text': '【永】你的休息室的CX在2張以下或6張以上的話，你的手牌的此卡等級-1。\n【永】在你的回合中，此卡的攻擊力+1000。\n【自】此卡從手牌被放置到舞台時，以下的2個效果之中你選擇1個執行。『你可以將自己的傷害區上方1張，放到休息室。』『對手將自己的能量全部，返回牌組，將那個牌組洗牌，從自己的牌組上方將相同張數放到能量區，在那個回合中，此卡的攻擊力+2000。』', 'base_id': 'GA04/S131-100', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA04/S131-100SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100.png', 'https://img.bottleneko.app/GA04_S131_100.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100.png']}, 'GA04/S131-100SSP': {'id': 'GA04/S131-100SSP', 'series': 'GA/S131', 'name': '新的黎明 女神官', 'jp_name': '新しい夜明け 女神官', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '神官'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_WR_CX_2OR6', 'CONT_YOUR_TURN_1000', 'AUTO_ON_PLAY_CHOOSE_HEAL_OR_RESHUFFLE_OPP_STOCK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SSP.png', 'text': '【永】你的休息室的CX在2張以下或6張以上的話，你的手牌的此卡等級-1。\n【永】在你的回合中，此卡的攻擊力+1000。\n【自】此卡從手牌被放置到舞台時，以下的2個效果之中你選擇1個執行。『你可以將自己的傷害區上方1張，放到休息室。』『對手將自己的能量全部，返回牌組，將那個牌組洗牌，從自己的牌組上方將相同張數放到能量區，在那個回合中，此卡的攻擊力+2000。』', 'base_id': 'GA04/S131-100', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA04/S131-100SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SSP.png', 'https://img.bottleneko.app/GA04_S131_100SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SP.png', 'https://img.bottleneko.app/GA04_S131_100SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100S.png', 'https://img.bottleneko.app/GA04_S131_100S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100s.gif']}, 'GA17/S131-010': {'id': 'GA17/S131-010', 'series': 'GA/S131', 'name': '第三章 伊蕾娜', 'jp_name': '第三章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 4, 'effects': ['AUTO_ATK_BURN1_ON_ENTER_TURN', 'AUTO_SEND_TO_MEMORY_ON_REV_OR_END', 'CX_COMBO_MEMORY_ASH_WITCH_DEPLOY_BURN2'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010.png', 'text': '【自】此卡從手牌或回憶區被放到舞台的回合中，此卡攻擊時，你可以給對手1點傷害。會發生傷害取消。\n【自】此卡【倒置】時或回合結束時，將此卡放到回憶區。\n【自】【CX連動】記憶 ［(2) 手牌1張放到休息室］ 此卡在回憶區，你的等級在3以上的話，當「灰之魔女」被放置到你的CX區時，你可以支付代價。支付代價的話，你將此卡放到舞台的前列的格子，給對手2點傷害。會發生傷害取消。', 'base_id': 'GA17/S131-010', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-010SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010.png', 'https://img.bottleneko.app/GA17_S131_010.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010.png']}, 'GA17/S131-010SP': {'id': 'GA17/S131-010SP', 'series': 'GA/S131', 'name': '第三章 伊蕾娜', 'jp_name': '第三章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['AUTO_ATK_BURN1_ON_ENTER_TURN', 'AUTO_SEND_TO_MEMORY_ON_REV_OR_END', 'CX_COMBO_MEMORY_ASH_WITCH_DEPLOY_BURN2'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010SP.png', 'text': '【自】此卡從手牌或回憶區被放到舞台的回合中，此卡攻擊時，你可以給對手1點傷害。會發生傷害取消。\n【自】此卡【倒置】時或回合結束時，將此卡放到回憶區。\n【自】【CX連動】記憶 ［(2) 手牌1張放到休息室］ 此卡在回憶區，你的等級在3以上的話，當「灰之魔女」被放置到你的CX區時，你可以支付代價。支付代價的話，你將此卡放到舞台的前列的格子，給對手2點傷害。會發生傷害取消。', 'base_id': 'GA17/S131-010', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA17/S131-010SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010SP.png', 'https://img.bottleneko.app/GA17_S131_010SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010S.png', 'https://img.bottleneko.app/GA17_S131_010S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010GA.png', 'https://img.bottleneko.app/GA17_S131_010GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010ga.gif']}, 'BTR/W107-098': {'id': 'BTR/W107-098', 'series': 'BTR/W107', 'name': '成長與信賴的8小節', 'jp_name': '成長と信頼の8小節', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 4, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-098', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BTR/W107-098OFR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098.png', 'https://img.bottleneko.app/BTR_W107_098.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098.png']}, 'BTR/W107-098OFR': {'id': 'BTR/W107-098OFR', 'series': 'BTR/W107', 'name': '成長與信賴的8小節', 'jp_name': '成長と信頼の8小節', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098OFR.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-098', 'is_high_rarity': True, 'rarity': 'OFR', 'high_rarity_id': 'BTR/W107-098OFR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098OFR.png', 'https://img.bottleneko.app/BTR_W107_098OFR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_098OFR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_098ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098ofr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098R.png', 'https://img.bottleneko.app/BTR_W107_098R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_098R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_098r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098r.gif']}, 'BTR/W107-100': {'id': 'BTR/W107-100', 'series': 'BTR/W107', 'name': '逐漸增加的回憶', 'jp_name': '増えていく思い出', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 4, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-100', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BTR/W107-100R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100.png', 'https://img.bottleneko.app/BTR_W107_100.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100.png']}, 'BTR/W107-100R': {'id': 'BTR/W107-100R', 'series': 'BTR/W107', 'name': '逐漸增加的回憶', 'jp_name': '増えていく思い出', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-100', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-100R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100R.png', 'https://img.bottleneko.app/BTR_W107_100R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100RRR.png', 'https://img.bottleneko.app/BTR_W107_100RRR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100RRR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100rrr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100rrr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100rrr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100OFR.png', 'https://img.bottleneko.app/BTR_W107_100OFR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100OFR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100ofr.gif']}, 'BTR/W107-T02': {'id': 'BTR/W107-T02', 'series': 'BTR/W107', 'name': '樂團的領導者 伊地知虹夏', 'jp_name': 'バンドのリーダー 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '可靠'], 'default_count': 2, 'effects': ['AUTO_ON_YELLOW_CX_BUFF_1500', 'ACT_CONCENTRATE_5_DRAW'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02.png', 'text': '【自】當你的黃色名場面放置到名場面區時，你選擇自己的角色1張，在那回合中，攻擊力+1500。\n【起】集中 ［(1) 此卡【橫置】］ 你從自己的牌組上方翻開5張卡片，放到休息室。那些卡片每有1張名場面，你最多抽1張牌。', 'base_id': 'BTR/W107-T02', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T02R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02.png', 'https://img.bottleneko.app/BTR_W107_T02.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02.png']}, 'BTR/W107-T02R': {'id': 'BTR/W107-T02R', 'series': 'BTR/W107', 'name': '樂團的領導者 伊地知虹夏', 'jp_name': 'バンドのリーダー 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '可靠'], 'default_count': 0, 'effects': ['AUTO_ON_YELLOW_CX_BUFF_1500', 'ACT_CONCENTRATE_5_DRAW'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02R.png', 'text': '【自】當你的黃色名場面放置到名場面區時，你選擇自己的角色1張，在那回合中，攻擊力+1500。\n【起】集中 ［(1) 此卡【橫置】］ 你從自己的牌組上方翻開5張卡片，放到休息室。那些卡片每有1張名場面，你最多抽1張牌。', 'base_id': 'BTR/W107-T02', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T02R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02R.png', 'https://img.bottleneko.app/BTR_W107_T02R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02S.png', 'https://img.bottleneko.app/BTR_W107_T02S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02SP.png', 'https://img.bottleneko.app/BTR_W107_T02SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02sp.gif']}, 'BTR/W107-T13': {'id': 'BTR/W107-T13', 'series': 'BTR/W107', 'name': '樂團女子？ 後藤一里', 'jp_name': 'バンドマン？ 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['CONT_BUFF_VOCAL_KITA_1000_1SOUL', 'AUTO_BOND_VOCAL_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13.png', 'text': '【永】其他的你的「主唱吉他手 喜多郁代」全部，攻擊力+1000，魂傷+1。\n【自】絆／「主唱吉他手 喜多郁代」 ［手牌1張放到休息室］ 此卡從手牌登場到舞台時，你可以支付費用。這樣做的話，你從自己的休息室選擇1張「主唱吉他手 喜多郁代」加到手牌。', 'base_id': 'BTR/W107-T13', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T13R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13.png', 'https://img.bottleneko.app/BTR_W107_T13.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13.png']}, 'BTR/W107-T13R': {'id': 'BTR/W107-T13R', 'series': 'BTR/W107', 'name': '樂團女子？ 後藤一里', 'jp_name': 'バンドマン？ 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['CONT_BUFF_VOCAL_KITA_1000_1SOUL', 'AUTO_BOND_VOCAL_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13R.png', 'text': '【永】其他的你的「主唱吉他手 喜多郁代」全部，攻擊力+1000，魂傷+1。\n【自】絆／「主唱吉他手 喜多郁代」 ［手牌1張放到休息室］ 此卡從手牌登場到舞台時，你可以支付費用。這樣做的話，你從自己的休息室選擇1張「主唱吉他手 喜多郁代」加到手牌。', 'base_id': 'BTR/W107-T13', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T13R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13R.png', 'https://img.bottleneko.app/BTR_W107_T13R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T13R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t13r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13S.png', 'https://img.bottleneko.app/BTR_W107_T13S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T13S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t13s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13s.gif']}, 'BTR/W107-T14': {'id': 'BTR/W107-T14', 'series': 'BTR/W107', 'name': '後藤一里', 'jp_name': '後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_LOOK3_EVENT', 'AUTO_ON_PLAY_BOMB_COST0_IF_OPP_LE1'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14.png', 'text': '【自】此卡從手牌被放置到舞台時，你從自己的牌組上方看最多3張，選擇事件最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，對手的前列的角色在1張以下的話，你可以選擇對手的前列的費用0以下的角色1張，放到休息室。', 'base_id': 'BTR/W107-T14', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T14SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14.png', 'https://img.bottleneko.app/BTR_W107_T14.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14.png']}, 'BTR/W107-T14SP': {'id': 'BTR/W107-T14SP', 'series': 'BTR/W107', 'name': '後藤一里', 'jp_name': '後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_LOOK3_EVENT', 'AUTO_ON_PLAY_BOMB_COST0_IF_OPP_LE1'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14SP.png', 'text': '【自】此卡從手牌被放置到舞台時，你從自己的牌組上方看最多3張，選擇事件最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，對手的前列的角色在1張以下的話，你可以選擇對手的前列的費用0以下的角色1張，放到休息室。', 'base_id': 'BTR/W107-T14', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BTR/W107-T14SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14SP.png', 'https://img.bottleneko.app/BTR_W107_T14SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14R.png', 'https://img.bottleneko.app/BTR_W107_T14R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14S.png', 'https://img.bottleneko.app/BTR_W107_T14S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14s.gif']}, 'BTR/W107-T15': {'id': 'BTR/W107-T15', 'series': 'BTR/W107', 'name': '陽角 喜多郁代', 'jp_name': '陽キャ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['AUTO_ON_REVERSE_LOOK3_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15.png', 'text': '【自】當戰鬥中的此卡【倒置】時，你從自己的牌組上方看最多3張，選擇名場面最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。', 'base_id': 'BTR/W107-T15', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T15R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15.png', 'https://img.bottleneko.app/BTR_W107_T15.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15.png']}, 'BTR/W107-T15R': {'id': 'BTR/W107-T15R', 'series': 'BTR/W107', 'name': '陽角 喜多郁代', 'jp_name': '陽キャ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_ON_REVERSE_LOOK3_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15R.png', 'text': '【自】當戰鬥中的此卡【倒置】時，你從自己的牌組上方看最多3張，選擇名場面最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。', 'base_id': 'BTR/W107-T15', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T15R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15R.png', 'https://img.bottleneko.app/BTR_W107_T15R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15S.png', 'https://img.bottleneko.app/BTR_W107_T15S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15SP.png', 'https://img.bottleneko.app/BTR_W107_T15SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15sp.gif']}, 'BTR/W107-T16': {'id': 'BTR/W107-T16', 'series': 'BTR/W107', 'name': '主唱吉他手 喜多郁代', 'jp_name': 'ギターボーカル 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': [], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16.png', 'text': '（無特殊效果）', 'base_id': 'BTR/W107-T16', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T16R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16.png', 'https://img.bottleneko.app/BTR_W107_T16.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16.png']}, 'BTR/W107-T16R': {'id': 'BTR/W107-T16R', 'series': 'BTR/W107', 'name': '主唱吉他手 喜多郁代', 'jp_name': 'ギターボーカル 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': [], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16R.png', 'text': '（無特殊效果）', 'base_id': 'BTR/W107-T16', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T16R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16R.png', 'https://img.bottleneko.app/BTR_W107_T16R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T16R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t16r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16S.png', 'https://img.bottleneko.app/BTR_W107_T16S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T16S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t16s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16s.gif']}, 'BTR/W107-T17': {'id': 'BTR/W107-T17', 'series': 'BTR/W107', 'name': '高人氣 喜多郁代', 'jp_name': '人気者 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_SELF_2000', 'AUTO_ENCORE_1STOCK_1HAND'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，在那回合中，此卡的攻擊力+2000。\n【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。', 'base_id': 'BTR/W107-T17', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T17R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17.png', 'https://img.bottleneko.app/BTR_W107_T17.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17.png']}, 'BTR/W107-T17R': {'id': 'BTR/W107-T17R', 'series': 'BTR/W107', 'name': '高人氣 喜多郁代', 'jp_name': '人気者 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_SELF_2000', 'AUTO_ENCORE_1STOCK_1HAND'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17R.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，在那回合中，此卡的攻擊力+2000。\n【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。', 'base_id': 'BTR/W107-T17', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T17R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17R.png', 'https://img.bottleneko.app/BTR_W107_T17R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T17R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t17r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17S.png', 'https://img.bottleneko.app/BTR_W107_T17S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T17S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t17s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17s.gif']}, 'BTR/W107-T18': {'id': 'BTR/W107-T18', 'series': 'BTR/W107', 'name': '喜多郁代', 'jp_name': '喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_ENCORE_1STOCK_1HAND', 'ACT_1STOCK_1000_CLOCK_KICK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18.png', 'text': '【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。\n【起】［(1)］ 在那回合中，此卡的攻擊力+1000，此卡獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以將那個角色放到時計區。』', 'base_id': 'BTR/W107-T18', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T18R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18.png', 'https://img.bottleneko.app/BTR_W107_T18.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18.png']}, 'BTR/W107-T18R': {'id': 'BTR/W107-T18R', 'series': 'BTR/W107', 'name': '喜多郁代', 'jp_name': '喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_ENCORE_1STOCK_1HAND', 'ACT_1STOCK_1000_CLOCK_KICK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18R.png', 'text': '【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。\n【起】［(1)］ 在那回合中，此卡的攻擊力+1000，此卡獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以將那個角色放到時計區。』', 'base_id': 'BTR/W107-T18', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T18R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18R.png', 'https://img.bottleneko.app/BTR_W107_T18R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18SP.png', 'https://img.bottleneko.app/BTR_W107_T18SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18S.png', 'https://img.bottleneko.app/BTR_W107_T18S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18s.gif']}, 'BTR/W107-077': {'id': 'BTR/W107-077', 'series': 'BTR/W107', 'name': '裝過頭的面子 後藤一里', 'jp_name': '張り切りすぎた見栄 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_TARGET_1000', 'AUTO_STAGE_TO_WR_DISCARD_MUSIC_LOOK4_LV1'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，你選擇自己的角色1張，在那回合中，攻擊力+1000。\n【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從舞台放到休息室時，你可以支付費用。這樣做的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面視為等級0。', 'base_id': 'BTR/W107-077', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-077KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077.png', 'https://img.bottleneko.app/BTR_W107_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077.png']}, 'BTR/W107-077KBR': {'id': 'BTR/W107-077KBR', 'series': 'BTR/W107', 'name': '裝過頭的面子 後藤一里', 'jp_name': '張り切りすぎた見栄 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_TARGET_1000', 'AUTO_STAGE_TO_WR_DISCARD_MUSIC_LOOK4_LV1'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077KBR.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，你選擇自己的角色1張，在那回合中，攻擊力+1000。\n【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從舞台放到休息室時，你可以支付費用。這樣做的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面視為等級0。', 'base_id': 'BTR/W107-077', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-077KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077KBR.png', 'https://img.bottleneko.app/BTR_W107_077KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_077KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_077kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077S.png', 'https://img.bottleneko.app/BTR_W107_077S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_077S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077s.gif']}, 'BTR/W107-076': {'id': 'BTR/W107-076', 'series': 'BTR/W107', 'name': '成長歷程 喜多郁代', 'jp_name': '成長の軌跡 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_OTHER_MUSIC_500_EACH', 'AUTO_ON_PLAY_HEAL', 'CX_COMBO_KITA_ATK_BURN4'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076.png', 'text': '【永】其他的你的《音樂》的角色每有1張，此卡的攻擊力+500。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。\n【自】【CX連動】［手牌2張卡片放到休息室］ 此卡攻擊時，名場面區有「逐漸增加的回憶」，且其他的你的《音樂》的角色有4張以上的話，你可以支付費用。這樣做的話，給予對手4點傷害。會發生傷害取消。', 'base_id': 'BTR/W107-076', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-076S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076.png', 'https://img.bottleneko.app/BTR_W107_076.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076.png']}, 'BTR/W107-076S': {'id': 'BTR/W107-076S', 'series': 'BTR/W107', 'name': '成長歷程 喜多郁代', 'jp_name': '成長の軌跡 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_OTHER_MUSIC_500_EACH', 'AUTO_ON_PLAY_HEAL', 'CX_COMBO_KITA_ATK_BURN4'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076S.png', 'text': '【永】其他的你的《音樂》的角色每有1張，此卡的攻擊力+500。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。\n【自】【CX連動】［手牌2張卡片放到休息室］ 此卡攻擊時，名場面區有「逐漸增加的回憶」，且其他的你的《音樂》的角色有4張以上的話，你可以支付費用。這樣做的話，給予對手4點傷害。會發生傷害取消。', 'base_id': 'BTR/W107-076', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BTR/W107-076S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076S.png', 'https://img.bottleneko.app/BTR_W107_076S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076SSP.png', 'https://img.bottleneko.app/BTR_W107_076SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076SP.png', 'https://img.bottleneko.app/BTR_W107_076SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076KBR.png', 'https://img.bottleneko.app/BTR_W107_076KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076kbr.gif']}, 'BTR/W107-075': {'id': 'BTR/W107-075', 'series': 'BTR/W107', 'name': '晚霞的歸路 喜多郁代', 'jp_name': '夕焼けの帰り道 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_OTHER_2MUSIC_BUFF_3000', 'AUTO_ON_PLAY_STOCK_HEAL_IF_4', 'CX_COMBO_SUNSET_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075.png', 'text': '【永】其他的你的《音樂》的角色有2張以上的話，此卡的攻擊力+3000。\n【自】此卡從手牌放置到舞台時，若你的等級區與時鐘區的卡片合計有4張以上，你可以將自己時鐘區上方1張放到能量區。\n【自】【CX連動】當「成長與信賴的8小節」放置到你的名場面區時，前列有此卡，且有其他的你的《音樂》角色的話，在那個回合中，此卡的攻擊力+1000，並獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以從自己的休息室選擇《音樂》的角色1張回到手牌。』', 'base_id': 'BTR/W107-075', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-075S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075.png', 'https://img.bottleneko.app/BTR_W107_075.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075.png']}, 'BTR/W107-075S': {'id': 'BTR/W107-075S', 'series': 'BTR/W107', 'name': '晚霞的歸路 喜多郁代', 'jp_name': '夕焼けの帰り道 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_OTHER_2MUSIC_BUFF_3000', 'AUTO_ON_PLAY_STOCK_HEAL_IF_4', 'CX_COMBO_SUNSET_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075S.png', 'text': '【永】其他的你的《音樂》的角色有2張以上的話，此卡的攻擊力+3000。\n【自】此卡從手牌放置到舞台時，若你的等級區與時鐘區的卡片合計有4張以上，你可以將自己時鐘區上方1張放到能量區。\n【自】【CX連動】當「成長與信賴的8小節」放置到你的名場面區時，前列有此卡，且有其他的你的《音樂》角色的話，在那個回合中，此卡的攻擊力+1000，並獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以從自己的休息室選擇《音樂》的角色1張回到手牌。』', 'base_id': 'BTR/W107-075', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BTR/W107-075S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075S.png', 'https://img.bottleneko.app/BTR_W107_075S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075SP.png', 'https://img.bottleneko.app/BTR_W107_075SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075KBR.png', 'https://img.bottleneko.app/BTR_W107_075KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075kbr.gif']}, 'BTR/W107-T06': {'id': 'BTR/W107-T06', 'series': 'BTR/W107', 'name': '音樂話題～ 伊地知虹夏', 'jp_name': '音楽バナシ～ 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 1, 'power': 500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '可靠'], 'default_count': 2, 'effects': ['COUNTER_BACKUP_2000_LV1', 'AUTO_ON_BACKUP_TOP_CHECK_MUSIC'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06.png', 'text': '【自】當你使用此卡的『助太刀』時，你將自己的牌組上方1張公開。那張卡片是《音樂》的角色的話加到手牌，你選擇自己的手牌1張，放到休息室。如果不是的話放回原位。\n【起】【反擊】助太刀2000 等級1 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那回合中，攻擊力+2000。', 'base_id': 'BTR/W107-T06', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T06R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06.png', 'https://img.bottleneko.app/BTR_W107_T06.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06.png']}, 'BTR/W107-T06R': {'id': 'BTR/W107-T06R', 'series': 'BTR/W107', 'name': '音樂話題～ 伊地知虹夏', 'jp_name': '音楽バナシ～ 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 1, 'power': 500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '可靠'], 'default_count': 0, 'effects': ['COUNTER_BACKUP_2000_LV1', 'AUTO_ON_BACKUP_TOP_CHECK_MUSIC'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06R.png', 'text': '【自】當你使用此卡的『助太刀』時，你將自己的牌組上方1張公開。那張卡片是《音樂》的角色的話加到手牌，你選擇自己的手牌1張，放到休息室。如果不是的話放回原位。\n【起】【反擊】助太刀2000 等級1 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那回合中，攻擊力+2000。', 'base_id': 'BTR/W107-T06', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T06R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06R.png', 'https://img.bottleneko.app/BTR_W107_T06R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T06R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t06r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06S.png', 'https://img.bottleneko.app/BTR_W107_T06S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T06S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t06s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06s.gif']}, 'BTR/W107-046': {'id': 'BTR/W107-046', 'series': 'BTR/W107', 'name': '打卡美照 喜多郁代', 'jp_name': '映える写真 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_OPP_ATK_START_MOVE_BACK', 'ACT_REST_SELF_BUFF_MUSIC_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046.png', 'text': '【自】當對手的攻擊階段開始時，你可以將此卡移動到後列沒有角色的格子。\n【起】［此卡【橫置】］ 你選擇自己1張《音樂》的角色，在那回合中，攻擊力+1000。', 'base_id': 'BTR/W107-046', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-046KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046.png', 'https://img.bottleneko.app/BTR_W107_046.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046.png']}, 'BTR/W107-046KBR': {'id': 'BTR/W107-046KBR', 'series': 'BTR/W107', 'name': '打卡美照 喜多郁代', 'jp_name': '映える写真 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_OPP_ATK_START_MOVE_BACK', 'ACT_REST_SELF_BUFF_MUSIC_1000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046KBR.png', 'text': '【自】當對手的攻擊階段開始時，你可以將此卡移動到後列沒有角色的格子。\n【起】［此卡【橫置】］ 你選擇自己1張《音樂》的角色，在那回合中，攻擊力+1000。', 'base_id': 'BTR/W107-046', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-046KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046KBR.png', 'https://img.bottleneko.app/BTR_W107_046KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_046KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_046kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046S.png', 'https://img.bottleneko.app/BTR_W107_046S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_046S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_046s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046s.gif']}, 'BTR/W107-089': {'id': 'BTR/W107-089', 'series': 'BTR/W107', 'name': '開始轉動的故事 後藤一里', 'jp_name': '動き出す物語 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_DISCARD_MUSIC_SEARCH_VOCAL_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089.png', 'text': '【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從手牌放到舞台時，你可以支付費用。這樣做的話，你從自己的牌組選擇「主唱吉他手 喜多郁代」最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-089', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-089KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089.png', 'https://img.bottleneko.app/BTR_W107_089.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089.png']}, 'BTR/W107-089KBR': {'id': 'BTR/W107-089KBR', 'series': 'BTR/W107', 'name': '開始轉動的故事 後藤一里', 'jp_name': '動き出す物語 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DISCARD_MUSIC_SEARCH_VOCAL_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089KBR.png', 'text': '【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從手牌放到舞台時，你可以支付費用。這樣做的話，你從自己的牌組選擇「主唱吉他手 喜多郁代」最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-089', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-089KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089KBR.png', 'https://img.bottleneko.app/BTR_W107_089KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_089KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_089kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089S.png', 'https://img.bottleneko.app/BTR_W107_089S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_089S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089s.gif']}, 'BTR/W107-069': {'id': 'BTR/W107-069', 'series': 'BTR/W107', 'name': '對於不憧憬的憧憬 喜多郁代', 'jp_name': '憧れなかった憧れ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_EARLY_PLAY_4MUSIC', 'CONT_CANNOT_PLAY_BACKUP', 'AUTO_ON_PLAY_HEAL'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069.png', 'text': '【永】其他的你的《音樂》的角色有4張以上的話，你的手牌的此卡的等級-1。\n【永】此卡戰鬥中，對手不能從手牌使用『助太刀』。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。', 'base_id': 'BTR/W107-069', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-069SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069.png', 'https://img.bottleneko.app/BTR_W107_069.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069.png']}, 'BTR/W107-069SSP': {'id': 'BTR/W107-069SSP', 'series': 'BTR/W107', 'name': '對於不憧憬的憧憬 喜多郁代', 'jp_name': '憧れなかった憧れ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4MUSIC', 'CONT_CANNOT_PLAY_BACKUP', 'AUTO_ON_PLAY_HEAL'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SSP.png', 'text': '【永】其他的你的《音樂》的角色有4張以上的話，你的手牌的此卡的等級-1。\n【永】此卡戰鬥中，對手不能從手牌使用『助太刀』。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。', 'base_id': 'BTR/W107-069', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'BTR/W107-069SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SSP.png', 'https://img.bottleneko.app/BTR_W107_069SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SP.png', 'https://img.bottleneko.app/BTR_W107_069SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069S.png', 'https://img.bottleneko.app/BTR_W107_069S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069KBR.png', 'https://img.bottleneko.app/BTR_W107_069KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069kbr.gif']}, 'BTR/W107-T10': {'id': 'BTR/W107-T10', 'series': 'BTR/W107', 'name': '樂團名「團結Band」', 'jp_name': 'バンド名「結束バンド」', 'type': 'EVENT', 'color': '黃', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 4, 'effects': ['EVENT_SEARCH_MUSIC_OR_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10.png', 'text': '你從自己的牌組選擇《音樂》的角色或名場面最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-T10', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T10R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10.png', 'https://img.bottleneko.app/BTR_W107_T10.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10.png']}, 'BTR/W107-T10R': {'id': 'BTR/W107-T10R', 'series': 'BTR/W107', 'name': '樂團名「團結Band」', 'jp_name': 'バンド名「結束バンド」', 'type': 'EVENT', 'color': '黃', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 0, 'effects': ['EVENT_SEARCH_MUSIC_OR_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10R.png', 'text': '你從自己的牌組選擇《音樂》的角色或名場面最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-T10', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T10R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10R.png', 'https://img.bottleneko.app/BTR_W107_T10R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T10R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t10r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10S.png', 'https://img.bottleneko.app/BTR_W107_T10S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T10S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t10s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10s.gif']}}

    SERIES_LABELS = {
        "BFR/S78": "防盾系列 (BFR/S78)",
        "GA/S131": "GA文庫 (GA/S131)",
        "BTR/W107": "孤獨搖滾 (BTR/W107)",
    }

    CARD_DB = {}
    DEFAULT_DECK_RECIPE = {}
    SERIES_DB = {}
    SERIES_DEFAULT_DECKS = {}


    def _infer_series_code(cid: str, data: dict, fallback_name: str = "") -> str:
        if data.get("series"):
            return str(data["series"])
        if "/W107-" in cid or cid.startswith("BTR"):
            return "BTR/W107"
        if "/S131-" in cid or cid.startswith("GA"):
            return "GA/S131"
        if "/S78-" in cid or cid.startswith("BFR"):
            return "BFR/S78"
        if "-" in cid:
            return cid.split("-")[0]
        return fallback_name or "BFR/S78"


    def load_all_card_sets(sets_dir="sets"):
        """自動掃描並載入 sets/*.json 所有系列卡片資料庫，支援分系列卡池與預設卡組"""
        global CARD_DB, DEFAULT_DECK_RECIPE, SERIES_DB, SERIES_DEFAULT_DECKS
        full_sets_dir = os.path.join(BASE_DIR, sets_dir)
        os.makedirs(full_sets_dir, exist_ok=True)

        card_db = {}
        default_recipe = {}
        series_db = {}
        series_decks = {}

        search_patterns = [
            os.path.join(full_sets_dir, "*.json"),
            os.path.join(BASE_DIR, "BFR_S78.json"),
            os.path.join(BASE_DIR, "GA_S131.json"),
            os.path.join(BASE_DIR, "BTR_W107.json"),
        ]
        for pattern in search_patterns:
            for path in sorted(glob.glob(pattern)):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if not isinstance(data, dict):
                        continue
                    file_stem = os.path.splitext(os.path.basename(path))[0]
                    explicit_series = data.get("series_name") or data.get("series_code") or ""
                    cards_dict = data.get("cards", data)
                    if isinstance(cards_dict, dict):
                        for cid, cinfo in cards_dict.items():
                            if isinstance(cinfo, dict) and "name" in cinfo:
                                scode = _infer_series_code(cid, cinfo, explicit_series or file_stem)
                                cinfo["series"] = scode
                                card_db[cid] = cinfo
                                series_db.setdefault(scode, {})[cid] = cinfo
                                if cinfo.get("default_count", 0) > 0:
                                    series_decks.setdefault(scode, {})[cid] = cinfo["default_count"]
                    if "default_deck_recipe" in data and isinstance(data["default_deck_recipe"], dict):
                        s_key = explicit_series or file_stem
                        series_decks[s_key] = dict(data["default_deck_recipe"])
                except Exception as e:
                    print(f"讀取系列檔 {path} 失敗: {e}")

        # 確保內建的 BFR/S78 與 GA/S131 永遠存在
        for cid, cinfo in FALLBACK_CARD_DB.items():
            if cid not in card_db:
                scode = _infer_series_code(cid, cinfo, "BFR/S78")
                cinfo["series"] = scode
                card_db[cid] = cinfo
                series_db.setdefault(scode, {})[cid] = cinfo
                if cinfo.get("default_count", 0) > 0:
                    series_decks.setdefault(scode, {})[cid] = cinfo["default_count"]

        if "BFR/S78" in series_decks:
            default_recipe = dict(series_decks["BFR/S78"])
        elif series_decks:
            first_s = next(iter(series_decks))
            default_recipe = dict(series_decks[first_s])

        CARD_DB.clear()
        CARD_DB.update(card_db)
        DEFAULT_DECK_RECIPE.clear()
        DEFAULT_DECK_RECIPE.update(default_recipe)
        SERIES_DB.clear()
        SERIES_DB.update(series_db)
        SERIES_DEFAULT_DECKS.clear()
        SERIES_DEFAULT_DECKS.update(series_decks)
        return CARD_DB, DEFAULT_DECK_RECIPE


    load_all_card_sets()


    class CardInstance:
        """單張實體卡片狀態與暫時加成屬性"""

        def __init__(self, cid: str):
            data = CARD_DB[cid]
            self.skin_id = cid
            self.id = data.get("base_id", cid)
            self.rarity = data.get("rarity", "R")
            self.is_high_rarity = bool(data.get("is_high_rarity", False))
            self.name = data["name"]
            self.type = data["type"]
            self.color = data["color"]
            self.base_level = data["level"]
            self.cost = data["cost"]
            self.base_power = data["power"]
            self.base_soul = data["soul"]
            self.trigger = data["trigger"]
            self.traits = list(data.get("traits", []))
            self.series = data.get("series", _infer_series_code(cid, data))
            raw_effects = data.get("effects", data.get("effect_tags", []))
            self.effects = list(raw_effects)
            self.effect_tags = self.effects
            self.text = data["text"]
            self.reset_stage_state()

        def has_effect(self, tag: str) -> bool:
            return tag in self.effects

        def reset_stage_state(self):
            self.state = "STAND"
            self.temp_power = 0
            self.temp_soul = 0
            self.temp_level = 0
            self.markers = []
            self.cannot_return_hand = False
            self.cannot_go_memory = False
            self.cannot_be_reversed = False
            self.cannot_move = False
            self.used_act_buff_turn = False
            self.entered_stage_this_turn = False
            self.anti_early_play_stock_bomb = False
            self.used_memory_minus_soul_turn = False
            self.clock_kick_on_reverse = False
            self.salvage_music_on_reverse = False

        def to_sync_dict(self) -> dict:
            return {
                "id": getattr(self, "skin_id", self.id),
                "state": self.state,
                "temp_power": self.temp_power,
                "temp_soul": self.temp_soul,
                "temp_level": self.temp_level,
                "markers": [getattr(m, "skin_id", m.id) for m in self.markers],
                "cannot_return_hand": self.cannot_return_hand,
                "cannot_go_memory": self.cannot_go_memory,
                "cannot_be_reversed": self.cannot_be_reversed,
                "cannot_move": self.cannot_move,
                "used_act_buff_turn": self.used_act_buff_turn,
                "entered_stage_this_turn": self.entered_stage_this_turn,
                "anti_early_play_stock_bomb": self.anti_early_play_stock_bomb,
                "used_memory_minus_soul_turn": self.used_memory_minus_soul_turn,
                "clock_kick_on_reverse": self.clock_kick_on_reverse,
                "salvage_music_on_reverse": self.salvage_music_on_reverse,
            }

        @classmethod
        def from_sync_dict(cls, d: dict):
            if not d or "id" not in d or d["id"] not in CARD_DB:
                return None
            inst = cls(d["id"])
            inst.state = d.get("state", "STAND")
            inst.temp_power = d.get("temp_power", 0)
            inst.temp_soul = d.get("temp_soul", 0)
            inst.temp_level = d.get("temp_level", 0)
            inst.markers = [cls(mid) for mid in d.get("markers", []) if mid in CARD_DB]
            inst.cannot_return_hand = d.get("cannot_return_hand", False)
            inst.cannot_go_memory = d.get("cannot_go_memory", False)
            inst.cannot_be_reversed = d.get("cannot_be_reversed", False)
            inst.cannot_move = d.get("cannot_move", False)
            inst.used_act_buff_turn = d.get("used_act_buff_turn", False)
            inst.entered_stage_this_turn = d.get("entered_stage_this_turn", False)
            inst.anti_early_play_stock_bomb = d.get("anti_early_play_stock_bomb", False)
            inst.used_memory_minus_soul_turn = d.get("used_memory_minus_soul_turn", False)
            inst.clock_kick_on_reverse = d.get("clock_kick_on_reverse", False)
            inst.salvage_music_on_reverse = d.get("salvage_music_on_reverse", False)
            return inst


    class PlayerState:
        """玩家全區域狀態管理與區網序列化介面"""

        def __init__(self, name: str, deck_recipe: dict, is_ai: bool = False):
            self.name = name
            self.is_ai = is_ai
            self.deck = []
            self.hand = []
            self.waiting_room = []
            self.clock = []
            self.level_zone = []
            self.stock = []
            self.memory = []
            self.climax_zone = None
            self.stage = [None] * 5
            self.pending_draw_phase_spawns = []
            self.ace_cid = "BFR/S78-063"
            self.build_deck(deck_recipe)

        def build_deck(self, deck_recipe: dict):
            self.deck = []
            for cid, count in deck_recipe.items():
                if cid in CARD_DB:
                    for _ in range(count):
                        self.deck.append(CardInstance(cid))
            random.shuffle(self.deck)

        def to_sync_dict(self) -> dict:
            return {
                "name": self.name,
                "deck": [getattr(c, "skin_id", c.id) for c in self.deck],
                "hand": [getattr(c, "skin_id", c.id) for c in self.hand],
                "waiting_room": [getattr(c, "skin_id", c.id) for c in self.waiting_room],
                "clock": [getattr(c, "skin_id", c.id) for c in self.clock],
                "level_zone": [getattr(c, "skin_id", c.id) for c in self.level_zone],
                "stock": [getattr(c, "skin_id", c.id) for c in self.stock],
                "memory": [getattr(c, "skin_id", c.id) for c in self.memory],
                "climax_zone": getattr(self.climax_zone, "skin_id", self.climax_zone.id) if self.climax_zone else None,
                "stage": [c.to_sync_dict() if c else None for c in self.stage],
                "pending_draw_phase_spawns": list(self.pending_draw_phase_spawns),
                "ace_cid": getattr(self, "ace_cid", "BFR/S78-063"),
            }

        def apply_sync_dict(self, d: dict):
            if not d:
                return
            self.deck = [CardInstance(cid) for cid in d.get("deck", []) if cid in CARD_DB]
            self.hand = [CardInstance(cid) for cid in d.get("hand", []) if cid in CARD_DB]
            self.waiting_room = [CardInstance(cid) for cid in d.get("waiting_room", []) if cid in CARD_DB]
            self.clock = [CardInstance(cid) for cid in d.get("clock", []) if cid in CARD_DB]
            self.level_zone = [CardInstance(cid) for cid in d.get("level_zone", []) if cid in CARD_DB]
            self.stock = [CardInstance(cid) for cid in d.get("stock", []) if cid in CARD_DB]
            self.memory = [CardInstance(cid) for cid in d.get("memory", []) if cid in CARD_DB]
            cx_id = d.get("climax_zone")
            self.climax_zone = CardInstance(cx_id) if (cx_id and cx_id in CARD_DB) else None
            stage_data = d.get("stage", [None] * 5)
            self.stage = [CardInstance.from_sync_dict(s) if s else None for s in stage_data[:5]]
            self.pending_draw_phase_spawns = list(d.get("pending_draw_phase_spawns", []))
            if "ace_cid" in d and d["ace_cid"] in CARD_DB:
                self.ace_cid = d["ace_cid"]


    class RuleEngine:
        """動態數值運算與通用效果結算積木，支援 BFR/S78 與 GA/S131"""

        @staticmethod
        def get_effective_level(p: PlayerState, card: CardInstance, stage_idx=None) -> int:
            if not card or card.type == "CX":
                return 0
            if stage_idx is None and card in p.hand:
                if card.has_effect("CONT_EARLY_PLAY_4GAME") or card.id == "BFR/S78-081":
                    game_chars = sum(1 for c in p.stage if c and "遊戲" in c.traits)
                    if game_chars >= 4:
                        return max(0, card.base_level - 1)
                if card.has_effect("CONT_EARLY_PLAY_4GA") or card.id == "GA02/S131-003":
                    ga_chars = sum(1 for c in p.stage if c and "GA文庫" in c.traits)
                    if ga_chars >= 4:
                        return max(0, card.base_level - 1)
                if card.has_effect("CONT_EARLY_PLAY_4MUSIC") or card.id == "BTR/W107-069":
                    music_chars = sum(1 for c in p.stage if c and "音樂" in c.traits)
                    if music_chars >= 4:
                        return max(0, card.base_level - 1)
                if card.has_effect("CONT_EARLY_PLAY_WR_CX_2OR6") or card.id == "GA04/S131-100":
                    wr_cx = sum(1 for c in p.waiting_room if c.type == "CX")
                    if wr_cx <= 2 or wr_cx >= 6:
                        return max(0, card.base_level - 1)
            if stage_idx is not None:
                return max(0, card.base_level + card.temp_level)
            return card.base_level

        @staticmethod
        def get_effective_power(
            p: PlayerState, opp: PlayerState, card: CardInstance, stage_idx: int, is_my_turn: bool = True
        ) -> int:
            if not card or card.type != "CHAR":
                return 0
            pwr = card.base_power + card.temp_power

            if p.climax_zone and (
                p.climax_zone.has_effect("CX_ALL_1000_1SOUL")
                or p.climax_zone.id in ["BFR/S78-107", "GA10/S131-030", "GA17/S131-033"]
            ):
                pwr += 1000

            if card.has_effect("CONT_OTHER_2GAME_BUFF_2000") or card.id == "BFR/S78-073":
                others = sum(
                    1 for i, c in enumerate(p.stage) if i != stage_idx and c and "遊戲" in c.traits
                )
                if others >= 2:
                    pwr += 2000

            if card.has_effect("CONT_ALL_GAME_BUFF_3000") or card.id == "BFR/S78-058":
                stage_chars = [c for c in p.stage if c is not None]
                if stage_chars and all("遊戲" in c.traits for c in stage_chars):
                    pwr += 3000

            if card.has_effect("CONT_OPP_BACKROW_BUFF_1500") or card.id == "BFR/S78-089":
                opp_back = sum(1 for i in [3, 4] if opp.stage[i] is not None)
                pwr += opp_back * 1500

            if stage_idx in [0, 1, 2] and "遊戲" in card.traits:
                char_lvl = RuleEngine.get_effective_level(p, card, stage_idx)
                if stage_idx in [0, 1] and p.stage[3] and (p.stage[3].has_effect("CONT_LEVEL_ASSIST") or p.stage[3].id == "BFR/S78-102"):
                    pwr += char_lvl * 500
                if stage_idx in [1, 2] and p.stage[4] and (p.stage[4].has_effect("CONT_LEVEL_ASSIST") or p.stage[4].id == "BFR/S78-102"):
                    pwr += char_lvl * 500

            # 孤獨搖滾 (BTR/W107) 永續加成
            if card.has_effect("CONT_OTHER_MUSIC_500_EACH") or card.id == "BTR/W107-076":
                other_music = sum(
                    1 for i, c in enumerate(p.stage) if i != stage_idx and c and "音樂" in c.traits
                )
                pwr += other_music * 500

            if card.has_effect("CONT_OTHER_2MUSIC_BUFF_3000") or card.id == "BTR/W107-075":
                other_music = sum(
                    1 for i, c in enumerate(p.stage) if i != stage_idx and c and "音樂" in c.traits
                )
                if other_music >= 2:
                    pwr += 3000

            if card.name == "主唱吉他手 喜多郁代" or card.id == "BTR/W107-T16":
                bocchi_support = sum(
                    1
                    for i, c in enumerate(p.stage)
                    if i != stage_idx
                    and c
                    and (c.has_effect("CONT_BUFF_VOCAL_KITA_1000_1SOUL") or c.id == "BTR/W107-T13")
                )
                pwr += bocchi_support * 1000

            # GA文庫 (GA/S131) 自回合永續加成
            if is_my_turn:
                if card.has_effect("CONT_YOUR_TURN_1000") or card.id == "GA04/S131-100":
                    pwr += 1000
                if card.has_effect("CONT_YOUR_TURN_6000") or card.id == "GA17/S131-015":
                    pwr += 6000
                if card.has_effect("CONT_YOUR_TURN_11000") or card.id == "GA17/S131-017":
                    pwr += 11000
                if (card.has_effect("CONT_HAND5_BUFF_2000") or card.id == "GA10/S131-T09") and len(p.hand) >= 5:
                    pwr += 2000

            return pwr

        @staticmethod
        def get_effective_soul(p: PlayerState, card: CardInstance, stage_idx: int) -> int:
            if not card or card.type != "CHAR":
                return 0
            soul = card.base_soul + card.temp_soul
            if p.climax_zone and (
                p.climax_zone.has_effect("CX_ALL_1000_1SOUL")
                or p.climax_zone.id in ["BFR/S78-107", "GA10/S131-030", "GA17/S131-033"]
            ):
                soul += 1
            if card.name == "主唱吉他手 喜多郁代" or card.id == "BTR/W107-T16":
                bocchi_support = sum(
                    1
                    for i, c in enumerate(p.stage)
                    if i != stage_idx
                    and c
                    and (c.has_effect("CONT_BUFF_VOCAL_KITA_1000_1SOUL") or c.id == "BTR/W107-T13")
                )
                soul += bocchi_support
            return max(0, soul)

        @staticmethod
        def can_play_card(p: PlayerState, card: CardInstance) -> bool:
            eff_lvl = RuleEngine.get_effective_level(p, card, None)
            if card.type in ["CHAR", "EVENT"]:
                if eff_lvl > len(p.level_zone) or card.cost > len(p.stock):
                    return False
                if card.has_effect("CONT_IGNORE_SELF_COLOR") or card.id == "GA01/S131-115":
                    return True
                if eff_lvl >= 1:
                    colors = {c.color for c in p.level_zone + p.clock}
                    if card.color not in colors:
                        return False
                return True
            elif card.type == "CX":
                if any(c and (c.has_effect("CONT_IGNORE_CX_COLOR") or c.id == "BFR/S78-031") for c in p.stage):
                    return True
                colors = {c.color for c in p.level_zone + p.clock}
                return card.color in colors
            return False

        @staticmethod
        def pay_stock(p: PlayerState, amount: int):
            for _ in range(amount):
                if p.stock:
                    p.waiting_room.append(p.stock.pop())

        @staticmethod
        def ai_declare_level_random() -> int:
            return random.choice([0, 1, 2, 3])



try:
    from network import WSNetNode
except ImportError:
    import json
    import os
    import re
    import socket
    import sys
    import threading
    import urllib.request
    import xml.etree.ElementTree as ET

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != BASE_DIR:
        os.chdir(BASE_DIR)
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)


    class WSNetNode:
        """提供區網與跨外網雙人對戰 Host 與 Client 封包通訊，支援 UPnP 自動開埠與域名隧道連線"""

        def __init__(self, on_msg_callback, on_disconnect_callback=None):
            self.on_msg = on_msg_callback
            self.on_disconnect = on_disconnect_callback
            self.sock = None
            self.conn = None
            self.is_host = False
            self.connected = False
            self._send_lock = threading.Lock()

        @staticmethod
        def get_local_ip() -> str:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except Exception:
                try:
                    return socket.gethostbyname(socket.gethostname())
                except Exception:
                    return "127.0.0.1"

        @staticmethod
        def get_public_ip_async(callback):
            """背景非阻塞查詢本機外網公網 IPv4"""
            def worker():
                for url in ["https://api.ipify.org", "https://ident.me", "https://ifconfig.me/ip"]:
                    try:
                        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=3.5) as resp:
                            ip = resp.read().decode("utf-8").strip()
                            if ip and "." in ip and len(ip) <= 16:
                                callback(ip)
                                return
                    except Exception:
                        pass
                callback(None)

            threading.Thread(target=worker, daemon=True).start()

        @staticmethod
        def parse_host_port(raw_address: str, default_port: int = 15780):
            """自動解析 'IP:Port'、'tcp://domain:port' 或純 IP/域名"""
            addr = raw_address.strip()
            for prefix in ["tcp://", "http://", "https://"]:
                if addr.lower().startswith(prefix):
                    addr = addr[len(prefix):]
            addr = addr.strip("/")
            if ":" in addr:
                host_part, port_part = addr.rsplit(":", 1)
                try:
                    return host_part.strip(), int(port_part.strip())
                except ValueError:
                    return addr, int(default_port)
            return addr, int(default_port)

        @staticmethod
        def try_upnp_forward_async(port: int, callback=None):
            """使用純 Python 標準庫發送 SSDP 與 UPnP SOAP 自動向家用路由器申請外網 Port 轉發"""
            def worker():
                local_ip = WSNetNode.get_local_ip()
                ssdp_req = (
                    "M-SEARCH * HTTP/1.1\r\n"
                    "HOST: 239.255.255.250:1900\r\n"
                    "MAN: \"ssdp:discover\"\r\n"
                    "MX: 2\r\n"
                    "ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n"
                )
                try:
                    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    udp.settimeout(2.2)
                    udp.sendto(ssdp_req.encode("utf-8"), ("239.255.255.250", 1900))
                    resp_data, _ = udp.recvfrom(4096)
                    udp.close()
                    resp_text = resp_data.decode("utf-8", errors="ignore")
                    loc_match = re.search(r"(?i)LOCATION:\s*(http://[^\r\n]+)", resp_text)
                    if not loc_match:
                        if callback:
                            callback(False, "未偵測到支援 UPnP 的路由器回應")
                        return
                    desc_url = loc_match.group(1).strip()
                    from urllib.parse import urljoin
                    with urllib.request.urlopen(desc_url, timeout=3.0) as r:
                        xml_text = r.read().decode("utf-8", errors="ignore")

                    control_url = None
                    service_type = None
                    for st in [
                        "urn:schemas-upnp-org:service:WANIPConnection:1",
                        "urn:schemas-upnp-org:service:WANPPPConnection:1",
                    ]:
                        if st in xml_text:
                            idx = xml_text.find(st)
                            sub = xml_text[idx:idx + 1500]
                            c_match = re.search(r"<controlURL>([^<]+)</controlURL>", sub)
                            if c_match:
                                service_type = st
                                control_url = urljoin(desc_url, c_match.group(1).strip())
                                break
                    if not control_url or not service_type:
                        if callback:
                            callback(False, "路由器未開放 WANIPConnection 介面")
                        return

                    soap_body = f"""<?xml version="1.0"?>
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
    <u:AddPortMapping xmlns:u="{service_type}">
    <NewRemoteHost></NewRemoteHost>
    <NewExternalPort>{port}</NewExternalPort>
    <NewProtocol>TCP</NewProtocol>
    <NewInternalPort>{port}</NewInternalPort>
    <NewInternalClient>{local_ip}</NewInternalClient>
    <NewEnabled>1</NewEnabled>
    <NewPortMappingDescription>WS_Simulator_TCP_{port}</NewPortMappingDescription>
    <NewLeaseDuration>0</NewLeaseDuration>
    </u:AddPortMapping>
    </s:Body>
    </s:Envelope>"""
                    req = urllib.request.Request(
                        control_url,
                        data=soap_body.encode("utf-8"),
                        headers={
                            "Content-Type": "text/xml; charset=\"utf-8\"",
                            "SOAPAction": f'"{service_type}#AddPortMapping"',
                        },
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=3.5) as sr:
                        if sr.status in (200, 201):
                            if callback:
                                callback(True, f"UPnP 自動開埠成功 (TCP Port {port})")
                            return
                except Exception as e:
                    if callback:
                        callback(False, f"UPnP 未生效 ({e})")
                    return
                if callback:
                    callback(False, "UPnP 未生效")

            threading.Thread(target=worker, daemon=True).start()

        def start_host(self, port=15780):
            self.is_host = True
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", int(port)))
            self.sock.listen(1)
            threading.Thread(target=self._accept_worker, daemon=True).start()

        def _accept_worker(self):
            try:
                conn, addr = self.sock.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.conn = conn
                self.connected = True
                if self.on_msg:
                    self.on_msg({"type": "SYS_CONNECTED", "peer": f"{addr[0]}:{addr[1]}"})
                self._recv_loop(conn)
            except Exception as e:
                if self.connected and self.on_msg:
                    self.on_msg({"type": "SYS_ERROR", "error": str(e)})

        def connect_to_host(self, ip_or_host, port=15780):
            self.is_host = False
            host, parsed_port = self.parse_host_port(ip_or_host, default_port=port)

            def worker():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(8.0)
                    s.connect((host, int(parsed_port)))
                    s.settimeout(None)
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    self.conn = s
                    self.connected = True
                    if self.on_msg:
                        self.on_msg({"type": "SYS_CONNECTED", "peer": f"{host}:{parsed_port}"})
                    self._recv_loop(s)
                except Exception as e:
                    if self.on_msg:
                        self.on_msg({"type": "SYS_ERROR", "error": str(e)})

            threading.Thread(target=worker, daemon=True).start()

        def _recv_loop(self, conn):
            buf = ""
            while self.connected:
                try:
                    data = conn.recv(16384)
                    if not data:
                        break
                    buf += data.decode("utf-8", errors="replace")
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if line:
                            try:
                                msg = json.loads(line)
                                if self.on_msg:
                                    self.on_msg(msg)
                            except Exception:
                                pass
                except Exception:
                    break
            self.connected = False
            if self.on_disconnect:
                try:
                    self.on_disconnect()
                except Exception:
                    pass

        def send(self, payload: dict) -> bool:
            if self.connected and self.conn:
                try:
                    raw = json.dumps(payload, ensure_ascii=False) + "\n"
                    with self._send_lock:
                        self.conn.sendall(raw.encode("utf-8"))
                    return True
                except Exception:
                    self.connected = False
            return False

        def send_action_log(self, text: str, player_state_dict: dict = None, opp_state_dict: dict = None):
            payload = {"type": "ACTION_LOG", "text": text}
            if player_state_dict is not None:
                payload["sender_state"] = player_state_dict
            if opp_state_dict is not None:
                payload["receiver_state"] = opp_state_dict
            return self.send(payload)

        def close(self):
            self.connected = False
            for s in (self.conn, self.sock):
                if s:
                    try:
                        s.close()
                    except Exception:
                        pass
            self.conn = None
            self.sock = None


# ==========================================
# 全域中文化對照表（階段名稱、卡片種類、判別標記）
# ==========================================
CARD_TYPE_ZH = {
    "CHAR": "角色",
    "EVENT": "事件",
    "CX": "名場面",
}

TRIGGER_ZH = {
    "NONE": "無",
    "SOUL": "+1魂傷",
    "STANDBY": "開機",
    "GATE": "城門",
    "CHOICE": "箭頭",
    "WIND": "風",
    "DRAW": "抽牌",
    "SHOT": "射擊",
    "TREASURE": "金磚",
    "BAG": "金袋",
    "BOOK": "書",
}

PHASE_ZH = {
    "SETUP": "開局準備",
    "MULLIGAN": "起手換牌",
    "CLOCK": "時計階段",
    "AI_CLOCK": "時計階段",
    "MAIN": "主要階段",
    "CLIMAX": "名場面階段",
    "ATTACK": "戰鬥階段",
    "ENCORE": "安可階段",
    "END": "結束階段",
    "OPP_TURN": "對手回合",
}


def get_card_type_zh(raw_type: str) -> str:
    return CARD_TYPE_ZH.get(raw_type, raw_type)


def get_trigger_zh(raw_trig: str) -> str:
    return TRIGGER_ZH.get(raw_trig, raw_trig)


def get_phase_zh(raw_phase: str) -> str:
    return PHASE_ZH.get(raw_phase, raw_phase)


def is_counter_only_event(card) -> bool:
    if not card or getattr(card, "type", "") != "EVENT":
        return False
    if card.id == "BFR/S78-075" or card.has_effect("EVENT_COUNTER_2500_MEMORY"):
        return True
    txt = getattr(card, "text", "")
    return txt.startswith("【反擊】")


# ==========================================
# 遊戲音效與背景音樂合成＆播放系統 (SoundManager)
# ==========================================
import math
import struct
import wave


class SoundManager:
    """
    跨平台零相依性音效與背景音樂管理系統：
    1. 啟動時自動於 ./ws_audio/ 合成高音質立體聲 .wav 音樂與音效：
       - 主選單音樂 (bgm_menu.wav)
       - 主要階段音樂 (bgm_main.wav)
       - 戰鬥階段音樂 (bgm_battle.wav)
       - 點擊音效 (sfx_click.wav)
       - 抽卡音效 (sfx_draw.wav)
       - 扣血命中音效 (sfx_damage.wav)
       - 翻出名場面/傷害取消音效 (sfx_climax.wav)
    2. 支援玩家於「遊戲設定」調整 BGM 音量、SFX 音量、開關靜音，或上傳自訂 .mp3/.wav 音樂替換。
    3. Windows 平台採用原生 winmm.dll MCI 多軌混音（BGM 可循環播放且與 SFX 同時發聲互不中斷）。
    """

    TRACK_KEYS = [
        ("bgm_menu", "主選單音樂", "bgm_menu.wav"),
        ("bgm_main", "主要階段音樂", "bgm_main.wav"),
        ("bgm_battle", "戰鬥階段音樂", "bgm_battle.wav"),
        ("sfx_click", "點擊音效", "sfx_click.wav"),
        ("sfx_draw", "抽卡音效", "sfx_draw.wav"),
        ("sfx_damage", "扣血命中音效", "sfx_damage.wav"),
        ("sfx_climax", "翻到名場面音效", "sfx_climax.wav"),
    ]

    def __init__(self, app):
        self.app = app
        self.audio_dir = os.path.join(BASE_DIR, "ws_audio")
        os.makedirs(self.audio_dir, exist_ok=True)
        self.current_bgm_key = None
        self._mci = None
        if os.name == "nt":
            try:
                import ctypes
                self._mci = ctypes.windll.winmm.mciSendStringW
            except Exception:
                self._mci = None
        self.default_files = {}
        for k, _, fname in self.TRACK_KEYS:
            self.default_files[k] = os.path.join(self.audio_dir, fname)
        threading.Thread(target=self._ensure_synthesized_assets, daemon=True).start()

    def _mci_cmd(self, cmd: str):
        if self._mci is not None:
            try:
                self._mci(cmd, None, 0, 0)
            except Exception:
                pass

    def _write_wav_mono(self, filepath: str, samples: list, sample_rate: int = 22050):
        if os.path.exists(filepath) and os.path.getsize(filepath) > 200:
            return
        try:
            with wave.open(filepath, "w") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                buf = bytearray()
                for s in samples:
                    v = max(-32767, min(32767, int(s * 32767.0)))
                    buf.extend(struct.pack("<h", v))
                wf.writeframes(bytes(buf))
        except Exception:
            pass

    def _ensure_synthesized_assets(self):
        sr = 22050
        two_pi = 2.0 * math.pi

        # 1. sfx_click.wav: 清脆《Master Duel》風格金屬科技點擊音 (0.08s)
        p_click = self.default_files["sfx_click"]
        if not os.path.exists(p_click):
            n = int(sr * 0.075)
            s = []
            for i in range(n):
                t = i / sr
                env = math.exp(-t * 48.0)
                f = 1320.0 if t < 0.025 else 1760.0
                val = (0.65 * math.sin(two_pi * f * t) + 0.35 * math.sin(two_pi * f * 2.0 * t)) * env * 0.55
                s.append(val)
            self._write_wav_mono(p_click, s, sr)

        # 2. sfx_draw.wav: 順暢刷卡抽牌刷動音 (0.18s)
        p_draw = self.default_files["sfx_draw"]
        if not os.path.exists(p_draw):
            n = int(sr * 0.18)
            s = []
            rng = random.Random(78)
            for i in range(n):
                t = i / sr
                env = math.sin(math.pi * (i / n)) ** 1.4
                sweep_f = 520.0 + 1480.0 * (i / n)
                noise = (rng.random() * 2.0 - 1.0) * 0.35
                tone = math.sin(two_pi * sweep_f * t) * 0.45
                s.append((noise + tone) * env * 0.6)
            self._write_wav_mono(p_draw, s, sr)

        # 3. sfx_damage.wav: 重低音雷擊扣血命中音效 (0.38s)
        p_dmg = self.default_files["sfx_damage"]
        if not os.path.exists(p_dmg):
            n = int(sr * 0.38)
            s = []
            rng = random.Random(131)
            for i in range(n):
                t = i / sr
                env = math.exp(-t * 8.5)
                drop_f = max(55.0, 240.0 - 480.0 * t)
                sub = math.sin(two_pi * drop_f * t) * 0.7
                crunch = (rng.random() * 2.0 - 1.0) * math.exp(-t * 16.0) * 0.45
                s.append(max(-0.95, min(0.95, (sub + crunch) * env * 0.85)))
            self._write_wav_mono(p_dmg, s, sr)

        # 4. sfx_climax.wav: 華麗聖光豎琴琶音 (翻到名場面 / 傷害取消！ 0.65s)
        p_cx = self.default_files["sfx_climax"]
        if not os.path.exists(p_cx):
            n = int(sr * 0.65)
            notes = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98]
            s = []
            for i in range(n):
                t = i / sr
                idx_n = min(len(notes) - 1, int(t / 0.08))
                f = notes[idx_n]
                local_t = t - idx_n * 0.08
                env = math.exp(-local_t * 6.0) * math.exp(-t * 1.8)
                val = (
                    0.6 * math.sin(two_pi * f * t)
                    + 0.25 * math.sin(two_pi * f * 2.0 * t)
                    + 0.15 * math.sin(two_pi * 1046.50 * t)
                ) * env * 0.7
                s.append(val)
            self._write_wav_mono(p_cx, s, sr)

        # 5. bgm_menu.wav: 《Master Duel》交響神秘氛圍主選單配樂 (8.0s 無縫循環)
        p_menu = self.default_files["bgm_menu"]
        if not os.path.exists(p_menu):
            dur = 8.0
            n = int(sr * dur)
            chords = [
                (220.0, 261.63, 329.63, 440.0),  # Am
                (174.61, 220.0, 261.63, 349.23), # F
                (130.81, 196.0, 261.63, 329.63), # C
                (196.0, 246.94, 293.66, 392.0),  # G
            ]
            s = []
            for i in range(n):
                t = i / sr
                c_idx = int(t / 2.0) % 4
                c_notes = chords[c_idx]
                arp_idx = int((t % 2.0) / 0.25) % 4
                arp_f = c_notes[arp_idx] * 2.0
                arp_t = (t % 0.25)
                arp_env = math.exp(-arp_t * 7.5)
                pad = (
                    0.28 * math.sin(two_pi * c_notes[0] * t)
                    + 0.22 * math.sin(two_pi * c_notes[1] * t)
                    + 0.20 * math.sin(two_pi * c_notes[2] * t)
                )
                arp = 0.26 * math.sin(two_pi * arp_f * t) * arp_env
                fade = min(1.0, t / 0.15, (dur - t) / 0.15)
                s.append((pad + arp) * 0.42 * fade)
            self._write_wav_mono(p_menu, s, sr)

        # 6. bgm_main.wav: 輕快戰術思考主要階段配樂 (6.4s 無縫循環)
        p_main = self.default_files["bgm_main"]
        if not os.path.exists(p_main):
            dur = 6.4
            n = int(sr * dur)
            prog = [
                (293.66, 349.23, 440.0, 523.25), # Dm7
                (196.0, 246.94, 293.66, 349.23), # G7
                (261.63, 329.63, 392.0, 493.88), # Cmaj7
                (220.0, 261.63, 329.63, 392.0),  # Am7
            ]
            s = []
            for i in range(n):
                t = i / sr
                c_idx = int(t / 1.6) % 4
                cn = prog[c_idx]
                step_i = int((t % 1.6) / 0.2) % 4
                lead_f = cn[step_i] * 1.5
                step_t = t % 0.2
                lead_env = math.exp(-step_t * 9.0)
                bass = 0.30 * math.sin(two_pi * (cn[0] * 0.5) * t)
                chord = 0.20 * math.sin(two_pi * cn[1] * t) + 0.18 * math.sin(two_pi * cn[2] * t)
                lead = 0.28 * math.sin(two_pi * lead_f * t) * lead_env
                fade = min(1.0, t / 0.12, (dur - t) / 0.12)
                s.append((bass + chord + lead) * 0.44 * fade)
            self._write_wav_mono(p_main, s, sr)

        # 7. bgm_battle.wav: 熱血疾走戰鬥階段配樂 (4.8s 無縫循環)
        p_battle = self.default_files["bgm_battle"]
        if not os.path.exists(p_battle):
            dur = 4.8
            n = int(sr * dur)
            prog = [
                (164.81, 246.94, 329.63, 392.0), # Em
                (130.81, 196.0, 261.63, 329.63), # C
                (146.83, 220.0, 293.66, 369.99), # D
                (196.0, 246.94, 293.66, 392.0),  # G
            ]
            melody = [659.25, 783.99, 880.0, 783.99, 659.25, 587.33, 659.25, 783.99]
            s = []
            for i in range(n):
                t = i / sr
                c_idx = int(t / 1.2) % 4
                cn = prog[c_idx]
                m_idx = int((t % 1.2) / 0.15) % 8
                m_f = melody[m_idx]
                m_t = t % 0.15
                m_env = math.exp(-m_t * 11.0)
                pulse = 1.0 if int(t / 0.075) % 2 == 0 else 0.65
                bass = 0.35 * math.sin(two_pi * cn[0] * t) * pulse
                power = 0.22 * math.sin(two_pi * cn[1] * t) + 0.20 * math.sin(two_pi * cn[2] * t)
                lead = 0.34 * math.sin(two_pi * m_f * t) * m_env
                fade = min(1.0, t / 0.1, (dur - t) / 0.1)
                s.append((bass + power + lead) * 0.48 * fade)
            self._write_wav_mono(p_battle, s, sr)

    def get_track_path(self, key: str) -> str:
        custom_map = self.app.settings.get("custom_audio_paths") or {}
        if key in custom_map and custom_map[key]:
            raw_p = str(custom_map[key]).strip()
            if os.path.exists(raw_p):
                return os.path.abspath(raw_p)
            rel_p = os.path.join(BASE_DIR, raw_p)
            if os.path.exists(rel_p):
                return os.path.abspath(rel_p)
            in_audio_p = os.path.join(self.audio_dir, os.path.basename(raw_p))
            if os.path.exists(in_audio_p):
                return os.path.abspath(in_audio_p)
        # 優先自動偵測 ./ws_audio/<key>.mp3（若玩家直接放入同名 .mp3 即自動採用）
        mp3_candidate = os.path.join(self.audio_dir, f"{key}.mp3")
        if os.path.exists(mp3_candidate) and os.path.getsize(mp3_candidate) > 100:
            return os.path.abspath(mp3_candidate)
        return self.default_files.get(key, "")

    def get_bgm_mci_volume(self, bgm_key: str = None) -> int:
        """
        計算背景音樂 (BGM) 的 MCI 音量值：
        - 依玩家需求，BGM 100% 音量上限設定為原始滿音量的 1/10（即 MCI 100 / 1000）
        - 結合 BGM 總音量 (0~100%) 與單曲個別音量 (0~100%)，最低可微調至 MCI 1 / 1000 極小聲
        """
        t_key = bgm_key or self.current_bgm_key or "bgm_menu"
        master_v = float(self.app.settings.get("bgm_volume", 50))
        track_map = self.app.settings.get("track_volumes") or {}
        track_v = float(track_map.get(t_key, 100))
        if master_v <= 0 or track_v <= 0:
            return 0
        # 100% 對應 MCI 100（原本 1000 的十分之一）
        raw_mci = (master_v / 100.0) * (track_v / 100.0) * 100.0
        return max(1, min(100, int(round(raw_mci))))

    def get_sfx_mci_volume(self, sfx_key: str) -> int:
        """
        計算動作音效 (SFX) 的 MCI 音量值：
        - 維持 SFX 正常音量上限（100% 對應 MCI 1000），並結合 SFX 總音量與各音效個別音量 (0~100%)
        """
        master_v = float(self.app.settings.get("sfx_volume", 80))
        track_map = self.app.settings.get("track_volumes") or {}
        track_v = float(track_map.get(sfx_key, 100))
        if master_v <= 0 or track_v <= 0:
            return 0
        raw_mci = (master_v / 100.0) * (track_v / 100.0) * 1000.0
        return max(1, min(1000, int(round(raw_mci))))

    def play_bgm(self, bgm_key: str, force_restart: bool = False):
        if not self.app.settings.get("bgm_enabled", True):
            self.stop_bgm()
            return
        mci_vol = self.get_bgm_mci_volume(bgm_key)
        if mci_vol <= 0:
            self.stop_bgm()
            return
        if self.current_bgm_key == bgm_key and not force_restart:
            self.update_bgm_volume()
            return
        path = self.get_track_path(bgm_key)
        if not path or not os.path.exists(path):
            return
        self.current_bgm_key = bgm_key
        if self._mci is not None:
            self._mci_cmd("close ws_bgm")
            self._mci_cmd(f'open "{path}" type mpegvideo alias ws_bgm')
            self._mci_cmd(f"setaudio ws_bgm volume to {mci_vol}")
            self._mci_cmd("play ws_bgm repeat")

    def update_bgm_volume(self):
        if not self.app.settings.get("bgm_enabled", True):
            self.stop_bgm()
            return
        if not self.current_bgm_key:
            return
        mci_vol = self.get_bgm_mci_volume(self.current_bgm_key)
        if mci_vol <= 0:
            self.stop_bgm()
            return
        if self._mci is not None:
            self._mci_cmd(f"setaudio ws_bgm volume to {mci_vol}")

    def stop_bgm(self):
        self.current_bgm_key = None
        if self._mci is not None:
            self._mci_cmd("close ws_bgm")

    def play_sfx(self, sfx_key: str):
        if not self.app.settings.get("sfx_enabled", True):
            return
        mci_vol = self.get_sfx_mci_volume(sfx_key)
        if mci_vol <= 0:
            return
        path = self.get_track_path(sfx_key)
        if not path or not os.path.exists(path):
            return
        if self._mci is not None:
            alias = f"ws_sfx_{sfx_key}"
            self._mci_cmd(f"close {alias}")
            self._mci_cmd(f'open "{path}" type mpegvideo alias {alias}')
            self._mci_cmd(f"setaudio {alias} volume to {mci_vol}")
            self._mci_cmd(f"play {alias} from 0")


# ==========================================
# 本地 .webp 圖檔讀取與實體卡面繪製管理模組
# ==========================================
class ImageManager:

    def __init__(self, root):
        self.root = root
        self.local_webp_dir = os.path.join(BASE_DIR, "ws_card_images")
        os.makedirs(self.local_webp_dir, exist_ok=True)
        self._write_folder_readme()

        self.pil_cache = {}
        self.tk_cache = {}
        self.hand_dock_cache = {}
        self.empty_slot_cache = {}
        self.deck_stack_cache = {}
        self.stock_stack_cache = {}
        self.ai_fan_cache = {}
        self.sleeve_pil_cache = {}
        self.avatar_cache = {}
        self.bg_cache = {}
        self.active_sleeve_style = "WS_DEFAULT"
        self.custom_sleeve_path = "" 
        self.callbacks = []
        self.font_title = self._load_font(16)
        self.font_sub = self._load_font(12)

        self._purge_synthetic_high_rarity_images()
        self._create_stylized_cards()
        self.load_local_images()
        self.start_background_download()

    def _write_folder_readme(self):
        readme_path = os.path.join(self.local_webp_dir, "請將webp卡圖放此資料夾_檔名對照表.txt")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("=== 本地 .webp 卡圖命名對照表 ===\n")
                f.write("請將卡圖放入此 ws_card_images 資料夾，檔名格式如下：\n\n")
                for cid, data in CARD_DB.items():
                    fname = cid.replace("/", "_").replace("-", "_") + ".webp"
                    f.write(f"{fname} --> {data['name']} ({cid})\n")

    def _load_font(self, size):
        for fname in ["msjhbd.ttc", "msjh.ttc", "simhei.ttf", "arial.ttf"]:
            try:
                return ImageFont.truetype(fname, size)
            except Exception:
                pass
        return ImageFont.load_default()

    def get_base_filename(self, cid: str) -> str:
        return cid.replace("/", "_").replace("-", "_")

    def _normalize_card_orientation(self, cid: str, img: Image.Image) -> Image.Image:
        """所有卡片（包含名場面 CX）在基礎快取中統一保持直立（豎向 height >= width），僅於放到場上名場面區時橫置呈現"""
        if img.width > img.height:
            return img.transpose(Image.Transpose.ROTATE_270)
        return img

    def _purge_synthetic_high_rarity_images(self):
        """清除舊版人工合成濾鏡圖檔，讓系統自動從貓罐子 (img.bottleneko.app) 與官網抓取真實異畫/簽卡圖檔"""
        marker = os.path.join(self.local_webp_dir, ".real_bottleneko_art_v2")
        if os.path.exists(marker):
            return
        old_synthetic_names = ['BFR_S78_001SP.webp', 'BFR_S78_015S.webp', 'BFR_S78_031SP.webp', 'BFR_S78_057S.webp', 'BFR_S78_058SP.webp', 'BFR_S78_060S.webp', 'BFR_S78_061S.webp', 'BFR_S78_062S.webp', 'BFR_S78_063S.webp', 'BFR_S78_064S.webp', 'BFR_S78_069S.webp', 'BFR_S78_072S.webp', 'BFR_S78_073S.webp', 'BFR_S78_075S.webp', 'BFR_S78_076R.webp', 'BFR_S78_077R.webp', 'BFR_S78_078R.webp', 'BFR_S78_081SP.webp', 'BFR_S78_083S.webp', 'BFR_S78_087S.webp', 'BFR_S78_089S.webp', 'BFR_S78_102S.webp', 'BFR_S78_107R.webp', 'BTR_W107_046KBR.webp', 'BTR_W107_069SSP.webp', 'BTR_W107_075S.webp', 'BTR_W107_076S.webp', 'BTR_W107_077S.webp', 'BTR_W107_089S.webp', 'BTR_W107_098OFR.webp', 'BTR_W107_100R.webp', 'BTR_W107_T02R.webp', 'BTR_W107_T06R.webp', 'BTR_W107_T10R.webp', 'BTR_W107_T13R.webp', 'BTR_W107_T14SP.webp', 'BTR_W107_T15R.webp', 'BTR_W107_T16R.webp', 'BTR_W107_T17R.webp', 'BTR_W107_T18R.webp', 'GA01_S131_115GA.webp', 'GA02_S131_003SP.webp', 'GA02_S131_009S.webp', 'GA04_S131_100SP.webp', 'GA05_S131_007SP.webp', 'GA08_S131_038SP.webp', 'GA10_S131_002S.webp', 'GA10_S131_012GA.webp', 'GA10_S131_019S.webp', 'GA10_S131_029S.webp', 'GA10_S131_030R.webp', 'GA10_S131_T09SP.webp', 'GA12_S131_013S.webp', 'GA13_S131_077SP.webp', 'GA17_S131_010SP.webp', 'GA17_S131_014GA.webp', 'GA17_S131_015S.webp', 'GA17_S131_017S.webp', 'GA17_S131_033R.webp']
        for fn in old_synthetic_names:
            p = os.path.join(self.local_webp_dir, fn)
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        try:
            with open(marker, "w", encoding="utf-8") as f:
                f.write("real_bottleneko_art_v2\n")
        except Exception:
            pass

    def _create_single_stylized_card(self, cid: str, data: dict) -> Image.Image:
        color_theme = {
            "紅": ("#5e1720", "#ff6b6b"),
            "藍": ("#152a4a", "#4cc9f0"),
            "黃": ("#594a15", "#ffd166"),
            "綠": ("#164a2b", "#06d6a0"),
            "紫": ("#3c1b5c", "#c77dff"),
        }
        bg, border = color_theme.get(data.get("color", "黃"), ("#2b2b36", "#aaaaaa"))
        img = Image.new("RGB", (200, 280), color=bg)
        draw = ImageDraw.Draw(img)
        draw.rectangle([4, 4, 195, 275], outline=border, width=4)
        draw.rectangle([12, 48, 187, 195], fill="#191922", outline=border, width=1)
        name = data.get("name", cid)
        line1, line2 = name[:6], name[6:12]
        if data.get("type") == "CX":
            draw.text((16, 16), "【名場面】", fill="#ffd166", font=self.font_title)
            draw.text((18, 95), line1, fill="#ffffff", font=self.font_title)
            if line2:
                draw.text((18, 125), line2, fill="#ffd166", font=self.font_title)
        else:
            draw.ellipse([10, 10, 44, 44], fill=border)
            draw.text((16, 15), f"L{data.get('level', 0)}", fill="#000000", font=self.font_title)
            draw.text((50, 16), f"費用:{data.get('cost', 0)} [{get_card_type_zh(data.get('type', 'CHAR'))}]", fill="#ffffff", font=self.font_sub)
            draw.text((18, 90), line1, fill="#ffffff", font=self.font_title)
            if line2:
                draw.text((18, 120), line2, fill="#ffd166", font=self.font_title)
            draw.rectangle([12, 232, 187, 266], fill="#0f0f14", outline=border, width=2)
            if data.get("type") == "CHAR":
                draw.text((18, 239), f"攻:{data.get('power', 0)} 魂:{data.get('soul', 1)}", fill="#ffffff", font=self.font_sub)
            else:
                draw.text((18, 239), f"標記:{get_trigger_zh(data.get('trigger', 'NONE'))}", fill="#ffd166", font=self.font_sub)
        self.pil_cache[cid] = img
        return img

    def load_local_images(self, only_missing: bool = False) -> int:
        loaded_count = 0
        loaded_cids = set()
        for cid, cdata in CARD_DB.items():
            if only_missing and cid in self.pil_cache:
                loaded_cids.add(cid)
                continue
            base_name = self.get_base_filename(cid)
            candidates = [
                f"{base_name}.webp",
                f"{base_name.lower()}.webp",
                f"{base_name}.png",
                f"{base_name.lower()}.png",
                f"{base_name}.jpg",
            ]
            for cand in candidates:
                full_path = os.path.join(self.local_webp_dir, cand)
                if os.path.exists(full_path) and os.path.getsize(full_path) > 100:
                    try:
                        img = Image.open(full_path).convert("RGB")
                        img = self._normalize_card_orientation(cid, img)
                        self.pil_cache[cid] = img
                        loaded_cids.add(cid)
                        loaded_count += 1
                        break
                    except Exception:
                        pass
        # 若高版本真實卡圖尚在背景下載中，暫時顯示原版卡圖避免空白方塊，待背景下載完成後自動替換為真實高版本異畫
        for cid, data in CARD_DB.items():
            if cid not in self.pil_cache:
                base_id = data.get("base_id", cid)
                if data.get("is_high_rarity") and base_id in self.pil_cache:
                    self.pil_cache[cid] = self.pil_cache[base_id]
                else:
                    self._create_single_stylized_card(cid, data)
        self.tk_cache.clear()
        self.hand_dock_cache.clear()
        if hasattr(self, "clock_spread_cache"):
            self.clock_spread_cache.clear()
        if hasattr(self, "level_spread_cache"):
            self.level_spread_cache.clear()
        self.deck_stack_cache.clear()
        self.stock_stack_cache.clear()
        self.ai_fan_cache.clear()
        self.avatar_cache.clear()
        self.bg_cache.clear()
        self._notify_all()
        return loaded_count

    def _create_stylized_cards(self):
        color_theme = {
            "紅": ("#5e1720", "#ff6b6b"),
            "藍": ("#152a4a", "#4cc9f0"),
            "黃": ("#594a15", "#ffd166"),
            "綠": ("#164a2b", "#06d6a0"),
        }
        for cid, data in CARD_DB.items():
            bg, border = color_theme.get(data["color"], ("#2b2b36", "#aaaaaa"))
            if data["type"] == "CX":
                # 名場面 (CX) 在手牌與未上場時與其他牌一樣保持豎向 (200x280)
                img = Image.new("RGB", (200, 280), color=bg)
                draw = ImageDraw.Draw(img)
                draw.rectangle([4, 4, 195, 275], outline=border, width=4)
                draw.rectangle([12, 48, 187, 215], fill="#191922", outline=border, width=1)
                draw.text((16, 16), "【名場面】", fill="#ffd166", font=self.font_title)
                name = data["name"]
                line1, line2 = name[:6], name[6:]
                draw.text((18, 95), line1, fill="#ffffff", font=self.font_title)
                if line2:
                    draw.text((18, 125), line2, fill="#ffd166", font=self.font_title)
                fname_hint = self.get_base_filename(cid) + ".webp"
                draw.text((18, 168), fname_hint, fill="#adb5bd", font=self.font_sub)
                self.pil_cache[cid] = img
            else:
                img = Image.new("RGB", (200, 280), color=bg)
                draw = ImageDraw.Draw(img)
                draw.rectangle([4, 4, 195, 275], outline=border, width=4)
                draw.rectangle([12, 48, 187, 195], fill="#191922", outline=border, width=1)
                draw.ellipse([10, 10, 44, 44], fill=border)
                draw.text((16, 15), f"L{data['level']}", fill="#000000", font=self.font_title)
                draw.text(
                    (50, 16),
                    f"費用:{data['cost']} [{get_card_type_zh(data['type'])}]",
                    fill="#ffffff",
                    font=self.font_sub,
                )
                name = data["name"]
                line1, line2 = name[:6], name[6:]
                draw.text((18, 90), line1, fill="#ffffff", font=self.font_title)
                if line2:
                    draw.text((18, 120), line2, fill="#ffd166", font=self.font_title)
                fname_hint = self.get_base_filename(cid) + ".webp"
                draw.text((18, 160), fname_hint, fill="#adb5bd", font=self.font_sub)
                draw.rectangle([12, 232, 187, 266], fill="#0f0f14", outline=border, width=2)
                if data["type"] == "CHAR":
                    draw.text(
                        (18, 239),
                        f"攻:{data['power']} 魂:{data['soul']}",
                        fill="#ffffff",
                        font=self.font_sub,
                    )
                else:
                    draw.text(
                        (18, 239), f"標記:{get_trigger_zh(data['trigger'])}", fill="#ffd166", font=self.font_sub
                    )
                self.pil_cache[cid] = img

    def start_background_download(self):
        if getattr(self, "_bg_downloading", False):
            return
        self._bg_downloading = True
        def fetch_one_card(item):
            cid, data = item
            base_name = self.get_base_filename(cid)
            webp_path = os.path.join(self.local_webp_dir, f"{base_name}.webp")
            if os.path.exists(webp_path) and os.path.getsize(webp_path) > 100:
                return None
            lower_id = base_name.lower()
            prefix_part = cid.split("/")[0].lower() if "/" in cid else "ga"
            candidate_urls = [
                f"https://img.bottleneko.app/w_900,f_webp&q_80/{base_name}.png",
                f"https://img.bottleneko.app/{base_name}.png",
                f"https://img.bottleneko.app/w_360,f_webp&q_80/{base_name}.png",
            ]
            for u in list(data.get("parallel_urls", [])) + [data.get("url", "")]:
                if u and u not in candidate_urls:
                    candidate_urls.append(u)
            if "/S131-" in cid and not data.get("is_high_rarity"):
                candidate_urls.extend([
                    f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/{lower_id}.png",
                    f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/{prefix_part}_s131/{lower_id}.png",
                ])
            elif "/W107-" in cid:
                candidate_urls.extend([
                    f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/{lower_id}.png",
                ])
            for u in candidate_urls:
                if not u:
                    continue
                try:
                    req_headers = {
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                        ),
                        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    }
                    if "bottleneko.app" in u:
                        req_headers["Referer"] = "https://bottleneko.app/"
                    else:
                        req_headers["Referer"] = "https://ws-tcg.com/cardlist/"
                    raw_bytes = None
                    if requests is not None:
                        r = requests.get(u, headers=req_headers, timeout=8)
                        if r.status_code == 200 and len(r.content) > 1000:
                            raw_bytes = r.content
                    else:
                        req = urllib.request.Request(u, headers=req_headers)
                        with urllib.request.urlopen(req, timeout=8) as resp:
                            content = resp.read()
                            if len(content) > 1000:
                                raw_bytes = content
                    if raw_bytes:
                        img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
                        img.save(webp_path, "WEBP", quality=92)
                        img = self._normalize_card_orientation(cid, img)
                        return (cid, img)
                except Exception:
                    pass
            return None

        def worker():
            import concurrent.futures
            # 自動下載官方預設 WS 卡背與 AmiAmi 特典角色卡套
            sleeve_targets = [
                (
                    "WS_DEFAULT",
                    "sleeve_ws_default.webp",
                    "https://static.wikia.nocookie.net/d4dj/images/c/cf/Wei%C3%9F_Schwarz_Card_Back.png/revision/latest?cb=20230109134612&path-prefix=zh",
                    "https://d4dj.fandom.com/",
                ),
                (
                    "AMIAMI_21593",
                    "sleeve_amiami_21593.webp",
                    "https://img.amiami.jp/images/product/main/232/CARD-00021593.jpg",
                    "https://www.amiami.jp/",
                ),
            ]
            sleeve_updated = False
            for s_key, s_fn, s_url, s_ref in sleeve_targets:
                s_path = os.path.join(self.local_webp_dir, s_fn)
                if not (os.path.exists(s_path) and os.path.getsize(s_path) > 500):
                    for use_ref in (True, False):
                        try:
                            s_hdr = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                            }
                            if use_ref and s_ref:
                                s_hdr["Referer"] = s_ref
                            raw_b = None
                            if requests is not None:
                                r = requests.get(s_url, headers=s_hdr, timeout=8)
                                if r.status_code == 200 and len(r.content) > 500:
                                    raw_b = r.content
                            else:
                                req = urllib.request.Request(s_url, headers=s_hdr)
                                with urllib.request.urlopen(req, timeout=8) as resp:
                                    c_b = resp.read()
                                    if len(c_b) > 500:
                                        raw_b = c_b
                            if raw_b:
                                s_im = Image.open(io.BytesIO(raw_b)).convert("RGB")
                                s_im.save(s_path, "WEBP", quality=92)
                                self.sleeve_pil_cache[s_key] = s_im
                                sleeve_updated = True
                                break
                        except Exception:
                            pass
            if sleeve_updated:
                self.deck_stack_cache.clear()
                self.stock_stack_cache.clear()
                self.ai_fan_cache.clear()
                self.root.after(60, self._notify_all)

            items = list(CARD_DB.items())
            updated_count = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for res in pool.map(fetch_one_card, items):
                    if res is not None:
                        cid, img = res
                        self.pil_cache[cid] = img
                        updated_count += 1
                        if updated_count % 24 == 0:
                            self.tk_cache.clear()
                            self.hand_dock_cache.clear()
                            self.root.after(80, self._notify_all)
            self._bg_downloading = False
            if updated_count > 0:
                self.tk_cache.clear()
                self.hand_dock_cache.clear()
                if hasattr(self, "clock_spread_cache"):
                    self.clock_spread_cache.clear()
                if hasattr(self, "level_spread_cache"):
                    self.level_spread_cache.clear()
                self.deck_stack_cache.clear()
                self.stock_stack_cache.clear()
                self.ai_fan_cache.clear()
                self.avatar_cache.clear()
                self.bg_cache.clear()
                self.root.after(80, self._notify_all)

        threading.Thread(target=worker, daemon=True).start()

    def _notify_all(self):
        for cb in self.callbacks:
            try:
                cb()
            except Exception:
                pass

    def get_card_visual(self, cid, width=84, height=118, state="STAND", is_selected=False):
        if hasattr(cid, "skin_id"):
            cid = cid.skin_id
        elif hasattr(cid, "id"):
            cid = cid.id
        if cid not in CARD_DB:
            cid = next(iter(CARD_DB.keys()))
        key = (cid, width, height, state, is_selected)
        if key in self.tk_cache:
            return self.tk_cache[key]

        c_data = CARD_DB.get(cid, {})
        src_img = self.pil_cache.get(cid)
        if src_img is None:
            src_img = self._create_single_stylized_card(cid, c_data)
        if c_data.get("type") == "CX":
            # 名場面在手牌、休息室、牌庫檢索與預覽等直立框 (width <= height) 時一律保持豎向且無多餘黑框注釋；
            # 僅在放置於場上名場面區 (width > height) 時轉為橫置呈現！
            if width > height:
                cx_src = src_img.transpose(Image.Transpose.ROTATE_90) if src_img.height > src_img.width else src_img
                base = cx_src.resize((width, height), Image.Resampling.LANCZOS).copy()
            else:
                cx_src = src_img.transpose(Image.Transpose.ROTATE_270) if src_img.width > src_img.height else src_img
                base = cx_src.resize((width, height), Image.Resampling.LANCZOS).copy()
        else:
            base = src_img.resize((width, height), Image.Resampling.LANCZOS).copy()
        draw = ImageDraw.Draw(base, "RGBA")

        if state == "REST":
            draw.rectangle([0, 0, width, height], fill=(20, 20, 30, 95))
            draw.rectangle([0, height // 2 - 13, width, height // 2 + 13], fill=(255, 183, 3, 220))
            draw.text((width // 2 - 26, height // 2 - 9), "【橫置】", fill="#000000", font=self.font_sub)
        elif state == "REVERSE":
            base = base.rotate(180)
            draw = ImageDraw.Draw(base, "RGBA")
            draw.rectangle([0, 0, width, height], fill=(90, 10, 10, 130))
            draw.rectangle([0, height // 2 - 13, width, height // 2 + 13], fill=(230, 57, 70, 235))
            draw.text((width // 2 - 26, height // 2 - 9), "【倒置】", fill="#ffffff", font=self.font_sub)

        if is_selected:
            draw.rectangle([1, 1, width - 2, height - 2], outline=(255, 209, 102, 255), width=4)

        tk_img = ImageTk.PhotoImage(base)
        self.tk_cache[key] = tk_img
        return tk_img

    def get_hand_dock_card_visual(
        self,
        cid,
        angle_deg: int = 0,
        is_hovered: bool = False,
        is_selected: bool = False,
        is_playable: bool = False,
        eff_level: int = 0,
        cost: int = 0,
    ):
        if hasattr(cid, "skin_id"):
            cid = cid.skin_id
        elif hasattr(cid, "id"):
            cid = cid.id
        if cid not in CARD_DB:
            cid = next(iter(CARD_DB.keys()))
        is_pop = bool(is_hovered)
        q_angle = 0 if is_pop else int(max(-8, min(8, round(angle_deg / 2.0) * 2)))
        key = (cid, q_angle, is_hovered, is_selected, is_playable)
        if key in self.hand_dock_cache:
            return self.hand_dock_cache[key]

        # 放大手牌尺寸，並徹底移除手牌頂部黑框與名場面黑框注釋，名場面於手牌中與其他牌一樣保持豎向！
        width = 148 if is_pop else 122
        height = 206 if is_pop else 170
        src_img = self.pil_cache.get(cid)
        if src_img is None:
            src_img = self._create_single_stylized_card(cid, CARD_DB.get(cid, {}))
        if src_img.width > src_img.height:
            src_img = src_img.transpose(Image.Transpose.ROTATE_270)
        base = src_img.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")

        draw = ImageDraw.Draw(base, "RGBA")
        if is_selected:
            draw.rectangle([0, 0, width - 1, height - 1], outline=(255, 209, 102, 255), width=4)
            draw.rectangle([3, 3, width - 4, height - 4], outline=(255, 255, 255, 210), width=1)
        elif is_hovered:
            draw.rectangle([0, 0, width - 1, height - 1], outline=(76, 201, 240, 255), width=4)
            draw.rectangle([3, 3, width - 4, height - 4], outline=(255, 255, 255, 210), width=1)
        elif is_playable:
            draw.rectangle([0, 0, width - 1, height - 1], outline=(6, 214, 160, 245), width=3)
        else:
            draw.rectangle([0, 0, width - 1, height - 1], outline=(68, 78, 108, 235), width=2)

        if q_angle != 0:
            base = base.rotate(q_angle, resample=Image.Resampling.BICUBIC, expand=True)

        tk_img = ImageTk.PhotoImage(base)
        self.hand_dock_cache[key] = tk_img
        return tk_img

    def get_empty_slot_visual(
        self, label_text, width=84, height=118, is_selected=False, bg_color="#1a212d"
    ):
        key = (label_text, width, height, is_selected, bg_color)
        if key in self.empty_slot_cache:
            return self.empty_slot_cache[key]
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        outline_col = "#ffd166" if is_selected else "#3b4963"
        draw.rectangle([2, 2, width - 3, height - 3], outline=outline_col, width=2)
        lines = label_text.split("\n")
        y_start = height // 2 - (len(lines) * 10)
        for line in lines:
            draw.text((10, y_start), line, fill="#8d99ae", font=self.font_sub)
            y_start += 20
        tk_img = ImageTk.PhotoImage(img)
        self.empty_slot_cache[key] = tk_img
        return tk_img

    def set_sleeve_config(self, sleeve_style: str, custom_path: str = ""):
        self.active_sleeve_style = sleeve_style or "WS_DEFAULT"
        self.custom_sleeve_path = custom_path or ""
        self.deck_stack_cache.clear()
        self.stock_stack_cache.clear()
        self.ai_fan_cache.clear()

    def _build_default_ws_sleeve_pil(self) -> Image.Image:
        """高精細復刻官方 Weiß Schwarz 經典黑銀格紋星芒卡背 (當本地尚未下載完成時的備援圖)"""
        w, h = 240, 336
        img = Image.new("RGB", (w, h), "#121318")
        draw = ImageDraw.Draw(img)
        # 黑銀交錯格紋背景
        cell = 16
        for y in range(12, h - 12, cell):
            for x in range(12, w - 12, cell):
                c_col = "#1c1e26" if ((x // cell + y // cell) % 2 == 0) else "#272a36"
                draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=c_col)
        # 外銀框與四角古典雕花框線
        draw.rectangle([2, 2, w - 3, h - 3], outline="#b8c0cc", width=3)
        draw.rectangle([9, 9, w - 10, h - 10], outline="#6c7585", width=2)
        draw.rectangle([14, 14, w - 15, h - 15], outline="#d8e2dc", width=1)
        # 中央雙環黑白金屬徽章
        cx, cy = w // 2, h // 2
        draw.ellipse([cx - 76, cy - 96, cx + 76, cy + 96], fill="#0d0e12", outline="#adb5bd", width=3)
        draw.ellipse([cx - 66, cy - 84, cx + 66, cy + 84], fill="#1a1d26", outline="#e5e5e5", width=2)
        # 中央十字星芒
        draw.polygon([(cx, cy - 64), (cx + 12, cy - 12), (cx + 58, cy), (cx + 12, cy + 12), (cx, cy + 64), (cx - 12, cy + 12), (cx - 58, cy), (cx - 12, cy - 12)], fill="#8d99ae", outline="#ffffff")
        draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill="#11131a", outline="#ffd166", width=2)
        draw.text((cx - 24, cy - 18), "Weiß", fill="#ffffff", font=self.font_title)
        draw.text((cx - 32, cy + 2), "Schwarz", fill="#adb5bd", font=self.font_sub)
        return img

    def _build_amiami_fallback_pil(self) -> Image.Image:
        """特典角色卡套備援圖 (優先等待背景下載真實 CARD-00021593.jpg)"""
        base_card = self.pil_cache.get("BFR/S78-082SP") or self.pil_cache.get("BTR/W107-069") or next(iter(self.pil_cache.values()), None)
        w, h = 240, 336
        if base_card:
            img = base_card.resize((w, h), Image.Resampling.LANCZOS).copy()
        else:
            img = self._build_default_ws_sleeve_pil()
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w - 1, h - 1], outline="#ffd166", width=6)
        draw.rectangle([6, 6, w - 7, h - 7], outline="#ffffff", width=2)
        return img

    def get_sleeve_pil(self, sleeve_style: str = None, custom_path: str = None) -> Image.Image:
        style = sleeve_style if sleeve_style is not None else getattr(self, "active_sleeve_style", "WS_DEFAULT")
        c_path = custom_path if custom_path is not None else (getattr(self, "custom_sleeve_path", "") if sleeve_style is None else "")
        if style == "LAN_PEER_CUSTOM" and "LAN_PEER_CUSTOM" in self.sleeve_pil_cache:
            return self.sleeve_pil_cache["LAN_PEER_CUSTOM"]
        if style == "CUSTOM" and c_path and os.path.exists(c_path):
            ckey = f"CUSTOM::{c_path}"
            if ckey in self.sleeve_pil_cache:
                return self.sleeve_pil_cache[ckey]
            try:
                im = Image.open(c_path).convert("RGB")
                self.sleeve_pil_cache[ckey] = im
                return im
            except Exception:
                pass
        if style == "AMIAMI_21593":
            p = os.path.join(self.local_webp_dir, "sleeve_amiami_21593.webp")
            if os.path.exists(p) and os.path.getsize(p) > 500:
                if "AMIAMI_21593" not in self.sleeve_pil_cache:
                    try:
                        self.sleeve_pil_cache["AMIAMI_21593"] = Image.open(p).convert("RGB")
                    except Exception:
                        pass
                if "AMIAMI_21593" in self.sleeve_pil_cache:
                    return self.sleeve_pil_cache["AMIAMI_21593"]
            return self._build_amiami_fallback_pil()

        p_def = os.path.join(self.local_webp_dir, "sleeve_ws_default.webp")
        if os.path.exists(p_def) and os.path.getsize(p_def) > 500:
            if "WS_DEFAULT" not in self.sleeve_pil_cache:
                try:
                    self.sleeve_pil_cache["WS_DEFAULT"] = Image.open(p_def).convert("RGB")
                except Exception:
                    pass
            if "WS_DEFAULT" in self.sleeve_pil_cache:
                return self.sleeve_pil_cache["WS_DEFAULT"]
        if "WS_FALLBACK" not in self.sleeve_pil_cache:
            self.sleeve_pil_cache["WS_FALLBACK"] = self._build_default_ws_sleeve_pil()
        return self.sleeve_pil_cache["WS_FALLBACK"]

    def get_sleeve_preview_visual(self, sleeve_style: str, custom_path: str = "", width=64, height=90):
        pil_im = self.get_sleeve_pil(sleeve_style, custom_path).resize((width, height), Image.Resampling.LANCZOS).copy()
        d = ImageDraw.Draw(pil_im)
        d.rectangle([0, 0, width - 1, height - 1], outline="#ffd166", width=2)
        return ImageTk.PhotoImage(pil_im)

    def get_ai_hand_sleeve_visual(
        self, width=52, height=74, angle_deg: int = 0, sleeve_style: str = None, custom_path: str = None
    ):
        style = sleeve_style if sleeve_style is not None else "WS_DEFAULT"
        c_path = custom_path if custom_path is not None else ""
        q_ang = int(max(-12, min(12, round(angle_deg / 2.0) * 2)))
        key = (style, c_path, width, height, q_ang)
        if key in self.ai_fan_cache:
            return self.ai_fan_cache[key]
        # 對手手牌朝向對面（旋轉 180 度）並加上扇形角度
        s_pil = self.get_sleeve_pil(style, c_path).resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        s_pil = s_pil.rotate(180 + q_ang, resample=Image.Resampling.BICUBIC, expand=True)
        tk_im = ImageTk.PhotoImage(s_pil)
        self.ai_fan_cache[key] = tk_im
        return tk_im

    def get_deck_stack_visual(
        self,
        deck_count: int,
        label_text: str,
        width=76,
        height=106,
        bg_color="#1a2838",
        sleeve_style: str = None,
        custom_path: str = None,
    ):
        style = sleeve_style if sleeve_style is not None else getattr(self, "active_sleeve_style", "WS_DEFAULT")
        c_path = custom_path if custom_path is not None else (getattr(self, "custom_sleeve_path", "") if sleeve_style is None else "")
        key = (deck_count, label_text, width, height, bg_color, style, c_path)
        if key in self.deck_stack_cache:
            return self.deck_stack_cache[key]

        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img, "RGBA")

        if deck_count <= 0:
            draw.rectangle([2, 2, width - 3, height - 3], outline="#5c3b47", width=2)
            draw.text((8, height // 2 - 10), "牌庫 0 張", fill="#ff6b6b", font=self.font_sub)
        elif label_text == "王牌覆蓋卡":
            # 單張覆蓋卡（如先後手翻王牌）：直接呈現完整精緻卡套
            sleeve_im = self.get_sleeve_pil(style, c_path).resize((width - 4, height - 4), Image.Resampling.LANCZOS)
            img.paste(sleeve_im, (2, 2))
            draw.rectangle([1, 1, width - 2, height - 2], outline="#ffd166", width=2)
        else:
            layers = max(1, min(12, (deck_count + 3) // 4))
            card_w = width - 16
            card_h = height - 18
            base_x = 3
            base_y = height - card_h - 3

            for lyr in range(layers):
                ox = base_x + lyr
                oy = base_y - lyr
                edge_col = "#d8e2dc" if lyr % 2 == 0 else "#8d99ae"
                fill_col = "#16243b" if lyr < layers - 1 else "#1d3557"
                draw.rectangle([ox, oy, ox + card_w, oy + card_h], fill=fill_col, outline=edge_col, width=1)

            tx = base_x + layers
            ty = base_y - layers
            sleeve_top = self.get_sleeve_pil(style, c_path).resize((card_w, card_h), Image.Resampling.LANCZOS)
            img.paste(sleeve_top, (tx, ty))
            draw.rectangle([tx, ty, tx + card_w - 1, ty + card_h - 1], outline="#ffd166", width=2)
            # 底部半透明剩餘張數角標
            draw.rectangle([tx + 2, ty + card_h - 20, tx + card_w - 2, ty + card_h - 2], fill=(12, 16, 26, 215))
            draw.text((tx + 6, ty + card_h - 19), f"剩 {deck_count} 張", fill="#ffffff", font=self.font_sub)

        tk_img = ImageTk.PhotoImage(img)
        self.deck_stack_cache[key] = tk_img
        return tk_img

    def get_stock_stack_visual(
        self,
        stock_count: int,
        width=82,
        height=114,
        bg_color="#1a2838",
        sleeve_style: str = None,
        custom_path: str = None,
    ):
        """繪製能量區（Stock）橫置疊放的卡背蓋牌堆：忠實還原實體 WS 將蓋牌橫置疊放作為能量的視覺"""
        style = sleeve_style if sleeve_style is not None else getattr(self, "active_sleeve_style", "WS_DEFAULT")
        c_path = custom_path if custom_path is not None else (getattr(self, "custom_sleeve_path", "") if sleeve_style is None else "")
        key = (stock_count, width, height, bg_color, style, c_path)
        if key in self.stock_stack_cache:
            return self.stock_stack_cache[key]

        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img, "RGBA")

        if stock_count <= 0:
            draw.rectangle([2, 2, width - 3, height - 3], outline="#3b4963", width=2)
            draw.text((12, height // 2 - 18), "能量區", fill="#8d99ae", font=self.font_sub)
            draw.text((14, height // 2 + 2), "0 張", fill="#6c757d", font=self.font_sub)
        else:
            # 將卡套旋轉 90 度成橫置蓋牌，由下往上層層疊放
            horiz_sleeve = self.get_sleeve_pil(style, c_path).transpose(Image.Transpose.ROTATE_90)
            cw = width - 10
            ch = max(36, int(cw * 0.71))
            horiz_sleeve = horiz_sleeve.resize((cw, ch), Image.Resampling.LANCZOS)

            vis_layers = min(stock_count, 7)
            avail_span = max(8, height - ch - 26)
            step_y = max(4, min(11, avail_span // max(1, vis_layers)))

            for lyr in range(vis_layers):
                ox = 4 + (lyr % 2) * 2
                oy = height - ch - 4 - lyr * step_y
                img.paste(horiz_sleeve, (ox, oy))
                border_c = "#ffd166" if lyr == vis_layers - 1 else "#adb5bd"
                draw.rectangle([ox, oy, ox + cw - 1, oy + ch - 1], outline=border_c, width=2 if lyr == vis_layers - 1 else 1)

            # 頂部醒目能量張數膠囊（純中文與數字，避免字型缺字方框）
            draw.rectangle([3, 3, width - 4, 23], fill=(14, 20, 34, 235), outline="#ffd166", width=1)
            draw.text((10, 4), f"能量: {stock_count} 張", fill="#ffd166", font=self.font_sub)

        tk_img = ImageTk.PhotoImage(img)
        self.stock_stack_cache[key] = tk_img
        return tk_img

    def get_clock_spread_visual(
        self,
        clock_cards: list,
        empty_title: str = "時鐘區",
        width: int = 216,
        height: int = 104,
        bg_color: str = "#1a2838",
    ):
        """將時鐘區 (Clock) 卡片像實體 WS 對戰一樣由左至右一字排開，方便一眼確認所有傷害卡與顏色"""
        if not hasattr(self, "clock_spread_cache"):
            self.clock_spread_cache = {}
        cids_tuple = tuple(getattr(c, "skin_id", c.id) for c in clock_cards)
        key = (cids_tuple, empty_title, width, height, bg_color)
        if key in self.clock_spread_cache:
            return self.clock_spread_cache[key]

        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img, "RGBA")

        if not clock_cards:
            draw.rectangle([2, 2, width - 3, height - 3], outline="#3b4963", width=2)
            # 繪製 6 格淡淡的時鐘卡槽底框，預示一字排開位置
            for s_i in range(6):
                sx = 8 + s_i * 33
                draw.rectangle([sx, 14, sx + 28, height - 14], outline="#28344a", width=1)
            draw.rectangle([width // 2 - 58, height // 2 - 14, width // 2 + 58, height // 2 + 14], fill=(16, 22, 34, 215), outline="#3b4963", width=1)
            draw.text((width // 2 - 48, height // 2 - 9), f"{empty_title} (0/7)", fill="#8d99ae", font=self.font_sub)
        else:
            draw.rectangle([1, 1, width - 2, height - 2], outline="#4cc9f0", width=2)
            n = len(clock_cards)
            cw, ch = 64, 90
            oy = (height - ch) // 2
            avail_w = max(1, width - cw - 12)
            step_x = 0 if n <= 1 else min(44, avail_w // max(1, n - 1))
            col_map = {"紅": "#ff6b6b", "藍": "#4cc9f0", "黃": "#ffd166", "綠": "#06d6a0"}

            for idx, c in enumerate(clock_cards):
                cid = getattr(c, "skin_id", c.id)
                src_im = self.pil_cache.get(cid)
                if src_im is None:
                    src_im = next(iter(self.pil_cache.values()))
                if src_im.width > src_im.height:
                    src_im = src_im.transpose(Image.Transpose.ROTATE_270)
                thumb = src_im.resize((cw, ch), Image.Resampling.LANCZOS)
                ox = 6 + idx * step_x
                img.paste(thumb, (ox, oy))
                b_col = col_map.get(getattr(c, "color", ""), "#ffd166")
                draw.rectangle([ox, oy, ox + cw - 1, oy + ch - 1], outline=b_col, width=2)
                # 左上角編號與色標小方塊
                draw.rectangle([ox + 1, oy + 1, ox + 17, oy + 17], fill=(12, 16, 26, 225), outline=b_col, width=1)
                draw.text((ox + 5, oy + 1), str(idx + 1), fill=b_col, font=self.font_sub)

        tk_img = ImageTk.PhotoImage(img)
        self.clock_spread_cache[key] = tk_img
        return tk_img

    def get_level_spread_visual(
        self,
        level_cards: list,
        empty_title: str = "等級區",
        width: int = 104,
        height: int = 104,
        bg_color: str = "#1a2838",
    ):
        """將等級區 (0~3 張) 卡片微幅錯開排列，一眼看清目前等級區所有發色"""
        if not hasattr(self, "level_spread_cache"):
            self.level_spread_cache = {}
        cids_tuple = tuple(getattr(c, "skin_id", c.id) for c in level_cards)
        key = (cids_tuple, empty_title, width, height, bg_color)
        if key in self.level_spread_cache:
            return self.level_spread_cache[key]

        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img, "RGBA")

        if not level_cards:
            draw.rectangle([2, 2, width - 3, height - 3], outline="#3b4963", width=2)
            draw.text((16, height // 2 - 18), empty_title, fill="#8d99ae", font=self.font_sub)
            draw.text((22, height // 2 + 4), "Lv.0", fill="#6c757d", font=self.font_sub)
        else:
            draw.rectangle([1, 1, width - 2, height - 2], outline="#06d6a0", width=2)
            n = len(level_cards)
            cw, ch = 62, 88
            oy = (height - ch) // 2
            step_x = 0 if n <= 1 else min(17, (width - cw - 10) // max(1, n - 1))
            col_map = {"紅": "#ff6b6b", "藍": "#4cc9f0", "黃": "#ffd166", "綠": "#06d6a0"}
            for idx, c in enumerate(level_cards):
                cid = getattr(c, "skin_id", c.id)
                src_im = self.pil_cache.get(cid)
                if src_im is None:
                    src_im = next(iter(self.pil_cache.values()))
                if src_im.width > src_im.height:
                    src_im = src_im.transpose(Image.Transpose.ROTATE_270)
                thumb = src_im.resize((cw, ch), Image.Resampling.LANCZOS)
                ox = 5 + idx * step_x
                img.paste(thumb, (ox, oy))
                b_col = col_map.get(getattr(c, "color", ""), "#ffd166")
                draw.rectangle([ox, oy, ox + cw - 1, oy + ch - 1], outline=b_col, width=2)

        tk_img = ImageTk.PhotoImage(img)
        self.level_spread_cache[key] = tk_img
        return tk_img

    AVATAR_PRESET_DEFAULTS = {
        "MAPLE": ("BFR/S78-073", "梅普露", "#e63946", 0.50, 0.24, 1.85),
        "SALLY": ("BFR/S78-083", "莎莉", "#4cc9f0", 0.48, 0.25, 1.85),
        "MII": ("BFR/S78-060", "蜜伊", "#ff6b6b", 0.50, 0.24, 1.85),
        "MAHIRU": ("GA02/S131-003", "小真晝", "#ffd166", 0.52, 0.24, 1.90),
        "ELAINA": ("GA17/S131-010", "伊蕾娜", "#a8dadc", 0.50, 0.24, 1.90),
        "RYU": ("GA10/S131-012", "琉", "#06d6a0", 0.50, 0.23, 1.90),
        "KITA": ("BTR/W107-075", "喜多郁代", "#ff758f", 0.50, 0.23, 1.95),
        "BOCCHI": ("BTR/W107-T14", "後藤一里", "#f4a261", 0.50, 0.24, 1.90),
        "NIJIKA": ("BTR/W107-T02", "伊地知虹夏", "#ffd166", 0.50, 0.24, 1.90),
    }

    def get_avatar_visual(
        self,
        avatar_id: str,
        size: int = 64,
        border_color: str = "#ffd166",
        custom_path: str = "",
        is_active_turn: bool = False,
        crop_cfg: dict = None,
        preset_crops: dict = None,
    ):
        """產生純淨滿版《大師決鬥》風格圓環金屬角色頭像（移除底部遮臉文字銘牌，支援 9 大預設頭像各自獨立裁切與任意卡圖滾輪縮放裁切）"""
        effective_crop = crop_cfg
        if effective_crop is None and isinstance(preset_crops, dict) and avatar_id in preset_crops:
            effective_crop = preset_crops[avatar_id]

        crop_tuple = None
        if isinstance(effective_crop, dict) and effective_crop.get("cid"):
            crop_tuple = (
                str(effective_crop.get("cid", "")),
                round(float(effective_crop.get("cx", 0.5)), 3),
                round(float(effective_crop.get("cy", 0.24)), 3),
                round(float(effective_crop.get("zoom", 1.85)), 3),
            )
        key = (avatar_id, size, border_color, custom_path, is_active_turn, crop_tuple)
        if key in self.avatar_cache:
            return self.avatar_cache[key]

        src_img = None
        ring_col = border_color
        cx_r, cy_r, zoom_f = 0.50, 0.24, 1.85

        if crop_tuple:
            c_cid, cx_r, cy_r, zoom_f = crop_tuple
            src_img = self.pil_cache.get(c_cid)
        elif avatar_id == "CUSTOM" and custom_path and os.path.exists(custom_path):
            try:
                src_img = Image.open(custom_path).convert("RGB")
                cx_r, cy_r, zoom_f = 0.50, 0.42, 1.25
            except Exception:
                src_img = None

        if src_img is None:
            cid, _, def_col, d_cx, d_cy, d_zm = self.AVATAR_PRESET_DEFAULTS.get(
                avatar_id, ("BFR/S78-073", "梅普露", "#ffd166", 0.50, 0.24, 1.85)
            )
            if not crop_tuple:
                cx_r, cy_r, zoom_f = d_cx, d_cy, d_zm
            if not border_color:
                ring_col = def_col
            src_img = self.pil_cache.get(cid)

        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        if src_img is not None:
            w, h = src_img.size
            base_dim = min(w, h)
            crop_s = max(18, min(base_dim, int(base_dim / max(0.8, zoom_f))))
            cx = int(w * cx_r)
            cy = int(h * cy_r)
            x0 = max(0, min(w - crop_s, cx - crop_s // 2))
            y0 = max(0, min(h - crop_s, cy - crop_s // 2))
            cropped = src_img.crop((x0, y0, x0 + crop_s, y0 + crop_s)).resize(
                (size, size), Image.Resampling.LANCZOS
            )
        else:
            cropped = Image.new("RGB", (size, size), color="#1d3557")

        # 建立圓形遮罩與雙層《Master Duel》風格金色/霓虹光環（不繪製底部文字條，完整呈現頭貼全貌！）
        mask = Image.new("L", (size, size), 0)
        m_draw = ImageDraw.Draw(mask)
        pad = 3
        m_draw.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill=255)
        canvas.paste(cropped.convert("RGBA"), (0, 0), mask)

        draw = ImageDraw.Draw(canvas)
        outer_col = "#06d6a0" if is_active_turn else ring_col
        draw.ellipse([1, 1, size - 2, size - 2], outline=outer_col, width=3)
        draw.ellipse([4, 4, size - 5, size - 5], outline="#141824", width=1)

        out_rgb = Image.new("RGB", (size, size), color="#141824")
        out_rgb.paste(canvas, (0, 0), canvas)
        tk_img = ImageTk.PhotoImage(out_rgb)
        self.avatar_cache[key] = tk_img
        return tk_img

    def get_wallpaper_visual(
        self,
        theme_id: str,
        custom_bg_path: str,
        dim_percent: int,
        width: int = 1600,
        height: int = 950,
        floating_cids: list = None,
    ):
        """產生主選單與設定頁面的《大師決鬥》風格背景圖（自動從玩家目前使用的出戰卡組隨機抽取 6 張卡片懸浮於背景）"""
        dim_clamped = max(15, min(92, int(dim_percent)))
        cids_tuple = tuple(floating_cids[:6]) if floating_cids else ()
        key = (theme_id, custom_bg_path, dim_clamped, width, height, cids_tuple)
        if key in self.bg_cache:
            return self.bg_cache[key]

        theme_colors = {
            "OCEAN": ("#0c1424", "#1b2e4b", "#ffd166"),
            "MAPLE_CRIMSON": ("#1f0b12", "#4a1222", "#ff6b6b"),
            "STARLIGHT_GOLD": ("#191528", "#342a52", "#ffd166"),
            "BOCCHI_NEON": ("#1c0f24", "#3d1a47", "#ff758f"),
        }
        base_col, mid_col, accent_col = theme_colors.get(
            theme_id, ("#0c1424", "#1b2e4b", "#ffd166")
        )

        bg_img = None
        if custom_bg_path and os.path.exists(custom_bg_path):
            try:
                raw_bg = Image.open(custom_bg_path).convert("RGB")
                # 等比例填滿 (Cover)
                rw, rh = raw_bg.size
                scale = max(width / max(1, rw), height / max(1, rh))
                nw, nh = int(rw * scale), int(rh * scale)
                resized = raw_bg.resize((nw, nh), Image.Resampling.LANCZOS)
                x0 = max(0, (nw - width) // 2)
                y0 = max(0, (nh - height) // 2)
                bg_img = resized.crop((x0, y0, x0 + width, y0 + height))
            except Exception:
                bg_img = None

        if bg_img is None:
            # 自動合成《大師決鬥》風格的三大系列王牌卡斜向展示牆
            bg_img = Image.new("RGB", (width, height), color=base_col)
            b_draw = ImageDraw.Draw(bg_img)
            # 繪製科技感斜紋格線
            for gx in range(-height, width + height, 90):
                b_draw.line([(gx, 0), (gx + height // 2, height)], fill=mid_col, width=2)
            hero_cids = list(cids_tuple) if cids_tuple else [
                "BFR/S78-063",
                "BFR/S78-089",
                "GA02/S131-003",
                "GA17/S131-010",
                "BTR/W107-075",
                "BTR/W107-076",
            ]
            positions = [
                (45, 55, -8),
                (235, 420, 6),
                (55, 580, -5),
                (width - 285, 50, 8),
                (width - 450, 380, -6),
                (width - 260, 560, 5),
            ]
            for idx_p, (px, py, ang) in enumerate(positions):
                cid = hero_cids[idx_p % len(hero_cids)]
                c_pil = self.pil_cache.get(cid)
                if c_pil:
                    card_thumb = c_pil.resize((210, 294), Image.Resampling.LANCZOS).convert("RGBA")
                    bordered = Image.new("RGBA", (218, 302), (255, 209, 102, 180))
                    bordered.paste(card_thumb, (4, 4))
                    rot = bordered.rotate(ang, expand=True, resample=Image.Resampling.BICUBIC)
                    bg_img.paste(rot.convert("RGB"), (px, py), rot)

        # 套用暗化遮罩 (dim_clamped %)，確保前景 UI 與文字絕對清晰
        overlay = Image.new("RGB", (width, height), color=base_col)
        alpha = dim_clamped / 100.0
        blended = Image.blend(bg_img, overlay, alpha)

        # 上下邊緣《Master Duel》風格金色飾條
        f_draw = ImageDraw.Draw(blended)
        f_draw.rectangle([0, 0, width, 6], fill=accent_col)
        f_draw.rectangle([0, height - 6, width, height], fill=accent_col)

        tk_img = ImageTk.PhotoImage(blended)
        self.bg_cache[key] = tk_img
        return tk_img


# ==========================================
# 雙人區網連線大廳介面 (LANLobbyFrame)
# ==========================================
class LANLobbyFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#111218")
        self.app = app
        self.net_node = None
        self.public_ip = "偵測中..."
        self.setup_ui()
        WSNetNode.get_public_ip_async(self._on_public_ip_fetched)

    def _on_public_ip_fetched(self, pub_ip):
        def _upd():
            if not self.winfo_exists():
                return
            self.public_ip = pub_ip if pub_ip else "無法自動取得（可能處於內網 NAT）"
            local_ip = WSNetNode.get_local_ip()
            self.lbl_ip_info.config(
                text=f"🏠 區網 IP：{local_ip} ｜ 🌐 外網公網 IP：{self.public_ip} ｜ 預設 Port：15780"
            )
        self.app.root.after(0, _upd)

    def setup_ui(self):
        box = tk.Frame(self, bg="#1b1c24", bd=3, relief=tk.RIDGE, padx=40, pady=26)
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            box,
            text="🌐 雙人對戰連線大廳（支援區網、UPnP 外網直連與隧道網址）",
            bg="#1b1c24",
            fg="#ffd166",
            font=("Microsoft JhengHei", 19, "bold"),
        ).pack(pady=(0, 10))

        local_ip = WSNetNode.get_local_ip()
        self.lbl_ip_info = tk.Label(
            box,
            text=f"🏠 區網 IP：{local_ip} ｜ 🌐 外網公網 IP：{self.public_ip} ｜ 預設 Port：15780",
            bg="#242632",
            fg="#06d6a0",
            font=("Microsoft JhengHei", 12, "bold"),
            padx=18,
            pady=8,
            relief=tk.SOLID,
            bd=1,
        )
        self.lbl_ip_info.pack(fill=tk.X, pady=6)

        # 玩家對戰名稱輸入列
        name_frame = tk.Frame(box, bg="#242632", padx=14, pady=8, relief=tk.SOLID, bd=1)
        name_frame.pack(fill=tk.X, pady=6)

        tk.Label(
            name_frame,
            text="👤 你的對戰名稱：",
            bg="#242632",
            fg="#ffd166",
            font=("Microsoft JhengHei", 12, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.ent_player_name = tk.Entry(
            name_frame,
            bg="#14151d",
            fg="#ffffff",
            insertbackground="white",
            font=("Microsoft JhengHei", 12, "bold"),
            width=18,
        )
        self.ent_player_name.insert(0, getattr(self.app, "player_battle_name", "玩家1"))
        self.ent_player_name.pack(side=tk.LEFT, padx=6)

        tk.Label(
            name_frame,
            text="（對戰時將顯示此名稱，而非卡組名稱）",
            bg="#242632",
            fg="#8ecae6",
            font=("Microsoft JhengHei", 10),
        ).pack(side=tk.LEFT, padx=6)

        # 顯示目前「我的卡組」資訊（固定使用「設定 我的卡組」所設定之牌組）
        deck_pick_frame = tk.Frame(box, bg="#242632", padx=14, pady=8, relief=tk.SOLID, bd=1)
        deck_pick_frame.pack(fill=tk.X, pady=6)

        tk.Label(
            deck_pick_frame,
            text=f"🎴 我方出戰卡組：我的卡組（{self.app.get_deck_display_name(self.app.active_series)}）",
            bg="#242632",
            fg="#06d6a0",
            font=("Microsoft JhengHei", 12, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 8))

        # 連線目標 IP / 隧道網址設定
        form = tk.Frame(box, bg="#1b1c24")
        form.pack(pady=10)

        tk.Label(
            form,
            text="目標房主位址（IP 或 隧道網址:Port）：",
            bg="#1b1c24",
            fg="#ffffff",
            font=("Microsoft JhengHei", 12, "bold"),
        ).grid(row=0, column=0, padx=6, pady=6, sticky="e")

        self.ent_ip = tk.Entry(
            form,
            bg="#14151d",
            fg="#ffffff",
            insertbackground="white",
            font=("Consolas", 13),
            width=26,
        )
        self.ent_ip.insert(0, local_ip)
        self.ent_ip.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(
            form,
            text="Port：",
            bg="#1b1c24",
            fg="#ffffff",
            font=("Microsoft JhengHei", 12, "bold"),
        ).grid(row=0, column=2, padx=6, pady=6, sticky="e")

        self.ent_port = tk.Entry(
            form,
            bg="#14151d",
            fg="#ffffff",
            insertbackground="white",
            font=("Consolas", 13),
            width=8,
        )
        self.ent_port.insert(0, "15780")
        self.ent_port.grid(row=0, column=3, padx=6, pady=6)

        btn_row = tk.Frame(box, bg="#1b1c24")
        btn_row.pack(pady=10)

        self.btn_host = tk.Button(
            btn_row,
            text="🏠 建立房間 (Host 自動嘗試 UPnP 外網開埠)",
            bg="#06d6a0",
            fg="#000000",
            font=("Microsoft JhengHei", 12, "bold"),
            padx=16,
            pady=8,
            command=self.on_start_host,
        )
        self.btn_host.pack(side=tk.LEFT, padx=10)

        self.btn_join = tk.Button(
            btn_row,
            text="🔗 加入房間 (Client 連線)",
            bg="#118ab2",
            fg="#ffffff",
            font=("Microsoft JhengHei", 12, "bold"),
            padx=18,
            pady=8,
            command=self.on_connect_host,
        )
        self.btn_join.pack(side=tk.LEFT, padx=10)

        self.lbl_status = tk.Label(
            box,
            text="尚未啟動連線。請先輸入你的對戰名稱，再選擇建立房間或輸入對方位址加入。",
            bg="#1b1c24",
            fg="#8ecae6",
            font=("Microsoft JhengHei", 11, "bold"),
            wraplength=680,
        )
        self.lbl_status.pack(pady=8)

        guide_box = tk.Frame(box, bg="#141620", padx=14, pady=8, relief=tk.SOLID, bd=1)
        guide_box.pack(fill=tk.X, pady=6)
        tk.Label(
            guide_box,
            text=(
                "💡 免 VPN 跨外網連線方式：\n"
                "1. 【UPnP / 路由器直連】點擊「建立房間」時程式會自動向路由器申請 UPnP 開通 Port 15780，朋友直接輸入上方「外網公網 IP」即可連線。\n"
                "2. 【免設定路由器隧道（推薦穿透內網）】房主下載免費單檔工具 playit.gg 或執行 ngrok tcp 15780，將產生的網址（如 xxx.ply.gg:12345）直接貼入上方目標房主位址即可跨網連線！"
            ),
            bg="#141620",
            fg="#adb5bd",
            font=("Microsoft JhengHei", 10),
            justify=tk.LEFT,
        ).pack(anchor="w")

        tk.Button(
            box,
            text="⬅ 返回主選單",
            bg="#3a3a48",
            fg="white",
            font=("Microsoft JhengHei", 12, "bold"),
            padx=20,
            pady=6,
            command=self.on_back,
        ).pack(pady=(8, 0))

    def _save_battle_name(self):
        typed = self.ent_player_name.get().strip()
        final_name = typed if typed else "玩家1"
        self.app.player_battle_name = final_name
        self.app.settings["player_name"] = final_name
        self.app.save_user_settings(self.app.settings)

    def _on_net_msg(self, msg: dict):
        if msg.get("type") not in ("SYS_CONNECTED", "SYS_ERROR", "SYS_DISCONNECTED"):
            if not hasattr(self.net_node, "_early_msg_queue"):
                self.net_node._early_msg_queue = []
            self.net_node._early_msg_queue.append(msg)
            return
        self.app.root.after(0, lambda: self._handle_net_msg_ui(msg))

    def _handle_net_msg_ui(self, msg: dict):
        if not self.winfo_exists():
            return
        mtype = msg.get("type")
        if mtype == "SYS_CONNECTED":
            self._save_battle_name()
            peer = msg.get("peer", "")
            self.lbl_status.config(
                text=f"✔ 已成功連線至 {peer}！正在進入對戰桌面...", fg="#06d6a0"
            )
            self.app.root.after(120, lambda: self.app.start_lan_game(self.net_node))
        elif mtype == "SYS_ERROR":
            err = msg.get("error", "")
            self.lbl_status.config(text=f"❌ 連線發生錯誤：{err}", fg="#ff6b6b")
            self.btn_host.config(state=tk.NORMAL)
            self.btn_join.config(state=tk.NORMAL)

    def on_start_host(self):
        self._save_battle_name()
        if self.net_node:
            self.net_node.close()
        raw_port = self.ent_port.get().strip() or "15780"
        port = int(raw_port) if raw_port.isdigit() else 15780
        self.net_node = WSNetNode(self._on_net_msg)
        self.net_node.start_host(port=port)
        self.btn_host.config(state=tk.DISABLED)
        self.btn_join.config(state=tk.DISABLED)
        self.lbl_status.config(
            text=f"⏳ 房間已開啟 (Port {port})，正在嘗試 UPnP 外網映射並等待對手連線...", fg="#ffd166"
        )

        def _upnp_cb(ok, detail):
            def _u():
                if not self.winfo_exists() or (self.net_node and self.net_node.connected):
                    return
                if ok:
                    self.lbl_status.config(
                        text=f"⏳ 房間已開啟！✔ {detail}，外網對手可直接輸入公網 IP ({self.public_ip}) 與 Port {port} 連線！",
                        fg="#06d6a0",
                    )
                else:
                    self.lbl_status.config(
                        text=f"⏳ 房間已開啟 (Port {port})，等待連線中（{detail}；若跨外網可使用 playit.gg / ngrok 隧道或路由器轉發）。",
                        fg="#ffd166",
                    )
            self.app.root.after(0, _u)

        WSNetNode.try_upnp_forward_async(port, _upnp_cb)

    def on_connect_host(self):
        self._save_battle_name()
        if self.net_node:
            self.net_node.close()
        raw_ip = self.ent_ip.get().strip()
        raw_port = self.ent_port.get().strip() or "15780"
        default_port = int(raw_port) if raw_port.isdigit() else 15780
        host, port = WSNetNode.parse_host_port(raw_ip, default_port=default_port)
        self.net_node = WSNetNode(self._on_net_msg)
        self.net_node.connect_to_host(host, port=port)
        self.btn_host.config(state=tk.DISABLED)
        self.btn_join.config(state=tk.DISABLED)
        self.lbl_status.config(text=f"⏳ 正在連線至 {host}:{port} ...", fg="#ffd166")

    def _select_lan_series(self, scode: str):
        self.app.set_active_series(scode)
        for k, b in self.lan_series_btns.items():
            b.config(
                bg="#06d6a0" if k == scode else "#343a40",
                fg="#000000" if k == scode else "#ffffff",
            )
        slabel = self.app.get_deck_display_name(scode)
        self.lbl_status.config(text=f"✔ 已選擇【{slabel}】作為連線出戰卡組！", fg="#06d6a0")

    def on_back(self):
        self._save_battle_name()
        if self.net_node:
            self.net_node.close()
        self.app.show_main_menu()


# ==========================================
# 設定我的卡組介面 (DeckBuilderFrame：支援預設三套小選單、任意編輯與查卡名搜索)
# ==========================================
DEFAULT_SERIES_ACE_CARDS = {
    "BFR/S78": "BFR/S78-063",
    "GA/S131": "GA02/S131-003",
    "BTR/W107": "BTR/W107-076",
}

PRESET_DECK_OPTIONS = [
    ("預設套牌 1：防盾系列 (BFR/S78)", "BFR/S78"),
    ("預設套牌 2：GA文庫 8箭地旅 (GA/S131)", "GA/S131"),
    ("預設套牌 3：孤獨搖滾！ (BTR/W107)", "BTR/W107"),
    ("我的自訂卡組 (CUSTOM)", "CUSTOM"),
]


class DeckBuilderFrame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#111218")
        self.app = app
        self.img_mgr = app.img_mgr
        load_all_card_sets()
        # 若有任何預設套牌已遺失對應設定，先同步內建三套
        self.selected_series = (
            app.active_series if app.active_series in SERIES_DB else "ALL"
        )
        self.rarity_filter = "ALL"  # "ALL", "NORMAL", "HIGH"
        self.search_keyword = ""
        self.current_page = 0
        self.page_size = 24
        self.working_recipe = {}
        self.count_labels = {}
        self.series_buttons = {}
        self.rarity_buttons = {}
        self._load_active_working_recipe()
        self.setup_ui()

    def _load_active_working_recipe(self):
        saved = self.app.get_active_deck()
        self.working_recipe = {cid: saved.get(cid, 0) for cid in CARD_DB}

    def _build_deck_slot_options(self) -> list:
        """回傳所有可選卡組清單 [(顯示名稱, slot_key), ...]：固定包含內建三套真實構築 ＋ 玩家自建的多套卡組"""
        opts = [
            ("預設套牌 1：防盾系列 (BFR/S78)", "BFR/S78"),
            ("預設套牌 2：GA文庫 8箭地旅 (GA/S131)", "GA/S131"),
            ("預設套牌 3：孤獨搖滾！ (BTR/W107)", "BTR/W107"),
        ]
        existing_keys = {k for _, k in opts}
        # 加入玩家自建卡組與透過貓罐子牌組網址匯入的 50 張完整牌組
        user_names = self.app.settings.get("user_deck_names") or {}
        for k, rec in self.app.decks_book.items():
            if k.startswith("_") or k in existing_keys:
                continue
            if self.app._is_valid_recipe(rec):
                disp = user_names.get(k) or self.app.get_deck_display_name(k)
                opts.append((f"自訂卡組：{disp}", k))
                existing_keys.add(k)
        if "CUSTOM" not in existing_keys:
            disp_c = user_names.get("CUSTOM", "我的自訂卡組 1")
            opts.append((f"自訂卡組：{disp_c}", "CUSTOM"))
        return opts

    def _build_series_filter_options(self) -> list:
        """回傳下拉選單專用的所有系列清單 [(顯示名稱, series_key), ...]"""
        opts = [
            ("🌟 全部系列卡池 (自由混編)", "ALL"),
            ("✅ 目前卡組已入編卡片", "IN_DECK"),
        ]
        for scode in ["BFR/S78", "GA/S131", "BTR/W107"]:
            if scode in SERIES_DB:
                cnt = len(SERIES_DB[scode])
                opts.append((f"🎴 {SERIES_LABELS.get(scode, scode)} ({cnt}張)", scode))
        for scode in sorted(SERIES_DB.keys()):
            if scode not in ("BFR/S78", "GA/S131", "BTR/W107"):
                cnt = len(SERIES_DB[scode])
                opts.append((f"🎴 {SERIES_LABELS.get(scode, scode)} ({cnt}張)", scode))
        return opts

    def setup_ui(self):
        ff = self.app.get_font_family()
        # 第一列：返回、卡組張數統計、匯入、清空、儲存、另存新卡組
        top_bar = tk.Frame(self, bg="#1b1c24", pady=8, padx=14, relief=tk.RIDGE, bd=2)
        top_bar.pack(fill=tk.X, padx=8, pady=(6, 3))

        tk.Button(
            top_bar,
            text="⬅ 返回主選單",
            bg="#3a3a48",
            fg="white",
            font=(ff, 11, "bold"),
            padx=14,
            pady=4,
            cursor="hand2",
            command=self.app.show_main_menu,
        ).pack(side=tk.LEFT, padx=4)

        self.lbl_summary = tk.Label(
            top_bar,
            text="",
            bg="#1b1c24",
            fg="#ffd166",
            font=(ff, 13, "bold"),
        )
        self.lbl_summary.pack(side=tk.LEFT, padx=12)

        self.lbl_feedback = tk.Label(
            top_bar,
            text="",
            bg="#1b1c24",
            fg="#06d6a0",
            font=(ff, 10, "bold"),
        )
        self.lbl_feedback.pack(side=tk.LEFT, padx=6)

        tk.Button(
            top_bar,
            text="💾 儲存目前卡組",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=14,
            pady=4,
            cursor="hand2",
            command=self.save_deck,
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            top_bar,
            text="➕ 另存為新卡組",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.save_as_new_deck_modal,
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            top_bar,
            text="🧹 清空配比",
            bg="#4a4e69",
            fg="white",
            font=(ff, 10, "bold"),
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.clear_all_counts,
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            top_bar,
            text="🌐 貓罐子匯入系列/牌組",
            bg="#9b5de5",
            fg="white",
            font=(ff, 10, "bold"),
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.app.open_bottleneko_importer_modal(refresh_callback=self.app.open_deck_builder),
        ).pack(side=tk.RIGHT, padx=4)

        # 第二列：多套卡組切換管理選單 ＋ 查卡名即時搜索欄
        preset_search_bar = tk.Frame(self, bg="#161822", pady=7, padx=14, relief=tk.SOLID, bd=1)
        preset_search_bar.pack(fill=tk.X, padx=8, pady=2)

        tk.Label(
            preset_search_bar,
            text="🃏 切換／管理我的卡組：",
            bg="#161822",
            fg="#ffd166",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.dynamic_preset_options = self._build_deck_slot_options()
        self.preset_var = tk.StringVar()
        preset_labels = [label for label, _ in self.dynamic_preset_options]
        cur_idx = 0
        for i, (_, code_key) in enumerate(self.dynamic_preset_options):
            if code_key == self.app.active_series:
                cur_idx = i
                break
        if preset_labels:
            self.preset_var.set(preset_labels[cur_idx])

        self.cmb_preset = ttk.Combobox(
            preset_search_bar,
            textvariable=self.preset_var,
            values=preset_labels,
            state="readonly",
            width=30,
            font=(ff, 11, "bold"),
        )
        self.cmb_preset.pack(side=tk.LEFT, padx=4)
        self.cmb_preset.bind("<<ComboboxSelected>>", self.on_select_preset_menu)

        tk.Button(
            preset_search_bar,
            text="📥 載入並設為出戰",
            bg="#118ab2",
            fg="white",
            font=(ff, 10, "bold"),
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.on_select_preset_menu,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            preset_search_bar,
            text="🗑️ 刪除此自訂卡組",
            bg="#e63946",
            fg="white",
            font=(ff, 10, "bold"),
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.delete_current_custom_deck,
        ).pack(side=tk.LEFT, padx=4)

        # 右側：查卡名搜索框
        search_box = tk.Frame(preset_search_bar, bg="#161822")
        search_box.pack(side=tk.RIGHT, padx=4)

        tk.Label(
            search_box,
            text="🔍 搜尋卡名 / 卡號 / 特徵：",
            bg="#161822",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.search_var = tk.StringVar()
        self.ent_search = tk.Entry(
            search_box,
            textvariable=self.search_var,
            bg="#10121a",
            fg="#ffffff",
            insertbackground="white",
            font=(ff, 11, "bold"),
            width=20,
        )
        self.ent_search.pack(side=tk.LEFT, padx=4)
        self.ent_search.bind("<Return>", lambda e: self.on_search_change())

        tk.Button(
            search_box,
            text="搜尋",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.on_search_change,
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            search_box,
            text="✖ 清除",
            bg="#3a3f58",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.clear_search,
        ).pack(side=tk.LEFT, padx=3)

        # 第三列：下拉式系列卡池選擇器 ＋ 快速切換「全部/已入編」 ＋ 版本篩選
        series_bar = tk.Frame(self, bg="#141620", pady=6, padx=14, relief=tk.SOLID, bd=1)
        series_bar.pack(fill=tk.X, padx=8, pady=(0, 4))

        tk.Label(
            series_bar,
            text="📚 選擇卡池系列：",
            bg="#141620",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.series_filter_options = self._build_series_filter_options()
        self.series_combo_var = tk.StringVar()
        s_labels = [lbl for lbl, _ in self.series_filter_options]
        s_idx = 0
        for idx_s, (_, skey) in enumerate(self.series_filter_options):
            if skey == self.selected_series:
                s_idx = idx_s
                break
        if s_labels:
            self.series_combo_var.set(s_labels[s_idx])

        self.cmb_series_filter = ttk.Combobox(
            series_bar,
            textvariable=self.series_combo_var,
            values=s_labels,
            state="readonly",
            width=34,
            font=(ff, 10, "bold"),
        )
        self.cmb_series_filter.pack(side=tk.LEFT, padx=4)
        self.cmb_series_filter.bind("<<ComboboxSelected>>", self._on_series_combo_selected)

        # 兩個最常用的快捷篩選鈕：看「已入編卡片」與「全部卡池」
        for f_key, f_label in [
            ("IN_DECK", "✅ 只看目前已入編卡片"),
            ("ALL", "🌟 全部系列卡池"),
        ]:
            is_cur = f_key == self.selected_series
            b = tk.Button(
                series_bar,
                text=f_label,
                bg="#ffd166" if is_cur else "#252734",
                fg="#000000" if is_cur else "#ffffff",
                font=(ff, 10, "bold"),
                padx=10,
                pady=2,
                cursor="hand2",
                command=lambda s=f_key: self.set_series_filter(s),
            )
            b.pack(side=tk.LEFT, padx=4)
            self.series_buttons[f_key] = b

        # 版本篩選與一鍵全閃/一般版切換按鈕
        tk.Label(
            series_bar,
            text="｜版本：",
            bg="#141620",
            fg="#ffd166",
            font=(ff, 10, "bold"),
        ).pack(side=tk.LEFT, padx=(8, 2))

        for r_key, r_lbl in [
            ("ALL", "全部版本"),
            ("NORMAL", "一般版"),
            ("HIGH", "✨高版本"),
        ]:
            is_rcur = r_key == self.rarity_filter
            rb = tk.Button(
                series_bar,
                text=r_lbl,
                bg="#06d6a0" if is_rcur else "#252734",
                fg="#000000" if is_rcur else "#ffffff",
                font=(ff, 9, "bold"),
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda rk=r_key: self.set_rarity_filter(rk),
            )
            rb.pack(side=tk.LEFT, padx=2)
            self.rarity_buttons[r_key] = rb

        tk.Button(
            series_bar,
            text="✨ 全卡組換高版本",
            bg="#9d4edd",
            fg="#ffffff",
            font=(ff, 9, "bold"),
            padx=9,
            pady=2,
            cursor="hand2",
            command=lambda: self.convert_deck_rarity(to_high=True),
        ).pack(side=tk.LEFT, padx=(8, 2))

        tk.Button(
            series_bar,
            text="🎴 全卡組換一般版",
            bg="#3a3f58",
            fg="#ffffff",
            font=(ff, 9, "bold"),
            padx=9,
            pady=2,
            cursor="hand2",
            command=lambda: self.convert_deck_rarity(to_high=False),
        ).pack(side=tk.LEFT, padx=2)

        self.lbl_active_badge = tk.Label(
            series_bar,
            text=f"⚔️ 出戰：{self.app.get_deck_display_name(self.app.active_series)}",
            bg="#141620",
            fg="#06d6a0",
            font=(ff, 10, "bold"),
        )
        self.lbl_active_badge.pack(side=tk.RIGHT, padx=4)

        body = tk.Frame(self, bg="#111218")
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # 左側預覽面板：上方放「卡圖＋規格資訊」，下方整塊滿版全部放「效果文」，零留白浪費！
        left_panel = tk.Frame(body, bg="#1b1c24", width=520, relief=tk.RIDGE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="◆ 卡片詳細資訊與效果文預覽 ◆",
            bg="#1b1c24",
            fg="#ffd166",
            font=(ff, 12, "bold"),
        ).pack(anchor="w", padx=12, pady=(8, 4))

        detail_box = tk.Frame(left_panel, bg="#242632", bd=1, relief=tk.SOLID)
        detail_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 上半部：左邊卡圖、右邊規格與高低版本切換
        top_info_area = tk.Frame(detail_box, bg="#242632")
        top_info_area.pack(fill=tk.X, padx=10, pady=(10, 6))

        self.lbl_card_img = tk.Label(top_info_area, bg="#111218", width=165, height=230)
        self.lbl_card_img.pack(side=tk.LEFT, anchor="n", padx=(0, 12))

        right_meta = tk.Frame(top_info_area, bg="#242632")
        right_meta.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_card_title = tk.Label(
            right_meta,
            text="點擊右側卡片預覽",
            bg="#242632",
            fg="#ffffff",
            font=(ff, 13, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=295,
        )
        self.lbl_card_title.pack(fill=tk.X)

        self.lbl_card_stats = tk.Label(
            right_meta,
            text="",
            bg="#242632",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=295,
        )
        self.lbl_card_stats.pack(fill=tk.X, pady=(6, 6))

        ver_btn_row = tk.Frame(right_meta, bg="#242632")
        ver_btn_row.pack(fill=tk.X, pady=(2, 0))

        self.btn_toggle_rarity_preview = tk.Button(
            ver_btn_row,
            text="✨ 切換看高版本",
            bg="#9d4edd",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._on_toggle_inspected_rarity,
        )
        self.btn_toggle_rarity_preview.pack(side=tk.LEFT)

        # 下半部：整塊滿版寬度全部用來顯示卡片效果文，徹底消除左下方空白！
        effect_header = tk.Frame(detail_box, bg="#1b1e2b", padx=10, pady=4)
        effect_header.pack(fill=tk.X, padx=10, pady=(4, 0))
        tk.Label(
            effect_header,
            text="📜 卡片效果文",
            bg="#1b1e2b",
            fg="#ffd166",
            font=(ff, 10, "bold"),
        ).pack(side=tk.LEFT)

        self.txt_card_effect = scrolledtext.ScrolledText(
            detail_box,
            bg="#14151d",
            fg="#f1faee",
            font=(ff, max(12, self.app.get_effect_font_size())),
            wrap=tk.WORD,
            bd=0,
            padx=10,
            pady=8,
        )
        self.txt_card_effect.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.txt_card_effect.config(state=tk.DISABLED)

        # 右側卡片網格面板
        right_panel = tk.Frame(body, bg="#181922", relief=tk.RIDGE, bd=2)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        page_bar = tk.Frame(right_panel, bg="#141620", pady=5, padx=10)
        page_bar.pack(fill=tk.X, side=tk.TOP)

        self.btn_prev_page = tk.Button(
            page_bar,
            text="◀ 上一頁",
            bg="#2b3348",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            pady=2,
            cursor="hand2",
            command=self.prev_page,
        )
        self.btn_prev_page.pack(side=tk.LEFT, padx=4)

        self.lbl_page_info = tk.Label(
            page_bar,
            text="第 1 / 1 頁（共 0 張）",
            bg="#141620",
            fg="#ffd166",
            font=(ff, 11, "bold"),
        )
        self.lbl_page_info.pack(side=tk.LEFT, padx=12)

        self.btn_next_page = tk.Button(
            page_bar,
            text="下一頁 ▶",
            bg="#2b3348",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            pady=2,
            cursor="hand2",
            command=self.next_page,
        )
        self.btn_next_page.pack(side=tk.LEFT, padx=4)

        self.canvas = tk.Canvas(right_panel, bg="#181922", highlightthickness=0)
        scrollbar = tk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.canvas.yview)
        self.grid_frame = tk.Frame(self.canvas, bg="#181922")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.populate_cards()
        self.update_summary()
        first_cid = next((cid for cid, cnt in self.working_recipe.items() if cnt > 0), None)
        if not first_cid and CARD_DB:
            first_cid = next(iter(CARD_DB.keys()))
        if first_cid:
            self.inspect_card(first_cid)

    def _on_mousewheel(self, event):
        if self.winfo_exists() and event.delta:
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def _on_series_combo_selected(self, event=None):
        chosen_lbl = self.series_combo_var.get()
        for lbl, skey in self.series_filter_options:
            if lbl == chosen_lbl:
                self.set_series_filter(skey)
                break

    def on_search_change(self):
        self.search_keyword = self.search_var.get().strip().lower()
        self.current_page = 0
        self.populate_cards()

    def clear_search(self):
        self.search_var.set("")
        self.search_keyword = ""
        self.current_page = 0
        self.populate_cards()

    def on_select_preset_menu(self, event=None):
        chosen_label = self.preset_var.get()
        chosen_key = "BFR/S78"
        for label, key in self.dynamic_preset_options:
            if label == chosen_label:
                chosen_key = key
                break

        recipe = self.app.get_series_deck(chosen_key)
        self.working_recipe = {cid: recipe.get(cid, 0) for cid in CARD_DB}
        self.app.set_active_series(chosen_key)

        # 自動將卡池切換至該套牌所屬系列或「已入編卡片」
        if chosen_key in SERIES_DB:
            self.set_series_filter(chosen_key)
        else:
            self.set_series_filter("IN_DECK")

        self.lbl_active_badge.config(
            text=f"⚔️ 出戰：{self.app.get_deck_display_name(self.app.active_series)}"
        )
        self.update_summary()
        self.lbl_feedback.config(
            text=f"📥 已載入【{self.app.get_deck_display_name(chosen_key)}】並設為出戰卡組！",
            fg="#06d6a0",
        )

    def save_as_new_deck_modal(self):
        """彈出命名視窗，讓玩家將目前配比儲存為一套全新的自訂卡組（支援建立多套不同卡組）"""
        total = sum(self.working_recipe.values())
        cx_total = sum(
            cnt for cid, cnt in self.working_recipe.items() if cid in CARD_DB and CARD_DB[cid]["type"] == "CX"
        )
        if total != 50:
            self.lbl_feedback.config(
                text=f"❌ 另存失敗：卡組必須剛好 50 張（目前 {total} 張）！", fg="#ff4d6d"
            )
            return
        if cx_total > 8:
            self.lbl_feedback.config(
                text=f"❌ 另存失敗：名場面不能超過 8 張（目前 {cx_total} 張）！", fg="#ff4d6d"
            )
            return

        ff = self.app.get_font_family()
        win = tk.Toplevel(self.app.root)
        win.title("➕ 另存為新自訂卡組")
        win.geometry("460x220")
        win.configure(bg="#151b29")
        win.transient(self.app.root)
        win.grab_set()

        tk.Label(
            win,
            text="請輸入這副新卡組的名稱：",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 13, "bold"),
        ).pack(pady=(20, 8))

        user_names = dict(self.app.settings.get("user_deck_names") or {})
        next_num = len(user_names) + 1
        ent_name = tk.Entry(
            win,
            bg="#0d111a",
            fg="#06d6a0",
            insertbackground="white",
            font=(ff, 13, "bold"),
            width=26,
        )
        ent_name.insert(0, f"我的自訂卡組 {next_num}")
        ent_name.pack(pady=6)
        ent_name.focus_set()

        def _confirm_create():
            d_name = ent_name.get().strip() or f"我的自訂卡組 {next_num}"
            idx_n = 1
            while f"USER_DECK_{idx_n}" in self.app.decks_book:
                idx_n += 1
            new_key = f"USER_DECK_{idx_n}"
            cleaned = {cid: cnt for cid, cnt in self.working_recipe.items() if cnt > 0}
            user_names[new_key] = d_name
            self.app.settings["user_deck_names"] = user_names
            self.app.save_user_settings(self.app.settings)
            self.app.save_series_deck(new_key, cleaned)
            self.app.set_active_series(new_key)
            win.destroy()
            # 重新整理卡組下拉選單
            self.dynamic_preset_options = self._build_deck_slot_options()
            preset_labels = [label for label, _ in self.dynamic_preset_options]
            self.cmb_preset.config(values=preset_labels)
            for label, k in self.dynamic_preset_options:
                if k == new_key:
                    self.preset_var.set(label)
                    break
            self.lbl_active_badge.config(text=f"⚔️ 出戰：{self.app.get_deck_display_name(new_key)}")
            self.lbl_feedback.config(text=f"🎉 已成功建立並切換至新卡組【{d_name}】！", fg="#06d6a0")

        btn_f = tk.Frame(win, bg="#151b29")
        btn_f.pack(pady=16)
        tk.Button(
            btn_f,
            text="✔ 確認儲存新卡組",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=16,
            pady=4,
            cursor="hand2",
            command=_confirm_create,
        ).pack(side=tk.LEFT, padx=8)
        tk.Button(
            btn_f,
            text="取消",
            bg="#3a3f58",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            padx=14,
            pady=4,
            command=win.destroy,
        ).pack(side=tk.LEFT, padx=8)

    def delete_current_custom_deck(self):
        cur_k = self.app.active_series
        if cur_k in ("BFR/S78", "GA/S131", "BTR/W107"):
            self.lbl_feedback.config(text="⚠️ 內建的三大預設套牌無法刪除，但你可以直接修改或另存新卡組！", fg="#ffd166")
            return
        disp_old = self.app.get_deck_display_name(cur_k)
        self.app.decks_book.pop(cur_k, None)
        user_names = dict(self.app.settings.get("user_deck_names") or {})
        user_names.pop(cur_k, None)
        self.app.settings["user_deck_names"] = user_names
        self.app.save_user_settings(self.app.settings)
        self.app.set_active_series("BFR/S78")
        self._load_active_working_recipe()
        self.dynamic_preset_options = self._build_deck_slot_options()
        preset_labels = [label for label, _ in self.dynamic_preset_options]
        self.cmb_preset.config(values=preset_labels)
        if preset_labels:
            self.preset_var.set(preset_labels[0])
        self.lbl_active_badge.config(text=f"⚔️ 出戰：{self.app.get_deck_display_name(self.app.active_series)}")
        self.populate_cards()
        self.update_summary()
        self.lbl_feedback.config(text=f"🗑️ 已刪除自訂卡組【{disp_old}】，並切回預設套牌。", fg="#ffd166")

    def inspect_card(self, cid):
        if cid not in CARD_DB:
            return
        data = CARD_DB[cid]
        img = self.img_mgr.get_card_visual(cid, 165, 230)
        self.lbl_card_img.config(image=img, width=165, height=230)
        self.lbl_card_img.image = img

        self.current_inspected_cid = cid
        is_hr = bool(data.get("is_high_rarity", False))
        r_tag = data.get("rarity", "R")
        ver_str = f"✨ 高版本 [{r_tag}]" if is_hr else f"一般版 [{r_tag}]"
        self.lbl_card_title.config(
            text=f"{data['name']}\n{cid} （{ver_str}）",
            fg="#ffd166" if is_hr else "#ffffff",
        )
        traits_str = " / ".join(data["traits"]) if data["traits"] else "無"
        base_id = data.get("base_id", cid)
        group_total = sum(
            self.working_recipe.get(k, 0)
            for k, v in CARD_DB.items()
            if v.get("base_id", k) == base_id
        )
        stats_text = (
            f"系列：{SERIES_LABELS.get(data.get('series', ''), data.get('series', ''))}\n"
            f"同名入編：{group_total} / 4 張 ｜ 種類：{get_card_type_zh(data['type'])} ｜ 顏色：{data['color']}\n"
            f"等級：{data['level']} ｜ 費用：{data['cost']} ｜ 攻擊力：{data['power']} ｜ 魂傷：{data['soul']}\n"
            f"標記：{get_trigger_zh(data['trigger'])} ｜ 特徵：{traits_str}"
        )
        self.lbl_card_stats.config(text=stats_text)
        if hasattr(self, "btn_toggle_rarity_preview"):
            partner_id = data.get("base_id", cid) if is_hr else data.get("high_rarity_id", cid)
            if partner_id and partner_id in CARD_DB and partner_id != cid:
                self.btn_toggle_rarity_preview.config(
                    text="🎴 切換看一般版" if is_hr else f"✨ 切換看高版本 ({CARD_DB[partner_id].get('rarity', 'SR')})",
                    bg="#3a3f58" if is_hr else "#9d4edd",
                    state=tk.NORMAL,
                )
            else:
                self.btn_toggle_rarity_preview.config(text="無其他版本", state=tk.DISABLED)

        self.txt_card_effect.config(state=tk.NORMAL)
        self.txt_card_effect.delete("1.0", tk.END)
        self.txt_card_effect.insert(tk.END, data["text"] or "（無效果文）")
        self.txt_card_effect.config(state=tk.DISABLED)

    def _on_toggle_inspected_rarity(self):
        cid = getattr(self, "current_inspected_cid", None)
        if not cid or cid not in CARD_DB:
            return
        data = CARD_DB[cid]
        is_hr = bool(data.get("is_high_rarity", False))
        partner_id = data.get("base_id", cid) if is_hr else data.get("high_rarity_id", cid)
        if partner_id and partner_id in CARD_DB:
            self.inspect_card(partner_id)

    def set_series_filter(self, scode: str):
        self.selected_series = scode
        self.current_page = 0
        for k, b in self.series_buttons.items():
            b.config(
                bg="#ffd166" if k == scode else "#252734",
                fg="#000000" if k == scode else "#ffffff",
            )
        if hasattr(self, "series_filter_options"):
            for lbl, skey in self.series_filter_options:
                if skey == scode:
                    self.series_combo_var.set(lbl)
                    break
        self.populate_cards()
        self.update_summary()

    def set_rarity_filter(self, r_mode: str):
        self.rarity_filter = r_mode
        self.current_page = 0
        for k, b in self.rarity_buttons.items():
            b.config(
                bg="#06d6a0" if k == r_mode else "#252734",
                fg="#000000" if k == r_mode else "#ffffff",
            )
        self.populate_cards()

    def convert_deck_rarity(self, to_high: bool = True):
        """一鍵將目前卡組內所有卡片升級為高版本 (SP/SSP/RRR/SR) 或還原為一般版"""
        new_recipe = {k: 0 for k in CARD_DB}
        converted_cnt = 0
        for cid, cnt in self.working_recipe.items():
            if cnt <= 0 or cid not in CARD_DB:
                continue
            data = CARD_DB[cid]
            if to_high:
                target_id = data.get("high_rarity_id", cid)
            else:
                target_id = data.get("base_id", cid)
            if target_id not in CARD_DB:
                target_id = cid
            if target_id != cid:
                converted_cnt += cnt
            new_recipe[target_id] = new_recipe.get(target_id, 0) + cnt
        self.working_recipe = new_recipe
        cur_ace = self.app.get_series_ace_card_id(self.app.active_series)
        if cur_ace in CARD_DB:
            ace_data = CARD_DB[cur_ace]
            new_ace = ace_data.get("high_rarity_id", cur_ace) if to_high else ace_data.get("base_id", cur_ace)
            if new_ace in CARD_DB:
                self.app.set_user_ace_card_id(new_ace)
        self.populate_cards()
        self.update_summary()
        if getattr(self, "current_inspected_cid", None) in CARD_DB:
            c_ins = CARD_DB[self.current_inspected_cid]
            t_ins = c_ins.get("high_rarity_id", self.current_inspected_cid) if to_high else c_ins.get("base_id", self.current_inspected_cid)
            if t_ins in CARD_DB:
                self.inspect_card(t_ins)
        mode_name = "✨ 高版本" if to_high else "🎴 一般版"
        self.lbl_feedback.config(
            text=f"✨ 已將目前卡組切換為【{mode_name}】（共轉換 {converted_cnt} 張）！記得點擊『儲存目前卡組』。",
            fg="#ffd166" if to_high else "#06d6a0",
        )

    def clear_all_counts(self):
        for cid in self.working_recipe:
            self.working_recipe[cid] = 0
        for cid, lbl in self.count_labels.items():
            lbl.config(text="0 張", fg="#adb5bd")
        self.update_summary()
        self.lbl_feedback.config(text="🧹 已清空配比，可從上方下拉選單切換任何系列自由組建 50 張卡組。", fg="#8ecae6")

    def _get_filtered_card_items(self):
        if self.selected_series == "ALL":
            base_items = list(CARD_DB.items())
        elif self.selected_series == "IN_DECK":
            base_items = [(cid, data) for cid, data in CARD_DB.items() if self.working_recipe.get(cid, 0) > 0]
        else:
            base_items = list(SERIES_DB.get(self.selected_series, {}).items())

        if self.rarity_filter == "NORMAL":
            base_items = [(cid, d) for cid, d in base_items if not d.get("is_high_rarity", False)]
        elif self.rarity_filter == "HIGH":
            base_items = [(cid, d) for cid, d in base_items if d.get("is_high_rarity", False)]

        kw = self.search_keyword
        if not kw:
            return base_items

        matched = []
        for cid, data in base_items:
            haystack = " ".join([
                cid.lower(),
                data.get("name", "").lower(),
                data.get("jp_name", "").lower(),
                " ".join(data.get("traits", [])).lower(),
                data.get("type", "").lower(),
                data.get("color", "").lower(),
                data.get("rarity", "").lower(),
            ])
            if kw in haystack:
                matched.append((cid, data))
        return matched

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.populate_cards()
            self.canvas.yview_moveto(0.0)

    def next_page(self):
        filtered_items = self._get_filtered_card_items()
        total_pages = max(1, (len(filtered_items) + self.page_size - 1) // self.page_size)
        if self.current_page + 1 < total_pages:
            self.current_page += 1
            self.populate_cards()
            self.canvas.yview_moveto(0.0)

    def populate_cards(self):
        if not self.winfo_exists():
            return
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.count_labels.clear()

        filtered_items = self._get_filtered_card_items()
        total_count = len(filtered_items)
        total_pages = max(1, (total_count + self.page_size - 1) // self.page_size)
        if self.current_page >= total_pages:
            self.current_page = max(0, total_pages - 1)

        if hasattr(self, "lbl_page_info"):
            start_n = self.current_page * self.page_size + 1 if total_count > 0 else 0
            end_n = min(total_count, (self.current_page + 1) * self.page_size)
            self.lbl_page_info.config(
                text=f"第 {self.current_page + 1} / {total_pages} 頁 （顯示 {start_n}~{end_n} 張，共 {total_count} 張）"
            )
            self.btn_prev_page.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
            self.btn_next_page.config(state=tk.NORMAL if self.current_page + 1 < total_pages else tk.DISABLED)

        if not filtered_items:
            tk.Label(
                self.grid_frame,
                text="🔍 找不到符合條件的卡片，請透過上方『📚 選擇卡池系列』下拉選單切換系列或清除關鍵字。",
                bg="#181922",
                fg="#ffd166",
                font=("Microsoft JhengHei", 13, "bold"),
                padx=30,
                pady=40,
            ).grid(row=0, column=0, columnspan=4)
            return

        page_items = filtered_items[self.current_page * self.page_size : (self.current_page + 1) * self.page_size]
        cols = 4
        for idx, (cid, data) in enumerate(page_items):
            r, c = divmod(idx, cols)
            is_hr = bool(data.get("is_high_rarity", False))
            r_tag = data.get("rarity", "R")
            box_bg = "#2b2338" if is_hr else "#252734"
            card_box = tk.Frame(
                self.grid_frame,
                bg=box_bg,
                bd=2,
                relief=tk.RAISED,
                padx=10,
                pady=8,
                highlightbackground="#ffd166" if is_hr else "#252734",
                highlightthickness=2 if is_hr else 0,
            )
            card_box.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            c_img = self.img_mgr.get_card_visual(cid, 122, 170, is_selected=is_hr)
            img_btn = tk.Button(
                card_box,
                image=c_img,
                bg="#181922",
                bd=0,
                cursor="hand2",
                command=lambda k=cid: self.inspect_card(k),
            )
            img_btn.image = c_img
            img_btn.pack()

            type_tag = "【名場面】" if data["type"] == "CX" else f"Lv.{data['level']}"
            ver_badge = f"✨{r_tag}" if is_hr else r_tag
            tk.Label(
                card_box,
                text=f"{data['name'][:12]}\n{type_tag} [{ver_badge}] ｜ {cid}",
                bg=box_bg,
                fg="#ffd166" if (is_hr or data["type"] == "CX") else "#ffffff",
                font=("Microsoft JhengHei", 9, "bold"),
                justify=tk.CENTER,
            ).pack(pady=4)

            # 僅保留乾淨的「－ / 張數 / ＋」按鈕，移除每張卡多餘的王牌按鈕
            ctrl_row = tk.Frame(card_box, bg=box_bg)
            ctrl_row.pack(pady=2)

            tk.Button(
                ctrl_row,
                text=" − ",
                bg="#e63946",
                fg="white",
                font=("Microsoft JhengHei", 12, "bold"),
                width=4,
                cursor="hand2",
                command=lambda k=cid: self.change_count(k, -1),
            ).pack(side=tk.LEFT, padx=4)

            cur_cnt = self.working_recipe.get(cid, 0)
            lbl_cnt = tk.Label(
                ctrl_row,
                text=f"{cur_cnt} 張",
                bg="#14151d",
                fg="#06d6a0" if cur_cnt > 0 else "#adb5bd",
                font=("Microsoft JhengHei", 12, "bold"),
                width=7,
                pady=2,
            )
            lbl_cnt.pack(side=tk.LEFT, padx=4)
            self.count_labels[cid] = lbl_cnt

            tk.Button(
                ctrl_row,
                text=" ＋ ",
                bg="#06d6a0",
                fg="black",
                font=("Microsoft JhengHei", 12, "bold"),
                width=4,
                cursor="hand2",
                command=lambda k=cid: self.change_count(k, 1),
            ).pack(side=tk.LEFT, padx=4)

    def change_count(self, cid, delta):
        if cid not in CARD_DB:
            return
        data = CARD_DB[cid]
        base_id = data.get("base_id", cid)
        same_group = [k for k, v in CARD_DB.items() if v.get("base_id", k) == base_id]
        cur = self.working_recipe.get(cid, 0)

        if delta < 0:
            new_val = max(0, cur + delta)
            self.working_recipe[cid] = new_val
        else:
            group_total = sum(self.working_recipe.get(k, 0) for k in same_group)
            if group_total < 4:
                new_val = min(4, cur + delta)
                self.working_recipe[cid] = new_val
            elif cur < 4:
                other_keys = [k for k in same_group if k != cid and self.working_recipe.get(k, 0) > 0]
                if other_keys:
                    ok = other_keys[0]
                    self.working_recipe[ok] -= 1
                    self.working_recipe[cid] = cur + 1
                    if ok in self.count_labels:
                        ov = self.working_recipe[ok]
                        self.count_labels[ok].config(
                            text=f"{ov} 張", fg="#06d6a0" if ov > 0 else "#adb5bd"
                        )
                    self.lbl_feedback.config(
                        text=f"🔄 同名卡合計上限 4 張：已自動將 1 張【{ok}】替換為【{cid}】！",
                        fg="#ffd166",
                    )

        for k in same_group:
            if k in self.count_labels:
                kv = self.working_recipe.get(k, 0)
                self.count_labels[k].config(
                    text=f"{kv} 張", fg="#06d6a0" if kv > 0 else "#adb5bd"
                )
        self.inspect_card(cid)
        self.update_summary()

    def update_summary(self):
        total = sum(self.working_recipe.values())
        cx_total = sum(
            cnt for cid, cnt in self.working_recipe.items() if cid in CARD_DB and CARD_DB[cid]["type"] == "CX"
        )
        is_valid = total == 50 and cx_total <= 8
        color = "#06d6a0" if is_valid else "#ff6b6b"
        self.lbl_summary.config(
            text=f"【{self.app.get_deck_display_name(self.app.active_series)}】總張數：{total} / 50 張 ｜ 名場面：{cx_total} / 8 張",
            fg=color,
        )
        if total != 50:
            self.lbl_feedback.config(
                text=f"⚠️ 卡組需滿 50 張（目前差 {50 - total} 張）", fg="#ff6b6b"
            )
        elif cx_total > 8:
            self.lbl_feedback.config(
                text=f"⚠️ 名場面不能超過 8 張（目前 {cx_total} 張）", fg="#ff6b6b"
            )
        else:
            self.lbl_feedback.config(text="✔ 符合 50 張規則！可按『💾 儲存目前卡組』或『➕ 另存為新卡組』。", fg="#06d6a0")

    def save_deck(self):
        total = sum(self.working_recipe.values())
        cx_total = sum(
            cnt for cid, cnt in self.working_recipe.items() if cid in CARD_DB and CARD_DB[cid]["type"] == "CX"
        )
        if total != 50:
            self.lbl_feedback.config(
                text=f"❌ 儲存失敗：卡組未滿或超過 50 張，目前 {total} 張！", fg="#ff4d6d"
            )
            return
        if cx_total > 8:
            self.lbl_feedback.config(
                text=f"❌ 儲存失敗：名場面超過 8 張上限，目前 {cx_total} 張！", fg="#ff4d6d"
            )
            return

        cleaned = {cid: cnt for cid, cnt in self.working_recipe.items() if cnt > 0}
        target_slot = self.app.active_series
        self.app.save_series_deck(target_slot, cleaned)
        self.app.set_active_series(target_slot)
        disp_name = self.app.get_deck_display_name(target_slot)
        self.lbl_active_badge.config(text=f"⚔️ 出戰：{disp_name}")
        self.lbl_feedback.config(
            text=f"💾 已成功儲存【{disp_name}】並設為出戰卡組！（若想保留多套不同牌組可點『➕ 另存為新卡組』）",
            fg="#06d6a0",
        )


# ==========================================
# 對戰主畫面 (WSBofuriGameFrame)
# ==========================================
class WSBofuriGameFrame(tk.Frame):

    def __init__(self, parent, app, net_node=None):
        super().__init__(parent, bg="#111218")
        self.app = app
        self.root = app.root
        self.img_mgr = app.img_mgr
        self.net_node = net_node
        self.is_lan = net_node is not None

        my_battle_name = (
            getattr(app, "player_battle_name", "").strip()
            or app.settings.get("player_name", "玩家1").strip()
            or "玩家1"
        )
        ai_series_label = SERIES_LABELS.get(app.ai_series, app.ai_series)
        self.player = PlayerState(
            my_battle_name,
            app.get_series_deck(app.active_series),
            is_ai=False,
        )
        self.player.ace_cid = app.get_series_ace_card_id(app.active_series)
        opp_name = "連線對手" if self.is_lan else f"AI ({ai_series_label})"
        # 關鍵修正：多人連線時 self.ai.is_ai 設為 False，徹底杜絕真人對戰中途變成 AI！
        self.ai = PlayerState(
            opp_name,
            app.get_series_deck(app.ai_series),
            is_ai=(not self.is_lan),
        )
        self.ai.ace_cid = app.get_ai_ace_card_id(app.ai_series)

        # 雙方獨立卡套設定：我方讀取玩家設定，AI 對手固定使用官方預設卡套 (WS_DEFAULT)，多人連線則透過封包同步對方卡套
        self.player_sleeve_style = app.settings.get("sleeve_style", "WS_DEFAULT")
        self.player_sleeve_custom = app.settings.get("custom_sleeve_path", "")
        self.opp_sleeve_style = "WS_DEFAULT"
        self.opp_sleeve_custom = ""

        self.turn_count = 1
        self.first_player = self.player
        self.active_player = self.player
        self.attacks_this_turn = 0
        self.phase = "SETUP"
        self.selected_hand_idx = None
        self.selected_stage_idx = None
        self.game_over = False
        self.overlay_var = tk.IntVar(value=0)
        self.end_anim_canvas = None
        self.particles = []
        self._lan_peer_mulligan_done = False
        self._lan_my_mulligan_done = False
        self._lan_turn_order_chosen = None
        self._lan_host_duel_started = False
        self._lan_ace_flip_callback = None
        self._remote_flip_state = None
        self._drag_state = {
            "source": None,
            "index": None,
            "card": None,
            "start_x": 0,
            "start_y": 0,
            "dragging": False,
            "ghost": None,
        }

        if self.net_node:
            self.net_node.on_msg = self._on_lan_packet

        self.setup_ui()
        self.start_game()
        if self.net_node and hasattr(self.net_node, "_early_msg_queue"):
            early_q = list(self.net_node._early_msg_queue)
            self.net_node._early_msg_queue.clear()
            for emsg in early_q:
                self.root.after(20, lambda m=emsg: self._process_lan_packet(m))

    def _encode_my_custom_sleeve_b64(self) -> str:
        if self.player_sleeve_style == "CUSTOM" and self.player_sleeve_custom and os.path.exists(self.player_sleeve_custom):
            try:
                import base64
                im = Image.open(self.player_sleeve_custom).convert("RGB").resize((120, 168), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, format="WEBP", quality=80)
                return base64.b64encode(buf.getvalue()).decode("ascii")
            except Exception:
                pass
        return ""

    def _apply_peer_sleeve_sync(self, style_val: str, b64_val: str = ""):
        if not style_val:
            return
        if style_val == "CUSTOM" and b64_val:
            try:
                import base64
                raw = base64.b64decode(b64_val.encode("ascii"))
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                self.img_mgr.sleeve_pil_cache["LAN_PEER_CUSTOM"] = im
                self.img_mgr.deck_stack_cache.clear()
                self.img_mgr.stock_stack_cache.clear()
                self.img_mgr.ai_fan_cache.clear()
                self.opp_sleeve_style = "LAN_PEER_CUSTOM"
                self.opp_sleeve_custom = ""
                return
            except Exception:
                pass
        self.opp_sleeve_style = style_val if style_val in ("WS_DEFAULT", "AMIAMI_21593") else "WS_DEFAULT"
        self.opp_sleeve_custom = ""

    def _on_lan_packet(self, msg: dict):
        self.root.after(0, lambda: self._process_lan_packet(msg))

    def _process_lan_packet(self, msg: dict):
        if not self.winfo_exists() or self.game_over:
            return
        mtype = msg.get("type")
        if mtype == "HELLO_REQ":
            if self.net_node and self.net_node.connected:
                self.net_node.send({
                    "type": "HELLO_SYNC",
                    "player_name": self.player.name,
                    "ace_cid": self.player.ace_cid,
                    "sleeve_style": self.player_sleeve_style,
                    "custom_sleeve_b64": self._encode_my_custom_sleeve_b64(),
                    "sender_state": self.player.to_sync_dict(),
                })
        elif mtype == "HELLO_SYNC":
            peer_name = str(msg.get("player_name", "連線對手")).strip() or "連線對手"
            if peer_name == self.player.name:
                if self.net_node and self.net_node.is_host:
                    self.player.name = f"{self.player.name} (房主)"
                    peer_name = f"{peer_name} (房客)"
                else:
                    self.player.name = f"{self.player.name} (房客)"
                    peer_name = f"{peer_name} (房主)"
            self.ai.name = peer_name
            if "ace_cid" in msg and msg["ace_cid"] in CARD_DB:
                self.ai.ace_cid = msg["ace_cid"]
            self._apply_peer_sleeve_sync(msg.get("sleeve_style", "WS_DEFAULT"), msg.get("custom_sleeve_b64", ""))
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            self.update_ui()
            if self.net_node and self.net_node.is_host and not self._lan_host_duel_started:
                self._lan_host_duel_started = True
                self._host_start_lan_duel_setup()
        elif mtype == "INIT_DUEL_SYNC":
            host_name = str(msg.get("host_name", self.ai.name)).strip() or "房主"
            client_name = str(msg.get("client_name", self.player.name)).strip() or self.player.name
            self.player.name = client_name
            self.ai.name = host_name
            self._apply_peer_sleeve_sync(msg.get("host_sleeve_style", "WS_DEFAULT"), msg.get("host_custom_sleeve_b64", ""))
            if "host_state" in msg:
                self.ai.apply_sync_dict(msg["host_state"])
            if "client_state" in msg:
                self.player.apply_sync_dict(msg["client_state"])
            ace_setup = msg.get("ace_setup", {})
            self.update_ui()
            self._run_lan_turn_order_phase(ace_setup)
        elif mtype == "TURN_ORDER_FLIP_SYNC":
            picked_idx = int(msg.get("picked_idx", 0))
            if callable(self._lan_ace_flip_callback):
                self._lan_ace_flip_callback(picked_idx)
        elif mtype == "TURN_ORDER_CONFIRM_SYNC":
            first_is_sender = bool(msg.get("first_is_sender", True))
            self.first_player = self.ai if first_is_sender else self.player
            self._lan_turn_order_chosen = "SECOND" if first_is_sender else "FIRST"
            self.log(f"👑 王牌先後手決定：由【{self.first_player.name}】獲得先攻！")
            self._close_overlay()
        elif mtype == "FLIP_SEQ_START":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self._start_remote_flip_spectator(msg)
        elif mtype == "FLIP_SEQ_STEP":
            cur_n = int(msg.get("cur_n", 1))
            self._step_remote_flip_spectator(cur_n)
        elif mtype == "FLIP_SEQ_END":
            self._end_remote_flip_spectator()
        elif mtype == "DAMAGE_CHECK_REQ":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            dmg_amt = int(msg.get("amount", 1))
            src_txt = msg.get("source_text", "攻擊")
            self.update_ui()
            self._execute_local_damage_check(self.player, dmg_amt, src_txt)
            if self.net_node and self.net_node.connected and not self.game_over:
                self.net_node.send({
                    "type": "DAMAGE_CHECK_RESP",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
        elif mtype == "DAMAGE_CHECK_RESP":
            self._end_remote_flip_spectator()
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self._close_overlay()
        elif mtype == "MULLIGAN_SYNC":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            self.log(f"🔄 【{self.ai.name}】已完成起手換牌。")
            self._lan_peer_mulligan_done = True
            self.update_ui()
            if self._lan_my_mulligan_done:
                self._close_overlay()
        elif mtype == "ACTION_LOG":
            self.log(f"🌐 [{self.ai.name}] {msg.get('text', '')}")
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
        elif mtype == "STATE_SYNC":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
        elif mtype == "TURN_PASS":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.turn_count = msg.get("turn_count", self.turn_count)
            self.update_ui()
            self.start_turn(self.player)
        elif mtype == "DECLARE_LEVEL_REQ":
            caller = msg.get("caller", self.ai.name)
            decl_lv = self.ask_declare_level_center(caller)
            if self.net_node and self.net_node.connected:
                self.net_node.send({"type": "DECLARE_LEVEL_RESP", "level": decl_lv})
        elif mtype == "DECLARE_LEVEL_RESP":
            self._lan_declared_level = int(msg.get("level", 0))
            self._close_overlay()
        elif mtype == "LEVEL_UP_REQ":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self.check_level_up(self.player)
            if self.net_node and self.net_node.connected and not self.game_over:
                self.net_node.send({
                    "type": "LEVEL_UP_RESP",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
        elif mtype == "LEVEL_UP_RESP":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self._close_overlay()
        elif mtype == "COUNTER_REQ":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            slot_idx = int(msg.get("slot_idx", 0))
            self.update_ui()
            self._handle_local_counter_step(self.ai, self.player, slot_idx)
            if self.net_node and self.net_node.connected:
                self.net_node.send({
                    "type": "COUNTER_RESP",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
        elif mtype == "COUNTER_RESP":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self._close_overlay()
        elif mtype == "ENCORE_REQ":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.phase = "ENCORE"
            self.update_ui()
            self._resolve_player_encore_step(self.player)
            if self.net_node and self.net_node.connected:
                self.net_node.send({
                    "type": "ENCORE_RESP",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
        elif mtype == "ENCORE_RESP":
            if "sender_state" in msg:
                self.ai.apply_sync_dict(msg["sender_state"])
            if "receiver_state" in msg:
                self.player.apply_sync_dict(msg["receiver_state"])
            self.update_ui()
            self._close_overlay()
        elif mtype == "GAME_OVER":
            is_win = bool(msg.get("receiver_win", True))
            reason = msg.get("reason", "對戰結束")
            self.show_game_over_animation(is_win, reason)

    def _broadcast_action(self, text: str):
        if self.net_node and self.net_node.connected:
            self.net_node.send_action_log(
                text,
                player_state_dict=self.player.to_sync_dict(),
                opp_state_dict=self.ai.to_sync_dict(),
            )

    def setup_ui(self):
        # 同步設定中的卡套樣式至 ImageManager
        self.img_mgr.set_sleeve_config(
            self.app.settings.get("sleeve_style", "WS_DEFAULT"),
            self.app.settings.get("custom_sleeve_path", ""),
        )
        ff = self.app.get_font_family()
        eff_fs = max(13, self.app.get_effect_font_size())

        main_pane = tk.Frame(self, bg="#0d111a")
        main_pane.pack(fill=tk.BOTH, expand=True)

        # === 100% 全螢幕決鬥場地 (《Master Duel》風格全畫面牌桌) ===
        theme_board_colors = {
            "OCEAN": "#0f1726",
            "MAPLE_CRIMSON": "#1f0d16",
            "STARLIGHT_GOLD": "#181426",
            "BOCCHI_NEON": "#1c1026",
        }
        cur_theme = self.app.settings.get("theme", "OCEAN")
        board_bg = theme_board_colors.get(cur_theme, "#0f1726")
        self.right_board = tk.Frame(main_pane, bg=board_bg)
        self.right_board.pack(fill=tk.BOTH, expand=True)

        custom_bg_p = self.app.settings.get("custom_bg_path", "")
        if custom_bg_p and os.path.exists(custom_bg_p):
            b_wall = self.img_mgr.get_wallpaper_visual(
                cur_theme,
                custom_bg_p,
                int(self.app.settings.get("bg_dim_percent", 65)),
                1600,
                950,
            )
            self.lbl_board_bg = tk.Label(self.right_board, image=b_wall, bg=board_bg)
            self.lbl_board_bg.image = b_wall
            self.lbl_board_bg.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # 0. 頂部列：中央對手扇形握持手牌卡背 ＋ 右上角《Master Duel》對手頭像與時鐘護盾 HUD
        top_hud_bar = tk.Frame(self.right_board, bg="#151018", pady=2, padx=12)
        top_hud_bar.pack(fill=tk.X)

        tk.Label(
            top_hud_bar,
            text="💡 點擊場上或手牌任意卡片可展開左側【卡片詳情】｜ 右下角可隨時展開【戰況紀錄】",
            bg="#151018",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
        ).pack(side=tk.LEFT, padx=6)

        self.ai_hand_canvas = tk.Canvas(
            top_hud_bar, bg="#151018", width=560, height=70, highlightthickness=0
        )
        self.ai_hand_canvas.pack(side=tk.LEFT, expand=True)
        self._ai_hand_photo_refs = []

        # 右上角：放大版對手決鬥者頭像與生命護盾條 (如 Master Duel 右上角)
        ai_hud = tk.Frame(
            top_hud_bar,
            bg="#2b1824",
            bd=3,
            relief=tk.RIDGE,
            highlightbackground="#ff758f",
            highlightthickness=1,
            padx=14,
            pady=4,
        )
        ai_hud.pack(side=tk.RIGHT, padx=6, pady=2)
        self.lbl_ai_avatar = tk.Label(ai_hud, bg="#2b1824")
        self.lbl_ai_avatar.pack(side=tk.RIGHT, padx=(10, 0))
        ai_hud_txt = tk.Frame(ai_hud, bg="#2b1824")
        ai_hud_txt.pack(side=tk.RIGHT)
        self.lbl_ai_hud_name = tk.Label(
            ai_hud_txt,
            text="",
            bg="#2b1824",
            fg="#ff758f",
            font=(ff, 14, "bold"),
            anchor="e",
        )
        self.lbl_ai_hud_name.pack(fill=tk.X)
        self.lbl_ai_hud_gauge = tk.Label(
            ai_hud_txt,
            text="",
            bg="#2b1824",
            fg="#ffd166",
            font=(ff, 11, "bold"),
            anchor="e",
        )
        self.lbl_ai_hud_gauge.pack(fill=tk.X)

        # 1. 對手半場（將左區「能量/等級/時鐘」與右區「回憶/牌庫/休息室」往中央舞台靠攏，避免被邊緣抽屜遮擋）
        ai_mat = tk.Frame(self.right_board, bg="#211620", bd=1, relief=tk.SOLID)
        ai_mat.pack(fill=tk.X, padx=10, pady=2)

        ai_board_row = tk.Frame(ai_mat, bg="#211620")
        ai_board_row.pack(anchor="center", pady=2)

        ai_left_zones = tk.Frame(ai_board_row, bg="#211620")
        ai_left_zones.pack(side=tk.LEFT, padx=(6, 16), pady=2)
        self.btn_ai_stock = tk.Button(
            ai_left_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#ffd166",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector(
                f"對手能量區 (共 {len(self.ai.stock)} 張蓋牌，依規則不公開明細)", []
            ),
        )
        self.btn_ai_stock.pack(side=tk.LEFT, padx=4)

        self.btn_ai_level = tk.Button(
            ai_left_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#ffadad",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("對手等級區", self.ai.level_zone),
        )
        self.btn_ai_level.pack(side=tk.LEFT, padx=4)

        self.btn_ai_clock = tk.Button(
            ai_left_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#ffadad",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("對手時鐘區", self.ai.clock),
        )
        self.btn_ai_clock.pack(side=tk.LEFT, padx=4)
        self.btn_ai_clock.bind("<Motion>", lambda e: self._on_clock_zone_motion(e, self.ai))

        ai_center_stage = tk.Frame(ai_board_row, bg="#211620")
        ai_center_stage.pack(side=tk.LEFT, padx=10, pady=2)

        ai_cx_col = tk.Frame(ai_center_stage, bg="#2b1924", bd=1, relief=tk.RIDGE, padx=6, pady=6)
        ai_cx_col.pack(side=tk.LEFT, padx=(0, 14), anchor="s", pady=4)
        self.btn_ai_cx = tk.Button(
            ai_cx_col,
            compound=tk.TOP,
            bg="#3b202c",
            fg="#ff758f",
            font=(ff, 10, "bold"),
            command=lambda: self.inspect_card(self.ai.climax_zone, self.ai, None, open_drawer=True) if self.ai.climax_zone else None,
        )
        self.btn_ai_cx.pack()

        ai_stage_5box = tk.Frame(
            ai_center_stage, bg="#291926", bd=2, relief=tk.GROOVE, padx=14, pady=3
        )
        ai_stage_5box.pack(side=tk.LEFT)

        self.btn_ai_stage = [None] * 5
        ai_back_row = tk.Frame(ai_stage_5box, bg="#291926")
        ai_back_row.pack(pady=2)
        for idx in [3, 4]:
            btn = tk.Button(
                ai_back_row,
                compound=tk.TOP,
                bg="#2d1e2b",
                fg="#ffccd5",
                font=(ff, 10, "bold"),
                command=lambda i=idx: self.on_click_ai_stage(i),
            )
            btn.pack(side=tk.LEFT, padx=7)
            btn.bind("<Enter>", lambda e, i=idx: self.inspect_card(self.ai.stage[i], self.ai, i, open_drawer=False) if self.ai.stage[i] else None)
            self.btn_ai_stage[idx] = btn

        ai_front_row = tk.Frame(ai_stage_5box, bg="#291926")
        ai_front_row.pack(pady=2)
        for idx in [0, 1, 2]:
            btn = tk.Button(
                ai_front_row,
                compound=tk.TOP,
                bg="#3c2638",
                fg="#ffffff",
                font=(ff, 10, "bold"),
                command=lambda i=idx: self.on_click_ai_stage(i),
            )
            btn.pack(side=tk.LEFT, padx=7)
            btn.bind("<Enter>", lambda e, i=idx: self.inspect_card(self.ai.stage[i], self.ai, i, open_drawer=False) if self.ai.stage[i] else None)
            self.btn_ai_stage[idx] = btn

        ai_right_zones = tk.Frame(ai_board_row, bg="#211620")
        ai_right_zones.pack(side=tk.LEFT, padx=(16, 6), pady=2)
        self.btn_ai_memory = tk.Button(
            ai_right_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("對手回憶區", self.ai.memory),
        )
        self.btn_ai_memory.pack(side=tk.LEFT, padx=4)

        self.btn_ai_deck = tk.Button(
            ai_right_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#ffffff",
            font=(ff, 10, "bold"),
        )
        self.btn_ai_deck.pack(side=tk.LEFT, padx=4)

        self.btn_ai_wr = tk.Button(
            ai_right_zones,
            compound=tk.TOP,
            bg="#2d1e2b",
            fg="#e0e0e0",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("對手休息室", self.ai.waiting_room),
        )
        self.btn_ai_wr.pack(side=tk.LEFT, padx=4)

        # 2. 《Master Duel》中線戰場資訊帶與右側圓形/膠囊階段推進鈕
        mid_bar = tk.Frame(
            self.right_board, bg="#121622", pady=3, padx=14, bd=2, relief=tk.RIDGE
        )
        mid_bar.pack(fill=tk.X, padx=10, pady=2)

        # 保留場上角色快捷能力鈕 (與頭頂浮動金色按鈕同步連動)
        self.btn_act_ability = tk.Button(
            mid_bar,
            text="⚡ 發動選中角色【起】能力",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=12,
            pady=2,
            state=tk.DISABLED,
            command=self.on_click_act_ability,
        )
        self.btn_act_ability.pack(side=tk.LEFT, padx=4)

        self.btn_move_stage = tk.Button(
            mid_bar,
            text="🔄 交換舞台位置",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=12,
            pady=2,
            state=tk.DISABLED,
            command=self.on_click_move_stage,
        )
        self.btn_move_stage.pack(side=tk.LEFT, padx=4)

        center_phase_box = tk.Frame(mid_bar, bg="#121622")
        center_phase_box.pack(side=tk.LEFT, expand=True)
        self.lbl_phase_info = tk.Label(
            center_phase_box,
            text="",
            bg="#121622",
            fg="#ffd166",
            font=(ff, 14, "bold"),
        )
        self.lbl_phase_info.pack()
        self.lbl_ai_hand_info = tk.Label(
            center_phase_box,
            text="",
            bg="#121622",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        )
        self.lbl_ai_hand_info.pack()

        self.btn_next_phase = tk.Button(
            mid_bar,
            text="進入下一階段 ➔",
            bg="#118ab2",
            fg="white",
            disabledforeground="#8890a8",
            font=(ff, 13, "bold"),
            padx=22,
            pady=5,
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.on_next_phase,
        )
        self.btn_next_phase.pack(side=tk.RIGHT, padx=6)

        # 3. 我方半場（同樣將左區「能量/等級/時鐘」與右區「回憶/牌庫/休息室」往中央舞台靠攏）
        p_mat = tk.Frame(self.right_board, bg="#141e2b", bd=1, relief=tk.SOLID)
        p_mat.pack(fill=tk.X, padx=10, pady=2)

        p_board_row = tk.Frame(p_mat, bg="#141e2b")
        p_board_row.pack(anchor="center", pady=2)

        p_left_zones = tk.Frame(p_board_row, bg="#141e2b")
        p_left_zones.pack(side=tk.LEFT, padx=(6, 16), pady=2)

        self.btn_p_stock = tk.Button(
            p_left_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#ffd166",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector(
                f"我方能量區 (共 {len(self.player.stock)} 張蓋牌，依規則背面朝下)", []
            ),
        )
        self.btn_p_stock.pack(side=tk.LEFT, padx=4)

        self.btn_p_level = tk.Button(
            p_left_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#06d6a0",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("我方等級區", self.player.level_zone),
        )
        self.btn_p_level.pack(side=tk.LEFT, padx=4)

        self.btn_p_clock = tk.Button(
            p_left_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#ff758f",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("我方時鐘區 (傷害區)", self.player.clock),
        )
        self.btn_p_clock.pack(side=tk.LEFT, padx=4)
        self.btn_p_clock.bind("<Motion>", lambda e: self._on_clock_zone_motion(e, self.player))

        p_center_stage = tk.Frame(p_board_row, bg="#141e2b")
        p_center_stage.pack(side=tk.LEFT, padx=10, pady=2)

        p_cx_col = tk.Frame(p_center_stage, bg="#182638", bd=1, relief=tk.RIDGE, padx=6, pady=6)
        p_cx_col.pack(side=tk.LEFT, padx=(0, 14), anchor="n", pady=4)
        self.btn_p_cx = tk.Button(
            p_cx_col,
            compound=tk.TOP,
            bg="#1f3142",
            fg="#ff758f",
            font=(ff, 10, "bold"),
            command=lambda: self.inspect_card(self.player.climax_zone, self.player, None, open_drawer=True)
            if self.player.climax_zone
            else None,
        )
        self.btn_p_cx.pack()

        p_stage_5box = tk.Frame(
            p_center_stage, bg="#182738", bd=2, relief=tk.GROOVE, padx=14, pady=3
        )
        p_stage_5box.pack(side=tk.LEFT)

        self.btn_p_stage = [None] * 5
        p_front_row = tk.Frame(p_stage_5box, bg="#182738")
        p_front_row.pack(pady=2)

        for idx in [0, 1, 2]:
            btn = tk.Button(
                p_front_row,
                compound=tk.TOP,
                bg="#1f3142",
                fg="#ffffff",
                font=(ff, 10, "bold"),
                command=lambda i=idx: self._on_stage_btn_command(i),
            )
            btn.pack(side=tk.LEFT, padx=7)
            btn.bind("<ButtonPress-1>", lambda e, i=idx: self._on_stage_press(e, i))
            btn.bind("<B1-Motion>", self._on_drag_motion)
            btn.bind("<ButtonRelease-1>", self._on_drag_release)
            btn.bind("<Enter>", lambda e, i=idx: self.inspect_card(self.player.stage[i], self.player, i, open_drawer=False) if self.player.stage[i] else None)
            self.btn_p_stage[idx] = btn

        p_back_row = tk.Frame(p_stage_5box, bg="#182738")
        p_back_row.pack(pady=2)
        for idx in [3, 4]:
            btn = tk.Button(
                p_back_row,
                compound=tk.TOP,
                bg="#182636",
                fg="#a8dadc",
                font=(ff, 10, "bold"),
                command=lambda i=idx: self._on_stage_btn_command(i),
            )
            btn.pack(side=tk.LEFT, padx=7)
            btn.bind("<ButtonPress-1>", lambda e, i=idx: self._on_stage_press(e, i))
            btn.bind("<B1-Motion>", self._on_drag_motion)
            btn.bind("<ButtonRelease-1>", self._on_drag_release)
            btn.bind("<Enter>", lambda e, i=idx: self.inspect_card(self.player.stage[i], self.player, i, open_drawer=False) if self.player.stage[i] else None)
            self.btn_p_stage[idx] = btn

        p_right_zones = tk.Frame(p_board_row, bg="#141e2b")
        p_right_zones.pack(side=tk.LEFT, padx=(16, 6), pady=2)

        self.btn_p_memory = tk.Button(
            p_right_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector(
                "我方回憶區", self.player.memory, is_player_memory=True
            ),
        )
        self.btn_p_memory.pack(side=tk.LEFT, padx=4)

        self.btn_p_deck = tk.Button(
            p_right_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#ffffff",
            font=(ff, 10, "bold"),
        )
        self.btn_p_deck.pack(side=tk.LEFT, padx=4)

        self.btn_p_wr = tk.Button(
            p_right_zones,
            compound=tk.TOP,
            bg="#1c2b3d",
            fg="#e0e0e0",
            font=(ff, 10, "bold"),
            command=lambda: self.open_zone_inspector("我方休息室", self.player.waiting_room),
        )
        self.btn_p_wr.pack(side=tk.LEFT, padx=4)

        # 4. 底部《Master Duel》風格三欄列：左下角放大版我方頭像護盾 HUD ＋ 中央扇形交疊握持手牌塢 ＋ 右下角放大版懸浮工具鈕
        hand_outer = tk.Frame(
            self.right_board,
            bg="#0d111a",
            bd=1,
            relief=tk.SOLID,
        )
        hand_outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 4))

        # 左下角：放大版我方決鬥者頭像與生命護盾條 (如 Master Duel 左下角)
        p_hud = tk.Frame(
            hand_outer,
            bg="#172236",
            bd=3,
            relief=tk.RIDGE,
            highlightbackground="#4cc9f0",
            highlightthickness=1,
            padx=16,
            pady=8,
        )
        p_hud.pack(side=tk.LEFT, anchor="s", padx=(10, 8), pady=8)
        self.lbl_p_avatar = tk.Label(p_hud, bg="#172236")
        self.lbl_p_avatar.pack(side=tk.LEFT, padx=(0, 12))
        p_hud_txt = tk.Frame(p_hud, bg="#172236")
        p_hud_txt.pack(side=tk.LEFT)
        self.lbl_p_hud_name = tk.Label(
            p_hud_txt,
            text="",
            bg="#172236",
            fg="#06d6a0",
            font=(ff, 15, "bold"),
            anchor="w",
        )
        self.lbl_p_hud_name.pack(fill=tk.X)
        self.lbl_p_hud_gauge = tk.Label(
            p_hud_txt,
            text="",
            bg="#172236",
            fg="#ffd166",
            font=(ff, 11, "bold"),
            anchor="w",
        )
        self.lbl_p_hud_gauge.pack(fill=tk.X)

        # 右下角：《Master Duel》風格放大版功能控制列 (出牌鈕 + 卡片詳情抽屜開關 + 戰況紀錄抽屜開關 + 返回主選單)
        br_hud = tk.Frame(hand_outer, bg="#0d111a", padx=8, pady=8)
        br_hud.pack(side=tk.RIGHT, anchor="s", padx=(8, 10), pady=6)

        self.btn_play_hand = tk.Button(
            br_hud,
            text="請先點選手牌（或拖移上場）",
            bg="#2b3144",
            fg="#98a2b8",
            disabledforeground="#98a2b8",
            font=(ff, 11, "bold"),
            padx=14,
            pady=6,
            state=tk.DISABLED,
            command=self.on_use_selected_hand,
        )
        self.btn_play_hand.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        br_btn_row = tk.Frame(br_hud, bg="#0d111a")
        br_btn_row.pack(side=tk.TOP, fill=tk.X)

        self.btn_toggle_card_drawer = tk.Button(
            br_btn_row,
            text="🃏 卡片詳情",
            bg="#1d3557",
            fg="#4cc9f0",
            font=(ff, 11, "bold"),
            padx=13,
            pady=6,
            cursor="hand2",
            command=self.toggle_card_drawer,
        )
        self.btn_toggle_card_drawer.pack(side=tk.LEFT, padx=4)

        self.btn_toggle_log_drawer = tk.Button(
            br_btn_row,
            text="📋 戰況紀錄",
            bg="#1d3557",
            fg="#06d6a0",
            font=(ff, 11, "bold"),
            padx=13,
            pady=6,
            cursor="hand2",
            command=self.toggle_log_drawer,
        )
        self.btn_toggle_log_drawer.pack(side=tk.LEFT, padx=4)

        tk.Button(
            br_btn_row,
            text="🏠 主選單",
            bg="#3a3a48",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            padx=13,
            pady=6,
            cursor="hand2",
            command=self.on_exit_to_menu,
        ).pack(side=tk.LEFT, padx=4)

        # 中央：放大版扇形握持手牌畫布
        self.hand_canvas = tk.Canvas(
            hand_outer, bg="#0d111a", height=214, highlightthickness=0
        )
        self.hand_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hand_inner_frame = tk.Frame(self.hand_canvas, bg="#0d111a")
        self.hovered_hand_idx = None
        self._hand_press_idx = None
        self.hand_card_hitboxes = []
        self._field_slot_select_state = None
        self._active_field_cutins = []

        self.hand_canvas.bind("<Configure>", lambda e: self.render_hand_dock())
        self.hand_canvas.bind("<Motion>", self._on_hand_canvas_motion)
        self.hand_canvas.bind("<Leave>", self._on_hand_canvas_leave)
        self.hand_canvas.bind("<ButtonPress-1>", self._on_hand_canvas_press)
        self.hand_canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.hand_canvas.bind("<ButtonRelease-1>", self._on_hand_canvas_release)
        self.hand_canvas.bind("<Double-Button-1>", self._on_hand_canvas_double_click)

        # 5. 場上選中角色頭頂直接浮現的《Master Duel》金色「發動效果 / 移動」浮動膠囊 (如圖 3)
        self.stage_floating_bar = tk.Frame(
            self.right_board,
            bg="#141824",
            bd=2,
            relief=tk.RAISED,
            highlightbackground="#ffd166",
            highlightcolor="#ffd166",
            highlightthickness=2,
            padx=6,
            pady=4,
        )
        self.btn_float_act = tk.Button(
            self.stage_floating_bar,
            text="⚡ 發動效果",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.on_click_act_ability,
        )
        self.btn_float_act.pack(side=tk.LEFT, padx=3)
        self.btn_float_move = tk.Button(
            self.stage_floating_bar,
            text="🔄 移動位置",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.on_click_move_stage,
        )
        self.btn_float_move.pack(side=tk.LEFT, padx=3)

        # 6. 《Master Duel》左側可收合「卡片詳細預覽抽屜」（預設隱藏，點擊任意卡片時彈出，如圖 3）
        self._card_drawer_open = False
        self.left_card_drawer = tk.Frame(
            self.right_board,
            bg="#161b28",
            bd=3,
            relief=tk.RIDGE,
            highlightbackground="#4cc9f0",
            highlightcolor="#4cc9f0",
            highlightthickness=2,
        )
        drawer_hdr = tk.Frame(self.left_card_drawer, bg="#10141f", padx=10, pady=6)
        drawer_hdr.pack(fill=tk.X)
        tk.Label(
            drawer_hdr,
            text="🃏 【卡片詳細資訊】",
            bg="#10141f",
            fg="#ffd166",
            font=(ff, 13, "bold"),
        ).pack(side=tk.LEFT)
        tk.Button(
            drawer_hdr,
            text="◀ 收合",
            bg="#e63946",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=10,
            pady=1,
            cursor="hand2",
            command=self.hide_card_drawer,
        ).pack(side=tk.RIGHT)

        self.lbl_card_title = tk.Label(
            self.left_card_drawer,
            text="點擊任意卡片檢視詳細效果",
            bg="#161b28",
            fg="#ffffff",
            font=(ff, 14, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=400,
            padx=12,
            pady=6,
        )
        self.lbl_card_title.pack(fill=tk.X)

        top_card_row = tk.Frame(self.left_card_drawer, bg="#1d2334", padx=10, pady=8, bd=1, relief=tk.SOLID)
        top_card_row.pack(fill=tk.X, padx=10, pady=4)

        self.lbl_card_img = tk.Label(top_card_row, bg="#111218", width=170, height=238)
        self.lbl_card_img.pack(side=tk.LEFT, padx=(2, 10))

        self.lbl_card_stats = tk.Label(
            top_card_row,
            text="",
            bg="#1d2334",
            fg="#8ecae6",
            font=(ff, 12, "bold"),
            anchor="nw",
            justify=tk.LEFT,
            wraplength=205,
        )
        self.lbl_card_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            self.left_card_drawer,
            text="【卡片效果全文（大字體清晰版）】",
            bg="#161b28",
            fg="#06d6a0",
            font=(ff, 11, "bold"),
            anchor="w",
            padx=12,
        ).pack(fill=tk.X, pady=(6, 2))

        self.txt_card_effect = scrolledtext.ScrolledText(
            self.left_card_drawer,
            bg="#0f131d",
            fg="#f1faee",
            font=(ff, eff_fs),
            wrap=tk.WORD,
            bd=1,
            relief=tk.SOLID,
            padx=10,
            pady=8,
        )
        self.txt_card_effect.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.txt_card_effect.config(state=tk.DISABLED)

        # 7. 《Master Duel》右側可收合「即時戰況紀錄抽屜」（預設隱藏，點擊右下角『📋 戰況紀錄』彈出，如圖 4）
        self._log_drawer_open = False
        self.right_log_drawer = tk.Frame(
            self.right_board,
            bg="#141926",
            bd=3,
            relief=tk.RIDGE,
            highlightbackground="#06d6a0",
            highlightcolor="#06d6a0",
            highlightthickness=2,
        )
        log_hdr = tk.Frame(self.right_log_drawer, bg="#0e121c", padx=10, pady=6)
        log_hdr.pack(fill=tk.X)
        tk.Label(
            log_hdr,
            text="📋 【即時戰況紀錄】",
            bg="#0e121c",
            fg="#06d6a0",
            font=(ff, 13, "bold"),
        ).pack(side=tk.LEFT)
        tk.Button(
            log_hdr,
            text="收合 ▶",
            bg="#e63946",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=10,
            pady=1,
            cursor="hand2",
            command=self.hide_log_drawer,
        ).pack(side=tk.RIGHT)

        self.txt_log = scrolledtext.ScrolledText(
            self.right_log_drawer,
            bg="#0b0e17",
            fg="#e9ecef",
            font=(ff, max(12, eff_fs - 1)),
            wrap=tk.WORD,
            padx=10,
            pady=8,
            bd=0,
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 8. 畫面中央內嵌互動面板與暫時隱藏看場地浮動列、翻牌動畫橫幅
        self.center_overlay = tk.Frame(
            self.right_board, bg="#1e2230", bd=3, relief=tk.RIDGE
        )
        self._overlay_is_waiting = False
        self._overlay_temporarily_hidden = False
        self.peek_board_bar = tk.Frame(
            self.right_board, bg="#ffd166", bd=3, relief=tk.RAISED, padx=14, pady=6
        )
        tk.Label(
            self.peek_board_bar,
            text="👁️ 目前正在檢視場地狀態（可點擊舞台/手牌彈出詳情預覽效果）",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT, padx=(4, 12))
        tk.Button(
            self.peek_board_bar,
            text="🔙 返回剛才的效果視窗（繼續操作）",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=14,
            pady=3,
            command=self._restore_overlay_from_peek,
        ).pack(side=tk.LEFT, padx=4)

        self.flip_anim_frame = tk.Frame(
            self.right_board, bg="#151928", bd=4, relief=tk.RIDGE
        )
        self._flip_anim_after_id = None

        # 點擊戰場上任意空白區域即可一鍵自動收回左側卡片詳情抽屜、右側戰況紀錄抽屜與角色頭頂浮動鈕
        self.bind_all("<ButtonPress-1>", self._on_any_board_click, add="+")
        # 全域滑鼠移動偵測：只要滑鼠離開手牌畫布，立即解除手牌懸停放大狀態，徹底防止手牌卡在放大狀態！
        self.bind_all("<Motion>", self._on_global_motion_check, add="+")

    def _on_global_motion_check(self, event):
        if not self.winfo_exists() or self.game_over:
            return
        if self.hovered_hand_idx is not None:
            w = getattr(event, "widget", None)
            if w != getattr(self, "hand_canvas", None) and not self._drag_state.get("dragging"):
                self.hovered_hand_idx = None
                self.render_hand_dock()

    def _on_clock_zone_motion(self, event, owner: PlayerState):
        if not owner.clock:
            return
        n = len(owner.clock)
        cw = 64
        avail_w = max(1, 216 - cw - 12)
        step_x = 0 if n <= 1 else min(44, avail_w // max(1, n - 1))
        mx = event.x
        for i in range(n - 1, -1, -1):
            ox = 6 + i * step_x
            if ox <= mx <= ox + cw + 6:
                self.inspect_card(owner.clock[i], owner, None, open_drawer=False)
                break

    def _is_descendant_of(self, widget, container) -> bool:
        curr = widget
        while curr is not None:
            if curr == container:
                return True
            curr = getattr(curr, "master", None)
        return False

    def _on_any_board_click(self, event):
        if not self.winfo_exists() or self.game_over:
            return
        w = getattr(event, "widget", None)
        if w is None or not self._is_descendant_of(w, self):
            return
        # 若點擊在左側抽屜、右側抽屜、角色頭頂浮動列或切換鈕本身，不自動關閉該面板
        if hasattr(self, "left_card_drawer") and self._is_descendant_of(w, self.left_card_drawer):
            return
        if hasattr(self, "right_log_drawer") and self._is_descendant_of(w, self.right_log_drawer):
            return
        if hasattr(self, "stage_floating_bar") and self._is_descendant_of(w, self.stage_floating_bar):
            return
        if w in (
            getattr(self, "btn_toggle_card_drawer", None),
            getattr(self, "btn_toggle_log_drawer", None),
        ):
            return

        # 點擊手牌畫布空白處：立即收回左側抽屜與場上浮動鈕
        if w == getattr(self, "hand_canvas", None):
            hit = self._hit_test_hand_dock(event.x, event.y)
            if hit is None:
                if getattr(self, "_card_drawer_open", False):
                    self.hide_card_drawer()
                if getattr(self, "_log_drawer_open", False):
                    self.hide_log_drawer()
                if self.selected_stage_idx is not None or self.selected_hand_idx is not None:
                    self.selected_stage_idx = None
                    self.selected_hand_idx = None
                    if hasattr(self, "stage_floating_bar"):
                        self.stage_floating_bar.place_forget()
                    self.update_ui()
            return

        # 點擊場上空的舞台格子按鈕（且非正在選格子目標或準備從手牌出牌）視為點擊空白處
        if w in getattr(self, "btn_p_stage", []):
            s_idx = self.btn_p_stage.index(w)
            if (
                self.player.stage[s_idx] is None
                and getattr(self, "_field_slot_select_state", None) is None
                and self.selected_hand_idx is None
            ):
                if getattr(self, "_card_drawer_open", False):
                    self.hide_card_drawer()
                if getattr(self, "_log_drawer_open", False):
                    self.hide_log_drawer()
            return
        if w in getattr(self, "btn_ai_stage", []):
            s_idx = self.btn_ai_stage.index(w)
            if (
                self.ai.stage[s_idx] is None
                and getattr(self, "_field_slot_select_state", None) is None
            ):
                if getattr(self, "_card_drawer_open", False):
                    self.hide_card_drawer()
                if getattr(self, "_log_drawer_open", False):
                    self.hide_log_drawer()
            return

        # 若點擊其他按鈕或捲軸，交由該按鈕自身指令處理
        w_cls = w.winfo_class()
        if w_cls in ("Button", "TButton", "Scrollbar", "Scale", "Entry"):
            return
        # 若點擊在彈窗中的卡圖 Label (cursor 為 hand2 或 fleur)，交由該卡圖處理
        if w_cls == "Label" and str(w.cget("cursor")) in ("hand2", "fleur"):
            return

        # 點擊任何背景 Frame / LabelFrame / Canvas / 空白處：立即收回左側詳情抽屜、右側戰報抽屜與頭頂浮動鈕！
        need_refresh = False
        if getattr(self, "_card_drawer_open", False):
            self.hide_card_drawer()
        if getattr(self, "_log_drawer_open", False):
            self.hide_log_drawer()
        if self.selected_stage_idx is not None:
            self.selected_stage_idx = None
            if hasattr(self, "stage_floating_bar"):
                self.stage_floating_bar.place_forget()
            need_refresh = True
        if need_refresh:
            self.update_ui()

    def show_card_drawer(self):
        if not hasattr(self, "left_card_drawer") or not self.left_card_drawer.winfo_exists():
            return
        self._card_drawer_open = True
        self.left_card_drawer.place(x=8, rely=0.06, width=435, relheight=0.78)
        self.left_card_drawer.lift()
        if hasattr(self, "btn_toggle_card_drawer") and self.btn_toggle_card_drawer.winfo_exists():
            self.btn_toggle_card_drawer.config(bg="#ffd166", fg="#000000", text="🃏 隱藏詳情")

    def hide_card_drawer(self):
        self._card_drawer_open = False
        if hasattr(self, "left_card_drawer") and self.left_card_drawer.winfo_exists():
            self.left_card_drawer.place_forget()
        if hasattr(self, "btn_toggle_card_drawer") and self.btn_toggle_card_drawer.winfo_exists():
            self.btn_toggle_card_drawer.config(bg="#1d3557", fg="#4cc9f0", text="🃏 卡片詳情")

    def toggle_card_drawer(self):
        if getattr(self, "_card_drawer_open", False):
            self.hide_card_drawer()
        else:
            self.show_card_drawer()

    def show_log_drawer(self):
        if not hasattr(self, "right_log_drawer") or not self.right_log_drawer.winfo_exists():
            return
        self._log_drawer_open = True
        self.right_log_drawer.place(relx=1.0, x=-8, rely=0.08, anchor="ne", width=410, relheight=0.76)
        self.right_log_drawer.lift()
        self.txt_log.see(tk.END)
        if hasattr(self, "btn_toggle_log_drawer") and self.btn_toggle_log_drawer.winfo_exists():
            self.btn_toggle_log_drawer.config(bg="#ffd166", fg="#000000", text="📋 隱藏紀錄")

    def hide_log_drawer(self):
        self._log_drawer_open = False
        if hasattr(self, "right_log_drawer") and self.right_log_drawer.winfo_exists():
            self.right_log_drawer.place_forget()
        if hasattr(self, "btn_toggle_log_drawer") and self.btn_toggle_log_drawer.winfo_exists():
            self.btn_toggle_log_drawer.config(bg="#1d3557", fg="#06d6a0", text="📋 戰況紀錄")

    def toggle_log_drawer(self):
        if getattr(self, "_log_drawer_open", False):
            self.hide_log_drawer()
        else:
            self.show_log_drawer()

    def render_ai_hand_fan(self):
        """於畫面頂部正中央繪製放大版《Master Duel》風格對手扇形覆蓋手牌 (使用對手卡套卡背)"""
        if not hasattr(self, "ai_hand_canvas") or not self.ai_hand_canvas.winfo_exists():
            return
        self.ai_hand_canvas.delete("all")
        self._ai_hand_photo_refs = []
        cw = max(self.ai_hand_canvas.winfo_width(), 560)
        ch = max(self.ai_hand_canvas.winfo_height(), 70)
        n = len(self.ai.hand)
        if n <= 0:
            self.ai_hand_canvas.create_text(
                cw // 2, ch // 2, text="對手手牌：0 張", fill="#adb5bd", font=("Microsoft JhengHei", 11, "bold")
            )
            return
        step_x = min(40, max(22, int(340 / max(1, n))))
        for idx in range(n):
            rel = idx - (n - 1) / 2.0
            cx_i = int(cw // 2 + rel * step_x)
            cy_i = int(20 + min(10, (rel ** 2) * 0.9))
            ang = int(max(-10, min(10, round((rel * 2.2) / 2.0) * 2)))
            s_tk = self.img_mgr.get_ai_hand_sleeve_visual(
                54,
                76,
                angle_deg=ang,
                sleeve_style=getattr(self, "opp_sleeve_style", "WS_DEFAULT"),
                custom_path=getattr(self, "opp_sleeve_custom", ""),
            )
            self._ai_hand_photo_refs.append(s_tk)
            self.ai_hand_canvas.create_image(cx_i, cy_i, image=s_tk, anchor="center")
        self.ai_hand_canvas.create_rectangle(
            cw // 2 - 74, ch - 22, cw // 2 + 74, ch - 2, fill="#1a121b", outline="#ff758f", width=1
        )
        self.ai_hand_canvas.create_text(
            cw // 2, ch - 12, text=f"對手手牌：{n} 張", fill="#ffd166", font=("Microsoft JhengHei", 10, "bold")
        )

    def on_exit_to_menu(self):
        self.game_over = True
        self.overlay_var.set(1)
        if self.net_node:
            self.net_node.close()
        self.app.show_main_menu()

    def _on_hand_mousewheel(self, event):
        if event.delta:
            step = -1 if event.delta > 0 else 1
            self.hand_canvas.xview_scroll(step * 2, "units")

    # ------------------------------------------
    # 任務 1：實裝遊戲結束全畫面粒子動畫 (VICTORY / DEFEAT)
    # ------------------------------------------
    def show_game_over_animation(self, is_victory: bool, reason_text: str):
        self.game_over = True
        self.overlay_var.set(1)
        if self.center_overlay.winfo_exists():
            self.center_overlay.place_forget()

        if self.end_anim_canvas and self.end_anim_canvas.winfo_exists():
            self.end_anim_canvas.destroy()

        self.end_anim_canvas = tk.Canvas(
            self,
            bg="#0e1017" if is_victory else "#1a090d",
            highlightthickness=0,
        )
        self.end_anim_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self.update_idletasks()

        w = max(self.winfo_width(), 1280)
        h = max(self.winfo_height(), 800)

        self.particles = []
        if is_victory:
            palette = ["#ffd166", "#ffb703", "#06d6a0", "#ffffff", "#4cc9f0", "#f4a261"]
            for _ in range(95):
                self.particles.append({
                    "x": random.uniform(0, w),
                    "y": random.uniform(-h, 0),
                    "vx": random.uniform(-2.2, 2.2),
                    "vy": random.uniform(2.8, 6.5),
                    "size": random.randint(6, 14),
                    "color": random.choice(palette),
                    "shape": "confetti",
                })
        else:
            palette = ["#e63946", "#9d0208", "#6a040f", "#370617", "#adb5bd"]
            for _ in range(75):
                self.particles.append({
                    "x": random.uniform(0, w),
                    "y": random.uniform(0, h),
                    "vx": random.uniform(-1.0, 1.0),
                    "vy": random.uniform(1.2, 3.6),
                    "size": random.randint(4, 10),
                    "color": random.choice(palette),
                    "shape": "ash",
                })

        banner_frame = tk.Frame(
            self.end_anim_canvas,
            bg="#181c28" if is_victory else "#240e14",
            bd=4,
            relief=tk.RIDGE,
            padx=55,
            pady=38,
        )
        banner_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_str = "🏆 V I C T O R Y 🏆" if is_victory else "💀 D E F E A T 💀"
        title_fg = "#ffd166" if is_victory else "#ff4d6d"

        tk.Label(
            banner_frame,
            text=title_str,
            bg=banner_frame["bg"],
            fg=title_fg,
            font=("Microsoft JhengHei", 34, "bold"),
        ).pack(pady=(0, 14))

        tk.Label(
            banner_frame,
            text=reason_text,
            bg=banner_frame["bg"],
            fg="#f1faee",
            font=("Microsoft JhengHei", 15, "bold"),
            justify=tk.CENTER,
        ).pack(pady=(0, 26))

        btn_row = tk.Frame(banner_frame, bg=banner_frame["bg"])
        btn_row.pack()

        tk.Button(
            btn_row,
            text="🔄 再戰一局",
            bg="#06d6a0",
            fg="#000000",
            font=("Microsoft JhengHei", 14, "bold"),
            width=14,
            height=2,
            command=self._restart_match,
        ).pack(side=tk.LEFT, padx=14)

        tk.Button(
            btn_row,
            text="🏠 返回主選單",
            bg="#118ab2",
            fg="#ffffff",
            font=("Microsoft JhengHei", 14, "bold"),
            width=14,
            height=2,
            command=self.on_exit_to_menu,
        ).pack(side=tk.LEFT, padx=14)

        if not is_victory:
            self.end_anim_canvas.create_line(
                0, h * 0.2, w * 0.35, h * 0.45, w * 0.28, h * 0.75, w * 0.6, h,
                fill="#590d22", width=3, tags="crack"
            )
            self.end_anim_canvas.create_line(
                w, h * 0.15, w * 0.72, h * 0.4, w * 0.8, h * 0.68, w * 0.45, h,
                fill="#800f2f", width=3, tags="crack"
            )
            self.end_anim_canvas.create_line(
                w * 0.2, 0, w * 0.48, h * 0.32, w * 0.42, h * 0.62, w * 0.55, h,
                fill="#6a040f", width=2, tags="crack"
            )

        for p in self.particles:
            s = p["size"]
            if p["shape"] == "confetti":
                p["cid"] = self.end_anim_canvas.create_rectangle(
                    p["x"], p["y"], p["x"] + s, p["y"] + s * 0.6,
                    fill=p["color"], outline="", tags="particle"
                )
            else:
                p["cid"] = self.end_anim_canvas.create_oval(
                    p["x"], p["y"], p["x"] + s, p["y"] + s,
                    fill=p["color"], outline="", tags="particle"
                )

        self._animate_end_particles(is_victory)

    def _animate_end_particles(self, is_victory: bool):
        if not self.end_anim_canvas or not self.end_anim_canvas.winfo_exists():
            return
        w = max(self.end_anim_canvas.winfo_width(), 1280)
        h = max(self.end_anim_canvas.winfo_height(), 800)

        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] > h + 20:
                p["y"] = -15
                p["x"] = random.uniform(0, w)
            if p["x"] < -20:
                p["x"] = w + 10
            elif p["x"] > w + 20:
                p["x"] = -10

            s = p["size"]
            cid = p.get("cid")
            if cid:
                if p["shape"] == "confetti":
                    self.end_anim_canvas.coords(cid, p["x"], p["y"], p["x"] + s, p["y"] + s * 0.6)
                else:
                    self.end_anim_canvas.coords(cid, p["x"], p["y"], p["x"] + s, p["y"] + s)

        self.root.after(33, lambda: self._animate_end_particles(is_victory))

    def _restart_match(self):
        if self.net_node:
            self.net_node.close()
        self.app.start_single_player()

    # ------------------------------------------
    # 畫面中央內嵌互動面板引擎
    # ------------------------------------------
    def _hide_overlay_to_peek_board(self):
        if not self._overlay_is_waiting or self.game_over:
            return
        self._overlay_temporarily_hidden = True
        if self.center_overlay.winfo_exists():
            self.center_overlay.place_forget()
        if self.peek_board_bar.winfo_exists():
            self.peek_board_bar.place(relx=0.5, rely=0.02, anchor="n")
            self.peek_board_bar.lift()

    def _place_center_overlay_by_geom(self):
        geom = getattr(self, "_last_overlay_geom", None)
        if geom and "x" in geom and "y" in geom:
            self.center_overlay.place(
                x=geom["x"], y=geom["y"], width=geom.get("width", 540), height=geom.get("height", 205)
            )
        elif geom:
            self.center_overlay.place(
                relx=geom.get("relx", 0.5),
                rely=geom.get("rely", 0.47),
                anchor="center",
                width=geom.get("width", 840),
                height=geom.get("height", 560),
            )
        else:
            self.center_overlay.place(relx=0.5, rely=0.47, anchor="center", width=840, height=560)
        self.center_overlay.lift()

    def _restore_overlay_from_peek(self):
        self._overlay_temporarily_hidden = False
        if self.peek_board_bar.winfo_exists():
            self.peek_board_bar.place_forget()
        if self._overlay_is_waiting and self.center_overlay.winfo_exists():
            self._place_center_overlay_by_geom()

    def _show_overlay_and_wait(self, build_fn, custom_place=None):
        if self.game_over:
            return
        self.selected_stage_idx = None
        if self.hovered_hand_idx is not None:
            self.hovered_hand_idx = None
            self.render_hand_dock()
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()
        self._overlay_is_waiting = True
        self._overlay_temporarily_hidden = False
        self._last_overlay_geom = custom_place
        if hasattr(self, "peek_board_bar") and self.peek_board_bar.winfo_exists():
            self.peek_board_bar.place_forget()
        self.selected_stage_idx = None
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()
        for w in self.center_overlay.winfo_children():
            w.destroy()

        peek_top_bar = tk.Frame(self.center_overlay, bg="#141824", pady=3, padx=8)
        peek_top_bar.pack(side=tk.TOP, fill=tk.X)
        tk.Label(
            peek_top_bar,
            text="💡 可隨時點擊右側按鈕暫時隱藏視窗檢視場地",
            bg="#141824",
            fg="#8ecae6",
            font=("Microsoft JhengHei", 9),
        ).pack(side=tk.LEFT, padx=4)
        tk.Button(
            peek_top_bar,
            text="👁️ 隱藏看場地",
            bg="#ffd166",
            fg="#000000",
            font=("Microsoft JhengHei", 9, "bold"),
            padx=10,
            pady=1,
            command=self._hide_overlay_to_peek_board,
        ).pack(side=tk.RIGHT, padx=4)

        build_fn(self.center_overlay)
        self._place_center_overlay_by_geom()
        self.overlay_var.set(0)
        self.root.wait_variable(self.overlay_var)
        self._overlay_is_waiting = False
        self._overlay_temporarily_hidden = False
        if hasattr(self, "peek_board_bar") and self.peek_board_bar.winfo_exists():
            self.peek_board_bar.place_forget()
        if self.center_overlay.winfo_exists():
            self.center_overlay.place_forget()

    def _close_overlay(self):
        self._overlay_is_waiting = False
        self._overlay_temporarily_hidden = False
        if hasattr(self, "peek_board_bar") and self.peek_board_bar.winfo_exists():
            self.peek_board_bar.place_forget()
        self.overlay_var.set(1)

    def show_card_flip_banner(
        self,
        owner: PlayerState,
        cards_flipped: list,
        banner_title: str,
        shout_text: str = "",
        shout_bg: str = "#ffd166",
        shout_fg: str = "#000000",
        duration_ms: int = 1550,
    ):
        """非阻塞式牌庫翻牌小動畫：從牌庫翻開卡片並彈出『+1魂傷！』或『傷害取消！』醒目標語"""
        if not self.winfo_exists() or self.game_over or not cards_flipped:
            return
        if not hasattr(self, "flip_anim_frame") or not self.flip_anim_frame.winfo_exists():
            return

        if self._flip_anim_after_id:
            try:
                self.root.after_cancel(self._flip_anim_after_id)
            except Exception:
                pass
            self._flip_anim_after_id = None

        for w in self.flip_anim_frame.winfo_children():
            w.destroy()

        border_col = shout_bg if shout_text else "#4cc9f0"
        self.flip_anim_frame.config(bg="#151928", highlightbackground=border_col, highlightthickness=3)

        header_row = tk.Frame(self.flip_anim_frame, bg="#151928")
        header_row.pack(fill=tk.X, padx=14, pady=(8, 4))

        deck_rem = len(owner.deck)
        tk.Label(
            header_row,
            text=f"🎴 {banner_title} （{owner.name} 牌庫剩餘 {deck_rem} 張）",
            bg="#151928",
            fg="#8ecae6",
            font=("Microsoft JhengHei", 12, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            header_row,
            text="✖",
            bg="#2b3044",
            fg="#ffffff",
            font=("Microsoft JhengHei", 9, "bold"),
            padx=6,
            command=lambda: self.flip_anim_frame.place_forget(),
        ).pack(side=tk.RIGHT)

        if shout_text:
            shout_lbl = tk.Label(
                self.flip_anim_frame,
                text=shout_text,
                bg=shout_bg,
                fg=shout_fg,
                font=("Microsoft JhengHei", 18, "bold"),
                padx=22,
                pady=6,
                relief=tk.RAISED,
                bd=3,
            )
            shout_lbl.pack(fill=tk.X, padx=16, pady=(2, 6))

        body_row = tk.Frame(self.flip_anim_frame, bg="#151928", padx=12, pady=6)
        body_row.pack()

        # 左側顯示目前牌庫厚度圖示 + 翻開箭頭
        deck_box = tk.Frame(body_row, bg="#151928")
        deck_box.pack(side=tk.LEFT, padx=(4, 10))
        is_opp_d = owner == self.ai
        d_img = self.img_mgr.get_deck_stack_visual(
            deck_rem,
            "牌庫",
            68,
            94,
            bg_color="#1c2536",
            sleeve_style=getattr(self, "opp_sleeve_style", "WS_DEFAULT") if is_opp_d else getattr(self, "player_sleeve_style", "WS_DEFAULT"),
            custom_path=getattr(self, "opp_sleeve_custom", "") if is_opp_d else getattr(self, "player_sleeve_custom", ""),
        )
        lbl_d = tk.Label(deck_box, image=d_img, bg="#151928")
        lbl_d.image = d_img
        lbl_d.pack()
        tk.Label(
            deck_box,
            text=f"牌堆厚度:{deck_rem}張",
            bg="#151928",
            fg="#adb5bd",
            font=("Microsoft JhengHei", 9, "bold"),
        ).pack()

        tk.Label(
            body_row,
            text="翻開 ➔",
            bg="#151928",
            fg="#ffd166",
            font=("Microsoft JhengHei", 14, "bold"),
        ).pack(side=tk.LEFT, padx=6)

        # 右側逐張展示翻出的卡片
        show_cards = cards_flipped[:5]
        for idx, c in enumerate(show_cards):
            is_cx = c.type == "CX"
            c_box = tk.Frame(
                body_row,
                bg="#590d22" if is_cx else "#23293d",
                bd=2,
                relief=tk.SOLID,
                padx=6,
                pady=4,
            )
            c_box.pack(side=tk.LEFT, padx=5)
            c_img = self.img_mgr.get_card_visual(getattr(c, "skin_id", c.id), 78, 108, is_selected=is_cx)
            l_img = tk.Label(c_box, image=c_img, bg="#141620")
            l_img.image = c_img
            l_img.pack()
            trig_tag = f"｜標記:{get_trigger_zh(c.trigger)}" if c.trigger != "NONE" else ""
            tk.Label(
                c_box,
                text=f"第{idx + 1}張:{c.name[:6]}\nLv.{0 if is_cx else c.base_level}{trig_tag}",
                bg=c_box["bg"],
                fg="#ffd166" if is_cx else "#ffffff",
                font=("Microsoft JhengHei", 9, "bold"),
            ).pack(pady=(2, 0))

        self.flip_anim_frame.place(relx=0.5, rely=0.47, anchor="center")
        self.flip_anim_frame.lift()
        if self.center_overlay.winfo_ismapped():
            self.center_overlay.lift()
        self.update_idletasks()

        def _auto_hide():
            self._flip_anim_after_id = None
            if hasattr(self, "flip_anim_frame") and self.flip_anim_frame.winfo_exists():
                self.flip_anim_frame.place_forget()

        self._flip_anim_after_id = self.root.after(duration_ms, _auto_hide)

    def _wait_ms_nonblocking(self, ms: int):
        """非阻塞式等待指定毫秒數，保持 Tkinter 視窗與動畫流暢回應"""
        if self.game_over or not self.winfo_exists():
            return
        wait_v = tk.IntVar(value=0)
        self.root.after(ms, lambda: wait_v.set(1))
        self.root.wait_variable(wait_v)

    def run_interactive_card_flip_sequence(
        self,
        deck_owner: PlayerState,
        clicker_is_ai: bool,
        banner_title: str,
        step_cards_info: list,
        final_summary_text: str,
        final_summary_bg: str = "#ffd166",
        final_summary_fg: str = "#000000",
        is_trigger_check: bool = False,
    ):
        """
        互動式牌組翻牌演出：
        - 真人玩家 (clicker_is_ai=False)：點擊畫面上的牌庫頂或按鈕逐張翻開卡片，確認是否有標記或名場面，翻完後點擊確認完成結算。
        - AI 對手 (clicker_is_ai=True)：自動逐張翻開，每張牌停留 1.5 秒 (1500ms) 再翻下一張，判定結束後停留 2.5 秒 (2500ms)。
        """
        if not self.winfo_exists() or self.game_over or not step_cards_info:
            return
        if hasattr(self, "flip_anim_frame") and self.flip_anim_frame.winfo_exists():
            self.flip_anim_frame.place_forget()

        total_steps = len(step_cards_info)
        revealed_Idx = {"n": 1 if clicker_is_ai else 0}
        step_var = tk.IntVar(value=0)

        # 多人連線同步：當我方翻開自己的牌組時，即時同步翻牌畫面給對手觀看
        should_broadcast_flip = (
            self.is_lan
            and self.net_node is not None
            and self.net_node.connected
            and deck_owner == self.player
        )
        if should_broadcast_flip:
            serial_steps = []
            for s_info in step_cards_info:
                sc = s_info["card"]
                serial_steps.append({
                    "cid": getattr(sc, "skin_id", sc.id),
                    "name": sc.name,
                    "type": sc.type,
                    "base_level": sc.base_level,
                    "trigger": getattr(sc, "trigger", "NONE"),
                    "badge": s_info.get("badge", ""),
                    "step_shout": s_info.get("step_shout", ""),
                    "step_bg": s_info.get("step_bg", "#2b3044"),
                    "step_fg": s_info.get("step_fg", "#ffffff"),
                    "step_sfx": s_info.get("step_sfx", ""),
                })
            self.net_node.send({
                "type": "FLIP_SEQ_START",
                "banner_title": banner_title,
                "deck_owner_name": deck_owner.name,
                "base_deck_cnt": len(deck_owner.deck),
                "steps": serial_steps,
                "final_summary_text": final_summary_text,
                "final_summary_bg": final_summary_bg,
                "final_summary_fg": final_summary_fg,
                "is_trigger_check": is_trigger_check,
                "sender_state": self.player.to_sync_dict(),
                "receiver_state": self.ai.to_sync_dict(),
            })

        def build(frame):
            tk.Label(
                frame,
                text=f"🎴 {banner_title}",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 16, "bold"),
            ).pack(pady=(10, 4))

            ai_step_sec = float(self.app.settings.get("ai_flip_interval_sec", 2.0))
            ai_end_sec = float(self.app.settings.get("ai_flip_end_pause_sec", 3.5))
            ai_step_ms = int(ai_step_sec * 1000)
            ai_end_ms = int(ai_end_sec * 1000)
            sub_hint = (
                f"🤖 AI 正在從牌庫翻牌判定中（每張間隔 {ai_step_sec:.1f} 秒，判定結束停留 {ai_end_sec:.1f} 秒）..."
                if clicker_is_ai
                else "👆 請點擊下方【牌庫卡堆】或【翻開下一張】按鈕，親自翻開卡片確認標記與名場面！"
            )
            lbl_sub = tk.Label(
                frame,
                text=sub_hint,
                bg="#1e2230",
                fg="#8ecae6",
                font=("Microsoft JhengHei", 11, "bold"),
            )
            lbl_sub.pack(pady=(0, 6))

            # 底部操作按鈕列（優先固定於最下方，絕不裁切）
            bottom_bar = tk.Frame(frame, bg="#1e2230")
            bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 14))

            # 中央醒目跳字橫幅區（顯示 ⚡ +1 魂傷！ 或 🛡️ 傷害取消！）
            shout_banner = tk.Label(
                frame,
                text="準備從牌庫頂翻開卡片...",
                bg="#282c3e",
                fg="#ffffff",
                font=("Microsoft JhengHei", 16, "bold"),
                padx=20,
                pady=8,
                relief=tk.RAISED,
                bd=3,
            )
            shout_banner.pack(fill=tk.X, padx=32, pady=6)

            # 牌庫立體卡堆 ＋ 已翻出卡片展示區
            stage_area = tk.Frame(frame, bg="#141824", bd=2, relief=tk.RIDGE, padx=16, pady=12)
            stage_area.pack(fill=tk.BOTH, expand=True, padx=24, pady=4)

            left_deck_col = tk.Frame(stage_area, bg="#141824")
            left_deck_col.pack(side=tk.LEFT, padx=(8, 16), pady=8)

            right_cards_col = tk.Frame(stage_area, bg="#141824")
            right_cards_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)

            def on_user_click_flip():
                if clicker_is_ai:
                    return
                if revealed_Idx["n"] < total_steps:
                    revealed_Idx["n"] += 1
                    if should_broadcast_flip and self.net_node and self.net_node.connected:
                        self.net_node.send({
                            "type": "FLIP_SEQ_STEP",
                            "cur_n": revealed_Idx["n"],
                        })
                    refresh_view()
                else:
                    if should_broadcast_flip and self.net_node and self.net_node.connected:
                        self.net_node.send({"type": "FLIP_SEQ_END"})
                    step_var.set(1)
                    self._close_overlay()

            def refresh_view():
                for w in left_deck_col.winfo_children():
                    w.destroy()
                for w in right_cards_col.winfo_children():
                    w.destroy()
                for w in bottom_bar.winfo_children():
                    w.destroy()

                cur_n = revealed_Idx["n"]
                rem_to_flip = max(0, total_steps - cur_n)
                shown_deck_cnt = len(deck_owner.deck) + rem_to_flip

                # 左側：可點擊的立體厚度牌庫
                is_opp_d = deck_owner == self.ai
                d_img = self.img_mgr.get_deck_stack_visual(
                    shown_deck_cnt,
                    f"{deck_owner.name}牌庫",
                    88,
                    122,
                    bg_color="#1c2536",
                    sleeve_style=getattr(self, "opp_sleeve_style", "WS_DEFAULT") if is_opp_d else getattr(self, "player_sleeve_style", "WS_DEFAULT"),
                    custom_path=getattr(self, "opp_sleeve_custom", "") if is_opp_d else getattr(self, "player_sleeve_custom", ""),
                )
                deck_btn = tk.Button(
                    left_deck_col,
                    image=d_img,
                    text=f"{deck_owner.name} 牌庫\n剩餘 {shown_deck_cnt} 張"
                    + ("\n👆 點此翻牌！" if (not clicker_is_ai and cur_n < total_steps) else ""),
                    compound=tk.TOP,
                    bg="#1d3557" if (not clicker_is_ai and cur_n < total_steps) else "#1b2234",
                    fg="#ffd166" if (not clicker_is_ai and cur_n < total_steps) else "#ffffff",
                    font=("Microsoft JhengHei", 10, "bold"),
                    padx=8,
                    pady=6,
                    bd=3,
                    relief=tk.RAISED,
                    cursor="hand2" if not clicker_is_ai else "arrow",
                    command=on_user_click_flip,
                )
                deck_btn.image = d_img
                deck_btn.pack()

                tk.Label(
                    left_deck_col,
                    text=f"翻牌進度：{cur_n} / {total_steps} 張",
                    bg="#141824",
                    fg="#8ecae6",
                    font=("Microsoft JhengHei", 10, "bold"),
                ).pack(pady=(6, 0))

                # 更新中央跳字橫幅
                if cur_n == 0:
                    shout_banner.config(
                        text=f"👆 請點擊左側【{deck_owner.name} 牌庫】或下方按鈕翻開第 1 張牌！",
                        bg="#282c3e",
                        fg="#ffd166",
                    )
                elif cur_n < total_steps:
                    latest_info = step_cards_info[cur_n - 1]
                    lc = latest_info["card"]
                    explicit_sfx = latest_info.get("step_sfx", "")
                    if explicit_sfx:
                        self.app.sound_mgr.play_sfx(explicit_sfx)
                    elif lc.type == "CX" or (is_trigger_check and getattr(lc, "trigger", "NONE") != "NONE"):
                        self.app.sound_mgr.play_sfx("sfx_climax")
                    else:
                        self.app.sound_mgr.play_sfx("sfx_draw")
                    shout_banner.config(
                        text=latest_info.get("step_shout", f"翻出：【{lc.name}】"),
                        bg=latest_info.get("step_bg", "#2b3044"),
                        fg=latest_info.get("step_fg", "#ffffff"),
                    )
                    self.inspect_card(lc, deck_owner, None)
                else:
                    latest_info = step_cards_info[cur_n - 1]
                    lc = latest_info["card"]
                    explicit_sfx = latest_info.get("step_sfx", "")
                    if "傷害命中" in final_summary_text:
                        self.app.sound_mgr.play_sfx("sfx_damage")
                    elif "傷害取消" in final_summary_text:
                        self.app.sound_mgr.play_sfx("sfx_climax")
                    elif explicit_sfx:
                        self.app.sound_mgr.play_sfx(explicit_sfx)
                    elif is_trigger_check and (lc.type == "CX" or getattr(lc, "trigger", "NONE") != "NONE"):
                        self.app.sound_mgr.play_sfx("sfx_climax")
                    else:
                        self.app.sound_mgr.play_sfx("sfx_draw")
                    self.inspect_card(lc, deck_owner, None)
                    shout_banner.config(
                        text=final_summary_text,
                        bg=final_summary_bg,
                        fg=final_summary_fg,
                    )

                # 右側：展示目前已翻開的卡片
                if cur_n == 0:
                    unflipped_box = tk.Button(
                        right_cards_col,
                        text="🎴 點擊此處或左側牌庫\n翻開第 1 張卡片",
                        bg="#23293d",
                        fg="#ffd166",
                        font=("Microsoft JhengHei", 14, "bold"),
                        width=28,
                        height=7,
                        bd=3,
                        relief=tk.RIDGE,
                        cursor="hand2",
                        command=on_user_click_flip,
                    )
                    unflipped_box.pack(expand=True, pady=18)
                else:
                    cards_row = tk.Frame(right_cards_col, bg="#141824")
                    cards_row.pack(expand=True, pady=4)
                    for idx in range(cur_n):
                        info = step_cards_info[idx]
                        c_obj = info["card"]
                        is_cx = c_obj.type == "CX"
                        is_latest = idx == cur_n - 1
                        card_frame = tk.Frame(
                            cards_row,
                            bg="#6a040f" if is_cx else ("#1d4e89" if is_latest else "#23293d"),
                            bd=3 if (is_cx or is_latest) else 1,
                            relief=tk.SOLID,
                            padx=6,
                            pady=6,
                        )
                        card_frame.pack(side=tk.LEFT, padx=5)
                        c_img = self.img_mgr.get_card_visual(
                            getattr(c_obj, "skin_id", c_obj.id), 92, 128, is_selected=(is_cx or is_latest)
                        )
                        l_img = tk.Label(card_frame, image=c_img, bg="#141620")
                        l_img.image = c_img
                        l_img.pack()
                        badge_txt = info.get("badge", "")
                        if not badge_txt:
                            if is_cx:
                                badge_txt = "🌟 名場面！"
                            elif c_obj.trigger == "SOUL":
                                badge_txt = "⚡ +1魂傷標記"
                            elif c_obj.trigger != "NONE":
                                badge_txt = f"標記:{get_trigger_zh(c_obj.trigger)}"
                            else:
                                badge_txt = f"Lv.{c_obj.base_level}"
                        tk.Label(
                            card_frame,
                            text=f"第 {idx + 1} 張：{c_obj.name[:7]}\n{badge_txt}",
                            bg=card_frame["bg"],
                            fg="#ffd166" if (is_cx or c_obj.trigger != "NONE") else "#ffffff",
                            font=("Microsoft JhengHei", 9, "bold"),
                            justify=tk.CENTER,
                        ).pack(pady=(4, 0))

                # 底部按鈕區
                if not clicker_is_ai:
                    if cur_n < total_steps:
                        tk.Button(
                            bottom_bar,
                            text=f"🎴 點擊翻開第 {cur_n + 1} / {total_steps} 張牌",
                            bg="#ffd166",
                            fg="#000000",
                            font=("Microsoft JhengHei", 13, "bold"),
                            padx=26,
                            pady=7,
                            cursor="hand2",
                            command=on_user_click_flip,
                        ).pack()
                    else:
                        tk.Button(
                            bottom_bar,
                            text="✔ 確認翻牌判定結果（繼續）",
                            bg="#06d6a0",
                            fg="#000000",
                            font=("Microsoft JhengHei", 13, "bold"),
                            padx=28,
                            pady=7,
                            cursor="hand2",
                            command=on_user_click_flip,
                        ).pack()
                else:
                    status_str = (
                        f"⏳ AI 正在翻開第 {cur_n} / {total_steps} 張牌 (每張停留 {ai_step_sec:.1f} 秒)..."
                        if cur_n < total_steps
                        else f"⏳ AI 翻牌判定結束 (停留 {ai_end_sec:.1f} 秒自動繼續)..."
                    )
                    tk.Label(
                        bottom_bar,
                        text=status_str,
                        bg="#1e2230",
                        fg="#ffd166",
                        font=("Microsoft JhengHei", 12, "bold"),
                    ).pack(side=tk.LEFT, padx=20)
                    tk.Button(
                        bottom_bar,
                        text="⏩ 立即略過等待",
                        bg="#3a3f58",
                        fg="#ffffff",
                        font=("Microsoft JhengHei", 10, "bold"),
                        padx=12,
                        pady=4,
                        command=lambda: [step_var.set(1), self._close_overlay()],
                    ).pack(side=tk.RIGHT, padx=20)

            refresh_view()

            # 若為 AI 翻牌：依設定秒數逐張翻開 (預設 2.0 秒)，全部翻完後依設定秒數停留 (預設 3.5 秒)
            if clicker_is_ai:
                def ai_auto_step():
                    if not self.winfo_exists() or self.game_over or not self._overlay_is_waiting:
                        return
                    if revealed_Idx["n"] < total_steps:
                        revealed_Idx["n"] += 1
                        refresh_view()
                        if revealed_Idx["n"] < total_steps:
                            self.root.after(ai_step_ms, ai_auto_step)
                        else:
                            self.root.after(ai_end_ms, lambda: [step_var.set(1), self._close_overlay()])
                    else:
                        self.root.after(ai_end_ms, lambda: [step_var.set(1), self._close_overlay()])

                if total_steps > 1:
                    self.root.after(ai_step_ms, ai_auto_step)
                else:
                    self.root.after(ai_end_ms, lambda: [step_var.set(1), self._close_overlay()])

        self._show_overlay_and_wait(build)

    def _start_remote_flip_spectator(self, msg: dict):
        """多人連線時，在螢幕中央即時同步展示對手親自翻牌的逐張過程"""
        if not self.winfo_exists() or self.game_over:
            return
        self._remote_flip_state = {
            "banner_title": msg.get("banner_title", "對手翻牌判定"),
            "deck_owner_name": msg.get("deck_owner_name", self.ai.name),
            "base_deck_cnt": int(msg.get("base_deck_cnt", len(self.ai.deck))),
            "steps": msg.get("steps", []),
            "final_summary_text": msg.get("final_summary_text", ""),
            "final_summary_bg": msg.get("final_summary_bg", "#ffd166"),
            "final_summary_fg": msg.get("final_summary_fg", "#000000"),
            "is_trigger_check": bool(msg.get("is_trigger_check", False)),
            "cur_n": 0,
        }
        self._render_remote_flip_spectator()

    def _step_remote_flip_spectator(self, cur_n: int):
        if not self._remote_flip_state or not self.winfo_exists() or self.game_over:
            return
        self._remote_flip_state["cur_n"] = cur_n
        self._render_remote_flip_spectator()

    def _end_remote_flip_spectator(self):
        self._remote_flip_state = None
        if hasattr(self, "flip_anim_frame") and self.flip_anim_frame.winfo_exists():
            self.flip_anim_frame.place_forget()

    def _render_remote_flip_spectator(self):
        st = self._remote_flip_state
        if not st or not hasattr(self, "flip_anim_frame") or not self.flip_anim_frame.winfo_exists():
            return
        for w in self.flip_anim_frame.winfo_children():
            w.destroy()

        steps = st["steps"]
        total_steps = len(steps)
        cur_n = max(0, min(st["cur_n"], total_steps))
        owner_name = st["deck_owner_name"]
        rem_to_flip = max(0, total_steps - cur_n)
        shown_deck_cnt = st["base_deck_cnt"] + rem_to_flip

        self.flip_anim_frame.config(bg="#1e2230", highlightbackground="#ffd166", highlightthickness=3)

        tk.Label(
            self.flip_anim_frame,
            text=f"🎴 {st['banner_title']}",
            bg="#1e2230",
            fg="#ffd166",
            font=("Microsoft JhengHei", 15, "bold"),
        ).pack(pady=(10, 2))

        tk.Label(
            self.flip_anim_frame,
            text=f"👀 正在同步觀看【{owner_name}】親自點擊翻開牌庫（進度：{cur_n} / {total_steps} 張）...",
            bg="#1e2230",
            fg="#8ecae6",
            font=("Microsoft JhengHei", 11, "bold"),
        ).pack(pady=(0, 6))

        if cur_n == 0:
            s_txt = f"⏳ 等待【{owner_name}】點擊牌庫翻開第 1 張卡片..."
            s_bg, s_fg = "#282c3e", "#ffd166"
        elif cur_n < total_steps:
            latest = steps[cur_n - 1]
            s_txt = latest.get("step_shout", f"翻出：【{latest.get('name', '')}】")
            s_bg = latest.get("step_bg", "#2b3044")
            s_fg = latest.get("step_fg", "#ffffff")
            exp_sfx = latest.get("step_sfx", "")
            if exp_sfx:
                self.app.sound_mgr.play_sfx(exp_sfx)
            elif latest.get("type") == "CX" or (st.get("is_trigger_check") and latest.get("trigger", "NONE") != "NONE"):
                self.app.sound_mgr.play_sfx("sfx_climax")
            else:
                self.app.sound_mgr.play_sfx("sfx_draw")
        else:
            latest = steps[cur_n - 1] if steps else {}
            s_txt = st["final_summary_text"] or latest.get("step_shout", "")
            s_bg = st["final_summary_bg"]
            s_fg = st["final_summary_fg"]
            exp_sfx = latest.get("step_sfx", "")
            if "傷害命中" in s_txt:
                self.app.sound_mgr.play_sfx("sfx_damage")
            elif "傷害取消" in s_txt:
                self.app.sound_mgr.play_sfx("sfx_climax")
            elif exp_sfx:
                self.app.sound_mgr.play_sfx(exp_sfx)
            elif st.get("is_trigger_check") and (latest.get("type") == "CX" or latest.get("trigger", "NONE") != "NONE"):
                self.app.sound_mgr.play_sfx("sfx_climax")
            else:
                self.app.sound_mgr.play_sfx("sfx_draw")

        tk.Label(
            self.flip_anim_frame,
            text=s_txt,
            bg=s_bg,
            fg=s_fg,
            font=("Microsoft JhengHei", 15, "bold"),
            padx=18,
            pady=7,
            relief=tk.RAISED,
            bd=3,
        ).pack(fill=tk.X, padx=24, pady=6)

        stage_area = tk.Frame(self.flip_anim_frame, bg="#141824", bd=2, relief=tk.RIDGE, padx=14, pady=10)
        stage_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(4, 12))

        left_col = tk.Frame(stage_area, bg="#141824")
        left_col.pack(side=tk.LEFT, padx=(8, 16), pady=6)
        d_img = self.img_mgr.get_deck_stack_visual(
            shown_deck_cnt,
            f"{owner_name}牌庫",
            84,
            116,
            bg_color="#2b1d28",
            sleeve_style=getattr(self, "opp_sleeve_style", "WS_DEFAULT"),
            custom_path=getattr(self, "opp_sleeve_custom", ""),
        )
        lbl_d = tk.Label(
            left_col,
            image=d_img,
            text=f"{owner_name} 牌庫\n剩餘 {shown_deck_cnt} 張",
            compound=tk.TOP,
            bg="#1b2234",
            fg="#ffffff",
            font=("Microsoft JhengHei", 10, "bold"),
            padx=8,
            pady=6,
            bd=2,
            relief=tk.RIDGE,
        )
        lbl_d.image = d_img
        lbl_d.pack()

        right_col = tk.Frame(stage_area, bg="#141824")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=6)
        if cur_n == 0:
            tk.Label(
                right_col,
                text=f"🎴 等待【{owner_name}】點擊翻開第 1 張卡片...",
                bg="#23293d",
                fg="#ffd166",
                font=("Microsoft JhengHei", 13, "bold"),
                width=30,
                height=6,
                bd=2,
                relief=tk.RIDGE,
            ).pack(expand=True, pady=12)
        else:
            cards_row = tk.Frame(right_col, bg="#141824")
            cards_row.pack(expand=True, pady=4)
            for idx in range(cur_n):
                info = steps[idx]
                cid = info.get("cid", "BFR/S78-063")
                c_name = info.get("name", cid)
                is_cx = info.get("type") == "CX"
                is_latest = idx == cur_n - 1
                card_frame = tk.Frame(
                    cards_row,
                    bg="#6a040f" if is_cx else ("#1d4e89" if is_latest else "#23293d"),
                    bd=3 if (is_cx or is_latest) else 1,
                    relief=tk.SOLID,
                    padx=5,
                    pady=5,
                )
                card_frame.pack(side=tk.LEFT, padx=4)
                c_img = self.img_mgr.get_card_visual(cid, 88, 122, is_selected=(is_cx or is_latest))
                l_img = tk.Label(card_frame, image=c_img, bg="#141620")
                l_img.image = c_img
                l_img.pack()
                badge_txt = info.get("badge", "") or f"Lv.{info.get('base_level', 0)}"
                tk.Label(
                    card_frame,
                    text=f"第 {idx + 1} 張：{c_name[:7]}\n{badge_txt}",
                    bg=card_frame["bg"],
                    fg="#ffd166" if (is_cx or info.get("trigger", "NONE") != "NONE") else "#ffffff",
                    font=("Microsoft JhengHei", 9, "bold"),
                    justify=tk.CENTER,
                ).pack(pady=(3, 0))

        self.flip_anim_frame.place(relx=0.5, rely=0.47, anchor="center", width=800, height=430)
        self.flip_anim_frame.lift()
        self.update_idletasks()

    # ------------------------------------------
    # 任務 2：BFR/S78-083《情報戰 莎莉》玩家手動點擊 0/1/2/3 等級宣言面板
    # ------------------------------------------
    def ask_declare_level_center(self, caller_name: str) -> int:
        res = {"lvl": 0}

        def build(frame):
            tk.Label(
                frame,
                text="🕵️ 【情報戰 莎莉】登場效果：請宣言等級",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 16, "bold"),
            ).pack(pady=(28, 10))

            btn_bar = tk.Frame(frame, bg="#1e2230")
            btn_bar.pack(side=tk.BOTTOM, pady=24)

            btn_colors = ["#06d6a0", "#118ab2", "#f4a261", "#e63946"]
            for lv in [0, 1, 2, 3]:
                tk.Button(
                    btn_bar,
                    text=f"宣言 Lv.{lv}",
                    bg=btn_colors[lv],
                    fg="#000000" if lv in [0, 2] else "#ffffff",
                    font=("Microsoft JhengHei", 13, "bold"),
                    width=11,
                    height=2,
                    command=lambda val=lv: [res.update({"lvl": val}), self._close_overlay()],
                ).pack(side=tk.LEFT, padx=10)

            tk.Label(
                frame,
                text=(
                    f"{caller_name} 打出了【情報戰 莎莉】！\n"
                    "請點擊下方按鈕宣言 0、1、2 或 3 等級。\n"
                    "若對手翻開牌庫頂送入休息室的卡片等級與你宣言相同（CX 視為 0 等），\n"
                    "對手將可抽取最多「宣言數字 + 1」張牌！"
                ),
                bg="#282c3e",
                fg="#ffffff",
                font=("Microsoft JhengHei", 12),
                justify=tk.LEFT,
                padx=24,
                pady=18,
                relief=tk.SOLID,
                bd=1,
            ).pack(fill=tk.X, padx=40, pady=12)

        self._show_overlay_and_wait(build)
        return res["lvl"]

    # ------------------------------------------
    # 任務 3：帶有「最多」字樣的逐步翻牌詢問機制與拖移排序面板
    # ------------------------------------------
    def ask_step_by_step_look_up_to(
        self,
        p: PlayerState,
        max_count: int,
        title: str,
        show_lv1_hint: bool = False,
        allow_skip_all: bool = False,
    ):
        looked = []
        if allow_skip_all and not p.is_ai:
            start_flip = self.ask_yes_no_center(
                title,
                f"是否開始翻看牌組上方的卡片（最多可看 {max_count} 張，亦可隨時停止或選擇不翻）？",
            )
            if not start_flip:
                self.log(f"🛑 {p.name} 選擇不翻看牌組頂卡片。")
                return []

        for step_idx in range(1, max_count + 1):
            c = self.pop_deck_top(p)
            if self.game_over or c is None:
                break
            looked.append(c)
            eff_lvl = 0 if c.type == "CX" else c.base_level
            self.log(
                f"🔍 [{title}] 翻開第 {step_idx}/{max_count} 張：【{c.name}】｜視為 Lv.{eff_lvl}"
            )

            if step_idx >= max_count or not p.deck:
                break

            if p.is_ai:
                if show_lv1_hint and any(x.type != "CX" and x.base_level >= 2 for x in looked):
                    break
                continue

            keep_going = {"val": True}

            def build_step(frame, card_obj=c, cur_step=step_idx, cur_list=list(looked)):
                tk.Label(
                    frame,
                    text=f"🔍 {title} — 逐步看牌 ({cur_step} / {max_count} 張)",
                    bg="#1e2230",
                    fg="#ffd166",
                    font=("Microsoft JhengHei", 15, "bold"),
                ).pack(pady=(12, 4))

                # 底部按鈕列優先固定於面板下方，確保絕不被裁切
                btn_bar = tk.Frame(frame, bg="#1e2230")
                btn_bar.pack(side=tk.BOTTOM, pady=14)

                tk.Button(
                    btn_bar,
                    text=f"👀 繼續翻下一張 (第 {cur_step + 1} 張)",
                    bg="#06d6a0",
                    fg="#000000",
                    font=("Microsoft JhengHei", 12, "bold"),
                    padx=18,
                    pady=6,
                    command=lambda: [keep_going.update({"val": True}), self._close_overlay()],
                ).pack(side=tk.LEFT, padx=12)

                stop_label = "🛑 停止翻牌，進入選牌結算" if show_lv1_hint else "🛑 停止翻牌，進入順序調整"
                tk.Button(
                    btn_bar,
                    text=stop_label,
                    bg="#f4a261",
                    fg="#000000",
                    font=("Microsoft JhengHei", 12, "bold"),
                    padx=18,
                    pady=6,
                    command=lambda: [keep_going.update({"val": False}), self._close_overlay()],
                ).pack(side=tk.LEFT, padx=12)

                self.inspect_card(card_obj, p, None)

                c_img = self.img_mgr.get_card_visual(getattr(card_obj, "skin_id", card_obj.id), 125, 175)
                lbl_img = tk.Label(frame, image=c_img, bg="#141620", bd=2, relief=tk.SOLID)
                lbl_img.image = c_img
                lbl_img.pack(pady=6)

                lv_tag = 0 if card_obj.type == "CX" else card_obj.base_level
                if show_lv1_hint:
                    qual_str = (
                        " — ✔ 符合 Lv.1 以上加手條件"
                        if (card_obj.type != "CX" and card_obj.base_level >= 1)
                        else " — ✖ 未達 Lv.1 (名場面視為 0 等)"
                    )
                    fg_col = "#06d6a0" if (card_obj.type != "CX" and card_obj.base_level >= 1) else "#ffadad"
                else:
                    qual_str = f" ｜ 種類：{get_card_type_zh(card_obj.type)}"
                    fg_col = "#06d6a0"

                tk.Label(
                    frame,
                    text=f"第 {cur_step} 張：【{card_obj.name}】 (視為 Lv.{lv_tag}){qual_str}",
                    bg="#1e2230",
                    fg=fg_col,
                    font=("Microsoft JhengHei", 12, "bold"),
                ).pack(pady=4)

                seen_names = "、".join(x.name for x in cur_list)
                tk.Label(
                    frame,
                    text=f"目前已翻開：{seen_names}",
                    bg="#1e2230",
                    fg="#8ecae6",
                    font=("Microsoft JhengHei", 10),
                    wraplength=680,
                ).pack(pady=4)

            self._show_overlay_and_wait(build_step)
            if not keep_going["val"]:
                self.log(f"🛑 {p.name} 選擇在第 {step_idx} 張停止翻牌。")
                break

        if p.is_ai and looked and not self.game_over:
            ai_steps = [
                {
                    "card": lc,
                    "badge": "🌟 名場面" if lc.type == "CX" else f"Lv.{lc.base_level}",
                    "step_shout": f"🔍 {p.name} 翻看第 {i_l + 1} 張：【{lc.name}】(視為 Lv.{0 if lc.type == 'CX' else lc.base_level})",
                    "step_bg": "#1d3557",
                    "step_fg": "#ffd166",
                    "step_sfx": "sfx_draw",
                }
                for i_l, lc in enumerate(looked)
            ]
            self.run_interactive_card_flip_sequence(
                deck_owner=p,
                clicker_is_ai=True,
                banner_title=f"{p.name} 發動效果翻牌 — {title}",
                step_cards_info=ai_steps,
                final_summary_text=f"🔍 {p.name} 翻看牌組頂 {len(looked)} 張完成！",
                final_summary_bg="#ffd166",
                final_summary_fg="#000000",
            )
        return looked

    def ask_reorder_cards_center(self, p: PlayerState, cards_list: list, title: str) -> list:
        # 視覺化卡圖拖移排序面板：優先將確認鍵固定於底部，徹底修復情報戰莎莉等卡片確認鍵被遮擋問題
        if not cards_list:
            return []
        if p.is_ai:
            return list(cards_list)

        ordered = list(cards_list)
        ord_names = ["第一張", "第二張", "第三張", "第四張"]

        def build(frame):
            tk.Label(
                frame,
                text=f"🔀 {title}",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 15, "bold"),
            ).pack(pady=(10, 2))

            tk.Label(
                frame,
                text="💡 用滑鼠左鍵按住卡圖左右拖移，或點選下方左右移按鈕交換順序（第一張為牌庫最頂端）",
                bg="#1e2230",
                fg="#8ecae6",
                font=("Microsoft JhengHei", 11, "bold"),
            ).pack(pady=(0, 6))

            # 關鍵修正：優先將「確認順序並放回牌庫上方」按鈕固定於面板最底部 (side=tk.BOTTOM)，永不裁切！
            bottom_bar = tk.Frame(frame, bg="#1e2230")
            bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 14))

            tk.Button(
                bottom_bar,
                text="✔ 確認順序並放回牌庫上方",
                bg="#06d6a0",
                fg="#000000",
                font=("Microsoft JhengHei", 13, "bold"),
                padx=28,
                pady=8,
                command=self._close_overlay,
            ).pack()

            slots_container = tk.Frame(frame, bg="#141824", bd=2, relief=tk.RIDGE, padx=18, pady=10)
            slots_container.pack(pady=4)

            slot_frames = []
            drag_info = {"src_idx": None, "ghost": None}

            def refresh_slots():
                for w in slots_container.winfo_children():
                    w.destroy()
                slot_frames.clear()

                for idx, card_obj in enumerate(ordered):
                    pos_label = ord_names[idx] if idx < len(ord_names) else f"第 {idx + 1} 張"
                    sub_tag = "（牌庫最頂）" if idx == 0 else ""

                    col_box = tk.Frame(
                        slots_container,
                        bg="#23283b",
                        bd=2,
                        relief=tk.RAISED,
                        padx=10,
                        pady=6,
                    )
                    col_box.pack(side=tk.LEFT, padx=10)
                    slot_frames.append(col_box)

                    c_img = self.img_mgr.get_card_visual(getattr(card_obj, "skin_id", card_obj.id), 110, 154, is_selected=(idx == 0))
                    lbl_img = tk.Label(
                        col_box,
                        image=c_img,
                        bg="#141620",
                        bd=2,
                        relief=tk.SOLID,
                        cursor="fleur",
                    )
                    lbl_img.image = c_img
                    lbl_img.pack(pady=3)

                    eff_lv = 0 if card_obj.type == "CX" else card_obj.base_level
                    lbl_name = tk.Label(
                        col_box,
                        text=f"{card_obj.name[:9]}\nLv.{eff_lv}｜{get_card_type_zh(card_obj.type)}",
                        bg="#23283b",
                        fg="#ffffff",
                        font=("Microsoft JhengHei", 10, "bold"),
                        justify=tk.CENTER,
                    )
                    lbl_name.pack(pady=2)

                    lbl_ord = tk.Label(
                        col_box,
                        text=f"📌 {pos_label}{sub_tag}",
                        bg="#ffd166" if idx == 0 else "#118ab2",
                        fg="#000000" if idx == 0 else "#ffffff",
                        font=("Microsoft JhengHei", 10, "bold"),
                        padx=8,
                        pady=2,
                    )
                    lbl_ord.pack(fill=tk.X, pady=(3, 3))

                    if len(ordered) > 1:
                        arrow_row = tk.Frame(col_box, bg="#23283b")
                        arrow_row.pack(pady=2)
                        tk.Button(
                            arrow_row,
                            text="◀ 左移",
                            bg="#3a3f58",
                            fg="white",
                            font=("Microsoft JhengHei", 9, "bold"),
                            state=tk.NORMAL if idx > 0 else tk.DISABLED,
                            command=lambda i=idx: swap_positions(i, i - 1),
                        ).pack(side=tk.LEFT, padx=3)
                        tk.Button(
                            arrow_row,
                            text="右移 ▶",
                            bg="#3a3f58",
                            fg="white",
                            font=("Microsoft JhengHei", 9, "bold"),
                            state=tk.NORMAL if idx < len(ordered) - 1 else tk.DISABLED,
                            command=lambda i=idx: swap_positions(i, i + 1),
                        ).pack(side=tk.LEFT, padx=3)

                    for drag_w in (col_box, lbl_img, lbl_name, lbl_ord):
                        drag_w.bind("<ButtonPress-1>", lambda e, i=idx: on_press(e, i))
                        drag_w.bind("<B1-Motion>", on_motion)
                        drag_w.bind("<ButtonRelease-1>", on_release)

            def swap_positions(i, j):
                if 0 <= i < len(ordered) and 0 <= j < len(ordered) and i != j:
                    ordered[i], ordered[j] = ordered[j], ordered[i]
                    refresh_slots()

            def on_press(event, idx):
                drag_info["src_idx"] = idx
                c_obj = ordered[idx]
                self.inspect_card(c_obj, p, None)
                g_img = self.img_mgr.get_card_visual(getattr(c_obj, "skin_id", c_obj.id), 86, 120, is_selected=True)
                ghost = tk.Label(
                    frame,
                    image=g_img,
                    text=c_obj.name[:6],
                    compound=tk.TOP,
                    bg="#ffd166",
                    fg="#000000",
                    font=("Microsoft JhengHei", 9, "bold"),
                    bd=2,
                    relief=tk.SOLID,
                )
                ghost.image = g_img
                drag_info["ghost"] = ghost

            def on_motion(event):
                ghost = drag_info.get("ghost")
                if ghost:
                    rx = event.x_root - frame.winfo_rootx() - 43
                    ry = event.y_root - frame.winfo_rooty() - 60
                    ghost.place(x=rx, y=ry)
                    ghost.lift()

            def on_release(event):
                ghost = drag_info.get("ghost")
                if ghost and ghost.winfo_exists():
                    ghost.destroy()
                drag_info["ghost"] = None
                src_i = drag_info.get("src_idx")
                drag_info["src_idx"] = None
                if src_i is None:
                    return
                xr, yr = event.x_root, event.y_root
                for dst_i, sf in enumerate(slot_frames):
                    if sf.winfo_exists():
                        sx, sy = sf.winfo_rootx(), sf.winfo_rooty()
                        sw, sh = sf.winfo_width(), sf.winfo_height()
                        if sx <= xr <= sx + sw and sy <= yr <= sy + sh:
                            if dst_i != src_i:
                                card_item = ordered.pop(src_i)
                                ordered.insert(dst_i, card_item)
                                refresh_slots()
                            break

            refresh_slots()

        self._show_overlay_and_wait(build)
        order_log = " ➔ ".join(
            f"{ord_names[i]}:{c.name}" for i, c in enumerate(ordered)
        )
        self.log(f"🔀 {p.name} 已調整牌庫頂順序：{order_log}")
        return ordered

    def _generate_ace_flip_setup(self, is_lan_mode: bool = False) -> dict:
        """
        產生『雙方王牌二選一翻牌決定先後手』設定：
        - 兩張覆蓋卡分別為【我方王牌】與【對手王牌】（即使卡號相同，亦以所屬玩家標記區分）
        - 單人對戰 AI：固定由玩家負責翻牌
        - 多人連線對戰：隨機決定其中一人負責翻牌
        - 翻牌者若抽到自己的王牌必定【先攻】，若抽到對方的王牌則必定【後攻】（即抽中誰的王牌就由誰先攻）
        """
        my_ace_cid = getattr(self.player, "ace_cid", None) or self.app.get_series_ace_card_id(self.app.active_series)
        opp_ace_cid = getattr(self.ai, "ace_cid", None) or self.app.get_ai_ace_card_id(self.app.ai_series)
        if my_ace_cid not in CARD_DB:
            my_ace_cid = "BFR/S78-063"
        if opp_ace_cid not in CARD_DB:
            opp_ace_cid = "BFR/S78-063"

        my_card_name = CARD_DB[my_ace_cid]["name"]
        opp_card_name = CARD_DB[opp_ace_cid]["name"]

        slots = [
            {
                "owner_role": "ME",
                "owner_name": self.player.name,
                "cid": my_ace_cid,
                "card_name": my_card_name,
            },
            {
                "owner_role": "OPP",
                "owner_name": self.ai.name,
                "cid": opp_ace_cid,
                "card_name": opp_card_name,
            },
        ]
        random.shuffle(slots)
        flipper_is_me = True if not is_lan_mode else random.choice([True, False])
        return {
            "slots": slots,
            "flipper_is_me": flipper_is_me,
        }

    def ask_ace_card_turn_order_center(
        self, ace_setup: dict, is_lan_mode: bool = False
    ) -> str:
        """
        顯示兩張覆蓋的王牌卡（一張為自己的王牌、一張為對手的王牌）：
        - 單人對戰固定由玩家點擊翻開其中一張；多人連線隨機指定一人點擊翻開
        - 翻到自己的王牌必定先攻，翻到對手的王牌必定後攻（無法手動更改先後手）
        """
        slots = ace_setup.get("slots", [])
        flipper_is_me = bool(ace_setup.get("flipper_is_me", True))
        flipper_name = self.player.name if flipper_is_me else self.ai.name

        state = {
            "picked_idx": None,
            "order": "FIRST",
        }

        def build(frame):
            tk.Label(
                frame,
                text="👑 先後手決定：雙方王牌二選一翻牌（抽中自己王牌必定先攻！）",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 15, "bold"),
            ).pack(pady=(12, 4))

            rule_desc = (
                f"🎯 單人對戰固定由【{self.player.name}】親自從下方兩張覆蓋王牌中選 1 張翻開！\n"
                "（兩張牌分別為你的王牌與對手的王牌：抽到自己的王牌必定【先攻】，抽到對手的王牌則【後攻】）"
                if not is_lan_mode
                else (
                    f"🎯 系統隨機指定由【你 ({self.player.name})】負責翻牌！請從下方兩張覆蓋王牌中點擊 1 張翻開！"
                    if flipper_is_me
                    else f"⏳ 系統隨機指定由對手【{self.ai.name}】負責翻牌，請等待對手點擊翻開覆蓋王牌..."
                )
            )
            lbl_hint = tk.Label(
                frame,
                text=rule_desc,
                bg="#282c3e",
                fg="#06d6a0" if flipper_is_me else "#ffd166",
                font=("Microsoft JhengHei", 11, "bold"),
                padx=16,
                pady=8,
                relief=tk.SOLID,
                bd=1,
            )
            lbl_hint.pack(fill=tk.X, padx=32, pady=4)

            bottom_bar = tk.Frame(frame, bg="#1e2230")
            bottom_bar.pack(side=tk.BOTTOM, pady=(6, 14))

            cards_row = tk.Frame(frame, bg="#1e2230")
            cards_row.pack(expand=True, pady=6)

            def on_pick_slot(idx: int, from_remote: bool = False):
                if state["picked_idx"] is not None:
                    return
                if not from_remote and not flipper_is_me:
                    return
                state["picked_idx"] = idx
                chosen_slot = slots[idx]
                first_is_me = chosen_slot["owner_role"] == "ME"
                state["order"] = "FIRST" if first_is_me else "SECOND"
                self.app.sound_mgr.play_sfx("sfx_climax")

                first_p_name = self.player.name if first_is_me else self.ai.name
                self.log(
                    f"👑 [王牌翻牌決定先後手] {flipper_name} 翻開了【{chosen_slot['owner_name']} 的王牌 — {chosen_slot['card_name']}】"
                    f" ➔ 由【{first_p_name}】固定獲得【先攻】！"
                )
                if is_lan_mode and not from_remote and self.net_node and self.net_node.connected:
                    self.net_node.send({
                        "type": "TURN_ORDER_FLIP_SYNC",
                        "picked_idx": idx,
                    })
                render_cards()

            self._lan_ace_flip_callback = lambda p_idx: on_pick_slot(p_idx, from_remote=True)

            def on_confirm_continue():
                if is_lan_mode and flipper_is_me and self.net_node and self.net_node.connected:
                    self.net_node.send({
                        "type": "TURN_ORDER_CONFIRM_SYNC",
                        "first_is_sender": (state["order"] == "FIRST"),
                    })
                self._close_overlay()

            def render_cards():
                for w in cards_row.winfo_children():
                    w.destroy()
                for w in bottom_bar.winfo_children():
                    w.destroy()

                picked = state["picked_idx"]
                pos_labels = ["左方覆蓋王牌", "右方覆蓋王牌"]

                for i, s_info in enumerate(slots):
                    is_picked = picked == i
                    is_my_ace = s_info["owner_role"] == "ME"

                    if picked is None:
                        # 尚未翻開：顯示精緻卡背與點擊翻牌按鈕
                        box_bg = "#1d3557" if flipper_is_me else "#23293d"
                        c_box = tk.Frame(
                            cards_row,
                            bg=box_bg,
                            bd=3,
                            relief=tk.RAISED,
                            padx=22,
                            pady=12,
                        )
                        c_box.pack(side=tk.LEFT, padx=24)

                        tk.Label(
                            c_box,
                            text=f"🎴 {pos_labels[i]}",
                            bg=box_bg,
                            fg="#ffd166",
                            font=("Microsoft JhengHei", 13, "bold"),
                        ).pack(pady=(0, 6))

                        back_img = self.img_mgr.get_deck_stack_visual(
                            1, "王牌覆蓋卡", 118, 164, bg_color="#141824", sleeve_style="WS_DEFAULT", custom_path=""
                        )
                        btn_card = tk.Button(
                            c_box,
                            image=back_img,
                            text="👆 點擊翻開此張王牌！" if flipper_is_me else "🔒 等待對手翻牌...",
                            compound=tk.TOP,
                            bg="#283655" if flipper_is_me else "#1b2030",
                            fg="#06d6a0" if flipper_is_me else "#adb5bd",
                            font=("Microsoft JhengHei", 11, "bold"),
                            padx=10,
                            pady=6,
                            bd=2,
                            relief=tk.RIDGE,
                            cursor="hand2" if flipper_is_me else "arrow",
                            command=lambda idx=i: on_pick_slot(idx, from_remote=False),
                        )
                        btn_card.image = back_img
                        btn_card.pack()
                    else:
                        # 已翻開：同時揭曉兩張王牌，並高亮標示被抽中的那一張與其所屬玩家！
                        box_bg = (
                            ("#0b4f6c" if is_my_ace else "#6a040f")
                            if is_picked
                            else "#1f2433"
                        )
                        c_box = tk.Frame(
                            cards_row,
                            bg=box_bg,
                            bd=4 if is_picked else 1,
                            relief=tk.SOLID,
                            padx=18,
                            pady=10,
                        )
                        c_box.pack(side=tk.LEFT, padx=20)

                        tag_header = (
                            f"🎯【抽中此張！】{s_info['owner_name']} 的王牌"
                            if is_picked
                            else f"（未抽中）{s_info['owner_name']} 的王牌"
                        )
                        tk.Label(
                            c_box,
                            text=tag_header,
                            bg=box_bg,
                            fg="#ffd166" if is_picked else "#adb5bd",
                            font=("Microsoft JhengHei", 12, "bold"),
                        ).pack(pady=(0, 4))

                        c_img = self.img_mgr.get_card_visual(
                            s_info["cid"], 116, 162, is_selected=is_picked
                        )
                        lbl_img = tk.Label(c_box, image=c_img, bg="#141620")
                        lbl_img.image = c_img
                        lbl_img.pack(pady=4)

                        owner_badge = (
                            f"👑 我方（{self.player.name}）所屬王牌"
                            if is_my_ace
                            else f"🔥 對手（{self.ai.name}）所屬王牌"
                        )
                        tk.Label(
                            c_box,
                            text=f"【{s_info['card_name'][:12]}】\n{owner_badge}",
                            bg=box_bg,
                            fg="#06d6a0" if (is_picked and is_my_ace) else ("#ff758f" if is_picked else "#adb5bd"),
                            font=("Microsoft JhengHei", 11, "bold"),
                            justify=tk.CENTER,
                        ).pack(pady=(4, 0))

                if picked is not None:
                    chosen_slot = slots[picked]
                    first_is_me = chosen_slot["owner_role"] == "ME"
                    if first_is_me:
                        res_txt = (
                            f"🎉 翻出【{self.player.name} 的王牌 — {chosen_slot['card_name']}】！"
                            f"由【{self.player.name}】固定獲得【先攻】！"
                        )
                        res_fg = "#06d6a0"
                    else:
                        res_txt = (
                            f"⚔️ 翻出【{self.ai.name} 的王牌 — {chosen_slot['card_name']}】！"
                            f"由【{self.ai.name}】固定獲得【先攻】（你為後攻）！"
                        )
                        res_fg = "#ffd166"

                    lbl_hint.config(text=res_txt, fg=res_fg, bg="#1d3557" if first_is_me else "#4a2530")

                    if not is_lan_mode or flipper_is_me:
                        tk.Button(
                            bottom_bar,
                            text="✔ 確認先後手結果（進入起手換牌階段）",
                            bg="#06d6a0",
                            fg="#000000",
                            font=("Microsoft JhengHei", 13, "bold"),
                            padx=26,
                            pady=8,
                            cursor="hand2",
                            command=on_confirm_continue,
                        ).pack()
                    else:
                        tk.Label(
                            bottom_bar,
                            text=f"⏳ 已揭曉王牌結果，等待【{self.ai.name}】點擊確認進入換牌階段...",
                            bg="#1e2230",
                            fg="#ffd166",
                            font=("Microsoft JhengHei", 12, "bold"),
                        ).pack(side=tk.LEFT, padx=12)
                        tk.Button(
                            bottom_bar,
                            text="✔ 直接確認進入換牌",
                            bg="#3a3f58",
                            fg="#ffffff",
                            font=("Microsoft JhengHei", 10, "bold"),
                            padx=14,
                            pady=5,
                            command=self._close_overlay,
                        ).pack(side=tk.LEFT, padx=8)

            render_cards()

        self._show_overlay_and_wait(build)
        self._lan_ace_flip_callback = None
        if is_lan_mode and not flipper_is_me and self._lan_turn_order_chosen:
            return self._lan_turn_order_chosen
        return state["order"]

    def ask_mulligan_multi_center(self):
        selected_indices = set()

        def build(frame):
            tk.Label(
                frame,
                text="🔄 起手換牌階段 (可點選多張要換掉的牌，一次替換)",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 14, "bold"),
            ).pack(pady=(12, 4))

            tk.Label(
                frame,
                text="點擊下方卡牌即可切換【保留 / 換掉】狀態（同時可於左側查看卡片效果）",
                bg="#1e2230",
                fg="#8ecae6",
                font=("Microsoft JhengHei", 10, "bold"),
            ).pack(pady=(0, 6))

            cards_box = tk.Frame(frame, bg="#141620", pady=12)
            cards_box.pack(fill=tk.X, padx=16, pady=4)

            btns = []

            def toggle_card(idx):
                self.inspect_card(self.player.hand[idx], self.player, None)
                if idx in selected_indices:
                    selected_indices.remove(idx)
                else:
                    selected_indices.add(idx)
                refresh_buttons()

            def refresh_buttons():
                for i, b in enumerate(btns):
                    c = self.player.hand[i]
                    is_marked = i in selected_indices
                    c_img = self.img_mgr.get_card_visual(
                        getattr(c, "skin_id", c.id), 95, 132, state="STAND", is_selected=is_marked
                    )
                    status_tag = "❌ [換掉]" if is_marked else "✔ [保留]"
                    b.config(
                        image=c_img,
                        text=f"{c.name[:7]}\nLv.{c.base_level} | {status_tag}",
                        bg="#e63946" if is_marked else "#252734",
                    )
                    b.image = c_img

            for idx, c in enumerate(self.player.hand):
                b = tk.Button(
                    cards_box,
                    compound=tk.TOP,
                    fg="white",
                    font=("Microsoft JhengHei", 9, "bold"),
                    width=114,
                    height=176,
                    bd=2,
                    command=lambda i=idx: toggle_card(i),
                )
                b.pack(side=tk.LEFT, padx=6, expand=True)
                btns.append(b)

            refresh_buttons()
            if self.player.hand:
                self.inspect_card(self.player.hand[0], self.player, None)

            btn_bar = tk.Frame(frame, bg="#1e2230")
            btn_bar.pack(side=tk.BOTTOM, pady=12)

            tk.Button(
                btn_bar,
                text="✔ 確認換牌 (替換所有標記紅色的卡片)",
                bg="#06d6a0",
                fg="#000000",
                font=("Microsoft JhengHei", 11, "bold"),
                padx=18,
                pady=6,
                command=self._close_overlay,
            ).pack(side=tk.LEFT, padx=12)

            tk.Button(
                btn_bar,
                text="全部保留不換",
                bg="#118ab2",
                fg="#ffffff",
                font=("Microsoft JhengHei", 11, "bold"),
                padx=18,
                pady=6,
                command=lambda: [selected_indices.clear(), self._close_overlay()],
            ).pack(side=tk.LEFT, padx=12)

        self._show_overlay_and_wait(build)
        return sorted(selected_indices, reverse=True)

    def _find_field_card_and_widget(self, title_or_name: str, prefer_player=None):
        if not title_or_name:
            return (None, None, None, None)
        players = [prefer_player] if prefer_player else [self.player, self.ai]
        for p in players:
            if not p:
                continue
            stage_btns = self.btn_p_stage if p == self.player else self.btn_ai_stage
            for idx, c in enumerate(p.stage):
                if c and (c.name in title_or_name or title_or_name in c.name):
                    return (p, c, stage_btns[idx], f"STAGE_{idx}")
            if p.climax_zone and (p.climax_zone.name in title_or_name or title_or_name in p.climax_zone.name):
                w = self.btn_p_cx if p == self.player else self.btn_ai_cx
                return (p, p.climax_zone, w, "CX")
            for c in reversed(p.memory):
                if c and (c.name in title_or_name or title_or_name in c.name):
                    w = self.btn_p_memory if p == self.player else self.btn_ai_memory
                    return (p, c, w, "MEMORY")
            for c in reversed(p.waiting_room):
                if c and (c.name in title_or_name or title_or_name in c.name):
                    w = self.btn_p_wr if p == self.player else self.btn_ai_wr
                    return (p, c, w, "WR")
        return (None, None, None, None)

    def show_field_effect_cutin(self, p: PlayerState, card: CardInstance, target_widget=None, effect_msg: str = ""):
        """《Master Duel》風格場上發動效果定位演出：直接在發動卡片所在的舞台格子/區域位置跳出金色脈衝與浮動特效卡標"""
        if self.game_over or not self.winfo_exists() or not card:
            return
        if target_widget is None:
            _, _, target_widget, _ = self._find_field_card_and_widget(card.name, prefer_player=p)
        if not target_widget or not target_widget.winfo_exists():
            return
        try:
            self.update_idletasks()
            rx = target_widget.winfo_rootx() - self.right_board.winfo_rootx()
            ry = target_widget.winfo_rooty() - self.right_board.winfo_rooty()
            rw = max(84, target_widget.winfo_width())
            rh = max(110, target_widget.winfo_height())
        except Exception:
            return

        orig_bg = target_widget.cget("bg")
        is_cx_combo = "連動" in effect_msg
        glow_col = "#ff4d6d" if is_cx_combo else "#ffd166"
        try:
            target_widget.config(bg=glow_col)
            self.root.after(650, lambda w=target_widget, bg=orig_bg: w.config(bg=bg) if w.winfo_exists() else None)
        except Exception:
            pass

        banner = tk.Frame(
            self.right_board,
            bg="#141826",
            bd=3,
            relief=tk.RIDGE,
            highlightbackground=glow_col,
            highlightcolor=glow_col,
            highlightthickness=2,
            padx=6,
            pady=4,
        )
        c_img = self.img_mgr.get_card_visual(getattr(card, "skin_id", card.id), 48, 68, is_selected=True)
        lbl_i = tk.Label(banner, image=c_img, bg="#141826")
        lbl_i.image = c_img
        lbl_i.pack(side=tk.LEFT, padx=(0, 6))

        txt_col = tk.Frame(banner, bg="#141826")
        txt_col.pack(side=tk.LEFT)
        tag_hdr = "🔥【CX連動發動】" if is_cx_combo else "⚡【場上效果發動】"
        tk.Label(
            txt_col,
            text=f"{tag_hdr} {card.name}",
            bg="#141826",
            fg=glow_col,
            font=("Microsoft JhengHei", 10, "bold"),
            anchor="w",
        ).pack(fill=tk.X)
        clean_desc = effect_msg.strip()
        if len(clean_desc) > 28:
            clean_desc = clean_desc[:28] + "..."
        tk.Label(
            txt_col,
            text=clean_desc,
            bg="#141826",
            fg="#ffffff",
            font=("Microsoft JhengHei", 9),
            anchor="w",
        ).pack(fill=tk.X)

        board_w = max(860, self.right_board.winfo_width())
        bx = max(8, min(board_w - 310, rx - 35))
        by = max(8, ry - 42 if ry > 80 else ry + rh - 30)
        banner.place(x=bx, y=by)
        banner.lift()
        self._active_field_cutins.append(banner)

        def _cleanup_banner():
            if banner in self._active_field_cutins:
                self._active_field_cutins.remove(banner)
            if banner.winfo_exists():
                banner.destroy()

        self.root.after(1150, _cleanup_banner)

    def ask_yes_no_center(self, title: str, message: str) -> bool:
        """《Master Duel》風格場上發動確認氣泡：直接定位於場上發動效果的卡片旁，按鈕列強制優先固定於底部絕不裁切"""
        ans = {"val": False}
        _, found_card, found_widget, _ = self._find_field_card_and_widget(title, prefer_player=self.player)
        orig_bg = None
        if found_widget and found_widget.winfo_exists():
            try:
                orig_bg = found_widget.cget("bg")
                found_widget.config(bg="#ffd166")
            except Exception:
                pass
        if found_card:
            self.inspect_card(found_card, self.player, None, open_drawer=False)
            self.show_field_effect_cutin(self.player, found_card, found_widget, f"是否發動：{message[:22]}")

        def build(frame):
            # 關鍵修正：優先將底部「是 / 否」按鈕列 pack(side=tk.BOTTOM)，確保無論訊息多長都絕對不會被切掉！
            btn_bar = tk.Frame(frame, bg="#192030")
            btn_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=(4, 10))
            tk.Button(
                btn_bar,
                text="✔ 發動效果 / 是",
                bg="#06d6a0",
                fg="#000000",
                font=("Microsoft JhengHei", 12, "bold"),
                width=18,
                pady=5,
                cursor="hand2",
                command=lambda: [ans.update({"val": True}), self._close_overlay()],
            ).pack(side=tk.LEFT, expand=True, padx=8)
            tk.Button(
                btn_bar,
                text="✖ 略過不發 / 否",
                bg="#e63946",
                fg="#ffffff",
                font=("Microsoft JhengHei", 12, "bold"),
                width=18,
                pady=5,
                cursor="hand2",
                command=lambda: [ans.update({"val": False}), self._close_overlay()],
            ).pack(side=tk.LEFT, expand=True, padx=8)

            top_row = tk.Frame(frame, bg="#192030", padx=14, pady=6)
            top_row.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            if found_card:
                c_img = self.img_mgr.get_card_visual(getattr(found_card, "skin_id", found_card.id), 80, 112, is_selected=True)
                l_img = tk.Label(top_row, image=c_img, bg="#192030")
                l_img.image = c_img
                l_img.pack(side=tk.LEFT, padx=(2, 12))

            right_col = tk.Frame(top_row, bg="#192030")
            right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            tk.Label(
                right_col,
                text=f"⚡ {title}",
                bg="#192030",
                fg="#ffd166",
                font=("Microsoft JhengHei", 13, "bold"),
                anchor="w",
                wraplength=420,
                justify=tk.LEFT,
            ).pack(fill=tk.X, pady=(0, 4))

            tk.Label(
                right_col,
                text=message,
                bg="#232b3e",
                fg="#ffffff",
                font=("Microsoft JhengHei", 11, "bold"),
                wraplength=415,
                justify=tk.LEFT,
                padx=10,
                pady=8,
                relief=tk.SOLID,
                bd=1,
            ).pack(fill=tk.BOTH, expand=True, pady=2)

        custom_geom = {"width": 580, "height": 270, "relx": 0.5, "rely": 0.46}
        if found_widget and found_widget.winfo_exists():
            try:
                self.update_idletasks()
                bw = max(960, self.right_board.winfo_width())
                bh = max(720, self.right_board.winfo_height())
                wx = found_widget.winfo_rootx() - self.right_board.winfo_rootx()
                wy = found_widget.winfo_rooty() - self.right_board.winfo_rooty()
                target_x = max(300, min(bw - 300, wx + 60))
                target_y = max(145, min(bh - 250, wy - 125 if wy > 260 else wy + 180))
                custom_geom = {
                    "width": 580,
                    "height": 270,
                    "x": int(target_x - 290),
                    "y": int(target_y - 135),
                }
            except Exception:
                pass

        self._show_overlay_and_wait(build, custom_place=custom_geom)
        if found_widget and found_widget.winfo_exists() and orig_bg:
            try:
                found_widget.config(bg=orig_bg)
            except Exception:
                pass
        return ans["val"]

    def show_info_center(self, title: str, message: str):
        def build(frame):
            tk.Button(
                frame,
                text="✔ 確認關閉",
                bg="#118ab2",
                fg="white",
                font=("Microsoft JhengHei", 12, "bold"),
                width=18,
                height=2,
                cursor="hand2",
                command=self._close_overlay,
            ).pack(side=tk.BOTTOM, pady=18)
            tk.Label(
                frame,
                text=title,
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 15, "bold"),
            ).pack(pady=(24, 12))
            tk.Label(
                frame,
                text=message,
                bg="#282c3e",
                fg="#ffffff",
                font=("Microsoft JhengHei", 12),
                wraplength=600,
                padx=20,
                pady=18,
            ).pack(fill=tk.X, padx=36, pady=10)

        self._show_overlay_and_wait(build, custom_place={"relx": 0.5, "rely": 0.46, "width": 680, "height": 320})

    def choose_card_dialog(self, title, card_list, allow_cancel=True):
        if not card_list:
            return None
        result = {"card": None}

        def build(frame):
            tk.Label(
                frame,
                text=title,
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 13, "bold"),
                wraplength=780,
            ).pack(pady=(8, 4))

            sel_state = {"idx": 0}
            btns = []

            # 關鍵修正：優先將底部「確定選擇此卡 / 略過」按鈕列 pack(side=tk.BOTTOM)，避免被 Canvas 擠出視窗外！
            btn_f = tk.Frame(frame, bg="#1e2230")
            btn_f.pack(side=tk.BOTTOM, pady=10)
            tk.Button(
                btn_f,
                text="✔ 確定選擇此卡",
                bg="#06d6a0",
                fg="black",
                font=("Microsoft JhengHei", 12, "bold"),
                padx=20,
                pady=5,
                command=lambda: [
                    result.update({"card": card_list[sel_state["idx"]]}),
                    self._close_overlay(),
                ],
            ).pack(side=tk.LEFT, padx=10)
            if allow_cancel:
                tk.Button(
                    btn_f,
                    text="✖ 略過 / 不選 (0 張)",
                    bg="#e63946",
                    fg="white",
                    font=("Microsoft JhengHei", 12, "bold"),
                    padx=20,
                    pady=5,
                    command=self._close_overlay,
                ).pack(side=tk.LEFT, padx=10)

            canvas = tk.Canvas(frame, bg="#141620", height=240, highlightthickness=0)
            sc = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
            inner = tk.Frame(canvas, bg="#141620")
            inner.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=inner, anchor="nw")
            canvas.configure(xscrollcommand=sc.set)
            sc.pack(side=tk.BOTTOM, fill=tk.X, padx=14, pady=(0, 4))
            canvas.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

            def select_idx(i):
                sel_state["idx"] = i
                self.inspect_card(card_list[i])
                for b_idx, b in enumerate(btns):
                    b.config(bg="#f4a261" if b_idx == i else "#252734")

            for idx, c in enumerate(card_list):
                c_img = self.img_mgr.get_card_visual(getattr(c, "skin_id", c.id), 95, 132)
                b = tk.Button(
                    inner,
                    image=c_img,
                    text=f"{c.name[:7]}\nLv.{c.base_level} 費:{c.cost}",
                    compound=tk.TOP,
                    bg="#f4a261" if idx == 0 else "#252734",
                    fg="white",
                    font=("Microsoft JhengHei", 9, "bold"),
                    width=106,
                    height=170,
                    command=lambda i=idx: select_idx(i),
                )
                b.image = c_img
                b.pack(side=tk.LEFT, padx=6, pady=8)
                btns.append(b)
                b.bind(
                    "<MouseWheel>",
                    lambda e: canvas.xview_scroll(-1 if e.delta > 0 else 1, "units"),
                )

            canvas.bind(
                "<MouseWheel>",
                lambda e: canvas.xview_scroll(-1 if e.delta > 0 else 1, "units"),
            )
            self.inspect_card(card_list[0])

        self._show_overlay_and_wait(build)
        return result["card"]

    def open_zone_inspector(self, title, card_list, is_player_memory=False):
        # 若當前正在執行其他效果視窗（包括暫時隱藏看場地狀態），點擊公開區域則在左側預覽最新一張卡並於日誌列出清單，不覆蓋原本的效果視窗
        if getattr(self, "_overlay_is_waiting", False):
            if card_list:
                self.inspect_card(card_list[-1])
                names_str = "、".join(f"{c.name}(Lv.{c.base_level})" for c in card_list)
                self.log(f"📂 [檢視 {title} 共 {len(card_list)} 張]：{names_str}")
            else:
                self.log(f"📂 [檢視 {title}]：目前為空 (0 張)。")
            return
        for w in self.center_overlay.winfo_children():
            w.destroy()

        tk.Label(
            self.center_overlay,
            text=f"📂 {title} (共 {len(card_list)} 張)",
            bg="#1e2230",
            fg="#ffd166",
            font=("Microsoft JhengHei", 13, "bold"),
        ).pack(pady=(10, 4))

        if not card_list:
            tk.Label(
                self.center_overlay,
                text="此區域目前沒有可公開檢視的卡片。",
                bg="#1e2230",
                fg="#adb5bd",
                font=("Microsoft JhengHei", 12),
            ).pack(expand=True)
        else:
            canvas = tk.Canvas(
                self.center_overlay, bg="#141620", height=240, highlightthickness=0
            )
            sc = tk.Scrollbar(self.center_overlay, orient=tk.HORIZONTAL, command=canvas.xview)
            inner = tk.Frame(canvas, bg="#141620")
            inner.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=inner, anchor="nw")
            canvas.configure(xscrollcommand=sc.set)
            canvas.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)
            sc.pack(fill=tk.X, padx=14)

            for c in card_list:
                c_img = self.img_mgr.get_card_visual(getattr(c, "skin_id", c.id), 95, 132)
                b = tk.Button(
                    inner,
                    image=c_img,
                    text=f"{c.name[:7]}\nLv.{c.base_level}",
                    compound=tk.TOP,
                    bg="#252734",
                    fg="white",
                    font=("Microsoft JhengHei", 9, "bold"),
                    width=106,
                    height=166,
                    command=lambda card=c: self.inspect_card(card),
                )
                b.image = c_img
                b.pack(side=tk.LEFT, padx=6, pady=8)
                b.bind(
                    "<MouseWheel>",
                    lambda e: canvas.xview_scroll(-1 if e.delta > 0 else 1, "units"),
                )

        btn_bar = tk.Frame(self.center_overlay, bg="#1e2230")
        btn_bar.pack(side=tk.BOTTOM, pady=10)

        if (
            is_player_memory
            and self.active_player == self.player
            and self.phase == "MAIN"
            and any(c.id == "BFR/S78-075" for c in self.player.memory)
        ):
            tk.Button(
                btn_bar,
                text="♻️ 發動【獨有系列】記憶效果 (棄1張《遊戲》角色回手)",
                bg="#06d6a0",
                fg="black",
                font=("Microsoft JhengHei", 11, "bold"),
                padx=12,
                pady=4,
                command=self._activate_memory_unique_series,
            ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            btn_bar,
            text="關閉檢視面板",
            bg="#118ab2",
            fg="white",
            font=("Microsoft JhengHei", 11, "bold"),
            padx=18,
            pady=4,
            command=lambda: self.center_overlay.place_forget(),
        ).pack(side=tk.LEFT, padx=8)

        self.center_overlay.place(relx=0.5, rely=0.47, anchor="center", width=840, height=560)
        self.center_overlay.lift()

    def _activate_memory_unique_series(self):
        self.center_overlay.place_forget()
        ev = next((c for c in self.player.memory if c.id == "BFR/S78-075"), None)
        game_chars = [c for c in self.player.hand if c.type == "CHAR" and "遊戲" in c.traits]
        if not ev or not game_chars:
            self.show_info_center("無法發動", "手牌中沒有《遊戲》角色可供捨棄！")
            return
        self.select_hand_discard(
            self.player,
            filter_fn=lambda x: x.type == "CHAR" and "遊戲" in x.traits,
            prompt="請選擇要捨棄的手牌《遊戲》角色",
        )
        self.player.memory.remove(ev)
        self.player.hand.append(ev)
        self.log("♻️ 玩家從回憶區手動發動【獨有系列】記憶效果，返回手牌！")
        self.update_ui()

    def select_stage_slot_dialog(
        self, p: PlayerState, indices, title="請選擇舞台格子", allow_cancel=False
    ):
        """《Master Duel》風格場上原地選目標：直接在場上實際舞台格子高亮閃爍點選，不遮擋雙方舞台"""
        if not indices:
            return None
        res = {"slot": None if allow_cancel else indices[0]}
        valid_set = set(indices)
        self._field_slot_select_state = {
            "target_player": p,
            "valid_set": valid_set,
            "res": res,
            "allow_cancel": allow_cancel,
            "title": title,
        }
        self.update_ui()

        def build(frame):
            for w in frame.winfo_children():
                w.destroy()
            bar = tk.Frame(frame, bg="#141a29", padx=14, pady=8)
            bar.pack(fill=tk.BOTH, expand=True)
            side_lbl = "我方舞台" if p == self.player else f"{p.name} 舞台"
            tk.Label(
                bar,
                text=f"🎯 {title}  —  請直接點擊場上發亮標記的【{side_lbl}】格子！",
                bg="#141a29",
                fg="#06d6a0",
                font=("Microsoft JhengHei", 12, "bold"),
            ).pack(side=tk.LEFT, padx=6)
            if allow_cancel:
                tk.Button(
                    bar,
                    text="✖ 取消操作",
                    bg="#e63946",
                    fg="#ffffff",
                    font=("Microsoft JhengHei", 10, "bold"),
                    padx=14,
                    pady=2,
                    cursor="hand2",
                    command=lambda: [res.update({"slot": None}), self._close_overlay()],
                ).pack(side=tk.RIGHT, padx=6)

        self._show_overlay_and_wait(
            build,
            custom_place={"relx": 0.5, "rely": 0.435, "width": 760, "height": 52},
        )
        self._field_slot_select_state = None
        self.update_ui()
        return res["slot"]

    def ask_attack_type_dialog(self, attacker: CardInstance, defender: CardInstance, slot_idx: int):
        atk_pwr = self.get_effective_power(self.player, attacker, slot_idx)
        atk_soul = self.get_effective_soul(self.player, attacker, slot_idx)
        def_pwr = self.get_effective_power(self.ai, defender, slot_idx)
        def_lvl = self.get_effective_level(self.ai, defender, slot_idx)
        side_soul = max(0, atk_soul - def_lvl)
        can_side = not (attacker.has_effect("CONT_CANNOT_SIDE_ATTACK") or attacker.id == "BFR/S78-015")
        res = {"type": "FRONT"}

        atk_btn = self.btn_p_stage[slot_idx]
        def_btn = self.btn_ai_stage[slot_idx]
        orig_atk_bg = atk_btn.cget("bg") if atk_btn else None
        orig_def_bg = def_btn.cget("bg") if def_btn else None
        if atk_btn and atk_btn.winfo_exists():
            atk_btn.config(bg="#ffd166")
        if def_btn and def_btn.winfo_exists():
            def_btn.config(bg="#e63946")

        def build(frame):
            box = tk.Frame(frame, bg="#192030", padx=14, pady=8)
            box.pack(fill=tk.BOTH, expand=True)

            btn_frame = tk.Frame(box, bg="#192030")
            btn_frame.pack(side=tk.BOTTOM, pady=(4, 8))

            tk.Button(
                btn_frame,
                text=f"🔥 正面攻擊 (Front)\n魂傷：{atk_soul} ｜ 進行戰鬥比拼 (可發動助太刀)",
                bg="#e63946",
                fg="white",
                font=("Microsoft JhengHei", 11, "bold"),
                width=25,
                height=3,
                cursor="hand2",
                command=lambda: [res.update({"type": "FRONT"}), self._close_overlay()],
            ).pack(side=tk.LEFT, padx=8)

            tk.Button(
                btn_frame,
                text=f"⚡ 側面攻擊 (Side)\n魂傷：{side_soul} (扣對手等級 {def_lvl}) ｜ 安全保怪",
                bg="#118ab2" if can_side else "#495057",
                fg="white",
                font=("Microsoft JhengHei", 11, "bold"),
                width=25,
                height=3,
                cursor="hand2" if can_side else "arrow",
                state=tk.NORMAL if can_side else tk.DISABLED,
                command=lambda: [res.update({"type": "SIDE"}), self._close_overlay()],
            ).pack(side=tk.LEFT, padx=8)

            tk.Label(
                box,
                text=f"⚔️ 【{attacker.name}】宣告攻擊方式",
                bg="#192030",
                fg="#ffd166",
                font=("Microsoft JhengHei", 13, "bold"),
            ).pack(pady=(2, 4))
            tk.Label(
                box,
                text=f"我方攻擊力：{atk_pwr} (魂傷：{atk_soul})   vs   正面對手：【{defender.name}】 (攻：{def_pwr} / 等級：{def_lvl})",
                bg="#232b3e",
                fg="#ffffff",
                font=("Microsoft JhengHei", 11, "bold"),
                padx=10,
                pady=6,
                relief=tk.SOLID,
                bd=1,
            ).pack(fill=tk.X, padx=6, pady=2)

        custom_geom = {"relx": 0.5, "rely": 0.44, "width": 580, "height": 235}
        if atk_btn and atk_btn.winfo_exists():
            try:
                self.update_idletasks()
                bw = max(960, self.right_board.winfo_width())
                wx = atk_btn.winfo_rootx() - self.right_board.winfo_rootx()
                wy = atk_btn.winfo_rooty() - self.right_board.winfo_rooty()
                tx = max(300, min(bw - 300, wx + 54))
                ty = max(140, wy - 115)
                custom_geom = {"x": int(tx - 290), "y": int(ty - 115), "width": 580, "height": 235}
            except Exception:
                pass

        self._show_overlay_and_wait(build, custom_place=custom_geom)
        if atk_btn and atk_btn.winfo_exists() and orig_atk_bg:
            atk_btn.config(bg=orig_atk_bg)
        if def_btn and def_btn.winfo_exists() and orig_def_bg:
            def_btn.config(bg=orig_def_bg)
        return res["type"]

    def select_hand_discard(self, p: PlayerState, filter_fn=None, prompt="請選擇要捨棄的手牌"):
        candidates = [c for c in p.hand if (filter_fn(c) if filter_fn else True)]
        if not candidates:
            return None
        c = (
            candidates[0]
            if p.is_ai
            else self.choose_card_dialog(prompt, candidates, allow_cancel=False)
        )
        if c in p.hand:
            p.hand.remove(c)
            p.waiting_room.append(c)
        return c

    # ------------------------------------------
    # 卡片詳細預覽與日誌輸出
    # ------------------------------------------
    def inspect_card(self, card: CardInstance, owner: PlayerState = None, stage_idx: int = None, open_drawer: bool = True):
        if not card:
            return
        if open_drawer:
            self.show_card_drawer()
        img = self.img_mgr.get_card_visual(getattr(card, "skin_id", card.id), 170, 238, state="STAND", is_selected=False)
        if img:
            self.lbl_card_img.config(image=img, width=170, height=238)
            self.lbl_card_img.image = img

        eff_lvl = self.get_effective_level(owner, card, stage_idx) if owner else card.base_level
        eff_pwr = (
            self.get_effective_power(owner, card, stage_idx)
            if owner and stage_idx is not None
            else card.base_power
        )
        eff_soul = (
            self.get_effective_soul(owner, card, stage_idx)
            if owner and stage_idx is not None
            else card.base_soul
        )

        disp_id = getattr(card, "skin_id", card.id)
        rar_tag = f" [✨{getattr(card, 'rarity', 'SR')}]" if getattr(card, "is_high_rarity", False) else ""
        self.lbl_card_title.config(text=f"{card.name} ({disp_id}){rar_tag}")
        traits_str = " / ".join(card.traits) if card.traits else "無"
        state_zh = {"STAND": "正置", "REST": "橫置", "REVERSE": "倒置"}.get(card.state, card.state)
        stats_text = (
            f"種類：{get_card_type_zh(card.type)} ｜ 顏色：{card.color} ｜ 特徵：{traits_str}\n"
            f"等級：{eff_lvl} ｜ 費用：{card.cost} ｜ 攻擊力：{eff_pwr} ｜ 魂傷：{eff_soul} ｜ 標記：{get_trigger_zh(card.trigger)}"
        )
        if stage_idx is not None:
            stats_text += f"\n狀態：{state_zh} ｜ 下方標記：{len(card.markers)} 張"
        self.lbl_card_stats.config(text=stats_text)

        self.txt_card_effect.config(state=tk.NORMAL)
        self.txt_card_effect.delete("1.0", tk.END)
        self.txt_card_effect.insert(tk.END, card.text)
        self.txt_card_effect.config(state=tk.DISABLED)

    def log(self, msg):
        if self.winfo_exists():
            self.txt_log.insert(tk.END, msg + "\n")
            self.txt_log.see(tk.END)
            try:
                if (
                    any(k in msg for k in ["發動", "觸發", "連動", "透過", "使對手", "使【", "回復", "檢索", "回收", "不倒置", "助太刀", "反擊", "飛躍登場", "標記"])
                    and not any(skip in msg for skip in ["===", "進入【", "起手替換", "置入時鐘", "檢視 "])
                ):
                    m = re.search(r"【([^】]+)】", msg)
                    if m:
                        cname = m.group(1)
                        prefer_p = None
                        if self.ai.name and self.ai.name in msg:
                            prefer_p = self.ai
                        elif self.player.name and self.player.name in msg:
                            prefer_p = self.player
                        p_found, c_found, w_found, _ = self._find_field_card_and_widget(cname, prefer_player=prefer_p)
                        if c_found and w_found:
                            self.show_field_effect_cutin(p_found, c_found, w_found, msg)
            except Exception:
                pass

    # ------------------------------------------
    # 動態數值計算委派至 engine.RuleEngine
    # ------------------------------------------
    def get_effective_level(self, p: PlayerState, card: CardInstance, stage_idx=None):
        return RuleEngine.get_effective_level(p, card, stage_idx)

    def get_effective_power(self, p: PlayerState, card: CardInstance, stage_idx: int):
        opp = self.ai if p == self.player else self.player
        is_my_turn = self.active_player == p
        return RuleEngine.get_effective_power(p, opp, card, stage_idx, is_my_turn=is_my_turn)

    def get_effective_soul(self, p: PlayerState, card: CardInstance, stage_idx: int):
        return RuleEngine.get_effective_soul(p, card, stage_idx)

    def can_play_card(self, p: PlayerState, card: CardInstance):
        return RuleEngine.can_play_card(p, card)

    def pay_stock(self, p: PlayerState, amount: int):
        RuleEngine.pay_stock(p, amount)

    # ------------------------------------------
    # 基礎規則：抽牌、洗牌罰血、升級、牌庫見底判負
    # ------------------------------------------
    def check_deck_refresh(self, p: PlayerState):
        """
        WS 核心優先規則：在任何情況下只要牌組變為 0 張，立即優先把休息室的牌洗回牌組，
        並馬上將牌組頂 1 張放到計時區（罰血 1 點），再繼續原本的動作！
        """
        while len(p.deck) == 0 and not self.game_over:
            if len(p.waiting_room) == 0:
                if not self.game_over:
                    winner = self.ai if p == self.player else self.player
                    is_win = winner == self.player
                    self.log(f"🏆 {p.name} 的牌庫與休息室同時歸零，{winner.name} 獲得勝利！")
                    self.show_game_over_animation(
                        is_win,
                        f"{p.name} 牌庫與休息室見底無法重洗！\n獲勝者：{winner.name}",
                    )
                return
            self.log(
                f"🔄 【WS 規則優先處理】{p.name} 牌庫歸零！立即將休息室 ({len(p.waiting_room)} 張) 洗回牌庫，並馬上扣 1 張去計時區！"
            )
            p.deck = list(p.waiting_room)
            p.waiting_room.clear()
            random.shuffle(p.deck)
            if len(p.deck) > 0:
                penalty = p.deck.pop(0)
                p.clock.append(penalty)
                self.log(f"🩸 [重洗罰血] {p.name} 立即將新牌庫頂【{penalty.name}】置入計時區！")
                self.check_level_up(p)
                self.update_ui()

    def pop_deck_top(self, p: PlayerState):
        """從牌組頂取出一張牌；若取出前或取出後牌組為 0 張，皆立即觸發休息室重洗與計時區罰血"""
        self.check_deck_refresh(p)
        if self.game_over or len(p.deck) == 0:
            return None
        c = p.deck.pop(0)
        if len(p.deck) == 0 and not self.game_over:
            self.check_deck_refresh(p)
        return c

    def pop_deck_bottom(self, p: PlayerState):
        """從牌組底取出一張牌；若取出前或取出後牌組為 0 張，皆立即觸發休息室重洗與計時區罰血"""
        self.check_deck_refresh(p)
        if self.game_over or len(p.deck) == 0:
            return None
        c = p.deck.pop()
        if len(p.deck) == 0 and not self.game_over:
            self.check_deck_refresh(p)
        return c

    def remove_card_from_deck(self, p: PlayerState, card_obj):
        """從牌組移除指定檢索卡；若移除後牌組變為 0 張，立即優先執行重洗與罰血"""
        if card_obj in p.deck:
            p.deck.remove(card_obj)
            if len(p.deck) == 0 and not self.game_over:
                self.check_deck_refresh(p)

    def draw_cards(self, p: PlayerState, count: int):
        if count > 0 and not self.game_over:
            self.app.sound_mgr.play_sfx("sfx_draw")
        for _ in range(count):
            c = self.pop_deck_top(p)
            if self.game_over or c is None:
                break
            p.hand.append(c)
        self.update_ui()

    def check_level_up(self, p: PlayerState):
        while len(p.clock) >= 7:
            if len(p.level_zone) >= 3:
                winner = self.ai if p == self.player else self.player
                is_win = winner == self.player
                self.update_ui()
                reason_str = f"{p.name} 總傷害達到等級 4！\n獲勝者：{winner.name}"
                self.log(f"🏆 {p.name} 升上等級 4，{winner.name} 獲得勝利！")
                if self.is_lan and self.net_node and self.net_node.connected:
                    self.net_node.send({
                        "type": "GAME_OVER",
                        "receiver_win": (not is_win),
                        "reason": reason_str,
                    })
                self.show_game_over_animation(is_win, reason_str)
                return

            if self.is_lan and p == self.ai and self.net_node and self.net_node.connected:
                self.net_node.send({
                    "type": "LEVEL_UP_REQ",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
                def _wait_lv(frame):
                    tk.Label(
                        frame,
                        text=f"⏳ 對手【{self.ai.name}】傷害達到 7 點，正在等待對手選擇升級卡片...",
                        bg="#1e2230",
                        fg="#ffd166",
                        font=("Microsoft JhengHei", 15, "bold"),
                    ).pack(pady=80)
                self._show_overlay_and_wait(_wait_lv)
                return

            top7 = p.clock[:7]
            p.clock = p.clock[7:]
            if not p.is_ai:
                chosen = self.choose_card_dialog(
                    "升級選擇：請從時鐘區 7 張卡片中選 1 張放入等級區", top7, allow_cancel=False
                )
            else:
                chosen = top7[0]
                existing_colors = {c.color for c in p.level_zone}
                for c in top7:
                    if c.color not in existing_colors and c.color in ["紅", "藍", "黃", "綠"]:
                        chosen = c
                        break
            p.level_zone.append(chosen)
            for c in top7:
                if c != chosen:
                    p.waiting_room.append(c)
            self.log(f"⬆️ {p.name} 升級至 Lv.{len(p.level_zone)}（放入等級區：{chosen.name}）")
            self.update_ui()

    def deal_damage(self, target: PlayerState, amount: int, source_text="攻擊"):
        if self.game_over or amount <= 0:
            return
        # 多人連線時，若承受傷害的是連線對手 (target == self.ai)，交由對手自己點擊翻開自己的牌組，並即時同步畫面給雙方觀看！
        if self.is_lan and target == self.ai and self.net_node and self.net_node.connected:
            self.log(f"💥 對 {target.name} 造成 {amount} 點傷害 ({source_text})，等待 {target.name} 親自翻開牌組進行傷害檢定...")
            self.net_node.send({
                "type": "DAMAGE_CHECK_REQ",
                "amount": amount,
                "source_text": source_text,
                "sender_state": self.player.to_sync_dict(),
                "receiver_state": self.ai.to_sync_dict(),
            })
            def _wait_remote_dmg(frame):
                tk.Label(
                    frame,
                    text=f"💥 對【{target.name}】造成 {amount} 點傷害 ({source_text})\n⏳ 正在同步觀看【{target.name}】親自翻開自己的牌組進行傷害判定...",
                    bg="#1e2230",
                    fg="#ffd166",
                    font=("Microsoft JhengHei", 15, "bold"),
                    justify=tk.CENTER,
                ).pack(pady=80)
            self._show_overlay_and_wait(_wait_remote_dmg)
            return

        self._execute_local_damage_check(target, amount, source_text)

    def _execute_local_damage_check(self, target: PlayerState, amount: int, source_text="攻擊"):
        if self.game_over or amount <= 0:
            return
        self.log(f"💥 對 {target.name} 造成 {amount} 點傷害 ({source_text})...")
        temp_cards = []
        canceled = False
        for _ in range(amount):
            c = self.pop_deck_top(target)
            if self.game_over or c is None:
                break
            temp_cards.append(c)
            if c.type == "CX":
                canceled = True
                self.log(f"🛡️ 翻出名場面【{c.name}】！{amount} 點傷害取消！")
                break
        # 建立逐張傷害判定翻牌資訊：真人玩家承受傷害時親自點擊翻自己的牌，AI 承受傷害時依設定秒數自動翻牌
        step_infos = []
        for idx_d, dc in enumerate(temp_cards):
            if dc.type == "CX":
                step_infos.append({
                    "card": dc,
                    "badge": "🛡️ 名場面 (傷害取消!)",
                    "step_shout": f"🛡️ 第 {idx_d + 1} 張翻出名場面【{dc.name}】！傷害取消！",
                    "step_bg": "#06d6a0",
                    "step_fg": "#000000",
                    "step_sfx": "sfx_climax",
                })
            else:
                step_infos.append({
                    "card": dc,
                    "badge": f"第 {idx_d + 1}/{amount} 點傷害",
                    "step_shout": f"🎴 傷害檢定第 {idx_d + 1}/{amount} 張：【{dc.name}】(Lv.{dc.base_level}，非名場面)",
                    "step_bg": "#3a3f58",
                    "step_fg": "#ffffff",
                    "step_sfx": "sfx_draw",
                })

        if canceled:
            cx_card = temp_cards[-1] if temp_cards else None
            cx_name = f"【{cx_card.name}】" if cx_card else ""
            self.run_interactive_card_flip_sequence(
                deck_owner=target,
                clicker_is_ai=target.is_ai,
                banner_title=f"傷害判定翻牌 — {target.name} 承受 {amount} 點傷害 ({source_text})",
                step_cards_info=step_infos,
                final_summary_text=f"🛡️ 傷害取消！翻出名場面 {cx_name}（全數送入休息室）",
                final_summary_bg="#06d6a0",
                final_summary_fg="#000000",
            )
            target.waiting_room.extend(temp_cards)
            self.update_ui()
        else:
            self.log(f"🩸 {amount} 點傷害命中！")
            self.run_interactive_card_flip_sequence(
                deck_owner=target,
                clicker_is_ai=target.is_ai,
                banner_title=f"傷害判定翻牌 — {target.name} 承受 {amount} 點傷害 ({source_text})",
                step_cards_info=step_infos,
                final_summary_text=f"💥 {len(temp_cards)} 點傷害命中！（置入時鐘傷害區）",
                final_summary_bg="#e63946",
                final_summary_fg="#ffffff",
            )
            target.clock.extend(temp_cards)
            self.check_level_up(target)
        if len(target.deck) == 0 and not self.game_over:
            self.check_deck_refresh(target)
        self.update_ui()

    # ==========================================================================
    # 萬用資料驅動效果執行引擎 (Universal Data-Driven Effect Engine)
    # 自動根據 ChineseEffectParser 編譯出的 parsed_abilities AST 執行效果，
    # 讓任何從貓罐子匯入的新系列／新牌組無須寫死 if card.id == ... 即可運作！
    # ==========================================================================
    def _can_pay_universal_cost(self, p: PlayerState, cost: dict, card: CardInstance = None) -> bool:
        if not cost:
            return True
        if len(p.stock) < cost.get("stock", 0):
            return False
        if len(p.hand) < cost.get("discard_hand", 0):
            return False
        if cost.get("discard_cx", 0) > 0:
            if sum(1 for c in p.hand if c.type == "CX") < cost["discard_cx"]:
                return False
        if cost.get("clock_top_deck", 0) > 0:
            if len(p.deck) == 0 and len(p.waiting_room) == 0:
                return False
        if cost.get("rest_self", 0) == 1 and card and card.state != "STAND":
            return False
        return True

    def _pay_universal_cost(self, p: PlayerState, cost: dict, card: CardInstance = None, slot_idx: int = None, title: str = "支付代價") -> bool:
        if not cost:
            return True
        if not self._can_pay_universal_cost(p, cost, card):
            return False
        if cost.get("stock", 0) > 0:
            self.pay_stock(p, cost["stock"])
        if cost.get("clock_top_deck", 0) > 0:
            self.check_deck_refresh(p)
            if p.deck:
                top_c = self.pop_deck_top(p)
                p.clock.append(top_c)
                self.log(f"⏱️ 【{title}】將牌組頂的【{top_c.name}】放到時鐘區作為代價。")
                self.check_level_up(p)
        if cost.get("discard_cx", 0) > 0:
            for _ in range(cost["discard_cx"]):
                self.select_hand_discard(p, filter_fn=lambda x: x.type == "CX", prompt=f"{title}：請選擇捨棄 1 張名場面")
        if cost.get("discard_hand", 0) > 0:
            disc_n = cost["discard_hand"]
            for idx_d in range(disc_n):
                self.select_hand_discard(p, prompt=f"{title}：請選擇捨棄第 {idx_d + 1}/{disc_n} 張手牌")
        if cost.get("rest_self", 0) == 1 and card:
            card.state = "REST"
        if cost.get("send_self_wr") and slot_idx is not None and p.stage[slot_idx] == card:
            self.send_stage_to_wr(p, slot_idx)
        elif cost.get("send_self_memory") and slot_idx is not None and p.stage[slot_idx] == card:
            p.stage[slot_idx] = None
            card.reset_stage_state()
            p.memory.append(card)
        return True

    def _execute_universal_ability(self, p: PlayerState, opp: PlayerState, card: CardInstance, ab: dict, slot_idx: int = None, target_opp_slot: int = None):
        if self.game_over:
            return
        if ab.get("is_cx_combo"):
            cx_name = ab.get("cx_name")
            if not p.climax_zone:
                return
            if cx_name and cx_name not in p.climax_zone.name:
                return
        cost = ab.get("cost", {})
        if not self._can_pay_universal_cost(p, cost, card):
            return
        raw_desc = ab.get("raw", card.text)
        has_any_cost = any(bool(v) for v in cost.values())
        if has_any_cost or ab.get("category") == "AUTO":
            ask_ok = True if p.is_ai else self.ask_yes_no_center(
                f"⚡ 發動效果：【{card.name}】",
                f"{raw_desc}\n\n是否發動此效果？"
            )
            if not ask_ok:
                return
        if not self._pay_universal_cost(p, cost, card, slot_idx, title=card.name):
            return

        for act in ab.get("actions", []):
            if self.game_over:
                break
            atype = act.get("action")
            if atype == "heal_to_wr":
                if len(p.clock) > 0:
                    healed = p.clock.pop()
                    p.waiting_room.append(healed)
                    self.log(f"💖 【{card.name}】回復 1 點傷害（移除時鐘區：{healed.name}）！")
            elif atype == "heal_to_stock":
                if len(p.clock) > 0:
                    healed = p.clock.pop()
                    p.stock.append(healed)
                    self.log(f"💖⚡ 【{card.name}】將時鐘區頂的【{healed.name}】放到能量區（回血＋充能）！")
            elif atype == "look_top_add_hand":
                look_n = act.get("look", 4)
                looked = self.ask_step_by_step_look_up_to(p, look_n, f"{card.name}：看牌組頂最多 {look_n} 張")
                if looked:
                    chars = [c for c in looked if c.type == "CHAR"]
                    picked = None
                    if chars:
                        picked = chars[0] if p.is_ai else self.choose_card_dialog(
                            f"{card.name}：選擇 1 張角色加入手牌（可略過）", chars, allow_cancel=True
                        )
                    if picked:
                        looked.remove(picked)
                        p.hand.append(picked)
                        self.log(f"🔍 【{card.name}】從牌組頂將【{picked.name}】加入手牌！")
                    p.waiting_room.extend(looked)
            elif atype == "search_deck_char":
                cands = [c for c in p.deck if c.type == "CHAR"]
                if cands:
                    picked = cands[0] if p.is_ai else self.choose_card_dialog(
                        f"{card.name}：從牌組選擇 1 張角色加入手牌", cands, allow_cancel=True
                    )
                    if picked and picked in p.deck:
                        p.deck.remove(picked)
                        p.hand.append(picked)
                        self.log(f"🔍 【{card.name}】從牌組檢索【{picked.name}】加入手牌！")
                random.shuffle(p.deck)
            elif atype == "salvage_wr":
                t_type = "CX" if act.get("target_type") == "Climax" else "CHAR"
                cands = [c for c in p.waiting_room if c.type == t_type]
                if cands:
                    picked = cands[0] if p.is_ai else self.choose_card_dialog(
                        f"{card.name}：從休息室選擇 1 張卡片返回手牌", cands, allow_cancel=True
                    )
                    if picked and picked in p.waiting_room:
                        p.waiting_room.remove(picked)
                        p.hand.append(picked)
                        self.log(f"♻️ 【{card.name}】從休息室回收【{picked.name}】返回手牌！")
            elif atype == "draw":
                cnt = act.get("count", 1)
                self.draw_cards(p, cnt)
                self.log(f"🎴 【{card.name}】抽 {cnt} 張牌！")
            elif atype == "discard_hand":
                cnt = act.get("count", 1)
                for _ in range(cnt):
                    if p.hand:
                        self.select_hand_discard(p, prompt=f"{card.name}：請選擇捨棄 1 張手牌")
            elif atype == "charge_stock_top":
                cnt = act.get("count", 1)
                for _ in range(cnt):
                    self.check_deck_refresh(p)
                    if p.deck:
                        p.stock.append(self.pop_deck_top(p))
                self.log(f"⚡ 【{card.name}】從牌組頂充能 +{cnt}！")
            elif atype == "burn":
                dmg = act.get("damage", 1)
                self.log(f"🔥 【{card.name}】發動追加傷害：給予對手 {dmg} 點傷害！")
                self.deal_damage(opp, dmg, source_text=f"{card.name} 效果傷害")
            elif atype == "buff_self":
                pwr = act.get("power", 1000)
                card.temp_power += pwr
                self.log(f"⚔️ 【{card.name}】本回合攻擊力 +{pwr}！")
            elif atype == "buff_ally":
                pwr = act.get("power", 1000)
                ally_slots = [i for i in range(5) if p.stage[i] is not None]
                if ally_slots:
                    t_s = ally_slots[0] if p.is_ai else self.select_stage_slot_dialog(
                        p, ally_slots, f"{card.name}：選擇 1 張角色攻擊力 +{pwr}"
                    )
                    if p.stage[t_s]:
                        p.stage[t_s].temp_power += pwr
                        self.log(f"⚔️ 【{card.name}】使【{p.stage[t_s].name}】本回合攻擊力 +{pwr}！")
            elif atype == "kick_opp_to_clock" and target_opp_slot is not None and opp.stage[target_opp_slot]:
                oc = opp.stage[target_opp_slot]
                opp.stage[target_opp_slot] = None
                oc.reset_stage_state()
                opp.clock.append(oc)
                self.log(f"⏱️ 【{card.name}】將被擊倒的【{oc.name}】直接送入對手時鐘區！")
                self.check_level_up(opp)
            elif atype == "kick_opp_to_memory" and target_opp_slot is not None and opp.stage[target_opp_slot]:
                oc = opp.stage[target_opp_slot]
                opp.stage[target_opp_slot] = None
                oc.reset_stage_state()
                opp.memory.append(oc)
                self.log(f"🌌 【{card.name}】將被擊倒的【{oc.name}】放逐至對手回憶區！")
            elif atype == "kick_opp_to_stock" and target_opp_slot is not None and opp.stage[target_opp_slot]:
                oc = opp.stage[target_opp_slot]
                opp.stage[target_opp_slot] = None
                oc.reset_stage_state()
                opp.stock.append(oc)
                self.log(f"⚡ 【{card.name}】將被擊倒的【{oc.name}】送入對手能量區！")
            elif atype == "reversal_bomb" and target_opp_slot is not None and opp.stage[target_opp_slot]:
                oc = opp.stage[target_opp_slot]
                if oc.base_level <= card.base_level:
                    oc.state = "REVERSE"
                    self.log(f"💥 【{card.name}】發動等級相殺！將對手的【{oc.name}】一併【倒置】！")
        self.update_ui()

    def _run_universal_timing(self, p: PlayerState, opp: PlayerState, card: CardInstance, timing: str, slot_idx: int = None, target_opp_slot: int = None):
        if not card or not getattr(card, "parsed_abilities", None):
            return
        for ab in card.parsed_abilities:
            if ab.get("category") == "AUTO" and ab.get("timing") == timing:
                self._execute_universal_ability(p, opp, card, ab, slot_idx=slot_idx, target_opp_slot=target_opp_slot)

    def send_stage_to_wr(self, p: PlayerState, slot_idx: int, is_overwritten: bool = False):
        card = p.stage[slot_idx]
        if not card:
            return
        p.stage[slot_idx] = None
        if card.markers:
            p.waiting_room.extend(card.markers)
            card.markers.clear()
        card.reset_stage_state()
        p.waiting_room.append(card)
        self.update_ui()

        # 任務 3：BFR/S78-062《咬咬 梅普露》逐步看最多 4 張並選最多 1 張加手
        if card.id == "BFR/S78-062" and len(p.hand) > 0:
            do_eff = (
                (len(p.hand) <= 5)
                if p.is_ai
                else self.ask_yes_no_center(
                    "咬咬 梅普露",
                    "是否捨棄 1 張手牌，從牌庫上方逐步看最多 4 張並選擇最多 1 張等級 1 以上的卡片（名場面視為 0 等）加入手牌？",
                )
            )
            if do_eff:
                disc = self.select_hand_discard(p, prompt="咬咬 梅普露：請選擇捨棄 1 張手牌作為代價")
                if disc:
                    looked = self.ask_step_by_step_look_up_to(p, 4, "咬咬 梅普露", show_lv1_hint=True)
                    valid = [c for c in looked if c.type != "CX" and c.base_level >= 1]
                    chosen = None
                    if valid:
                        chosen = (
                            max(valid, key=lambda x: x.base_level)
                            if p.is_ai
                            else self.choose_card_dialog(
                                "咬咬 梅普露：選擇最多 1 張等級 1 以上卡片加入手牌 (可點略過不拿)",
                                valid,
                                allow_cancel=True,
                            )
                        )
                    if chosen:
                        p.hand.append(chosen)
                        looked.remove(chosen)
                        self.log(f"🔍 {p.name} 發動【咬咬 梅普露】選擇了【{chosen.name}】加入手牌！")
                    else:
                        self.log(f"🔍 {p.name} 結束【咬咬 梅普露】翻牌結算（未拿取卡片）。")
                    p.waiting_room.extend(looked)
                    self.update_ui()

        # GA13/S131-077《我的女神 草壁由佳》退場時 (1)+牌組頂1張放傷害區 -> 看牌組頂最多2張選最多2張《GA文庫》角色加手
        if card.id == "GA13/S131-077" and len(p.stock) >= 1 and len(p.deck) >= 1:
            do_yuka = (
                (len(p.level_zone) < 3)
                if p.is_ai
                else self.ask_yes_no_center(
                    "我的女神 草壁由佳",
                    "【我的女神 草壁由佳】從舞台放到休息室！\n是否支付 (1) 能量並將牌組頂 1 張放到傷害區，看牌組上方最多 2 張並選擇最多 2 張《GA文庫》角色加入手牌？",
                )
            )
            if do_yuka:
                self.pay_stock(p, 1)
                self.check_deck_refresh(p)
                if p.deck and not self.game_over:
                    dmg_c = self.pop_deck_top(p)
                    p.clock.append(dmg_c)
                    self.log(f"⏰ {p.name} 支付代價將牌組頂【{dmg_c.name}】置入傷害區。")
                    self.check_level_up(p)
                if not self.game_over:
                    looked = self.ask_step_by_step_look_up_to(p, 2, "我的女神 草壁由佳")
                    for pick_n in range(2):
                        valid_ga = [c for c in looked if c.type == "CHAR" and "GA文庫" in c.traits]
                        if not valid_ga:
                            break
                        chosen = (
                            valid_ga[0]
                            if p.is_ai
                            else self.choose_card_dialog(
                                f"我的女神 草壁由佳：選擇第 {pick_n + 1} 張《GA文庫》角色加入手牌",
                                valid_ga,
                                allow_cancel=True,
                            )
                        )
                        if not chosen:
                            break
                        p.hand.append(chosen)
                        looked.remove(chosen)
                        self.log(f"🌾 {p.name} 透過【我的女神 草壁由佳】將【{chosen.name}】加入手牌！")
                    p.waiting_room.extend(looked)
                    self.update_ui()

        if not is_overwritten and card.id == "BFR/S78-073" and p.stage[slot_idx] is None:
            char_in_hand = [c for c in p.hand if c.type == "CHAR"]
            if char_in_hand:
                do_enc = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "手牌安可", "是否捨棄手牌 1 張角色卡，讓【不屈的守護者 梅普露】橫置復活回原位？"
                    )
                )
                if do_enc:
                    disc = (
                        char_in_hand[0]
                        if p.is_ai
                        else self.choose_card_dialog(
                            "選擇要捨棄的手牌角色作為安可代價", char_in_hand, allow_cancel=False
                        )
                    )
                    if disc in p.hand:
                        p.hand.remove(disc)
                        p.waiting_room.append(disc)
                    if card in p.waiting_room:
                        p.waiting_room.remove(card)
                    card.state = "REST"
                    p.stage[slot_idx] = card
                    self.log(f"♻️ {p.name} 支付手牌角色發動安可，【{card.name}】橫置回到場上！")
                    self.update_ui()

        # BTR/W107-077《裝過頭的面子 後藤一里》退場時：［手牌1張《音樂》角色放到休息室］ 看牌組頂最多4張選最多1張 Lv.1 以上卡片加手
        if card.id == "BTR/W107-077":
            music_in_hand = [c for c in p.hand if c.type == "CHAR" and "音樂" in c.traits]
            if music_in_hand:
                do_bocchi77 = (
                    (len(p.hand) <= 5)
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "裝過頭的面子 後藤一里",
                        "【裝過頭的面子 後藤一里】從舞台放到休息室！\n是否捨棄手牌 1 張《音樂》角色，從牌組上方逐步看最多 4 張並選擇最多 1 張等級 1 以上的卡片（名場面視為 0 等）加入手牌？",
                    )
                )
                if do_bocchi77:
                    disc = self.select_hand_discard(
                        p,
                        filter_fn=lambda x: x.type == "CHAR" and "音樂" in x.traits,
                        prompt="裝過頭的面子 後藤一里：請選擇捨棄 1 張手牌《音樂》角色",
                    )
                    if disc:
                        looked = self.ask_step_by_step_look_up_to(
                            p, 4, "裝過頭的面子 後藤一里", show_lv1_hint=True
                        )
                        valid = [c for c in looked if c.type != "CX" and c.base_level >= 1]
                        chosen = None
                        if valid:
                            chosen = (
                                max(valid, key=lambda x: x.base_level)
                                if p.is_ai
                                else self.choose_card_dialog(
                                    "裝過頭的面子 後藤一里：選擇最多 1 張等級 1 以上卡片加入手牌 (可點略過不拿)",
                                    valid,
                                    allow_cancel=True,
                                )
                            )
                        if chosen:
                            p.hand.append(chosen)
                            looked.remove(chosen)
                            self.log(f"🎸 {p.name} 發動【裝過頭的面子 後藤一里】將【{chosen.name}】加入手牌！")
                        p.waiting_room.extend(looked)
                        self.update_ui()

        # BTR/W107-T17《高人氣 喜多郁代》& BTR/W107-T18《喜多郁代》再登場：［(1) 手牌1張卡片放到休息室］
        if not is_overwritten and (card.has_effect("AUTO_ENCORE_1STOCK_1HAND") or card.id in ["BTR/W107-T17", "BTR/W107-T18"]) and p.stage[slot_idx] is None:
            if len(p.stock) >= 1 and len(p.hand) >= 1:
                do_enc1 = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        f"再登場（安可）：{card.name}",
                        f"是否支付 (1) 能量並捨棄手牌 1 張卡片，讓【{card.name}】以【橫置】狀態回到原本所在的格子？",
                    )
                )
                if do_enc1:
                    self.pay_stock(p, 1)
                    self.select_hand_discard(p, prompt=f"{card.name} 再登場：請選擇捨棄 1 張手牌")
                    if card in p.waiting_room:
                        p.waiting_room.remove(card)
                    card.state = "REST"
                    p.stage[slot_idx] = card
                    self.log(f"♻️ {p.name} 支付 (1) 能量與 1 張手牌發動再登場，【{card.name}】橫置回到場上！")
                    self.update_ui()
        else:
            opp_wr = self.ai if p == self.player else self.player
            self._run_universal_timing(p, opp_wr, card, "ON_STAGE_TO_WR", slot_idx=slot_idx)
            # 萬用手牌安可 (hand_encore)
            if not is_overwritten and p.stage[slot_idx] is None and any(ab.get("effect") == "hand_encore" for ab in getattr(card, "parsed_abilities", [])):
                char_h = [c for c in p.hand if c.type == "CHAR"]
                if char_h:
                    do_he = True if p.is_ai else self.ask_yes_no_center(
                        f"♻️ 手牌安可：【{card.name}】",
                        f"是否將手牌 1 張角色放到休息室，使【{card.name}】以【橫置】狀態回到原位？"
                    )
                    if do_he:
                        self.select_hand_discard(p, filter_fn=lambda x: x.type == "CHAR", prompt=f"{card.name} 手牌安可：請選擇捨棄 1 張角色")
                        if card in p.waiting_room:
                            p.waiting_room.remove(card)
                        card.state = "REST"
                        p.stage[slot_idx] = card
                        self.log(f"♻️ {p.name} 發動手牌安可，【{card.name}】橫置回到場上！")
                        self.update_ui()

        # WS 共通規則「3 能量安可（アンコール ［(3)］）」：當角色從舞台進休息室（非壓卡覆蓋）且尚未藉由其他安可回場時，若擁有 3 點以上能量，可支付 (3) 能量將該角色橫置放回原位！
        if not is_overwritten and p.stage[slot_idx] is None and len(p.stock) >= 3 and not self.game_over:
            pos_names = ["前列左", "前列中", "前列右", "後列左", "後列右"]
            pos_str = pos_names[slot_idx] if 0 <= slot_idx < 5 else f"位置 {slot_idx}"
            if p.is_ai:
                # AI 僅針對主力角色（Lv.2 以上，或 Lv.1 且基礎攻擊力 >= 5500 且能量充裕 >= 5）執行 3 費規則安可
                do_rule_enc = (card.base_level >= 2 and len(p.stock) >= 4) or (
                    card.base_level >= 1 and card.base_power >= 5500 and len(p.stock) >= 5
                )
            else:
                do_rule_enc = self.ask_yes_no_center(
                    f"♻️ 安可階段 — 規則 3 能量安可：【{card.name}】",
                    f"我方【{pos_str}】的【{card.name}】(Lv.{card.base_level} / 攻:{card.base_power}) 退場送入休息室！\n"
                    f"目前我方共有 {len(p.stock)} 點能量，是否支付 (3) 點能量發動『規則安可』，將【{card.name}】以【橫置】狀態放回【{pos_str}】？",
                )
            if do_rule_enc:
                self.pay_stock(p, 3)
                if card in p.waiting_room:
                    p.waiting_room.remove(card)
                card.state = "REST"
                p.stage[slot_idx] = card
                self.log(f"♻️ {p.name} 支付 (3) 點能量發動規則安可，【{card.name}】以【橫置】狀態回到【{pos_str}】！")
                self.update_ui()

    def resolve_standby(self, p: PlayerState, source_cx_id: str, current_atk_slot: int = None):
        max_lvl = len(p.level_zone) + 1
        valid_chars = [
            c for c in p.waiting_room if c.type == "CHAR" and c.base_level <= max_lvl
        ]
        if not valid_chars:
            self.log(f"⚙️ {p.name} 觸發開機，但休息室無等級 {max_lvl} 以下的角色。")
            return

        if p.is_ai:
            support_ids = {
                "BFR/S78-031",
                "BFR/S78-102",
                "BFR/S78-061",
                "GA10/S131-012",
                "GA17/S131-014",
                "BTR/W107-T02",
                "BTR/W107-T13",
                "BTR/W107-046",
            }
            chosen = max(valid_chars, key=lambda x: (x.id not in support_ids, x.base_level, x.base_power))
            empty_front = [i for i in [0, 1, 2] if p.stage[i] is None]
            empty_back = [i for i in [3, 4] if p.stage[i] is None]
            rev_or_rest_front = [
                i
                for i in [0, 1, 2]
                if i != current_atk_slot and p.stage[i] and p.stage[i].state == "REVERSE"
            ]
            if chosen.id in support_ids and empty_back:
                slot = empty_back[0]
            elif empty_front:
                slot = empty_front[0]
            elif empty_back:
                slot = empty_back[0]
            elif rev_or_rest_front:
                slot = rev_or_rest_front[0]
            else:
                slot = 3
        else:
            chosen = self.choose_card_dialog(
                f"開機效果：請從休息室選擇 1 張等級 {max_lvl} 以下的角色橫置登場",
                valid_chars,
                allow_cancel=True,
            )
            if not chosen:
                return
            while True:
                slot = self.select_stage_slot_dialog(
                    p,
                    [0, 1, 2, 3, 4],
                    f"請選擇【{chosen.name}】要放置的舞台格子",
                    allow_cancel=True,
                )
                if slot is None:
                    return
                if p.stage[slot] is not None:
                    old_c = p.stage[slot]
                    confirm_over = self.ask_yes_no_center(
                        "⚠️ 壓卡覆蓋確認",
                        f"該位置目前已有【{old_c.name}】！\n確定要將【{old_c.name}】壓掉送入休息室，改由【{chosen.name}】登場嗎？",
                    )
                    if not confirm_over:
                        continue
                break

        if chosen in p.waiting_room:
            p.waiting_room.remove(chosen)
        if p.stage[slot] is not None:
            self.send_stage_to_wr(p, slot, is_overwritten=True)
        if chosen in p.waiting_room:
            p.waiting_room.remove(chosen)
        if current_atk_slot is not None and slot == current_atk_slot:
            self._current_attack_slot_overwritten = True
        chosen.reset_stage_state()
        chosen.state = "REST"
        p.stage[slot] = chosen
        self.log(f"⚙️ 開機登場：{p.name} 將休息室的【{chosen.name}】以【橫置】狀態放置到舞台位置 {slot}！")
        self.update_ui()

        if chosen.id == "BFR/S78-064" and source_cx_id == "BFR/S78-078":
            game_in_hand = [c for c in p.hand if c.type == "CHAR" and "遊戲" in c.traits]
            if len(game_in_hand) >= 3:
                do_combo = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "炎帝 蜜伊 CX連動",
                        "【炎帝 蜜伊】因「炎帝之國的公會長」效果登場！\n是否捨棄手牌 3 張《遊戲》角色將此卡【正置】？",
                    )
                )
                if do_combo:
                    for n in range(3):
                        self.select_hand_discard(
                            p,
                            filter_fn=lambda x: x.type == "CHAR" and "遊戲" in x.traits,
                            prompt=f"炎帝 蜜伊連動：請選擇捨棄第 {n+1}/3 張《遊戲》角色",
                        )
                    chosen.state = "STAND"
                    self.log("🔥 CX連動發動！【炎帝 蜜伊】直接【正置】！")
                    self.update_ui()

    # ------------------------------------------
    # 對戰流程控制（支援單人 VS AI 與雙人真人連線同步）
    # ------------------------------------------
    def start_game(self):
        if self.is_lan and self.net_node and self.net_node.connected:
            self.log("🌐 正在與連線對手同步玩家名稱、王牌與卡組資料...")
            self.net_node.send({
                "type": "HELLO_SYNC",
                "player_name": self.player.name,
                "ace_cid": self.player.ace_cid,
                "sleeve_style": self.player_sleeve_style,
                "custom_sleeve_b64": self._encode_my_custom_sleeve_b64(),
                "sender_state": self.player.to_sync_dict(),
            })
            if self.net_node.is_host:
                def _retry_hello_req():
                    if self.winfo_exists() and not self.game_over and not self._lan_host_duel_started and self.net_node and self.net_node.connected:
                        self.net_node.send({"type": "HELLO_REQ"})
                self.root.after(450, _retry_hello_req)
            return

        # 單人模式：進行雙方王牌二選一翻牌決定先後手，並抽起手 5 張牌
        ace_setup = self._generate_ace_flip_setup(is_lan_mode=False)
        self.draw_cards(self.player, 5)
        self.draw_cards(self.ai, 5)
        ai_keep = [c for c in self.ai.hand if c.type == "CHAR" and c.base_level == 0]
        ai_drop = [c for c in self.ai.hand if c not in ai_keep]
        for c in ai_drop:
            self.ai.hand.remove(c)
            self.ai.waiting_room.append(c)
        self.draw_cards(self.ai, len(ai_drop))

        self.log("=== 對戰開始！ ===")
        self.update_ui()
        self.root.after(
            200,
            lambda: self.prompt_initial_setup(ace_setup=ace_setup),
        )

    def _host_start_lan_duel_setup(self):
        # 由房主產生雙方王牌二選一翻牌設定與起手 5 張發牌，並同步給 Client
        host_setup = self._generate_ace_flip_setup(is_lan_mode=True)
        self.draw_cards(self.player, 5)
        self.draw_cards(self.ai, 5)

        client_slots = []
        for s in host_setup["slots"]:
            client_slots.append({
                "owner_role": "OPP" if s["owner_role"] == "ME" else "ME",
                "owner_name": s["owner_name"],
                "cid": s["cid"],
                "card_name": s["card_name"],
            })
        client_setup = {
            "slots": client_slots,
            "flipper_is_me": (not host_setup["flipper_is_me"]),
        }
        if self.net_node and self.net_node.connected:
            self.net_node.send({
                "type": "INIT_DUEL_SYNC",
                "host_name": self.player.name,
                "client_name": self.ai.name,
                "host_sleeve_style": self.player_sleeve_style,
                "host_custom_sleeve_b64": self._encode_my_custom_sleeve_b64(),
                "ace_setup": client_setup,
                "host_state": self.player.to_sync_dict(),
                "client_state": self.ai.to_sync_dict(),
            })
        self.update_ui()
        self._run_lan_turn_order_phase(host_setup)

    def _run_lan_turn_order_phase(self, ace_setup: dict):
        if self.game_over:
            return
        self._lan_turn_order_chosen = None
        order = self.ask_ace_card_turn_order_center(
            ace_setup, is_lan_mode=True
        )
        if self.game_over:
            return
        first_is_me = order == "FIRST"
        self.first_player = self.player if first_is_me else self.ai
        self.log(f"👑 先後手決定：由【{self.first_player.name}】先攻！")
        self.update_ui()
        self._run_mulligan_phase()

    def prompt_initial_setup(self, ace_setup=None):
        if self.game_over:
            return
        if ace_setup is None:
            ace_setup = self._generate_ace_flip_setup(is_lan_mode=False)
        order = self.ask_ace_card_turn_order_center(
            ace_setup, is_lan_mode=False
        )
        if self.game_over:
            return
        if order == "FIRST":
            self.first_player = self.player
            self.log(f"👑 先後手決定：抽中我方王牌，由【{self.player.name}】固定獲得先攻！")
        else:
            self.first_player = self.ai
            self.log(f"👑 先後手決定：抽中對手王牌，由【{self.ai.name}】固定獲得先攻，{self.player.name}後攻！")
        self.update_ui()
        self._run_mulligan_phase()

    def _run_mulligan_phase(self):
        self.phase = "MULLIGAN"
        self.update_ui()
        drop_indices = self.ask_mulligan_multi_center()
        if self.game_over:
            return
        if drop_indices:
            dropped_names = []
            for idx in drop_indices:
                c = self.player.hand.pop(idx)
                self.player.waiting_room.append(c)
                dropped_names.append(c.name)
            self.draw_cards(self.player, len(drop_indices))
            self.log(
                f"🔄 {self.player.name} 起手替換了 {len(drop_indices)} 張牌（{', '.join(dropped_names)}）。"
            )
        else:
            self.log(f"🔄 {self.player.name} 選擇保留全部 5 張起手牌。")

        if self.is_lan and self.net_node and self.net_node.connected:
            self._lan_my_mulligan_done = True
            self.net_node.send({
                "type": "MULLIGAN_SYNC",
                "sender_state": self.player.to_sync_dict(),
            })
            if not self._lan_peer_mulligan_done:
                def _wait_mul(frame):
                    tk.Label(
                        frame,
                        text=f"⏳ 等待對手【{self.ai.name}】完成起手換牌...",
                        bg="#1e2230",
                        fg="#ffd166",
                        font=("Microsoft JhengHei", 15, "bold"),
                    ).pack(pady=80)
                self._show_overlay_and_wait(_wait_mul)

        self.start_turn(self.first_player)

    def start_turn(self, p: PlayerState):
        if self.game_over:
            return
        self.active_player = p
        self.attacks_this_turn = 0
        self.app.sound_mgr.play_bgm("bgm_main")
        self.selected_hand_idx = None
        self.selected_stage_idx = None
        first_turn_note = " (先攻首回合僅限攻擊 1 次)" if self.turn_count == 1 else ""
        self.log(
            f"\n================ 第 {self.turn_count} 回合：{p.name}{first_turn_note} ================"
        )

        for c in p.stage:
            if c:
                c.state = "STAND"

        if self.is_lan and p == self.ai:
            self.phase = "OPP_TURN"
            self.log(f"⏳ 輪到對手【{self.ai.name}】的回合，等待對手行動...")
            self.update_ui()
            return

        # 處理第一章/第二章 伊蕾娜預約於下次抽牌階段開始時從回憶區登場的效果
        if p.pending_draw_phase_spawns:
            spawns = list(p.pending_draw_phase_spawns)
            p.pending_draw_phase_spawns.clear()
            for target_cid in spawns:
                mem_matches = [c for c in p.memory if c.id == target_cid]
                if mem_matches:
                    spawn_c = mem_matches[0]
                    do_sp = (
                        True
                        if p.is_ai
                        else self.ask_yes_no_center(
                            "伊蕾娜記憶傳承登場",
                            f"抽牌階段開始！是否將回憶區的【{spawn_c.name}】放置到舞台上任意格子？",
                        )
                    )
                    if do_sp:
                        if p.is_ai:
                            empty_front = [i for i in [0, 1, 2] if p.stage[i] is None]
                            slot = empty_front[0] if empty_front else 0
                        else:
                            slot = self.select_stage_slot_dialog(
                                p, [0, 1, 2, 3, 4], f"選擇【{spawn_c.name}】要登場的舞台格子", allow_cancel=True
                            )
                        if slot is not None:
                            p.memory.remove(spawn_c)
                            if p.stage[slot] is not None:
                                self.send_stage_to_wr(p, slot, is_overwritten=True)
                            spawn_c.reset_stage_state()
                            spawn_c.entered_stage_this_turn = True
                            p.stage[slot] = spawn_c
                            self.log(f"🪄 {p.name} 於抽牌階段開始時將回憶區的【{spawn_c.name}】登場於位置 {slot}！")
                            self.update_ui()

        self.draw_cards(p, 1)
        if self.game_over:
            return

        if p.is_ai:
            self.phase = "AI_CLOCK"
            self.update_ui()
            self.root.after(900, self.ai_step_clock)
        else:
            self.phase = "CLOCK"
            self.log("⏰ 進入【時計階段】：請從選單選擇是否置入 1 張手牌到時計區抽 2 張牌（痛一抽二），或選擇不放置直接進入主要階段。")
            self.update_ui()
            self.root.after(80, self.prompt_clock_phase_dialog)

    def prompt_clock_phase_dialog(self):
        """時計階段（痛一抽二）專屬選單：可直觀點選 1 張手牌置入時計區抽 2 張，或點擊『不放置（直接進入主要階段）』"""
        if self.game_over or self.active_player != self.player or self.phase != "CLOCK":
            return
        if not self.player.hand:
            self.log("⏰ 我方目前無手牌可置入時計區，直接進入【主要階段】。")
            self.enter_main_phase(self.player)
            return

        choice = {"hand_idx": None}
        sel_state = {"idx": 0}

        def build(frame):
            tk.Label(
                frame,
                text="⏰ 【時計階段】是否將 1 張手牌放到時計區並抽 2 張牌？（痛一抽二）",
                bg="#1e2230",
                fg="#ffd166",
                font=("Microsoft JhengHei", 15, "bold"),
            ).pack(pady=(10, 2))

            tk.Label(
                frame,
                text="💡 點選下方任一張手牌即可預覽效果，再按下方按鈕執行痛一抽二，或選擇「不放置」直接進入主要階段：",
                bg="#1e2230",
                fg="#8ecae6",
                font=("Microsoft JhengHei", 11, "bold"),
            ).pack(pady=(0, 6))

            # 優先將底部雙按鈕列固定於視窗最底部 (side=tk.BOTTOM)，絕不裁切
            btn_bar = tk.Frame(frame, bg="#1e2230")
            btn_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 14))

            btn_box = tk.Frame(btn_bar, bg="#1e2230")
            btn_box.pack()

            btn_confirm_clock = tk.Button(
                btn_box,
                text="⏰ 置入選中手牌並抽 2 張（痛一抽二）",
                bg="#f4a261",
                fg="#000000",
                font=("Microsoft JhengHei", 12, "bold"),
                padx=22,
                pady=7,
                cursor="hand2",
                command=lambda: [
                    choice.update({"hand_idx": sel_state["idx"]}),
                    self._close_overlay(),
                ],
            )
            btn_confirm_clock.pack(side=tk.LEFT, padx=12)

            tk.Button(
                btn_box,
                text="⏩ 不放置手牌（直接進入主要階段）",
                bg="#06d6a0",
                fg="#000000",
                font=("Microsoft JhengHei", 12, "bold"),
                padx=22,
                pady=7,
                cursor="hand2",
                command=lambda: [
                    choice.update({"hand_idx": None}),
                    self._close_overlay(),
                ],
            ).pack(side=tk.LEFT, padx=12)

            canvas = tk.Canvas(frame, bg="#141824", height=255, highlightthickness=0)
            sc = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
            inner = tk.Frame(canvas, bg="#141824")
            inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=inner, anchor="nw")
            canvas.configure(xscrollcommand=sc.set)
            sc.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=(0, 4))
            canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=4)

            btns = []

            def select_idx(i):
                sel_state["idx"] = i
                c_sel = self.player.hand[i]
                self.inspect_card(c_sel, self.player, None, open_drawer=False)
                btn_confirm_clock.config(text=f"⏰ 將【{c_sel.name[:8]}】置入時計區並抽 2 張")
                for b_i, b_w in enumerate(btns):
                    is_s = b_i == i
                    b_w.config(
                        bg="#f4a261" if is_s else "#23293d",
                        fg="#000000" if is_s else "#ffffff",
                    )

            for idx, hc in enumerate(self.player.hand):
                c_img = self.img_mgr.get_card_visual(
                    getattr(hc, "skin_id", hc.id), 102, 142, is_selected=(idx == 0)
                )
                b = tk.Button(
                    inner,
                    image=c_img,
                    text=f"{hc.name[:8]}\nLv.{hc.base_level}｜{hc.color}色",
                    compound=tk.TOP,
                    bg="#f4a261" if idx == 0 else "#23293d",
                    fg="#000000" if idx == 0 else "#ffffff",
                    font=("Microsoft JhengHei", 9, "bold"),
                    width=114,
                    height=184,
                    bd=2,
                    relief=tk.RAISED,
                    cursor="hand2",
                    command=lambda i=idx: select_idx(i),
                )
                b.image = c_img
                b.pack(side=tk.LEFT, padx=7, pady=10)
                btns.append(b)
                b.bind("<MouseWheel>", lambda e: canvas.xview_scroll(-1 if e.delta > 0 else 1, "units"))

            canvas.bind("<MouseWheel>", lambda e: canvas.xview_scroll(-1 if e.delta > 0 else 1, "units"))
            if self.player.hand:
                select_idx(0)

        self._show_overlay_and_wait(
            build, custom_place={"relx": 0.5, "rely": 0.45, "width": 860, "height": 450}
        )
        if self.game_over or self.active_player != self.player or self.phase != "CLOCK":
            return

        picked_idx = choice["hand_idx"]
        if picked_idx is not None and 0 <= picked_idx < len(self.player.hand):
            self.selected_hand_idx = picked_idx
            self.on_use_selected_hand()
        else:
            self.log("⏰ 玩家於【時計階段】選擇不放置手牌，直接進入【主要階段】。")
            self.enter_main_phase(self.player)

    def enter_main_phase(self, p: PlayerState):
        self.phase = "MAIN"
        self.app.sound_mgr.play_bgm("bgm_main")
        self.log("🎴 進入【主要階段】。")
        mem_events = [c for c in p.memory if c.id == "BFR/S78-075"]
        for ev in mem_events:
            game_chars = [c for c in p.hand if c.type == "CHAR" and "遊戲" in c.traits]
            if game_chars:
                do_ret = (
                    False
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "記憶效果：獨有系列",
                        "主要階段開始，回憶區有【獨有系列】。\n是否捨棄手牌 1 張《遊戲》角色將【獨有系列】返回手牌？",
                    )
                )
                if do_ret:
                    self.select_hand_discard(
                        p,
                        filter_fn=lambda x: x.type == "CHAR" and "遊戲" in x.traits,
                        prompt="請選擇要捨棄的《遊戲》角色",
                    )
                    p.memory.remove(ev)
                    p.hand.append(ev)
                    self.log(f"♻️ {p.name} 發動記憶效果，將回憶區的【獨有系列】收回手牌！")
        self.update_ui()

    def enter_attack_phase(self, p: PlayerState):
        self.phase = "ATTACK"
        self.app.sound_mgr.play_bgm("bgm_battle")
        self.log("⚔️ 進入【戰鬥階段】！")
        opp = self.ai if p == self.player else self.player
        # BTR/W107-046《打卡美照 喜多郁代》：當對手的攻擊階段開始時，你可以將此卡移動到後列沒有角色的格子
        for s_idx in [0, 1, 2, 3, 4]:
            opp_c = opp.stage[s_idx]
            if opp_c and (opp_c.has_effect("AUTO_OPP_ATK_START_MOVE_BACK") or opp_c.id == "BTR/W107-046") and not opp_c.cannot_move:
                empty_back = [b_i for b_i in [3, 4] if opp.stage[b_i] is None and b_i != s_idx]
                if empty_back and s_idx in [0, 1, 2]:
                    do_mv_back = (
                        True
                        if opp.is_ai
                        else self.ask_yes_no_center(
                            "打卡美照 喜多郁代",
                            "對手的攻擊階段開始！是否將前列的【打卡美照 喜多郁代】移動到後列沒有角色的格子？",
                        )
                    )
                    if do_mv_back:
                        dst_b = (
                            empty_back[0]
                            if (opp.is_ai or len(empty_back) == 1)
                            else self.select_stage_slot_dialog(
                                opp, empty_back, "打卡美照 喜多郁代：選擇要移動過去的後列空位"
                            )
                        )
                        if dst_b is not None and opp.stage[dst_b] is None:
                            opp.stage[dst_b] = opp_c
                            opp.stage[s_idx] = None
                            self.log(f"📸 {opp.name} 的【打卡美照 喜多郁代】於對手攻擊階段開始時移動至後列位置 {dst_b}！")
                            self.update_ui()
        if p.climax_zone and p.climax_zone.id == "BFR/S78-076":
            for i in [0, 1, 2]:
                c = p.stage[i]
                if c and c.id == "BFR/S78-057":
                    copy_in_hand = [h for h in p.hand if h.id == "BFR/S78-057"]
                    if copy_in_hand and p.climax_zone:
                        do_c = (
                            True
                            if p.is_ai
                            else self.ask_yes_no_center(
                                "移動要塞 梅普露 CX連動",
                                "攻擊階段開始！是否捨棄手牌 1 張「移動要塞 梅普露」並將名場面「公會長之間的對決」送入休息室，正置 1 隻其他《遊戲》角色並從休息室回收 1 張《遊戲》角色？",
                            )
                        )
                        if do_c:
                            disc = copy_in_hand[0]
                            p.hand.remove(disc)
                            p.waiting_room.append(disc)
                            cx = p.climax_zone
                            p.climax_zone = None
                            p.waiting_room.append(cx)

                            other_indices = [
                                idx
                                for idx in range(5)
                                if idx != i
                                and p.stage[idx]
                                and "遊戲" in p.stage[idx].traits
                                and p.stage[idx].state != "STAND"
                            ]
                            if other_indices:
                                target_slot = (
                                    other_indices[0]
                                    if p.is_ai
                                    else self.select_stage_slot_dialog(
                                        p, other_indices, "選擇要【正置】的其他《遊戲》角色"
                                    )
                                )
                                p.stage[target_slot].state = "STAND"
                                self.log(f"✨ 【{p.stage[target_slot].name}】透過連動效果【正置】！")

                            wr_chars = [
                                w for w in p.waiting_room if w.type == "CHAR" and "遊戲" in w.traits
                            ]
                            if wr_chars:
                                rec = (
                                    wr_chars[-1]
                                    if p.is_ai
                                    else self.choose_card_dialog(
                                        "選擇要從休息室回收的《遊戲》角色", wr_chars, allow_cancel=True
                                    )
                                )
                                if rec:
                                    p.waiting_room.remove(rec)
                                    p.hand.append(rec)
                                    self.log(f"📥 {p.name} 從休息室回收了【{rec.name}】！")
                            break
        self.update_ui()

    def _resolve_player_encore_step(self, target_p: PlayerState):
        """結算指定玩家於安可階段場上所有【倒置】角色的退場與安可（手牌安可 / 1費1手安可 / 3能量規則安可）"""
        for idx in range(5):
            c = target_p.stage[idx]
            if c and c.cannot_be_reversed and c.state == "REVERSE":
                c.state = "REST"
            if c and c.state == "REVERSE" and not c.cannot_be_reversed:
                self.log(f"💀 [安可階段] {target_p.name} 的倒置角色【{c.name}】送入休息室（檢定安可時機）。")
                self.send_stage_to_wr(target_p, idx)

    def end_turn(self):
        if self.game_over:
            return
        p = self.active_player
        opp = self.ai if p == self.player else self.player

        # 1. 先進入【安可階段 (ENCORE)】：處理戰鬥階段結束後場上所有倒置角色退場與安可復活（含 3 能量規則安可）
        self.phase = "ENCORE"
        self.log("♻️ 戰鬥階段結束，進入【安可階段】：結算倒置角色退場與安可（可支付 3 點能量或角色專屬安可代價橫置回場）...")
        self.update_ui()

        # 先由回合玩家結算自己的倒置角色安可
        self._resolve_player_encore_step(p)

        # 再由非回合玩家結算倒置角色安可（若為雙人連線且對手場上有倒置角色，同步請對手於本地視窗選擇是否安可）
        opp_has_reversed = any(
            c and c.state == "REVERSE" and not c.cannot_be_reversed for c in opp.stage
        )
        if opp_has_reversed:
            if self.is_lan and opp == self.ai and self.net_node and self.net_node.connected:
                self.net_node.send({
                    "type": "ENCORE_REQ",
                    "sender_state": self.player.to_sync_dict(),
                    "receiver_state": self.ai.to_sync_dict(),
                })
                def _wait_enc(frame):
                    tk.Label(
                        frame,
                        text=f"⏳ 安可階段：等待對手【{self.ai.name}】確認倒置角色是否發動安可...",
                        bg="#1e2230",
                        fg="#ffd166",
                        font=(self.app.get_font_family(), 15, "bold"),
                    ).pack(pady=80)
                self._show_overlay_and_wait(_wait_enc)
            else:
                self._resolve_player_encore_step(opp)

        # 2. 進入【結束階段 (END)】
        self.phase = "END"
        self.log("🌙 進入【結束階段】...")
        self.update_ui()

        # GA17/S131-010《第三章 伊蕾娜》回合結束時放到回憶區
        for player_obj in [p, opp]:
            for idx in range(5):
                c = player_obj.stage[idx]
                if c and (c.has_effect("AUTO_SEND_TO_MEMORY_ON_REV_OR_END") or c.id == "GA17/S131-010"):
                    if not c.cannot_go_memory:
                        player_obj.stage[idx] = None
                        if c.markers:
                            player_obj.waiting_room.extend(c.markers)
                            c.markers.clear()
                        c.reset_stage_state()
                        player_obj.memory.append(c)
                        self.log(f"🪄 回合結束，{player_obj.name} 的【{c.name}】返回回憶區。")

        if p.climax_zone:
            p.waiting_room.append(p.climax_zone)
            p.climax_zone = None

        for player_obj in [p, opp]:
            for c in player_obj.stage:
                if c:
                    c.temp_power = 0
                    c.temp_soul = 0
                    c.temp_level = 0
                    c.cannot_return_hand = False
                    c.cannot_go_memory = False
                    c.cannot_be_reversed = False
                    c.used_act_buff_turn = False
                    c.entered_stage_this_turn = False
                    c.anti_early_play_stock_bomb = False
                    c.used_memory_minus_soul_turn = False
                    c.clock_kick_on_reverse = False
                    c.salvage_music_on_reverse = False
                    if player_obj == p:
                        c.cannot_move = False

        while len(p.hand) > 7 and not self.game_over:
            self.select_hand_discard(p, prompt="手牌超過 7 張，請選擇捨棄至 7 張")

        self.turn_count += 1
        self.update_ui()
        if self.is_lan and self.net_node and self.net_node.connected:
            self.net_node.send({
                "type": "TURN_PASS",
                "turn_count": self.turn_count,
                "sender_state": self.player.to_sync_dict(),
                "receiver_state": self.ai.to_sync_dict(),
            })
            self.start_turn(self.ai)
            return

        next_p = self.ai if p == self.player else self.player
        self.root.after(600, lambda: self.start_turn(next_p))

    def on_next_phase(self):
        if self.game_over or self.active_player != self.player or getattr(self, "_overlay_is_waiting", False):
            return
        if self.phase == "CLOCK":
            self.enter_main_phase(self.player)
        elif self.phase == "MAIN":
            self.phase = "CLIMAX"
            self.log("🌟 進入【名場面階段】：可從手牌打出 1 張名場面卡，或按『進入下一階段』進入攻擊。")
            self.update_ui()
        elif self.phase == "CLIMAX":
            self.enter_attack_phase(self.player)
        elif self.phase == "ATTACK":
            self.end_turn()

    # ------------------------------------------
    # 玩家手牌與舞台操作
    # ------------------------------------------
    # ------------------------------------------
    # 滑鼠左鍵按住拖移上場與舞台交換機制
    # ------------------------------------------
    def _on_hand_btn_command(self, idx: int):
        if self._drag_state.get("just_dragged"):
            self._drag_state["just_dragged"] = False
            return
        self.on_click_hand(idx)

    def _on_stage_btn_command(self, slot_idx: int):
        if self._drag_state.get("just_dragged"):
            self._drag_state["just_dragged"] = False
            return
        self.on_click_player_stage(slot_idx)

    def _on_hand_press(self, event, idx: int):
        if self.game_over or idx >= len(self.player.hand):
            return
        card = self.player.hand[idx]
        self.inspect_card(card, self.player, None, open_drawer=False)
        if self.center_overlay.winfo_ismapped() or getattr(self, "_overlay_is_waiting", False):
            return
        self._drag_state = {
            "source": "HAND",
            "index": idx,
            "card": card,
            "start_x": event.x_root,
            "start_y": event.y_root,
            "dragging": False,
            "ghost": None,
            "just_dragged": False,
        }

    def _on_stage_press(self, event, slot_idx: int):
        if self.game_over:
            return
        card = self.player.stage[slot_idx]
        if card:
            self.inspect_card(card, self.player, slot_idx, open_drawer=False)
        if self.center_overlay.winfo_ismapped() or getattr(self, "_overlay_is_waiting", False):
            return
        if not card:
            return
        self._drag_state = {
            "source": "STAGE",
            "index": slot_idx,
            "card": card,
            "start_x": event.x_root,
            "start_y": event.y_root,
            "dragging": False,
            "ghost": None,
            "just_dragged": False,
        }

    def _on_drag_motion(self, event):
        st = self._drag_state
        if not st.get("source") or not st.get("card"):
            return
        dx = abs(event.x_root - st["start_x"])
        dy = abs(event.y_root - st["start_y"])
        if not st["dragging"] and (dx > 6 or dy > 6):
            st["dragging"] = True
            card = st["card"]
            g_img = self.img_mgr.get_card_visual(getattr(card, "skin_id", card.id), 78, 108, state="STAND", is_selected=True)
            ghost = tk.Label(
                self,
                image=g_img,
                text=f"拖移：{card.name[:6]}",
                compound=tk.TOP,
                bg="#ffd166",
                fg="#000000",
                font=("Microsoft JhengHei", 9, "bold"),
                bd=2,
                relief=tk.SOLID,
                padx=3,
                pady=2,
            )
            ghost.image = g_img
            st["ghost"] = ghost

        if st["dragging"] and st.get("ghost"):
            rel_x = event.x_root - self.winfo_rootx() - 40
            rel_y = event.y_root - self.winfo_rooty() - 55
            st["ghost"].place(x=rel_x, y=rel_y)
            st["ghost"].lift()

    def _find_drop_target(self, x_root: int, y_root: int):
        def is_inside(widget):
            if not widget or not widget.winfo_ismapped():
                return False
            wx = widget.winfo_rootx()
            wy = widget.winfo_rooty()
            ww = widget.winfo_width()
            wh = widget.winfo_height()
            return wx <= x_root <= wx + ww and wy <= y_root <= wy + wh

        for idx in range(5):
            if is_inside(self.btn_p_stage[idx]):
                return ("P_STAGE", idx)
        for idx in range(5):
            if is_inside(self.btn_ai_stage[idx]):
                return ("AI_STAGE", idx)
        if is_inside(self.btn_p_clock):
            return ("P_CLOCK", 0)
        if is_inside(self.btn_p_cx):
            return ("P_CX", 0)
        return (None, None)

    def _on_drag_release(self, event):
        st = self._drag_state
        ghost = st.get("ghost")
        if ghost and ghost.winfo_exists():
            ghost.destroy()
        st["ghost"] = None

        if not st.get("dragging"):
            st["source"] = None
            return

        st["dragging"] = False
        st["just_dragged"] = True
        self.selected_stage_idx = None
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()
        src = st.get("source")
        idx = st.get("index")
        card = st.get("card")
        st["source"] = None

        if self.game_over or self.active_player != self.player:
            return

        target_type, target_idx = self._find_drop_target(event.x_root, event.y_root)
        if not target_type:
            return

        if src == "HAND" and idx is not None and idx < len(self.player.hand):
            if self.phase == "MAIN" and card.type == "CHAR" and target_type == "P_STAGE":
                self.play_character_from_hand(self.player, idx, target_idx)
            elif self.phase == "MAIN" and card.type == "EVENT" and target_type == "P_STAGE":
                if is_counter_only_event(card):
                    self.show_info_center(
                        "反擊事件使用時機限制",
                        f"【{card.name}】為【反擊】專用事件卡，不能在主要階段主動發動！\n請在對手角色宣告正面攻擊我方角色時的【反擊步驟（助太刀時機）】選發。",
                    )
                    return
                if not self.can_play_card(self.player, card):
                    self.show_info_center("無法使用", "等級、費用或顏色條件不足！")
                    return
                self.selected_hand_idx = idx
                self.on_use_selected_hand()
            elif self.phase == "CLIMAX" and card.type == "CX" and target_type in ("P_CX", "P_STAGE"):
                self.selected_hand_idx = idx
                self.on_use_selected_hand()
            elif self.phase == "CLOCK" and target_type == "P_CLOCK":
                self.selected_hand_idx = idx
                self.on_use_selected_hand()

        elif src == "STAGE" and idx is not None:
            if self.phase == "MAIN" and target_type == "P_STAGE" and target_idx != idx:
                if (self.player.stage[idx] and self.player.stage[idx].cannot_move) or (
                    self.player.stage[target_idx] and self.player.stage[target_idx].cannot_move
                ):
                    self.show_info_center("無法移動", "該角色受到效果封鎖，無法移動到其他舞台格子！")
                    return
                pos_names = ["前列左", "前列中", "前列右", "後列左", "後列右"]
                self.player.stage[idx], self.player.stage[target_idx] = (
                    self.player.stage[target_idx],
                    self.player.stage[idx],
                )
                self.selected_stage_idx = target_idx
                self.log(f"🔄 玩家將【{pos_names[idx]}】與【{pos_names[target_idx]}】交換位置。")
                self._broadcast_action(f"交換舞台位置 {pos_names[idx]} 與 {pos_names[target_idx]}")
                self.update_ui()
            elif (
                self.phase == "ATTACK"
                and idx in [0, 1, 2]
                and target_type == "AI_STAGE"
                and self.player.stage[idx]
                and self.player.stage[idx].state == "STAND"
            ):
                if self.turn_count == 1 and self.attacks_this_turn >= 1:
                    self.show_info_center("先攻首回合限制", "依 WS 規則，先攻玩家的第 1 個回合只能進行 1 次攻擊！")
                    return
                self.initiate_attack(self.player, idx)

    def on_click_hand(self, idx):
        if idx >= len(self.player.hand):
            return
        card = self.player.hand[idx]
        self.inspect_card(card, self.player, None)
        if getattr(self, "_overlay_is_waiting", False):
            return
        # QoL 優化：手牌已經選定卡片時再按一次可以取消選擇
        if self.selected_hand_idx == idx:
            self.selected_hand_idx = None
        else:
            self.selected_hand_idx = idx
            self.selected_stage_idx = None
        self.update_ui()

    def on_use_selected_hand(self):
        if getattr(self, "_overlay_is_waiting", False):
            return
        if self.active_player == self.player and self.phase == "CLOCK" and self.selected_hand_idx is None:
            self.prompt_clock_phase_dialog()
            return
        if self.selected_hand_idx is None or self.active_player != self.player:
            return
        card = self.player.hand[self.selected_hand_idx]

        if self.phase == "CLOCK":
            self.player.hand.pop(self.selected_hand_idx)
            self.selected_hand_idx = None
            self.player.clock.append(card)
            self.log(f"⏰ 玩家將【{card.name}】置入時鐘傷害區，抽取 2 張牌。")
            self._broadcast_action(f"將【{card.name}】置入時鐘區並抽 2 張牌")
            self.check_level_up(self.player)
            if not self.game_over:
                self.draw_cards(self.player, 2)
                if not self.game_over:
                    self.enter_main_phase(self.player)
            return

        if self.phase == "MAIN" and card.type == "EVENT":
            if is_counter_only_event(card):
                self.show_info_center(
                    "反擊事件使用時機限制",
                    f"【{card.name}】為【反擊】專用事件卡，不能在主要階段發動！\n當對手角色正面攻擊時，系統會在反擊步驟自動詢問你是否發動。",
                )
                return
            if not self.can_play_card(self.player, card):
                self.show_info_center("無法使用", "等級、費用或顏色條件不足！")
                return
            # BTR/W107-T10《樂團名「團結Band」》：從牌組選擇《音樂》角色或名場面最多 1 張加入手牌並洗牌
            if card.has_effect("EVENT_SEARCH_MUSIC_OR_CX") or card.id == "BTR/W107-T10":
                self.pay_stock(self.player, card.cost)
                self.player.hand.pop(self.selected_hand_idx)
                self.selected_hand_idx = None
                self.player.waiting_room.append(card)
                valid_targets = [
                    c
                    for c in self.player.deck
                    if (c.type == "CHAR" and "音樂" in c.traits) or c.type == "CX"
                ]
                if valid_targets:
                    chosen = self.choose_card_dialog(
                        "樂團名「團結Band」：從牌組選擇最多 1 張《音樂》角色或名場面加入手牌",
                        valid_targets,
                        allow_cancel=True,
                    )
                    if chosen:
                        self.remove_card_from_deck(self.player, chosen)
                        self.player.hand.append(chosen)
                        self.log(f"🎸 玩家使用事件【{card.name}】，從牌組檢索【{chosen.name}】加入手牌！")
                        self._broadcast_action(f"使用事件【{card.name}】檢索【{chosen.name}】")
                else:
                    self.log(f"🎸 玩家使用事件【{card.name}】，但牌組中無符合條件的卡片。")
                random.shuffle(self.player.deck)
                self.update_ui()
                return

        if self.phase == "MAIN" and card.type == "CHAR":
            if not self.can_play_card(self.player, card):
                self.show_info_center("無法登場", "等級、能量費用或顏色條件不足！")
                return
            slot = self.select_stage_slot_dialog(
                self.player,
                [0, 1, 2, 3, 4],
                f"請選擇【{card.name}】要登場的舞台格子",
                allow_cancel=True,
            )
            if slot is not None:
                self.play_character_from_hand(self.player, self.selected_hand_idx, slot)
            return

        if self.phase == "CLIMAX" and card.type == "CX":
            if self.player.climax_zone is not None:
                self.show_info_center("無法使用", "本回合已打出過名場面卡！")
                return
            if not self.can_play_card(self.player, card):
                self.show_info_center(
                    "顏色條件不符", "等級區或傷害區需要有對應顏色！"
                )
                return
            self.play_climax_from_hand(self.player, self.selected_hand_idx)

    def play_climax_from_hand(self, p: PlayerState, hand_idx: int):
        self.app.sound_mgr.play_sfx("sfx_climax")
        cx = p.hand.pop(hand_idx)
        self.selected_hand_idx = None
        p.climax_zone = cx
        self.log(f"🌟 {p.name} 打出名場面卡：【{cx.name}】！")
        if not p.is_ai:
            self._broadcast_action(f"打出名場面【{cx.name}】")
        self.update_ui()

        if cx.has_effect("CX_STANDBY") or cx.id in [
            "BFR/S78-076",
            "BFR/S78-077",
            "BFR/S78-078",
            "BTR/W107-098",
            "BTR/W107-100",
        ]:
            self.resolve_standby(p, cx.id)

        # BTR/W107-T02《樂團的領導者 伊地知虹夏》：當你的黃色名場面放置到名場面區時，選擇自己 1 張角色攻擊力+1500
        if cx.color == "黃":
            for c in p.stage:
                if c and (c.has_effect("AUTO_ON_YELLOW_CX_BUFF_1500") or c.id == "BTR/W107-T02"):
                    my_slots = [i for i in range(5) if p.stage[i] is not None]
                    if my_slots:
                        t_s = (
                            my_slots[0]
                            if p.is_ai
                            else self.select_stage_slot_dialog(
                                p, my_slots, "樂團的領導者 伊地知虹夏：選擇 1 隻角色攻擊力 +1500"
                            )
                        )
                        p.stage[t_s].temp_power += 1500
                        self.log(f"🥁 【樂團的領導者 伊地知虹夏】使【{p.stage[t_s].name}】攻擊力 +1500！")

        # BTR/W107-075《晚霞的歸路 喜多郁代》CX 連動：當「成長與信賴的8小節」放置到名場面區時，前列有此卡且有其他《音樂》角色
        if cx.id == "BTR/W107-098":
            for f_i in [0, 1, 2]:
                c = p.stage[f_i]
                if c and c.id == "BTR/W107-075":
                    other_music = any(
                        idx != f_i and p.stage[idx] and "音樂" in p.stage[idx].traits
                        for idx in range(5)
                    )
                    if other_music:
                        c.temp_power += 1000
                        c.salvage_music_on_reverse = True
                        self.log(
                            "🌇 【晚霞的歸路 喜多郁代】發動 CX 連動！本回合攻擊力 +1000，並獲得『擊倒戰鬥對手時從休息室回收 1 張《音樂》角色』！"
                        )

        # GA17/S131-010《第三章 伊蕾娜》記憶 CX 連動：灰之魔女置入 CX 區且 Lv.3 以上時，[(2) 手牌1張放休息室] 從回憶區放到前列並造成 2 點傷害
        if cx.id == "GA17/S131-033" and len(p.level_zone) >= 3:
            opp = self.ai if p == self.player else self.player
            elaina_in_mem = [c for c in p.memory if c.id == "GA17/S131-010"]
            for el_card in elaina_in_mem:
                if len(p.stock) >= 2 and len(p.hand) >= 1 and not self.game_over:
                    do_el = (
                        True
                        if p.is_ai
                        else self.ask_yes_no_center(
                            "第三章 伊蕾娜 記憶CX連動",
                            "「灰之魔女」放置到名場面區！\n是否支付 (2) 能量並捨棄 1 張手牌，將回憶區的【第三章 伊蕾娜】放置到舞台前列，並給對手 2 點傷害？",
                        )
                    )
                    if do_el:
                        self.pay_stock(p, 2)
                        self.select_hand_discard(p, prompt="第三章 伊蕾娜連動：請選擇捨棄 1 張手牌")
                        if p.is_ai:
                            empty_f = [i for i in [0, 1, 2] if p.stage[i] is None]
                            f_slot = empty_f[0] if empty_f else 0
                        else:
                            f_slot = self.select_stage_slot_dialog(
                                p, [0, 1, 2], "選擇【第三章 伊蕾娜】要登場的前列格子", allow_cancel=False
                            )
                        if el_card in p.memory:
                            p.memory.remove(el_card)
                        if p.stage[f_slot] is not None:
                            self.send_stage_to_wr(p, f_slot, is_overwritten=True)
                        el_card.reset_stage_state()
                        el_card.entered_stage_this_turn = True
                        p.stage[f_slot] = el_card
                        self.log(f"🪄 【第三章 伊蕾娜】從回憶區飛躍登場於前列位置 {f_slot}，並對對手發動 2 點火焰傷害！")
                        self.update_ui()
                        self.deal_damage(opp, 2, source_text="第三章 伊蕾娜 記憶連動")

        for c in p.stage:
            if c and c.id == "BFR/S78-031" and len(p.hand) > 0:
                do_loot = (
                    False
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "多彩多樣 莎莉", "名場面放置到名場面區！是否捨棄 1 張手牌並抽 1 張牌？"
                    )
                )
                if do_loot:
                    self.select_hand_discard(p, prompt="多彩多樣 莎莉：請選擇捨棄 1 張手牌")
                    self.draw_cards(p, 1)
                    self.log(f"💧 {p.name} 發動【多彩多樣 莎莉】棄 1 抽 1！")
        self.update_ui()

    def play_character_from_hand(self, p: PlayerState, hand_idx: int, slot_idx: int):
        card = p.hand[hand_idx]
        if not self.can_play_card(p, card):
            if not p.is_ai:
                self.show_info_center("無法登場", "等級、能量費用或顏色條件不足！")
            return False

        if not p.is_ai and p.stage[slot_idx] is not None:
            existing_c = p.stage[slot_idx]
            pos_names = ["前列左", "前列中", "前列右", "後列左", "後列右"]
            confirm_over = self.ask_yes_no_center(
                "⚠️ 舞台壓卡確認",
                f"【{pos_names[slot_idx]}】目前已有角色【{existing_c.name}】！\n\n"
                f"確定要將【{existing_c.name}】壓掉送入休息室，改由【{card.name}】登場嗎？",
            )
            if not confirm_over:
                return False

        self.pay_stock(p, card.cost)
        p.hand.pop(hand_idx)
        self.selected_hand_idx = None
        self.selected_stage_idx = None
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()

        if p.stage[slot_idx] is not None:
            self.send_stage_to_wr(p, slot_idx, is_overwritten=True)

        card.reset_stage_state()
        card.entered_stage_this_turn = True
        p.stage[slot_idx] = card
        opp = self.ai if p == self.player else self.player
        self.log(f"✨ {p.name} 將【{card.name}】登場於舞台位置 {slot_idx}！")
        if not p.is_ai:
            self._broadcast_action(f"將【{card.name}】登場於位置 {slot_idx}")
        self.update_ui()

        if card.id == "BFR/S78-015":
            cx_in_hand = [c for c in p.hand if c.type == "CX"]
            cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
            if len(p.stock) >= 1 and cx_in_hand and cx_in_wr:
                do_eff = (
                    False
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "雙胞胎的妹妹 結衣", "是否支付 (1) 能量並捨棄手牌 1 張名場面，從休息室回收 1 張名場面？"
                    )
                )
                if do_eff:
                    self.pay_stock(p, 1)
                    self.select_hand_discard(
                        p, filter_fn=lambda x: x.type == "CX", prompt="選擇捨棄的手牌名場面"
                    )
                    cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
                    target = self.choose_card_dialog(
                        "選擇要從休息室回收的名場面", cx_in_wr, allow_cancel=False
                    )
                    if target:
                        p.waiting_room.remove(target)
                        p.hand.append(target)
                        self.log(f"🔄 {p.name} 透過【雙胞胎的妹妹 結衣】交換回收了【{target.name}】！")

        elif card.id == "BFR/S78-001":
            if len(p.stock) >= 1 and len(p.deck) >= 1:
                do_eff = (
                    (len(p.level_zone) < 3)
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "戰鬥的工匠 伊茲",
                        "是否支付 (1) 能量並將牌庫頂 1 張牌放到傷害區，從牌庫檢索最多 1 張等級 1 以下的角色？",
                    )
                )
                if do_eff:
                    self.pay_stock(p, 1)
                    self.check_deck_refresh(p)
                    if p.deck:
                        dmg_c = self.pop_deck_top(p)
                        p.clock.append(dmg_c)
                        self.check_level_up(p)
                    valid = [c for c in p.deck if c.type == "CHAR" and c.base_level <= 1]
                    if valid and not self.game_over:
                        chosen = (
                            valid[0]
                            if p.is_ai
                            else self.choose_card_dialog(
                                "戰鬥的工匠 伊茲：選擇最多 1 張等級 1 以下角色加入手牌",
                                valid,
                                allow_cancel=True,
                            )
                        )
                        if chosen:
                            self.remove_card_from_deck(p, chosen)
                            p.hand.append(chosen)
                            self.log(f"🔨 {p.name} 透過【戰鬥的工匠 伊茲】檢索了【{chosen.name}】！")
                        random.shuffle(p.deck)

        elif card.id == "BFR/S78-060":
            opp_front = [i for i in [0, 1, 2] if opp.stage[i] is not None]
            if opp_front:
                t_slot = (
                    opp_front[0]
                    if p.is_ai
                    else self.select_stage_slot_dialog(
                        opp, opp_front, "焰火飛馳 蜜伊：選擇對手前列 1 隻角色攻擊力 -1000"
                    )
                )
                opp.stage[t_slot].temp_power -= 1000
                self.log(f"🔥 【焰火飛馳 蜜伊】使對手【{opp.stage[t_slot].name}】攻擊力 -1000！")
            if len(p.stock) >= 1 and len(p.hand) >= 1:
                do_search = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "焰火飛馳 蜜伊", "是否支付 (1) 能量並捨棄 1 張手牌，從牌庫檢索最多 1 張《遊戲》角色？"
                    )
                )
                if do_search:
                    self.pay_stock(p, 1)
                    self.select_hand_discard(p, prompt="焰火飛馳 蜜伊：請選擇捨棄 1 張手牌")
                    valid = [c for c in p.deck if c.type == "CHAR" and "遊戲" in c.traits]
                    if valid:
                        chosen = (
                            valid[0]
                            if p.is_ai
                            else self.choose_card_dialog(
                                "焰火飛馳 蜜伊：選擇最多 1 張《遊戲》角色加入手牌", valid, allow_cancel=True
                            )
                        )
                        if chosen:
                            self.remove_card_from_deck(p, chosen)
                            p.hand.append(chosen)
                            self.log(f"🔍 {p.name} 檢索了【{chosen.name}】加入手牌！")
                        random.shuffle(p.deck)

        # 任務 2：修正 BFR/S78-083《情報戰 莎莉》雙向隨機 / 玩家手動 0,1,2,3 宣言與最多 X 張抽牌
        elif card.id == "BFR/S78-083":
            self.check_deck_refresh(p)
            if p.is_ai:
                top2 = []
                for _ in range(min(2, len(p.deck))):
                    top2.append(self.pop_deck_top(p))
                p.deck = top2 + p.deck
            else:
                top2 = self.ask_step_by_step_look_up_to(
                    p, 2, "情報戰 莎莉：看牌庫頂最多 2 張", show_lv1_hint=False, allow_skip_all=True
                )
                if len(top2) >= 1:
                    top2 = self.ask_reorder_cards_center(p, top2, "情報戰 莎莉：拖移調整放回牌庫頂順序")
                p.deck = top2 + p.deck

            if not p.is_ai:
                if self.net_node and self.net_node.connected:
                    self._lan_declared_level = None
                    self.net_node.send({"type": "DECLARE_LEVEL_REQ", "caller": p.name})
                    def build_wait(frame):
                        tk.Label(
                            frame,
                            text="⏳ 等待連線對手宣言等級 0 / 1 / 2 / 3 ...",
                            bg="#1e2230",
                            fg="#ffd166",
                            font=("Microsoft JhengHei", 16, "bold"),
                        ).pack(pady=80)
                    self._show_overlay_and_wait(build_wait)
                    decl = self._lan_declared_level if self._lan_declared_level is not None else RuleEngine.ai_declare_level_random()
                    self.log(f"🕵️ 【情報戰 莎莉】發動！連線對手宣言等級：{decl}")
                else:
                    decl = RuleEngine.ai_declare_level_random()
                    self.log(f"🕵️ 【情報戰 莎莉】發動！對手 AI 隨機宣言等級：{decl}")
            else:
                decl = self.ask_declare_level_center(p.name)
                self.log(f"🕵️ 【情報戰 莎莉】發動！玩家親自宣言等級：{decl}")

            self.check_deck_refresh(p)
            if p.deck and not self.game_over:
                milled = self.pop_deck_top(p)
                p.waiting_room.append(milled)
                milled_lvl = 0 if milled.type == "CX" else milled.base_level
                self.log(f"📄 翻開牌庫頂送入休息室：【{milled.name}】(等級視為 {milled_lvl})")
                if milled_lvl == decl:
                    max_draw = decl + 1
                    if p.is_ai:
                        self.draw_cards(p, max_draw)
                        self.log(f"🎯 命中宣言等級！{p.name} 抽取了 {max_draw} 張牌！")
                    else:
                        # 支援「抽最多 X 張牌」逐步詢問
                        drawn_cnt = 0
                        for d_idx in range(1, max_draw + 1):
                            want_draw = self.ask_yes_no_center(
                                f"情報戰 莎莉：命中宣言 Lv.{decl}！",
                                f"翻開【{milled.name}】命中對手宣言的 Lv.{decl}！\n"
                                f"最多可抽 {max_draw} 張牌，是否抽取第 {d_idx} / {max_draw} 張？",
                            )
                            if not want_draw:
                                break
                            self.draw_cards(p, 1)
                            drawn_cnt += 1
                            if self.game_over:
                                break
                        self.log(f"🎯 命中宣言等級！{p.name} 選擇抽取了 {drawn_cnt} 張牌！")

        elif card.id == "BFR/S78-057":
            card.temp_power += 1500
            self.log("🛡️ 【移動要塞 梅普露】登場攻擊力 +1500！")

        elif card.id == "BFR/S78-087":
            opp_lv1_slots = [
                i
                for i in range(5)
                if opp.stage[i] and self.get_effective_level(opp, opp.stage[i], i) >= 1
            ]
            if len(p.hand) >= 1 and opp_lv1_slots:
                do_swap = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "盾與盾 梅普露＆莎莉",
                        "是否捨棄 1 張手牌，選擇對手 1 隻等級 1 以上的角色強迫降級交換？",
                    )
                )
                if do_swap:
                    self.select_hand_discard(p, prompt="盾與盾 梅普露＆莎莉：選擇捨棄 1 張手牌")
                    t_slot = (
                        opp_lv1_slots[0]
                        if p.is_ai
                        else self.select_stage_slot_dialog(
                            opp, opp_lv1_slots, "選擇對手要被交換的 Lv.1 以上角色"
                        )
                    )
                    target_c = opp.stage[t_slot]
                    max_x = self.get_effective_level(opp, target_c, t_slot) - 1
                    wr_cands = [
                        c for c in opp.waiting_room if c.type == "CHAR" and c.base_level <= max_x
                    ]
                    self.send_stage_to_wr(opp, t_slot)
                    if wr_cands:
                        rep = wr_cands[0]
                        opp.waiting_room.remove(rep)
                        rep.reset_stage_state()
                        opp.stage[t_slot] = rep
                        self.log(f"🔄 強迫交換！對手的【{target_c.name}】被換成了【{rep.name}】！")

        elif card.id == "BFR/S78-072":
            game_cnt = sum(1 for c in p.stage if c and "遊戲" in c.traits)
            buff = game_cnt * 500
            card.temp_power += buff
            opp_slots = [i for i in range(5) if opp.stage[i] is not None]
            if opp_slots:
                t_slot = (
                    opp_slots[0]
                    if p.is_ai
                    else self.select_stage_slot_dialog(
                        opp, opp_slots, "火炎牢 蜜伊：選擇對手 1 隻角色封鎖回手與回憶"
                    )
                )
                opp.stage[t_slot].cannot_return_hand = True
                opp.stage[t_slot].cannot_go_memory = True
                self.log(
                    f"🔒 【火炎牢 蜜伊】攻擊力+{buff}，並封鎖了對手【{opp.stage[t_slot].name}】！"
                )

        elif card.id == "BFR/S78-063":
            card.temp_power += 3000
            cx_wr = [c for c in p.waiting_room if c.type == "CX"]
            if len(p.stock) >= 1 and cx_wr:
                do_sal = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "暴虐 梅普露", "是否支付 (1) 能量，從休息室選擇 1 張名場面回到手牌？"
                    )
                )
                if do_sal:
                    self.pay_stock(p, 1)
                    chosen = (
                        cx_wr[0]
                        if p.is_ai
                        else self.choose_card_dialog(
                            "暴虐 梅普露：選擇回收的名場面", cx_wr, allow_cancel=False
                        )
                    )
                    p.waiting_room.remove(chosen)
                    p.hand.append(chosen)
                    self.log(f"👑 【暴虐 梅普露】登場+3000，並回收了名場面【{chosen.name}】！")

        elif card.id == "BFR/S78-064":
            if len(p.clock) > 0:
                do_heal = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "炎帝 蜜伊", "是否將傷害區最上方 1 張卡片放到休息室（回 1 點血）？"
                    )
                )
                if do_heal:
                    healed = p.clock.pop()
                    p.waiting_room.append(healed)
                    self.log(f"💖 【炎帝 蜜伊】登場回復 1 點傷害（移除：{healed.name}）！")

        elif card.id == "BFR/S78-081":
            if len(p.clock) > 0:
                do_heal = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "天才少年 奏", "是否將傷害區最上方 1 張卡片放到休息室（回 1 點血）？"
                    )
                )
                if do_heal:
                    healed = p.clock.pop()
                    p.waiting_room.append(healed)
                    self.log("💖 【天才少年 奏】登場回復 1 點傷害！")
            if any(
                i != slot_idx and p.stage[i] and "遊戲" in p.stage[i].traits for i in range(5)
            ):
                card.temp_power += 2000
                self.log("📘 【天才少年 奏】獲得登場攻擊力 +2000！")

        elif card.id == "BFR/S78-082":
            if len(p.stock) >= 1 and len(opp.stock) >= 1:
                do_stock = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "機械神 梅普露",
                        f"是否支付 (1) 能量，將對手的 {len(opp.stock)} 張能量全部送入休息室並以牌庫頂重洗？",
                    )
                )
                if do_stock:
                    self.pay_stock(p, 1)
                    cnt = len(opp.stock)
                    opp.waiting_room.extend(opp.stock)
                    opp.stock.clear()
                    for _ in range(cnt):
                        self.check_deck_refresh(opp)
                        if opp.deck:
                            opp.stock.append(self.pop_deck_top(opp))
                    self.log(f"⚙️ 【機械神 梅普露】將對手的 {cnt} 點能量全數洗入休息室並重填！")

        # === GA文庫 (GA/S131) 角色登場效果 ===
        elif card.id == "GA01/S131-115":
            other_slots = [i for i in range(5) if i != slot_idx and p.stage[i] is not None]
            cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
            if other_slots and cx_in_wr:
                do_hatoko = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "《五帝》櫛川鳩子",
                        "是否將舞台上其他 1 隻我方角色放到休息室，從休息室選擇 1 張名場面返回手牌？",
                    )
                )
                if do_hatoko:
                    sac_slot = (
                        other_slots[0]
                        if p.is_ai
                        else self.select_stage_slot_dialog(
                            p, other_slots, "《五帝》櫛川鳩子：選擇要送入休息室的其他我方角色"
                        )
                    )
                    self.send_stage_to_wr(p, sac_slot)
                    cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
                    if cx_in_wr:
                        chosen_cx = (
                            cx_in_wr[0]
                            if p.is_ai
                            else self.choose_card_dialog(
                                "《五帝》櫛川鳩子：選擇要返回手牌的名場面", cx_in_wr, allow_cancel=False
                            )
                        )
                        p.waiting_room.remove(chosen_cx)
                        p.hand.append(chosen_cx)
                        self.log(f"🌊 【《五帝》櫛川鳩子】犧牲隊友回收了名場面【{chosen_cx.name}】！")

        elif card.id == "GA02/S131-003":
            card.temp_power += 1500
            self.log("👼 【隔壁的天使 椎名真晝】登場攻擊力 +1500！")
            has_other_ga = any(
                i != slot_idx and p.stage[i] and "GA文庫" in p.stage[i].traits for i in range(5)
            )
            if has_other_ga and len(p.hand) >= 1:
                do_mahiru = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "隔壁的天使 椎名真晝",
                        "是否捨棄 1 張手牌，將傷害區上方最多 1 張放到休息室（回 1 點血），並從休息室回收 1 張《GA文庫》角色？",
                    )
                )
                if do_mahiru:
                    self.select_hand_discard(p, prompt="隔壁的天使 椎名真晝：選擇捨棄 1 張手牌")
                    if p.clock:
                        healed = p.clock.pop()
                        p.waiting_room.append(healed)
                        self.log(f"💖 【隔壁的天使 椎名真晝】回復 1 點傷害（移除：{healed.name}）！")
                    wr_ga = [c for c in p.waiting_room if c.type == "CHAR" and "GA文庫" in c.traits]
                    if wr_ga:
                        picked = (
                            wr_ga[-1]
                            if p.is_ai
                            else self.choose_card_dialog(
                                "隔壁的天使 椎名真晝：選擇要從休息室回收的《GA文庫》角色",
                                wr_ga,
                                allow_cancel=False,
                            )
                        )
                        if picked:
                            p.waiting_room.remove(picked)
                            p.hand.append(picked)
                            self.log(f"📥 【隔壁的天使 椎名真晝】從休息室回收了【{picked.name}】！")

        elif card.id == "GA04/S131-100":
            if p.is_ai:
                use_heal = len(p.clock) > 0
            else:
                use_heal = self.ask_yes_no_center(
                    "新的黎明 女神官：二選一效果",
                    "請選擇要執行的登場效果：\n\n"
                    "點擊【是】👉 將自己傷害區上方 1 張放到休息室（回復 1 點傷害）\n"
                    "點擊【否】👉 對手將能量全部返回牌組洗牌並重填相同張數，且此卡本回合攻擊力 +2000",
                )
            if use_heal:
                if p.clock:
                    healed = p.clock.pop()
                    p.waiting_room.append(healed)
                    self.log(f"✨ 【新的黎明 女神官】發動聖光治癒，回復 1 點傷害（{healed.name}）！")
            else:
                cnt = len(opp.stock)
                if cnt > 0:
                    opp.deck.extend(opp.stock)
                    opp.stock.clear()
                    random.shuffle(opp.deck)
                    for _ in range(cnt):
                        self.check_deck_refresh(opp)
                        if opp.deck:
                            opp.stock.append(self.pop_deck_top(opp))
                card.temp_power += 2000
                self.log(f"✨ 【新的黎明 女神官】將對手 {cnt} 張能量洗回牌組重填，且自身攻擊力 +2000！")

        elif card.id == "GA05/S131-007":
            opp_slots = [i for i in range(5) if opp.stage[i] is not None]
            if opp_slots:
                t_slot = (
                    opp_slots[0]
                    if p.is_ai
                    else self.select_stage_slot_dialog(
                        opp, opp_slots, "莉姿夏爾蒂：選擇對手 1 隻角色封鎖移動能力"
                    )
                )
                opp.stage[t_slot].cannot_move = True
                self.log(f"🔒 【莉姿夏爾蒂】使對手【{opp.stage[t_slot].name}】直到下回合結束前無法移動位置！")
            cx_in_hand = [c for c in p.hand if c.type == "CX"]
            cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
            if len(p.stock) >= 1 and cx_in_hand and cx_in_wr:
                do_swap_cx = (
                    False
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "莉姿夏爾蒂：名場面交換",
                        "是否支付 (1) 能量並捨棄手牌 1 張名場面，從休息室選擇 1 張名場面回到手牌？",
                    )
                )
                if do_swap_cx:
                    self.pay_stock(p, 1)
                    self.select_hand_discard(p, filter_fn=lambda x: x.type == "CX", prompt="選擇捨棄的手牌名場面")
                    cx_in_wr = [c for c in p.waiting_room if c.type == "CX"]
                    if cx_in_wr:
                        target_cx = self.choose_card_dialog("選擇要從休息室回收的名場面", cx_in_wr, allow_cancel=False)
                        if target_cx:
                            p.waiting_room.remove(target_cx)
                            p.hand.append(target_cx)
                            self.log(f"🔄 {p.name} 透過【莉姿夏爾蒂】交換回收了名場面【{target_cx.name}】！")

        elif card.id == "GA08/S131-038":
            if len(p.hand) >= 1 and len(p.waiting_room) >= 1:
                do_beel = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "魔族農業大臣 別西卜",
                        "是否捨棄 1 張手牌，公開牌組頂 1 張卡片並從休息室回收 1 張該等級以下的角色？",
                    )
                )
                if do_beel:
                    self.select_hand_discard(p, prompt="魔族農業大臣 別西卜：請選擇捨棄 1 張手牌")
                    self.check_deck_refresh(p)
                    if p.deck and not self.game_over:
                        top_c = p.deck[0]
                        rev_lvl = 0 if top_c.type == "CX" else top_c.base_level
                        self.log(f"🔍 【魔族農業大臣 別西卜】公開牌組頂：【{top_c.name}】，視為 Lv.{rev_lvl}！")
                        valid_wr = [c for c in p.waiting_room if c.type == "CHAR" and c.base_level <= rev_lvl]
                        if valid_wr:
                            chosen = (
                                max(valid_wr, key=lambda x: (x.base_level, x.base_power))
                                if p.is_ai
                                else self.choose_card_dialog(
                                    f"別西卜：選擇休息室 Lv.{rev_lvl} 以下的角色 1 張返回手牌",
                                    valid_wr,
                                    allow_cancel=False,
                                )
                            )
                            if chosen:
                                p.waiting_room.remove(chosen)
                                p.hand.append(chosen)
                                self.log(f"📥 {p.name} 從休息室回收了【{chosen.name}】！")

        elif card.id == "GA10/S131-002":
            opp_cnt = sum(1 for c in opp.stage if c is not None)
            buff = opp_cnt * 1000
            card.temp_power += buff
            self.log(f"🗡️ 【跨越復仇 琉】依對手場上 {opp_cnt} 隻角色，本回合攻擊力 +{buff}！")

        elif card.id == "GA10/S131-019":
            opp_cx_wr = [c for c in opp.waiting_room if c.type == "CX"]
            if len(p.stock) >= 1 and len(p.hand) >= 1 and len(opp.waiting_room) > 1:
                do_ais = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "炸薯球 艾絲：逆壓縮",
                        "是否支付 (1) 能量並捨棄 1 張手牌，讓對手除休息室 1 張名場面以外的所有休息室卡片洗回牌組？",
                    )
                )
                if do_ais:
                    self.pay_stock(p, 1)
                    self.select_hand_discard(p, prompt="炸薯球 艾絲：請選擇捨棄 1 張手牌")
                    keep_cx = opp_cx_wr[0] if opp_cx_wr else None
                    returned = [c for c in opp.waiting_room if c != keep_cx]
                    opp.deck.extend(returned)
                    opp.waiting_room = [keep_cx] if keep_cx else []
                    random.shuffle(opp.deck)
                    self.log(f"🌪️ 【炸薯球 艾絲】發動逆壓縮！將對手休息室 {len(returned)} 張非名場面卡洗回牌組！")

        elif card.id == "GA10/S131-029":
            my_slots = [i for i in range(5) if p.stage[i] is not None]
            for pick_i in range(min(2, len(my_slots))):
                avail = [i for i in my_slots if not p.stage[i].anti_early_play_stock_bomb]
                if not avail:
                    break
                t_s = (
                    avail[0]
                    if p.is_ai
                    else self.select_stage_slot_dialog(
                        p, avail, f"蕾菲亞&艾絲：選擇第 {pick_i + 1}/2 隻賦予『早出相殺送能量』的角色", allow_cancel=True
                    )
                )
                if t_s is None:
                    break
                p.stage[t_s].anti_early_play_stock_bomb = True
                self.log(f"✨ 【蕾菲亞&艾絲】賦予【{p.stage[t_s].name}】早出相殺送能量能力！")

        elif card.id == "GA12/S131-013":
            card.temp_power += 3000
            self.log("💛 【朋友的話是當然的 月之森真白】登場攻擊力 +3000！")

        # === 孤獨搖滾 (BTR/W107) 角色登場效果 ===
        elif card.id == "BTR/W107-T13":
            kita_in_wr = [
                c
                for c in p.waiting_room
                if c.id == "BTR/W107-T16" or c.name == "主唱吉他手 喜多郁代"
            ]
            if len(p.hand) >= 1 and kita_in_wr:
                do_bond = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "樂團女子？ 後藤一里：絆／主唱吉他手 喜多郁代",
                        "是否捨棄 1 張手牌，從休息室選擇 1 張「主唱吉他手 喜多郁代」加入手牌？",
                    )
                )
                if do_bond:
                    self.select_hand_discard(p, prompt="絆代價：請選擇捨棄 1 張手牌")
                    kita_in_wr = [
                        c
                        for c in p.waiting_room
                        if c.id == "BTR/W107-T16" or c.name == "主唱吉他手 喜多郁代"
                    ]
                    if kita_in_wr:
                        picked = kita_in_wr[0]
                        p.waiting_room.remove(picked)
                        p.hand.append(picked)
                        self.log(f"🎸 【樂團女子？ 後藤一里】發動絆效果，從休息室回收【{picked.name}】！")

        elif card.id == "BTR/W107-T14":
            looked = self.ask_step_by_step_look_up_to(
                p, 3, "後藤一里：看牌組頂最多 3 張選事件"
            )
            valid_ev = [c for c in looked if c.type == "EVENT"]
            chosen_ev = None
            if valid_ev:
                chosen_ev = (
                    valid_ev[0]
                    if p.is_ai
                    else self.choose_card_dialog(
                        "後藤一里：選擇最多 1 張事件加入手牌（加手的話須捨棄 1 張手牌）",
                        valid_ev,
                        allow_cancel=True,
                    )
                )
            if chosen_ev:
                p.hand.append(chosen_ev)
                looked.remove(chosen_ev)
                p.waiting_room.extend(looked)
                self.log(f"🎸 【後藤一里】翻牌取得事件【{chosen_ev.name}】加入手牌！")
                self.select_hand_discard(p, prompt="後藤一里：因事件加手，請選擇捨棄 1 張手牌")
            else:
                p.waiting_room.extend(looked)

            opp_front = [i for i in [0, 1, 2] if opp.stage[i] is not None]
            if len(opp_front) <= 1:
                cost0_front = [i for i in opp_front if opp.stage[i].cost <= 0]
                if cost0_front:
                    do_kill = (
                        True
                        if p.is_ai
                        else self.ask_yes_no_center(
                            "後藤一里：退場對手前列費用0角色",
                            f"對手前列角色在 1 張以下！是否將對手前列的【{opp.stage[cost0_front[0]].name}】(費用 0 以下) 放到休息室？",
                        )
                    )
                    if do_kill:
                        self.log(f"💥 【後藤一里】將對手前列的【{opp.stage[cost0_front[0]].name}】送入休息室！")
                        self.send_stage_to_wr(opp, cost0_front[0])

        elif card.id == "BTR/W107-089":
            music_hand = [c for c in p.hand if c.type == "CHAR" and "音樂" in c.traits]
            kita_deck = [
                c
                for c in p.deck
                if c.id == "BTR/W107-T16" or c.name == "主唱吉他手 喜多郁代"
            ]
            if music_hand and kita_deck:
                do_s_kita = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "開始轉動的故事 後藤一里",
                        "是否捨棄手牌 1 張《音樂》角色，從牌組檢索最多 1 張「主唱吉他手 喜多郁代」加入手牌？",
                    )
                )
                if do_s_kita:
                    self.select_hand_discard(
                        p,
                        filter_fn=lambda x: x.type == "CHAR" and "音樂" in x.traits,
                        prompt="開始轉動的故事 後藤一里：請選擇捨棄 1 張手牌《音樂》角色",
                    )
                    kita_deck = [
                        c
                        for c in p.deck
                        if c.id == "BTR/W107-T16" or c.name == "主唱吉他手 喜多郁代"
                    ]
                    if kita_deck:
                        target_k = (
                            kita_deck[0]
                            if p.is_ai
                            else self.choose_card_dialog(
                                "開始轉動的故事 後藤一里：選擇「主唱吉他手 喜多郁代」加入手牌",
                                kita_deck,
                                allow_cancel=True,
                            )
                        )
                        if target_k:
                            self.remove_card_from_deck(p, target_k)
                            p.hand.append(target_k)
                            self.log(f"🎸 【開始轉動的故事 後藤一里】從牌組檢索了【{target_k.name}】！")
                    random.shuffle(p.deck)

        elif card.id == "BTR/W107-075":
            if (len(p.level_zone) + len(p.clock)) >= 4 and len(p.clock) > 0:
                do_st_heal = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        "晚霞的歸路 喜多郁代：千鳥回血充能",
                        "你的等級區與時鐘區合計有 4 張以上！\n是否將自己時鐘區最上方 1 張卡片放到能量區（回 1 血並 +1 能量）？",
                    )
                )
                if do_st_heal:
                    healed_c = p.clock.pop()
                    p.stock.append(healed_c)
                    self.log(f"🌇 【晚霞的歸路 喜多郁代】將時鐘區頂端的【{healed_c.name}】移入能量區（回血+充能）！")

        elif card.id in ["BTR/W107-076", "BTR/W107-069"]:
            if len(p.clock) > 0:
                do_heal_k = (
                    True
                    if p.is_ai
                    else self.ask_yes_no_center(
                        card.name,
                        f"【{card.name}】登場！是否將自己時鐘區上方 1 張卡片放到休息室（回復 1 點傷害）？",
                    )
                )
                if do_heal_k:
                    healed = p.clock.pop()
                    p.waiting_room.append(healed)
                    self.log(f"💖 【{card.name}】登場回復 1 點傷害（移除：{healed.name}）！")
        else:
            # 萬用資料驅動 ON_PLAY 自動結算（支援所有從貓罐子匯入的新系列角色！）
            opp = self.ai if p == self.player else self.player
            self._run_universal_timing(p, opp, card, "ON_PLAY", slot_idx=slot_idx)

        self.update_ui()
        return True

    def on_click_player_stage(self, slot_idx: int):
        if self.game_over:
            return
        card = self.player.stage[slot_idx]
        if card:
            self.inspect_card(card, self.player, slot_idx)

        sel_st = getattr(self, "_field_slot_select_state", None)
        if sel_st is not None:
            if sel_st["target_player"] == self.player and slot_idx in sel_st["valid_set"]:
                self.app.sound_mgr.play_sfx("sfx_click")
                sel_st["res"]["slot"] = slot_idx
                self._close_overlay()
            return

        if (
            self.active_player == self.player
            and self.phase == "MAIN"
            and self.selected_hand_idx is not None
        ):
            h_card = self.player.hand[self.selected_hand_idx]
            if h_card.type == "CHAR":
                self.play_character_from_hand(self.player, self.selected_hand_idx, slot_idx)
                return

        if self.phase == "MAIN" and self.selected_stage_idx == slot_idx:
            self.selected_stage_idx = None
        else:
            self.selected_stage_idx = slot_idx
        self.selected_hand_idx = None
        self.update_ui()

        if (
            self.active_player == self.player
            and self.phase == "ATTACK"
            and slot_idx in [0, 1, 2]
            and card
            and card.state == "STAND"
        ):
            if self.turn_count == 1 and self.attacks_this_turn >= 1:
                self.show_info_center("先攻首回合限制", "依 WS 規則，先攻玩家的第 1 個回合只能進行 1 次攻擊！")
                return
            self.initiate_attack(self.player, slot_idx)

    def on_click_ai_stage(self, slot_idx: int):
        card = self.ai.stage[slot_idx]
        if card:
            self.inspect_card(card, self.ai, slot_idx)
        sel_st = getattr(self, "_field_slot_select_state", None)
        if sel_st is not None:
            if sel_st["target_player"] == self.ai and slot_idx in sel_st["valid_set"]:
                self.app.sound_mgr.play_sfx("sfx_click")
                sel_st["res"]["slot"] = slot_idx
                self._close_overlay()
            return

    def on_click_move_stage(self):
        if self.phase != "MAIN" or self.selected_stage_idx is None:
            return
        src = self.selected_stage_idx
        self.selected_stage_idx = None
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()
        if self.player.stage[src] and self.player.stage[src].cannot_move:
            self.show_info_center("無法移動", "此角色受到效果封鎖，無法移動到其他舞台格子！")
            return
        dst = self.select_stage_slot_dialog(
            self.player, [i for i in range(5) if i != src], "選擇要交換位置的舞台格子"
        )
        self.player.stage[src], self.player.stage[dst] = (
            self.player.stage[dst],
            self.player.stage[src],
        )
        self.selected_stage_idx = dst
        self.log(f"🔄 舞台位置 {src} 與 {dst} 交換完成。")
        self.update_ui()

    def trigger_act_used_bonus(self, p: PlayerState):
        for idx, c in enumerate(p.stage):
            if c and c.id == "BFR/S78-102" and not c.used_act_buff_turn:
                c.used_act_buff_turn = True
                valid_slots = [i for i in range(5) if p.stage[i] is not None]
                if valid_slots:
                    t_slot = (
                        valid_slots[0]
                        if p.is_ai
                        else self.select_stage_slot_dialog(
                            p, valid_slots, "通往勝利的方程式 梅普露：選擇 1 隻角色攻擊力 +1000"
                        )
                    )
                    p.stage[t_slot].temp_power += 1000
                    self.log(
                        f"📐 【通往勝利的方程式 梅普露】觸發！使【{p.stage[t_slot].name}】攻擊力 +1000！"
                    )

    def on_click_act_ability(self):
        if getattr(self, "_overlay_is_waiting", False) or self.phase != "MAIN" or self.selected_stage_idx is None:
            return
        card = self.player.stage[self.selected_stage_idx]
        self.selected_stage_idx = None
        if hasattr(self, "stage_floating_bar") and self.stage_floating_bar.winfo_exists():
            self.stage_floating_bar.place_forget()
        if not card:
            return
        if card.id != "BTR/W107-T18" and card.state != "STAND":
            return

        if card.id == "BFR/S78-031":
            if len(self.player.stock) < 1:
                self.show_info_center("能量不足", "需要 1 點能量才能發動集中！")
                return
            self.pay_stock(self.player, 1)
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)

            flipped = []
            for _ in range(4):
                self.check_deck_refresh(self.player)
                if self.player.deck:
                    flipped.append(self.pop_deck_top(self.player))
            self.player.waiting_room.extend(flipped)
            cx_hits = sum(1 for c in flipped if c.type == "CX")
            names = ", ".join(c.name for c in flipped)
            self.log(f"🌀 集中翻開 4 張：[{names}] -> 命中 {cx_hits} 張名場面！")
            self.update_ui()
            c_steps = [
                {
                    "card": fc,
                    "badge": "🌟 名場面命中！" if fc.type == "CX" else f"Lv.{fc.base_level}",
                    "step_shout": (
                        f"🎯 第 {idx_f + 1} 張翻出名場面【{fc.name}】！"
                        if fc.type == "CX"
                        else f"🎴 第 {idx_f + 1} 張翻出：【{fc.name}】"
                    ),
                    "step_bg": "#06d6a0" if fc.type == "CX" else "#2b3044",
                    "step_fg": "#000000" if fc.type == "CX" else "#ffffff",
                    "step_sfx": "sfx_climax" if fc.type == "CX" else "sfx_draw",
                }
                for idx_f, fc in enumerate(flipped)
            ]
            self.run_interactive_card_flip_sequence(
                deck_owner=self.player,
                clicker_is_ai=False,
                banner_title="【多彩多樣 莎莉】集中翻牌 (4 張)",
                step_cards_info=c_steps,
                final_summary_text=(
                    f"🎯 集中完成！翻出 {cx_hits} 張名場面（可從牌組檢索最多 1 張《遊戲》角色）"
                    if cx_hits > 0
                    else "💨 集中完成：未翻出名場面"
                ),
                final_summary_bg="#06d6a0" if cx_hits > 0 else "#4a4e69",
                final_summary_fg="#000000" if cx_hits > 0 else "#ffffff",
            )

            # 無論翻到幾張名場面，皆為選擇最多 1 張《遊戲》角色加手
            if cx_hits > 0:
                valid = [c for c in self.player.deck if c.type == "CHAR" and "遊戲" in c.traits]
                if valid:
                    chosen = self.choose_card_dialog(
                        f"集中命中（翻出 {cx_hits} 張名場面）：請從牌組選擇最多 1 張《遊戲》角色加入手牌",
                        valid,
                        allow_cancel=True,
                    )
                    if chosen:
                        self.remove_card_from_deck(self.player, chosen)
                        self.player.hand.append(chosen)
                        self.log(f"🎯 集中檢索：【{chosen.name}】加入手牌！")
                random.shuffle(self.player.deck)
            self._broadcast_action("發動【多彩多樣 莎莉】集中效果")
            self.update_ui()

        elif card.id == "BFR/S78-061":
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)
            if len(card.markers) == 0:
                self.check_deck_refresh(self.player)
                if self.player.deck:
                    top_c = self.player.deck[0]
                    lvl = 0 if top_c.type == "CX" else top_c.base_level
                    if lvl >= 1:
                        self.pop_deck_top(self.player)
                        card.markers.append(top_c)
                        self.log(
                            f"🔖 【作戰變更 米瑟莉】翻開牌庫頂【{top_c.name}】(Lv.{lvl})，成功吸收為下方標記！"
                        )
                    else:
                        self.log(
                            f"🔖 【作戰變更 米瑟莉】翻開牌庫頂【{top_c.name}】(視為 Lv.0)，放回原位。"
                        )
            else:
                mk = card.markers.pop(0)
                self.player.stock.append(mk)
                self.log("⚡ 【作戰變更 米瑟莉】將下方標記送入能量區（能量 +1）！")
            self.update_ui()

        elif card.id == "GA10/S131-012":
            if len(self.player.stock) < 1:
                self.show_info_center("能量不足", "需要 1 點能量才能發動 5 張集中！")
                return
            self.pay_stock(self.player, 1)
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)

            flipped = []
            for _ in range(5):
                self.check_deck_refresh(self.player)
                if self.player.deck:
                    flipped.append(self.pop_deck_top(self.player))
            self.player.waiting_room.extend(flipped)
            has_choice_cx_in_zone = (
                self.player.climax_zone is not None and self.player.climax_zone.trigger == "CHOICE"
            )
            choice_hits = sum(
                1
                for c in flipped
                if (c.type == "CX" and c.trigger == "CHOICE")
                or (has_choice_cx_in_zone and c.id == "GA12/S131-013")
            )
            names = ", ".join(c.name for c in flipped)
            self.log(f"🌀 【奇怪的妖精 琉】集中翻開 5 張：[{names}] -> 命中 {choice_hits} 張箭頭標誌！")
            self.update_ui()
            c_steps = [
                {
                    "card": fc,
                    "badge": (
                        "🏹 箭頭命中！"
                        if ((fc.type == "CX" and fc.trigger == "CHOICE") or (has_choice_cx_in_zone and fc.id == "GA12/S131-013"))
                        else f"Lv.{0 if fc.type == 'CX' else fc.base_level}"
                    ),
                    "step_shout": (
                        f"🎯 第 {idx_f + 1} 張翻出箭頭標誌【{fc.name}】！"
                        if ((fc.type == "CX" and fc.trigger == "CHOICE") or (has_choice_cx_in_zone and fc.id == "GA12/S131-013"))
                        else f"🎴 第 {idx_f + 1} 張翻出：【{fc.name}】"
                    ),
                    "step_bg": (
                        "#06d6a0"
                        if ((fc.type == "CX" and fc.trigger == "CHOICE") or (has_choice_cx_in_zone and fc.id == "GA12/S131-013"))
                        else "#2b3044"
                    ),
                    "step_fg": (
                        "#000000"
                        if ((fc.type == "CX" and fc.trigger == "CHOICE") or (has_choice_cx_in_zone and fc.id == "GA12/S131-013"))
                        else "#ffffff"
                    ),
                    "step_sfx": (
                        "sfx_climax"
                        if ((fc.type == "CX" and fc.trigger == "CHOICE") or (has_choice_cx_in_zone and fc.id == "GA12/S131-013"))
                        else "sfx_draw"
                    ),
                }
                for idx_f, fc in enumerate(flipped)
            ]
            self.run_interactive_card_flip_sequence(
                deck_owner=self.player,
                clicker_is_ai=False,
                banner_title="【奇怪的妖精 琉】集中翻牌 (5 張)",
                step_cards_info=c_steps,
                final_summary_text=(
                    f"🎯 集中完成！命中 {choice_hits} 張箭頭標誌（可從休息室回收最多 1 張角色）"
                    if choice_hits > 0
                    else "💨 集中完成：未命中箭頭標誌"
                ),
                final_summary_bg="#06d6a0" if choice_hits > 0 else "#4a4e69",
                final_summary_fg="#000000" if choice_hits > 0 else "#ffffff",
            )

            # 無論翻到幾張名場面，皆為從休息室選擇最多 1 張角色返回手牌
            if choice_hits > 0:
                valid_wr = [c for c in self.player.waiting_room if c.type == "CHAR"]
                if valid_wr:
                    chosen = self.choose_card_dialog(
                        f"集中命中（翻出 {choice_hits} 張箭頭標誌）：請從休息室選擇最多 1 張角色返回手牌",
                        valid_wr,
                        allow_cancel=True,
                    )
                    if chosen:
                        self.player.waiting_room.remove(chosen)
                        self.player.hand.append(chosen)
                        self.log(f"🎯 集中回收：【{chosen.name}】返回手牌！")
            self._broadcast_action("發動【奇怪的妖精 琉】集中效果")
            self.update_ui()

        elif card.id == "GA17/S131-014":
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)
            elaina_targets = [
                c for c in self.player.deck if c.id in ["GA17/S131-017", "GA17/S131-010"]
            ]
            if elaina_targets:
                chosen_el = self.choose_card_dialog(
                    "我的旅路 伊蕾娜：從牌組選擇最多 1 張「第二章 伊蕾娜」或「第三章 伊蕾娜」放到休息室",
                    elaina_targets,
                    allow_cancel=True,
                )
                if chosen_el:
                    self.remove_card_from_deck(self.player, chosen_el)
                    self.player.waiting_room.append(chosen_el)
                    self.log(f"🪄 【我的旅路 伊蕾娜】從牌組將【{chosen_el.name}】送入休息室以準備記憶連鎖！")
            random.shuffle(self.player.deck)
            ga_slots = [
                i for i in range(5) if self.player.stage[i] and "GA文庫" in self.player.stage[i].traits
            ]
            if ga_slots:
                t_slot = self.select_stage_slot_dialog(
                    self.player, ga_slots, "我的旅路 伊蕾娜：選擇 1 隻《GA文庫》角色攻擊力 +2000"
                )
                self.player.stage[t_slot].temp_power += 2000
                self.log(f"✨ 【我的旅路 伊蕾娜】使【{self.player.stage[t_slot].name}】本回合攻擊力 +2000！")
            self.update_ui()

        elif card.id == "BTR/W107-T02":
            if len(self.player.stock) < 1:
                self.show_info_center("能量不足", "需要 1 點能量才能發動 5 張抽牌集中！")
                return
            self.pay_stock(self.player, 1)
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)

            flipped = []
            for _ in range(5):
                self.check_deck_refresh(self.player)
                if self.player.deck:
                    flipped.append(self.pop_deck_top(self.player))
            self.player.waiting_room.extend(flipped)
            cx_hits = sum(1 for c in flipped if c.type == "CX")
            names = ", ".join(c.name for c in flipped)
            self.log(f"🥁 【樂團的領導者 伊地知虹夏】集中翻開 5 張：[{names}] -> 命中 {cx_hits} 張名場面！")
            self.update_ui()
            c_steps = [
                {
                    "card": fc,
                    "badge": "🌟 名場面命中！" if fc.type == "CX" else f"Lv.{fc.base_level}",
                    "step_shout": (
                        f"🎯 第 {idx_f + 1} 張翻出名場面【{fc.name}】！"
                        if fc.type == "CX"
                        else f"🎴 第 {idx_f + 1} 張翻出：【{fc.name}】"
                    ),
                    "step_bg": "#06d6a0" if fc.type == "CX" else "#2b3044",
                    "step_fg": "#000000" if fc.type == "CX" else "#ffffff",
                    "step_sfx": "sfx_climax" if fc.type == "CX" else "sfx_draw",
                }
                for idx_f, fc in enumerate(flipped)
            ]
            self.run_interactive_card_flip_sequence(
                deck_owner=self.player,
                clicker_is_ai=False,
                banner_title="【樂團的領導者 伊地知虹夏】集中翻牌 (5 張)",
                step_cards_info=c_steps,
                final_summary_text=(
                    f"🎯 集中完成！翻出 {cx_hits} 張名場面（可抽取最多 1 張牌）"
                    if cx_hits > 0
                    else "💨 集中完成：未翻出名場面"
                ),
                final_summary_bg="#06d6a0" if cx_hits > 0 else "#4a4e69",
                final_summary_fg="#000000" if cx_hits > 0 else "#ffffff",
            )

            # 無論翻到幾張名場面，皆為最多抽取 1 張牌
            if cx_hits > 0 and not self.game_over:
                want_dr = self.ask_yes_no_center(
                    "伊地知虹夏 集中命中",
                    f"集中翻出 {cx_hits} 張名場面！是否抽取 1 張牌？（最多抽 1 張）",
                )
                if want_dr:
                    self.draw_cards(self.player, 1)
                    self.log("🥁 集中抽牌 +1！")
            self._broadcast_action("發動【樂團的領導者 伊地知虹夏】集中效果")
            self.update_ui()

        elif card.id == "BTR/W107-046":
            card.state = "REST"
            self.trigger_act_used_bonus(self.player)
            music_slots = [
                i for i in range(5) if self.player.stage[i] and "音樂" in self.player.stage[i].traits
            ]
            if music_slots:
                t_slot = self.select_stage_slot_dialog(
                    self.player, music_slots, "打卡美照 喜多郁代：選擇 1 隻《音樂》角色攻擊力 +1000"
                )
                self.player.stage[t_slot].temp_power += 1000
                self.log(f"📸 【打卡美照 喜多郁代】使【{self.player.stage[t_slot].name}】本回合攻擊力 +1000！")
            self.update_ui()

        elif card.id == "BTR/W107-T18":
            if len(self.player.stock) < 1:
                self.show_info_center("能量不足", "需要 1 點能量才能發動【喜多郁代】的【起】能力！")
                return
            self.pay_stock(self.player, 1)
            self.trigger_act_used_bonus(self.player)
            card.temp_power += 1000
            card.clock_kick_on_reverse = True
            self.log("🎸 【喜多郁代】發動【起】能力：本回合攻擊力 +1000，並獲得『擊倒戰鬥對手時可將其放到時計區』！")
            self.update_ui()
        else:
            # 萬用資料驅動【起】能力結算（集中 Brainstorm / 橫置加攻）
            act_abs = [ab for ab in getattr(card, "parsed_abilities", []) if ab.get("category") == "ACT"]
            if not act_abs:
                self.show_info_center("無起動能力", f"【{card.name}】沒有可於主要階段發動的【起】能力。")
                return
            ab = act_abs[0]
            cost = ab.get("cost", {})
            if not self._can_pay_universal_cost(self.player, cost, card):
                self.show_info_center("無法支付代價", f"發動【{card.name}】的【起】能力代價不足（或此卡非正置狀態）！")
                return
            if not self._pay_universal_cost(self.player, cost, card, slot_idx, title=card.name):
                return
            self.trigger_act_used_bonus(self.player)
            if ab.get("effect") == "brainstorm":
                flip_n = ab.get("flip_count", 4)
                cx_hits, _ = self.flip_brainstorm_cards(self.player, flip_n, f"【{card.name}】集中翻牌 ({flip_n} 張)")
                if cx_hits > 0:
                    rew = ab.get("reward", "search")
                    if rew == "draw":
                        self.draw_cards(self.player, cx_hits)
                        self.log(f"✨ 【{card.name}】集中命中 {cx_hits} 張名場面，抽 {cx_hits} 張牌！")
                    elif rew == "salvage":
                        for h_i in range(cx_hits):
                            cands = [c for c in self.player.waiting_room if c.type == "CHAR"]
                            if cands:
                                pk = self.choose_card_dialog(f"集中回收 ({h_i+1}/{cx_hits})：選擇休息室角色回手", cands, allow_cancel=True)
                                if pk and pk in self.player.waiting_room:
                                    self.player.waiting_room.remove(pk)
                                    self.player.hand.append(pk)
                    else:
                        for h_i in range(cx_hits):
                            cands = [c for c in self.player.deck if c.type == "CHAR"]
                            if cands:
                                pk = self.choose_card_dialog(f"集中檢索 ({h_i+1}/{cx_hits})：選擇牌組角色加手", cands, allow_cancel=True)
                                if pk and pk in self.player.deck:
                                    self.player.deck.remove(pk)
                                    self.player.hand.append(pk)
                        random.shuffle(self.player.deck)
            elif ab.get("effect") == "act_buff":
                pwr = ab.get("power", 1000)
                if ab.get("target") == "ally":
                    slots = [i for i in range(5) if self.player.stage[i] is not None]
                    if slots:
                        ts = self.select_stage_slot_dialog(self.player, slots, f"{card.name}：選擇 1 張角色攻擊力 +{pwr}")
                        if self.player.stage[ts]:
                            self.player.stage[ts].temp_power += pwr
                            self.log(f"⚔️ 【{card.name}】使【{self.player.stage[ts].name}】本回合攻擊力 +{pwr}！")
                else:
                    card.temp_power += pwr
                    self.log(f"⚔️ 【{card.name}】本回合攻擊力 +{pwr}！")
            self.update_ui()

    # ------------------------------------------
    # 戰鬥引擎
    # ------------------------------------------
    def initiate_attack(self, atk_p: PlayerState, slot_idx: int, on_complete=None):
        attacker = atk_p.stage[slot_idx]
        def_p = self.ai if atk_p == self.player else self.player
        defender = def_p.stage[slot_idx]

        if defender is None:
            atk_type = "DIRECT"
        else:
            if atk_p.is_ai:
                my_pwr = self.get_effective_power(atk_p, attacker, slot_idx)
                op_pwr = self.get_effective_power(def_p, defender, slot_idx)
                if (
                    my_pwr < op_pwr
                    and attacker.id != "BFR/S78-069"
                    and attacker.id != "BFR/S78-015"
                ):
                    atk_type = "SIDE"
                else:
                    atk_type = "FRONT"
            else:
                atk_type = self.ask_attack_type_dialog(attacker, defender, slot_idx)

        self.attacks_this_turn += 1
        self._current_attack_slot_overwritten = False
        attacker.state = "REST"
        if atk_type == "DIRECT":
            attacker.temp_soul += 1
        elif atk_type == "SIDE" and defender:
            def_lvl = self.get_effective_level(def_p, defender, slot_idx)
            attacker.temp_soul -= def_lvl

        self.log(f"\n⚔️ {atk_p.name} 的【{attacker.name}】宣告【{atk_type}】攻擊！")
        if not atk_p.is_ai:
            self._broadcast_action(f"以【{attacker.name}】宣告 {atk_type} 攻擊")
        self.update_ui()

        # GA17/S131-014《我的旅路 伊蕾娜》記憶防禦：對手直接攻擊時，回憶區有伊蕾娜且無其他同名卡時，攻擊角色魂傷-1
        if atk_type == "DIRECT":
            my_journey_slots = [
                i for i in range(5) if def_p.stage[i] and def_p.stage[i].id == "GA17/S131-014"
            ]
            has_elaina_mem = any("伊蕾娜" in c.name for c in def_p.memory)
            if len(my_journey_slots) == 1 and has_elaina_mem:
                mj_card = def_p.stage[my_journey_slots[0]]
                if not mj_card.used_memory_minus_soul_turn:
                    mj_card.used_memory_minus_soul_turn = True
                    attacker.temp_soul -= 1
                    self.log(f"🛡️ {def_p.name} 的【我的旅路 伊蕾娜】發動記憶守護！使直接攻擊的【{attacker.name}】魂傷 -1！")

        # GA10/S131-019《炸薯球 艾絲》直接攻擊時選休息室1張黃色卡片放到能量區
        if attacker.id == "GA10/S131-019" and atk_type == "DIRECT":
            wr_yellow = [c for c in atk_p.waiting_room if c.color == "黃"]
            if wr_yellow:
                do_ais_st = (
                    True
                    if atk_p.is_ai
                    else self.ask_yes_no_center(
                        "炸薯球 艾絲", "直接攻擊時，是否從休息室選擇 1 張黃色卡片放到能量區？"
                    )
                )
                if do_ais_st:
                    ch_y = (
                        wr_yellow[0]
                        if atk_p.is_ai
                        else self.choose_card_dialog(
                            "炸薯球 艾絲：選擇放到能量區的黃色卡片", wr_yellow, allow_cancel=False
                        )
                    )
                    atk_p.waiting_room.remove(ch_y)
                    atk_p.stock.append(ch_y)
                    self.log(f"⚡ 【炸薯球 艾絲】將休息室的【{ch_y.name}】置入能量區！")

        # GA17/S131-010《第三章 伊蕾娜》從手牌或回憶區登場的回合中，攻擊時給對手 1 點傷害
        if attacker.id == "GA17/S131-010" and attacker.entered_stage_this_turn:
            do_b1 = (
                True
                if atk_p.is_ai
                else self.ask_yes_no_center(
                    "第三章 伊蕾娜：登場回合攻擊追加傷害",
                    "【第三章 伊蕾娜】於本回合登場並發起攻擊！是否給對手 1 點傷害？",
                )
            )
            if do_b1:
                self.deal_damage(def_p, 1, source_text="第三章 伊蕾娜攻擊追加傷害")
                if self.game_over:
                    return

        # GA10/S131-002《跨越復仇 琉》CX 連動：名場面區有「時隔五年的【能力值】更新」時，看牌組頂最多2張，公開頂1張回收等級X以下角色
        if (
            attacker.id == "GA10/S131-002"
            and atk_p.climax_zone
            and atk_p.climax_zone.id == "GA10/S131-030"
        ):
            self.log("🗡️ 【跨越復仇 琉】發動 CX 連動！")
            if atk_p.is_ai:
                self.check_deck_refresh(atk_p)
            else:
                looked_ryu = self.ask_step_by_step_look_up_to(atk_p, 2, "跨越復仇 琉 CX連動：看牌組頂最多 2 張")
                keep_top = []
                for lc in looked_ryu:
                    put_top = self.ask_yes_no_center(
                        "跨越復仇 琉 CX連動",
                        f"是否將【{lc.name}】放回牌組上方？\n（點擊「否」則將此卡放到休息室）",
                    )
                    if put_top:
                        keep_top.append(lc)
                    else:
                        atk_p.waiting_room.append(lc)
                if len(keep_top) >= 1:
                    keep_top = self.ask_reorder_cards_center(
                        atk_p, keep_top, "跨越復仇 琉 CX連動：調整放回牌組頂的順序"
                    )
                atk_p.deck = keep_top + atk_p.deck

            self.check_deck_refresh(atk_p)
            if atk_p.deck and not self.game_over:
                top_rev = atk_p.deck[0]
                x_lvl = 0 if top_rev.type == "CX" else top_rev.base_level
                self.log(f"🔍 【跨越復仇 琉】公開牌組頂：【{top_rev.name}】，視為 Lv.{x_lvl}！")
                wr_cands = [c for c in atk_p.waiting_room if c.type == "CHAR" and c.base_level <= x_lvl]
                if wr_cands:
                    picked_c = (
                        max(wr_cands, key=lambda x: (x.base_level, x.base_power))
                        if atk_p.is_ai
                        else self.choose_card_dialog(
                            f"跨越復仇 琉：選擇休息室 Lv.{x_lvl} 以下的角色 1 張返回手牌",
                            wr_cands,
                            allow_cancel=True,
                        )
                    )
                    if picked_c:
                        atk_p.waiting_room.remove(picked_c)
                        atk_p.hand.append(picked_c)
                        self.log(f"📥 {atk_p.name} 透過【跨越復仇 琉】連動回收了【{picked_c.name}】！")

        if attacker.id == "BFR/S78-058" and atk_type == "DIRECT":
            wr_games = [c for c in atk_p.waiting_room if c.type == "CHAR" and "遊戲" in c.traits]
            if wr_games:
                do_chg = (
                    True
                    if atk_p.is_ai
                    else self.ask_yes_no_center(
                        "聖女米瑟莉", "直接攻擊時，是否從休息室選擇 1 張《遊戲》角色放到能量區？"
                    )
                )
                if do_chg:
                    ch = (
                        wr_games[0]
                        if atk_p.is_ai
                        else self.choose_card_dialog(
                            "選擇放到能量區的《遊戲》角色", wr_games, allow_cancel=False
                        )
                    )
                    atk_p.waiting_room.remove(ch)
                    atk_p.stock.append(ch)
                    self.log(f"⚡ 【聖女米瑟莉】將休息室的【{ch.name}】置入能量區！")

        if attacker.id == "BFR/S78-069" and atk_type == "FRONT" and len(atk_p.stock) >= 1:
            opp_slots = [i for i in range(5) if def_p.stage[i] is not None]
            if opp_slots:
                do_lv = (
                    True
                    if atk_p.is_ai
                    else self.ask_yes_no_center(
                        "被託付的生命 蜜伊", "正打時，是否支付 (1) 能量讓對手 1 隻角色當回合等級 -1？"
                    )
                )
                if do_lv:
                    self.pay_stock(atk_p, 1)
                    t_s = (
                        slot_idx
                        if atk_p.is_ai
                        else self.select_stage_slot_dialog(
                            def_p, opp_slots, "選擇要等級 -1 的對手角色"
                        )
                    )
                    def_p.stage[t_s].temp_level -= 1
                    self.log(f"📉 【被託付的生命 蜜伊】使對手【{def_p.stage[t_s].name}】等級 -1！")

        # BTR/W107-076《成長歷程 喜多郁代》CX 連動：名場面區有「逐漸增加的回憶」且其他《音樂》角色 4 張以上時，棄 2 手牌給對手 4 點傷害
        if (
            attacker.id == "BTR/W107-076"
            and atk_p.climax_zone
            and atk_p.climax_zone.id == "BTR/W107-100"
        ):
            other_music_cnt = sum(
                1
                for idx_m, cm in enumerate(atk_p.stage)
                if idx_m != slot_idx and cm and "音樂" in cm.traits
            )
            if other_music_cnt >= 4 and len(atk_p.hand) >= 2:
                do_kita_burn = (
                    True
                    if atk_p.is_ai
                    else self.ask_yes_no_center(
                        "成長歷程 喜多郁代：CX 連動",
                        "此卡攻擊時名場面區有「逐漸增加的回憶」且其他《音樂》角色有 4 張以上！\n是否捨棄 2 張手牌，給予對手 4 點傷害？",
                    )
                )
                if do_kita_burn:
                    for n_d in range(2):
                        self.select_hand_discard(
                            atk_p, prompt=f"成長歷程 喜多郁代 CX連動：請選擇捨棄第 {n_d + 1}/2 張手牌"
                        )
                    self.log("🎸🔥 【成長歷程 喜多郁代】發動 CX 連動！給予對手 4 點傷害！")
                    self.deal_damage(def_p, 4, source_text="成長歷程 喜多郁代 CX連動")
                    if self.game_over:
                        return

        if (
            attacker.id == "BFR/S78-082"
            and atk_p.climax_zone
            and atk_p.climax_zone.id == "BFR/S78-107"
        ):
            milled = []
            for _ in range(4):
                self.check_deck_refresh(def_p)
                if def_p.deck:
                    milled.append(self.pop_deck_bottom(def_p))
            def_p.waiting_room.extend(milled)
            cx_cnt = sum(1 for c in milled if c.type == "CX")
            self.log(
                f"🤖 【機械神 梅普露】CX連動！削去對手牌庫底 4 張，其中有 {cx_cnt} 張名場面！"
            )
            if cx_cnt > 0:
                self.deal_damage(def_p, cx_cnt, source_text="機械神 梅普露連動")
                if self.game_over:
                    return

        # BFR/S78-089《大摯友 梅普露＆莎莉》被正打時的不倒置效果統一於防守方反擊步驟 (_handle_local_counter_step) 執行，確保單人與連線模式皆不會被狀態同步覆蓋

        # 萬用資料驅動 ON_ATTACK 效果結算（針對非既有硬編碼特例的新系列卡片）
        HARDCODED_ATK_IDS = {
            "GA10/S131-019", "GA17/S131-010", "GA10/S131-002",
            "BFR/S78-058", "BFR/S78-069", "BTR/W107-076", "BFR/S78-082"
        }
        if attacker.id not in HARDCODED_ATK_IDS:
            self._run_universal_timing(atk_p, def_p, attacker, "ON_ATTACK", slot_idx=slot_idx)
            if self.game_over:
                return

        trig_times = 1
        if attacker.id == "GA10/S131-T09" and len(atk_p.stock) >= 1:
            do_td = (
                True
                if atk_p.is_ai
                else self.ask_yes_no_center(
                    "女神之鐘 赫斯緹雅：雙重判定",
                    "是否支付 (1) 能量，在本次攻擊的判定階段執行 2 次判定？",
                )
            )
            if do_td:
                self.pay_stock(atk_p, 1)
                trig_times = 2
                self.log("🔔 【女神之鐘 赫斯緹雅】發動雙重判定（Twin Drive）！")

        for t_idx in range(trig_times):
            self.check_deck_refresh(atk_p)
            if not atk_p.deck or self.game_over:
                break
            trig_c = self.pop_deck_top(atk_p)
            atk_p.stock.append(trig_c)
            eff_trig = trig_c.trigger
            has_choice_cx_zone = (
                atk_p.climax_zone is not None and atk_p.climax_zone.trigger == "CHOICE"
            )
            if trig_c.id == "GA12/S131-013" and has_choice_cx_zone:
                eff_trig = "CHOICE"

            self.log(f"🎲 攻擊判定翻出：【{trig_c.name}】｜標記：{get_trigger_zh(eff_trig)}")
            trig_added_soul = 1 if (eff_trig in ("SOUL", "GATE") or getattr(trig_c, "trigger", "") == "SOUL") else 0
            if trig_added_soul > 0:
                attacker.temp_soul += trig_added_soul
                self.log(f"⚡ 判定觸發魂刻！{atk_p.name} 的【{attacker.name}】本回合魂傷 +{trig_added_soul}！")
            if eff_trig == "SOUL":
                t_shout = f"⚡ +1 魂傷！翻出【{trig_c.name}】"
                t_badge = "⚡ +1 魂傷！"
                t_bg, t_fg = "#ffd166", "#000000"
            elif eff_trig == "STANDBY":
                t_shout = f"⚙️ 標記：開機觸發！翻出【{trig_c.name}】"
                t_badge = "⚙️ 開機觸發！"
                t_bg, t_fg = "#e63946", "#ffffff"
            elif eff_trig == "GATE":
                t_shout = (
                    f"🚪 標記：城門觸發 ＋ ⚡ +1 魂傷！翻出【{trig_c.name}】"
                    if trig_added_soul
                    else f"🚪 標記：城門觸發！翻出【{trig_c.name}】"
                )
                t_badge = "🚪 城門觸發！"
                t_bg, t_fg = "#4cc9f0", "#000000"
            elif eff_trig == "CHOICE":
                t_shout = f"🏹 標記：箭頭觸發！翻出【{trig_c.name}】"
                t_badge = "🏹 箭頭觸發！"
                t_bg, t_fg = "#ffd166", "#000000"
            else:
                t_shout = f"🎴 攻擊判定翻出：【{trig_c.name}】（無特殊標記）"
                t_badge = "無標記"
                t_bg, t_fg = "#3a3f58", "#ffffff"
            self.update_ui()
            self.run_interactive_card_flip_sequence(
                deck_owner=atk_p,
                clicker_is_ai=atk_p.is_ai,
                banner_title=f"攻擊觸發判定 — {atk_p.name} 的【{attacker.name}】攻擊",
                step_cards_info=[{
                    "card": trig_c,
                    "badge": t_badge,
                    "step_shout": t_shout,
                    "step_bg": t_bg,
                    "step_fg": t_fg,
                    "step_sfx": "sfx_climax" if (eff_trig != "NONE" or trig_c.type == "CX") else "sfx_draw",
                }],
                final_summary_text=t_shout,
                final_summary_bg=t_bg,
                final_summary_fg=t_fg,
                is_trigger_check=True,
            )
            if eff_trig == "STANDBY":
                self.resolve_standby(atk_p, trig_c.id, current_atk_slot=slot_idx)
            elif eff_trig == "GATE":
                cx_in_wr = [c for c in atk_p.waiting_room if c.type == "CX"]
                if cx_in_wr:
                    do_g = (
                        True
                        if atk_p.is_ai
                        else self.ask_yes_no_center(
                            "標記：城門觸發", "判定出城門！是否從休息室選擇 1 張名場面回到手牌？"
                        )
                    )
                    if do_g:
                        ch = (
                            cx_in_wr[0]
                            if atk_p.is_ai
                            else self.choose_card_dialog(
                                "選擇回收的名場面", cx_in_wr, allow_cancel=False
                            )
                        )
                        atk_p.waiting_room.remove(ch)
                        atk_p.hand.append(ch)
                        self.log(f"🚪 城門觸發回收了名場面【{ch.name}】！")
            elif eff_trig == "CHOICE":
                soul_chars = [
                    c for c in atk_p.waiting_room if c.type == "CHAR" and c.trigger == "SOUL"
                ]
                if soul_chars:
                    if atk_p.is_ai:
                        ch_sc = max(soul_chars, key=lambda x: x.base_level)
                        atk_p.waiting_room.remove(ch_sc)
                        atk_p.hand.append(ch_sc)
                        self.log(f"🏹 箭頭觸發：{atk_p.name} 從休息室將【{ch_sc.name}】收回手牌！")
                    else:
                        ch_sc = self.choose_card_dialog(
                            "標記：箭頭觸發 — 選擇休息室 1 張帶有 +1魂傷 標記的角色（可選略過）",
                            soul_chars,
                            allow_cancel=True,
                        )
                        if ch_sc:
                            to_hand = self.ask_yes_no_center(
                                "標記：箭頭觸發",
                                f"已選擇【{ch_sc.name}】！\n點擊【是】👉 返回手牌\n點擊【否】👉 放到能量區",
                            )
                            atk_p.waiting_room.remove(ch_sc)
                            if to_hand:
                                atk_p.hand.append(ch_sc)
                                self.log(f"🏹 箭頭觸發：將【{ch_sc.name}】返回手牌！")
                            else:
                                atk_p.stock.append(ch_sc)
                                self.log(f"🏹 箭頭觸發：將【{ch_sc.name}】置入能量區！")

            # GA10/S131-012《奇怪的妖精 琉》：CX區有箭頭CX時，賦予所有領域的黃色CX「風」觸發
            if (
                trig_c.type == "CX"
                and trig_c.color == "黃"
                and has_choice_cx_zone
                and any(c and c.id == "GA10/S131-012" for c in atk_p.stage)
            ):
                opp_bounce_slots = [
                    i
                    for i in range(5)
                    if def_p.stage[i] is not None and not def_p.stage[i].cannot_return_hand
                ]
                if opp_bounce_slots:
                    do_wind = (
                        True
                        if atk_p.is_ai
                        else self.ask_yes_no_center(
                            "奇怪的妖精 琉：追加風觸發",
                            "因【奇怪的妖精 琉】效果，此黃色名場面獲得「風」觸發！是否選擇對手場上 1 隻角色返回手牌？",
                        )
                    )
                    if do_wind:
                        b_slot = (
                            opp_bounce_slots[0]
                            if atk_p.is_ai
                            else self.select_stage_slot_dialog(
                                def_p, opp_bounce_slots, "風觸發：選擇要吹回手牌的對手角色"
                            )
                        )
                        b_card = def_p.stage[b_slot]
                        def_p.stage[b_slot] = None
                        if b_card.markers:
                            def_p.waiting_room.extend(b_card.markers)
                            b_card.markers.clear()
                        b_card.reset_stage_state()
                        def_p.hand.append(b_card)
                        self.log(f"🌪️ 風觸發發動！將對手的【{b_card.name}】吹回手牌！")
        self.update_ui()

        if atk_p.is_ai:
            self.root.after(
                750,
                lambda orig=attacker: self._finish_attack_after_trigger(
                    atk_p, def_p, slot_idx, atk_type, on_complete, original_attacker=orig
                ),
            )
        else:
            self._finish_attack_after_trigger(
                atk_p, def_p, slot_idx, atk_type, on_complete, original_attacker=attacker
            )

    def _handle_local_counter_step(self, atk_p, def_p, slot_idx):
        attacker = atk_p.stage[slot_idx]
        defender = def_p.stage[slot_idx]
        if not attacker or not defender:
            return

        # BFR/S78-089《大摯友 梅普露＆莎莉》：【自】［(1) 手牌的《遊戲》的角色1張放到休息室］ 此卡被正打時，你可以支付代價。支付代價的話，在那個回合中，此卡不會【倒置】。
        if (defender.id == "BFR/S78-089" or defender.has_effect("AUTO_DEFEND_IMMUNE_REVERSE")) and not defender.cannot_be_reversed:
            g_hand = [c for c in def_p.hand if c.type == "CHAR" and "遊戲" in c.traits]
            if len(def_p.stock) >= 1 and g_hand:
                do_imm = (
                    True
                    if def_p.is_ai
                    else self.ask_yes_no_center(
                        "🛡️ 大摯友 梅普露＆莎莉（被正打不倒置效果）",
                        "我方【大摯友 梅普露＆莎莉】被正面攻擊！\n是否支付 (1) 能量並將手牌 1 張《遊戲》角色放到休息室，使此卡在本回合中不會【倒置】？",
                    )
                )
                if do_imm:
                    disc_c = self.select_hand_discard(
                        def_p,
                        filter_fn=lambda x: x.type == "CHAR" and "遊戲" in x.traits,
                        prompt="大摯友 梅普露＆莎莉：請選擇放到休息室的手牌《遊戲》角色",
                    )
                    if disc_c:
                        self.pay_stock(def_p, 1)
                        defender.cannot_be_reversed = True
                        if defender.state == "REVERSE":
                            defender.state = "REST"
                        self.log(f"🛡️ {def_p.name} 的【大摯友 梅普露＆莎莉】發動效果（捨棄【{disc_c.name}】），本回合不會【倒置】！")
                        self.update_ui()

        backup_blocked = attacker.has_effect("CONT_CANNOT_PLAY_BACKUP") or attacker.id == "BTR/W107-069"
        if backup_blocked:
            self.log(f"🚫 【{attacker.name}】永續效果生效：此卡戰鬥中，對手不能從手牌使用『助太刀』！")

        # BTR/W107-T06《音樂話題～ 伊地知虹夏》助太刀 2000 等級 1 ＋ 公開牌組頂《音樂》角色加手棄1
        nijika_backups = (
            []
            if backup_blocked
            else [
                c
                for c in def_p.hand
                if c.id == "BTR/W107-T06" and len(def_p.level_zone) >= 1 and len(def_p.stock) >= 1
            ]
        )
        if nijika_backups:
            atk_pwr = self.get_effective_power(atk_p, attacker, slot_idx)
            def_pwr = self.get_effective_power(def_p, defender, slot_idx)
            if def_p.is_ai:
                do_nj = def_pwr <= atk_pwr < (def_pwr + 2000)
            else:
                do_nj = self.ask_yes_no_center(
                    "🛡️ 反擊步驟：音樂話題～ 伊地知虹夏",
                    f"對手【{attacker.name}】(攻:{atk_pwr}) 正面攻擊我方【{defender.name}】(攻:{def_pwr})！\n"
                    "是否支付 (1) 能量並捨棄手牌【音樂話題～ 伊地知虹夏】發動『助太刀 2000』（並公開牌組頂 1 張，若為《音樂》角色則加手並棄 1 張手牌）？",
                )
            if do_nj:
                nj_c = nijika_backups[0]
                self.pay_stock(def_p, 1)
                def_p.hand.remove(nj_c)
                def_p.waiting_room.append(nj_c)
                defender.temp_power += 2000
                self.log(f"🥁 {def_p.name} 發動助太刀【音樂話題～ 伊地知虹夏】，【{defender.name}】攻擊力 +2000！")
                self.check_deck_refresh(def_p)
                if def_p.deck and not self.game_over:
                    top_c = def_p.deck[0]
                    self.log(f"🔍 【音樂話題～ 伊地知虹夏】公開牌組頂：【{top_c.name}】")
                    if top_c.type == "CHAR" and "音樂" in top_c.traits:
                        self.pop_deck_top(def_p)
                        def_p.hand.append(top_c)
                        self.log(f"🎵 公開卡為《音樂》角色！【{top_c.name}】加入手牌，並捨棄 1 張手牌。")
                        self.select_hand_discard(def_p, prompt="音樂話題～ 伊地知虹夏：請選擇捨棄 1 張手牌")
                    else:
                        self.log("🎵 公開卡非《音樂》角色，放回牌組頂原位。")
                self.update_ui()

        mahiru_backups = (
            []
            if backup_blocked
            else [
                c
                for c in def_p.hand
                if c.id == "GA02/S131-009" and len(def_p.level_zone) >= 2 and len(def_p.stock) >= 1
            ]
        )
        if mahiru_backups:
            atk_pwr = self.get_effective_power(atk_p, attacker, slot_idx)
            def_pwr = self.get_effective_power(def_p, defender, slot_idx)
            if def_p.is_ai:
                do_mb = (def_pwr <= atk_pwr < (def_pwr + 2500)) or (len(def_p.deck) <= 5 and len(def_p.stock) >= 3)
            else:
                do_mb = self.ask_yes_no_center(
                    "🛡️ 反擊步驟：告別膽小的自己 椎名真晝",
                    f"對手【{attacker.name}】(攻:{atk_pwr}) 正面攻擊我方【{defender.name}】(攻:{def_pwr})！\n"
                    "是否支付 (1) 能量並捨棄手牌【告別膽小的自己 椎名真晝】發動『助太刀 2500』（並可額外支付 2 能量將休息室全部洗回牌組）？",
                )
            if do_mb:
                mb_c = mahiru_backups[0]
                self.pay_stock(def_p, 1)
                def_p.hand.remove(mb_c)
                def_p.waiting_room.append(mb_c)
                defender.temp_power += 2500
                self.log(f"🛡️ {def_p.name} 發動助太刀【告別膽小的自己 椎名真晝】，【{defender.name}】攻擊力 +2500！")
                if len(def_p.stock) >= 2 and len(def_p.waiting_room) > 0:
                    do_ref = (
                        (len(def_p.deck) <= 6)
                        if def_p.is_ai
                        else self.ask_yes_no_center(
                            "告別膽小的自己 椎名真晝：椎名拳洗牌",
                            f"是否額外支付 (2) 能量，將自己休息室的全部 {len(def_p.waiting_room)} 張卡片返回牌組並洗牌？",
                        )
                    )
                    if do_ref:
                        self.pay_stock(def_p, 2)
                        def_p.deck.extend(def_p.waiting_room)
                        def_p.waiting_room.clear()
                        random.shuffle(def_p.deck)
                        self.log("♻️ 【告別膽小的自己 椎名真晝】發動休息室全數返回牌組重洗（無罰血）！")
                self.update_ui()

        counters = [
            c
            for c in def_p.hand
            if c.id == "BFR/S78-075" and self.can_play_card(def_p, c)
        ]
        if counters:
            atk_pwr = self.get_effective_power(atk_p, attacker, slot_idx)
            def_pwr = self.get_effective_power(def_p, defender, slot_idx)
            if def_p.is_ai:
                do_cnt = def_pwr <= atk_pwr < (def_pwr + 2500)
            else:
                do_cnt = self.ask_yes_no_center(
                    "🛡️ 反擊步驟 (助太刀時機)",
                    f"對手【{attacker.name}】(攻擊力:{atk_pwr}) 正面攻擊我方【{defender.name}】(攻擊力:{def_pwr})！\n\n"
                    "是否支付 (1) 點能量發動手牌中的【獨有系列】(任一《遊戲》角色攻擊力+2500 並將此卡送入回憶區)？",
                )
            if do_cnt:
                ev = counters[0]
                self.pay_stock(def_p, ev.cost)
                def_p.hand.remove(ev)
                game_slots = [
                    i
                    for i in range(5)
                    if def_p.stage[i] and "遊戲" in def_p.stage[i].traits
                ]
                t_slot = (
                    slot_idx
                    if def_p.is_ai
                    else self.select_stage_slot_dialog(
                        def_p, game_slots, "獨有系列：選擇要 +2500 攻擊力的《遊戲》角色"
                    )
                )
                def_p.stage[t_slot].temp_power += 2500
                def_p.memory.append(ev)
                self.log(
                    f"⚡ {def_p.name} 發動反擊【獨有系列】，【{def_p.stage[t_slot].name}】攻擊力 +2500！"
                )
                self.update_ui()

        # 萬用資料驅動『助太刀 (BACKUP)』支援（任何從貓罐子匯入的新系列助太刀角色皆可發動）
        if not backup_blocked:
            uni_backups = []
            for c in def_p.hand:
                if c.id in {"BTR/W107-T06", "GA02/S131-009", "BFR/S78-075"}:
                    continue
                for ab in getattr(c, "parsed_abilities", []):
                    if ab.get("category") == "BACKUP":
                        req_lv = ab.get("level", 1)
                        st_cost = ab.get("cost", {}).get("stock", c.cost)
                        if len(def_p.level_zone) >= req_lv and len(def_p.stock) >= st_cost:
                            uni_backups.append((c, ab, st_cost))
            if uni_backups:
                b_card, b_ab, b_stock = uni_backups[0]
                b_pwr = b_ab.get("power", 1500)
                atk_pwr = self.get_effective_power(atk_p, attacker, slot_idx)
                def_pwr = self.get_effective_power(def_p, defender, slot_idx)
                do_ub = (def_pwr <= atk_pwr < (def_pwr + b_pwr)) if def_p.is_ai else self.ask_yes_no_center(
                    f"🛡️ 反擊步驟：助太刀【{b_card.name}】",
                    f"對手【{attacker.name}】(攻:{atk_pwr}) 正面攻擊我方【{defender.name}】(攻:{def_pwr})！\n"
                    f"是否支付 ({b_stock}) 能量並捨棄手牌【{b_card.name}】，使【{defender.name}】本回合攻擊力 +{b_pwr}？"
                )
                if do_ub:
                    self.pay_stock(def_p, b_stock)
                    if b_card in def_p.hand:
                        def_p.hand.remove(b_card)
                        def_p.waiting_room.append(b_card)
                    defender.temp_power += b_pwr
                    self.log(f"🛡️ {def_p.name} 發動助太刀【{b_card.name}】，【{defender.name}】攻擊力 +{b_pwr}！")
                    self.update_ui()

    def _finish_attack_after_trigger(
        self, atk_p, def_p, slot_idx, atk_type, on_complete, original_attacker=None
    ):
        if self.game_over:
            return
        cur_slot_card = atk_p.stage[slot_idx]
        defender = def_p.stage[slot_idx]
        # 關鍵判定：若攻擊格在判定階段被開機 (Standby) 壓卡替換，新登場的角色並非原攻擊角色，保持【橫置】且不進行戰鬥比拼！
        attacker_is_same = (
            not getattr(self, "_current_attack_slot_overwritten", False)
            and ((original_attacker is None) or (cur_slot_card is original_attacker))
        )
        active_attacker = cur_slot_card if attacker_is_same else original_attacker

        if attacker_is_same and atk_type == "FRONT" and defender and cur_slot_card:
            backup_blocked = cur_slot_card.has_effect("CONT_CANNOT_PLAY_BACKUP") or cur_slot_card.id == "BTR/W107-069"
            has_bfr089_def = (
                (defender.id == "BFR/S78-089" or defender.has_effect("AUTO_DEFEND_IMMUNE_REVERSE"))
                and not defender.cannot_be_reversed
                and len(def_p.stock) >= 1
                and any(c.type == "CHAR" and "遊戲" in c.traits for c in def_p.hand)
            )
            has_counter = has_bfr089_def or any(
                (
                    not backup_blocked
                    and c.id == "GA02/S131-009"
                    and len(def_p.level_zone) >= 2
                    and len(def_p.stock) >= 1
                )
                or (
                    not backup_blocked
                    and c.id == "BTR/W107-T06"
                    and len(def_p.level_zone) >= 1
                    and len(def_p.stock) >= 1
                )
                or (c.id == "BFR/S78-075" and self.can_play_card(def_p, c))
                for c in def_p.hand
            )
            if has_counter:
                if self.is_lan and def_p == self.ai and self.net_node and self.net_node.connected:
                    self.net_node.send({
                        "type": "COUNTER_REQ",
                        "slot_idx": slot_idx,
                        "sender_state": self.player.to_sync_dict(),
                        "receiver_state": self.ai.to_sync_dict(),
                    })
                    def _wait_cnt(frame):
                        tk.Label(
                            frame,
                            text=f"⏳ 等待對手【{self.ai.name}】確認反擊助太刀時機...",
                            bg="#1e2230",
                            fg="#ffd166",
                            font=("Microsoft JhengHei", 15, "bold"),
                        ).pack(pady=80)
                    self._show_overlay_and_wait(_wait_cnt)
                else:
                    self._handle_local_counter_step(atk_p, def_p, slot_idx)

        if active_attacker:
            dmg = self.get_effective_soul(atk_p, active_attacker, slot_idx)
            self.deal_damage(def_p, dmg, source_text=f"{active_attacker.name} 攻擊")
            if self.game_over:
                return

        if not attacker_is_same:
            # 確保開機壓上該格的新角色維持【橫置 (REST)】，絕不倒置
            if atk_p.stage[slot_idx] is not None:
                atk_p.stage[slot_idx].state = "REST"
                self.log(
                    f"⚙️ 位置 {slot_idx} 已由開機登場的【{atk_p.stage[slot_idx].name}】覆蓋，維持【橫置】狀態不進行戰鬥比拼。"
                )
        else:
            defender = def_p.stage[slot_idx]
            if atk_type == "FRONT" and cur_slot_card and defender:
                atk_pwr = self.get_effective_power(atk_p, cur_slot_card, slot_idx)
                def_pwr = self.get_effective_power(def_p, defender, slot_idx)
                self.log(
                    f"⚔️ 戰鬥比拼：【{cur_slot_card.name}】({atk_pwr}) vs 【{defender.name}】({def_pwr})"
                )

                if atk_pwr > def_pwr:
                    self.reverse_character(def_p, slot_idx, victor_p=atk_p, victor_slot=slot_idx)
                elif atk_pwr < def_pwr:
                    self.reverse_character(atk_p, slot_idx, victor_p=def_p, victor_slot=slot_idx)
                else:
                    self.reverse_character(def_p, slot_idx, victor_p=atk_p, victor_slot=slot_idx)
                    self.reverse_character(atk_p, slot_idx, victor_p=def_p, victor_slot=slot_idx)

        self.update_ui()
        if self.is_lan and atk_p == self.player:
            self._broadcast_action(f"完成位置 {slot_idx} 的攻擊結算")
        if on_complete and not self.game_over:
            self.root.after(900, on_complete)

    def reverse_character(
        self, loser_p: PlayerState, slot_idx: int, victor_p: PlayerState, victor_slot: int
    ):
        loser = loser_p.stage[slot_idx]
        victor = victor_p.stage[victor_slot]
        if not loser:
            return
        if loser.cannot_be_reversed:
            if loser.state == "REVERSE":
                loser.state = "REST"
            self.log(f"🛡️ 【{loser.name}】擁有『本回合不會倒置』效果，穩守舞台不倒置！")
            self.update_ui()
            return
        if loser.state == "REVERSE":
            return

        loser.state = "REVERSE"
        self.log(f"💥 {loser_p.name} 的【{loser.name}】戰鬥落敗【倒置】！")
        self.update_ui()

        for idx, c in enumerate(victor_p.stage):
            if c and c.id == "BFR/S78-001" and idx != victor_slot:
                c.temp_power += 1000
                self.log("🔨 【戰鬥的工匠 伊茲】因隊友擊倒對手，攻擊力 +1000！")

        # BTR/W107-T17《高人氣 喜多郁代》：其他的你的戰鬥中的角色【倒置】時，在那回合中，此卡的攻擊力+2000
        # BTR/W107-077《裝過頭的面子 後藤一里》：其他的你的戰鬥中的角色【倒置】時，你選擇自己的角色1張，在那回合中，攻擊力+1000
        for idx, c in enumerate(loser_p.stage):
            if idx != slot_idx and c:
                if c.id == "BTR/W107-T17":
                    c.temp_power += 2000
                    self.log(f"✨ {loser_p.name} 的【高人氣 喜多郁代】因隊友戰鬥倒置，本回合攻擊力 +2000！")
                if c.id == "BTR/W107-077":
                    my_slots = [i for i in range(5) if loser_p.stage[i] is not None]
                    if my_slots:
                        t_s = (
                            my_slots[0]
                            if loser_p.is_ai
                            else self.select_stage_slot_dialog(
                                loser_p, my_slots, "裝過頭的面子 後藤一里：選擇 1 隻角色攻擊力 +1000"
                            )
                        )
                        loser_p.stage[t_s].temp_power += 1000
                        self.log(
                            f"🎸 {loser_p.name} 的【裝過頭的面子 後藤一里】觸發！使【{loser_p.stage[t_s].name}】攻擊力 +1000！"
                        )

        # BTR/W107-T15《陽角 喜多郁代》：當戰鬥中的此卡【倒置】時，看牌組頂最多 3 張選最多 1 張名場面加手，加手則棄 1 手牌
        if loser.id == "BTR/W107-T15":
            looked_cx = self.ask_step_by_step_look_up_to(
                loser_p, 3, "陽角 喜多郁代：看牌組頂最多 3 張選名場面"
            )
            valid_cxs = [c for c in looked_cx if c.type == "CX"]
            picked_cx = None
            if valid_cxs:
                picked_cx = (
                    valid_cxs[0]
                    if loser_p.is_ai
                    else self.choose_card_dialog(
                        "陽角 喜多郁代：選擇最多 1 張名場面加入手牌（加手的話須捨棄 1 張手牌）",
                        valid_cxs,
                        allow_cancel=True,
                    )
                )
            if picked_cx:
                loser_p.hand.append(picked_cx)
                looked_cx.remove(picked_cx)
                loser_p.waiting_room.extend(looked_cx)
                self.log(f"🌟 {loser_p.name} 的【陽角 喜多郁代】取得名場面【{picked_cx.name}】加入手牌！")
                self.select_hand_discard(loser_p, prompt="陽角 喜多郁代：因名場面加手，請選擇捨棄 1 張手牌")
            else:
                loser_p.waiting_room.extend(looked_cx)

        # BTR/W107-075《晚霞的歸路 喜多郁代》CX 連動擊倒對手時回收《音樂》角色
        if victor and victor.salvage_music_on_reverse:
            wr_music = [c for c in victor_p.waiting_room if c.type == "CHAR" and "音樂" in c.traits]
            if wr_music:
                rec_m = (
                    max(wr_music, key=lambda x: (x.base_level, x.base_power))
                    if victor_p.is_ai
                    else self.choose_card_dialog(
                        "晚霞的歸路 喜多郁代 CX連動：從休息室選擇 1 張《音樂》角色回到手牌",
                        wr_music,
                        allow_cancel=True,
                    )
                )
                if rec_m:
                    victor_p.waiting_room.remove(rec_m)
                    victor_p.hand.append(rec_m)
                    self.log(f"🌇 【晚霞的歸路 喜多郁代】連動擊倒對手，從休息室回收了【{rec_m.name}】！")

        # BTR/W107-T18《喜多郁代》【起】能力獲得的擊倒送時計區
        if victor and victor.clock_kick_on_reverse and loser_p.stage[slot_idx] == loser:
            do_ck = (
                True
                if victor_p.is_ai
                else self.ask_yes_no_center(
                    "喜多郁代：擊倒送時計區",
                    f"戰鬥對手【{loser.name}】倒置！是否將【{loser.name}】直接放到對手的時計區（傷害區）？",
                )
            )
            if do_ck:
                loser_p.stage[slot_idx] = None
                if loser.markers:
                    loser_p.waiting_room.extend(loser.markers)
                    loser.markers.clear()
                loser.reset_stage_state()
                loser_p.clock.append(loser)
                self.log(f"⏰ 【喜多郁代】將戰鬥落敗的【{loser.name}】直接打進對手時計區！")
                self.check_level_up(loser_p)
                self.update_ui()
                return

        if loser.id == "BFR/S78-069" and victor and victor.state != "REVERSE":
            v_lvl = self.get_effective_level(victor_p, victor, victor_slot)
            if v_lvl <= 2 and not victor.cannot_be_reversed:
                do_bomb = (
                    True
                    if loser_p.is_ai
                    else self.ask_yes_no_center(
                        "被託付的生命 蜜伊",
                        f"戰鬥對手【{victor.name}】當前為等級 {v_lvl} (Lv.2 以下)！是否將其相殺【倒置】？",
                    )
                )
                if do_bomb:
                    victor.state = "REVERSE"
                    self.log(f"💣 相殺發動！【被託付的生命 蜜伊】將【{victor.name}】一併【倒置】！")

        if (
            victor
            and victor.id == "BFR/S78-063"
            and victor_p.climax_zone
            and victor_p.climax_zone.id == "BFR/S78-077"
        ):
            if len(victor_p.stock) >= 6 and len(victor_p.hand) >= 2:
                do_fin = (
                    True
                    if victor_p.is_ai
                    else self.ask_yes_no_center(
                        "暴虐 梅普露 CX連動",
                        "戰鬥對手倒置！是否支付代價［(6) 能量、捨棄 2 張手牌、將名場面「Boss級怪物」送入休息室］，給予對手 1點、2點、3點 連續傷害？",
                    )
                )
                if do_fin:
                    self.pay_stock(victor_p, 6)
                    for n in range(2):
                        self.select_hand_discard(
                            victor_p, prompt=f"暴虐 梅普露連動：請選擇捨棄第 {n+1}/2 張手牌"
                        )
                    cx = victor_p.climax_zone
                    victor_p.climax_zone = None
                    victor_p.waiting_room.append(cx)
                    self.log("🐉 【暴虐 梅普露】發動毀滅連擊：1點、2點、3點傷害！")
                    for dmg_val in [1, 2, 3]:
                        if not self.game_over:
                            self.deal_damage(
                                loser_p, dmg_val, source_text=f"暴虐 梅普露連動({dmg_val}點)"
                            )

        # GA10/S131-029《蕾菲亞&艾絲》賦予的早出相殺送能量
        if loser.anti_early_play_stock_bomb and victor and victor_p.stage[victor_slot] == victor:
            v_lvl = self.get_effective_level(victor_p, victor, victor_slot)
            if v_lvl > len(victor_p.level_zone):
                do_eb = (
                    True
                    if loser_p.is_ai
                    else self.ask_yes_no_center(
                        "蕾菲亞&艾絲：早出相殺送能量",
                        f"戰鬥對手【{victor.name}】(Lv.{v_lvl}) 高於對手玩家等級 (Lv.{len(victor_p.level_zone)})！\n是否將其放到對手能量區，並將對手能量區下方 1 張放到休息室？",
                    )
                )
                if do_eb:
                    victor_p.stage[victor_slot] = None
                    if victor.markers:
                        victor_p.waiting_room.extend(victor.markers)
                        victor.markers.clear()
                    victor.reset_stage_state()
                    victor_p.stock.append(victor)
                    if victor_p.stock:
                        bot_st = victor_p.stock.pop(0)
                        victor_p.waiting_room.append(bot_st)
                    self.log(f"⚡ 早出相殺發動！將對手的【{victor.name}】送入能量區並削去底層能量！")

        # GA17/S131-010《第三章 伊蕾娜》倒置時放到回憶區
        if loser.id == "GA17/S131-010" and loser_p.stage[slot_idx] == loser and not loser.cannot_go_memory:
            loser_p.stage[slot_idx] = None
            if loser.markers:
                loser_p.waiting_room.extend(loser.markers)
                loser.markers.clear()
            loser.reset_stage_state()
            loser_p.memory.append(loser)
            self.log(f"🪄 {loser_p.name} 的【第三章 伊蕾娜】倒置時返回回憶區！")

        # GA17/S131-015《第一章 伊蕾娜》擊倒對手時：[(1) 此卡放休息室] 將休息室「第二章 伊蕾娜」放回憶區，看頂最多3張排序，下個抽牌階段登場
        if victor and victor.id == "GA17/S131-015" and victor_p.stage[victor_slot] == victor:
            other_ga = sum(
                1 for i, c in enumerate(victor_p.stage) if i != victor_slot and c and "GA文庫" in c.traits
            )
            ch2_in_wr = [c for c in victor_p.waiting_room if c.id == "GA17/S131-017"]
            if other_ga >= 2 and len(victor_p.stock) >= 1 and ch2_in_wr:
                do_ch1 = (
                    True
                    if victor_p.is_ai
                    else self.ask_yes_no_center(
                        "第一章 伊蕾娜：記憶傳承第二章",
                        "戰鬥對手倒置！是否支付 (1) 能量並將【第一章 伊蕾娜】放到休息室，把休息室的「第二章 伊蕾娜」放到回憶區（並於下次抽牌階段開始時登場）？",
                    )
                )
                if do_ch1:
                    self.pay_stock(victor_p, 1)
                    self.send_stage_to_wr(victor_p, victor_slot)
                    ch2_card = ch2_in_wr[0]
                    if ch2_card in victor_p.waiting_room:
                        victor_p.waiting_room.remove(ch2_card)
                        victor_p.memory.append(ch2_card)
                        victor_p.pending_draw_phase_spawns.append("GA17/S131-017")
                        self.log("📖 【第一章 伊蕾娜】將「第二章 伊蕾娜」送入回憶區，預約於下次抽牌階段登場！")
                        if not victor_p.is_ai:
                            top3 = self.ask_step_by_step_look_up_to(
                                victor_p,
                                3,
                                "第一章 伊蕾娜：看牌組上方最多 3 張",
                                show_lv1_hint=False,
                                allow_skip_all=True,
                            )
                            if len(top3) >= 1:
                                top3 = self.ask_reorder_cards_center(
                                    victor_p,
                                    top3,
                                    "第一章 伊蕾娜：左鍵拖移調整放回牌庫上方的順序",
                                )
                            victor_p.deck = top3 + victor_p.deck

        # GA17/S131-017《第二章 伊蕾娜》擊倒對手時：[(1) 此卡放休息室] 將休息室「第三章 伊蕾娜」放回憶區，看頂1張（上/下/休息室），下個抽牌階段登場
        if victor and victor.id == "GA17/S131-017" and victor_p.stage[victor_slot] == victor:
            other_ga = sum(
                1 for i, c in enumerate(victor_p.stage) if i != victor_slot and c and "GA文庫" in c.traits
            )
            ch3_in_wr = [c for c in victor_p.waiting_room if c.id == "GA17/S131-010"]
            if other_ga >= 1 and len(victor_p.stock) >= 1 and ch3_in_wr:
                do_ch2 = (
                    True
                    if victor_p.is_ai
                    else self.ask_yes_no_center(
                        "第二章 伊蕾娜：記憶傳承第三章",
                        "戰鬥對手倒置！是否支付 (1) 能量並將【第二章 伊蕾娜】放到休息室，把休息室的「第三章 伊蕾娜」放到回憶區（並於下次抽牌階段開始時登場）？",
                    )
                )
                if do_ch2:
                    self.pay_stock(victor_p, 1)
                    self.send_stage_to_wr(victor_p, victor_slot)
                    ch3_card = ch3_in_wr[0]
                    if ch3_card in victor_p.waiting_room:
                        victor_p.waiting_room.remove(ch3_card)
                        victor_p.memory.append(ch3_card)
                        victor_p.pending_draw_phase_spawns.append("GA17/S131-010")
                        self.log("📖 【第二章 伊蕾娜】將「第三章 伊蕾娜」送入回憶區，預約於下次抽牌階段登場！")
                        self.check_deck_refresh(victor_p)
                        if victor_p.deck and not victor_p.is_ai and not self.game_over:
                            top1 = self.pop_deck_top(victor_p)
                            keep_t = self.ask_yes_no_center(
                                "第二章 伊蕾娜：觀看牌組頂 1 張",
                                f"牌組頂為【{top1.name}】！\n點擊【是】👉 放回牌組上方\n點擊【否】👉 送到休息室",
                            )
                            if keep_t:
                                victor_p.deck.insert(0, top1)
                            else:
                                victor_p.waiting_room.append(top1)

        # 萬用資料驅動 ON_REVERSED (被倒置相殺) 與 ON_REVERSE_OPP (擊倒對手時連動/踢鐘/回手)
        HARDCODED_REV_IDS = {
            "BFR/S78-073", "BFR/S78-060", "GA13/S131-077",
            "BFR/S78-081", "GA02/S131-003", "GA12/S131-013", "GA17/S131-017"
        }
        if target_c and target_c.id not in HARDCODED_REV_IDS and victor_p:
            self._run_universal_timing(p, victor_p, target_c, "ON_REVERSED", slot_idx=slot_idx, target_opp_slot=victor_slot)
        if victor_p and victor_slot is not None and victor_p.stage[victor_slot]:
            v_card = victor_p.stage[victor_slot]
            if v_card.id not in HARDCODED_REV_IDS:
                self._run_universal_timing(victor_p, p, v_card, "ON_REVERSE_OPP", slot_idx=victor_slot, target_opp_slot=slot_idx)

    # ------------------------------------------
    # AI 慢速步進狀態機
    # ------------------------------------------
    def _pick_ai_clock_card_index(self) -> int:
        """智慧痛抽評估：判斷 AI 在計時階段是否應該痛抽，並回傳最適合放進時鐘區的手牌索引（若不痛抽則回傳 None）"""
        if not self.ai.hand or len(self.ai.hand) >= 7:
            return None

        ai_lv = len(self.ai.level_zone)
        ai_clk = len(self.ai.clock)

        # 等級 3 時除非手牌極度乾涸 (<=2) 且時鐘安全 (<=2)，否則不痛抽以免自爆
        if ai_lv >= 3:
            if not (ai_clk <= 2 and len(self.ai.hand) <= 2):
                return None
        elif ai_lv == 2:
            # 等級 2 時，若時鐘已達 5 點以上且手牌充裕 (>=5)，保留血量不痛抽
            if ai_clk >= 5 and len(self.ai.hand) >= 5:
                return None
        # 等級 0 與等級 1（含先攻首回合抽牌後 6 張手牌）積極執行痛抽補牌與湊色！

        existing_colors = {c.color for c in self.ai.level_zone + self.ai.clock}
        needed_colors = {
            c.color for c in self.ai.hand if c.type != "CX" and c.base_level >= 1
        } - existing_colors
        cx_indices = [i for i, c in enumerate(self.ai.hand) if c.type == "CX"]
        lv0_chars = [i for i, c in enumerate(self.ai.hand) if c.type == "CHAR" and c.base_level == 0]

        best_idx = None
        best_score = -9999

        for idx, c in enumerate(self.ai.hand):
            score = 0
            if c.type == "CX":
                # 手上只有 1 張名場面時盡量保留供連動與加魂；若有 2 張以上名場面則優先痛抽多餘名場面
                if len(cx_indices) >= 2:
                    score += 85
                else:
                    score -= 120
            else:
                # 優先痛抽目前等級還打不出來的高等級卡（如 Lv.0 時手上的 Lv.2 / Lv.3）
                if c.base_level > ai_lv + 1:
                    score += 95 + c.base_level * 10
                elif c.base_level > ai_lv:
                    score += 55 + c.cost * 10
                elif c.base_level == 0 and ai_lv == 0:
                    # Lv.0 時若只有 1~2 張 Lv.0 角色，避免把唯一能出場的 Lv.0 痛抽掉
                    if len(lv0_chars) <= 2:
                        score -= 80
                    else:
                        score += 20

                # 若該卡顏色正好是湊色所需的顏色，加分優先置入時鐘區
                if c.color in needed_colors:
                    score += 45

                # 同條件下優先保留高攻擊力主力
                score -= c.base_power // 1000

            if score > best_score:
                best_score = score
                best_idx = idx

        return best_idx

    def ai_step_clock(self):
        if self.game_over:
            return
        clk_idx = self._pick_ai_clock_card_index()
        if clk_idx is not None and 0 <= clk_idx < len(self.ai.hand):
            c = self.ai.hand.pop(clk_idx)
            self.ai.clock.append(c)
            self.log(f"⏰ {self.ai.name} 執行計時痛抽：將【{c.name}】置入時鐘區並抽取 2 張牌！")
            self.check_level_up(self.ai)
            if self.game_over:
                return
            self.draw_cards(self.ai, 2)
        else:
            self.log(f"⏰ {self.ai.name} 評估手牌與血量後選擇略過計時階段痛抽。")
        self.root.after(900, self.ai_step_main)

    def ai_step_main(self):
        if self.game_over:
            return
        self.enter_main_phase(self.ai)

        # 1. AI 若手牌有可使用之檢索事件（如 BTR/W107-T10 樂團名「團結Band」），優先發動補牌
        ev_indices = [
            i
            for i, c in enumerate(self.ai.hand)
            if c.type == "EVENT"
            and (c.id == "BTR/W107-T10" or c.has_effect("EVENT_SEARCH_MUSIC_OR_CX"))
            and self.can_play_card(self.ai, c)
        ]
        if ev_indices:
            ev_i = ev_indices[0]
            ev_card = self.ai.hand.pop(ev_i)
            self.pay_stock(self.ai, ev_card.cost)
            self.ai.waiting_room.append(ev_card)
            valid_targets = [
                c
                for c in self.ai.deck
                if (c.type == "CHAR" and "音樂" in c.traits)
            ]
            if valid_targets:
                chosen = max(valid_targets, key=lambda x: (x.base_level <= len(self.ai.level_zone), x.base_power))
                self.remove_card_from_deck(self.ai, chosen)
                self.ai.hand.append(chosen)
                self.log(f"🎸 {self.ai.name} 使用事件【{ev_card.name}】，從牌組檢索【{chosen.name}】加入手牌！")
            random.shuffle(self.ai.deck)
            self.update_ui()

        # 2. 智慧調整前後列位置：僅在手牌或場上有其他角色可擔任前排攻擊手時，才將前列支援角色退至後列
        support_ids = {
            "BFR/S78-031",
            "BFR/S78-102",
            "BFR/S78-061",
            "GA10/S131-012",
            "GA17/S131-014",
            "BTR/W107-T02",
            "BTR/W107-T13",
            "BTR/W107-046",
        }
        playable_chars_now = [
            c for c in self.ai.hand if c.type == "CHAR" and self.can_play_card(self.ai, c)
        ]
        for f_i in [0, 1, 2]:
            fc = self.ai.stage[f_i]
            if fc and fc.id in support_ids and not fc.cannot_move:
                other_front_stand = sum(
                    1
                    for o_i in [0, 1, 2]
                    if o_i != f_i and self.ai.stage[o_i] and self.ai.stage[o_i].state == "STAND"
                )
                # 確保退到後列後，AI 至少還有手牌可出到前列、或前列已有其他正置角色可攻擊
                if other_front_stand >= 1 or len(playable_chars_now) >= 1:
                    empty_b = [b_i for b_i in [3, 4] if self.ai.stage[b_i] is None]
                    if empty_b:
                        b_dst = empty_b[0]
                        self.ai.stage[b_dst] = fc
                        self.ai.stage[f_i] = None
                        self.log(f"🔄 {self.ai.name} 將支援角色【{fc.name}】移至後列位置 {b_dst}。")

        # 3. 優先填滿前列攻擊格！先攻首回合優先放到前列中央 (1)，若有第 2 張支援卡再放後列 (3)；一般回合先排前列 [1, 0, 2] 再排後列 [3, 4]
        if self.turn_count == 1 and self.first_player == self.ai:
            self.ai_deploy_slots = [1, 3]
        else:
            self.ai_deploy_slots = [1, 0, 2, 3, 4]
        self.root.after(800, self.ai_step_deploy_next)

    def ai_step_deploy_next(self):
        if self.game_over:
            return
        support_ids = {
            "BFR/S78-031",
            "BFR/S78-102",
            "BFR/S78-061",
            "GA10/S131-012",
            "GA17/S131-014",
            "BTR/W107-T02",
            "BTR/W107-T13",
            "BTR/W107-046",
        }
        while self.ai_deploy_slots:
            slot = self.ai_deploy_slots.pop(0)
            cur_c = self.ai.stage[slot]
            # 允許於空位登場，或於前列壓掉已被倒置 (REVERSE) 的角色
            can_deploy_here = (cur_c is None) or (slot in [0, 1, 2] and cur_c.state == "REVERSE")
            if can_deploy_here:
                playable = [
                    idx
                    for idx, c in enumerate(self.ai.hand)
                    if c.type == "CHAR" and self.can_play_card(self.ai, c)
                ]
                if playable:
                    if slot in [0, 1, 2]:
                        # 前列攻擊格：優先選擇非支援型、等級高且攻擊力高的主力角色（並考慮剩餘能量不要把唯一能出 2 隻的能量單卡花光，除非該卡是強力主力）
                        atk_playable = [i for i in playable if self.ai.hand[i].id not in support_ids]
                        pool = atk_playable if atk_playable else playable
                        best_idx = max(
                            pool,
                            key=lambda i: (
                                self.get_effective_level(self.ai, self.ai.hand[i], None),
                                self.ai.hand[i].base_power,
                                -self.ai.hand[i].cost,
                            ),
                        )
                    else:
                        # 後列支援格：僅當前排已經至少有 1 隻正置角色（或手牌有純支援角色且出了之後仍有角色能站前排）時才放後列
                        front_stand_cnt = sum(
                            1 for f_i in [0, 1, 2] if self.ai.stage[f_i] and self.ai.stage[f_i].state == "STAND"
                        )
                        sup_playable = [i for i in playable if self.ai.hand[i].id in support_ids]
                        if sup_playable and (front_stand_cnt >= 1 or len(playable) >= 2):
                            best_idx = sup_playable[0]
                        elif front_stand_cnt >= 3 and playable:
                            best_idx = min(playable, key=lambda i: self.ai.hand[i].base_power)
                        else:
                            continue
                    self.play_character_from_hand(self.ai, best_idx, slot)
                    self.root.after(850, self.ai_step_deploy_next)
                    return

        # 4. 保底矯正：若部署完畢後，AI 前列 [0, 1, 2] 完全沒有任何正置 (STAND) 角色，但後列 [3, 4] 有可移動的正置角色，立即將後列角色移到前列中央作戰！
        front_stand_now = [
            f_i for f_i in [0, 1, 2] if self.ai.stage[f_i] and self.ai.stage[f_i].state == "STAND"
        ]
        if not front_stand_now:
            movable_back = [
                b_i
                for b_i in [3, 4]
                if self.ai.stage[b_i]
                and self.ai.stage[b_i].state == "STAND"
                and not self.ai.stage[b_i].cannot_move
            ]
            target_front_slots = [
                f_i for f_i in [1, 0, 2] if self.ai.stage[f_i] is None or self.ai.stage[f_i].state == "REVERSE"
            ]
            while movable_back and target_front_slots:
                b_src = movable_back.pop(0)
                f_dst = target_front_slots.pop(0)
                self.ai.stage[f_dst], self.ai.stage[b_src] = (
                    self.ai.stage[b_src],
                    self.ai.stage[f_dst],
                )
                self.log(
                    f"⚔️ {self.ai.name} 將後列的【{self.ai.stage[f_dst].name}】推進至前列位置 {f_dst} 準備發動攻擊！"
                )
                if self.turn_count == 1 and self.first_player == self.ai:
                    break

        # 3. AI 於主要階段結束前自動發動後列有利的【起】能力
        for s_i in [3, 4, 0, 1, 2]:
            sc = self.ai.stage[s_i]
            if not sc or sc.state != "STAND":
                continue
            if sc.id == "BFR/S78-061":
                sc.state = "REST"
                self.trigger_act_used_bonus(self.ai)
                if len(sc.markers) == 0:
                    self.check_deck_refresh(self.ai)
                    if self.ai.deck:
                        top_c = self.ai.deck[0]
                        lvl = 0 if top_c.type == "CX" else top_c.base_level
                        if lvl >= 1:
                            self.pop_deck_top(self.ai)
                            sc.markers.append(top_c)
                            self.log(f"🔖 {self.ai.name} 發動【作戰變更 米瑟莉】吸收牌庫頂【{top_c.name}】為標記！")
                else:
                    mk = sc.markers.pop(0)
                    self.ai.stock.append(mk)
                    self.log(f"⚡ {self.ai.name} 發動【作戰變更 米瑟莉】將標記置入能量區！")
            elif sc.id == "GA17/S131-014" and s_i in [3, 4]:
                sc.state = "REST"
                self.trigger_act_used_bonus(self.ai)
                el_t = [c for c in self.ai.deck if c.id in ["GA17/S131-017", "GA17/S131-010"]]
                if el_t:
                    ch_el = el_t[0]
                    self.remove_card_from_deck(self.ai, ch_el)
                    self.ai.waiting_room.append(ch_el)
                random.shuffle(self.ai.deck)
                front_ga = [f_i for f_i in [0, 1, 2] if self.ai.stage[f_i] and "GA文庫" in self.ai.stage[f_i].traits]
                if front_ga:
                    self.ai.stage[front_ga[0]].temp_power += 2000
                    self.log(f"✨ {self.ai.name} 發動【我的旅路 伊蕾娜】強化前排【{self.ai.stage[front_ga[0]].name}】+2000 攻！")
            elif sc.id == "BTR/W107-046" and s_i in [3, 4]:
                front_m = [f_i for f_i in [0, 1, 2] if self.ai.stage[f_i] and "音樂" in self.ai.stage[f_i].traits]
                if front_m:
                    sc.state = "REST"
                    self.trigger_act_used_bonus(self.ai)
                    self.ai.stage[front_m[0]].temp_power += 1000
                    self.log(f"📸 {self.ai.name} 發動【打卡美照 喜多郁代】使【{self.ai.stage[front_m[0]].name}】攻擊力 +1000！")

        self.update_ui()
        self.root.after(800, self.ai_step_climax)

    def ai_step_climax(self):
        if self.game_over:
            return
        self.phase = "CLIMAX"
        self.update_ui()
        cxs = [
            idx
            for idx, c in enumerate(self.ai.hand)
            if c.type == "CX" and self.can_play_card(self.ai, c)
        ]
        if cxs:
            self.play_climax_from_hand(self.ai, cxs[0])
        self.root.after(950, self.ai_step_start_attack)

    def ai_step_start_attack(self):
        if self.game_over:
            return
        self.enter_attack_phase(self.ai)
        self.ai_atk_slots = [0, 1, 2]
        self.root.after(950, self.ai_step_next_attack)

    def ai_step_next_attack(self):
        if self.game_over:
            return
        if self.turn_count == 1 and self.attacks_this_turn >= 1:
            self.root.after(800, self.end_turn)
            return
        while self.ai_atk_slots:
            slot = self.ai_atk_slots.pop(0)
            c = self.ai.stage[slot]
            if c and c.state == "STAND":
                self.initiate_attack(self.ai, slot, on_complete=self.ai_step_next_attack)
                return
        self.root.after(800, self.end_turn)

    # ------------------------------------------
    # UI 官方桌布全區域卡圖化同步更新
    # ------------------------------------------
    def _update_zone_button(
        self, btn, zone_cards, empty_title, bottom_label, bg_color="#1a212d", is_cx_zone=False
    ):
        if is_cx_zone:
            if zone_cards:
                top_c = zone_cards[-1]
                img = self.img_mgr.get_card_visual(getattr(top_c, "skin_id", top_c.id), 108, 76)
            else:
                img = self.img_mgr.get_empty_slot_visual(empty_title, 108, 76, bg_color=bg_color)
            btn.config(image=img, text=bottom_label, width=116, height=102)
            btn.image = img
            return

        if zone_cards:
            top_c = zone_cards[-1]
            img = self.img_mgr.get_card_visual(getattr(top_c, "skin_id", top_c.id), 72, 100)
        else:
            img = self.img_mgr.get_empty_slot_visual(empty_title, 72, 100, bg_color=bg_color)
        btn.config(image=img, text=bottom_label, width=84, height=124)
        btn.image = img

    def update_ui(self):
        if not self.winfo_exists():
            return
        p_colors = ",".join(c.color for c in self.player.level_zone) or "無"
        ai_colors = ",".join(c.color for c in self.ai.level_zone) or "無"

        # 更新放大版《Master Duel》風格雙人頭像與等級/時鐘/能量/牌庫護盾條
        p_is_turn = self.active_player == self.player
        cur_p_av = self.app.settings.get("avatar", "MAPLE")
        p_av_img = self.img_mgr.get_avatar_visual(
            cur_p_av,
            size=68,
            border_color="#06d6a0" if p_is_turn else "#4cc9f0",
            custom_path=self.app.settings.get("custom_avatar_path", ""),
            is_active_turn=p_is_turn,
            crop_cfg=self.app.settings.get("avatar_crop") if cur_p_av == "CARD_CROP" else None,
            preset_crops=self.app.settings.get("preset_avatar_crops"),
        )
        self.lbl_p_avatar.config(image=p_av_img)
        self.lbl_p_avatar.image = p_av_img

        ai_av_key = self.app.get_ai_avatar_id(self.app.ai_series)
        ai_av_img = self.img_mgr.get_avatar_visual(
            ai_av_key,
            size=64,
            border_color="#ff758f",
            is_active_turn=(not p_is_turn),
            preset_crops=self.app.settings.get("preset_avatar_crops"),
        )
        self.lbl_ai_avatar.config(image=ai_av_img)
        self.lbl_ai_avatar.image = ai_av_img

        p_clk_dots = "●" * min(7, len(self.player.clock)) + "○" * max(0, 7 - len(self.player.clock))
        ai_clk_dots = "●" * min(7, len(self.ai.clock)) + "○" * max(0, 7 - len(self.ai.clock))
        self.lbl_p_hud_name.config(
            text=f"{'▶ ' if p_is_turn else ''}{self.player.name}  [Lv.{len(self.player.level_zone)}｜發色:{p_colors}]"
        )
        self.lbl_p_hud_gauge.config(
            text=f"時鐘 {p_clk_dots} ({len(self.player.clock)}/7)\n能量: {len(self.player.stock)} ｜ 手牌: {len(self.player.hand)} ｜ 牌庫: {len(self.player.deck)}"
        )

        self.lbl_ai_hud_name.config(
            text=f"[Lv.{len(self.ai.level_zone)}｜發色:{ai_colors}]  {self.ai.name}{' ◀' if not p_is_turn else ''}"
        )
        self.lbl_ai_hud_gauge.config(
            text=f"({len(self.ai.clock)}/7) {ai_clk_dots} 時鐘\n能量: {len(self.ai.stock)} ｜ 手牌: {len(self.ai.hand)} ｜ 牌庫: {len(self.ai.deck)}"
        )

        self.lbl_phase_info.config(
            text=f"◆ 第 {self.turn_count} 回合 ｜ 行動方：{self.active_player.name} ｜ 階段：{get_phase_zh(self.phase)} ◆"
        )
        self.lbl_ai_hand_info.config(
            text=f"對手手牌：{len(self.ai.hand)} 張  ｜  我方手牌：{len(self.player.hand)} 張  ｜  我方能量：{len(self.player.stock)}"
        )

        # QoL 優化：在對方回合（AI 或雙人連線對手回合）時，「進入下一階段」按鈕顯示為灰色禁用狀態
        if (
            self.active_player == self.player
            and not self.game_over
            and self.phase in ("CLOCK", "MAIN", "CLIMAX", "ATTACK")
        ):
            next_phase_label_map = {
                "CLOCK": "進入主要階段 ➔",
                "MAIN": "進入名場面階段 ➔",
                "CLIMAX": "進入戰鬥階段 ➔",
                "ATTACK": "結束戰階 (進入安可) ➔",
            }
            self.btn_next_phase.config(
                state=tk.NORMAL,
                bg="#118ab2",
                fg="#ffffff",
                text=next_phase_label_map.get(self.phase, "進入下一階段 ➔"),
            )
        else:
            self.btn_next_phase.config(
                state=tk.DISABLED,
                bg="#3a3f58",
                fg="#8890a8",
                disabledforeground="#8890a8",
                text="⏳ 對手回合進行中" if self.active_player != self.player else "進入下一階段 ➔",
            )

        self.render_ai_hand_fan()

        opp_s_style = getattr(self, "opp_sleeve_style", "WS_DEFAULT")
        opp_s_cust = getattr(self, "opp_sleeve_custom", "")
        my_s_style = getattr(self, "player_sleeve_style", "WS_DEFAULT")
        my_s_cust = getattr(self, "player_sleeve_custom", "")

        ai_stock_img = self.img_mgr.get_stock_stack_visual(
            len(self.ai.stock), 78, 104, bg_color="#2b1d28", sleeve_style=opp_s_style, custom_path=opp_s_cust
        )
        self.btn_ai_stock.config(
            image=ai_stock_img, text=f"能量: {len(self.ai.stock)}", width=88, height=126
        )
        self.btn_ai_stock.image = ai_stock_img

        ai_lvl_img = self.img_mgr.get_level_spread_visual(
            self.ai.level_zone, "對手等級區", width=104, height=104, bg_color="#2b1d28"
        )
        self.btn_ai_level.config(
            image=ai_lvl_img, text=f"Lv.{len(self.ai.level_zone)} ({ai_colors})", width=114, height=126
        )
        self.btn_ai_level.image = ai_lvl_img

        ai_clk_img = self.img_mgr.get_clock_spread_visual(
            self.ai.clock, "對手時鐘區", width=216, height=104, bg_color="#2b1d28"
        )
        self.btn_ai_clock.config(
            image=ai_clk_img, text=f"時鐘區一字排開: {len(self.ai.clock)}/7 (點此檢視)", width=226, height=126
        )
        self.btn_ai_clock.image = ai_clk_img
        self._update_zone_button(
            self.btn_ai_memory,
            self.ai.memory,
            "對手\n回憶區",
            f"回憶: {len(self.ai.memory)}",
            "#2b1d28",
        )
        ai_deck_img = self.img_mgr.get_deck_stack_visual(
            len(self.ai.deck), "對手牌庫", 76, 104, bg_color="#2b1d28", sleeve_style=opp_s_style, custom_path=opp_s_cust
        )
        self.btn_ai_deck.config(
            image=ai_deck_img, text=f"牌庫: {len(self.ai.deck)}", width=88, height=126
        )
        self.btn_ai_deck.image = ai_deck_img

        self._update_zone_button(
            self.btn_ai_wr,
            self.ai.waiting_room,
            "對手\n休息室",
            f"休息室: {len(self.ai.waiting_room)}",
            "#2b1d28",
        )
        self._update_zone_button(
            self.btn_ai_cx,
            [self.ai.climax_zone] if self.ai.climax_zone else [],
            "對手名場面\n(橫置區)",
            self.ai.climax_zone.name[:7] if self.ai.climax_zone else "名場面:無",
            "#381f2b",
            is_cx_zone=True,
        )

        p_stock_img = self.img_mgr.get_stock_stack_visual(
            len(self.player.stock), 78, 104, bg_color="#1a2838", sleeve_style=my_s_style, custom_path=my_s_cust
        )
        self.btn_p_stock.config(
            image=p_stock_img, text=f"能量: {len(self.player.stock)}", width=88, height=126
        )
        self.btn_p_stock.image = p_stock_img

        p_lvl_img = self.img_mgr.get_level_spread_visual(
            self.player.level_zone, "我方等級區", width=104, height=104, bg_color="#1a2838"
        )
        self.btn_p_level.config(
            image=p_lvl_img, text=f"Lv.{len(self.player.level_zone)} ({p_colors})", width=114, height=126
        )
        self.btn_p_level.image = p_lvl_img

        p_clk_img = self.img_mgr.get_clock_spread_visual(
            self.player.clock, "我方時鐘區", width=216, height=104, bg_color="#1a2838"
        )
        self.btn_p_clock.config(
            image=p_clk_img, text=f"時鐘區一字排開: {len(self.player.clock)}/7 (點此檢視)", width=226, height=126
        )
        self.btn_p_clock.image = p_clk_img
        self._update_zone_button(
            self.btn_p_memory,
            self.player.memory,
            "我方\n回憶區",
            f"回憶: {len(self.player.memory)}",
            "#1a2838",
        )
        p_deck_img = self.img_mgr.get_deck_stack_visual(
            len(self.player.deck), "我方牌庫", 76, 104, bg_color="#1a2838", sleeve_style=my_s_style, custom_path=my_s_cust
        )
        self.btn_p_deck.config(
            image=p_deck_img, text=f"牌庫: {len(self.player.deck)}", width=88, height=126
        )
        self.btn_p_deck.image = p_deck_img
        self._update_zone_button(
            self.btn_p_wr,
            self.player.waiting_room,
            "我方\n休息室",
            f"休息室: {len(self.player.waiting_room)}",
            "#1a2838",
        )
        self._update_zone_button(
            self.btn_p_cx,
            [self.player.climax_zone] if self.player.climax_zone else [],
            "我方名場面\n(橫置區)",
            self.player.climax_zone.name[:7] if self.player.climax_zone else "名場面:無",
            "#1e3148",
            is_cx_zone=True,
        )

        pos_names = ["前列左", "前列中", "前列右", "後列左", "後列右"]
        sel_st = getattr(self, "_field_slot_select_state", None)
        ai_target_mode = sel_st is not None and sel_st["target_player"] == self.ai
        p_target_mode = sel_st is not None and sel_st["target_player"] == self.player

        for i in range(5):
            ac = self.ai.stage[i]
            ai_valid_target = ai_target_mode and (i in sel_st["valid_set"])
            if ac:
                apwr = self.get_effective_power(self.ai, ac, i)
                asoul = self.get_effective_soul(self.ai, ac, i)
                alvl = self.get_effective_level(self.ai, ac, i)
                a_img = self.img_mgr.get_card_visual(
                    getattr(ac, "skin_id", ac.id), 86, 120, state=ac.state, is_selected=ai_valid_target
                )
                lbl_a = f"🎯點選 L{alvl} 攻:{apwr}" if ai_valid_target else f"L{alvl} 攻:{apwr} 魂:{asoul}"
                self.btn_ai_stage[i].config(
                    image=a_img,
                    text=lbl_a,
                    width=98,
                    height=140,
                    bg="#06d6a0" if ai_valid_target else ("#4a2530" if ac.state == "STAND" else "#281822"),
                    fg="#000000" if ai_valid_target else "#ffffff",
                )
                self.btn_ai_stage[i].image = a_img
            else:
                e_img = self.img_mgr.get_empty_slot_visual(
                    pos_names[i], 86, 120, is_selected=ai_valid_target, bg_color="#261a24"
                )
                self.btn_ai_stage[i].config(
                    image=e_img,
                    text="🎯點選此格" if ai_valid_target else "空位",
                    width=98,
                    height=140,
                    bg="#06d6a0" if ai_valid_target else "#211620",
                    fg="#000000" if ai_valid_target else "#ffccd5",
                )
                self.btn_ai_stage[i].image = e_img

            pc = self.player.stage[i]
            p_valid_target = p_target_mode and (i in sel_st["valid_set"])
            is_sel = (i == self.selected_stage_idx) or p_valid_target
            if pc:
                ppwr = self.get_effective_power(self.player, pc, i)
                psoul = self.get_effective_soul(self.player, pc, i)
                plvl = self.get_effective_level(self.player, pc, i)
                mk_txt = f" 標:{len(pc.markers)}" if pc.markers else ""
                imm_txt = " 🛡️" if pc.cannot_be_reversed else ""
                p_img = self.img_mgr.get_card_visual(
                    getattr(pc, "skin_id", pc.id), 86, 120, state=pc.state, is_selected=is_sel
                )
                lbl_p = f"🎯點選 L{plvl} 攻:{ppwr}" if p_valid_target else f"L{plvl} 攻:{ppwr} 魂:{psoul}{mk_txt}{imm_txt}"
                self.btn_p_stage[i].config(
                    image=p_img,
                    text=lbl_p,
                    width=98,
                    height=140,
                    bg="#06d6a0" if p_valid_target else ("#b56576" if is_sel else ("#1d4e89" if pc.state == "STAND" else "#152638")),
                    fg="#000000" if p_valid_target else "#ffffff",
                )
                self.btn_p_stage[i].image = p_img
            else:
                e_img = self.img_mgr.get_empty_slot_visual(
                    pos_names[i], 86, 120, is_selected=is_sel, bg_color="#182432"
                )
                self.btn_p_stage[i].config(
                    image=e_img,
                    text="🎯點選登場" if p_valid_target else "空位",
                    width=98,
                    height=140,
                    bg="#06d6a0" if p_valid_target else ("#b56576" if is_sel else "#141e2b"),
                    fg="#000000" if p_valid_target else "#a8dadc",
                )
                self.btn_p_stage[i].image = e_img

        sel_stage_c = (
            self.player.stage[self.selected_stage_idx]
            if self.selected_stage_idx is not None
            else None
        )
        can_act_stage = bool(
            self.active_player == self.player
            and self.phase == "MAIN"
            and sel_stage_c
            and (
                (
                    sel_stage_c.state == "STAND"
                    and sel_stage_c.id
                    in [
                        "BFR/S78-031",
                        "BFR/S78-061",
                        "GA10/S131-012",
                        "GA17/S131-014",
                        "BTR/W107-T02",
                        "BTR/W107-046",
                    ]
                )
                or sel_stage_c.id == "BTR/W107-T18"
            )
        )
        if can_act_stage:
            self.btn_act_ability.config(state=tk.NORMAL, bg="#ffd166", fg="#000000")
            if hasattr(self, "btn_float_act"):
                self.btn_float_act.config(state=tk.NORMAL, bg="#ffd166", fg="#000000")
        else:
            self.btn_act_ability.config(state=tk.DISABLED, bg="#3a3f58", fg="#8890a8")
            if hasattr(self, "btn_float_act"):
                self.btn_float_act.config(state=tk.DISABLED, bg="#3a3f58", fg="#8890a8", disabledforeground="#8890a8")

        if (
            self.active_player == self.player
            and self.phase == "MAIN"
            and self.selected_stage_idx is not None
        ):
            self.btn_move_stage.config(state=tk.NORMAL)
        else:
            self.btn_move_stage.config(state=tk.DISABLED)

        # 《Master Duel》風格場上角色頭頂懸浮行動列：僅在無彈窗遮罩且玩家主動點選場上角色時浮現於該卡正上方
        if (
            self.active_player == self.player
            and self.phase == "MAIN"
            and self.selected_stage_idx is not None
            and sel_stage_c is not None
            and not getattr(self, "_overlay_is_waiting", False)
            and not self.center_overlay.winfo_ismapped()
            and getattr(self, "_field_slot_select_state", None) is None
        ):
            def _place_floating_bar(idx=self.selected_stage_idx):
                if (
                    not self.winfo_exists()
                    or self.selected_stage_idx != idx
                    or self.phase != "MAIN"
                    or self.active_player != self.player
                    or getattr(self, "_overlay_is_waiting", False)
                    or self.center_overlay.winfo_ismapped()
                    or getattr(self, "_field_slot_select_state", None) is not None
                ):
                    self.stage_floating_bar.place_forget()
                    return
                t_btn = self.btn_p_stage[idx]
                bx = t_btn.winfo_rootx() - self.right_board.winfo_rootx() + (t_btn.winfo_width() // 2)
                by = t_btn.winfo_rooty() - self.right_board.winfo_rooty() - 6
                if bx > 20 and by > 20:
                    self.stage_floating_bar.place(x=bx, y=by, anchor="s")
                    self.stage_floating_bar.lift()
                    if getattr(self, "_card_drawer_open", False):
                        self.left_card_drawer.lift()
                    if getattr(self, "_log_drawer_open", False):
                        self.right_log_drawer.lift()

            self.after(10, _place_floating_bar)
        else:
            if hasattr(self, "stage_floating_bar"):
                self.stage_floating_bar.place_forget()

        self.render_hand_dock()

        if self.active_player == self.player and self.selected_hand_idx is not None:
            hc = self.player.hand[self.selected_hand_idx]
            if self.phase == "CLOCK":
                self.btn_play_hand.config(
                    text=f"⏰ 將【{hc.name}】置入時鐘並抽 2 張",
                    state=tk.NORMAL,
                    bg="#f4a261",
                    fg="#000000",
                )
            elif self.phase == "MAIN" and hc.type == "EVENT" and is_counter_only_event(hc):
                self.btn_play_hand.config(
                    text=f"🛡️ 【{hc.name}】為反擊卡（被正打時於反擊步驟選發）",
                    state=tk.DISABLED,
                    bg="#2b3144",
                    fg="#ffd166",
                    disabledforeground="#ffd166",
                )
            elif self.phase == "MAIN" and hc.type in ["CHAR", "EVENT"]:
                self.btn_play_hand.config(
                    text=f"✨ 打出 / 使用【{hc.name}】",
                    state=tk.NORMAL,
                    bg="#06d6a0",
                    fg="#000000",
                )
            elif self.phase == "CLIMAX" and hc.type == "CX":
                self.btn_play_hand.config(
                    text=f"🌟 發動名場面【{hc.name}】",
                    state=tk.NORMAL,
                    bg="#e63946",
                    fg="#ffffff",
                )
            else:
                self.btn_play_hand.config(
                    text="當前階段無法使用此卡",
                    state=tk.DISABLED,
                    bg="#2b3144",
                    fg="#98a2b8",
                    disabledforeground="#98a2b8",
                )
        elif self.active_player == self.player and self.phase == "CLOCK":
            self.btn_play_hand.config(
                text="⏰ 開啟【時計階段】痛一抽二選單",
                state=tk.NORMAL,
                bg="#f4a261",
                fg="#000000",
            )
        else:
            self.btn_play_hand.config(
                text="請先點選手牌（或按住左鍵拖移上場）",
                state=tk.DISABLED,
                bg="#2b3144",
                fg="#98a2b8",
                disabledforeground="#98a2b8",
            )

    def _is_hand_card_playable_now(self, hc: CardInstance) -> bool:
        if self.active_player != self.player:
            return False
        if self.phase == "CLOCK":
            return True
        if self.phase == "MAIN":
            if hc.type == "CHAR":
                return self.can_play_card(self.player, hc)
            if hc.type == "EVENT" and not is_counter_only_event(hc):
                return self.can_play_card(self.player, hc)
            return False
        if self.phase == "CLIMAX":
            return hc.type == "CX" and self.can_play_card(self.player, hc)
        return False

    def render_hand_dock(self):
        """繪製《Master Duel》風格放大版扇形微弧交疊握持手牌塢：移除上方黑框與浮動黑底標籤，完整呈現高畫質卡圖"""
        if not hasattr(self, "hand_canvas") or not self.hand_canvas.winfo_exists():
            return
        self.hand_canvas.delete("all")
        self.hand_card_hitboxes = []
        self._hand_photo_refs = []

        cw = max(self.hand_canvas.winfo_width(), 920)
        ch = max(self.hand_canvas.winfo_height(), 214)

        self.hand_canvas.create_oval(
            cw // 2 - 480,
            ch - 56,
            cw // 2 + 480,
            ch + 96,
            fill="#141b2d",
            outline="#293859",
            width=2,
        )
        self.hand_canvas.create_line(
            cw // 2 - 420, ch - 3, cw // 2 + 420, ch - 3, fill="#4cc9f0", width=2
        )

        n = len(self.player.hand)
        if n == 0:
            self.hand_canvas.create_text(
                cw // 2,
                ch // 2,
                text="目前我方手牌為 0 張",
                fill="#6c757d",
                font=("Microsoft JhengHei", 12, "bold"),
            )
            return

        if self.hovered_hand_idx is not None and self.hovered_hand_idx >= n:
            self.hovered_hand_idx = None
        if self.selected_hand_idx is not None and self.selected_hand_idx >= n:
            self.selected_hand_idx = None

        modal_open = bool(getattr(self, "_overlay_is_waiting", False) or self.center_overlay.winfo_ismapped())
        pop_idx = self.hovered_hand_idx if not modal_open else None
        step_x = 98 if n <= 6 else max(56, min(94, int((cw - 240) / max(1, n - 1))))

        draw_order = [i for i in range(n) if i != pop_idx]
        if pop_idx is not None and 0 <= pop_idx < n:
            draw_order.append(pop_idx)

        for idx in draw_order:
            hc = self.player.hand[idx]
            rel = idx - (n - 1) / 2.0
            cx_i = int(cw // 2 + rel * step_x)
            if pop_idx is not None and idx != pop_idx:
                cx_i += -22 if idx < pop_idx else 22

            is_hov = (idx == pop_idx)
            is_sel = (idx == self.selected_hand_idx)
            is_pop = is_hov
            is_play = self._is_hand_card_playable_now(hc)
            hlvl = self.get_effective_level(self.player, hc, None)

            if is_pop:
                cy_i = ch - 104
                ang = 0
                w_box, h_box = 148, 206
            else:
                arc_drop = int(min(18, (rel ** 2) * 1.4))
                sel_lift = -10 if is_sel else 0
                cy_i = ch - 72 + arc_drop + sel_lift
                ang = 0 if is_sel else int(max(-6, min(6, round((-rel * 1.8) / 2.0) * 2)))
                w_box, h_box = 122, 170

            tk_img = self.img_mgr.get_hand_dock_card_visual(
                getattr(hc, "skin_id", hc.id),
                angle_deg=ang,
                is_hovered=is_hov,
                is_selected=is_sel,
                is_playable=is_play,
                eff_level=hlvl,
                cost=hc.cost,
            )
            self._hand_photo_refs.append(tk_img)
            self.hand_canvas.create_image(cx_i, cy_i, image=tk_img, anchor="center")

            x1 = cx_i - w_box // 2
            y1 = cy_i - h_box // 2
            x2 = cx_i + w_box // 2
            y2 = cy_i + h_box // 2
            self.hand_card_hitboxes.append((idx, x1, y1, x2, y2))

    def _hit_test_hand_dock(self, x: int, y: int):
        for idx, x1, y1, x2, y2 in reversed(self.hand_card_hitboxes):
            if x1 <= x <= x2 and y1 <= y <= y2:
                return idx
        return None

    def _on_hand_canvas_motion(self, event):
        if self._drag_state.get("dragging"):
            return
        hit = self._hit_test_hand_dock(event.x, event.y)
        if hit != self.hovered_hand_idx:
            self.hovered_hand_idx = hit
            self.render_hand_dock()
            if hit is not None and hit < len(self.player.hand):
                self.inspect_card(self.player.hand[hit], self.player, None, open_drawer=False)

    def _on_hand_canvas_leave(self, event):
        if self.hovered_hand_idx is not None and not self._drag_state.get("dragging"):
            self.hovered_hand_idx = None
            self.render_hand_dock()

    def _on_hand_canvas_press(self, event):
        hit = self._hit_test_hand_dock(event.x, event.y)
        self._hand_press_idx = hit
        if hit is not None:
            self._on_hand_press(event, hit)
        else:
            self.hide_card_drawer()

    def _on_hand_canvas_release(self, event):
        if self._drag_state.get("dragging"):
            self._on_drag_release(event)
            self._hand_press_idx = None
            return
        self._drag_state["source"] = None
        if self._hand_press_idx is not None:
            idx = self._hand_press_idx
            self._hand_press_idx = None
            self.on_click_hand(idx)

    def _on_hand_canvas_double_click(self, event):
        if getattr(self, "_overlay_is_waiting", False):
            return
        hit = self._hit_test_hand_dock(event.x, event.y)
        if hit is not None and hit < len(self.player.hand):
            self.selected_hand_idx = hit
            self.update_ui()
            if self._is_hand_card_playable_now(self.player.hand[hit]):
                self.on_use_selected_hand()


# ==========================================
# 遊戲設定常數與設定面板 (SettingsFrame：《大師決鬥》風格客製化中心)
# ==========================================
AVATAR_OPTIONS = [
    ("MAPLE", "【防盾】梅普露"),
    ("SALLY", "【防盾】莎莉"),
    ("MII", "【防盾】蜜伊"),
    ("MAHIRU", "【GA文庫】小真晝"),
    ("ELAINA", "【GA文庫】伊蕾娜"),
    ("RYU", "【GA文庫】琉"),
    ("KITA", "【孤獨搖滾】喜多郁代"),
    ("BOCCHI", "【孤獨搖滾】後藤一里"),
    ("NIJIKA", "【孤獨搖滾】伊地知虹夏"),
    ("CARD_CROP", "【卡圖裁切】自選卡片圓框"),
]

THEME_OPTIONS = [
    ("OCEAN", "經典深海藍 (Master Duel 皇家藍)"),
    ("MAPLE_CRIMSON", "大楓樹黑紅盾紋 (梅普露主題)"),
    ("STARLIGHT_GOLD", "星夜金羽暖色調 (小真晝＆伊蕾娜)"),
    ("BOCCHI_NEON", "下北澤霓虹搖滾 (喜多＆團結Band)"),
]

FONT_FAMILY_OPTIONS = [
    "Microsoft JhengHei",
    "PMingLiU",
    "DFKai-SB",
    "SimHei",
    "Arial",
]


class SettingsFrame(tk.Frame):
    """《大師決鬥》風格設定中心：支援 AI 翻牌/停留秒數滑桿 (1~10秒)、角色頭像選擇與上傳、背景主題與自訂桌布、字體與文字大小設定"""

    def __init__(self, parent, app):
        super().__init__(parent, bg="#0d111a")
        self.app = app
        self.img_mgr = app.img_mgr
        self.working = dict(app.settings)
        self.avatar_btns = {}
        self.theme_btns = {}
        self.setup_ui()

    def setup_ui(self):
        ff = self.app.get_font_family()
        # 背景畫布（即時反映主題與自訂背景）
        self.bg_label = tk.Label(self, bg="#0d111a")
        self.bg_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self._refresh_bg_preview()

        # 頂部《Master Duel》風格導覽列
        top_bar = tk.Frame(
            self, bg="#141926", bd=2, relief=tk.RIDGE, padx=18, pady=10
        )
        top_bar.pack(fill=tk.X, padx=18, pady=(12, 6))

        tk.Button(
            top_bar,
            text="◀ 返回主選單",
            bg="#2b3348",
            fg="#ffffff",
            activebackground="#3d4766",
            activeforeground="#ffd166",
            font=(ff, 11, "bold"),
            padx=16,
            pady=5,
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.app.show_main_menu,
        ).pack(side=tk.LEFT)

        tk.Label(
            top_bar,
            text="◆ 遊 戲 設 定 中 心 (GAME SETTINGS) ◆",
            bg="#141926",
            fg="#ffd166",
            font=(ff, 17, "bold"),
        ).pack(side=tk.LEFT, padx=22)

        self.lbl_save_status = tk.Label(
            top_bar,
            text="調整完畢後點擊右側按鈕即可儲存並立即套用",
            bg="#141926",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        )
        self.lbl_save_status.pack(side=tk.LEFT, padx=10)

        tk.Button(
            top_bar,
            text="✔ 儲存並套用設定",
            bg="#06d6a0",
            fg="#000000",
            activebackground="#ffd166",
            font=(ff, 12, "bold"),
            padx=20,
            pady=5,
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.on_save_settings,
        ).pack(side=tk.RIGHT, padx=6)

        tk.Button(
            top_bar,
            text="↺ 恢復預設值",
            bg="#4a4e69",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.on_reset_defaults,
        ).pack(side=tk.RIGHT, padx=6)

        # 主體雙欄容器
        body = tk.Frame(self, bg="#0d111a")
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=6)

        left_col = tk.Frame(body, bg="#151b29", bd=2, relief=tk.RIDGE, padx=18, pady=14)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        right_col = tk.Frame(body, bg="#151b29", bd=2, relief=tk.RIDGE, padx=18, pady=14)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        # ==========================================
        # 左欄區塊 1：AI 翻牌與判定停留時間設定（預設翻牌 2.0 秒、停留 3.5 秒，可調 1.0 ~ 10.0 秒）
        # ==========================================
        sec1 = tk.LabelFrame(
            left_col,
            text=" ◆ 1. AI 翻牌速度與判定停留時間（1.0 秒 ～ 10.0 秒） ",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
            padx=14,
            pady=10,
        )
        sec1.pack(fill=tk.X, pady=(0, 12))

        row_flip = tk.Frame(sec1, bg="#1b2234")
        row_flip.pack(fill=tk.X, pady=4)
        self.lbl_flip_val = tk.Label(
            row_flip,
            text=f"AI 每張牌翻開間隔時間：{self.working['ai_flip_interval_sec']:.1f} 秒（預設 2.0 秒）",
            bg="#1b2234",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            anchor="w",
        )
        self.lbl_flip_val.pack(fill=tk.X)

        self.scale_flip = tk.Scale(
            sec1,
            from_=1.0,
            to=10.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#ffd166",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 10, "bold"),
            command=self._on_flip_scale_change,
        )
        self.scale_flip.set(float(self.working.get("ai_flip_interval_sec", 2.0)))
        self.scale_flip.pack(fill=tk.X, pady=(2, 8))

        row_pause = tk.Frame(sec1, bg="#1b2234")
        row_pause.pack(fill=tk.X, pady=4)
        self.lbl_pause_val = tk.Label(
            row_pause,
            text=f"AI 翻牌判定結束停留時間：{self.working['ai_flip_end_pause_sec']:.1f} 秒（預設 3.5 秒）",
            bg="#1b2234",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            anchor="w",
        )
        self.lbl_pause_val.pack(fill=tk.X)

        self.scale_pause = tk.Scale(
            sec1,
            from_=1.0,
            to=10.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#06d6a0",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 10, "bold"),
            command=self._on_pause_scale_change,
        )
        self.scale_pause.set(float(self.working.get("ai_flip_end_pause_sec", 3.5)))
        self.scale_pause.pack(fill=tk.X, pady=(2, 4))

        # ==========================================
        # 左欄區塊 2：玩家名稱與專屬角色頭像（梅普露 / 小真晝 / 喜多 等 + 自訂頭像上傳）
        # ==========================================
        sec2 = tk.LabelFrame(
            left_col,
            text=" ◆ 2. 玩家名稱與專屬頭像設定（含梅普露・小真晝・喜多與自訂上傳） ",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
            padx=14,
            pady=10,
        )
        sec2.pack(fill=tk.BOTH, expand=True)

        top_av_row = tk.Frame(sec2, bg="#1b2234")
        top_av_row.pack(fill=tk.X, pady=(0, 8))

        self.lbl_cur_avatar_preview = tk.Label(
            top_av_row, bg="#141824", bd=2, relief=tk.SOLID
        )
        self.lbl_cur_avatar_preview.pack(side=tk.LEFT, padx=(4, 14))

        name_and_upload = tk.Frame(top_av_row, bg="#1b2234")
        name_and_upload.pack(side=tk.LEFT, fill=tk.X, expand=True)

        n_row = tk.Frame(name_and_upload, bg="#1b2234")
        n_row.pack(fill=tk.X, pady=3)
        tk.Label(
            n_row,
            text="玩家對戰暱稱：",
            bg="#1b2234",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT)
        self.ent_name = tk.Entry(
            n_row,
            bg="#10141f",
            fg="#ffffff",
            insertbackground="#ffd166",
            font=(ff, 12, "bold"),
            width=18,
        )
        self.ent_name.insert(0, self.working.get("player_name", "玩家1"))
        self.ent_name.pack(side=tk.LEFT, padx=8)

        u_row = tk.Frame(name_and_upload, bg="#1b2234")
        u_row.pack(fill=tk.X, pady=3)
        tk.Button(
            u_row,
            text="✂️ 裁切/縮放目前預設頭像",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.open_card_avatar_cropper_dialog(target_preset_key=self.working.get("avatar", "MAPLE")),
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            u_row,
            text="🎴 按系列選任意卡圖裁切",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.open_card_avatar_cropper_dialog(target_preset_key=None),
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            u_row,
            text="📂 上傳圖片",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.on_upload_custom_avatar,
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.lbl_avatar_name = tk.Label(
            name_and_upload,
            text="",
            bg="#1b2234",
            fg="#06d6a0",
            font=(ff, 10, "bold"),
            anchor="w",
        )
        self.lbl_avatar_name.pack(fill=tk.X, pady=(2, 0))

        # 角色頭像快速選擇網格 (5 列 x 2 行)
        av_grid = tk.Frame(sec2, bg="#141824", bd=1, relief=tk.SOLID, padx=8, pady=8)
        av_grid.pack(fill=tk.BOTH, expand=True)

        for idx_a, (av_key, av_label) in enumerate(AVATAR_OPTIONS):
            r, c = divmod(idx_a, 5)
            av_img = self.img_mgr.get_avatar_visual(
                av_key,
                size=56,
                border_color="#ffd166",
                custom_path=self.working.get("custom_avatar_path", ""),
                crop_cfg=self.working.get("avatar_crop") if av_key == "CARD_CROP" else None,
                preset_crops=self.working.get("preset_avatar_crops"),
            )
            btn = tk.Button(
                av_grid,
                image=av_img,
                text=av_label.replace("【", "").replace("】", "\n"),
                compound=tk.TOP,
                width=92,
                height=88,
                bg="#252c42",
                fg="#ffffff",
                font=(ff, 9, "bold"),
                bd=2,
                cursor="hand2",
                command=lambda k=av_key: self.select_avatar(k),
            )
            btn.image = av_img
            btn.grid(row=r, column=c, padx=5, pady=5)
            self.avatar_btns[av_key] = btn

        self._refresh_avatar_selection_ui()

        # ==========================================
        # 右欄區塊 3：桌布背景主題與用戶自訂背景圖上傳
        # ==========================================
        sec3 = tk.LabelFrame(
            right_col,
            text=" ◆ 3. 桌布主題風格與自訂背景圖片上傳 ",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
            padx=14,
            pady=10,
        )
        sec3.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            sec3,
            text="選擇預設主題色調：",
            bg="#1b2234",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(anchor="w", pady=(0, 4))

        theme_grid = tk.Frame(sec3, bg="#1b2234")
        theme_grid.pack(fill=tk.X, pady=2)
        for idx_t, (t_key, t_name) in enumerate(THEME_OPTIONS):
            r, c = divmod(idx_t, 2)
            b = tk.Button(
                theme_grid,
                text=t_name,
                width=28,
                pady=6,
                bg="#252c42",
                fg="#ffffff",
                font=(ff, 10, "bold"),
                bd=2,
                cursor="hand2",
                command=lambda k=t_key: self.select_theme(k),
            )
            b.grid(row=r, column=c, padx=6, pady=4, sticky="ew")
            self.theme_btns[t_key] = b

        bg_upload_row = tk.Frame(sec3, bg="#1b2234")
        bg_upload_row.pack(fill=tk.X, pady=(10, 4))

        tk.Button(
            bg_upload_row,
            text="🖼️ 上傳自訂桌布背景圖 (.png/.jpg/.webp)",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.on_upload_custom_bg,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            bg_upload_row,
            text="✖ 清除自訂背景 (使用主題動態卡牆)",
            bg="#4a4e69",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.on_clear_custom_bg,
        ).pack(side=tk.LEFT)

        self.lbl_bg_path = tk.Label(
            sec3,
            text="",
            bg="#1b2234",
            fg="#06d6a0",
            font=(ff, 9, "bold"),
            anchor="w",
        )
        self.lbl_bg_path.pack(fill=tk.X, pady=2)

        self.lbl_dim_val = tk.Label(
            sec3,
            text=f"背景暗化遮罩濃度：{self.working.get('bg_dim_percent', 65)}%（數值越高文字越清晰）",
            bg="#1b2234",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            anchor="w",
        )
        self.lbl_dim_val.pack(fill=tk.X, pady=(6, 0))

        self.scale_dim = tk.Scale(
            sec3,
            from_=20,
            to=90,
            resolution=5,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#ffd166",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 9, "bold"),
            command=self._on_dim_scale_change,
        )
        self.scale_dim.set(int(self.working.get("bg_dim_percent", 65)))
        self.scale_dim.pack(fill=tk.X, pady=2)

        # 卡套 / 卡背樣式選擇列（官方 WS 預設卡背 / AmiAmi 特典角色卡套 / 自訂上傳）
        sleeve_row = tk.Frame(sec3, bg="#141824", padx=8, pady=6, relief=tk.SOLID, bd=1)
        sleeve_row.pack(fill=tk.X, pady=(6, 2))

        self.lbl_sleeve_preview = tk.Label(sleeve_row, bg="#141824")
        self.lbl_sleeve_preview.pack(side=tk.LEFT, padx=(2, 10))

        sleeve_right = tk.Frame(sleeve_row, bg="#141824")
        sleeve_right.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            sleeve_right,
            text="🎴 牌庫、對手手牌與能量區蓋牌卡套樣式：",
            bg="#141824",
            fg="#ffd166",
            font=(ff, 10, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 4))

        sleeve_btn_bar = tk.Frame(sleeve_right, bg="#141824")
        sleeve_btn_bar.pack(fill=tk.X)

        self.sleeve_btns = {}
        for s_key, s_label in [
            ("WS_DEFAULT", "🎴 官方 WS 卡背 (預設)"),
            ("AMIAMI_21593", "✨ 特典角色卡套 (AmiAmi)"),
        ]:
            b = tk.Button(
                sleeve_btn_bar,
                text=s_label,
                bg="#252c42",
                fg="#ffffff",
                font=(ff, 9, "bold"),
                padx=10,
                pady=4,
                cursor="hand2",
                command=lambda k=s_key: self.select_sleeve_style(k),
            )
            b.pack(side=tk.LEFT, padx=(0, 6))
            self.sleeve_btns[s_key] = b

        b_cust_sleeve = tk.Button(
            sleeve_btn_bar,
            text="📂 上傳自訂卡套",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 9, "bold"),
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.on_upload_custom_sleeve,
        )
        b_cust_sleeve.pack(side=tk.LEFT, padx=(0, 6))
        self.sleeve_btns["CUSTOM"] = b_cust_sleeve

        self._refresh_theme_selection_ui()
        self._refresh_sleeve_selection_ui()

        # ==========================================
        # 右欄區塊 4：字體樣式與效果文字大小設定
        # ==========================================
        sec4 = tk.LabelFrame(
            right_col,
            text=" ◆ 4. 介面字體與卡片效果文字大小設定 ",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
            padx=14,
            pady=10,
        )
        sec4.pack(fill=tk.X, pady=(0, 4))

        f_row1 = tk.Frame(sec4, bg="#1b2234")
        f_row1.pack(fill=tk.X, pady=6)
        tk.Label(
            f_row1,
            text="介面與卡表字體：",
            bg="#1b2234",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT)

        self.font_var = tk.StringVar(value=self.working.get("font_family", "Microsoft JhengHei"))
        self.cmb_font = ttk.Combobox(
            f_row1,
            textvariable=self.font_var,
            values=FONT_FAMILY_OPTIONS,
            state="readonly",
            width=22,
            font=(ff, 11, "bold"),
        )
        self.cmb_font.pack(side=tk.LEFT, padx=10)
        self.cmb_font.bind("<<ComboboxSelected>>", self._on_font_change)

        f_row2 = tk.Frame(sec4, bg="#1b2234")
        f_row2.pack(fill=tk.X, pady=6)
        tk.Label(
            f_row2,
            text="效果文與戰報字級：",
            bg="#1b2234",
            fg="#8ecae6",
            font=(ff, 11, "bold"),
        ).pack(side=tk.LEFT)

        self.font_size_btns = {}
        for sz_val, sz_label in [(11, "標準 (11pt)"), (13, "放大 (13pt)"), (15, "特大 (15pt)")]:
            b = tk.Button(
                f_row2,
                text=sz_label,
                bg="#252c42",
                fg="#ffffff",
                font=(ff, 10, "bold"),
                padx=12,
                pady=4,
                cursor="hand2",
                command=lambda s=sz_val: self.select_font_size(s),
            )
            b.pack(side=tk.LEFT, padx=6)
            self.font_size_btns[sz_val] = b

        self.lbl_font_preview = tk.Label(
            sec4,
            text="【字體預覽】【自】此卡從手牌放置到舞台時，你看自己牌組上方最多 4 張，選擇等級 1 以上卡片最多 1 張加入手牌。",
            bg="#10141f",
            fg="#f1faee",
            font=(
                self.working.get("font_family", "Microsoft JhengHei"),
                int(self.working.get("effect_font_size", 12)),
            ),
            justify=tk.LEFT,
            wraplength=540,
            padx=12,
            pady=6,
            relief=tk.SOLID,
            bd=1,
        )
        self.lbl_font_preview.pack(fill=tk.X, pady=(4, 2))
        self._refresh_font_selection_ui()

        # ==========================================
        # 右欄區塊 5：背景音樂 (BGM) 與音效 (SFX) 設定
        # ==========================================
        sec5 = tk.LabelFrame(
            right_col,
            text=" ◆ 5. 音樂與音效設定（主選單 / 主階 / 戰階音樂 ＆ 抽卡 / 扣血 / 名場面 / 點擊音效） ",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 12, "bold"),
            padx=14,
            pady=8,
        )
        sec5.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        toggle_row = tk.Frame(sec5, bg="#1b2234")
        toggle_row.pack(fill=tk.X, pady=2)

        self.btn_toggle_bgm = tk.Button(
            toggle_row,
            text="",
            font=(ff, 10, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._on_toggle_bgm,
        )
        self.btn_toggle_bgm.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_toggle_sfx = tk.Button(
            toggle_row,
            text="",
            font=(ff, 10, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=self._on_toggle_sfx,
        )
        self.btn_toggle_sfx.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            toggle_row,
            text="🎚️ 個別音樂/音效音量 ＆ 換檔設定",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 9, "bold"),
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.open_custom_audio_modal,
        ).pack(side=tk.RIGHT)

        vol_row = tk.Frame(sec5, bg="#1b2234")
        vol_row.pack(fill=tk.X, pady=2)

        bgm_v_col = tk.Frame(vol_row, bg="#1b2234")
        bgm_v_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.lbl_bgm_vol = tk.Label(
            bgm_v_col,
            text=f"音樂 (BGM) 總音量：{int(self.working.get('bgm_volume', 50))}% (上限已降為原1/10)",
            bg="#1b2234",
            fg="#06d6a0",
            font=(ff, 9, "bold"),
            anchor="w",
        )
        self.lbl_bgm_vol.pack(fill=tk.X)
        self.scale_bgm_vol = tk.Scale(
            bgm_v_col,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#06d6a0",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 8, "bold"),
            command=self._on_bgm_vol_change,
        )
        self.scale_bgm_vol.set(int(self.working.get("bgm_volume", 50)))
        self.scale_bgm_vol.pack(fill=tk.X)

        sfx_v_col = tk.Frame(vol_row, bg="#1b2234")
        sfx_v_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        self.lbl_sfx_vol = tk.Label(
            sfx_v_col,
            text=f"音效 (SFX) 總音量：{int(self.working.get('sfx_volume', 80))}% (可點右上個別調整)",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 9, "bold"),
            anchor="w",
        )
        self.lbl_sfx_vol.pack(fill=tk.X)
        self.scale_sfx_vol = tk.Scale(
            sfx_v_col,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#ffd166",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 8, "bold"),
            command=self._on_sfx_vol_change,
        )
        self.scale_sfx_vol.set(int(self.working.get("sfx_volume", 80)))
        self.scale_sfx_vol.pack(fill=tk.X)

        # 四大音效與三大音樂快速個別音量微調列
        indiv_box = tk.Frame(sec5, bg="#141824", padx=6, pady=4, relief=tk.SOLID, bd=1)
        indiv_box.pack(fill=tk.X, pady=(2, 2))
        self.indiv_vol_scales = {}
        self.indiv_vol_labels = {}
        t_vols = dict(self.working.get("track_volumes") or {})
        short_names = [
            ("bgm_menu", "主選單樂"),
            ("bgm_main", "主階音樂"),
            ("bgm_battle", "戰階音樂"),
            ("sfx_click", "點擊音效"),
            ("sfx_draw", "抽卡音效"),
            ("sfx_damage", "扣血音效"),
            ("sfx_climax", "名場面音"),
        ]
        for idx_s, (tk_k, tk_short) in enumerate(short_names):
            r_idx = idx_s // 4
            c_idx = idx_s % 4
            cell = tk.Frame(indiv_box, bg="#141824")
            cell.grid(row=r_idx, column=c_idx, sticky="ew", padx=4, pady=1)
            indiv_box.grid_columnconfigure(c_idx, weight=1)
            init_tv = int(t_vols.get(tk_k, 100))
            is_b = tk_k.startswith("bgm_")
            lbl_iv = tk.Label(
                cell,
                text=f"{tk_short}:{init_tv}%",
                bg="#141824",
                fg="#06d6a0" if is_b else "#ffd166",
                font=(ff, 8, "bold"),
                anchor="w",
            )
            lbl_iv.pack(fill=tk.X)
            self.indiv_vol_labels[tk_k] = lbl_iv
            sc_iv = tk.Scale(
                cell,
                from_=0,
                to=100,
                resolution=1,
                orient=tk.HORIZONTAL,
                showvalue=False,
                bg="#1b2234",
                fg="#06d6a0" if is_b else "#ffd166",
                troughcolor="#2b3348",
                highlightthickness=0,
                bd=0,
                sliderlength=14,
                width=8,
                command=lambda val, key=tk_k, name=tk_short: self._on_indiv_track_vol_change(key, name, val),
            )
            sc_iv.set(init_tv)
            sc_iv.pack(fill=tk.X)
            self.indiv_vol_scales[tk_k] = sc_iv

        test_bar = tk.Frame(sec5, bg="#141824", padx=8, pady=6, relief=tk.SOLID, bd=1)
        test_bar.pack(fill=tk.X, pady=(4, 0))
        tk.Label(
            test_bar,
            text="🔊 試聽：",
            bg="#141824",
            fg="#8ecae6",
            font=(ff, 9, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 4))

        for t_key, t_lbl in [
            ("bgm_menu", "主選單BGM"),
            ("bgm_main", "主階BGM"),
            ("bgm_battle", "戰階BGM"),
            ("sfx_click", "點擊音"),
            ("sfx_draw", "抽卡音"),
            ("sfx_damage", "扣血音"),
            ("sfx_climax", "名場面音"),
        ]:
            tk.Button(
                test_bar,
                text=t_lbl,
                bg="#252c42",
                fg="#ffd166" if t_key.startswith("bgm_") else "#ffffff",
                font=(ff, 9, "bold"),
                padx=6,
                pady=2,
                cursor="hand2",
                command=lambda k=t_key: self._test_play_audio(k),
            ).pack(side=tk.LEFT, padx=3)

        self._refresh_audio_selection_ui()

    def _refresh_bg_preview(self):
        bg_img = self.img_mgr.get_wallpaper_visual(
            self.working.get("theme", "OCEAN"),
            self.working.get("custom_bg_path", ""),
            int(self.working.get("bg_dim_percent", 65)),
            1600,
            950,
            floating_cids=self.app.get_menu_floating_deck_cids(),
        )
        self.bg_label.config(image=bg_img)
        self.bg_label.image = bg_img

    def _on_flip_scale_change(self, val):
        v = float(val)
        self.working["ai_flip_interval_sec"] = v
        self.lbl_flip_val.config(text=f"AI 每張牌翻開間隔時間：{v:.1f} 秒（預設 2.0 秒）")

    def _on_pause_scale_change(self, val):
        v = float(val)
        self.working["ai_flip_end_pause_sec"] = v
        self.lbl_pause_val.config(text=f"AI 翻牌判定結束停留時間：{v:.1f} 秒（預設 3.5 秒）")

    def _on_dim_scale_change(self, val):
        v = int(float(val))
        self.working["bg_dim_percent"] = v
        self.lbl_dim_val.config(text=f"背景暗化遮罩濃度：{v}%（數值越高文字越清晰）")
        self._refresh_bg_preview()

    def select_avatar(self, av_key: str):
        self.app.sound_mgr.play_sfx("sfx_click")
        if av_key == "CARD_CROP":
            self.open_card_avatar_cropper_dialog(target_preset_key=None)
            return
        if av_key == "CUSTOM" and not self.working.get("custom_avatar_path"):
            self.on_upload_custom_avatar()
            return
        # 若再次點擊目前已選中的預設角色頭像，直接開啟該預設頭像的圓框裁切器讓玩家微調位置與縮放！
        if self.working.get("avatar") == av_key and av_key in self.img_mgr.AVATAR_PRESET_DEFAULTS:
            self.open_card_avatar_cropper_dialog(target_preset_key=av_key)
            return
        self.working["avatar"] = av_key
        self._refresh_avatar_selection_ui()

    def _refresh_avatar_selection_ui(self):
        cur_av = self.working.get("avatar", "MAPLE")
        custom_p = self.working.get("custom_avatar_path", "")
        crop_cfg = self.working.get("avatar_crop") if cur_av == "CARD_CROP" else None
        preset_crops = self.working.get("preset_avatar_crops") or {}
        big_img = self.img_mgr.get_avatar_visual(
            cur_av,
            size=76,
            border_color="#06d6a0",
            custom_path=custom_p,
            is_active_turn=True,
            crop_cfg=crop_cfg,
            preset_crops=preset_crops,
        )
        self.lbl_cur_avatar_preview.config(image=big_img)
        self.lbl_cur_avatar_preview.image = big_img

        for k, b in self.avatar_btns.items():
            k_crop = self.working.get("avatar_crop") if k == "CARD_CROP" else None
            k_img = self.img_mgr.get_avatar_visual(
                k,
                size=56,
                border_color="#ffd166",
                custom_path=custom_p,
                crop_cfg=k_crop,
                preset_crops=preset_crops,
            )
            b.config(image=k_img)
            b.image = k_img

        av_dict = dict(AVATAR_OPTIONS)
        av_dict["CUSTOM"] = "【自訂】上傳電腦圖片"
        if cur_av == "CARD_CROP" and isinstance(self.working.get("avatar_crop"), dict) and self.working["avatar_crop"].get("cid") in CARD_DB:
            c_title = CARD_DB[self.working["avatar_crop"]["cid"]]["name"]
            self.lbl_avatar_name.config(text=f"目前選用：【自選卡圖】{c_title}（點擊頭像可重新裁切）")
        else:
            self.lbl_avatar_name.config(
                text=f"目前選用：{av_dict.get(cur_av, cur_av)}（再點一次該頭像或按上方按鈕可裁切縮放）"
            )
        for k, b in self.avatar_btns.items():
            is_sel = k == cur_av
            b.config(
                bg="#f4a261" if is_sel else "#252c42",
                fg="#000000" if is_sel else "#ffffff",
                relief=tk.SUNKEN if is_sel else tk.RAISED,
            )

    def open_card_avatar_cropper_dialog(self, target_preset_key: str = None):
        """
        互動式卡圖圓框頭像裁切器：
        - 支援直接裁切 9 款預設代表角色頭像（梅普露 / 小真晝 / 喜多 等）
        - 支援先選擇「系列分類」（預設代表角色 / 防盾 / GA文庫 / 孤獨搖滾）再挑卡，不需從全部卡池盲找
        - 支援滑鼠左鍵拖動圓框、滑鼠滾輪放大縮小
        """
        self.app.sound_mgr.play_sfx("sfx_click")
        if hasattr(self, "_crop_overlay") and self._crop_overlay and self._crop_overlay.winfo_exists():
            self._crop_overlay.destroy()

        crop_overlay = tk.Frame(self, bg="#151b29", bd=3, relief=tk.RIDGE, padx=22, pady=16)
        crop_overlay.place(relx=0.5, rely=0.5, anchor="center", width=1040, height=660)
        crop_overlay.lift()
        self._crop_overlay = crop_overlay

        ff = self.app.get_font_family()
        preset_crops = dict(self.working.get("preset_avatar_crops") or {})

        if target_preset_key and target_preset_key in self.img_mgr.AVATAR_PRESET_DEFAULTS:
            def_cid, def_name, _, def_cx, def_cy, def_zm = self.img_mgr.AVATAR_PRESET_DEFAULTS[target_preset_key]
            saved_p = preset_crops.get(target_preset_key, {})
            init_cid = saved_p.get("cid", def_cid)
            init_cx = float(saved_p.get("cx", def_cx))
            init_cy = float(saved_p.get("cy", def_cy))
            init_zm = float(saved_p.get("zoom", def_zm))
            init_series_tab = "PRESETS"
        else:
            existing_crop = self.working.get("avatar_crop") or {}
            init_cid = existing_crop.get("cid", "BFR/S78-073")
            if init_cid not in CARD_DB:
                init_cid = next(iter(CARD_DB.keys()))
            init_cx = float(existing_crop.get("cx", 0.50))
            init_cy = float(existing_crop.get("cy", 0.24))
            init_zm = float(existing_crop.get("zoom", 1.85))
            init_series_tab = CARD_DB.get(init_cid, {}).get("series", "BFR/S78")

        state = {
            "preset_key": target_preset_key if (target_preset_key in self.img_mgr.AVATAR_PRESET_DEFAULTS) else None,
            "series_tab": init_series_tab,
            "cid": init_cid,
            "cx": init_cx,
            "cy": init_cy,
            "zoom": init_zm,
        }

        top_row = tk.Frame(crop_overlay, bg="#151b29")
        top_row.pack(fill=tk.X, pady=(0, 6))
        tk.Label(
            top_row,
            text="✂️ 卡圖圓框頭像裁切器（可調預設角色或分系列選卡・左鍵拖曳圓框・滑鼠滾輪放大縮小）",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 14, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            top_row,
            text="✖ 關閉",
            bg="#e63946",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            command=crop_overlay.destroy,
        ).pack(side=tk.RIGHT)

        # 底部確認列優先固定
        bot_row = tk.Frame(crop_overlay, bg="#151b29")
        bot_row.pack(side=tk.BOTTOM, fill=tk.X, pady=(8, 2))

        def apply_cropped_avatar():
            self.app.sound_mgr.play_sfx("sfx_click")
            new_cfg = {
                "cid": state["cid"],
                "cx": round(state["cx"], 3),
                "cy": round(state["cy"], 3),
                "zoom": round(state["zoom"], 3),
            }
            if state["preset_key"] and state["preset_key"] in self.img_mgr.AVATAR_PRESET_DEFAULTS:
                p_map = dict(self.working.get("preset_avatar_crops") or {})
                p_map[state["preset_key"]] = new_cfg
                self.working["preset_avatar_crops"] = p_map
                self.working["avatar"] = state["preset_key"]
            else:
                self.working["avatar_crop"] = new_cfg
                self.working["avatar"] = "CARD_CROP"
            self.img_mgr.avatar_cache.clear()
            self._refresh_avatar_selection_ui()
            self.lbl_save_status.config(
                text=f"✔ 已套用【{CARD_DB[state['cid']]['name']}】圓框頭像裁切！記得點擊右上角『儲存並套用設定』。",
                fg="#06d6a0",
            )
            crop_overlay.destroy()

        tk.Button(
            bot_row,
            text="✔ 確定套用此圓框頭像",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 12, "bold"),
            padx=26,
            pady=6,
            cursor="hand2",
            command=apply_cropped_avatar,
        ).pack(side=tk.RIGHT, padx=8)

        tk.Button(
            bot_row,
            text="↺ 重置對準頭部中央",
            bg="#3a3f58",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            padx=16,
            pady=6,
            cursor="hand2",
            command=lambda: [
                state.update({"cx": 0.50, "cy": 0.24, "zoom": 1.85}),
                zoom_scale.set(1.85),
                redraw_cropper(),
            ],
        ).pack(side=tk.RIGHT, padx=8)

        # 中央三欄：左欄分系列選卡清單、中欄互動式卡圖圓框畫布、右欄圓形頭像即時預覽
        mid_body = tk.Frame(crop_overlay, bg="#151b29")
        mid_body.pack(fill=tk.BOTH, expand=True)

        # 左欄：先選系列分類，再挑卡片
        card_pick_col = tk.Frame(mid_body, bg="#1b2234", bd=2, relief=tk.SOLID, padx=10, pady=8, width=335)
        card_pick_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        card_pick_col.pack_propagate(False)

        tk.Label(
            card_pick_col,
            text="1. 先選擇系列分類或預設代表角色：",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 10, "bold"),
        ).pack(anchor="w", pady=(0, 4))

        series_tab_frame = tk.Frame(card_pick_col, bg="#1b2234")
        series_tab_frame.pack(fill=tk.X, pady=(0, 6))

        tab_defs = [
            ("PRESETS", "★ 預設代表角色 (9位)"),
            ("BFR/S78", "防盾 BFR/S78"),
            ("GA/S131", "GA文庫 S131"),
            ("BTR/W107", "孤獨搖滾 BTR/W107"),
        ]
        tab_btns = {}

        def switch_series_tab(t_code: str):
            state["series_tab"] = t_code
            for k, tb in tab_btns.items():
                tb.config(
                    bg="#ffd166" if k == t_code else "#252c42",
                    fg="#000000" if k == t_code else "#ffffff",
                )
            populate_card_list()

        for idx_t, (t_code, t_label) in enumerate(tab_defs):
            r_t, c_t = divmod(idx_t, 2)
            tb = tk.Button(
                series_tab_frame,
                text=t_label,
                bg="#ffd166" if state["series_tab"] == t_code else "#252c42",
                fg="#000000" if state["series_tab"] == t_code else "#ffffff",
                font=(ff, 9, "bold"),
                width=19,
                pady=3,
                cursor="hand2",
                command=lambda tc=t_code: switch_series_tab(tc),
            )
            tb.grid(row=r_t, column=c_t, padx=3, pady=2, sticky="ew")
            tab_btns[t_code] = tb

        s_row = tk.Frame(card_pick_col, bg="#1b2234")
        s_row.pack(fill=tk.X, pady=(2, 6))
        kw_var = tk.StringVar()
        ent_kw = tk.Entry(s_row, textvariable=kw_var, bg="#10141f", fg="#ffffff", insertbackground="white", font=(ff, 10))
        ent_kw.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        list_canvas = tk.Canvas(card_pick_col, bg="#141824", highlightthickness=0)
        list_sc = tk.Scrollbar(card_pick_col, orient=tk.VERTICAL, command=list_canvas.yview)
        list_inner = tk.Frame(list_canvas, bg="#141824")
        list_inner.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=list_inner, anchor="nw")
        list_canvas.configure(yscrollcommand=list_sc.set)
        list_sc.pack(side=tk.RIGHT, fill=tk.Y)
        list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def populate_card_list():
            for w in list_inner.winfo_children():
                w.destroy()
            kw = kw_var.get().strip().lower()
            cur_tab = state["series_tab"]

            if cur_tab == "PRESETS":
                for p_key, (p_cid, p_name, _, _, _, _) in self.img_mgr.AVATAR_PRESET_DEFAULTS.items():
                    if p_cid not in CARD_DB:
                        continue
                    cdata = CARD_DB[p_cid]
                    if kw and kw not in p_name.lower() and kw not in cdata["name"].lower() and kw not in p_cid.lower():
                        continue
                    is_cur = (state["preset_key"] == p_key) or (state["cid"] == p_cid and state["preset_key"] is None)
                    b = tk.Button(
                        list_inner,
                        text=f"★ 預設【{p_name}】— {cdata['name']}",
                        bg="#f4a261" if is_cur else "#23293d",
                        fg="#000000" if is_cur else "#ffffff",
                        font=(ff, 9, "bold"),
                        anchor="w",
                        width=36,
                        pady=4,
                        cursor="hand2",
                        command=lambda pk=p_key, pc=p_cid: select_crop_card(pc, preset_key=pk),
                    )
                    b.pack(fill=tk.X, padx=3, pady=2)
            else:
                series_cards = SERIES_DB.get(cur_tab, CARD_DB)
                for cid, cdata in series_cards.items():
                    if kw and kw not in cid.lower() and kw not in cdata["name"].lower():
                        continue
                    is_cur = (cid == state["cid"]) and (state["preset_key"] is None)
                    b = tk.Button(
                        list_inner,
                        text=f"{cdata['name']} ({cid})",
                        bg="#f4a261" if is_cur else "#23293d",
                        fg="#000000" if is_cur else "#ffffff",
                        font=(ff, 9, "bold"),
                        anchor="w",
                        width=36,
                        pady=3,
                        cursor="hand2",
                        command=lambda k=cid: select_crop_card(k, preset_key=None),
                    )
                    b.pack(fill=tk.X, padx=3, pady=2)

        tk.Button(
            s_row,
            text="搜尋",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 9, "bold"),
            padx=8,
            command=populate_card_list,
        ).pack(side=tk.RIGHT)
        ent_kw.bind("<Return>", lambda e: populate_card_list())

        # 中欄：卡圖與可拖動/滾輪縮放的圓形取景框
        center_canvas_col = tk.Frame(mid_body, bg="#1b2234", bd=2, relief=tk.SOLID, padx=12, pady=8)
        center_canvas_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        tk.Label(
            center_canvas_col,
            text="2. 滑鼠左鍵拖動圓框・滾輪放大縮小：",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 11, "bold"),
        ).pack(pady=(0, 4))

        CANVAS_W, CANVAS_H = 280, 392
        crop_canvas = tk.Canvas(
            center_canvas_col,
            width=CANVAS_W,
            height=CANVAS_H,
            bg="#0f131d",
            highlightthickness=2,
            highlightbackground="#ffd166",
            cursor="fleur",
        )
        crop_canvas.pack(pady=4)

        # 右欄：即時圓框頭像預覽與縮放倍率滑桿
        preview_col = tk.Frame(mid_body, bg="#1b2234", bd=2, relief=tk.SOLID, padx=14, pady=12, width=260)
        preview_col.pack(side=tk.LEFT, fill=tk.Y)
        preview_col.pack_propagate(False)

        tk.Label(
            preview_col,
            text="3. 圓框頭像即時預覽：",
            bg="#1b2234",
            fg="#06d6a0",
            font=(ff, 11, "bold"),
        ).pack(pady=(0, 10))

        lbl_big_preview = tk.Label(preview_col, bg="#141824", bd=2, relief=tk.RIDGE)
        lbl_big_preview.pack(pady=6)

        lbl_hud_preview = tk.Label(preview_col, bg="#141824", bd=1, relief=tk.SOLID)
        lbl_hud_preview.pack(pady=6)

        lbl_zoom_info = tk.Label(
            preview_col,
            text="縮放倍率：1.85x",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 10, "bold"),
        )
        lbl_zoom_info.pack(pady=(12, 2))

        def on_zoom_slider(val):
            state["zoom"] = float(val)
            redraw_cropper()

        zoom_scale = tk.Scale(
            preview_col,
            from_=1.0,
            to=3.5,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            bg="#141824",
            fg="#ffd166",
            troughcolor="#2b3348",
            highlightthickness=0,
            font=(ff, 9, "bold"),
            command=on_zoom_slider,
        )
        zoom_scale.set(state["zoom"])
        zoom_scale.pack(fill=tk.X, pady=4)

        tk.Label(
            preview_col,
            text="💡 提示：\n• 在中間卡圖上滑動【滑鼠滾輪】可直接放大/縮小圓框\n• 按住【滑鼠左鍵】可自由移動圓框位置對準角色臉部",
            bg="#141824",
            fg="#adb5bd",
            font=(ff, 9),
            justify=tk.LEFT,
            wraplength=220,
            padx=8,
            pady=8,
        ).pack(fill=tk.X, pady=(12, 0))

        def select_crop_card(cid: str, preset_key: str = None):
            state["preset_key"] = preset_key
            state["cid"] = cid
            saved_p = (self.working.get("preset_avatar_crops") or {}).get(preset_key, {}) if preset_key else {}
            if saved_p and saved_p.get("cid") == cid:
                state["cx"] = float(saved_p.get("cx", 0.50))
                state["cy"] = float(saved_p.get("cy", 0.24))
                state["zoom"] = float(saved_p.get("zoom", 1.85))
            elif preset_key and preset_key in self.img_mgr.AVATAR_PRESET_DEFAULTS:
                _, _, _, d_cx, d_cy, d_zm = self.img_mgr.AVATAR_PRESET_DEFAULTS[preset_key]
                state["cx"], state["cy"], state["zoom"] = d_cx, d_cy, d_zm
            else:
                is_cx = CARD_DB.get(cid, {}).get("type") == "CX"
                state["cx"] = 0.50
                state["cy"] = 0.45 if is_cx else 0.24
                state["zoom"] = 1.60 if is_cx else 1.85
            zoom_scale.set(state["zoom"])
            populate_card_list()
            redraw_cropper()

        def redraw_cropper():
            cid = state["cid"]
            src_pil = self.img_mgr.pil_cache.get(cid)
            if src_pil is None:
                return
            disp_img = src_pil.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS).convert("RGBA")
            # 繪製半透明暗角與亮色圓形取景框
            base_dim = min(CANVAS_W, CANVAS_H)
            radius = max(18, int((base_dim / max(0.8, state["zoom"])) / 2))
            cx_px = int(CANVAS_W * state["cx"])
            cy_px = int(CANVAS_H * state["cy"])
            cx_px = max(radius, min(CANVAS_W - radius, cx_px))
            cy_px = max(radius, min(CANVAS_H - radius, cy_px))
            state["cx"] = cx_px / float(CANVAS_W)
            state["cy"] = cy_px / float(CANVAS_H)

            dim_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (10, 14, 24, 150))
            hole_mask = Image.new("L", (CANVAS_W, CANVAS_H), 255)
            h_draw = ImageDraw.Draw(hole_mask)
            h_draw.ellipse(
                [cx_px - radius, cy_px - radius, cx_px + radius, cy_px + radius], fill=0
            )
            composed = Image.composite(dim_layer, Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0)), hole_mask)
            final_canvas_pil = Image.alpha_composite(disp_img, composed).convert("RGB")
            c_draw = ImageDraw.Draw(final_canvas_pil)
            c_draw.ellipse(
                [cx_px - radius, cy_px - radius, cx_px + radius, cy_px + radius],
                outline="#06d6a0",
                width=3,
            )
            c_draw.ellipse(
                [cx_px - radius - 2, cy_px - radius - 2, cx_px + radius + 2, cy_px + radius + 2],
                outline="#ffd166",
                width=1,
            )

            tk_c_img = ImageTk.PhotoImage(final_canvas_pil)
            crop_canvas.delete("all")
            crop_canvas.create_image(0, 0, anchor="nw", image=tk_c_img)
            crop_canvas.image = tk_c_img

            lbl_zoom_info.config(text=f"縮放倍率：{state['zoom']:.2f}x")
            self.img_mgr.avatar_cache.clear()
            cur_crop_cfg = {
                "cid": state["cid"],
                "cx": state["cx"],
                "cy": state["cy"],
                "zoom": state["zoom"],
            }
            big_av = self.img_mgr.get_avatar_visual(
                "CARD_CROP", size=104, border_color="#06d6a0", is_active_turn=True, crop_cfg=cur_crop_cfg
            )
            lbl_big_preview.config(image=big_av)
            lbl_big_preview.image = big_av

            hud_av = self.img_mgr.get_avatar_visual(
                "CARD_CROP", size=52, border_color="#ffd166", is_active_turn=False, crop_cfg=cur_crop_cfg
            )
            lbl_hud_preview.config(image=hud_av, text="對戰 HUD 尺寸預覽", compound=tk.TOP, fg="#8ecae6", font=(ff, 9))
            lbl_hud_preview.image = hud_av

        def on_canvas_press(event):
            state["cx"] = event.x / float(CANVAS_W)
            state["cy"] = event.y / float(CANVAS_H)
            redraw_cropper()

        def on_canvas_drag(event):
            state["cx"] = max(0.05, min(0.95, event.x / float(CANVAS_W)))
            state["cy"] = max(0.05, min(0.95, event.y / float(CANVAS_H)))
            redraw_cropper()

        def on_canvas_wheel(event):
            if getattr(event, "delta", 0) > 0 or getattr(event, "num", 0) == 4:
                new_z = min(3.5, state["zoom"] + 0.12)
            else:
                new_z = max(1.0, state["zoom"] - 0.12)
            state["zoom"] = new_z
            zoom_scale.set(round(new_z, 2))
            redraw_cropper()

        crop_canvas.bind("<ButtonPress-1>", on_canvas_press)
        crop_canvas.bind("<B1-Motion>", on_canvas_drag)
        crop_canvas.bind("<MouseWheel>", on_canvas_wheel)
        crop_canvas.bind("<Button-4>", on_canvas_wheel)
        crop_canvas.bind("<Button-5>", on_canvas_wheel)

        populate_card_list()
        redraw_cropper()

    def on_upload_custom_avatar(self):
        path = filedialog.askopenfilename(
            title="選擇自訂玩家頭像圖片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp"), ("All Files", "*.*")],
        )
        if path and os.path.exists(path):
            self.working["custom_avatar_path"] = path
            self.working["avatar"] = "CUSTOM"
            self.img_mgr.avatar_cache.clear()
            av_img = self.img_mgr.get_avatar_visual(
                "CUSTOM", size=56, border_color="#ffd166", custom_path=path
            )
            if "CUSTOM" in self.avatar_btns:
                self.avatar_btns["CUSTOM"].config(image=av_img)
                self.avatar_btns["CUSTOM"].image = av_img
            self._refresh_avatar_selection_ui()
            self.lbl_save_status.config(text="✔ 已載入自訂頭像圖片！記得點擊右上角儲存設定。", fg="#06d6a0")

    def select_theme(self, t_key: str):
        self.working["theme"] = t_key
        self._refresh_theme_selection_ui()
        self._refresh_bg_preview()

    def _refresh_theme_selection_ui(self):
        cur_t = self.working.get("theme", "OCEAN")
        for k, b in self.theme_btns.items():
            is_sel = k == cur_t
            b.config(
                bg="#ffd166" if is_sel else "#252c42",
                fg="#000000" if is_sel else "#ffffff",
            )
        bg_p = self.working.get("custom_bg_path", "")
        if bg_p and os.path.exists(bg_p):
            self.lbl_bg_path.config(text=f"目前自訂背景：{os.path.basename(bg_p)}")
        else:
            self.lbl_bg_path.config(text="目前背景模式：內建《大師決鬥》王牌卡斜向動態主題牆")

    def on_upload_custom_bg(self):
        path = filedialog.askopenfilename(
            title="選擇自訂背景桌布圖片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp"), ("All Files", "*.*")],
        )
        if path and os.path.exists(path):
            self.working["custom_bg_path"] = path
            self.img_mgr.bg_cache.clear()
            self._refresh_theme_selection_ui()
            self._refresh_bg_preview()
            self.lbl_save_status.config(text="✔ 已套用自訂背景圖片預覽！點擊右上角即可儲存。", fg="#06d6a0")

    def on_clear_custom_bg(self):
        self.working["custom_bg_path"] = ""
        self.img_mgr.bg_cache.clear()
        self._refresh_theme_selection_ui()
        self._refresh_bg_preview()

    def select_sleeve_style(self, s_key: str):
        self.working["sleeve_style"] = s_key
        self.img_mgr.set_sleeve_config(s_key, self.working.get("custom_sleeve_path", ""))
        self._refresh_sleeve_selection_ui()
        self.lbl_save_status.config(text="✔ 已切換卡套樣式！記得點擊右上角儲存設定。", fg="#06d6a0")

    def on_upload_custom_sleeve(self):
        path = filedialog.askopenfilename(
            title="選擇自訂卡套圖片 (.png / .jpg / .webp)",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp"), ("All Files", "*.*")],
        )
        if path and os.path.exists(path):
            self.working["custom_sleeve_path"] = path
            self.working["sleeve_style"] = "CUSTOM"
            self.img_mgr.set_sleeve_config("CUSTOM", path)
            self._refresh_sleeve_selection_ui()
            self.lbl_save_status.config(text="✔ 已套用自訂卡套圖片！記得點擊右上角儲存設定。", fg="#06d6a0")

    def _refresh_sleeve_selection_ui(self):
        cur_s = self.working.get("sleeve_style", "WS_DEFAULT")
        c_path = self.working.get("custom_sleeve_path", "")
        if hasattr(self, "sleeve_btns"):
            for k, b in self.sleeve_btns.items():
                is_sel = k == cur_s
                b.config(
                    bg="#06d6a0" if is_sel else ("#118ab2" if k == "CUSTOM" else "#252c42"),
                    fg="#000000" if is_sel else "#ffffff",
                )
        if hasattr(self, "lbl_sleeve_preview"):
            pv_img = self.img_mgr.get_sleeve_preview_visual(cur_s, c_path, width=48, height=68)
            self.lbl_sleeve_preview.config(image=pv_img)
            self.lbl_sleeve_preview.image = pv_img

    def _on_font_change(self, event=None):
        self.working["font_family"] = self.font_var.get()
        self._refresh_font_selection_ui()

    def select_font_size(self, sz: int):
        self.working["effect_font_size"] = int(sz)
        self._refresh_font_selection_ui()

    def _refresh_font_selection_ui(self):
        cur_sz = int(self.working.get("effect_font_size", 12))
        cur_ff = self.working.get("font_family", "Microsoft JhengHei")
        for sz_val, b in self.font_size_btns.items():
            is_sel = sz_val == cur_sz
            b.config(
                bg="#06d6a0" if is_sel else "#252c42",
                fg="#000000" if is_sel else "#ffffff",
            )
        self.lbl_font_preview.config(font=(cur_ff, cur_sz))

    def _on_toggle_bgm(self):
        cur = bool(self.working.get("bgm_enabled", True))
        self.working["bgm_enabled"] = not cur
        self.app.settings["bgm_enabled"] = self.working["bgm_enabled"]
        if self.working["bgm_enabled"]:
            self.app.sound_mgr.play_bgm("bgm_menu", force_restart=True)
        else:
            self.app.sound_mgr.stop_bgm()
        self._refresh_audio_selection_ui()

    def _on_toggle_sfx(self):
        cur = bool(self.working.get("sfx_enabled", True))
        self.working["sfx_enabled"] = not cur
        self.app.settings["sfx_enabled"] = self.working["sfx_enabled"]
        if self.working["sfx_enabled"]:
            self.app.sound_mgr.play_sfx("sfx_click")
        self._refresh_audio_selection_ui()

    def _on_bgm_vol_change(self, val):
        v = int(float(val))
        self.working["bgm_volume"] = v
        self.app.settings["bgm_volume"] = v
        self.lbl_bgm_vol.config(text=f"音樂 (BGM) 總音量：{v}% (上限已降為原1/10)")
        self.app.sound_mgr.update_bgm_volume()

    def _on_sfx_vol_change(self, val):
        v = int(float(val))
        self.working["sfx_volume"] = v
        self.app.settings["sfx_volume"] = v
        self.lbl_sfx_vol.config(text=f"音效 (SFX) 總音量：{v}% (可點右上個別調整)")

    def _on_indiv_track_vol_change(self, t_key: str, short_name: str, val):
        v = int(float(val))
        t_vols = dict(self.working.get("track_volumes") or {})
        t_vols[t_key] = v
        self.working["track_volumes"] = t_vols
        self.app.settings["track_volumes"] = dict(t_vols)
        if hasattr(self, "indiv_vol_labels") and t_key in self.indiv_vol_labels:
            self.indiv_vol_labels[t_key].config(text=f"{short_name}:{v}%")
        if t_key.startswith("bgm_"):
            self.app.sound_mgr.update_bgm_volume()

    def _test_play_audio(self, key: str):
        if key.startswith("bgm_"):
            self.working["bgm_enabled"] = True
            self.app.settings["bgm_enabled"] = True
            self._refresh_audio_selection_ui()
            self.app.sound_mgr.play_bgm(key, force_restart=True)
        else:
            self.working["sfx_enabled"] = True
            self.app.settings["sfx_enabled"] = True
            self._refresh_audio_selection_ui()
            self.app.sound_mgr.play_sfx(key)

    def _refresh_audio_selection_ui(self):
        bgm_on = bool(self.working.get("bgm_enabled", True))
        sfx_on = bool(self.working.get("sfx_enabled", True))
        self.btn_toggle_bgm.config(
            text="🎵 背景音樂：開啟" if bgm_on else "🔇 背景音樂：關閉",
            bg="#06d6a0" if bgm_on else "#4a4e69",
            fg="#000000" if bgm_on else "#ffffff",
        )
        self.btn_toggle_sfx.config(
            text="🔊 動作音效：開啟" if sfx_on else "🔇 動作音效：關閉",
            bg="#06d6a0" if sfx_on else "#4a4e69",
            fg="#000000" if sfx_on else "#ffffff",
        )

    def open_custom_audio_modal(self):
        """彈出『個別音樂與音效音量微調 ＆ 檔案替換』視窗，支援 1% 級距個別調整各項 BGM 與 SFX 音量"""
        self.app.sound_mgr.play_sfx("sfx_click")
        modal = tk.Frame(self, bg="#151b29", bd=3, relief=tk.RIDGE, padx=22, pady=16)
        modal.place(relx=0.5, rely=0.5, anchor="center", width=880, height=540)
        modal.lift()

        ff = self.app.get_font_family()
        top_r = tk.Frame(modal, bg="#151b29")
        top_r.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            top_r,
            text="🎚️ 個別背景音樂 (BGM) 與動作音效 (SFX) 音量微調 ＆ 音檔設定",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 14, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            top_r,
            text="✖ 關閉",
            bg="#e63946",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            command=modal.destroy,
        ).pack(side=tk.RIGHT)

        tk.Label(
            modal,
            text="💡 音樂 (BGM) 100% 音量已調降為原本的 1/10，且所有音樂與音效皆可以 1% 為單位個別調整音量或替換 .mp3/.wav：",
            bg="#151b29",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        rows_box = tk.Frame(modal, bg="#1b2234", bd=1, relief=tk.SOLID, padx=12, pady=8)
        rows_box.pack(fill=tk.BOTH, expand=True)

        custom_map = dict(self.working.get("custom_audio_paths") or {})
        t_vols = dict(self.working.get("track_volumes") or {})
        path_labels = {}
        modal_vol_labels = {}
        short_lookup = {
            "bgm_menu": "主選單樂",
            "bgm_main": "主階音樂",
            "bgm_battle": "戰階音樂",
            "sfx_click": "點擊音效",
            "sfx_draw": "抽卡音效",
            "sfx_damage": "扣血音效",
            "sfx_climax": "名場面音",
        }

        def on_modal_track_vol(t_key: str, val):
            v = int(float(val))
            self._on_indiv_track_vol_change(t_key, short_lookup.get(t_key, t_key), v)
            if hasattr(self, "indiv_vol_scales") and t_key in self.indiv_vol_scales:
                self.indiv_vol_scales[t_key].set(v)
            if t_key in modal_vol_labels:
                modal_vol_labels[t_key].config(text=f"個別音量: {v:3d}%")

        def pick_audio_file(t_key: str):
            p = filedialog.askopenfilename(
                title=f"選擇 {t_key} 的音訊檔案 (.mp3 / .wav)",
                filetypes=[("Audio Files", "*.mp3;*.wav"), ("All Files", "*.*")],
            )
            if p and os.path.exists(p):
                custom_map[t_key] = p
                self.working["custom_audio_paths"] = dict(custom_map)
                self.app.settings["custom_audio_paths"] = dict(custom_map)
                path_labels[t_key].config(text=os.path.basename(p), fg="#06d6a0")
                self._test_play_audio(t_key)

        def reset_audio_file(t_key: str):
            custom_map.pop(t_key, None)
            self.working["custom_audio_paths"] = dict(custom_map)
            self.app.settings["custom_audio_paths"] = dict(custom_map)
            resolved = self.app.sound_mgr.get_track_path(t_key)
            path_labels[t_key].config(text=os.path.basename(resolved) if resolved else "預設音檔", fg="#adb5bd")
            self._test_play_audio(t_key)

        for idx_k, (t_key, t_name, def_fname) in enumerate(SoundManager.TRACK_KEYS):
            r_f = tk.Frame(rows_box, bg="#1b2234", pady=5)
            r_f.pack(fill=tk.X)
            is_b = t_key.startswith("bgm_")
            tk.Label(
                r_f,
                text=f"• {t_name}：",
                bg="#1b2234",
                fg="#06d6a0" if is_b else "#ffd166",
                font=(ff, 10, "bold"),
                width=14,
                anchor="w",
            ).pack(side=tk.LEFT)

            cur_tv = int(t_vols.get(t_key, 100))
            lbl_mv = tk.Label(
                r_f,
                text=f"個別音量: {cur_tv:3d}%",
                bg="#1b2234",
                fg="#ffffff",
                font=(ff, 9, "bold"),
                width=13,
                anchor="w",
            )
            lbl_mv.pack(side=tk.LEFT, padx=(2, 4))
            modal_vol_labels[t_key] = lbl_mv

            sc_mv = tk.Scale(
                r_f,
                from_=0,
                to=100,
                resolution=1,
                orient=tk.HORIZONTAL,
                showvalue=False,
                bg="#141824",
                fg="#06d6a0" if is_b else "#ffd166",
                troughcolor="#2b3348",
                highlightthickness=0,
                width=12,
                length=160,
                command=lambda val, k=t_key: on_modal_track_vol(k, val),
            )
            sc_mv.set(cur_tv)
            sc_mv.pack(side=tk.LEFT, padx=6)

            resolved_p = self.app.sound_mgr.get_track_path(t_key)
            disp_p = os.path.basename(resolved_p) if (resolved_p and os.path.exists(resolved_p)) else def_fname
            is_mp3 = disp_p.lower().endswith(".mp3")
            lbl_p = tk.Label(
                r_f,
                text=disp_p,
                bg="#10141f",
                fg="#06d6a0" if is_mp3 else "#adb5bd",
                font=(ff, 9, "bold"),
                width=22,
                anchor="w",
                padx=8,
                pady=3,
            )
            lbl_p.pack(side=tk.LEFT, padx=6)
            path_labels[t_key] = lbl_p

            tk.Button(
                r_f,
                text="📂 選擇檔案",
                bg="#118ab2",
                fg="#ffffff",
                font=(ff, 9, "bold"),
                padx=8,
                command=lambda k=t_key: pick_audio_file(k),
            ).pack(side=tk.LEFT, padx=3)

            tk.Button(
                r_f,
                text="🔊 試聽",
                bg="#252c42",
                fg="#ffd166",
                font=(ff, 9, "bold"),
                padx=8,
                command=lambda k=t_key: self._test_play_audio(k),
            ).pack(side=tk.LEFT, padx=3)

            tk.Button(
                r_f,
                text="↺ 預設檔",
                bg="#3a3f58",
                fg="#ffffff",
                font=(ff, 9, "bold"),
                padx=8,
                command=lambda k=t_key: reset_audio_file(k),
            ).pack(side=tk.LEFT, padx=3)

    def on_reset_defaults(self):
        self.working = dict(self.app.default_settings())
        self.scale_flip.set(self.working["ai_flip_interval_sec"])
        self.scale_pause.set(self.working["ai_flip_end_pause_sec"])
        self.scale_dim.set(self.working["bg_dim_percent"])
        if hasattr(self, "scale_bgm_vol"):
            self.scale_bgm_vol.set(self.working["bgm_volume"])
        if hasattr(self, "scale_sfx_vol"):
            self.scale_sfx_vol.set(self.working["sfx_volume"])
        if hasattr(self, "indiv_vol_scales"):
            t_vols = self.working.get("track_volumes") or {}
            for k, sc in self.indiv_vol_scales.items():
                sc.set(int(t_vols.get(k, 100)))
        self._refresh_audio_selection_ui()
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, self.working["player_name"])
        self.font_var.set(self.working["font_family"])
        self._refresh_avatar_selection_ui()
        self.img_mgr.set_sleeve_config(
            self.working.get("sleeve_style", "WS_DEFAULT"),
            self.working.get("custom_sleeve_path", ""),
        )
        self._refresh_theme_selection_ui()
        self._refresh_sleeve_selection_ui()
        self._refresh_font_selection_ui()
        self._refresh_bg_preview()
        self.lbl_save_status.config(text="↺ 已恢復預設值（翻牌 2.0 秒、停留 3.5 秒），請按儲存確認。", fg="#ffd166")

    def on_save_settings(self):
        typed_name = self.ent_name.get().strip() or "玩家1"
        self.working["player_name"] = typed_name
        self.app.save_user_settings(self.working)
        self.lbl_save_status.config(
            text="💾 設定已成功儲存並套用！（AI 翻牌秒數、頭像、背景與字體皆已生效）",
            fg="#06d6a0",
        )


# ==========================================
# 最外層主系統介面 (MainApp：單人、區網連線、編輯卡組)
# ==========================================
class MainApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Weiß Schwarz 卡牌對戰模擬器")
        self.root.geometry("1600x950")
        self.root.configure(bg="#0d111a")

        load_all_card_sets()
        self.deck_save_file = os.path.join(BASE_DIR, "custom_deck.json")
        self.decks_book_file = os.path.join(BASE_DIR, "custom_decks_book.json")
        self.settings_file = os.path.join(BASE_DIR, "user_settings.json")
        self.settings = self._load_user_settings()
        self.player_battle_name = self.settings.get("player_name", "玩家1")
        self.active_series = "BTR/W107" if "BTR/W107" in SERIES_DB else ("GA/S131" if "GA/S131" in SERIES_DB else "BFR/S78")
        self.ai_series = "BFR/S78" if "BFR/S78" in SERIES_DB else self.active_series
        self.decks_book = self._load_decks_book()
        self.current_deck_recipe = self.get_series_deck(self.active_series)

        self.img_mgr = ImageManager(self.root)
        self.img_mgr.set_sleeve_config(
            self.settings.get("sleeve_style", "WS_DEFAULT"),
            self.settings.get("custom_sleeve_path", ""),
        )
        self.sound_mgr = SoundManager(self)
        self._cached_floating_deck_key = None
        self._cached_floating_cids = []
        self.current_frame = None

        # 全域綁定按鈕點擊音效：當點擊任何 Button 時自動播放清脆點擊音效
        self.root.bind_all("<ButtonPress-1>", self._on_global_click_sfx, add="+")

        self.show_main_menu()

    def _on_global_click_sfx(self, event):
        try:
            w = event.widget
            if w and w.winfo_class() in ("Button", "TButton", "Scale"):
                self.sound_mgr.play_sfx("sfx_click")
        except Exception:
            pass

    def get_menu_floating_deck_cids(self) -> list:
        """從玩家目前使用的出戰卡組 (50張) 中隨機抽取 6 張卡片作為主選單大廳懸浮背景卡"""
        recipe = self.get_series_deck(self.active_series)
        recipe_sig = (self.active_series, tuple(sorted(recipe.items())))
        if self._cached_floating_deck_key == recipe_sig and len(self._cached_floating_cids) == 6:
            return list(self._cached_floating_cids)

        expanded = []
        for cid, cnt in recipe.items():
            if cid in CARD_DB and cnt > 0:
                expanded.extend([cid] * int(cnt))
        if not expanded:
            expanded = list(CARD_DB.keys())
        # 優先讓不同卡號都能被抽中，若不足 6 種則從 50 張卡池隨機抽滿 6 張
        unique_cids = list({cid for cid in expanded})
        if len(unique_cids) >= 6:
            chosen6 = random.sample(unique_cids, 6)
        elif len(expanded) >= 6:
            chosen6 = random.sample(expanded, 6)
        else:
            chosen6 = (expanded * 6)[:6]

        self._cached_floating_deck_key = recipe_sig
        self._cached_floating_cids = chosen6
        return list(chosen6)

    @staticmethod
    def default_settings() -> dict:
        return {
            "player_name": "玩家1",
            "avatar": "MAPLE",
            "custom_avatar_path": "",
            "avatar_crop": {"cid": "BFR/S78-073", "cx": 0.50, "cy": 0.24, "zoom": 1.85},
            "preset_avatar_crops": {},
            "ace_card_by_series": {},
            "ai_flip_interval_sec": 2.0,
            "ai_flip_end_pause_sec": 3.5,
            "theme": "OCEAN",
            "custom_bg_path": "",
            "bg_dim_percent": 65,
            "sleeve_style": "WS_DEFAULT",
            "custom_sleeve_path": "",
            "font_family": "Microsoft JhengHei",
            "effect_font_size": 12,
            "bgm_enabled": True,
            "sfx_enabled": True,
            "bgm_volume": 50,
            "sfx_volume": 80,
            "track_volumes": {
                "bgm_menu": 100,
                "bgm_main": 100,
                "bgm_battle": 100,
                "sfx_click": 100,
                "sfx_draw": 100,
                "sfx_damage": 100,
                "sfx_climax": 100,
            },
            "custom_audio_paths": {},
        }

    def _load_user_settings(self) -> dict:
        cfg = self.default_settings()
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict):
                    cfg.update(raw)
            except Exception:
                pass
        cfg["ai_flip_interval_sec"] = max(1.0, min(10.0, float(cfg.get("ai_flip_interval_sec", 2.0))))
        cfg["ai_flip_end_pause_sec"] = max(1.0, min(10.0, float(cfg.get("ai_flip_end_pause_sec", 3.5))))
        cfg["bg_dim_percent"] = max(20, min(90, int(cfg.get("bg_dim_percent", 65))))
        cfg["effect_font_size"] = max(10, min(18, int(cfg.get("effect_font_size", 12))))
        return cfg

    def save_user_settings(self, new_cfg: dict):
        self.settings.update(new_cfg)
        self.settings["ai_flip_interval_sec"] = max(
            1.0, min(10.0, float(self.settings.get("ai_flip_interval_sec", 2.0)))
        )
        self.settings["ai_flip_end_pause_sec"] = max(
            1.0, min(10.0, float(self.settings.get("ai_flip_end_pause_sec", 3.5)))
        )
        self.player_battle_name = self.settings.get("player_name", "玩家1")
        if hasattr(self, "img_mgr"):
            self.img_mgr.set_sleeve_config(
                self.settings.get("sleeve_style", "WS_DEFAULT"),
                self.settings.get("custom_sleeve_path", ""),
            )
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_font_family(self) -> str:
        return self.settings.get("font_family", "Microsoft JhengHei")

    def get_effect_font_size(self) -> int:
        return int(self.settings.get("effect_font_size", 12))

    def get_ai_avatar_id(self, ai_series_code: str) -> str:
        if ai_series_code == "GA/S131":
            return "MAHIRU"
        if ai_series_code == "BTR/W107":
            return "KITA"
        return "MAPLE"

    def set_user_ace_card_id(self, cid: str, scode: str = None):
        target_s = scode or self.active_series
        ace_map = dict(self.settings.get("ace_card_by_series") or {})
        ace_map[target_s] = cid
        self.settings["ace_card_by_series"] = ace_map
        self.save_user_settings(self.settings)

    def get_series_ace_card_id(self, scode: str) -> str:
        ace_map = self.settings.get("ace_card_by_series") or {}
        if scode in ace_map and ace_map[scode] in CARD_DB:
            return ace_map[scode]
        if scode in DEFAULT_SERIES_ACE_CARDS and DEFAULT_SERIES_ACE_CARDS[scode] in CARD_DB:
            return DEFAULT_SERIES_ACE_CARDS[scode]
        recipe = self.get_series_deck(scode)
        for def_cid in DEFAULT_SERIES_ACE_CARDS.values():
            if recipe.get(def_cid, 0) > 0 and def_cid in CARD_DB:
                return def_cid
        lv3_cids = [
            cid for cid, cnt in recipe.items()
            if cnt > 0 and cid in CARD_DB and CARD_DB[cid].get("level", 0) == 3
        ]
        if lv3_cids:
            return lv3_cids[0]
        return "BFR/S78-063"

    def get_ai_ace_card_id(self, ai_scode: str) -> str:
        if ai_scode in DEFAULT_SERIES_ACE_CARDS and DEFAULT_SERIES_ACE_CARDS[ai_scode] in CARD_DB:
            return DEFAULT_SERIES_ACE_CARDS[ai_scode]
        return self.get_series_ace_card_id(ai_scode) 

    def _migrate_recipe_ids(self, data: dict) -> dict:
        if not isinstance(data, dict):
            return {}
        out = {}
        for cid, cnt in data.items():
            if cnt <= 0:
                continue
            if cid in CARD_DB:
                out[cid] = out.get(cid, 0) + cnt
            else:
                m = re.match(r"^([A-Z0-9]+/[A-Z0-9]+-[T0-9]+)", str(cid))
                if m:
                    base_cand = m.group(1)
                    if base_cand in CARD_DB:
                        hr_cand = CARD_DB[base_cand].get("high_rarity_id")
                        target = hr_cand if (hr_cand and hr_cand in CARD_DB) else base_cand
                        out[target] = out.get(target, 0) + cnt
        return out

    def _is_valid_recipe(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False
        total = sum(cnt for cid, cnt in data.items() if cid in CARD_DB and cnt > 0)
        cx_cnt = sum(
            cnt
            for cid, cnt in data.items()
            if cid in CARD_DB and cnt > 0 and CARD_DB[cid]["type"] == "CX"
        )
        base_counts = {}
        for cid, cnt in data.items():
            if cid in CARD_DB and cnt > 0:
                bid = CARD_DB[cid].get("base_id", cid)
                base_counts[bid] = base_counts.get(bid, 0) + cnt
        max_base = max(base_counts.values()) if base_counts else 0
        return total == 50 and cx_cnt <= 8 and max_base <= 4

    def get_deck_display_name(self, scode: str) -> str:
        user_names = self.settings.get("user_deck_names") or {}
        if scode in user_names:
            return user_names[scode]
        if scode == "CUSTOM":
            return "我的自訂卡組 1"
        return SERIES_LABELS.get(scode, scode)

    def _load_decks_book(self) -> dict:
        book = {}
        for scode, def_rec in SERIES_DEFAULT_DECKS.items():
            book[scode] = dict(def_rec)
        if os.path.exists(self.decks_book_file):
            try:
                with open(self.decks_book_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict):
                    if "_active_series" in raw:
                        self.active_series = raw["_active_series"]
                    if "_ai_series" in raw:
                        self.ai_series = raw["_ai_series"]
                    for k, v in raw.items():
                        if not k.startswith("_") and isinstance(v, dict):
                            migrated_v = self._migrate_recipe_ids(v)
                            if self._is_valid_recipe(migrated_v):
                                book[k] = migrated_v
            except Exception:
                pass
        if "CUSTOM" not in book:
            book["CUSTOM"] = dict(book.get(self.active_series, DEFAULT_DECK_RECIPE))
        return book

    def _persist_decks_book(self):
        payload = dict(self.decks_book)
        payload["_active_series"] = self.active_series
        payload["_ai_series"] = self.ai_series
        try:
            with open(self.decks_book_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            with open(self.deck_save_file, "w", encoding="utf-8") as f:
                json.dump(self.get_series_deck(self.active_series), f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_active_deck(self) -> dict:
        return self.get_series_deck(self.active_series)

    def get_series_deck(self, scode: str) -> dict:
        if scode in self.decks_book and self._is_valid_recipe(self.decks_book[scode]):
            return dict(self.decks_book[scode])
        if scode in SERIES_DEFAULT_DECKS:
            return dict(SERIES_DEFAULT_DECKS[scode])
        return dict(DEFAULT_DECK_RECIPE)

    def save_series_deck(self, scode: str, recipe: dict):
        self.decks_book[scode] = dict(recipe)
        if scode == self.active_series:
            self.current_deck_recipe = dict(recipe)
        self._persist_decks_book()

    def set_active_series(self, scode: str):
        if scode in SERIES_DB or scode in self.decks_book or scode == "CUSTOM":
            self.active_series = scode
            self.current_deck_recipe = self.get_series_deck(scode)
            self._cached_floating_deck_key = None
            self.img_mgr.bg_cache.clear()
            self._persist_decks_book()

    def set_ai_series(self, scode: str):
        if scode in SERIES_DB or scode in self.decks_book or scode == "CUSTOM":
            self.ai_series = scode
            self._persist_decks_book()

    def clear_current_frame(self):
        self.img_mgr.callbacks.clear()
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def open_bottleneko_importer_modal(self, refresh_callback=None):
        ff = self.get_font_family()
        win = tk.Toplevel(self.root)
        win.title("🌐 貓罐子 (BottleNeko) 全系列免組牌抓取 ＆ 20張分批匯入中心")
        win.geometry("920x680")
        win.configure(bg="#131926")
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win,
            text="🌐 貓罐子 (BottleNeko) 全系列免組牌抓取 ／ 每次 20 張分批匯入中心",
            bg="#131926",
            fg="#ffd166",
            font=(ff, 15, "bold"),
        ).pack(pady=(12, 4))

        tk.Label(
            win,
            text="不用自己先去貓罐子組牌！直接從下方搜尋貓罐子全系列清單（或貼上系列網址如 https://bottleneko.app/ws/series/172），\n即可選擇【一次抓完整個系列】或【每次穩定抓 20 張】，自動解析中文效果與高低版本卡圖！",
            bg="#131926",
            fg="#8ecae6",
            font=(ff, 10),
            justify=tk.LEFT,
        ).pack(padx=20, pady=(0, 6), anchor="w")

        # 區塊 A：貓罐子全系列目錄搜尋與點選
        cat_frame = tk.Frame(win, bg="#1b2234", padx=12, pady=8, bd=1, relief=tk.SOLID)
        cat_frame.pack(fill=tk.X, padx=20, pady=4)

        top_cat_row = tk.Frame(cat_frame, bg="#1b2234")
        top_cat_row.pack(fill=tk.X)

        tk.Label(
            top_cat_row,
            text="步驟 1：從貓罐子載入全系列清單（或直接在下方輸入系列網址／編號）：",
            bg="#1b2234",
            fg="#ffd166",
            font=(ff, 10, "bold"),
        ).pack(side=tk.LEFT)

        catalog_data = []
        filtered_catalog = []

        mid_cat_row = tk.Frame(cat_frame, bg="#1b2234")
        mid_cat_row.pack(fill=tk.X, pady=(6, 2))

        tk.Label(mid_cat_row, text="🔍 篩選系列名稱/代號：", bg="#1b2234", fg="white", font=(ff, 10)).pack(side=tk.LEFT)
        var_filter = tk.StringVar()
        ent_filter = tk.Entry(mid_cat_row, textvariable=var_filter, width=22, bg="#0d111a", fg="#06d6a0", insertbackground="white", font=(ff, 10))
        ent_filter.pack(side=tk.LEFT, padx=6)

        list_frame = tk.Frame(cat_frame, bg="#0d111a")
        list_frame.pack(fill=tk.X, pady=4)
        scrollbar_cat = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        lst_series = tk.Listbox(
            list_frame,
            height=6,
            bg="#0d111a",
            fg="#ffffff",
            selectbackground="#9b5de5",
            selectforeground="#ffffff",
            font=(ff, 10),
            yscrollcommand=scrollbar_cat.set,
            exportselection=False,
        )
        scrollbar_cat.config(command=lst_series.yview)
        lst_series.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar_cat.pack(side=tk.RIGHT, fill=tk.Y)

        # 區塊 B：目標網址／系列編號 與 分批進度控制
        ctrl_frame = tk.Frame(win, bg="#1b2234", padx=12, pady=8, bd=1, relief=tk.SOLID)
        ctrl_frame.pack(fill=tk.X, padx=20, pady=4)

        row_url = tk.Frame(ctrl_frame, bg="#1b2234")
        row_url.pack(fill=tk.X, pady=2)
        tk.Label(row_url, text="步驟 2：目標系列網址 / 系列 ID / 牌組網址：", bg="#1b2234", fg="white", font=(ff, 10, "bold")).pack(side=tk.LEFT)
        var_target = tk.StringVar(value="https://bottleneko.app/ws/series/172")
        ent_target = tk.Entry(row_url, textvariable=var_target, width=48, bg="#0d111a", fg="#06d6a0", insertbackground="white", font=("Consolas", 11))
        ent_target.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

        row_batch = tk.Frame(ctrl_frame, bg="#1b2234")
        row_batch.pack(fill=tk.X, pady=(6, 2))
        tk.Label(row_batch, text="分批起始位置 (Offset)：", bg="#1b2234", fg="#8ecae6", font=(ff, 10)).pack(side=tk.LEFT)
        var_offset = tk.IntVar(value=0)
        spn_offset = tk.Spinbox(row_batch, from_=0, to=2000, increment=20, textvariable=var_offset, width=7, bg="#0d111a", fg="#ffd166", font=("Consolas", 11, "bold"))
        spn_offset.pack(side=tk.LEFT, padx=6)

        var_inc_high = tk.BooleanVar(value=True)
        tk.Checkbutton(
            row_batch,
            text="同時收錄高版本異畫卡 (SP / SSP / OFR / SR)",
            variable=var_inc_high,
            bg="#1b2234",
            fg="#ffd166",
            selectcolor="#0d111a",
            activebackground="#1b2234",
            activeforeground="#ffd166",
            font=(ff, 10, "bold"),
        ).pack(side=tk.LEFT, padx=14)

        lbl_batch_prog = tk.Label(row_batch, text="目前進度：尚未開始", bg="#1b2234", fg="#06d6a0", font=(ff, 10, "bold"))
        lbl_batch_prog.pack(side=tk.RIGHT, padx=6)

        # 區塊 C：執行紀錄 Log
        log_box = tk.Text(win, height=9, bg="#0b0e14", fg="#e0e1dd", font=("Consolas", 10))
        log_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=6)
        log_box.insert(
            "1.0",
            "💡 使用指南：\n"
            "  • 方式 A（最推薦）：點擊上方【🔄 連線載入貓罐子全系列清單】，點選任一你想玩的系列，接著按【📦 分批抓 20 張】或【🚀 一次抓完整個系列】！\n"
            "  • 方式 B：直接貼上貓罐子系列網址（如 https://bottleneko.app/ws/series/172）或牌組網址（如 https://bottleneko.app/ws/deck/wMI7n）。\n",
        )

        def _append_log(msg):
            log_box.insert(tk.END, msg + "\n")
            log_box.see(tk.END)
            win.update_idletasks()

        def _refresh_listbox(*_):
            kw = var_filter.get().strip().lower()
            lst_series.delete(0, tk.END)
            filtered_catalog.clear()
            for item in catalog_data:
                disp = item["display"]
                if not kw or kw in disp.lower() or kw in item["jp_name"].lower():
                    filtered_catalog.append(item)
                    lst_series.insert(tk.END, disp)

        var_filter.trace_add("write", _refresh_listbox)

        def _on_select_series( evt=None):
            sel = lst_series.curselection()
            if not sel:
                return
            idx = sel[0]
            if 0 <= idx < len(filtered_catalog):
                s_item = filtered_catalog[idx]
                var_target.set(f"https://bottleneko.app/ws/series/{s_item['id']}")
                var_offset.set(0)
                lbl_batch_prog.config(text=f"已選擇：{s_item['name']} (準備從第 1 張開始)")

        lst_series.bind("<<ListboxSelect>>", _on_select_series)

        def _fetch_catalog():
            _append_log("🌐 正在連線至 https://api.bottleneko.app/series 取得全部 WS 系列清單...")
            try:
                cats = BottleNekoImporter.fetch_all_series_catalog()
                catalog_data.clear()
                catalog_data.extend(cats)
                _refresh_listbox()
                _append_log(f"✅ 成功載入 {len(cats)} 個 WS 系列！請在上方列表點選或輸入關鍵字篩選。")
            except Exception as e:
                _append_log(f"❌ 載入系列清單失敗：{e}")

        tk.Button(
            top_cat_row,
            text="🔄 連線載入貓罐子全系列清單 (170+系列)",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=12,
            pady=2,
            cursor="hand2",
            command=_fetch_catalog,
        ).pack(side=tk.RIGHT)

        def _run_series_batch(limit_n: int):
            raw_val = var_target.get().strip()
            if not raw_val:
                return
            cur_off = int(var_offset.get() or 0)
            try:
                if "/ws/deck/" in raw_val or raw_val.startswith("{") or raw_val.startswith("["):
                    res = BottleNekoImporter.import_from_url_or_json(raw_val, sets_dir="sets", log_callback=_append_log)
                    self.img_mgr.load_local_images(only_missing=True)
                    self.img_mgr.start_background_download()
                    lbl_batch_prog.config(text=f"已完成牌組匯入 ({res['card_count']} 種)")
                else:
                    res = BottleNekoImporter.import_series_by_id(
                        raw_val,
                        sets_dir="sets",
                        batch_offset=cur_off if limit_n > 0 else 0,
                        batch_limit=limit_n,
                        include_high_rarity=bool(var_inc_high.get()),
                        log_callback=_append_log,
                    )
                    self.img_mgr.load_local_images(only_missing=True)
                    self.img_mgr.start_background_download()
                    if limit_n > 0:
                        next_off = res["next_offset"]
                        tot_av = res["total_available"]
                        if next_off >= tot_av:
                            var_offset.set(0)
                            lbl_batch_prog.config(text=f"🎉 全系列 {tot_av}/{tot_av} 張已全數抓取完畢！")
                            _append_log(f"🎉 恭喜！【{res['deck_name']}】全部 {tot_av} 張卡片已全數匯入完成！")
                        else:
                            var_offset.set(next_off)
                            lbl_batch_prog.config(text=f"進度：{next_off} / {tot_av} 張（再按一次抓下 20 張）")
                    else:
                        lbl_batch_prog.config(text=f"🎉 全系列共 {res['total_in_file']} 張一次匯入完成！")
                if refresh_callback:
                    refresh_callback()
            except Exception as e:
                _append_log(f"❌ 匯入失敗：{e}")

        btn_row = tk.Frame(win, bg="#131926")
        btn_row.pack(fill=tk.X, padx=20, pady=8)

        tk.Button(
            btn_row,
            text="📦 分批抓取 20 張 (自動推進 +20)",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=16,
            pady=6,
            cursor="hand2",
            command=lambda: _run_series_batch(20),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_row,
            text="🚀 一次抓完整個系列 (全部卡片)",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 11, "bold"),
            padx=16,
            pady=6,
            cursor="hand2",
            command=lambda: _run_series_batch(0),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_row,
            text="🛠️ 萬用效果編譯＆除錯器",
            bg="#118ab2",
            fg="#ffffff",
            font=(ff, 11, "bold"),
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.open_effect_debugger_modal,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_row,
            text="關閉視窗",
            bg="#3a3f58",
            fg="white",
            font=(ff, 11, "bold"),
            padx=14,
            pady=6,
            command=win.destroy,
        ).pack(side=tk.RIGHT, padx=5)

    def open_effect_debugger_modal(self):
        ff = self.get_font_family()
        win = tk.Toplevel(self.root)
        win.title("🛠️ 萬用卡片效果編譯與 AST 除錯器 (Universal Effect Compiler & Debugger)")
        win.geometry("860x620")
        win.configure(bg="#131926")
        win.transient(self.root)

        tk.Label(
            win,
            text="🛠️ 萬用中文效果解析器 (ChineseEffectParser) 即時測試＆除錯工具",
            bg="#131926",
            fg="#ffd166",
            font=(ff, 14, "bold"),
        ).pack(pady=(12, 4))

        tk.Label(
            win,
            text="選擇任一張現有卡片，或直接貼上任何 WS 繁體中文效果文，即可檢視系統自動編譯出的 AST 結構（無須手動寫死 if/elif）：",
            bg="#131926",
            fg="#8ecae6",
            font=(ff, 10),
        ).pack(padx=18, pady=(0, 6), anchor="w")

        top_sel = tk.Frame(win, bg="#1b2234", padx=10, pady=8)
        top_sel.pack(fill=tk.X, padx=18, pady=4)

        tk.Label(top_sel, text="快速載入現有卡片測試：", bg="#1b2234", fg="white", font=(ff, 10, "bold")).pack(side=tk.LEFT)
        sample_cids = sorted(list(CARD_DB.keys()))
        var_cid = tk.StringVar(value=sample_cids[0] if sample_cids else "")
        opt = tk.OptionMenu(top_sel, var_cid, *(sample_cids[:80] if sample_cids else [""]))
        opt.config(bg="#2b3348", fg="#ffd166", font=(ff, 10))
        opt.pack(side=tk.LEFT, padx=8)

        panes = tk.Frame(win, bg="#131926")
        panes.pack(fill=tk.BOTH, expand=True, padx=18, pady=6)

        left_f = tk.Frame(panes, bg="#1b2234", padx=8, pady=8)
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(left_f, text="📄 卡片中文效果原文（可自由修改測試）：", bg="#1b2234", fg="#ffd166", font=(ff, 10, "bold")).pack(anchor="w")
        txt_raw = tk.Text(left_f, bg="#0d111a", fg="white", insertbackground="white", font=(ff, 11), wrap=tk.WORD)
        txt_raw.pack(fill=tk.BOTH, expand=True, pady=4)

        right_f = tk.Frame(panes, bg="#1b2234", padx=8, pady=8)
        right_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))
        tk.Label(right_f, text="⚙️ 編譯後的可執行 AST (parsed_abilities JSON)：", bg="#1b2234", fg="#06d6a0", font=(ff, 10, "bold")).pack(anchor="w")
        txt_ast = tk.Text(right_f, bg="#0b0e14", fg="#06d6a0", font=("Consolas", 10), wrap=tk.WORD)
        txt_ast.pack(fill=tk.BOTH, expand=True, pady=4)

        def _compile_now(*_):
            raw_text = txt_raw.get("1.0", tk.END).strip()
            parsed = ChineseEffectParser.parse_card_effects(raw_text, "CHAR")
            txt_ast.delete("1.0", tk.END)
            txt_ast.insert("1.0", json.dumps(parsed, ensure_ascii=False, indent=2))

        def _load_selected_card(*_):
            cid = var_cid.get()
            cinfo = CARD_DB.get(cid, {})
            txt_raw.delete("1.0", tk.END)
            txt_raw.insert("1.0", cinfo.get("text", cinfo.get("effect", "")))
            _compile_now()

        tk.Button(
            top_sel,
            text="載入此卡效果",
            bg="#06d6a0",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=10,
            command=_load_selected_card,
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            top_sel,
            text="⚡ 立即重新編譯 AST",
            bg="#ffd166",
            fg="#000000",
            font=(ff, 10, "bold"),
            padx=12,
            command=_compile_now,
        ).pack(side=tk.RIGHT, padx=4)

        if sample_cids:
            _load_selected_card()

    def show_main_menu(self):
        self.clear_current_frame()
        ff = self.get_font_family()
        menu = tk.Frame(self.root, bg="#0d111a")
        menu.pack(fill=tk.BOTH, expand=True)
        self.current_frame = menu

        self.sound_mgr.play_bgm("bgm_menu")
        # 1. 全畫面背景圖（自動從玩家目前使用的出戰卡組隨機抽取 6 張卡片懸浮於背景）
        bg_img = self.img_mgr.get_wallpaper_visual(
            self.settings.get("theme", "OCEAN"),
            self.settings.get("custom_bg_path", ""),
            int(self.settings.get("bg_dim_percent", 65)),
            1600,
            950,
            floating_cids=self.get_menu_floating_deck_cids(),
        )
        bg_lbl = tk.Label(menu, image=bg_img, bg="#0d111a")
        bg_lbl.image = bg_img
        bg_lbl.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # 2. 頂部玩家個人資訊橫條
        top_hud = tk.Frame(
            menu,
            bg="#131926",
            bd=2,
            relief=tk.RIDGE,
            padx=24,
            pady=10,
            highlightbackground="#2b3856",
            highlightthickness=1,
        )
        top_hud.place(relx=0.5, rely=0.065, anchor="center", width=1120)

        cur_av_id = self.settings.get("avatar", "MAPLE")
        av_img = self.img_mgr.get_avatar_visual(
            cur_av_id,
            size=64,
            border_color="#06d6a0",
            custom_path=self.settings.get("custom_avatar_path", ""),
            is_active_turn=True,
            crop_cfg=self.settings.get("avatar_crop") if cur_av_id == "CARD_CROP" else None,
            preset_crops=self.settings.get("preset_avatar_crops"),
        )
        lbl_av = tk.Label(top_hud, image=av_img, bg="#131926", cursor="hand2")
        lbl_av.image = av_img
        lbl_av.pack(side=tk.LEFT, padx=(4, 16))
        lbl_av.bind("<Button-1>", lambda e: self.open_settings())

        p_info_col = tk.Frame(top_hud, bg="#131926")
        p_info_col.pack(side=tk.LEFT)
        tk.Label(
            p_info_col,
            text=f"玩家：{self.settings.get('player_name', '玩家1')}",
            bg="#131926",
            fg="#ffd166",
            font=(ff, 16, "bold"),
            anchor="w",
        ).pack(fill=tk.X)
        tk.Label(
            p_info_col,
            text=f"目前出戰卡組：{self.get_deck_display_name(self.active_series)}",
            bg="#131926",
            fg="#06d6a0",
            font=(ff, 12, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(2, 0))

        right_status_col = tk.Frame(top_hud, bg="#131926")
        right_status_col.pack(side=tk.RIGHT, padx=6)
        tk.Label(
            right_status_col,
            text=(
                f"已收錄系列：{len(SERIES_DB)} 個 ｜ 總卡池：{len(CARD_DB)} 張 ｜ "
                f"AI 翻牌：{self.settings.get('ai_flip_interval_sec', 2.0):.1f} 秒"
            ),
            bg="#1c2538",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
            padx=14,
            pady=6,
            relief=tk.SOLID,
            bd=1,
        ).pack(side=tk.RIGHT, padx=6)

        # 3. 中央雙欄主大廳面板（移除多餘英文與舊三套宣傳字樣，乾淨高質感設計）
        center_hub = tk.Frame(
            menu,
            bg="#151b29",
            bd=3,
            relief=tk.RIDGE,
            padx=46,
            pady=32,
            highlightbackground="#ffd166",
            highlightthickness=1,
        )
        center_hub.place(relx=0.5, rely=0.535, anchor="center")

        tk.Label(
            center_hub,
            text="◆ WEISS SCHWARZ 卡牌對戰模擬器 ◆",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 22, "bold"),
        ).pack(pady=(0, 18))

        hub_Mid = tk.Frame(center_hub, bg="#151b29")
        hub_Mid.pack(fill=tk.X, pady=4)

        # 左欄：目前出戰卡組王牌卡展示框（僅能從目前出戰卡組的 50 張牌裡面挑選王牌）
        showcase_box = tk.Frame(
            hub_Mid, bg="#1b2336", bd=2, relief=tk.GROOVE, padx=24, pady=18
        )
        showcase_box.pack(side=tk.LEFT, padx=(0, 32), fill=tk.Y)

        tk.Label(
            showcase_box,
            text="★ 出戰卡組王牌 ★",
            bg="#1b2336",
            fg="#ffd166",
            font=(ff, 13, "bold"),
        ).pack(pady=(0, 8))

        ace_cid = self.get_series_ace_card_id(self.active_series)
        ace_img = self.img_mgr.get_card_visual(ace_cid, 162, 226, is_selected=True)
        lbl_ace = tk.Label(
            showcase_box, image=ace_img, bg="#10141f", bd=2, relief=tk.SOLID, cursor="hand2"
        )
        lbl_ace.image = ace_img
        lbl_ace.pack(pady=4)
        lbl_ace.bind("<Button-1>", lambda e: self.open_ace_card_picker_modal(menu))

        ace_name = CARD_DB.get(ace_cid, {}).get("name", ace_cid)
        tk.Label(
            showcase_box,
            text=f"{ace_name}\n【{self.get_deck_display_name(self.active_series)}】",
            bg="#1b2336",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            justify=tk.CENTER,
            wraplength=190,
        ).pack(pady=(6, 6))

        tk.Button(
            showcase_box,
            text="★ 從卡組挑選代表王牌",
            bg="#2b3348",
            fg="#ffd166",
            activebackground="#ffd166",
            activeforeground="#000000",
            font=(ff, 10, "bold"),
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.open_ace_card_picker_modal(menu),
        ).pack(pady=(2, 0))

        # 右欄：五大中文主選單按鈕（移除括號英文與多餘字樣）
        nav_col = tk.Frame(hub_Mid, bg="#151b29")
        nav_col.pack(side=tk.LEFT, fill=tk.Y)

        menu_buttons = [
            ("▶  單 人 對 戰", "選擇預設套牌或你自組的卡組作為 AI 對手進行決鬥", "#06d6a0", "#000000", self.open_ai_deck_select),
            ("◆  雙 人 連 線", "建立房間或跨網連線與真人玩家進行決鬥", "#f4a261", "#000000", self.open_lan_lobby),
            ("■  設 定 我 的 卡 組", "自由組建並保存多套卡組・切換系列卡池與高低版本", "#118ab2", "#ffffff", self.open_deck_builder),
            ("🌐  貓罐子系列 ＆ 牌組匯入", "免組牌直接抓取貓罐子系列卡池・每次 20 張分批匯入", "#9b5de5", "#ffffff", lambda: self.open_bottleneko_importer_modal(refresh_callback=self.show_main_menu)),
            ("★  遊 戲 設 定", "調整音樂與個別音效音量・更換卡套・玩家頭像與背景", "#ffd166", "#000000", self.open_settings),
        ]

        for main_txt, sub_txt, b_bg, b_fg, cmd_fn in menu_buttons:
            btn_wrap = tk.Frame(nav_col, bg="#2b3348", padx=2, pady=2)
            btn_wrap.pack(fill=tk.X, pady=5)
            b = tk.Button(
                btn_wrap,
                text=f"{main_txt}\n{sub_txt}",
                bg=b_bg,
                fg=b_fg,
                activebackground="#ffffff",
                activeforeground="#000000",
                font=(ff, 12, "bold"),
                width=40,
                pady=7,
                bd=0,
                cursor="hand2",
                command=cmd_fn,
            )
            b.pack(fill=tk.X)

        bottom_bar = tk.Frame(center_hub, bg="#151b29")
        bottom_bar.pack(fill=tk.X, pady=(16, 0))

        self.lbl_webp_status = tk.Label(
            bottom_bar,
            text="卡圖資料夾：./ws_card_images/ （支援背景自動下載高清卡圖）",
            bg="#1b2234",
            fg="#adb5bd",
            font=(ff, 10),
            padx=14,
            pady=6,
            relief=tk.SOLID,
            bd=1,
        )
        self.lbl_webp_status.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Button(
            bottom_bar,
            text="↻ 重新掃描卡圖",
            bg="#2b3348",
            fg="#ffd166",
            font=(ff, 10, "bold"),
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.reload_webp_folder,
        ).pack(side=tk.RIGHT)

    def open_settings(self):
        self.clear_current_frame()
        self.img_mgr.load_local_images(only_missing=True)
        sf = SettingsFrame(self.root, self)
        sf.pack(fill=tk.BOTH, expand=True)
        self.current_frame = sf

    def open_ace_card_picker_modal(self, parent_frame):
        """於主選單彈出『從目前出戰卡組挑選王牌代表卡』視窗，只列出該卡組內已入編的卡片"""
        modal = tk.Frame(parent_frame, bg="#151b29", bd=3, relief=tk.RIDGE, padx=22, pady=18)
        modal.place(relx=0.5, rely=0.5, anchor="center", width=860, height=560)
        modal.lift()

        ff = self.get_font_family()
        top_r = tk.Frame(modal, bg="#151b29")
        top_r.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            top_r,
            text=f"★ 從【{self.get_deck_display_name(self.active_series)}】挑選代表王牌卡 ★",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 15, "bold"),
        ).pack(side=tk.LEFT)

        tk.Button(
            top_r,
            text="✖ 關閉",
            bg="#e63946",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            command=modal.destroy,
        ).pack(side=tk.RIGHT)

        tk.Label(
            modal,
            text="點擊下方卡組內的任一張卡片，即可將其設為這副卡組的『出戰王牌』並展示於主選單：",
            bg="#151b29",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        canvas = tk.Canvas(modal, bg="#10141f", highlightthickness=0)
        sc = tk.Scrollbar(modal, orient=tk.VERTICAL, command=canvas.yview)
        inner = tk.Frame(canvas, bg="#10141f")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sc.set)
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        recipe = self.get_series_deck(self.active_series)
        deck_cids = [cid for cid, cnt in recipe.items() if cnt > 0 and cid in CARD_DB]
        if not deck_cids:
            deck_cids = list(CARD_DB.keys())[:20]
        deck_cids.sort(key=lambda k: (-CARD_DB[k].get("level", 0), -CARD_DB[k].get("power", 0)))
        cur_ace = self.get_series_ace_card_id(self.active_series)

        def pick_ace(chosen_cid: str):
            self.set_user_ace_card_id(chosen_cid, self.active_series)
            modal.destroy()
            self.show_main_menu()

        cols = 5
        for idx, cid in enumerate(deck_cids):
            r, c = divmod(idx, cols)
            cdata = CARD_DB[cid]
            is_cur = cid == cur_ace
            box = tk.Frame(
                inner,
                bg="#f4a261" if is_cur else "#23293d",
                bd=2,
                relief=tk.RAISED,
                padx=6,
                pady=6,
            )
            box.grid(row=r, column=c, padx=7, pady=7)
            c_img = self.img_mgr.get_card_visual(cid, 105, 146, is_selected=is_cur)
            b = tk.Button(
                box,
                image=c_img,
                text=f"{cdata['name'][:8]}\nLv.{cdata['level']} ({get_card_type_zh(cdata['type'])})",
                compound=tk.TOP,
                bg="#f4a261" if is_cur else "#1b2030",
                fg="#000000" if is_cur else "#ffffff",
                font=(ff, 9, "bold"),
                width=116,
                height=184,
                cursor="hand2",
                command=lambda k=cid: pick_ace(k),
            )
            b.image = c_img
            b.pack()

    def open_ai_deck_select(self):
        """單人決鬥出戰與 AI 對手選擇畫面：移除胡亂編排的匯入系列自動套牌，固定顯示內建三套預設套牌＋玩家自己組建保存的多套卡組！"""
        self.clear_current_frame()
        ff = self.get_font_family()
        sel_frame = tk.Frame(self.root, bg="#0d111a")
        sel_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = sel_frame

        bg_img = self.img_mgr.get_wallpaper_visual(
            self.settings.get("theme", "OCEAN"),
            self.settings.get("custom_bg_path", ""),
            int(self.settings.get("bg_dim_percent", 65)),
            1600,
            950,
            floating_cids=self.get_menu_floating_deck_cids(),
        )
        bg_lbl = tk.Label(sel_frame, image=bg_img, bg="#0d111a")
        bg_lbl.image = bg_img
        bg_lbl.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        box = tk.Frame(
            sel_frame,
            bg="#151b29",
            bd=3,
            relief=tk.RIDGE,
            padx=42,
            pady=26,
            highlightbackground="#ffd166",
            highlightthickness=1,
        )
        box.place(relx=0.5, rely=0.5, anchor="center", width=780)

        tk.Label(
            box,
            text="◆ 單人對戰 — 選擇我方出戰卡組與 AI 對手 ◆",
            bg="#151b29",
            fg="#ffd166",
            font=(ff, 19, "bold"),
        ).pack(pady=(0, 12))

        # 建立可用卡組清單（僅包含內建三套真實構築套牌 ＋ 玩家已保存的 50 張自訂卡組）
        deck_options = [
            ("預設套牌 1：防盾系列 (BFR/S78)", "BFR/S78"),
            ("預設套牌 2：GA文庫 8箭地旅 (GA/S131)", "GA/S131"),
            ("預設套牌 3：孤獨搖滾！ (BTR/W107)", "BTR/W107"),
        ]
        existing_keys = {k for _, k in deck_options}
        user_names = self.settings.get("user_deck_names") or {}
        for k, rec in self.decks_book.items():
            if k.startswith("_") or k in existing_keys:
                continue
            if self._is_valid_recipe(rec):
                disp = user_names.get(k) or self.get_deck_display_name(k)
                deck_options.append((f"自訂卡組：{disp}", k))
                existing_keys.add(k)

        # 上方：可直接切換「我方出戰卡組」與「指定自訂卡組給 AI 對手使用」
        custom_duel_bar = tk.Frame(box, bg="#1c2436", padx=16, pady=12, relief=tk.SOLID, bd=1)
        custom_duel_bar.pack(fill=tk.X, pady=(0, 14))

        row_my = tk.Frame(custom_duel_bar, bg="#1c2436")
        row_my.pack(fill=tk.X, pady=3)
        tk.Label(
            row_my,
            text="⚔️ 我方出戰卡組：",
            bg="#1c2436",
            fg="#06d6a0",
            font=(ff, 11, "bold"),
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        my_deck_var = tk.StringVar()
        opt_labels = [lbl for lbl, _ in deck_options]
        my_idx = 0
        for idx_d, (_, k) in enumerate(deck_options):
            if k == self.active_series:
                my_idx = idx_d
                break
        if opt_labels:
            my_deck_var.set(opt_labels[my_idx])

        cmb_my = ttk.Combobox(
            row_my,
            textvariable=my_deck_var,
            values=opt_labels,
            state="readonly",
            width=36,
            font=(ff, 11, "bold"),
        )
        cmb_my.pack(side=tk.LEFT, padx=6)

        def _on_change_my_deck(event=None):
            sel_l = my_deck_var.get()
            for l, k in deck_options:
                if l == sel_l:
                    self.set_active_series(k)
                    break

        cmb_my.bind("<<ComboboxSelected>>", _on_change_my_deck)

        row_ai_custom = tk.Frame(custom_duel_bar, bg="#1c2436")
        row_ai_custom.pack(fill=tk.X, pady=(6, 3))
        tk.Label(
            row_ai_custom,
            text="🤖 指定 AI 使用卡組：",
            bg="#1c2436",
            fg="#ffd166",
            font=(ff, 11, "bold"),
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        ai_deck_var = tk.StringVar()
        ai_idx = 0
        for idx_d, (_, k) in enumerate(deck_options):
            if k == self.ai_series:
                ai_idx = idx_d
                break
        if opt_labels:
            ai_deck_var.set(opt_labels[ai_idx])

        cmb_ai = ttk.Combobox(
            row_ai_custom,
            textvariable=ai_deck_var,
            values=opt_labels,
            state="readonly",
            width=36,
            font=(ff, 11, "bold"),
        )
        cmb_ai.pack(side=tk.LEFT, padx=6)

        def _start_with_selected_ai_dropdown():
            _on_change_my_deck()
            sel_ai_l = ai_deck_var.get()
            chosen_ai_k = "BFR/S78"
            for l, k in deck_options:
                if l == sel_ai_l:
                    chosen_ai_k = k
                    break
            self._launch_single_with_ai(chosen_ai_k)

        tk.Button(
            row_ai_custom,
            text="▶ 與此卡組開戰",
            bg="#9b5de5",
            fg="#ffffff",
            font=(ff, 10, "bold"),
            padx=12,
            pady=3,
            cursor="hand2",
            command=_start_with_selected_ai_dropdown,
        ).pack(side=tk.LEFT, padx=6)

        # 下方：快速點選三大預設 AI 對手、隨機對手或鏡像對決（固定 5 個按鈕，絕不向下無限延伸！）
        tk.Label(
            box,
            text="或直接點選下方代表對手立即開戰：",
            bg="#151b29",
            fg="#8ecae6",
            font=(ff, 10, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        ai_choices = [
            ("MAPLE", "【防盾系列 BFR/S78】梅普露＆莎莉＆蜜伊", "BFR/S78", "#c92a3e", "#ffffff"),
            ("MAHIRU", "【GA文庫 8箭地旅 GA/S131】小真晝＆伊蕾娜＆琉", "GA/S131", "#e09f3e", "#000000"),
            ("KITA", "【孤獨搖滾！ 8電源 BTR/W107】喜多郁代＆後藤一里", "BTR/W107", "#e56b8f", "#000000"),
            ("ELAINA", "【隨機抽選對手】從三大預設套牌與自訂卡組隨機抽選 AI", "RANDOM", "#06d6a0", "#000000"),
            ("SALLY", "【鏡像對決模式】讓 AI 使用與我方出戰卡組相同的配比", "MIRROR", "#118ab2", "#ffffff"),
        ]

        for av_key, label_txt, scode_val, bg_col, fg_col in ai_choices:
            row_f = tk.Frame(box, bg="#252c42", bd=2, relief=tk.RAISED, padx=6, pady=3)
            row_f.pack(fill=tk.X, pady=4)

            av_im = self.img_mgr.get_avatar_visual(
                av_key,
                size=46,
                border_color="#ffd166",
                preset_crops=self.settings.get("preset_avatar_crops"),
            )
            lbl_i = tk.Label(row_f, image=av_im, bg="#252c42")
            lbl_i.image = av_im
            lbl_i.pack(side=tk.LEFT, padx=(4, 10))

            tk.Button(
                row_f,
                text=label_txt,
                bg=bg_col,
                fg=fg_col,
                activebackground="#ffffff",
                activeforeground="#000000",
                font=(ff, 12, "bold"),
                width=48,
                pady=6,
                bd=0,
                cursor="hand2",
                command=lambda s=scode_val: (
                    _on_change_my_deck(),
                    self._launch_single_with_ai(self.active_series if s == "MIRROR" else s),
                ),
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            box,
            text="◀ 返回主選單",
            bg="#2b3348",
            fg="#ffffff",
            font=(ff, 12, "bold"),
            padx=24,
            pady=6,
            cursor="hand2",
            command=self.show_main_menu,
        ).pack(pady=(12, 0))

    def _launch_single_with_ai(self, chosen_ai_code: str):
        if chosen_ai_code == "RANDOM":
            pool = [k for k in ["BFR/S78", "GA/S131", "BTR/W107"] if k in SERIES_DB]
            for k, rec in self.decks_book.items():
                if not k.startswith("_") and k not in pool and self._is_valid_recipe(rec):
                    pool.append(k)
            chosen_ai_code = random.choice(pool) if pool else "BFR/S78"
        self.set_ai_series(chosen_ai_code)
        self.start_single_player()

    def reload_webp_folder(self):
        cnt = self.img_mgr.load_local_images()
        self.img_mgr.start_background_download()
        self.lbl_webp_status.config(
            text=f"✔ 已載入 {cnt} 張本地卡圖，並於背景同步檢查 WS 官網卡圖！",
            fg="#06d6a0",
        )

    def start_single_player(self):
        self.clear_current_frame()
        self.img_mgr.load_local_images()
        game_frame = WSBofuriGameFrame(self.root, self, net_node=None)
        game_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = game_frame
        self.img_mgr.callbacks.append(game_frame.update_ui)

    def open_lan_lobby(self):
        self.clear_current_frame()
        lobby = LANLobbyFrame(self.root, self)
        lobby.pack(fill=tk.BOTH, expand=True)
        self.current_frame = lobby

    def start_lan_game(self, net_node):
        self.clear_current_frame()
        self.img_mgr.load_local_images()
        game_frame = WSBofuriGameFrame(self.root, self, net_node=net_node)
        game_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = game_frame
        self.img_mgr.callbacks.append(game_frame.update_ui)

    def open_deck_builder(self):
        self.clear_current_frame()
        self.img_mgr.load_local_images(only_missing=True)
        builder = DeckBuilderFrame(self.root, self)
        builder.pack(fill=tk.BOTH, expand=True)
        self.current_frame = builder
        self.img_mgr.callbacks.append(builder.populate_cards)


def launch_game():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_game()
