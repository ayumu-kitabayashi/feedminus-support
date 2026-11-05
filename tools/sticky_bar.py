#!/usr/bin/env python3
"""Mobile sticky App Store bar on article pages (2026-11-05).

Inserts one small inline CSS+JS block before </body> on every article page that
already has an App Store button for minulo (id6809352229). Idempotent: the block
sits between START/END markers and is replaced on re-run. Re-run this after
regenerating pages with the other tools/*.py generators.

The bar (phones only, max-width 760px):
- appears after the first App Store button has scrolled off the top,
- hides while any App Store button on the page is on screen,
- links to the first button's App Store URL with ct "<ct>-sticky" and
  data-pos="sticky" (t.js keeps the -sticky suffix and sends pos=sticky),
- can be closed; closing is remembered for the day in localStorage.

Usage: python3 tools/sticky_bar.py   (prints the changed files, one per line)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIRS = ["en", "ko", "fr", "de", "es", "pt", "it", "ru", "th", "vi", "id", "zh-Hant"]
SKIP = {"index.html", "privacy.html", "terms.html", "press.html", "support.html"}
APP = "id6809352229"
START = "<!-- minulo-sticky:start -->"
END = "<!-- minulo-sticky:end -->"

CSS = (
    "#msb{position:fixed;left:0;right:0;bottom:0;z-index:50;display:none;visibility:hidden;"
    "padding:8px 12px calc(8px + env(safe-area-inset-bottom));background:#fbfbfa;"
    "border-top:1px solid #e4e4e0;"
    "transform:translateY(100%);transition:transform .2s,visibility .2s}"
    "#msb.on{transform:none;visibility:visible}"
    "#msb>div{display:flex;gap:6px;align-items:center;max-width:720px;margin:0 auto}"
    "#msb a{flex:1;display:block;padding:12px;border-radius:12px;background:#141518;color:#fff;"
    "font:700 16px/1.3 -apple-system,system-ui,sans-serif;text-align:center;text-decoration:none}"
    "#msb button{flex:none;width:40px;height:44px;border:0;background:none;color:#7a7d86;font-size:24px;line-height:1;padding:0}"
    "@media(max-width:760px){#msb{display:block}}"
    "@media(prefers-color-scheme:dark){#msb{background:#121315;border-color:#26282c}"
    "#msb a{background:#ececee;color:#121315}}"
    "@media(prefers-reduced-motion:reduce){#msb{transition:none}}"
)

# Button text per <html lang> (first subtag; zh-Hant -> zh).
TEXT = {
    "ja": "minulo を無料で入れる",
    "en": "Get minulo free",
    "ko": "minulo 무료로 받기",
    "fr": "Télécharger minulo gratuitement",
    "de": "minulo kostenlos laden",
    "es": "Descargar minulo gratis",
    "pt": "Baixar o minulo grátis",
    "it": "Scarica minulo gratis",
    "ru": "Скачать minulo бесплатно",
    "th": "ดาวน์โหลด minulo ฟรี",
    "vi": "Tải minulo miễn phí",
    "id": "Unduh minulo gratis",
    "zh": "免費下載 minulo",
}
CLOSE = {"ja": "閉じる"}


def js(lang):
    key = lang.split("-")[0]
    text = TEXT.get(key, TEXT["en"])
    close = CLOSE.get(key, "Close")
    return (
        "(function(){var d=document,W=window,A=d.querySelectorAll('a[href*=\"" + APP + "\"]');"
        "if(!A.length||!W.IntersectionObserver)return;"
        "var K='m_sticky_x',D=new Date().toDateString();"
        "try{if(localStorage.getItem(K)==D)return}catch(e){}"
        "var u;try{u=new URL(A[0].href)}catch(e){return}"
        "u.searchParams.set('ct',(u.searchParams.get('ct')||'page')+'-sticky');"
        "var b=d.createElement('div');b.id='msb';"
        "b.innerHTML='<div><a data-pos=\"sticky\"></a><button type=\"button\">\\u00d7</button></div>';"
        "var a=b.firstChild.firstChild,x=a.nextSibling;a.href=u.href;"
        "a.textContent=" + repr_js(text) + ";x.setAttribute('aria-label'," + repr_js(close) + ");"
        "d.body.appendChild(b);"
        "function f(){var v=0;for(var i=0;i<A.length;i++)if(A[i]._v)v=1;"
        "b.className=(!v&&A[0].getBoundingClientRect().bottom<0)?'on':''}"
        "var o=new W.IntersectionObserver(function(es){es.forEach(function(e){e.target._v=e.isIntersecting});f()});"
        "for(var i=0;i<A.length;i++)o.observe(A[i]);"
        "x.onclick=function(){try{localStorage.setItem(K,D)}catch(e){}o.disconnect();b.remove()}"
        "})();"
    )


def repr_js(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def snippet(lang):
    return START + "<style>" + CSS + "</style><script>" + js(lang) + "</script>" + END + "\n"


def pages():
    out = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html") and name not in SKIP:
            out.append(name)
    for d in LANG_DIRS:
        p = os.path.join(ROOT, d)
        for name in sorted(os.listdir(p)):
            if name.endswith(".html") and name not in SKIP:
                out.append(d + "/" + name)
    return out


BLOCK = re.compile(re.escape(START) + ".*?" + re.escape(END) + "\n?", re.S)
LANG = re.compile(r'<html[^>]*\blang="([^"]+)"')


def main():
    changed = []
    for rel in pages():
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if APP not in html or "apps.apple.com" not in html or html.count("</body>") != 1:
            continue
        m = LANG.search(html)
        lang = m.group(1) if m else ("ja" if "/" not in rel else rel.split("/")[0])
        new = BLOCK.sub("", html)
        new = new.replace("</body>", snippet(lang) + "</body>")
        if new != html:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
            changed.append(rel)
    for rel in changed:
        print(rel)
    print(f"{len(changed)} changed", file=sys.stderr)


if __name__ == "__main__":
    main()
