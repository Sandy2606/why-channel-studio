"""Golden Sparrow S1 - motion-graphics proof of concept (lines 1.4 -> 1.7 first sentence).
python3 poc.py en|te land|vert [stills]
Scenes: MAP (world output, borders 1700 vs 1950, 100-square output grid) -> CATCH (coins) -> POP (people grid)
-> MADE (2.5D depth-parallax reconstruction + equation) -> INCOME (per-person bars) -> HARVEST (grain split)."""
import sys, os, json, math, re, subprocess, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/gs/vis')
from lines import L
import gsmap

LANG, ASP = sys.argv[1], sys.argv[2]; STILLS = len(sys.argv) > 3
TE = LANG == 'te'; LAND = ASP == 'land'
W, H = (1920, 1080) if LAND else (1080, 1920); FPS = 30; SR = 48000
GS = '/home/claude/gs'; OUT = f'{GS}/poc/out'; os.makedirs(OUT, exist_ok=True)
VIS = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/test_batch/'
TL = json.load(open(f'{GS}/out/timeline_{LANG}.json')); M = TL['lines']
ROWS = {r['id']: r for r in L}
F = '/home/claude/gs/vis/fonts/'; RAQM = ImageFont.Layout.RAQM

# ---------------------------------------------------------------- art direction tokens
INK = (13, 12, 18); PAPER = (240, 232, 214); MUTED = (150, 145, 160)
GOLD = (228, 178, 72); RUST = (186, 84, 60); TEAL = (88, 168, 160); SLATE = (120, 140, 178)
LAND_C = (44, 42, 54); EDGE_C = (78, 75, 92); GHOST = (70, 66, 80)

@functools.lru_cache(None)
def font(kind, size):
    size = int(size)
    if TE and kind in ('ui', 'label', 'small', 'disp'):
        return ImageFont.truetype(F + {'disp': 'NotoSerifTelugu-700', 'ui': 'NotoSerifTelugu-600', 'label': 'NotoSerifTelugu-600', 'small': 'NotoSerifTelugu-400'}[kind] + '.ttf', int(size * 0.92), layout_engine=RAQM)
    return ImageFont.truetype(F + {'num': 'Cinzel-700', 'disp': 'Cinzel-700', 'ui': 'SourceSans3-600', 'label': 'SourceSans3-700', 'small': 'SourceSans3-400'}[kind] + '.ttf', size, layout_engine=RAQM)

S = {  # en, te
 'head': ('SHARE OF WORLD OUTPUT', 'ప్రపంచ ఉత్పత్తిలో వాటా'),
 'src1': ('ANGUS MADDISON · ECONOMIC HISTORIAN', 'అంగస్ మాడిసన్ · ఆర్థిక చరిత్రకారుడు'),
 'src2': ('The World Economy (OECD 2001) · estimates', 'The World Economy (OECD 2001) · అంచనాలు'),
 'a1700': ('INDIAN SUBCONTINENT · c.1700', 'భారత ఉపఖండం · సుమారు 1700'), 'pak': ('PAKISTAN', 'పాకిస్తాన్'), 'bgd': ('BANGLADESH', 'బంగ్లాదేశ్'),
 'a1950': ('INDIA · 1950 (DIFFERENT TERRITORY)', 'భారతదేశం · 1950 (వేరే భూభాగం)'),
 'grid': ('100 SQUARES = ALL WORLD OUTPUT', '100 చతురస్రాలు = ప్రపంచ ఉత్పత్తి మొత్తం'),
 'india': ('INDIA', 'భారతదేశం'), 'brit': ('BRITAIN', 'బ్రిటన్'), 'china': ('CHINA', 'చైనా'),
 'half': ('INDIA + CHINA: ALMOST HALF', ''), 'in1700': ('BACK IN 1700', ''),
 'catch': ('A BIG SHARE, BUT NOT EVERYONE RICH', 'పెద్ద వాటా, కానీ అందరూ ధనికులు కాదు'),
 'pop': ('WORLD POPULATION · c.1700', 'ప్రపంచ జనాభా · సుమారు 1700'),
 'pop2': ('ABOUT 1 IN 4 PEOPLE LIVED HERE', 'ప్రతి 4 మందిలో ఒకరు ఇక్కడే'),
 'eq1': ('MANY PEOPLE', 'ఎక్కువ మంది'), 'eq2': ('+ MAKING THINGS', '+ ఎన్నో తయారీలు'), 'eq3': ('= A BIG SHARE', '= పెద్ద వాటా'),
 'dram': ('DRAMATIZED RECONSTRUCTION · c.1680', 'నాటకీయ పునఃసృష్టి · సుమారు 1680'),
 'inc': ('INCOME PER PERSON · c.1700', 'ఒక్కొక్కరి సగటు ఆదాయం · సుమారు 1700'),
 'wavg': ('WORLD AVERAGE', 'ప్రపంచ సగటు'), 'weu': ('WESTERN EUROPE', 'పశ్చిమ యూరప్'),
 'incsrc': ('ESTIMATES · MADDISON 2001 · GDP PER HEAD (1990 INT. $)', 'అంచనాలు · మాడిసన్ 2001 · తలసరి ఆదాయం (1990 అంతర్జాతీయ డాలర్లు)'),
 'harv': ('WHO TOOK THE HARVEST', 'పంట ఎవరికి'),
 'farmer': ('FARMER', 'రైతు'), 'landlord': ('LANDLORD', 'భూస్వామి'), 'state': ('STATE', 'రాజ్యం'),
 'unequal': ('RARELY EQUAL', 'సమానంగా కాదు'),
 'illus': ('ILLUSTRATIVE · SHARES VARIED BY REGION AND RULER', 'ఉదాహరణ మాత్రమే · వాటాలు ప్రాంతాన్ని, పాలకుడిని బట్టి మారేవి'),
}
def T(k): return S[k][1 if TE else 0]

# ---------------------------------------------------------------- event times (EN: word timestamps; TE: phrase + character position)
def take_audio(i):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{GS}/rec/take/{LANG}_{i}.mp3', '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); v = np.where(db > -50)[0]
    return x[max(0, v[0] * hop - 960):min(len(x), (v[-1] + 1) * hop + 2400)]
@functools.lru_cache(None)
def phrases(i):
    x = take_audio(i); hop = 480; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); vo = db > -42
    gaps = []; s = None
    for k, b in enumerate(vo):
        if not b and s is None: s = k
        if b and s is not None:
            if k - s >= 12: gaps.append((k - s, s * hop / SR, k * hop / SR))
            s = None
    nb = ROWS[i]['te' if TE else 'en'].count('⏸')
    sel = sorted(sorted(gaps, reverse=True)[:nb], key=lambda g: g[1]); t0 = M[i][0]
    st = [0] + [g[2] for g in sel]; en = [g[1] for g in sel] + [len(x) / SR - 0.05]
    return [(t0 + a, t0 + b) for a, b in zip(st, en)]
def tok(i, p, token=None, end=False):
    a, b = phrases(i)[p]
    if end: return b
    if token is None: return a
    txt = re.sub(r'\*\*', '', ROWS[i]['te' if TE else 'en']).split('⏸')[p].strip()
    k = txt.find(token); k = max(0, k)
    return a + (b - a) * (k / max(1, len(txt)))
if TE:
    E = dict(big=tok('1.4', 0), maddison=tok('1.4', 1, 'Angus'), y1700=tok('1.4', 1, '1700'), india=tok('1.4', 1, 'మన వాటా'), n24=tok('1.4', 1, '24'),
             britain=tok('1.4', 2), n3=tok('1.4', 2, '3'), y1950=tok('1.4', 3), n4=tok('1.4', 3, '4 శాతం'),
             catch=tok('1.5', 0), every=tok('1.5', 1), rich=tok('1.5', 1, 'ధనికుడని'),
             quarter=tok('1.6', 0, 'నాలుగో'), huge=tok('1.6', 1), made=tok('1.6', 1, 'తయారుచేసేది'), bigshare=tok('1.6', 1, 'అందుకే'),
             income=tok('1.6', 2), avg=tok('1.6', 2, 'ప్రపంచ సగటుకు'), europe=tok('1.6', 2, 'పశ్చిమ'),
             harvest=tok('1.7', 0), split=tok('1.7', 0, 'పంచుకోలేదు'), farmer=tok('1.7', 0, 'రైతు'), landlord=tok('1.7', 0, 'భూస్వామి'),
             state=tok('1.7', 0, 'రాజ్యం'), equal=tok('1.7', 0, 'పంచుకోలేదు') + 0.3, end=tok('1.7', 0, end=True))
else:
    WD = json.load(open(f'{GS}/poc/words_en.json'))
    def w(i, word, after=0.0):
        for x, a, b in WD[i]:
            if x.lower().strip('.,?!').startswith(word.lower()) and a >= after: return a
        raise KeyError(word)
    E = dict(big=M['1.4'][0], maddison=w('1.4', 'Angus'), y1700=w('1.4', '1700'), india=w('1.4', 'India'), n24=w('1.4', '24'),
             britain=w('1.4', 'Britain'), n3=w('1.4', 'three'), y1950=w('1.4', '1950'), n4=w('1.4', 'four'),
             china=w('1.4e', 'China'), n22=w('1.4e', '22'), together=w('1.4e', 'Together'), halfw=w('1.4e', 'half'),
             catch=M['1.5'][0], every=w('1.5', 'every'), rich=w('1.5', 'rich'),
             quarter=w('1.6', 'quarter'), huge=w('1.6', 'huge'), made=w('1.6', 'made'), bigshare=w('1.6', 'made') + 0.8,
             income=w('1.6', 'Income'), avg=w('1.6', 'world'), europe=w('1.6', 'Western'),
             harvest=w('1.7', 'harvest'), split=w('1.7', 'split'), farmer=w('1.7', 'farmer'), landlord=w('1.7', 'landlord'),
             state=w('1.7', 'state'), equal=w('1.7', 'rarely'), end=w('1.7', 'one') + 0.4)
T0 = M['1.4'][0] - 0.8; T1 = E['end'] + 1.3

# ---------------------------------------------------------------- easing + text
def cl(x): return np.clip(x, 0.0, 1.0) if isinstance(x, np.ndarray) else min(1.0, max(0.0, x))
def eo(x): x = cl(x); return 1 - (1 - x) ** 3
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t
def win(t, a, b, fi=0.4, fo=0.4):
    if t < a or t > b: return 0.0
    return min(1.0, (t - a) / fi if fi else 1, (b - t) / fo if fo else 1)
def txt_img(s, kind, size, fill, track=0.0):
    f = font(kind, size); asc, desc = f.getmetrics()
    if track and not TE:
        ws = [f.getlength(c) + size * track for c in s]; wdt = int(sum(ws)) + 4
        im = Image.new('RGBA', (wdt, asc + desc + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 0
        for c, cw in zip(s, ws): d.text((x, 2), c, font=f, fill=fill); x += cw
        return im
    wdt = int(f.getlength(s)) + 6; im = Image.new('RGBA', (wdt, asc + desc + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2, 2), s, font=f, fill=fill); return im
TXC = {}
def txt(s, kind, size, fill=PAPER, track=0.0, glow=False):
    k = (s, kind, size, fill, track, glow)
    if k not in TXC:
        im = txt_img(s, kind, size, fill + (255,), track)
        if glow:
            pad = 30; g = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); g.alpha_composite(im, (pad, pad))
            bl = g.filter(ImageFilter.GaussianBlur(12)); a = bl.split()[3].point(lambda v: int(v * 0.7)); gl = Image.new('RGBA', g.size, fill + (0,)); gl.putalpha(a)
            gl.alpha_composite(g); im = gl
        TXC[k] = im
    return TXC[k]
def put(fr, im, x, y, a=1.0, anchor='lt', dy=0.0):
    if a <= 0.01: return
    if anchor[0] == 'c': x -= im.width / 2
    if anchor[0] == 'r': x -= im.width
    if anchor[1] == 'c': y -= im.height / 2
    if anchor[1] == 'b': y -= im.height
    if a < 0.999:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    fr.alpha_composite(im, (int(x), int(y + dy)))
def rise(t, a, d=0.5):          # enter: fade + 18 px rise
    k = eo((t - a) / d); return k, (1 - k) * 18
def label(fr, t, a, b, s, kind, size, x, y, fill=PAPER, anchor='lt', track=0.0, glow=False):
    if t < a - 0.01: return
    k, dy = rise(t, a); k *= min(1.0, (b - t) / 0.4) if t < b else 0
    put(fr, txt(s, kind, size, fill, track, glow), x, y, k, anchor, dy)
def rule(fr, x, y, w_, t, a, b, col=GOLD, th=3):
    if t < a: return
    k = eo((t - a) / 0.6) * (min(1, (b - t) / 0.4) if t < b else 0)
    if k <= 0: return
    d = ImageDraw.Draw(fr); d.rectangle((x, y, x + int(w_ * k), y + th), fill=col + (int(255 * k),))
def lower_third(fr, t, a, b):
    x = 70 if LAND else 70; y = H - 150 if LAND else 1010
    rule(fr, x, y, 80, t, a, b)
    label(fr, t, a + 0.15, b, T('src1'), 'label', 30 if LAND else 34, x, y + 14, PAPER, track=0.06)
    label(fr, t, a + 0.3, b, T('src2'), 'small', 26 if LAND else 30, x, y + 56, MUTED)
def headline(fr, t, a, b, key, y=None):
    y = (62 if LAND else 150) if y is None else y
    rule(fr, 70, y, 60, t, a, b)
    label(fr, t, a + 0.1, b, T(key), 'label', 34 if LAND else 42, 70, y + 14, PAPER, track=0.08)

# ---------------------------------------------------------------- background (ink + paper grain + vignette)
rng = np.random.default_rng(3)
_paper = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
_paper = cv2.resize(cv2.GaussianBlur(_paper, (0, 0), 1.2), (W, H), interpolation=cv2.INTER_CUBIC)
BG = np.clip(np.array(INK, np.float32)[None, None] + _paper[..., None] * 2.2, 0, 255).astype(np.uint8)
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.42 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.3).clip(0.4, 1).astype(np.float32)[..., None]
GRAIN = [rng.normal(0, 2.6, (H, W, 1)).astype(np.float32) for _ in range(4)]
def base(): return Image.fromarray(BG).convert('RGBA')

# ---------------------------------------------------------------- world map (Equal Earth) layers
def ee(lon, lat):
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796; Mx = math.sqrt(3) / 2
    l, p = math.radians(lon), math.radians(lat); th = math.asin(Mx * math.sin(p)); t2 = th * th; t6 = t2 ** 3
    x = 2 * math.sqrt(3) * l * math.cos(th) / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2)); return x, y
MS = 1500.0                       # map px per projected unit; world ~ 8000 px wide
def mp(lon, lat): x, y = ee(lon, lat); return (x * MS + 4200, -y * MS + 2100)
def svg2ll(x, y):
    lon = (x - gsmap.BX) / gsmap.AX; m = (y - gsmap.BY) / gsmap.AY; return lon, math.degrees(2 * math.atan(math.exp(m)) - math.pi / 2)
@functools.lru_cache(None)
def layers():
    Wm, Hm = 8400, 4200; L_ = {}
    def poly_mask(polys):
        im = Image.new('L', (Wm, Hm), 0); d = ImageDraw.Draw(im)
        for p in polys:
            if len(p) > 2: d.polygon(p, fill=255)
        return im
    def cpolys(names):
        out = []
        for f in gsmap.GEO['features']:
            if names is None or f['properties']['name'] in names:
                g = f['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
                for p in cs: out.append([mp(*pt) for pt in p[0]])
        return out
    ind = [[mp(*svg2ll(x, y)) for x, y in p] for p in gsmap.india_polys()]
    L_['land'] = poly_mask(cpolys(None)); L_['ind'] = poly_mask(ind)
    L_['pb'] = ImageChops.subtract(poly_mask(cpolys(['Pakistan', 'Bangladesh'])), L_['ind'])
    L_['land'] = ImageChops.lighter(L_['land'], L_['ind'])
    L_['gbr'] = poly_mask(cpolys(['United Kingdom'])); L_['chn'] = ImageChops.subtract(poly_mask(cpolys(['China'])), L_['ind'])
    # graticule
    g = Image.new('L', (Wm, Hm), 0); d = ImageDraw.Draw(g)
    for lon in range(-180, 181, 15): d.line([mp(lon, la) for la in range(-85, 86, 5)], fill=255, width=2)
    for lat in range(-75, 76, 15): d.line([mp(lo, lat) for lo in range(-180, 181, 5)], fill=255, width=2)
    L_['grat'] = g
    return L_
def cam_rect(lon0, lon1, lat0, lat1):
    pts = [mp(lo, la) for lo in (lon0, lon1) for la in (lat0, lat1, (lat0 + lat1) / 2, 0 if lat0 < 0 < lat1 else lat0)]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; return (min(xs), min(ys), max(xs), max(ys))
def lerp_rect(a, b, k): return tuple(lerp(p, q, k) for p, q in zip(a, b))
def map_frame(vw, vh, rect, st):
    """Render the map viewport. st: dict of layer states (alpha 0..1, colours, reveal radius)."""
    Ls = layers(); x0, y0, x1, y1 = rect
    # keep aspect: expand rect to viewport aspect
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rw, rh = x1 - x0, y1 - y0
    if rw / rh > vw / vh: rh = rw * vh / vw
    else: rw = rh * vw / vh
    box = (int(cx - rw / 2), int(cy - rh / 2), int(cx + rw / 2), int(cy + rh / 2))
    def m(k): return np.asarray(Ls[k].crop(box).resize((vw, vh), Image.BILINEAR), np.float32)[..., None] / 255
    land, ind, pb, gbr, chn, grat = m('land'), m('ind'), m('pb'), m('gbr'), m('chn'), m('grat')
    img = np.zeros((vh, vw, 3), np.float32) + np.array(INK, np.float32)
    img = img * (1 - grat * 0.35) + np.array((40, 38, 52), np.float32) * grat * 0.35
    img = img * (1 - land) + np.array(LAND_C, np.float32) * land
    def reveal(key, mask):
        r = st.get(key + '_r', 1.0)
        if r >= 1: return mask
        c = st.get(key + '_c'); px = (np.array(c) - np.array([box[0], box[1]])) * vw / (box[2] - box[0])
        d = np.sqrt((np.arange(vw)[None, :] - px[0]) ** 2 + (np.arange(vh)[:, None] - px[1]) ** 2) / (0.6 * vw)
        return mask * np.clip((r - d) / 0.05, 0, 1)[..., None]
    def fill(mask, col, a):
        nonlocal img
        if a > 0: img = img * (1 - mask * a) + np.array(col, np.float32) * mask * a
    sub = np.clip(ind + pb, 0, 1)
    fill(reveal('sub', sub), GOLD, st.get('sub', 0))
    if st.get('pb_grey', 0) > 0:            # 1950: Pakistan + Bangladesh greyed and hatched
        a = st['pb_grey']; hat = (((np.arange(vw)[None, :] + np.arange(vh)[:, None]) // 7) % 2).astype(np.float32)[..., None]
        fill(pb, (64, 62, 72), a); fill(pb * hat * 0.6, (120, 116, 130), a)
        fill(ind, GOLD, a * st.get('sub', 0))
    fill(gbr, RUST, st.get('gbr', 0)); fill(chn, TEAL, st.get('chn', 0))
    # coast/border edge
    e = cv2.dilate(land[..., 0], np.ones((3, 3))) - land[..., 0]
    img = img * (1 - e[..., None] * 0.6) + np.array(EDGE_C, np.float32) * e[..., None] * 0.6
    si = sub[..., 0] * st.get('sub', 0); ei = cv2.dilate(si, np.ones((3, 3))) - si
    img = img * (1 - ei[..., None]) + np.array((255, 224, 150), np.float32) * ei[..., None]
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
    # soft edges into the page
    fade = np.ones((vh, vw), np.float32); f = 60
    fade[:, :f] *= np.linspace(0, 1, f)[None]; fade[:, -f:] *= np.linspace(1, 0, f)[None]; fade[:f] *= np.linspace(0, 1, f)[:, None]; fade[-f:] *= np.linspace(1, 0, f)[:, None]
    out.putalpha(Image.fromarray((fade * 255).astype(np.uint8)))
    return out, box
def to_view(lon, lat, box, vw, vh, ox, oy):
    x, y = mp(lon, lat); return ox + (x - box[0]) * vw / (box[2] - box[0]), oy + (y - box[1]) * vh / (box[3] - box[1])

# ---------------------------------------------------------------- 100-square grid
def grid(fr, t, x0, y0, cell, gap, state, alpha=1.0):
    """state: list of (count, colour, t_on, t_off) applied in order; squares fill row-wise from top-left."""
    d = ImageDraw.Draw(fr); idx = 0; filled = {}
    for cnt, col, ton, toff, ghost in state:
        for k in range(cnt):
            i = idx + k; kk = eo((t - ton - k * 0.035) / 0.35)
            gone = eo((t - toff - (cnt - 1 - k) * 0.03) / 0.35) if toff is not None else 0
            filled[i] = (col, kk * (1 - gone), ghost and gone > 0)
        idx += cnt
    for i in range(100):
        r, c = divmod(i, 10); x = x0 + c * (cell + gap); y = y0 + r * (cell + gap)
        d.rectangle((x, y, x + cell, y + cell), outline=GHOST + (int(200 * alpha),), width=2)
        if i in filled:
            col, k, gh = filled[i]
            if k > 0.01:
                s = cell * (0.55 + 0.45 * k); o = (cell - s) / 2
                d.rectangle((x + o, y + o, x + o + s, y + o + s), fill=col + (int(255 * k * alpha),))
            if gh: d.rectangle((x + 4, y + 4, x + cell - 4, y + cell - 4), outline=col + (int(110 * alpha),), width=2)
def counter(fr, t, t0, val_from, val_to, x, y, size, col, anchor='lt', a=1.0, suffix='%'):
    k = eio((t - t0) / 0.9); v = round(lerp(val_from, val_to, k))
    put(fr, txt(f'{v}{suffix}', 'num', size, col, glow=True), x, y, a, anchor)

# ---------------------------------------------------------------- scene: MAP
def scene_map(fr, t):
    if LAND: vw, vh, ox, oy = W, H, 0, 0
    else: vw, vh, ox, oy = W, 860, 0, 180
    wide = cam_rect(-88, 150, -16, 68) if LAND else cam_rect(-14, 132, -6, 64)
    asia = cam_rect(-82, 144, -12, 66) if LAND else cam_rect(-8, 124, -2, 62)
    sa = cam_rect(22, 112, 2, 42) if LAND else cam_rect(52, 100, 4, 38)
    rect = lerp_rect(wide, asia, eio((t - E['india'] + 0.3) / 2.4))
    if t > E['y1950'] - 0.2: rect = lerp_rect(rect, sa, eio((t - E['y1950'] + 0.2) / 1.6))
    if not TE and t > E['china'] - 0.6: rect = lerp_rect(rect, wide if LAND else asia, eio((t - E['china'] + 0.6) / 1.4))
    st = {'sub': eo((t - E['india']) / 0.4), 'sub_r': eo((t - E['india']) / 1.4) * 1.2, 'sub_c': mp(78, 22),
          'gbr': eo((t - E['britain']) / 0.5) * (1 - eo((t - E['y1950']) / 0.5)), 'pb_grey': eo((t - E['y1950'] - 0.5) / 0.9)}
    if not TE:
        back = eo((t - E['china'] + 0.4) / 0.6); st['pb_grey'] *= 1 - back
        st['gbr'] = max(st['gbr'], back * eo((t - E['china']) / 0.4)); st['chn'] = eo((t - E['china']) / 0.5)
    m, box = map_frame(vw, vh, rect, st); fr.alpha_composite(m, (ox, oy))
    def at(lon, lat): return to_view(lon, lat, box, vw, vh, ox, oy)
    if LAND:     # dark panel behind the grid (left, over the Atlantic)
        pan = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(pan).rectangle((0, 0, 600, H), fill=INK + (215,))
        fr.alpha_composite(pan.filter(ImageFilter.GaussianBlur(50)))
    # map labels
    a1700 = win(t, E['india'] + 0.6, E['y1950'] + 0.3) + (win(t, E['china'] + 0.2, 1e9) if not TE else 0)
    a1950 = win(t, E['y1950'] + 0.8, (E['china'] - 0.3) if not TE else 1e9)
    x, y = at(80, 5)
    put(fr, txt(T('a1700'), 'label', 30 if LAND else 42, GOLD, 0.06), x, y, a1700, 'ct')
    put(fr, txt(T('a1950'), 'label', 30 if LAND else 42, GOLD, 0.06), x, y, a1950, 'ct')
    if a1950 > 0:
        for k_, lo, la in (('pak', 68.5, 28.0), ('bgd', 90.3, 23.6)):
            px, py = at(lo, la); put(fr, txt(T(k_), 'label', 24 if LAND else 32, (215, 210, 225)), px, py, a1950, 'cc')
    if E['britain'] - 0.1 < t < E['y1950'] + 0.3 or (not TE and t > E['china']):
        x, y = at(-2, 54.5); a = win(t, E['britain'], E['y1950'] + 0.3) + (win(t, E['china'], 1e9) if not TE else 0)
        d = ImageDraw.Draw(fr); g = eo((t - E['britain']) / 1.0); r = 16 + 46 * g
        if t < E['y1950']: d.ellipse((x - r, y - r, x + r, y + r), outline=RUST + (int(255 * (1 - g)),), width=3)
        put(fr, txt(T('brit'), 'label', 26 if LAND else 30, RUST, 0.06), x + 28, y - 44, a)
    if not TE and t > E['china']:
        x, y = at(104, 36); put(fr, txt(T('china'), 'label', 28, (220, 245, 240), 0.06), x, y, win(t, E['china'], 1e9), 'cc')
    # headline + year (rolls 1700 -> 1950 -> 1700)
    headline(fr, t, E['big'] - 0.1, E['catch'] - 0.3, 'head')
    if t > E['y1700'] - 0.2:
        ya = win(t, E['y1700'] - 0.2, E['catch'] - 0.3); yfrom, yto, tt = '1700', '1700', E['y1700']
        if t > E['y1950'] - 0.1: yfrom, yto, tt = '1700', '1950', E['y1950'] - 0.1
        if not TE and t > E['china'] - 0.5: yfrom, yto, tt = '1950', '1700', E['china'] - 0.5
        k = eio((t - tt) / 0.5); size = 110 if LAND else 100; yx, yyy = W - 70, (46 if LAND else 120)
        if yfrom != yto and k < 1:
            put(fr, txt(yfrom, 'num', size, PAPER, glow=True), yx, yyy, ya * (1 - k), 'rt', -50 * k); put(fr, txt(yto, 'num', size, PAPER, glow=True), yx, yyy, ya * k, 'rt', 50 * (1 - k))
        else: put(fr, txt(yto, 'num', size, PAPER, glow=True), yx, yyy, ya, 'rt')
    lower_third(fr, t, E['maddison'] - 0.1, E['maddison'] + 3.6)
    # numbers + 100-square grid
    if LAND: gx, gy, cell, gap = 70, 380, 42, 7; nx, ny = 70, 160
    else: gx, gy, cell, gap = 275, 1290, 46, 7; nx, ny = 110, 1060
    ga = win(t, E['y1700'], E['catch'] + 0.5)
    if ga <= 0: return
    put(fr, txt(T('grid'), 'small', 24 if LAND else 28, MUTED), gx, gy + 10 * (cell + gap) + 10, ga * (1 if (LAND or TE) else 1 - eo((t - E['halfw'] + 0.5) / 0.3)))
    india_off = E['n4']; brit_off = E['y1950']
    st_ = [(4, GOLD, E['n24'], None, False), (20, GOLD, E['n24'] + 0.14, india_off, True), (3, RUST, E['n3'], brit_off, True)]
    if not TE and t > E['china'] - 0.4:
        st_ = [(24, GOLD, -9, None, False), (3, RUST, -9, None, False), (22, TEAL, E['n22'], None, False)]
    grid(fr, t, gx, gy, cell, gap, st_, ga)
    sz = 120 if LAND else 120
    if t > E['n24'] - 0.1:
        a = win(t, E['n24'] - 0.1, E['catch'] + 0.3)
        put(fr, txt(T('india'), 'label', 26 if LAND else 30, GOLD, 0.08), nx, ny, a)
        if not TE and t > E['china'] - 0.4: counter(fr, t, E['china'] - 0.4, 4, 24, nx, ny + 30, sz, GOLD, a=a)
        elif t > E['n4'] - 0.1: counter(fr, t, E['n4'] - 0.1, 24, 4, nx, ny + 30, sz, GOLD, a=a)
        else: counter(fr, t, E['n24'] - 0.1, 0, 24, nx, ny + 30, sz, GOLD, a=a)
    if t > E['n3'] - 0.1:
        a = win(t, E['n3'] - 0.1, E['y1950'] + 0.2) + (win(t, E['china'] - 0.2, E['catch'] + 0.3) if not TE else 0)
        bx = nx + (300 if LAND else 360)
        put(fr, txt(T('brit'), 'label', 26 if LAND else 30, RUST, 0.08), bx, ny, a); put(fr, txt('3%', 'num', 64, RUST), bx, ny + 40, a)
    if not TE and t > E['n22'] - 0.1:
        a = win(t, E['n22'] - 0.1, E['catch'] + 0.3); cx_ = nx + (440 if LAND else 600)
        put(fr, txt(T('china'), 'label', 26, TEAL, 0.08), cx_, ny, a); counter(fr, t, E['n22'] - 0.1, 0, 22, cx_, ny + 40, 64, TEAL, a=a)
    if not TE and t > E['halfw'] - 0.4:
        a = win(t, E['halfw'] - 0.4, E['catch'] + 0.3); k = eo((t - E['halfw'] + 0.4) / 0.6)
        d = ImageDraw.Draw(fr); x1 = gx + 10 * (cell + gap) + 10; ytop = gy; ybot = gy + 5 * (cell + gap) - gap
        d.line((x1, ytop, x1 + 18, ytop, x1 + 18, ytop + (ybot - ytop) * k, x1, ytop + (ybot - ytop) * k), fill=PAPER + (int(255 * a),), width=3)
        if LAND: put(fr, txt(T('half'), 'label', 26, PAPER, 0.06), x1 + 34, ytop + (ybot - ytop) / 2, a * k, 'lc')
        else: put(fr, txt(T('half'), 'label', 32, PAPER, 0.06), W / 2, gy + 10 * (cell + gap) + 36, a * k, 'ct')

# ---------------------------------------------------------------- scene: CATCH (coins)
COINS = None
def scene_catch(fr, t):
    a0, a1 = E['catch'] - 0.3, E['quarter'] - 0.9
    cols, rows, R0, gx_, gy_ = (14, 5, 30, 92, 92) if LAND else (8, 8, 34, 112, 112)
    x0 = W / 2 - (cols - 1) * gx_ / 2; y0 = (420 if LAND else 640)
    d = ImageDraw.Draw(fr); out = win(t, a0, a1, 0.3, 0.5); goldi = (rows // 2) * cols + cols // 2
    for i in range(cols * rows):
        r, c = divmod(i, cols); k = eo((t - E['every'] + 0.6 - (c + r) * 0.025) / 0.5)
        if k <= 0: continue
        cx, cy = x0 + c * gx_, y0 + r * gy_ - (1 - k) * 40
        gold = i == goldi and t > E['rich'] - 0.1
        col = GOLD if gold else (92, 80, 64); rim = (255, 222, 150) if gold else (124, 108, 84); al = int(255 * k * out)
        rr = R0 * (1 + 0.15 * eo((t - E['rich'] + 0.1) / 0.4)) if gold else R0
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col + (al,), outline=rim + (al,), width=3)
        d.ellipse((cx - rr * 0.6, cy - rr * 0.6, cx + rr * 0.6, cy + rr * 0.6), outline=rim + (int(al * 0.6),), width=2)
        if gold:
            g = eo((t - E['rich'] + 0.1) / 0.8); q = rr * (1 + 2.2 * g)
            d.ellipse((cx - q, cy - q, cx + q, cy + q), outline=GOLD + (int(220 * (1 - g) * out),), width=3)
    label(fr, t, E['catch'], a1, T('catch'), 'disp', 52 if LAND else 50, W / 2, 200 if LAND else 360, PAPER, 'ct')

# ---------------------------------------------------------------- scene: POPULATION (people grid)
@functools.lru_cache(None)
def person(size, col):
    im = Image.new('RGBA', (size, int(size * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = size * 0.24; d.ellipse((size / 2 - r, 0, size / 2 + r, 2 * r), fill=col + (255,))
    d.rounded_rectangle((size * 0.18, 2 * r + size * 0.08, size * 0.82, size * 1.6 - 1), radius=int(size * 0.28), fill=col + (255,))
    return im
def scene_pop(fr, t):
    a0, a1 = E['quarter'] - 1.0, E['income'] - 0.2
    headline(fr, t, a0, a1, 'pop')
    shrink = eio((t - E['huge'] + 0.2) / 0.8)
    if LAND: cols, size, gx_, gy_ = 20, 46, 70, 100; X0, Y0 = W / 2 - 9.5 * gx_ - size / 2, 300
    else: cols, size, gx_, gy_ = 10, 56, 86, 118; X0, Y0 = W / 2 - 4.5 * gx_ - size / 2, 380
    sc = lerp(1, 0.38, shrink); x0 = lerp(X0, 70, shrink); y0 = lerp(Y0, (700 if LAND else 1180), shrink)
    out = win(t, a0, a1, 0.4, 0.4)
    for i in range(100):
        r, c = divmod(i, cols); india = i in INDIA_IDX
        k = eo((t - a0 - 0.2 - i * 0.006) / 0.4)
        lit = eo((t - E['quarter'] - INDIA_IDX.index(i) * 0.03) / 0.3) if india else 0
        col = tuple(int(lerp(a, b, lit)) for a, b in zip((74, 70, 84), GOLD))
        put(fr, person(max(8, int(size * sc)), col), x0 + c * gx_ * sc, y0 + r * gy_ * sc, k * out)
    pa = win(t, E['quarter'] + 0.4, E['huge'] - 0.1)
    put(fr, txt(T('pop2'), 'disp', 46 if LAND else 48, GOLD, glow=True), W / 2, (860 if LAND else 1650), pa, 'ct')
INDIA_IDX = sorted(np.random.default_rng(5).choice(100, 27, replace=False).tolist())

# ---------------------------------------------------------------- scene: MADE THINGS (2.5D depth parallax)
@functools.lru_cache(None)
def depth_img(name):
    im = Image.open(VIS + name + '.png').convert('RGB')
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    a = np.asarray(im).astype(np.float32) / 255; a = 0.03 + 0.95 * a; a = a ** np.array([0.98, 1.0, 1.06]); l = a.mean(2, keepdims=True); a = l + (a - l) * 0.93
    d = np.asarray(Image.open(f'{GS}/poc/{name}_depth.png').convert('L').resize(im.size, Image.BICUBIC)).astype(np.float32) / 255
    d = cv2.GaussianBlur(d, (0, 0), 3)
    return (np.clip(a, 0, 1) * 255).astype(np.uint8), d
def parallax(name, u, fx, fy, z0, z1, amt=0.10, pan=(0.0, 0.0)):
    img, dep = depth_img(name); ih, iw = dep.shape
    cover = max(W / iw, H / ih); z = lerp(z0, z1, u)
    cx, cy = fx * iw + pan[0] * u * iw, fy * ih + pan[1] * u * ih
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    s = cover * z
    sx = cx + (gx - W / 2) / s; sy = cy + (gy - H / 2) / s
    dd = cv2.remap(dep, sx, sy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    k = 1 + amt * u * (dd - 0.5) * 2              # near pixels scale up faster than far ones: a dolly-in
    sx2 = cx + (gx - W / 2) / (s * k); sy2 = cy + (gy - H / 2) / (s * k)
    out = cv2.remap(img, sx2, sy2, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return Image.fromarray(out).convert('RGBA')
def scene_made(fr, t):
    a0, a1 = E['huge'] - 0.2, E['income'] - 0.2
    u = cl((t - a0) / (a1 - a0 + 1.0))
    p = parallax('T6_chatgpt_v2', u, 0.5 if LAND else 0.56, 0.52, 1.0, 1.12, 0.14, (0.0, -0.01))
    fr.alpha_composite(p); a = win(t, a0, a1, 0.5, 0.4)
    if a < 1: fr.alpha_composite(Image.blend(Image.new('RGBA', (W, H), INK + (255,)), fr, a))
    dk = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(dk).rectangle((0, H - (300 if LAND else 560), W, H), fill=(0, 0, 0, 120)); fr.alpha_composite(dk.filter(ImageFilter.GaussianBlur(60)))
    put(fr, txt(T('dram'), 'small', 22 if LAND else 26, (220, 212, 196), 0.04), 70, 60 if LAND else 200, a * 0.9)
    y = H - 110 if LAND else 1600; sz = 46 if LAND else 52
    xs = (W / 2 - 520, W / 2 - 140, W / 2 + 300) if LAND else (W / 2, W / 2, W / 2)
    ys = (y, y, y) if LAND else (1450, 1540, 1630)
    anc = 'cb'
    for key, tt, x_, y_ in (('eq1', E['huge'] + 0.3, xs[0], ys[0]), ('eq2', E['made'], xs[1], ys[1]), ('eq3', E['bigshare'], xs[2], ys[2])):
        label(fr, t, tt, a1, T(key), 'disp', sz, x_, y_, GOLD if key == 'eq3' else PAPER, anc, glow=(key == 'eq3'))

# ---------------------------------------------------------------- scene: INCOME (per-person bars)
def scene_income(fr, t):
    a0, a1 = E['income'] - 0.2, E['harvest'] - 0.3
    headline(fr, t, a0, a1, 'inc')
    vals = [('wavg', 615, MUTED, a0 + 0.5), ('india', 550, GOLD, E['avg'] - 0.2), ('weu', 997, SLATE, E['europe'])]
    if LAND: bx0, base_y, bw, gap, hmax = 520, 900, 220, 120, 560
    else: bx0, base_y, bw, gap, hmax = 110, 1560, 230, 60, 900
    d = ImageDraw.Draw(fr); out = win(t, a0, a1, 0.3, 0.4)
    d.line((bx0 - 40, base_y, bx0 + 3 * bw + 2 * gap + 40, base_y), fill=EDGE_C + (int(255 * out),), width=2)
    for j, (key, v, col, tt) in enumerate(vals):
        k = eo((t - tt) / 0.9); h = hmax * v / 1000 * k; x = bx0 + j * (bw + gap)
        if k > 0: d.rectangle((x, base_y - h, x + bw, base_y), fill=col + (int(255 * out),))
        label(fr, t, tt, a1, T(key), 'label', 30 if LAND else 32, x + bw / 2, base_y + 18, col if key != 'wavg' else PAPER, 'ct', 0.05)
    # dashed world-average line across the chart
    if t > a0 + 1.0:
        k = eo((t - a0 - 1.0) / 0.8); yv = base_y - hmax * 0.615; xend = bx0 - 40 + (3 * bw + 2 * gap + 80) * k
        x = bx0 - 40
        while x < xend: d.line((x, yv, min(x + 18, xend), yv), fill=PAPER + (int(200 * out),), width=2); x += 30
    put(fr, txt(T('incsrc'), 'small', 22 if LAND else 26, MUTED), W / 2, H - 50 if LAND else 1800, win(t, a0 + 0.6, a1), 'cb')

# ---------------------------------------------------------------- scene: HARVEST (grain particles split three ways)
GR = None
def scene_harvest(fr, t):
    global GR
    a0, a1 = E['harvest'] - 0.3, T1
    headline(fr, t, a0, a1 + 1, 'harv')
    n = 1600; r = np.random.default_rng(9)
    if GR is None:
        ang = r.uniform(0, math.pi, n); rad = np.sqrt(r.uniform(0, 1, n))
        hx = np.cos(ang) * rad * (300 if LAND else 260); hy = -np.sin(ang) * rad * (150 if LAND else 140)
        dest = r.choice(3, n, p=[0.45, 0.22, 0.33])       # illustrative shares, NOT data
        GR = (hx, hy, dest, r.uniform(0, 0.6, n), r.uniform(0.85, 1.15, n))
    hx, hy, dest, dl, sz = GR
    if LAND: cxh, cyh = W / 2, 720; tgt = [(W / 2 - 560, 870), (W / 2, 870), (W / 2 + 560, 870)]
    else: cxh, cyh = W / 2, 760; tgt = [(W / 2 - 340, 1260), (W / 2, 1260), (W / 2 + 340, 1260)]
    tk = [E['farmer'], E['landlord'], E['state']]
    d = ImageDraw.Draw(fr); appear = eo((t - a0) / 0.8)
    pts = []
    for j in range(3):
        sel = dest == j; m_ = int(sel.sum()); rj = np.random.default_rng(20 + j)
        u = rj.uniform(-1, 1, m_); v = np.sqrt(rj.uniform(0, 1, m_)); wdt = (90 + 260 * m_ / n) * (1 if LAND else 0.8)
        tx = tgt[j][0] + u * wdt; ty = tgt[j][1] - (1 - u * u) * v * wdt * 0.55
        k = eio((t - tk[j] + 0.2 - dl[sel] * 0.8) / 1.1)
        sx = cxh + hx[sel]; sy = cyh + hy[sel]
        x = sx + (tx - sx) * k; y = sy + (ty - sy) * k - np.sin(k * math.pi) * 140
        pts.append((x, y, sz[sel]))
    col = (226, 182, 96)
    for x, y, s_ in pts:
        for xi, yi, si in zip(x, y, s_):
            rr = 3.2 * si; d.ellipse((xi - rr, yi - rr * 0.7, xi + rr, yi + rr * 0.7), fill=col + (int(235 * appear),))
    for j, key in enumerate(('farmer', 'landlord', 'state')):
        label(fr, t, tk[j] - 0.1, a1 + 1, T(key), 'label', 34 if LAND else 36, tgt[j][0], tgt[j][1] + 40, PAPER, 'ct', 0.08)
    label(fr, t, E['equal'], a1 + 1, T('unequal'), 'disp', 54 if LAND else 56, W / 2, 230 if LAND else 420, GOLD, 'ct', glow=True)
    put(fr, txt(T('illus'), 'small', 22 if LAND else 24, MUTED), W / 2, H - 50 if LAND else 1800, win(t, E['split'], a1 + 1), 'cb')

# ---------------------------------------------------------------- timeline
SC = [(T0, E['catch'] - 0.1, scene_map), (E['catch'] - 0.5, E['quarter'] - 0.8, scene_catch), (E['quarter'] - 1.0, E['income'] - 0.1, scene_pop),
      (E['huge'] - 0.2, E['income'] - 0.1, scene_made), (E['income'] - 0.3, E['harvest'] - 0.2, scene_income), (E['harvest'] - 0.4, T1, scene_harvest)]
def frame(t):
    fr = base()
    for a, b, fn in SC:
        if a <= t < b: fn(fr, t)
    a = np.asarray(fr.convert('RGB')).astype(np.float32) * VIG + GRAIN[int(t * FPS) % 4]
    fo = min(1, (t - T0) / 0.4, (T1 - t) / 0.6)
    return np.clip(a * max(0, fo), 0, 255).astype(np.uint8)

if __name__ == '__main__':
    tag = f'{LANG.upper()}_{"16x9" if LAND else "9x16"}'
    if STILLS:
        ts = [E['big'] + 0.5, E['maddison'] + 1.5, E['n24'] + 1.2, E['n3'] + 0.8, E['n4'] + 1.0] + ([E['halfw'] + 1.0] if not TE else []) + \
             [E['rich'] + 0.4, E['quarter'] + 1.2, E['bigshare'] + 0.8, E['europe'] + 1.0, E['state'] + 1.2, E['end']]
        ims = [Image.fromarray(frame(t)) for t in ts]
        cols = 4 if LAND else 6; w = 480 if LAND else 270; h = int(w * H / W)
        Sh = Image.new('RGB', (cols * w, ((len(ims) + cols - 1) // cols) * h))
        for i, im in enumerate(ims): Sh.paste(im.resize((w, h), Image.LANCZOS), ((i % cols) * w, (i // cols) * h))
        Sh.save(f'/tmp/claude-0/poc_{tag}.jpg', quality=88); print('stills', len(ims)); sys.exit()
    name = f'GS_S1_POC_motion_{tag}'; vid = f'{OUT}/{name}_v.mp4'
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    nfr = int((T1 - T0) * FPS)
    for f in range(nfr): ff.stdin.write(frame(T0 + f / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    mix = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{GS}/out/{LANG}/GS_S1_film_{LANG.upper()}.wav', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)
    seg = mix[int(T0 * SR):int(T0 * SR) + int(nfr / FPS * SR)].copy(); fl = int(0.3 * SR); fo = int(1.0 * SR)
    seg[:fl] *= np.linspace(0, 1, fl)[:, None]; seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
    import soundfile as sf; sf.write(f'{OUT}/{name}_a.wav', seg, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', f'{OUT}/{name}_a.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{OUT}/{name}.mp4'], check=True)
    os.remove(vid); os.remove(f'{OUT}/{name}_a.wav'); print('done', name, round(T1 - T0, 1))
