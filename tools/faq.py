#!/usr/bin/env python3
"""よくある質問のページを7言語で組む（2026-09-27・ChatGPT の入口を太くする）。

★なぜ要るか。ASC の実測で ChatGPT 経由が DL の29%（9/9〜9/25）。
  ChatGPT は App Store のページを引いて minulo を答えていたが、名前は旧名の「FeedMinus」のまま、
  minulo.app には「質問 → そのまま引ける答え」が1つも無かった（LP は簡潔にしたときに FAQ を外した）。
★書き方の決め（supplens の docs/seo-aeo-ja.md と同じ）：
  見出しは質問の形／答えは1段落で完結（日本語 100〜190字）／代名詞で始めない／折りたたまない。
★事実はアプリの実装と訳（~/feedminus/src/i18n）から取った。呼び名（休憩する・ロックモード等）はアプリと同じ語。
★本文は tools/faq.json。ここは組むだけ。

使い方:  python3 tools/faq.py   （リポジトリのルートで）
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'tools' / 'faq.json').read_text())
CMP = json.loads((ROOT / 'tools' / 'compare.json').read_text())   # ★選び方のページ（比較）。他社の記述は App Store の説明と評価件数だけ
SITE = 'https://minulo.app/'
LANGS = ['ja', 'en', 'de', 'fr', 'es', 'pt', 'it']
NAMES = {'ja': '日本語', 'en': 'English', 'de': 'Deutsch', 'fr': 'Français', 'es': 'Español', 'pt': 'Português', 'it': 'Italiano'}
INLANG = {'ja': 'ja', 'en': 'en', 'de': 'de', 'fr': 'fr', 'es': 'es', 'pt': 'pt-BR', 'it': 'it'}

CSS = """
:root{--ink:#17181D;--ink2:#5B5C64;--ink3:#74757D;--pri:#5663E8;--priSoft:#ECEEFF;--bg:#FFF9F2;--card:#FFFFFF;--line:#E8E2D8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-size:16px;line-height:1.85;
  font-family:"Figtree","M PLUS 2",system-ui,-apple-system,"Hiragino Sans",sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ink)}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
header{padding:22px 0 8px}
header a{display:inline-block}
header img{display:block;height:24px;width:auto}
h1{font-size:30px;font-weight:600;line-height:1.35;margin:36px 0 10px;text-wrap:balance}
.lede{color:var(--ink2);margin:0 0 6px}
.upd{font-size:13px;color:var(--ink3);margin:0 0 30px}
.qa{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 24px;margin:0 0 12px}
.qa h2{font-size:18px;font-weight:600;line-height:1.5;margin:0 0 8px;text-wrap:balance}
.qa p{margin:0;color:var(--ink2)}
.cta{text-align:center;margin:36px 0 10px}
.cta img{height:54px;width:auto}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 60px;font-size:13.5px;color:var(--ink3)}
footer .langs a,footer .langs b{margin-right:12px;white-space:nowrap}
footer .langs a{color:var(--ink3);text-decoration:none}
footer .langs b{color:var(--ink);font-weight:600}
footer p{margin:10px 0 0}
.also{margin:0 0 26px;font-size:14.5px}
.also a{color:var(--pri);text-decoration:none;font-weight:600}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:18px;margin:0 0 22px}
table{border-collapse:collapse;width:100%;min-width:560px;font-size:14.5px;line-height:1.6}
th,td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}
th{font-size:12.5px;color:var(--ink3);font-weight:600}
tr:last-child td{border-bottom:none}
td:first-child{font-weight:600;color:var(--ink);white-space:nowrap}
.src{font-size:13px;color:var(--ink3);margin:18px 0 0}
@media (max-width:520px){h1{font-size:25px}.qa{padding:18px 18px}}
"""


def page(lang: str) -> str:
    d = DATA[lang]
    up = '' if d['dir'] == '' else '../'
    url = SITE + d['dir'] + 'faq.html'
    store = f"https://apps.apple.com/{d['store']}/app/id6809352229"
    alts = '\n'.join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{DATA[l]["dir"]}faq.html">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}faq.html">'
    ld_app = {
        '@context': 'https://schema.org', '@type': 'MobileApplication',
        'name': 'minulo', 'alternateName': 'FeedMinus',
        'operatingSystem': 'iOS', 'applicationCategory': 'UtilitiesApplication',
        'description': d['lede'], 'inLanguage': INLANG[lang],
        'url': SITE + d['dir'], 'installUrl': store,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'JPY' if lang == 'ja' else 'USD'},
    }
    ld_faq = {
        '@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': INLANG[lang],
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in d['qa']],
    }
    qa = '\n'.join(
        f'<section class="qa"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></section>' for q, a in d['qa'])
    langs = ''.join(
        (f'<b>{NAMES[l]}</b>' if l == lang else
         f'<a href="{up}{DATA[l]["dir"]}faq.html" hreflang="{l}" lang="{l}">{NAMES[l]}</a>') for l in LANGS)
    return f"""<!doctype html>
<html lang="{INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(d['title'])}</title>
<meta name="description" content="{html.escape(d['lede'])}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up}icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{up}icon-180.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(d['title'])}">
<meta property="og:description" content="{html.escape(d['lede'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=M+PLUS+2:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld_app, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><a href="{up}{d['dir']}" aria-label="{html.escape(d['home'])}"><img src="{up}logo-trim.png" alt="minulo" width="140" height="24"></a></header>
<main>
<h1>{html.escape(d['title'])}</h1>
<p class="lede">{html.escape(d['lede'])}</p>
<p class="upd">{html.escape(d['updated'])}</p>
<p class="also"><a href="compare.html">{html.escape(CMP[lang]['title'])} →</a></p>
{qa}
<div class="cta"><a href="{store}"><img src="{up}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
</body>
</html>
"""


def compare(lang: str) -> str:
    d, c = DATA[lang], CMP[lang]
    up = '' if d['dir'] == '' else '../'
    url = SITE + d['dir'] + 'compare.html'
    store = f"https://apps.apple.com/{d['store']}/app/id6809352229"
    alts = '\n'.join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{DATA[l]["dir"]}compare.html">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}compare.html">'
    ld_art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': c['title'], 'description': c['lede'],
              'inLanguage': INLANG[lang], 'datePublished': '2026-09-27', 'dateModified': '2026-09-27',
              'author': {'@type': 'Person', 'name': 'Ayumu Kitabayashi'},
              'publisher': {'@type': 'Organization', 'name': 'minulo', 'url': SITE},
              'mainEntityOfPage': url}
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': INLANG[lang],
              'mainEntity': [{'@type': 'Question', 'name': q,
                              'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['qa']]}
    head = ''.join(f'<th>{html.escape(x)}</th>' for x in c['cols'])
    body = ''.join('<tr>' + ''.join(f'<td>{html.escape(x)}</td>' for x in r) + '</tr>' for r in c['rows'])
    qa = '\n'.join(
        f'<section class="qa"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></section>' for q, a in c['qa'])
    langs = ''.join(
        (f'<b>{NAMES[l]}</b>' if l == lang else
         f'<a href="{up}{DATA[l]["dir"]}compare.html" hreflang="{l}" lang="{l}">{NAMES[l]}</a>') for l in LANGS)
    return f"""<!doctype html>
<html lang="{INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['title'])} | minulo</title>
<meta name="description" content="{html.escape(c['lede'])}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up}icon-32.png" sizes="32x32">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(c['title'])}">
<meta property="og:description" content="{html.escape(c['lede'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=M+PLUS+2:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld_art, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><a href="{up}{d['dir']}" aria-label="{html.escape(d['home'])}"><img src="{up}logo-trim.png" alt="minulo" width="140" height="24"></a></header>
<main>
<h1>{html.escape(c['title'])}</h1>
<p class="lede">{html.escape(c['lede'])}</p>
<p class="upd">{html.escape(d['updated'])}</p>
<div class="tw"><table><tr>{head}</tr>{body}</table></div>
{qa}
<p class="src">{html.escape(c['src'])}</p>
<p class="also"><a href="faq.html">{html.escape(c['more'])} →</a></p>
<div class="cta"><a href="{store}"><img src="{up}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
</body>
</html>
"""


def main():
    for lang in LANGS:
        for name, fn in (('faq.html', page), ('compare.html', compare)):
            out = ROOT / DATA[lang]['dir'] / name
            out.write_text(fn(lang))
            print('書き出し', out.relative_to(ROOT))


if __name__ == '__main__':
    main()
