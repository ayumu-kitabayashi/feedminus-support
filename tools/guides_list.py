#!/usr/bin/env python3
"""言語ごとの「すべてのガイド」一覧ページ（<lang>/guides.html・日本語はルート）を書き出す（2026-10-27）。

★なぜ：トップから新しい問いのページへのリンクがなく、Bing で主なページが「発見されたがクロールされていない」まま。
  言語ごとに全記事を1ページに並べ、トップと各記事のフッターからここへつなぐ。
★分け方は slug の言葉で決める（全言語で同じ並びになる）。迷うものは OVERRIDE で「その他」へ。
使い方:  python3 tools/guides_list.py          → 13言語の guides.html を書き出す（記事を足したら回し直す）
        python3 tools/guides_list.py --wire   → さらに各記事のフッター・各トップに guides.html へのリンクを足す（何度回しても同じ）
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://minulo.app/'
LANGS = ['ja', 'en', 'ko', 'de', 'fr', 'es', 'pt', 'it', 'zh-Hant', 'id', 'th', 'vi', 'ru']
HREFLANG = {'pt': 'pt-BR'}
NAMES = {'ja': '日本語', 'en': 'English', 'ko': '한국어', 'de': 'Deutsch', 'fr': 'Français', 'es': 'Español',
         'pt': 'Português', 'it': 'Italiano', 'zh-Hant': '繁體中文', 'id': 'Bahasa Indonesia', 'th': 'ไทย',
         'vi': 'Tiếng Việt', 'ru': 'Русский'}
SKIP = {'index.html', 'privacy.html', 'support.html', 'press.html', 'android.html', 'guides.html'}
CATS = ['yt', 'ig', 'tt', 'night', 'cmp', 'svc', 'other']

T = {
 'ja': dict(label='すべてのガイド',
   title='minulo のガイド一覧：リール・ショート・TikTok のおすすめを消す方法と比べ方',
   desc='iPhone でインスタのリール、YouTube のショート、TikTok のおすすめを消す方法と、アプリの比べ方のガイドをテーマ別にまとめた一覧です。',
   intro='minulo は、iPhone でインスタのリール、YouTube のショート、TikTok のおすすめだけを無料で消して、DM やふつうの動画は残せるアプリです。このページは、そのやり方とアプリの比べ方をまとめたガイドの一覧です。',
   cats=['YouTube ショート', 'Instagram（リール・DM）', 'TikTok', '夜・スクリーンタイム', 'アプリの比較・代わり（SocialLite など）', 'サービス別', 'その他']),
 'en': dict(label='All guides',
   title='All minulo guides: hiding Reels, Shorts and TikTok For You, and comparing apps',
   desc='Every minulo guide by topic: how to hide Instagram Reels, YouTube Shorts and TikTok For You on iPhone, and how the apps that do it compare.',
   intro='minulo is a free iPhone app that hides just Reels, Shorts and TikTok For You, while you keep your DMs and regular videos. This page lists every guide on how to do it and how the apps compare.',
   cats=['YouTube Shorts', 'Instagram (Reels and DMs)', 'TikTok', 'Night and Screen Time', 'App comparisons and alternatives (SocialLite and others)', 'By network', 'Other']),
 'ko': dict(label='모든 가이드',
   title='minulo 가이드 모음: 릴스·쇼츠·틱톡 추천 숨기는 방법과 앱 비교',
   desc='아이폰에서 인스타 릴스, 유튜브 쇼츠, 틱톡 추천을 숨기는 방법과 앱 비교 가이드를 주제별로 모았습니다.',
   intro='minulo는 아이폰에서 인스타 릴스, 유튜브 쇼츠, 틱톡 추천만 무료로 숨기고 DM과 일반 영상은 그대로 쓸 수 있는 앱입니다. 이 페이지에는 그 방법과 앱 비교를 다룬 가이드를 모두 모았습니다.',
   cats=['유튜브 쇼츠', '인스타그램 (릴스·DM)', '틱톡', '밤·스크린 타임', '앱 비교·대안 (SocialLite 등)', '서비스별', '기타']),
 'de': dict(label='Alle Anleitungen',
   title='Alle Anleitungen von minulo: Reels, Shorts und TikTok ausblenden, Apps vergleichen',
   desc='Alle Anleitungen von minulo nach Thema: Instagram Reels, YouTube Shorts und TikTok „Für dich“ auf dem iPhone ausblenden und die Apps dafür vergleichen.',
   intro='minulo ist eine kostenlose iPhone-App, die nur Reels, Shorts und die TikTok-Empfehlungen ausblendet. DMs und normale Videos bleiben. Hier findest du alle Anleitungen dazu und alle App-Vergleiche.',
   cats=['YouTube Shorts', 'Instagram (Reels und DMs)', 'TikTok', 'Abends und Bildschirmzeit', 'App-Vergleiche und Alternativen (SocialLite u. a.)', 'Nach Netzwerk', 'Sonstiges']),
 'fr': dict(label='Tous les guides',
   title='Tous les guides minulo : masquer Reels, Shorts et TikTok, comparer les apps',
   desc='Tous les guides minulo par thème : masquer les Reels Instagram, les Shorts YouTube et le fil Pour toi de TikTok sur iPhone, et comparer les apps.',
   intro='minulo est une app iPhone gratuite qui masque seulement les Reels, les Shorts et les recommandations TikTok, et vous laisse vos messages privés et les vidéos normales. Cette page rassemble tous les guides pour le faire et pour comparer les apps.',
   cats=['YouTube Shorts', 'Instagram (Reels et messages)', 'TikTok', 'Le soir et Temps d’écran', 'Comparatifs et alternatives (SocialLite, etc.)', 'Par réseau', 'Autres']),
 'es': dict(label='Todas las guías',
   title='Todas las guías de minulo: ocultar Reels, Shorts y TikTok, y comparar apps',
   desc='Todas las guías de minulo por tema: cómo ocultar los Reels de Instagram, los Shorts de YouTube y el Para ti de TikTok en el iPhone, y cómo se comparan las apps.',
   intro='minulo es una app gratis para iPhone que oculta solo los Reels, los Shorts y las recomendaciones de TikTok, y te deja seguir usando los mensajes directos y los videos normales. Aquí están todas las guías para hacerlo y para comparar apps.',
   cats=['YouTube Shorts', 'Instagram (Reels y mensajes)', 'TikTok', 'Por la noche y Tiempo de uso', 'Comparativas y alternativas (SocialLite y otras)', 'Por red social', 'Otros']),
 'pt': dict(label='Todos os guias',
   title='Todos os guias do minulo: esconder Reels, Shorts e TikTok e comparar apps',
   desc='Todos os guias do minulo por tema: como esconder os Reels do Instagram, os Shorts do YouTube e o Para Você do TikTok no iPhone, e como os apps se comparam.',
   intro='O minulo é um app gratuito para iPhone que esconde só os Reels, os Shorts e as recomendações do TikTok, e mantém as DMs e os vídeos normais. Esta página reúne todos os guias de como fazer isso e de como comparar os apps.',
   cats=['YouTube Shorts', 'Instagram (Reels e DMs)', 'TikTok', 'À noite e Tempo de Uso', 'Comparações e alternativas (SocialLite e outros)', 'Por rede social', 'Outros']),
 'it': dict(label='Tutte le guide',
   title='Tutte le guide di minulo: nascondere Reels, Shorts e TikTok e confrontare le app',
   desc='Tutte le guide di minulo per tema: come nascondere i Reels di Instagram, gli Shorts di YouTube e i Per te di TikTok su iPhone, e come si confrontano le app.',
   intro='minulo è un’app gratuita per iPhone che nasconde solo Reels, Shorts e i consigli di TikTok, e ti lascia i DM e i video normali. In questa pagina trovi tutte le guide su come farlo e su come confrontare le app.',
   cats=['YouTube Shorts', 'Instagram (Reels e DM)', 'TikTok', 'La sera e Tempo di utilizzo', 'Confronti e alternative (SocialLite e altre)', 'Per social', 'Altro']),
 'zh-Hant': dict(label='所有指南',
   title='minulo 指南總覽：隱藏 Reels、Shorts 與 TikTok 推薦的方法和 App 比較',
   desc='依主題整理的 minulo 指南：在 iPhone 上隱藏 Instagram Reels、YouTube Shorts 與 TikTok 推薦的方法，以及各 App 的比較。',
   intro='minulo 是一款免費的 iPhone App，只隱藏 Reels、Shorts 和 TikTok 的推薦，私訊和一般影片照常使用。這一頁整理了所有做法與 App 比較的指南。',
   cats=['YouTube Shorts', 'Instagram（Reels・私訊）', 'TikTok', '夜間・螢幕使用時間', 'App 比較與替代方案（SocialLite 等）', '依服務', '其他']),
 'id': dict(label='Semua panduan',
   title='Semua panduan minulo: menyembunyikan Reels, Shorts, dan TikTok, serta membandingkan aplikasi',
   desc='Semua panduan minulo per topik: cara menyembunyikan Reels Instagram, Shorts YouTube, dan FYP TikTok di iPhone, serta perbandingan aplikasinya.',
   intro='minulo adalah aplikasi iPhone gratis yang hanya menyembunyikan Reels, Shorts, dan rekomendasi TikTok, sementara DM dan video biasa tetap bisa dipakai. Halaman ini berisi semua panduan cara melakukannya dan cara membandingkan aplikasinya.',
   cats=['YouTube Shorts', 'Instagram (Reels dan DM)', 'TikTok', 'Malam hari dan Durasi Layar', 'Perbandingan dan alternatif aplikasi (SocialLite dll.)', 'Per layanan', 'Lainnya']),
 'th': dict(label='คู่มือทั้งหมด',
   title='คู่มือทั้งหมดของ minulo: วิธีซ่อน Reels, Shorts และ TikTok และการเปรียบเทียบแอป',
   desc='รวมคู่มือของ minulo ตามหัวข้อ: วิธีซ่อน Reels ของ Instagram, Shorts ของ YouTube และหน้าสำหรับคุณของ TikTok บน iPhone และการเปรียบเทียบแอป',
   intro='minulo เป็นแอป iPhone ฟรีที่ซ่อนเฉพาะ Reels, Shorts และคลิปแนะนำของ TikTok โดยยังใช้ DM และดูวิดีโอปกติได้ตามเดิม หน้านี้รวบรวมคู่มือวิธีทำและการเปรียบเทียบแอปไว้ทั้งหมด',
   cats=['YouTube Shorts', 'Instagram (Reels และ DM)', 'TikTok', 'ตอนกลางคืนและเวลาหน้าจอ', 'เปรียบเทียบแอปและทางเลือกอื่น (SocialLite ฯลฯ)', 'แยกตามบริการ', 'อื่น ๆ']),
 'vi': dict(label='Tất cả hướng dẫn',
   title='Tất cả hướng dẫn của minulo: ẩn Reels, Shorts, TikTok và so sánh ứng dụng',
   desc='Tất cả hướng dẫn của minulo theo chủ đề: cách ẩn Reels Instagram, Shorts YouTube và mục Dành cho bạn của TikTok trên iPhone, cùng so sánh các ứng dụng.',
   intro='minulo là ứng dụng iPhone miễn phí chỉ ẩn Reels, Shorts và video đề xuất của TikTok, còn tin nhắn và video thường vẫn dùng như bình thường. Trang này tổng hợp mọi hướng dẫn về cách làm và cách so sánh các ứng dụng.',
   cats=['YouTube Shorts', 'Instagram (Reels và tin nhắn)', 'TikTok', 'Ban đêm và Thời gian sử dụng', 'So sánh và ứng dụng thay thế (SocialLite và các app khác)', 'Theo mạng xã hội', 'Khác']),
 'ru': dict(label='Все руководства',
   title='Все руководства minulo: как скрыть Reels, Shorts и TikTok и сравнить приложения',
   desc='Все руководства minulo по темам: как скрыть Reels в Instagram, Shorts в YouTube и рекомендации TikTok на iPhone и как сравнить приложения.',
   intro='Бесплатное приложение minulo для iPhone скрывает только Reels, Shorts и рекомендации TikTok, а личные сообщения и обычные видео остаются. На этой странице собраны все руководства о том, как это сделать и как сравнить приложения.',
   cats=['YouTube Shorts', 'Instagram (Reels и сообщения)', 'TikTok', 'Ночью и Экранное время', 'Сравнения и альтернативы (SocialLite и другие)', 'По сервисам', 'Другое']),
}

# 迷うもの（リールとショートの両方・一般論）は「その他」
OVERRIDE = {'why-reels-are-addictive': 'other', 'reels-time-calculator': 'other', 'reels-shorts-data-2026': 'other',
            'short-videos-attention-span': 'other', 'study-focus': 'other'}


def cat_of(slug):
    if slug in OVERRIDE:
        return OVERRIDE[slug]
    if any(k in slug for k in ('alternative', '-vs-', 'sociallite', 'compare', 'reels-blocker', 'smartphone-limit-apps', 'safari-extensions')):
        return 'cmp'
    if any(k in slug for k in ('night', 'downtime', 'screen-time', 'focus-mode', 'grayscale', 'app-limit', 'phone-addiction')):
        return 'night'
    if 'tiktok' in slug:
        return 'tt'
    if 'youtube' in slug or 'shorts' in slug:
        return 'yt'
    if 'instagram' in slug or ('reels' in slug and 'facebook' not in slug):
        return 'ig'
    return 'other'


def ldir(l):
    return ROOT if l == 'ja' else ROOT / l


def url(l, rel=''):
    return BASE + ('' if l == 'ja' else l + '/') + rel


def meta(p):
    t = p.read_text()
    title = html.unescape(re.search(r'<title>(.*?)</title>', t, re.S).group(1)).strip()
    title = re.sub(r'\s*[|｜]\s*minulo\s*$', '', title)
    d = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = html.unescape(d.group(1)).strip() if d else ''
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t).group(1)
    return title, desc, canon


def pages(l):
    d = ldir(l)
    out = []
    for p in sorted(d.glob('*.html')):
        if p.name in SKIP or p.name.startswith('naver'):
            continue
        out.append((cat_of(p.stem), p.name, p))
    for p in sorted((d / 'hide').glob('*.html')):
        out.append(('svc', 'hide/' + p.name, p))
    out.sort(key=lambda x: (0 if x[1] == 'hide/index.html' else 1))   # hide の目次を先頭に
    return out


def template(l):
    t = (ldir(l) / 'minulo-limitations.html').read_text()
    g = lambda pat: (re.search(pat, t) or re.search(pat, (ROOT / 'en/minulo-limitations.html').read_text())).group(0)
    return dict(icon=g(r'<link rel="icon"[^>]*>'), apple=g(r'<link rel="apple-touch-icon"[^>]*>'),
                header=g(r'<header>.*?</header>'), cta=g(r'<div class="cta">.*?</div>'))


def og_image(l):
    if l in ('vi', 'ru', 'en'):   # og/en.png は無い（英語の記事は og.png）
        return BASE + 'og.png'
    return BASE + 'og/' + l + '.png'


STYLE = ('<style>.glist{list-style:none;padding:0!important;margin:0 0 8px}.glist li{margin:0 0 14px!important;padding:0!important}'
         '.glist a{font-weight:600;color:var(--pri);text-decoration:none}.glist a:hover{text-decoration:underline}'
         '.glist p{margin:3px 0 0;font-size:14px;line-height:1.6;color:var(--ink3)}</style>')


def build(l):
    tr = T[l]
    tp = template(l)
    pre = '' if l == 'ja' else '../'
    me = url(l, 'guides.html')
    e = lambda s: html.escape(s, quote=True)
    groups = {c: [] for c in CATS}
    for c, rel, p in pages(l):
        title, desc, canon = meta(p)
        groups[c].append((rel, title, desc, canon))
    for c in CATS:
        if c != 'svc':
            groups[c].sort(key=lambda x: x[0])
    head = ['<!doctype html>', f'<html lang="{HREFLANG.get(l, l)}">', '<head>', '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{e(tr["title"])} | minulo</title>',
            f'<meta name="description" content="{e(tr["desc"])}">',
            f'<link rel="canonical" href="{me}">']
    for x in LANGS:
        head.append(f'<link rel="alternate" hreflang="{HREFLANG.get(x, x)}" href="{url(x, "guides.html")}">')
    head.append(f'<link rel="alternate" hreflang="x-default" href="{url("en", "guides.html")}">')
    head += [tp['icon'], tp['apple'], '<meta property="og:type" content="website">',
             f'<meta property="og:title" content="{e(tr["title"])}">',
             f'<meta property="og:description" content="{e(tr["desc"])}">',
             f'<meta property="og:url" content="{me}">', f'<meta property="og:image" content="{og_image(l)}">',
             '<meta name="twitter:card" content="summary_large_image">',
             f'<meta name="twitter:title" content="{e(tr["title"])}">',
             f'<meta name="twitter:description" content="{e(tr["desc"])}">']
    items, n = [], 0
    for c in CATS:
        for rel, title, desc, canon in groups[c]:
            n += 1
            items.append({'@type': 'ListItem', 'position': n, 'url': canon, 'name': title})
    cp = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': tr['title'], 'description': tr['desc'],
          'url': me, 'inLanguage': HREFLANG.get(l, l), 'datePublished': '2026-10-27', 'dateModified': '2026-10-27',
          'isPartOf': {'@type': 'WebSite', 'name': 'minulo', 'url': BASE},
          'publisher': {'@type': 'Organization', 'name': 'minulo'},
          'hasPart': [{'@type': 'WebPage', 'url': i['url'], 'name': i['name']} for i in items],
          'mainEntity': {'@type': 'ItemList', 'numberOfItems': n, 'itemListElement': items}}
    bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'minulo', 'item': url(l)},
        {'@type': 'ListItem', 'position': 2, 'name': tr['label'], 'item': me}]}
    j = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    head += [f'<script type="application/ld+json">{j(cp)}</script>', f'<script type="application/ld+json">{j(bc)}</script>',
             '<link rel="stylesheet" href="/article.css">', STYLE, '</head>']
    body = ['<body>', '<div class="wrap">', tp['header'], '<main>', f'<h1>{e(tr["title"])}</h1>',
            f'<p class="lede">{e(tr["intro"])}</p>', '<p class="upd"><time datetime="2026-10-27">2026-10-27</time></p>']
    for i, c in enumerate(CATS):
        if not groups[c]:
            continue
        lis = ''.join(f'<li><a href="{e(rel)}">{e(title)}</a>' + (f'<p>{e(desc)}</p>' if desc else '') + '</li>'
                      for rel, title, desc, canon in groups[c])
        body.append(f'<section class="qa" id="{c}"><h2>{e(tr["cats"][i])}</h2><ul class="glist">{lis}</ul></section>')
    cta = re.sub(r'ct=[^&"]+', f'ct={l}-guides', tp['cta'])
    body.append(cta)
    body.append('</main>')
    langs = []
    for x in LANGS:
        if x == l:
            langs.append(f'<b>{NAMES[x]}</b>')
        else:
            href = pre + ('' if x == 'ja' else x + '/') + 'guides.html'
            hl = HREFLANG.get(x, x)
            langs.append(f'<a href="{href}" hreflang="{hl}" lang="{hl}">{NAMES[x]}</a>')
    body.append(f'<footer><div class="langs">{"".join(langs)}</div><p>© 2026 minulo</p></footer>')
    body += ['</div>', '<script src="/t.js" defer></script>', '</body>', '</html>', '']
    (ldir(l) / 'guides.html').write_text('\n'.join(head + body))
    return n, {c: len(groups[c]) for c in CATS}


FOOT = '<p>© 2026 minulo</p></footer>'


def wire():
    changed = []
    for l in LANGS:
        lab = html.escape(T[l]['label'])
        for c, rel, p in pages(l):
            t = p.read_text()
            if 'class="allg"' in t:
                continue
            assert t.count(FOOT) == 1, p
            href = ('../' if rel.startswith('hide/') else '') + 'guides.html'
            t = t.replace(FOOT, f'<p class="allg"><a href="{href}">{lab}</a></p>{FOOT}')
            p.write_text(t); changed.append(p)
        ip = ldir(l) / 'index.html'
        t = ip.read_text()
        if 'href="./guides.html"' not in t:
            m = re.search(r'(<nav class="guides"[^>]*><p class="gl">[^<]*</p><div class="gs">)', t)
            assert m and t.count(m.group(1)) == 1, ip
            t = t.replace(m.group(1), m.group(1) + f'<a href="./guides.html">{lab} →</a>')
            ip.write_text(t); changed.append(ip)
    return changed


if __name__ == '__main__':
    for l in LANGS:
        n, by = build(l)
        print(l, n, by)
    if '--wire' in sys.argv:
        print('wired', len(wire()))
