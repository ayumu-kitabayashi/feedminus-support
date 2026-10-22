#!/usr/bin/env python3
"""「iPhoneでYouTubeのショートを止める方法」「Instagramのリールを止める方法」— すべての方法を公平に並べた手引き（2026-09-28）。

★なぜ：ChatGPT に「YouTube のショートだけ止めたい」と聞くと、アプリ名を1つも出さずに一般論で答えた。
  公式の設定からアプリまでを1ページにまとめた、出典つきの手引きなら引用される余地がある。
★事実は公式のヘルプを優先し、出典と確かめた日を書く。確かめられないことは書かないか「未確認」と書く。
  YouTube は 2026-04 から大人もショートの上限を 0 分にできる（ただし上限は閉じられる）。これを隠さない。
★開発者が書いていることを明記する。

使い方:  python3 tools/guides.py   → /en/block-youtube-shorts.html ほか（日英）
        python3 tools/guides.py id th vi ru zh-Hant   → その言語だけ書き出す（2026-10-22〜）
★2026-10-22：既存の7言語のページは公開後に手で直した所（題・関連リンク・hreflang）があり、
  引数なしで回すと戻ってしまう。新しい言語を足すときは言語を引数に渡し、その言語だけ書き出す。
  そのとき、同じページのほかの言語（手書きのページも含む）の hreflang・フッター・sitemap.xml に新しい言語を足す。
  hreflang は「guides.json に訳がある言語＋ディスクにページがある言語」。書き出したあとは tools/ct.py も回す。
★任意のキー：seo（<title>）・desc（meta description）・date（公開日）・links（[[文, href], …]）・
  src（その言語の出典名と URL）・steps（{h, items, after}：表のあとの手順）・
  secs（[[見出し, [段落の HTML, …]], …]：表のあと・Q&A の前の地の文。<p>・<ol> を含む自前の HTML）。無ければ従来どおり。
"""
import datetime, html, importlib.util, json, pathlib, re, sys

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
ALL = ['ja', 'en', 'de', 'fr', 'es', 'pt', 'it', 'ko', 'zh-Hant', 'id', 'th', 'vi', 'ru']
# faq.json に無い言語の札（LP・FAQ の公開ページと同じ値）
XL = {
    'ko': dict(dir='ko/', store='kr', badge='appstore-en-us', badgeAlt='Download on the App Store', home='홈'),
    'zh-Hant': dict(dir='zh-Hant/', store='tw', badge='appstore-en-us', badgeAlt='Download on the App Store', home='首頁'),
    'id': dict(dir='id/', store='id', badge='appstore-en-us', badgeAlt='Download on the App Store', home='Beranda'),
    'th': dict(dir='th/', store='th', badge='appstore-en-us', badgeAlt='Download on the App Store', home='หน้าแรก'),
    'vi': dict(dir='vi/', store='vn', badge='appstore-en-us', badgeAlt='Download on the App Store', home='Trang chủ'),
    'ru': dict(dir='ru/', store='', badge='appstore-en-us', badgeAlt='Download on the App Store', home='Главная'),
}
D = {**XL, **F.DATA}
NAMES = {**F.NAMES, 'ko': '한국어', 'zh-Hant': '繁體中文', 'id': 'Bahasa Indonesia', 'th': 'ไทย', 'vi': 'Tiếng Việt', 'ru': 'Русский'}
INLANG = {**F.INLANG, 'ko': 'ko', 'zh-Hant': 'zh-Hant', 'id': 'id', 'th': 'th', 'vi': 'vi', 'ru': 'ru'}


def langs_of(path):   # ページごとに、訳のある言語＋手書きでページがある言語
    return [l for l in ALL if l in G[path] or (F.ROOT / D[l]['dir'] / path).exists()]


def page(path, lang):
    g = G[path]; t = g[lang]; d = D[lang]
    ck = g.get('checked', CHECKED)   # ページごとに確かめた日（無ければ共通の日）
    url = F.SITE + d['dir'] + path
    up = '' if d['dir'] == '' else '../'
    LANGS = langs_of(path)
    alts = '\n'.join(f'<link rel="alternate" hreflang="{INLANG[l]}" href="{F.SITE}{D[l]["dir"]}{path}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{F.SITE}en/{path}">'
    pub = t.get('date', ck)   # 公開日（無ければ確かめた日）
    srcs = t.get('src', g.get('src', []))   # 出典（その言語の名前があればそれ）
    seo, desc = t.get('seo', t['title']), t.get('desc', t['lede'])
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': t['title'], 'description': t['lede'], 'inLanguage': INLANG[lang],
           'datePublished': pub, 'dateModified': pub, 'url': url,
           'author': {'@type': 'Organization', 'name': 'ReliefNote' if lang != 'ja' else 'リリーフノート', 'url': F.SITE}}
    if srcs: art['citation'] = [u for _, u in srcs]
    ld = [
        art,
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': INLANG[lang],
         'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['qa']]},
    ]
    lds = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    head = ''.join(f'<th>{html.escape(c)}</th>' for c in t['cols'])
    rows = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in t['rows'])   # 表の中身は <b> を含む自前の文
    qa = '\n'.join(f'<section class="qa"><h2>{html.escape(q)}</h2><p>{html.escape(a)}</p></section>' for q, a in t['qa'])
    src = ''.join(f'<li><a href="{u}" rel="noopener">{html.escape(n)}</a></li>' for n, u in srcs)
    srcsec = f'<section class="qa"><h2>{html.escape(t["srcTitle"])}</h2><ol class="src">{src}</ol></section>\n' if srcs else ''
    st = t.get('steps')   # 手順（<b> を含む自前の文）
    steps = (f'<section class="qa"><h2>{html.escape(st["h"])}</h2><ol>' + ''.join(f'<li>{x}</li>' for x in st['items']) + '</ol>'
             + (f'<p>{html.escape(st["after"])}</p>' if st.get('after') else '') + '</section>\n') if st else ''
    secs = ''.join(f'<section class="qa"><h2>{html.escape(h)}</h2>' + ''.join(body) + '</section>\n' for h, body in t.get('secs', []))
    links = t.get('links') or [[t['more'], t['moreHref']], [t['faq'], t['faqHref']]]
    links = ''.join(f'<a href="{h}">{html.escape(x)} →</a>' for x, h in links)
    store = f"https://apps.apple.com/{d['store'] + '/' if d['store'] else ''}app/id6809352229"
    langs = ''.join((f'<b>{NAMES[l]}</b>' if l == lang else f'<a href="{up}{D[l]["dir"]}{path}" hreflang="{INLANG[l]}" lang="{INLANG[l]}">{NAMES[l]}</a>') for l in LANGS)
    return f"""<!doctype html>
<html lang="{INLANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(seo)} | minulo</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" href="{up}icon-32.png" sizes="32x32">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(seo)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{F.SITE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(seo)}">
<meta name="twitter:description" content="{html.escape(desc)}">
{lds}
<link rel="stylesheet" href="/article.css">
</head>
<body>
<div class="wrap">
<header><a href="{up}{d['dir']}" aria-label="{html.escape(d['home'])}"><img src="{up}logo-trim.png" alt="minulo" width="140" height="24"></a></header>
<main>
<h1>{html.escape(t['title'])}</h1>
<p class="lede">{html.escape(t['lede'])}</p>
<p class="upd"><time datetime="{pub}">{pub}</time></p>
<p class="disc">{html.escape(t['disclose'].replace('{date}', ck))}</p>
<div class="tw"><table><tr>{head}</tr>{rows}</table></div>
{steps}{secs}{qa}
{srcsec}<div class="links">{links}</div>
<div class="cta"><a href="{store}"><img src="{up}badges/{d['badge']}.svg" alt="{html.escape(d['badgeAlt'])}" height="54"></a></div>
</main>
<footer><div class="langs">{langs}</div><p>© 2026 minulo</p></footer>
</div>
<script src="/t.js" defer></script>
</body>
</html>
"""


def rel(src_lang, dst_lang, path):   # src_lang のページから dst_lang のページへの相対パス
    return ('' if D[src_lang]['dir'] == '' else '../') + D[dst_lang]['dir'] + path


def sync_others(path, done):
    """同じページのほかの言語（手書き含む）に、新しい言語の hreflang とフッターのリンクを足す。消しはしない。"""
    LANGS = langs_of(path)
    for l in LANGS:
        if l in done:
            continue
        f = F.ROOT / D[l]['dir'] / path
        s = f.read_text()
        for n in LANGS:
            href = f'{F.SITE}{D[n]["dir"]}{path}'
            if f'hreflang="{INLANG[n]}" href="{href}"' not in s:
                xd = re.search(r'<link rel="alternate" hreflang="x-default"[^>]*>', s)
                s = s[:xd.start()] + f'<link rel="alternate" hreflang="{INLANG[n]}" href="{href}">\n' + s[xd.start():]
            m = re.search(r'<div class="langs">(.*?)</div>', s)
            if m and n != l and f'hreflang="{INLANG[n]}" lang=' not in m.group(1):
                a = f'<a href="{rel(l, n, path)}" hreflang="{INLANG[n]}" lang="{INLANG[n]}">{NAMES[n]}</a>'
                s = s[:m.end(1)] + a + s[m.end(1):]
        f.write_text(s); print('hreflang', f.relative_to(F.ROOT))


def sync_sitemap(path, done, today):
    """sitemap.xml のこのページの <url> を、全言語の hreflang つきに揃える（無い言語は足す）。"""
    sm = F.ROOT / 'sitemap.xml'; s = sm.read_text()
    LANGS = langs_of(path)
    alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{INLANG[l]}" href="{F.SITE}{D[l]["dir"]}{path}"/>' for l in LANGS)
    alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{F.SITE}en/{path}"/>'
    add = ''
    for l in LANGS:
        loc = f'{F.SITE}{D[l]["dir"]}{path}'
        m = re.search(r'[ ]*<url><loc>' + re.escape(loc) + r'</loc><lastmod>([^<]*)</lastmod>.*?</url>', s, re.S)
        lastmod = today if l in done or not m else m.group(1)
        block = f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>{alts}</url>'
        if m:
            s = s[:m.start()] + block + s[m.end():]
        else:
            add += block + '\n'
    s = s.replace('</urlset>', add + '</urlset>')
    sm.write_text(s); print('sitemap', path)


if __name__ == '__main__':
    only = sys.argv[1:]
    if not only:   # 従来どおり全部（既存ページの手直しが戻るので注意）
        for path in G:
            for lang in [l for l in langs_of(path) if l in G[path]]:
                out = F.ROOT / D[lang]['dir'] / path
                out.write_text(page(path, lang)); print('wrote', out)
    else:
        today = datetime.date.today().isoformat()
        for path in G:
            done = [l for l in only if l in G[path]]
            if not done:
                continue
            for lang in done:
                out = F.ROOT / D[lang]['dir'] / path
                out.write_text(page(path, lang)); print('wrote', out.relative_to(F.ROOT))
            sync_others(path, done)
            sync_sitemap(path, done, today)
