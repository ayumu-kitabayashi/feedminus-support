#!/usr/bin/env python3
"""「リールとショートを消して、DMは残せるアプリの比較」ページ（2026-09-28・ChatGPT の入口を太くする）。

★なぜ：ログインなしの ChatGPT に6通りで聞いたら、minulo は1度も挙がらなかった（名前で聞けば正しく説明する）。
  根拠にされていたのは競合の公式サイトと App Store だけ。minulo を他のアプリと並べて書いたページがどこにも無い。
★他社の事実は App Store の説明文と米国の評価数（tools/alts.json の checked の日）だけから書く。分からないことは「記載なし」。
★このページを minulo の開発者が書いていることを、ページの上に明記する（隠すと信用を失う）。
★答えの段落を先に、表、疑問形の見出しの順（AI に引用されやすい形）。

使い方:  python3 tools/alts.py   → /alternatives.html（日本語）と /en/alternatives.html
"""
import html, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('faq', HERE / 'faq.py')
F = importlib.util.module_from_spec(_s); _s.loader.exec_module(F)
D = json.loads((HERE / 'alts.json').read_text())
LANGS = ['ja', 'en', 'de', 'fr', 'es', 'pt', 'it']
PATH = 'alternatives.html'
# 手引き（tools/guides.py）は日英だけ
GUIDES = {'ja': '<a href="turn-off-instagram-reels.html">Instagramのリールをオフにする方法 →</a><a href="block-youtube-shorts.html">YouTubeのショートを止める方法 →</a>',
          'en': '<a href="turn-off-instagram-reels.html">How to turn off Instagram Reels →</a><a href="block-youtube-shorts.html">How to block YouTube Shorts →</a>'}

EXTRA = """
.disc{font-size:14px;color:var(--ink3);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:0 0 22px}
.tw{overflow-x:auto;margin:6px 0 26px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:860px;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:11px 13px;border-bottom:1px solid var(--line);line-height:1.6}
th{font-size:12.5px;color:var(--ink3);font-weight:600;white-space:nowrap}
tr:last-child td{border-bottom:none}
td.n{white-space:nowrap;font-variant-numeric:tabular-nums}
td a{color:var(--ink);font-weight:600}
tr.me td{background:var(--priSoft,#ECEEFF)}
.links{display:flex;flex-wrap:wrap;gap:8px 18px;margin:26px 0 0;font-size:14.5px}
.links a{color:var(--pri);text-decoration:none;font-weight:600}
"""


def num(n, lang):
    """桁の区切りをその言語の書き方に（ドイツ語などで 7,776 は小数に読める）"""
    s = f'{n:,}'
    return s.replace(',', '.') if lang in ('de', 'es', 'pt', 'it') else s.replace(',', '\u202f') if lang == 'fr' else s


def page(lang):
    t = D['t'][lang]; d = F.DATA[lang]
    url = F.SITE + d['dir'] + PATH
    up = '' if d['dir'] == '' else '../'
    title = t['title']; lede = t['lede']
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{F.SITE}{F.DATA[l]["dir"]}{PATH}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{F.SITE}en/{PATH}">'
    items = [{'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'MobileApplication', 'name': a['name'], 'operatingSystem': 'iOS',
              'applicationCategory': 'UtilitiesApplication', 'url': f'https://apps.apple.com/{d["store"]}/app/id{a["id"]}'}}
             for i, a in enumerate(D['apps'])]
    ld = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': lede, 'inLanguage': F.INLANG[lang],
         'datePublished': D['checked'], 'dateModified': D['checked'], 'url': url,
         'author': {'@type': 'Organization', 'name': 'ReliefNote' if lang != 'ja' else 'リリーフノート', 'url': F.SITE},
         'about': {'@type': 'ItemList', 'itemListElement': items}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': F.INLANG[lang],
         'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['qa']]},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'minulo', 'item': F.SITE + d['dir']},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url}]},
    ]
    lds = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    rows = []
    for a in D['apps']:
        link = f'https://apps.apple.com/{d["store"]}/app/id{a["id"]}'
        cls = ' class="me"' if a['name'] == 'minulo' else ''
        rows.append(f'<tr{cls}><td><a href="{link}">{html.escape(a["name"])}</a></td><td>{html.escape(a["how"][lang])}</td>'
                    f'<td>{html.escape(a["nets"][lang])}</td><td>{html.escape(a["free"][lang])}</td><td>{html.escape(a["dms"][lang])}</td>'
                    f'<td>{html.escape(a["also"][lang])}</td><td class="n">{num(a["ratings"], lang)}</td></tr>')
    head = ''.join(f'<th>{html.escape(c)}</th>' for c in t['cols'])
    qa = '\n'.join(f'<section class="qa"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></section>' for q, a in t['qa'])
    store = f"https://apps.apple.com/{d['store']}/app/id6809352229"
    langs = ''.join((f'<b>{F.NAMES[l]}</b>' if l == lang else f'<a href="{up}{F.DATA[l]["dir"]}{PATH}" hreflang="{l}" lang="{l}">{F.NAMES[l]}</a>') for l in LANGS)
    return f"""<!doctype html>
<html lang="{F.INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | minulo</title>
<meta name="description" content="{html.escape(lede)}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up}icon-32.png" sizes="32x32">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(lede)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F.SITE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(lede)}">
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
<h1>{html.escape(title)}</h1>
<p class="lede">{html.escape(lede)}</p>
<p class="upd"><time datetime="{D['checked']}">{D['checked']}</time></p>
<p class="disc">{html.escape(t['disclose'].replace('{date}', D['checked']))}</p>
<div class="tw"><table><tr>{head}</tr>
{''.join(rows)}
</table></div>
{qa}
<div class="links">{GUIDES.get(lang, '')}<a href="hide/index.html">{html.escape(t['more'])} →</a><a href="faq.html">{html.escape(t['faq'])} →</a></div>
<div class="cta"><a href="{store}"><img src="{up}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
</body>
</html>
"""


if __name__ == '__main__':
    for lang in LANGS:
        out = F.ROOT / F.DATA[lang]['dir'] / PATH
        out.write_text(page(lang)); print('wrote', out)
