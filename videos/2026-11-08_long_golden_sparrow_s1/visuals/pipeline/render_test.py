"""Golden Sparrow S1 - visual test sequence (5 segments) in 16:9 or 9:16, EN or TE.
python3 render_test.py en|te land|vert
Segments: A cold open + title, B trunk scene, C GDP map (1.4), D weaving (2.2-2.3), E ending + Season 2 card.
Audio is cut from the final film mix, so picture timing = real narration timing."""
import sys, os, json, math, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
sys.path.insert(0, '/home/claude/gs'); sys.path.insert(0, '/home/claude/gs/vis')
from lines import L
import gsmap

LANG, ASP = sys.argv[1], sys.argv[2]
W, H = (1920, 1080) if ASP == 'land' else (1080, 1920)
FPS = 30; SR = 48000
GS = '/home/claude/gs'; V = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/test_batch'
OUT = f'{GS}/vis/out'; os.makedirs(OUT, exist_ok=True)
TL = json.load(open(f'{GS}/out/timeline_{LANG}.json')); M = TL['lines']
ROWS = {r['id']: r for r in L}
F = '/home/claude/gs/vis/fonts/'
RAQM = ImageFont.Layout.RAQM
TE = LANG == 'te'

@functools.lru_cache(None)
def font(kind, size):
    if TE and kind != 'title_en': name = {'disp': 'NotoSerifTelugu-700', 'ui': 'NotoSerifTelugu-600', 'small': 'NotoSerifTelugu-400'}.get(kind, 'NotoSerifTelugu-600')
    else: name = {'disp': 'Cinzel-700', 'title_en': 'Cinzel-700', 'ui': 'SourceSans3-600', 'small': 'SourceSans3-400', 'num': 'Cinzel-700'}[kind]
    return ImageFont.truetype(F + name + '.ttf', size, layout_engine=RAQM)

K = 1.0 if ASP == 'land' else 1.0      # text scale (vertical frames are narrower: chips wrap via max width)
TXT = {
 'ban': ('1721 · BRITAIN BANS PRINTED COTTON', '1721 · అచ్చు గుడ్డలపై బ్రిటన్ నిషేధం'),
 'why': ('WHY?', 'ఎందుకు?'),
 'met': ('Palampore · Coromandel Coast, 18th c. · The Met (public domain)', 'పలంపోర్ · కోరమాండల్ తీరం, 18వ శతాబ్దం · The Met'),
 'gdp': ('c.1700 · ~24% OF WORLD OUTPUT · MADDISON ESTIMATE', 'సుమారు 1700 · ప్రపంచ ఉత్పత్తిలో ~24% · మాడిసన్ అంచనా'),
 't1': ('THE GOLDEN SPARROW', 'బంగారు పిచ్చుక'), 't1b': ('SEASON 1', 'సీజన్ 1'),
 'dram': ('DRAMATIZED RECONSTRUCTION · BASED ON SURVIVING MUSEUM CHINTZ', 'నాటకీయ పునఃసృష్టి · మ్యూజియంలోని అసలు చింట్జ్ ఆధారంగా'),
 'dram2': ('DRAMATIZED RECONSTRUCTION', 'నాటకీయ పునఃసృష్టి'),
 'place': ('c.1680 · COROMANDEL COAST', 'సుమారు 1680 · కోరమాండల్ తీరం'),
 'share': ('SHARE OF WORLD OUTPUT', 'ప్రపంచ ఉత్పత్తిలో వాటా'),
 'a1700': ('AREA: UNDIVIDED SUBCONTINENT', 'ప్రాంతం: విభజనకు ముందు ఉపఖండం'),
 'a1950': ('AREA: REPUBLIC OF INDIA ONLY', 'ప్రాంతం: భారత గణతంత్రం మాత్రమే'),
 'brit': ('BRITAIN', 'బ్రిటన్'), 'china': ('CHINA', 'చైనా'),
 'half': ('INDIA + CHINA ~ HALF THE WORLD', ''),
 'pak': ('PAKISTAN', 'పాకిస్తాన్'), 'bgd': ('BANGLADESH', 'బంగ్లాదేశ్'),
 'src': ('ANGUS MADDISON, THE WORLD ECONOMY (OECD 2001) · ESTIMATES', 'అంగస్ మాడిసన్, The World Economy (OECD 2001) · అంచనాలు'),
 't2': ('THE GOLDEN SPARROW · SEASON 2', 'బంగారు పిచ్చుక · సీజన్ 2'),
 't2b': ('HOW A COMPANY BECAME AN EMPIRE', 'ఒక కంపెనీ సామ్రాజ్యం ఎలా అయింది'),
}
def T(k): return TXT[k][1 if TE else 0]

# ---------------------------------------------------------------- images
GOLD = (226, 178, 74); INK = (14, 12, 18)
def grade(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    a = 0.03 + 0.95 * a                                   # lift blacks a touch
    a = a ** np.array([0.98, 1.0, 1.06])                  # warm
    l = a.mean(2, keepdims=True); a = l + (a - l) * 0.93  # gentle desat to unify sources
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
@functools.lru_cache(None)
def src(name):
    p = {'met': f'{GS}/vis/src/met_1982_66.jpg'}.get(name) or f'{V}/{name}.png'
    im = Image.open(p).convert('RGB')
    if im.width < 2500:                                   # upscale small AI stills once, then sharpen
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    return grade(im)
@functools.lru_cache(None)
def bgfill(name):
    im = src(name); s = max(W / im.width, H / im.height) * 1.08
    b = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
    return ImageEnhance.Brightness(b).enhance(0.45)
def kb(name, z, fx, fy):
    """z: 1 = image covers frame; <1 shows more (blurred fill around). (fx, fy): source point at frame centre."""
    im = src(name); cover = max(W / im.width, H / im.height); s = cover * z
    # clamp focus so the image edge never comes inside the frame while it still covers
    hw, hh = W / 2 / s, H / 2 / s
    if im.width * s >= W: fx = min(max(fx * im.width, hw), im.width - hw) / im.width
    if im.height * s >= H: fy = min(max(fy * im.height, hh), im.height - hh) / im.height
    cx, cy = fx * im.width, fy * im.height
    data = (1 / s, 0, cx - W / 2 / s, 0, 1 / s, cy - H / 2 / s)
    fg = im.convert('RGBA').transform((W, H), Image.AFFINE, data, Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    out = bgfill(name).copy(); out.paste(fg, (0, 0), fg); return out

def ease(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t

# ---------------------------------------------------------------- text chips
@functools.lru_cache(None)
def chip(text, kind='ui', size=34, pad=18, bg=(10, 9, 14, 170), fg=(245, 238, 222), maxw=None, accent=True):
    f = font(kind, int(size)); maxw = maxw or W - 120
    words = text.split(' '); lines = []; cur = ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if f.getlength(t) + 2 * pad > maxw and cur: lines.append(cur); cur = w_
        else: cur = t
    lines.append(cur)
    asc, desc = f.getmetrics(); lh = asc + desc + 4
    tw = int(max(f.getlength(l) for l in lines)); th = lh * len(lines)
    im = Image.new('RGBA', (tw + 2 * pad + (8 if accent else 0), th + 2 * pad - 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 8, fill=bg)
    if accent: d.rectangle((0, 6, 4, im.height - 7), fill=GOLD + (255,))
    for i, l in enumerate(lines): d.text((pad + (8 if accent else 0), pad - 6 + i * lh), l, font=f, fill=fg)
    return im
@functools.lru_cache(None)
def big(text, kind='disp', size=120, fg=GOLD, glow=True, maxw=None):
    f = font(kind, int(size)); maxw = maxw or W - 120
    while f.getlength(text) > maxw: size *= 0.92; f = font(kind, int(size))
    asc, desc = f.getmetrics(); tw = int(f.getlength(text)) + 80; th = asc + desc + 80
    im = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.text((40, 40), text, font=f, fill=fg + (255,))
    if glow:
        g = im.filter(ImageFilter.GaussianBlur(14)); a = g.split()[3].point(lambda v: int(v * 0.8))
        g2 = Image.new('RGBA', im.size, fg + (0,)); g2.putalpha(a); g2.alpha_composite(im); im = g2
    return im
def put(frame, im, x, y, alpha=1.0, anchor='lt'):
    if alpha <= 0.01: return
    if anchor[0] == 'c': x -= im.width // 2
    if anchor[0] == 'r': x -= im.width
    if anchor[1] == 'c': y -= im.height // 2
    if anchor[1] == 'b': y -= im.height
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    frame.alpha_composite(im, (int(x), int(y)))
def fadewin(t, a, b, fi=0.35, fo=0.35):
    if t < a or t > b: return 0.0
    return min(1, (t - a) / fi if fi else 1, (b - t) / fo if fo else 1)

# ---------------------------------------------------------------- phrase timing from the takes (pauses = ⏸ marks)
def load_take(i):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{GS}/rec/take/{LANG}_{i}.mp3', '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); v = np.where(db > -50)[0]
    return x[max(0, v[0] * hop - 960):min(len(x), (v[-1] + 1) * hop + 2400)]
@functools.lru_cache(None)
def phrases(i):
    """start times (film time) of each ⏸-separated phrase of line i"""
    x = load_take(i); hop = 480; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); voiced = db > -42
    gaps = []; s = None
    for k, b in enumerate(voiced):
        if not b and s is None: s = k
        if b and s is not None:
            if k - s >= 12: gaps.append((k - s, s * hop / SR, k * hop / SR))
            s = None
    txt = ROWS[i]['te' if TE else 'en']; nb = txt.count('⏸')
    sel = sorted(sorted(gaps, reverse=True)[:nb], key=lambda g: g[1])
    t0 = M[i][0]
    return [t0] + [t0 + g[2] for g in sel]

# ---------------------------------------------------------------- map panels
MST = dict(sea=(17, 19, 30, 255), other=((44, 42, 54, 255), (66, 64, 80, 255)),
           PAK=((200, 150, 40, 255), (255, 226, 150, 255)), BGD=((200, 150, 40, 255), (255, 226, 150, 255)), IND=((200, 150, 40, 255), (255, 226, 150, 255)))
MST50 = dict(MST, PAK=((58, 56, 66, 255), (150, 146, 160, 255)), BGD=((58, 56, 66, 255), (150, 146, 160, 255)))
@functools.lru_cache(None)
def mappanel(which, w, h):
    view = (-230, -40, 700, 720)
    im, (s, ox, oy) = gsmap.render(view, (w, h), MST if which == 1700 else MST50)
    if which == 1950:   # hatch the cut-out areas so the change of borders reads at a glance
        d = ImageDraw.Draw(im)
        mask = Image.new('L', (w, h), 0); md = ImageDraw.Draw(mask)
        for n in ('Pakistan', 'Bangladesh'):
            for p in gsmap.polys(n): md.polygon([(x * s + ox, y * s + oy) for x, y in p], fill=255)
        ind = Image.new('L', (w, h), 0); idd = ImageDraw.Draw(ind)
        for p in gsmap.india_polys(): idd.polygon([(x * s + ox, y * s + oy) for x, y in p], fill=255)
        mask = ImageChops.subtract(mask, ind)
        hat = Image.new('RGBA', (w, h), (0, 0, 0, 0)); hd = ImageDraw.Draw(hat)
        for k in range(-h, w, 14): hd.line((k, 0, k + h, h), fill=(150, 146, 160, 140), width=2)
        im.paste(hat, (0, 0), ImageChops.multiply(mask, hat.split()[3]))
        lab = lambda n, lon, lat: (gsmap.to_svg(lon, lat)[0] * s + ox, gsmap.to_svg(lon, lat)[1] * s + oy)
        for k, lon, lat in (('pak', 67.5, 28.5), ('bgd', 90.2, 24.0)):
            x, y = lab(k, lon, lat); c = chip(T(k), 'small', 22 * w / 900, 6, (0, 0, 0, 0), (200, 196, 210), accent=False)
            im.alpha_composite(c, (int(x - c.width / 2), int(y - c.height / 2)))
    # soft outer glow for the filled area
    return im.convert('RGB')

@functools.lru_cache(None)
def panel(which, pw, ph, mw):
    im = Image.new('RGBA', (pw, ph), (24, 23, 32, 255))
    im.paste(mappanel(which, mw, ph - 70), (0, 0))
    return im

def map_scene(frame, t):
    p = phrases('1.4'); t_name, t24, t3, t4 = p[1], p[1] + 2.6, p[2], p[3]
    t24 = p[2] - 1.0                                     # "24 percent" ends the 2nd phrase
    if TE: t24 = p[2] - 1.1
    t_end = M['1.4e'][1] if (not TE and '1.4e' in M) else M['1.4'][1]
    d = ImageDraw.Draw(frame)
    frame.paste((16, 15, 22), (0, 0, W, H))
    if ASP == 'land': pw, ph, mw = 880, 720, 560; P1 = (50, 150); P2 = (W - 50 - pw, 150)
    else: pw, ph, mw = 960, 700, 560; P1 = (60, 260); P2 = (60, 1040)
    CX = lambda P: P[0] + mw + (pw - mw) // 2          # centre of the numbers column
    head = chip(T('share'), 'ui', 40, 16)
    put(frame, head, W // 2, 60 if ASP == 'land' else 110, fadewin(t, M['1.4'][0] - 0.2, 1e9, 0.4), 'ct')
    # panel 1700 from the start of the line
    a1 = fadewin(t, M['1.4'][0] + 0.2, 1e9, 0.6)
    if a1 > 0:
        pan = panel(1700, pw, ph, mw); put(frame, pan, *P1, a1)
        put(frame, chip('1700', 'num', 46, 12), P1[0] + 20, P1[1] + 20, a1)
        put(frame, chip(T('a1700'), 'ui', 26, 10), P1[0] + 20, P1[1] + ph - 20, a1, 'lb')
        k = ease((t - t24) / 1.2)
        if t > t24 - 0.1:
            n = big(f'{round(24 * k)}%', 'num', 150, maxw=pw - mw); put(frame, n, CX(P1), P1[1] + 90, min(1, (t - t24 + 0.1) / 0.3), 'ct')
        if t > t3 - 0.2:
            al = min(1, (t - t3 + 0.2) / 0.4)
            b = chip(f"{T('brit')}  ~3%", 'ui', 34, 12, maxw=pw - mw - 10); put(frame, b, CX(P1), P1[1] + 330, al, 'ct')
    if t > t4 - 0.3:
        a2 = min(1, (t - t4 + 0.3) / 0.6)
        pan = panel(1950, pw, ph, mw); put(frame, pan, *P2, a2)
        put(frame, chip('1950', 'num', 46, 12), P2[0] + 20, P2[1] + 20, a2)
        put(frame, chip(T('a1950'), 'ui', 26, 10), P2[0] + 20, P2[1] + ph - 20, a2, 'lb')
        k = ease((t - t4 - 1.4) / 1.0)
        if t > t4 + 1.2: put(frame, big(f'{max(1, round(4 * k))}%', 'num', 150, maxw=pw - mw), CX(P2), P2[1] + 90, min(1, (t - t4 - 1.2) / 0.3), 'ct')
    if not TE and '1.4e' in M and t > M['1.4e'][0] - 0.2:
        pe = phrases('1.4e')
        c = chip(f"{T('china')}  ~22%", 'ui', 34, 12, maxw=pw - mw - 10); put(frame, c, CX(P1), P1[1] + 410, min(1, (t - M['1.4e'][0] + 0.2) / 0.4), 'ct')
        if t > pe[1] - 0.2:
            hb = chip(T('half'), 'ui', 36, 14, (120, 84, 14, 220)); put(frame, hb, W // 2, H - 150 if ASP == 'land' else H - 230, min(1, (t - pe[1] + 0.2) / 0.4), 'cb')
    put(frame, chip(T('src'), 'small', 22, 8, (0, 0, 0, 120), (190, 186, 200), accent=False), W // 2, H - 40 if ASP == 'land' else H - 120, fadewin(t, M['1.4'][0], 1e9, 0.5), 'cb')

def subcontinent_scene(frame, t, t0):
    """0.4: the subcontinent glows on a dark map"""
    w, h = (1400, 1100) if ASP == 'land' else (1080, 1300)
    pan = mappanel(1700, w, h); z = lerp(1.0, 1.06, ease((t - t0) / 6))
    pw, ph = int(w * z * (H / h if ASP == 'land' else 1)), int(h * z * (H / h if ASP == 'land' else 1))
    im = pan.resize((pw, ph), Image.BILINEAR); frame.paste((17, 19, 30), (0, 0, W, H)); frame.paste(im, ((W - pw) // 2, (H - ph) // 2))
    put(frame, chip(T('gdp'), 'ui', 34, 14), W // 2, H - 90 if ASP == 'land' else H - 300, fadewin(t, t0 + 0.6, 1e9, 0.4), 'cb')

# ---------------------------------------------------------------- shot lists (film time)
def shots_A():
    p1 = phrases('0.1'); why = p1[-1]
    s = [  # (start, end, kind, args)
        (0.0, M['0.2'][0] + 0.2, 'kb', ('met', 2.2, 2.0, 0.50, 0.40, 0.48, 0.42)),
        (M['0.2'][0] + 0.2, M['0.3'][0] + 0.1, 'kb', ('met', 1.8, 0.42 if ASP == 'land' else 0.8, 0.5, 0.45, 0.5, 0.5)),
        (M['0.3'][0] + 0.1, M['0.3'][1] - 1.3, 'kb', ('T1_chatgpt_v1', 1.0, 1.08, 0.5, 0.55, 0.52, 0.5)),
        (M['0.3'][1] - 1.3, M['0.4'][0] - 0.1, 'kb', ('met', 2.4, 2.7, 0.38, 0.62, 0.40, 0.60)),
        (M['0.4'][0] - 0.1, M['0.5'][0] - 0.1, 'map04', ()),
        (M['0.5'][0] - 0.1, TL['title_hit'] - 0.15, 'kb', ('T2_chatgpt_v1', 1.0, 1.14, 0.5, 0.5, 0.5, 0.42)),
        (TL['title_hit'] - 0.15, TL['title_hit'] + 3.0, 'title1', ()),
    ]
    ov = [('chip', 'ban', M['0.1'][0] + 0.7, M['0.2'][0] + 0.6, 'low'), ('big', 'why', why - 0.05, M['0.2'][0] + 0.2, 'mid'),
          ('small', 'met', M['0.1'][0] + 0.5, M['0.3'][0], 'corner')]
    return s, ov, 0.0, TL['title_hit'] + 3.0
def shots_B():
    a, b = M['F1.1'][0] - 0.6, M['F1.3'][1] + 0.9
    s = [(a, M['F1.2'][0] - 0.1, 'kb', ('T3_chatgpt_v1', 1.0, 1.08, 0.5, 0.55, 0.5, 0.52) if ASP == 'land' else ('T3_chatgpt_v1', 1.0, 1.06, 0.72, 0.5, 0.76, 0.48)),
         (M['F1.2'][0] - 0.1, M['F1.3'][1] - 1.6, 'kb', ('T4_chatgpt_v1', 1.04, 1.12, 0.46 if ASP == 'land' else 0.42, 0.5, 0.52, 0.48)),
         (M['F1.3'][1] - 1.6, b, 'kb', ('met', 2.0, 2.3, 0.5, 0.35, 0.5, 0.33))]
    ov = [('chip', 'dram', M['F1.3'][0] - 0.2, M['F1.3'][1] - 1.4, 'top')]
    return s, ov, a, b
def shots_C():
    a = M['1.4'][0] - 0.6; b = (M['1.4e'][1] if (not TE and '1.4e' in M) else M['1.4'][1]) + 0.8
    return [(a, b, 'map14', ())], [], a, b
def shots_D():
    a, b = M['2.2'][0] - 0.5, M['2.3'][1] + 0.8
    s = [(a, M['2.3'][0] - 0.1, 'kb', ('T5_chatgpt_v1', 1.0, 1.1, 0.45 if ASP == 'land' else 0.4, 0.5, 0.42, 0.48)),
         (M['2.3'][0] - 0.1, b, 'kb', ('T6_chatgpt_v2', 1.08, 1.0, 0.45, 0.5, 0.5, 0.55) if ASP == 'land' else ('T6_chatgpt_v2', 1.0, 1.04, 0.28, 0.5, 0.6, 0.5))]
    ov = [('chip', 'dram2', a + 0.6, a + 4.0, 'top'), ('chip', 'place', a + 0.8, a + 4.0, 'low')]
    return s, ov, a, b
def shots_E():
    a, b = M['7.6'][0] - 0.6, TL['total']
    s = [(a, M['7.7'][0] - 0.1, 'kb', ('T7_chatgpt_v1', 1.0, 1.08, 0.5, 0.5, 0.5, 0.48) if ASP == 'land' else ('T7_chatgpt_v1', 1.0, 1.06, 0.2, 0.5, 0.26, 0.48)),
         (M['7.7'][0] - 0.1, M['7.8'][0] - 0.05, 'kb', ('T7_chatgpt_v1', 1.25, 1.4, 0.68, 0.42, 0.7, 0.4)),
         (M['7.8'][0] - 0.05, M['7.9'][0] - 0.2, 'kb', ('T7_chatgpt_v1', 1.4, 1.5, 0.3, 0.4, 0.3, 0.38)),
         (M['7.9'][0] - 0.2, TL['s2_hit'] - 0.15, 'kb', ('T8_chatgpt_v2', 1.0, 1.18, 0.5, 0.5, 0.5, 0.5)),
         (TL['s2_hit'] - 0.15, b, 'title2', ())]
    return s, [], a, b
SEGS = [('A', 'COLD OPEN', shots_A), ('B', 'TRUNK SCENE', shots_B), ('C', 'GDP MAP (1.4)', shots_C), ('D', 'WEAVING', shots_D), ('E', 'ENDING · SEASON 2', shots_E)]

# ---------------------------------------------------------------- frame compositor
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 5.5, (H, W, 1)).astype(np.float32) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.38 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4).clip(0.45, 1).astype(np.float32)[..., None]

def draw_shot(sh, t):
    st, en, kind, args = sh; u = (t - st) / max(0.01, en - st)
    fr = Image.new('RGBA', (W, H), INK + (255,))
    if kind == 'kb':
        name, z0, z1, x0, y0, x1, y1 = args; e = ease(u) * 0.85 + u * 0.15
        fr.paste(kb(name, lerp(z0, z1, e), lerp(x0, x1, e), lerp(y0, y1, e)))
    elif kind == 'map04': subcontinent_scene(fr, t, st)
    elif kind == 'map14': map_scene(fr, t)
    elif kind in ('title1', 'title2'):
        k1, k2 = ('t1', 't1b') if kind == 'title1' else ('t2', 't2b'); a = min(1, (t - st) / 0.5)
        t1 = big(T(k1), 'disp', 112 if ASP == 'land' else 86, GOLD); put(fr, t1, W // 2, H // 2 - 10, a, 'cb')
        t2 = big(T(k2), 'disp' if kind == 'title1' else 'ui', 52 if ASP == 'land' else 44, (236, 226, 204), glow=False); put(fr, t2, W // 2, H // 2 + 10, min(1, (t - st - 0.5) / 0.6), 'ct')
    return fr

def frame_at(shots, ovs, t):
    cur = [s for s in shots if s[0] <= t < s[1]] or [shots[-1]]; sh = cur[0]
    fr = draw_shot(sh, t)
    i = shots.index(sh); XF = 0.45
    if i + 1 < len(shots) and t > sh[1] - XF and shots[i + 1][2] not in ('title1', 'title2'):   # crossfade into the next shot
        nx = draw_shot(shots[i + 1], t); fr = Image.blend(fr, nx, (t - (sh[1] - XF)) / XF)
    if shots[i][2] == 'kb' and i + 1 < len(shots) and shots[i + 1][2] in ('title1', 'title2'):  # fade to black before the card
        fo = ease((t - (sh[1] - 1.0)) / 1.0); fr = Image.blend(fr, Image.new('RGBA', (W, H), INK + (255,)), fo)
    for kind, key, a, b, where in ovs:
        al = fadewin(t, a, b)
        if al <= 0: continue
        if kind == 'chip':
            c = chip(T(key), 'ui', 36 if ASP == 'land' else 40, 16, maxw=W - 140)
            pos = {'low': (W // 2, H - 110 if ASP == 'land' else H - 420, 'cb'), 'top': (60, 60 if ASP == 'land' else 220, 'lt')}[where]
            put(fr, c, pos[0], pos[1], al, pos[2])
        elif kind == 'big':
            fr = Image.blend(fr, Image.new('RGBA', (W, H), INK + (255,)), 0.5 * al)
            put(fr, big(T(key), 'disp', 170 if ASP == 'land' else 150), W // 2, H // 2, al, 'cc')
        elif kind == 'small':
            c = chip(T(key), 'small', 22 if ASP == 'land' else 26, 8, (0, 0, 0, 120), (210, 205, 195), maxw=W - 100, accent=False)
            put(fr, c, 40, H - 30 if ASP == 'land' else H - 250, al, 'lb')
    a = np.asarray(fr.convert('RGB')).astype(np.float32)
    a = a * VIG + GRAIN[int(t * FPS) % 6]
    return np.clip(a, 0, 255).astype(np.uint8)

def slate(label, n):
    fr = Image.new('RGBA', (W, H), INK + (255,))
    put(fr, chip(f'TEST {n}/5 · {label} · {LANG.upper()} · {"16:9" if ASP == "land" else "9:16"}', 'ui' if not TE else 'ui', 30, 14, (30, 28, 40, 255)), W // 2, H // 2, 1, 'cc')
    return np.asarray(fr.convert('RGB'))

if __name__ == '__main__':
    name = f'GS_S1_visual_test_{LANG.upper()}_{"16x9" if ASP == "land" else "9x16"}'
    vid = f'{OUT}/{name}_v.mp4'
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    mix = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{GS}/out/{LANG}/GS_S1_film_{LANG.upper()}.wav', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)
    audio = []; SL = 1.2
    for n, (k, label, fn) in enumerate(SEGS, 1):
        shots, ovs, a, b = fn()
        sl = slate(label, n)
        for _ in range(int(SL * FPS)): ff.stdin.write(sl.tobytes())
        audio.append(np.zeros((int(SL * SR), 2), np.float32))
        nfr = int(round((b - a) * FPS))
        for f in range(nfr):
            ff.stdin.write(frame_at(shots, ovs, a + f / FPS).tobytes())
        seg = mix[int(a * SR):int(a * SR) + int(round(nfr / FPS * SR))].copy()
        fl = int(0.25 * SR); seg[:fl] *= np.linspace(0, 1, fl)[:, None]; seg[-fl:] *= np.linspace(1, 0, fl)[:, None]
        audio.append(seg); print(k, round(b - a, 1), 's', flush=True)
    ff.stdin.close(); ff.wait()
    import soundfile as sf
    sf.write(f'{OUT}/{name}_a.wav', np.concatenate(audio), SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', f'{OUT}/{name}_a.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{OUT}/{name}.mp4'], check=True)
    os.remove(vid); os.remove(f'{OUT}/{name}_a.wav'); print('done', name)
