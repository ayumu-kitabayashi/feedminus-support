"""Bing の検索結果で minulo.app が何位か（ChatGPT の検索は Bing を使う）。
使い方: python3 tools/aeo_bing.py [en|ja|fr] 。表示URL（cite）で数える。"""
import re, sys, html, time, urllib.parse, urllib.request
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
Q = {
 "en": ["app to hide instagram reels but keep dms", "hide instagram reels iphone", "block youtube shorts iphone",
        "sociallite alternative", "opal alternative keep instagram dms", "app that blocks reels and shorts",
        "how to turn off instagram reels", "stop doomscrolling app iphone", "minulo app", "minulo reels"],
 "ja": ["インスタ リール 消す アプリ", "インスタ リール 非表示 iphone", "youtube ショート 非表示 iphone",
        "リール 制限 アプリ", "minulo アプリ"],
 "fr": ["masquer reels instagram iphone", "bloquer youtube shorts iphone", "application bloquer reels garder messages"],
}
MK = {"en": ("en-US", "US"), "ja": ("ja-JP", "JP"), "fr": ("fr-FR", "FR")}
def run(lang):
    al, cc = MK[lang]
    for q in Q[lang]:
        u = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": q, "count": 30, "setlang": al, "cc": cc})
        t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": al}), timeout=20).read().decode("utf8", "ignore")
        cites = [re.sub("<[^>]+>", "", html.unescape(c)) for c in re.findall(r'<li class="b_algo".*?<cite[^>]*>(.*?)</cite>', t, re.S)]
        hits = [f"{i}:{c[:60]}" for i, c in enumerate(cites, 1) if "minulo" in c or "feedminus" in c]
        print(f"[{lang}] {q} → {len(cites)}件 / minulo: {hits or 'なし'} / 上位3: {[c[:40] for c in cites[:3]]}", flush=True)
        time.sleep(2)
if __name__ == "__main__":
    for l in (sys.argv[1:] or ["en", "ja", "fr"]): run(l)
