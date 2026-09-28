#!/usr/bin/env python3
"""「iPhoneでYouTubeのショートを止める方法」「Instagramのリールを止める方法」— すべての方法を公平に並べた手引き（2026-09-28）。

★なぜ：ChatGPT に「YouTube のショートだけ止めたい」と聞くと、アプリ名を1つも出さずに一般論で答えた。
  公式の設定からアプリまでを1ページにまとめた、出典つきの手引きなら引用される余地がある。
★事実は公式のヘルプを優先し、出典と確かめた日を書く。確かめられないことは書かないか「未確認」と書く。
  YouTube は 2026-04 から大人もショートの上限を 0 分にできる（ただし上限は閉じられる）。これを隠さない。
★開発者が書いていることを明記する。

使い方:  python3 tools/guides.py   → /en/block-youtube-shorts.html ほか（日英）
"""
import html, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('faq', HERE / 'faq.py')
F = importlib.util.module_from_spec(_s); _s.loader.exec_module(F)
CHECKED = '2026-09-28'

EXTRA = """
.disc{font-size:14px;color:var(--ink3);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:0 0 22px}
.tw{overflow-x:auto;margin:6px 0 26px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:14px;table-layout:fixed}
th:nth-child(1),td:nth-child(1){width:28%}
th:nth-child(2),td:nth-child(2){width:36%}
th,td{white-space:normal!important;word-break:auto-phrase}
th,td{text-align:left;vertical-align:top;padding:11px 13px;border-bottom:1px solid var(--line);line-height:1.6}
th{font-size:12.5px;color:var(--ink3);font-weight:600;white-space:nowrap}
tr:last-child td{border-bottom:none}
td b{font-weight:600}
ol.src{font-size:13.5px;color:var(--ink3);padding-left:1.3em}
ol.src a{color:var(--ink3);word-break:break-all}
.links{display:flex;flex-wrap:wrap;gap:8px 18px;margin:26px 0 0;font-size:14.5px}
.links a{color:var(--pri);text-decoration:none;font-weight:600}
"""

G = json.loads((HERE / 'guides.json').read_text())   # 中身は guides.json（言語ごと）
ALL = ['ja', 'en', 'de', 'fr', 'es', 'pt', 'it']
def langs_of(path): return [l for l in ALL if l in G[path]]   # ページごとに、訳のある言語だけ


def page(path, lang):
    g = G[path]; t = g[lang]; d = F.DATA[lang]
    url = F.SITE + d['dir'] + path
    up = '' if d['dir'] == '' else '../'
    LANGS = langs_of(path)
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{F.SITE}{F.DATA[l]["dir"]}{path}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{F.SITE}en/{path}">'
    ld = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': t['title'], 'description': t['lede'], 'inLanguage': F.INLANG[lang],
         'datePublished': CHECKED, 'dateModified': CHECKED, 'url': url,
         'author': {'@type': 'Organization', 'name': 'ReliefNote' if lang != 'ja' else 'リリーフノート', 'url': F.SITE},
         'citation': [u for _, u in g['src']]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': F.INLANG[lang],
         'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['qa']]},
    ]
    lds = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    head = ''.join(f'<th>{html.escape(c)}</th>' for c in t['cols'])
    rows = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in t['rows'])   # 表の中身は <b> を含む自前の文
    qa = '\n'.join(f'<section class="qa"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></section>' for q, a in t['qa'])
    src = ''.join(f'<li><a href="{u}" rel="noopener">{html.escape(n)}</a></li>' for n, u in g['src'])
    store = f"https://apps.apple.com/{d['store']}/app/id6809352229"
    langs = ''.join((f'<b>{F.NAMES[l]}</b>' if l == lang else f'<a href="{up}{F.DATA[l]["dir"]}{path}" hreflang="{l}" lang="{l}">{F.NAMES[l]}</a>') for l in LANGS)
    return f"""<!doctype html>
<html lang="{F.INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])} | minulo</title>
<meta name="description" content="{html.escape(t['lede'])}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up}icon-32.png" sizes="32x32">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(t['title'])}">
<meta property="og:description" content="{html.escape(t['lede'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F.SITE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(t['title'])}">
<meta name="twitter:description" content="{html.escape(t['lede'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=M+PLUS+2:wght@400;500;600&display=swap" rel="stylesheet">
{lds}
<style>{F.CSS}{EXTRA}</style>
</head>
<body>
<div class="wrap">
<header><a href="{up}{d['dir']}" aria-label="{html.escape(d['home'])}"><img src="{up}logo-trim.png" alt="minulo" width="140" height="24"></a></header>
<main>
<h1>{html.escape(t['title'])}</h1>
<p class="lede">{html.escape(t['lede'])}</p>
<p class="upd"><time datetime="{CHECKED}">{CHECKED}</time></p>
<p class="disc">{html.escape(t['disclose'].replace('{date}', CHECKED))}</p>
<div class="tw"><table><tr>{head}</tr>{rows}</table></div>
{qa}
<section class="qa"><h2>{html.escape(t['srcTitle'])}</h2><ol class="src">{src}</ol></section>
<div class="links"><a href="{t['moreHref']}">{html.escape(t['more'])} →</a><a href="{t['faqHref']}">{html.escape(t['faq'])} →</a></div>
<div class="cta"><a href="{store}"><img src="{up}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
</body>
</html>
"""


if __name__ == '__main__':
    for path in G:
        for lang in langs_of(path):
            out = F.ROOT / F.DATA[lang]['dir'] / path
            out.write_text(page(path, lang)); print('wrote', out)
