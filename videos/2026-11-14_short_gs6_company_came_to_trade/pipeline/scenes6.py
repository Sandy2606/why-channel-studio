
# ------------------------------------------------------------------ GS 6/6 specific
EV6 = '/home/claude/gs6/src/'
SRC.update({'HAYMAN': (EV6 + 'hayman_clive_mir_jafar.jpg', None), 'CHINTZ': (ARC + '21a_PD20_Chintz_wall_panel_MET.jpg', None),
            'RUPEE': (ARC + '10_PD18a_Silver_Rupee_Aurangzeb_Surat_AH1109.jpg', (1140, 1012, 2454, 2326))})
KC = 'C' if has('C') else 'C2'; KC1 = 'C' if has('C') else 'C1'
AB = L('≈ ', 'దాదాపు ')   # Telugu fonts have no ≈ / → glyphs: spelled out
SEPOY = (255, 178, 36); EURO = (236, 228, 208); NAWAB = (176, 120, 88); CAV = (196, 146, 108); DIM = (92, 88, 82)

# the season line: permission -> taxes
RAIL = [('1608', L('ASKED', 'అనుమతి కోరారు')), ('1613', L('APPROVED', 'ఆమోదం')), ('1686', L('WAR LOST', 'యుద్ధం ఓటమి')), ('1717', L('FARMAN', 'ఫర్మానా')),
        ('1740s', L('WARS', 'యుద్ధాలు')), ('1757', L('PLASSEY', 'ప్లాసీ')), ('1765', L('TAXES', 'పన్నులు'))]
def rail_strip(img, upto, a=1.0, y=300, k_last=1.0):
    """compact season line at the top: filled up to mark `upto`; only the newest label is spelled out"""
    if a <= .01: return
    x0, x1 = 110, W - 110; xs = [lerp(x0, x1, i / (len(RAIL) - 1)) for i in range(len(RAIL))]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((40, y - 62, W - 40, y + 56), 16, fill=(14, 13, 11, int(190 * a)))
    d.line((x0, y, x1, y), fill=(110, 100, 80, int(220 * a)), width=4)
    xf = lerp(xs[max(0, upto - 1)], xs[upto], k_last) if upto > 0 else xs[0]
    d.line((x0, y, xf, y), fill=GOLD_A + (int(255 * a),), width=6)
    for i, x in enumerate(xs):
        on = i < upto or (i == upto and k_last > .5); col = (AMBER if i == len(RAIL) - 1 else CREAM) if on else (90, 84, 74)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col + (int(255 * a),), outline=(20, 18, 14, int(255 * a)), width=2)
    img.paste(lay, (0, 0), lay)
    for i, (yr, lab) in enumerate(RAIL):
        on = i < upto or (i == upto and k_last > .5)
        small(img, yr, xs[i], y + 32, 27, PARCH if on else (120, 112, 98), 'mm', a)
    i = upto; yr, lab = RAIL[i]; small(img, lab, min(max(xs[i], 160), W - 160), y - 36, 34 if not TE else 30, AMBER if i == len(RAIL) - 1 else CREAM, 'mm', a * clamp(k_last * 2))
    LY.reg('card', (x0 - 20, y - 52, x1 + 20, y + 48), owner='season line')

# ---- 9-11 · Plassey as a counted diagram (1 dot ~ 500 men) on a battlefield that fills the frame; the cavalry separates; then Hayman
# Layout v3 (full-frame direction): the small Company force sits high, the Nawab's army fills the field down to the bottom edge.
# Text stays out of the platform overlays (no labels below y 1540 or in the right-hand button column).
GX0, GY0, GSX, GSY = 162, 872, 84, 104
def nawab_dots():
    return [(GX0 + c * GSX, GY0 + r * GSY, c < 4 and r < 8) for r in range(10) for c in range(10)]   # 32 cavalry dots ~ 16,000
def dots_layer(img, pts):
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x, y, r, col, a in pts:
        if 1392 < y < 1500: a *= .55     # under the caption line: softer, so captions stay clear
        if a > .01 and r > .5: d.ellipse(((x - r) * 2, (y - r) * 2, (x + r) * 2, (y + r) * 2), fill=col + (int(255 * a),), outline=(20, 16, 12, int(255 * a)), width=3)
    lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)
def field_ground(img, t, k, y0=790, vp=(540, 520)):
    """muted-earth battlefield from the horizon to the bottom edge; faint furrows drift toward the viewer"""
    if k <= .01: return
    yy = np.arange(H, dtype=np.float32)[:, None]; g = np.clip((yy - y0) / (H - y0), 0, 1)
    base = np.asarray(img).astype(np.float32); earth = np.array([58, 48, 34], np.float32)
    m = ((g > 0) * (.35 + .4 * g) * k)[:, 0]; m = np.repeat(m[:, None], W, 1)
    img.paste(Image.fromarray((base * (1 - m[..., None]) + earth * m[..., None]).clip(0, 255).astype(np.uint8)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((0, y0, W, y0), fill=GOLD_A + (int(90 * k),), width=2)
    for i in range(14):                                   # furrows: horizontal bands that slide down slowly (perspective spacing)
        f = ((i + (t * .18) % 1.0) / 14); y = y0 + (H - y0) * f ** 1.6
        d.line((0, y, W, y), fill=(92, 78, 56, int(80 * k * f)), width=2)
    for i in range(-6, 7):                                # radial lines from the horizon
        d.line((vp[0] + i * 40, y0, vp[0] + i * 260, H), fill=(92, 78, 56, int(44 * k)), width=2)
    img.paste(lay, (0, 0), lay)
def s_plassey(t, s0, s1):
    c3 = AT('B', 'three', 'మూడు') - .1; ctr = AT('B', 'troops', 'సైనికులు…') - .05; c50 = AT('B', 'fifty', 'యాభై') - .1
    cnv = AT(KC1, 'never', 'యుద్ధమే') - .1; cmj = AT(KC1, 'Mir', 'మీర్') - .1; chp = AT(KC1, 'helped', 'కంపెనీ') - .15
    if t >= chp: return s_hayman(t, chp, s1)
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, s0, s0 + .4))
    field_ground(img, t, e_io(prog(t, s0 + .2, s0 + 2.5)))
    plate_text(img, (150, 280, W - 150, 420), L('23 JUNE 1757 · BENGAL', '1757 జూన్ 23 · బెంగాల్'), L('PLASSEY', 'ప్లాసీ'), k, 62, owner='plassey')
    small(img, L('1 DOT ≈ 500 MEN · ESTIMATES: NATIONAL ARMY MUSEUM', '1 చుక్క = దాదాపు 500 మంది'), W / 2, 454, 30, PARCH, 'mm', k)
    # the two sides are named first (no numbers until the narration gives them)
    ksC = e_out(prog(t, s0 + 1.0, s0 + 1.6)) * (1 - e_out(prog(t, c3 + .2, c3 + .5))); ksN = e_out(prog(t, s0 + 1.6, s0 + 2.2)) * (1 - e_out(prog(t, c50 + .3, c50 + .6)))
    for kk_, lab, yb in ((ksC, L("THE COMPANY'S ARMY", 'కంపెనీ సైన్యం'), 528), (ksN, L("THE NAWAB OF BENGAL'S ARMY", 'బెంగాల్ నవాబు సైన్యం'), 822)):
        if kk_ > .01:
            small(img, lab, W / 2, yb, 38 if not TE else 34, CREAM, 'mm', kk_)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay); wv = 360 * e_io(clamp(prog(t, s0 + 1.0, s0 + 4.0)))
            dd.line((W / 2 - wv, yb + 34, W / 2 + wv, yb + 34), fill=GOLD_A + (int(200 * kk_),), width=3); img.paste(lay, (0, 0), lay)
    # the Nawab's army marches up into the field from the bottom edge on "fifty thousand"; the cavalry block separates on "never fought"
    kn = prog(t, c50, c50 + 1.6); aside = e_io(prog(t, cnv, cnv + 1.4)); pts = []
    for i, (x, y, cav) in enumerate(nawab_dots()):
        r_, c_ = divmod(i, 10); kk = e_out(clamp((kn * 1.4 - (9 - r_) / 14 - c_ / 60) * 2.2))
        col = tuple(int(lerp(a_, b_, aside)) for a_, b_ in zip(CAV, DIM)) if cav else NAWAB
        dx = -110 * aside if cav else 46 * aside; dy = (1 - kk) * 420 + (34 * aside if cav else 0)
        pts.append((x + dx, y + dy, 26, col, kk if kk > .01 else 0))
    dots_layer(img, pts)
    small(img, L("THE NAWAB'S ARMY ≈ 50,000", 'నవాబు సైన్యం: దాదాపు 50,000'), W / 2, 822, 38 if not TE else 34, CREAM, 'mm', e_out(prog(t, c50 + .4, c50 + .9)))
    if aside > .01:
        map_label(img, L('CAVALRY ≈ 16,000', 'అశ్వికదళం 16,000'), GX0 - 110 + 126, GY0 + 34 + 3.5 * GSY, 30 if not TE else 28, INK, aside)
        plate_text(img, (70, 480, W - 70, 760), L("MIR JAFAR · COMMANDER OF THE CAVALRY", 'మీర్ జాఫర్ · అశ్వికదళ సేనాని'), L('HIS CAVALRY STOOD ASIDE', 'అతని అశ్వికదళం యుద్ధానికి దిగలేదు'),
                   e_out(prog(t, cmj, cmj + .35)) * aside, 54 if not TE else 46, owner='mir jafar', sub=L('SOURCE: NATIONAL ARMY MUSEUM', 'ఆధారం: నేషనల్ ఆర్మీ మ్యూజియం'))
    # the Company: 6 dots (~3,000): ~2,100 Indian sepoys + ~800 Europeans, high in the frame
    ka = 1 - e_io(prog(t, cnv - .1, cnv + .5))
    if ka > .01:
        kc = prog(t, c3, c3 + .6); ks = e_out(prog(t, ctr, ctr + .5)); y = 590; xs = [W / 2 - 175 + i * 70 for i in range(6)]
        dots_layer(img, [(x, y, 24 * min(1, e_back(clamp(kc * 2 - i * .15))), tuple(int(lerp(EURO[j], (SEPOY if i < 4 else EURO)[j], ks)) for j in range(3)), ka) for i, x in enumerate(xs)])
        small(img, L('THE COMPANY ≈ 3,000', 'కంపెనీ: దాదాపు 3,000'), W / 2, 528, 38 if not TE else 34, CREAM, 'mm', ka * e_out(prog(t, c3 + .2, c3 + .7)))
        if ks > .01:
            small(img, L('≈ 2,100 INDIAN SEPOYS  ·  ≈ 800 EUROPEANS', 'దాదాపు 2,100 భారతీయ సిపాయిలు · 800 యూరోపియన్లు'), W / 2, 648, 30, SEPOY, 'mm', ka * ks)
            plate_text(img, (60, 684, W - 60, 756), None, L('MOST COMPANY TROOPS WERE INDIAN SEPOYS', 'కంపెనీ సైనికుల్లో ఎక్కువమంది భారతీయ సిపాయిలే'), ka * ks, 32 if not TE else 28, owner='sepoys')
    return img

def s_hayman(t, c0, s1):
    """after Plassey: Francis Hayman, Clive meeting Mir Jafar (c. 1760), full frame height on native pixels (1.0 source px per output px),
    panning from Clive to Mir Jafar; plates sit on the picture with their own ink backing"""
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, c0, c0 + .35))
    im = NAT('HAYMAN'); u = e_io(prog(t, c0, s1 + .5)); cx = lerp(.44, .60, u) * im.width
    crop = im.crop((int(cx - W / 2), 0, int(cx - W / 2) + W, im.height)); y0 = (H - im.height) // 2
    m = Image.new('L', crop.size, int(255 * k)); img.paste(crop, (0, y0), m)
    plate_text(img, (90, 270, W - 90, 456), L('1757 · THE COMPANY HELPED', '1757 · కంపెనీ సాయంతో'), L("MIR JAFAR ON BENGAL'S THRONE", 'బెంగాల్ నవాబుగా మీర్ జాఫర్'), k, 52 if not TE else 46, owner='new nawab')
    plate_text(img, (90, 1268, W - 90, 1376), None, L('FRANCIS HAYMAN · CLIVE MEETING MIR JAFAR · c. 1760', 'ఫ్రాన్సిస్ హేమన్ · క్లైవ్, మీర్ జాఫర్ · c. 1760'), k, 26 if not TE else 24, owner='hayman credit',
               sub=L('NATIONAL PORTRAIT GALLERY · PUBLIC DOMAIN', 'నేషనల్ పోర్ట్రెయిట్ గ్యాలరీ · పబ్లిక్ డొమైన్'))
    return img

# ---- 13 · the payoff: imported silver bullion -> Indian revenue buys the same cloth
def bars(img, x, y, k, n=4, bw=150, bh=46):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n):
        for j in range(n - i):
            bx = x - (n - i) * (bw + 8) / 2 + j * (bw + 8); by = y - i * (bh + 2)
            d.polygon([(bx, by + bh), (bx + bw, by + bh), (bx + bw - 16, by), (bx + 16, by)], fill=(206, 210, 214, int(255 * k)), outline=(60, 62, 66, int(255 * k)))
            d.line((bx + 20, by + 7, bx + bw - 22, by + 7), fill=(244, 246, 248, int(200 * k)), width=3)
    img.paste(lay, (0, 0), lay)
def fields(img, x, y, k):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(6):
        d.rounded_rectangle((x - 330 + i * 110, y - 32, x - 230 + i * 110, y + 32), 8, fill=((150, 160, 96) if i % 2 else (176, 170, 104)) + (int(255 * k),), outline=(40, 38, 26, int(255 * k)), width=2)
    img.paste(lay, (0, 0), lay)
def stream(img, t, p0, p1, rate, col, k, size=9, seed=1, spread=26, shape='dot'):
    if rate <= .01 or k <= .01: return
    rng = np.random.default_rng(seed); n = int(28 * rate) + 1; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    off = rng.uniform(-spread, spread, 60); ph = rng.uniform(0, 1, 60)
    for i in range(n):
        f = (t * .5 + ph[i]) % 1.0; x = lerp(p0[0], p1[0], f) + off[i]; y = lerp(p0[1], p1[1], f); al = math.sin(math.pi * f) * k * (.3 if 1392 < y < 1500 else 1)
        if shape == 'bar': d.rounded_rectangle((x - size * 1.6, y - size * .7, x + size * 1.6, y + size * .7), 3, fill=col + (int(240 * al),), outline=(40, 40, 44, int(200 * al)), width=2)
        else: d.ellipse((x - size, y - size, x + size, y + size), fill=col + (int(240 * al),), outline=(40, 30, 10, int(200 * al)), width=2)
    img.paste(lay, (0, 0), lay)
def bengal_fields(img, t, k, lit, y0=1480):
    """Bengal's fields fill the bottom of the frame (perspective strips); dim before 1765, lit after"""
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rows = 7
    for r in range(rows):
        f0, f1 = r / rows, (r + 1) / rows; ya = y0 + (H - y0) * f0 ** 1.3; yb = y0 + (H - y0) * f1 ** 1.3 - 4
        n = 5 + r; wdt = lerp(780, 1400, f1); x0 = W / 2 - wdt / 2
        for c in range(n):
            xa = x0 + c * wdt / n + 3; xb = x0 + (c + 1) * wdt / n - 3
            base = (118, 122, 80) if (r + c) % 2 else (138, 130, 86); dim = (62, 56, 42)
            col = tuple(int(lerp(dim[j], base[j], lit)) for j in range(3))
            d.polygon([(xa, ya), (xb, ya), (xb + (xb - W / 2) * .06, yb), (xa + (xa - W / 2) * .06, yb)], fill=col + (int(230 * k),))
    img.paste(lay, (0, 0), lay)
    small(img, L('BENGAL', 'బెంగాల్'), 70, y0 + 40, 30, (int(lerp(140, 214, lit)), int(lerp(134, 196, lit)), int(lerp(110, 120, lit))), 'lm', k)
def s_payoff(t, s0, s1):
    c_sil = AT(KC, 'silver', 'వెండి') - .15; c_after = AT(KC, 'After', 'తర్వాత,') - .15; c_end = AT(KC, 'collected', 'పన్నులతోనే') - .1
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.5, reach=.95).copy(); k = e_out(prog(t, s0, s0 + .4))
    sw = e_io(prog(t, c_after, c_after + 1.6))        # 0 = silver era, 1 = revenue era
    # top: what the Company bought (spices first, then cloth) -> the season line reaches TAXES -> the closing card
    ki = k * (1 - e_io(prog(t, c_after - .6, c_after - .2)))
    if ki > .01: plate_text(img, (70, 290, W - 70, 470), L("THE COMPANY'S TRADE", 'కంపెనీ వ్యాపారం'), L('EARLY: SPICES → BY THE LATE 1600s: TEXTILES A MAJOR TRADE', 'మొదట సుగంధ ద్రవ్యాలు · 1600ల చివరికి వస్త్రాలే పెద్ద వ్యాపారం'), ki, 38 if not TE else 34, owner='spices')
    kr_ = e_out(prog(t, c_after - .2, c_after + .3)) * (1 - e_io(prog(t, c_end - .3, c_end)))
    if kr_ > .01: rail_strip(img, 6, kr_, 380, k_last=sw)
    kf = e_out(prog(t, c_end, c_end + .4))
    if kf > .01: plate_text(img, (50, 280, W - 50, 500), L('THE SAME CLOTH', 'అదే వస్త్రం'), L("BOUGHT WITH IMPORTED SILVER → INCREASINGLY WITH INDIA'S OWN REVENUE", 'దిగుమతి వెండితో కొన్నది… క్రమంగా ఇక్కడి పన్నులతోనే'), kf, 36 if not TE else 39, owner='payoff')
    # Bengal's fields fill the bottom of the frame from the start; they light up and pay after 1765
    kr = e_out(prog(t, c_after + .2, c_after + .9)); bengal_fields(img, t, k, sw)
    # Europe's silver, as bullion (shrinks after 1765)
    kb = e_out(prog(t, s0, c_sil + .3)); bars(img, W / 2, 650 - 60 * (1 - kb), kb * (1 - .6 * sw))
    small(img, L('IMPORTED SILVER (BULLION)', 'దిగుమతి చేసిన వెండి కడ్డీలు'), W / 2, 738, 34 if not TE else 30, (214, 218, 222), 'mm', kb * (1 - .5 * sw))
    # the cloth (real Indian chintz, native pixels)
    # the cloth leaves for Europe
    stream(img, t + .3, (W - 230, 830), (W - 130, 580), .6 * kb, (196, 150, 96), k, 11, 2, 18, 'bar')
    small(img, L('CLOTH TO EUROPE', 'యూరప్‌కు వస్త్రం'), W - 60, 524, 30, (214, 176, 120), 'rm', kb)
    cb = (110, 790, W - 110, 1180); panel_nat(img, 'CHINTZ', cb, prog(t, s0, s1), (.38, .45), (.46, .52), sc=.5, radius=10, a=k)
    small(img, L('INDIAN CHINTZ · THE MET (CC0)', 'భారతీయ చింట్జ్ · ది మెట్ (CC0)'), cb[0], 1210, 28, PARCH, 'lm', k)
    # flows: silver bars down into the cloth (thin after 1765); revenue coins up from Bengal's fields (after 1765)
    stream(img, t, (W / 2, 762), (W / 2, cb[1] + 60), (1 - .8 * sw) * kb, (214, 218, 222), k, 13, 1, 180, 'bar')
    stream(img, t * 1.4, (W / 2 + 330, 1700), (W / 2 + 260, cb[3] - 60), sw, AMBER, kr, 16, 3, 50)
    stream(img, t * 1.1 + .4, (W / 2 + 200, 1790), (W / 2 + 230, cb[3] - 40), sw * .7, AMBER, kr, 13, 5, 30)
    if kr > .01:
        panel_nat(img, 'RUPEE', (96, 1232, 246, 1382), 0, (.5, .5), (.5, .5), sc=150 / 1314, radius=75, a=kr, tint=(330, 330, 330))
        small(img, L('BENGAL REVENUE (TAXES)', 'బెంగాల్ పన్నుల ఆదాయం'), 272, 1262, 34 if not TE else 30, AMBER, 'lm', kr, 420)
        small(img, L('AFTER 1765', '1765 తర్వాత'), 272, 1302, 28, CREAM, 'lm', kr, 420)
        small(img, L('COIN: ILLUSTRATIVE RUPEE', 'నాణెం: ఉదాహరణ మాత్రమే'), 272, 1340, 26, PARCH, 'lm', kr, 440)
        small(img, L('MINTED IN SURAT, INDIA', 'సూరత్‌లో ముద్రించినది'), 272, 1374, 26, PARCH, 'lm', kr, 440)
    return img

# ---- 14 · the completed season line and the question
def s_question(t, s0, s1):
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, s0, s0 + .4))
    x = 250; y0, y1 = 560, 1330; ys = [lerp(y0, y1, i / (len(RAIL) - 1)) for i in range(len(RAIL))]; kf = e_io(prog(t, s0, s0 + 1.4))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((x, y0, x, y1), fill=(110, 100, 80, int(230 * k)), width=5); d.line((x, y0, x, lerp(y0, y1, kf)), fill=GOLD_A + (int(255 * k),), width=8)
    for i, yy in enumerate(ys):
        on = kf >= i / (len(RAIL) - 1) - .01; col = (AMBER if i == len(RAIL) - 1 else CREAM) if on else (90, 84, 74)
        d.ellipse((x - 16, yy - 16, x + 16, yy + 16), fill=col + (int(255 * k),), outline=(20, 18, 14, int(255 * k)), width=3)
    # the line runs on past 1765, down through the frame and off the bottom edge: the story continues (Season 2)
    kd = e_io(prog(t, s0 + 1.2, s0 + 2.6)); yd = lerp(y1, H, kd)
    for yy_ in range(int(y1 + 24), int(yd), 36): d.line((x, yy_, x, min(yy_ + 20, yd)), fill=AMBER + (int(200 * k * (1 - (yy_ - y1) / (H - y1) * .6)),), width=6)
    if kd > .01:
        yp = y1 + ((t - s0) * 240) % (H - y1); d.ellipse((x - 10, yp - 10, x + 10, yp + 10), fill=AMBER + (int(220 * k * kd),))
    img.paste(lay, (0, 0), lay)
    for i, (yr, lab) in enumerate(RAIL):
        on = kf >= i / (len(RAIL) - 1) - .01
        text(img, yr, x - 40, ys[i], 40, PARCH if on else (120, 112, 98), 'rm', 'monob', k, None, None)
        text(img, lab, x + 46, ys[i], 48 if not TE else 50, (AMBER if i == len(RAIL) - 1 else CREAM) if on else (120, 112, 98), 'lm', 'head', k, W - x - 120, None)
    LY.reg('card', (x - 160, y0 - 30, W - 80, y1 + 30), owner='season line')
    plate_text(img, (70, 270, W - 70, 480), L('1608 → 1765', '1608 - 1765'), L('WHAT HAPPENS WHEN A TRADING COMPANY COLLECTS THE TAXES?', 'వ్యాపార కంపెనీ పన్నులు వసూలు చేస్తే ఏమవుతుంది?'), e_out(prog(t, s0 + .1, s0 + .6)), 42 if not TE else 40, owner='question')
    return img

