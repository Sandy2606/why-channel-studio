# ---------------- scene graphics (16:9) for the gold long video ----------------
def header(img, v, t0, text, y=150, px=34):
    mono(img, text, W / 2, y, px, AMBER, prog(v, t0, t0 + .3), track=4)

def chapter_card(img, v, t0, num, title):
    k = e_out(prog(v, t0, t0 + .5))
    mono(img, num, W / 2, 360, 34, AMBER, k, track=6)
    px = 110 if not is_te(title) else 100
    while head_font(title, px).getlength(title) > 1700 and px > 50: px -= 4
    big_text(img, title, W / 2, 470 + 30 * (1 - k), px if not is_te(title) else int(px / .82), CREAM, k)
    d = ImageDraw.Draw(img); lw = 320 * e_io(prog(v, t0 + .2, t0 + .8))
    d.rounded_rectangle((W / 2 - lw, 572, W / 2 + lw, 578), radius=3, fill=AMBER)

def g_price5k(img, v, t0, t1, s):
    header(img, v, t0, L('1 OUNCE OF GOLD', 'ఒక ounce gold'), 210)
    tc = s['t_cross']; k = e_out(prog(v, t0 + .2, tc + .3)); n = 5000 * k
    big_text(img, f'${int(round(n)):,}', W / 2, 420, 220, GOLD if n >= 4999 else CREAM, prog(v, t0 + .2, t0 + .4))
    if v >= s['t_gram']: mono(img, L('≈ 31 GRAMS · FITS IN YOUR PALM', '≈ 31 గ్రాములు · అరచేతిలో పడుతుంది'), W / 2, 570, 30, CREAM, prog(v, s['t_gram'], s['t_gram'] + .3))
    if v >= s['t_first']: stamp_text(img, L('FIRST TIME IN HISTORY', 'చరిత్రలో మొదటిసారి'), W / 2, 700, 64, AMBER, v, s['t_first'], rot=-4)

def g_notfood(img, v, t0, t1, s):
    items = [(L('JUST A METAL', 'కేవలం ఒక metal'), s['t_metal'], False), (L("CAN'T EAT IT", 'తినలేం'), s['t_eat'], True), (L("CAN'T RUN CARS ON IT", 'కార్లు నడపలేం'), s['t_cars'], True)]
    for i, (txt, ti, strike) in enumerate(items):
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .3)); y = 280 + i * 160
        chip(img, txt, W / 2 - 60 * (1 - k), y, 54, (14, 12, 8, 235), GOLD if not strike else CREAM, prog(v, ti, ti + .15))
        if strike:
            sk = e_io(prog(v, ti + .3, ti + .6)); f = head_font(txt, 54); w = f.getlength(txt) + 60
            if sk > 0: ImageDraw.Draw(img).rounded_rectangle((W / 2 - w / 2, y - 5, W / 2 - w / 2 + w * sk, y + 7), radius=5, fill=RED + (255,))

ELS = [('H', 1, (120, 190, 255)), ('He', 2, (150, 225, 235)), ('C', 6, (120, 120, 125)), ('O', 8, (235, 95, 80)),
       ('Ne', 10, (240, 130, 200)), ('Mg', 12, (180, 200, 160)), ('Si', 14, (170, 150, 120)), ('Fe', 26, (185, 95, 60))]
def g_fusion(img, v, t0, t1, s):
    mono(img, L('INSIDE EVERY STAR', 'ప్రతి స్టార్ లోపల'), W / 2, 150, 30, AMBER, prog(v, t0, t0 + .3), track=4)
    headline(img, L('STARS FUSE ATOMS INTO NEW ELEMENTS', 'స్టార్స్ ఆటమ్స్‌ని కలిపి కొత్త elements చేస్తాయి'), v, t0, W / 2, 230, 56 if not TE else 50, 1700)
    tH = s['t_H']
    if v < tH:                                                              # squeeze loop
        ph = ((v - t0) % 1.0); cx, cy = W / 2, 500
        if ph < .55:
            dx = 380 * (1 - e_io(ph / .55)); put(img, sphere(70, (120, 190, 255)), cx - dx - 20, cy); put(img, sphere(70, (120, 190, 255)), cx + dx + 20, cy)
        else:
            q = (ph - .55) / .45; put(img, glow(260, (255, 240, 200), 1 - q), cx, cy); put(img, sphere(95, (150, 225, 235)), cx, cy, 1, .7 + .3 * e_back(min(1, q * 2)))
        return
    ts = [s['t_H'], s['t_He'], s['t_C']] + list(np.linspace(s['t_C'], s['t_Fe'], 6)[1:-1]) + [s['t_Fe']]
    for i, (sym, z, col) in enumerate(ELS):
        if v < ts[i]: continue
        x = 260 + i * 200; y = 500; r = 70 + i * 3; k = e_back(prog(v, ts[i], ts[i] + .3))
        if v >= s['t_stop'] and sym == 'Fe': put(img, glow(170, (240, 60, 50), .8), x, y)
        put(img, sphere(r, col), x, y, 1, k); text_plain(img, sym, x, y - 4, 58, WHITE, prog(v, ts[i], ts[i] + .2))
        mono(img, str(z), x, y + r + 24, 24, AMBER if sym == 'Fe' else GREY, prog(v, ts[i], ts[i] + .2))
        if i < 7 and v >= ts[i + 1]: mono(img, '›', x + 100, y, 40, AMBER, prog(v, ts[i + 1] - .1, ts[i + 1] + .1))
    if v >= s['t_stop']: stamp_text(img, 'STOP', 260 + 7 * 200, 380, 50, RED, v, s['t_stop'], rot=-10)
    th = s['t_heavy']
    if v >= th:
        k = prog(v, th, th + .3); mono(img, L('GOLD ATOM', 'గోల్డ్ ఆటమ్'), W / 2, 700, 26, CREAM, k)
        text_plain(img, L('Au 197  vs  Fe 56  ·  3.5× HEAVIER', 'Au 197  vs  Fe 56  ·  3.5 రెట్లు బరువు'), W / 2, 760, 52 if not TE else 46, GOLD, k)

def g_nasa(img, v, t0, t1, s):
    if v < s['t_crash']: chip(img, s['label'], W / 2, 150, 40, AMBER, (10, 10, 10), prog(v, t0, t0 + .3) * (1 - prog(v, s['t_crash'] - .2, s['t_crash'])))
    tag(img, L('NASA ANIMATION', 'NASA యానిమేషన్'), W - 40, 92, prog(v, t0, t0 + .3), px=18, anchor='r')

def g_y2017(img, v, t0, t1, s):
    mono(img, L('FIRST ONE EVER SEEN', 'మొదటిసారి కనిపించింది'), 480, 230, 28, AMBER, prog(v, t0, t0 + .3), track=3)
    big_text(img, '2017', 480, 360, 200, CREAM, prog(v, t0, t0 + .15), e_back(prog(v, t0 + .05, t0 + .4)))
    ta = s['t_away']
    if v >= ta:
        k = e_out(prog(v, ta, ta + .8))
        big_text(img, L(f'{int(round(130 * k))} MILLION', f'{int(round(13 * k))} కోట్ల'), 480, 520, 90, AMBER, prog(v, ta, ta + .15))
        mono(img, L('LIGHT-YEARS AWAY', 'లైట్ ఇయర్స్ దూరం'), 480, 610, 26, CREAM, prog(v, ta + .3, ta + .6))
    if v >= t0 + .9: news_card(img, 'NASA', 'OCT 16, 2017', 'NASA Missions Catch First Light from a Gravitational-Wave Event', 1380, 420, v, t0 + .9, w=820, hl_words=(3, 4))
    tag(img, L('NASA ANIMATION', 'NASA యానిమేషన్'), W - 40, 92, 1.0, px=18, anchor='r')

def g_cutaway(img, v, t0, t1, s):
    cx, cy, R = W / 2, 500, 330; a = prog(v, t0, t0 + .3); ts = s['t_sank']
    mono(img, L('YOUNG EARTH · MOLTEN', 'కొత్త భూమి · కరిగిన లావా'), W / 2, 120, 30, AMBER, a * (1 - prog(v, ts, ts + .2)), track=4)
    if v >= ts: chip(img, L('GOLD SANK TO THE CORE', 'గోల్డ్ కోర్‌లోకి మునిగింది'), W / 2, 120, 40, AMBER, (10, 10, 10), prog(v, ts, ts + .25), e_back(prog(v, ts, ts + .3)))
    put(img, glow(int(R * 1.5), (255, 90, 20), .55 * a), cx, cy)
    sz = 2 * R; yy, xx = np.mgrid[0:sz, 0:sz].astype(np.float32); d = np.sqrt((xx - R) ** 2 + (yy - R) ** 2) / R
    nz = (np.sin(xx / 23 + v * 2.1) + np.sin(yy / 19 - v * 1.7) + np.sin((xx + yy) / 31 + v * 1.3)) / 3
    base = np.array([200, 55, 15], np.float32) + (np.array([255, 150, 40], np.float32) - [200, 55, 15]) * (.5 + .5 * nz)[..., None] * (1 - d * .5)[..., None]
    base = np.where((d > .93)[..., None], np.array([70, 30, 20], np.float32), base)
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(base, 0, 255), np.clip((1 - d) * R / 2, 0, 1) * 255 * a]).astype(np.uint8), 'RGBA'), (int(cx - R), int(cy - R)))
    gk = e_io(prog(v, t0 + 1.0, ts + .6)); rc = 115
    put(img, sphere(rc, (int(90 + 165 * gk), int(60 + 136 * gk), int(40 + 24 * gk)), .6 + .4 * gk), cx, cy, a)
    if gk > .5: mono(img, L('CORE', 'కోర్'), cx, cy, 28, (40, 26, 6), (gk - .5) * 2)
    rng = np.random.default_rng(9); d2 = ImageDraw.Draw(img)
    for i in range(110):
        ang = rng.uniform(0, 2 * math.pi); r0 = rng.uniform(150, 300); st = t0 + .3 + rng.uniform(0, max(.4, ts - t0 - .6)); du = rng.uniform(1.0, 1.8)
        if v < st: continue
        q = e_io(prog(v, st, st + du))
        if q >= 1: continue
        rr = r0 + (rc * .6 - r0) * q; x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        d2.ellipse((x - 6, y - 6, x + 6, y + 6), fill=GOLD + (int(255 * min(1, (1 - q) * 3)),))

def g_meteor(img, v, t0, t1, s):
    chip(img, L('METEORITES', 'మీటియోరైట్స్'), W / 2, 150, 42, AMBER, (10, 10, 10), prog(v, t0 + .3, t0 + .55), e_back(prog(v, t0 + .3, t0 + .6)))
    mono(img, L('~4 BILLION YEARS AGO', '~400 కోట్ల ఏళ్ల క్రితం'), W / 2, 225, 26, CREAM, prog(v, t0 + .5, t0 + .8))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (st, x0, y0, x1, y1, w0) in [(t0 + .2, 1900, 120, 700, 820, 28), (t0 + .9, 1500, 60, 900, 560, 18), (t0 + 1.5, 1950, 380, 1100, 1000, 24)]:
        q = prog(v, st, st + .75)
        if q <= 0 or v > st + 1.1: continue
        hx, hy = x0 + (x1 - x0) * e_io(q), y0 + (y1 - y0) * e_io(q); fade = 1 - prog(v, st + .75, st + 1.1)
        for j in range(28):
            u = j / 28; tx, ty = hx - (x1 - x0) * .32 * u, hy - (y1 - y0) * .32 * u
            wd = w0 * (1 - u) + 2; d.ellipse((tx - wd / 2, ty - wd / 2, tx + wd / 2, ty + wd / 2), fill=(255, int(240 - 150 * u), int(200 - 190 * u), int(255 * (1 - u) ** 1.5 * fade)))
        d.ellipse((hx - w0 * .7, hy - w0 * .7, hx + w0 * .7, hy + w0 * .7), fill=(255, 255, 240, int(255 * fade)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9))); img.alpha_composite(lay)

def g_reason(img, v, t0, t1, s):
    mono(img, L(f'REASON #{s["n"]}', f'కారణం #{s["n"]}'), W / 2, 300, 40, CREAM, prog(v, t0, t0 + .3), track=6)
    stamp_text(img, s['word'], W / 2, 440, 140 if not TE else 120, AMBER, v, t0 + .3, rot=-4)

def cube_spr(sz):
    im = Image.new('RGBA', (int(sz * 2.2), int(sz * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx, cy = im.width / 2, im.height / 2
    d.polygon([(cx, cy - sz), (cx + sz * .95, cy - sz * .5), (cx, cy), (cx - sz * .95, cy - sz * .5)], fill=(255, 220, 120))
    d.polygon([(cx - sz * .95, cy - sz * .5), (cx, cy), (cx, cy + sz * 1.05), (cx - sz * .95, cy + sz * .55)], fill=(214, 160, 40))
    d.polygon([(cx + sz * .95, cy - sz * .5), (cx, cy), (cx, cy + sz * 1.05), (cx + sz * .95, cy + sz * .55)], fill=(170, 120, 25))
    return im
def g_allgold(img, v, t0, t1, s):
    tcount = s['t_count']
    if v >= t0:
        mono(img, L('ALL THE GOLD EVER MINED', 'ఇప్పటిదాకా తవ్విన gold అంతా'), W / 2, 150, 30, AMBER, prog(v, t0, t0 + .3), track=4)
    if v >= tcount:
        k = e_out(prog(v, tcount, tcount + 1.0))
        big_text(img, L(f'{int(round(222000 * k)):,} TONNES', f'{int(round(222000 * k)):,} టన్నులు'), W / 2, 260, 96, GOLD, prog(v, tcount, tcount + .15))
    tc = s['t_cube']
    if v >= tc:
        gy = 860; d = ImageDraw.Draw(img); d.line((260, gy, 1660, gy), fill=(120, 116, 110, 255), width=4)
        k = e_back(prog(v, tc, tc + .4)); cs = 210                         # cube ~22.6 m
        put(img, glow(380, (255, 190, 60), .4 * k), 720, gy - 230); put(img, cube_spr(cs), 720, gy - cs * 1.1, 1, k)
        mono(img, L('22.6 m', '22.6 మీ.'), 720, gy + 30, 26, GOLD, prog(v, tc + .3, tc + .6))
        tb = s['t_bld']
        if v >= tb:                                                         # 7-storey building ~21 m
            bh = int(430 * e_out(prog(v, tb, tb + .5))); bx = 1180
            d.rectangle((bx, gy - bh, bx + 240, gy), fill=(70, 74, 82, 255))
            for fl in range(7):
                for wn in range(3):
                    yy = gy - 430 + fl * 61 + 16; xx = bx + 28 + wn * 70
                    if yy > gy - bh: d.rectangle((xx, yy, xx + 44, yy + 30), fill=(150, 170, 190, 255))
            mono(img, L('7-STOREY BUILDING', '7 అంతస్తుల building'), bx + 120, gy + 30, 22, CREAM, prog(v, tb + .3, tb + .6))
    if v >= s['t_all']: stamp_text(img, L("THAT'S ALL OF IT", 'అంతే'), 1430, 330, 56, AMBER, v, s['t_all'], rot=-4)

def g_metals4(img, v, t0, t1, s):
    header(img, v, t0, L('WHAT TIME DOES TO METALS', 'కాలం metals ని ఏం చేస్తుంది'), 160)
    tau = max(s['t_cu'] + .7, t1 - .9)
    tiles = [('Fe', L('RUSTS', 'తుప్పు'), s['t_fe'], (150, 152, 158), (178, 82, 36)), ('Ag', L('TURNS BLACK', 'నల్లబడుతుంది'), s['t_ag'], (200, 202, 210), (40, 40, 44)),
             ('Cu', L('GOES GREEN', 'ఆకుపచ్చ'), s['t_cu'], (205, 120, 70), (70, 160, 130)), ('Au', L('NEVER CHANGES', 'మారదు'), tau, GOLD, GOLD)]
    for i, (sym, lab, ti, c0, c1) in enumerate(tiles):
        x = 380 + i * 390; y = 500; a = prog(v, t0 + i * .1, t0 + .3 + i * .1)
        k = e_io(prog(v, ti, ti + .8)); col = tuple(int(p * (1 - k) + q * k) for p, q in zip(c0, c1))
        if sym == 'Au' and v >= ti: put(img, glow(240, (255, 200, 80), .7), x, y)
        put(img, sphere(120, col), x, y, a); text_plain(img, sym, x, y - 6, 80, WHITE if sym != 'Au' else (40, 26, 6), a)
        if v >= ti: chip(img, lab, x, y + 190, 30, (14, 12, 8, 230), GOLD if sym == 'Au' else CREAM, prog(v, ti, ti + .25))

def g_goldox(img, v, t0, t1, s):
    cx, cy, R = W / 2, 480, 170
    headline(img, L('GOLD HOLDS ITS ELECTRONS TIGHT', 'గోల్డ్ ఎలక్ట్రాన్స్‌ని గట్టిగా పట్టుకుంటుంది'), v, t0, W / 2, 140, 56 if not TE else 48, 1700)
    put(img, glow(320, (255, 190, 60), .6), cx, cy); put(img, sphere(R, GOLD), cx, cy); text_plain(img, 'Au', cx, cy - 6, 96, (40, 26, 6))
    for j in range(4):
        aa = v * 5 + j * math.pi / 2; put(img, sphere(13, (150, 220, 255)), cx + (R + 40) * math.cos(aa), cy + (R + 40) * math.sin(aa))
    rng = np.random.default_rng(8)
    for i in range(10):
        st = t0 + .3 + i * .36; ang = rng.uniform(0, 2 * math.pi)
        if v < st: continue
        q = prog(v, st, st + 1.1); r1 = R + 70
        rr = 820 - (820 - r1) * e_out(q / .4) if q < .4 else r1 + 750 * e_io((q - .4) / .6); aa = ang if q < .4 else ang + .5
        if q < 1: o2(img, cx + rr * math.cos(aa), cy + rr * .62 * math.sin(aa), aa + math.pi / 2, min(1, (1 - q) * 3), s=.9)
    if v >= s['t_cant']: chip(img, L('OXYGEN CAN\'T GRAB IT', 'ఆక్సిజన్‌కి పట్టు దొరకదు'), W / 2, 760, 38, AMBER, (10, 10, 10), prog(v, s['t_cant'], s['t_cant'] + .25), e_back(prog(v, s['t_cant'], s['t_cant'] + .3)))

def g_tut(img, v, t0, t1, s):
    ty = s.get('t_years')
    if ty and v >= ty:
        k = e_out(prog(v, ty, ty + .8))
        big_text(img, f'{int(round(3300 * k)):,}', 1550, 380, 150, AMBER, prog(v, ty, ty + .15)); mono(img, L('YEARS · STILL SHINING', 'ఏళ్ళు · ఇంకా మెరుస్తోంది'), 1550, 480, 24, CREAM, prog(v, ty + .3, ty + .6))
        shine_sweep(img, v, ty + 1.2, 1.0, .35)

def g_stillhere(img, v, t0, t1, s):
    ts = s['t_still']
    if v >= ts:
        big_text(img, L('ALMOST ALL OF IT\nIS STILL HERE', 'దాదాపు అంతా\nఇంకా ఉంది'), W / 2, 420, 110, GOLD, prog(v, ts, ts + .2), e_back(prog(v, ts, ts + .4)))

def g_hands(img, v, t0, t1, s):
    names = [L('COIN', 'నాణెం'), L('NECKLACE', 'నెక్లెస్'), L('BAR', 'బార్'), L('RING', 'ఉంగరం')]
    for i, (nm, ti) in enumerate(zip(names, s['ts'])):
        if v < ti: continue
        x = 330 + i * 420; k = e_back(prog(v, ti, ti + .3))
        chip(img, nm, x, 450, 52, (14, 12, 8, 235), GOLD, prog(v, ti, ti + .15), .8 + .2 * k)
        if i > 0: mono(img, '→', x - 210, 450, 50, AMBER, prog(v, ti - .1, ti + .1))
    header(img, v, t0, L('THE SAME GOLD, CHANGING HANDS', 'అదే gold, చేతులు మారుతూ'), 300)

# periodic table
PT = """H 1 1|He 1 18|Li 2 1|Be 2 2|B 2 13|C 2 14|N 2 15|O 2 16|F 2 17|Ne 2 18|Na 3 1|Mg 3 2|Al 3 13|Si 3 14|P 3 15|S 3 16|Cl 3 17|Ar 3 18|
K 4 1|Ca 4 2|Sc 4 3|Ti 4 4|V 4 5|Cr 4 6|Mn 4 7|Fe 4 8|Co 4 9|Ni 4 10|Cu 4 11|Zn 4 12|Ga 4 13|Ge 4 14|As 4 15|Se 4 16|Br 4 17|Kr 4 18|
Rb 5 1|Sr 5 2|Y 5 3|Zr 5 4|Nb 5 5|Mo 5 6|Tc 5 7|Ru 5 8|Rh 5 9|Pd 5 10|Ag 5 11|Cd 5 12|In 5 13|Sn 5 14|Sb 5 15|Te 5 16|I 5 17|Xe 5 18|
Cs 6 1|Ba 6 2|La 6 3|Hf 6 4|Ta 6 5|W 6 6|Re 6 7|Os 6 8|Ir 6 9|Pt 6 10|Au 6 11|Hg 6 12|Tl 6 13|Pb 6 14|Bi 6 15|Po 6 16|At 6 17|Rn 6 18|
Fr 7 1|Ra 7 2|Ac 7 3|Rf 7 4|Db 7 5|Sg 7 6|Bh 7 7|Hs 7 8|Mt 7 9|Ds 7 10|Rg 7 11|Cn 7 12|Nh 7 13|Fl 7 14|Mc 7 15|Lv 7 16|Ts 7 17|Og 7 18|
Ce 8 4|Pr 8 5|Nd 8 6|Pm 8 7|Sm 8 8|Eu 8 9|Gd 8 10|Tb 8 11|Dy 8 12|Ho 8 13|Er 8 14|Tm 8 15|Yb 8 16|Lu 8 17|
Th 9 4|Pa 9 5|U 9 6|Np 9 7|Pu 9 8|Am 9 9|Cm 9 10|Bk 9 11|Cf 9 12|Es 9 13|Fm 9 14|Md 9 15|No 9 16|Lr 9 17"""
PTE = [(e.split()[0], int(e.split()[1]), int(e.split()[2])) for e in PT.replace('\n', '').split('|')]
CAT = dict(gas='H He N O F Ne Cl Ar Kr Xe Rn Og', liq='Br Hg', fire='Li Na K Rb Cs Fr Be Mg Ca Sr Ba Ra',
           rad='Tc Pm Po At Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts La Ce Pr Nd Sm Eu Gd Tb Dy Ho Er Tm Yb Lu',
           rare='Ru Rh Pd Os Ir')
def g_ptable(img, v, t0, t1, s):
    cw, chh = 86, 62; x0 = (W - 18 * cw) / 2; y0 = 175
    steps = [('gas', s['t_gas'], L('OUT: GASES', 'అవుట్: GASES')), ('liq', s['t_liq'], L('OUT: LIQUIDS', 'అవుట్: LIQUIDS')),
             ('fire', s['t_fire'], L('OUT: CATCH FIRE / REACT WITH WATER', 'అవుట్: మండేవి')), ('rad', s['t_rad'], L('OUT: RADIOACTIVE', 'అవుట్: RADIOACTIVE')),
             ('common', s['t_common'], L('OUT: TOO COMMON, CORRODE', 'అవుట్: COMMON')), ('rare', s['t_rare'], L('OUT: TOO RARE', 'అవుట్: మరీ అరుదు')),
             ('Ag', s['t_ag'], L('SILVER TARNISHES', 'SILVER నల్లబడుతుంది')), ('Pt', s['t_pt'], L('PLATINUM: TOO HARD TO MELT', 'PLATINUM కరగదు'))]
    out_t = {}
    for key, tt, _ in steps:
        names = CAT.get(key, key).split()
        for nm in names: out_t.setdefault(nm, tt)
    for sym, r, c in PTE:                                                       # everything else not precious = common
        if sym not in out_t and sym not in ('Ru', 'Rh', 'Pd', 'Os', 'Ir', 'Pt', 'Au', 'Ag'): out_t[sym] = s['t_common']
    out_t.setdefault('Ag', s['t_ag']); out_t['Ag'] = s['t_ag']; out_t['Pt'] = s['t_pt']
    d = ImageDraw.Draw(img); f = font('archivo', 26); win = s['t_win']
    for i, (sym, r, c) in enumerate(PTE):
        ta = t0 + .03 * i / 3
        if v < ta: continue
        x = x0 + (c - 1) * cw; y = y0 + (r - 1) * chh + (14 if r >= 8 else 0); a = prog(v, ta, ta + .2)
        to = out_t.get(sym, 1e9); dead = prog(v, to, to + .35)
        left = sym in ('Ag', 'Pt', 'Au') and v >= s['t_left'] and dead < 1
        fill = (40, 40, 44) if not left else (60, 46, 14)
        if sym == 'Au' and v >= win: fill = (120, 86, 10)
        alpha = int(255 * a * (1 - .78 * dead))
        d.rounded_rectangle((x + 3, y + 3, x + cw - 3, y + chh - 3), radius=8, fill=fill + (alpha,), outline=(AMBER + (alpha,)) if left else None, width=3)
        d.text((x + cw / 2, y + chh / 2), sym, font=f, fill=(CREAM if not left else GOLD) + (alpha,), anchor='mm')
        if 0 < dead: d.line((x + 10, y + chh - 10, x + 10 + (cw - 20) * min(1, dead * 1.5), y + chh - 10 - (chh - 20) * min(1, dead * 1.5)), fill=RED + (int(220 * (1 - .5 * dead)),), width=4)
    cur = None
    for key, tt, lab in steps:
        if v >= tt: cur = (lab, tt)
    if v < s['t_gas']: header(img, v, t0, L('PICK A METAL FOR MONEY', 'డబ్బు కోసం ఒక metal ఎంచుకోండి'), 120)
    elif v < s['t_left'] or v >= s['t_ag']:
        if cur and v < win: chip(img, cur[0], W / 2, 120, 34, (230, 70, 60), WHITE, prog(v, cur[1], cur[1] + .2))
    if s['t_left'] <= v < s['t_ag']: chip(img, L("WHAT'S LEFT: SILVER, PLATINUM, GOLD", 'మిగిలినవి: SILVER, PLATINUM, GOLD'), W / 2, 120, 34, AMBER, (10, 10, 10), prog(v, s['t_left'], s['t_left'] + .2))
    if v >= win:
        k = e_back(prog(v, win, win + .45)); img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(150 * prog(v, win, win + .3)))))
        put(img, glow(360, (255, 190, 60), .8), W / 2, 470, prog(v, win, win + .3))
        t = Image.new('RGBA', (300, 340), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
        td.rounded_rectangle((0, 0, 299, 339), radius=26, fill=(30, 22, 6, 245), outline=GOLD + (255,), width=6)
        td.text((26, 20), '79', font=font('mono', 40), fill=GOLD); fb = font('archivo', 150); td.text((150, 160), 'Au', font=fb, fill=GOLD, anchor='mm')
        td.text((150, 285), L('GOLD', 'గోల్డ్'), font=head_font(L('GOLD', 'గోల్డ్'), 40), fill=CREAM, anchor='mm')
        put(img, t, W / 2, 470, prog(v, win, win + .2), .6 + .4 * k)
        mono(img, L('RARE, BUT NOT TOO RARE · EASY TO MELT · NEVER ROTS', 'అరుదు, కానీ మరీ కాదు · సులభంగా కరుగుతుంది · పాడవదు'), W / 2, 700, 24, CREAM, prog(v, win + .5, win + .8))
    if v >= s['t_gas'] - .5 and v < win: tag(img, 'SOURCE · S. KUMAR (COLUMBIA) VIA NPR / VISUAL CAPITALIST', 60, 820, prog(v, s['t_gas'] - .5, s['t_gas']), px=16, col=AMBER)

def g_tonne(img, v, t0, t1, s):
    tr, tg, tp = s['t_rock'], s['t_gold'], s['t_pep']
    if v >= tr: chip(img, L('1 TONNE OF ROCK', '1 టన్ను రాళ్ళు'), 560, 300, 54, (14, 14, 14, 235), CREAM, prog(v, tr, tr + .2), e_back(prog(v, tr, tr + .3)))
    if v >= tg:
        mono(img, '→', W / 2, 300, 60, AMBER, prog(v, tg - .1, tg + .1))
        chip(img, L('≈ 1.5 g GOLD', '≈ 1.5 గ్రా. గోల్డ్'), 1360, 300, 54, AMBER, (10, 10, 10), prog(v, tg, tg + .2), e_back(prog(v, tg, tg + .3)))
    if v >= tp:
        k = e_back(prog(v, tp, tp + .4)); put(img, glow(120, (255, 200, 80), .8), W / 2, 540, k); put(img, sphere(18, GOLD), W / 2, 540, 1, k)
        mono(img, L('SMALLER THAN A PEPPERCORN', 'మిరియం గింజ కంటే చిన్నది'), W / 2, 620, 30, GOLD, prog(v, tp + .2, tp + .5))
    if v >= tr - .3: tag(img, L('SOURCE · METALS FOCUS: AVG GRADE ~1.4 g/t', 'SOURCE · METALS FOCUS: ~1.4 g/t'), 60, 820, prog(v, tr - .3, tr), px=16, col=AMBER)

def g_yearly(img, v, t0, t1, s):
    tn, tp = s['t_n'], s['t_pct']
    if v >= tn:
        k = e_out(prog(v, tn, tn + .8))
        big_text(img, L(f'{int(round(3600 * k)):,} TONNES / YEAR', f'ఏడాదికి {int(round(3600 * k)):,} టన్నులు'), W / 2, 300, 96, GOLD, prog(v, tn, tn + .15))
    if v >= tp:
        a = prog(v, tp, tp + .3); x0, x1, y = 260, 1660, 560; d = ImageDraw.Draw(img)
        d.rounded_rectangle((x0, y - 40, x1, y + 40), radius=12, fill=(60, 50, 20, int(255 * a)))
        sl = (x1 - x0) * .016 * e_out(prog(v, tp + .3, tp + .8)); d.rounded_rectangle((x1 - sl - 6, y - 40, x1, y + 40), radius=6, fill=GOLD + (int(255 * a),))
        mono(img, L('ALL GOLD EVER MINED · 222,000 t', 'ఇప్పటిదాకా తవ్విన gold · 222,000 t'), x0 + 20, y, 22, CREAM, a, anchor='l')
        mono(img, L('+1 YEAR = LESS THAN 2%', '+1 ఏడాది = 2% కంటే తక్కువ'), x1 - 10, y + 80, 26, GOLD, prog(v, tp + .6, tp + .9), anchor='r')
        tag(img, 'SOURCE · WORLD GOLD COUNCIL', 60, 820, a, px=16, col=AMBER)

def g_three(img, v, t0, t1, s):
    names = [L('RARE', 'అరుదు'), L('LASTS FOREVER', 'ఎప్పటికీ ఉంటుంది'), L('HARD TO MINE', 'తవ్వడం కష్టం')]
    for i, (nm, ti) in enumerate(zip(names, s['ts'])):
        if v < ti: continue
        chip(img, nm, 420 + i * 540, 300, 50, (14, 12, 8, 235), GOLD, prog(v, ti, ti + .15), .8 + .2 * e_back(prog(v, ti, ti + .3)))
    if v >= s['t_always'] and v < s['t_q']: stamp_text(img, L('ALWAYS TRUE', 'ఎప్పుడూ ఉన్నవే'), W / 2, 480, 80, CREAM, v, s['t_always'], rot=-4)
    if v >= s['t_q']: pop_big(img, v, s['t_q'], L('SO WHY NOW?', 'మరి ఇప్పుడెందుకు?'), W / 2, 500, 150, AMBER)

def g_banks(img, v, t0, t1, s):
    if v >= s['t_buy']: stamp_text(img, L('COUNTRIES ARE BUYING', 'దేశాలే కొంటున్నాయి'), W / 2, 430, 100 if not TE else 90, AMBER, v, s['t_buy'], rot=-4)

def g_cbchart(img, v, t0, t1, s):
    header(img, v, t0, L('CENTRAL BANKS: GOLD BOUGHT PER YEAR (TONNES)', 'Central banks: ఏడాదికి కొన్న gold (టన్నులు)'), 120, 28)
    bars = [(L('2010–21 AVG', '2010–21 సగటు'), 473, s['t_470']), ('2022', 1082, s['t_1000']), ('2023', 1037, s['t_1000'] + .5), ('2024', 1092, s['t_1000'] + 1.0), ('2025', 863, s['t_860'])]
    base = 800; hmax = 560; x0 = 380; gap = 300; d = ImageDraw.Draw(img)
    d.line((x0 - 120, base, x0 + gap * 4 + 120, base), fill=(120, 116, 110, 255), width=3)
    for i, (lab, val, ti) in enumerate(bars):
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .6)); h = hmax * val / 1100 * k; x = x0 + i * gap
        col = (150, 146, 138) if i == 0 else GOLD
        d.rounded_rectangle((x - 80, base - h, x + 80, base), radius=10, fill=col + (255,))
        mono(img, f'{int(round(val * k)):,}', x, base - h - 30, 30, col, prog(v, ti, ti + .2))
        mono(img, lab, x, base + 32, 22, CREAM, prog(v, ti, ti + .2))
    if v >= s['t_1000'] + 1.2:
        a = prog(v, s['t_1000'] + 1.2, s['t_1000'] + 1.5); y = base - hmax * 1000 / 1100
        for xx in range(x0 - 100, x0 + gap * 4 + 100, 28): d.line((xx, y, xx + 14, y), fill=AMBER + (int(200 * a),), width=3)
        mono(img, '1,000 t', x0 + gap * 4 + 150, y, 22, AMBER, a)
    tag(img, 'SOURCE · WORLD GOLD COUNCIL, GOLD DEMAND TRENDS FY2025', 60, 880, prog(v, t0 + .5, t0 + .8), px=16, col=AMBER)

def g_scary(img, v, t0, t1, s):
    names = [L('WARS', 'యుద్ధాలు'), L('RISING PRICES', 'పెరిగే ధరలు'), L('COUNTRIES NOT TRUSTING EACH OTHER', 'దేశాల మధ్య నమ్మకం లేదు')]
    for i, (nm, ti) in enumerate(zip(names, s['ts'])):
        if v < ti: continue
        chip(img, nm, W / 2 - 50 * (1 - e_back(prog(v, ti, ti + .3))), 260 + i * 150, 54, (14, 12, 8, 235), CREAM, prog(v, ti, ti + .15))

def g_printvs(img, v, t0, t1, s):
    chip(img, L('MONEY: CAN BE PRINTED', 'డబ్బు: ప్రింట్ చేయొచ్చు'), 560, 300, 44, (14, 14, 14, 235), CREAM, prog(v, t0 + .3, t0 + .5))
    if v >= s['t_gold']: stamp_text(img, L("GOLD: CAN'T", 'గోల్డ్: చేయలేం'), 1360, 300, 80, AMBER, v, s['t_gold'], rot=-5)

def g_pricechart(img, v, t0, t1, s):
    header(img, v, t0, L('PRICE OF 1 OUNCE OF GOLD (US$)', '1 ounce gold ధర (US$)'), 120, 28)
    pts = [(2019.0, 1393, s['t_19'], L('2019', '2019')), (2026.08, 5502, s['t_26'], L('JAN 2026 · PEAK', 'జన 2026 · గరిష్టం')), (2026.82, 4016, s['t_now'], L('NOW', 'ఇప్పుడు'))]
    X = lambda yr: 300 + (yr - 2019) / (2027 - 2019) * 1320; Y = lambda p: 820 - p / 6000 * 620
    d = ImageDraw.Draw(img); d.line((260, 820, 1680, 820), fill=(120, 116, 110, 255), width=3)
    for yr in range(2019, 2027): mono(img, str(yr), X(yr), 850, 18, GREY, prog(v, t0, t0 + .3))
    prev = None
    for i, (yr, p, ti, lab) in enumerate(pts):
        if v < ti: continue
        x, y = X(yr), Y(p)
        if prev:
            k = e_io(prog(v, ti, ti + .7)); px_, py_ = prev; d.line((px_, py_, px_ + (x - px_) * k, py_ + (y - py_) * k), fill=GOLD + (255,), width=8)
            if k < 1: continue
        put(img, sphere(16, GOLD), x, y)
        if i == 2: big_text(img, f'${p:,}', x + 30, y + 70, 52, GOLD, prog(v, ti, ti + .2)); mono(img, lab, x + 30, y + 125, 20, CREAM, prog(v, ti, ti + .2))
        else: big_text(img, f'${p:,}', x - (60 if i == 1 else 0), y - 60, 52, GOLD if i else CREAM, prog(v, ti, ti + .2)); mono(img, lab, x - (60 if i == 1 else 0), y + 40 if i == 0 else y - 110, 20, CREAM, prog(v, ti, ti + .2))
        prev = (x, y)
    if v >= s['t_x3']: stamp_text(img, L('≈ 3× SINCE 2019', '2019 కంటే ≈ 3 రెట్లు'), 1350, 700, 60, AMBER, v, s['t_x3'], rot=-5)
    tag(img, 'SOURCE · LBMA PRICES · FORTUNE, OCT 26, 2026', 60, 880, prog(v, t0 + .5, t0 + .8), px=16, col=AMBER)

def g_festivals(img, v, t0, t1, s):
    names = [L('WEDDINGS', 'పెళ్ళిళ్ళు'), L('AKSHAYA TRITIYA', 'అక్షయ తృతీయ'), L('DHANTERAS', 'ధన్‌తేరస్')]
    for i, (nm, ti) in enumerate(zip(names, s['ts'])):
        if v < ti: continue
        chip(img, nm, 420 + i * 540, 300, 50, (14, 12, 8, 235), GOLD, prog(v, ti, ti + .15), .8 + .2 * e_back(prog(v, ti, ti + .3)))
    if v >= s['t_date']: stamp_text(img, L('DHANTERAS · NOV 6', 'ధన్‌తేరస్ · నవంబర్ 6'), W / 2, 500, 80, AMBER, v, s['t_date'], rot=-4)

def g_top2(img, v, t0, t1, s):
    header(img, v, t0, L('THE TWO BIGGEST GOLD BUYERS', 'ఎక్కువ gold కొనే రెండు దేశాలు'), 170)
    for i, (nm, ti) in enumerate([(L('INDIA', 'ఇండియా'), t0 + .4), (L('CHINA', 'చైనా'), s['t_cn'])]):
        if v < ti: continue
        k = e_back(prog(v, ti, ti + .35)); x = 640 + i * 640
        put(img, glow(260, (255, 190, 60), .45), x, 470, prog(v, ti, ti + .3))
        t = Image.new('RGBA', (460, 240), (0, 0, 0, 0)); td = ImageDraw.Draw(t); td.rounded_rectangle((0, 0, 459, 239), radius=28, fill=(30, 22, 6, 240), outline=GOLD + (255,), width=6)
        fb = head_font(nm, 96); td.text((230, 120), nm, font=fb, fill=GOLD, anchor='mm'); put(img, t, x, 470, prog(v, ti, ti + .2), .7 + .3 * k)
    tag(img, 'SOURCE · WORLD GOLD COUNCIL', 60, 820, prog(v, t0 + .5, t0 + .8), px=16, col=AMBER)

def g_recap(img, v, t0, t1, s):
    items = [L('MADE IN EXPLODING STARS', 'పేలిన స్టార్స్‌లో పుట్టింది'), L('VERY LITTLE OF IT', 'చాలా తక్కువ'), L('NEVER ROTS', 'పాడవదు'),
             L('BRUTAL TO DIG UP', 'తవ్వడం కష్టం'), L('EVERYONE WANTS IT IN SCARY TIMES', 'భయం వస్తే అందరికీ కావాలి')]
    for i, (nm, ti) in enumerate(zip(items, s['ts'])):
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .35)); y = 190 + i * 130
        put(img, sphere(22, GOLD), 360, y, 1, k); text_plain(img, nm, 420 + 40 * (1 - k), y - 4, 58 if not TE else 52, CREAM, k, anchor='l')

def cta(img, v, t0, s):
    big_text(img, 'WHY?' if not TE else 'WHY? తెలుగు', W / 2, 230, 190 if not TE else 150, CREAM, prog(v, t0, t0 + .25))
    sub_button(img, v, t0 + .6, W / 2, 450, 1.3, tap=1.4)
    mono(img, L('A NEW WHY EVERY DAY', 'రోజూ ఒక కొత్త "ఎందుకు"'), W / 2, 570, 30, AMBER, prog(v, t0 + .8, t0 + 1.2), track=4)
    big_text(img, L('COMMENT YOUR WHY BELOW', 'మీ "ఎందుకు" కామెంట్ చేయండి'), W / 2, 700, 64 if not TE else 56, CREAM, prog(v, t0 + 2.6, t0 + 3.0))
    mono(img, s['src'], W / 2, 1030, 20, GREY, prog(v, t0 + 1.2, t0 + 1.6), track=2)

GFX = dict(price5k=g_price5k, notfood=g_notfood, fusion=g_fusion, nasa=g_nasa, y2017=g_y2017, cutaway=g_cutaway, meteor=g_meteor, reason=g_reason,
           allgold=g_allgold, metals4=g_metals4, goldox=g_goldox, tut=g_tut, stillhere=g_stillhere, hands=g_hands, ptable=g_ptable, tonne=g_tonne,
           yearly=g_yearly, three=g_three, banks=g_banks, cbchart=g_cbchart, scary=g_scary, printvs=g_printvs, pricechart=g_pricechart,
           festivals=g_festivals, top2=g_top2, recap=g_recap)

def SFX_EVENTS(s, t0, t1):
    k = s['kind']; E = []
    if k == 'price5k': E += [('coins_clink', t0, .3), ('ticker_run', t0 + .2, .35), ('sub_knock', s['t_cross'] + .3, .5), ('stamp', s['t_first'], .45)]
    if k == 'notfood': E += [('sub_knock', s['t_metal'], .4), ('sub_knock', s['t_eat'], .4), ('marker', s['t_eat'] + .3, .2), ('sub_knock', s['t_cars'], .4), ('marker', s['t_cars'] + .3, .2)]
    if k == 'fusion':
        ts = [s['t_H'], s['t_He'], s['t_C']] + list(np.linspace(s['t_C'], s['t_Fe'], 6)[1:-1]) + [s['t_Fe']]
        E += [('tick', t, .5) for t in ts] + [('stamp', s['t_stop'], .5), ('metal_transform', s['t_heavy'] + .1, .2)]
        tt = t0 + .55
        while tt < s['t_H'] - .2: E.append(('sub_knock', tt, .25)); tt += 1.0
    if k == 'nasa': E += [('riser', s['t_crash'] - 2.53, .4), ('impact_trailer', s['t_crash'], .7)]
    if k == 'y2017': E += [('shutter', t0, .4), ('ticker_run', s['t_away'], .3), ('paper_slide', t0 + .9, .3)]
    if k == 'cutaway': E += [('sub_knock', s['t_sank'], .45)]
    if k == 'meteor': E += [('meteor_fall', t0 + .2 + .75 - 2.54, .4), ('meteor_fall', t0 + 1.5 + .75 - 2.54, .28)]
    if k == 'reason': E += [('stamp', t0 + .3, .5)]
    if k == 'allgold': E += [('ticker_run', s['t_count'], .35), ('sub_knock', s['t_cube'], .5), ('sub_knock', s['t_bld'], .4), ('stamp', s['t_all'], .45)]
    if k == 'metals4': E += [('sub_knock', s[x], .4) for x in ('t_fe', 't_ag', 't_cu')] + [('coin_flutter', max(s['t_cu'] + .7, t1 - .9) - .3, .35)]
    if k == 'goldox': E += [('tick', t0 + .3 + i * .36 + .44, .25) for i in range(10)] + [('sub_knock', s['t_cant'], .45)]
    if k == 'tut' and s.get('t_years'): E += [('ticker_run', s['t_years'], .3)]
    if k == 'stillhere': E += [('sub_knock', s['t_still'], .5)]
    if k == 'hands': E += [('coin_flutter', t - .3, .3) for t in s['ts']]
    if k == 'ptable':
        E += [('ticker_run', t0, .3)] + [('stamp', s[x], .4) for x in ('t_gas', 't_liq', 't_fire', 't_rad', 't_common', 't_rare', 't_ag', 't_pt')]
        E += [('sub_knock', s['t_left'], .45), ('coins_clink', s['t_win'], .4), ('boom_distant', s['t_win'], .25)]
    if k == 'tonne': E += [('sub_knock', s['t_rock'], .45), ('sub_knock', s['t_gold'], .45), ('coin_flutter', s['t_pep'] - .3, .3)]
    if k == 'yearly': E += [('ticker_run', s['t_n'], .3), ('sub_knock', s['t_pct'], .45)]
    if k == 'three': E += [('sub_knock', t, .4) for t in s['ts']] + [('stamp', s['t_always'], .4), ('sub_knock', s['t_q'], .5)]
    if k == 'banks': E += [('vault_open', t0 + .1, .5), ('stamp', s['t_buy'], .5)]
    if k == 'cbchart': E += [('sub_knock', t, .4) for t in (s['t_470'], s['t_1000'], s['t_1000'] + .5, s['t_1000'] + 1.0, s['t_860'])] + [('paper_slide', t0 + .5, .25)]
    if k == 'scary': E += [('sub_knock', t, .4) for t in s['ts']]
    if k == 'printvs': E += [('sub_knock', t0 + .3, .4), ('stamp', s['t_gold'], .5)]
    if k == 'pricechart': E += [('sub_knock', s['t_19'], .4), ('ticker_run', s['t_26'], .3), ('sub_knock', s['t_26'] + .7, .5), ('sub_knock', s['t_now'] + .7, .4), ('stamp', s['t_x3'], .45)]
    if k == 'festivals': E += [('sub_knock', t, .4) for t in s['ts']] + [('stamp', s['t_date'], .45)]
    if k == 'top2': E += [('sub_knock', t0 + .4, .45), ('sub_knock', s['t_cn'], .45)]
    if k == 'recap': E += [('sub_knock', t, .4) for t in s['ts']]
    if k == 'cta': E += [('mouse_click', t0 + .6 + 1.4, .5)]
    return E

def AMB_EVENTS(s, t0, t1):
    k = s['kind']; A = []
    if k in ('nasa', 'y2017'): A.append(('space_drone', t0 - .2, t1 + .3, .28))
    if k == 'cutaway': A.append(('lava_bubble', t0, t1 + .2, .4))
    if k in ('printvs',): A.append(('machine_hum', t0, t1 + .2, .2))
    if k in ('tonne',): A.append(('machine_hum', t0, t1 + .2, .15))
    return A

# ---------------- title sequence (documentary collage style: paper, clippings, marker, stamp, typewriter) ----------------
FL = '/home/claude/why-channel-studio/brand/fonts/library/'
@functools.lru_cache(8)
def ffont(kind, px):
    from PIL import ImageFont
    if kind == 'bebas': return ImageFont.truetype(FL + 'English/BebasNeue/BebasNeue-Regular.ttf', px)
    if kind == 'baloo':
        f = ImageFont.truetype(FL + 'Telugu/BalooTammudu2/BalooTammudu2[wght].ttf', px, layout_engine=ImageFont.Layout.RAQM)
        try: f.set_variation_by_name(b'ExtraBold')
        except Exception:
            try: f.set_variation_by_name('ExtraBold')
            except Exception: pass
        return f
@functools.lru_cache(1)
def paper():
    rng = np.random.default_rng(42); h, w = H + 200, W + 300
    base = np.zeros((h, w, 3), np.float32) + np.array([233, 224, 204], np.float32)
    n = rng.normal(0, 1, (h // 4, w // 4)).astype(np.float32)
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255 - .5
    base += n[..., None] * 26 + rng.normal(0, 5, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w]; d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    base *= (1 - .32 * np.clip(d - .35, 0, 1) ** 1.5)[..., None]
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA'); dr = ImageDraw.Draw(im)
    for k in range(14):                                                              # faint contour lines (no borders)
        cx, cy, r0 = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(80, 260)
        for j in range(5):
            r = r0 + j * 38; pts = [(cx + r * (1 + .12 * math.sin(a * 3 + k)) * math.cos(a), cy + r * .7 * (1 + .1 * math.cos(a * 2 + j)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 90)]
            dr.line(pts, fill=(150, 130, 100, 60), width=2)
    return im
def clipping(kind, w, h):
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((26, 30, w + 26, h + 30), fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    card = Image.new('RGBA', (w, h), (246, 241, 228, 255)); d = ImageDraw.Draw(card)
    if kind == 'photo':
        return im, card
    return im, card
def make_clip(kind):
    if kind == 'tut':
        s = _still('tut.jpg'); w, h = 300, 360; card = Image.new('RGBA', (w, h), (248, 246, 240, 255))
        ph = s.resize((260, int(s.height * 260 / s.width))).crop((0, 20, 260, 300)); card.paste(ph, (20, 18))
        ImageDraw.Draw(card).text((w / 2, 326), 'c. 1323 BC', font=font('mono', 20), fill=(60, 50, 40), anchor='mm')
    elif kind == 'bars':
        fr = cframe('B', 1.0).resize((420, 236)); w, h = 450, 300; card = Image.new('RGBA', (w, h), (248, 246, 240, 255)); card.paste(fr, (15, 15))
        ImageDraw.Draw(card).text((w / 2, 274), 'FINE GOLD 999.9', font=font('mono', 20), fill=(60, 50, 40), anchor='mm')
    elif kind == 'nasa':
        w, h = 520, 210; card = Image.new('RGBA', (w, h), (244, 240, 228, 255)); d = ImageDraw.Draw(card)
        d.text((22, 18), 'NASA · OCT 16, 2017', font=font('mono', 18), fill=(150, 40, 30))
        f = font('archivo', 34); y = 54
        for ln in ['NASA Missions Catch First', 'Light from a Gravitational-', 'Wave Event']: d.text((22, y), ln, font=f, fill=(25, 22, 18)); y += 44
    elif kind == 'price':
        w, h = 360, 200; card = Image.new('RGBA', (w, h), (244, 240, 228, 255)); d = ImageDraw.Draw(card)
        d.text((w / 2, 50), 'GOLD · 1 OZ · JAN 2026', font=font('mono', 18), fill=(90, 80, 60), anchor='mm')
        d.text((w / 2, 125), '$5,000', font=ffont('bebas', 120), fill=(25, 22, 18), anchor='mm')
    else:   # chart
        w, h = 380, 250; card = Image.new('RGBA', (w, h), (244, 240, 228, 255)); d = ImageDraw.Draw(card)
        d.text((20, 16), 'CENTRAL BANK BUYING (t)', font=font('mono', 17), fill=(90, 80, 60))
        for i, val in enumerate([473, 1082, 1037, 1092, 863]):
            bh = 150 * val / 1100; x = 40 + i * 64; d.rectangle((x, 220 - bh, x + 44, 220), fill=(196, 150, 40) if i else (150, 146, 138))
        d.line((24, 220, w - 20, 220), fill=(60, 50, 40), width=3)
    out = Image.new('RGBA', (card.width + 40, card.height + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((24, 28, card.width + 24, card.height + 28), fill=(0, 0, 0, 130))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9))); out.alpha_composite(card, (14, 14)); return out
@functools.lru_cache(8)
def clip_spr(kind, rot): return make_clip(kind).rotate(rot, Image.BICUBIC, expand=True)
JH = [('nasa', 470, 300, -4, .25), ('tut', 1460, 330, 5, .65), ('bars', 520, 690, 3, 1.05), ('price', 1440, 720, -6, 1.45), ('chart', 960, 250, 2, 1.85)]
def marker_circle(d, cx, cy, rx, ry, k, col=(200, 30, 30, 235), wdt=7, seed=0):
    rng = np.random.default_rng(seed); n = int(80 * k)
    pts = [(cx + rx * (1 + .04 * math.sin(a * 5 + seed)) * math.cos(a + .3), cy + ry * (1 + .05 * math.cos(a * 4)) * math.sin(a + .3)) for a in np.linspace(0, 2 * math.pi * 1.08, 80)[:max(2, n)]]
    d.line(pts, fill=col, width=wdt, joint='curve')
def g_jhintro(img, v, t0, t1, s):
    q = v - t0; dur = max(1.0, t1 - t0)
    z = 1.0 + .05 * e_io(min(1, q / dur)); rot = -1.2 + 1.2 * e_io(min(1, q / dur))
    canvas = paper().copy().convert('RGBA'); d = ImageDraw.Draw(canvas); ox, oy = 150, 100
    for kind, x, y, r, ti in JH:                                                # clippings drop onto the table
        if q < ti: continue
        k = e_out(prog(q, ti, ti + .28)); spr = clip_spr(kind, r)
        paste_c(canvas, spr, x + ox, y + oy - 40 * (1 - k), prog(q, ti, ti + .12), 1.15 - .15 * k)
        pk = prog(q, ti + .2, ti + .3)
        if pk > 0: put(canvas, sphere(11, (200, 40, 35)), x + ox, y + oy - spr.height / 2 + 18, pk)
    if q > 2.25:                                                                # red string connecting the evidence
        k = e_io(prog(q, 2.25, 2.9)); pts = [(470, 300), (960, 250), (1460, 330), (1440, 720), (520, 690)]
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = len(segs) * k
        for i, (a, b) in enumerate(segs):
            f = max(0, min(1, tot - i))
            if f > 0: d.line((a[0] + ox, a[1] + oy - 120, a[0] + ox + (b[0] - a[0]) * f, a[1] + oy - 120 + (b[1] - a[1]) * f), fill=(190, 30, 30, 220), width=4)
    if q > 2.0: marker_circle(d, 1440 + ox, 730 + oy, 210, 120, prog(q, 2.0, 2.45), seed=1)
    if q > 2.45: marker_circle(d, 1460 + ox, 330 + oy, 190, 230, prog(q, 2.45, 2.9), seed=2)
    out = canvas.rotate(rot, Image.BICUBIC, center=(canvas.width / 2, canvas.height / 2))
    cw, chh = W / z, H / z; x0 = (out.width - cw) / 2; y0 = (out.height - chh) / 2
    img.paste(out.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + chh)), (0, 0))
    tt = 3.1                                                                    # title: highlighter strip + stamp
    if q >= tt:
        a = prog(q, tt, tt + .1); hk = e_out(prog(q, tt, tt + .35)); dd = ImageDraw.Draw(img)
        dd.rectangle((W / 2 - 860 * hk, 430, W / 2 + 860 * hk, 640), fill=(255, 205, 40, int(225 * a)))
        title = L('WHY IS GOLD SO EXPENSIVE?', 'Gold ఎందుకు ఇంత costly?')
        f = ffont('bebas', 190) if not TE else ffont('baloo', 120)
        sc = 1.35 - .35 * e_out(prog(q, tt + .05, tt + .25))
        tim = Image.new('RGBA', (1800, 260), (0, 0, 0, 0)); ImageDraw.Draw(tim).text((900, 130), title, font=f, fill=(18, 16, 14), anchor='mm')
        put(img, tim, W / 2, 535, prog(q, tt + .05, tt + .12), sc)
    ts = 3.9
    if q >= ts:
        sub = L('IT CAME FROM SPACE', 'అది space నుంచి వచ్చింది'); n = int(len(sub) * prog(q, ts, ts + 1.1))
        txt = sub[:n] + ('_' if int(q * 4) % 2 == 0 and n < len(sub) else '')
        tb = Image.new('RGBA', (1400, 90), (0, 0, 0, 0)); ImageDraw.Draw(tb).text((700, 45), txt, font=(font('mono', 54) if not TE else font('tesans', 50)), fill=(25, 22, 18), anchor='mm')
        put(img, tb, W / 2, 712)
    gr = np.random.default_rng(int(v * 30)).normal(0, 9, (H // 4, W // 4)).astype(np.int16)    # film grain
    gim = Image.fromarray(np.clip(128 + gr, 0, 255).astype(np.uint8)).resize((W, H), Image.NEAREST).convert('RGBA'); gim.putalpha(26)
    img.alpha_composite(gim)
    if q > dur - .35: img.alpha_composite(Image.new('RGBA', (W, H), (10, 10, 10, int(255 * prog(q, dur - .35, dur)))))
GFX['jhintro'] = g_jhintro

_SFX0 = SFX_EVENTS
def SFX_EVENTS(s, t0, t1):
    if s['kind'] != 'jhintro': return _SFX0(s, t0, t1)
    E = [('paper_slide', t0 - .05, .35)] + [('pin_push', t0 + ti + .22, .45) for _, _, _, _, ti in JH] + [('paper_drop', t0 + ti, .25) for _, _, _, _, ti in JH]
    E += [('marker', t0 + 2.0, .35), ('marker', t0 + 2.45, .3), ('scribble', t0 + 2.25, .2), ('stamp', t0 + 3.15, .55), ('boom_impact', t0 + 3.15, .45),
          ('typing_run', t0 + 3.9, .3), ('woosh_deep', t1 - .5, .3)]
    return E
