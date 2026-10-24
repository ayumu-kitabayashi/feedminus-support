"""スラッグを渡すと、実在する言語ファイルから hreflang・フッターの言語リンク・sitemap の alternate を組み直す。
使い方: python3 tools/sync_langs.py why-reels-are-addictive.html study-focus.html
ja はルート。別スラッグの ja は JA に足す。sitemap は該当スラッグの <url> を消して末尾に入れ直す。"""
import os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=[('ja','', '日本語'),('en','en','English'),('ko','ko','한국어'),('de','de','Deutsch'),('fr','fr','Français'),('es','es','Español'),('pt-BR','pt','Português'),('it','it','Italiano'),('zh-Hant','zh-Hant','繁體中文'),('id','id','Bahasa Indonesia'),('th','th','ไทย'),('vi','vi','Tiếng Việt'),('ru','ru','Русский')]
JA={'turn-off-youtube-autoplay-recommendations.html':'youtube-autoplay-recommendations-off.html'}
def js(d,s): return JA.get(s,s) if not d else s
def path(d,s): s=js(d,s); return os.path.join(ROOT,d,s) if d else os.path.join(ROOT,s)
def url(d,s): s=js(d,s); return f'https://minulo.app/{d+"/" if d else ""}{s}'
slugs=sys.argv[1:]
sm=open(f'{ROOT}/sitemap.xml').read()
for s in slugs:
    have=[(h,d,n) for h,d,n in L if os.path.exists(path(d,s))]
    xdef = url('en',s) if any(d=='en' for _,d,_ in have) else url(have[0][1],s)
    block='\n'.join(f'<link rel="alternate" hreflang="{h}" href="{url(d,s)}">' for h,d,_ in have)+f'\n<link rel="alternate" hreflang="x-default" href="{xdef}">'
    for h0,d0,n0 in have:
        p=path(d0,s); t=open(p).read()
        t=re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?','',t)
        t=re.sub(r'(<link rel="canonical"[^>]*>\n)',lambda m:m.group(1)+block+'\n',t,count=1)
        parts=[]
        for h,d,n in have:
            if d==d0: parts.append(f'<b>{n}</b>')
            else:
                rel=(('../' if d0 else '')+(d+'/' if d else '')+js(d,s))
                parts.append(f'<a href="{rel}" hreflang="{h}" lang="{h}">{n}</a>')
        t=re.sub(r'<div class="langs">.*?</div>','<div class="langs">'+''.join(parts)+'</div>',t)
        open(p,'w').write(t)
    # sitemap
    locs=[url(d,s) for _,d,_ in have]
    for lc in locs:
        sm=re.sub(r'  <url><loc>'+re.escape(lc)+r'</loc>.*?</url>\n','',sm,flags=re.S)
    alts=''.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{url(d,s)}"/>\n' for h,d,_ in have)+f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xdef}"/>\n'
    add=''.join(f'  <url><loc>{url(d,s)}</loc><lastmod>2026-10-24</lastmod>\n{alts}  </url>\n' for _,d,_ in have)
    sm=sm.replace('</urlset>',add+'</urlset>')
    print(s, [h for h,_,_ in have])
open(f'{ROOT}/sitemap.xml','w').write(sm)
