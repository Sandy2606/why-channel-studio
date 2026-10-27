# ---------------- scene graphics (Short 2: why gold never rusts) ----------------
@functools.lru_cache(8)
def _still(name): return Image.open(G + 'media/' + name).convert('RGB')
def still_bg(img, name, v, t0, t1, dim, focus, zoom):
    s = _still(name); u = e_io(prog(v, t0, t1 + .5)); z = zoom[0] + (zoom[1] - zoom[0]) * u
    sc = max(W / s.width, H / s.height) * z; cw, ch = W / sc, H / sc
    x0 = (s.width - cw) * focus[0]; y0 = (s.height - ch) * focus[1]
    img.paste(s.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)), (0, 0))
    if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))

def shine_sweep(img, v, t0, dur=.9, a=.55):
    q = prog(v, t0, t0 + dur)
    if q <= 0 or q >= 1: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x = -400 + (W + 800) * e_io(q)
    d.polygon([(x - 90, 0), (x + 90, 0), (x - 330, H), (x - 510, H)], fill=(255, 245, 210, int(255 * a * math.sin(math.pi * q))))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(40)))

def o2(img, x, y, ang=0.0, a=1.0, sep=0.0, s=1.0):
    r = int(24 * s); dx = (r * .8 + sep) * math.cos(ang); dy = (r * .8 + sep) * math.sin(ang)
    put(img, sphere(r, (230, 70, 60)), x - dx, y - dy, a); put(img, sphere(r, (230, 70, 60)), x + dx, y + dy, a)

def g_hook(img, v, t0, t1):
    ty = T['years']
    if v >= ty:
        k = e_out(prog(v, ty, ty + .8))
        big_text(img, f'{int(round(3300 * k)):,}', W / 2, 330, 170, AMBER, prog(v, ty, ty + .15), e_back(prog(v, ty, ty + .35)))
        mono(img, L('YEARS OLD · STILL SHINING', 'ఏళ్ళ వయసు · ఇంకా మెరుస్తోంది'), W / 2, 450, 30, CREAM, prog(v, ty + .3, ty + .6))
    shine_sweep(img, v, ty + 1.6, 1.0)

def g_rusty(img, v, t0, t1):
    mono(img, L('IRON · A FEW MONTHS OUTSIDE', 'ఐరన్ · కొన్ని నెలలు బయట'), W / 2, 330, 30, CREAM, prog(v, t0, t0 + .3))
    tr = T['rusty']
    if v >= tr: stamp_text(img, L('RUST', 'తుప్పు'), W / 2, 520, 130, (232, 110, 50), v, tr, rot=-6)

ORB = [(.0, -1), (.6, -1), (1.2, -1), (1.9, -1), (2.6, -1), (3.3, -1)]
def g_ironox(img, v, t0, t1):
    cx, cy, R = W / 2, 780, 210
    headline(img, L('RUST = OXYGEN EATING IRON', 'తుప్పు = ఆక్సిజన్ ఐరన్‌ని తినడం'), v, t0, W / 2, 360, 62 if not TE else 56, 1000)
    rk = e_io(prog(v, T['gives'] - .8, T['gives'] + .6))                       # rust spreading
    col = tuple(int(c0 * (1 - rk) + c1 * rk) for c0, c1 in zip((150, 152, 158), (178, 82, 36)))
    put(img, sphere(R, col), cx, cy); text_plain(img, 'Fe', cx, cy - 6, 96, WHITE, .9)
    mono(img, L('IRON', 'ఐరన్'), cx, cy + R + 40, 28, CREAM)
    rng = np.random.default_rng(5)
    for i in range(10):                                                         # O2 flies in and sticks
        st = t0 + .5 + i * .32; ang = rng.uniform(0, 2 * math.pi); q = e_out(prog(v, st, st + .45))
        if v < st: continue
        r0 = 700; r1 = R + 18; rr = r0 + (r1 - r0) * q; x, y = cx + rr * math.cos(ang), cy + rr * .9 * math.sin(ang)
        o2(img, x, y, ang + math.pi / 2, 1.0, s=.9)
    if v >= T['gives']:                                                         # flakes falling
        d = ImageDraw.Draw(img)
        for i in range(40):
            st = T['gives'] + rng.uniform(0, 1.2); q = prog(v, st, st + 1.4)
            if q <= 0 or q >= 1: continue
            x = cx + rng.uniform(-R * .8, R * .8); y = cy + R * .6 + 420 * q * q
            s = rng.uniform(5, 11); d.polygon([(x, y - s), (x + s, y), (x, y + s * .7), (x - s * .8, y)], fill=(176, 84, 40, int(255 * (1 - q))))
    if v >= t0 + .5: mono(img, L('O2 = OXYGEN', 'O2 = ఆక్సిజన్'), W / 2, 1080, 28, (240, 120, 110), prog(v, t0 + .5, t0 + .8))

def g_goldox(img, v, t0, t1):
    cx, cy, R = W / 2, 780, 170
    headline(img, L('GOLD HOLDS ITS ELECTRONS TIGHT', 'గోల్డ్ ఎలక్ట్రాన్స్‌ని గట్టిగా పట్టుకుంటుంది'), v, t0, W / 2, 360, 58 if not TE else 50, 1000)
    put(img, glow(320, (255, 190, 60), .6), cx, cy); put(img, sphere(R, GOLD), cx, cy); text_plain(img, 'Au', cx, cy - 6, 96, (40, 26, 6))
    d = ImageDraw.Draw(img); d.ellipse((cx - R - 40, cy - R - 40, cx + R + 40, cy + R + 40), outline=(255, 230, 160, 90), width=3)
    for j in range(4):                                                          # tight, fast electrons
        a = v * 5 + j * math.pi / 2; put(img, sphere(13, (150, 220, 255)), cx + (R + 40) * math.cos(a), cy + (R + 40) * math.sin(a))
    rng = np.random.default_rng(8)
    for i in range(9):                                                          # O2 bounces off
        st = t0 + .4 + i * .36; ang = rng.uniform(0, 2 * math.pi)
        if v < st: continue
        q = prog(v, st, st + 1.1); r1 = R + 70
        rr = 720 - (720 - r1) * e_out(q / .4) if q < .4 else r1 + 650 * e_io((q - .4) / .6)
        aa = ang if q < .4 else ang + .5
        if q < 1: o2(img, cx + rr * math.cos(aa), cy + rr * math.sin(aa), aa + math.pi / 2, min(1, (1 - q) * 3), s=.9)
    if v >= T['cant']:
        pill(img, L('NO GRIP', 'పట్టు దొరకదు'), W / 2, 1060, 40, AMBER, (10, 10, 10), prog(v, T['cant'], T['cant'] + .25), e_back(prog(v, T['cant'], T['cant'] + .3)))

def g_proof(img, v, t0, t1):
    mono(img, L('HERE IS WHAT BLEW MY MIND', 'నాకు షాకింగ్ అనిపించింది'), W / 2, 330, 30, AMBER, prog(v, t0, t0 + .3))
    ty = T['year']
    if v >= ty - .1:
        big_text(img, '2026', W / 2, 560, 220, CREAM, prog(v, ty - .1, ty + .05), e_back(prog(v, ty - .1, ty + .25)))
    if v >= ty + .5:
        news_card(img, 'SCIENCEALERT', 'MAY 22, 2026', 'Scientists Found The Atomic Reason That Gold Refuses to Rust', W / 2, 900, v, ty + .5, w=940, hl_words=(6, 7, 8))
        mono(img, 'TULANE UNIVERSITY · PHYSICAL REVIEW LETTERS', W / 2, 1065, 22, GREY, prog(v, ty + .9, ty + 1.2))

HEX = None
def _hexpts():
    pts = []; r = 46; dx = 2 * r * .98; dy = dx * math.sqrt(3) / 2
    for row in range(-5, 6):
        for col in range(-6, 7):
            x = W / 2 + col * dx + (row % 2) * dx / 2; y = 760 + row * dy
            if 60 < x < W - 60 and 450 < y < 1090: pts.append((x, y))
    return pts, r
def g_hexa(img, v, t0, t1):
    headline(img, L("GOLD'S SURFACE: A TIGHT HEXAGON", 'గోల్డ్ ఉపరితలం: టైట్ హెక్సాగన్'), v, t0, W / 2, 340, 58 if not TE else 50, 1000)
    pts, r = _hexpts(); cx, cy = W / 2, 760
    for (x, y) in pts:
        dd = math.hypot(x - cx, y - cy); st = t0 + .2 + dd / 900
        if v < st: continue
        put(img, sphere(r, GOLD, .8), x, y, 1, e_back(prog(v, st, st + .3)))
    if v >= t0 + 1.2:                                                           # highlight one hexagon
        a = prog(v, t0 + 1.2, t0 + 1.5); d = ImageDraw.Draw(img); R = 2 * r * .98
        hx = [(cx + R * math.cos(math.radians(60 * k)), cy + R * math.sin(math.radians(60 * k))) for k in range(7)]
        d.line(hx, fill=AMBER + (int(255 * a),), width=7, joint='curve')
    ts = T['split']
    if v >= ts:                                                                 # O2 lands, tries to split, fails, leaves
        q = v - ts
        if q < .5: y = 200 + (cy - 70 - 200) * e_out(q / .5); sep = 0
        elif q < 2.0: y = cy - 70; sep = 22 * abs(math.sin((q - .5) * 7)) * (1 - (q - .5) / 1.5)
        else: y = cy - 70 - 700 * e_io(min(1, (q - 2.0) / .8)); sep = 0
        if q < 2.8: o2(img, cx, y, 0, 1.0, sep=sep, s=1.2)
        if q > .6: pill(img, L("O2 CAN'T SPLIT", 'O2 విడిపోలేదు'), W / 2, 1100, 38, (230, 70, 60), WHITE, prog(v, ts + .6, ts + .85))

def g_aqua(img, v, t0, t1):
    ta, tr, tc = T['aqua'], T['royal'], T['acids']
    if v >= ta: pill(img, 'AQUA REGIA', W / 2, 380, 52, AMBER, (10, 10, 10), prog(v, ta, ta + .25), e_back(prog(v, ta, ta + .3)))
    if v >= tr: mono(img, L('= "ROYAL WATER"', '= "రాజ ద్రవం"'), W / 2, 470, 34, CREAM, prog(v, tr, tr + .3))
    if v >= tc:
        for i, (txt, ti) in enumerate([('NITRIC ACID', tc), ('HYDROCHLORIC ACID', tc + .45)]):
            if v < ti: continue
            k = e_back(prog(v, ti, ti + .3)); y = 680 + i * 170
            pill(img, txt, W / 2 + 60 * (1 - k), y, 40, (14, 14, 14, 230), CREAM, prog(v, ti, ti + .2))
            if i == 1: text_plain(img, '+', W / 2, 765, 70, AMBER, prog(v, ti, ti + .2))

def g_fav(img, v, t0, t1):
    sc = 1 + .05 * prog(v, t0, t1)
    big_text(img, L('MY FAVOURITE\nPART', 'నాకు బాగా నచ్చిన\nస్టోరీ'), W / 2, 820, int(120 * sc) if not TE else int(130 * sc), CREAM, prog(v, t0, t0 + .3))

def g_1940(img, v, t0, t1):
    stamp_text(img, '1940', W / 2, 520, 200, AMBER, v, t0 + .1, rot=-5)
    tn = t0 + .9
    if v >= tn:
        pill(img, L('NAZIS INVADE DENMARK', 'నాజీలు డెన్మార్క్‌పై దాడి'), W / 2, 760, 44, (230, 70, 60), WHITE, prog(v, tn, tn + .25), e_back(prog(v, tn, tn + .3)))
        mono(img, L('APRIL 9, 1940', 'ఏప్రిల్ 9, 1940'), W / 2, 845, 30, CREAM, prog(v, tn + .2, tn + .5))

@functools.lru_cache(8)
def medal(r, sh=1.0):
    im = sphere(r, GOLD, .7).copy(); d = ImageDraw.Draw(im); c = im.width / 2
    d.ellipse((c - r * .82, c - r * .82, c + r * .82, c + r * .82), outline=(150, 100, 20, 255), width=max(2, r // 18))
    f = font('archivo', max(10, int(r * .32))); d.text((c, c), 'NOBEL', font=f, fill=(110, 70, 10), anchor='mm'); return im
def g_medals(img, v, t0, t1):
    pill(img, L('NIELS BOHR INSTITUTE · COPENHAGEN', 'నీల్స్ బోర్ ఇన్‌స్టిట్యూట్ · కోపెన్‌హాగెన్'), W / 2, 330, 32, AMBER, (10, 10, 10), prog(v, t0, t0 + .3))
    for i, (x, nm) in enumerate([(320, 'MAX VON LAUE · 1914'), (760, 'JAMES FRANCK · 1925')]):
        ti = t0 + 1.4 + i * .45
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .35)); put(img, glow(240, (255, 190, 60), .5), x, 760, prog(v, ti, ti + .3))
        put(img, medal(150), x, 760, 1, k); mono(img, nm, x, 960, 22, CREAM, prog(v, ti + .2, ti + .5))
    if v >= t0 + 2.4: mono(img, L('2 GOLD NOBEL MEDALS · HIDE THEM', '2 గోల్డ్ నోబెల్ మెడల్స్ · దాచాలి'), W / 2, 1060, 28, AMBER, prog(v, t0 + 2.4, t0 + 2.7))

JAR = (360, 470)
def draw_jar(img, cx, cy, s, tint, a=1.0):
    w, h = JAR[0] * s, JAR[1] * s; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    lvl = cy - h * .5 + h * .22
    d.rounded_rectangle((cx - w / 2 + 10, lvl, cx + w / 2 - 10, cy + h / 2 - 10), radius=int(40 * s), fill=tint + (int(150 * a),))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(46 * s), outline=(220, 235, 240, int(220 * a)), width=max(3, int(7 * s)))
    d.rounded_rectangle((cx - w * .38, cy - h / 2 - 40 * s, cx + w * .38, cy - h / 2 + 6 * s), radius=int(10 * s), fill=(80, 80, 86, int(255 * a)))
    d.rounded_rectangle((cx - w * .34, cy + h * .02, cx + w * .34, cy + h * .2), radius=8, fill=(244, 241, 234, int(235 * a)))
    img.alpha_composite(lay); mono(img, 'AQUA REGIA', cx, cy + h * .11, max(12, int(26 * s)), (30, 30, 30), a)
    return lvl

def g_jar(img, v, t0, t1):
    td, tl, tw = T['dropin'], T['leave'], T['war']
    dk = prog(v, td + .9, td + 2.3)                                             # dissolve progress
    tint = tuple(int(c0 * (1 - dk) + c1 * dk) for c0, c1 in zip((200, 225, 150), (235, 150, 30)))
    mv = e_io(prog(v, tl + .3, tl + 1.1)); s = 1 - .3 * mv; cx = W / 2 - 150 * mv; cy = 760 + 170 * mv
    if mv > 0:                                                                  # the shelf + other bottles
        d = ImageDraw.Draw(img); a = int(255 * mv); sy = cy + JAR[1] * s / 2
        d.rectangle((60, sy, W - 60, sy + 22), fill=(120, 84, 50, a))
        for bx, bh in [(700, 260), (860, 190)]:
            d.rounded_rectangle((bx - 55, sy - bh, bx + 55, sy), radius=18, outline=(170, 170, 176, a), width=5, fill=(60, 70, 80, int(a * .6)))
    lvl = draw_jar(img, cx, cy, s, tint, prog(v, t0, t0 + .3))
    rng = np.random.default_rng(3)
    for i, ox in enumerate((-60, 60)):                                          # medals drop in, then dissolve
        st = td + .15 + i * .2
        if v < st: continue
        q = e_out(prog(v, st, st + .6)); y = cy - 700 * s * (1 - q) + 120 * s * q
        r = int(70 * s * (1 - dk) ** .8)
        if r > 4: put(img, medal(max(5, r)), cx + ox * s, y)
    if td + .8 <= v < td + 3.0:                                                 # fizz bubbles
        d = ImageDraw.Draw(img)
        for i in range(40):
            st = td + .8 + rng.uniform(0, 1.8); q = prog(v, st, st + .8)
            if 0 < q < 1:
                x = cx + rng.uniform(-120, 120) * s; y = cy + 150 * s - (cy + 150 * s - lvl) * q; rr = rng.uniform(4, 10) * s
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 255, 255, int(200 * (1 - q))), width=2)
    if v >= tw:                                                                 # the whole war: years roll by
        k = prog(v, tw, tw + 1.6); yr = 1940 + int(round(5 * k))
        big_text(img, str(yr), W / 2, 360, 150, CREAM, prog(v, tw, tw + .2)); mono(img, L('UNTOUCHED', 'ఎవరూ ముట్టుకోలేదు'), W / 2, 460, 30, AMBER, prog(v, tw + .3, tw + .6))
    elif v >= td: mono(img, L('MEDALS → DISSOLVED', 'మెడల్స్ కరిగిపోయాయి'), W / 2, 360, 32, AMBER, prog(v, td + 1.2, td + 1.6))

def g_recast(img, v, t0, t1):
    cx, cy = W / 2 - 150, 930; s = .7
    k1 = prog(v, t0 + .2, t0 + 1.4)                                             # gold settles out of the liquid
    tint = tuple(int(c0 * (1 - k1) + c1 * k1) for c0, c1 in zip((235, 150, 30), (200, 225, 150)))
    jar_a = 1 - prog(v, t0 + 2.0, t0 + 2.5)
    d = ImageDraw.Draw(img); sy = cy + JAR[1] * s / 2; d.rectangle((60, sy, W - 60, sy + 22), fill=(120, 84, 50, int(255 * jar_a)))
    if jar_a > 0:
        draw_jar(img, cx, cy, s, tint, jar_a); rng = np.random.default_rng(12)
        for i in range(70):
            x = cx + rng.uniform(-100, 100); y0 = cy - 60 + rng.uniform(-40, 60); q = e_io(prog(v, t0 + .2 + rng.uniform(0, .6), t0 + 1.4))
            y = y0 + (sy - 30 - y0) * q; d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GOLD + (int(255 * jar_a),))
    for i, x in enumerate((360, 720)):                                         # medals reborn
        ti = t0 + 2.2 + i * .3
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .4)); put(img, glow(260, (255, 200, 80), .6), x, 760, prog(v, ti, ti + .3)); put(img, medal(140), x, 760, 1, k)
    if v >= t0 + 2.6:
        pill(img, L('RECAST · 1952', 'మళ్ళీ తయారు · 1952'), W / 2, 380, 44, AMBER, (10, 10, 10), prog(v, t0 + 2.6, t0 + 2.85), e_back(prog(v, t0 + 2.6, t0 + 2.9)))
    if v >= T['came']: shine_sweep(img, v, T['came'], .9, .45)

def g_chips(img, v, t0, t1):
    items = [(L('NO RUST', 'తుప్పు పట్టదు'), T['rust2']), (L('NO FADE', 'రంగు పోదు'), T['fade']), (L('ALWAYS COMES BACK', 'తిరిగి వస్తుంది'), T['comes'])]
    for i, (txt, ti) in enumerate(items):
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .3)); y = 440 + i * 150
        pill(img, txt, W / 2 - 70 * (1 - k), y, 50, (14, 12, 8, 235), GOLD, prog(v, ti, ti + .15))
    tc = T['costly']
    if v >= tc:
        big_text(img, L('= SO EXPENSIVE', '= అందుకే కాస్ట్లీ'), W / 2, 960, 110 if not TE else 120, AMBER, prog(v, tc, tc + .15), e_back(prog(v, tc, tc + .35)))
