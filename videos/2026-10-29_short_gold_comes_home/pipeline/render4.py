"""GOLD · 4/6 'Why is India bringing its gold back home?' — evidence board, style v2."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
_argv = sys.argv; sys.argv = sys.argv[:1]
LANGV = os.environ.get('LANGV', 'en'); PLAT = os.environ.get('PLAT', 'yt')
sys.path.insert(0, '/home/claude/g3'); sys.path.insert(0, '/home/claude/rv')
import render3 as R3
import render2 as K
import host
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.7
ROOT = '/home/claude/g4/'
CREAM, AMBER, AMBER2, INK = K.CREAM, K.AMBER, K.AMBER2, K.INK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, mono, head, rrect = K.font, K.mono, K.head, K.rrect
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad
surf_from_pil, torn, thread, board_bg = R3.surf_from_pil, R3.torn, R3.thread, R3.board_bg
def pill(c, *a, **k):
    if k.get('s', 1.0) <= 0.01: return
    K.pill(c, *a, **k)

# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}_{PLAT}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
KEYS = {  # key: (EN word, nth, TE unit, frac)
    'y1991': ('1991', 1, 0, 0.0), 'broke': ('broke', 1, 0, 0.6), 'weeks': ('few', 1, 1, 0.1),
    'sends': ('government', 1, 2, 0.0), 't47': ('47', 1, 2, 0.45), 'abroad': ('abroad', 1, 2, 0.8), 'loan': ('loan', 1, 3, 0.3),
    'worked': ('worked', 1, 4, 0.0), 'survived': ('survived', 1, 5, 0.3), 'y2024': ('2024', 1, 6, 0.1), 'opposite': ('opposite', 1, 7, 0.6),
    't100': ('100', 1, 8, 0.2), 'london': ('london', 1, 8, 0.0), 't102': ('102', 1, 9, 0.5), 'diwali': ('diwali', 1, 9, 0.15),
    'y2023': ('2023', 1, 10, 0.0), 'p38': ('38', 1, 10, 0.45), 'march': ('march', 1, 11, 0.0), 'p77': ('77', 1, 11, 0.8),
    'why': ('why', 1, 12, 0.0), 'y2022': ('2022', 1, 13, 0.0), 'vaults': ('vaults', 1, 13, 0.7), 'b300': ('300', 1, 14, 0.35), 'froze': ('froze', 1, 14, 0.8),
    'lesson': ('lesson', 1, 15, 0.6), 'keep': ('keep', 1, 16, 0.0), 'y1991b': ('1991', 2, 17, 0.0), 'save': ('save', 1, 17, 0.6),
    'now2': ('now', 1, 18, 0.0), 'protect': ('protect', 1, 18, 0.6), 'full': ('full', 1, 19, 0.0), 'cta': ('if', 1, 20, 0.0), 'comment': ('comment', 1, 21, 0.0),
}
if LANGV == 'en':
    WORDS = json.load(open(ROOT + f'words_en_{PLAT}.json'))
    def norm(w): return w.strip('.,?!$%').lower()
    def T(word, n=1, after=0.0):
        k = 0
        for s, e, w in WORDS:
            if s < after: continue
            if norm(w) == word or (word.isdigit() and norm(w).startswith(word)):
                k += 1
                if k == n: return s + LEAD
        raise KeyError(word)
    A = {}
    for key, (w, n, u, f) in KEYS.items():
        after = 0.0
        if key == 'now2': A[key] = T('now', 1, after=A['save'] - LEAD); continue
        A[key] = T(w, n)
else:
    _J = json.load(open(ROOT + f'words_te_{PLAT}.json')); WORDS = _J['words']; SS = _J['sent'] + [VOICE_LEN]
    A = {key: SS[u] + f * (SS[u + 1] - SS[u]) + LEAD for key, (w, n, u, f) in KEYS.items()}
A['end'] = DUR

CAP = []
for s, e, w in WORDS:
    w = {'RMBI\'s': "RBI's", 'RNBI\'s': "RBI's", 'tons': 'tonnes'}.get(w, w)
    if w.startswith('-') and CAP: CAP[-1][2] += w; CAP[-1][1] = e; continue
    CAP.append([s, e, w])
GROUPS = []; g = []; MAXC = 16 if LANGV == 'en' else 22
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!…' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
K.GROUPS = GROUPS; R3.GROUPS = GROUPS; R3.TECACHE = {}

# ---------------- clippings (real print-to-PDF captures) ----------------
CJ = json.load(open(ROOT + 'clips.json')); CL = {}
def clip(name):
    if name not in CL:
        im = Image.open(ROOT + f'clip_{name}.png').convert('RGB')
        paper, pad = torn(im, seed=len(name))
        CL[name] = (surf_from_pil(paper), [(a + pad, b + pad, c_ + pad, d + pad) for a, b, c_, d in CJ[name]['hl']])
    return CL[name]
def draw_clip(c, name, cx, cy, wpx, t, t0, rot=-1.5, hl_t0=None, hl_dur=0.9, a=1.0, guide=True):
    if t < t0: return
    (sf, _), rects = clip(name)
    u = e_out(prog(t, t0, t0 + 0.4)); sc = wpx / sf.get_width(); w, h = sf.get_width(), sf.get_height()
    c.save(); c.translate(cx, cy + (1 - u) * 260); c.rotate(math.radians(rot + (1 - u) * 6)); c.scale(sc, sc)
    c.set_source_rgba(0, 0, 0, 0.45 * u * a); c.rectangle(-w / 2 + 10, -h / 2 + 18, w, h); c.fill()
    c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a)
    tip = None
    if hl_t0 is not None and t >= hl_t0:
        tot = sum(r[2] - r[0] for r in rects); done = prog(t, hl_t0, hl_t0 + hl_dur) * tot
        for (x0, y0, x1, y1) in rects:
            wl = x1 - x0; f = clamp(done / wl); done -= wl
            if f <= 0: break
            xa, xb = -w / 2 + x0 - 3, -w / 2 + x0 + wl * f + 3
            c.set_source_rgba(1.0, 0.70, 0.14, 0.42); c.rectangle(xa, -h / 2 + y0 - 2, xb - xa, y1 - y0 + 4); c.fill()
            tip = c.user_to_device(xb, -h / 2 + (y0 + y1) / 2)
    for tx in (-w / 2 + 90, w / 2 - 90):
        c.save(); c.translate(tx, -h / 2 + 4); c.rotate(math.radians(-30 if tx < 0 else 30)); s2 = 1 / sc
        c.set_source_rgba(0.95, 0.89, 0.70, 0.75 * u); c.rectangle(-55 * s2, -14 * s2, 110 * s2, 28 * s2); c.fill(); c.restore()
    c.restore()
    if tip and guide and prog(t, hl_t0, hl_t0 + hl_dur) < 1: glowdot(c, tip[0], tip[1], 10)
def source_tag(c, txt, x, y, a=1.0):
    font(c, 'mono', 20); e = c.text_extents(txt)
    glass_dark(c, x - 14, y - 22, e.x_advance + 28, 40, 20, a); c.move_to(x, y + 6); c.set_source_rgba(*CREAM, a); c.show_text(txt)

# ---------------- photos ----------------
PH = {}
def photo(name):
    if name not in PH:
        im = Image.open(ROOT + name).convert('RGB')
        s = max(W * 1.12 / im.width, H * 1.12 / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        PH[name] = surf_from_pil(im)
    return PH[name][0]
def full_photo(c, name, t, t0, t1, z=(1.0, 1.08), focus=(0.5, 0.5), dim=0.3, label=None):
    sf = photo(name); u = e_io(prog(t, t0, t1)); zz = z[0] + (z[1] - z[0]) * u
    sw, sh = sf.get_width(), sf.get_height()
    c.save(); c.translate(W / 2, H / 2); c.scale(zz, zz); c.translate(-sw * focus[0], -sh * focus[1]); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()
    if dim: c.set_source_rgba(0, 0, 0, dim); c.paint()
    g = cairo.LinearGradient(0, 1150, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8); c.set_source(g); c.paint()
    if label: mono(c, label, W - 150, 1250, 18, (1, 1, 1), a=0.7, anchor='r', kind='mono')
def print_photo(c, name, cx, cy, w, t, t0, rot=3, caption=None):
    R3.ROOT = ROOT; R3.print_photo(c, name, cx, cy, w, t, t0, rot=rot, caption=caption)

# ---------------- map (wide: India to London) ----------------
GEO = json.load(open('/home/claude/sandy2606/why-channel-studio/pipeline/lib/countries.geojson')); POLYS = []
for f in GEO['features']:
    gg = f['geometry']
    if gg is None: continue
    for p in (gg['coordinates'] if gg['type'] == 'MultiPolygon' else [gg['coordinates']]):
        r = np.array(p[0])
        if r[:, 0].max() < -30 or r[:, 0].min() > 110 or r[:, 1].max() < -10 or r[:, 1].min() > 72: continue
        POLYS.append(r)
KX = math.cos(math.radians(35))
def ll(lon, lat, clon, clat, z): return W / 2 + (lon - clon) * z * KX, H / 2 - (lat - clat) * z
def draw_map(c, clon, clat, z):
    c.set_source_rgb(0.05, 0.065, 0.085); c.paint()
    c.save(); c.translate(W / 2, H / 2); c.scale(z * KX, -z); c.translate(-clon, -clat)
    for r in POLYS:
        c.move_to(*r[0]); [c.line_to(*q) for q in r[1:]]; c.close_path()
    c.restore(); c.set_source_rgb(0.17, 0.155, 0.13); c.fill_preserve(); c.set_line_width(2); c.stroke()
    K.grain(c)
MUM, LON = (72.88, 19.08), (-0.13, 51.51)
MAPV = (38.0, 30.0, 13.5)
def arc(c, a, b, t, t0, dur, cam, col=AMBER, label=None, bar=True, lift=260):
    u = e_io(prog(t, t0, t0 + dur))
    if u <= 0: return None
    x0, y0 = ll(*a, *cam); x1, y1 = ll(*b, *cam); xm, ym = (x0 + x1) / 2, min(y0, y1) - lift
    pts = [((1 - s) ** 2 * x0 + 2 * (1 - s) * s * xm + s * s * x1, (1 - s) ** 2 * y0 + 2 * (1 - s) * s * ym + s * s * y1) for s in np.linspace(0, u, 50)]
    c.set_line_width(5); c.set_dash([3, 12]); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgba(*col, 0.9)
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke(); c.set_dash([]); c.set_line_cap(cairo.LINE_CAP_BUTT)
    if bar and u < 1:
        px, py = pts[-1]; R3.gold_bar(c, px, py, 0.18, glow=0.8)
    return pts[-1]
def city(c, lonlat, name, cam, t, t0, side='r', sub=None):
    if t < t0: return
    x, y = ll(*lonlat, *cam); K.pin(c, x, y, t, t0)
    u = e_out(prog(t, t0, t0 + 0.3)); font(c, 'head', 42); e = c.text_extents(name); w = e.x_advance + 48
    xx = x + 34 if side == 'r' else x - 34 - w
    glass_dark(c, xx, y - 40, w, 80, 20, u); c.move_to(xx + 24, y + 15); c.set_source_rgba(*CREAM, u); c.show_text(name)

# ---------------- graphics ----------------
def big_num(c, txt, x, y, px, t, t0, anchor='c'):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); font(c, 'head', px); e = c.text_extents(txt)
    c.save(); c.translate(x, y); c.scale(u, u)
    xx = -e.width / 2 - e.x_bearing if anchor == 'c' else 0
    c.move_to(xx, px * 0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(0, 0, 0, 0.85); c.set_line_width(px * 0.1); c.stroke_preserve(); c.set_source(agrad(xx, 0, xx + e.width, 0)); c.fill(); c.restore()
def share_bar(c, y, label, frac, t, t0, col_grad=True):
    x0, w, h = 120, 840, 90
    glass_dark(c, x0, y, w, h, 45)
    u = e_out(prog(t, t0, t0 + 0.8)); fw = max(h, w * frac * u)
    rrect(c, x0, y, fw, h, 45); c.set_source(agrad(x0, 0, x0 + w, 0) if col_grad else cairo.SolidPattern(0.55, 0.55, 0.6)); c.fill()
    mono(c, label, x0, y - 30, 26, CREAM, anchor='l', kind='monob')
    if u > 0.2:
        font(c, 'head', 60); s = f'{int(round(frac * 100 * u))}%'; e = c.text_extents(s)
        c.move_to(x0 + fw - e.width - 30, y + h / 2 + 22); c.set_source_rgb(*INK); c.show_text(s)
def lock(c, x, y, s, closed, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.set_line_width(22); c.set_source_rgba(*CREAM, a); lift = 40 * (1 - closed)
    c.arc(0, -70 - lift, 60, math.pi, 0); c.line_to(60, -40 - lift); c.move_to(-60, -70 - lift); c.line_to(-60, -40); c.stroke()
    rrect(c, -95, -50, 190, 150, 26); c.set_source(agrad(-95, 0, 95, 0)); c.fill()
    c.set_source_rgba(*INK, a); c.arc(0, 15, 18, 0, 2 * math.pi); c.fill(); c.rectangle(-7, 15, 14, 45); c.fill()
    c.restore()
def qmark(c, t, x, y, size, morph=0.0):
    host.draw(c, x, y, size, morph=morph, glow=0.8, eye='open', look=(0, 0), brow=0, tilt=3 * math.sin(t * 2), sq=1.0)

TAGS = None
def tag(c):
    global TAGS
    txt = 'GOLD · 4/6' if LANGV == 'en' else 'గోల్డ్ · 4/6'
    if LANGV == 'te':
        if TAGS is None:
            f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 26, layout_engine=ImageFont.Layout.RAQM)
            try: f.set_variation_by_name('Bold')
            except Exception: pass
            im = Image.new('RGBA', (300, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 30), txt, font=f, fill=(244, 241, 234, 255), anchor='lm')
            TAGS = surf_from_pil(im)
        glass_dark(c, 40, 92, 230, 54, 27); glowdot(c, 68, 119, 7); c.set_source_surface(TAGS[0], 88, 89); c.paint(); return
    font(c, 'monob', 24); e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7); c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)

# ---------------- frame ----------------
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    # 1. 1991: India almost broke + BT clipping
    if t < A['sends'] - 0.05:
        full_photo(c, 'rbi.jpg', t, 0, A['sends'], z=(1.12, 1.0), focus=(0.5, 0.42), dim=0.45, label='RBI, Mumbai · Pinakpani · CC BY-SA 4.0')
        big_num(c, '1991', W / 2, 380, 260, t, -0.3)
        if t >= A['broke'] - 0.1: pill(c, 'INDIA: ALMOST BROKE', W / 2, 580, 40, AMBER, s=e_back(prog(t, A['broke'] - 0.1, A['broke'] + 0.2)))
        if t >= A['weeks'] - 0.35:
            c.set_source_rgba(0, 0, 0, 0.35 * prog(t, A['weeks'] - 0.35, A['weeks'])); c.paint()
            draw_clip(c, 'bt26_q1', W / 2, 860, 960, t, A['weeks'] - 0.35, rot=-1.2, hl_t0=A['weeks'], hl_dur=1.4)
            if t >= A['weeks']: source_tag(c, 'BUSINESS TODAY · MAY 6, 2026', 100, 1040, a=prog(t, A['weeks'], A['weeks'] + 0.3))
    # 2. gold goes abroad + BT 1991 line
    elif t < A['worked'] - 0.05:
        cam = MAPV; draw_map(c, *cam)
        city(c, MUM, 'INDIA', cam, t, A['sends'], side='l'); city(c, LON, 'LONDON', cam, t, A['abroad'] - 0.3, side='r')
        arc(c, MUM, LON, t, A['t47'] - 0.2, 1.3, cam, col=CREAM)
        big_num(c, '47 TONNES', W / 2, 330, 120, t, A['t47'])
        draw_clip(c, 'bt26_q2', W / 2, 1060, 900, t, A['loan'] - 0.6, rot=1.2, hl_t0=A['loan'] - 0.4, hl_dur=1.6)
        mono(c, 'TO THE BANK OF ENGLAND & BANK OF JAPAN', W / 2, 1255, 20, CREAM, a=0.75 * prog(t, A['loan'], A['loan'] + 0.3), kind='mono')
    # 3. it worked
    elif t < A['y2024'] - 0.05:
        full_photo(c, 'boe.jpg', t, A['worked'], A['y2024'], z=(1.0, 1.08), focus=(0.45, 0.5), dim=0.35, label='Bank of England · David Iliff · CC BY-SA 3.0')
        pill(c, 'IT WORKED', W / 2, 520, 50, CREAM, s=e_back(prog(t, A['worked'], A['worked'] + 0.25)))
        if t >= A['survived']: pill(c, 'INDIA SURVIVED', W / 2, 660, 44, AMBER, s=e_back(prog(t, A['survived'], A['survived'] + 0.25)))
    # 4. 2024: exact opposite
    elif t < A['t100'] - 0.1:
        big_num(c, '2024', W / 2, 360, 260, t, A['y2024'])
        draw_clip(c, 'bt24_head', W / 2, 860, 900, t, A['opposite'] - 0.6, rot=-1.5)
        if t >= A['opposite'] - 0.3: source_tag(c, 'BUSINESS TODAY · JUN 1, 2024', 110, 1150, a=prog(t, A['opposite'] - 0.3, A['opposite']))
    # 5. 100 + 102 tonnes flown back
    elif t < A['y2023'] - 0.05:
        cam = MAPV; draw_map(c, *cam)
        city(c, MUM, 'INDIA', cam, t, A['t100'] - 0.1, side='l'); city(c, LON, 'LONDON', cam, t, A['t100'] - 0.1, side='r')
        arc(c, LON, MUM, t, A['t100'] - 0.05, 1.2, cam)
        arc(c, LON, MUM, t, A['t102'] - 0.3, 1.2, cam, lift=360)
        big_num(c, '100 T', 280, 340, 120, t, A['t100'])
        big_num(c, '+102 T', 760, 340, 120, t, A['t102'])
        draw_clip(c, 'wk_head', W / 2, 1010, 820, t, A['diwali'] - 0.2, rot=1.5, hl_t0=A['diwali'] + 0.2, hl_dur=1.2)
    # 6. 38% -> 77%
    elif t < A['why'] - 0.05:
        draw_clip(c, 'dr_q', W / 2, 470, 1000, t, A['y2023'] - 0.05, rot=-1.0, hl_t0=A['p77'] - 0.1, hl_dur=1.0)
        if t >= A['y2023']: share_bar(c, 760, "RBI GOLD KEPT IN INDIA · MARCH 2023", 0.38, t, A['p38'] - 0.1, col_grad=False)
        if t >= A['march']: share_bar(c, 990, 'MARCH 2026', 0.77, t, A['p77'] - 0.2)
        if t >= A['y2023']: source_tag(c, 'DRISHTI IAS (VIA INDIAN EXPRESS) · MAY 6, 2026', 90, 1180, a=prog(t, A['y2023'], A['y2023'] + 0.3))
    # 7. why bring it home?
    elif t < A['y2022'] - 0.05:
        full_photo(c, 'vault.jpg', t, A['why'], A['y2022'], z=(1.0, 1.1), focus=(0.55, 0.45), dim=0.5, label='Connor McManus · Pexels')
        qmark(c, t, W / 2, 1000, 520)
    # 8. 2022: Russia's $300B frozen
    elif t < A['lesson'] - 0.1:
        draw_clip(c, 'rt_q', W / 2, 400, 1000, t, A['y2022'] - 0.05, rot=1.0, hl_t0=A['b300'] - 0.05, hl_dur=0.8)
        source_tag(c, 'REUTERS FACTBOX (VIA ENERGIESNET) · 2022', 100, 600, a=prog(t, A['y2022'], A['y2022'] + 0.3))
        big_num(c, '$300 BILLION', W / 2, 820, 120, t, A['b300'])
        if t >= A['froze'] - 0.4:
            lock(c, W / 2, 1110, 0.9, e_out(prog(t, A['froze'], A['froze'] + 0.25)))
            pill(c, 'FROZEN', W / 2, 1290, 40, CREAM, s=e_back(prog(t, A['froze'], A['froze'] + 0.25)))
    # 9. the lesson
    elif t < A['y1991b'] - 0.05:
        full_photo(c, 'vault.jpg', t, A['lesson'], A['y1991b'], z=(1.1, 1.18), focus=(0.55, 0.45), dim=0.6)
        u = e_out(prog(t, A['lesson'] - 0.1, A['lesson'] + 0.25))
        c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 90, 520, 900, 300, 34, u)
        c.set_source_rgba(*AMBER, u); c.rectangle(112, 545, 6, 250); c.fill()
        mono(c, 'THE LESSON', 150, 580, 24, AMBER, a=u, anchor='l', kind='monob')
        head(c, 'KEEP YOUR GOLD', 150, 660, 54, CREAM, a=u, anchor='l', shadow=False)
        if t >= A['keep'] + 0.4:
            font(c, 'head', 54); e = c.text_extents('WHERE YOU CAN REACH IT'); hw = e.width * e_out(prog(t, A['keep'] + 0.5, A['keep'] + 1.2))
            c.set_source_rgba(1.0, 0.70, 0.14, 0.45); c.rectangle(146, 718, hw + 8, 62); c.fill()
        head(c, 'WHERE YOU CAN REACH IT', 150, 750, 54, CREAM, a=u, anchor='l', shadow=False)
        c.restore()
        lock(c, W / 2, 1070, 0.7, 0.0 if t < A['keep'] + 0.6 else 1.0 - e_out(prog(t, A['keep'] + 0.6, A['keep'] + 0.9)) * 0)
    # 10. payoff: save -> protect
    elif t < A['full'] - 0.1:
        cam = MAPV; draw_map(c, *cam)
        city(c, MUM, 'INDIA', cam, t, A['y1991b'], side='l'); city(c, LON, 'LONDON', cam, t, A['y1991b'], side='r')
        arc(c, MUM, LON, t, A['y1991b'], 0.9, cam, col=CREAM, bar=False)
        if t >= A['save'] - 0.1: pill(c, '1991 · TO SAVE IT', 300, 330, 34, CREAM, s=e_back(prog(t, A['save'] - 0.1, A['save'] + 0.2)))
        arc(c, LON, MUM, t, A['now2'], 0.9, cam, lift=380)
        if t >= A['protect'] - 0.1: pill(c, 'NOW · TO PROTECT IT', 760, 430, 34, AMBER, s=e_back(prog(t, A['protect'] - 0.1, A['protect'] + 0.2)))
        qmark(c, t, W / 2, 1180, 380, morph=e_io(prog(t, A['protect'], A['protect'] + 0.5)))
    # 11. board zoom-out + CTA
    else:
        print_photo(c, 'rbi.jpg', 250, 470, 280, t, A['full'] - 0.1, rot=-4)
        draw_clip(c, 'wk_head', 770, 380, 480, t, A['full'], rot=3, guide=False)
        draw_clip(c, 'dr_q', 600, 720, 700, t, A['full'] + 0.15, rot=-2, guide=False)
        draw_clip(c, 'rt_q', 480, 900, 640, t, A['full'] + 0.3, rot=1.5, guide=False)
        thread(c, 380, 560, 560, 420, t, A['full'] + 0.3, 0.5); thread(c, 770, 560, 640, 680, t, A['full'] + 0.5, 0.5); thread(c, 330, 640, 300, 880, t, A['full'] + 0.7, 0.5)
        if t >= A['comment'] - 0.1:
            u2 = e_back(prog(t, A['comment'] - 0.1, A['comment'] + 0.2))
            c.save(); c.translate(W / 2, 1150); c.scale(u2, u2); glass_dark(c, -400, -90, 800, 180, 40)
            head(c, 'GOT A WHY?', 0, -26, 60, CREAM, shadow=False); mono(c, 'COMMENT IT · WE FIND THE ANSWER', 0, 42, 24, AMBER, kind='monob'); c.restore()
    (K.captions(c, t, y=1420) if LANGV == 'en' else R3.te_captions(c, t, y=1420))
    tag(c)
    return s

def main(part=0, parts=1, out=None, still=None):
    if still is not None:
        os.makedirs(ROOT + 'stills', exist_ok=True)
        for tt in still: frame(tt).write_to_png(f'{ROOT}stills/{LANGV}_{tt:05.2f}.png')
        return
    n = int(DUR * FPS); a = n * part // parts; b = n * (part + 1) // parts
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        s = frame(i / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'still': main(still=[float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == 'anchors': print({k: round(v, 2) for k, v in A.items()})
    else: main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
