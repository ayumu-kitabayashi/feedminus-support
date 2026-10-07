#!/usr/bin/env python3
"""LP（7言語のトップ）を AI 検索に引用されやすい形に整える（2026-09-28・AgentSignal の AIO 診断 68点への対応）。

何度流しても同じ結果になる（済んでいる所は触らない）。
  ・ヒーローの見出しを h1 に（見た目は h2 と同じ）
  ・フッターの小見出し h4 を見出しでない札に（h2 → h4 の飛ばしをなくす）
  ・twitter:title / twitter:description
  ・JSON-LD：アプリの説明を直し（FAQ の文が混ざっていた）、WebSite・Organization・WebPage（公開日・更新日）を足す
  ・フッターに運営者と更新日（<time>）、運営者情報へのリンク
  ・サービスのアイコンとミヌの画像に alt
★嘘は足さない：公式 SNS は無いので sameAs と SNS リンクは入れない。見出しを無理に疑問文にしない（広告のコピーなので）。

使い方:  python3 tools/lp_aio.py   （リポジトリのルートで）
"""
import json, pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://minulo.app/'
PUBLISHED = '2026-09-08'   # LP を入口にした日（git の履歴）
MODIFIED = '2026-10-07'
LANGS = {
    'ja': dict(dir='', op='運営', opname='リリーフノート', upd='更新', about='運営者情報', minu='minulo のキャラクター、ミヌ', aboutHref='support.html#operator'),
    'en': dict(dir='en/', op='Operated by', opname='ReliefNote', upd='Updated', about='About us', minu='Minu, the minulo character', aboutHref='support.html#operator'),
    'de': dict(dir='de/', op='Betrieben von', opname='ReliefNote', upd='Aktualisiert', about='Über uns', minu='Minu, die Figur von minulo', aboutHref='../en/support.html#operator'),
    'fr': dict(dir='fr/', op='Édité par', opname='ReliefNote', upd='Mis à jour le', about='À propos', minu='Minu, le personnage de minulo', aboutHref='../en/support.html#operator'),
    'es': dict(dir='es/', op='Gestionado por', opname='ReliefNote', upd='Actualizado', about='Quiénes somos', minu='Minu, el personaje de minulo', aboutHref='../en/support.html#operator'),
    'pt': dict(dir='pt/', op='Mantido por', opname='ReliefNote', upd='Atualizado em', about='Sobre nós', minu='Minu, o personagem do minulo', aboutHref='../en/support.html#operator'),
    'it': dict(dir='it/', op='Gestito da', opname='ReliefNote', upd='Aggiornato il', about='Chi siamo', minu='Minu, il personaggio di minulo', aboutHref='../en/support.html#operator'),
}
SVC = {'tiktok': 'TikTok', 'instagram': 'Instagram', 'youtube': 'YouTube', 'x': 'X', 'threads': 'Threads', 'facebook': 'Facebook',
       'pinterest': 'Pinterest', 'reddit': 'Reddit', 'linkedin': 'LinkedIn', 'snapchat': 'Snapchat'}


def meta(s, prop, attr='property'):
    m = re.search(rf'<meta {attr}="{re.escape(prop)}" content="([^"]*)"', s)
    return html.unescape(m.group(1)) if m else ''


def fix(lang, cfg):
    p = ROOT / cfg['dir'] / 'index.html'
    s = p.read_text()
    url = SITE + cfg['dir']
    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    desc = meta(s, 'description', 'name')

    # 1) ヒーローの見出し → h1（最初の h2 だけ）
    m = re.search(r'<h2 style="font-size:clamp\(31px,4\.1vw,52px\)[^"]*">(.*?)</h2>', s, re.S)
    if m:
        s = s[:m.start()] + m.group(0).replace('<h2', '<h1', 1)[:-5] + '</h1>' + s[m.end():]
    if 'h1{margin:0' not in s:
        s = s.replace('h2{margin:0;', 'h1{margin:0;font-weight:600;letter-spacing:-.02em;word-break:auto-phrase}\nh2{margin:0;', 1)

    # 2) フッターの h4 → 見出しでない札
    s = s.replace('footer h4{', 'footer .fh{')
    s = re.sub(r'<h4>(.*?)</h4>', r'<p class="fh">\1</p>', s)

    # 3) Twitter Card
    if 'twitter:title' not in s:
        s = s.replace('<meta name="twitter:card" content="summary_large_image">',
                      '<meta name="twitter:card" content="summary_large_image">\n'
                      f'<meta name="twitter:title" content="{html.escape(title, quote=True)}">\n'
                      f'<meta name="twitter:description" content="{html.escape(desc, quote=True)}">', 1)

    # 4) JSON-LD：アプリの説明を直して、@graph にまとめる
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    app = json.loads(m.group(1))
    if app.get('@type') == 'MobileApplication':
        app.pop('@context', None)
        app['@id'] = SITE + '#app'
        app['description'] = desc
        app['publisher'] = {'@id': SITE + '#org'}
        graph = {'@context': 'https://schema.org', '@graph': [
            app,
            {'@type': 'Organization', '@id': SITE + '#org', 'name': 'ReliefNote' if lang != 'ja' else 'リリーフノート',
             'alternateName': 'リリーフノート' if lang != 'ja' else 'ReliefNote', 'url': SITE, 'logo': SITE + 'icon-180.png',
             'email': 'workflowai.japan@gmail.com', 'founder': {'@type': 'Person', 'name': 'Ayumu Kitabayashi' if lang != 'ja' else '北林 歩'}},
            {'@type': 'WebSite', '@id': SITE + '#website', 'name': 'minulo', 'url': SITE, 'inLanguage': app.get('inLanguage', lang),
             'publisher': {'@id': SITE + '#org'}},
            {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': title, 'description': desc, 'inLanguage': app.get('inLanguage', lang),
             'isPartOf': {'@id': SITE + '#website'}, 'about': {'@id': SITE + '#app'},
             'datePublished': PUBLISHED, 'dateModified': MODIFIED},
        ]}
        s = s[:m.start()] + '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + '</script>' + s[m.end():]
    else:  # 済み：更新日だけ進める
        s = re.sub(r'"dateModified": "[\d-]+"', f'"dateModified": "{MODIFIED}"', s)

    # 5) フッター：運営者・更新日・運営者情報へのリンク
    if 'class="opby"' not in s:
        s = s.replace('<span>© 2026 minulo</span>',
                      f'<span>© 2026 minulo<span class="dot" aria-hidden="true"> · </span><span class="opby">{cfg["op"]} <a href="{cfg["aboutHref"]}">{cfg["opname"]}</a></span>'
                      f'<span class="dot" aria-hidden="true"> · </span><span class="opby">{cfg["upd"]} <time datetime="{MODIFIED}">{MODIFIED}</time></span></span>', 1)
        s = s.replace('<li><a href="./privacy.html">', f'<li><a href="{cfg["aboutHref"]}">{cfg["about"]}</a></li><li><a href="./privacy.html">', 1)
        s = s.replace('footer .fh{', '.opby a{text-decoration:underline;text-underline-offset:3px}\nfooter .fh{', 1)
    else:
        s = re.sub(r'<time datetime="[\d-]+">[\d-]+</time>', f'<time datetime="{MODIFIED}">{MODIFIED}</time>', s)

    # 6) alt
    s = re.sub(r'<img src="((?:\.\./)?svc/([a-z]+)\.png)" alt="">', lambda m: f'<img src="{m.group(1)}" alt="{SVC.get(m.group(2), m.group(2))}">', s)
    s = re.sub(r'<img class="minu" src="([^"]+)" alt=""', lambda m: f'<img class="minu" src="{m.group(1)}" alt="{cfg["minu"]}"', s)

    p.write_text(s)
    n_h1 = s.count('<h1'); n_h4 = s.count('<h4'); empty = len(re.findall(r'alt=""', s))
    print(f'{lang}: h1={n_h1} h4={n_h4} 空alt={empty} ld={s.count("application/ld+json")} tw={s.count("twitter:")}')


def support_operator():
    """support.html（日本語）と en/support.html に運営者の節（#operator）"""
    blocks = {
        'support.html': ('<h2 id="operator">運営者</h2>\n<div class="box">\n'
                         '  <p>屋号：リリーフノート（個人事業、2025年7月開業）</p>\n'
                         '  <p>代表：北林 歩</p>\n'
                         '  <p>所在地：北海道</p>\n'
                         '  <p>提供しているアプリ：minulo（iPhone・Mac・Chrome）</p>\n'
                         '  <p>連絡先：<a href="mailto:workflowai.japan@gmail.com">workflowai.japan@gmail.com</a></p>\n</div>\n\n', '<h2>連絡先</h2>'),
        'en/support.html': ('<h2 id="operator">About us</h2>\n<div class="box">\n'
                            '  <p>minulo is made by ReliefNote, a sole proprietorship founded in July 2025 in Hokkaido, Japan.</p>\n'
                            '  <p>Founder: Ayumu Kitabayashi</p>\n'
                            '  <p>Apps: minulo (iPhone, Mac, Chrome)</p>\n'
                            '  <p>Contact: <a href="mailto:workflowai.japan@gmail.com">workflowai.japan@gmail.com</a></p>\n</div>\n\n', None),
    }
    for f, (blk, anchor) in blocks.items():
        p = ROOT / f
        if not p.exists(): print('no', f); continue
        s = p.read_text()
        if 'id="operator"' in s: print(f, 'already'); continue
        if anchor and anchor in s:
            s = s.replace(anchor, blk + anchor, 1)
        else:
            m = re.search(r'<h2[^>]*>(Contact|Kontakt)[^<]*</h2>', s)
            s = (s[:m.start()] + blk + s[m.start():]) if m else s.replace('<footer>', blk + '<footer>', 1)
        p.write_text(s); print(f, 'operator added')


def llms_full():
    """llms.txt と FAQ・比較ページの中身を1つにまとめた全文版"""
    faq = json.loads((ROOT / 'tools/faq.json').read_text())
    cmp_ = json.loads((ROOT / 'tools/compare.json').read_text())
    out = [(ROOT / 'llms.txt').read_text().rstrip(), '', '---', '']
    for lang in ('en', 'ja'):
        d = faq[lang]
        out += [f'# {d["title"]} ({lang})', '', d['lede'], '']
        for q, a in d['qa']:
            out += [f'## {q}', '', a, '']
        c = cmp_[lang]
        out += [f'# {c["title"]} ({lang})', '', c['lede'], '']
        for q, a in c['qa']:
            out += [f'## {q}', '', a, '']
        if c.get('src'): out += [c['src'], '']
    (ROOT / 'llms-full.txt').write_text('\n'.join(out) + '\n')
    print('llms-full.txt', len('\n'.join(out)), 'chars')


if __name__ == '__main__':
    for lang, cfg in LANGS.items():
        fix(lang, cfg)
    support_operator()
    llms_full()
