import sys, random
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 900
random.seed(7)

def defs():
    return '''<defs>
<radialGradient id="glow"><stop offset="0" stop-color="#FFB347" stop-opacity=".75"/><stop offset="1" stop-color="#FFB347" stop-opacity="0"/></radialGradient>
<radialGradient id="glowR"><stop offset="0" stop-color="#FF5A3C" stop-opacity=".7"/><stop offset="1" stop-color="#FF5A3C" stop-opacity="0"/></radialGradient>
<linearGradient id="lan" x1="0" x2="1"><stop offset="0" stop-color="#8E1F18"/><stop offset=".45" stop-color="#E8432F"/><stop offset="1" stop-color="#7A1A14"/></linearGradient>
<linearGradient id="vig" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".3" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .18 0"/></filter>
</defs>'''

def lantern(x, y, s=1, text="酒"):
    return f'''<g transform="translate({x},{y}) scale({s})">
<circle r="120" fill="url(#glowR)"/>
<rect x="-6" y="-70" width="12" height="14" fill="#2A1A12"/>
<ellipse cx="0" cy="0" rx="46" ry="58" fill="url(#lan)"/>
{''.join(f'<path d="M-44 {yy} Q0 {yy+6} 44 {yy}" stroke="#6A140F" stroke-width="1.5" fill="none" opacity=".6"/>' for yy in range(-40,50,12))}
<rect x="-26" y="-60" width="52" height="8" rx="2" fill="#1A1210"/>
<rect x="-26" y="52" width="52" height="8" rx="2" fill="#1A1210"/>
<text y="16" text-anchor="middle" font-family="Shippori Mincho" font-weight="800" font-size="44" fill="#1A0D0A">{text}</text>
</g>'''

def steam(x, y, n=3, h=120, sp=26, op=.35):
    out = []
    for i in range(n):
        xx = x + (i-(n-1)/2)*sp
        out.append(f'<path d="M{xx} {y} c-18 -{h*.2} 18 -{h*.4} 0 -{h*.6} s18 -{h*.3} 0 -{h*.4}" stroke="#fff" stroke-width="10" stroke-linecap="round" fill="none" opacity="{op}" filter="url(#soft)"/>')
    return ''.join(out)

def badge(no, title, sub):
    return f'''<g transform="translate(48,{H-170})">
<rect width="560" height="122" rx="4" fill="#14131A" opacity=".82"/>
<rect x="6" y="6" width="548" height="110" rx="2" fill="none" stroke="#C9A24B" stroke-width="1.5"/>
<text x="28" y="44" font-family="Zen Kaku Gothic New" font-weight="700" font-size="20" fill="#C9A24B" letter-spacing="4">東京秘境めし ── 其の{no}</text>
<text x="28" y="94" font-family="Shippori Mincho" font-weight="800" font-size="40" fill="#EFE6D2">{title}</text>
</g>
<text x="{W-48}" y="{H-48}" text-anchor="end" font-family="Zen Kaku Gothic New" font-size="22" fill="#EFE6D2" opacity=".85" letter-spacing="2">{sub}</text>'''

def finish():
    return f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" filter="url(#grain)"/>'

# ---------- 1. 路地裏横丁 ----------
def yokocho():
    s = [f'<rect width="{W}" height="{H}" fill="#0F0E16"/>']
    # sky strip
    s.append('<path d="M470 0 L730 0 L680 300 L520 300 Z" fill="#1E2340"/>')
    for _ in range(18):
        s.append(f'<circle cx="{random.randint(500,700)}" cy="{random.randint(10,200)}" r="{random.choice([1,1.5,2])}" fill="#fff" opacity=".6"/>')
    # buildings left/right perspective
    s.append('<path d="M0 0 L470 0 L520 300 L520 640 L0 900 Z" fill="#2B2230"/>')
    s.append('<path d="M1200 0 L730 0 L680 300 L680 640 L1200 900 Z" fill="#251E2A"/>')
    # alley floor
    s.append('<path d="M0 900 L520 640 L680 640 L1200 900 Z" fill="#1A1517"/>')
    s.append('<path d="M520 640 L680 640 L760 900 L440 900 Z" fill="#3A2A22" opacity=".5"/>')
    # wet reflections
    for x in (560, 610, 640):
        s.append(f'<rect x="{x}" y="680" width="8" height="200" fill="#FF6A3C" opacity=".12" filter="url(#blur)"/>')
    # wires
    s.append('<path d="M470 40 Q600 120 730 30 M470 90 Q600 160 730 80" stroke="#0A0A0A" stroke-width="3" fill="none"/>')
    # shop fronts left
    for i,(x,y,w,h) in enumerate([(60,330,330,330),(400,350,110,250)]):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFB25C" opacity=".85"/>')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glow)" opacity=".5"/>')
    # noren
    for k in range(4):
        s.append(f'<rect x="{80+k*76}" y="330" width="70" height="120" fill="#1F2A44"/>')
    s.append('<text x="225" y="410" text-anchor="middle" font-family="Shippori Mincho" font-weight="800" font-size="60" fill="#EFE6D2">やき鳥</text>')
    # silhouettes customers
    for x in (110,190,280):
        s.append(f'<circle cx="{x}" cy="520" r="30" fill="#1A1210"/><path d="M{x-45} 660 Q{x} 540 {x+45} 660 Z" fill="#1A1210"/>')
    # counter
    s.append('<rect x="60" y="600" width="330" height="60" fill="#3B2416"/>')
    # right side shop
    s.append('<rect x="700" y="340" width="110" height="260" fill="#FFCF7A" opacity=".8"/>')
    s.append('<rect x="820" y="320" width="330" height="340" fill="#E8A24A" opacity=".9"/>')
    s.append('<rect x="820" y="320" width="330" height="70" fill="#B5382E"/>')
    s.append('<text x="985" y="372" text-anchor="middle" font-family="Shippori Mincho" font-weight="800" font-size="46" fill="#EFE6D2">もつ煮 酒場</text>')
    for k in range(5):
        s.append(f'<rect x="{830+k*64}" y="400" width="56" height="190" fill="none" stroke="#5A3418" stroke-width="5"/>')
    # smoke from grill
    s.append(steam(225, 330, 4, 260, 40, .22))
    # lanterns
    for (x,y,sc,t) in [(150,250,1.1,"酒"),(330,240,1,"串"),(470,300,.6,"呑"),(735,300,.6,"処"),(870,240,1,"酒"),(1060,250,1.1,"肴")]:
        s.append(lantern(x,y,sc,t))
    # vertical signboards
    s.append('<rect x="540" y="200" width="36" height="150" fill="#EFE6D2"/><text x="558" y="232" font-family="Shippori Mincho" font-weight="800" font-size="28" fill="#B5382E" text-anchor="middle" writing-mode="tb">立呑</text>')
    s.append('<rect x="628" y="210" width="32" height="130" fill="#C9A24B"/><text x="644" y="238" font-family="Shippori Mincho" font-weight="800" font-size="24" fill="#14131A" text-anchor="middle" writing-mode="tb">珈琲</text>')
    s.append(finish())
    s.append(badge("一","路地裏の赤提灯横丁","肩寄せ合う、七席だけの焼き鳥屋"))
    return ''.join(s)

# ---------- 2. 屋台おでん ----------
def oden():
    s = [f'<rect width="{W}" height="{H}" fill="#120F17"/>']
    s.append(f'<ellipse cx="600" cy="420" rx="700" ry="420" fill="url(#glow)" opacity=".55"/>')
    # stall roof & noren
    s.append('<path d="M60 70 L1140 70 L1100 150 L100 150 Z" fill="#3A2418"/>')
    for k in range(9):
        s.append(f'<rect x="{110+k*110}" y="150" width="104" height="150" fill="#EFE6D2"/>')
    s.append('<text x="600" y="255" text-anchor="middle" font-family="Shippori Mincho" font-weight="800" font-size="92" fill="#14131A" letter-spacing="40">おでん</text>')
    # pot
    s.append('<rect x="150" y="430" width="900" height="420" rx="16" fill="#8A8F96"/>')
    s.append('<rect x="170" y="450" width="860" height="380" rx="10" fill="#7A4A1E"/>')
    s.append('<rect x="170" y="450" width="860" height="380" rx="10" fill="url(#glow)" opacity=".35"/>')
    s.append('<path d="M450 450 V830 M750 450 V830 M170 640 H1030" stroke="#9EA3A9" stroke-width="10"/>')
    # daikon
    for (x,y) in [(250,520),(350,560),(270,610)]:
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="62" ry="40" fill="#E2B877"/><ellipse cx="{x}" cy="{y-6}" rx="50" ry="28" fill="#F0CF94"/>')
    # eggs
    for (x,y) in [(540,520),(650,560),(580,600)]:
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="44" ry="34" fill="#B97A3A"/><ellipse cx="{x-12}" cy="{y-10}" rx="14" ry="8" fill="#E6B276" opacity=".7"/>')
    # konnyaku triangles
    for (x,y) in [(830,500),(930,560),(860,600)]:
        s.append(f'<path d="M{x-50} {y+30} L{x} {y-40} L{x+50} {y+30} Z" fill="#5B4D48"/>')
        for d in range(5): s.append(f'<circle cx="{x-20+d*10}" cy="{y+d%2*12}" r="2.5" fill="#3A302C"/>')
    # chikuwa
    for (x,y) in [(230,730),(330,770)]:
        s.append(f'<rect x="{x-70}" y="{y-24}" width="140" height="48" rx="24" fill="#C98A44"/><ellipse cx="{x+70}" cy="{y}" rx="12" ry="22" fill="#F2E3C2"/><ellipse cx="{x+70}" cy="{y}" rx="5" ry="10" fill="#7A4A1E"/>')
    # ganmo / atsuage
    for (x,y) in [(560,740),(660,760)]:
        s.append(f'<rect x="{x-55}" y="{y-35}" width="110" height="70" rx="10" fill="#B0702E"/><rect x="{x-45}" y="{y-28}" width="90" height="10" fill="#D6964C" opacity=".6"/>')
    # skewers (gyusuji)
    for (x,y) in [(850,720),(940,760)]:
        s.append(f'<line x1="{x-80}" y1="{y+40}" x2="{x+80}" y2="{y-70}" stroke="#E9D3A4" stroke-width="6"/>')
        for k in range(3): s.append(f'<ellipse cx="{x-40+k*40}" cy="{y+12-k*28}" rx="28" ry="20" fill="#6E3A1E"/>')
    s.append(steam(400, 470, 3, 260, 60, .28)); s.append(steam(800, 470, 3, 260, 60, .28))
    # karashi dish
    s.append('<ellipse cx="1110" cy="560" rx="70" ry="22" fill="#EFE6D2"/><ellipse cx="1110" cy="555" rx="22" ry="8" fill="#E2B52B"/>')
    s.append(lantern(70,330,.9,"お"))
    s.append(lantern(1130,330,.9,"燗"))
    s.append(finish())
    s.append(badge("二","高架下、屋台のおでん","電車の音を肴に、熱燗一本"))
    return ''.join(s)

# ---------- 3. 純喫茶ナポリタン ----------
def kissa():
    s = [f'<rect width="{W}" height="{H}" fill="#2A1A14"/>']
    # wall & stained glass lamp
    s.append('<rect width="1200" height="330" fill="#3B241A"/>')
    for k in range(12): s.append(f'<rect x="{k*100}" y="0" width="6" height="330" fill="#2A1710"/>')
    s.append('<circle cx="600" cy="120" r="300" fill="url(#glow)" opacity=".7"/>')
    s.append('<path d="M480 40 L720 40 L780 170 L420 170 Z" fill="#C9A24B"/>')
    for i,c in enumerate(["#B5382E","#2F6B4F","#E6C77A","#1F2A44","#B5382E","#2F6B4F"]):
        s.append(f'<path d="M{430+i*60} 165 L{490+i*60} 165 L{480+i*55} 60 L{470+i*50} 60 Z" fill="{c}" opacity=".85"/>')
    s.append('<line x1="600" y1="0" x2="600" y2="40" stroke="#1A0F0A" stroke-width="5"/>')
    # table (marble-ish)
    s.append('<path d="M0 330 H1200 V900 H0 Z" fill="#E9E1D2"/>')
    for k in range(6): s.append(f'<path d="M{k*220-50} 330 q120 200 260 570" stroke="#CFC4B0" stroke-width="3" fill="none" opacity=".7"/>')
    # plate + napolitan
    s.append('<ellipse cx="470" cy="630" rx="330" ry="190" fill="#B9B3A3" opacity=".5" transform="translate(12 18)"/>')
    s.append('<ellipse cx="470" cy="620" rx="330" ry="190" fill="#F7F3EA"/>')
    s.append('<ellipse cx="470" cy="620" rx="270" ry="150" fill="none" stroke="#1F2A44" stroke-width="4" opacity=".5"/>')
    s.append('<ellipse cx="470" cy="610" rx="220" ry="118" fill="#D6542A"/>')
    for _ in range(70):
        x = random.randint(280,660); y = random.randint(520,700)
        s.append(f'<path d="M{x} {y} q{random.randint(-50,50)} {random.randint(-30,30)} {random.randint(-80,80)} {random.randint(-20,20)}" stroke="{random.choice(["#E8743A","#F08A4B","#C4461F"])}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    for _ in range(10):
        x = random.randint(330,610); y = random.randint(540,680)
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="8" fill="#3E7A3A"/>')
    for _ in range(8):
        x = random.randint(330,610); y = random.randint(540,680)
        s.append(f'<circle cx="{x}" cy="{y}" r="16" fill="#D99C9A" stroke="#B8706E" stroke-width="3"/>')
    for _ in range(6):
        x = random.randint(330,610); y = random.randint(540,680)
        s.append(f'<path d="M{x} {y} a22 14 0 0 1 44 0" stroke="#F3EBD8" stroke-width="6" fill="none"/>')
    s.append('<line x1="700" y1="760" x2="860" y2="520" stroke="#C9C9C9" stroke-width="8" stroke-linecap="round"/>')
    # cream soda
    s.append('<path d="M890 330 L1090 330 L1060 780 L920 780 Z" fill="#2FB36A" opacity=".85"/>')
    for _ in range(25): s.append(f'<circle cx="{random.randint(930,1050)}" cy="{random.randint(420,760)}" r="{random.randint(3,8)}" fill="#fff" opacity=".45"/>')
    s.append('<path d="M890 330 L1090 330 L1060 780 L920 780 Z" fill="none" stroke="#fff" stroke-width="4" opacity=".6"/>')
    s.append('<ellipse cx="990" cy="320" rx="95" ry="60" fill="#FFF7E4"/><ellipse cx="960" cy="300" rx="40" ry="20" fill="#fff"/>')
    s.append('<circle cx="1030" cy="265" r="22" fill="#C8102E"/><path d="M1030 245 q10 -40 40 -60" stroke="#3E7A3A" stroke-width="4" fill="none"/>')
    s.append('<line x1="1050" y1="330" x2="1120" y2="120" stroke="#E04A6B" stroke-width="10" stroke-linecap="round"/>')
    s.append('<rect x="905" y="780" width="170" height="20" rx="6" fill="#DCD3C0"/>')
    s.append(finish())
    s.append(badge("三","昭和から続く純喫茶","鉄板じゃないナポリタンと、メロンのソーダ水"))
    return ''.join(s)

# ---------- 4. 町中華ラーメン ----------
def chuka():
    s = [f'<rect width="{W}" height="{H}" fill="#7A1E18"/>']
    # red counter top with subtle pattern
    for k in range(0,1200,60): s.append(f'<rect x="{k}" y="0" width="30" height="900" fill="#8A241C" opacity=".5"/>')
    # bowl
    s.append('<circle cx="560" cy="460" r="360" fill="#000" opacity=".25" transform="translate(16 20)"/>')
    s.append('<circle cx="560" cy="460" r="360" fill="#F4EFE4"/>')
    # raimon border
    s.append('<circle cx="560" cy="460" r="340" fill="none" stroke="#B5382E" stroke-width="22" stroke-dasharray="30 10"/>')
    s.append('<circle cx="560" cy="460" r="300" fill="#8A4A1C"/>')
    s.append('<circle cx="560" cy="460" r="300" fill="url(#glow)" opacity=".4"/>')
    # oil droplets
    for _ in range(40): s.append(f'<circle cx="{random.randint(300,820)}" cy="{random.randint(200,720)}" r="{random.randint(3,10)}" fill="#E8B060" opacity=".55"/>')
    # noodles
    for _ in range(28):
        x = random.randint(380,700); y = random.randint(380,600)
        s.append(f'<path d="M{x} {y} q30 -20 60 0 t60 0 t60 0" stroke="#E9CC6A" stroke-width="7" fill="none" opacity=".9"/>')
    # chashu
    for (x,y,r) in [(420,330,80),(530,300,78)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#B56E4A"/><circle cx="{x}" cy="{y}" r="{r-14}" fill="#E7B595"/><circle cx="{x+8}" cy="{y+6}" r="{r-40}" fill="#C98261"/>')
    # naruto
    s.append('<circle cx="700" cy="380" r="56" fill="#FFF"/><path d="M700 380 m-6 0 a6 6 0 1 1 12 0 a14 14 0 1 1 -28 0 a24 24 0 1 1 48 0 a34 34 0 1 1 -68 0" stroke="#E0457B" stroke-width="7" fill="none"/>')
    # menma
    for (x,y,a) in [(390,560,20),(420,600,-10),(450,570,35),(470,620,5)]:
        s.append(f'<rect x="{x}" y="{y}" width="70" height="20" rx="6" fill="#C29447" transform="rotate({a} {x} {y})"/>')
    # nori
    s.append('<rect x="640" y="470" width="130" height="170" fill="#1E2A1E" transform="rotate(12 700 560)"/>')
    # negi
    for _ in range(22):
        x = random.randint(560,680); y = random.randint(520,660)
        s.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#6FA34B" stroke="#C9E39A" stroke-width="3"/>')
    s.append(steam(560, 200, 4, 220, 70, .25))
    # renge & gyoza plate
    s.append('<path d="M940 760 q60 -40 120 0 q-20 60 -120 0 z" fill="#F4EFE4"/><rect x="1000" y="640" width="24" height="120" rx="10" fill="#F4EFE4" transform="rotate(30 1012 700)"/>')
    s.append('<ellipse cx="1000" cy="250" rx="170" ry="110" fill="#F4EFE4"/>')
    for k in range(5):
        s.append(f'<path d="M{880+k*50} 290 q20 -110 50 0 z" fill="#E2B877" stroke="#B57A3A" stroke-width="3"/><path d="M{880+k*50} 290 l50 0" stroke="#8A4A1C" stroke-width="10"/>')
    s.append(finish())
    s.append(badge("四","商店街の奥の町中華","醤油ラーメンと焼き餃子、迷わずセットで"))
    return ''.join(s)

# ---------- 5. 甘味処あんみつ ----------
def kanmi():
    s = [f'<rect width="{W}" height="{H}" fill="#3A2A22"/>']
    # engawa / tatami
    s.append('<rect y="0" width="1200" height="300" fill="#1E2A22"/>')
    for _ in range(60):
        x=random.randint(0,1200); y=random.randint(0,290); r=random.randint(20,60)
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{random.choice(["#2F4A33","#3E5E3A","#26402C"])}" opacity=".8"/>')
    for _ in range(14):
        x=random.randint(0,1200); y=random.randint(10,280)
        s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#E9A3B4"/>')
    for k in range(0,1200,200): s.append(f'<rect x="{k}" y="0" width="14" height="300" fill="#2A1A12"/>')
    s.append('<rect y="290" width="1200" height="20" fill="#2A1A12"/>')
    s.append('<rect y="310" width="1200" height="590" fill="#C8B07A"/>')
    for k in range(310,900,14): s.append(f'<line x1="0" y1="{k}" x2="1200" y2="{k}" stroke="#B39A64" stroke-width="2"/>')
    # tray
    s.append('<rect x="160" y="380" width="880" height="460" rx="20" fill="#14131A"/>')
    s.append('<rect x="176" y="396" width="848" height="428" rx="14" fill="none" stroke="#B5382E" stroke-width="4"/>')
    # anmitsu bowl (glass)
    s.append('<ellipse cx="460" cy="620" rx="230" ry="150" fill="#DCE8EE" opacity=".6"/>')
    s.append('<ellipse cx="460" cy="600" rx="200" ry="120" fill="#7FA8B8" opacity=".35"/>')
    # kanten cubes
    for _ in range(14):
        x=random.randint(320,580); y=random.randint(540,670)
        s.append(f'<rect x="{x}" y="{y}" width="34" height="34" fill="#F4F8FA" opacity=".8" stroke="#BCD0DA"/>')
    s.append('<ellipse cx="400" cy="560" rx="80" ry="55" fill="#3B1E1E"/><ellipse cx="385" cy="545" rx="30" ry="14" fill="#5A2E2E"/>')  # anko
    s.append('<ellipse cx="520" cy="560" rx="62" ry="50" fill="#FFF7E4"/>')  # icecream
    for (x,y,c) in [(560,640,"#F2E5D0"),(600,610,"#F2E5D0"),(330,640,"#F6C9D6"),(360,670,"#B8DDA0"),(440,660,"#FFFFFF")]:
        s.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{c}" stroke="#D8C8B0"/>')  # shiratama
    s.append('<path d="M470 520 q20 -30 50 -10 q-10 30 -50 10 z" fill="#E9A23B"/>')  # mikan
    s.append('<circle cx="600" cy="560" r="18" fill="#C8102E"/>')
    # kuromitsu pitcher
    s.append('<path d="M720 520 q-10 80 30 110 h60 q40 -30 30 -110 z" fill="#EFE6D2"/><path d="M820 540 q40 0 30 40" stroke="#EFE6D2" stroke-width="10" fill="none"/>')
    s.append('<ellipse cx="780" cy="522" rx="60" ry="10" fill="#2A1208"/>')
    # tea cup
    s.append('<path d="M840 680 h150 l-20 110 h-110 z" fill="#3E5E3A"/><ellipse cx="915" cy="680" rx="75" ry="16" fill="#9CB86A"/>')
    s.append(steam(915, 660, 2, 160, 40, .25))
    s.append(finish())
    s.append(badge("五","谷中の路地、縁側の甘味処","黒蜜たっぷりのクリームあんみつ"))
    return ''.join(s)

scenes = [("01_yokocho", yokocho), ("02_oden", oden), ("03_kissa", kissa), ("04_machichuka", chuka), ("05_kanmi", kanmi)]
FONT = '<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@800&family=Zen+Kaku+Gothic+New:wght@400;700&display=swap" rel="stylesheet">'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
    for name, fn in scenes:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}{fn()}</svg>'
        pg.set_content(f'<html><head>{FONT}<style>body{{margin:0}}</style></head><body>{svg}</body></html>')
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=88)
        print("ok", name)
    b.close()
