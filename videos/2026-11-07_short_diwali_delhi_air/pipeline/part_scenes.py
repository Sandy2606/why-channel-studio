
# ---------------- anchors ----------------
A = {
    'part': AT('1', 'part', 'భాగం'),
    'b488': AT('2', '488', '488'), 'three2': AT('2', 'Three', 'మూడు'), 'eight': AT('2', 'eight', 'ఎనిమిది'),
    'crackers4': AT('4', 'Crackers', 'బాణాసంచా'),
    'inversion': AT('5', 'inversion', 'inversion'), 'lid': AT('5', 'lid', 'మూతలా'), 'wind': AT('5', 'wind', 'వేగం'),
    'veh6': AT('6', 'vehicles', 'వాహనాలు'), 'dust': AT('6', 'dust', 'దుమ్ము'), 'industry': AT('6', 'industry', 'పరిశ్రమలు'),
    'garbage': AT('6', 'garbage', 'చెత్త'), 'farm': AT('6', 'Farm', 'పంట'),
    'half': AT('7', 'half', 'సగం'),
    'eight9': AT('9', '8', '8'),
    'constr': AT('10', 'construction', 'నిర్మాణాలు'), 'cars': AT('10', 'cars', 'కార్లపై'), 'hybrid': AT('10', 'hybrid', 'hybrid'),
    'stages': AT('11', 'stages', 'దశల'),
    'p40': AT('12', '40', '40'),
    'p100': AT('13', '100', '100'), 'annual': AT('13', 'annual', None) if LANGV == 'en' else AT('13', None, 'సంవత్సర', n=2),
    'c23': AT('14', '23', '23'), 'delhi14': AT('14', 'Delhi', 'Delhi'),
    'y2013': AT('15', '2013', '2013'), 'v27': AT('15', '27', '27'), 'v70': AT('15', '70', '70'),
    'coal': AT('16', 'coal', 'బొగ్గు'), 'gas': AT('16', 'gas', 'gas'), 'vrules': AT('16', 'vehicle', 'వాహనాల'),
    'neigh': AT('16', 'neighbouring', 'పక్క'), 'decade': AT('16', 'decade', 'పదేళ్లకు'),
    'spike17': AT('17', 'spike', 'బాణాసంచా'), 'winter17': AT('17', 'Winter', 'చలికాలం'), 'every17': AT('17', 'Everyday', 'రోజువారీ'),
    'region': AT('17', 'year-round', 'పొడవునా', off=-0.4),
    'tomorrow': S('18'), 'loop': S('L'),
}
A['end'] = DUR
"""HELPERS"""
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
    """zoom on a log scale so big zoom changes feel smooth"""
    z = math.exp(lerp(math.log(c0[2]), math.log(c1[2]), k)); f = (1 / z - 1 / c0[2]) / (1 / c1[2] - 1 / c0[2]) if c1[2] != c0[2] else k
    return (lerp(c0[0], c1[0], f), lerp(c0[1], c1[1], f), z)
def w2s(cam, x, y): return (MAPC[0] + (x - cam[0]) * cam[2], MAPC[1] + (y - cam[1]) * cam[2])
def state_path(c, n):
    for p in MAPP[n]:
        c.move_to(*p[0])
        for q in p[1:]: c.line_to(*q)
        c.close_path()
def map_draw(c, t, cam, haze=1.0, wash=0.0, fires=0.0, labels=(), clear=0.0, ring=0.0, dots=None):
    c.set_source_rgb(*SEA); c.paint()
    font(c, 'mono', 14)
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
            c.arc(x, y, rr * 1.6, 0, 2 * math.pi); c.fill()
    if fires > 0:
        for i, (x, y) in enumerate(FIRES):
            bl = 0.5 + 0.5 * math.sin(t * 7 + i * 1.9)
            c.set_source_rgba(1.0, 0.45 + 0.3 * bl, 0.1, fires * (0.55 + 0.45 * bl)); c.arc(x, y, 1.6 + 0.6 * bl, 0, 2 * math.pi); c.fill()
    if ring > 0:
        c.set_source_rgba(*AMBER, 0.9 * (1 - 0.6 * ring)); c.set_line_width(3 / cam[2]); c.arc(DELHI[0], DELHI[1], 10 + 150 * ring, 0, 2 * math.pi); c.stroke()
    c.set_source_rgb(0.85, 0.15, 0.15); c.arc(DELHI[0], DELHI[1], 3.2 / max(1, cam[2] / 3), 0, 2 * math.pi); c.fill()
    c.restore()
    for n in labels:
        x, y = w2s(cam, *(DELHI if n == 'Delhi' else CENT[n])); lab = n.upper() if n != 'Uttar Pradesh' else 'UTTAR PRADESH'
        if n == 'Delhi': x += 46
        mono(c, lab, x, y + (-22 if n == 'Delhi' else 0), 20, INK, a=0.85, kind='monob')
def flats(c, x0, x1, ybase, rng, col, hmin=80, hmax=260):
    x = x0
    while x < x1:
        w = rng.uniform(50, 110); h = rng.uniform(hmin, hmax)
        c.set_source_rgb(*col); c.rectangle(x, ybase - h, w - 6, h); c.fill()
        x += w
def skyline_window(c, t, x0, y0, w, h, haze=1.0):
    """the view out of Raju's window: Delhi rooftops, India Gate, haze"""
    c.save(); c.rectangle(x0, y0, w, h); c.clip()
    g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgb(0, 0.78, 0.74, 0.66); g.add_color_stop_rgb(1, 0.62, 0.58, 0.52); c.set_source(g); c.paint()
    c.set_source_rgba(1, 0.92, 0.75, 0.55); c.arc(x0 + w * 0.7, y0 + h * 0.28, 40, 0, 2 * math.pi); c.fill()
    rng = np.random.default_rng(3); flats(c, x0 - 20, x0 + w + 20, y0 + h * 0.80, rng, (0.50, 0.47, 0.44), 60, 180)
    gx, gy = x0 + w * 0.40, y0 + h * 0.80                                     # India Gate silhouette
    c.set_source_rgb(0.45, 0.42, 0.40); c.rectangle(gx - 60, gy - 200, 120, 200); c.fill()
    c.set_source_rgb(0.62, 0.58, 0.52); c.move_to(gx - 30, gy); c.line_to(gx - 30, gy - 110); c.curve_to(gx - 30, gy - 150, gx + 30, gy - 150, gx + 30, gy - 110); c.line_to(gx + 30, gy); c.close_path(); c.fill()
    c.set_source_rgb(0.45, 0.42, 0.40); c.rectangle(gx - 70, gy - 215, 140, 20); c.fill()
    rng2 = np.random.default_rng(9); flats(c, x0 - 20, x0 + w + 20, y0 + h, rng2, (0.36, 0.33, 0.31), 80, 220)
    for k in range(3):
        c.set_source_rgba(*HAZE, (0.28 + 0.12 * k) * haze); c.rectangle(x0, y0 + h * (0.2 + 0.2 * k), w, h); c.fill()
    c.restore()
def home_draw(c, t, curtain=0.7, haze=1.0, people='raju', shells=True):
    c.set_source_rgb(0.30, 0.24, 0.21); c.rectangle(60, 260, 960, 1080); c.fill()
    wx, wy, ww, wh = 200, 330, 680, 700
    skyline_window(c, t, wx, wy, ww, wh, haze)
    c.set_source_rgb(0.85, 0.82, 0.76); c.set_line_width(18); c.rectangle(wx, wy, ww, wh); c.stroke()
    c.set_line_width(10); c.move_to(wx + ww / 2, wy); c.line_to(wx + ww / 2, wy + wh); c.stroke()
    c.set_source_rgb(0.40, 0.42, 0.45); c.rectangle(wx, wy + wh - 110, ww, 10); c.fill()   # balcony rail
    for i in range(6): c.rectangle(wx + 20 + i * 120, wy + wh - 110, 8, 110); c.fill()
    if shells:
        for i, x in enumerate((wx + 140, wx + 190, wx + 520)):
            c.save(); c.translate(x, wy + wh - 116); c.rotate(0.3 * (i - 1)); c.set_source_rgb(0.75, 0.18, 0.15); c.rectangle(-9, -34, 18, 34); c.fill()
            c.set_source_rgb(0.15, 0.12, 0.10); c.rectangle(-9, -38, 18, 6); c.fill(); c.restore()
    cw = ww / 2 * (1 - curtain)                                                  # curtains
    for side in (0, 1):
        x = wx - 30 if side == 0 else wx + ww + 30 - (cw + 60)
        c.set_source_rgb(0.62, 0.20, 0.22); c.rectangle(x, wy - 40, cw + 60, wh + 80); c.fill()
        c.set_source_rgba(0, 0, 0, 0.18)
        for k in range(4): c.rectangle(x + 10 + k * (cw + 60) / 4, wy - 40, 6, wh + 80); c.fill()
    c.set_source_rgb(0.40, 0.30, 0.24); c.rectangle(60, 1180, 960, 160); c.fill()                # floor
    if people == 'raju':
        person(c, 200, 1250, 1.0, (0.30, 0.45, 0.70), t=t)
    elif people == 'family':
        person(c, 230, 1250, 1.0, (0.30, 0.45, 0.70), t=t)
        person(c, 540, 1250, 0.62, (0.90, 0.55, 0.20), t=t + 1)
        person(c, 840, 1250, 0.92, (0.55, 0.40, 0.60), t=t + 2)
        c.set_source_rgb(0.85, 0.85, 0.85); c.arc(840, 1250 - 0.92 * 362, 0.92 * 58, math.pi * 1.02, math.pi * 1.98); c.fill()   # grey hair
    c.set_source_rgba(*HAZE, 0.10 * haze); c.rectangle(60, 260, 960, 1080); c.fill()
def city_draw(c, t, night=0.0, haze=1.0, lights=1.0):
    c.set_source_rgb(0.40, 0.38, 0.36); c.rectangle(60, 260, 960, 1080); c.fill()
    rng = np.random.default_rng(11)
    for i in range(16):
        for j in range(19):
            x = 70 + i * 60 + rng.uniform(-4, 4); y = 270 + j * 56 + rng.uniform(-4, 4)
            v = rng.uniform(0.45, 0.70); c.set_source_rgb(v, v * 0.95, v * 0.88); c.rectangle(x, y, 48, 44); c.fill()
    c.set_source_rgb(0.42, 0.58, 0.66); c.set_line_width(46)                      # Yamuna
    c.move_to(860, 260); c.curve_to(760, 560, 960, 820, 820, 1340); c.stroke()
    c.set_source_rgb(0.25, 0.25, 0.27); c.set_line_width(22); c.save(); c.translate(540, 800); c.scale(1, 0.8); c.arc(0, 0, 330, 0, 2 * math.pi); c.restore(); c.stroke()
    c.set_source_rgb(0.30, 0.42, 0.28); c.arc(470, 760, 55, 0, 2 * math.pi); c.fill()                  # India Gate lawns
    c.set_source_rgb(0.85, 0.80, 0.70); c.rectangle(455, 745, 30, 30); c.fill()
    mono(c, 'INDIA GATE', 470, 840, 18, CREAM, a=0.9, kind='monob'); mono(c, 'YAMUNA', 850, 600, 18, CREAM, a=0.8, kind='monob')
    if night > 0: c.set_source_rgba(0.03, 0.04, 0.10, 0.72 * night); c.rectangle(60, 260, 960, 1080); c.fill()
    if lights > 0:
        for k in range(46):
            an = (t * 0.25 + k / 46) * 2 * math.pi; x = 540 + 330 * math.cos(an); y = 800 + 264 * math.sin(an)
            c.set_source_rgba(1, 0.92 if k % 2 else 0.35, 0.6 if k % 2 else 0.25, 0.9 * lights); c.arc(x, y, 5, 0, 2 * math.pi); c.fill()
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
                c.set_source_rgba(*col, a * (1 - k * 0.7)); c.arc(x + r * math.cos(an), y + r * math.sin(an), 6, 0, 2 * math.pi); c.fill()
        sk = prog(t, st + 0.3, st + 3)
        if sk > 0:
            g = cairo.RadialGradient(x, y, 0, x, y, 40 + 90 * sk); g.add_color_stop_rgba(0, *HAZE, 0.5 * a * sk); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.arc(x, y, 40 + 90 * sk, 0, 2 * math.pi); c.fill()
def sky_cut(c, t, lid=0.0, smoke=0.0, sources=0, wind=0.0):
    c.save(); c.rectangle(60, 330, 960, 850); c.clip(); _sky_cut(c, t, lid, smoke, sources, wind); c.restore()
def _sky_cut(c, t, lid=0.0, smoke=0.0, sources=0, wind=0.0):
    g = cairo.LinearGradient(0, 330, 0, 700); g.add_color_stop_rgb(0, 0.85, 0.52, 0.28); g.add_color_stop_rgb(1, 0.70, 0.45, 0.30); c.set_source(g); c.rectangle(60, 330, 960, 370); c.fill()
    g = cairo.LinearGradient(0, 700, 0, 1110); g.add_color_stop_rgb(0, 0.30, 0.45, 0.62); g.add_color_stop_rgb(1, 0.20, 0.32, 0.48); c.set_source(g); c.rectangle(60, 700, 960, 410); c.fill()
    mono(c, 'WARM AIR', 180, 380, 22, INK, anchor='l', kind='monob'); mono(c, 'COOL AIR', 180, 760, 22, CREAM, anchor='l', kind='monob')
    rng = np.random.default_rng(5); flats(c, 60, 1020, 1110, rng, (0.18, 0.16, 0.15), 60, 200)
    c.set_source_rgb(0.14, 0.12, 0.11); c.rectangle(60, 1110, 960, 70); c.fill()
    srcs = [(170, 'car'), (360, 'dust'), (560, 'factory'), (760, 'bin')]
    for i, (x, kind) in enumerate(srcs[:sources]):
        glass_dark(c, x - 60, 1120, 120, 52, 16); mono(c, ['VEHICLES', 'DUST', 'INDUSTRY', 'GARBAGE'][i], x, 1146, 16, CREAM, kind='monob')
    if smoke > 0:
        top = 720 if lid > 0.5 else 400
        for i in range(26):
            ph = (t * 0.25 + ((i * 0.618) % 1.0)) % 1.0; x0 = 120 + (i * 37) % 860
            y = 1100 - (1100 - top) * min(1, ph * 1.6); spread = max(0, ph * 1.6 - 1) * (160 if lid > 0.5 else 30)
            x = x0 + spread * (1 if i % 2 else -1); r = 26 + 40 * ph
            g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *HAZE, 0.55 * smoke); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    if lid > 0:
        x = lerp(-900, 60, e_out(lid))
        c.set_source_rgba(0.85, 0.95, 1.0, 0.35); rrect(c, x, 690, 960, 22, 10); c.fill()
        c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(3); rrect(c, x, 690, 960, 22, 10); c.stroke()
    if wind > 0:
        c.save(); c.translate(900, 470)
        c.set_source_rgba(*CREAM, wind); c.set_line_width(6); c.move_to(0, 0); c.line_to(0, 160); c.stroke()
        c.set_source_rgba(0.95, 0.45, 0.2, wind); c.move_to(0, 0); c.line_to(16, 90); c.line_to(-6, 90); c.close_path(); c.fill()
        c.restore()
def street_draw(c, t):
    c.set_source_rgb(0.66, 0.64, 0.60); c.rectangle(60, 260, 960, 1080); c.fill()
    rng = np.random.default_rng(14); flats(c, 60, 1020, 1000, rng, (0.52, 0.50, 0.48), 120, 420)
    c.set_source_rgb(0.28, 0.28, 0.30); c.rectangle(60, 1000, 960, 180); c.fill()
    c.set_source_rgb(0.9, 0.9, 0.85)
    for x in range(80, 1020, 120): c.rectangle(x, 1085, 60, 8); c.fill()
    c.set_source_rgb(0.95, 0.70, 0.15); c.set_line_width(12); c.move_to(220, 1000); c.line_to(220, 520); c.line_to(430, 520); c.stroke()   # crane
    c.move_to(410, 520); c.line_to(410, 640); c.set_line_width(4); c.stroke()
    c.set_source_rgb(0.55, 0.20, 0.18); rrect(c, 480, 960, 200, 70, 18); c.fill(); rrect(c, 520, 920, 120, 50, 14); c.fill()   # old car
    c.set_source_rgb(0.1, 0.1, 0.1); c.arc(520, 1035, 22, 0, 2 * math.pi); c.fill(); c.arc(640, 1035, 22, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.75, 0.60, 0.40); c.rectangle(790, 760, 200, 240); c.fill(); c.set_source_rgb(0.35, 0.25, 0.20); c.rectangle(860, 880, 60, 120); c.fill()   # school
    mono(c, 'SCHOOL', 890, 800, 18, INK, kind='monob')
    for k in range(3): c.set_source_rgba(*HAZE, 0.14); c.rectangle(60, 260, 960, 1080); c.fill()
HEBEI = [(-330, -60), (-260, -230), (-60, -300), (120, -260), (260, -150), (330, 40), (240, 230), (40, 300), (-180, 260), (-310, 120)]
def beijing_card(c, t, haze=1.0, stickers=0, tl=0.0):
    c.save(); c.translate(540, 760)
    c.set_source_rgba(0.94, 0.90, 0.80, 1); rrect(c, -460, -420, 920, 840, 28); c.fill()
    c.set_source_rgb(0.80, 0.74, 0.60); c.move_to(*HEBEI[0]); [c.line_to(*p) for p in HEBEI[1:]]; c.close_path(); c.fill()
    c.set_source_rgb(0.70, 0.62, 0.48); c.move_to(-120, -170); c.curve_to(-20, -230, 90, -180, 70, -80); c.curve_to(50, 0, -100, 10, -140, -60); c.close_path(); c.fill()
    c.set_source_rgb(0.72, 0.64, 0.50); c.arc(170, 10, 52, 0, 2 * math.pi); c.fill()
    mono(c, 'BEIJING', -30, -110, 26, INK, kind='monob'); mono(c, 'TIANJIN', 170, 10, 18, INK, kind='monob'); mono(c, 'HEBEI', -150, 170, 24, INK, kind='monob')
    c.set_source_rgba(0.85, 0.15, 0.15, 1); c.arc(-30, -150, 7, 0, 2 * math.pi); c.fill()
    if haze > 0:
        for k in range(3):
            g = cairo.RadialGradient(-20, -60, 0, -20, -60, 330); g.add_color_stop_rgba(0, *HAZE, 0.42 * haze); g.add_color_stop_rgba(1, *HAZE, 0); c.set_source(g); c.arc(-20, -60, 330, 0, 2 * math.pi); c.fill()
    icons = [(-300, -340, 'COAL PLANTS SHUT'), (300, -340, 'HOMES: GAS + POWER'), (-300, 340, 'VEHICLE RULES'), (300, 340, 'REGIONAL TEAMWORK')]
    for i, (x, y, lab) in enumerate(icons[:stickers]):
        u = e_back(prog(t, STK[i], STK[i] + 0.3)) if i < len(STK) else 1
        c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -150, -38, 300, 76, 20)
        mono(c, lab, 0, 0, 18, CREAM, kind='monob'); c.restore()
        if i == 3 and u > 0.5:
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(5); c.move_to(-30, -150); c.line_to(170, 10); c.stroke(); c.move_to(-30, -150); c.line_to(-150, 170); c.stroke()
    if tl > 0:
        c.set_source_rgba(*INK, 0.7); c.set_line_width(4); c.move_to(-380, 395); c.line_to(-380 + 760 * tl, 395); c.stroke()
        mono(c, '2013', -380, 375, 18, INK, kind='monob');
        if tl > 0.95: mono(c, '2025', 380, 375, 18, INK, kind='monob')
    c.restore()
STK = []
SECT = ['PROBLEM', 'WHY', 'EFFECTS', 'ACTION', 'BEIJING', 'FIX']
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
    c.save(); c.push_group(); c.translate(cx + dx, cy); c.scale(s, s); c.translate(-cx, -cy); fn(c); c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def bars2(c, t, t0, k=1.0):
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
    c.set_source_rgba(*(AMBER if filled else CREAM), 1); c.arc(0, 0, 34, 0, 2 * math.pi); c.fill(); c.move_to(-16, 26); c.line_to(0, 64); c.line_to(16, 26); c.close_path(); c.fill()
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
    if not frozen and t > A['part']:
        k = e_io(prog(t, A['part'], S('2') + 0.2))
        layer(c, lambda cc: home_draw(cc, tt, curtain=cur), s=1 - 0.15 * k)
    else: home_draw(c, tt, curtain=cur)
    mono(c, 'DIWALI · DELHI', W / 2, 1210, 28, CREAM, kind='monob')
    head(c, 'WHY DELHI CHOKES', W / 2, 1300, 84, AMBER)

CAM_INDIA = (306, 348, 1.55); CAM_NORTH = (205, 205, 4.2); CAM_PH = (163, 178, 6.0); CAM_DELHI = (DELHI[0], DELHI[1], 40.0); CAM_NI = (230, 225, 3.0)
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True; loc = None; sec = None
    if t < S('2') - 0.05:
        sc_hook(c, t); loc = 'HOME · DELHI'
    elif t < S('3') - 0.05:   # 2 pull up to the city, the numbers
        k = e_io(prog(t, S('2') - 0.05, S('2') + 1.0))
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95), a=1 - k, s=0.85 - 0.55 * k)
        layer(c, lambda cc: city_draw(cc, t, haze=1.0), a=k, s=2.2 - 1.2 * k)
        if t > A['b488'] - 0.9: bars2(c, t, A['b488'] - 0.9)
        if t > A['eight'] - 0.2: pill(c, '≈ 8× THE LIMIT', 700, 470, 26, (0.9, 0.3, 0.3), col=CREAM, s=e_back(prog(t, A['eight'] - 0.2, A['eight'] + 0.1)))
        t0c = A['three2'] - 0.3
        draw_clip(c, 'print', W / 2, 640, 820, t, t0c, rot=-1.0, hl_t0=t0c + 0.25, hl_dur=0.9, t1=t0c + 1.6)
        if t0c <= t <= t0c + 1.8: source_tag(c, 'THEPRINT / PTI · OCT 2025', 300, 790, a=prog(t, t0c + 0.2, t0c + 0.4) * (1 - prog(t, t0c + 1.6, t0c + 1.8)))
        loc = 'DELHI'; sec = 0
    elif t < S('5') - 0.05:   # 3-4 three reasons; the spike
        night = prog(t, S('4') - 0.1, S('4') + 0.5)
        city_draw(c, t, night=night, haze=1.0, lights=1 - 0.6 * night)
        if t >= S('4') - 0.1: fireworks(c, t, A['crackers4'] - 0.4)
        for i, (x, y) in enumerate(((300, 560), (540, 470), (780, 560))):
            pin(c, x, y, i + 1, ['SPIKE', 'TRAP', 'BUILD'][i], t, S('3') + 0.15 * i, A['crackers4'] - 0.3 if i == 0 else None)
        loc = 'DELHI'; sec = 1
    elif t < A['farm'] - 0.35:   # 5-6 the sky cut-away
        k = e_io(prog(t, S('5') - 0.05, S('5') + 0.7))
        layer(c, lambda cc: city_draw(cc, t, night=1.0, haze=1.0, lights=0.4), a=1 - k)
        def sk(cc):
            src = sum(1 for key in ('veh6', 'dust', 'industry', 'garbage') if t >= A[key] - 0.15)
            sky_cut(cc, t, lid=prog(t, A['lid'] - 0.5, A['lid'] + 0.2), smoke=prog(t, S('5'), S('5') + 1.5), sources=src, wind=prog(t, A['wind'] - 0.2, A['wind'] + 0.2))
        c.save(); c.translate(0, 800); c.scale(1, 0.6 + 0.4 * k); c.translate(0, -800); layer(c, sk, a=k); c.restore()
        if t >= A['inversion'] - 0.2: pill(c, 'TEMPERATURE INVERSION', W / 2, 300, 30, AMBER, s=e_back(prog(t, A['inversion'] - 0.2, A['inversion'] + 0.1)))
        if t >= A['wind'] - 0.2 and t < S('6'): pill(c, 'WIND < 1 m/s · DIWALI 2025', 760, 1260, 22, CREAM, s=e_back(prog(t, A['wind'] - 0.2, A['wind'] + 0.1)))
        if t >= S('6') - 0.2: pin(c, 960, 560, 3, 'BUILD', t, S('6') - 0.2, S('6'))
        elif t >= A['lid']: pin(c, 960, 560, 2, 'TRAP', t, A['lid'] - 0.2, A['lid'])
        loc = 'SKY ABOVE DELHI'; sec = 1
    elif t < S('7') - 0.05:   # 6b farm fires, a brief side trip
        k = e_io(prog(t, A['farm'] - 0.35, A['farm'] + 0.4))
        cam = CAM_PH
        layer(c, lambda cc: map_draw(cc, t, cam, haze=0.8, fires=prog(t, A['farm'], A['farm'] + 0.4), labels=('Punjab', 'Haryana', 'Delhi')), a=k, s=1.6 - 0.6 * k)
        if k > 0.6:
            sx, sy = w2s(cam, 150, 160); ex, ey = w2s(cam, *DELHI); u = prog(t, A['farm'] + 0.3, A['farm'] + 1.3)
            c.set_source_rgba(*HAZE, 0.9); c.set_line_width(10); c.set_dash([18, 14]); c.move_to(sx, sy); c.line_to(lerp(sx, ex, u), lerp(sy, ey, u)); c.stroke(); c.set_dash([])
            pill(c, 'FARM FIRES · SOME DAYS', W / 2, 1260, 26, CREAM, s=e_back(prog(t, A['farm'], A['farm'] + 0.3)))
        loc = 'PUNJAB · HARYANA'; sec = 1
    elif t < S('8') - 0.05:   # 7 back to Delhi, vehicles
        k = prog(t, S('7') - 0.05, S('7') + 1.1)
        if k < 0.6:
            cam = cam_lerp(CAM_PH, (DELHI[0], DELHI[1], 14.0), e_io(k / 0.6)); map_draw(c, t, cam, haze=0.8, labels=('Delhi',))
        else:
            kk = e_io((k - 0.6) / 0.4)
            layer(c, lambda cc: map_draw(cc, t, (DELHI[0], DELHI[1], 14.0), haze=0.8), a=1 - kk, s=1 + 1.5 * kk)
            layer(c, lambda cc: city_draw(cc, t, haze=0.8, lights=1.0), a=kk, s=0.6 + 0.4 * kk)
        if t >= A['half'] - 0.8:
            donut(c, t, A['half'] - 0.8)
            mono(c, 'MODELED LOCAL PM2.5 ONLY · NOV 10–20, 2023–25', W / 2, 1010, 18, CREAM, kind='monob'); mono(c, 'CSE ANALYSIS OF IITM DSS', W / 2, 1040, 16, CREAM, a=0.8, kind='mono')
        loc = 'DELHI'; sec = 1
    elif t < S('9') - 0.05:   # 8 channel note
        city_draw(c, t, haze=0.8)
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        u = e_back(prog(t, S('8'), S('8') + 0.35)); c.save(); c.translate(W / 2, 760); c.scale(max(0.01, u), max(0.01, u))
        c.set_source_rgba(0.95, 0.92, 0.85, 1); rrect(c, -330, -200, 660, 400, 26); c.fill(); c.set_source_rgba(0.80, 0.15, 0.10, 1); rrect(c, -330, -200, 660, 90, 26); c.fill(); c.rectangle(-330, -140, 660, 30); c.fill()
        mono(c, 'EVERY WEEK', 0, -155, 30, CREAM, kind='monob')
        head(c, 'SUN', -170, -30, 60, INK, shadow=False); mono(c, 'FULL VIDEO', -170, 40, 24, INK, kind='monob')
        head(c, 'MON–SAT', 150, -30, 60, INK, shadow=False); mono(c, 'SHORTS', 150, 40, 24, INK, kind='monob')
        c.restore(); loc = 'DELHI'; sec = 1
    elif t < S('10') - 0.05:   # 9 back home: effects
        k = e_io(prog(t, S('9') - 0.05, S('9') + 0.9))
        layer(c, lambda cc: city_draw(cc, t, haze=0.8), a=1 - k, s=1 + 2 * k, cx=600, cy=760)
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95, people='family', shells=False), a=k, s=0.6 + 0.4 * k)
        if t >= A['eight9'] - 0.5:
            u = e_out(prog(t, A['eight9'] - 0.5, A['eight9'] + 0.4))
            glass_dark(c, 140, 360, 800, 230, 30, u)
            c.set_source_rgba(*CREAM, 0.35 * u); rrect(c, 180, 430, 720, 46, 23); c.fill()
            c.set_source_rgba(*PM25, u); rrect(c, 180 + 720 * 0.86, 430, 720 * 0.14 * prog(t, A['eight9'], A['eight9'] + 0.8) + 1, 46, 23); c.fill()
            head(c, '+8.2 YEARS', 540, 395, 46, AMBER, a=u, shadow=False)
            mono(c, 'POTENTIAL GAIN · AQLI 2025 · 2023 DATA', 540, 515, 18, CREAM, a=u, kind='monob'); mono(c, 'IF PM2.5 MET THE WHO GUIDELINE', 540, 548, 18, CREAM, a=u, kind='monob')
        loc = 'HOME · DELHI'; sec = 2
    elif t < S('11') - 0.05:   # 10 the street on the worst days
        k = e_io(prog(t, S('10') - 0.05, S('10') + 0.7))
        layer(c, lambda cc: home_draw(cc, t, curtain=0.95, people='family', shells=False), a=1 - k, dx=-900 * k)
        layer(c, lambda cc: street_draw(cc, t), a=k, dx=900 * (1 - k))
        for key, lab, x, y in (('constr', 'CONSTRUCTION PAUSED', 300, 470), ('cars', 'SOME OLD CARS RESTRICTED', 580, 870), ('hybrid', 'PRIMARY CLASSES: HYBRID', 830, 690)):
            if t >= A[key] - 0.2: pill(c, lab, x, y, 20, AMBER, s=e_back(prog(t, A[key] - 0.2, A[key] + 0.1)))
        loc = 'STREET · DELHI'; sec = 2
    elif t < S('12') - 0.05:   # 11 GRAP staircase over the city
        k = e_io(prog(t, S('11') - 0.05, S('11') + 0.8))
        layer(c, lambda cc: street_draw(cc, t), a=1 - k, s=1 - 0.5 * k)
        layer(c, lambda cc: city_draw(cc, t, haze=0.9), a=k, s=1.8 - 0.8 * k)
        cols = [(0.95, 0.75, 0.2), (0.95, 0.5, 0.2), (0.85, 0.25, 0.2), (0.55, 0.1, 0.25)]
        for i, (lab, band) in enumerate((('STAGE I', '201–300'), ('STAGE II', '301–400'), ('STAGE III', '401–450'), ('STAGE IV', '>450'))):
            tt = S('11') + 0.6 + 0.25 * i
            if t < tt: continue
            u = e_out(prog(t, tt, tt + 0.3)); x = 150 + i * 200; h = 140 + 90 * i
            c.set_source_rgba(*cols[i], 0.95 * u); rrect(c, x, 1180 - h, 180, h, 14); c.fill()
            mono(c, lab, x + 90, 1180 - h + 30, 20, CREAM, kind='monob'); mono(c, 'AQI ' + band, x + 90, 1180 - h + 62, 18, CREAM, kind='monob')
        pill(c, 'GRAP · CAQM · STRICTER IN STAGES', W / 2, 560, 26, CREAM, s=e_back(prog(t, S('11') + 0.3, S('11') + 0.6)))
        loc = 'DELHI'; sec = 3
    elif t < S('13') - 0.05:   # 12 zoom out to India: NCAP
        k = prog(t, S('12') - 0.05, S('12') + 1.6)
        if k < 0.3:
            kk = e_io(k / 0.3)
            layer(c, lambda cc: city_draw(cc, t, haze=0.9), a=1 - kk, s=1 - 0.6 * kk)
            layer(c, lambda cc: map_draw(cc, t, CAM_DELHI, haze=1.0), a=kk, s=1.5 - 0.5 * kk)
        else:
            map_draw(c, t, cam_lerp(CAM_DELHI, CAM_INDIA, e_io((k - 0.3) / 0.7)), haze=1.0, labels=('Delhi',) if k > 0.9 else ())
        if t >= A['p40'] - 0.4:
            u = e_back(prog(t, A['p40'] - 0.4, A['p40'] - 0.1)); c.save(); c.translate(830, 1180); c.scale(max(0.01, u), max(0.01, u))
            glass_dark(c, -200, -130, 400, 260, 30); c.set_source_rgba(*PM10, 1); c.set_line_width(14); c.new_path(); c.arc(0, -20, 70, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.4); c.stroke()
            head(c, '−40%', 0, -20, 40, PM10, shadow=False); mono(c, 'NCAP · PM10 TARGET', 0, 78, 18, CREAM, kind='monob'); mono(c, 'BY 2025–26 vs 2017–18', 0, 104, 16, CREAM, kind='mono')
            c.restore()
        loc = 'INDIA'; sec = 3
    elif t < S('14') - 0.05:   # 13 push toward Delhi: 97
        k = e_io(prog(t, S('13') - 0.05, S('13') + 1.2))
        map_draw(c, t, cam_lerp(CAM_INDIA, CAM_NORTH, k), haze=1.0, labels=('Delhi', 'Haryana', 'Uttar Pradesh') if k > 0.8 else ())
        if t >= A['p100'] - 0.4:
            u = e_out(prog(t, A['p100'] - 0.4, A['p100'] + 0.2)); x0, base = 660, 1240
            glass_dark(c, x0 - 40, 600, 400, 720, 30, u)
            pill(c, 'PM2.5', x0 + 160, 650, 22, PM25, a=u)
            h = 97 * 5.2 * prog(t, A['p100'] - 0.3, A['p100'] + 0.5)
            c.set_source_rgba(*PM25, u); rrect(c, x0 + 90, base - h, 140, h, 12); c.fill()
            if h > 50: head(c, '97', x0 + 160, base - h - 34, 48, AMBER, shadow=False)
            c.set_source_rgba(0.9, 0.3, 0.3, u); c.set_line_width(4); c.set_dash([12, 8]); c.move_to(x0, base - 40 * 5.2); c.line_to(x0 + 320, base - 40 * 5.2); c.stroke(); c.set_dash([])
            mono(c, 'ANNUAL LIMIT 40', x0 + 160, base - 40 * 5.2 + 22, 16, (1, 0.6, 0.6), a=u, kind='monob')
            mono(c, 'DELHI · 2025 · µg/m³', x0 + 160, base + 28, 16, CREAM, a=u, kind='monob')
            mono(c, 'CAQM · FULL YEAR', x0 + 160, base + 52, 15, CREAM, a=0.8 * u, kind='mono')
            if t >= A['annual'] - 0.2: pill(c, '≈ 2.5×', x0 + 160, 760, 30, AMBER, s=e_back(prog(t, A['annual'] - 0.2, A['annual'] + 0.1)))
        loc = 'NORTH INDIA'; sec = 3
    elif t < S('15') - 0.05:   # 14 back to India: 23 of 100
        k = e_io(prog(t, S('14') - 0.05, S('14') + 0.8))
        wash = 0.6 * prog(t, A['c23'] + 1.2, A['c23'] + 2.0)
        map_draw(c, t, cam_lerp(CAM_NORTH, CAM_INDIA, k), haze=0.6, wash=wash, labels=('Delhi',))
        glass_dark(c, 80, 900, 340, 400, 26, k)
        pill(c, 'PM10', 250, 935, 18, PM10, col=INK, a=k)
        dotgrid(c, t, S('14'), A['c23'] - 0.1, cx=250, cy=1115)
        if t >= A['c23'] - 0.1: head(c, '23 / 100', 250, 1285, 40, PM10, shadow=False)
        if t >= A['delhi14'] - 0.2: mono(c, 'DELHI: NOT IN THE 23', 250, 1325, 16, CREAM, kind='monob')
        t0c = max(A['c23'] + 0.4, E('14') - 2.7)
        draw_clip(c, 'crea', 620, 560, 860, t, t0c, rot=0.8, hl_t0=t0c + 0.25, hl_dur=0.7, t1=t0c + 1.25)
        draw_clip(c, 'crea2', 620, 560, 860, t, t0c + 1.25 if t >= t0c + 1.25 else 1e9, rot=0.8, hl_t0=t0c + 1.3, hl_dur=0.8, t1=t0c + 2.5)
        if t0c <= t <= t0c + 2.6: source_tag(c, 'CREA · JAN 2026', 300, 745, a=1.0)
        loc = 'INDIA'; sec = 3
    elif t < S('17') - 0.05:   # 15-16 fly east to Beijing
        k = e_io(prog(t, S('15') - 0.05, S('15') + 1.4))
        cam = (lerp(CAM_INDIA[0], 900, k), lerp(CAM_INDIA[1], 250, k), lerp(1.55, 1.2, k))
        if k < 1: map_draw(c, t, cam, haze=0.6, labels=())
        if 0.2 < k < 1:
            sx, sy = w2s(cam, *DELHI); c.set_source_rgba(*AMBER, 0.9); c.set_line_width(5); c.set_dash([14, 12]); c.move_to(sx, sy); c.line_to(sx + 900, sy - 300); c.stroke(); c.set_dash([])
        hz = 1 - 0.75 * prog(t, A['y2013'], A['v27'] + 0.4)
        global STK; STK = [A['coal'] - 0.15, A['gas'] - 0.15, A['vrules'] - 0.15, A['neigh'] - 0.15]
        stk = sum(1 for x in STK if t >= x)
        layer(c, lambda cc: beijing_card(cc, t, haze=hz, stickers=stk, tl=prog(t, A['coal'] - 0.3, A['decade'] + 0.3)), a=prog(t, S('15') + 0.6, S('15') + 1.0), dx=1100 * (1 - e_out(prog(t, S('15') + 0.5, S('15') + 1.4))))
        if t >= A['y2013'] - 0.2:
            v = 89.5 if t < A['v27'] - 0.5 else lerp(89.5, 27, e_io(prog(t, A['v27'] - 0.5, A['v27'] + 0.2)))
            yr = '2013' if t < A['v27'] - 0.5 else ('2025' if t > A['v27'] else '…')
            glass_dark(c, 330, 1210, 420, 120, 30)
            pill(c, 'PM2.5', 400, 1270, 18, PM25)
            head(c, f'{v:.1f}' if v != 27 and v > 27.05 else '27', 560, 1262, 56, AMBER, shadow=False); mono(c, yr, 690, 1270, 22, CREAM, kind='monob')
            if t >= A['v70'] - 0.2 and t < S('16'): pill(c, '−70%', 880, 1270, 34, AMBER, s=e_back(prog(t, A['v70'] - 0.2, A['v70'] + 0.1)))
            if t < S('16'): mono(c, 'BEIJING ECOLOGY BUREAU via CHINA DAILY', 540, 1345, 15, CREAM, a=0.8, kind='mono')
        loc = 'BEIJING'; sec = 4
    elif t < S('18') - 0.05:   # 17 fly back west: the fix
        k = e_io(prog(t, S('17') - 0.05, S('17') + 1.2))
        layer(c, lambda cc: beijing_card(cc, t, haze=0.25, stickers=4, tl=1.0), a=1 - k, dx=1100 * k)
        clear = prog(t, A['region'] - 0.2, A['region'] + 2.0)
        cam = cam_lerp((900, 250, 1.2), CAM_NI, k)
        layer(c, lambda cc: map_draw(cc, t, cam, haze=1.0, clear=clear, ring=clear, labels=('Punjab', 'Haryana', 'Uttar Pradesh', 'Delhi') if k > 0.9 else ()), a=k, dx=-1100 * (1 - k))
        for i, (key, lab, sub) in enumerate((('spike17', 'SPIKE', 'FIRECRACKERS'), ('winter17', 'TRAP', 'WINTER CONDITIONS'), ('every17', 'BUILD', 'ONGOING EMISSIONS'))):
            if t < A[key] - 0.2: continue
            u = e_back(prog(t, A[key] - 0.2, A[key] + 0.1)); x = 200 + i * 340
            c.save(); c.translate(x, 1230); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -150, -60, 300, 120, 24)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -150, -60, 300, 120, 24); c.stroke()
            head(c, lab, 0, -14, 40, AMBER, shadow=False); mono(c, sub, 0, 34, 16, CREAM, kind='monob'); c.restore()
        if t >= A['region'] - 0.2: pill(c, 'YEAR-ROUND + REGION-WIDE', W / 2, 360, 32, AMBER, s=e_back(prog(t, A['region'] - 0.2, A['region'] + 0.1)))
        loc = 'NORTH INDIA'; sec = 5
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('18') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # dive back: slide → city → through the window into frame 0
        k1 = e_io(prog(t, S('L') - 0.05, S('L') + 0.5)); k2 = e_io(prog(t, S('L') + 0.5, S('L') + 1.3))
        c.push_group(); slide(c, t, S('18') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - k1)
        layer(c, lambda cc: city_draw(cc, t, haze=1.0), a=k1 * (1 - k2), s=1 + 2.5 * k2, cx=470, cy=760)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k2)
    if sec is not None and t < S('18') - 0.05: strip(c, sec)
    if loc and t < S('18') - 0.05: locator(c, loc)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('18') - 0.05: tag(c)
    return s
