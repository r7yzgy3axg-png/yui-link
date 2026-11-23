import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__))
GEO=os.environ.get('GEO','/tmp/claude-0/-home-user-yui-link/4019066c-ab27-584d-add1-17b60d3859c9/scratchpad/geo/japan.geojson')
OUT=os.path.join(HERE,'slides.html')
feats=json.load(open(GEO))['features']
COL={'fk':'#1F5F8B','yg':'#C0392B','sm':'#2E8B57','tt':'#C77D12'}
PNAME={'fk':'福岡','yg':'山口県','sm':'島根','tt':'鳥取'}

def make_proj(lon0,lon1,lat0,lat1,W,H):
    c=math.cos(math.radians((lat0+lat1)/2))
    k=min(W/((lon1-lon0)*c), H/(lat1-lat0))
    return (lambda lon,lat: ((lon-lon0)*c*k, (lat1-lat)*k)), (lon1-lon0)*c*k, (lat1-lat0)*k

def paths(proj,bbox,minpx=1.0,skip=()):
    out={}
    for f in feats:
        n=f['properties']['nam_ja']
        if n in skip: continue
        g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        d=[]
        for poly in polys:
            for ring in poly:
                lo=[p[0] for p in ring]; la=[p[1] for p in ring]
                if max(lo)<bbox[0] or min(lo)>bbox[1] or max(la)<bbox[2] or min(la)>bbox[3]: continue
                pts=[];last=None
                for lon,lat in ring:
                    x,y=proj(lon,lat)
                    if last is None or abs(x-last[0])+abs(y-last[1])>=minpx: pts.append((x,y)); last=(x,y)
                if len(pts)>=3: d.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z')
        if d: out[n]=''.join(d)
    return out

# ---------- spots (route order) ----------
# id, map label, legend name, desc, lon, lat, pref, day, dx, dy, anchor
spots=[
 ('1','博多・天神','博多・天神','屋台・ラーメン',130.40,33.59,'fk','D1',0,-22,'middle'),
 ('2','太宰府天満宮','太宰府天満宮','学問の神様',130.535,33.521,'fk','D1',15,6,'start'),
 ('3','小倉城','小倉城','九州の玄関口の城',130.874,33.884,'fk','D2',-15,6,'end'),
 ('4','門司港レトロ','門司港レトロ','レトロ建築と焼きカレー',130.975,33.93,'fk','D2',15,12,'start'),
 ('5','下関・唐戸市場','下関 唐戸市場・赤間神宮','朝のふく寿司・源平の舞台',130.93,34.0,'yg','D2',15,0,'start'),
 ('6','角島大橋','角島大橋','コバルトブルーの海を渡る橋',130.886,34.355,'yg','D3',-15,6,'end'),
 ('7','元乃隅神社','元乃隅神社','海へ続く123基の赤鳥居',131.031,34.418,'yg','D3',-8,-17,'end'),
 ('8','青海島','青海島','「海上アルプス」の遊覧船',131.215,34.44,'yg','D3',0,-18,'middle'),
 ('9','長門湯本温泉','長門湯本温泉','川沿いの再生温泉街',131.183,34.322,'yg','D3',-15,22,'end'),
 ('10','秋吉台・秋芳洞','秋吉台・秋芳洞','カルスト台地と大鍾乳洞',131.303,34.235,'yg','D4',-15,22,'end'),
 ('11','瑠璃光寺','山口市 瑠璃光寺・湯田温泉','国宝の五重塔と名湯',131.474,34.18,'yg','D4',15,20,'start'),
 ('12','萩','萩 城下町・松下村塾','幕末・維新の城下町',131.399,34.41,'yg','D5',8,-16,'start'),
 ('13','津和野','津和野','山陰の小京都',131.773,34.467,'sm','D6',15,6,'start'),
 ('14','石見銀山','石見銀山・温泉津温泉','世界遺産の鉱山町',132.42,35.10,'sm','D6-7',15,16,'start'),
 ('15','出雲大社','出雲大社','縁結びの神様',132.685,35.402,'sm','D7',-15,-6,'end'),
 ('16','松江城・宍道湖','松江城・宍道湖','国宝天守と夕日',133.05,35.475,'sm','D7-8',-6,-16,'end'),
 ('17','境港 水木しげるロード','境港 水木しげるロード','妖怪ブロンズ像の通り',133.235,35.545,'tt','D8',-4,-16,'start'),
 ('18','大山','大山','中国地方最高峰',133.53,35.37,'tt','D9',0,30,'middle'),
 ('19','三朝温泉','三朝温泉','ラジウムの名湯',133.86,35.41,'tt','D9',0,30,'middle'),
 ('20','鳥取砂丘','鳥取砂丘・砂の美術館','日本最大級の砂丘',134.23,35.54,'tt','D10',0,30,'middle'),
]
opts=[('A','錦帯橋',132.178,34.168,15,6,'start','11'),('B','宮島・広島',132.37,34.33,15,6,'start','A'),
      ('C','足立美術館',133.20,35.38,-30,28,'start','16'),('D','浦富海岸',134.34,35.59,0,-18,'end','20')]

# ---------- Detail map ----------
B=(130.15,134.5,33.35,35.78)
dproj,DW,DH=make_proj(*B,1240,860)
dp=paths(dproj,B,1.0)
fills={'山口県':'#F6C9A8','福岡県':'#DCE7F0','島根県':'#DCEEDF','鳥取県':'#F6E4C4'}
svg=[f'<svg viewBox="0 0 {DW:.0f} {DH:.0f}" width="{DW:.0f}" height="{DH:.0f}"><rect width="100%" height="100%" fill="var(--sea)"/>']
for n,d in dp.items():
    svg.append(f'<path d="{d}" fill="{fills.get(n,"#EFEBE3")}" stroke="#B59C82" stroke-width="{1.6 if n=="山口県" else 0.8}" stroke-linejoin="round"/>')
def T(lon,lat,txt,cls):
    x,y=dproj(lon,lat); return f'<text x="{x:.0f}" y="{y:.0f}" class="{cls}" text-anchor="middle">{txt}</text>'
for lon,lat,t,c in [(131.82,34.03,'山 口 県','pref main'),(132.55,34.88,'島 根 県','pref'),(133.85,35.22,'鳥 取 県','pref'),
                    (132.95,34.55,'広島県','pref dim'),(133.95,34.85,'岡山県','pref dim'),(130.98,33.66,'福 岡 県','pref'),(131.35,33.5,'大分県','pref dim'),(132.85,33.6,'愛媛県','pref dim')]:
    svg.append(T(lon,lat,t,c))
for lon,lat,t in [(131.6,35.3,'日 本 海'),(130.55,34.22,'響灘'),(132.1,33.8,'瀬 戸 内 海'),(130.35,33.98,'玄界灘')]:
    svg.append(T(lon,lat,t,'sea'))
P={s[0]:dproj(s[4],s[5]) for s in spots}
for o in opts: P[o[0]]=dproj(o[2],o[3])
pts=' '.join(f'{P[s[0]][0]:.0f},{P[s[0]][1]:.0f}' for s in spots)
for o in opts:
    (ax,ay),(bx,by)=P[o[7]],P[o[0]]
    svg.append(f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx:.0f}" y2="{by:.0f}" stroke="#8A8F99" stroke-width="3" stroke-dasharray="4 7" stroke-linecap="round"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#C0392B" stroke-width="4" stroke-dasharray="12 7" stroke-linejoin="round" stroke-linecap="round"/>')
for o in opts:
    x,y=P[o[0]]
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="#fff" stroke="#8A8F99" stroke-width="3"/><text x="{x:.0f}" y="{y+5:.0f}" class="mk gray" text-anchor="middle">{o[0]}</text>')
    svg.append(f'<text x="{x+o[4]:.0f}" y="{y+o[5]:.0f}" class="lbl gray halo" text-anchor="{o[6]}">{o[1]}</text>')
for s in spots:
    x,y=P[s[0]]
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{COL[s[6]]}" stroke="#fff" stroke-width="3"/><text x="{x:.0f}" y="{y+5:.0f}" class="mk" text-anchor="middle">{s[0]}</text>')
    svg.append(f'<text x="{x+s[8]:.0f}" y="{y+s[9]:.0f}" class="lbl halo" text-anchor="{s[10]}">{s[1]}</text>')
for r,t,dy in [('1','START',-58),('20','GOAL',-34)]:
    x,y=P[r]; svg.append(f'<g transform="translate({x:.0f},{y+dy:.0f})"><rect x="-38" y="-18" width="76" height="28" rx="14" fill="#2B2B2B"/><text y="2" class="flag" text-anchor="middle">{t}</text></g>')
x0,y0=30,DH-40; km=50/(111.32*math.cos(math.radians(34.5)))
x1=dproj(B[0]+km,34)[0]
svg.append(f'<rect x="{x0}" y="{y0-6}" width="{x1:.0f}" height="8" fill="#2B2B2B"/><text x="{x0}" y="{y0+24}" class="sea" style="fill:#2B2B2B">0</text><text x="{x0+x1:.0f}" y="{y0+24}" class="sea" style="fill:#2B2B2B" text-anchor="middle">50km</text>')
svg.append(f'<g transform="translate({DW-50:.0f},{DH-90:.0f})"><path d="M0,-30 L10,8 L0,2 L-10,8Z" fill="#2B2B2B"/><text y="30" class="sea" style="fill:#2B2B2B" text-anchor="middle">N</text></g>')
svg.append('</svg>'); detail='\n'.join(svg)

# ---------- Overview Japan ----------
JB=(128.6,146.0,30.8,45.7)
jproj,JW,JH=make_proj(*JB,780,900)
jp=paths(jproj,JB,1.4,skip=('沖縄県',))
s=[f'<svg viewBox="0 0 {JW:.0f} {JH:.0f}" width="{JW:.0f}" height="{JH:.0f}">']
jf={'山口県':'#C0392B','福岡県':'#9DBBD3','島根県':'#9CCFA9','鳥取県':'#EBC27F'}
for n,d in jp.items(): s.append(f'<path d="{d}" fill="{jf.get(n,"#E4DED3")}" stroke="#fff" stroke-width=".6"/>')
bx0,by0=jproj(B[0],B[3]); bx1,by1=jproj(B[1],B[2])
s.append(f'<rect x="{bx0:.0f}" y="{by0:.0f}" width="{bx1-bx0:.0f}" height="{by1-by0:.0f}" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-dasharray="5 4"/>')
yx,yy=jproj(131.5,34.2)
s.append(f'<line x1="{yx:.0f}" y1="{yy:.0f}" x2="{yx-20:.0f}" y2="{yy-170:.0f}" stroke="#C0392B" stroke-width="2.5"/><circle cx="{yx:.0f}" cy="{yy:.0f}" r="5" fill="#2B2B2B"/><text x="{yx-20:.0f}" y="{yy-184:.0f}" class="jlbl" text-anchor="middle">山口県</text>')
tx,ty=jproj(134.2,35.5); s.append(f'<line x1="{tx:.0f}" y1="{ty:.0f}" x2="{tx+30:.0f}" y2="{ty-120:.0f}" stroke="#C77D12" stroke-width="2.5"/><circle cx="{tx:.0f}" cy="{ty:.0f}" r="5" fill="#2B2B2B"/><text x="{tx+30:.0f}" y="{ty-134:.0f}" class="jlbl" style="fill:#C77D12" text-anchor="middle">鳥取県</text>')
for lon,lat,n,dx,dy,a in [(139.7,35.7,'東京',12,24,'start'),(135.5,34.7,'大阪',0,30,'middle')]:
    x,y=jproj(lon,lat); s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#2B2B2B"/><text x="{x+dx:.0f}" y="{y+dy:.0f}" class="jsm" text-anchor="{a}">{n}</text>')
s.append('</svg>'); japan='\n'.join(s)

# ---------- legend ----------
def li(s): return f'<li><span class="dot" style="background:{COL[s[6]]}">{s[0]}</span><div><b>{s[2]}</b><small>{s[3]}</small></div><em>{s[7]}</em></li>'
legend=''
for k,title in [('fk','福岡（九州の入口）'),('yg','山口県'),('sm','島根'),('tt','鳥取（ゴール）')]:
    legend+=f'<h3 style="border-color:{COL[k]}">{title}</h3><ul>'+''.join(li(s) for s in spots if s[6]==k)+'</ul>'
legend+='<h3 style="border-color:#8A8F99">日数が余ったら</h3><p class="optl">A 錦帯橋 / B 宮島・広島（山口市から寄り道）<br>C 足立美術館（松江から約40分）/ D 浦富海岸（砂丘から約30分）</p>'

itin=[
('1','fk','博多 → 太宰府','博多駅IN・太宰府天満宮<br>夜は中洲の屋台','博多','電車'),
('2','fk','小倉 → 関門海峡','小倉城・門司港レトロ<br>人道トンネルで本州へ<br>唐戸市場・赤間神宮','下関','電車＋徒歩'),
('3','yg','下関 → 長門','角島大橋・元乃隅神社<br>青海島観光船<br>※1番の絶景日','長門湯本温泉','車 約2h30'),
('4','yg','秋吉台 → 山口市','秋芳洞・秋吉台カルスト<br>瑠璃光寺五重塔','湯田温泉','車 約1h15'),
('5','yg','萩','城下町散策・松下村塾<br>萩城跡・萩焼体験','萩','車 約1h'),
('6','sm','津和野 → 温泉津','殿町通り・太皷谷稲成神社<br>夕方に温泉津温泉へ','温泉津温泉','車 約3h'),
('7','sm','石見銀山 → 出雲','大森の町並み・龍源寺間歩<br>出雲大社・出雲そば<br>宍道湖の夕日','松江','車 約2h'),
('8','tt','松江 → 境港','松江城・堀川めぐり<br>水木しげるロード','皆生温泉','車 約1h'),
('9','tt','大山 → 三朝','大山の山麓ドライブ<br>三朝温泉でのんびり','三朝温泉','車 約1h30'),
('10','tt','鳥取砂丘','鳥取砂丘・砂の美術館<br>→ 鳥取空港OUT','—','車 約1h'),
]
cards=''.join(f'<div class="card" style="border-top-color:{COL[p]}"><div class="dn">DAY<b>{i}</b></div><h4>{a}</h4><p>{b}</p><div class="meta"><span>🏨 {c}</span><span>🚗 {d}</span></div></div>' for i,p,a,b,c,d in itin)

css=open(os.path.join(HERE,'style.css')).read()
html=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<section class="slide s1" id="s1">
 <div class="jp">{japan}</div>
 <div class="right">
  <span class="tag">TRAVEL PLAN 2026</span>
  <h1><span>山口県</span>を巡る<br>10日間の旅</h1>
  <p class="sub">九州の入口・福岡から、山口・島根を抜けて鳥取砂丘まで</p>
  <div class="stats">
   <div class="stat"><b>10<small>日間</small></b><p>9泊10日</p></div>
   <div class="stat"><b>20<small>スポット</small></b><p>山口8 + 周辺12</p></div>
   <div class="stat"><b>4<small>県</small></b><p>福岡・山口・島根・鳥取</p></div>
  </div>
  <div class="flow"><span class="st">福岡 IN</span><i>▶</i><span class="st y">山口県 4日</span><i>▶</i><span class="st">島根</span><i>▶</i><span class="st">鳥取 OUT</span></div>
  <ul class="points">
   <li>西から東へ一筆書き ─ 同じ道を戻らない</li>
   <li>九州は電車、山口からはレンタカーで点在する名所へ</li>
   <li>行きは博多駅、帰りは鳥取空港（羽田便）で往復が楽</li>
  </ul>
 </div>
</section>
<section class="slide s2" id="s2">
 <div class="hdr"><div class="k">MAP &amp; SPOTS</div><h2>観光名所マップ</h2></div>
 <div class="mapwrap">{detail}</div>
 <div class="side">{legend}
  <div class="routekey"><svg width="60" height="10"><line x1="0" y1="5" x2="60" y2="5" stroke="#C0392B" stroke-width="4" stroke-dasharray="12 7"/></svg>おすすめルート<svg width="60" height="10"><line x1="0" y1="5" x2="60" y2="5" stroke="#8A8F99" stroke-width="3" stroke-dasharray="4 7"/></svg>寄り道</div>
 </div>
</section>
<section class="slide s3" id="s3">
 <div class="hdr"><div class="k">ITINERARY</div><h2>10日間モデルコース</h2></div>
 <div class="legend3">{''.join(f'<span style="--c:{COL[k]}">{PNAME[k]}</span>' for k in COL)}</div>
 <div class="grid">{cards}</div>
</section>
<section class="slide s4" id="s4">
 <div class="hdr"><div class="k">GOURMET &amp; TIPS</div><h2>旅を楽しむポイント</h2></div>
 <div class="cols">
  <div class="box"><h3>食べたい<span>ご当地グルメ</span></h3><div class="food">
   <div><i>🍜</i><span><b>博多ラーメン・もつ鍋</b><small>中洲の屋台で（D1）</small></span></div>
   <div><i>🍛</i><span><b>焼きカレー</b><small>門司港名物（D2）</small></span></div>
   <div><i>🐡</i><span><b>ふく（ふぐ）料理・瓦そば</b><small>下関・唐戸市場の朝寿司（D2〜3）</small></span></div>
   <div><i>🍊</i><span><b>夏みかんスイーツ</b><small>萩の名産（D5）</small></span></div>
   <div><i>🥢</i><span><b>出雲そば</b><small>割子そばで食べ比べ（D7）</small></span></div>
   <div><i>🐚</i><span><b>宍道湖のしじみ汁</b><small>松江で朝ごはんに（D8）</small></span></div>
   <div><i>🦀</i><span><b>松葉ガニ・二十世紀梨</b><small>鳥取の冬と秋の味覚（D9〜10）</small></span></div>
  </div></div>
  <div class="box"><h3>効率よく回る<span>コツ</span></h3><ul class="tips">
   <li data-n="1">九州は電車、車はD3から<small>博多〜下関は電車と徒歩で十分</small></li>
   <li data-n="2">乗り捨て料金は事前に比較<small>下関で借りて鳥取で返す。県をまたぐので高めになりがち</small></li>
   <li data-n="3">絶景の日（D3）は晴れ予報に合わせる<small>雨なら秋芳洞（D4）と入れ替え</small></li>
   <li data-n="4">関門海峡は歩いて渡れる<small>海底の人道トンネル約780m・15分で九州→本州</small></li>
   <li data-n="5">冬の大山は雪に注意<small>12〜3月はスタッドレスタイヤ必須</small></li>
  </ul></div>
  <div class="box"><h3>日数が<span>余ったら</span></h3><ul class="tips">
   <li data-n="A">錦帯橋（岩国）<small>山口市から車で約1h15。5連アーチの木造橋 +1日</small></li>
   <li data-n="B">宮島・広島<small>錦帯橋とセットで +1〜2日</small></li>
   <li data-n="C">足立美術館<small>松江から約40分。日本一と評される庭園</small></li>
   <li data-n="D">浦富海岸<small>鳥取砂丘から約30分。透明度の高い海と奇岩</small></li>
   <li data-n="E">宿は早めに予約<small>長門湯本・温泉津・三朝は宿が少なめ</small></li>
  </ul></div>
 </div>
</section>
</body></html>'''
open(OUT,'w').write(html); print(DW,DH)
