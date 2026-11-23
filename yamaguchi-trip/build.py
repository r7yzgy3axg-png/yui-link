import json, math
GEO='/tmp/claude-0/-home-user-yui-link/4019066c-ab27-584d-add1-17b60d3859c9/scratchpad/geo/japan.geojson'
OUT='/tmp/claude-0/-home-user-yui-link/4019066c-ab27-584d-add1-17b60d3859c9/scratchpad/slides.html'
feats=json.load(open(GEO))['features']

def make_proj(lon0,lon1,lat0,lat1,W,H):
    c=math.cos(math.radians((lat0+lat1)/2))
    k=min(W/((lon1-lon0)*c), H/(lat1-lat0))
    w=(lon1-lon0)*c*k; h=(lat1-lat0)*k
    return (lambda lon,lat: ((lon-lon0)*c*k, (lat1-lat)*k)), w, h

def paths(proj, bbox, minpx=1.2, skip=()):
    out={}
    for f in feats:
        name=f['properties']['nam_ja']
        if name in skip: continue
        g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        d=[]
        for poly in polys:
            for ring in poly:
                lons=[p[0] for p in ring]; lats=[p[1] for p in ring]
                if max(lons)<bbox[0] or min(lons)>bbox[1] or max(lats)<bbox[2] or min(lats)>bbox[3]: continue
                pts=[];last=None
                for lon,lat in ring:
                    x,y=proj(lon,lat)
                    if last is None or abs(x-last[0])+abs(y-last[1])>=minpx:
                        pts.append((x,y)); last=(x,y)
                if len(pts)<3: continue
                d.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z')
        if d: out[name]=''.join(d)
    return out

# ---------- Detail map ----------
B=(130.15,133.0,33.15,35.55)
dproj,DW,DH=make_proj(*B,1120,1000)
dp=paths(dproj,B,1.0)
fill={'山口県':'#F6C9A8'}
neigh={'広島県','島根県','福岡県'}
svg=[f'<svg class="map" viewBox="0 0 {DW:.0f} {DH:.0f}" width="{DW:.0f}" height="{DH:.0f}"><rect width="100%" height="100%" fill="var(--sea)"/>']
for n,d in dp.items():
    c=fill.get(n,'#FBF3E4' if n in neigh else '#EFEBE3')
    svg.append(f'<path d="{d}" fill="{c}" stroke="#B59C82" stroke-width="{1.6 if n=="山口県" else 0.8}" stroke-linejoin="round"/>')
def T(lon,lat,txt,cls,dx=0,dy=0,anchor='middle'):
    x,y=dproj(lon,lat); return f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" class="{cls}" text-anchor="{anchor}">{txt}</text>'
for lon,lat,t in [(131.85,34.0,'山 口 県'),(132.78,34.72,'広島県'),(132.55,35.0,'島根県'),(130.72,33.62,'福岡県'),(131.32,33.48,'大分県'),(132.75,33.55,'愛媛県')]:
    svg.append(T(lon,lat,t,'pref' if t!='山 口 県' else 'pref main'))
for lon,lat,t in [(130.75,34.95,'日 本 海'),(130.48,34.2,'響 灘'),(131.95,33.75,'瀬 戸 内 海'),(130.38,33.98,'玄 界 灘')]:
    svg.append(T(lon,lat,t,'sea'))

spots=[ # id, name, lon, lat, kind, label dx,dy,anchor
 ('10','広島 平和記念公園',132.453,34.395,'n',16,6,'start'),
 ('11','宮島 厳島神社',132.320,34.296,'n',16,22,'start'),
 ('1','錦帯橋',132.178,34.168,'y',16,6,'start'),
 ('2','山口市 瑠璃光寺',131.474,34.180,'y',16,24,'start'),
 ('12','津和野',131.773,34.467,'n',16,6,'start'),
 ('3','萩 城下町・松下村塾',131.399,34.410,'y',0,36,'start'),
 ('4','秋吉台・秋芳洞',131.303,34.235,'y',16,-6,'start'),
 ('5','長門湯本温泉',131.183,34.322,'y',-16,26,'end'),
 ('6','青海島',131.215,34.432,'y',-6,-18,'end'),
 ('7','元乃隅神社',131.031,34.418,'y',-16,-8,'end'),
 ('8','角島大橋',130.886,34.355,'y',-16,6,'end'),
 ('9','下関 唐戸市場・赤間神宮',130.93,33.99,'y',16,0,'start'),
 ('13','門司港レトロ',130.968,33.935,'n',16,14,'start'),
 ('14','小倉城',130.874,33.884,'n',-16,10,'end'),
 ('15','太宰府天満宮',130.535,33.521,'n',16,6,'start'),
 ('16','博多・天神',130.40,33.59,'n',0,-24,'middle'),
]
opts=[('A','出雲大社',132.685,35.402,16,6,'start'),('B','石見銀山',132.44,35.11,16,6,'start'),
      ('C','別府・湯布院',131.45,33.27,16,6,'start'),('D','周防大島',132.27,33.92,16,6,'start'),
      ('E','川棚温泉（瓦そば）',130.955,34.156,-14,6,'end')]
P={s[0]:dproj(s[2],s[3]) for s in spots}
route=['10','11','1','2','12','3','4','5','6','7','8','9','13','14','15','16']
pts=' '.join(f'{P[r][0]:.0f},{P[r][1]:.0f}' for r in route)
svg.append(f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>')
svg.append(f'<polyline points="{pts}" fill="none" stroke="#C0392B" stroke-width="4" stroke-dasharray="12 7" stroke-linejoin="round" stroke-linecap="round"/>')
# optional dashed branches
for a,b in [('12','A'),('14','C'),('1','D')]:
    ox,oy=P[a]; o=[x for x in opts if x[0]==b][0]; tx,ty=dproj(o[2],o[3])
    svg.append(f'<line x1="{ox:.0f}" y1="{oy:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="#8A8F99" stroke-width="3" stroke-dasharray="4 7" stroke-linecap="round"/>')
for o in opts:
    x,y=dproj(o[2],o[3])
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="#fff" stroke="#8A8F99" stroke-width="3"/><text x="{x:.0f}" y="{y+5:.0f}" class="mk gray" text-anchor="middle">{o[0]}</text>')
    svg.append(f'<text x="{x+o[4]:.0f}" y="{y+o[5]:.0f}" class="lbl gray halo" text-anchor="{o[6]}">{o[1]}</text>')
for s in spots:
    x,y=P[s[0]]; col='#C0392B' if s[4]=='y' else '#1F5F8B'
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="{col}" stroke="#fff" stroke-width="3"/><text x="{x:.0f}" y="{y+5.5:.0f}" class="mk" text-anchor="middle">{s[0]}</text>')
    svg.append(f'<text x="{x+s[5]:.0f}" y="{y+s[6]:.0f}" class="lbl halo" text-anchor="{s[7]}">{s[1]}</text>')
# IN/OUT flags
for r,t,dx,dy in [('10','START',0,-30),('16','GOAL',0,-64)]:
    x,y=P[r]; svg.append(f'<g transform="translate({x+dx:.0f},{y+dy:.0f})"><rect x="-38" y="-18" width="76" height="28" rx="14" fill="#2B2B2B"/><text y="2" class="flag" text-anchor="middle">{t}</text></g>')
# scale bar 50km
x0,y0=30,DH-40; km=50/ (111.32*math.cos(math.radians(34.3)))
x1=dproj(B[0]+km,34)[0]-dproj(B[0],34)[0]
svg.append(f'<g><rect x="{x0}" y="{y0-6}" width="{x1:.0f}" height="8" fill="#2B2B2B"/><text x="{x0}" y="{y0+24}" class="sea" style="fill:#2B2B2B">0</text><text x="{x0+x1:.0f}" y="{y0+24}" class="sea" style="fill:#2B2B2B" text-anchor="middle">50km</text></g>')
# compass
svg.append(f'<g transform="translate({DW-50:.0f},{DH-110:.0f})"><path d="M0,-30 L10,8 L0,2 L-10,8Z" fill="#2B2B2B"/><text y="30" class="sea" style="fill:#2B2B2B" text-anchor="middle">N</text></g>')
svg.append('</svg>')
detail='\n'.join(svg)

# ---------- Overview Japan ----------
JB=(128.6,146.0,30.8,45.7)
jproj,JW,JH=make_proj(*JB,780,900)
jp=paths(jproj,JB,1.4,skip=('沖縄県',))
s=[f'<svg viewBox="0 0 {JW:.0f} {JH:.0f}" width="{JW:.0f}" height="{JH:.0f}">']
for n,d in jp.items():
    c='#C0392B' if n=='山口県' else ('#F3D9B8' if n in neigh else '#E4DED3')
    s.append(f'<path d="{d}" fill="{c}" stroke="#fff" stroke-width=".6"/>')
bx0,by0=jproj(B[0],B[3]); bx1,by1=jproj(B[1],B[2])
s.append(f'<rect x="{bx0:.0f}" y="{by0:.0f}" width="{bx1-bx0:.0f}" height="{by1-by0:.0f}" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-dasharray="5 4"/>')
yx,yy=jproj(131.5,34.2)
s.append(f'<line x1="{yx:.0f}" y1="{yy:.0f}" x2="{yx-20:.0f}" y2="{yy-170:.0f}" stroke="#C0392B" stroke-width="2.5"/><circle cx="{yx:.0f}" cy="{yy:.0f}" r="5" fill="#2B2B2B"/><text x="{yx-20:.0f}" y="{yy-184:.0f}" class="jlbl" text-anchor="middle">山口県</text>')
tx,ty=jproj(139.7,35.7); s.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="6" fill="#2B2B2B"/><text x="{tx+12:.0f}" y="{ty+24:.0f}" class="jsm">東京</text>')
ox,oy=jproj(135.5,34.7); s.append(f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="6" fill="#2B2B2B"/><text x="{ox:.0f}" y="{oy+30:.0f}" class="jsm" text-anchor="middle">大阪</text>')
s.append('</svg>')
japan='\n'.join(s)

legend_y=[s for s in spots if s[4]=='y']; legend_n=[s for s in spots if s[4]=='n']
days={'10':'D1','11':'D2','1':'D3','2':'D3','12':'D4','3':'D4-5','4':'D6','5':'D6','6':'D7','7':'D7','8':'D7','9':'D8','13':'D8','14':'D9','15':'D9','16':'D10'}
desc={'1':'5連アーチの木造橋','2':'国宝の五重塔と名湯','3':'幕末・維新の城下町','4':'日本最大級のカルスト台地と鍾乳洞','5':'川沿いの再生温泉街','6':'「海上アルプス」の遊覧船','7':'海へ続く123基の赤鳥居','8':'コバルトブルーの海を渡る橋','9':'朝のふく寿司・源平の舞台',
'10':'原爆ドーム','11':'海に浮かぶ大鳥居','12':'山陰の小京都','13':'レトロ建築と焼きカレー','14':'九州の玄関口の城','15':'学問の神様','16':'屋台・ラーメン'}
full={'2':'山口市 瑠璃光寺・湯田温泉'}
def li(s,col):
    return f'<li><span class="dot" style="background:{col}">{s[0]}</span><div><b>{full.get(s[0],s[1])}</b><small>{desc[s[0]]}</small></div><em>{days[s[0]]}</em></li>'
legend='<h3 class="y">山口県の名所</h3><ul>'+''.join(li(s,'#C0392B') for s in legend_y)+'</ul><h3 class="n">近場（広島・島根・福岡）</h3><ul>'+''.join(li(s,'#1F5F8B') for s in legend_n)+'</ul><h3 class="g">日数が余ったら</h3><p class="optl">A 出雲大社 / B 石見銀山（津和野から北へ +2日）<br>C 別府・湯布院（小倉から +1〜2日）<br>D 周防大島 / E 川棚温泉の瓦そば</p>'

itin=[
('1','広島','原爆ドーム・平和記念公園<br>夜はお好み焼き','広島','新幹線で広島IN'),
('2','宮島 → 岩国','厳島神社・弥山ロープウェー<br>牡蠣・もみじ饅頭','岩国','車 約1h'),
('3','岩国 → 山口市','錦帯橋・岩国城<br>瑠璃光寺五重塔','湯田温泉','車 約1h15'),
('4','津和野 → 萩','津和野 殿町通り・太皷谷稲成神社<br>夕方に萩へ','萩','車 約1h+1h'),
('5','萩','城下町散策・松下村塾<br>萩城跡・萩焼体験','萩（連泊）','レンタサイクル'),
('6','秋吉台 → 長門','秋芳洞・秋吉台カルスト<br>長門湯本の温泉街','長門湯本','車 約1h30'),
('7','長門 → 下関','青海島観光船・元乃隅神社<br>角島大橋 ※1番の絶景日','下関','車 約2h30'),
('8','関門海峡','唐戸市場で朝ふく寿司・赤間神宮<br>人道トンネルで九州へ → 門司港','小倉','徒歩で海峡越え'),
('9','小倉 → 太宰府','小倉城 → 太宰府天満宮<br>夜は博多の屋台','博多','電車 約1h30'),
('10','福岡','博多・天神でお土産<br>明太子・博多ラーメン','—','福岡空港/博多駅OUT'),
]
cards=''.join(f'<div class="card {"y" if i in "34567" or i=="8" else ""}"><div class="dn">DAY<b>{i}</b></div><h4>{a}</h4><p>{b}</p><div class="meta"><span>🏨 {c}</span><span>🚗 {d}</span></div></div>' for i,a,b,c,d in itin)

html=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
<style>
:root{{--sea:#D8EAF2;--ink:#2B2B2B;--red:#C0392B;--blue:#1F5F8B;--paper:#FFFBF4}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#999;font-family:"Zen Maru Gothic","IPAPGothic",sans-serif;color:var(--ink)}}
.slide{{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;margin-bottom:20px}}
.hdr{{position:absolute;left:60px;top:40px}}
.hdr .k{{font-size:22px;letter-spacing:.3em;color:var(--red);font-weight:700}}
.hdr h2{{font-size:52px;font-weight:900;margin-top:4px}}
.pg{{position:absolute;right:60px;top:52px;font-size:22px;color:#8a7f72;font-weight:700}}
/* slide1 */
.s1 .jp{{position:absolute;left:30px;top:110px}}
.jlbl{{font-size:34px;font-weight:900;fill:var(--red)}} .jsm{{font-size:22px;fill:#555;font-weight:700}}
.s1 .right{{position:absolute;left:820px;top:130px;width:1020px}}
.s1 .tag{{display:inline-block;background:var(--red);color:#fff;font-weight:700;padding:8px 22px;border-radius:30px;font-size:24px;letter-spacing:.1em}}
.s1 h1{{font-size:108px;font-weight:900;line-height:1.1;margin:26px 0 10px}}
.s1 h1 span{{color:var(--red)}}
.s1 .sub{{font-size:30px;color:#6b6157;font-weight:700}}
.stats{{display:flex;gap:24px;margin:50px 0 40px}}
.stat{{flex:1;background:#fff;border-radius:22px;padding:24px 26px;box-shadow:0 4px 0 #EADFCF}}
.stat b{{font-size:64px;font-weight:900;color:var(--red);line-height:1}} .stat b small{{font-size:26px}}
.stat p{{font-size:22px;font-weight:700;margin-top:8px;color:#6b6157}}
.flow{{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:900}}
.flow .st{{background:#fff;border:3px solid var(--ink);border-radius:16px;padding:12px 20px}}
.flow .st.y{{background:var(--red);border-color:var(--red);color:#fff}}
.flow i{{font-style:normal;color:var(--red)}}
.points{{margin-top:44px;font-size:26px;font-weight:700;line-height:1.9}}
.points li{{list-style:none;padding-left:40px;position:relative}}
.points li:before{{content:"✓";position:absolute;left:0;color:var(--red);font-weight:900}}
/* slide2 */
.s2 .mapwrap{{position:absolute;left:40px;top:40px;border-radius:24px;overflow:hidden;box-shadow:0 6px 0 #EADFCF}}
.pref{{font-size:26px;font-weight:700;fill:#9b8b78;letter-spacing:.1em}} .pref.main{{font-size:40px;fill:#B5542F;font-weight:900;letter-spacing:.2em}}
.sea{{font-size:20px;fill:#6E98AE;font-weight:700;letter-spacing:.2em}}
.mk{{font-size:15px;font-weight:900;fill:#fff}} .mk.gray{{fill:#5d636e}}
.lbl{{font-size:19px;font-weight:900;fill:var(--ink)}} .lbl.gray{{fill:#5d636e;font-weight:700}}
.halo{{paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round}}
.flag{{font-size:15px;font-weight:900;fill:#fff;letter-spacing:.1em}}
.s2 .side{{position:absolute;left:1065px;top:40px;right:50px}}
.s2 .side .k{{font-size:20px;letter-spacing:.3em;color:var(--red);font-weight:700}}
.s2 .side h2{{font-size:44px;font-weight:900;margin:2px 0 12px}}
.s2 h3{{font-size:22px;font-weight:900;margin:14px 0 6px;padding-left:14px;border-left:8px solid}}
h3.y{{border-color:var(--red)}} h3.n{{border-color:var(--blue)}} h3.g{{border-color:#8A8F99}}
.s2 ul{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}}
.s2 li{{display:flex;align-items:center;gap:10px;background:#fff;border-radius:12px;padding:7px 10px}}
.s2 li .dot{{flex:none;width:32px;height:32px;border-radius:50%;color:#fff;font-weight:900;font-size:15px;display:grid;place-items:center}}
.s2 li div{{flex:1;line-height:1.2}} .s2 li b{{font-size:17px;display:block}} .s2 li small{{font-size:13.5px;color:#7a6f63;font-weight:700}}
.s2 li em{{font-style:normal;font-size:13px;font-weight:900;background:#F3E6D4;border-radius:8px;padding:3px 7px;color:#8a5a2b}}
.optl{{font-size:17px;font-weight:700;line-height:1.6;color:#5d636e}}
.routekey{{display:flex;gap:20px;font-size:16px;font-weight:700;margin-top:10px;color:#5d636e;align-items:center}}
/* slide3 */
.grid{{position:absolute;left:60px;right:60px;top:170px;display:grid;grid-template-columns:repeat(5,1fr);gap:22px}}
.card{{background:#fff;border-radius:22px;padding:22px 22px 18px;height:400px;display:flex;flex-direction:column;box-shadow:0 5px 0 #EADFCF;border-top:10px solid var(--blue)}}
.card.y{{border-top-color:var(--red)}}
.dn{{font-size:20px;font-weight:900;color:#a39584;letter-spacing:.15em}} .dn b{{font-size:54px;color:var(--ink);margin-left:8px;letter-spacing:0}}
.card h4{{font-size:30px;font-weight:900;margin:6px 0 12px}}
.card p{{font-size:21px;font-weight:700;line-height:1.6;color:#4a423a;flex:1}}
.meta{{display:flex;flex-direction:column;gap:6px;font-size:18px;font-weight:700;border-top:2px dashed #E6DACA;padding-top:12px;color:#6b6157}}
.legend3{{position:absolute;right:60px;top:60px;display:flex;gap:24px;font-size:20px;font-weight:700}}
.legend3 span:before{{content:"";display:inline-block;width:26px;height:10px;border-radius:5px;margin-right:8px;vertical-align:middle;background:var(--c)}}
/* slide4 */
.cols{{position:absolute;left:60px;right:60px;top:170px;display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:28px}}
.box{{background:#fff;border-radius:24px;padding:30px 32px;box-shadow:0 5px 0 #EADFCF;height:850px}}
.box h3{{font-size:34px;font-weight:900;margin-bottom:20px}} .box h3 span{{color:var(--red)}}
.food{{display:grid;grid-template-columns:1fr;gap:12px}}
.food div{{display:flex;gap:16px;align-items:center;background:var(--paper);border-radius:16px;padding:12px 16px}}
.food i{{font-style:normal;font-size:40px}} .food b{{font-size:24px;display:block}} .food small{{font-size:18px;color:#7a6f63;font-weight:700}}
.tips li{{list-style:none;font-size:25px;font-weight:700;line-height:1.55;margin-bottom:40px;padding-left:44px;position:relative}}
.tips li:before{{content:attr(data-n);position:absolute;left:0;top:2px;width:32px;height:32px;border-radius:50%;background:var(--red);color:#fff;font-size:18px;display:grid;place-items:center}}
.tips li small{{display:block;font-size:20px;margin-top:4px;color:#7a6f63}}
</style></head><body>

<section class="slide s1" id="s1">
 <div class="jp">{japan}</div>
 <div class="right">
  <span class="tag">TRAVEL PLAN 2026</span>
  <h1><span>山口県</span>を巡る<br>10日間の旅</h1>
  <p class="sub">本州の西の端から、広島・島根・福岡までぐるっと周遊</p>
  <div class="stats">
   <div class="stat"><b>10<small>日間</small></b><p>9泊10日</p></div>
   <div class="stat"><b>16<small>スポット</small></b><p>山口9 + 近場7</p></div>
   <div class="stat"><b>4<small>県</small></b><p>山口・広島・島根・福岡</p></div>
  </div>
  <div class="flow"><span class="st">広島 IN</span><i>▶</i><span class="st y">山口県 7日</span><i>▶</i><span class="st">関門海峡</span><i>▶</i><span class="st">福岡 OUT</span></div>
  <ul class="points">
   <li>一筆書きルートで「行って戻る」ムダをなくす</li>
   <li>山口県内は名所が点在 → レンタカー移動が効率的</li>
   <li>新幹線の駅がある広島 IN／博多 OUT で往復を楽に</li>
  </ul>
 </div>
</section>

<section class="slide s2" id="s2">
 <div class="mapwrap">{detail}</div>
 <div class="side">
  <div class="k">MAP & SPOTS</div><h2>観光名所マップ</h2>
  {legend}
  <div class="routekey"><svg width="60" height="10"><line x1="0" y1="5" x2="60" y2="5" stroke="#C0392B" stroke-width="4" stroke-dasharray="12 7"/></svg>おすすめルート<svg width="60" height="10"><line x1="0" y1="5" x2="60" y2="5" stroke="#8A8F99" stroke-width="3" stroke-dasharray="4 7"/></svg>寄り道オプション</div>
 </div>
</section>

<section class="slide s3" id="s3">
 <div class="hdr"><div class="k">ITINERARY</div><h2>10日間モデルコース</h2></div>
 <div class="legend3"><span style="--c:#C0392B">山口県内</span><span style="--c:#1F5F8B">近場（広島・福岡）</span></div>
 <div class="grid">{cards}</div>
</section>

<section class="slide s4" id="s4">
 <div class="hdr"><div class="k">GOURMET & TIPS</div><h2>旅を楽しむポイント</h2></div>
 <div class="cols">
  <div class="box"><h3>食べたい<span>ご当地グルメ</span></h3><div class="food">
   <div><i>🐡</i><span><b>ふく（ふぐ）料理</b><small>下関・唐戸市場の朝寿司（D8）</small></span></div>
   <div><i>🍵</i><span><b>瓦そば</b><small>熱した瓦の上で茶そば（D7〜8）</small></span></div>
   <div><i>🍣</i><span><b>岩国寿司</b><small>殿様に献上した押し寿司（D3）</small></span></div>
   <div><i>🍊</i><span><b>夏みかんスイーツ</b><small>萩の名産（D4〜5）</small></span></div>
   <div><i>🦪</i><span><b>牡蠣・お好み焼き</b><small>宮島・広島（D1〜2）</small></span></div>
   <div><i>🍛</i><span><b>焼きカレー</b><small>門司港名物（D8）</small></span></div>
   <div><i>🍜</i><span><b>博多ラーメン・もつ鍋</b><small>屋台でシメ（D9〜10）</small></span></div>
  </div></div>
  <div class="box"><h3>効率よく回る<span>コツ</span></h3><ul class="tips">
   <li data-n="1">レンタカーは広島で借りて下関で返却<small>乗り捨て料金はかかるが、往復するより時間を節約</small></li>
   <li data-n="2">萩は連泊してゆっくり<small>荷ほどき1回で2日観光。萩市内は自転車が便利</small></li>
   <li data-n="3">絶景の日（D7）は晴れ予報に合わせる<small>角島・元乃隅は青空で映える。雨なら秋芳洞の日と入替え</small></li>
   <li data-n="4">関門海峡は歩いて渡れる<small>海底の人道トンネル約780m・15分で本州→九州</small></li>
   <li data-n="5">宿は早めに予約<small>長門湯本・萩・宮島は人気で埋まりやすい</small></li>
  </ul></div>
  <div class="box"><h3>日数が<span>余ったら</span></h3><ul class="tips">
   <li data-n="A">出雲大社・石見銀山（島根）<small>津和野から北上 +2日。縁結びの聖地と世界遺産</small></li>
   <li data-n="B">別府・湯布院（大分）<small>小倉から特急で約1h20、温泉三昧 +1〜2日</small></li>
   <li data-n="C">周防大島<small>瀬戸内のハワイ。錦帯橋から車で約1h</small></li>
   <li data-n="D">SLやまぐち号<small>新山口〜津和野を走る蒸気機関車（運行日要確認）</small></li>
   <li data-n="E">電車派なら<small>新山口駅を拠点にバス利用。ただし角島・元乃隅は車推奨</small></li>
  </ul></div>
 </div>
</section>
</body></html>'''
open(OUT,'w').write(html)
print(DW,DH,JW,JH,len(html))
