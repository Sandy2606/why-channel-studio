
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
    d.line((x0, y, x1, y), fill=(110, 100, 80, int(220 * a)), width=4)
    xf = lerp(xs[max(0, upto - 1)], xs[upto], k_last) if upto > 0 else xs[0]
    d.line((x0, y, xf, y), fill=GOLD_A + (int(255 * a),), width=6)
    for i, x in enumerate(xs):
        on = i < upto or (i == upto and k_last > .5); col = (AMBER if i == len(RAIL) - 1 else CREAM) if on else (90, 84, 74)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col + (int(255 * a),), outline=(20, 18, 14, int(255 * a)), width=2)
    img.paste(lay, (0, 0), lay)
    for i, (yr, lab) in enumerate(RAIL):
        on = i < upto or (i == upto and k_last > .5)
        small(img, yr, xs[i], y + 32, 25, PARCH if on else (120, 112, 98), 'mm', a)
    i = upto; yr, lab = RAIL[i]; small(img, lab, min(max(xs[i], 160), W - 160), y - 36, 32 if not TE else 30, AMBER if i == len(RAIL) - 1 else CREAM, 'mm', a * clamp(k_last * 2))
    LY.reg('card', (x0 - 20, y - 52, x1 + 20, y + 48), owner='season line')

# ---- 9-11 · Plassey as a counted diagram (1 dot ~ 500 men), then Mir Jafar's cavalry stands aside, then Hayman
GX0, GY0, GS = 279, 588, 58   # GS 6/6 layout v2: the diagram fills the working area (y 260-1400)
def nawab_dots():
    return [(GX0 + c * GS, GY0 + r * GS, c < 4 and r < 8) for r in range(10) for c in range(10)]   # 32 cavalry dots ~ 16,000
def dots_layer(img, pts):
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x, y, r, col, a in pts:
        if a > .01 and r > .5: d.ellipse(((x - r) * 2, (y - r) * 2, (x + r) * 2, (y + r) * 2), fill=col + (int(255 * a),), outline=(20, 16, 12, int(255 * a)), width=3)
    lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)
def s_plassey(t, s0, s1):
    c3 = AT('B', 'three', 'మూడు') - .1; ctr = AT('B', 'troops', 'సైనికులు…') - .05; c50 = AT('B', 'fifty', 'యాభై') - .1
    cnv = AT(KC1, 'never', 'యుద్ధమే') - .1; cmj = AT(KC1, 'Mir', 'మీర్') - .1; chp = AT(KC1, 'helped', 'కంపెనీ') - .15
    if t >= chp: return s_hayman(t, chp, s1)
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, s0, s0 + .4))
    plate_text(img, (150, 296, W - 150, 440), L('23 JUNE 1757 · BENGAL', '1757 జూన్ 23 · బెంగాల్'), L('PLASSEY', 'ప్లాసీ'), k, 62, owner='plassey')
    small(img, L('1 DOT ≈ 500 MEN · NATIONAL ARMY MUSEUM ESTIMATES', '1 చుక్క = దాదాపు 500 మంది'), W / 2, 482, 27, MUTED, 'mm', k)
    # the two sides are set up first (no numbers until the narration gives them)
    ksN = e_out(prog(t, s0 + .5, s0 + 1.1)) * (1 - e_out(prog(t, c50 + .3, c50 + .6))); ksC = e_out(prog(t, s0 + 1.4, s0 + 2.0)) * (1 - e_out(prog(t, c3 + .2, c3 + .5)))
    # two camps: soft ground panels fade in slowly (motion before the numbers arrive)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    for (x0_, y0_, x1_, y1_), ka_ in (((GX0 - 160, GY0 - 40, GX0 + 9 * GS + 50, GY0 + 9 * GS + 34), e_io(prog(t, s0 + .4, s0 + 5.0))), ((W / 2 - 230, 1180, W / 2 + 230, 1250), e_io(prog(t, s0 + 1.4, s0 + 5.5)))):
        dd.rounded_rectangle((x0_, y0_, x1_, y1_), 18, fill=(70, 58, 40, int(70 * ka_ * k)))
    img.paste(lay, (0, 0), lay)
    for kk_, lab, yb in ((ksN, L("THE NAWAB OF BENGAL'S ARMY", 'బెంగాల్ నవాబు సైన్యం'), GY0 - 48), (ksC, L("THE COMPANY'S ARMY", 'కంపెనీ సైన్యం'), 1160)):
        if kk_ > .01:
            small(img, lab, W / 2, yb, 38 if not TE else 34, CREAM, 'mm', kk_)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay); wv = 380 * e_io(clamp(prog(t, s0 + .5, s0 + 3.5)))
            dd.line((W / 2 - wv, yb + 34, W / 2 + wv, yb + 34), fill=GOLD_A + (int(200 * kk_),), width=3); img.paste(lay, (0, 0), lay)
    kn = prog(t, c50, c50 + 1.2); aside = e_io(prog(t, cnv, cnv + 1.0)); pts = []
    for i, (x, y, cav) in enumerate(nawab_dots()):
        kk = e_back(clamp((kn * 1.25 - (i % 10 + i // 10) / 24) * 3))
        col = tuple(int(lerp(a_, b_, aside)) for a_, b_ in zip(CAV, DIM)) if cav else NAWAB
        pts.append((x - (120 * aside if cav else 0), y, 20 * min(1, kk), col, 1.0 if kk > .01 else 0))
    dots_layer(img, pts)
    small(img, L("THE NAWAB'S ARMY ≈ 50,000", 'నవాబు సైన్యం: దాదాపు 50,000'), W / 2, GY0 - 48, 38 if not TE else 34, CREAM, 'mm', e_out(prog(t, c50 + .3, c50 + .8)))
    if aside > .01:
        map_label(img, L('CAVALRY ≈ 16,000', 'అశ్వికదళం 16,000'), GX0 - 120 + 87, GY0 + 3.5 * GS, 30 if not TE else 28, INK, aside)
        plate_text(img, (70, 1150, W - 70, 1390), L("MIR JAFAR · COMMANDER OF THE CAVALRY", 'మీర్ జాఫర్ · అశ్వికదళ సేనాని'), L('HIS CAVALRY STOOD ASIDE', 'అతని అశ్వికదళం యుద్ధానికి దిగలేదు'),
                   e_out(prog(t, cmj, cmj + .35)) * aside, 50 if not TE else 44, owner='mir jafar', sub=L('SOURCE: NATIONAL ARMY MUSEUM', 'ఆధారం: నేషనల్ ఆర్మీ మ్యూజియం'))
    # the Company: 6 dots (~3,000): ~2,100 Indian sepoys + ~800 Europeans
    ka = 1 - e_io(prog(t, cnv - .1, cnv + .5))
    if ka > .01:
        kc = prog(t, c3, c3 + .6); ks = e_out(prog(t, ctr, ctr + .5)); y = 1214; xs = [W / 2 - 185 + i * 74 for i in range(6)]
        dots_layer(img, [(x, y, 24 * min(1, e_back(clamp(kc * 2 - i * .15))), tuple(int(lerp(EURO[j], (SEPOY if i < 4 else EURO)[j], ks)) for j in range(3)), ka) for i, x in enumerate(xs)])
        small(img, L('THE COMPANY ≈ 3,000', 'కంపెనీ: దాదాపు 3,000'), W / 2, y - 54, 38 if not TE else 34, CREAM, 'mm', ka * e_out(prog(t, c3 + .2, c3 + .7)))
        if ks > .01:
            small(img, L('≈ 2,100 INDIAN SEPOYS', 'దాదాపు 2,100 భారతీయ సిపాయిలు'), W / 2, y + 54, 32, SEPOY, 'mm', ka * ks)
            small(img, L('≈ 800 EUROPEANS', 'దాదాపు 800 యూరోపియన్లు'), W / 2, y + 92, 28, EURO, 'mm', ka * ks)
            plate_text(img, (60, 1328, W - 60, 1396), None, L('MOST COMPANY TROOPS WERE INDIAN SEPOYS', 'కంపెనీ సైనికుల్లో ఎక్కువమంది భారతీయ సిపాయిలే'), ka * ks, 30 if not TE else 28, owner='sepoys')
    return img

def s_hayman(t, c0, s1):
    """after Plassey: Francis Hayman, Clive meeting Mir Jafar (c. 1760), on native pixels"""
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, c0, c0 + .35))
    plate_text(img, (90, 290, W - 90, 476), L('1757 · THE COMPANY HELPED', '1757 · కంపెనీ సాయంతో'), L("MIR JAFAR ON BENGAL'S THRONE", 'బెంగాల్ నవాబుగా మీర్ జాఫర్'), k, 52 if not TE else 46, owner='new nawab')
    panel_nat(img, 'HAYMAN', (60, 500, W - 60, 1250), prog(t, c0, s1), (.46, .5), (.54, .5), sc=.42, radius=12, a=k)
    small(img, L('FRANCIS HAYMAN · CLIVE MEETING MIR JAFAR · c. 1760', 'ఫ్రాన్సిస్ హేమన్ · క్లైవ్, మీర్ జాఫర్ · c. 1760'), W / 2, 1296, 30, PARCH, 'mm', k, ST.sw - 40)
    small(img, L('NATIONAL PORTRAIT GALLERY · PUBLIC DOMAIN', 'నేషనల్ పోర్ట్రెయిట్ గ్యాలరీ · పబ్లిక్ డొమైన్'), W / 2, 1340, 26, MUTED, 'mm', k, ST.sw - 40)
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
        f = (t * .5 + ph[i]) % 1.0; x = lerp(p0[0], p1[0], f) + off[i]; y = lerp(p0[1], p1[1], f); al = math.sin(math.pi * f) * k
        if shape == 'bar': d.rounded_rectangle((x - size * 1.6, y - size * .7, x + size * 1.6, y + size * .7), 3, fill=col + (int(240 * al),), outline=(40, 40, 44, int(200 * al)), width=2)
        else: d.ellipse((x - size, y - size, x + size, y + size), fill=col + (int(240 * al),), outline=(40, 30, 10, int(200 * al)), width=2)
    img.paste(lay, (0, 0), lay)
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
    # Europe's silver, as bullion (shrinks after 1765)
    kb = e_out(prog(t, s0, c_sil + .3)) ; bars(img, W / 2, 650, kb * (1 - .6 * sw))
    small(img, L('IMPORTED SILVER (BULLION)', 'దిగుమతి చేసిన వెండి కడ్డీలు'), W / 2, 738, 34 if not TE else 30, (214, 218, 222), 'mm', kb * (1 - .5 * sw))
    # the cloth (real Indian chintz, native pixels)
    # the cloth leaves for Europe
    stream(img, t + .3, (W - 230, 830), (W - 130, 580), .6 * kb, (196, 150, 96), k, 11, 2, 18, 'bar')
    small(img, L('CLOTH TO EUROPE', 'యూరప్‌కు వస్త్రం'), W - 60, 524, 30, (214, 176, 120), 'rm', kb)
    cb = (110, 790, W - 110, 1180); panel_nat(img, 'CHINTZ', cb, prog(t, s0, s1), (.38, .45), (.46, .52), sc=.5, radius=10, a=k)
    small(img, L('INDIAN CHINTZ · THE MET (CC0)', 'భారతీయ చింట్జ్ · ది మెట్ (CC0)'), cb[0], 1210, 28, PARCH, 'lm', k)
    # flows: silver bars down into the cloth (thin after 1765); revenue coins up from Bengal's fields (after 1765)
    stream(img, t, (W / 2, 762), (W / 2, cb[1] + 60), (1 - .8 * sw) * kb, (214, 218, 222), k, 13, 1, 180, 'bar')
    ry = 1268; kr = e_out(prog(t, c_after + .2, c_after + .9)); fields(img, W / 2 - 60, ry, kr)
    stream(img, t * 1.4, (W / 2 + 60, ry - 36), (W / 2, cb[1] + 140), sw, AMBER, kr, 16, 3, 110)
    if kr > .01:
        panel_nat(img, 'RUPEE', (W - 240, ry - 80, W - 80, ry + 80), 0, (.5, .5), (.5, .5), sc=160 / 1314, radius=80, a=kr, tint=(330, 330, 330))
        small(img, L('BENGAL REVENUE (TAXES), AFTER 1765', '1765 తర్వాత: బెంగాల్ పన్నుల ఆదాయం'), W / 2 - 80, ry + 66, 32 if not TE else 29, AMBER, 'mm', kr, 760)
        small(img, L('COIN SHOWN: ILLUSTRATIVE · SILVER RUPEE MINTED IN INDIA (SURAT)', 'చూపిన నాణెం ఉదాహరణ మాత్రమే: సూరత్‌లో ముద్రించిన వెండి రూపాయి'), W / 2, ry + 108, 24, MUTED, 'mm', kr)
    return img

# ---- 14 · the completed season line and the question
def s_question(t, s0, s1):
    img = radial_bg(W, H, (34, 30, 22), (9, 9, 9), cy=.45, reach=.9).copy(); k = e_out(prog(t, s0, s0 + .4))
    x = 250; y0, y1 = 350, 1150; ys = [lerp(y0, y1, i / (len(RAIL) - 1)) for i in range(len(RAIL))]; kf = e_io(prog(t, s0, s0 + 1.4))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((x, y0, x, y1), fill=(110, 100, 80, int(230 * k)), width=5); d.line((x, y0, x, lerp(y0, y1, kf)), fill=GOLD_A + (int(255 * k),), width=8)
    for i, yy in enumerate(ys):
        on = kf >= i / (len(RAIL) - 1) - .01; col = (AMBER if i == len(RAIL) - 1 else CREAM) if on else (90, 84, 74)
        d.ellipse((x - 16, yy - 16, x + 16, yy + 16), fill=col + (int(255 * k),), outline=(20, 18, 14, int(255 * k)), width=3)
    img.paste(lay, (0, 0), lay)
    for i, (yr, lab) in enumerate(RAIL):
        on = kf >= i / (len(RAIL) - 1) - .01
        text(img, yr, x - 40, ys[i], 40, PARCH if on else (120, 112, 98), 'rm', 'monob', k, None, None)
        text(img, lab, x + 46, ys[i], 48 if not TE else 50, (AMBER if i == len(RAIL) - 1 else CREAM) if on else (120, 112, 98), 'lm', 'head', k, W - x - 120, None)
    LY.reg('card', (x - 160, y0 - 30, W - 80, y1 + 30), owner='season line')
    plate_text(img, (70, 1210, W - 70, 1396), L('1608 → 1765', '1608 - 1765'), L('WHAT HAPPENS WHEN A TRADING COMPANY COLLECTS THE TAXES?', 'వ్యాపార కంపెనీ పన్నులు వసూలు చేస్తే ఏమవుతుంది?'), e_out(prog(t, s0 + .8, s0 + 1.3)), 42 if not TE else 40, owner='question')
    return img

def s_todo(t, s0, s1, name):
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9)).copy(); text(img, f'[{name}]', W / 2, H / 2, 40, MUTED, 'mm', 'head'); return img
FUNCS = {'plassey': s_plassey, 'payoff': s_payoff, 'question': s_question}
def render(t):
    LY.reset(); name, s0, s1 = scene_at(t)
    if name.startswith('cartoon'): img = cartoon(t, s0, [('CHELLI', 'Q1')])
    elif name == 'plassey' and S('Q2') - .15 <= t < E('Q2') + .2: img = cartoon(t, S('Q2') - .15, [('CHELLI', 'Q2')]); name = 'cartoon2'
    elif name in FUNCS: img = FUNCS[name](t, s0, s1)
    else: img = s_todo(t, s0, s1, name)
    overlays(img, t, name); captions(img, t, name); return img
