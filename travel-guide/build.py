# 5県旅カタログ生成スクリプト
# 使い方: python3 build.py <spots.tsv> <wiki.json> <japan.geojson> <画像フォルダ>
import csv, json, math, sys, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
TSV, WIKI, GEO, IMGDIR = sys.argv[1:5]

PREFS = {
    'fk': ('福岡', '福岡県', '#2F6DB5'),
    'hs': ('広島', '広島県', '#8A4FB8'),
    'yg': ('山口', '山口県', '#D2462E'),
    'sm': ('島根', '島根県', '#2E8B57'),
    'tt': ('鳥取', '鳥取県', '#C27A0E'),
}
CATS = ['絶景', '歴史', '街歩き', '温泉', 'グルメ']

# グルメ（料理）は場所の座標がないので、食べられる町に置く
FOOD_AT = {
    '博多ラーメン': (130.42, 33.59), 'もつ鍋': (130.42, 33.59), '水炊き': (130.42, 33.59), '明太子': (130.42, 33.59),
    '焼きカレー': (130.962, 33.945),
    '広島風お好み焼き': (132.46, 34.39), '汁なし担担麺': (132.46, 34.39),
    'カキ (貝類)': (132.31, 34.31), 'あなごめし': (132.31, 34.31), 'もみじ饅頭': (132.31, 34.31),
    '尾道ラーメン': (133.20, 34.41),
    'フグ料理': (130.94, 33.96), '瓦そば': (130.955, 34.156), '岩国寿司': (132.18, 34.17),
    'ナツミカン': (131.40, 34.41), '外郎': (131.47, 34.18),
    '出雲そば': (132.69, 35.40), 'ぜんざい': (132.69, 35.40), '宍道湖七珍': (133.05, 35.47), 'アカムツ': (132.08, 34.90),
    'ズワイガニ': (133.23, 35.54), '境港市': (133.23, 35.54), '二十世紀 (ナシ)': (134.24, 35.50),
    'ラッキョウ': (134.24, 35.50), '牛骨ラーメン': (133.33, 35.43),
}
# 観光地の座標（経度, 緯度）。Wikipediaから座標が取れないものが多いため手で指定
COORD = {
 '太宰府天満宮':(130.5348,33.5215),'柳川市':(130.406,33.163),'門司港レトロ':(130.962,33.945),'小倉城':(130.874,33.884),
 '皿倉山':(130.808,33.850),'河内藤園':(130.796,33.832),'糸島市':(130.157,33.645),'宗像大社':(130.517,33.831),
 '櫛田神社 (福岡市)':(130.410,33.593),'福岡タワー':(130.351,33.593),'大濠公園':(130.376,33.586),'二日市温泉':(130.523,33.500),
 '能古島':(130.304,33.631),
 '原爆ドーム':(132.4536,34.3955),'広島平和記念資料館':(132.452,34.392),'厳島神社':(132.320,34.296),'弥山 (廿日市市)':(132.319,34.279),
 '広島城':(132.459,34.403),'縮景園':(132.467,34.400),'尾道市':(133.198,34.409),'西瀬戸自動車道':(133.17,34.29),
 '大久野島':(132.991,34.310),'鞆の浦':(133.383,34.383),'竹原市':(132.917,34.344),'呉市海事歴史科学館':(132.555,34.241),
 '三段峡':(132.215,34.640),'帝釈峡':(133.232,34.858),
 '角島大橋':(130.887,34.346),'元乃隅神社':(131.032,34.418),'秋芳洞':(131.302,34.228),'秋吉台':(131.307,34.250),
 '青海島':(131.205,34.432),'別府弁天池':(131.262,34.212),'錦帯橋':(132.178,34.168),'瑠璃光寺':(131.474,34.190),
 '松下村塾':(131.414,34.405),'萩城':(131.385,34.418),'赤間神宮':(130.949,33.962),'唐戸市場':(130.944,33.957),
 '関門トンネル':(130.960,33.966),'長門湯本温泉':(131.183,34.322),'湯田温泉':(131.458,34.163),'周防大島':(132.25,33.93),
 '出雲大社':(132.6855,35.4017),'稲佐の浜':(132.676,35.393),'出雲日御碕灯台':(132.629,35.433),'松江城':(133.0505,35.4752),
 '堀川遊覧船':(133.056,35.478),'宍道湖':(133.040,35.462),'足立美術館':(133.196,35.381),'石見銀山':(132.437,35.105),
 '津和野町':(131.773,34.467),'太皷谷稲成神社':(131.766,34.472),'八重垣神社':(133.073,35.441),'美保神社':(133.319,35.564),
 '玉造温泉':(133.012,35.420),'温泉津温泉':(132.343,35.088),'隠岐諸島':(133.25,36.20),
 '鳥取砂丘':(134.228,35.540),'砂の美術館':(134.236,35.533),'浦富海岸':(134.31,35.59),'白兎神社':(134.080,35.522),
 '三徳山三佛寺':(133.959,35.402),'三朝温泉':(133.862,35.410),'皆生温泉':(133.360,35.450),'大山 (鳥取県)':(133.546,35.371),
 '大山寺':(133.533,35.391),'水木しげるロード':(133.234,35.542),'植田正治写真美術館':(133.452,35.376),'白壁土蔵群':(133.825,35.430),
 '青山剛昌ふるさと館':(133.693,35.493),'とっとり花回廊':(133.392,35.363),'仁風閣':(134.240,35.509),
}

rows = list(csv.reader(open(TSV, encoding='utf-8'), delimiter='\t'))
wiki = json.load(open(WIKI, encoding='utf-8'))

def strip_tags(s):
    import re
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()

spots = []
for i, (pref, cat, name, wt, desc, extra) in enumerate(rows):
    w = wiki.get(wt) or {}
    sid = f'{pref}{i:02d}'
    if cat == 'グルメ':
        lonlat = FOOD_AT.get(wt)
    else:
        lonlat = COORD.get(wt) or FOOD_AT.get(wt)
    if not lonlat:
        print('NO COORD', name, file=sys.stderr)
        continue
    img = None
    if os.path.exists(os.path.join(IMGDIR, sid + '.jpg')):
        img = f'img/{sid}.jpg'
    lic = w.get('lic') or {}
    spots.append({
        'id': sid, 'pref': pref, 'cat': cat, 'name': name, 'desc': desc,
        'time' if cat != 'グルメ' else 'where': extra,
        'lon': round(lonlat[0], 4), 'lat': round(lonlat[1], 4),
        'img': img,
        'credit': strip_tags(lic.get('artist'))[:60] if img else '',
        'license': lic.get('license', '') if img else '',
        'file': ('https://commons.wikimedia.org/wiki/File:' + w['file']) if img and w.get('file') else '',
        'wiki': w.get('url') or '',
    })

# ---- 地図 ----
feats = json.load(open(GEO, encoding='utf-8'))['features']
B = (129.85, 134.65, 32.95, 36.42)
c = math.cos(math.radians((B[2] + B[3]) / 2))
K = 1000 / ((B[1] - B[0]) * c)
W, H = 1000, (B[3] - B[2]) * K
def proj(lon, lat):
    return ((lon - B[0]) * c * K, (B[3] - lat) * K)

prefname = {v[1]: k for k, v in PREFS.items()}
land, pbox = [], {}
for f in feats:
    n = f['properties']['nam_ja']
    g = f['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    d = []
    xs, ys = [], []
    for poly in polys:
        for ring in poly:
            lo = [p[0] for p in ring]; la = [p[1] for p in ring]
            if max(lo) < B[0] or min(lo) > B[1] or max(la) < B[2] or min(la) > B[3]:
                continue
            pts, last = [], None
            for lon, lat in ring:
                x, y = proj(lon, lat)
                if last is None or abs(x - last[0]) + abs(y - last[1]) >= 0.9:
                    pts.append((x, y)); last = (x, y)
            if len(pts) < 3:
                continue
            xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
            d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
    if not d:
        continue
    key = prefname.get(n)
    cls = f'land p-{key}' if key else 'land other'
    land.append(f'<path class="{cls}" d="{"".join(d)}"><title>{n}</title></path>')
    if key:
        # 隠岐を除いた本土の範囲で拡大する（島根のみ）
        pbox[key] = [min(xs), min(ys), max(xs), max(ys)]

# 島根は本土＋隠岐で広すぎるので、拡大範囲を手で指定
x0, y0 = proj(131.65, 35.65); x1, y1 = proj(133.45, 34.30)
pbox['sm'] = [x0, y0, x1, y1]

labels = []
for lon, lat, t in [(130.7, 33.38, '福岡県'), (132.75, 34.62, '広島県'), (131.55, 34.12, '山口県'),
                    (132.35, 35.0, '島根県'), (133.85, 35.33, '鳥取県')]:
    x, y = proj(lon, lat)
    labels.append(f'<text class="plabel" x="{x:.0f}" y="{y:.0f}">{t}</text>')
for lon, lat, t in [(131.4, 35.6, '日 本 海'), (132.1, 33.75, '瀬 戸 内 海'), (130.2, 34.2, '響 灘')]:
    x, y = proj(lon, lat)
    labels.append(f'<text class="slabel" x="{x:.0f}" y="{y:.0f}">{t}</text>')

for s in spots:
    x, y = proj(s['lon'], s['lat'])
    s['x'] = round(x, 1); s['y'] = round(y, 1)

# 同じ町に重なるグルメを少しずらす
from collections import defaultdict
groups = defaultdict(list)
for s in spots:
    groups[(round(s['x']), round(s['y']))].append(s)
for g in groups.values():
    if len(g) > 1:
        for j, s in enumerate(g):
            a = 2 * math.pi * j / len(g)
            s['x'] = round(s['x'] + 7 * math.cos(a), 1); s['y'] = round(s['y'] + 7 * math.sin(a), 1)

mapsvg = (f'<svg id="map" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="福岡・広島・山口・島根・鳥取の地図">'
          f'<rect class="sea" x="-500" y="-500" width="{W+1000:.0f}" height="{H+1000:.0f}"/>'
          + ''.join(land) + ''.join(labels) + '<g id="pins"></g></svg>')

data = {'spots': spots, 'prefs': {k: {'short': v[0], 'name': v[1], 'color': v[2], 'box': [round(t, 1) for t in pbox[k]]} for k, v in PREFS.items()},
        'cats': CATS, 'full': [0, 0, round(W), round(H)]}
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('<!--MAP-->', mapsvg).replace('/*DATA*/null', json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('spots', len(spots), 'with photo', sum(1 for s in spots if s['img']), 'size', len(out))
