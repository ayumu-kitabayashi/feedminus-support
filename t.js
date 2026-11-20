/* どの記事・サイトから来て、App Store に進んだかを測る（種まきの効果を見るため）。
   Cookie も localStorage も使わない。同じタブの中だけ sessionStorage で「最初の参照元」を覚える。
   送るのは：開いたページ・参照元のドメイン・?ref= の値・言語（頁の言語とブラウザの表示言語の2字）・端末の種類（iphone などの1語）・App Store を押したか。
   11/20 から：どの AI・検索から来たか（chatgpt などの1語）・utm_source の値・アプリの中のブラウザか（instagram などの1語）。 */
(function(){
  var KEY='phc_B8s9xLNrx8Eg8DPWqLQDN3WGHBEbQwqpQiXDKTxxVJY4', HOST='https://us.i.posthog.com/i/v0/e/';
  var ss; try{ss=window.sessionStorage;}catch(e){}
  function get(k){try{return ss&&ss.getItem(k);}catch(e){return null;}}
  function set(k,v){try{ss&&ss.setItem(k,v);}catch(e){}}

  var q=new URLSearchParams(location.search);
  var refHost=''; try{refHost=document.referrer?new URL(document.referrer).hostname.replace(/^www\./,''):'';}catch(e){}
  var internal=/(^|\.)minulo\.app$/.test(refHost)||refHost===location.hostname;
  var utm=(q.get('utm_source')||'').toLowerCase().slice(0,60);
  /* AI・検索の名前を1語に。ChatGPT は utm_source=chatgpt.com を付けるが referrer はほぼ付かない（11/20 実測：8週で 2,202人中 referrer ありは 5人）。
     claude.ai は Referrer-Policy: same-origin で referrer を渡さず、utm も付けない＝Claude の答えからの来訪は「直接」に入る。 */
  function engine(h){
    h=String(h||'').toLowerCase();
    if(/chatgpt/.test(h)) return 'chatgpt';
    if(h==='openai') return 'openai';
    if(/claude|anthropic/.test(h)) return 'claude';
    if(/perplexity/.test(h)) return 'perplexity';
    if(/gemini|bard\.google/.test(h)) return 'gemini';
    if(/copilot/.test(h)) return 'copilot';
    if(/(^|\.)bing\.com$/.test(h)) return 'bing';
    if(/(^|\.)search\.brave\.com$/.test(h)) return 'brave';
    if(/duckduckgo/.test(h)) return 'duckduckgo';
    if(/(^|\.)kagi\.com$/.test(h)) return 'kagi';
    if(/(^|\.)you\.com$/.test(h)) return 'you';
    if(/phind/.test(h)) return 'phind';
    if(/(^|\.)google\.[a-z.]+$/.test(h)) return 'google';
    return '';
  }
  var utmAi=engine(utm);
  /* AI の utm は、頁の URL に残っていた ?ref=（種のリンクの札）より先にする。AI が種の札つきの URL を引いても AI の来訪として数える。 */
  var tag=utmAi?utm:(q.get('ref')||utm||'');
  /* 最初に来たときの参照元を、このタブの間は持ち続ける */
  if(!get('m_src')){ set('m_src', tag||(!internal&&refHost)||'direct'); set('m_land', location.pathname); set('m_ai', utmAi||(!internal&&engine(refHost))||''); }
  var src=get('m_src')||'direct', land=get('m_land')||location.pathname, ai=get('m_ai')||'';
  var sid=get('m_sid'); if(!sid){ sid='w'+Math.random().toString(36).slice(2)+Date.now().toString(36); set('m_sid',sid); }

  /* 端末の種類を1語だけ（iphone・ipad・mac・windows・android・other）。UA の文字列そのものは送らない。 */
  var device='other';
  try{
    var ua=navigator.userAgent||'', uad=navigator.userAgentData, plat=(uad&&uad.platform)||'';
    if(/iPhone|iPod/.test(ua)) device='iphone';
    else if(/iPad/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1)) device='ipad';
    else if(/Android/i.test(plat)||/Android/.test(ua)) device='android';
    else if(/Windows/i.test(plat)||/Windows/.test(ua)) device='windows';
    else if(/macOS/i.test(plat)||/Macintosh|Mac OS X/.test(ua)) device='mac';
  }catch(e){}

  /* アプリの中のブラウザかを1語だけ。referrer の無い「直接」を、SNS のアプリから来た人と分けるため。UA の文字列そのものは送らない。
     ios_webview は Safari の札が無い iPhone の画面（アプリの中のブラウザ）。Claude・ChatGPT のアプリがどれを使うかは確かめていない。 */
  var inapp='';
  try{
    var ua2=navigator.userAgent||'';
    if(/Instagram/.test(ua2)) inapp='instagram';
    else if(/FBAN|FBAV/.test(ua2)) inapp='facebook';
    else if(/ Line\//.test(ua2)) inapp='line';
    else if(/KAKAOTALK/i.test(ua2)) inapp='kakaotalk';
    else if(/NAVER\(inapp/.test(ua2)) inapp='naver';
    else if(/iPhone|iPad|iPod/.test(ua2)&&!/Safari\//.test(ua2)) inapp='ios_webview';
    else if(/; wv\)/.test(ua2)) inapp='android_webview';
  }catch(e){}

  /* ブラウザの表示言語の最初の2字だけ（ko・ja など）。サイトの計測は IP も国も持たないので、韓国語の人がどの頁に来たかをこれで見る。 */
  var blang=''; try{ blang=String((navigator.languages&&navigator.languages[0])||navigator.language||'').slice(0,2).toLowerCase(); }catch(e){}

  function send(ev,props){
    var p={distinct_id:sid,$process_person_profile:false,site:true,host:location.hostname,path:location.pathname,
      lang:document.documentElement.lang||'',blang:blang,src:src,landing:land,ref_domain:internal?'(内部)':(refHost||'(なし)'),ref_tag:tag,ref_utm:utm,ai:ai,inapp:inapp};
    for(var k in props) p[k]=props[k];
    var body=JSON.stringify({api_key:KEY,event:ev,properties:p,timestamp:new Date().toISOString()});
    try{ if(navigator.sendBeacon&&navigator.sendBeacon(HOST,new Blob([body],{type:'text/plain'}))) return; }catch(e){}
    try{ fetch(HOST,{method:'POST',body:body,keepalive:true,headers:{'Content-Type':'text/plain'}}); }catch(e){}
  }
  send('site_view',{device:device});
  /* ページ内の小さなスクリプト（言語の案内など）からも同じ形で送れるようにする。t.js より先に積まれた分もここで送る。 */
  window.minuloTrack=send;
  var mq=window.minuloQ||[]; window.minuloQ=[]; for(var qi=0;qi<mq.length;qi++){ try{ send(mq[qi][0],mq[qi][1]||{}); }catch(e){} }

  /* App Store の minulo へのリンクに、参照元を ct として付ける（ASC の「キャンペーン」で数が見える） */
  function slug(s){return String(s).toLowerCase().replace(/[^a-z0-9.]+/g,'-').replace(/^-|-$/g,'');}
  var page=slug(location.pathname.replace(/\.html$/,'').replace(/\/$/,'/top'))||'top';
  var links=document.querySelectorAll('a[href*="apps.apple.com"][href*="id6809352229"]');
  for(var i=0;i<links.length;i++){
    (function(a){
      try{
        var u=new URL(a.href), old=u.searchParams.get('ct');
        /* data-pos（例：下に固定のバー＝sticky）のリンクは、40字で切っても ct の最後に -pos が残るようにする */
        var pos=a.getAttribute('data-pos')||'', sx=pos?'-'+pos:'';
        if(sx&&old&&old.slice(-sx.length)===sx) old=old.slice(0,-sx.length);
        var ct=(slug(src.replace(/\.(com|io|dev|jp|net|org|co\.kr|me|app)$/,''))+'_'+(old||page)).slice(0,40-sx.length)+sx;
        u.searchParams.set('pt','129109285'); u.searchParams.set('ct',ct); u.searchParams.set('mt','8');
        a.href=u.toString();
        a.addEventListener('click',function(){ send('site_store_click',{ct:ct,where:(old||'')+sx,pos:pos,device:device}); });
      }catch(e){}
    })(links[i]);
  }
  /* Mac 版（.dmg）のダウンロードも数える */
  var macs=document.querySelectorAll('a[href*="minulo.dmg"]');
  for(var j=0;j<macs.length;j++){
    (function(a){ a.addEventListener('click',function(){ send('site_mac_click',{where:a.getAttribute('data-pos')||page}); }); })(macs[j]);
  }
})();
