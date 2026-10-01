"""minulo の検索順位を iTunes Search API（上位200）で測る。
使い方: python3 tools/aso_rank.py [出力.json]
順位はストアの検索と完全一致ではない（store-ja.md の測り方と同じ）。"""
import json, sys, time, urllib.parse, urllib.request

APP = 6809352229
TERMS = {
    "jp": ["リール 制限", "リール 非表示", "ショート 非表示", "ショート動画 制限", "ショート動画 ブロック",
           "ショート ブロッカー", "インスタ 制限", "インスタ リール 非表示", "SNS 制限", "SNS ロック",
           "おすすめ 非表示", "フィード 非表示", "tiktok 制限", "リール ブロック", "スマホ依存対策", "ドパガキ"],
    "us": ["reels blocker", "block reels", "shorts blocker", "youtube shorts blocker", "instagram blocker",
           "social media blocker", "doomscrolling", "keep dms", "hide reels", "minulo"],
    "gb": ["reels blocker", "block reels", "shorts blocker", "feed blocker", "doomscrolling"],
    "ca": ["reels blocker", "shorts blocker"],
    "au": ["reels blocker", "shorts blocker"],
    "fr": ["bloquer reels", "bloquer shorts", "reels blocker", "détox numérique", "addiction téléphone", "block youtube shorts"],
    "de": ["reels blockieren", "shorts blockieren", "reels blocker", "handysucht", "doomscroll"],
    "es": ["bloquear reels", "bloquear shorts", "adicción al móvil", "desintoxicación digital"],
    "mx": ["bloquear reels", "bloquear shorts", "adicción celular"],
    "br": ["bloquear reels", "bloquear shorts", "vício celular", "reduzir tempo de tela"],
    "it": ["bloccare reels", "bloccare shorts", "dipendenza telefono"],
    "kr": ["릴스 차단", "쇼츠 차단"],
}

def search(term, cc):
    q = urllib.parse.urlencode({"term": term, "country": cc, "entity": "software", "limit": 200})
    for _ in range(3):
        try:
            with urllib.request.urlopen(f"https://itunes.apple.com/search?{q}", timeout=20) as r:
                return json.load(r)["results"]
        except Exception:
            time.sleep(3)
    return None

out = []
for cc, terms in TERMS.items():
    for t in terms:
        res = search(t, cc)
        time.sleep(1.2)
        if res is None:
            out.append({"cc": cc, "term": t, "rank": "err"}); continue
        ids = [a["trackId"] for a in res]
        rank = ids.index(APP) + 1 if APP in ids else None
        top = [(a["trackName"][:28], a.get("userRatingCount", 0)) for a in res[:3]]
        out.append({"cc": cc, "term": t, "rank": rank, "n": len(res), "top": top})
        print(f"{cc} {t:28} {rank if rank else '圏外':>4} /{len(res):<3} {top}", flush=True)
if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
