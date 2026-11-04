
# ---------------- anchors (6/6 v5 story version) ----------------
def _A(line, en, te, n=1, off=0.0, ten=1):
    return AT(line, en, te, n=(n if LANGV == 'en' else ten), off=off)
A = {
    'window': _A('1', 'window', 'కిటికీ'),
    'tiny': _A('3', 'tiny', 'చిన్న'), 'hair': _A('3', 'hair', 'వెంట్రుక'), 'lungs': _A('3', 'lungs', 'ఊపిరితిత్తుల్లోకి'),
    'blood': _A('3', 'bloodstream', 'రక్తంలోకి'), 'heart': _A('3', 'heart', 'గుండెపోటు'), 'strokes': _A('3', 'strokes', 'స్ట్రోక్'),
    'eight4': _A('4', '8', '8'),
    'b488': _A('5', '488', '488'), 'three5': _A('5', 'Three', 'మూడు'), 'eight5': _A('5', 'eight', 'ఎనిమిది'),
    'crackers6': _A('6', 'Crackers', 'బాణాసంచా'),
    'warm': _A('7', 'Warm', 'వెచ్చని'), 'lid': _A('7', 'lid', 'మూతలా'),
    'veh8': _A('8', 'Vehicles', 'వాహనాలు'), 'dust': _A('8', 'dust', 'దుమ్ము'), 'industry': _A('8', 'industry', 'పరిశ్రమలు'),
    'garbage': _A('8', 'garbage', 'చెత్త'), 'biggest': _A('8', 'biggest', 'అతిపెద్ద'),
    'gurpreet': _A('9', 'Gurpreet', 'Gurpreet'), 'two9': _A('9', 'two', 'రెండు'), 'machines': _A('9', 'Machines', 'యంత్రాలకు'), 'burning': _A('9', 'Burning', 'కాల్చడం'),
    'p7': _A('10', '7', '7'), 'p22': _A('10', '22', '22'),
    'constr': _A('11', 'construction', 'నిర్మాణాలు'), 'cars': _A('11', 'cars', 'కార్లపై'), 'hybrid': _A('11', 'hybrid', 'hybrid'),
    'pm10': _A('12', 'PM10', 'PM10'), 'p40': _A('12', '40', '40'),
    'cleanest': _A('13', 'cleanest', 'శుభ్రంగా'), 'annual': _A('13', 'annual', 'సంవత్సర', ten=2), 'c23': _A('13', '23', '23'),
    'didnt': _A('13', "didn't", 'చేరలేదు'),
    'beijing': _A('14', 'Beijing', 'Beijing'), 'y2013': _A('14', '2013', '2013'), 'v70': _A('14', '70', '70'),
    'coal': _A('14', 'coal', 'బొగ్గు'), 'gas': _A('14', 'gas', 'gas'), 'vrules': _A('14', 'vehicle', 'వాహనాల'),
    'neigh': _A('14', 'neighbours', 'పక్క'), 'decade': _A('14', 'decade', 'పదేళ్లకు'),
    'spike15': _A('15', 'Crackers', 'బాణాసంచా'), 'winter15': _A('15', 'winter', 'చలికాలం'), 'every15': _A('15', 'everyday', 'రోజువారీ'),
    'region': _A('15', 'year-round', 'పొడవునా', off=-0.4),
    'sunday': _A('16', 'Sunday', 'ఆదివారం'),
    'tomorrow': S('16'), 'loop': S('L'),
}
A['end'] = DUR
A['xr'] = A['lungs'] - 1.2; A['alv'] = A['blood'] - 0.9; A['hb'] = A['heart'] - 0.3
"""HELPERS"""
# ---------------- talking: mouth driven by the voice envelope ----------------
def _env():
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', VFILE, '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    hop = 160; n = len(x) // hop; r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-6
    db = 20 * np.log10(r); hi = np.percentile(db, 97); v = np.clip((db - (hi - 30)) / 30, 0, 1)
    out = np.zeros_like(v); y = 0.0
    for i, u in enumerate(v):                       # soft attack, slower release: lips glide, they don't flap
        y += (u - y) * (0.35 if u > y else 0.12); out[i] = y
    k = 100 / FPS; idx = (np.arange(int(len(out) / k)) * k).astype(int)
    return np.clip(out[idx] ** 1.2 * 0.85, 0, 0.75)
ENV = _env()
LINES = sorted(MK.items(), key=lambda kv: kv[1][0])
def speaker(t):
    for k, (a, b) in LINES:
        if a - 0.05 <= t <= b + 0.05: return k
    return None
def talk(t, who):
    k = speaker(t)
    if k is None: return 0.0
    if (who == 'meera') != k.startswith('M'): return 0.0
    if who == 'raju' and k in ('1', 'L'): return 0.0
    i = int((t - LEAD) * FPS)
    return float(ENV[i]) if 0 <= i < len(ENV) else 0.0
def blink(t, seed=0.0):
    ph = (t + seed * 1.7) % 3.9
    return 0.15 if ph < 0.12 else 1.0

# ---------------- characters: Anna & Chelli from the long videos (play Raju & Meera) ----------------
sys.path.insert(0, '/home/claude/dl'); import chars2 as C2
def blinkv(t, seed=0.0): return 1.0 if ((t + 1.3 + seed * 1.7) % 3.9) < 0.12 else 0.0
def raju_c(c, x, y, s, t, look=(0, 0), tk=None):
    tk = talk(t, 'raju') if tk is None else tk
    C2.anna(c, x, y, s, t=t, talk=tk, blink=blinkv(t), gesture=(0.25 + 0.15 * math.sin(t * 1.3)) if tk > 0.05 else 0.05, look=look, tilt=3 * math.sin(t * 0.7) if tk > 0.05 else 0)
def meera_c(c, x, y, s, t, look=(0, 0), tk=None, gesture=0.0):
    tk = talk(t, 'meera') if tk is None else tk
    C2.chelli(c, x, y, s, t=t, talk=tk, blink=blinkv(t, 1), gesture=gesture, look=look, q=0)
def gurpreet_c(c, x, y, s, t):
    """Punjab farmer in the same long-video style: green kurta, orange turban, beard"""
    old = (C2.KURTA, C2.KURTA_D, C2.PANT, C2.PANT_D)
    C2.KURTA, C2.KURTA_D, C2.PANT, C2.PANT_D = (0.34, 0.56, 0.38), (0.22, 0.40, 0.26), (0.92, 0.90, 0.84), (0.76, 0.74, 0.68)
    C2.anna(c, x, y, s, t=t, talk=0.0, blink=blinkv(t, 2), gesture=0.0, look=(0.5, 0))
    C2.KURTA, C2.KURTA_D, C2.PANT, C2.PANT_D = old
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(0, -735 + 2 * math.sin(t * 2.0))
    C2.blob(c, [(-58, 92), (-118, 40), (-150, -10), (-120, 125), (-40, 200), (40, 200), (120, 125), (150, -10), (118, 40), (58, 92), (0, 108)]); C2.paint(c, C2.vgrad(-10, 200, (0.20, 0.13, 0.10), (0.10, 0.06, 0.05)))   # beard
    c.set_source_rgb(0.55, 0.30, 0.25); c.set_line_width(7); c.new_path(); c.arc(0, 72, 30, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    C2.blob(c, [(-162, -40), (-170, -130), (-110, -205), (0, -232), (110, -205), (170, -130), (162, -40), (80, -78), (0, -92), (-80, -78)]); C2.paint(c, C2.vgrad(-232, -40, (1.0, 0.62, 0.20), (0.88, 0.45, 0.10)))   # turban
    c.set_source_rgba(0.75, 0.35, 0.05, 0.9); c.set_line_width(6)
    for k in range(3): c.new_path(); c.move_to(-150 + 20 * k, -60 - 30 * k); c.curve_to(-60, -150 - 20 * k, 60, -150 - 20 * k, 150 - 20 * k, -60 - 30 * k); c.stroke()
    c.restore()
# ---------------- characters (flat 2D; feet at (x, y)) ----------------
MEERA_KURTI = (0.88, 0.64, 0.18); RAJU_SHIRT = (0.30, 0.45, 0.70); GRAN_SAREE = (0.55, 0.40, 0.60)
def char(c, x, y, s, who, t=0.0, tk=0.0, a=1.0, walk=0.0, nod=0.0, look=0.0):
    if a <= 0.01 or s <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s, s); c.push_group()
    bob = 3 * math.sin(t * 3.0) + (6 * abs(math.sin(t * 7)) if walk > 0 else 0)
    shirt = {'raju': RAJU_SHIRT, 'meera': MEERA_KURTI, 'gran': GRAN_SAREE, 'gurpreet': (0.28, 0.50, 0.36)}[who]
    # legs
    sw = 18 * math.sin(t * 7) * walk
    c.set_source_rgb(0.15, 0.15, 0.18); rrect(c, -48 + sw, -120, 40, 120, 16); c.fill(); rrect(c, 8 - sw, -120, 40, 120, 16); c.fill()
    if who == 'meera' or who == 'gran':      # kurti / saree reaches lower
        c.set_source_rgb(*shirt); rrect(c, -78, -300 + bob, 156, 230, 46); c.fill()
        if who == 'meera':
            c.set_source_rgb(0.80, 0.22, 0.30); c.rectangle(-78, -250 + bob, 156, 16); c.fill()   # dupatta band
        else:
            c.set_source_rgba(0.95, 0.80, 0.45, 0.9); c.set_line_width(10); c.move_to(-70, -290 + bob); c.line_to(60, -90 + bob); c.stroke()
    else:
        c.set_source_rgb(*shirt); rrect(c, -72, -290 + bob, 144, 190, 50); c.fill()
        if who == 'gurpreet':
            c.set_source_rgba(0.92, 0.88, 0.75, 0.55); c.set_line_width(5)
            for k in range(-60, 70, 28): c.move_to(k, -285 + bob); c.line_to(k, -105 + bob); c.stroke()
            for k in range(-270, -100, 28): c.move_to(-70, k + bob); c.line_to(70, k + bob); c.stroke()
    hy = -350 + bob + 6 * nod
    if who == 'meera':   # ponytail behind the head
        c.set_source_rgb(*HAIR); c.save(); c.translate(48, hy + 10); c.rotate(0.25 + 0.06 * math.sin(t * 2.2)); rrect(c, -14, 0, 28, 110, 14); c.fill(); c.restore()
    if who == 'gran':
        c.set_source_rgb(0.86, 0.86, 0.86); c.arc(0, hy - 58, 26, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*SKIN); c.arc(0, hy, 56, 0, 2 * math.pi); c.fill()
    if who == 'gurpreet':
        c.set_source_rgb(0.95, 0.55, 0.15); c.arc(0, hy - 16, 62, math.pi * 0.95, math.pi * 2.05); c.fill(); rrect(c, -62, hy - 30, 124, 22, 10); c.fill()
        c.set_source_rgb(*HAIR); c.move_to(-50, hy + 4); c.curve_to(-46, hy + 72, 46, hy + 72, 50, hy + 4); c.curve_to(30, hy + 34, -30, hy + 34, -50, hy + 4); c.fill()
    else:
        hc = (0.86, 0.86, 0.86) if who == 'gran' else HAIR
        c.set_source_rgb(*hc); c.arc(0, hy - 12, 58, math.pi * 1.02, math.pi * 1.98); c.fill()
        if who == 'meera': c.arc(-30, hy - 30, 30, 0, 2 * math.pi); c.fill()
    ex = 6 * look; bk = blink(t, {'raju': 0, 'meera': 1, 'gran': 2, 'gurpreet': 3}[who])
    c.set_source_rgb(*HAIR)
    for sx in (-20, 20):
        c.save(); c.translate(sx + ex, hy + 5); c.scale(1, bk); c.arc(0, 0, 6, 0, 2 * math.pi); c.restore(); c.fill()
    if who == 'meera': c.set_source_rgb(0.80, 0.15, 0.20); c.arc(ex, hy - 18, 4, 0, 2 * math.pi); c.fill()
    my = hy + 26
    if who == 'gurpreet': my = hy + 22
    if tk > 0.06:     # open mouth, height follows the voice
        h = 4 + 20 * tk; c.set_source_rgb(0.32, 0.08, 0.10); c.save(); c.translate(ex, my); c.scale(1, h / 13); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_source_rgb(0.85, 0.35, 0.35); c.save(); c.translate(ex, my + h * 0.45); c.scale(1, 0.4); c.arc(0, 0, 8, 0, 2 * math.pi); c.restore(); c.fill()
    else:
        c.set_source_rgb(*HAIR); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.new_path(); c.arc(ex, my - 20, 18, 0.25 * math.pi, 0.75 * math.pi); c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def avatar(c, who, cx, cy, r, t, tk, a=1.0):
    """round bust used in the corner of map/city shots"""
    if a <= 0.01: return
    c.save(); c.push_group()
    c.set_source_rgba(0.10, 0.10, 0.12, 0.92); c.arc(cx, cy, r, 0, 2 * math.pi); c.fill()
    c.arc(cx, cy, r - 4, 0, 2 * math.pi); c.clip()
    sc_ = r / 132 * 0.62; meera_c(c, cx, cy + 660 * sc_ + 0.12 * r, sc_, t, tk=tk)
    c.reset_clip(); c.set_source_rgba(*AMBER, 1); c.set_line_width(5); c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
QTXT = {k: txt for k, spk, txt in json.load(open('/home/claude/dwv/s7_lines.json'))[LANGV] if spk == 'M'}
def wrap2(txt, n):
    w = txt.split(); out = ['']
    for x in w:
        if len(out[-1]) + len(x) + 1 > n and out[-1]: out.append(x)
        else: out[-1] = (out[-1] + ' ' + x).strip()
    return out[:3]
def bubble(c, txt, x, y, w, t, t0, tail=(-1, 1)):
    u = e_back(prog(t, t0, t0 + 0.3))
    if u <= 0.01: return
    lines = wrap2(txt, 24 if LANGV == 'en' else 26); lh = 52 if LANGV == 'en' else 58; h = 40 + lh * len(lines)
    c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
    c.set_source_rgba(0.97, 0.95, 0.90, 1); rrect(c, -w / 2, -h / 2, w, h, 30); c.fill()
    c.move_to(-w / 2 + 50 if tail[0] < 0 else w / 2 - 50, h / 2 - 2); c.line_to(-w / 2 + 20 if tail[0] < 0 else w / 2 - 20, h / 2 + 40); c.line_to(-w / 2 + 100 if tail[0] < 0 else w / 2 - 100, h / 2 - 2); c.close_path(); c.fill()
    for i, ln in enumerate(lines):
        yy = -h / 2 + 20 + lh * (i + 0.5)
        if LANGV == 'te': TT.draw(c, ln, 0, yy, 38, INK, 1.0, 'c', 'Bold')
        else: K.head(c, ln, 0, yy, 42, INK, 1.0, 'c', False)
    c.restore()
def qmark(c, x, y, t, a=1.0):
    if a <= 0.01: return
    s = 1 + 0.06 * math.sin(t * 6); c.save(); c.translate(x, y); c.scale(s, s)
    glowdot(c, 0, 0, 34)
    K.head(c, '?', 0, 4, 56, INK, a, 'c', False); c.restore()
def meera_corner(c, t, k):
    """Meera asks from the corner while the camera is on the map/city"""
    a0, a1 = S(k), E(k); u = e_out(prog(t, a0 - 0.25, a0 + 0.05)) * (1 - prog(t, a1 + 0.25, a1 + 0.5))
    if u <= 0.01: return
    avatar(c, 'meera', 170, 1240, 105, t, talk(t, 'meera'), a=u)
    qmark(c, 250, 1130, t, a=u)
    bubble(c, QTXT[k], 650, 1240, 700, t, a0 - 0.1, tail=(-1, 1))
def m_active(t):
    k = speaker(t); return k if (k and k.startswith('M')) else None

# ---------------- 6/6: world layers ----------------
MAPP = json.load(open(ROOT + 'india.json')); META = json.load(open(ROOT + 'mapmeta.json'))
CENT = META['cent']; FIRES = META['fires']; DELHI = CENT['Delhi']
PAPER = (0.86, 0.80, 0.66); SEA = (0.10, 0.13, 0.17)
CREA_STATES = {'Rajasthan', 'Maharashtra', 'Bihar', 'Haryana', 'Odisha', 'Punjab', 'West Bengal', 'Gujarat', 'Chandigarh', 'Himachal Pradesh',
               'Jammu and Kashmir', 'Delhi', 'Jharkhand', 'Arunachal Pradesh', 'Telangana'}
PM25 = AMBER; PM10 = (0.25, 0.78, 0.76); HAZE = (0.62, 0.62, 0.60)
IGP = [(150, 150, 34), (166, 196, 30), (186, 210, 26), (232, 230, 40), (290, 250, 42), (350, 268, 38), (395, 280, 30)]
MAPC = (540, 820)
def lerp(a, b, k): return a + (b - a) * k
def cam_lerp(c0, c1, k):
    z = math.exp(lerp(math.log(c0[2]), math.log(c1[2]), k)); f = (1 / z - 1 / c0[2]) / (1 / c1[2] - 1 / c0[2]) if c1[2] != c0[2] else k
    return (lerp(c0[0], c1[0], f), lerp(c0[1], c1[1], f), z)
def w2s(cam, x, y): return (MAPC[0] + (x - cam[0]) * cam[2], MAPC[1] + (y - cam[1]) * cam[2])
def state_path(c, n):
    for p in MAPP[n]:
        c.move_to(*p[0])
        for q in p[1:]: c.line_to(*q)
        c.close_path()
def map_draw(c, t, cam, haze=1.0, wash=0.0, fires=0.0, labels=(), clear=0.0, ring=0.0):
    c.set_source_rgb(*SEA); c.paint()
    c.save(); c.translate(*MAPC); c.scale(cam[2], cam[2]); c.translate(-cam[0], -cam[1])
    for i, n in enumerate(MAPP):
        c.new_path(); state_path(c, n); v = 0.03 * ((i * 37) % 5 - 2)
        c.set_source_rgb(PAPER[0] + v, PAPER[1] + v, PAPER[2] + v); c.fill_preserve()
        if wash > 0 and n in CREA_STATES: c.set_source_rgba(*PM10, 0.22 * wash); c.fill_preserve()
        c.set_source_rgba(0.35, 0.30, 0.25, 0.8); c.set_line_width(1.2 / cam[2]); c.stroke()
    if haze > 0:
        for (x, y, r) in IGP:
            rr = r * (1 + 0.04 * math.sin(t * 0.7 + x))
            g = cairo.RadialGradient(x, y, 0, x, y, rr * 1.6); a = 0.62 * haze * (1 - clear)
            g.add_color_stop_rgba(0, *HAZE, a); g.add_color_stop_rgba(0.6, *HAZE, a * 0.6); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g)
            c.new_path(); c.arc(x, y, rr * 1.6, 0, 2 * math.pi); c.fill()
    if fires > 0:
        for i, (x, y) in enumerate(FIRES):
            bl = 0.5 + 0.5 * math.sin(t * 7 + i * 1.9)
            c.set_source_rgba(1.0, 0.45 + 0.3 * bl, 0.1, fires * (0.55 + 0.45 * bl)); c.new_path(); c.arc(x, y, 1.6 + 0.6 * bl, 0, 2 * math.pi); c.fill()
    if ring > 0:
        c.set_source_rgba(*AMBER, 0.9 * (1 - 0.6 * ring)); c.set_line_width(3 / cam[2]); c.new_path(); c.arc(DELHI[0], DELHI[1], 10 + 150 * ring, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.85, 0.15, 0.15); c.new_path(); c.arc(DELHI[0], DELHI[1], 3.2 / max(1, cam[2] / 3), 0, 2 * math.pi); c.fill()
    c.restore()
    for n in labels:
        x, y = w2s(cam, *(DELHI if n == 'Delhi' else CENT[n])); lab = n.upper()
        if n == 'Delhi': x += 46
        mono(c, lab, x, y + (-22 if n == 'Delhi' else 0), 20, INK, a=0.85, kind='monob')
def flats(c, x0, x1, ybase, rng, col, hmin=80, hmax=260):
    x = x0
    while x < x1:
        w = rng.uniform(50, 110); h = rng.uniform(hmin, hmax)
        c.set_source_rgb(*col); c.rectangle(x, ybase - h, w - 6, h); c.fill()
        x += w
def skyline_window(c, t, x0, y0, w, h, haze=1.0):
    c.save(); c.rectangle(x0, y0, w, h); c.clip()
    g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgb(0, 0.78, 0.74, 0.66); g.add_color_stop_rgb(1, 0.62, 0.58, 0.52); c.set_source(g); c.paint()
    c.set_source_rgba(1, 0.92, 0.75, 0.55); c.arc(x0 + w * 0.7, y0 + h * 0.28, 40, 0, 2 * math.pi); c.fill()
    rng = np.random.default_rng(3); flats(c, x0 - 20, x0 + w + 20, y0 + h * 0.80, rng, (0.50, 0.47, 0.44), 60, 180)
    gx, gy = x0 + w * 0.40, y0 + h * 0.80
    c.set_source_rgb(0.45, 0.42, 0.40); c.rectangle(gx - 60, gy - 200, 120, 200); c.fill()
    c.set_source_rgb(0.62, 0.58, 0.52); c.move_to(gx - 30, gy); c.line_to(gx - 30, gy - 110); c.curve_to(gx - 30, gy - 150, gx + 30, gy - 150, gx + 30, gy - 110); c.line_to(gx + 30, gy); c.close_path(); c.fill()
    c.set_source_rgb(0.45, 0.42, 0.40); c.rectangle(gx - 70, gy - 215, 140, 20); c.fill()
    rng2 = np.random.default_rng(9); flats(c, x0 - 20, x0 + w + 20, y0 + h, rng2, (0.36, 0.33, 0.31), 80, 220)
    for k in range(3):
        c.set_source_rgba(*HAZE, (0.28 + 0.12 * k) * haze); c.rectangle(x0, y0 + h * (0.2 + 0.2 * k), w, h); c.fill()
    for i in range(18):   # drifting haze specks
        x = x0 + ((i * 97 + t * 18) % w); y = y0 + (i * 53) % h
        c.set_source_rgba(0.9, 0.9, 0.88, 0.18 * haze); c.arc(x, y, 3 + i % 3, 0, 2 * math.pi); c.fill()
    c.restore()
def room(c, t, curtain=0.7, haze=1.0, shells=True):
    c.set_source_rgb(0.30, 0.24, 0.21); c.rectangle(60, 260, 960, 1080); c.fill()
    wx, wy, ww, wh = 200, 330, 680, 700
    skyline_window(c, t, wx, wy, ww, wh, haze)
    c.set_source_rgb(0.85, 0.82, 0.76); c.set_line_width(18); c.rectangle(wx, wy, ww, wh); c.stroke()
    c.set_line_width(10); c.move_to(wx + ww / 2, wy); c.line_to(wx + ww / 2, wy + wh); c.stroke()
    c.set_source_rgb(0.40, 0.42, 0.45); c.rectangle(wx, wy + wh - 110, ww, 10); c.fill()
    for i in range(6): c.rectangle(wx + 20 + i * 120, wy + wh - 110, 8, 110); c.fill()
    if shells:
        for i, x in enumerate((wx + 140, wx + 190, wx + 520)):
            c.save(); c.translate(x, wy + wh - 116); c.rotate(0.3 * (i - 1)); c.set_source_rgb(0.75, 0.18, 0.15); c.rectangle(-9, -34, 18, 34); c.fill()
            c.set_source_rgb(0.15, 0.12, 0.10); c.rectangle(-9, -38, 18, 6); c.fill(); c.restore()
    cw = ww / 2 * (1 - curtain)
    for side in (0, 1):
        x = wx - 30 if side == 0 else wx + ww + 30 - (cw + 60)
        c.set_source_rgb(0.62, 0.20, 0.22); c.rectangle(x, wy - 40, cw + 60, wh + 80); c.fill()
        c.set_source_rgba(0, 0, 0, 0.18)
        for k in range(4): c.rectangle(x + 10 + k * (cw + 60) / 4, wy - 40, 6, wh + 80); c.fill()
    c.set_source_rgb(0.40, 0.30, 0.24); c.rectangle(60, 1180, 960, 160); c.fill()
def home_draw(c, t, curtain=0.7, haze=1.0, people='raju', shells=True, meera_x=None, nod=0.0):
    room(c, t, curtain, haze, shells)
    if people in ('raju', 'two', 'family'):
        raju_c(c, 270, 1290, 0.62, t, look=(0.6, 0) if people != 'raju' else (0.3, -0.2))
    if people in ('two', 'family'):
        mx = 790 if meera_x is None else meera_x
        meera_c(c, mx, 1290, 0.62, t + 1, look=(-0.6, 0), gesture=0.5 * prog(t, S('M1') - 0.2, S('M1') + 0.3) * (1 - prog(t, E('M2'), E('M2') + 0.4)))
    c.set_source_rgba(*HAZE, 0.10 * haze); c.rectangle(60, 260, 960, 1080); c.fill()
def city_draw(c, t, night=0.0, haze=1.0, lights=1.0):
    c.set_source_rgb(0.40, 0.38, 0.36); c.rectangle(60, 260, 960, 1080); c.fill()
    rng = np.random.default_rng(11)
    for i in range(16):
        for j in range(19):
            x = 70 + i * 60 + rng.uniform(-4, 4); y = 270 + j * 56 + rng.uniform(-4, 4)
            v = rng.uniform(0.45, 0.70); c.set_source_rgb(v, v * 0.95, v * 0.88); c.rectangle(x, y, 48, 44); c.fill()
    c.set_source_rgb(0.42, 0.58, 0.66); c.set_line_width(46)
    c.move_to(860, 260); c.curve_to(760, 560, 960, 820, 820, 1340); c.stroke()
    c.set_source_rgb(0.25, 0.25, 0.27); c.set_line_width(22); c.save(); c.translate(540, 800); c.scale(1, 0.8); c.new_path(); c.arc(0, 0, 330, 0, 2 * math.pi); c.restore(); c.stroke()
    c.set_source_rgb(0.30, 0.42, 0.28); c.new_path(); c.arc(470, 760, 55, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.85, 0.80, 0.70); c.rectangle(455, 745, 30, 30); c.fill()
    mono(c, 'INDIA GATE', 470, 840, 18, CREAM, a=0.9, kind='monob'); mono(c, 'YAMUNA', 850, 600, 18, CREAM, a=0.8, kind='monob')
    if night > 0: c.set_source_rgba(0.03, 0.04, 0.10, 0.72 * night); c.rectangle(60, 260, 960, 1080); c.fill()
    if lights > 0:
        for k in range(46):
            an = (t * 0.25 + k / 46) * 2 * math.pi; x = 540 + 330 * math.cos(an); y = 800 + 264 * math.sin(an)
            c.set_source_rgba(1, 0.92 if k % 2 else 0.35, 0.6 if k % 2 else 0.25, 0.9 * lights); c.new_path(); c.arc(x, y, 5, 0, 2 * math.pi); c.fill()
    for k in range(4):
        c.set_source_rgba(*HAZE, 0.16 * haze * (1 - 0.75 * night)); c.rectangle(60, 260, 960, 1080); c.fill()
def fireworks(c, t, t0, a=1.0):
    rng = np.random.default_rng(21)
    for i in range(9):
        x, y = rng.uniform(150, 930), rng.uniform(380, 1000); st = t0 + rng.uniform(0, 2.2); k = prog(t, st, st + 0.9)
        if 0 < k < 1:
            col = [(1, 0.8, 0.3), (1, 0.4, 0.4), (0.5, 0.8, 1), (0.6, 1, 0.6)][i % 4]
            for q in range(14):
                an = q / 14 * 2 * math.pi; r = 95 * e_out(k)
                c.set_source_rgba(*col, a * (1 - k * 0.7)); c.new_path(); c.arc(x + r * math.cos(an), y + r * math.sin(an), 6, 0, 2 * math.pi); c.fill()
        sk = prog(t, st + 0.3, st + 3)
        if sk > 0:
            g = cairo.RadialGradient(x, y, 0, x, y, 40 + 90 * sk); g.add_color_stop_rgba(0, *HAZE, 0.5 * a * sk); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.new_path(); c.arc(x, y, 40 + 90 * sk, 0, 2 * math.pi); c.fill()
def sky_cut(c, t, lid=0.0, smoke=0.0, sources=0):
    c.save(); c.rectangle(60, 330, 960, 850); c.clip()
    g = cairo.LinearGradient(0, 330, 0, 700); g.add_color_stop_rgb(0, 0.85, 0.52, 0.28); g.add_color_stop_rgb(1, 0.70, 0.45, 0.30); c.set_source(g); c.rectangle(60, 330, 960, 370); c.fill()
    g = cairo.LinearGradient(0, 700, 0, 1110); g.add_color_stop_rgb(0, 0.30, 0.45, 0.62); g.add_color_stop_rgb(1, 0.20, 0.32, 0.48); c.set_source(g); c.rectangle(60, 700, 960, 410); c.fill()
    mono(c, 'WARM AIR', 180, 380, 22, INK, anchor='l', kind='monob'); mono(c, 'COOL AIR', 180, 760, 22, CREAM, anchor='l', kind='monob')
    rng = np.random.default_rng(5); flats(c, 60, 1020, 1110, rng, (0.18, 0.16, 0.15), 60, 200)
    c.set_source_rgb(0.14, 0.12, 0.11); c.rectangle(60, 1110, 960, 70); c.fill()
    srcs = [170, 360, 560, 760]
    for i, x in enumerate(srcs[:sources]):
        glass_dark(c, x - 70, 1120, 140, 52, 16); mono(c, ['VEHICLES', 'DUST', 'INDUSTRY', 'GARBAGE'][i], x, 1146, 16, CREAM, kind='monob')
    if smoke > 0:
        top = 720 if lid > 0.5 else 400
        for i in range(26):
            ph = (t * 0.25 + ((i * 0.618) % 1.0)) % 1.0; x0 = 120 + (i * 37) % 860
            y = 1100 - (1100 - top) * min(1, ph * 1.6); spread = max(0, ph * 1.6 - 1) * (160 if lid > 0.5 else 30)
            x = x0 + spread * (1 if i % 2 else -1); r = 26 + 40 * ph
            g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *HAZE, 0.55 * smoke); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    if lid > 0:
        x = lerp(-900, 60, e_out(lid))
        c.set_source_rgba(0.85, 0.95, 1.0, 0.35); rrect(c, x, 690, 960, 22, 10); c.fill()
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(3); rrect(c, x, 690, 960, 22, 10); c.stroke()
    c.restore()
def street_draw(c, t):
    c.set_source_rgb(0.66, 0.64, 0.60); c.rectangle(60, 260, 960, 1080); c.fill()
    rng = np.random.default_rng(14); flats(c, 60, 1020, 1000, rng, (0.52, 0.50, 0.48), 120, 420)
    c.set_source_rgb(0.28, 0.28, 0.30); c.rectangle(60, 1000, 960, 180); c.fill()
    c.set_source_rgb(0.9, 0.9, 0.85)
    for x in range(80, 1020, 120): c.rectangle(x, 1085, 60, 8); c.fill()
    c.set_source_rgb(0.95, 0.70, 0.15); c.set_line_width(12); c.move_to(220, 1000); c.line_to(220, 520); c.line_to(430, 520); c.stroke()
    c.move_to(410, 520); c.line_to(410, 640); c.set_line_width(4); c.stroke()
    c.set_source_rgb(0.55, 0.20, 0.18); rrect(c, 480, 960, 200, 70, 18); c.fill(); rrect(c, 520, 920, 120, 50, 14); c.fill()
    c.set_source_rgb(0.1, 0.1, 0.1); c.new_path(); c.arc(520, 1035, 22, 0, 2 * math.pi); c.fill(); c.new_path(); c.arc(640, 1035, 22, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.75, 0.60, 0.40); c.rectangle(790, 760, 200, 240); c.fill(); c.set_source_rgb(0.35, 0.25, 0.20); c.rectangle(860, 880, 60, 120); c.fill()
    mono(c, 'SCHOOL', 890, 800, 18, INK, kind='monob')
    for k in range(3): c.set_source_rgba(*HAZE, 0.14); c.rectangle(60, 260, 960, 1080); c.fill()
HEBEI = [(-330, -60), (-260, -230), (-60, -300), (120, -260), (260, -150), (330, 40), (240, 230), (40, 300), (-180, 260), (-310, 120)]
STK = []
def beijing_card(c, t, haze=1.0, stickers=0, tl=0.0):
    c.save(); c.translate(540, 760)
    c.set_source_rgba(0.94, 0.90, 0.80, 1); rrect(c, -460, -420, 920, 840, 28); c.fill()
    c.set_source_rgb(0.80, 0.74, 0.60); c.move_to(*HEBEI[0]); [c.line_to(*p) for p in HEBEI[1:]]; c.close_path(); c.fill()
    c.set_source_rgb(0.70, 0.62, 0.48); c.move_to(-120, -170); c.curve_to(-20, -230, 90, -180, 70, -80); c.curve_to(50, 0, -100, 10, -140, -60); c.close_path(); c.fill()
    c.set_source_rgb(0.72, 0.64, 0.50); c.new_path(); c.arc(170, 10, 52, 0, 2 * math.pi); c.fill()
    mono(c, 'BEIJING', -30, -110, 26, INK, kind='monob'); mono(c, 'TIANJIN', 170, 10, 18, INK, kind='monob'); mono(c, 'HEBEI', -150, 170, 24, INK, kind='monob')
    c.set_source_rgba(0.85, 0.15, 0.15, 1); c.new_path(); c.arc(-30, -150, 7, 0, 2 * math.pi); c.fill()
    if haze > 0:
        for k in range(3):
            g = cairo.RadialGradient(-20, -60, 0, -20, -60, 330); g.add_color_stop_rgba(0, *HAZE, 0.42 * haze); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.new_path(); c.arc(-20, -60, 330, 0, 2 * math.pi); c.fill()
    icons = [(-300, -340, 'COAL PLANTS SHUT'), (300, -340, 'HOMES: GAS + POWER'), (-300, 340, 'VEHICLE RULES'), (300, 340, 'REGIONAL TEAMWORK')]
    for i, (x, y, lab) in enumerate(icons[:stickers]):
        u = e_back(prog(t, STK[i], STK[i] + 0.3)) if i < len(STK) else 1
        c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -150, -38, 300, 76, 20)
        mono(c, lab, 0, 0, 18, CREAM, kind='monob'); c.restore()
        if i == 3 and u > 0.5:
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(5); c.move_to(-30, -150); c.line_to(170, 10); c.stroke(); c.move_to(-30, -150); c.line_to(-150, 170); c.stroke()
    if tl > 0:
        c.set_source_rgba(*INK, 0.7); c.set_line_width(4); c.move_to(-380, 395); c.line_to(-380 + 760 * tl, 395); c.stroke()
        mono(c, '2013', -380, 375, 18, INK, kind='monob')
        if tl > 0.95: mono(c, '2025', 380, 375, 18, INK, kind='monob')
    c.restore()

# ---------------- NEW: inside the body (cinematic) ----------------
def cine_bg(c, t, col=(0.04, 0.06, 0.09)):
    c.set_source_rgb(*col); c.rectangle(60, 260, 960, 1080); c.fill()
    rng = np.random.default_rng(31)
    for i in range(40):     # out-of-focus dust (bokeh)
        x = 60 + (rng.uniform(0, 960) + t * rng.uniform(4, 20)) % 960; y = 260 + (rng.uniform(0, 1080) + 6 * math.sin(t + i)) % 1080; r = rng.uniform(8, 38)
        g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, 0.75, 0.75, 0.72, rng.uniform(0.04, 0.14)); g.add_color_stop_rgba(1, 0.75, 0.75, 0.72, 0)
        c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
def vignette(c, a=0.55):
    g = cairo.RadialGradient(540, 800, 260, 540, 800, 820); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    c.set_source(g); c.rectangle(60, 260, 960, 1080); c.fill()
def pm_dot(c, x, y, r, t, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 3.2); g.add_color_stop_rgba(0, *AMBER, 0.55 * a); g.add_color_stop_rgba(1, *AMBER, 0); c.set_source(g); c.new_path(); c.arc(x, y, r * 3.2, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1.0, 0.80, 0.35, a); c.new_path()
    for q in range(9):   # lumpy soot particle
        an = q / 9 * 2 * math.pi; rr = r * (0.82 + 0.25 * math.sin(q * 2.3 + 1))
        (c.move_to if q == 0 else c.line_to)(x + rr * math.cos(an), y + rr * math.sin(an))
    c.close_path(); c.fill()
def macro_hair(c, t, k):
    """the human hair next to one PM2.5 particle, in a magnified circle"""
    cine_bg(c, t)
    z = 1.0 + 0.12 * k
    c.save(); c.translate(540, 760); c.scale(z, z); c.translate(-540, -760)
    c.save(); c.translate(540, 760); c.rotate(-0.42)
    g = cairo.LinearGradient(0, -140, 0, 140); g.add_color_stop_rgb(0, 0.30, 0.20, 0.12); g.add_color_stop_rgb(0.35, 0.62, 0.45, 0.28); g.add_color_stop_rgb(0.6, 0.48, 0.33, 0.20); g.add_color_stop_rgb(1, 0.22, 0.14, 0.09)
    c.set_source(g); c.rectangle(-900, -140, 1800, 280); c.fill()
    c.set_source_rgba(0.15, 0.09, 0.05, 0.45); c.set_line_width(4)
    for xx in range(-900, 900, 70):    # cuticle scales
        c.move_to(xx, -140); c.curve_to(xx + 30, -60, xx + 30, 60, xx, 140); c.stroke()
    c.restore()
    for i in range(14):
        x = 120 + (i * 131 + t * 10) % 840; y = 330 + (i * 211) % 900
        if abs((y - 760) + (x - 540) * 0.45) < 170: continue
        c.set_source_rgba(0.6, 0.6, 0.58, 0.35); c.new_path(); c.arc(x, y, 3 + i % 4, 0, 2 * math.pi); c.fill()
    px, py = 760, 1040 + 8 * math.sin(t * 1.3)
    pm_dot(c, px, py, 9, t)
    c.restore()
    u = prog(t, A['tiny'] - 0.4, A['tiny'] + 0.2)
    pill(c, 'HAIR ≈ 70 µm', 330, 520, 24, CREAM, col=INK, a=u)
    pill(c, 'PM2.5 ≤ 2.5 µm', 760, 1150, 24, AMBER, a=u)
    if t >= A['hair'] - 0.1: pill(c, '≈ 30× SMALLER', 540, 1290, 30, AMBER, s=e_back(prog(t, A['hair'] - 0.1, A['hair'] + 0.2)))
    vignette(c, 0.7)
    c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(3); c.new_path(); c.arc(540, 800, 520, 0, 2 * math.pi); c.stroke()   # lens edge
LUNG_L = [(500, 760), (440, 760), (350, 820), (300, 960), (300, 1110), (380, 1170), (470, 1140), (500, 1040)]
LUNG_R = [(580, 760), (640, 760), (730, 820), (780, 960), (780, 1110), (700, 1170), (610, 1140), (590, 1080)]
def blob(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]; c.curve_to((2 * x0 + x1) / 3, (2 * y0 + y1) / 3 + 0, (x0 + 2 * x1) / 3, (y0 + 2 * y1) / 3, x1, y1)
    c.close_path()
BR = [((540, 700), (540, 790)), ((540, 790), (450, 850)), ((540, 790), (630, 850)), ((450, 850), (380, 930)), ((450, 850), (430, 1010)),
      ((630, 850), (700, 930)), ((630, 850), (650, 1010)), ((380, 930), (340, 1040)), ((430, 1010), (400, 1110)), ((700, 930), (740, 1040)), ((650, 1010), (690, 1110))]
SPOTS = [(345, 1030), (400, 1100), (435, 1000), (740, 1040), (690, 1105), (650, 1000), (375, 930), (705, 930)]
def body_xray(c, t, scan=1.0, flow=0.0, react=0.0, blood=0.0, heart=0.0, brain=0.0, breathe=True):
    """Raju from the front; an x-ray band reveals what happens under the shirt"""
    cine_bg(c, t, (0.05, 0.07, 0.10))
    br = 1 + (0.025 * math.sin(t * 2.2) if breathe else 0); cough = 6 * math.sin(t * 40) * (prog(t, A['xr'] + 2.2, A['xr'] + 2.4) * (1 - prog(t, A['xr'] + 2.7, A['xr'] + 2.9)))
    c.save(); c.translate(cough, 0)
    # outside: skin, shirt
    c.set_source_rgb(*SKIN); rrect(c, 495, 560, 90, 120, 30); c.fill()
    c.save(); c.translate(540, 1000); c.scale(br, br); c.translate(-540, -1000)
    c.set_source_rgb(*RAJU_SHIRT); rrect(c, 220, 650, 640, 720, 140); c.fill()
    c.restore()
    c.set_source_rgb(*SKIN); c.new_path(); c.arc(540, 450, 150, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*HAIR); c.new_path(); c.arc(540, 420, 156, math.pi * 1.02, math.pi * 1.98); c.fill()
    bk = blink(t)
    for sx in (-50, 50): c.save(); c.translate(540 + sx, 455); c.scale(1, bk); c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore(); c.set_source_rgb(*HAIR); c.fill()
    c.set_source_rgb(0.65, 0.45, 0.33); c.new_path(); c.arc(540, 505, 12, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*HAIR); c.set_line_width(7); c.new_path(); c.arc(540, 520, 36, 0.25 * math.pi, 0.75 * math.pi); c.stroke()
    # x-ray reveal: everything above the scan line becomes see-through
    ys = 300 + 1100 * scan
    c.save(); c.rectangle(60, 260, 960, ys - 260); c.clip()
    c.set_source_rgba(0.10, 0.25, 0.40, 0.92); rrect(c, 220, 650, 640, 720, 140); c.fill()
    rrect(c, 495, 560, 90, 120, 30); c.fill()
    hx = max(blood, 0.0)
    if hx > 0: c.set_source_rgba(0.10, 0.25, 0.40, 0.92 * hx); c.new_path(); c.arc(540, 450, 150, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.75, 0.88, 1.0, 0.25); c.set_line_width(5)
    for yy in range(800, 1200, 55): c.new_path(); c.arc(540, yy - 200, 300, 0.2 * math.pi, 0.8 * math.pi); c.stroke()   # ribs
    # brain
    bcol = (1.0, 0.35, 0.35) if brain > 0 else (0.95, 0.70, 0.75)
    c.set_source_rgba(*bcol, (0.55 + 0.35 * brain * (0.5 + 0.5 * math.sin(t * 12))) * hx); c.save(); c.translate(540, 400); c.scale(1.2, 0.85); c.new_path(); c.arc(0, 0, 100, 0, 2 * math.pi); c.restore(); c.fill()
    # lungs
    for pts in (LUNG_L, LUNG_R):
        blob(c, pts); c.set_source_rgba(0.95, 0.55, 0.60, 0.55); c.fill_preserve(); c.set_source_rgba(1, 0.8, 0.85, 0.8); c.set_line_width(3); c.stroke()
    # airway
    c.set_source_rgba(0.85, 0.95, 1.0, 0.9); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(540, 560 if hx < 0.5 else 505); c.line_to(540, 700); c.stroke()
    for (a_, b_) in BR:
        c.set_line_width(10 if a_[1] < 800 else 6); c.move_to(*a_); c.line_to(*b_); c.stroke()
    # heart + vessels
    hb = 1 + (0.10 + 0.12 * heart) * max(0, math.sin(t * (7 + 6 * heart)))
    c.save(); c.translate(575, 1010); c.scale(hb, hb)
    c.set_source_rgba(0.85, 0.12 + 0.1 * (1 - heart), 0.15, 0.95); c.move_to(0, 60); c.curve_to(-90, 0, -60, -70, 0, -30); c.curve_to(60, -70, 90, 0, 0, 60); c.fill(); c.restore()
    if blood > 0:
        c.set_source_rgba(0.85, 0.15, 0.18, 0.85 * blood); c.set_line_width(9)
        c.move_to(470, 1040); c.curve_to(500, 1060, 540, 1030, 560, 1010); c.stroke()      # lung → heart
        c.move_to(585, 960); c.curve_to(600, 800, 560, 700, 560, 560); c.line_to(560, 470); c.stroke()  # heart → neck → brain
        for i in range(10):    # blood cells carrying the particle along
            ph = (t * 0.6 + i / 10) % 1.0
            if ph < 0.35: u = ph / 0.35; x = lerp(470, 560, u); y = lerp(1040, 1010, u)
            else: u = (ph - 0.35) / 0.65; x = lerp(585, 560, u); y = lerp(960, 480, u)
            if i % 3 == 0: pm_dot(c, x, y, 6, t, a=blood)
            else: c.set_source_rgba(0.95, 0.25, 0.25, blood); c.new_path(); c.arc(x, y, 8, 0, 2 * math.pi); c.fill()
    # particles flowing in with each breath
    if flow > 0:
        for i, sp in enumerate(SPOTS):
            ph = clamp((flow * 1.4 - i * 0.05), 0, 1)
            if ph <= 0: continue
            pts = [(540, 505), (540, 700), (540, 790), (450 if sp[0] < 540 else 630, 850), sp]
            seg = ph * (len(pts) - 1); j = min(int(seg), len(pts) - 2); u = seg - j
            x = lerp(pts[j][0], pts[j + 1][0], u); y = lerp(pts[j][1], pts[j + 1][1], u)
            pm_dot(c, x, y, 7, t)
            if ph >= 1 and react > 0:   # the body reacts: the spot gets inflamed
                g = cairo.RadialGradient(x, y, 0, x, y, 55); g.add_color_stop_rgba(0, 1, 0.15, 0.1, 0.7 * react); g.add_color_stop_rgba(1, 1, 0.15, 0.1, 0); c.set_source(g); c.new_path(); c.arc(x, y, 55, 0, 2 * math.pi); c.fill()
    c.restore()
    # scan band
    if 0 < scan < 1:
        g = cairo.LinearGradient(0, ys - 40, 0, ys + 6); g.add_color_stop_rgba(0, 0.5, 0.9, 1, 0); g.add_color_stop_rgba(1, 0.6, 0.95, 1, 0.8)
        c.set_source(g); c.rectangle(60, ys - 40, 960, 46); c.fill()
    # breath in: little air arrows to the nose
    if flow > 0 and flow < 1:
        for i in range(5):
            ph = (t * 1.2 + i / 5) % 1.0; x = lerp(860, 560, ph); y = lerp(380 + i * 30, 505, ph)
            c.set_source_rgba(0.8, 0.8, 0.8, 0.5 * (1 - ph)); c.new_path(); c.arc(x, y, 6, 0, 2 * math.pi); c.fill()
    c.restore()
    vignette(c, 0.6)
def alveoli(c, t, k, cross=0.0, immune=0.0):
    """deep inside the lung: air sacs, the particle crosses into a capillary"""
    cine_bg(c, t, (0.12, 0.03, 0.05))
    z = 1 + 0.10 * k; c.save(); c.translate(540, 800); c.scale(z, z); c.translate(-540, -800)
    rng = np.random.default_rng(41)
    for i in range(26):
        x = rng.uniform(140, 940); y = rng.uniform(340, 1260); r = rng.uniform(70, 130)
        g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.add_color_stop_rgba(0, 1, 0.78, 0.80, 0.95); g.add_color_stop_rgba(1, 0.85, 0.40, 0.48, 0.95)
        c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(0.6, 0.15, 0.2, 0.5); c.set_line_width(3); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.stroke()
    # capillary across the middle with blood cells
    c.set_source_rgba(0.55, 0.05, 0.08, 0.9); c.set_line_width(90); c.move_to(40, 980); c.curve_to(380, 860, 700, 1120, 1040, 960); c.stroke()
    for i in range(16):
        ph = (t * 0.35 + i / 16) % 1.0; x = 40 + 1000 * ph; y = 980 + 70 * math.sin(ph * math.pi * 2) * -1 + 0
        c.save(); c.translate(x, y); c.scale(1, 0.62); c.set_source_rgba(0.95, 0.20, 0.22, 1); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(0.75, 0.10, 0.14, 1); c.new_path(); c.arc(0, 0, 11, 0, 2 * math.pi); c.fill(); c.restore()
    # the particle: sitting in an air sac, then slipping through the wall
    px = lerp(520, 600, e_io(cross)); py = lerp(720, 975, e_io(cross)) + (0 if cross < 1 else 0)
    if cross >= 1: px = lerp(600, 1040, prog(t, A['blood'] + 0.6, A['blood'] + 2.4)); py = 975 - 20 * math.sin(px / 120)
    g = cairo.RadialGradient(520, 720, 0, 520, 720, 160); g.add_color_stop_rgba(0, 1, 0.1, 0.1, 0.45 * immune); g.add_color_stop_rgba(1, 1, 0.1, 0.1, 0); c.set_source(g); c.new_path(); c.arc(520, 720, 160, 0, 2 * math.pi); c.fill()
    pm_dot(c, px, py, 16, t)
    for i in range(4):    # immune cells crawl toward it
        an = i * 1.6 + 0.4; d = lerp(260, 90, e_out(immune))
        x = 520 + d * math.cos(an); y = 720 + d * math.sin(an)
        c.set_source_rgba(0.95, 0.95, 0.92, 0.9 * min(1, immune * 2)); c.new_path()
        for q in range(10):
            a_ = q / 10 * 2 * math.pi; rr = 30 * (1 + 0.18 * math.sin(q * 3 + t * 5 + i))
            (c.move_to if q == 0 else c.line_to)(x + rr * math.cos(a_), y + rr * math.sin(a_))
        c.close_path(); c.fill()
        c.set_source_rgba(0.55, 0.45, 0.75, 0.9 * min(1, immune * 2)); c.new_path(); c.arc(x, y, 10, 0, 2 * math.pi); c.fill()
    c.restore()
    vignette(c, 0.65)


# ---------------- NEW v6: real-image body sequence (Unsplash, free licence) ----------------
RIMG = {}
def rimg(name):
    if name not in RIMG:
        im = Image.open(ROOT + 'real/' + name + '.jpg').convert('RGB')
        RIMG[name] = (surf_from_pil(im)[0], im.size)
    return RIMG[name]
PX, PY, PW, PH = 60, 260, 960, 1080
def cover(c, name, fx, fy, z=1.0, a=1.0, dx=0.0, dy=0.0):
    """paint a photo to cover the panel, centred on focal point (fx, fy) in 0..1 image coords; returns mapper img->screen"""
    sf, (iw, ih) = rimg(name); sc = max(PW / iw, PH / ih) * z
    ox = PX + PW / 2 - fx * iw * sc + dx; oy = PY + PH / 2 - fy * ih * sc + dy
    c.save(); c.rectangle(PX, PY, PW, PH); c.clip(); c.translate(ox, oy); c.scale(sc, sc); c.set_source_surface(sf, 0, 0); c.paint_with_alpha(a); c.restore()
    return lambda u, v: (ox + u * iw * sc, oy + v * ih * sc)
def grade(c, dark=0.35, tint=None, ta=0.0):
    c.save(); c.rectangle(PX, PY, PW, PH); c.clip()
    if tint: c.set_source_rgba(*tint, ta); c.paint()
    vignette(c, dark); c.restore()
def hair_curve(c, x0, y0, x1, y1, w, a=1.0):
    """one real-scale hair lying on the table: thin, slightly wavy, with a soft shadow and a highlight"""
    def path(dx, dy):
        c.new_path(); c.move_to(x0 + dx, y0 + dy); c.curve_to(x0 + (x1 - x0) * 0.3 + dx, y0 - 120 + dy, x0 + (x1 - x0) * 0.65 + dx, y1 + 140 + dy, x1 + dx, y1 + dy)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    path(3, 5); c.set_source_rgba(0, 0, 0, 0.35 * a); c.set_line_width(w * 2.2); c.stroke()
    path(0, 0); c.set_source_rgba(0.09, 0.06, 0.04, a); c.set_line_width(w); c.stroke()
    path(-w * 0.2, -w * 0.25); c.set_source_rgba(0.75, 0.60, 0.45, 0.55 * a); c.set_line_width(max(1, w * 0.25)); c.stroke()
def micro_field(c, t, k):
    """bright-field microscope view: one strand of hair, ~70 µm, next to a 2.5 µm soot particle drawn to true scale"""
    c.set_source_rgb(0.02, 0.02, 0.03); c.rectangle(PX, PY, PW, PH); c.fill()
    cx, cy, R = 540, 780, 450
    c.save(); c.new_path(); c.arc(cx, cy, R, 0, 2 * math.pi); c.clip()
    g = cairo.RadialGradient(cx - 80, cy - 120, 40, cx, cy, R); g.add_color_stop_rgb(0, 0.93, 0.92, 0.86); g.add_color_stop_rgb(1, 0.62, 0.62, 0.58); c.set_source(g); c.paint()
    cover(c, 'hair', 0.55, 0.5, z=1.4, a=0.10)             # faint out-of-focus strands behind
    z = 1 + 0.06 * k
    c.save(); c.translate(cx, cy); c.scale(z, z); c.rotate(-0.38)
    Wd = 280                                              # strand width = 70 µm  ->  4 px per µm
    gg = cairo.LinearGradient(0, -Wd / 2, 0, Wd / 2)
    for p, col in ((0, (0.16, 0.10, 0.06)), (0.18, (0.42, 0.28, 0.17)), (0.38, (0.66, 0.50, 0.33)), (0.48, (0.80, 0.66, 0.48)), (0.62, (0.55, 0.39, 0.24)), (0.86, (0.30, 0.19, 0.11)), (1, (0.12, 0.07, 0.04))):
        gg.add_color_stop_rgb(p, *col)
    c.set_source(gg); c.rectangle(-900, -Wd / 2, 1800, Wd); c.fill()
    for i, xx in enumerate(range(-900, 900, 46)):             # cuticle scales, overlapping roof tiles
        c.new_path(); c.move_to(xx, -Wd / 2); c.curve_to(xx + 34, -Wd / 4, xx + 30 + 6 * math.sin(i), Wd / 4, xx + 8, Wd / 2)
        c.set_source_rgba(0.12, 0.07, 0.04, 0.35); c.set_line_width(3); c.stroke_preserve(); c.set_source_rgba(1, 0.9, 0.75, 0.10); c.set_line_width(1.5); c.stroke()
    c.restore()
    # the particle: 2.5 µm -> 10 px at this scale, a fluffy soot aggregate
    px, py = 760 + 4 * math.sin(t * 0.9), 1030 + 4 * math.cos(t * 0.7)
    rng = np.random.default_rng(7)
    for j in range(9):
        a_ = rng.uniform(0, 2 * math.pi); d = rng.uniform(0, 4); r = rng.uniform(2.0, 3.4)
        x, y = px + d * math.cos(a_), py + d * math.sin(a_)
        gq = cairo.RadialGradient(x - r * 0.4, y - r * 0.4, 0, x, y, r); gq.add_color_stop_rgb(0, 0.35, 0.33, 0.30); gq.add_color_stop_rgb(1, 0.05, 0.05, 0.05)
        c.set_source(gq); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.restore()
    c.set_source_rgba(0.85, 0.85, 0.85, 0.8); c.set_line_width(10); c.new_path(); c.arc(cx, cy, R + 4, 0, 2 * math.pi); c.stroke()   # eyepiece ring
    u = prog(t, A['hair'] - 0.2, A['hair'] + 0.2)
    if u > 0:
        # calipers on the hair and an arrow to the particle
        c.save(); c.translate(cx, cy); c.rotate(-0.38); c.set_source_rgba(1, 1, 1, 0.95 * u); c.set_line_width(3)
        c.move_to(-200, -150); c.line_to(-200, 150); c.stroke(); c.move_to(-215, -140); c.line_to(-185, -140); c.stroke(); c.move_to(-215, 140); c.line_to(-185, 140); c.stroke(); c.restore()
        pill(c, 'ONE HAIR · ≈ 70 µm', 330, 520, 24, CREAM, col=INK, a=u)
        c.set_source_rgba(*AMBER, u); c.set_line_width(4); c.arc(px, py, 22, 0, 2 * math.pi); c.stroke(); c.move_to(px + 18, py + 18); c.line_to(px + 70, py + 120); c.stroke()
        pill(c, 'PM2.5 · 2.5 µm', 830, 1170, 24, AMBER, a=u)
    if t >= A['hair'] + 0.5: pill(c, '≈ 30× SMALLER · DRAWN TO SCALE', 540, 1290, 26, AMBER, s=e_back(prog(t, A['hair'] + 0.5, A['hair'] + 0.8)))
LUNG_PTS = [(0.30, 0.50), (0.27, 0.68), (0.36, 0.80), (0.40, 0.58), (0.62, 0.52), (0.68, 0.66), (0.60, 0.80), (0.72, 0.78), (0.33, 0.38), (0.66, 0.38)]
def real_lungs(c, t, k, flow, react):
    c.set_source_rgb(0.80, 0.66, 0.54); c.rectangle(PX, PY, PW, PH); c.fill()
    m = cover(c, 'lungs', 0.495, 0.50, z=0.92 + 0.10 * k)
    grade(c, 0.75, (0.05, 0.02, 0.03), 0.35)
    for i, (u, v) in enumerate(LUNG_PTS):
        ph = clamp(flow * 1.5 - i * 0.05, 0, 1)
        if ph <= 0: continue
        pts = [(0.495, 0.02), (0.495, 0.33), (0.45 if u < 0.5 else 0.54, 0.40), (u, v)]
        seg = ph * 3; j = min(int(seg), 2); f = seg - j
        x, y = m(lerp(pts[j][0], pts[j + 1][0], f), lerp(pts[j][1], pts[j + 1][1], f))
        pm_dot(c, x, y, 6, t)
        if ph >= 1 and react > 0:
            g = cairo.RadialGradient(x, y, 0, x, y, 70); g.add_color_stop_rgba(0, 1, 0.12, 0.08, 0.65 * react); g.add_color_stop_rgba(1, 1, 0.12, 0.08, 0); c.set_source(g); c.new_path(); c.arc(x, y, 70, 0, 2 * math.pi); c.fill()
    for i in range(16):        # the breath carrying dust in
        ph = (t * 0.9 + i / 16) % 1.0; x, y = m(0.495 + 0.02 * math.sin(i), lerp(-0.25, 0.30, ph))
        c.set_source_rgba(0.85, 0.85, 0.82, 0.45 * (1 - ph) * (1 - prog(flow, 0.8, 1))); c.new_path(); c.arc(x, y, 3 + i % 3, 0, 2 * math.pi); c.fill()
def real_blood(c, t, k, n=1.0):
    cover(c, 'rbc', lerp(0.35, 0.62, k), 0.5, z=1.15)
    grade(c, 0.6)
    for i in range(14):
        ph = (t * 0.22 + i / 14) % 1.0; x = PX + PW * ph; y = 380 + (i * 97) % 880 + 20 * math.sin(t + i)
        pm_dot(c, x, y, 5 + (i % 3) * 2, t, a=n)
def real_heart(c, t, beat):
    bt = max(0, math.sin(t * 7.5)) ** 3
    m = cover(c, 'heart', 0.52, 0.42, z=1.9 * (1 + 0.035 * bt))
    c.save(); c.rectangle(PX, PY, PW, PH); c.clip()
    g = cairo.RadialGradient(540, 760, 260, 540, 760, 620); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.02, 0.0, 0.0, 0.92); c.set_source(g); c.paint()
    g = cairo.RadialGradient(540, 760, 0, 540, 760, 420); g.add_color_stop_rgba(0, 1, 0.1, 0.05, 0.30 * beat * bt); g.add_color_stop_rgba(1, 1, 0.1, 0.05, 0); c.set_source(g); c.paint()
    c.restore()
def real_brain(c, t, flash):
    cover(c, 'brain', 0.55, 0.40, z=1.05)
    c.save(); c.rectangle(PX, PY, PW, PH); c.clip()
    fl = flash * (0.5 + 0.5 * math.sin(t * 10))
    g = cairo.RadialGradient(600, 700, 0, 600, 700, 260); g.add_color_stop_rgba(0, 1, 0.12, 0.08, 0.75 * fl); g.add_color_stop_rgba(1, 1, 0.12, 0.08, 0); c.set_source(g); c.paint()
    c.restore(); vignette(c, 0.55)

# ---------------- NEW: Gurpreet's field in Punjab ----------------
def field_draw(c, t, burn=0.0):
    g = cairo.LinearGradient(0, 260, 0, 760); g.add_color_stop_rgb(0, 0.80, 0.70, 0.55); g.add_color_stop_rgb(1, 0.90, 0.78, 0.58); c.set_source(g); c.rectangle(60, 260, 960, 500); c.fill()
    c.set_source_rgba(1, 0.9, 0.7, 0.7); c.new_path(); c.arc(780, 430, 50, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.42, 0.48, 0.32)
    for i in range(14): c.new_path(); c.arc(80 + i * 72, 760, 50 + (i * 17) % 30, math.pi, 2 * math.pi); c.fill()
    g = cairo.LinearGradient(0, 760, 0, 1340); g.add_color_stop_rgb(0, 0.78, 0.64, 0.30); g.add_color_stop_rgb(1, 0.62, 0.48, 0.20); c.set_source(g); c.rectangle(60, 760, 960, 580); c.fill()
    c.set_source_rgba(0.45, 0.33, 0.12, 0.6); c.set_line_width(3)
    for i in range(-12, 13):   # stubble rows in perspective
        c.move_to(540 + i * 14, 760); c.line_to(540 + i * 110, 1340); c.stroke()
    for j in range(18):
        y = 770 + (j ** 1.6) * 6.5
        for i in range(30):
            x = 60 + (i * 37 + j * 19) % 960; h = 6 + j * 0.9
            c.set_source_rgba(0.88, 0.76, 0.40, 0.9); c.move_to(x, y); c.line_to(x + 1, y - h); c.set_line_width(2); c.stroke()
    # combine harvester in the distance
    c.save(); c.translate(780, 820)
    c.set_source_rgb(0.20, 0.50, 0.25); rrect(c, -90, -70, 180, 70, 12); c.fill(); rrect(c, -30, -110, 80, 45, 8); c.fill()
    c.set_source_rgb(0.12, 0.12, 0.12); c.new_path(); c.arc(-50, 4, 20, 0, 2 * math.pi); c.fill(); c.new_path(); c.arc(55, 4, 26, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.85, 0.75, 0.20); c.rectangle(-150, -20, 70, 18); c.fill(); c.restore()
    if burn > 0:   # a stubble fire and its smoke
        for i in range(10):
            x = 330 + i * 26; fl = 0.5 + 0.5 * math.sin(t * 9 + i)
            c.set_source_rgba(1, 0.5 + 0.3 * fl, 0.1, burn); c.move_to(x - 12, 900); c.line_to(x, 900 - 30 - 20 * fl); c.line_to(x + 12, 900); c.close_path(); c.fill()
        for i in range(8):
            ph = (t * 0.2 + i / 8) % 1.0; x = 450 + 260 * ph; y = 880 - 520 * ph; r = 40 + 90 * ph
            g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, 0.45, 0.43, 0.42, 0.55 * burn * (1 - ph * 0.6)); g.add_color_stop_rgba(1, 0.45, 0.43, 0.42, 0)
            c.set_source(g); c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); c.fill()

# ---------------- small bits ----------------
SECT = ['PROBLEM', 'WHY', 'PUNJAB', 'ACTION', 'BEIJING', 'FIX']
def strip(c, active):
    xs = [130, 300, 470, 640, 800, 950]
    for i, (w_, x) in enumerate(zip(SECT, xs)):
        if i == active: pill(c, w_, x, 215, 20, AMBER)
        else: mono(c, w_, x, 215, 16, AMBER if i < active else CREAM, a=0.55 if i < active else 0.28, kind='monob')
def locator(c, txt):
    if LANGV == 'te' and txt in TT.TR: pill(c, txt, 920, 119, 18, CREAM); return
    font(c, 'monob', 18); e = c.text_extents(txt); glass_dark(c, 1010 - e.x_advance - 40, 97, e.x_advance + 40, 44, 22); c.move_to(1010 - e.x_advance - 20, 126); c.set_source_rgb(*CREAM); c.show_text(txt)
def layer(c, fn, a=1.0, s=1.0, cx=540, cy=800, dx=0.0):
    if a <= 0.005: return
    c.save(); c.rectangle(60, 260, 960, 1080); c.clip(); c.push_group(); c.translate(cx + dx, cy); c.scale(s, s); c.translate(-cx, -cy); fn(c); c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def bars2(c, t, t0):
    base = 1180; sc = 1.15
    for j, (lab, v, x, col) in enumerate((('BEFORE', 156.6, 380, CREAM), ('AFTER', 488, 700, PM25))):
        kk = e_out(prog(t, t0 + 0.4 * j, t0 + 0.4 * j + 0.8)); h = v * sc * kk
        c.set_source_rgba(*col, 0.92); rrect(c, x - 80, base - h, 160, h, 14); c.fill()
        if kk > 0.2:
            head(c, f'{v:g}' if v != 488 else '488', x, base - h - 40, 54, col, a=prog(kk, 0.2, 0.6))
            mono(c, lab, x, base + 26, 20, CREAM, kind='monob')
    c.set_source_rgba(0.9, 0.3, 0.3, 0.95); c.set_line_width(4); c.set_dash([14, 10]); c.move_to(240, base - 60 * sc); c.line_to(860, base - 60 * sc); c.stroke(); c.set_dash([])
    mono(c, "INDIA'S 24-HR LIMIT · 60", 250, base - 60 * sc - 18, 18, (1, 0.6, 0.6), anchor='l', kind='monob')
    mono(c, 'PM2.5 · µg/m³ · DIWALI 2025 · CPCB DATA (CLIMATE TRENDS)', W / 2, base + 64, 17, CREAM, a=0.8, kind='mono')
def pin(c, x, y, n, lab, t, t0, filled_t=None):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); c.save(); c.translate(x, y - (1 - min(1, u)) * 80)
    filled = filled_t is not None and t >= filled_t
    c.set_source_rgba(*(AMBER if filled else CREAM), 1); c.new_path(); c.arc(0, 0, 34, 0, 2 * math.pi); c.fill(); c.move_to(-16, 26); c.line_to(0, 64); c.line_to(16, 26); c.close_path(); c.fill()
    head(c, str(n), 0, 2, 40, INK, shadow=False); c.restore()
    if filled: pill(c, lab, x, y + 100, 24, AMBER, s=e_back(prog(t, filled_t, filled_t + 0.3)))
def donut(c, t, t0, cx=540, cy=720, r=200):
    k = e_out(prog(t, t0, t0 + 0.8)); share = 0.52
    c.set_line_width(70)
    c.set_source_rgba(*CREAM, 0.35); c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi); c.stroke()
    c.set_source_rgba(*PM25, 1); c.new_path(); c.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * share * k); c.stroke()
    head(c, '≈ 51–53%', cx, cy - 10, 60, AMBER); mono(c, 'VEHICLES', cx, cy + 50, 22, CREAM, kind='monob')
def dotgrid(c, t, t0, lit_t, cx=250, cy=1080):
    for i in range(100):
        r_, q = divmod(i, 10); x = cx - 135 + q * 30; y = cy - 135 + r_ * 30
        on = t >= lit_t + 0.02 * i if i < 23 else False
        if t < t0 + 0.005 * i: continue
        if i == 99: c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(3); c.new_path(); c.arc(x, y, 11, 0, 2 * math.pi); c.stroke()
        c.set_source_rgba(*(PM10 if on else CREAM), 0.95 if on else 0.3); c.new_path(); c.arc(x, y, 9, 0, 2 * math.pi); c.fill()
def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    cur = 0.7 if frozen else 0.7 + 0.25 * e_io(prog(t, 0.3, 2.0))
    home_draw(c, tt, curtain=cur, people='raju')
    if frozen or t < A['window'] + 1.2:
        a = 1.0 if frozen else 1 - prog(t, A['window'] + 0.8, A['window'] + 1.2)
        mono(c, 'DIWALI · DELHI', W / 2, 1210, 28, CREAM, a=a, kind='monob')
        head(c, 'WHY DELHI CHOKES', W / 2, 1300, 84, AMBER, a=a)
def bar_pair(c, t, t0, items, cap1, cap2, x0=140, base=1230, scale=14):
    u = e_out(prog(t, t0, t0 + 0.35))
    if u <= 0.01: return
    glass_dark(c, x0, 520, 800, 820, 30, u)
    for j, (lab, v, tv) in enumerate(items):
        x = x0 + 230 + j * 340; kk = e_out(prog(t, tv, tv + 0.7)); h = v * scale * kk
        c.set_source_rgba(*(AMBER if j else CREAM), 0.95 * u); rrect(c, x - 90, base - h, 180, h, 14); c.fill()
        if kk > 0.1: head(c, f'{v}%', x, base - h - 40, 56, AMBER if j else CREAM, a=u)
        mono(c, lab, x, base + 30, 20, CREAM, a=u, kind='monob')
    mono(c, cap1, x0 + 400, 570, 18, CREAM, a=u, kind='monob'); mono(c, cap2, x0 + 400, 600, 16, CREAM, a=0.8 * u, kind='mono')

CAM_INDIA = (306, 348, 1.55); CAM_NORTH = (205, 205, 4.2); CAM_PH = (163, 178, 6.0); CAM_DELHI = (DELHI[0], DELHI[1], 40.0); CAM_NI = (230, 225, 3.0)
CAM_FIELD = (158, 168, 60.0)
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True; loc = None; sec = None
    if t < S('M1') - 0.3:                                  # 1 frame 0: Raju at the window
        sc_hook(c, t); loc = 'HOME · DELHI'; sec = 0
    elif t < S('3') - 0.15:                                # M1, 2, M2: Meera walks in and asks
        mx = lerp(1150, 800, e_out(prog(t, S('M1') - 0.3, S('M1') + 0.6)))
        push = e_io(prog(t, E('M2') - 0.2, S('3') - 0.15))
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95, people='two', meera_x=mx), s=1 + 1.8 * push, cx=540, cy=620)
        for k in ('M1', 'M2'):
            if S(k) - 0.1 <= t <= E(k) + 0.3:
                qmark(c, mx + 30, 700, t); bubble(c, QTXT[k], 560, 470, 700, t, S(k) - 0.1, tail=(1, 1)); caps = False
        loc = 'HOME · DELHI'; sec = 0
    elif t < A['hair'] - 0.35:                            # 3a one hair lying on the table, at real size
        k = prog(t, S('3') - 0.15, A['hair'] - 0.35)
        m = cover(c, 'table', 0.70, 0.22, z=1.6 + 0.25 * k)
        c.save(); c.rectangle(PX, PY, PW, PH); c.clip(); c.set_operator(cairo.OPERATOR_SCREEN); c.set_source_rgba(0.45, 0.32, 0.20, 1); c.paint(); c.restore()
        grade(c, 0.40)
        c.save(); c.rectangle(PX, PY, PW, PH); c.clip(); hair_curve(c, 40, 640, 1040, 980, 3.2); c.restore()
        u = e_out(prog(t, S('3') + 0.5, S('3') + 0.9))
        if u > 0:
            c.set_source_rgba(1, 1, 1, 0.9 * u); c.set_line_width(4); c.new_path(); c.arc(560, 805, 70 * u + 1, 0, 2 * math.pi); c.stroke()
        a = 1 - prog(t, S('3') - 0.15, S('3') + 0.35)
        if a > 0: c.set_source_rgba(0.85, 0.85, 0.85, a); c.rectangle(60, 260, 960, 1080); c.fill()
        if t > S('3') + 0.4: pill(c, 'ONE HUMAN HAIR · ACTUAL SIZE', 540, 420, 24, CREAM, col=INK, s=e_back(prog(t, S('3') + 0.4, S('3') + 0.7)))
        loc = 'ON THE TABLE'; sec = 0
    elif t < A['xr']:                                      # 3b under the microscope: hair vs particle, true scale
        k0 = A['hair'] - 0.35; kk = e_io(prog(t, k0, k0 + 0.55))
        if kk < 1:
            layer(c, lambda cc: (cover(cc, 'table', 0.70, 0.22, z=1.85), hair_curve(cc, 40, 640, 1040, 980, 3.2)), a=1 - kk, s=1 + 6 * kk, cx=560, cy=820)
        layer(c, lambda cc: micro_field(cc, t, prog(t, k0, A['xr'])), a=kk, s=0.3 + 0.7 * kk, cx=540, cy=780)
        loc = 'MICROSCOPE'; sec = 0
    elif t < A['alv']:                                     # 3c breathed in: deep into the lungs, the tissue reacts
        k0 = A['xr']; kk = e_io(prog(t, k0, k0 + 0.5))
        layer(c, lambda cc: micro_field(cc, t, 1), a=1 - kk, s=1 + 0.6 * kk)
        layer(c, lambda cc: real_lungs(cc, t, prog(t, k0, A['alv']), prog(t, k0 + 0.3, k0 + 2.0), prog(t, k0 + 1.4, k0 + 2.2)), a=kk, s=0.85 + 0.15 * kk)
        if t > k0 + 0.6: pill(c, 'LUNGS', 540, 330, 24, CREAM, col=INK, s=e_back(prog(t, k0 + 0.6, k0 + 0.9)))
        if t > k0 + 1.5: pill(c, 'IRRITATION · INFLAMMATION', 540, 1290, 24, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, k0 + 1.5, k0 + 1.8)))
        loc = 'INSIDE THE BODY'; sec = 0
    elif t < A['hb']:                                      # 3d through the air sacs into the bloodstream
        k0 = A['alv']; kk = e_io(prog(t, k0, k0 + 0.6))
        layer(c, lambda cc: real_lungs(cc, t, 1, 1, 1), a=1 - kk, s=1 + 2.5 * kk, cx=700, cy=1000)
        layer(c, lambda cc: real_blood(cc, t, prog(t, k0, A['hb'])), a=kk, s=0.7 + 0.3 * kk)
        if t > A['blood'] - 0.1: pill(c, 'INTO THE BLOODSTREAM', 540, 1290, 26, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, A['blood'] - 0.1, A['blood'] + 0.2)))
        loc = 'BLOODSTREAM'; sec = 0
    elif t < S('4') - 0.1:                                 # 3e heart, then brain
        k0 = A['hb']; split = A['strokes'] - 0.35
        if t < split:
            kk = e_io(prog(t, k0, k0 + 0.5))
            layer(c, lambda cc: real_blood(cc, t, 1), a=1 - kk, s=1 + kk)
            layer(c, lambda cc: real_heart(cc, t, prog(t, A['heart'] - 0.2, A['heart'] + 0.2)), a=kk, s=0.8 + 0.2 * kk)
            if t > A['heart'] - 0.2: pill(c, 'HEART ATTACK', 540, 1290, 28, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, A['heart'] - 0.2, A['heart'] + 0.1)))
        else:
            kk = e_io(prog(t, split, split + 0.45))
            layer(c, lambda cc: real_heart(cc, t, 1), a=1 - kk, dx=-400 * kk)
            layer(c, lambda cc: real_brain(cc, t, prog(t, A['strokes'] - 0.2, A['strokes'] + 0.2)), a=kk, dx=400 * (1 - kk))
            if t > A['strokes'] - 0.2: pill(c, 'STROKE', 540, 1290, 28, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, A['strokes'] - 0.2, A['strokes'] + 0.1)))
        source_tag(c, 'US EPA · WHO', 300, 360)
        loc = 'INSIDE THE BODY'; sec = 0
    elif t < S('5') - 0.05:                                # 4 back home: the family, 8 years
        k = e_io(prog(t, S('4') - 0.1, S('4') + 0.7))
        layer(c, lambda cc: real_brain(cc, t, 1), a=1 - k, s=1 - 0.4 * k)
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95, people='two', shells=False), a=k, s=1.3 - 0.3 * k)
        if t >= A['eight4'] - 0.5:
            u = e_out(prog(t, A['eight4'] - 0.5, A['eight4'] + 0.4))
            glass_dark(c, 140, 360, 800, 230, 30, u)
            c.set_source_rgba(*CREAM, 0.35 * u); rrect(c, 180, 430, 720, 46, 23); c.fill()
            c.set_source_rgba(*PM25, u); rrect(c, 180 + 720 * 0.86, 430, 720 * 0.14 * prog(t, A['eight4'], A['eight4'] + 0.8) + 1, 46, 23); c.fill()
            head(c, '+8.2 YEARS', 540, 395, 46, AMBER, a=u, shadow=False)
            mono(c, 'POTENTIAL GAIN · AQLI 2025 · UNIV. OF CHICAGO', 540, 515, 18, CREAM, a=u, kind='monob'); mono(c, 'IF PM2.5 MET THE WHO GUIDELINE', 540, 548, 18, CREAM, a=u, kind='monob')
        loc = 'HOME · DELHI'; sec = 0
    elif t < S('M5') - 0.1:                                # 5 pull up to the city: 488
        k = e_io(prog(t, S('5') - 0.05, S('5') + 1.0))
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95, people='two', shells=False), a=1 - k, s=0.85 - 0.55 * k)
        layer(c, lambda cc: city_draw(cc, t, haze=1.0), a=k, s=2.2 - 1.2 * k)
        if t > A['b488'] - 0.9: bars2(c, t, A['b488'] - 0.9)
        if t > A['eight5'] - 0.2: pill(c, '≈ 8× THE LIMIT', 700, 470, 26, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, A['eight5'] - 0.2, A['eight5'] + 0.1)))
        t0c = A['three5'] - 0.3
        draw_clip(c, 'print', W / 2, 640, 820, t, t0c, rot=-1.0, hl_t0=t0c + 0.25, hl_dur=0.9, t1=t0c + 1.6)
        if t0c <= t <= t0c + 1.8: source_tag(c, 'THEPRINT / PTI · OCT 2025', 300, 790, a=prog(t, t0c + 0.2, t0c + 0.4) * (1 - prog(t, t0c + 1.6, t0c + 1.8)))
        loc = 'DELHI'; sec = 0
    elif t < S('7') - 0.05:                                # M5 + 6: three pins, the spike
        night = prog(t, S('6') - 0.1, S('6') + 0.5)
        city_draw(c, t, night=night, haze=1.0, lights=1 - 0.6 * night)
        if t >= S('6') - 0.1: fireworks(c, t, A['crackers6'] - 0.4)
        for i, (x, y) in enumerate(((300, 560), (540, 470), (780, 560))):
            pin(c, x, y, i + 1, ['SPIKE', 'TRAP', 'BUILD'][i], t, S('M5') + 0.3 + 0.15 * i, A['crackers6'] - 0.3 if i == 0 else None)
        loc = 'DELHI'; sec = 1
    elif t < A['biggest'] - 0.6:                           # 7-8 the sky cut-away
        k = e_io(prog(t, S('7') - 0.05, S('7') + 0.7))
        layer(c, lambda cc: city_draw(cc, t, night=1.0, haze=1.0, lights=0.4), a=1 - k)
        def sk(cc):
            src = sum(1 for key in ('veh8', 'dust', 'industry', 'garbage') if t >= A[key] - 0.15)
            sky_cut(cc, t, lid=prog(t, A['lid'] - 0.5, A['lid'] + 0.2), smoke=prog(t, S('7'), S('7') + 1.5), sources=src)
        c.save(); c.translate(0, 800); c.scale(1, 0.6 + 0.4 * k); c.translate(0, -800); layer(c, sk, a=k); c.restore()
        if t >= A['warm'] - 0.2: pill(c, 'TEMPERATURE INVERSION', W / 2, 300, 30, AMBER, s=e_back(prog(t, A['warm'] - 0.2, A['warm'] + 0.1)))
        if t >= S('8') - 0.2: pin(c, 960, 560, 3, 'BUILD', t, S('8') - 0.2, S('8'))
        elif t >= A['lid']: pin(c, 960, 560, 2, 'TRAP', t, A['lid'] - 0.2, A['lid'])
        loc = 'SKY ABOVE DELHI'; sec = 1
    elif t < S('9') - 0.05:                                # 8b vehicles donut, M8 Meera, pull up to the map
        k = e_io(prog(t, A['biggest'] - 0.6, A['biggest'] + 0.1))
        up = e_io(prog(t, S('M8') - 0.1, S('9') - 0.05))
        if up <= 0:
            layer(c, lambda cc: sky_cut(cc, t, lid=1, smoke=1, sources=4), a=1 - k)
            layer(c, lambda cc: city_draw(cc, t, haze=0.8, lights=1.0), a=k, s=1.4 - 0.4 * k)
        else:
            layer(c, lambda cc: city_draw(cc, t, haze=0.8, lights=1.0), a=1 - up, s=1 - 0.7 * up)
            layer(c, lambda cc: map_draw(cc, t, cam_lerp(CAM_DELHI, CAM_NORTH, up), haze=0.8, labels=('Delhi',)), a=up)
        if t >= A['biggest'] - 0.4 and up < 0.5:
            donut(c, t, A['biggest'] - 0.4)
            mono(c, 'MODELED LOCAL PM2.5 · NOV 10–20, 2023–25', W / 2, 1010, 18, CREAM, kind='monob'); mono(c, 'CSE ANALYSIS OF IITM DSS', W / 2, 1040, 16, CREAM, a=0.8, kind='mono')
        loc = 'DELHI'; sec = 1
    elif t < S('10') - 0.05:                               # 9 fly to Punjab, dive into Gurpreet's field
        k = prog(t, S('9') - 0.05, A['gurpreet'] + 0.3)
        if k < 1:
            cam = cam_lerp(CAM_NORTH, CAM_FIELD, e_io(k)); map_draw(c, t, cam, haze=0.6, fires=1.0, labels=('Punjab',) if cam[2] < 15 else ())
            if k > 0.7: c.set_source_rgba(0.85, 0.75, 0.55, (k - 0.7) / 0.3); c.rectangle(60, 260, 960, 1080); c.fill()
        else:
            kk = e_out(prog(t, A['gurpreet'] + 0.3, A['gurpreet'] + 0.9))
            layer(c, lambda cc: field_draw(cc, t, burn=prog(t, A['burning'] - 0.2, A['burning'] + 0.6)), s=1.15 - 0.15 * kk)
            gurpreet_c(c, 250, 1290, 0.66, t)
            pill(c, 'GURPREET · PADDY FARMER', 300, 1310, 22, CREAM, col=INK, a=kk)
            mono(c, 'ILLUSTRATIVE EXAMPLE', 300, 1350, 16, CREAM, a=0.85 * kk, kind='monob')
            if t >= A['two9'] - 0.4 and t < A['machines'] - 0.2:
                u = e_out(prog(t, A['two9'] - 0.4, A['two9'] - 0.1)); glass_dark(c, 120, 330, 840, 210, 28, u)
                mono(c, 'PADDY HARVEST → WHEAT SOWING', 540, 375, 22, CREAM, a=u, kind='monob')
                for d in range(14):
                    on = prog(t, A['two9'] - 0.2 + d * 0.06, A['two9'] + d * 0.06)
                    c.set_source_rgba(*(AMBER if on > 0.5 else CREAM), (0.95 if on > 0.5 else 0.25) * u); rrect(c, 170 + d * 53, 420, 44, 44, 8); c.fill()
                head(c, '≈ 2 WEEKS', 540, 505, 34, AMBER, a=u, shadow=False)
            if t >= A['machines'] - 0.2:
                for j, (lab, sub, tv) in enumerate((('MACHINE', 'COSTS MONEY', A['machines'] - 0.2), ('BURNING', 'FASTER · CHEAPER UPFRONT', A['burning'] - 0.2))):
                    if t < tv: continue
                    u = e_back(prog(t, tv, tv + 0.3)); x = 330 + j * 420
                    c.save(); c.translate(x, 430); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -190, -90, 380, 180, 26)
                    head(c, lab, 0, -30, 40, AMBER if j else CREAM, shadow=False); mono(c, sub, 0, 30, 18, CREAM, kind='monob'); c.restore()
        loc = 'PUNJAB · FIELD' if k >= 1 else 'PUNJAB'; sec = 2
    elif t < S('11') - 0.05:                               # 10 + M10: smoke to Delhi, the CREA share
        k = e_io(prog(t, S('10') - 0.05, S('10') + 1.0))
        if k < 1:
            layer(c, lambda cc: field_draw(cc, t, burn=1), a=1 - k, s=1 - 0.5 * k)
        cam = cam_lerp(CAM_FIELD, CAM_PH, k)
        layer(c, lambda cc: map_draw(cc, t, cam, haze=0.8, fires=1.0, labels=('Punjab', 'Haryana', 'Delhi') if k > 0.8 else ()), a=k)
        if k > 0.8:
            sx, sy = w2s(cam, 150, 160); ex, ey = w2s(cam, *DELHI); u = prog(t, S('10') + 0.8, S('10') + 1.8)
            c.set_source_rgba(*HAZE, 0.9); c.set_line_width(10); c.set_dash([18, 14]); c.move_to(sx, sy); c.line_to(lerp(sx, ex, u), lerp(sy, ey, u)); c.stroke(); c.set_dash([])
        if t >= A['p7'] - 0.6 and t < S('M10') - 0.1:
            bar_pair(c, t, A['p7'] - 0.6, (('AVERAGE', 7, A['p7'] - 0.3), ('PEAK DAY', 22, A['p22'] - 0.3)), 'MODELED CONTRIBUTION · FARM FIRES → DELHI PM2.5', 'NOV 2025 · CREA')
        loc = 'PUNJAB → DELHI'; sec = 2
    elif t < S('12') - 0.05:                               # 11 dive to the street: GRAP
        k = e_io(prog(t, S('11') - 0.05, S('11') + 0.8))
        layer(c, lambda cc: map_draw(cc, t, cam_lerp(CAM_PH, CAM_DELHI, k), haze=0.8, fires=1 - k), a=1 - prog(k, 0.6, 1))
        layer(c, lambda cc: street_draw(cc, t), a=prog(k, 0.6, 1), s=1.4 - 0.4 * prog(k, 0.6, 1))
        pill(c, 'GRAP · EMERGENCY PLAN · STRICTER IN STAGES', W / 2, 330, 22, CREAM, s=e_back(prog(t, S('11') + 0.5, S('11') + 0.8)))
        for key, lab, x, y in (('constr', 'CONSTRUCTION PAUSED', 300, 470), ('cars', 'SOME OLD CARS RESTRICTED', 580, 870), ('hybrid', 'PRIMARY CLASSES: HYBRID', 830, 690)):
            if t >= A[key] - 0.2: pill(c, lab, x, y, 20, AMBER, s=e_back(prog(t, A[key] - 0.2, A[key] + 0.1)))
        loc = 'STREET · DELHI'; sec = 3
    elif t < S('13') - 0.05:                               # 12 + M12 zoom out to India: NCAP
        k = prog(t, S('12') - 0.05, S('12') + 1.6)
        if k < 0.3:
            kk = e_io(k / 0.3)
            layer(c, lambda cc: street_draw(cc, t), a=1 - kk, s=1 - 0.6 * kk)
            layer(c, lambda cc: map_draw(cc, t, CAM_DELHI, haze=1.0), a=kk, s=1.5 - 0.5 * kk)
        else:
            map_draw(c, t, cam_lerp(CAM_DELHI, CAM_INDIA, e_io((k - 0.3) / 0.7)), haze=1.0, labels=('Delhi',) if k > 0.9 else ())
        if t >= A['pm10'] - 0.3:
            u = e_out(prog(t, A['pm10'] - 0.3, A['pm10']))
            glass_dark(c, 90, 330, 420, 330, 30, u)
            c.set_source_rgba(*PM10, 0.9 * u); c.set_line_width(6); c.new_path(); c.arc(300, 480, 110, 0, 2 * math.pi); c.stroke()
            c.set_source_rgba(*PM25, u); c.new_path(); c.arc(300, 520, 34, 0, 2 * math.pi); c.fill()
            mono(c, 'PM10 ≤ 10 µm', 300, 405, 18, PM10, a=u, kind='monob'); mono(c, 'PM2.5 ≤ 2.5 µm', 300, 575, 16, AMBER, a=u, kind='monob')
            mono(c, 'PM10 INCLUDES THE FINER PARTICLES', 300, 630, 14, CREAM, a=u, kind='monob')
        if t >= A['p40'] - 0.4:
            u = e_back(prog(t, A['p40'] - 0.4, A['p40'] - 0.1)); c.save(); c.translate(830, 1120); c.scale(max(0.01, u), max(0.01, u))
            glass_dark(c, -200, -130, 400, 260, 30); c.set_source_rgba(*PM10, 1); c.set_line_width(14); c.new_path(); c.arc(0, -20, 70, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.4); c.stroke()
            head(c, '−40%', 0, -20, 40, PM10, shadow=False); mono(c, 'NCAP · PM10 TARGET', 0, 78, 18, CREAM, kind='monob'); mono(c, 'BY 2025–26 vs 2017–18', 0, 104, 16, CREAM, kind='mono')
            c.restore()
        loc = 'INDIA'; sec = 3
    elif t < S('14') - 0.05:                               # 13 + M13: did it work? 97, then 23 of 100
        split = A['c23'] - 0.9
        if t < split:
            k = e_io(prog(t, S('13') - 0.05, S('13') + 1.2))
            map_draw(c, t, cam_lerp(CAM_INDIA, CAM_NORTH, k), haze=1.0, labels=('Delhi', 'Haryana', 'Uttar Pradesh') if k > 0.8 else ())
            t0 = A['cleanest'] - 0.5
            if t >= t0:
                u = e_out(prog(t, t0, t0 + 0.4)); x0, base = 660, 1240
                glass_dark(c, x0 - 40, 600, 400, 720, 30, u)
                pill(c, 'PM2.5', x0 + 160, 650, 22, PM25, a=u)
                h = 97 * 5.2 * prog(t, t0 + 0.1, t0 + 0.9)
                c.set_source_rgba(*PM25, u); rrect(c, x0 + 90, base - h, 140, h, 12); c.fill()
                if h > 50: head(c, '97', x0 + 160, base - h - 34, 48, AMBER, shadow=False)
                c.set_source_rgba(0.9, 0.3, 0.3, u); c.set_line_width(4); c.set_dash([12, 8]); c.move_to(x0, base - 40 * 5.2); c.line_to(x0 + 320, base - 40 * 5.2); c.stroke(); c.set_dash([])
                mono(c, 'ANNUAL LIMIT 40', x0 + 160, base - 40 * 5.2 + 22, 16, (1, 0.6, 0.6), a=u, kind='monob')
                mono(c, 'DELHI · 2025 · µg/m³', x0 + 160, base + 28, 16, CREAM, a=u, kind='monob')
                mono(c, 'CAQM · CLEANEST IN YEARS · EXCL. 2020', x0 + 160, base + 52, 14, CREAM, a=0.8 * u, kind='mono')
                if t >= A['annual'] - 0.2: pill(c, '≈ 2.5×', x0 + 160, 760, 30, AMBER, s=e_back(prog(t, A['annual'] - 0.2, A['annual'] + 0.1)))
            loc = 'NORTH INDIA'
        else:
            k = e_io(prog(t, split, split + 0.8))
            wash = 0.6 * prog(t, A['c23'] + 1.2, A['c23'] + 2.0)
            map_draw(c, t, cam_lerp(CAM_NORTH, CAM_INDIA, k), haze=0.6, wash=wash, labels=('Delhi',))
            glass_dark(c, 80, 900, 340, 400, 26, k)
            pill(c, 'PM10', 250, 935, 18, PM10, col=INK, a=k)
            dotgrid(c, t, split, A['c23'] - 0.1, cx=250, cy=1115)
            if t >= A['c23'] - 0.1: head(c, '23 / 100', 250, 1285, 40, PM10, shadow=False)
            if t >= A['didnt'] - 0.2: mono(c, 'DELHI: NOT IN THE 23', 250, 1325, 16, CREAM, kind='monob')
            t0c = max(A['c23'] + 0.4, E('13') - 2.7)
            draw_clip(c, 'crea', 620, 560, 860, t, t0c, rot=0.8, hl_t0=t0c + 0.25, hl_dur=0.7, t1=t0c + 1.25)
            draw_clip(c, 'crea2', 620, 560, 860, t, t0c + 1.25 if t >= t0c + 1.25 else 1e9, rot=0.8, hl_t0=t0c + 1.3, hl_dur=0.8, t1=t0c + 2.5)
            if t0c <= t <= t0c + 2.6: source_tag(c, 'CREA · JAN 2026', 300, 745, a=1.0)
            loc = 'INDIA'
        sec = 3
    elif t < S('15') - 0.05:                               # 14 fly east to Beijing
        k = e_io(prog(t, S('14') - 0.05, S('14') + 1.4))
        cam = (lerp(CAM_INDIA[0], 900, k), lerp(CAM_INDIA[1], 250, k), lerp(1.55, 1.2, k))
        if k < 1: map_draw(c, t, cam, haze=0.6, labels=())
        if 0.2 < k < 1:
            sx, sy = w2s(cam, *DELHI); c.set_source_rgba(*AMBER, 0.9); c.set_line_width(5); c.set_dash([14, 12]); c.move_to(sx, sy); c.line_to(sx + 900, sy - 300); c.stroke(); c.set_dash([])
        hz = 1 - 0.75 * prog(t, A['y2013'], A['v70'] + 0.4)
        global STK; STK = [A['coal'] - 0.15, A['gas'] - 0.15, A['vrules'] - 0.15, A['neigh'] - 0.15]
        stk = sum(1 for x in STK if t >= x)
        layer(c, lambda cc: beijing_card(cc, t, haze=hz, stickers=stk, tl=prog(t, A['coal'] - 0.3, A['decade'] + 0.3)), a=prog(t, S('14') + 0.6, S('14') + 1.0), dx=1100 * (1 - e_out(prog(t, S('14') + 0.5, S('14') + 1.4))))
        if t >= A['y2013'] - 0.2:
            v = lerp(89.5, 27, e_io(prog(t, A['y2013'] + 0.3, A['v70'] - 0.1)))
            yr = '2013' if v > 89 else ('2025' if v < 27.05 else '…')
            glass_dark(c, 330, 1210, 420, 120, 30)
            pill(c, 'PM2.5', 400, 1270, 18, PM25)
            head(c, '27' if v < 27.05 else f'{v:.1f}', 560, 1262, 56, AMBER, shadow=False); mono(c, yr, 690, 1270, 22, CREAM, kind='monob')
            if t >= A['v70'] - 0.2: pill(c, '−70%', 880, 1270, 34, AMBER, s=e_back(prog(t, A['v70'] - 0.2, A['v70'] + 0.1)))
            if t >= A['v70'] + 0.4: mono(c, "STILL ABOVE WHO'S 5 µg/m³", 540, 1345, 15, CREAM, a=0.9, kind='monob')
            else: mono(c, 'BEIJING ECOLOGY BUREAU via CHINA DAILY', 540, 1345, 15, CREAM, a=0.8, kind='mono')
        loc = 'BEIJING'; sec = 4
    elif t < S('16') - 0.05:                               # 15 fly back west: the fix
        k = e_io(prog(t, S('15') - 0.05, S('15') + 1.2))
        layer(c, lambda cc: beijing_card(cc, t, haze=0.25, stickers=4, tl=1.0), a=1 - k, dx=1100 * k)
        clear = prog(t, A['region'] - 0.2, A['region'] + 2.0)
        cam = cam_lerp((900, 250, 1.2), CAM_NI, k)
        layer(c, lambda cc: map_draw(cc, t, cam, haze=1.0, clear=clear, ring=clear, labels=('Punjab', 'Haryana', 'Uttar Pradesh', 'Delhi') if k > 0.9 else ()), a=k, dx=-1100 * (1 - k))
        for i, (key, lab, sub) in enumerate((('spike15', 'SPIKE', 'FIRECRACKERS'), ('winter15', 'TRAP', 'WINTER CONDITIONS'), ('every15', 'BUILD', 'ONGOING EMISSIONS'))):
            if t < A[key] - 0.2: continue
            u = e_back(prog(t, A[key] - 0.2, A[key] + 0.1)); x = 200 + i * 340
            c.save(); c.translate(x, 1230); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -150, -60, 300, 120, 24)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -150, -60, 300, 120, 24); c.stroke()
            head(c, lab, 0, -14, 40, AMBER, shadow=False); mono(c, sub, 0, 34, 16, CREAM, kind='monob'); c.restore()
        if t >= A['region'] - 0.2: pill(c, 'YEAR-ROUND + REGION-WIDE', W / 2, 360, 32, AMBER, s=e_back(prog(t, A['region'] - 0.2, A['region'] + 0.1)))
        if t >= A['region']:
            u = e_out(prog(t, A['region'], A['region'] + 0.4)); avatar(c, 'meera', 940, 520, 70, t, 0.0, a=u)
        loc = 'NORTH INDIA'; sec = 5
    elif t < S('L') - 0.05:                                # 16 the week's series slide
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('16') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        k1 = e_io(prog(t, S('L') - 0.05, S('L') + 0.5)); k2 = e_io(prog(t, S('L') + 0.5, S('L') + 1.3))
        c.push_group(); slide(c, t, S('16') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - k1)
        layer(c, lambda cc: city_draw(cc, t, haze=1.0), a=k1 * (1 - k2), s=1 + 2.5 * k2, cx=470, cy=760)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k2)
    mk = m_active(t)
    if mk and mk not in ('M1', 'M2') and t < S('16') - 0.05:
        meera_corner(c, t, mk); caps = False
    for k in ('M5', 'M8', 'M10', 'M12', 'M13'):
        if E(k) < t < E(k) + 0.5: meera_corner(c, t, k)
    if sec is not None and t < S('16') - 0.05: strip(c, sec)
    if loc and t < S('16') - 0.05: locator(c, loc)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('16') - 0.05: tag(c)
    return s
