#!/usr/bin/env python3
"""SNS ごとの「消し方」のページを組む（2026-09-27・ChatGPT の入口を太くする）。

★ChatGPT への質問は「Instagram のリールを消す方法」のように SNS ごとに来る。
  FAQ は minulo 全体の話なので、10サービス×7言語の「消し方」を置く。
★消せるもの・すぐ開ける画面は、**アプリのルールの定義と訳から取った**（tools/rules.json）。
  作り直すとき：~/feedminus で rules-dump.ts を tsx で流して rules.json を上書きする
  （SHIPPED の rules から hideRow を除き、group ごとに1行＝設定画面と同じ行）。
★公式アプリの設定については書かない（確かめられない事実を書かない）。書くのは minulo で起きることだけ。
★ボタン名（サービスを追加・ブロック等）は hide.json の ui に、アプリの訳から写してある。

使い方:  python3 tools/hide.py   （リポジトリのルートで。faq.py の見た目と言語の設定を使う）
"""
import html
import importlib.util
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('faq', HERE / 'faq.py')
F = importlib.util.module_from_spec(_s); _s.loader.exec_module(F)

RULES = json.loads((HERE / 'rules.json').read_text())
T = json.loads((HERE / 'hide.json').read_text())
ORDER = ['instagram', 'youtube', 'tiktok', 'x', 'threads', 'facebook', 'pinterest', 'reddit', 'linkedin', 'snapchat']

EXTRA = """
.qa ul,.qa ol{margin:10px 0 0;padding-left:1.3em;color:var(--ink2)}
.qa li{margin:4px 0}
.svc{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin:0 0 20px}
.svc a{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px;text-decoration:none;color:var(--ink);font-weight:600}
.svc img{width:28px;height:28px;border-radius:7px}
.svc span{display:block;font-weight:400;font-size:13px;color:var(--ink3);line-height:1.4}
.links{display:flex;flex-wrap:wrap;gap:8px 18px;margin:26px 0 0;font-size:14.5px}
.links a{color:var(--pri);text-decoration:none;font-weight:600}
"""


AND = {'ja': None, 'en': ' and ', 'de': ' und ', 'fr': ' et ', 'es': ' y ', 'pt': ' e ', 'it': ' e '}


def join(lang, items, sep):
    """並べ方。日本語は「、」だけ。ほかは最後を「と」にあたる語でつなぐ（A, B and C）"""
    if AND[lang] is None or len(items) < 2:
        return sep.join(items)
    return sep.join(items[:-1]) + AND[lang] + items[-1]


def short(label):
    """見出しに入れるときは、括弧の補足（「（フォロー中を開く）」など）を外す"""
    import re
    return re.sub(r'\s*[（(][^）)]*[）)]\s*$', '', label)


def fill(s, **kw):
    for k, v in kw.items():
        s = s.replace('{' + k + '}', v)
    return s


def head(lang, title, desc, path, ld):
    d = F.DATA[lang]
    up = '' if d['dir'] == '' else '../'
    up2 = up + '../'
    url = F.SITE + d['dir'] + path
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{F.SITE}{F.DATA[l]["dir"]}{path}">' for l in F.LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{F.SITE}{path}">'
    lds = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="{F.INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | minulo</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up2}icon-32.png" sizes="32x32">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F.SITE}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600&family=M+PLUS+2:wght@400;500;600&display=swap" rel="stylesheet">
{lds}
<style>{F.CSS}{EXTRA}</style>
</head>
<body>
<div class="wrap">
<header><a href="{up2}{d['dir']}" aria-label="{html.escape(d['home'])}"><img src="{up2}logo-trim.png" alt="minulo" width="140" height="24"></a></header>
<main>
"""


def tail(lang, path, t, body_links=True):
    d = F.DATA[lang]
    up2 = ('' if d['dir'] == '' else '../') + '../'
    store = f"https://apps.apple.com/{d['store']}/app/id6809352229"
    langs = ''.join(
        (f'<b>{F.NAMES[l]}</b>' if l == lang else
         f'<a href="{up2}{F.DATA[l]["dir"]}{path}" hreflang="{l}" lang="{l}">{F.NAMES[l]}</a>') for l in F.LANGS)
    links = (f'<div class="links"><a href="index.html">{html.escape(t["other"])} →</a>'
             f'<a href="../faq.html">{html.escape(t["faq"])} →</a><a href="../compare.html">{html.escape(t["cmp"])} →</a></div>') if body_links else ''
    return f"""{links}
<div class="cta"><a href="{store}"><img src="{up2}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
</body>
</html>
"""


def service(lang, sid):
    t, r = T[lang], RULES[sid]
    name, tr = r['name'], r['tr'][lang]
    # ★フランス語の「de」は母音の前で d' になる（de Instagram → d'Instagram）
    de_name = ("d'" + name) if name[0].lower() in 'aeiou' else ('de ' + name)
    kw = dict(name=name, de_name=de_name, t0=short(tr['rows'][0]), intents=join(lang, tr['intents'], t['sep']), **t['ui'])
    h1, lede = fill(t['h1'], **kw), fill(t['lede'], **kw)
    steps = [fill(s, **kw) for s in t['steps']]
    qas = [(fill(t['q1'], **kw), fill(t['a1'], **kw), tr['rows']),
           (fill(t['q2'], **kw), fill(t['a2'], **kw), None),
           (fill(t['q3'], **kw), None, steps),
           (fill(t['q4'], **kw), fill(t['a4'], **kw), None),
           (fill(t['q5'], **kw), fill(t['a5'], **kw), None)]
    path = f'hide/{sid}.html'
    ld_how = {'@context': 'https://schema.org', '@type': 'HowTo', 'name': h1, 'inLanguage': F.INLANG[lang],
              'step': [{'@type': 'HowToStep', 'position': i + 1, 'text': s} for i, s in enumerate(steps)]}
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': F.INLANG[lang],
              'mainEntity': [{'@type': 'Question', 'name': q,
                              'acceptedAnswer': {'@type': 'Answer', 'text': (a or '') + (' ' + ' / '.join(lst) if lst else '')}}
                             for q, a, lst in qas]}
    out = [head(lang, h1, lede, path, [ld_how, ld_faq]),
           f'<h1>{html.escape(h1)}</h1>\n<p class="lede">{html.escape(lede)}</p>\n<p class="upd">{html.escape(F.DATA[lang]["updated"])}</p>']
    for i, (q, a, lst) in enumerate(qas):
        inner = f'<p>{html.escape(a)}</p>' if a else ''
        if lst:
            tag = 'ol' if i == 2 else 'ul'
            inner += f'<{tag}>' + ''.join(f'<li>{html.escape(x)}</li>' for x in lst) + f'</{tag}>'
        out.append(f'<section class="qa"><h2>{html.escape(q)}</h2>{inner}</section>')
    out.append(tail(lang, path, t))
    return '\n'.join(out)


def hub(lang):
    t = T[lang]
    up2 = ('' if F.DATA[lang]['dir'] == '' else '../') + '../'
    items = ''.join(
        f'<a href="{sid}.html"><img src="{up2}svc/{sid}.png" alt="" width="28" height="28">'
        f'<div>{html.escape(RULES[sid]["name"])}<span>{html.escape(short(RULES[sid]["tr"][lang]["rows"][0]))}</span></div></a>'
        for sid in ORDER)
    path = 'hide/index.html'
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': t['hub'], 'inLanguage': F.INLANG[lang],
          'hasPart': [{'@type': 'WebPage', 'url': F.SITE + F.DATA[lang]['dir'] + f'hide/{sid}.html'} for sid in ORDER]}
    return '\n'.join([head(lang, t['hub'], t['hubLede'], path, [ld]),
                      f'<h1>{html.escape(t["hub"])}</h1>\n<p class="lede">{html.escape(t["hubLede"])}</p>\n<p class="upd">{html.escape(F.DATA[lang]["updated"])}</p>',
                      f'<nav class="svc">{items}</nav>',
                      f'<div class="links"><a href="../faq.html">{html.escape(t["faq"])} →</a><a href="../compare.html">{html.escape(t["cmp"])} →</a></div>',
                      tail(lang, path, t, body_links=False)])


def main():
    n = 0
    for lang in F.LANGS:
        base = F.ROOT / F.DATA[lang]['dir'] / 'hide'
        base.mkdir(parents=True, exist_ok=True)
        (base / 'index.html').write_text(hub(lang)); n += 1
        for sid in ORDER:
            (base / f'{sid}.html').write_text(service(lang, sid)); n += 1
    print('書き出し', n, 'ページ')


if __name__ == '__main__':
    main()
