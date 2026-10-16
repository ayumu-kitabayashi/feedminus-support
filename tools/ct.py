"""サイト内の minulo の App Store リンクにキャンペーン印（pt・ct）を付ける。

ASC の「キャンペーン」で、どのページ・どのボタンからダウンロードされたかが見える（Apple 側の集計だけ。
Cookie も個人の追跡も無いので privacy.html は変わらない）。
ct は「言語-ページ-場所」（40字まで）。例 ja-top-hero, en-faq-1, fr-hide-instagram-2。
トップは場所に名前（nav・hero・price・end・dock）、ほかのページは出てきた順の番号。
ほかの生成スクリプト（faq.py・guides.py・hide.py・alts.py など）を回したあとに、これも回す。
何度回しても同じ（付け済みの印は付け直す）。JSON-LD の installUrl とほかのアプリへのリンクは触らない。
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PT = '129109285'
LANGS = {'en', 'de', 'fr', 'es', 'pt', 'it', 'ko', 'zh-Hant', 'id', 'th', 'vi', 'ru'}
LINK = re.compile(r'href="(https://apps\.apple\.com/(?:[a-z]{2}/)?app/(?:[^"/]+/)?id6809352229)(?:\?[^"]*)?"')
TOP_POS = ['nav', 'hero', 'price', 'end', 'dock']


def token(rel):
    parts = list(rel.parts)
    lang = 'ja'
    if parts[0] in LANGS:
        lang = {'zh-Hant': 'zh'}.get(parts[0], parts[0])
        parts = parts[1:]
    page = '-'.join(parts)[:-5] or 'top'
    page = 'top' if page == 'index' else page.replace('-index', '').replace('/index', '')
    return lang, page


def main():
    n_files = n_links = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts[0].startswith('.') or rel.parts[0] in ('node_modules',):
            continue
        s = p.read_text(encoding='utf-8')
        if 'id6809352229' not in s:
            continue
        lang, page = token(rel)
        i = 0

        def sub(m):
            nonlocal i
            pos = TOP_POS[i] if page == 'top' and i < len(TOP_POS) else str(i + 1)
            i += 1
            ct = f'{lang}-{page}'[:40 - len(pos) - 1] + '-' + pos
            return f'href="{m.group(1)}?pt={PT}&amp;ct={ct}&amp;mt=8"'

        t = LINK.sub(sub, s)
        if t != s:
            p.write_text(t, encoding='utf-8')
            n_files += 1
        n_links += i
    print(f'{n_files} files changed, {n_links} links')


if __name__ == '__main__':
    main()
