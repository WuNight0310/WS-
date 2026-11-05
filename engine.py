import glob
import json
import os
import random
import sys

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


FALLBACK_CARD_DB = {'BFR/S78-076': {'id': 'BFR/S78-076', 'name': '公會長之間的對決', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 2, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-076', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-076R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076.png', 'https://img.bottleneko.app/BFR_S78_076.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076.png']}, 'BFR/S78-076R': {'id': 'BFR/S78-076R', 'name': '公會長之間的對決', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-076', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-076R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_076R.png', 'https://img.bottleneko.app/BFR_S78_076R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_076R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_076r.gif']}, 'BFR/S78-077': {'id': 'BFR/S78-077', 'name': 'Boss級怪物', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'DOOR', 'traits': [], 'default_count': 2, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n木門：當你判定出此卡時，你可以選擇自己休息室的角色1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-077', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-077R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077.png', 'https://img.bottleneko.app/BFR_S78_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077.png']}, 'BFR/S78-077R': {'id': 'BFR/S78-077R', 'name': 'Boss級怪物', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'DOOR', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n木門：當你判定出此卡時，你可以選擇自己休息室的角色1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-077', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-077R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_077R.png', 'https://img.bottleneko.app/BFR_S78_077R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_077R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_077r.gif']}, 'BFR/S78-078': {'id': 'BFR/S78-078', 'name': '炎帝之國的公會長', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 2, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-078', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-078R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078.png', 'https://img.bottleneko.app/BFR_S78_078.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078.png']}, 'BFR/S78-078R': {'id': 'BFR/S78-078R', 'name': '炎帝之國的公會長', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你從自己的休息室選擇自己等級+1的等級的角色1張，【橫置】放置到任意的格子。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-078', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-078R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_078R.png', 'https://img.bottleneko.app/BFR_S78_078R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_078R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_078r.gif']}, 'BFR/S78-107': {'id': 'BFR/S78-107', 'name': '展開．左手', 'type': 'CX', 'color': '藍', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'GATE', 'traits': [], 'default_count': 2, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n城門：當你判定出此卡時，你可以選擇自己休息室的1張名場面，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-107', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BFR/S78-107R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107.png', 'https://img.bottleneko.app/BFR_S78_107.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107.png']}, 'BFR/S78-107R': {'id': 'BFR/S78-107R', 'name': '展開．左手', 'type': 'CX', 'color': '藍', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'GATE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n城門：當你判定出此卡時，你可以選擇自己休息室的1張名場面，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-107', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BFR/S78-107R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_107R.png', 'https://img.bottleneko.app/BFR_S78_107R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_107R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_107r.gif']}, 'BFR/S78-075': {'id': 'BFR/S78-075', 'name': '獨有系列', 'type': 'EVENT', 'color': '紅', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 2, 'effects': ['EVENT_COUNTER_2500_MEMORY', 'MEMORY_MAIN_START_RETURN'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_075.png', 'text': '【反擊】你選擇自己的《遊戲》的角色1張，在那個回合中，攻擊力+2500。將此卡放到回憶區。\n【自】記憶 ［手牌的《遊戲》的角色1張放到休息室］ 在你的主要階段開始時，回憶區有此卡存在的話，你可以支付代價。支付代價的話，將此卡返回手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-075', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_075.png', 'https://img.bottleneko.app/BFR_S78_075.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_075.png']}, 'BFR/S78-015': {'id': 'BFR/S78-015', 'name': '雙胞胎的妹妹 結衣', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 3000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '雙胞胎'], 'default_count': 2, 'effects': ['CONT_CANNOT_SIDE_ATTACK', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_015.png', 'text': '【永】此卡不能側打。\n【自】［(1) 手牌1張名場面放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-015', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_015.png', 'https://img.bottleneko.app/BFR_S78_015.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_015.png']}, 'BFR/S78-001': {'id': 'BFR/S78-001', 'name': '戰鬥的工匠 伊茲', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '鍛造'], 'default_count': 3, 'effects': ['AUTO_ON_PLAY_CLOCK_SEARCH_LV1', 'AUTO_OTHER_REVERSE_BUFF_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇等級1以下的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。\n【自】其他的你的角色的戰鬥對手【倒置】時，在那個回合中，此卡的攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-001', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-001SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001.png', 'https://img.bottleneko.app/BFR_S78_001.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001.png']}, 'BFR/S78-001SP': {'id': 'BFR/S78-001SP', 'name': '戰鬥的工匠 伊茲', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '鍛造'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_CLOCK_SEARCH_LV1', 'AUTO_OTHER_REVERSE_BUFF_1000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001SP.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇等級1以下的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。\n【自】其他的你的角色的戰鬥對手【倒置】時，在那個回合中，此卡的攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-001', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-001SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001SP.png', 'https://img.bottleneko.app/BFR_S78_001SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_001SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_001S.png', 'https://img.bottleneko.app/BFR_S78_001S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_001S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_001s.gif']}, 'BFR/S78-031': {'id': 'BFR/S78-031', 'name': '多彩多樣 莎莉', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 3, 'effects': ['CONT_IGNORE_CX_COLOR', 'AUTO_ON_CX_LOOT', 'ACT_CONCENTRATE_SINGLE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031.png', 'text': '【永】你的名場面可以無需滿足顏色條件從手牌使用。\n【自】［手牌1張放到休息室］ 當你的名場面被放置到名場面區時，你可以支付代價。支付代價的話，你抽1張牌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻4張，放到休息室。那些卡片中每有1張名場面，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-031', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-031SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031.png', 'https://img.bottleneko.app/BFR_S78_031.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031.png']}, 'BFR/S78-031SP': {'id': 'BFR/S78-031SP', 'name': '多彩多樣 莎莉', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 0, 'effects': ['CONT_IGNORE_CX_COLOR', 'AUTO_ON_CX_LOOT', 'ACT_CONCENTRATE_SINGLE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031SP.png', 'text': '【永】你的名場面可以無需滿足顏色條件從手牌使用。\n【自】［手牌1張放到休息室］ 當你的名場面被放置到名場面區時，你可以支付代價。支付代價的話，你抽1張牌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻4張，放到休息室。那些卡片中每有1張名場面，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-031', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-031SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031SP.png', 'https://img.bottleneko.app/BFR_S78_031SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_031SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_031S.png', 'https://img.bottleneko.app/BFR_S78_031S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_031S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_031s.gif']}, 'BFR/S78-062': {'id': 'BFR/S78-062', 'name': '咬咬 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 3, 'effects': ['AUTO_STAGE_TO_WR_LOOK4_STEPWISE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062.png', 'text': '【自】［手牌1張放到休息室］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-062', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-062S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062.png', 'https://img.bottleneko.app/BFR_S78_062.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062.png']}, 'BFR/S78-062S': {'id': 'BFR/S78-062S', 'name': '咬咬 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_STAGE_TO_WR_LOOK4_STEPWISE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062S.png', 'text': '【自】［手牌1張放到休息室］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-062', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-062S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_062S.png', 'https://img.bottleneko.app/BFR_S78_062S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_062S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_062s.gif']}, 'BFR/S78-061': {'id': 'BFR/S78-061', 'name': '作戰變更 米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['ACT_MARKER_OR_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_061.png', 'text': '【起】［將此卡【橫置】］ 此卡下方沒有標記的話，你將自己的牌組上方1張公開。那張卡片的等級是1以上的話作為標記以裏側表示放到此卡下方。名場面的等級視為0。如果不是的話放回原位。\n【起】［將此卡【橫置】］ 你將此卡下方的標記1張放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-061', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_061.png', 'https://img.bottleneko.app/BFR_S78_061.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_061.png']}, 'BFR/S78-060': {'id': 'BFR/S78-060', 'name': '焰火飛馳 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 3, 'effects': ['AUTO_ON_PLAY_DEBUFF_AND_SEARCH'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手前列的角色1張，在那個回合中，攻擊力-1000。\n【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-060', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-060S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060.png', 'https://img.bottleneko.app/BFR_S78_060.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060.png']}, 'BFR/S78-060S': {'id': 'BFR/S78-060S', 'name': '焰火飛馳 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DEBUFF_AND_SEARCH'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060S.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手前列的角色1張，在那個回合中，攻擊力-1000。\n【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你從自己的牌組選擇《遊戲》的角色最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-060', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-060S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_060S.png', 'https://img.bottleneko.app/BFR_S78_060S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_060S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_060s.gif']}, 'BFR/S78-083': {'id': 'BFR/S78-083', 'name': '情報戰 莎莉', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '水'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_SCRY2_AND_GUESS_DRAW'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_083.png', 'text': '【自】此卡從手牌被放置到舞台時，你看自己的牌組上方最多2張，以任意順序放回牌組上方。\n【自】此卡從手牌被放置到舞台時，對手宣言0或1或2或3。你將自己的牌組上方1張，放到休息室，那張卡片是對手宣言的等級的卡片的話，你抽最多X張牌。X等於對手宣言的數字+1。名場面的等級視為0。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-083', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_083.png', 'https://img.bottleneko.app/BFR_S78_083.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_083.png']}, 'BFR/S78-073': {'id': 'BFR/S78-073', 'name': '不屈的守護者 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 3, 'effects': ['CONT_OTHER_2GAME_BUFF_2000', 'AUTO_HAND_ENCORE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_073.png', 'text': '【永】其他的你的《遊戲》的角色存在2張以上的話，此卡的攻擊力+2000。\n【自】安可 ［手牌的角色1張放到休息室］', 'series': 'BFR/S78', 'base_id': 'BFR/S78-073', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_073.png', 'https://img.bottleneko.app/BFR_S78_073.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_073.png']}, 'BFR/S78-057': {'id': 'BFR/S78-057', 'name': '移動要塞 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 4, 'effects': ['AUTO_ON_PLAY_BUFF_1500', 'CX_COMBO_ATK_START_STAND_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】【CX連動】 ［手牌的「移動要塞 梅普露」1張放到休息室，你的名場面區的「公會長之間的對決」1張放到休息室］ 在你的攻擊階段開始時，此卡存在於前列的話，你可以支付代價。支付代價的話，你選擇其他的自己的《遊戲》的角色最多1張，【正置】，選擇自己休息室的《遊戲》的角色最多1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-057', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-057SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057.png', 'https://img.bottleneko.app/BFR_S78_057.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057.png']}, 'BFR/S78-057SP': {'id': 'BFR/S78-057SP', 'name': '移動要塞 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_BUFF_1500', 'CX_COMBO_ATK_START_STAND_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057SP.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】【CX連動】 ［手牌的「移動要塞 梅普露」1張放到休息室，你的名場面區的「公會長之間的對決」1張放到休息室］ 在你的攻擊階段開始時，此卡存在於前列的話，你可以支付代價。支付代價的話，你選擇其他的自己的《遊戲》的角色最多1張，【正置】，選擇自己休息室的《遊戲》的角色最多1張，回到手牌。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-057', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-057SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057SP.png', 'https://img.bottleneko.app/BFR_S78_057SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_057SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_057S.png', 'https://img.bottleneko.app/BFR_S78_057S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_057S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_057s.gif']}, 'BFR/S78-102': {'id': 'BFR/S78-102', 'name': '通往勝利的方程式 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 1, 'cost': 1, 'power': 3000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['CONT_LEVEL_ASSIST', 'AUTO_ON_ACT_BUFF_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_102.png', 'text': '【永】應援 此卡前面的你的《遊戲》的角色全部，攻擊力+X。X等於那張角色的等級×500。\n【自】此能力每1回合最多發動1次。當你使用【起】的時候，你選擇自己的角色1張，在那個回合中，攻擊力+1000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-102', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_102.png', 'https://img.bottleneko.app/BFR_S78_102.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_102.png']}, 'BFR/S78-087': {'id': 'BFR/S78-087', 'name': '盾與盾 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_FORCE_OPP_SWAP'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_087.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇對手的等級1以上的角色1張，對手選擇自己休息室的等級X以下的角色1張，交換位置。X等於你選擇的角色的等級-1。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-087', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_087.png', 'https://img.bottleneko.app/BFR_S78_087.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_087.png']}, 'BFR/S78-072': {'id': 'BFR/S78-072', 'name': '火炎牢 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 4500, 'soul': 1, 'trigger': 'NONE', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_SCALING_BUFF_AND_LOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_072.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於你的《遊戲》的角色張數×500。\n【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，在那個回合中，給予以下能力。『【永】此卡不能回到手牌，不能放到回憶區。』', 'series': 'BFR/S78', 'base_id': 'BFR/S78-072', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_072.png', 'https://img.bottleneko.app/BFR_S78_072.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_072.png']}, 'BFR/S78-058': {'id': 'BFR/S78-058', 'name': '聖女米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 1, 'effects': ['CONT_ALL_GAME_BUFF_3000', 'AUTO_DIRECT_ATK_STOCK_CHARGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058.png', 'text': '【永】你的角色全部都是《遊戲》的話，此卡的攻擊力+3000。\n【自】此卡直接攻擊時，你可以選擇自己休息室的《遊戲》的角色1張，放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-058', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-058S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058.png', 'https://img.bottleneko.app/BFR_S78_058.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058.png']}, 'BFR/S78-058S': {'id': 'BFR/S78-058S', 'name': '聖女米瑟莉', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['CONT_ALL_GAME_BUFF_3000', 'AUTO_DIRECT_ATK_STOCK_CHARGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058SP.png', 'text': '【永】你的角色全部都是《遊戲》的話，此卡的攻擊力+3000。\n【自】此卡直接攻擊時，你可以選擇自己休息室的《遊戲》的角色1張，放到能量區。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-058', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-058S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058SP.png', 'https://img.bottleneko.app/BFR_S78_058SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_058SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_058S.png', 'https://img.bottleneko.app/BFR_S78_058S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_058S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_058s.gif']}, 'BFR/S78-069': {'id': 'BFR/S78-069', 'name': '被託付的生命 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 1, 'effects': ['AUTO_FRONT_ATK_LOWER_LEVEL', 'AUTO_REVERSE_BOMB_LV2'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_069.png', 'text': '【自】［(1)］ 此卡正打時，你可以支付代價。支付代價的話，你選擇對手的角色1張，在那個回合中，等級-1。\n【自】此卡【倒置】時，此卡的戰鬥對手是等級2以下的話，你可以將那張角色【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-069', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': None, 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_069.png', 'https://img.bottleneko.app/BFR_S78_069.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_069.png']}, 'BFR/S78-089': {'id': 'BFR/S78-089', 'name': '大摯友 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 1, 'effects': ['CONT_OPP_BACKROW_BUFF_1500', 'AUTO_DEFEND_IMMUNE_REVERSE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089.png', 'text': '【永】對手的後列的角色每有1張，此卡的攻擊力+1500。\n【自】［(1) 手牌的《遊戲》的角色1張放到休息室］ 此卡被正打時，你可以支付代價。支付代價的話，在那個回合中，此卡不會【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-089', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-089S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089.png', 'https://img.bottleneko.app/BFR_S78_089.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089.png']}, 'BFR/S78-089S': {'id': 'BFR/S78-089S', 'name': '大摯友 梅普露＆莎莉', 'type': 'CHAR', 'color': '藍', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['CONT_OPP_BACKROW_BUFF_1500', 'AUTO_DEFEND_IMMUNE_REVERSE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089S.png', 'text': '【永】對手的後列的角色每有1張，此卡的攻擊力+1500。\n【自】［(1) 手牌的《遊戲》的角色1張放到休息室］ 此卡被正打時，你可以支付代價。支付代價的話，在那個回合中，此卡不會【倒置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-089', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-089S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_089S.png', 'https://img.bottleneko.app/BFR_S78_089S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_089S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_089s.gif']}, 'BFR/S78-063': {'id': 'BFR/S78-063', 'name': '暴虐 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_3000_AND_SALVAGE_CX', 'CX_COMBO_REVERSE_BURN_1_2_3'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。\n【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。\n【自】【CX連動】 ［(6) 手牌2張放到休息室，你的名場面區的「Boss級怪物」1張放到休息室］ 此卡的戰鬥對手【倒置】時，你可以支付代價。支付代價的話，給對手1點傷害，給對手2點傷害，給對手3點傷害。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-063', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-063S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063.png', 'https://img.bottleneko.app/BFR_S78_063.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063.png']}, 'BFR/S78-063S': {'id': 'BFR/S78-063S', 'name': '暴虐 梅普露', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_3000_AND_SALVAGE_CX', 'CX_COMBO_REVERSE_BURN_1_2_3'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063S.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。\n【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的名場面1張，回到手牌。\n【自】【CX連動】 ［(6) 手牌2張放到休息室，你的名場面區的「Boss級怪物」1張放到休息室］ 此卡的戰鬥對手【倒置】時，你可以支付代價。支付代價的話，給對手1點傷害，給對手2點傷害，給對手3點傷害。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-063', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-063S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063S.png', 'https://img.bottleneko.app/BFR_S78_063S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063SEC.png', 'https://img.bottleneko.app/BFR_S78_063SEC.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063SEC.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sec.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sec.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_063SP.png', 'https://img.bottleneko.app/BFR_S78_063SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_063SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_063sp.gif']}, 'BFR/S78-064': {'id': 'BFR/S78-064', 'name': '炎帝 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_HEAL', 'CX_COMBO_STANDBY_STAND'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064.png', 'text': '【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】【CX連動】 ［手牌的《遊戲》的角色3張放到休息室］ 此卡因為「炎帝之國的公會長」的效果被放到舞台時，你可以支付代價。支付代價的話，將此卡【正置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-064', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-064S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064.png', 'https://img.bottleneko.app/BFR_S78_064.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064.png']}, 'BFR/S78-064S': {'id': 'BFR/S78-064S', 'name': '炎帝 蜜伊', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '炎'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_HEAL', 'CX_COMBO_STANDBY_STAND'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064S.png', 'text': '【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】【CX連動】 ［手牌的《遊戲》的角色3張放到休息室］ 此卡因為「炎帝之國的公會長」的效果被放到舞台時，你可以支付代價。支付代價的話，將此卡【正置】。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-064', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BFR/S78-064S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064S.png', 'https://img.bottleneko.app/BFR_S78_064S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_064S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_064SP.png', 'https://img.bottleneko.app/BFR_S78_064SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_064SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_064sp.gif']}, 'BFR/S78-081': {'id': 'BFR/S78-081', 'name': '天才少年 奏', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '武器'], 'default_count': 1, 'effects': ['CONT_EARLY_PLAY_4GAME', 'AUTO_ON_PLAY_HEAL', 'AUTO_ON_PLAY_OTHER_GAME_2000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081.png', 'text': '【永】你的《遊戲》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，有其他的你的《遊戲》的角色存在的話，在那個回合中，此卡的攻擊力+2000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-081', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-081SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081.png', 'https://img.bottleneko.app/BFR_S78_081.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081.png']}, 'BFR/S78-081SP': {'id': 'BFR/S78-081SP', 'name': '天才少年 奏', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '武器'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4GAME', 'AUTO_ON_PLAY_HEAL', 'AUTO_ON_PLAY_OTHER_GAME_2000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081SP.png', 'text': '【永】你的《遊戲》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，你可以將自己的傷害區上方1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，有其他的你的《遊戲》的角色存在的話，在那個回合中，此卡的攻擊力+2000。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-081', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-081SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081SP.png', 'https://img.bottleneko.app/BFR_S78_081SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_081SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_081S.png', 'https://img.bottleneko.app/BFR_S78_081S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_081S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_081s.gif']}, 'BFR/S78-082': {'id': 'BFR/S78-082', 'name': '機械神 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_RESHUFFLE_OPP_STOCK', 'CX_COMBO_ATK_BOTTOM_MILL4_BURN'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082.png', 'text': '【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手將自己的能量區全部，放到休息室，從自己的牌組上方將相同張數放到能量區。\n【自】【CX連動】 此卡攻擊時，名場面區有「展開．左手」的話，你將對手的牌組下方4張，放到休息室，給對手X點傷害。X等於那些卡片中的名場面張數。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-082', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BFR/S78-082SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082.png', 'https://img.bottleneko.app/BFR_S78_082.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082.png']}, 'BFR/S78-082SP': {'id': 'BFR/S78-082SP', 'name': '機械神 梅普露', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['遊戲', '盾'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_RESHUFFLE_OPP_STOCK', 'CX_COMBO_ATK_BOTTOM_MILL4_BURN'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082SP.png', 'text': '【自】［(1)］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手將自己的能量區全部，放到休息室，從自己的牌組上方將相同張數放到能量區。\n【自】【CX連動】 此卡攻擊時，名場面區有「展開．左手」的話，你將對手的牌組下方4張，放到休息室，給對手X點傷害。X等於那些卡片中的名場面張數。會發生傷害取消。', 'series': 'BFR/S78', 'base_id': 'BFR/S78-082', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BFR/S78-082SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082SP.png', 'https://img.bottleneko.app/BFR_S78_082SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_082SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BFR_S78_082S.png', 'https://img.bottleneko.app/BFR_S78_082S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BFR_S78_082S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/bfr_s78/bfr_s78_082s.gif']}, 'GA10/S131-030': {'id': 'GA10/S131-030', 'series': 'GA/S131', 'name': '時隔五年的【能力值】更新', 'jp_name': '五年振りの【ステイタス】更新', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 4, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA10/S131-030', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'GA10/S131-030R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030.png', 'https://img.bottleneko.app/GA10_S131_030.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030.png']}, 'GA10/S131-030R': {'id': 'GA10/S131-030R', 'series': 'GA/S131', 'name': '時隔五年的【能力值】更新', 'jp_name': '五年振りの【ステイタス】更新', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA10/S131-030', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'GA10/S131-030R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_030R.png', 'https://img.bottleneko.app/GA10_S131_030R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_030R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_030r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_030r.gif']}, 'GA17/S131-033': {'id': 'GA17/S131-033', 'series': 'GA/S131', 'name': '灰之魔女', 'jp_name': '灰の魔女', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 4, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA17/S131-033', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'GA17/S131-033R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033.png', 'https://img.bottleneko.app/GA17_S131_033.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033.png']}, 'GA17/S131-033R': {'id': 'GA17/S131-033R', 'series': 'GA/S131', 'name': '灰之魔女', 'jp_name': '灰の魔女', 'type': 'CX', 'color': '黃', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'CHOICE', 'traits': [], 'default_count': 0, 'effects': ['CX_ALL_1000_1SOUL', 'CX_TRIGGER_CHOICE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033R.png', 'text': '【永】你的角色全部，攻擊力+1000，魂傷+1。\n箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。', 'base_id': 'GA17/S131-033', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'GA17/S131-033R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_033R.png', 'https://img.bottleneko.app/GA17_S131_033R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_033R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_033r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_033r.gif']}, 'GA05/S131-007': {'id': 'GA05/S131-007', 'series': 'GA/S131', 'name': '〈迪亞馬特〉的使用者 莉姿夏爾蒂·亞提司瑪特', 'jp_name': '《ティアマト》の使い手 リーズシャルテ・アティスマータ', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '王族', '機龍'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_LOCK_MOVE', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，到下次的對手回合結束前，給予以下能力。『【永】此卡不能移動到其他格子。』\n【自】［(1) 手牌的CX1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA05/S131-007', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA05/S131-007SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007.png', 'https://img.bottleneko.app/GA05_S131_007.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007.png']}, 'GA05/S131-007SP': {'id': 'GA05/S131-007SP', 'series': 'GA/S131', 'name': '〈迪亞馬特〉的使用者 莉姿夏爾蒂·亞提司瑪特', 'jp_name': '《ティアマト》の使い手 リーズシャルテ・アティスマータ', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '王族', '機龍'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_LOCK_MOVE', 'AUTO_ON_PLAY_SWAP_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007SP.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇對手的角色1張，到下次的對手回合結束前，給予以下能力。『【永】此卡不能移動到其他格子。』\n【自】［(1) 手牌的CX1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA05/S131-007', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA05/S131-007SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007SP.png', 'https://img.bottleneko.app/GA05_S131_007SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA05_S131_007SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga05_s131/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga05_s131_007sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA05_S131_007S.png', 'https://img.bottleneko.app/GA05_S131_007S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA05_S131_007S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga05_s131/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga05_s131_007s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga05_s131_007s.gif']}, 'GA08/S131-038': {'id': 'GA08/S131-038', 'series': 'GA/S131', 'name': '魔族農業大臣 別西卜', 'jp_name': '魔族の農相 ベルゼブブ', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔族', '農家'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_DOKITEMA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA08/S131-038', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA08/S131-038SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038.png', 'https://img.bottleneko.app/GA08_S131_038.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038.png']}, 'GA08/S131-038SP': {'id': 'GA08/S131-038SP', 'series': 'GA/S131', 'name': '魔族農業大臣 別西卜', 'jp_name': '魔族の農相 ベルゼブブ', 'type': 'CHAR', 'color': '綠', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔族', '農家'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DOKITEMA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038SP.png', 'text': '【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA08/S131-038', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA08/S131-038SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038SP.png', 'https://img.bottleneko.app/GA08_S131_038SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA08_S131_038SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga08_s131/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga08_s131_038sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA08_S131_038S.png', 'https://img.bottleneko.app/GA08_S131_038S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA08_S131_038S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga08_s131/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga08_s131_038s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga08_s131_038s.gif']}, 'GA10/S131-012': {'id': 'GA10/S131-012', 'series': 'GA/S131', 'name': '奇怪的妖精 琉', 'jp_name': '変り種のエルフ リュー', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 3, 'effects': ['CONT_CHOICE_CX_GIVES_WIND', 'ACT_CONCENTRATE_5_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，給予你的所有的領域的黃色的CX風的判定標誌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻出5張，放到休息室。那些卡片中每有1張判定標誌是箭頭的CX，你選擇自己休息室的角色最多1張，回到手牌。', 'base_id': 'GA10/S131-012', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-012GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012.png', 'https://img.bottleneko.app/GA10_S131_012.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012.png']}, 'GA10/S131-012GA': {'id': 'GA10/S131-012GA', 'series': 'GA/S131', 'name': '奇怪的妖精 琉', 'jp_name': '変り種のエルフ リュー', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 0, 'effects': ['CONT_CHOICE_CX_GIVES_WIND', 'ACT_CONCENTRATE_5_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012GA.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，給予你的所有的領域的黃色的CX風的判定標誌。\n【起】集中 ［(1) 將此卡【橫置】］ 你從自己的牌組上方翻出5張，放到休息室。那些卡片中每有1張判定標誌是箭頭的CX，你選擇自己休息室的角色最多1張，回到手牌。', 'base_id': 'GA10/S131-012', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA10/S131-012GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012GA.png', 'https://img.bottleneko.app/GA10_S131_012GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_012GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_012ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_012S.png', 'https://img.bottleneko.app/GA10_S131_012S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_012S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_012s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_012s.gif']}, 'GA10/S131-T09': {'id': 'GA10/S131-T09', 'series': 'GA/S131', 'name': '女神之鐘 赫斯緹雅', 'jp_name': '女神のカンパネラ ヘスティア', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '眷族', '神'], 'default_count': 3, 'effects': ['CONT_HAND5_BUFF_2000', 'AUTO_ATK_TWIN_DRIVE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09.png', 'text': '【永】在你的回合中，你的手牌有5張以上的話，此卡的攻擊力+2000。\n【自】［(1)］ 此卡攻擊時，你可以支付代價。支付代價的話，在那次攻擊中，你在判定階段執行2次判定。', 'base_id': 'GA10/S131-T09', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-T09TDP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09.png', 'https://img.bottleneko.app/GA10_S131_T09.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09.png']}, 'GA10/S131-T09TDP': {'id': 'GA10/S131-T09TDP', 'series': 'GA/S131', 'name': '女神之鐘 赫斯緹雅', 'jp_name': '女神のカンパネラ ヘスティア', 'type': 'CHAR', 'color': '藍', 'level': 0, 'cost': 0, 'power': 1500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '眷族', '神'], 'default_count': 0, 'effects': ['CONT_HAND5_BUFF_2000', 'AUTO_ATK_TWIN_DRIVE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09TDP.png', 'text': '【永】在你的回合中，你的手牌有5張以上的話，此卡的攻擊力+2000。\n【自】［(1)］ 此卡攻擊時，你可以支付代價。支付代價的話，在那次攻擊中，你在判定階段執行2次判定。', 'base_id': 'GA10/S131-T09', 'is_high_rarity': True, 'rarity': 'TDP', 'high_rarity_id': 'GA10/S131-T09TDP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09TDP.png', 'https://img.bottleneko.app/GA10_S131_T09TDP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09TDP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09tdp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09tdp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09SP.png', 'https://img.bottleneko.app/GA10_S131_T09SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09R.png', 'https://img.bottleneko.app/GA10_S131_T09R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_T09S.png', 'https://img.bottleneko.app/GA10_S131_T09S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_T09S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_t09s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_t09s.gif']}, 'GA12/S131-013': {'id': 'GA12/S131-013', 'series': 'GA/S131', 'name': '朋友的話是當然的 月之森真白', 'jp_name': '友達ならトーゼン 月ノ森真白', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '學生'], 'default_count': 4, 'effects': ['CONT_GAIN_CHOICE_TRIGGER', 'AUTO_ON_PLAY_BUFF_3000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，所有的領域的此卡獲得箭頭的判定標誌。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。', 'base_id': 'GA12/S131-013', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA12/S131-013GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013.png', 'https://img.bottleneko.app/GA12_S131_013.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013.png']}, 'GA12/S131-013GA': {'id': 'GA12/S131-013GA', 'series': 'GA/S131', 'name': '朋友的話是當然的 月之森真白', 'jp_name': '友達ならトーゼン 月ノ森真白', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '學生'], 'default_count': 0, 'effects': ['CONT_GAIN_CHOICE_TRIGGER', 'AUTO_ON_PLAY_BUFF_3000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013GA.png', 'text': '【永】你的CX區有判定標誌是箭頭的CX的話，所有的領域的此卡獲得箭頭的判定標誌。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+3000。', 'base_id': 'GA12/S131-013', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA12/S131-013GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013GA.png', 'https://img.bottleneko.app/GA12_S131_013GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA12_S131_013GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga12_s131/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga12_s131_013ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA12_S131_013S.png', 'https://img.bottleneko.app/GA12_S131_013S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA12_S131_013S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga12_s131/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga12_s131_013s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga12_s131_013s.gif']}, 'GA13/S131-077': {'id': 'GA13/S131-077', 'series': 'GA/S131', 'name': '我的女神 草壁由佳', 'jp_name': 'ぼくの女神 草壁ゆか', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '農業'], 'default_count': 4, 'effects': ['AUTO_STAGE_TO_WR_CLOCK_LOOK2_GA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多2張，選擇《GA文庫》的角色最多2張給對手確認，加到手牌，剩下的卡片放到休息室。', 'base_id': 'GA13/S131-077', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA13/S131-077GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077.png', 'https://img.bottleneko.app/GA13_S131_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077.png']}, 'GA13/S131-077GA': {'id': 'GA13/S131-077GA', 'series': 'GA/S131', 'name': '我的女神 草壁由佳', 'jp_name': 'ぼくの女神 草壁ゆか', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '農業'], 'default_count': 0, 'effects': ['AUTO_STAGE_TO_WR_CLOCK_LOOK2_GA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077GA.png', 'text': '【自】［(1) 你的牌組上方1張放到傷害區］ 此卡從舞台被放到休息室時，你可以支付代價。支付代價的話，你從自己的牌組上方看最多2張，選擇《GA文庫》的角色最多2張給對手確認，加到手牌，剩下的卡片放到休息室。', 'base_id': 'GA13/S131-077', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA13/S131-077GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077GA.png', 'https://img.bottleneko.app/GA13_S131_077GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA13_S131_077GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga13_s131/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga13_s131_077ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA13_S131_077S.png', 'https://img.bottleneko.app/GA13_S131_077S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA13_S131_077S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga13_s131/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga13_s131_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga13_s131_077s.gif']}, 'GA10/S131-002': {'id': 'GA10/S131-002', 'series': 'GA/S131', 'name': '跨越復仇 琉', 'jp_name': '復讐を越えて リュー', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 4, 'effects': ['AUTO_ON_PLAY_OPP_COUNT_BUFF_1000', 'CX_COMBO_RYU_ATK_SCRY2_SALVAGE'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於對手的角色張數×1000。\n【自】【CX連動】此卡攻擊時，CX區有「時隔五年的【能力值】更新」的話，你看自己牌組上方最多2張，選擇卡片最多2張，以任意順序放到牌組上方，剩下的卡片放到休息室，將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA10/S131-002', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-002SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002.png', 'https://img.bottleneko.app/GA10_S131_002.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002.png']}, 'GA10/S131-002SSP': {'id': 'GA10/S131-002SSP', 'series': 'GA/S131', 'name': '跨越復仇 琉', 'jp_name': '復讐を越えて リュー', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '妖精'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_OPP_COUNT_BUFF_1000', 'CX_COMBO_RYU_ATK_SCRY2_SALVAGE'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002SSP.png', 'text': '【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+X。X等於對手的角色張數×1000。\n【自】【CX連動】此卡攻擊時，CX區有「時隔五年的【能力值】更新」的話，你看自己牌組上方最多2張，選擇卡片最多2張，以任意順序放到牌組上方，剩下的卡片放到休息室，將自己的牌組上方1張公開，選擇自己休息室的等級X以下的角色1張，回到手牌。X等於被公開的卡片等級。CX視為等級0。公開過的卡片放回原位。', 'base_id': 'GA10/S131-002', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA10/S131-002SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002SSP.png', 'https://img.bottleneko.app/GA10_S131_002SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_002SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_002ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_002S.png', 'https://img.bottleneko.app/GA10_S131_002S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_002S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_002s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_002s.gif']}, 'GA17/S131-014': {'id': 'GA17/S131-014', 'series': 'GA/S131', 'name': '我的旅路 伊蕾娜', 'jp_name': '私の旅路 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔法'], 'default_count': 1, 'effects': ['AUTO_MEMORY_DEF_DIRECT_MINUS_SOUL', 'ACT_MILL_ELAINA_BUFF_2000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014.png', 'text': '【自】回合1次 記憶 對手的角色直接攻擊時，你的回憶區有卡名包含「伊蕾娜」的角色，沒有其他的你的「我的旅路 伊蕾娜」存在的話，你選擇攻擊中的角色最多1張，在那個回合中，魂傷-1。\n【起】［將此卡【橫置】］ 你從自己的牌組選擇「第二章 伊蕾娜」或「第三章 伊蕾娜」最多1張，放到休息室，將那個牌組洗牌，你選擇自己的《GA文庫》的角色1張，在那個回合中，攻擊力+2000。', 'base_id': 'GA17/S131-014', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-014GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014.png', 'https://img.bottleneko.app/GA17_S131_014.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014.png']}, 'GA17/S131-014GA': {'id': 'GA17/S131-014GA', 'series': 'GA/S131', 'name': '我的旅路 伊蕾娜', 'jp_name': '私の旅路 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['AUTO_MEMORY_DEF_DIRECT_MINUS_SOUL', 'ACT_MILL_ELAINA_BUFF_2000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014GA.png', 'text': '【自】回合1次 記憶 對手的角色直接攻擊時，你的回憶區有卡名包含「伊蕾娜」的角色，沒有其他的你的「我的旅路 伊蕾娜」存在的話，你選擇攻擊中的角色最多1張，在那個回合中，魂傷-1。\n【起】［將此卡【橫置】］ 你從自己的牌組選擇「第二章 伊蕾娜」或「第三章 伊蕾娜」最多1張，放到休息室，將那個牌組洗牌，你選擇自己的《GA文庫》的角色1張，在那個回合中，攻擊力+2000。', 'base_id': 'GA17/S131-014', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA17/S131-014GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014GA.png', 'https://img.bottleneko.app/GA17_S131_014GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_014GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_014ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_014S.png', 'https://img.bottleneko.app/GA17_S131_014S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_014S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_014s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_014s.gif']}, 'GA17/S131-015': {'id': 'GA17/S131-015', 'series': 'GA/S131', 'name': '第一章 伊蕾娜', 'jp_name': '第一章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 3, 'effects': ['CONT_YOUR_TURN_6000', 'AUTO_REVERSE_CHAIN_CH2_ELAINA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015.png', 'text': '【永】在你的回合中，此卡的攻擊力+6000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，其他的你的《GA文庫》的角色存在2張以上的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第二章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方最多3張，以任意順序放到牌組上方，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第二章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-015', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-015S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015.png', 'https://img.bottleneko.app/GA17_S131_015.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015.png']}, 'GA17/S131-015S': {'id': 'GA17/S131-015S', 'series': 'GA/S131', 'name': '第一章 伊蕾娜', 'jp_name': '第一章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['CONT_YOUR_TURN_6000', 'AUTO_REVERSE_CHAIN_CH2_ELAINA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015S.png', 'text': '【永】在你的回合中，此卡的攻擊力+6000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，其他的你的《GA文庫》的角色存在2張以上的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第二章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方最多3張，以任意順序放到牌組上方，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第二章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-015', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA17/S131-015S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015S.png', 'https://img.bottleneko.app/GA17_S131_015S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_015S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_015s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_015GA.png', 'https://img.bottleneko.app/GA17_S131_015GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_015GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_015ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_015ga.gif']}, 'GA02/S131-009': {'id': 'GA02/S131-009', 'series': 'GA/S131', 'name': '告別膽小的自己 椎名真晝', 'jp_name': '臆病だった自分にさよならを 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 1, 'effects': ['COUNTER_BACKUP_2500_LV2', 'AUTO_ON_BACKUP_REFRESH_WR'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009.png', 'text': '【自】［(2)］ 當你使用此卡的『助太刀』時，你可以支付代價。支付代價的話，你將自己休息室的卡片全部，返回牌組，將那個牌組洗牌。\n【起】【反擊】 助太刀2500 等級2 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那個回合中，攻擊力+2500。', 'base_id': 'GA02/S131-009', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA02/S131-009SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009.png', 'https://img.bottleneko.app/GA02_S131_009.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009.png']}, 'GA02/S131-009SP': {'id': 'GA02/S131-009SP', 'series': 'GA/S131', 'name': '告別膽小的自己 椎名真晝', 'jp_name': '臆病だった自分にさよならを 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 2500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 0, 'effects': ['COUNTER_BACKUP_2500_LV2', 'AUTO_ON_BACKUP_REFRESH_WR'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009SP.png', 'text': '【自】［(2)］ 當你使用此卡的『助太刀』時，你可以支付代價。支付代價的話，你將自己休息室的卡片全部，返回牌組，將那個牌組洗牌。\n【起】【反擊】 助太刀2500 等級2 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那個回合中，攻擊力+2500。', 'base_id': 'GA02/S131-009', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA02/S131-009SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009SP.png', 'https://img.bottleneko.app/GA02_S131_009SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_009SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_009sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_009S.png', 'https://img.bottleneko.app/GA02_S131_009S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_009S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_009s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_009s.gif']}, 'GA10/S131-019': {'id': 'GA10/S131-019', 'series': 'GA/S131', 'name': '炸薯球 艾絲', 'jp_name': 'ジャガ丸くん アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 7000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_OPP_REVERSE_COMPRESS', 'AUTO_DIRECT_ATK_YELLOW_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019.png', 'text': '【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手選擇自己休息室的CX1張，除那張卡片以外的休息室的卡片全部，回到牌組，將那個牌組洗牌。\n【自】此卡直接攻擊時，你可以選擇自己休息室的黃色的卡片1張，放到能量區。', 'base_id': 'GA10/S131-019', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-019S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019.png', 'https://img.bottleneko.app/GA10_S131_019.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019.png']}, 'GA10/S131-019S': {'id': 'GA10/S131-019S', 'series': 'GA/S131', 'name': '炸薯球 艾絲', 'jp_name': 'ジャガ丸くん アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 7000, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_OPP_REVERSE_COMPRESS', 'AUTO_DIRECT_ATK_YELLOW_STOCK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019S.png', 'text': '【自】［(1) 手牌1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，對手選擇自己休息室的CX1張，除那張卡片以外的休息室的卡片全部，回到牌組，將那個牌組洗牌。\n【自】此卡直接攻擊時，你可以選擇自己休息室的黃色的卡片1張，放到能量區。', 'base_id': 'GA10/S131-019', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA10/S131-019S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019S.png', 'https://img.bottleneko.app/GA10_S131_019S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_019S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_019s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_019GA.png', 'https://img.bottleneko.app/GA10_S131_019GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_019GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_019ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_019ga.gif']}, 'GA10/S131-029': {'id': 'GA10/S131-029', 'series': 'GA/S131', 'name': '蕾菲亞&艾絲', 'jp_name': 'レフィーヤ＆アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 1, 'effects': ['AUTO_ON_PLAY_GRANT_ANTI_EARLY_PLAY_BOMB'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇自己的角色最多2張，在那個回合中，給予以下能力。『【自】此卡【倒置】時，此卡的戰鬥對手的等級比對手玩家等級還要高的話，你可以將那張角色放到能量區。放到能量區的話，你將對手的能量區下方1張，放到休息室。』', 'base_id': 'GA10/S131-029', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA10/S131-029GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029.png', 'https://img.bottleneko.app/GA10_S131_029.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029.png']}, 'GA10/S131-029GA': {'id': 'GA10/S131-029GA', 'series': 'GA/S131', 'name': '蕾菲亞&艾絲', 'jp_name': 'レフィーヤ＆アイズ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '眷族'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_GRANT_ANTI_EARLY_PLAY_BOMB'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029GA.png', 'text': '【自】此卡從手牌被放置到舞台時，你選擇自己的角色最多2張，在那個回合中，給予以下能力。『【自】此卡【倒置】時，此卡的戰鬥對手的等級比對手玩家等級還要高的話，你可以將那張角色放到能量區。放到能量區的話，你將對手的能量區下方1張，放到休息室。』', 'base_id': 'GA10/S131-029', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA10/S131-029GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029GA.png', 'https://img.bottleneko.app/GA10_S131_029GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_029GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_029ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA10_S131_029S.png', 'https://img.bottleneko.app/GA10_S131_029S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA10_S131_029S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga10_s131/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga10_s131_029s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga10_s131_029s.gif']}, 'GA17/S131-017': {'id': 'GA17/S131-017', 'series': 'GA/S131', 'name': '第二章 伊蕾娜', 'jp_name': '第二章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 1500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 4, 'effects': ['CONT_YOUR_TURN_11000', 'AUTO_REVERSE_CHAIN_CH3_ELAINA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017.png', 'text': '【永】在你的回合中，此卡的攻擊力+11000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第三章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方1張，放到牌組上方或下方或休息室，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第三章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-017', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-017S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017.png', 'https://img.bottleneko.app/GA17_S131_017.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017.png']}, 'GA17/S131-017S': {'id': 'GA17/S131-017S', 'series': 'GA/S131', 'name': '第二章 伊蕾娜', 'jp_name': '第二章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 2, 'cost': 1, 'power': 1500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['CONT_YOUR_TURN_11000', 'AUTO_REVERSE_CHAIN_CH3_ELAINA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017S.png', 'text': '【永】在你的回合中，此卡的攻擊力+11000。\n【自】［(1) 將此卡放到休息室］ 此卡的戰鬥對手【倒置】時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你選擇自己休息室的「第三章 伊蕾娜」1張，放到回憶區。放到回憶區的話，你看自己的牌組上方1張，放到牌組上方或下方或休息室，在下次的你的抽牌階段開始時，你可以選擇自己的回憶區的「第三章 伊蕾娜」1張，放到舞台上任意的格子。', 'base_id': 'GA17/S131-017', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'GA17/S131-017S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017S.png', 'https://img.bottleneko.app/GA17_S131_017S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_017S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_017s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_017GA.png', 'https://img.bottleneko.app/GA17_S131_017GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_017GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_017ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_017ga.gif']}, 'GA01/S131-115': {'id': 'GA01/S131-115', 'series': 'GA/S131', 'name': '《五帝》櫛川鳩子', 'jp_name': '《五帝》櫛川鳩子', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '文藝部'], 'default_count': 1, 'effects': ['CONT_IGNORE_SELF_COLOR', 'AUTO_ON_PLAY_SAC_STAGE_SALVAGE_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115.png', 'text': '【永】此卡可以無需滿足顏色條件從手牌使用。\n【自】［其他的你的舞台的角色1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA01/S131-115', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA01/S131-115GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115.png', 'https://img.bottleneko.app/GA01_S131_115.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115.png']}, 'GA01/S131-115GA': {'id': 'GA01/S131-115GA', 'series': 'GA/S131', 'name': '《五帝》櫛川鳩子', 'jp_name': '《五帝》櫛川鳩子', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 10500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '文藝部'], 'default_count': 0, 'effects': ['CONT_IGNORE_SELF_COLOR', 'AUTO_ON_PLAY_SAC_STAGE_SALVAGE_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115GA.png', 'text': '【永】此卡可以無需滿足顏色條件從手牌使用。\n【自】［其他的你的舞台的角色1張放到休息室］ 此卡從手牌被放置到舞台時，你可以支付代價。支付代價的話，你選擇自己休息室的CX1張，回到手牌。', 'base_id': 'GA01/S131-115', 'is_high_rarity': True, 'rarity': 'GA', 'high_rarity_id': 'GA01/S131-115GA', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115GA.png', 'https://img.bottleneko.app/GA01_S131_115GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA01_S131_115GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga01_s131/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga01_s131_115ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115ga.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA01_S131_115S.png', 'https://img.bottleneko.app/GA01_S131_115S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA01_S131_115S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga01_s131/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga01_s131_115s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga01_s131_115s.gif']}, 'GA02/S131-003': {'id': 'GA02/S131-003', 'series': 'GA/S131', 'name': '隔壁的天使 椎名真晝', 'jp_name': 'お隣の天使様 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 2, 'effects': ['CONT_EARLY_PLAY_4GA', 'AUTO_ON_PLAY_BUFF_1500', 'AUTO_ON_PLAY_DISCARD_HEAL_AND_SALVAGE_GA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003.png', 'text': '【永】你的《GA文庫》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你將自己的傷害區上方最多1張，放到休息室，選擇自己休息室的《GA文庫》的角色1張，回到手牌。', 'base_id': 'GA02/S131-003', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA02/S131-003SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003.png', 'https://img.bottleneko.app/GA02_S131_003.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003.png']}, 'GA02/S131-003SSP': {'id': 'GA02/S131-003SSP', 'series': 'GA/S131', 'name': '隔壁的天使 椎名真晝', 'jp_name': 'お隣の天使様 椎名真昼', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '天使'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4GA', 'AUTO_ON_PLAY_BUFF_1500', 'AUTO_ON_PLAY_DISCARD_HEAL_AND_SALVAGE_GA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SSP.png', 'text': '【永】你的《GA文庫》的角色存在4張以上的話，你的手牌的此卡等級-1。\n【自】此卡從手牌被放置到舞台時，在那個回合中，此卡的攻擊力+1500。\n【自】［手牌1張放到休息室］ 此卡從手牌被放置到舞台時，有其他的你的《GA文庫》的角色存在的話，你可以支付代價。支付代價的話，你將自己的傷害區上方最多1張，放到休息室，選擇自己休息室的《GA文庫》的角色1張，回到手牌。', 'base_id': 'GA02/S131-003', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA02/S131-003SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SSP.png', 'https://img.bottleneko.app/GA02_S131_003SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003SP.png', 'https://img.bottleneko.app/GA02_S131_003SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA02_S131_003S.png', 'https://img.bottleneko.app/GA02_S131_003S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA02_S131_003S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga02_s131/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga02_s131_003s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga02_s131_003s.gif']}, 'GA04/S131-100': {'id': 'GA04/S131-100', 'series': 'GA/S131', 'name': '新的黎明 女神官', 'jp_name': '新しい夜明け 女神官', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '神官'], 'default_count': 2, 'effects': ['CONT_EARLY_PLAY_WR_CX_2OR6', 'CONT_YOUR_TURN_1000', 'AUTO_ON_PLAY_CHOOSE_HEAL_OR_RESHUFFLE_OPP_STOCK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100.png', 'text': '【永】你的休息室的CX在2張以下或6張以上的話，你的手牌的此卡等級-1。\n【永】在你的回合中，此卡的攻擊力+1000。\n【自】此卡從手牌被放置到舞台時，以下的2個效果之中你選擇1個執行。『你可以將自己的傷害區上方1張，放到休息室。』『對手將自己的能量全部，返回牌組，將那個牌組洗牌，從自己的牌組上方將相同張數放到能量區，在那個回合中，此卡的攻擊力+2000。』', 'base_id': 'GA04/S131-100', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA04/S131-100SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100.png', 'https://img.bottleneko.app/GA04_S131_100.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100.png']}, 'GA04/S131-100SSP': {'id': 'GA04/S131-100SSP', 'series': 'GA/S131', 'name': '新的黎明 女神官', 'jp_name': '新しい夜明け 女神官', 'type': 'CHAR', 'color': '藍', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '冒險者', '神官'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_WR_CX_2OR6', 'CONT_YOUR_TURN_1000', 'AUTO_ON_PLAY_CHOOSE_HEAL_OR_RESHUFFLE_OPP_STOCK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SSP.png', 'text': '【永】你的休息室的CX在2張以下或6張以上的話，你的手牌的此卡等級-1。\n【永】在你的回合中，此卡的攻擊力+1000。\n【自】此卡從手牌被放置到舞台時，以下的2個效果之中你選擇1個執行。『你可以將自己的傷害區上方1張，放到休息室。』『對手將自己的能量全部，返回牌組，將那個牌組洗牌，從自己的牌組上方將相同張數放到能量區，在那個回合中，此卡的攻擊力+2000。』', 'base_id': 'GA04/S131-100', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'GA04/S131-100SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SSP.png', 'https://img.bottleneko.app/GA04_S131_100SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100SP.png', 'https://img.bottleneko.app/GA04_S131_100SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA04_S131_100S.png', 'https://img.bottleneko.app/GA04_S131_100S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA04_S131_100S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga04_s131/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga04_s131_100s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga04_s131_100s.gif']}, 'GA17/S131-010': {'id': 'GA17/S131-010', 'series': 'GA/S131', 'name': '第三章 伊蕾娜', 'jp_name': '第三章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 4, 'effects': ['AUTO_ATK_BURN1_ON_ENTER_TURN', 'AUTO_SEND_TO_MEMORY_ON_REV_OR_END', 'CX_COMBO_MEMORY_ASH_WITCH_DEPLOY_BURN2'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010.png', 'text': '【自】此卡從手牌或回憶區被放到舞台的回合中，此卡攻擊時，你可以給對手1點傷害。會發生傷害取消。\n【自】此卡【倒置】時或回合結束時，將此卡放到回憶區。\n【自】【CX連動】記憶 ［(2) 手牌1張放到休息室］ 此卡在回憶區，你的等級在3以上的話，當「灰之魔女」被放置到你的CX區時，你可以支付代價。支付代價的話，你將此卡放到舞台的前列的格子，給對手2點傷害。會發生傷害取消。', 'base_id': 'GA17/S131-010', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'GA17/S131-010SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010.png', 'https://img.bottleneko.app/GA17_S131_010.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010.png']}, 'GA17/S131-010SP': {'id': 'GA17/S131-010SP', 'series': 'GA/S131', 'name': '第三章 伊蕾娜', 'jp_name': '第三章 イレイナ', 'type': 'CHAR', 'color': '黃', 'level': 3, 'cost': 2, 'power': 10000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['GA文庫', '魔法'], 'default_count': 0, 'effects': ['AUTO_ATK_BURN1_ON_ENTER_TURN', 'AUTO_SEND_TO_MEMORY_ON_REV_OR_END', 'CX_COMBO_MEMORY_ASH_WITCH_DEPLOY_BURN2'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010SP.png', 'text': '【自】此卡從手牌或回憶區被放到舞台的回合中，此卡攻擊時，你可以給對手1點傷害。會發生傷害取消。\n【自】此卡【倒置】時或回合結束時，將此卡放到回憶區。\n【自】【CX連動】記憶 ［(2) 手牌1張放到休息室］ 此卡在回憶區，你的等級在3以上的話，當「灰之魔女」被放置到你的CX區時，你可以支付代價。支付代價的話，你將此卡放到舞台的前列的格子，給對手2點傷害。會發生傷害取消。', 'base_id': 'GA17/S131-010', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'GA17/S131-010SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010SP.png', 'https://img.bottleneko.app/GA17_S131_010SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010S.png', 'https://img.bottleneko.app/GA17_S131_010S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/GA17_S131_010GA.png', 'https://img.bottleneko.app/GA17_S131_010GA.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/GA17_S131_010GA.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga17_s131/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131_td/ga17_s131_010ga.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/g/ga_s131/ga17_s131_010ga.gif']}, 'BTR/W107-098': {'id': 'BTR/W107-098', 'series': 'BTR/W107', 'name': '成長與信賴的8小節', 'jp_name': '成長と信頼の8小節', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 4, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-098', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BTR/W107-098OFR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098.png', 'https://img.bottleneko.app/BTR_W107_098.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098.png']}, 'BTR/W107-098OFR': {'id': 'BTR/W107-098OFR', 'series': 'BTR/W107', 'name': '成長與信賴的8小節', 'jp_name': '成長と信頼の8小節', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098OFR.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-098', 'is_high_rarity': True, 'rarity': 'OFR', 'high_rarity_id': 'BTR/W107-098OFR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098OFR.png', 'https://img.bottleneko.app/BTR_W107_098OFR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_098OFR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_098ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098ofr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_098R.png', 'https://img.bottleneko.app/BTR_W107_098R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_098R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_098r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_098r.gif']}, 'BTR/W107-100': {'id': 'BTR/W107-100', 'series': 'BTR/W107', 'name': '逐漸增加的回憶', 'jp_name': '増えていく思い出', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 4, 'effects': ['CX_STANDBY'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-100', 'is_high_rarity': False, 'rarity': 'CR', 'high_rarity_id': 'BTR/W107-100R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100.png', 'https://img.bottleneko.app/BTR_W107_100.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100.png']}, 'BTR/W107-100R': {'id': 'BTR/W107-100R', 'series': 'BTR/W107', 'name': '逐漸增加的回憶', 'jp_name': '増えていく思い出', 'type': 'CX', 'color': '紅', 'level': 0, 'cost': 0, 'power': 0, 'soul': 0, 'trigger': 'STANDBY', 'traits': [], 'default_count': 0, 'effects': ['CX_STANDBY'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100R.png', 'text': '【自】當此卡從手牌放到名場面區時，執行開機的效果。\n開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。', 'base_id': 'BTR/W107-100', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-100R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100R.png', 'https://img.bottleneko.app/BTR_W107_100R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100RRR.png', 'https://img.bottleneko.app/BTR_W107_100RRR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100RRR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100rrr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100rrr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100rrr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_100OFR.png', 'https://img.bottleneko.app/BTR_W107_100OFR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_100OFR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_100ofr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_100ofr.gif']}, 'BTR/W107-T02': {'id': 'BTR/W107-T02', 'series': 'BTR/W107', 'name': '樂團的領導者 伊地知虹夏', 'jp_name': 'バンドのリーダー 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '可靠'], 'default_count': 2, 'effects': ['AUTO_ON_YELLOW_CX_BUFF_1500', 'ACT_CONCENTRATE_5_DRAW'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02.png', 'text': '【自】當你的黃色名場面放置到名場面區時，你選擇自己的角色1張，在那回合中，攻擊力+1500。\n【起】集中 ［(1) 此卡【橫置】］ 你從自己的牌組上方翻開5張卡片，放到休息室。那些卡片每有1張名場面，你最多抽1張牌。', 'base_id': 'BTR/W107-T02', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T02R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02.png', 'https://img.bottleneko.app/BTR_W107_T02.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02.png']}, 'BTR/W107-T02R': {'id': 'BTR/W107-T02R', 'series': 'BTR/W107', 'name': '樂團的領導者 伊地知虹夏', 'jp_name': 'バンドのリーダー 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '可靠'], 'default_count': 0, 'effects': ['AUTO_ON_YELLOW_CX_BUFF_1500', 'ACT_CONCENTRATE_5_DRAW'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02R.png', 'text': '【自】當你的黃色名場面放置到名場面區時，你選擇自己的角色1張，在那回合中，攻擊力+1500。\n【起】集中 ［(1) 此卡【橫置】］ 你從自己的牌組上方翻開5張卡片，放到休息室。那些卡片每有1張名場面，你最多抽1張牌。', 'base_id': 'BTR/W107-T02', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T02R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02R.png', 'https://img.bottleneko.app/BTR_W107_T02R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02S.png', 'https://img.bottleneko.app/BTR_W107_T02S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T02SP.png', 'https://img.bottleneko.app/BTR_W107_T02SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T02SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t02sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t02sp.gif']}, 'BTR/W107-T13': {'id': 'BTR/W107-T13', 'series': 'BTR/W107', 'name': '樂團女子？ 後藤一里', 'jp_name': 'バンドマン？ 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['CONT_BUFF_VOCAL_KITA_1000_1SOUL', 'AUTO_BOND_VOCAL_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13.png', 'text': '【永】其他的你的「主唱吉他手 喜多郁代」全部，攻擊力+1000，魂傷+1。\n【自】絆／「主唱吉他手 喜多郁代」 ［手牌1張放到休息室］ 此卡從手牌登場到舞台時，你可以支付費用。這樣做的話，你從自己的休息室選擇1張「主唱吉他手 喜多郁代」加到手牌。', 'base_id': 'BTR/W107-T13', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T13R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13.png', 'https://img.bottleneko.app/BTR_W107_T13.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13.png']}, 'BTR/W107-T13R': {'id': 'BTR/W107-T13R', 'series': 'BTR/W107', 'name': '樂團女子？ 後藤一里', 'jp_name': 'バンドマン？ 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['CONT_BUFF_VOCAL_KITA_1000_1SOUL', 'AUTO_BOND_VOCAL_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13R.png', 'text': '【永】其他的你的「主唱吉他手 喜多郁代」全部，攻擊力+1000，魂傷+1。\n【自】絆／「主唱吉他手 喜多郁代」 ［手牌1張放到休息室］ 此卡從手牌登場到舞台時，你可以支付費用。這樣做的話，你從自己的休息室選擇1張「主唱吉他手 喜多郁代」加到手牌。', 'base_id': 'BTR/W107-T13', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T13R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13R.png', 'https://img.bottleneko.app/BTR_W107_T13R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T13R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t13r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T13S.png', 'https://img.bottleneko.app/BTR_W107_T13S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T13S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t13s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t13s.gif']}, 'BTR/W107-T14': {'id': 'BTR/W107-T14', 'series': 'BTR/W107', 'name': '後藤一里', 'jp_name': '後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_LOOK3_EVENT', 'AUTO_ON_PLAY_BOMB_COST0_IF_OPP_LE1'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14.png', 'text': '【自】此卡從手牌被放置到舞台時，你從自己的牌組上方看最多3張，選擇事件最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，對手的前列的角色在1張以下的話，你可以選擇對手的前列的費用0以下的角色1張，放到休息室。', 'base_id': 'BTR/W107-T14', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T14SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14.png', 'https://img.bottleneko.app/BTR_W107_T14.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14.png']}, 'BTR/W107-T14SP': {'id': 'BTR/W107-T14SP', 'series': 'BTR/W107', 'name': '後藤一里', 'jp_name': '後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_LOOK3_EVENT', 'AUTO_ON_PLAY_BOMB_COST0_IF_OPP_LE1'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14SP.png', 'text': '【自】此卡從手牌被放置到舞台時，你從自己的牌組上方看最多3張，選擇事件最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。\n【自】此卡從手牌被放置到舞台時，對手的前列的角色在1張以下的話，你可以選擇對手的前列的費用0以下的角色1張，放到休息室。', 'base_id': 'BTR/W107-T14', 'is_high_rarity': True, 'rarity': 'SP', 'high_rarity_id': 'BTR/W107-T14SP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14SP.png', 'https://img.bottleneko.app/BTR_W107_T14SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14R.png', 'https://img.bottleneko.app/BTR_W107_T14R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T14S.png', 'https://img.bottleneko.app/BTR_W107_T14S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T14S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t14s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t14s.gif']}, 'BTR/W107-T15': {'id': 'BTR/W107-T15', 'series': 'BTR/W107', 'name': '陽角 喜多郁代', 'jp_name': '陽キャ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['AUTO_ON_REVERSE_LOOK3_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15.png', 'text': '【自】當戰鬥中的此卡【倒置】時，你從自己的牌組上方看最多3張，選擇名場面最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。', 'base_id': 'BTR/W107-T15', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T15R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15.png', 'https://img.bottleneko.app/BTR_W107_T15.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15.png']}, 'BTR/W107-T15R': {'id': 'BTR/W107-T15R', 'series': 'BTR/W107', 'name': '陽角 喜多郁代', 'jp_name': '陽キャ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_ON_REVERSE_LOOK3_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15R.png', 'text': '【自】當戰鬥中的此卡【倒置】時，你從自己的牌組上方看最多3張，選擇名場面最多1張給對手確認，加到手牌，剩下的卡片放到休息室。加到手牌的話，你選擇自己的手牌1張，放到休息室。', 'base_id': 'BTR/W107-T15', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T15R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15R.png', 'https://img.bottleneko.app/BTR_W107_T15R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15S.png', 'https://img.bottleneko.app/BTR_W107_T15S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T15SP.png', 'https://img.bottleneko.app/BTR_W107_T15SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T15SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t15sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t15sp.gif']}, 'BTR/W107-T16': {'id': 'BTR/W107-T16', 'series': 'BTR/W107', 'name': '主唱吉他手 喜多郁代', 'jp_name': 'ギターボーカル 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': [], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16.png', 'text': '（無特殊效果）', 'base_id': 'BTR/W107-T16', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T16R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16.png', 'https://img.bottleneko.app/BTR_W107_T16.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16.png']}, 'BTR/W107-T16R': {'id': 'BTR/W107-T16R', 'series': 'BTR/W107', 'name': '主唱吉他手 喜多郁代', 'jp_name': 'ギターボーカル 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 0, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': [], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16R.png', 'text': '（無特殊效果）', 'base_id': 'BTR/W107-T16', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T16R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16R.png', 'https://img.bottleneko.app/BTR_W107_T16R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T16R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t16r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T16S.png', 'https://img.bottleneko.app/BTR_W107_T16S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T16S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t16s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t16s.gif']}, 'BTR/W107-T17': {'id': 'BTR/W107-T17', 'series': 'BTR/W107', 'name': '高人氣 喜多郁代', 'jp_name': '人気者 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_SELF_2000', 'AUTO_ENCORE_1STOCK_1HAND'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，在那回合中，此卡的攻擊力+2000。\n【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。', 'base_id': 'BTR/W107-T17', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T17R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17.png', 'https://img.bottleneko.app/BTR_W107_T17.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17.png']}, 'BTR/W107-T17R': {'id': 'BTR/W107-T17R', 'series': 'BTR/W107', 'name': '高人氣 喜多郁代', 'jp_name': '人気者 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 1, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_SELF_2000', 'AUTO_ENCORE_1STOCK_1HAND'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17R.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，在那回合中，此卡的攻擊力+2000。\n【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。', 'base_id': 'BTR/W107-T17', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T17R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17R.png', 'https://img.bottleneko.app/BTR_W107_T17R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T17R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t17r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T17S.png', 'https://img.bottleneko.app/BTR_W107_T17S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T17S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t17s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t17s.gif']}, 'BTR/W107-T18': {'id': 'BTR/W107-T18', 'series': 'BTR/W107', 'name': '喜多郁代', 'jp_name': '喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_ENCORE_1STOCK_1HAND', 'ACT_1STOCK_1000_CLOCK_KICK'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18.png', 'text': '【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。\n【起】［(1)］ 在那回合中，此卡的攻擊力+1000，此卡獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以將那個角色放到時計區。』', 'base_id': 'BTR/W107-T18', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T18R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18.png', 'https://img.bottleneko.app/BTR_W107_T18.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18.png']}, 'BTR/W107-T18R': {'id': 'BTR/W107-T18R', 'series': 'BTR/W107', 'name': '喜多郁代', 'jp_name': '喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 2, 'power': 7000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_ENCORE_1STOCK_1HAND', 'ACT_1STOCK_1000_CLOCK_KICK'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18R.png', 'text': '【自】再登場 ［(1) 手牌的1張卡片放到休息室］ 此卡從舞台放到休息室時，你可以支付費用。這樣做的話，此卡【橫置】放到它本來在的格子上。\n【起】［(1)］ 在那回合中，此卡的攻擊力+1000，此卡獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以將那個角色放到時計區。』', 'base_id': 'BTR/W107-T18', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T18R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18R.png', 'https://img.bottleneko.app/BTR_W107_T18R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18SP.png', 'https://img.bottleneko.app/BTR_W107_T18SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T18S.png', 'https://img.bottleneko.app/BTR_W107_T18S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T18S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t18s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t18s.gif']}, 'BTR/W107-077': {'id': 'BTR/W107-077', 'series': 'BTR/W107', 'name': '裝過頭的面子 後藤一里', 'jp_name': '張り切りすぎた見栄 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_TARGET_1000', 'AUTO_STAGE_TO_WR_DISCARD_MUSIC_LOOK4_LV1'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，你選擇自己的角色1張，在那回合中，攻擊力+1000。\n【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從舞台放到休息室時，你可以支付費用。這樣做的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面視為等級0。', 'base_id': 'BTR/W107-077', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-077KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077.png', 'https://img.bottleneko.app/BTR_W107_077.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077.png']}, 'BTR/W107-077KBR': {'id': 'BTR/W107-077KBR', 'series': 'BTR/W107', 'name': '裝過頭的面子 後藤一里', 'jp_name': '張り切りすぎた見栄 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 1000, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_OTHER_BATTLE_REVERSE_TARGET_1000', 'AUTO_STAGE_TO_WR_DISCARD_MUSIC_LOOK4_LV1'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077KBR.png', 'text': '【自】其他的你的戰鬥中的角色【倒置】時，你選擇自己的角色1張，在那回合中，攻擊力+1000。\n【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從舞台放到休息室時，你可以支付費用。這樣做的話，你從自己的牌組上方看最多4張，選擇等級1以上的卡片最多1張給對手確認，加到手牌，剩下的卡片放到休息室。名場面視為等級0。', 'base_id': 'BTR/W107-077', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-077KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077KBR.png', 'https://img.bottleneko.app/BTR_W107_077KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_077KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_077kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_077S.png', 'https://img.bottleneko.app/BTR_W107_077S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_077S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_077s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_077s.gif']}, 'BTR/W107-076': {'id': 'BTR/W107-076', 'series': 'BTR/W107', 'name': '成長歷程 喜多郁代', 'jp_name': '成長の軌跡 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_OTHER_MUSIC_500_EACH', 'AUTO_ON_PLAY_HEAL', 'CX_COMBO_KITA_ATK_BURN4'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076.png', 'text': '【永】其他的你的《音樂》的角色每有1張，此卡的攻擊力+500。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。\n【自】【CX連動】［手牌2張卡片放到休息室］ 此卡攻擊時，名場面區有「逐漸增加的回憶」，且其他的你的《音樂》的角色有4張以上的話，你可以支付費用。這樣做的話，給予對手4點傷害。會發生傷害取消。', 'base_id': 'BTR/W107-076', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-076S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076.png', 'https://img.bottleneko.app/BTR_W107_076.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076.png']}, 'BTR/W107-076S': {'id': 'BTR/W107-076S', 'series': 'BTR/W107', 'name': '成長歷程 喜多郁代', 'jp_name': '成長の軌跡 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 9000, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_OTHER_MUSIC_500_EACH', 'AUTO_ON_PLAY_HEAL', 'CX_COMBO_KITA_ATK_BURN4'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076S.png', 'text': '【永】其他的你的《音樂》的角色每有1張，此卡的攻擊力+500。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。\n【自】【CX連動】［手牌2張卡片放到休息室］ 此卡攻擊時，名場面區有「逐漸增加的回憶」，且其他的你的《音樂》的角色有4張以上的話，你可以支付費用。這樣做的話，給予對手4點傷害。會發生傷害取消。', 'base_id': 'BTR/W107-076', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BTR/W107-076S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076S.png', 'https://img.bottleneko.app/BTR_W107_076S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076SSP.png', 'https://img.bottleneko.app/BTR_W107_076SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076SP.png', 'https://img.bottleneko.app/BTR_W107_076SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_076KBR.png', 'https://img.bottleneko.app/BTR_W107_076KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_076KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_076kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_076kbr.gif']}, 'BTR/W107-075': {'id': 'BTR/W107-075', 'series': 'BTR/W107', 'name': '晚霞的歸路 喜多郁代', 'jp_name': '夕焼けの帰り道 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_OTHER_2MUSIC_BUFF_3000', 'AUTO_ON_PLAY_STOCK_HEAL_IF_4', 'CX_COMBO_SUNSET_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075.png', 'text': '【永】其他的你的《音樂》的角色有2張以上的話，此卡的攻擊力+3000。\n【自】此卡從手牌放置到舞台時，若你的等級區與時鐘區的卡片合計有4張以上，你可以將自己時鐘區上方1張放到能量區。\n【自】【CX連動】當「成長與信賴的8小節」放置到你的名場面區時，前列有此卡，且有其他的你的《音樂》角色的話，在那個回合中，此卡的攻擊力+1000，並獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以從自己的休息室選擇《音樂》的角色1張回到手牌。』', 'base_id': 'BTR/W107-075', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-075S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075.png', 'https://img.bottleneko.app/BTR_W107_075.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075.png']}, 'BTR/W107-075S': {'id': 'BTR/W107-075S', 'series': 'BTR/W107', 'name': '晚霞的歸路 喜多郁代', 'jp_name': '夕焼けの帰り道 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 2, 'cost': 1, 'power': 5500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_OTHER_2MUSIC_BUFF_3000', 'AUTO_ON_PLAY_STOCK_HEAL_IF_4', 'CX_COMBO_SUNSET_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075S.png', 'text': '【永】其他的你的《音樂》的角色有2張以上的話，此卡的攻擊力+3000。\n【自】此卡從手牌放置到舞台時，若你的等級區與時鐘區的卡片合計有4張以上，你可以將自己時鐘區上方1張放到能量區。\n【自】【CX連動】當「成長與信賴的8小節」放置到你的名場面區時，前列有此卡，且有其他的你的《音樂》角色的話，在那個回合中，此卡的攻擊力+1000，並獲得以下能力。『【自】此卡的戰鬥對手【倒置】時，你可以從自己的休息室選擇《音樂》的角色1張回到手牌。』', 'base_id': 'BTR/W107-075', 'is_high_rarity': True, 'rarity': 'SR', 'high_rarity_id': 'BTR/W107-075S', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075S.png', 'https://img.bottleneko.app/BTR_W107_075S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075SP.png', 'https://img.bottleneko.app/BTR_W107_075SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_075KBR.png', 'https://img.bottleneko.app/BTR_W107_075KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_075KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_075kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_075kbr.gif']}, 'BTR/W107-T06': {'id': 'BTR/W107-T06', 'series': 'BTR/W107', 'name': '音樂話題～ 伊地知虹夏', 'jp_name': '音楽バナシ～ 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 1, 'power': 500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '可靠'], 'default_count': 2, 'effects': ['COUNTER_BACKUP_2000_LV1', 'AUTO_ON_BACKUP_TOP_CHECK_MUSIC'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06.png', 'text': '【自】當你使用此卡的『助太刀』時，你將自己的牌組上方1張公開。那張卡片是《音樂》的角色的話加到手牌，你選擇自己的手牌1張，放到休息室。如果不是的話放回原位。\n【起】【反擊】助太刀2000 等級1 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那回合中，攻擊力+2000。', 'base_id': 'BTR/W107-T06', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T06R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06.png', 'https://img.bottleneko.app/BTR_W107_T06.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06.png']}, 'BTR/W107-T06R': {'id': 'BTR/W107-T06R', 'series': 'BTR/W107', 'name': '音樂話題～ 伊地知虹夏', 'jp_name': '音楽バナシ～ 伊地知虹夏', 'type': 'CHAR', 'color': '黃', 'level': 1, 'cost': 1, 'power': 500, 'soul': 1, 'trigger': 'SOUL', 'traits': ['音樂', '可靠'], 'default_count': 0, 'effects': ['COUNTER_BACKUP_2000_LV1', 'AUTO_ON_BACKUP_TOP_CHECK_MUSIC'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06R.png', 'text': '【自】當你使用此卡的『助太刀』時，你將自己的牌組上方1張公開。那張卡片是《音樂》的角色的話加到手牌，你選擇自己的手牌1張，放到休息室。如果不是的話放回原位。\n【起】【反擊】助太刀2000 等級1 ［(1) 手牌的此卡放到休息室］ 你選擇自己的正在被正打的角色1張，在那回合中，攻擊力+2000。', 'base_id': 'BTR/W107-T06', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T06R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06R.png', 'https://img.bottleneko.app/BTR_W107_T06R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T06R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t06r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T06S.png', 'https://img.bottleneko.app/BTR_W107_T06S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T06S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t06s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t06s.gif']}, 'BTR/W107-046': {'id': 'BTR/W107-046', 'series': 'BTR/W107', 'name': '打卡美照 喜多郁代', 'jp_name': '映える写真 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 2, 'effects': ['AUTO_OPP_ATK_START_MOVE_BACK', 'ACT_REST_SELF_BUFF_MUSIC_1000'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046.png', 'text': '【自】當對手的攻擊階段開始時，你可以將此卡移動到後列沒有角色的格子。\n【起】［此卡【橫置】］ 你選擇自己1張《音樂》的角色，在那回合中，攻擊力+1000。', 'base_id': 'BTR/W107-046', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-046KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046.png', 'https://img.bottleneko.app/BTR_W107_046.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046.png']}, 'BTR/W107-046KBR': {'id': 'BTR/W107-046KBR', 'series': 'BTR/W107', 'name': '打卡美照 喜多郁代', 'jp_name': '映える写真 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['AUTO_OPP_ATK_START_MOVE_BACK', 'ACT_REST_SELF_BUFF_MUSIC_1000'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046KBR.png', 'text': '【自】當對手的攻擊階段開始時，你可以將此卡移動到後列沒有角色的格子。\n【起】［此卡【橫置】］ 你選擇自己1張《音樂》的角色，在那回合中，攻擊力+1000。', 'base_id': 'BTR/W107-046', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-046KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046KBR.png', 'https://img.bottleneko.app/BTR_W107_046KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_046KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_046kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_046S.png', 'https://img.bottleneko.app/BTR_W107_046S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_046S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_046s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_046s.gif']}, 'BTR/W107-089': {'id': 'BTR/W107-089', 'series': 'BTR/W107', 'name': '開始轉動的故事 後藤一里', 'jp_name': '動き出す物語 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 2, 'effects': ['AUTO_ON_PLAY_DISCARD_MUSIC_SEARCH_VOCAL_KITA'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089.png', 'text': '【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從手牌放到舞台時，你可以支付費用。這樣做的話，你從自己的牌組選擇「主唱吉他手 喜多郁代」最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-089', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-089KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089.png', 'https://img.bottleneko.app/BTR_W107_089.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089.png']}, 'BTR/W107-089KBR': {'id': 'BTR/W107-089KBR', 'series': 'BTR/W107', 'name': '開始轉動的故事 後藤一里', 'jp_name': '動き出す物語 後藤ひとり', 'type': 'CHAR', 'color': '紅', 'level': 0, 'cost': 0, 'power': 2500, 'soul': 1, 'trigger': 'NONE', 'traits': ['音樂'], 'default_count': 0, 'effects': ['AUTO_ON_PLAY_DISCARD_MUSIC_SEARCH_VOCAL_KITA'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089KBR.png', 'text': '【自】［手牌1張《音樂》的角色放到休息室］ 當此卡從手牌放到舞台時，你可以支付費用。這樣做的話，你從自己的牌組選擇「主唱吉他手 喜多郁代」最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-089', 'is_high_rarity': True, 'rarity': 'KBR', 'high_rarity_id': 'BTR/W107-089KBR', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089KBR.png', 'https://img.bottleneko.app/BTR_W107_089KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_089KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_089kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089kbr.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_089S.png', 'https://img.bottleneko.app/BTR_W107_089S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_089S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_089s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_089s.gif']}, 'BTR/W107-069': {'id': 'BTR/W107-069', 'series': 'BTR/W107', 'name': '對於不憧憬的憧憬 喜多郁代', 'jp_name': '憧れなかった憧れ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 4, 'effects': ['CONT_EARLY_PLAY_4MUSIC', 'CONT_CANNOT_PLAY_BACKUP', 'AUTO_ON_PLAY_HEAL'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069.png', 'text': '【永】其他的你的《音樂》的角色有4張以上的話，你的手牌的此卡的等級-1。\n【永】此卡戰鬥中，對手不能從手牌使用『助太刀』。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。', 'base_id': 'BTR/W107-069', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-069SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069.png', 'https://img.bottleneko.app/BTR_W107_069.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069.png']}, 'BTR/W107-069SSP': {'id': 'BTR/W107-069SSP', 'series': 'BTR/W107', 'name': '對於不憧憬的憧憬 喜多郁代', 'jp_name': '憧れなかった憧れ 喜多郁代', 'type': 'CHAR', 'color': '紅', 'level': 3, 'cost': 2, 'power': 8500, 'soul': 2, 'trigger': 'SOUL', 'traits': ['音樂', '高人氣'], 'default_count': 0, 'effects': ['CONT_EARLY_PLAY_4MUSIC', 'CONT_CANNOT_PLAY_BACKUP', 'AUTO_ON_PLAY_HEAL'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SSP.png', 'text': '【永】其他的你的《音樂》的角色有4張以上的話，你的手牌的此卡的等級-1。\n【永】此卡戰鬥中，對手不能從手牌使用『助太刀』。\n【自】此卡從手牌放置到舞台時，你可以將自己時鐘區上方1張卡片放到休息室。', 'base_id': 'BTR/W107-069', 'is_high_rarity': True, 'rarity': 'SSP', 'high_rarity_id': 'BTR/W107-069SSP', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SSP.png', 'https://img.bottleneko.app/BTR_W107_069SSP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069SSP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069ssp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069ssp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069SP.png', 'https://img.bottleneko.app/BTR_W107_069SP.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069SP.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069sp.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069sp.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069S.png', 'https://img.bottleneko.app/BTR_W107_069S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069s.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_069KBR.png', 'https://img.bottleneko.app/BTR_W107_069KBR.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_069KBR.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_069kbr.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_069kbr.gif']}, 'BTR/W107-T10': {'id': 'BTR/W107-T10', 'series': 'BTR/W107', 'name': '樂團名「團結Band」', 'jp_name': 'バンド名「結束バンド」', 'type': 'EVENT', 'color': '黃', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 4, 'effects': ['EVENT_SEARCH_MUSIC_OR_CX'], 'url': 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10.png', 'text': '你從自己的牌組選擇《音樂》的角色或名場面最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-T10', 'is_high_rarity': False, 'rarity': 'R', 'high_rarity_id': 'BTR/W107-T10R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10.png', 'https://img.bottleneko.app/BTR_W107_T10.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10.png']}, 'BTR/W107-T10R': {'id': 'BTR/W107-T10R', 'series': 'BTR/W107', 'name': '樂團名「團結Band」', 'jp_name': 'バンド名「結束バンド」', 'type': 'EVENT', 'color': '黃', 'level': 1, 'cost': 1, 'power': 0, 'soul': 0, 'trigger': 'NONE', 'traits': [], 'default_count': 0, 'effects': ['EVENT_SEARCH_MUSIC_OR_CX'], 'url': 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10R.png', 'text': '你從自己的牌組選擇《音樂》的角色或名場面最多1張給對手確認，加到手牌，將那個牌組洗牌。', 'base_id': 'BTR/W107-T10', 'is_high_rarity': True, 'rarity': 'RRR', 'high_rarity_id': 'BTR/W107-T10R', 'parallel_urls': ['https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10R.png', 'https://img.bottleneko.app/BTR_W107_T10R.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T10R.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t10r.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10r.gif', 'https://img.bottleneko.app/w_900,f_webp&q_80/BTR_W107_T10S.png', 'https://img.bottleneko.app/BTR_W107_T10S.png', 'https://img.bottleneko.app/w_360,f_webp&q_80/BTR_W107_T10S.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107_td/btr_w107_t10s.png', 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/b/btr_w107/btr_w107_t10s.gif']}}

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


def _natural_card_sort_key(cid: str) -> tuple:
    """依卡號自然排序：一般卡號 (001 -> 001S -> 001SP -> 002) 優先於預組 (T01) 與 PR 卡 (P01)"""
    s = str(cid or "").strip()
    right = s.split("-", 1)[1] if "-" in s else s
    m = re.match(r"^([A-Za-z]*)(\d+)([A-Za-z]*)$", right)
    if m:
        pref, num_s, suf = m.group(1).upper(), int(m.group(2)), m.group(3).upper()
        cat_order = 0 if pref == "" else (1 if pref == "T" else 2)
        suf_order = {"": 0, "R": 1, "S": 2, "SR": 2, "RRR": 3, "OFR": 4, "SP": 5, "SSP": 6, "SEC": 7}.get(suf, 8)
        return (s.split("-")[0].upper(), cat_order, pref, num_s, suf_order, suf)
    return (s.upper(), 9, "", 9999, 9, s)


BUILTIN_SERIES_TITLES = {
    "BFR/S78": "怕痛的我，把防禦力點滿就對了 (BFR/S78)",
    "GA/S131": "GA文庫 (GA/S131)",
    "BTR/W107": "孤獨搖滾 (BTR/W107)",
}


def _is_polluted_deck_title(title_str: str) -> bool:
    t = str(title_str or "")
    return any(k in t for k in ("牌組", "優勝", "Challenge", "タイトルカップ", "デッキ", "社群"))


def _migrate_polluted_deck_to_book(deck_title: str, recipe_dict: dict):
    """若舊版曾誤將匯入的社群牌組寫入 sets/*.json，啟動時自動遷移至 custom_decks_book.json 並還原系列檔"""
    if not isinstance(recipe_dict, dict) or sum(recipe_dict.values()) != 50:
        return
    clean_name = re.sub(r"\s*\([A-Za-z0-9/_-]+\)\s*$", "", str(deck_title or "")).strip() or "貓罐子社群牌組"
    book_path = os.path.join(BASE_DIR, "custom_decks_book.json")
    settings_path = os.path.join(BASE_DIR, "user_settings.json")
    try:
        book = {}
        if os.path.exists(book_path):
            with open(book_path, "r", encoding="utf-8") as f:
                loaded_b = json.load(f)
            if isinstance(loaded_b, dict):
                book = loaded_b
        settings = {}
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                loaded_s = json.load(f)
            if isinstance(loaded_s, dict):
                settings = loaded_s
        user_names = dict(settings.get("user_deck_names") or {})
        existing_slot = next((k for k, v in user_names.items() if v == clean_name and k.startswith("BN_DECK_")), None)
        if not existing_slot:
            idx_n = 1
            while f"BN_DECK_{idx_n}" in book or f"BN_DECK_{idx_n}" in user_names:
                idx_n += 1
            existing_slot = f"BN_DECK_{idx_n}"
        book[existing_slot] = dict(recipe_dict)
        user_names[existing_slot] = clean_name
        settings["user_deck_names"] = user_names
        with open(book_path, "w", encoding="utf-8") as f:
            json.dump(book, f, ensure_ascii=False, indent=2)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_all_card_sets(sets_dir="sets"):
    """自動掃描並載入 sets/*.json 所有系列卡片資料庫，嚴格分離『系列卡池』與『玩家牌組』"""
    global CARD_DB, DEFAULT_DECK_RECIPE, SERIES_DB, SERIES_DEFAULT_DECKS
    full_sets_dir = os.path.join(BASE_DIR, sets_dir)
    os.makedirs(full_sets_dir, exist_ok=True)

    card_db = {}
    default_recipe = {}
    series_db = {}
    series_decks = {}

    for k_def, v_def in BUILTIN_SERIES_TITLES.items():
        SERIES_LABELS[k_def] = v_def

    # 內建三套預設套牌固定由 FALLBACK_CARD_DB 提供，永不被外部檔案覆蓋
    for cid, cinfo in FALLBACK_CARD_DB.items():
        scode = _infer_series_code(cid, cinfo, "BFR/S78")
        if cinfo.get("default_count", 0) > 0:
            series_decks.setdefault(scode, {})[cid] = cinfo["default_count"]

    search_patterns = [
        os.path.join(full_sets_dir, "*.json"),
        os.path.join(BASE_DIR, "BFR_S78.json"),
        os.path.join(BASE_DIR, "GA_S131.json"),
        os.path.join(BASE_DIR, "BTR_W107.json"),
    ]
    extra_deck_cards_paths = []

    for pattern in search_patterns:
        for path in sorted(glob.glob(pattern)):
            fname = os.path.basename(path)
            if fname.startswith("_"):
                extra_deck_cards_paths.append(path)
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    continue
                file_stem = os.path.splitext(fname)[0]
                explicit_series = data.get("series_code") or data.get("series_name") or ""
                if not explicit_series and file_stem in ("BFR_S78", "GA_S131", "BTR_W107"):
                    explicit_series = file_stem.replace("_", "/")

                cards_dict = data.get("cards", data) if "cards" in data and isinstance(data.get("cards"), dict) else data
                if not isinstance(cards_dict, dict):
                    continue

                # 自動修復曾被舊版牌組匯入覆寫的 series_title 與 default_deck_recipe
                needs_resave = False
                raw_title = str(data.get("series_title") or "")
                if _is_polluted_deck_title(raw_title):
                    if isinstance(data.get("default_deck_recipe"), dict) and sum(data["default_deck_recipe"].values()) == 50:
                        _migrate_polluted_deck_to_book(raw_title, data["default_deck_recipe"])
                    clean_s = explicit_series or file_stem.replace("_", "/")
                    data["series_title"] = BUILTIN_SERIES_TITLES.get(clean_s, f"系列 ({clean_s})")
                    raw_title = data["series_title"]
                    needs_resave = True

                if "cards" in data and isinstance(data.get("default_deck_recipe"), dict) and data["default_deck_recipe"]:
                    if explicit_series not in ("BFR/S78", "GA/S131", "BTR/W107") or len(cards_dict) > 40:
                        data["default_deck_recipe"] = {}
                        needs_resave = True

                # 若該系列已匯入完整卡表 (>40張)，移除舊版誤塞入的 BFR/S78-058SP 等非官方卡號並依卡號自然排序
                if len(cards_dict) > 40 and "BFR/S78-058SP" in cards_dict:
                    cards_dict.pop("BFR/S78-058SP", None)
                    needs_resave = True

                if explicit_series and raw_title and not _is_polluted_deck_title(raw_title):
                    SERIES_LABELS[explicit_series] = raw_title
                elif explicit_series in BUILTIN_SERIES_TITLES:
                    SERIES_LABELS[explicit_series] = BUILTIN_SERIES_TITLES[explicit_series]

                sorted_items = sorted(
                    [(k, v) for k, v in cards_dict.items() if isinstance(v, dict) and "name" in v],
                    key=lambda kv: _natural_card_sort_key(kv[0]),
                )
                if "cards" in data and len(sorted_items) > 40 and list(cards_dict.keys()) != [k for k, _ in sorted_items]:
                    data["cards"] = {k: v for k, v in sorted_items}
                    needs_resave = True

                if needs_resave and "cards" in data:
                    try:
                        with open(path, "w", encoding="utf-8") as fw:
                            json.dump(data, fw, ensure_ascii=False, indent=2)
                    except Exception:
                        pass

                for cid, cinfo in sorted_items:
                    scode = explicit_series or _infer_series_code(cid, cinfo, file_stem)
                    cinfo["series"] = scode
                    if len(sorted_items) > 40:
                        cinfo["default_count"] = 0
                    if "translate_jp_ws_text_to_zh" in globals():
                        raw_t = cinfo.get("text", cinfo.get("effect", ""))
                        if not raw_t and cid in FALLBACK_CARD_DB:
                            raw_t = FALLBACK_CARD_DB[cid].get("text", "")
                            cinfo["text"] = raw_t
                        if _has_japanese_kana(raw_t) or "控え室" in raw_t or "山札" in raw_t:
                            cinfo["text"] = translate_jp_ws_text_to_zh(raw_t)
                            cinfo["parsed_abilities"] = []
                        if _has_japanese_kana(cinfo.get("name", "")):
                            cinfo["name"] = translate_jp_ws_name_to_zh(cinfo["name"])
                        if cinfo.get("traits"):
                            cinfo["traits"] = [translate_jp_ws_trait_to_zh(t) for t in cinfo["traits"]]
                        cinfo["parallel_urls"] = build_universal_ws_image_urls(cid, cinfo)
                    # 強制矯正 BFR/S78-077 Boss級怪物 為木門 (DOOR) 與全體+1000/+1魂
                    if cid in ("BFR/S78-077", "BFR/S78-077R") or cinfo.get("base_id") == "BFR/S78-077":
                        cinfo["trigger"] = "DOOR"
                        cinfo["effects"] = ["CX_ALL_1000_1SOUL"]
                        cinfo["text"] = "【永】你的角色全部，攻擊力+1000，魂傷+1。\n木門：當你判定出此卡時，你可以選擇自己休息室的角色1張，回到手牌。"
                    if "ChineseEffectParser" in globals():
                        raw_eff_text = cinfo.get("text", cinfo.get("effect", ""))
                        c_type = cinfo.get("type", "CHAR")
                        cinfo["parsed_abilities"] = ChineseEffectParser.parse_card_effects(raw_eff_text, c_type)
                        inferred_tags = ChineseEffectParser.infer_effect_tags(raw_eff_text, c_type, cinfo.get("trigger", "NONE"))
                        cur_tags = list(cinfo.get("effects", cinfo.get("effect_tags", [])))
                        for itag in inferred_tags:
                            if itag not in cur_tags:
                                cur_tags.append(itag)
                        cinfo["effects"] = cur_tags
                    card_db[cid] = cinfo
                    series_db.setdefault(scode, {})[cid] = cinfo
            except Exception as e:
                print(f"讀取系列檔 {path} 失敗: {e}")

    # 記錄已從外部完整匯入的系列（超過 40 張卡者不再混入 FALLBACK_CARD_DB 卡片，確保系列張數 100% 精準）
    full_imported_series = {sc for sc, smap in series_db.items() if len(smap) > 40}

    # 確保內建的 BFR/S78、GA/S131、BTR/W107 預設卡片存在於 CARD_DB（供預設套牌對戰使用）
    for cid, cinfo in FALLBACK_CARD_DB.items():
        scode = _infer_series_code(cid, cinfo, "BFR/S78")
        cinfo["series"] = scode
        if cid not in card_db:
            card_db[cid] = cinfo
        if scode not in full_imported_series and cid not in series_db.get(scode, {}):
            series_db.setdefault(scode, {})[cid] = card_db[cid]

    # 載入僅供已匯入牌組使用的額外卡片快取（_deck_extra_cards.json），絕不汙染或改變 SERIES_DB 系列卡池
    for extra_path in extra_deck_cards_paths:
        try:
            with open(extra_path, "r", encoding="utf-8") as f:
                ex_data = json.load(f)
            ex_cards = ex_data.get("cards", ex_data) if isinstance(ex_data, dict) else {}
            if isinstance(ex_cards, dict):
                for cid, cinfo in ex_cards.items():
                    if isinstance(cinfo, dict) and "name" in cinfo and cid not in card_db:
                        if "ChineseEffectParser" in globals():
                            raw_eff_text = cinfo.get("text", cinfo.get("effect", ""))
                            c_type = cinfo.get("type", "CHAR")
                            cinfo["parsed_abilities"] = ChineseEffectParser.parse_card_effects(raw_eff_text, c_type)
                            cinfo["effects"] = ChineseEffectParser.infer_effect_tags(raw_eff_text, c_type, cinfo.get("trigger", "NONE"))
                        card_db[cid] = cinfo
        except Exception:
            pass

    # 對每個系列卡池進行自然卡號排序
    for sc in list(series_db.keys()):
        series_db[sc] = dict(sorted(series_db[sc].items(), key=lambda kv: _natural_card_sort_key(kv[0])))

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


# (將於 ChineseEffectParser 定義完成後統一執行 load_all_card_sets)


class CardInstance:
    """單張實體卡片狀態與暫時加成屬性（支援高低版本異畫卡圖共用規則基準 ID）"""

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
        self.text = data.get("text", data.get("effect", ""))
        raw_effects = list(data.get("effects", data.get("effect_tags", [])))
        if "ChineseEffectParser" in globals():
            for itag in ChineseEffectParser.infer_effect_tags(self.text, self.type, self.trigger):
                if itag not in raw_effects:
                    raw_effects.append(itag)
            fresh_parsed = ChineseEffectParser.parse_card_effects(self.text, self.type)
            self.parsed_abilities = fresh_parsed if fresh_parsed else list(data.get("parsed_abilities") or [])
        else:
            self.parsed_abilities = list(data.get("parsed_abilities") or [])
        self.effects = raw_effects
        self.effect_tags = self.effects
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
        if stage_idx is None and card in p.hand and getattr(card, "parsed_abilities", None):
            for ab in card.parsed_abilities:
                if ab.get("category") == "CONT":
                    eff = ab.get("effect")
                    if eff == "early_play_stage_4":
                        if sum(1 for c in p.stage if c is not None) >= 4:
                            return max(0, card.base_level + ab.get("level_mod", -1))
                    elif eff == "early_play_wr_cx_2_or_less":
                        if sum(1 for c in p.waiting_room if c.type == "CX") <= 2:
                            return max(0, card.base_level + ab.get("level_mod", -1))
                    elif eff == "early_play_wr_cx_6_or_more":
                        if sum(1 for c in p.waiting_room if c.type == "CX") >= 6:
                            return max(0, card.base_level + ab.get("level_mod", -1))
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

        if p.climax_zone:
            if (
                p.climax_zone.has_effect("CX_ALL_1000_1SOUL")
                or p.climax_zone.id in ["BFR/S78-077", "BFR/S78-077R", "BFR/S78-107", "BFR/S78-107R", "GA10/S131-030", "GA10/S131-030R", "GA17/S131-033", "GA17/S131-033R"]
                or any(ab.get("effect") == "climax_1k1" for ab in getattr(p.climax_zone, "parsed_abilities", []))
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

        # [萬用資料驅動 CONT 效果結算] 若非既有硬編碼特例，自動套用 parsed_abilities
        HARDCODED_CONT_IDS = {
            "BFR/S78-073", "BFR/S78-058", "BFR/S78-089", "BFR/S78-102",
            "BTR/W107-076", "BTR/W107-075", "BTR/W107-T16", "BTR/W107-T13",
            "GA04/S131-100", "GA17/S131-015", "GA17/S131-017", "GA10/S131-T09"
        }
        if card.id not in HARDCODED_CONT_IDS:
            for ab in getattr(card, "parsed_abilities", []):
                if ab.get("category") == "CONT":
                    eff = ab.get("effect")
                    if ab.get("my_turn_only") and not is_my_turn:
                        continue
                    if ab.get("opp_turn_only") and is_my_turn:
                        continue
                    if eff == "per_other_char_buff":
                        other_cnt = sum(1 for i, c in enumerate(p.stage) if i != stage_idx and c is not None)
                        pwr += other_cnt * ab.get("power", 500)
                    elif eff == "per_opp_backrow_buff" and opp:
                        opp_b = sum(1 for i in [3, 4] if opp.stage[i] is not None)
                        pwr += opp_b * ab.get("power", 500)
                    elif eff == "per_opp_frontrow_buff" and opp:
                        opp_f = sum(1 for i in [0, 1, 2] if opp.stage[i] is not None)
                        pwr += opp_f * ab.get("power", 500)
                    elif eff == "per_marker_buff":
                        pwr += len(card.markers) * ab.get("power", 1000)
                    elif eff == "has_marker_buff":
                        if len(card.markers) > 0:
                            pwr += ab.get("power", 1000)
                    elif eff == "hand_min_buff":
                        if len(p.hand) >= ab.get("min_hand", 5):
                            pwr += ab.get("power", 1000)
                    elif eff == "stock_min_buff":
                        if len(p.stock) >= ab.get("min_stock", 3):
                            pwr += ab.get("power", 1000)
                    elif eff == "memory_has_buff":
                        if len(p.memory) > 0:
                            pwr += ab.get("power", 1000)
                    elif eff == "experience_buff":
                        exp_sum = sum(c.base_level for c in p.level_zone)
                        if exp_sum >= ab.get("min_exp", 2):
                            pwr += ab.get("power", 1000)
                    elif eff == "other_char_count_buff":
                        other_cnt = sum(1 for i, c in enumerate(p.stage) if i != stage_idx and c is not None)
                        if other_cnt >= ab.get("min_count", 2):
                            pwr += ab.get("power", 1000)
                    elif eff == "other_char_max_buff":
                        other_cnt = sum(1 for i, c in enumerate(p.stage) if i != stage_idx and c is not None)
                        if other_cnt <= ab.get("max_count", 1):
                            pwr += ab.get("power", 1000)
                    elif eff == "my_turn_self_buff" and is_my_turn:
                        pwr += ab.get("power", 1000)
                    elif eff == "opp_turn_self_buff" and (not is_my_turn):
                        pwr += ab.get("power", 1000)
                    elif eff == "flat_self_buff":
                        pwr += ab.get("power", 1000)

        # 檢查舞台上其他角色的萬用應援與光環 (assist_level / assist_flat / global_other_buff / front_center_other_buff / named_other_buff)
        char_lvl = RuleEngine.get_effective_level(p, card, stage_idx)
        for i, other_c in enumerate(p.stage):
            if other_c is None or i == stage_idx or other_c.id in HARDCODED_CONT_IDS:
                continue
            for ab in getattr(other_c, "parsed_abilities", []):
                if ab.get("category") == "CONT":
                    eff = ab.get("effect")
                    if ab.get("my_turn_only") and not is_my_turn:
                        continue
                    if ab.get("opp_turn_only") and is_my_turn:
                        continue
                    if eff == "front_center_other_buff":
                        if stage_idx == 1 and char_lvl <= ab.get("max_level", 99):
                            pwr += ab.get("power", 1000)
                    elif eff == "named_other_buff":
                        t_name = ab.get("target_name", "")
                        if t_name and t_name in card.name:
                            pwr += ab.get("power", 1000)
                    elif eff == "global_other_buff":
                        if ab.get("front_only") and stage_idx not in [0, 1, 2]:
                            continue
                        if char_lvl <= ab.get("max_level", 99):
                            pwr += ab.get("power", 500)
                    elif eff == "assist_flat":
                        if (i == 3 and stage_idx in [0, 1]) or (i == 4 and stage_idx in [1, 2]):
                            pwr += ab.get("power", 500)
                    elif eff == "assist_level":
                        if (i == 3 and stage_idx in [0, 1]) or (i == 4 and stage_idx in [1, 2]):
                            pwr += char_lvl * ab.get("multiplier", 500)

        return pwr

    @staticmethod
    def get_effective_soul(p: PlayerState, card: CardInstance, stage_idx: int, opp: PlayerState = None, is_my_turn: bool = True) -> int:
        if not card or card.type != "CHAR":
            return 0
        soul = card.base_soul + card.temp_soul
        if p.climax_zone:
            if (
                p.climax_zone.has_effect("CX_ALL_1000_1SOUL")
                or p.climax_zone.id in ["BFR/S78-077", "BFR/S78-077R", "BFR/S78-107", "BFR/S78-107R", "GA10/S131-030", "GA10/S131-030R", "GA17/S131-033", "GA17/S131-033R"]
                or any(ab.get("effect") == "climax_1k1" for ab in getattr(p.climax_zone, "parsed_abilities", []))
            ):
                soul += 1
            elif (
                p.climax_zone.has_effect("CX_ALL_2SOUL")
                or any(ab.get("effect") == "climax_2soul" for ab in getattr(p.climax_zone, "parsed_abilities", []))
            ):
                soul += 2
        if card.name == "主唱吉他手 喜多郁代" or card.id == "BTR/W107-T16":
            bocchi_support = sum(
                1
                for i, c in enumerate(p.stage)
                if i != stage_idx
                and c
                and (c.has_effect("CONT_BUFF_VOCAL_KITA_1000_1SOUL") or c.id == "BTR/W107-T13")
            )
            soul += bocchi_support
        # 其他角色的萬用 CONT 魂傷加成
        for i, other_c in enumerate(p.stage):
            if other_c is None or i == stage_idx or other_c.id == "BTR/W107-T13":
                continue
            for ab in getattr(other_c, "parsed_abilities", []):
                if ab.get("category") == "CONT" and ab.get("soul", 0) > 0:
                    eff = ab.get("effect")
                    if eff == "global_other_buff":
                        soul += ab.get("soul", 0)
                    elif eff == "named_other_buff" and ab.get("target_name", "") in card.name:
                        soul += ab.get("soul", 0)
                    elif eff == "front_center_other_buff" and stage_idx == 1:
                        soul += ab.get("soul", 0)
        # 對手正對面角色的永續減魂（如 身捧ぐ慈愛 メイプル）
        if opp and stage_idx in [0, 1, 2] and opp.stage[stage_idx]:
            opp_front = opp.stage[stage_idx]
            soul -= getattr(opp_front, "temp_front_opp_soul_penalty", 0)
            for ab in getattr(opp_front, "parsed_abilities", []):
                if ab.get("category") == "CONT" and ab.get("effect") == "front_opp_soul_penalty":
                    soul -= ab.get("penalty", 1)
        return max(0, soul)

    @staticmethod
    def can_play_card(p: PlayerState, card: CardInstance) -> bool:
        eff_lvl = RuleEngine.get_effective_level(p, card, None)
        if card.type in ["CHAR", "EVENT"]:
            if eff_lvl > len(p.level_zone) or card.cost > len(p.stock):
                return False
            if (
                card.has_effect("CONT_IGNORE_SELF_COLOR")
                or card.id == "GA01/S131-115"
                or any(ab.get("effect") == "ignore_color" and ab.get("target") == "all" for ab in getattr(card, "parsed_abilities", []))
            ):
                return True
            if eff_lvl >= 1:
                colors = {c.color for c in p.level_zone + p.clock}
                if card.color not in colors:
                    return False
            return True
        elif card.type == "CX":
            if any(
                c and (
                    c.has_effect("CONT_IGNORE_CX_COLOR")
                    or c.id == "BFR/S78-031"
                    or any(ab.get("effect") == "ignore_color" for ab in getattr(c, "parsed_abilities", []))
                )
                for c in p.stage
            ):
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


def _launch_from_any_file():
    try:
        from main import launch_game
        launch_game()
        return
    except ImportError:
        pass
    import tempfile
    import zipfile
    search_dirs = [
        BASE_DIR,
        os.path.dirname(BASE_DIR),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
    ]
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for root_d, _, files in os.walk(sdir):
            for fname in files:
                if fname.lower().endswith(".zip"):
                    zpath = os.path.join(root_d, fname)
                    try:
                        with zipfile.ZipFile(zpath, "r") as zf:
                            if any(n.endswith("main.py") for n in zf.namelist()):
                                target_dir = os.path.join(tempfile.gettempdir(), "WS_Bofuri_Run")
                                zf.extractall(target_dir)
                                for r2, _, f2 in os.walk(target_dir):
                                    if "main.py" in f2:
                                        os.chdir(r2)
                                        sys.path.insert(0, r2)
                                        from main import launch_game
                                        launch_game()
                                        return
                    except Exception:
                        pass


if __name__ == "__main__":
    _launch_from_any_file()




# ==============================================================================
# 萬用資料驅動效果解析器與貓罐子 (BottleNeko) 全系列／分批／牌組匯入引擎
# ==============================================================================
import re
import urllib.request
import urllib.parse
import ssl


class ChineseEffectParser:
    """
    將 Weiß Schwarz 繁體中文效果文（同時相容「官方台版譯名：牌組/休息室/名場面/時鐘區/攻擊力/安可」
    與「貓罐子 BottleNeko 譯名：山札/控室/高潮區/鐘區/戰力/再場/被放置到」）自動編譯為標準化 AST 結構 (parsed_abilities)，
    支援多子句複合效果（永/自/起/反擊/事件/名場面），全面擺脫逐張寫死 if card.id == ... 的限制。
    """

    @classmethod
    def normalize_terms(cls, text: str) -> str:
        """將貓罐子 (BottleNeko) 與各種中文譯名統一正規化為模擬器內部標準術語"""
        if not text:
            return ""
        t = str(text)
        replacements = [
            ("山札頂", "牌組上方"),
            ("山札上方", "牌組上方"),
            ("卡組頂", "牌組上方"),
            ("卡組上方", "牌組上方"),
            ("山札底", "牌組下方"),
            ("卡組底", "牌組下方"),
            ("卡組下方", "牌組下方"),
            ("山札", "牌組"),
            ("卡組", "牌組"),
            ("控室", "休息室"),
            ("控え室", "休息室"),
            ("高潮區", "名場面區"),
            ("CX區", "名場面區"),
            ("クライマックス置場", "名場面區"),
            ("高潮卡", "名場面"),
            ("高潮", "名場面"),
            ("クライマックス", "名場面"),
            ("鐘區", "時鐘區"),
            ("時計區", "時鐘區"),
            ("時计区", "時鐘區"),
            ("傷害區", "時鐘區"),
            ("クロック置場", "時鐘區"),
            ("クロック", "時鐘區"),
            ("庫存區", "能量區"),
            ("ストック置場", "能量區"),
            ("ストック", "能量區"),
            ("記憶區", "回憶區"),
            ("思出區", "回憶區"),
            ("思い出置場", "回憶區"),
            ("戰力", "攻擊力"),
            ("力量", "攻擊力"),
            ("パワー", "攻擊力"),
            ("再場", "安可"),
            ("再登場", "安可"),
            ("再演", "安可"),
            ("アンコール", "安可"),
            ("被放置到", "被放到"),
            ("放置到", "放到"),
            ("被置於", "被放到"),
            ("置於", "放到"),
            ("置入", "放到"),
            ("放上", "放到"),
            ("上場時", "被放到舞台時"),
            ("登場到舞台時", "被放到舞台時"),
            ("登場時", "被放到舞台時"),
            ("加入手牌", "加到手牌"),
            ("返回手牌", "回到手牌"),
            ("返回牌組", "回到牌組"),
            ("返回卡組", "回到牌組"),
            ("【起】【反擊】", "【起】 助太刀"),
            ("【CXコンボ】", "【CX連動】"),
            ("【高潮連動】", "【CX連動】"),
            ("靈魂值", "魂傷"),
            ("靈魂", "魂傷"),
            ("ソウル", "魂傷"),
            ("魂+", "魂傷+"),
            ("魂＋", "魂傷+"),
            ("魂-", "魂傷-"),
            ("魂－", "魂傷-"),
            ("正面攻擊", "正打"),
            ("側面攻擊", "側打"),
            ("側擊", "側打"),
            ("給予對手", "給對手造成"),
            ("給對手", "給對手造成"),
            ("造成造成", "造成"),
            ("點傷害", "傷害"),
        ]
        for old_w, new_w in replacements:
            t = t.replace(old_w, new_w)
        # 統一將獨立的 CX（排除【CX連動】）轉為名場面
        t = re.sub(r"(?<!【)CX(?!連動)", "名場面", t)
        t = re.sub(r"造成(\d+)傷害", r"造成\1點傷害", t)
        return t

    @classmethod
    def infer_effect_tags(cls, effect_text: str, card_type: str = "CHAR", trigger: str = "NONE") -> list:
        """根據效果文與卡片類型自動推導標準化效果標籤 (effects_tags)"""
        tags = []
        if not effect_text:
            return tags
        norm = cls.normalize_terms(effect_text)
        if card_type == "CX":
            if ("角色全部" in norm or "全部的角色" in norm or "所有的角色" in norm) and "1000" in norm and "魂傷+1" in norm:
                tags.append("CX_ALL_1000_1SOUL")
            elif ("角色全部" in norm or "全部的角色" in norm or "所有的角色" in norm) and ("魂傷+2" in norm or "魂傷＋2" in norm):
                tags.append("CX_ALL_2SOUL")
            if trigger == "STANDBY" or "執行開機的效果" in norm or "開機：" in norm or "スタンバイ" in effect_text:
                if "CX_STANDBY" not in tags:
                    tags.append("CX_STANDBY")
            if "抽1張" in norm and "2000" in norm:
                tags.append("CX_DRAW1_2000_1SOUL")
            elif "抽1張" in norm and "1000" in norm and ("角色全部" in norm or "全部的角色" in norm):
                tags.append("CX_DRAW1_ALL_1000_1SOUL")
            elif "放到能量區" in norm and ("手牌被放到名場面區時" in norm or "手牌放到名場面區時" in norm):
                if "休息室" in norm:
                    tags.append("CX_WR_STOCK1_ALL_1SOUL")
                else:
                    tags.append("CX_STOCK1_ALL_1SOUL")
        return tags

    @classmethod
    def parse_card_effects(cls, effect_text: str, card_type: str = "CHAR") -> list:
        if not effect_text or effect_text.strip() == "（無特殊效果）":
            return []
        norm_text = cls.normalize_terms(effect_text)
        abilities = []
        raw_lines = [line.strip() for line in str(effect_text).replace("\r\n", "\n").split("\n") if line.strip()]
        norm_lines = [line.strip() for line in norm_text.replace("\r\n", "\n").split("\n") if line.strip()]

        for idx, line in enumerate(norm_lines):
            orig_line = raw_lines[idx] if idx < len(raw_lines) else line
            # 略過純觸發標記說明行（如 木門：當你判定出此卡時...）
            if re.match(r"^(木門|開機|城門|箭頭|金磚|書|金袋|風|射擊|寶物|門|袋|電源|選擇)：", line):
                continue
            if line.startswith("【永】") or line.startswith("[永]"):
                abilities.extend(cls._parse_cont(line, orig_line, card_type))
            elif line.startswith("【自】") or line.startswith("[自]"):
                abilities.extend(cls._parse_auto(line, orig_line, card_type))
            elif line.startswith("【起】") or line.startswith("[起]"):
                abilities.extend(cls._parse_act(line, orig_line, card_type))
            elif line.startswith("【反擊】") or line.startswith("[反擊]"):
                abilities.extend(cls._parse_counter_event(line, orig_line))
            elif card_type == "EVENT":
                abilities.extend(cls._parse_main_event(line, orig_line))
            elif card_type == "CX":
                abilities.extend(cls._parse_auto("【自】" + line, orig_line, card_type))
        return abilities

    @classmethod
    def _parse_cost(cls, line: str) -> dict:
        cost = {
            "stock": 0,
            "discard_hand": 0,
            "discard_cx": 0,
            "clock_top_deck": 0,
            "rest_self": 0,
            "send_self_wr": False,
            "send_self_memory": False,
            "return_self_hand": False,
            "sac_other_stage": 0,
            "send_cx_wr": False,
        }
        # 擷取能力前段括號內的代價（排除『...』引號內部授予能力之括號）
        prefix_line = line.split("『")[0]
        sq_matches = [m[0] or m[1] for m in re.findall(r"［([^］]+)］|\[([^\]]+)\]", prefix_line)]
        if sq_matches:
            cost_str = " ".join(sq_matches)
        else:
            p_matches = re.findall(r"[\(（]([^\)）]+)[\)）]", prefix_line)
            if not p_matches:
                return cost
            cost_str = " ".join(p_matches)
        m_stock = re.search(r"(?:^|[^\d])([1-9])(?:$|[^\d張枚點級])", cost_str)
        m_paren_stock = re.search(r"[\(（](\d+)[\)）]", prefix_line)
        if m_paren_stock:
            cost["stock"] = int(m_paren_stock.group(1))
        elif m_stock and f"({m_stock.group(1)})" in prefix_line:
            cost["stock"] = int(m_stock.group(1))
        elif "①" in cost_str:
            cost["stock"] = 1
        elif "②" in cost_str:
            cost["stock"] = 2
        elif "③" in cost_str:
            cost["stock"] = 3
        elif "④" in cost_str:
            cost["stock"] = 4

        if "手牌1張名場面" in cost_str or "手牌的名場面1張" in cost_str or "1張名場面從手牌放到休息室" in cost_str:
            cost["discard_cx"] = 1
        else:
            m_dh = re.search(r"手牌.*?(\d+)張.*?放到休息室", cost_str)
            if not m_dh:
                m_dh = re.search(r"(\d+)張手牌.*?放到休息室", cost_str)
            if m_dh:
                cost["discard_hand"] = int(m_dh.group(1))
            elif "手牌放到休息室" in cost_str:
                cost["discard_hand"] = 1

        if "牌組上方1張放到時鐘區" in cost_str or "牌組上方1張卡放到時鐘區" in cost_str:
            cost["clock_top_deck"] = 1

        if "此卡【橫置】" in cost_str or "將此卡【橫置】" in cost_str:
            cost["rest_self"] = 1
        if "2張【橫置】" in cost_str:
            cost["rest_self"] = 2

        if "此卡放到休息室" in cost_str or "手牌的此卡放到休息室" in cost_str:
            cost["send_self_wr"] = True
        if "此卡放到回憶區" in cost_str:
            cost["send_self_memory"] = True
        if "此卡回到手牌" in cost_str:
            cost["return_self_hand"] = True
        if "其他的你的舞台的角色1張放到休息室" in cost_str or "其他的你的角色1張放到休息室" in cost_str:
            cost["sac_other_stage"] = 1
        if "名場面區的" in cost_str and "放到休息室" in cost_str:
            cost["send_cx_wr"] = True
        return cost

    @classmethod
    def _parse_cont(cls, line: str, orig_line: str, card_type: str = "CHAR") -> list:
        res = []
        my_turn_only = ("你的回合中" in line)
        opp_turn_only = ("對手的回合中" in line)

        # 0. 名場面全體 +1000/+1魂 或 +2魂
        if ("你所有的角色" in line or "你全部的角色" in line or "你的角色全部" in line or "自己的角色全部" in line):
            if "1000" in line and ("魂傷+1" in line or "魂傷＋1" in line):
                res.append({"category": "CONT", "effect": "climax_1k1", "power": 1000, "soul": 1, "raw": orig_line})
                return res
            if "魂傷+2" in line or "魂傷＋2" in line:
                res.append({"category": "CONT", "effect": "climax_2soul", "soul": 2, "raw": orig_line})
                return res

        # 1. 應援 等級×X (也可能同時帶有固定應援或等級+1)
        m_lv_assist = re.search(r"應援.*等級[×xX\*](\d+)", line)
        if m_lv_assist:
            res.append({"category": "CONT", "effect": "assist_level", "multiplier": int(m_lv_assist.group(1)), "raw": orig_line})
            return res

        # 2. 應援 固定數值 +X
        m_flat_assist = re.search(r"應援.*攻擊力[＋\+](\d+)", line)
        if m_flat_assist:
            res.append({"category": "CONT", "effect": "assist_flat", "power": int(m_flat_assist.group(1)), "raw": orig_line})
            return res

        # 3. 早出し：手牌的此卡等級-1
        if ("等級-1" in line or "等級－1" in line) and "手牌" in line:
            if "4張以上" in line or "四張以上" in line:
                res.append({"category": "CONT", "effect": "early_play_stage_4", "level_mod": -1, "raw": orig_line})
                return res
            if "2張以下" in line or "兩張以下" in line:
                res.append({"category": "CONT", "effect": "early_play_wr_cx_2_or_less", "level_mod": -1, "raw": orig_line})
                return res
            if "6張以上" in line or "六張以上" in line:
                res.append({"category": "CONT", "effect": "early_play_wr_cx_6_or_more", "level_mod": -1, "raw": orig_line})
                return res
            if "回憶區" in line:
                m_mc = re.search(r"(\d+)張以上", line)
                res.append({"category": "CONT", "effect": "early_play_memory_min", "min_count": int(m_mc.group(1)) if m_mc else 1, "level_mod": -1, "raw": orig_line})
                return res

        # 4. 負面規則限制 / 無視顏色 / 封鎖助太刀 / 正面對手減魂
        if "不能側打" in line or "不可側打" in line:
            res.append({"category": "CONT", "effect": "cannot_side_attack", "raw": orig_line})
        if "不能正打" in line or "不可正打" in line:
            res.append({"category": "CONT", "effect": "cannot_front_attack", "raw": orig_line})
        if "不能移動" in line:
            res.append({"category": "CONT", "effect": "cannot_move", "raw": orig_line})
        if "不能從手牌使用『助太刀』" in line or "不能使用『助太刀』" in line:
            res.append({"category": "CONT", "effect": "cannot_play_backup", "raw": orig_line})
        if "無需滿足顏色條件" in line or "無視顏色條件" in line or "不需滿足顏色條件" in line or "無視顏色限制" in line:
            target = "climax" if "名場面" in line else "all"
            res.append({"category": "CONT", "effect": "ignore_color", "target": target, "raw": orig_line})
        m_f_soul = re.search(r"此卡正面的角色.*魂傷[－\-](\d+)", line)
        if m_f_soul:
            res.append({"category": "CONT", "effect": "front_opp_soul_penalty", "penalty": int(m_f_soul.group(1)), "raw": orig_line})

        # 5. 前列中央其他角色加成（如 BFR/S78-056 內心的表裏 蜜伊：其他的你的前列中央的等級0以下的角色，攻擊力+1000）
        if "前列中央" in line and ("其他的你的" in line or "你的前列中央" in line) and "此卡的" not in line:
            m_p = re.search(r"攻擊力[＋\+](\d+)", line)
            m_s = re.search(r"魂傷[＋\+](\d+)", line)
            m_lv = re.search(r"等級(\d+)以下", line)
            if m_p or m_s:
                res.append({
                    "category": "CONT",
                    "effect": "front_center_other_buff",
                    "power": int(m_p.group(1)) if m_p else 0,
                    "soul": int(m_s.group(1)) if m_s else 0,
                    "max_level": int(m_lv.group(1)) if m_lv else 99,
                    "my_turn_only": my_turn_only,
                    "opp_turn_only": opp_turn_only,
                    "raw": orig_line,
                })
                return res

        # 6. 指定卡名其他角色加成（如 其他的你的「...」全部，攻擊力+X）
        if "其他的你的" in line and "「" in line and "此卡的" not in line:
            m_name = re.search(r"「([^」]+)」", line)
            m_p = re.search(r"攻擊力[＋\+](\d+)", line)
            m_s = re.search(r"魂傷[＋\+](\d+)", line)
            if m_name and (m_p or m_s):
                res.append({
                    "category": "CONT",
                    "effect": "named_other_buff",
                    "target_name": m_name.group(1),
                    "power": int(m_p.group(1)) if m_p else 0,
                    "soul": int(m_s.group(1)) if m_s else 0,
                    "my_turn_only": my_turn_only,
                    "opp_turn_only": opp_turn_only,
                    "raw": orig_line,
                })
                return res

        # 7. 全體其他角色固定加成（其他的你的...角色全部，攻擊力+X）
        if "其他的你的" in line and "此卡的" not in line and "每有1張" not in line:
            m_all = re.search(r"攻擊力[＋\+](\d+)", line)
            m_s = re.search(r"魂傷[＋\+](\d+)", line)
            m_lv = re.search(r"等級(\d+)以下", line)
            if m_all or m_s:
                res.append({
                    "category": "CONT",
                    "effect": "global_other_buff",
                    "power": int(m_all.group(1)) if m_all else 0,
                    "soul": int(m_s.group(1)) if m_s else 0,
                    "max_level": int(m_lv.group(1)) if m_lv else 99,
                    "front_only": ("前列" in line),
                    "my_turn_only": my_turn_only,
                    "opp_turn_only": opp_turn_only,
                    "raw": orig_line,
                })
                return res

        # 8. 自身動態比例加成（每有1張對手後列/前列、每有1張標記、每有1張其他我方角色）
        m_opp_back = re.search(r"對手的後列.*每有1張.*攻擊力[＋\+](\d+)", line)
        if m_opp_back:
            res.append({"category": "CONT", "effect": "per_opp_backrow_buff", "power": int(m_opp_back.group(1)), "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            return res

        m_opp_front = re.search(r"對手的前列.*每有1張.*攻擊力[＋\+](\d+)", line)
        if m_opp_front:
            res.append({"category": "CONT", "effect": "per_opp_frontrow_buff", "power": int(m_opp_front.group(1)), "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            return res

        m_mk_per = re.search(r"標記每有1張.*攻擊力[＋\+](\d+)", line)
        if m_mk_per:
            m_lv_b = re.search(r"等級[＋\+](\d+)", line)
            res.append({"category": "CONT", "effect": "per_marker_buff", "power": int(m_mk_per.group(1)), "level_mod": int(m_lv_b.group(1)) if m_lv_b else 0, "raw": orig_line})
            return res

        m_per = re.search(r"其他的你的.*每有1張.*攻擊力[＋\+](\d+)", line) or re.search(r"每有1張其他的你的.*攻擊力[＋\+](\d+)", line)
        if m_per:
            res.append({
                "category": "CONT",
                "effect": "per_other_char_buff",
                "power": int(m_per.group(1)),
                "my_turn_only": my_turn_only,
                "opp_turn_only": opp_turn_only,
                "raw": orig_line,
            })
            return res

        # 9. 自身條件式固定加成（標記存在 / 手牌張數 / 能量張數 / 回憶區 / 經驗 / 其他角色張數 / 自回合 / 對手回合）
        m_self_pwr = re.search(r"此卡的?攻擊力[＋\+](\d+)", line)
        if m_self_pwr:
            pwr_val = int(m_self_pwr.group(1))
            m_lv_b = re.search(r"此卡的?等級[＋\+](\d+)", line)
            lv_val = int(m_lv_b.group(1)) if m_lv_b else 0
            m_s_b = re.search(r"此卡的?魂傷[＋\+](\d+)", line)
            soul_val = int(m_s_b.group(1)) if m_s_b else 0

            if "下方有標記" in line:
                res.append({"category": "CONT", "effect": "has_marker_buff", "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "手牌" in line and re.search(r"(\d+)張以上", line):
                mh = re.search(r"(\d+)張以上", line)
                res.append({"category": "CONT", "effect": "hand_min_buff", "min_hand": int(mh.group(1)), "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "能量區" in line and re.search(r"(\d+)張以上", line):
                ms = re.search(r"(\d+)張以上", line)
                res.append({"category": "CONT", "effect": "stock_min_buff", "min_stock": int(ms.group(1)), "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "回憶區" in line:
                res.append({"category": "CONT", "effect": "memory_has_buff", "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "經驗" in line and re.search(r"(\d+)以上", line):
                me = re.search(r"(\d+)以上", line)
                res.append({"category": "CONT", "effect": "experience_buff", "min_exp": int(me.group(1)), "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "其他的你的" in line and re.search(r"(\d+)張以上", line):
                mc = re.search(r"(\d+)張以上", line)
                res.append({"category": "CONT", "effect": "other_char_count_buff", "min_count": int(mc.group(1)), "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "其他的你的" in line and "存在的話" in line:
                res.append({"category": "CONT", "effect": "other_char_count_buff", "min_count": 1, "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "其他的你的" in line and re.search(r"(\d+)張以下", line):
                mc = re.search(r"(\d+)張以下", line)
                res.append({"category": "CONT", "effect": "other_char_max_buff", "max_count": int(mc.group(1)), "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif "你的角色全部" in line or "你全部的角色" in line:
                res.append({"category": "CONT", "effect": "other_char_count_buff", "min_count": 1, "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "my_turn_only": my_turn_only, "opp_turn_only": opp_turn_only, "raw": orig_line})
            elif opp_turn_only:
                res.append({"category": "CONT", "effect": "opp_turn_self_buff", "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "raw": orig_line})
            elif my_turn_only:
                res.append({"category": "CONT", "effect": "my_turn_self_buff", "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "raw": orig_line})
            else:
                res.append({"category": "CONT", "effect": "flat_self_buff", "power": pwr_val, "level_mod": lv_val, "soul": soul_val, "raw": orig_line})

            if "安可" in line and "手牌" in line:
                res.append({"category": "CONT", "effect": "hand_encore", "raw": orig_line})
            return res

        return res

    @classmethod
    def _extract_actions(cls, line: str, timing: str = "ON_PLAY", cost: dict = None) -> list:
        """從正規化後的效果句子中提取所有可執行動作 (actions)，支援單句複合多重效果"""
        actions = []
        cost = cost or {}
        # 去除前半段括號代價說明，避免將代價誤判為效果動作
        body = re.sub(r"^[【\[](?:自|起|永|反擊)[】\]]\s*(?:【CX連動】\s*)?(?:回合1次\s*)?(?:記憶\s*)?(?:經驗\s*)?(?:絆[／/][^［\[]+\s*)?[［\[\(（][^］\]\)）]+[］\]\)）]", "", line)

        # 0. 開機效果 (Standby)
        if "執行開機的效果" in body:
            actions.append({"action": "standby_deploy"})
            return actions

        # 1. 登場或效果回血 (Heal to WR / Stock)
        if ("時鐘區上方1張" in body or "時鐘區上方最多1張" in body or "時鐘區頂1張" in body or "時鐘區最多1張" in body or "時鐘區最上1張" in body or "回復1點" in body):
            if "放到能量區" in body:
                actions.append({"action": "heal_to_stock", "amount": 1})
            elif "放到休息室" in body or "回復1點" in body:
                actions.append({"action": "heal_to_wr", "amount": 1})

        # 2. 絆 (Bond) 回收指定卡名
        m_bond = re.search(r"絆[／/]「([^」]+)」", line)
        if m_bond:
            actions.append({"action": "salvage_wr", "target_type": "Character", "target_name": m_bond.group(1), "count": 1})

        # 3. 看牌組頂 X 張選 Y 張加手牌，其餘放休息室
        m_look = re.search(r"(?:看.*?牌組上方|牌組上方看)最多(\d+)張.*?選.*?最多(\d+)張.*?(?:加到手牌|回到手牌)", body)
        if not m_look:
            m_look = re.search(r"(?:看.*?牌組上方|牌組上方看)(\d+)張.*?選.*?最多(\d+)張.*?(?:加到手牌|回到手牌)", body)
        if m_look:
            t_type = "CHAR"
            if "名場面" in body and "角色" not in body:
                t_type = "CX"
            elif "事件" in body and "角色" not in body:
                t_type = "EVENT"
            elif "等級1以上" in body:
                t_type = "LV1_PLUS"
            elif "選最多1張卡" in body or "選擇卡片" in body:
                t_type = "ANY"
            then_disc = 1 if ("加到手牌的話" in body and "手牌1張" in body and "放到休息室" in body) else 0
            actions.append({
                "action": "look_top_add_hand",
                "look": int(m_look.group(1)),
                "pick": int(m_look.group(2)),
                "target_type": t_type,
                "then_discard": then_disc,
            })

        # 4. 占卜看牌組頂 X 張按任意順序放回牌組頂 (Scry)
        if not m_look:
            m_scry = re.search(r"看.*?牌組上方最多(\d+)張.*?(?:任意順序|放回牌組上方|放到牌組上方)", body)
            if m_scry:
                actions.append({"action": "scry_top", "count": int(m_scry.group(1))})

        # 5. 公開牌組頂 1 張，回收休息室 Lv.X 以下角色 (Dokitema) 或判定加手/放標記/彈回對手
        if "牌組上方1張公開" in body or "公開自己牌組上方1張" in body:
            if "等級X以下" in body and "休息室" in body:
                actions.append({"action": "dokitema_salvage"})
            elif "作為標記" in body:
                actions.append({"action": "top_check_marker", "min_level": 1 if "等級是1以上" in body else 0})
            elif "選擇對手" in body and "回到牌組" in body:
                actions.append({"action": "top_check_bounce_opp_deck"})
            elif "加到手牌" in body or "回到手牌" in body:
                then_disc = 1 if ("手牌1張" in body and "放到休息室" in body) else 0
                actions.append({"action": "top_check_add_hand", "then_discard": then_disc})

        # 6. 削自己牌組頂 N 張，回收等級合計 X 以下角色（如 BFR/S78-080 二人の時間 サリー）
        m_mill_sal = re.search(r"牌組上方(\d+)張，?放到休息室.*?休息室.*?等級X以下", body)
        if m_mill_sal:
            actions.append({"action": "mill_salvage_level_sum", "mill_count": int(m_mill_sal.group(1))})

        # 7. 從牌組檢索卡片加入手牌
        if not m_look and ("從自己的牌組" in body or "從牌組" in body or "選自己牌組" in body) and ("加到手牌" in body or "回到手牌" in body):
            m_lv_max = re.search(r"等級(\d+)以下", body)
            t_type = "CHAR_OR_CX" if ("角色或名場面" in body) else ("CX" if ("名場面" in body and "角色" not in body) else "CHAR")
            actions.append({
                "action": "search_deck_char",
                "count": 1,
                "max_level": int(m_lv_max.group(1)) if m_lv_max else 99,
                "target_type": t_type,
            })

        # 8. 從休息室回收角色或名場面回手牌
        if not m_look and not m_bond and "等級X以下" not in body and ("休息室" in body) and ("回到手牌" in body or "加到手牌" in body):
            after_trigger = body.split("時，")[-1] if "時，" in body else body
            if any(k in after_trigger for k in ("休息室的", "從自己的休息室", "從休息室", "選自己休息室")):
                t_type = "Climax" if ("名場面" in after_trigger and "角色" not in after_trigger) else "Character"
                m_lv_max = re.search(r"等級(\d+)以下", after_trigger)
                actions.append({
                    "action": "salvage_wr",
                    "target_type": t_type,
                    "max_level": int(m_lv_max.group(1)) if m_lv_max else 99,
                    "count": 1,
                })

        # 9. 從休息室選卡放到能量區（如 決鬥系統 BFR/S78-109、聖女米瑟莉、大物喰らい マイ＆ユイ）
        if "休息室" in body and "放到能量區" in body:
            after_trigger = body.split("時，")[-1] if "時，" in body else body
            if "休息室" in after_trigger and "放到能量區" in after_trigger:
                col_f = None
                for c_zh in ("藍", "紅", "綠", "黃"):
                    if f"{c_zh}色" in after_trigger:
                        col_f = c_zh
                        break
                actions.append({
                    "action": "charge_stock_wr",
                    "color": col_f,
                    "char_only": ("角色" in after_trigger and "卡片" not in after_trigger),
                    "count": 1,
                })

        # 10. 將標記放到能量區 / 從牌組頂充能
        if "標記1張放到能量區" in body or "標記放到能量區" in body:
            actions.append({"action": "marker_to_stock", "count": 1})
        elif "對手" not in body and "時鐘區" not in body:
            m_stock = re.search(r"牌組上方(?:最多)?(\d+)張.*?放到能量區", body)
            if m_stock:
                actions.append({"action": "charge_stock_top", "count": int(m_stock.group(1))})

        # 11. 魔石 / 機械神：對手能量全部洗回或放休息室並重填相同張數
        if ("對手的能量" in body or "對手將自己的能量" in body or "對手能量區所有" in body) and "相同張數放到能量區" in body:
            actions.append({"action": "reshuffle_opp_stock"})

        # 12. 抽牌與棄牌 (Draw / Loot)
        m_draw = re.search(r"抽(?:最多)?(\d+)張", body)
        if m_draw:
            actions.append({"action": "draw", "count": int(m_draw.group(1))})
            after_draw = body.split("抽")[1]
            if "手牌" in after_draw and "放到休息室" in after_draw:
                actions.append({"action": "discard_hand", "count": 1})

        # 13. 削對手牌組底/頂燒血 或 翻自己頂燒等級+1傷害
        m_mill_opp_burn = re.search(r"對手的?牌組(?:下方|上方)(\d+)張，?放到休息室.*?給對手造成X點?傷害", body)
        if m_mill_opp_burn:
            actions.append({"action": "mill_opp_bottom_burn_cx", "count": int(m_mill_opp_burn.group(1))})
        elif "牌組上方1張" in body and "放到休息室" in body and "給對手造成X" in body and ("等級+1" in body or "等級＋1" in body):
            actions.append({"action": "mill_self_top_burn_lv1"})

        # 14. 直接燒血（支援單句多段燒血，如給對手1點傷害，給對手2點傷害，給對手3點傷害）
        for m_b in re.finditer(r"給對手造成(\d+)點?傷害", body):
            actions.append({"action": "burn", "damage": int(m_b.group(1))})

        # 15. 擊倒對手踢時鐘 / 踢回憶 / 踢能量 / 踢牌組底 / 彈回手牌
        if timing == "ON_REVERSE_OPP":
            after_t = body.split("時，")[-1] if "時，" in body else body
            if "放到時鐘區" in after_t:
                actions.append({"action": "kick_opp_to_clock"})
            elif "放到回憶區" in after_t and "此卡" not in after_t:
                actions.append({"action": "kick_opp_to_memory"})
            elif "放到能量區" in after_t and "休息室" not in after_t and "牌組" not in after_t:
                actions.append({"action": "kick_opp_to_stock"})
            elif "放到牌組下方" in after_t:
                actions.append({"action": "kick_opp_to_deck_bottom"})

        # 16. 被倒置時相殺 (Reversal Bomb)
        if timing == "ON_REVERSED":
            m_rev_lv = re.search(r"等級(\d+)以下", body)
            m_rev_cost = re.search(r"費用(\d+)以下", body)
            anti_early = ("比對手玩家等級還要高" in body or "比對手的等級高" in body)
            if "將那張角色【倒置】" in body or "將那個角色【倒置】" in body:
                actions.append({
                    "action": "reversal_bomb",
                    "max_level": int(m_rev_lv.group(1)) if m_rev_lv else None,
                    "max_cost": int(m_rev_cost.group(1)) if m_rev_cost else None,
                    "anti_early": anti_early,
                })
            elif "放到時鐘區" in body and "那" in body:
                actions.append({"action": "reversal_clock_bomb", "max_level": int(m_rev_lv.group(1)) if m_rev_lv else None})
            elif "放到能量區" in body and "那" in body:
                actions.append({"action": "reversal_stock_bomb", "anti_early": anti_early})
            elif "此卡【橫置】" in body:
                actions.append({"action": "rest_self_survive"})

        # 17. 對手角色減益 / 退場 / 彈回手牌或牌組
        if "選擇對手" in body or "選對手" in body:
            m_debuff_p = re.search(r"攻擊力[－\-](\d+)", body)
            m_debuff_lv = re.search(r"等級[－\-](\d+)", body)
            m_debuff_s = re.search(r"魂傷[－\-](\d+)", body)
            if m_debuff_p or m_debuff_lv or m_debuff_s:
                actions.append({
                    "action": "debuff_opp",
                    "power": int(m_debuff_p.group(1)) if m_debuff_p else 0,
                    "level": int(m_debuff_lv.group(1)) if m_debuff_lv else 0,
                    "soul": int(m_debuff_s.group(1)) if m_debuff_s else 0,
                    "front_only": ("對手前列" in body or "對手的前列" in body),
                })
            elif "回到手牌" in body and "休息室" not in body:
                actions.append({"action": "bounce_opp_hand"})
            elif "放到休息室" in body and ("費用0以下" in body or "等級0以下" in body):
                actions.append({"action": "bomb_opp_front_low"})

        # 18. 移動至空位 (Runner)
        if "移動到" in body and "沒有角色的格子" in body:
            z = "back" if "後列" in body else ("front" if "前列" in body else "any")
            actions.append({"action": "move_to_empty_slot", "zone": z})

        # 19. 正置 (Restand)
        if "【正置】" in body:
            if "選擇其他的" in body or "選其他的" in body:
                actions.append({"action": "stand_ally", "other_only": True})
            else:
                actions.append({"action": "stand_self"})

        # 20. 賦予本回合特殊能力（擊倒踢鐘 / 擊倒回收 / 正面減魂 / 不會倒置）
        if "獲得以下能力" in body or "給予以下能力" in body or "得以下能力" in body:
            granted_part = body.split("能力")[-1]
            if "戰鬥對手【倒置】時" in granted_part and "時鐘區" in granted_part:
                actions.append({"action": "grant_clock_kick"})
            if "戰鬥對手【倒置】時" in granted_part and "休息室" in granted_part and ("回到手牌" in granted_part or "加到手牌" in granted_part):
                actions.append({"action": "grant_salvage_on_reverse"})
            if "正面的角色" in granted_part and "魂傷-" in granted_part:
                actions.append({"action": "grant_front_soul_penalty", "penalty": 1})
        if "不會【倒置】" in body:
            actions.append({"action": "grant_immune_reverse"})

        # 21. 攻擊力 / 魂傷 / 等級 增加（全體我方 / 指定友軍 / 自身 / 動態比例）
        # 排除已由『獲得以下能力』內部子句處理的數字
        main_clause = body.split("『")[0].split("「【")[0]
        m_scale_p = re.search(r"攻擊力[＋\+]X.*?X等於(對手|你的).*?×(\d+)", main_clause)
        if m_scale_p:
            actions.append({
                "action": "buff_self_scaling",
                "target_side": "opp" if "對手" in m_scale_p.group(1) else "self",
                "multiplier": int(m_scale_p.group(2)),
            })
        else:
            m_pwr = re.search(r"攻擊力[＋\+](\d+)", main_clause)
            m_soul = re.search(r"魂傷[＋\+](\d+)", main_clause)
            m_lvl = re.search(r"(?<!那張卡)(?<!那張卡片)等級[＋\+](\d+)", main_clause.split("X等於")[0])
            pwr_v = int(m_pwr.group(1)) if m_pwr else 0
            soul_v = int(m_soul.group(1)) if m_soul else 0
            lvl_v = int(m_lvl.group(1)) if m_lvl else 0
            if pwr_v > 0 or soul_v > 0 or lvl_v > 0:
                if "自己的角色全部" in main_clause or "你的角色全部" in main_clause or "你所有的角色" in main_clause or "你全部的角色" in main_clause:
                    actions.append({"action": "buff_all_allies", "power": pwr_v, "soul": soul_v, "level": lvl_v})
                elif "選擇自己的" in main_clause or "選自己" in main_clause or "選擇其他的" in main_clause or "選擇你" in main_clause:
                    actions.append({
                        "action": "buff_ally",
                        "power": pwr_v,
                        "soul": soul_v,
                        "level": lvl_v,
                        "other_only": ("其他的" in main_clause),
                    })
                else:
                    actions.append({
                        "action": "buff_self",
                        "power": pwr_v,
                        "soul": soul_v,
                        "level": lvl_v,
                    })

        return actions

    @classmethod
    def _parse_auto(cls, line: str, orig_line: str, card_type: str = "CHAR") -> list:
        res = []
        cost = cls._parse_cost(line)

        # 優先處理安可 / 再登場能力
        if "安可" in line and ("手牌" in line or cost.get("discard_hand", 0) > 0 or cost.get("clock_top_deck", 0) > 0):
            if cost.get("stock", 0) >= 1 and cost.get("discard_hand", 0) >= 1:
                res.append({"category": "CONT", "effect": "stock1_hand1_encore", "raw": orig_line})
            elif cost.get("clock_top_deck", 0) >= 1:
                res.append({"category": "CONT", "effect": "clock_encore", "raw": orig_line})
            else:
                res.append({"category": "CONT", "effect": "hand_encore", "raw": orig_line})
            return res

        # 名場面卡自身的【自】登場效果（如 決鬥系統 BFR/S78-109 等）
        if card_type == "CX":
            if "執行開機的效果" in line:
                res.append({"category": "AUTO", "timing": "ON_PLAY", "effect": "climax_standby", "cost": cost, "actions": [{"action": "standby_deploy"}], "raw": orig_line})
                return res
            actions = cls._extract_actions(line, timing="ON_PLAY", cost=cost)
            if actions:
                res.append({
                    "category": "AUTO",
                    "timing": "ON_PLAY",
                    "cost": cost,
                    "is_cx_combo": False,
                    "cx_name": None,
                    "actions": actions,
                    "raw": orig_line,
                })
            return res

        is_cx_combo = ("【CX連動】" in line or "CX連動" in line or "高潮連動" in line or "名場面區有「" in line or "名場面區存在「" in line or "名場面區放上「" in line or "名場面區放到「" in line)
        cx_name = None
        # 尋找名場面名稱引號（排除絆或角色自身名稱引號）
        quotes = re.findall(r"「([^」]+)」", line.split("『")[0])
        if is_cx_combo and quotes:
            # 優先選在「名場面區」附近的引號名稱
            m_cx_near = re.search(r"(?:名場面區|當)[^「]*「([^」]+)」", line)
            cx_name = m_cx_near.group(1) if m_cx_near else quotes[0]

        timing = "OTHER"
        atk_subtype = None
        req_entered_this_turn = False

        if "使用此卡的『助太刀』時" in line or "使用『助太刀』時" in line:
            timing = "ON_BACKUP_USED"
        elif "對手的攻擊階段開始時" in line:
            timing = "ON_OPP_ATK_PHASE_START"
        elif "攻擊階段開始時" in line:
            timing = "ON_ATK_PHASE_START"
        elif "安可步驟開始時" in line or "安可階段開始時" in line:
            timing = "ON_ENCORE_STEP_START"
        elif "主要階段開始時" in line:
            timing = "ON_MAIN_PHASE_START"
        elif "使用【起】" in line:
            timing = "ON_ACT_USED"
        elif "造成的傷害被取消時" in line:
            timing = "ON_DAMAGE_CANCEL"
            if "被放到舞台的回合中" in line:
                req_entered_this_turn = True
        elif "觸發" in line and ("名場面" in line or "判定" in line or "潮" in orig_line):
            timing = "ON_TRIGGER_CX"
        elif ("名場面" in line or "「" in line) and ("被放到名場面區時" in line or "放到名場面區時" in line or "被放到你的名場面區時" in line or "放到你的名場面區時" in line):
            timing = "ON_CX_PLACED"
        elif "被放到舞台的回合中" in line and "攻擊時" in line:
            timing = "ON_ATTACK"
            req_entered_this_turn = True
        elif "其他的你的" in line and "戰鬥對手【倒置】時" in line:
            timing = "ON_OTHER_REVERSE_OPP"
        elif "其他的你的" in line and "【倒置】時" in line:
            timing = "ON_OTHER_REVERSED"
        elif re.search(r"其他的你的[^，。]*角色攻擊時", line):
            timing = "ON_OTHER_ATTACK"
        elif "此卡直接攻擊時" in line:
            timing = "ON_ATTACK"
            atk_subtype = "DIRECT"
        elif "此卡正打時" in line:
            timing = "ON_ATTACK"
            atk_subtype = "FRONT"
        elif "此卡攻擊時" in line or "這張卡攻擊時" in line:
            timing = "ON_ATTACK"
        elif "此卡被正打時" in line or "對手的角色直接攻擊時" in line:
            timing = "ON_BEING_ATTACKED"
        elif "戰鬥對手【倒置】時" in line:
            timing = "ON_REVERSE_OPP"
        elif "此卡【倒置】時" in line:
            timing = "ON_REVERSED"
        elif "從舞台被放到休息室時" in line or "從舞台放到休息室時" in line:
            timing = "ON_STAGE_TO_WR"
        elif "從手牌被放到舞台時" in line or "從手牌放到舞台時" in line or "被放到舞台時" in line:
            timing = "ON_PLAY"

        actions = cls._extract_actions(line, timing=timing, cost=cost)
        if actions:
            res.append({
                "category": "AUTO",
                "timing": timing,
                "atk_subtype": atk_subtype,
                "req_entered_this_turn": req_entered_this_turn,
                "cost": cost,
                "is_cx_combo": is_cx_combo,
                "cx_name": cx_name,
                "actions": actions,
                "raw": orig_line,
            })
        return res

    @classmethod
    def _parse_act(cls, line: str, orig_line: str, card_type: str = "CHAR") -> list:
        res = []
        cost = cls._parse_cost(line)
        # 1. 助太刀 (Backup)
        m_backup = re.search(r"助太刀\s*(\d+)\s*等級\s*(\d+)", line)
        if m_backup or ("助太刀" in line) or ("【反擊】" in orig_line):
            pwr = int(m_backup.group(1)) if m_backup else 1500
            lv = int(m_backup.group(2)) if m_backup else 1
            if not m_backup:
                m_p = re.search(r"攻擊力[＋\+](\d+)", line)
                if m_p:
                    pwr = int(m_p.group(1))
            res.append({
                "category": "BACKUP",
                "power": pwr,
                "level": lv,
                "cost": cost,
                "raw": orig_line,
            })
            return res

        # 2. 集中 (Brainstorm)
        if "集中" in line:
            flip_cnt = 4
            m_flip = re.search(r"翻(?:開|出)?(\d+)張", line)
            if m_flip:
                flip_cnt = int(m_flip.group(1))
            after_flip = line.split("每有1張")[-1] if "每有1張" in line else line
            reward = "search"
            if "最多抽1張" in after_flip:
                reward = "draw_once"
            elif "抽" in after_flip:
                reward = "draw"
            elif "休息室" in after_flip and ("回到手牌" in after_flip or "加到手牌" in after_flip):
                reward = "salvage"
            elif "牌組" in after_flip and ("加到手牌" in after_flip or "回到手牌" in after_flip):
                reward = "search"
            res.append({
                "category": "ACT",
                "effect": "brainstorm",
                "flip_count": flip_cnt,
                "reward": reward,
                "cost": cost,
                "raw": orig_line,
            })
            return res

        # 3. 萬用一般【起】能力（支援看頂加手、檢索、回收、充能、標記、加攻、加魂、賦予能力等所有動作）
        actions = cls._extract_actions(line, timing="ACT", cost=cost)
        if actions:
            res.append({
                "category": "ACT",
                "effect": "universal_act",
                "actions": actions,
                "cost": cost,
                "raw": orig_line,
            })
        return res

    @classmethod
    def _parse_counter_event(cls, line: str, orig_line: str) -> list:
        cost = cls._parse_cost(line)
        actions = cls._extract_actions(line, timing="COUNTER", cost=cost)
        if actions:
            return [{
                "category": "COUNTER_EVENT",
                "cost": cost,
                "actions": actions,
                "send_to_memory": ("放到回憶區" in line),
                "raw": orig_line,
            }]
        return []

    @classmethod
    def _parse_main_event(cls, line: str, orig_line: str) -> list:
        cost = cls._parse_cost(line)
        actions = cls._extract_actions(line, timing="EVENT", cost=cost)
        if actions:
            return [{
                "category": "EVENT",
                "cost": cost,
                "actions": actions,
                "send_to_memory": ("放到回憶區" in line),
                "raw": orig_line,
            }]
        return []



# ==========================================
# 日文 WS 卡片名稱、特徵與效果文 自動轉繁體中文翻譯器 (離線規則引擎)
# ==========================================
_JP_KANJI_TO_ZH_MAP = str.maketrans({
    "将": "將", "姫": "姬", "総": "總", "内": "內", "実": "實", "虚": "虛",
    "剣": "劍", "悪": "惡", "竜": "龍", "霊": "靈", "闘": "鬥", "体": "體",
    "戻": "回", "選": "選", "見": "看", "払": "付", "戦": "戰", "護": "護",
    "発": "發", "動": "動", "変": "變", "転": "轉", "撃": "擊", "獣": "獸",
    "団": "團", "隊": "隊", "学": "學", "園": "園", "会": "會", "員": "員",
    "黒": "黑", "赤": "紅", "青": "藍", "緑": "綠", "黄": "黃", "対": "對",
    "処": "處", "残": "殘", "当": "當", "数": "數", "枚": "張", "枠": "格",
    "置": "放", "場": "場", "札": "牌", "控": "休", "室": "室", "鉄": "鐵",
    "銃": "槍", "双": "雙", "翼": "翼", "聖": "聖", "魔": "魔", "術": "術",
    "師": "師", "錬": "鍊", "金": "金", "鎧": "鎧", "盾": "盾", "槍": "槍",
    "弓": "弓", "矢": "矢", "炎": "炎", "氷": "冰", "雷": "雷", "風": "風",
    "光": "光", "闇": "暗", "無": "無", "気": "氣", "愛": "愛", "恋": "戀",
    "夢": "夢", "希": "希", "望": "望", "絶": "絕", "滅": "滅", "殺": "殺",
    "死": "死", "生": "生", "命": "命", "魂": "魂", "心": "心", "声": "聲",
    "音": "音", "楽": "樂", "歌": "歌", "舞": "舞", "踊": "踊", "絵": "繪",
    "画": "畫", "書": "書", "記": "記", "憶": "憶", "忘": "忘", "想": "想",
    "念": "念", "願": "願", "祈": "祈", "誓": "誓", "約": "約", "束": "束",
    "絆": "絆", "縁": "緣", "運": "運", "宿": "宿", "軌": "軌", "跡": "跡",
    "道": "道", "路": "路", "旅": "旅", "行": "行", "帰": "歸", "還": "還",
    "来": "來", "去": "去", "出": "出", "入": "入", "開": "開", "閉": "閉",
    "始": "始", "終": "終", "完": "完", "全": "全", "部": "部", "分": "分",
    "半": "半", "片": "片", "単": "單", "独": "獨", "複": "複", "雑": "雜",
    "純": "純", "粋": "粹", "真": "真", "偽": "偽", "仮": "假", "嘘": "謊",
    "誠": "誠", "信": "信", "頼": "賴", "裏": "裏", "表": "表", "側": "側",
    "面": "面", "点": "點", "線": "線", "円": "圓", "角": "角", "方": "方",
    "向": "向", "位": "位", "所": "所", "界": "界", "域": "域", "圏": "圈",
    "層": "層", "階": "階", "段": "段", "級": "級", "等": "等", "差": "差",
    "異": "異", "同": "同", "様": "樣", "似": "似", "別": "別", "特": "特",
    "殊": "殊", "普": "普", "通": "通", "常": "常", "凡": "凡", "庸": "庸",
    "優": "優", "秀": "秀", "良": "良", "好": "好", "善": "善", "美": "美",
    "麗": "麗", "華": "華", "栄": "榮", "誉": "譽", "誇": "誇", "恥": "恥",
    "辱": "辱", "罪": "罪", "罰": "罰", "過": "過", "誤": "誤", "正": "正",
    "義": "義", "理": "理", "論": "論", "説": "說", "話": "話", "語": "語",
    "言": "言", "葉": "葉", "辞": "辭", "典": "典", "則": "則", "法": "法",
    "律": "律", "規": "規", "制": "制", "限": "限", "極": "極", "端": "端",
    "頂": "頂", "底": "底", "奥": "奧", "深": "深", "浅": "淺", "広": "廣",
    "狭": "狹", "長": "長", "短": "短", "高": "高", "低": "低", "強": "強",
    "弱": "弱", "硬": "硬", "軟": "軟", "重": "重", "軽": "輕", "速": "速",
    "遅": "遲", "早": "早", "晩": "晚", "新": "新", "古": "古", "旧": "舊",
    "若": "若", "老": "老", "幼": "幼", "稚": "稚", "成": "成", "熟": "熟",
    "未": "未", "既": "既", "済": "濟", "予": "預", "備": "備", "準": "準",
    "整": "整", "揃": "齊", "乱": "亂", "壊": "壞", "破": "破", "砕": "碎",
    "裂": "裂", "割": "割", "切": "切", "断": "斷", "続": "續", "連": "連",
    "繋": "繫", "結": "結", "縛": "縛", "鎖": "鎖", "解": "解", "放": "放",
    "釈": "釋", "赦": "赦", "許": "許", "認": "認", "識": "識", "知": "知",
    "覚": "覺", "悟": "悟", "迷": "迷", "惑": "惑", "疑": "疑", "問": "問",
    "答": "答", "応": "應", "返": "返", "報": "報", "酬": "酬", "償": "償",
    "購": "購", "買": "買", "売": "賣", "販": "販", "商": "商", "貿": "貿",
    "易": "易", "難": "難", "困": "困", "苦": "苦", "喜": "喜", "怒": "怒",
    "哀": "哀", "悲": "悲", "歓": "歡", "迎": "迎", "送": "送", "届": "屆",
    "達": "達", "到": "到", "着": "著", "乗": "乘", "降": "降", "飛": "飛",
    "翔": "翔", "跳": "跳", "躍": "躍", "走": "走", "駆": "驅", "歩": "步",
    "止": "止", "停": "停", "滞": "滯", "留": "留", "居": "居", "住": "住",
    "泊": "泊", "眠": "眠", "寝": "寢", "起": "起", "醒": "醒", "働": "働",
    "労": "勞", "休": "休", "憩": "憩", "遊": "遊", "戯": "戲", "娯": "娛",
    "競": "競", "争": "爭", "勝": "勝", "負": "負", "敗": "敗", "北": "北",
    "南": "南", "東": "東", "西": "西", "央": "央", "左": "左", "右": "右",
    "上": "上", "下": "下", "前": "前", "後": "後", "隣": "鄰", "近": "近",
    "遠": "遠", "離": "離", "隔": "隔", "間": "間", "隙": "隙", "暇": "暇",
    "忙": "忙", "急": "急", "緩": "緩", "慢": "慢", "静": "靜", "寂": "寂",
    "穏": "穩", "激": "激", "烈": "烈", "猛": "猛", "狂": "狂", "暴": "暴",
    "荒": "荒", "廃": "廢", "棄": "棄", "捨": "捨", "拾": "拾", "集": "集",
    "散": "散", "拡": "擴", "張": "張", "縮": "縮", "減": "減", "増": "增",
    "加": "加", "除": "除", "算": "算", "計": "計", "測": "測", "量": "量",
    "験": "驗", "試": "試", "検": "檢", "査": "查", "調": "調", "探": "探",
    "索": "索", "尋": "尋", "訪": "訪", "視": "視", "聴": "聽", "聞": "聞",
    "触": "觸", "味": "味", "匂": "匂", "香": "香", "臭": "臭", "色": "色",
    "彩": "彩", "影": "影", "形": "形", "姿": "姿", "態": "態", "状": "狀",
    "況": "況", "勢": "勢", "力": "力", "権": "權", "威": "威", "厳": "嚴",
    "格": "格", "品": "品", "質": "質", "材": "材", "料": "料", "具": "具",
    "器": "器", "械": "械", "機": "機", "関": "關", "係": "係", "絡": "絡",
    "統": "統", "領": "領", "導": "導", "指": "指", "揮": "揮", "令": "令",
    "従": "從", "順": "順", "逆": "逆", "反": "反", "抗": "抗", "攻": "攻",
    "守": "守", "防": "防", "御": "禦", "衛": "衛", "救": "救", "援": "援",
    "助": "助", "支": "支", "持": "持", "保": "保", "維": "維",
})

_WS_TRAIT_JP_TO_ZH = {
    "ゲーム": "遊戲", "盾": "盾", "双子": "雙胞胎", "水": "水", "炎": "炎", "武器": "武器",
    "音楽": "音樂", "魔法": "魔法", "冒険者": "冒險者", "神": "神", "獣": "獸", "王族": "王族",
    "和服": "和服", "着物": "和服", "ドレス": "禮服", "扇子": "扇", "扇": "扇", "刀": "刀",
    "剣士": "劍士", "忍": "忍", "忍者": "忍者", "虫": "蟲", "霊": "靈", "巫女": "巫女",
    "人形": "人偶", "仮面": "假面", "将棋": "將棋", "仙人": "仙人", "占い": "占卜",
    "雪": "雪", "氷": "冰", "愛": "愛", "家族": "家族", "生徒会": "學生會", "風紀委員": "風紀委員",
    "メガネ": "眼鏡", "眼鏡": "眼鏡", "メイド": "女僕", "執事": "執事", "水着": "泳裝",
    "制服": "制服", "スポーツ": "運動", "科学": "科學", "メカ": "機械", "ロボ": "機器人",
    "艦娘": "艦娘", "アイドル": "偶像", "バンド": "樂團", "下北沢": "下北澤",
    "精霊": "精靈", "悪魔": "惡魔", "天使": "天使", "竜": "龍", "ドラゴン": "龍",
    "騎士": "騎士", "兵士": "士兵", "海賊": "海賊", "怪盗": "怪盜", "探偵": "偵探",
    "警察": "警察", "軍人": "軍人", "教師": "教師", "先生": "老師", "委員長": "班長",
    "不良": "不良", "オタク": "御宅族", "漫画": "漫畫", "アニメ": "動畫", "小説": "小說",
    "料理": "料理", "お菓子": "甜點", "お茶": "茶", "酒": "酒", "動物": "動物",
    "猫": "貓", "犬": "狗", "鳥": "鳥", "兎": "兔", "蛙": "蛙", "蛇": "蛇",
    "植物": "植物", "花": "花", "星": "星", "月": "月", "太陽": "太陽", "宇宙": "宇宙",
    "時間": "時間", "空間": "空間", "異世界": "異世界", "転生": "轉生", "召喚": "召喚",
    "死神": "死神", "妖怪": "妖怪", "鬼": "鬼", "吸血鬼": "吸血鬼", "不死": "不死",
    "改造": "改造", "クローン": "複製人", "超能力": "超能力", "錬金術": "鍊金術",
}


def _has_japanese_kana(s: str) -> bool:
    if not s:
        return False
    return bool(re.search(r"[\u3040-\u30ff]", s))


def translate_jp_ws_trait_to_zh(trait: str) -> str:
    if not trait:
        return ""
    t = str(trait).replace("《", "").replace("》", "").strip()
    if t in _WS_TRAIT_JP_TO_ZH:
        return _WS_TRAIT_JP_TO_ZH[t]
    t = t.translate(_JP_KANJI_TO_ZH_MAP)
    return t


def translate_jp_ws_name_to_zh(name: str) -> str:
    if not name:
        return ""
    s = str(name)
    jp_name_terms = [
        ("とがめ", "咎女"), ("七花", "七花"), ("七実", "七實"), ("否定姫", "否定姬"),
        ("容赦姫", "容赦姬"), ("真庭", "真庭"), ("奇策士", "奇策士"), ("虚刀", "虛刀"),
        ("との思い出", "的回憶"), ("の夏休み", "的暑假"), ("の日常", "的日常"),
        ("の決意", "的決意"), ("の戦い", "的戰鬥"), ("の約束", "的約定"),
        ("の笑顔", "的笑容"), ("の涙", "的眼淚"), ("の力", "的力量"),
        ("お姉ちゃん", "姊姊"), ("お兄ちゃん", "哥哥"), ("ちゃん", "醬"),
        ("さん", "小姐"), ("くん", "君"), ("たち", "們"),
        ("すべての", "所有的"), ("ふたり", "兩人"), ("ひとり", "獨自"),
    ]
    for k, v in jp_name_terms:
        s = s.replace(k, v)
    s = re.sub(r"([\u4e00-\u9fff])の([\u4e00-\u9fff])", r"\1之\2", s)
    s = s.replace("の", "的").replace("・", "．")
    s = s.translate(_JP_KANJI_TO_ZH_MAP)
    return s


def translate_jp_ws_text_to_zh(text: str) -> str:
    if not text:
        return ""
    s = str(text)
    if not _has_japanese_kana(s) and "控え室" not in s and "山札" not in s and "手札" not in s:
        return s

    def _repl_trait(m):
        return f"《{translate_jp_ws_trait_to_zh(m.group(1))}》"
    s = re.sub(r"《([^》]+)》", _repl_trait, s)

    def _repl_quote(m):
        return f"「{translate_jp_ws_name_to_zh(m.group(1))}」"
    s = re.sub(r"「([^」]+)」", _repl_quote, s)

    phrase_rules = [
        ("【CXコンボ】", "【CX連動】"),
        ("（カムバック：このカードがトリガーした時、あなたは自分の控え室のキャラを1枚選び、手札に戻してよい）", "木門：當你判定出此卡時，你可以選擇自己休息室的角色1張，回到手牌。"),
        ("（ゲート：このカードがトリガーした時、あなたは自分の控え室のクライマックスを1枚選び、手札に戻してよい）", "城門：當你判定出此卡時，你可以選擇自己休息室的名場面1張，回到手牌。"),
        ("（スタンバイ：このカードがトリガーした時、あなたは自分の控え室の自分のレベル＋1以下のレベルのキャラを1枚選び、舞台の好きな枠に【レスト】して置いてよい）", "開機：當你判定出此卡時，你可以從自己的休息室選擇自己等級+1以下的等級的角色1張，【橫置】放到舞台上任意的格子。"),
        ("（チョイス：このカードがトリガーした時、あなたは自分の控え室のトリガーアイコンにソウルがあるキャラを1枚選び、手札に戻すかストック置場に置いてよい）", "箭頭：當你判定出此卡時，你可以選擇自己休息室的判定標誌有魂傷的角色1張，回到手牌或放到能量區。"),
        ("（トレジャー：このカードがトリガーした時、あなたはこのカードを手札に戻す。あなたは自分の山札の上から1枚を、ストック置場に置いてよい）", "金磚：當你判定出此卡時，你將此卡回到手牌。你可以將自己的牌組上方1張，放到能量區。"),
        ("（ブック：このカードがトリガーした時、あなたは1枚引いてよい）", "書：當你判定出此卡時，你可以抽1張牌。"),
        ("（プール：このカードがトリガーした時、あなたは自分の山札の上から1枚を、ストック置場に置いてよい）", "金袋：當你判定出此卡時，你可以將自己的牌組上方1張，放到能量區。"),
        ("（リターン：このカードがトリガーした時、あなたは相手のキャラを1枚選び、手札に戻してよい）", "風：當你判定出此卡時，你可以選擇對手的角色1張，回到手牌。"),
        ("（ショット：このターン中、このカードをトリガーした攻撃キャラが次に与えるダメージがキャンセルされた時、相手に1ダメージを与える）", "射擊：在這個回合中，觸發此卡的攻擊角色下次造成的傷害被取消時，給對手1點傷害。"),
        ("スタンバイの効果を行う。", "執行開機的效果。"),
        ("カムバック：", "木門："),
        ("スタンバイ：", "開機："),
        ("ゲート：", "城門："),
        ("チョイス：", "箭頭："),
        ("トレジャー：", "金磚："),
        ("ブック：", "書："),
        ("プール：", "金袋："),
        ("リターン：", "風："),
        ("ショット：", "射擊："),
        ("【クライマックスコンボ】", "【CX連動】"),
        ("【カウンター】", "【反擊】"),
        ("【スタンド】", "【正置】"),
        ("【レスト】", "【橫置】"),
        ("【リバース】", "【倒置】"),
        ("応援 このカードの前のあなたの", "應援 此卡前面的你的"),
        ("応援 このカードの前の", "應援 此卡前面的"),
        ("アンコール ［手札のキャラを1枚控え室に置く］", "安可 ［手牌的角色1張放到休息室］"),
        ("（舞台から控え室に置かれた時、あなたはコストを払ってよい。そうしたら、このカードがいた枠に【レスト】して置く）", ""),
        ("（あなたは自分のフロントアタックされているキャラを1枚選び、そのターン中、パワーを＋", "（你選擇自己被正打的角色1張，在那個回合中，攻擊力+"),
        ("あなたのキャラすべてに、パワーを＋1000し、ソウルを＋1。", "你的角色全部，攻擊力+1000，魂傷+1。"),
        ("あなたのキャラすべてに、ソウルを＋2。", "你的角色全部，魂傷+2。"),
        ("このカードが手札から舞台に置かれた時、", "此卡從手牌被放置到舞台時，"),
        ("このカードが舞台から控え室に置かれた時、", "此卡從舞台被放到休息室時，"),
        ("このカードがアタックした時、", "此卡攻擊時，"),
        ("このカードがフロントアタックされた時、", "此卡被正打時，"),
        ("このカードがサイドアタックされた時、", "此卡被側打時，"),
        ("このカードがダイレクトアタックした時、", "此卡直接攻擊時，"),
        ("このカードのバトル相手が【リバース】した時、", "此卡的戰鬥對手【倒置】時，"),
        ("このカードが【リバース】した時、", "此卡【倒置】時，"),
        ("このカードが手札からクライマックス置場に置かれた時、", "當此卡從手牌放到名場面區時，"),
        ("あなたのクライマックスがクライマックス置場に置かれた時、", "當你的名場面被放置到名場面區時，"),
        ("あなたのメインフェイズの始めに、", "在你的主要階段開始時，"),
        ("あなたのクライマックスフェイズの始めに、", "在你的名場面階段開始時，"),
        ("あなたのアタックフェイズの始めに、", "在你的攻擊階段開始時，"),
        ("あなたのアンコールステップの始めに、", "在你的安可步驟開始時，"),
        ("相手のアンコールステップの始めに、", "在對手的安可步驟開始時，"),
        ("相手のアタックフェイズの始めに、", "在對手的攻擊階段開始時，"),
        ("あなたはコストを払ってよい。そうしたら、", "你可以支付代價。支付代價的話，"),
        ("あなたはコストを払ってよい。そうしたら", "你可以支付代價。支付代價的話，"),
        ("あなたは自分の山札の上から", "你從自己的牌組上方"),
        ("あなたは自分の山札を見て", "你從自己的牌組選擇"),
        ("あなたは自分の控え室の", "你選擇自己休息室的"),
        ("あなたは自分のクロックの上から1枚を、控え室に置いてよい。", "你可以將自己的傷害區上方1張，放到休息室。"),
        ("あなたは自分のクロックの上から1枚を、控え室に置く。", "你將自己的傷害區上方1張，放到休息室。"),
        ("相手に見せ、手札に加え、その山札をシャッフルする。", "給對手確認，加到手牌，將那個牌組洗牌。"),
        ("選んで相手に見せ、手札に加え、その山札をシャッフルする。", "給對手確認，加到手牌，將那個牌組洗牌。"),
        ("その山札をシャッフルする。", "將那個牌組洗牌。"),
        ("ダメージキャンセルは発生する。", "會發生傷害取消。"),
        ("ダメージキャンセルは発生する", "會發生傷害取消"),
        ("そのキャラをそのキャラがいた枠に【レスト】して置く。", "將那張角色【橫置】放置到那張角色原本所在的格子。"),
        ("このカードをこのカードがいた枠に【レスト】して置く。", "將此卡【橫置】放置到此卡原本所在的格子。"),
        ("舞台の好きな枠に【レスト】して置く。", "【橫置】放置到舞台任意的格子。"),
        ("舞台の好きな枠に置く。", "放置到舞台任意的格子。"),
        ("めくり、控え室に置く。それらのカードのクライマックス1枚につき、", "翻開並放到休息室。那些卡片中每有1張名場面，"),
        ("めくり、控え室に置く。", "翻開並放到休息室。"),
        ("クライマックス置場に", "名場面區有"),
        ("クライマックス置場", "名場面區"),
        ("クライマックス", "名場面"),
        ("クロック置場", "傷害區"),
        ("ストック置場", "能量區"),
        ("レベル置場", "等級區"),
        ("思い出置場", "回憶區"),
        ("控え室に置く", "放到休息室"),
        ("控え室に置き", "放到休息室，"),
        ("控え室に置かれた時", "被放到休息室時"),
        ("控え室の", "休息室的"),
        ("控え室", "休息室"),
        ("ストックに置く", "放到能量區"),
        ("ストック置場に置く", "放到能量區"),
        ("ストック置場に置き", "放到能量區，"),
        ("ストック", "能量"),
        ("クロックに置く", "放到傷害區"),
        ("クロック", "傷害區"),
        ("思い出にする", "放到回憶區"),
        ("思い出に置き", "放到回憶區，"),
        ("思い出", "回憶區"),
        ("山札の上から", "牌組上方"),
        ("山札の下から", "牌組下方"),
        ("山札の上に置く", "放到牌組上方"),
        ("山札の下に置く", "放到牌組下方"),
        ("山札", "牌組"),
        ("手札に戻す", "回到手牌"),
        ("手札に戻してよい", "可以回到手牌"),
        ("手札に加える", "加到手牌"),
        ("手札に加え", "加到手牌，"),
        ("手札から", "從手牌"),
        ("手札の", "手牌的"),
        ("手札を", "手牌"),
        ("手札", "手牌"),
        ("舞台から", "從舞台"),
        ("舞台に置かれた時", "被放置到舞台時"),
        ("舞台に", "到舞台"),
        ("舞台", "舞台"),
        ("パワーを＋", "攻擊力+"),
        ("パワーを－", "攻擊力-"),
        ("パワー＋", "攻擊力+"),
        ("パワー－", "攻擊力-"),
        ("パワー", "攻擊力"),
        ("ソウルを＋", "魂傷+"),
        ("ソウルを－", "魂傷-"),
        ("ソウル＋", "魂傷+"),
        ("ソウル－", "魂傷-"),
        ("ソウル", "魂傷"),
        ("レベルを＋", "等級+"),
        ("レベルを－", "等級-"),
        ("レベル＋", "等級+"),
        ("レベル－", "等級-"),
        ("レベル", "等級"),
        ("コスト", "費用"),
        ("フロントアタック", "正打"),
        ("サイドアタック", "側打"),
        ("ダイレクトアタック", "直接攻擊"),
        ("アタックした時", "攻擊時"),
        ("アタック", "攻擊"),
        ("バトル相手", "戰鬥對手"),
        ("バトル中", "戰鬥中"),
        ("バトル", "戰鬥"),
        ("トリガーした時", "觸發判定時"),
        ("トリガーアイコン", "觸發標記"),
        ("トリガー", "觸發"),
        ("マーカー", "標記"),
        ("イベント", "事件"),
        ("そのターン中、", "在那個回合中，"),
        ("次の相手のターンの終わりまで、", "直到下一個對手的回合結束為止，"),
        ("他のあなたの", "其他的你的"),
        ("あなたの", "你的"),
        ("あなたは", "你"),
        ("自分の", "自己的"),
        ("相手の", "對手的"),
        ("相手に", "給對手"),
        ("相手は", "對手"),
        ("このカードの", "此卡的"),
        ("このカードを", "將此卡"),
        ("このカードは", "此卡"),
        ("このカードが", "此卡"),
        ("このカード", "此卡"),
        ("そのキャラを", "將那張角色"),
        ("そのキャラが", "那張角色"),
        ("そのキャラの", "那張角色的"),
        ("そのキャラ", "那張角色"),
        ("キャラすべてに", "角色全部"),
        ("キャラを", "角色"),
        ("キャラが", "角色"),
        ("キャラの", "角色的"),
        ("キャラ", "角色"),
        ("カード名に", "卡名含有"),
        ("カードを", "卡片"),
        ("カードが", "卡片"),
        ("カードの", "卡片的"),
        ("カード", "卡片"),
        ("後列に", "後列有"),
        ("前列に", "前列有"),
        ("いるなら、", "存在的話，"),
        ("あるなら、", "存在的話，"),
        ("いるなら", "存在的話"),
        ("につき、", "每有1張，"),
        ("1枚につき", "每有1張"),
        ("1枚まで選び、", "選擇最多1張，"),
        ("2枚まで選び、", "選擇最多2張，"),
        ("1枚選び、", "選擇1張，"),
        ("2枚選び、", "選擇2張，"),
        ("選び、", "選擇，"),
        ("引いてよい。", "可以抽牌。"),
        ("引く。", "抽牌。"),
        ("ダメージを与える。", "點傷害。"),
        ("ダメージを与える", "點傷害"),
        ("に等しい。", "。"),
        ("を含む", ""),
        ("すべてに、", "全部，"),
        ("すべて", "全部"),
        ("枚", "張"),
        ("選び", "選擇"),
        ("見て", "看"),
        ("置き、", "放置，"),
        ("置く。", "放置。"),
        ("置く", "放置"),
        ("し、", "，"),
        ("してよい。", "。"),
    ]
    for jp_pat, zh_rep in phrase_rules:
        s = s.replace(jp_pat, zh_rep)

    s = re.sub(r"(\d+)張まで", r"最多\1張", s)
    s = re.sub(r"(\d+)張引き", r"抽\1張牌", s)
    s = re.sub(r"(\d+)張引く", r"抽\1張牌", s)
    s = re.sub(r"(\d+)點傷害", r"\1點傷害", s)
    s = re.sub(r"([\u4e00-\u9fff])の([\u4e00-\u9fff])", r"\1的\2", s)
    s = s.replace("の", "的").replace("を", "").replace("に、", "，").replace("、", "，")
    s = re.sub(r"[\u3040-\u309f]+", "", s)
    s = s.translate(_JP_KANJI_TO_ZH_MAP)
    return s


def build_universal_ws_image_urls(cid: str, c_info: dict = None) -> list:
    c_info = c_info or {}
    urls = []
    for k in ("imageUrl", "image", "img", "url", "pic", "cover"):
        v = c_info.get(k)
        if isinstance(v, str) and v.strip():
            u = v.strip()
            if u.startswith("/"):
                u = "https://img.bottleneko.app" + u
            if u not in urls:
                urls.append(u)
    for u in (c_info.get("parallel_urls") or []):
        if isinstance(u, str) and u.strip() and u.strip() not in urls:
            urls.append(u.strip())

    scraper_id = c_info.get("scraperId") or cid.replace("/", "_").replace("-", "_")
    for bn_u in [
        f"https://img.bottleneko.app/{scraper_id}.png",
        f"https://img.bottleneko.app/w_900,f_jpeg&q_85/{scraper_id}.png",
        f"https://img.bottleneko.app/w_900,f_webp&q_80/{scraper_id}.png",
        f"https://img.bottleneko.app/w_360,f_webp&q_80/{scraper_id}.png",
    ]:
        if bn_u not in urls:
            urls.append(bn_u)

    if "/" in cid and "-" in cid:
        left_raw = cid.split("/")[0].lower()
        left_alpha = re.sub(r"\\d+$", "", left_raw) or left_raw
        first_ch = left_alpha[0] if left_alpha else "w"
        right_set = cid.split("-")[0].split("/")[-1].lower()
        lower_id = cid.replace("/", "_").replace("-", "_").lower()
        base_cid = c_info.get("base_id") or re.sub(r"(SP|SSP|SEC|OFR|RRR|SR|S|R)$", "", cid)
        lower_base_id = base_cid.replace("/", "_").replace("-", "_").lower()

        folders = []
        for fd in (f"{left_alpha}_{right_set}", f"{left_raw}_{right_set}", f"{left_alpha}_{right_set}_td", f"{left_alpha}_{right_set}_bp"):
            if fd not in folders:
                folders.append(fd)

        id_cands = [lower_id]
        if lower_base_id != lower_id:
            id_cands.append(lower_base_id)

        for fd in folders:
            for lid in id_cands:
                for ext in ("png", "gif", "jpg"):
                    ws_u = f"https://ws-tcg.com/wordpress/wp-content/images/cardlist/{first_ch}/{fd}/{lid}.{ext}"
                    if ws_u not in urls:
                        urls.append(ws_u)
    return urls


class BottleNekoImporter:
    """
    支援三種免組牌直接擴充卡池的方式：
    1. 【全系列瀏覽器】：直接連線 `https://api.bottleneko.app/series` 列出貓罐子全部 170+ 個 WS 系列，搜尋關鍵字即可點選！
    2. 【整個系列一次抓 / 20 張分批抓】：透過 `https://api.bottleneko.app/series/{id}/cards`（或貼上 `https://bottleneko.app/ws/series/172`），
       免組牌直接把該系列的全部卡片（包含 `i18n.zh` 繁中效果與 `highVer` 高版本 SP/SSP 異畫卡）一次抓下來，或以每次 20 張分批穩定匯入！
    3. 【貓罐子牌組網址】：相容既有 `https://bottleneko.app/ws/deck/wMI7n` 牌組匯入。
    """

    @staticmethod
    def _http_get_json(url: str, timeout: int = 20):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)

    @classmethod
    def fetch_all_series_catalog(cls) -> list:
        """從 https://api.bottleneko.app/series 取得所有 WS 系列清單"""
        data = cls._http_get_json("https://api.bottleneko.app/series")
        if not isinstance(data, list):
            return []
        catalog = []
        for item in data:
            if not isinstance(item, dict):
                continue
            sid = item.get("id")
            jp_name = item.get("name") or ""
            zh_name = (item.get("i18n", {}).get("zh", {}) or {}).get("name") or jp_name
            codes = item.get("code") or []
            if isinstance(codes, str):
                codes = [codes]
            catalog.append({
                "id": sid,
                "name": zh_name,
                "jp_name": jp_name,
                "codes": codes,
                "display": f"[{sid}] {zh_name} ({'/'.join(codes[:4])})",
            })
        return catalog

    @classmethod
    def _convert_bottleneko_card_obj(cls, c_info: dict, default_series_code: str = "CUSTOM/S01", count: int = 0) -> dict:
        cid = str(c_info.get("id") or c_info.get("cardId") or c_info.get("code") or "").strip()
        if not cid:
            return None
        i18n_obj = c_info.get("i18n") or c_info.get("translations") or {}
        zh_block = (
            i18n_obj.get("zh")
            or i18n_obj.get("zh-TW")
            or i18n_obj.get("zh_TW")
            or i18n_obj.get("tw")
            or i18n_obj.get("zh-Hant")
            or {}
        )
        jp_name = c_info.get("title") or c_info.get("jpName") or c_info.get("name") or cid
        raw_zh_name = zh_block.get("title") or zh_block.get("name") or c_info.get("zhName") or c_info.get("zhTitle") or ""
        name = raw_zh_name if (raw_zh_name and not _has_japanese_kana(raw_zh_name)) else translate_jp_ws_name_to_zh(raw_zh_name or jp_name)

        raw_type = str(c_info.get("type") or c_info.get("cardType") or "CHAR").upper()
        if "キャラ" in raw_type or "CHAR" in raw_type or "角色" in raw_type:
            ctype = "CHAR"
        elif "イベント" in raw_type or "EVENT" in raw_type or "事件" in raw_type:
            ctype = "EVENT"
        elif "クライマックス" in raw_type or "CLIMAX" in raw_type or "CX" in raw_type or "名場面" in raw_type or "高潮" in raw_type:
            ctype = "CX"
        else:
            ctype = "CHAR"

        color_map = {
            "YELLOW": "黃", "GREEN": "綠", "RED": "紅", "BLUE": "藍", "PURPLE": "紫",
            "黃": "黃", "綠": "綠", "紅": "紅", "藍": "藍", "紫": "紫",
        }
        raw_color = str(c_info.get("color") or "黃").upper()
        color = color_map.get(raw_color, "黃")

        level = int(c_info.get("level") or 0)
        cost = int(c_info.get("cost") or 0)
        power = int(c_info.get("attack") if c_info.get("attack") is not None else (c_info.get("power") or 0))
        soul = int(c_info.get("soul") if c_info.get("soul") is not None else (0 if ctype != "CHAR" else 1))

        raw_trig = c_info.get("trigger") or []
        if isinstance(raw_trig, list):
            trig_list = [str(t).upper().strip() for t in raw_trig if str(t).strip()]
            trig_str = "+".join(trig_list) if trig_list else "NONE"
        else:
            trig_str = str(raw_trig).upper().strip() or "NONE"
            trig_list = [t for t in trig_str.split("+") if t]
        if "STANDBY" in trig_str:
            trigger = "STANDBY"
        elif "COMEBACK" in trig_str or "DOOR" in trig_str or "SALVAGE" in trig_str:
            trigger = "DOOR"
        elif "GATE" in trig_str or "ARCH" in trig_str or "PANTS" in trig_str:
            trigger = "GATE"
        elif "CHOICE" in trig_str:
            trigger = "CHOICE"
        elif "WIND" in trig_str or "RETURN" in trig_str or "BOUNCE" in trig_str:
            trigger = "WIND"
        elif "TREASURE" in trig_str or "GOLD" in trig_str or "BAR" in trig_str:
            trigger = "TREASURE"
        elif "BOOK" in trig_str or "DRAW" in trig_str:
            trigger = "BOOK"
        elif "SHOT" in trig_str:
            trigger = "SHOT"
        elif "BAG" in trig_str or "POOL" in trig_str or "STOCK" in trig_str:
            trigger = "BAG"
        elif trig_list.count("SOUL") >= 2 or "SOUL2" in trig_str or "2SOUL" in trig_str:
            trigger = "SOUL2"
        elif "SOUL" in trig_str:
            trigger = "SOUL"
        else:
            trigger = "NONE"

        raw_traits = zh_block.get("feature") or zh_block.get("traits") or c_info.get("feature") or c_info.get("traits") or []
        if isinstance(raw_traits, str):
            raw_traits = [raw_traits]
        traits = [translate_jp_ws_trait_to_zh(t) for t in raw_traits if t]

        effect_text = (
            zh_block.get("effect")
            or zh_block.get("ability")
            or zh_block.get("text")
            or c_info.get("zhEffect")
            or c_info.get("effect")
            or c_info.get("text")
            or ""
        )
        if isinstance(effect_text, list):
            effect_text = "\n".join(str(x) for x in effect_text)
        effect_text = translate_jp_ws_text_to_zh(effect_text)

        parallel_urls = build_universal_ws_image_urls(cid, c_info)
        hi_res_url = parallel_urls[0] if parallel_urls else f"https://img.bottleneko.app/{cid.replace('/', '_').replace('-', '_')}.png"

        rare = str(c_info.get("rare") or c_info.get("rarity") or "R")
        low_vers = c_info.get("lowVer") or []
        if isinstance(low_vers, str):
            low_vers = [low_vers]
        high_vers = c_info.get("highVer") or []
        if isinstance(high_vers, str):
            high_vers = [high_vers]
        is_high_rarity = bool(low_vers) or any(tag in rare for tag in ["SP", "SSP", "SEC", "OFR", "SR", "RRR"])
        base_id = low_vers[0] if low_vers else cid
        high_rarity_id = high_vers[-1] if high_vers else None

        series_code = default_series_code
        if "/" in cid and "-" in cid:
            series_code = cid.split("-")[0]

        # 若卡片效果文內明確寫了標記說明，優先以實際卡片效果文校準標記，杜絕按顏色或錯誤分類
        if ctype == "CX":
            if ("選擇自己休息室的角色1張，回到手牌" in effect_text or "選擇自己休息室的1張角色，回到手牌" in effect_text or "控え室のキャラを1枚選び、手札に戻してよい" in effect_text or "木門：" in effect_text or "扉：" in effect_text) and trigger in ("NONE", "SOUL", "GATE", "STANDBY"):
                trigger = "DOOR"
            elif ("選擇自己休息室的名場面1張，回到手牌" in effect_text or "選擇自己休息室的1張名場面，回到手牌" in effect_text or "控え室のクライマックスを1枚選び、手札に戻してよい" in effect_text or "城門：" in effect_text) and trigger in ("NONE", "SOUL", "DOOR"):
                trigger = "GATE"
            elif ("執行開機的效果" in effect_text or "開機：" in effect_text or "スタンバイ" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "STANDBY"
            elif ("箭頭：" in effect_text or "判定標誌有魂傷的角色1張，回到手牌或放到能量區" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "CHOICE"
            elif ("金磚：" in effect_text or "寶：" in effect_text or "將此卡回到手牌" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "TREASURE"
            elif ("書：" in effect_text or "當你判定出此卡時，你可以抽1張牌" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "BOOK"
            elif ("金袋：" in effect_text or "袋：" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "BAG"
            elif ("風：" in effect_text or "當你判定出此卡時，你可以選擇對手的角色1張，回到手牌" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "WIND"
            elif ("射擊：" in effect_text or "觸發此卡的攻擊角色下次造成的傷害被取消時" in effect_text) and trigger in ("NONE", "SOUL"):
                trigger = "SHOT"

        effects_tags = ChineseEffectParser.infer_effect_tags(effect_text, ctype, trigger)

        parsed_abs = ChineseEffectParser.parse_card_effects(effect_text, ctype)
        return {
            "id": cid,
            "base_id": base_id,
            "series": series_code,
            "name": name,
            "jp_name": jp_name,
            "type": ctype,
            "color": color,
            "level": level,
            "cost": cost,
            "power": power,
            "soul": soul,
            "trigger": trigger,
            "traits": traits,
            "default_count": count,
            "rarity": rare,
            "is_high_rarity": is_high_rarity,
            "high_rarity_id": high_rarity_id,
            "effects": effects_tags,
            "text": effect_text,
            "url": hi_res_url,
            "parallel_urls": parallel_urls,
            "parsed_abilities": parsed_abs,
        }

    @classmethod
    def import_series_by_id(
        cls,
        series_id_or_url: str,
        sets_dir: str = "sets",
        batch_offset: int = 0,
        batch_limit: int = 0,
        include_high_rarity: bool = True,
        log_callback=None,
    ) -> dict:
        """
        直接從貓罐子系列 API (`https://api.bottleneko.app/series/{id}/cards`) 抓取整個系列（或指定 20 張分批區間）！
        - batch_limit = 0 代表一次抓取該系列全部卡片
        - batch_limit = 20 代表每次抓 20 張（配合 batch_offset = 0, 20, 40... 分批匯入）
        """
        def _log(msg):
            if log_callback:
                log_callback(msg)
            print(msg)

        s_str = str(series_id_or_url).strip().rstrip("/")
        if "bottleneko.app" in s_str and "/series/" in s_str:
            s_id = s_str.split("/series/")[-1].split("?")[0].split("/")[0]
        else:
            s_id = s_str

        meta_url = f"https://api.bottleneko.app/series/{s_id}"
        cards_url = f"https://api.bottleneko.app/series/{s_id}/cards"
        _log(f"🌐 正在從貓罐子連線取得系列 #{s_id} 卡表：{cards_url} ...")

        series_title = f"系列 #{s_id}"
        series_code = f"SERIES_{s_id}"
        try:
            meta = cls._http_get_json(meta_url)
            if isinstance(meta, dict):
                zh_n = (meta.get("i18n", {}).get("zh", {}) or {}).get("name") or meta.get("name")
                codes = meta.get("code") or []
                if codes and isinstance(codes, list):
                    series_code = codes[0]
                if zh_n:
                    series_title = f"{zh_n} ({series_code})"
        except Exception:
            pass

        raw_cards = cls._http_get_json(cards_url)
        if not isinstance(raw_cards, list) or not raw_cards:
            raise ValueError(f"從 {cards_url} 取得的卡片列表為空！")

        # 過濾是否包含異畫高版本
        if not include_high_rarity:
            raw_cards = [c for c in raw_cards if not (c.get("lowVer") and len(c.get("lowVer")) > 0)]

        total_available = len(raw_cards)
        if batch_limit > 0:
            sliced_cards = raw_cards[batch_offset : batch_offset + batch_limit]
            _log(f"📦 分批模式：系列總共 {total_available} 張，本次抓取第 {batch_offset + 1} ~ {min(batch_offset + len(sliced_cards), total_available)} 張（共 {len(sliced_cards)} 張）...")
        else:
            sliced_cards = raw_cards
            _log(f"📦 全系列模式：共取得 {total_available} 張卡片，正在自動編譯中文效果 AST...")

        first_cid = raw_cards[0].get("id", "") if raw_cards else ""
        if "/S131-" in first_cid:
            series_code = "GA/S131"
        elif "/W107-" in first_cid:
            series_code = "BTR/W107"
        elif "/S78-" in first_cid:
            series_code = "BFR/S78"
        elif series_code.startswith("SERIES_") and "/" in first_cid and "-" in first_cid:
            series_code = first_cid.split("-")[0]

        if series_code in BUILTIN_SERIES_TITLES:
            series_title = BUILTIN_SERIES_TITLES[series_code]

        converted = {}
        for c_obj in sliced_cards:
            c_dict = cls._convert_bottleneko_card_obj(c_obj, default_series_code=series_code, count=0)
            if c_dict:
                c_dict["series"] = series_code
                c_dict["default_count"] = 0
                converted[c_dict["id"]] = c_dict

        full_sets_dir = os.path.join(BASE_DIR, sets_dir)
        os.makedirs(full_sets_dir, exist_ok=True)
        safe_fname = series_code.replace("/", "_") + ".json"
        out_path = os.path.join(full_sets_dir, safe_fname)

        existing_payload = {
            "series_code": series_code,
            "series_name": series_code,
            "series_title": series_title,
            "default_deck_recipe": {},
            "cards": {},
        }
        if os.path.exists(out_path) and batch_limit > 0:
            try:
                with open(out_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    if "cards" in loaded and isinstance(loaded["cards"], dict):
                        existing_payload["cards"] = loaded["cards"]
                    else:
                        existing_payload["cards"] = {k: v for k, v in loaded.items() if isinstance(v, dict) and "name" in v}
            except Exception:
                pass

        if batch_limit == 0 and batch_offset == 0:
            # 一次抓取全系列時，直接以官方完整卡表覆寫，杜絕殘留舊卡造成張數對不上
            cards_map = dict(sorted(converted.items(), key=lambda kv: _natural_card_sort_key(kv[0])))
        else:
            cards_map = existing_payload.get("cards", {})
            cards_map.update(converted)
            cards_map = dict(sorted(cards_map.items(), key=lambda kv: _natural_card_sort_key(kv[0])))

        existing_payload["series_code"] = series_code
        existing_payload["series_name"] = series_code
        existing_payload["series_title"] = series_title
        existing_payload["default_deck_recipe"] = {}
        existing_payload["cards"] = cards_map

        # 純系列卡表匯入時不自動拼湊隨機 50 張套牌，僅保留貓罐子實際牌組匯入或內建三大真實構築套牌

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(existing_payload, f, ensure_ascii=False, indent=2)

        load_all_card_sets(sets_dir)
        _log(f"✅ 成功寫入 {len(converted)} 張卡片至 {out_path}（目前該系列累計收錄 {len(cards_map)} 張）！")
        return {
            "series_code": series_code,
            "deck_name": series_title,
            "card_count": len(converted),
            "total_in_file": len(cards_map),
            "total_available": total_available,
            "next_offset": batch_offset + len(sliced_cards),
            "file_path": out_path,
        }

    @classmethod
    def _http_get_text(cls, url: str, timeout: int = 20) -> str:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/json,text/plain,*/*",
                "Accept-Language": "zh-TW,zh;q=0.9,ja;q=0.8,en;q=0.7",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")

    @classmethod
    def search_social_decks(cls, keyword: str = "", series_id: str = "", log_callback=None) -> list:
        """
        搜尋貓罐子社群牌組 (https://bottleneko.app/social/?k=...&s=...)
        回傳清單: [{"code": "KxDS8", "title": "帕瓦！", "author": "MaXXC", "date": "2023-06-14", "desc": "帕瓦臉單", "display": "..."}]
        """
        def _log(msg):
            if log_callback:
                log_callback(msg)
            print(msg)

        import urllib.parse
        q_parts = []
        if keyword and keyword.strip():
            q_parts.append(f"k={urllib.parse.quote(keyword.strip())}")
        if series_id and str(series_id).strip() and str(series_id).strip() != "ALL":
            q_parts.append(f"s={urllib.parse.quote(str(series_id).strip())}")
        qs = ("?" + "&".join(q_parts)) if q_parts else ""

        results = []
        seen_codes = set()

        for api_u in [
            f"https://api.bottleneko.app/social{qs}",
            f"https://api.bottleneko.app/decks{qs}",
            f"https://api.bottleneko.app/ws/social{qs}",
        ]:
            try:
                data = cls._http_get_json(api_u, timeout=10)
                items = data if isinstance(data, list) else (data.get("list") or data.get("data") or data.get("items") or data.get("decks") or []) if isinstance(data, dict) else []
                if isinstance(items, list) and items:
                    for it in items:
                        if not isinstance(it, dict):
                            continue
                        code = str(it.get("code") or it.get("id") or it.get("deckCode") or it.get("shortId") or "").strip()
                        if not code or code in seen_codes:
                            continue
                        seen_codes.add(code)
                        title = str(it.get("title") or it.get("name") or "未命名社群牌組").strip()
                        author = str((it.get("author") or {}).get("name") if isinstance(it.get("author"), dict) else (it.get("author") or it.get("userName") or it.get("user") or "社群玩家")).strip()
                        date_s = str(it.get("date") or it.get("createdAt") or it.get("updatedAt") or "")[:10]
                        desc = str(it.get("description") or it.get("content") or "").replace("\n", " ").strip()[:40]
                        disp = f"[{code}] {title} — 作者:{author} ({date_s}) {desc}"
                        results.append({
                            "code": code,
                            "title": title,
                            "author": author,
                            "date": date_s,
                            "desc": desc,
                            "display": disp,
                        })
                    if results:
                        return results
            except Exception:
                pass

        for web_u in [
            f"https://bottleneko.app/social/{qs}",
            f"https://bottleneko.app/ws/social{qs}",
        ]:
            try:
                _log(f"🌐 正在連線搜尋貓罐子社群牌組：{web_u} ...")
                html = cls._http_get_text(web_u, timeout=15)
                m_next = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
                if m_next:
                    nj = json.loads(m_next.group(1))
                    pp = nj.get("props", {}).get("pageProps", {})
                    cand_lists = [
                        pp.get("socialList"), pp.get("articles"), pp.get("decks"), pp.get("list"), pp.get("items")
                    ]
                    for cl in cand_lists:
                        if isinstance(cl, list) and cl:
                            for it in cl:
                                if not isinstance(it, dict):
                                    continue
                                code = str(it.get("code") or it.get("id") or "").strip()
                                if not code or code in seen_codes:
                                    continue
                                seen_codes.add(code)
                                title = str(it.get("title") or it.get("name") or "社群牌組").strip()
                                author = str(it.get("authorName") or it.get("author") or "社群玩家").strip()
                                date_s = str(it.get("publishDate") or it.get("createdAt") or "")[:10]
                                desc = str(it.get("description") or "").replace("\n", " ").strip()[:40]
                                results.append({
                                    "code": code,
                                    "title": title,
                                    "author": author,
                                    "date": date_s,
                                    "desc": desc,
                                    "display": f"[{code}] {title} — 作者:{author} ({date_s}) {desc}",
                                })
                for m_link in re.finditer(r'/(?:ws/)?(?:social|deck)/([A-Za-z0-9_-]{4,10})', html):
                    c_code = m_link.group(1)
                    if c_code not in seen_codes and c_code not in ("upload", "create", "search", "login", "index"):
                        seen_codes.add(c_code)
                        results.append({
                            "code": c_code,
                            "title": f"社群牌組 {c_code}",
                            "author": "貓罐子社群",
                            "date": "",
                            "desc": "",
                            "display": f"[{c_code}] 貓罐子社群分享牌組 (點擊即可直接載入)",
                        })
                clean_txt = re.sub(r"<[^>]+>", "\n", html)
                lines = [ln.strip() for ln in clean_txt.splitlines() if ln.strip()]
                for i, ln in enumerate(lines):
                    if re.match(r"^\d{4}-\d{2}-\d{2}$", ln) and i + 1 < len(lines):
                        cand_code = lines[i + 1]
                        if re.match(r"^[A-Za-z0-9]{5}$", cand_code):
                            author = lines[i - 1] if i - 1 >= 0 else "社群玩家"
                            title = lines[i + 3] if i + 3 < len(lines) else f"社群牌組 {cand_code}"
                            desc = lines[i + 4] if i + 4 < len(lines) else ""
                            disp = f"[{cand_code}] {title} — 作者:{author} ({ln}) {desc[:30]}"
                            existing = next((r for r in results if r["code"] == cand_code), None)
                            if existing:
                                existing.update({"title": title, "author": author, "date": ln, "desc": desc, "display": disp})
                            else:
                                seen_codes.add(cand_code)
                                results.append({
                                    "code": cand_code,
                                    "title": title,
                                    "author": author,
                                    "date": ln,
                                    "desc": desc,
                                    "display": disp,
                                })
                if results:
                    break
            except Exception as e:
                _log(f"⚠️ 搜尋頁面連線提示：{e}")

        return results

    @classmethod
    def _parse_cards_from_bottleneko_html(cls, html: str, fallback_code: str = "") -> tuple:
        """
        從貓罐子 `/deck/{code}` 或 `/social/{code}` 網頁 HTML 中解析牌組名稱與 50 張卡片清單。
        """
        deck_name = f"貓罐子社群牌組 {fallback_code}".strip()
        m_title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        if m_title:
            raw_t = m_title.group(1).split("|")[0].strip()
            if raw_t and raw_t.lower() != "undefined":
                deck_name = raw_t

        m_next = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
        if m_next:
            try:
                next_json = json.loads(m_next.group(1))
                pp = next_json.get("props", {}).get("pageProps", {})
                deck_obj = pp.get("deck") or pp.get("article") or pp.get("social") or pp.get("data") or next_json
                if isinstance(deck_obj, dict):
                    d_name = deck_obj.get("name") or deck_obj.get("title")
                    if d_name and str(d_name).lower() != "undefined":
                        deck_name = str(d_name).strip()
                    raw_c = deck_obj.get("cards") or deck_obj.get("deckCards") or deck_obj.get("list") or []
                    if isinstance(raw_c, list) and raw_c:
                        return deck_name, raw_c
            except Exception:
                pass

        clean_txt = re.sub(r"<[^>]+>", "\n", html)
        lines = [ln.strip() for ln in clean_txt.splitlines() if ln.strip()]

        def _normalize_scraped_cid(raw_cid: str) -> str:
            s = raw_cid.strip()
            for dup, single in [("RRRR", "R"), ("SPSP", "SP"), ("SBRSBR", "SBR"), ("SSR", "SR"), ("TD", ""), ("CR", ""), ("CC", ""), ("RR", ""), ("U", ""), ("C", "")]:
                if s.endswith(dup) and len(s) > len(dup) + 5:
                    base_part = s[: -len(dup)]
                    if re.search(r"-[T0-9]\d{1,3}$", base_part):
                        return base_part + single if single in ("SP", "SSP", "SEC", "OFR", "RRR", "SR", "S") else base_part
            m_base = re.match(r"^([A-Za-z0-9]+/[A-Za-z0-9]+-[A-Za-z0-9]+?)(RR|CR|CC|TD|PR|R|U|C)$", s)
            if m_base:
                return m_base.group(1)
            return s

        card_entries = []
        cid_pattern = re.compile(r"^([A-Za-z0-9]{2,6}/[SWsw]\d{1,3}-[A-Za-z0-9]{2,10})$")
        i = 0
        while i < len(lines):
            ln = lines[i]
            m_c = cid_pattern.match(ln)
            if m_c:
                raw_cid = m_c.group(1)
                norm_cid = _normalize_scraped_cid(raw_cid)
                c_title = lines[i + 1] if (i + 1 < len(lines) and not lines[i + 1].startswith("Type")) else norm_cid
                c_type = "CHAR"
                c_soul = 1
                c_lv = 0
                c_pwr = 0
                c_cost = 0
                for k_off in range(1, min(10, len(lines) - i)):
                    sub = lines[i + k_off]
                    if sub.startswith("Type"):
                        if "クライマックス" in sub or "CX" in sub.upper():
                            c_type = "CX"
                        elif "イベント" in sub or "EVENT" in sub.upper():
                            c_type = "EVENT"
                    elif sub.startswith("Soul"):
                        m_n = re.search(r"\d+", sub)
                        if m_n:
                            c_soul = int(m_n.group(0))
                    elif sub.startswith("Level"):
                        m_n = re.search(r"\d+", sub)
                        if m_n:
                            c_lv = int(m_n.group(0))
                    elif sub.startswith("Power"):
                        m_n = re.search(r"\d+", sub)
                        if m_n:
                            c_pwr = int(m_n.group(0))
                    elif sub.startswith("Cost"):
                        m_n = re.search(r"\d+", sub)
                        if m_n:
                            c_cost = int(m_n.group(0))
                card_entries.append({
                    "id": norm_cid,
                    "raw_id": raw_cid,
                    "title": c_title,
                    "type": c_type,
                    "soul": 0 if c_type != "CHAR" else c_soul,
                    "level": c_lv,
                    "attack": c_pwr,
                    "cost": c_cost,
                    "count": 1,
                })
            i += 1

        return deck_name, card_entries

    @classmethod
    def _match_card_in_db(cls, raw_cid: str) -> str:
        """在現有 CARD_DB 中比對卡號（支援精確比對、忽略大小寫、去除爬取贅字與 base_id 比對）"""
        s = str(raw_cid or "").strip()
        if not s:
            return ""
        if s in CARD_DB:
            return s
        upper_map = {k.upper(): k for k in CARD_DB}
        if s.upper() in upper_map:
            return upper_map[s.upper()]
        # 嘗試去除爬取常見的尾綴 (RR, R, U, C, CR, CC, TD, PR)
        m_base = re.match(r"^([A-Za-z0-9]+/[A-Za-z0-9]+-[A-Za-z0-9]+?)(RRRR|SPSP|SBRSBR|SSR|RR|CR|CC|TD|PR|R|U|C)$", s, re.I)
        if m_base:
            cand = m_base.group(1)
            if cand.upper() in upper_map:
                return upper_map[cand.upper()]
        for k, v in CARD_DB.items():
            if not v.get("is_high_rarity") and str(v.get("base_id", "")).upper() == s.upper():
                return k
        return ""

    @classmethod
    def import_from_url_or_json(cls, source_input: str, sets_dir: str = "sets", log_callback=None) -> dict:
        """
        純粹匯入貓罐子牌組配比（50張）至玩家自訂卡組：
        - 優先直接映射至已匯入的 SERIES_DB / CARD_DB 卡片，完全不修改或覆寫 sets/{series_code}.json！
        - 絕不變更現有系列的名稱、卡池張數或預設套牌！
        - 若牌組內含尚未匯入系列的卡片，僅寫入獨立快取 sets/_deck_extra_cards.json 供牌組顯示與對戰使用。
        """
        def _log(msg):
            if log_callback:
                log_callback(msg)
            print(msg)

        source_input = source_input.strip()
        if "/ws/series/" in source_input or "/series/" in source_input or source_input.isdigit():
            return cls.import_series_by_id(source_input, sets_dir=sets_dir, log_callback=log_callback)

        deck_data = None
        raw_cards = []
        deck_name = "貓罐子社群牌組"

        if source_input.startswith("{") or source_input.startswith("["):
            deck_data = json.loads(source_input)
        elif os.path.isfile(source_input):
            with open(source_input, "r", encoding="utf-8") as f:
                deck_data = json.load(f)
        else:
            clean_url = source_input.split("?")[0].rstrip("/")
            deck_id = clean_url.split("/")[-1]
            is_social_url = "/social/" in source_input

            api_candidates = [
                f"https://api.bottleneko.app/deck/{deck_id}",
                f"https://api.bottleneko.app/decks/{deck_id}",
                f"https://api.bottleneko.app/social/{deck_id}",
            ]
            for api_u in api_candidates:
                try:
                    res_j = cls._http_get_json(api_u, timeout=10)
                    if isinstance(res_j, dict) and (res_j.get("cards") or res_j.get("deckCards") or res_j.get("list") or isinstance(res_j.get("deck"), dict)):
                        deck_data = res_j.get("deck") if isinstance(res_j.get("deck"), dict) else res_j
                        _log(f"✅ 已從貓罐子 API 取得牌組資料：{api_u}")
                        break
                except Exception:
                    pass

            if not deck_data:
                web_candidates = (
                    [f"https://bottleneko.app/social/{deck_id}", f"https://bottleneko.app/deck/{deck_id}", f"https://bottleneko.app/ws/deck/{deck_id}"]
                    if is_social_url
                    else [f"https://bottleneko.app/deck/{deck_id}", f"https://bottleneko.app/social/{deck_id}", f"https://bottleneko.app/ws/deck/{deck_id}"]
                )
                for web_u in web_candidates:
                    try:
                        _log(f"🌐 正在連線至貓罐子抓取社群/牌組資料：{web_u} ...")
                        html = cls._http_get_text(web_u, timeout=15)
                        parsed_name, parsed_cards = cls._parse_cards_from_bottleneko_html(html, fallback_code=deck_id)
                        if parsed_cards:
                            deck_name = parsed_name
                            raw_cards = parsed_cards
                            _log(f"✅ 成功從 {web_u} 解析出牌組【{deck_name}】（共 {len(raw_cards)} 筆卡片項目）！")
                            break
                    except Exception as e:
                        _log(f"⚠️ 嘗試 {web_u} 失敗：{e}")

        if deck_data and not raw_cards:
            if isinstance(deck_data, dict):
                deck_name = deck_data.get("name") or deck_data.get("title") or deck_name
                raw_cards = deck_data.get("cards") or deck_data.get("deckCards") or deck_data.get("list") or []
            elif isinstance(deck_data, list):
                raw_cards = deck_data

        if not raw_cards:
            raise ValueError("無法從該網址或代碼解析出卡片清單，請確認牌組代碼（如 peAYS / o7Hhb）或網址是否正確。")

        # 檢查是否有卡片尚未收錄於本地 CARD_DB 或缺少效果文
        missing_prefixes = set()
        for it in raw_cards:
            c_obj = it.get("card", it) if isinstance(it, dict) and "card" in it else it
            if not isinstance(c_obj, dict):
                continue
            cid_tmp = str(c_obj.get("id") or c_obj.get("cardId") or c_obj.get("code") or "").strip()
            raw_tmp = str(c_obj.get("raw_id") or "").strip()
            matched_k = cls._match_card_in_db(cid_tmp) or cls._match_card_in_db(raw_tmp)
            zh_b = ((c_obj.get("i18n") or {}).get("zh") or {}) if isinstance(c_obj.get("i18n"), dict) else {}
            raw_eff = zh_b.get("effect") or zh_b.get("ability") or zh_b.get("text") or c_obj.get("zhEffect") or c_obj.get("effect") or c_obj.get("text") or ""
            if not matched_k or not str(CARD_DB.get(matched_k, {}).get("text") or "").strip():
                if not str(raw_eff).strip() and "/" in cid_tmp and "-" in cid_tmp:
                    missing_prefixes.add(cid_tmp.split("-")[0].upper())

        api_card_lookup = {}
        if missing_prefixes:
            try:
                _log(f"🔍 牌組內含本地尚未收錄效果的卡片，正在從貓罐子補齊 {', '.join(sorted(missing_prefixes))} 的卡片資料...")
                cats = cls.fetch_all_series_catalog()
                matched_sids = set()
                for cat in cats:
                    cat_codes = [str(x).upper() for x in (cat.get("codes") or [])]
                    for pref in missing_prefixes:
                        left_p = pref.split("/")[0]
                        right_p = pref.split("/")[-1]
                        if any(pref == cc or left_p == cc or right_p in cc for cc in cat_codes):
                            matched_sids.add(cat["id"])
                for sid in list(matched_sids)[:4]:
                    try:
                        s_cards = cls._http_get_json(f"https://api.bottleneko.app/series/{sid}/cards", timeout=15)
                        if isinstance(s_cards, list):
                            for sc in s_cards:
                                if isinstance(sc, dict) and sc.get("id"):
                                    api_card_lookup[sc["id"].upper()] = sc
                    except Exception:
                        pass
            except Exception as e:
                _log(f"ℹ️ 自動補齊系列詳細效果略過：{e}")

        recipe_dict = {}
        extra_cards_to_cache = {}
        series_counts = {}

        for item in raw_cards:
            c_info = item.get("card", item) if isinstance(item, dict) and "card" in item else item
            if not isinstance(c_info, dict):
                continue
            count = int(item.get("count") or item.get("quantity") or item.get("amount") or 1) if isinstance(item, dict) else 1
            raw_cid = str(c_info.get("id") or c_info.get("cardId") or c_info.get("code") or "").strip()
            alt_cid = str(c_info.get("raw_id") or "").strip()

            matched_cid = cls._match_card_in_db(raw_cid) or cls._match_card_in_db(alt_cid)
            if matched_cid and str(CARD_DB[matched_cid].get("text") or "").strip():
                # 本地系列已存在此卡且具備完整效果：直接加入牌組配比，完全不動動到原本的系列卡池！
                recipe_dict[matched_cid] = recipe_dict.get(matched_cid, 0) + count
                sc = CARD_DB[matched_cid].get("series", "")
                if sc:
                    series_counts[sc] = series_counts.get(sc, 0) + count
                continue

            # 若本地尚未匯入該系列，或舊版缺少效果文，才轉換單卡供牌組使用
            full_sc = api_card_lookup.get(raw_cid.upper()) or api_card_lookup.get(alt_cid.upper())
            src_obj = dict(full_sc) if full_sc else c_info
            c_dict = cls._convert_bottleneko_card_obj(src_obj, default_series_code="CUSTOM/S01", count=0)
            if not c_dict:
                continue
            cid = matched_cid or c_dict["id"]
            c_dict["id"] = cid
            c_dict["default_count"] = 0

            if matched_cid and matched_cid in CARD_DB:
                # 僅修補文字與解析後能力，不改變卡片所屬系列與結構
                c_dict["series"] = CARD_DB[matched_cid].get("series", c_dict["series"])
                CARD_DB[matched_cid].update({
                    "text": c_dict["text"] or CARD_DB[matched_cid].get("text", ""),
                    "trigger": c_dict["trigger"],
                    "traits": c_dict["traits"] or CARD_DB[matched_cid].get("traits", []),
                    "effects": c_dict["effects"],
                    "parsed_abilities": c_dict["parsed_abilities"],
                })
            else:
                CARD_DB[cid] = c_dict
                extra_cards_to_cache[cid] = c_dict

            recipe_dict[cid] = recipe_dict.get(cid, 0) + count
            sc = CARD_DB[cid].get("series", "")
            if sc:
                series_counts[sc] = series_counts.get(sc, 0) + count

        # 若有牌組專屬的未收錄卡片，僅寫入獨立快取檔 sets/_deck_extra_cards.json，絕不觸碰任何 sets/{series}.json
        if extra_cards_to_cache:
            full_sets_dir = os.path.join(BASE_DIR, sets_dir)
            os.makedirs(full_sets_dir, exist_ok=True)
            extra_path = os.path.join(full_sets_dir, "_deck_extra_cards.json")
            existing_extra = {"cards": {}}
            if os.path.exists(extra_path):
                try:
                    with open(extra_path, "r", encoding="utf-8") as f:
                        ld = json.load(f)
                    if isinstance(ld, dict) and isinstance(ld.get("cards"), dict):
                        existing_extra = ld
                except Exception:
                    pass
            existing_extra["cards"].update(extra_cards_to_cache)
            try:
                with open(extra_path, "w", encoding="utf-8") as f:
                    json.dump(existing_extra, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        primary_series = max(series_counts, key=series_counts.get) if series_counts else "BFR/S78"
        total_cards_in_deck = sum(recipe_dict.values())
        _log(f"✅ 成功匯入社群牌組【{deck_name}】（共 {len(recipe_dict)} 種 / {total_cards_in_deck} 張卡片，未更動任何現有系列卡池）！")
        return {
            "series_code": primary_series,
            "deck_name": deck_name,
            "card_count": len(recipe_dict),
            "total_cards": total_cards_in_deck,
            "recipe": recipe_dict,
        }


# 確保所有翻譯器與萬用效果解析器定義完成後重新同步載入全部卡池
load_all_card_sets()

# 模組初始化完成後立即載入並編譯所有系列卡片 AST
load_all_card_sets()
