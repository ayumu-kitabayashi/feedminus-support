"""Apple の検索候補（MZSearchHints）を国ごとに引く。候補に出る＝実際に打たれている語。
使い方: python3 tools/aso_hints.py jp "リール" "ショート" ...
store-ja.md「②③の叩き方」と同じヘッダ。"""
import sys, urllib.parse, urllib.request, plistlib, json
SF = {"jp": "143462", "us": "143441", "gb": "143444", "ca": "143455", "au": "143460", "fr": "143442",
      "de": "143443", "it": "143450", "es": "143454", "mx": "143468", "br": "143503", "kr": "143466",
      "nl": "143452", "pt": "143453", "in": "143467", "tr": "143480", "pl": "143478", "se": "143456",
      "tw": "143470", "id": "143476", "th": "143475", "vn": "143471", "sa": "143479", "ae": "143481"}
UA = "AppStore/3.0 iOS/18.0 model/iPhone16,1 hwp/t8130 build/22A3354 (6; dt:310) AMS/1"
def hints(cc, term):
    u = "https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?" + urllib.parse.urlencode({"clientApplication": "Software", "term": term})
    r = urllib.request.Request(u, headers={"User-Agent": UA, "X-Apple-Store-Front": SF[cc] + ",29"})
    data = urllib.request.urlopen(r, timeout=20).read()
    try: p = plistlib.loads(data); return [h["term"] for h in p.get("hints", [])]
    except Exception:
        try: return [h["term"] for h in json.loads(data).get("hints", [])]
        except Exception: return ["?", data[:80]]
if __name__ == "__main__":
    cc = sys.argv[1]
    for t in sys.argv[2:]:
        print(f"{cc} [{t}] →", " | ".join(hints(cc, t)))
