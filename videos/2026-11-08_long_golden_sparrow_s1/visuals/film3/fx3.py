"""v4 pass: 2D historical scene animation for events (conflicts, negotiations, movement of goods, transfers of power)."""
import math, functools
import numpy as np, cv2
from PIL import Image, ImageDraw
import flib as FL, fx
import sprites as SP
from sprites import COMPANY, MUGHAL, FRENCH, NAWAB, PORT, INKC
from flib import W, H, put, text, eo, GOLD, PAPER, INK, MUTED
sm, lerp = fx.sm, fx.lerp
X = {}
def init(**k): X.update(k)
def cue(i, en, te): return X['cue'](i, en, te)
def L(en, te): return te if X['TE'] else en
def P(n): return X['P'][n]

def lab(fr, s, x, y, k, size=30, col=PAPER, anchor='ct', bg=True):
    if k <= 0: return
    im = text(s, 'label', size, col, maxw=560)
    if bg:
        b = Image.new('RGBA', (im.width + 26, im.height + 12), (12, 10, 16, int(185 * k))); b.alpha_composite(im, (13, 6)); im = b
    put(fr, im, x, y, k, anchor)
def path_at(pts, f):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; Lt = sum(seg) * max(0, min(1, f)); acc = 0
    for i, sg in enumerate(seg):
        if acc + sg >= Lt: q = (Lt - acc) / max(1e-6, sg); return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * q, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * q)
        acc += sg
    return pts[-1]
def arrow(d, p0, p1, k, col, w=10, a=1.0):
    if k <= 0: return
    x1, y1 = p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k
    d.line((p0[0], p0[1], x1, y1), fill=SP.A(col, 0.85 * a), width=w)
    ang = math.atan2(y1 - p0[1], x1 - p0[0])
    d.polygon([(x1 + 22 * math.cos(ang), y1 + 22 * math.sin(ang)), (x1 + 16 * math.cos(ang + 2.4), y1 + 16 * math.sin(ang + 2.4)), (x1 + 16 * math.cos(ang - 2.4), y1 + 16 * math.sin(ang - 2.4))], fill=SP.A(col, a))
def glow(fr, x, y, r, col, a):
    if a <= 0: return
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((x - r, y - r, x + r, y + r), fill=tuple(col) + (int(110 * a),))
    from PIL import ImageFilter; fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * 0.35)))
def mapfn(spec):
    return lambda t, a, b: FL.render_map(None, t, spec, a, b)
def court_bg():
    a = fx.blurred('PD08', 0.30, 1.0, .5, .3).astype(np.float32); a *= np.array([1.0, 0.9, 0.8]); return Image.fromarray(a.astype(np.uint8)).convert('RGBA')
def dark_field():
    a = fx.blurred('G30', 0.28).astype(np.float32); return Image.fromarray(a.astype(np.uint8)).convert('RGBA')

# ================================================================== 6.8b  Anglo-Mughal War, 1686-90
def s68b(t, a, b):
    i = '6.8b'
    c0 = a + 0.2; c86 = cue(i, '1686', '1686'); cA = cue(i, 'Aurangzeb', 'ఔరంగజేబుతో'); cL = cue(i, 'lost', 'ఓడిపోయింది')
    cE = cue(i, 'envoys', 'దూతలు') - 0.15; cP = cue(i, 'pardon', 'క్షమాపణ'); cF = cue(i, 'fine', 'జరిమానా'); cB = cue(i, 'promise', 'బుద్ధిగా')
    cO = cue(i, 'Only', 'అప్పుడే') - 0.15; c90 = cue(i, '1690', '1690')
    posts = [('Surat', 'Surat'), ('Bombay', 'Bombay'), ('Madras', 'Madras'), ('Machilipatnam', 'Machilipatnam'), ('Hooghly', None)]
    HOOGHLY = (88.39, 22.9)
    if cE <= t < cO:                                                    # the court: envoys, pardon, fine, promise
        fr = court_bg(); d = ImageDraw.Draw(fr); tx, ty = 1380, 860
        SP.throne(d, tx, ty, 330, 1.0)
        lab(fr, L("AURANGZEB'S COURT", 'ఔరంగజేబు దర్బారు'), tx, ty + 30, eo((t - cE) / 0.5), 28)
        for j in range(2):
            walk = sm((t - cE - 0.2 - j * 0.2) / 1.6); x = lerp(-80, 760 + j * 150, walk)
            kneel = t > cP + j * 0.15
            SP.man(d, x, ty, 230, (30, 26, 32), 1.0, hat='tricorn', musket=False, kneel=kneel)
        lab(fr, L('COMPANY ENVOYS', 'కంపెనీ దూతలు'), 860, ty + 30, eo((t - cE - 0.6) / 0.5), 28)
        if t > cP: lab(fr, L('BEG PARDON', 'క్షమాపణ'), 860, 300, eo((t - cP) / 0.4) * (1 - eo((t - cF + 0.2) / 0.3)), 40, GOLD)
        for j in range(8):
            f = (t - cF - j * 0.12) / 0.8
            if 0 < f < 1.6: SP.coin(d, lerp(900, tx - 60, sm(min(f, 1))), lerp(700, 760, sm(min(f, 1))) - 120 * math.sin(math.pi * min(f, 1)), 14, min(1, 2 - f))
        if t > cF: lab(fr, L('A HEAVY FINE', 'భారీ జరిమానా'), 860, 300, eo((t - cF) / 0.4) * (1 - eo((t - cB + 0.2) / 0.3)), 40, GOLD)
        if t > cB:
            k = eo((t - cB) / 0.5); SP.scroll(d, lerp(900, 1120, k), 560, 150, k, seals=1)
            lab(fr, L('A PROMISE TO BEHAVE', 'ఇక బుద్ధిగా ఉంటామని మాట'), 1010, 300, k, 40, GOLD)
        return fr
    def draw(out, d, V, tt):
        for j, (n, _) in enumerate(posts):
            ll = HOOGHLY if n == 'Hooghly' else P(n); x, y = V(*ll)
            k = eo((tt - c0 - j * 0.15) / 0.4)
            seized = (cL + 0.2 + j * 0.15) < tt < (cO if tt < cE else 1e9) and n in ('Surat', 'Machilipatnam', 'Hooghly')
            if tt >= cO and n in ('Surat', 'Machilipatnam', 'Hooghly'): seized = tt < cO + 0.6 + j * 0.15
            SP.factory(d, x, y, 84, COMPANY, k, seized=seized)
        # 1686: Company ships move against Mughal shipping and up the Hooghly
        k86 = eo((tt - c86) / 0.4); back = sm((tt - cL) / 1.2)
        if k86 > 0 and tt < cE:
            for (p0, p1) in ((V(72.0, 18.0), V(70.5, 21.5)), (V(89.5, 20.5), V(88.5, 22.3))):
                f = sm((tt - c86) / 2.2) * (1 - back); x, y = lerp(p0[0], p1[0], f), lerp(p0[1], p1[1], f)
                SP.ship(d, x, y, 72, a=k86 * (1 - 0.6 * back), flagcol=COMPANY)
        # Mughal pressure: big green arrows towards the Company's posts
        kA = eo((tt - cA) / 0.6)
        if kA > 0 and tt < cE + 99:
            src = V(78.0, 26.5)
            for tgt in ((72.95, 19.3), (88.2, 22.8), (72.9, 21.3)):
                q = V(*tgt); arrow(d, src, (lerp(src[0], q[0], 0.9), lerp(src[1], q[1], 0.9)), sm((tt - cA) / 1.0), MUGHAL, 14, kA * (1 - eo((tt - cO) / 0.5)) if tt > cO else kA)
        if tt > cL and tt < cE: lab(out, L('1686–90 · THE COMPANY LOSES', '1686–90 · కంపెనీ ఓటమి'), W / 2, 150, eo((tt - cL) / 0.4), 36, GOLD)
        if tt > c90:
            x, y = V(88.36, 22.57); SP.fort(d, x + 40, y + 10, 60, COMPANY, 1.0, build=sm((tt - c90) / 1.0))
            lab(out, L('CALCUTTA · 1690', 'కలకత్తా · 1690'), x + 40, y + 30, eo((tt - c90 - 0.4) / 0.4), 28)
        elif tt > cO: lab(out, L('TRADE ALLOWED AGAIN', 'మళ్లీ వ్యాపార అనుమతి'), W / 2, 150, eo((tt - cO) / 0.4), 34, GOLD)
    spec = dict(box0=(56, 101, 6, 31), box1=(57, 100, 6.5, 30.5), glows=[('Mughal empire' if not X['TE'] else 'మొఘల్ సామ్రాజ్యం', 78, 24, 8, (60, 120, 80), a)],
                pins=[], draw=draw, autoships=False)
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 6.10  Carnatic wars: companies, sepoys, rival claimants
def drill(fr, t, c, lab_):
    d = ImageDraw.Draw(fr); y0 = 560
    for blk, (col, x0) in enumerate(((FRENCH, 180), (COMPANY, 1040))):
        for r in range(3):
            for c_ in range(9):
                step = int((t - c) / 0.5) % 2; x = x0 + c_ * 74 + (12 if step else 0) * (1 if r % 2 else -1) * 0
                SP.man(d, x + (r % 2) * 30, y0 + r * 110, 120, col, eo((t - c - r * 0.1) / 0.4), hat='turban')
        SP.man(d, x0 - 80, y0 + 110, 140, (30, 26, 32), eo((t - c) / 0.4), hat='tricorn', musket=False)
    lab(fr, L('FRENCH COMPANY', 'ఫ్రెంచ్ కంపెనీ'), 520, 420, eo((t - c) / 0.4), 30, (150, 170, 240))
    lab(fr, L('ENGLISH COMPANY', 'ఇంగ్లీష్ కంపెనీ'), 1380, 420, eo((t - c) / 0.4), 30, (240, 150, 140))
    lab(fr, lab_, W / 2, 160, eo((t - c - 0.2) / 0.4), 38, GOLD)
def claimants(fr, t, c, c_first):
    d = ImageDraw.Draw(fr)
    for j, (name, x) in enumerate(((L('CARNATIC', 'కర్ణాటక'), 520), (L('HYDERABAD', 'హైదరాబాద్'), 1400))):
        k = eo((t - c - j * 0.3) / 0.5)
        SP.throne(d, x, 520, 200, k, seated=False)
        lab(fr, name, x, 540, k, 32, GOLD)
        for s_, (col, dx) in enumerate(((FRENCH, -170), (COMPANY, 170))):
            first = (col == FRENCH and t > c_first)
            kk = eo((t - c - 0.4 - j * 0.3 - s_ * 0.2) / 0.5)
            SP.man(d, x + dx, 880, 200, (40, 34, 40), kk, hat='turban', musket=False, crown=True)
            SP.flag(d, x + dx + 60, 880, 180, col, kk, t=t)
            if first: glow(fr, x + dx, 780, 120, FRENCH, eo((t - c_first) / 0.5))
    lab(fr, L('RIVAL CLAIMANTS · EACH BACKED BY A COMPANY', 'పోటీ వారసులు · ఒక్కొక్కరి వెనక ఒక కంపెనీ'), W / 2, 160, eo((t - c) / 0.4), 36, PAPER)
    if t > c_first: lab(fr, L('THE FRENCH DID IT FIRST', 'మొదట ఫ్రెంచ్ వాళ్లే'), W / 2, 220, eo((t - c_first) / 0.4), 34, (150, 170, 240))
def s610(t, a, b):
    i = '6.10'
    cW = cue(i, 'wars', 'యుద్ధాలు'); cF = cue(i, 'fought', 'పోరాడాయి'); cS = cue(i, 'They', 'సిపాయిలు') - 0.2
    cC = cue(i, 'backed', 'కర్ణాటక') - 0.3; c1 = cue(i, 'first', 'వాళ్లే')
    if cC <= t: fr = fx.dark(); claimants(fr, t, cC, c1); return fr
    if cS <= t: fr = fx.dark(); drill(fr, t, cS, L('SEPOYS · INDIAN SOLDIERS IN EUROPEAN DRILL', 'సిపాయిలు · యూరోపియన్ శిక్షణ పొందిన భారతీయ సైనికులు')); return fr
    def draw(out, d, V, tt):
        pp, pm = V(*P('Pondicherry')), V(*P('Madras'))
        glow(out, pp[0], pp[1], 260 + 30 * math.sin(tt * 2), FRENCH, eo((tt - cW) / 0.6)); glow(out, pm[0], pm[1], 260 + 30 * math.sin(tt * 2 + 1), COMPANY, eo((tt - cW) / 0.6))
        d = ImageDraw.Draw(out)
        SP.fort(d, pp[0], pp[1] + 10, 70, FRENCH, eo((tt - a) / 0.5)); SP.fort(d, pm[0], pm[1] + 10, 70, COMPANY, eo((tt - a) / 0.5))
        lab(out, L('FRENCH · PONDICHERRY', 'ఫ్రెంచ్ · పాండిచ్చేరి'), pp[0], pp[1] + 30, eo((tt - a) / 0.5), 26, (170, 190, 250))
        lab(out, L('ENGLISH · MADRAS', 'ఇంగ్లీష్ · మద్రాసు'), pm[0] + 40, pm[1] - 150, eo((tt - a) / 0.5), 26, (250, 170, 160))
        kF = eo((tt - cF) / 0.5)
        if kF > 0:
            mid = V(79.2, 12.6); f = sm((tt - cF) / 1.6)
            bx, by = lerp(pp[0] - 160, mid[0] - 150, f), lerp(pp[1] - 60, mid[1], f); rx_, ry_ = lerp(pm[0] - 40, mid[0] + 40, f), lerp(pm[1] - 60, mid[1], f)
            SP.formation(d, bx, by, 4, 2, 44, FRENCH, kF); SP.formation(d, rx_, ry_, 4, 2, 44, COMPANY, kF)
            if f > 0.8:
                for j in range(3): SP.puff(d, mid[0] - 30 + j * 30, mid[1] - 30 + 10 * math.sin(tt * 3 + j), 18, 0.5 + 0.5 * math.sin(tt * 4 + j))
            SP.swords(d, mid[0] - 10, mid[1] - 90, 50, kF)
        lab(out, L('1740s–50s · THE COMPANIES AT WAR', '1740–50లు · కంపెనీల యుద్ధాలు'), W / 2, 150, eo((tt - cW) / 0.4), 34, GOLD)
    spec = dict(box0=(70.5, 89.5, 8, 18.5), box1=(71, 89, 8.3, 18.2), pins=[('Arcot',) + P('Arcot') + (a + 0.6, 'l'), ('Hyderabad',) + P('Hyderabad') + (a + 0.8,)], draw=draw)
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 6.12  fighting the Mughals failed; choosing rulers paid
def s612(t, a, b):
    i = '6.12'; cF = cue(i, 'Fighting', 'మొఘలులతో') - 0.1; cP = cue(i, 'paid', 'లాభం') - 0.2
    if t < cF: return fx.to_rgba(fx.cam(FL.img('G28'), (t - a) / max(0.1, cF - a), (.25, .5), (.27, .5), 1.3, 1.42))
    fr = fx.dark(); d = ImageDraw.Draw(fr)
    # left: the Company against the Mughals -> failed
    k = eo((t - cF) / 0.4); SP.flag(d, 300, 640, 220, COMPANY, k, t=t)
    hit = sm((t - cF - 0.3) / 0.5); bounce = sm((t - cF - 0.8) / 0.5)
    x = lerp(360, 520, hit) - 160 * bounce; SP.formation(d, x, 560, 3, 2, 60, COMPANY, k)
    d.ellipse((600, 420, 860, 680), fill=SP.A(MUGHAL, k)); lab(fr, L('MUGHALS', 'మొఘలులు'), 730, 700, k, 30)
    if t > cF + 0.9:
        kx = eo((t - cF - 0.9) / 0.3); d.line((560, 420, 900, 760), fill=SP.A((220, 40, 34), kx), width=16); d.line((900, 420, 560, 760), fill=SP.A((220, 40, 34), kx), width=16)
        lab(fr, L('FIGHTING · FAILED', 'యుద్ధం · విఫలం'), 600, 820, kx, 32)
    # right: place a ruler -> paid
    kp = eo((t - cP) / 0.4)
    if kp > 0:
        SP.throne(d, 1440, 760, 240, kp, seated=False); SP.man(d, 1440, 730, 190, (40, 34, 40), kp, hat='turban', musket=False, crown=t > cP + 0.6)
        SP.flag(d, 1600, 760, 220, COMPANY, kp, t=t)
        for j in range(7):
            f = (t - cP - 0.8 - j * 0.12) / 0.8
            if 0 < f < 1.5: SP.coin(d, lerp(1440, 1650, sm(min(f, 1))), lerp(560, 520, sm(min(f, 1))) - 90 * math.sin(math.pi * min(f, 1)), 13, min(1, 2 - f))
        lab(fr, L('CHOOSING RULERS · PAID', 'రాజులను ఎంచుకోవడం · లాభం'), 1460, 820, eo((t - cP - 0.4) / 0.4), 32, GOLD)
    return fr

# ================================================================== 6.13  Bengal 1756
def s613(t, a, b):
    i = '6.13'; cFort = cue(i, 'fortifications', 'కోటలు'); cPass = cue(i, 'abusing', 'దుర్వినియోగం'); c56 = cue(i, '1756', '1756'); cMad = cue(i, 'sent', 'మద్రాసు') - 0.2
    MUR = (88.27, 24.18)
    def draw(out, d, V, tt):
        cx, cy = V(*P('Calcutta')); mx, my = V(*MUR); ms = V(*P('Madras'))
        seized = tt > c56 + 1.6
        SP.fort(d, cx + 30, cy + 8, 70, COMPANY if not seized else MUGHAL, eo((tt - a) / 0.5), build=0.55 + 0.45 * sm((tt - cFort) / 1.2))
        lab(out, L('CALCUTTA', 'కలకత్తా'), cx + 30, cy + 30, eo((tt - a) / 0.5), 26)
        SP.throne(d, mx, my + 10, 90, eo((tt - a - 0.3) / 0.5)); lab(out, L('NAWAB · MURSHIDABAD', 'నవాబు · ముర్షిదాబాద్'), mx, my + 30, eo((tt - a - 0.3) / 0.5), 24)
        if tt > cFort: lab(out, L('COMPANY BUILDS FORTIFICATIONS', 'కంపెనీ కోటలు'), W / 2, 150, eo((tt - cFort) / 0.4) * (1 - eo((tt - cPass) / 0.3)), 32, GOLD)
        if tt > cPass:
            for j in range(4):
                f = ((tt - cPass) * 0.6 + j / 4) % 1
                SP.scroll(d, lerp(cx - 20, cx - 260, f), lerp(cy - 20, cy - 160 - j * 30, f), 40, (1 - f) * (1 - eo((tt - c56) / 0.3)))
            lab(out, L('ABUSING THE PASSES', 'పాసుల దుర్వినియోగం'), W / 2, 150, eo((tt - cPass) / 0.4) * (1 - eo((tt - c56) / 0.3)), 32, GOLD)
        if tt > c56:
            f = sm((tt - c56) / 1.6); x, y = lerp(mx, cx, f), lerp(my, cy - 20, f)
            SP.formation(d, x - 90, y - 20, 5, 2, 44, NAWAB, eo((tt - c56) / 0.3), kind='rider')
            lab(out, L('1756 · CALCUTTA SEIZED', '1756 · కలకత్తా స్వాధీనం'), W / 2, 150, eo((tt - c56) / 0.4) * (1 - eo((tt - cMad) / 0.3)), 34, GOLD)
        if tt > cMad:
            route = [V(*P('Madras')), V(84, 14), V(88, 19), V(88.2, 21.8)]; f = sm((tt - cMad) / 2.6)
            for j in range(3):
                x, y = path_at(route, max(0, f - j * 0.06)); SP.ship(d, x, y, 64, a=eo((tt - cMad) / 0.4), flagcol=COMPANY)
            lab(out, L('AN ARMY FROM MADRAS', 'మద్రాసు నుంచి సైన్యం'), W / 2, 150, eo((tt - cMad) / 0.4), 34, GOLD)
    spec = dict(box0=(73, 99, 15.5, 30), box1=(73.5, 98.5, 15.8, 29.7), pins=[], draw=draw, autoships=False)
    if t < cFort - 0.6: return fx.to_rgba(fx.cam(FL.img('PD16'), (t - a) / max(0.1, cFort - a), (.5, .5), (.52, .5), 1.0, 1.08))
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 7.2 / 7.3  Plassey as a battle scene
GROVE = (430, 600)
def battlefield(fr, t, k=1.0):
    d = ImageDraw.Draw(fr)
    d.polygon([(0, 140), (260, 150), (330, 1080), (0, 1080)], fill=(52, 84, 112, int(170 * k)))                 # the river
    lab(fr, L('RIVER', 'నది'), 120, 170, k, 22, (170, 200, 230), bg=False)
    rng = np.random.default_rng(3)
    for j in range(26):
        x, y = GROVE[0] + rng.uniform(-170, 170), GROVE[1] + rng.uniform(-160, 160)
        d.ellipse((x - 26, y - 22, x + 26, y + 22), fill=(48, 82, 44, int(200 * k)))
    lab(fr, L('MANGO GROVE', 'మామిడి తోట'), GROVE[0], GROVE[1] + 190, k, 22, (170, 210, 150), bg=False)
NAWAB_BLOCKS = [('jafar', 1020, 260, 7, 4, 'rider'), ('centre', 1050, 560, 9, 3, 'man'), ('centre_e', 1150, 690, 3, 1, 'elephant'), ('right', 1020, 840, 7, 3, 'rider')]
def plassey(fr, t, c_co, c_nb, c_never=1e9, c_deal=1e9, c_fight=None):
    battlefield(fr, t); d = ImageDraw.Draw(fr)
    k1 = eo((t - c_co) / 0.6)
    if k1 > 0:
        SP.formation(d, GROVE[0] - 130, GROVE[1] - 80, 7, 4, 52, (178, 64, 54), k1, hat='turban', mix=(0.27, (214, 60, 48), 'tricorn'))
        for j in range(3): SP.cannon(d, GROVE[0] + 150, GROVE[1] - 40 + j * 50, 50, INKC, k1, ang=0)
        lab(fr, L('COMPANY ~3,000 · MOSTLY INDIAN SEPOYS', 'కంపెనీ ~3,000 · ఎక్కువమంది భారతీయ సిపాయిలు'), GROVE[0], 330, k1, 26)
    k2 = eo((t - c_nb) / 0.8)
    if k2 > 0:
        for name, x, y, cols, rows, kind in NAWAB_BLOCKS:
            idle = t > c_never and name in ('jafar', 'right')
            gk = eo((t - c_never) / 0.6) if idle else 0
            col = tuple(int(lerp(c1, c2, gk)) for c1, c2 in zip(NAWAB, (96, 96, 104)))
            dx = 0
            if c_fight and name.startswith('centre'): dx = 40 * sm((t - c_fight) / 1.5)          # the engaged centre falls back
            SP.formation(d, x + 140 * (1 - k2) + dx, y, cols, rows, 46 if kind != 'elephant' else 70, col, k2, kind=kind, gap=60 if kind != 'elephant' else 110)
        lab(fr, L("NAWAB'S ARMY ~50,000", 'నవాబు సైన్యం ~50,000'), 1300, 150, k2, 28)
    if t > c_never:
        kj = eo((t - c_never) / 0.6)
        lab(fr, L("MIR JAFAR'S TROOPS · STOOD ASIDE", 'మీర్ జాఫర్ సైన్యం · యుద్ధానికి దిగలేదు'), 1250, 220, kj, 26, (210, 210, 220))
        lab(fr, L('MUCH OF THE ARMY NEVER FOUGHT', 'చాలామంది యుద్ధమే చేయలేదు'), 1250, 980, kj, 26, (210, 210, 220))
        for j in range(4):                                    # only the centre exchanges fire with the grove
            ph = (t * 1.3 + j * 0.37) % 1
            SP.puff(d, lerp(GROVE[0] + 230, 980, (j % 2)), 600 + (j - 1.5) * 50, 16 + 14 * ph, (1 - ph) * kj)
    if t > c_deal:
        f = sm((t - c_deal) / 1.4); x, y = lerp(GROVE[0] + 60, 1200, f), lerp(GROVE[1] - 120, 330, f)
        SP.scroll(d, x, y, 110, eo((t - c_deal) / 0.3), seals=2); lab(fr, L('SECRET DEAL', 'రహస్య ఒప్పందం'), x, y + 60, eo((t - c_deal) / 0.4), 26, GOLD)
def s72(t, a, b):
    i = '7.2'; c_co = cue(i, 'three', 'మూడు') if X['TE'] else cue(i, '3', 'మూడు'); c_nb = cue(i, 'fifty', 'యాభై') if X['TE'] else cue(i, '50', 'యాభై')
    if t < c_co - 0.5: return fx.to_rgba(fx.cam(FL.img('G30'), (t - a) / max(0.1, c_co - a), (.5, .55), (.48, .55), 1.02, 1.08))
    fr = dark_field(); plassey(fr, t, c_co, c_nb); return fr
def s73(t, a, b):
    i = '7.3'; cN = cue(i, 'never', 'చేయలేదు') - 0.3; cD = cue(i, 'secret', 'రహస్య') - 0.2; cT = cue(i, 'throne', 'నవాబుగా') - 0.6
    if t < cT:
        fr = dark_field(); plassey(fr, t, a - 5, a - 5, cN, cD, cN + 0.8); return fr
    fr = fx.dark(); d = ImageDraw.Draw(fr); k = sm((t - cT) / 1.2)
    SP.throne(d, W / 2, 820, 300, 1.0, seated=False)
    SP.man(d, lerp(W / 2, W / 2 - 520, k), 790, 220, (60, 54, 60), 1 - 0.6 * k, hat='turban', musket=False, crown=k < 0.5)
    SP.man(d, lerp(W / 2 + 520, W / 2, k), 790, 220, (40, 34, 40), 0.4 + 0.6 * k, hat='turban', musket=False, crown=k > 0.5)
    SP.flag(d, W / 2 + 190, 820, 300, COMPANY, eo((t - cT - 0.8) / 0.5), t=t)
    lab(fr, L('SIRAJ-UD-DAULAH', 'సిరాజ్-ఉద్-దౌలా'), W / 2 - 520, 840, 1 - 0.5 * k, 28)
    lab(fr, L('MIR JAFAR · NAWAB OF BENGAL', 'మీర్ జాఫర్ · బెంగాల్ నవాబు'), W / 2, 840, eo((t - cT - 0.9) / 0.4), 30, GOLD)
    lab(fr, L('PUT ON THE THRONE WITH THE COMPANY\'S HELP', 'కంపెనీ సాయంతో సింహాసనంపై'), W / 2, 160, eo((t - cT - 1.2) / 0.4), 32)
    return fr

# ================================================================== 7.4 (TE)  Machilipatnam 1759
def s74(t, a, b):
    i = '7.4'; c = cue(i, 'మచిలీపట్నాన్ని', 'మచిలీపట్నాన్ని') - 1.2
    def draw(out, d, V, tt):
        x, y = V(*P('Machilipatnam')); taken = tt > c + 1.6
        SP.fort(d, x + 20, y + 10, 80, COMPANY if taken else FRENCH, 1.0)
        f = sm((tt - c) / 1.6); SP.formation(d, lerp(x - 260, x - 90, f), lerp(y + 160, y + 40, f), 4, 2, 34, COMPANY, eo((tt - c) / 0.4))
        lab(out, 'మచిలీపట్నం · 1759', x + 20, y + 30, 1.0, 28)
        if taken: lab(out, 'ఫ్రెంచ్ నుంచి కంపెనీ చేతికి', W / 2, 150, eo((tt - c - 1.6) / 0.4), 32, GOLD)
    spec = dict(box0=(74, 89, 12, 20.3), box1=(74.5, 88.5, 12.3, 20), pins=[], draw=draw)
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 7.5  Buxar, then Bengal-Bihar-Orissa revenue
REG = [('Bengal', 'బెంగాల్', 89.3, 22.9), ('Bihar', 'బీహార్', 85.6, 25.4), ('Orissa', 'ఒరిస్సా', 85.0, 20.6)]
def s75(t, a, b):
    i = '7.5'; cB = cue(i, 'Buxar', 'బక్సర్‌లో'); c65 = cue(i, '1765', '1765'); cR = cue(i, 'revenue', 'ఆదాయం'); cPaint = cR + 2.0
    if t >= cPaint: return fx.to_rgba(fx.cam(FL.img('PD17'), (t - cPaint) / max(0.1, b - cPaint), (.5, .5), (.52, .48), 1.0, 1.08))
    def draw(out, d, V, tt):
        bx, by = V(*P('Buxar'))
        if tt > cB:
            f = sm((tt - cB) / 1.4); k = eo((tt - cB) / 0.4)
            SP.formation(d, bx - 300 + 120 * f, by - 30, 4, 2, 44, COMPANY, k)
            SP.formation(d, bx + 120 - 60 * f + 120 * sm((tt - cB - 1.6) / 1.0), by - 30, 5, 2, 44, NAWAB, k * (1 - 0.5 * sm((tt - cB - 1.6) / 1.0)), kind='rider')
            SP.swords(d, bx, by - 110, 50, k)
            lab(out, L('BUXAR 1764 · COMPANY vs BENGAL–AWADH–MUGHAL ALLIANCE', 'బక్సర్ 1764 · కంపెనీ vs బెంగాల్–అవధ్–మొఘల్ కూటమి'), W / 2, 150, k * (1 - eo((tt - c65) / 0.3)), 30, GOLD)
        for j, (en, te, lo, la) in enumerate(REG):
            x, y = V(lo, la); k = eo((tt - c65 - j * 0.35) / 0.5)
            if k > 0:
                glow(out, x, y, 150, COMPANY, k); lab(out, L(en, te), x, y, k, 28, PAPER, 'cc', bg=False)
        if tt > c65: lab(out, L('1765 · REVENUE RIGHTS TO THE COMPANY', '1765 · ఆదాయ హక్కు కంపెనీకి'), W / 2, 150, eo((tt - c65) / 0.4), 34, GOLD)
        if tt > cR:                                                  # the revenue now flows to the Company
            src = V(86.5, 23.3); co = (W - 300, 520); k = eo((tt - cR) / 0.4)
            put(out, fx.medallion('PD12', 1340, 1340, 1200, 170), co[0], co[1], k, 'cc'); lab(out, L('THE COMPANY', 'కంపెనీ'), co[0], co[1] + 100, k, 26)
            for j in range(6):
                f = ((tt - cR) * 0.6 + j / 6) % 1; SP.coin(d, lerp(src[0], co[0] - 90, f), lerp(src[1], co[1], f) - 60 * math.sin(math.pi * f), 12, k)
    spec = dict(box0=(75.5, 98.5, 17, 29.5), box1=(76, 98, 17.3, 29.2), pins=[('Plassey',) + P('Plassey') + (a + 0.2,), ('Buxar',) + P('Buxar') + (a + 0.4, 'u')], draw=draw)
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 7.6  silver from London -> taxes from Bengal (world map, Britain on screen)
def s76(t, a, b):
    i = '7.6'; cS = cue(i, 'silver', 'వెండి') - 0.3; cT = cue(i, 'taxes', 'పన్నులతో') - 0.3
    if t < cS - 0.1: return fx.to_rgba(fx.cam(FL.img('MET1'), (t - a) / max(0.1, cS - a), (.5, .45), (.5, .47), 1.6, 1.75))
    out_route = [P('London'), (-5, 49), (-12, 40), (-18, 15), (-5, -10), (18, -36), (40, -36), (73, -8), (80, 5), P('Machilipatnam')]
    back_route = list(reversed(out_route))
    def draw(out, d, V, tt):
        ld = V(*P('London')); glow(out, ld[0], ld[1], 70, (200, 200, 220), 1.0)
        lab(out, L('LONDON', 'లండన్'), ld[0], ld[1] - 70, 1.0, 26, PAPER, 'cb')
        sw = sm((tt - cT) / 0.8) if tt > cT else 0.0
        vo = [V(*q) for q in out_route]; vb = [V(*q) for q in back_route]
        for j in range(3):                                              # silver ships out, bale ships home
            f = ((tt - cS) / 6.0 + j / 3) % 1
            x, y = path_at(vo, f); SP.ship(d, x, y, 58, a=(1 - sw) * min(1, f / 0.06, (1 - f) / 0.06), flagcol=COMPANY, cargo='silver')
            x, y = path_at(vb, f); SP.ship(d, x, y, 58, a=min(1, f / 0.06, (1 - f) / 0.06), flagcol=COMPANY, cargo='bale')
        mp = V(*P('Machilipatnam')); bg_ = V(87.5, 23.5)
        lab(out, L('SILVER FROM EUROPE BUYS OUR CLOTH', 'యూరప్ వెండితో మన గుడ్డ కొనుగోలు'), W / 2, 150, (1 - sw) * eo((tt - cS) / 0.4), 32, (210, 210, 220))
        if sw > 0:
            glow(out, bg_[0], bg_[1], 90, COMPANY, sw)
            for j in range(5):
                f = ((tt - cT) * 0.7 + j / 5) % 1; SP.coin(d, lerp(bg_[0], mp[0], f), lerp(bg_[1], mp[1], f), 9, sw, silver=True)
            lab(out, L('NOW: TAXES COLLECTED IN INDIA BUY IT', 'ఇప్పుడు: భారత్‌లో వసూలైన పన్నులతోనే కొనుగోలు'), W / 2, 150, sw, 32, (240, 150, 130))
            lab(out, L('BENGAL REVENUE', 'బెంగాల్ ఆదాయం'), bg_[0] + 60, bg_[1] - 40, sw, 24, (240, 150, 130), 'lb')
    spec = dict(box0=(-40, 130, -38, 62), box1=(-40, 130, -38, 62), pins=[('Machilipatnam',) + P('Machilipatnam') + (a,)], draw=draw, contain=True)
    return FL.render_map(None, t, spec, a, b)

# ================================================================== 3.3  village -> broker -> buyer -> boat -> ship (side view, one camera move)
def chain(t, a, b):
    fr = fx.dark(); d = ImageDraw.Draw(fr); u = sm((t - a) / max(0.1, b - a)); PW = W * 2.4; cam_x = (PW - W) * u
    X_ = lambda x: x - cam_x; GY = 780
    fr = Image.fromarray(fx.blurred('G09', 0.62, 1.15, .5, .35)).convert('RGBA'); d = ImageDraw.Draw(fr)
    d.rectangle((0, GY, W, H), fill=(86, 70, 52, 255))
    sea0 = X_(PW * 0.62)
    if sea0 < W: d.rectangle((max(0, sea0), GY - 10, W, H), fill=(46, 78, 104, 255))
    for j in range(12): d.arc((sea0 + j * 140 - (t * 60) % 140, GY - 4, sea0 + j * 140 + 120 - (t * 60) % 140, GY + 30), 200, 340, fill=(200, 220, 230, 160), width=3)
    # village hut + weaver
    hx = X_(260); d.polygon([(hx - 120, GY - 140), (hx, GY - 230), (hx + 120, GY - 140)], fill=(120, 96, 60, 255)); d.rectangle((hx - 100, GY - 140, hx + 100, GY), fill=(150, 120, 80, 255))
    SP.man(d, hx + 170, GY, 170, INKC, 1.0, musket=False)
    lab(fr, L('WEAVING VILLAGE', 'నేత గ్రామం'), hx, GY + 40, 1.0, 26)
    # the bale's journey: village -> broker -> port -> boat -> ship
    pts = [(X_(430), GY), (X_(1150), GY), (X_(1900), GY), (X_(2520), GY + 30), (X_(3420), GY - 40)]
    f = sm((t - a - 0.2) / max(0.1, (b - a) * 0.9))
    bxp, byp = path_at(pts, f)
    # broker carrying (walks with the bale on land)
    if f < 0.55: SP.man(d, bxp - 40, GY, 170, (40, 34, 30), 1.0, musket=False)
    lab(fr, L('BROKER', 'దళారి'), X_(1150), GY + 40, 1.0, 26)
    # interpreter + foreign buyer at the port
    SP.man(d, X_(1820), GY, 170, (40, 34, 30), 1.0, musket=False); SP.man(d, X_(1980), GY, 175, (30, 26, 32), 1.0, hat='tricorn', musket=False)
    lab(fr, L('INTERPRETER · FOREIGN BUYER', 'దుబాసీ · విదేశీ కొనుగోలుదారు'), X_(1900), GY + 40, 1.0, 26)
    # masula boat through the surf, ship at anchor
    boat_x = X_(lerp(2350, 3300, sm((f - 0.62) / 0.3))) if f > 0.62 else X_(2350)
    SP.boat(d, boat_x, GY + 40, 120, 1.0, 2, t)
    SP.ship(d, X_(3500), GY + 10, 300, flagcol=COMPANY)
    lab(fr, L('MASULA BOAT', 'మసులా పడవ'), boat_x, GY + 90, 1.0, 24); lab(fr, L('SHIP AT ANCHOR', 'లంగరు వేసిన ఓడ'), X_(3500), GY + 90, 1.0, 24)
    if f > 0.62: bxp, byp = (boat_x, GY + 6) if f < 0.92 else (lerp(boat_x, X_(3460), sm((f - 0.92) / 0.08)), lerp(GY + 6, GY - 120, sm((f - 0.92) / 0.08)))
    SP.bale(d, bxp, byp - (60 if f < 0.55 else 0), 70)
    return fr

# ================================================================== 4.2 kingdoms: Vijayanagara capital sacked, Aravidu forts continue
def deccan_draw(cT, cAr, cG, cM):
    def draw(out, d, V, tt):
        vx, vy = V(*P('Vijayanagara')); sacked = tt > cT + 0.3
        SP.fort(d, vx - 60, vy + 12, 64, (200, 150, 60), 1.0, ruined=sacked)
        if sacked:
            for j in range(4):
                ph = (tt * 0.6 + j / 4) % 1; SP.puff(d, vx - 60 + 10 * math.sin(j), vy - 50 - ph * 90, 14 + 18 * ph, (1 - ph) * 0.8)
            lab(out, L('1565 · CAPITAL SACKED', '1565 · రాజధాని దోపిడీ'), vx - 60, vy + 30, eo((tt - cT - 0.3) / 0.4), 24)
        for j, n in enumerate(('Penukonda', 'Chandragiri', 'Vellore')):
            k = eo((tt - cAr - j * 0.25) / 0.4)
            if k > 0: x, y = V(*P(n)); SP.flag(d, x + 14, y, 70, (200, 150, 60), k, t=tt)
        if tt > cAr: lab(out, L('ARAVIDU KINGS RULE ON', 'ఆరవీడు రాజుల పాలన కొనసాగింది'), W / 2, 150, eo((tt - cAr) / 0.4) * (1 - eo((tt - cG) / 0.3)), 30, GOLD)
        if tt > cM:
            src, dst = V(77.2, 28.0), V(77.5, 20.5); arrow(d, src, dst, sm((tt - cM) / 1.2), MUGHAL, 16, eo((tt - cM) / 0.4))
    return draw

# ================================================================== 6.3 Surat: Hawkins to Jahangir, Swally 1612, deal confirmed 1613
def surat_draw(c08, cJ, c12, c13, roe):
    def draw(out, d, V, tt):
        s_, ag, sw = V(*P('Surat')), V(*P('Agra')), V(*P('Swally'))
        if tt > c08:
            f = sm((tt - c08) / 1.2); SP.ship(d, lerp(s_[0] - 300, s_[0] - 30, f), lerp(s_[1] + 60, s_[1] + 10, f), 50, a=eo((tt - c08) / 0.3) * (1 - eo((tt - c12 + 0.3) / 0.3)), flagcol=COMPANY)
        SP.throne(d, ag[0] + 10, ag[1] + 6, 70, eo((tt - cJ) / 0.4)); lab(out, L("JAHANGIR'S COURT", 'జహంగీర్ దర్బారు'), ag[0] + 10, ag[1] + 24, eo((tt - cJ) / 0.4), 24)
        if tt > c12:
            f = sm((tt - c12) / 2.0); k = eo((tt - c12) / 0.4)
            for j in range(2): SP.ship(d, sw[0] - 120 + j * 30, sw[1] + 40 + j * 40, 50, a=k, flagcol=COMPANY)
            for j in range(3): SP.ship(d, sw[0] - 360 - 160 * sm((tt - c12 - 1.4) / 1.2) + j * 40, sw[1] + 80 + j * 30, 50, sail=(220, 220, 228), a=k * (1 - 0.6 * sm((tt - c12 - 1.4) / 1.2)), flagcol=PORT)
            if tt < c12 + 1.8:
                for j in range(3): SP.puff(d, sw[0] - 240, sw[1] + 60 + j * 30, 16 + 10 * math.sin(tt * 5 + j), 0.8)
            lab(out, L('1612 · SWALLY: ENGLISH SHIPS BEAT A PORTUGUESE FLEET', '1612 · స్వాలీ: పోర్చుగీస్‌పై ఇంగ్లీష్ ఓడల గెలుపు'), W / 2, 150, k * (1 - eo((tt - c13) / 0.3)), 28, GOLD)
        if tt > c13:
            f = sm((tt - c13) / 1.2); SP.scroll(d, lerp(ag[0], s_[0] + 20, f), lerp(ag[1], s_[1] - 40, f), 60, eo((tt - c13) / 0.3))
            if f >= 1: SP.factory(d, s_[0] + 50, s_[1] + 10, 60, COMPANY, eo((tt - c13 - 1.2) / 0.4))
            lab(out, L('1613 · DEAL CONFIRMED BY THE EMPEROR', '1613 · చక్రవర్తి ఆమోదం'), W / 2, 150, eo((tt - c13) / 0.4), 30, GOLD)
    return draw

# ================================================================== 6.5 east coast: Machilipatnam 1611, Madras 1639
def madras_draw(c11, c39, cM):
    def draw(out, d, V, tt):
        mp, md = V(*P('Machilipatnam')), V(*P('Madras'))
        SP.factory(d, mp[0] + 40, mp[1] + 8, 56, COMPANY, eo((tt - c11) / 0.4)); lab(out, L('ENGLISH FACTORY · 1611', 'ఇంగ్లీష్ వ్యాపార కేంద్రం · 1611'), mp[0] + 40, mp[1] + 28, eo((tt - c11) / 0.4), 22)
        if tt > c39:
            k = eo((tt - c39) / 0.4); nx, ny = md[0] - 260, md[1] + 30
            SP.man(d, nx, ny, 170, (40, 34, 40), k, hat='turban', musket=False, crown=True)
            lab(out, L('DAMARLA NAYAKAS', 'దామెర్ల నాయకులు'), nx, ny + 20, k, 22)
            f = sm((tt - c39 - 0.6) / 1.0); SP.scroll(d, lerp(nx + 30, md[0] - 20, f), lerp(ny - 70, md[1] - 50, f), 50, k)
            d.rectangle((md[0] - 6, md[1] - 60, md[0] + 26, md[1] + 50), outline=SP.A(GOLD, eo((tt - c39 - 1.6) / 0.4)), width=4)
            lab(out, L('A STRIP OF LAND BY THE SEA · 1639', 'సముద్రతీరంలో చిన్న భూమి · 1639'), W / 2, 150, k * (1 - eo((tt - cM) / 0.3)), 30, GOLD)
        if tt > cM:
            SP.fort(d, md[0] + 60, md[1] + 20, 70, COMPANY, 1.0, build=sm((tt - cM) / 1.0)); lab(out, L('MADRAS', 'మద్రాసు'), md[0] + 60, md[1] + 40, eo((tt - cM - 0.5) / 0.4), 28)
    return draw

# ================================================================== 5.x ocean
def malindi_draw(cP, cDeb):
    def draw(out, d, V, tt):
        ml = V(*P('Malindi'))
        if tt > cP:
            k = eo((tt - cP) / 0.4); SP.man(d, ml[0] - 40, ml[1] + 10, 70, (240, 230, 210), k, hat='turban', musket=False)
            lab(out, L('AN EXPERIENCED PILOT JOINS', 'అనుభవం ఉన్న దారిచూపే నావికుడు'), ml[0] - 40, ml[1] + 30, k * (1 - eo((tt - cDeb) / 0.3)), 24)
        if tt > cDeb: lab(out, L('WHO WAS HE? HISTORIANS DEBATE', 'అతనెవరు? చరిత్రకారుల చర్చ'), ml[0] - 40, ml[1] + 30, eo((tt - cDeb) / 0.4), 26, GOLD)
    return draw
def monsoon_draw(arrows):
    def draw(out, d, V, tt):
        for (lo0, la0, lo1, la1, c0, c1) in arrows:
            if c0 <= tt <= c1:
                p0, p1 = V(lo0, la0), V(lo1, la1); f = ((tt - c0) / 2.2) % 1
                SP.ship(d, lerp(p0[0], p1[0], f), lerp(p0[1], p1[1], f) - 10, 40, a=min(1, f / 0.1, (1 - f) / 0.1))
    return draw
def encounter(t, a, b, cQ, cA_):
    fr = fx.to_rgba(fx.blurred('G22', 0.36)); d = ImageDraw.Draw(fr)
    k = eo((t - a) / 0.5)
    SP.man(d, 600, 860, 240, (30, 26, 32), k, hat='turban', musket=False); SP.man(d, 720, 860, 240, (30, 26, 32), k, hat='turban', musket=False)
    SP.man(d, 1300, 860, 250, (30, 26, 32), k, hat='helmet', musket=False)
    lab(fr, L('TWO MERCHANTS FROM TUNIS', 'ట్యూనిస్ వ్యాపారులు ఇద్దరు'), 660, 560, k, 26, anchor='cb'); lab(fr, L('A PORTUGUESE MAN ASHORE', 'ఒడ్డుకి వచ్చిన పోర్చుగీస్ మనిషి'), 1300, 560, k, 26, anchor='cb')
    if t > cQ: lab(fr, L("“What brought you here?”", "“ఇంత దూరం ఎందుకొచ్చారు?”"), 660, 300, eo((t - cQ) / 0.4), 44, PAPER)
    if t > cA_: lab(fr, L("“Christians… and spices.”", "“క్రైస్తవుల కోసం… సుగంధ ద్రవ్యాల కోసం.”"), 1300, 400, eo((t - cA_) / 0.4), 44, GOLD)
    return fr
def gifts(t, a, b, cs, cLaugh):
    fr = fx.to_rgba(fx.blurred('G23', 0.36)); d = ImageDraw.Draw(fr)
    names = [L('HATS', 'టోపీలు'), L('CORAL', 'పగడాలు'), L('SUGAR', 'చక్కెర'), L('HONEY', 'తేనె')]
    for j, (c, nm) in enumerate(zip(cs, names)):
        k = eo((t - c) / 0.35); x = 420 + j * 360; y = 560; dim = 1 - 0.5 * eo((t - cLaugh) / 0.5) if t > cLaugh else 1
        if k <= 0: continue
        if j == 0: d.polygon([(x - 70, y + 30), (x + 70, y + 30), (x + 50, y), (x + 30, y - 50), (x - 30, y - 50), (x - 50, y)], fill=SP.A((60, 48, 40), k * dim))
        if j == 1:
            for q in range(5): d.line((x, y + 40, x - 60 + q * 30, y - 50 + abs(q - 2) * 15), fill=SP.A((220, 90, 80), k * dim), width=10)
        if j == 2: d.polygon([(x, y - 70), (x - 50, y + 40), (x + 50, y + 40)], fill=SP.A((240, 236, 226), k * dim))
        if j == 3: d.rounded_rectangle((x - 45, y - 40, x + 45, y + 40), 16, fill=SP.A((214, 150, 40), k * dim))
        lab(fr, nm, x, y + 80, k * dim, 28)
    if t > cLaugh: lab(fr, L("“THE POOREST MERCHANT FROM MECCA GAVE MORE”", "“మక్కా అతి పేద వ్యాపారి కూడా ఇంతకంటే ఎక్కువ ఇస్తాడు”"), W / 2, 220, eo((t - cLaugh) / 0.4), 36, GOLD)
    return fr
def cannons_vs_permission(t, a, b, cC, cP):
    fr = fx.dark(); d = ImageDraw.Draw(fr)
    k = eo((t - cC) / 0.4); SP.ship(d, 520, 700, 360, a=k, flagcol=PORT)
    if t > cC:
        for j in range(3):
            ph = (t * 1.2 + j * 0.33) % 1; SP.puff(d, 700 + ph * 160, 640 + j * 20, 20 + 30 * ph, (1 - ph) * k)
    lab(fr, L('PORTUGUESE · CANNONS', 'పోర్చుగీస్ · ఫిరంగులు'), 520, 760, k, 30)
    kp = eo((t - cP) / 0.4)
    if kp > 0:
        SP.man(d, 1300, 820, 260, (30, 26, 32), kp, hat='tricorn', musket=False, bow=sm((t - cP) / 0.8))
        SP.scroll(d, 1400, 600, 100, kp); lab(fr, L('ENGLISH · ASKING PERMISSION', 'ఇంగ్లీష్ · అనుమతి అడుగుతూ'), 1340, 860, kp, 30)
        lab(fr, L('A CENTURY LATER', 'ఒక శతాబ్దం తర్వాత'), 1340, 300, kp, 30, GOLD)
    return fr

# ================================================================== recurring lower-corner subscribe reminder
def sub_corner(fr, t, t0, lang, dur=5.0):
    if not (t0 <= t <= t0 + dur): return fr
    import sys, cairo; sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    sc = 0.62; c.translate(W - 1080 * sc + 40, H - 300 * sc - 40); c.scale(sc, sc)
    cta_card.draw(c, t, t0, 'yt', lang, y=200, t_out=t0 + dur - 0.5)
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data()); rgba = buf[..., [2, 1, 0, 3]].copy()
    fr.alpha_composite(Image.fromarray(rgba, 'RGBA')); return fr
