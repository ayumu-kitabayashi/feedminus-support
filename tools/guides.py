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

SRC_YT = [
    ('YouTube Help: Shorts feed limit', 'https://support.google.com/youtube/answer/16671528'),
    ('9to5Google (2026-04-15): YouTube Shorts can now be turned off with a zero-minute timer', 'https://9to5google.com/2026/04/15/youtube-shorts-turn-off-zero-minute-timer-setting/'),
    ('YouTube Help: Show fewer Shorts / Not interested', 'https://support.google.com/youtube/answer/6342839'),
    ('YouTube Help: Watch history and recommendations', 'https://support.google.com/youtube/answer/95725'),
    ('YouTube Blog (2026-01-14): supervised teen accounts', 'https://blog.youtube/news-and-events/updates-youtube-supervised-accounts-teens/'),
    ('Apple: Content & Privacy Restrictions on iPhone', 'https://support.apple.com/guide/iphone/iph3ff83f3b1/ios'),
]
SRC_IG = [
    ('Meta (2022-03-23): Following and Favorites feeds', 'https://about.fb.com/news/2022/03/two-new-ways-to-control-your-instagram-feed/'),
    ('Instagram Help: Set a daily time limit', 'https://help.instagram.com/2049425491975359/'),
    ('Instagram Help: Sleep mode', 'https://help.instagram.com/688407339404755/'),
    ('Meta (2024-09-17): Instagram Teen Accounts', 'https://about.fb.com/news/2024/09/instagram-teen-accounts/'),
    ('Apple: Content & Privacy Restrictions on iPhone', 'https://support.apple.com/guide/iphone/iph3ff83f3b1/ios'),
]

G = {
 'block-youtube-shorts.html': {
  'src': SRC_YT,
  'en': {
   'title': 'How to block YouTube Shorts on iPhone and keep normal videos (every method, 2026)',
   'lede': "The quickest built-in way is YouTube's Shorts feed limit: in the YouTube app, go to You → Settings → Time management → Shorts feed limit and choose 0. For adults the limit can be dismissed, and Shorts can still appear in Subscriptions and shared links. If you want a stop you can't just tap away, an app such as minulo hides Shorts in its own view and can lock the official YouTube app with Screen Time.",
   'cols': ['Method', 'What it does', 'Limits'],
   'rows': [
    ['<b>Shorts feed limit set to 0</b> (YouTube app)', 'Stops the Shorts feed from the home screen and Shorts tab once you reach the limit. 0 minutes became available to everyone from April 2026.', 'Adults can dismiss the limit. Shorts in Subscriptions and from links remain. App only, not youtube.com. Whether Shorts leave search results is unclear.'],
    ['<b>Show fewer Shorts</b> (⋮ on the Shorts shelf)', 'Hides the Shorts shelf you tapped and tells YouTube you want fewer.', 'YouTube does not say how long it lasts. Shorts can come back.'],
    ['<b>Turn off watch history</b>', 'YouTube removes homepage recommendations when you have no relevant recent history.', "YouTube's help page does not say this removes the Shorts tab."],
    ['<b>Supervised teen account</b>', 'Parents can set a Shorts scrolling timer, including zero.', 'Only for supervised teen accounts.'],
    ['<b>iPhone Screen Time</b>', 'App Limits can limit or block the whole YouTube app.', 'It cannot target Shorts only. Blocking just the /shorts address in Safari is not documented by Apple.'],
    ['<b>Apps that hide Shorts</b> (minulo, UNDOOMED, Nope, LoomWeb and others)', 'Show YouTube in their own view or in Safari with Shorts hidden; normal videos, search and subscriptions keep working.', 'The official YouTube app itself is not changed. minulo can lock the official app with Screen Time and send you to minulo instead.'],
   ],
   'qa': [
    ['Can I turn off YouTube Shorts completely?', 'Not completely inside the YouTube app for an adult account. Setting the Shorts feed limit to 0 removes the Shorts feed after the limit, but adults can dismiss it, and Shorts still appear in Subscriptions and in links people send you.'],
    ['Does the Shorts limit work on youtube.com in Safari?', "YouTube's help page describes the Shorts feed limit for the YouTube app only. On youtube.com, apps that work in Safari or in their own browser, such as Nope or minulo, can hide Shorts."],
    ['How can I stop opening the YouTube app out of habit?', 'iPhone Screen Time can block the whole YouTube app. minulo uses Screen Time the same way, but when you try to open YouTube it offers minulo instead, where Shorts are hidden and normal videos still play.'],
   ],
   'disclose': 'This page is written by the developer of minulo. Facts about YouTube and iPhone settings come from the sources listed below, checked on {date}. Menu names can change with app and iOS updates.',
   'srcTitle': 'Sources', 'more': 'Apps that hide Shorts compared', 'moreHref': 'alternatives.html', 'faq': 'Hide Shorts with minulo', 'faqHref': 'hide/youtube.html',
  },
  'ja': {
   'title': 'iPhoneでYouTubeのショートだけを止めて、ふつうの動画は見る方法（すべての方法・2026年）',
   'lede': 'いちばん手早い公式の方法は、YouTube アプリの、ショートのフィードの上限です。YouTube アプリの設定にある、ショートのフィードの上限を 0 にします（英語の画面では You → Settings → Time management → Shorts feed limit。日本語の表示名は確かめていません）。ただし大人のアカウントでは上限の表示を閉じられ、登録チャンネルや送られてきたリンクからはショートが出ます。閉じるだけでは戻れない止め方がほしいなら、minulo のようなアプリで、ショートを消した画面で見て、公式の YouTube アプリはスクリーンタイムで止める方法があります。',
   'cols': ['方法', 'できること', '限界'],
   'rows': [
    ['<b>ショートのフィードの上限を 0 に</b>（YouTube アプリ。英語の画面では Shorts feed limit）', '上限に達すると、ホームとショートのタブのショートが止まる。2026年4月から、誰でも 0 分を選べる。', '大人は上限を閉じられる。登録チャンネルやリンクのショートは残る。アプリだけで、youtube.com では使えない。検索結果から消えるかははっきりしない。'],
    ['<b>ショートの表示を減らす</b>（ショートの棚の ⋮。英語の画面では Show fewer Shorts）', '押した棚を隠し、ショートを減らしたいと YouTube に伝える。', 'どれくらい続くかは公式に書かれていない。また出てくることがある。'],
    ['<b>再生履歴をオフ</b>', '最近の履歴がないと、ホームのおすすめが表示されなくなる。', 'ショートのタブまで消えるとは、公式のヘルプに書かれていない。'],
    ['<b>保護者が見守る10代のアカウント</b>', '保護者がショートを見る時間に上限をかけられる（0 も可）。', '見守りの設定をした10代のアカウントだけ。'],
    ['<b>iPhone のスクリーンタイム</b>', 'YouTube アプリ全体の時間を制限する、または止める。', 'ショートだけは狙えない。Safari で /shorts のアドレスだけを止められるとは、Apple は説明していない。'],
    ['<b>ショートを消すアプリ</b>（minulo・UNDOOMED・Nope・LoomWeb など）', '自前の画面か Safari で YouTube を開き、ショートを表示しない。ふつうの動画・検索・登録チャンネルは使える。', '公式の YouTube アプリそのものは変わらない。minulo は公式アプリをスクリーンタイムで止め、minulo へ案内できる。'],
   ],
   'qa': [
    ['YouTubeのショートを完全にオフにできる？', '大人のアカウントでは、YouTube アプリの中だけで完全にはオフにできません。ショートのフィードの上限を 0 にすると、上限のあとはショートのフィードが止まりますが、大人は上限の表示を閉じられます。登録チャンネルや送られてきたリンクのショートも残ります。'],
    ['ショートの上限は、Safari の youtube.com でも効く？', 'YouTube のヘルプでは、ショートのフィードの上限は YouTube アプリの機能として説明されています。youtube.com でショートを消したい場合は、Safari や自前のブラウザで動く Nope や minulo のようなアプリが使えます。'],
    ['つい YouTube アプリを開いてしまうのを止めるには？', 'iPhone のスクリーンタイムで YouTube アプリ全体を止められます。minulo も同じスクリーンタイムの仕組みを使いますが、YouTube を開こうとすると minulo に案内し、そこではショートが消えたまま、ふつうの動画は見られます。'],
   ],
   'disclose': 'このページは minulo の開発者が書いています。YouTube と iPhone の設定については、下の出典を {date} に確かめました。メニューの名前は、アプリや iOS の更新で変わることがあります。',
   'srcTitle': '出典', 'more': 'ショートを消すアプリの比較', 'moreHref': 'alternatives.html', 'faq': 'minulo でショートを消す', 'faqHref': 'hide/youtube.html',
  },
 },
 'turn-off-instagram-reels.html': {
  'src': SRC_IG,
  'en': {
   'title': 'How to turn off Instagram Reels on iPhone and keep your DMs (every method, 2026)',
   'lede': "We could not find any setting in Instagram's official help pages that turns off Reels for an adult account. The closest built-in options are the Following feed, a daily time limit reminder and Sleep mode, and iPhone Screen Time can only block the whole app. To hide Reels but keep DMs, use an app that shows Instagram with Reels hidden, such as minulo, UNDOOMED, Awhile, SocialLite, LoomWeb or Nope.",
   'cols': ['Method', 'What it does', 'Limits'],
   'rows': [
    ['<b>Following feed</b> (tap the Instagram logo)', 'Shows posts from accounts you follow in time order, without suggested posts, going back 30 days.', 'The Reels tab is still there.'],
    ['<b>Daily time limit</b>', 'Reminds you after the time you set.', 'A reminder, not a block. It covers all of Instagram, not just Reels.'],
    ['<b>Sleep mode</b> (formerly Quiet mode)', 'Mutes notifications and auto-replies to DMs.', 'Does not hide Reels.'],
    ['<b>Teen Accounts</b>', 'For teens: a reminder after 60 minutes a day and sleep mode from 10 PM to 7 AM.', 'Only for teen accounts. Reels are not removed.'],
    ['<b>iPhone Screen Time</b>', 'Limits or blocks the whole Instagram app, or instagram.com in Safari.', 'It cannot block Reels only, and blocking the app also blocks DMs.'],
    ['<b>Apps that hide Reels</b> (minulo, UNDOOMED, Awhile, SocialLite, LoomWeb, Nope)', 'Show Instagram in their own view or in Safari with Reels and suggested posts hidden; DMs keep working.', 'The official Instagram app is not changed. minulo can lock the official app with Screen Time and send you to minulo instead.'],
   ],
   'qa': [
    ['Is there a setting to turn off Reels on Instagram?', "We could not find one in Instagram's official help pages as of September 2026. The Following feed removes suggested posts from your feed, but the Reels tab stays."],
    ['Can Screen Time block only Instagram Reels?', 'No. Screen Time App Limits work on the whole app, and website blocking works on whole addresses. Blocking Instagram this way also blocks your DMs.'],
    ['How do I hide Reels but keep DMs?', 'Use an app that opens Instagram with Reels hidden. minulo, UNDOOMED, Awhile, SocialLite, LoomWeb and Nope all say DMs keep working. minulo also covers 9 other networks and can lock the official Instagram app so you open minulo instead.'],
   ],
   'disclose': 'This page is written by the developer of minulo. Facts about Instagram and iPhone settings come from the sources listed below, checked on {date}. Menu names can change with app and iOS updates.',
   'srcTitle': 'Sources', 'more': 'Apps that hide Reels compared', 'moreHref': 'alternatives.html', 'faq': 'Hide Reels with minulo', 'faqHref': 'hide/instagram.html',
  },
  'ja': {
   'title': 'iPhoneでInstagramのリールをオフにして、DMは使う方法（すべての方法・2026年）',
   'lede': 'Instagram の公式のヘルプでは、大人のアカウントでリールをオフにする設定は見つかりませんでした。公式にあるのは、フォロー中のフィード、1日の利用時間のお知らせ、スリープモード（Sleep mode）で、iPhone のスクリーンタイムではアプリ全体しか止められません。リールは消して DM は使いたいなら、リールを消した状態で Instagram を開けるアプリ（minulo・UNDOOMED・Awhile・SocialLite・LoomWeb・Nope）を使います。',
   'cols': ['方法', 'できること', '限界'],
   'rows': [
    ['<b>フォロー中のフィード</b>（Instagram のロゴを押す）', 'フォローしている人の投稿を新しい順に、おすすめなしで表示する（30日前まで）。', 'リールのタブは残る。'],
    ['<b>1日の利用時間の上限</b>（英語の画面では Daily time limit）', '決めた時間を過ぎるとお知らせが出る。', 'お知らせで、止まるわけではない。リールだけでなく Instagram 全体が対象。'],
    ['<b>スリープモード</b>（英語の画面では Sleep mode。旧 Quiet mode）', '通知を止め、DM に自動で返信する。', 'リールは消えない。'],
    ['<b>10代のアカウント</b>', '10代は、1日60分でお知らせ、夜10時〜朝7時はスリープモード。', '10代のアカウントだけ。リールは消えない。'],
    ['<b>iPhone のスクリーンタイム</b>', 'Instagram アプリ全体、または Safari の instagram.com を制限・停止する。', 'リールだけは止められない。アプリを止めると DM も止まる。'],
    ['<b>リールを消すアプリ</b>（minulo・UNDOOMED・Awhile・SocialLite・LoomWeb・Nope）', '自前の画面か Safari で Instagram を開き、リールとおすすめ投稿を表示しない。DM は使える。', '公式の Instagram アプリそのものは変わらない。minulo は公式アプリをスクリーンタイムで止め、minulo へ案内できる。'],
   ],
   'qa': [
    ['Instagramにリールをオフにする設定はある？', '2026年9月の時点で、Instagram の公式のヘルプには見つかりませんでした。フォロー中のフィードにすると、フィードからおすすめ投稿は消えますが、リールのタブは残ります。'],
    ['スクリーンタイムでリールだけを止められる？', '止められません。スクリーンタイムの時間制限はアプリ全体に、サイトの制限はアドレス全体にかかります。この方法で Instagram を止めると、DM も使えなくなります。'],
    ['リールは消して、DMは使うには？', 'リールを消した状態で Instagram を開けるアプリを使います。minulo・UNDOOMED・Awhile・SocialLite・LoomWeb・Nope は、どれも DM は使えると説明しています。minulo はほかの9つのSNSにも対応し、公式の Instagram アプリを止めて minulo へ案内することもできます。'],
   ],
   'disclose': 'このページは minulo の開発者が書いています。Instagram と iPhone の設定については、下の出典を {date} に確かめました。メニューの名前は、アプリや iOS の更新で変わることがあります。',
   'srcTitle': '出典', 'more': 'リールを消すアプリの比較', 'moreHref': 'alternatives.html', 'faq': 'minulo でリールを消す', 'faqHref': 'hide/instagram.html',
  },
 },
}
LANGS = ['ja', 'en']


def page(path, lang):
    g = G[path]; t = g[lang]; d = F.DATA[lang]
    url = F.SITE + d['dir'] + path
    up = '' if d['dir'] == '' else '../'
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
        for lang in LANGS:
            out = F.ROOT / F.DATA[lang]['dir'] / path
            out.write_text(page(path, lang)); print('wrote', out)
