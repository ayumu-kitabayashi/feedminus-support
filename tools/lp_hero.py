"""トップ13言語の最初の画面に「何をするアプリか」の一文と、ボタン下の注記を入れる。題も検索語に合わせる。

10/16 のデータ（Search Console 28日・ASC 30日）から：
- 検索語は具体的（「インスタ リールだけ制限」「bloquear reels」「youtube shorts ausblenden」）なのに、
  見出しは抽象的（「無限スクロールだけをやめる」）で、何のアプリか最初の画面で分からなかった。
- 指名以外のクリックはほぼ0。題を検索語に寄せる。
何度実行しても同じ結果になる（入れ済みなら置き換えるだけ）。
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

T = {
 '.': ('minulo — インスタのリール・ショート動画だけ消すアプリ',
       'Instagram のリール、YouTube のショート、TikTok のおすすめだけを消す iPhone アプリ。DM・フォロー中の投稿・検索はそのまま使えます。',
       '消す機能は無料 · iPhone 用 · 10のSNSに対応'),
 'en': ('minulo — Hide Instagram Reels & YouTube Shorts on iPhone',
        'An iPhone app that hides Instagram Reels, YouTube Shorts and TikTok’s For You feed. DMs, posts from people you follow and search keep working.',
        'Free to hide · iPhone · 10 social apps'),
 'de': ('minulo – Instagram Reels & YouTube Shorts ausblenden',
        'Eine iPhone-App, die Instagram Reels, YouTube Shorts und TikToks „Für dich“ ausblendet. DMs, Beiträge von Leuten, denen du folgst, und die Suche funktionieren weiter.',
        'Ausblenden kostenlos · iPhone · 10 soziale Netzwerke'),
 'fr': ('minulo — Masquer les Reels Instagram et les Shorts YouTube',
        'Une app iPhone qui masque les Reels d’Instagram, les Shorts de YouTube et le « Pour toi » de TikTok. Les messages, les publications des comptes suivis et la recherche restent accessibles.',
        'Masquage gratuit · iPhone · 10 réseaux'),
 'es': ('minulo — Oculta los Reels de Instagram y los Shorts de YouTube',
        'Una app para iPhone que oculta los Reels de Instagram, los Shorts de YouTube y el «Para ti» de TikTok. Los mensajes, las publicaciones de las cuentas que sigues y la búsqueda siguen funcionando.',
        'Ocultar es gratis · iPhone · 10 redes'),
 'pt': ('minulo — Esconda os Reels do Instagram e os Shorts do YouTube',
        'Um app para iPhone que esconde os Reels do Instagram, os Shorts do YouTube e o «Para você» do TikTok. As mensagens, as publicações de quem você segue e a busca continuam funcionando.',
        'Esconder é grátis · iPhone · 10 redes'),
 'it': ('minulo — Nascondi i Reels di Instagram e gli Shorts di YouTube',
        'Un’app per iPhone che nasconde i Reels di Instagram, gli Shorts di YouTube e il «Per te» di TikTok. I messaggi, i post degli account seguiti e la ricerca continuano a funzionare.',
        'Nascondere è gratis · iPhone · 10 social'),
 'ko': ('minulo — 인스타 릴스·유튜브 쇼츠만 숨기는 앱',
        '인스타그램 릴스와 유튜브 쇼츠만 숨기는 iPhone 앱이에요. DM, 팔로우한 사람의 게시물, 검색은 그대로 쓸 수 있어요.',
        '숨기기는 무료 · iPhone · SNS 10개 지원'),
 'zh-Hant': ('minulo — 只隱藏 IG 的 Reels 和 YouTube Shorts',
        '隱藏 Instagram 的 Reels、YouTube 的 Shorts 和 TikTok「推薦」的 iPhone App。私訊、追蹤對象的貼文和搜尋都能照常使用。',
        '隱藏功能免費 · iPhone · 支援 10 個社群'),
 'id': ('minulo — Sembunyikan Reels Instagram & Shorts YouTube',
        'Aplikasi iPhone yang menyembunyikan Reels Instagram, Shorts YouTube, dan For You TikTok. DM, postingan dari akun yang diikuti, dan pencarian tetap bisa dipakai.',
        'Gratis untuk menyembunyikan · iPhone · 10 medsos'),
 'th': ('minulo — ซ่อน Reels ของ IG และ Shorts ของ YouTube',
        'แอป iPhone ที่ซ่อน Reels ของ Instagram, Shorts ของ YouTube และ For You ของ TikTok ส่วน DM โพสต์ของคนที่ติดตาม และการค้นหายังใช้ได้ตามปกติ',
        'ซ่อนได้ฟรี · iPhone · รองรับ 10 โซเชียล'),
 'vi': ('minulo — Ẩn Reels Instagram và Shorts YouTube',
        'Ứng dụng iPhone ẩn Reels của Instagram, Shorts của YouTube và mục Dành cho bạn của TikTok. Tin nhắn, bài đăng của người bạn theo dõi và tìm kiếm vẫn dùng bình thường.',
        'Ẩn miễn phí · iPhone · 10 mạng xã hội'),
 'ru': ('minulo — Скрыть Reels в Instagram и Shorts в YouTube',
        'Приложение для iPhone, которое скрывает Reels в Instagram, Shorts в YouTube и «Рекомендации» в TikTok. Сообщения, посты тех, на кого вы подписаны, и поиск работают как обычно.',
        'Скрытие бесплатно · iPhone · 10 соцсетей'),
}

LEAD = '<p class="lead herolead" style="margin-top:14px">{}</p>'
NOTE = '<p class="heronote" style="margin-top:12px;font-size:13.5px;line-height:1.6;color:var(--ink2);font-weight:600">{}</p>'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


for lang, (title, lead, note) in T.items():
    p = ROOT / lang / 'index.html'
    s = p.read_text(encoding='utf-8')
    old = re.search(r'<title>(.*?)</title>', s).group(1)
    # 題・og/twitter・JSON-LD の WebPage 名は同じ文なので、まとめて置き換える
    if old != esc(title):
        s = s.replace(old, esc(title))
        s = s.replace(old.replace('&amp;', '&'), title)
    head, rest = s.split('id="top"', 1)
    hero, tail = rest.split('</header>', 1)
    hero = re.sub(r'\s*<p class="lead herolead".*?</p>', '', hero, flags=re.S)
    hero = re.sub(r'\s*<p class="(?:note )?heronote".*?</p>', '', hero, flags=re.S)
    hero = hero.replace('</h1>', '</h1>\n    ' + LEAD.format(esc(lead)), 1)
    m = re.search(r'<div class="cta">.*?</div>', hero, flags=re.S)
    hero = hero[:m.end()] + '\n    ' + NOTE.format(esc(note)) + hero[m.end():]
    p.write_text(head + 'id="top"' + hero + '</header>' + tail, encoding='utf-8')
    print(lang, 'ok', len(title))
