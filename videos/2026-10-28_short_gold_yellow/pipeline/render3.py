"""GOLD · 3/6 'Why is gold yellow?' — evidence-board style (dark glass + amber guide + real clippings)."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageFilter, ImageDraw
_argv = sys.argv; sys.argv = sys.argv[:1]
sys.path.insert(0, '/home/claude/rv')
import render2 as K           # style helpers (glass, glow, pills, captions, fonts)
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.7
ROOT = '/home/claude/g3/'
PLAT = os.environ.get('PLAT', 'yt')
CREAM, AMBER, AMBER2, INK, BLACK = K.CREAM, K.AMBER, K.AMBER2, K.INK, K.BLACK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, mono, head, rrect = K.font, K.mono, K.head, K.rrect
def pill(c, *a, **k):
    if k.get('s', 1.0) <= 0.01: return
    K.pill(c, *a, **k)
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad

# ---------------- words / anchors ----------------
LANGV = os.environ.get('LANGV', 'en')
VFILE = ROOT + (f'voice_{PLAT}.wav' if LANGV == 'en' else f'voice_te_{PLAT}.wav')
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
if LANGV == 'en':
    WORDS = []
    for s_, e_, w_ in json.load(open(ROOT + f'words_{PLAT}.json')):
        if w_.lower().startswith('illiquid'):
            m_ = (s_ + e_) / 2; WORDS += [[s_, m_, 'a'], [m_, e_, 'liquid.']]
        else: WORDS.append([s_, e_, w_])
    def T(word, n=1, after=0.0):
        k = 0
        for s, e, w in WORDS:
            if s < after: continue
            if w.strip('.,?!').lower() == word.lower():
                k += 1
                if k == n: return s + LEAD
        raise KeyError(word)
    A = dict(keys=T('keys'), spoons=T('spoons'), phone=T('phone'), silver1=T('silver'), gold1=T('gold'), yellow=T('yellow'),
             thought=T('thought'), turns=T('turns'), einstein=T('einstein'), atom=T('atom'), n79=T('79'),
             some=T('some'), over=T('over'), half=T('half'), at=T('at', 3), relativity=T('relativity'), heavier=T('heavier'),
             closer=T('closer'), changes=T('changes'), soaks=T('soaks'), swallows=T('swallows'), blue1=T('blue'),
             minus=T('minus'), yellow2=T('yellow', 2), silver2=T('silver', 2), see=T('see'), bounces=T('bounces'),
             which=T('which', 2), without=T('without'), silver3=T('silver', 3), notjust=T('not'), y2013=T('2013'),
             mercury=T('mercury'), liquid=T('liquid'), without2=T('without', 2), n105=T('105'), higher=T('higher'),
             full=T('full'), comment=T('comment'), cta2=T('if'))
else:
    _J = json.load(open(ROOT + f'words_te_{PLAT}.json')); WORDS = _J['words']; SS = _J['sent'] + [VOICE_LEN]
    def SA(i, f=0.0): return SS[i] + f * (SS[i + 1] - SS[i]) + LEAD
    A = dict(keys=SA(1, 0.0), spoons=SA(1, 0.3), phone=SA(1, 0.6), silver1=SA(2, 0.45), gold1=SA(3, 0.0), yellow=SA(3, 0.05),
             thought=SA(4), turns=SA(5), einstein=SA(6), atom=SA(7), n79=SA(8, 0.08), some=SA(8, 0.45), over=SA(8, 0.62), half=SA(8, 0.7),
             at=SA(9), relativity=SA(9, 0.55), heavier=SA(10, 0.15), closer=SA(10, 0.6), changes=SA(11), soaks=SA(11, 0.6),
             swallows=SA(12), blue1=SA(12, 0.2), minus=SA(13, 0.3), yellow2=SA(13, 0.8), silver2=SA(14), see=SA(15, 0.6), bounces=SA(16, 0.4),
             which=SA(17), without=SA(18), silver3=SA(18, 0.72), notjust=SA(19), y2013=SA(20), mercury=SA(20, 0.3), liquid=SA(20, 0.45),
             without2=SA(21), n105=SA(21, 0.45), higher=SA(21, 0.8), full=SA(22), cta2=SA(23), comment=SA(24))
A['end'] = DUR

# captions
CAP = []
for s, e, w in WORDS:
    w = {'gem': 'jump', 'video': 'why', 'We': 'We'}.get(w, w)
    if w.startswith('-'): CAP[-1][2] += w; CAP[-1][1] = e; continue
    CAP.append([s, e, w])
GROUPS = []; g = []
MAXC = 16 if LANGV == 'en' else 22
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!…' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
K.GROUPS = GROUPS

from PIL import ImageFont
TEF = None; TECACHE = {}
def te_captions(c, t, y=1400):
    global TEF
    if TEF is None:
        TEF = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 76, layout_engine=ImageFont.Layout.RAQM)
        try: TEF.set_variation_by_name('Black')
        except Exception: pass
    for gi, g in enumerate(GROUPS):
        end = GROUPS[gi + 1][0][0] if gi + 1 < len(GROUPS) else g[-1][1] + 0.6
        if g[0][0] - 0.02 <= t < min(end, g[-1][1] + 0.6):
            act = -1
            for k, (s, e, _) in enumerate(g):
                if s <= t < e + 0.05: act = k
            key = (gi, act)
            if key not in TECACHE:
                words = [x[2].strip(',') for x in g]
                d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
                sp = 22; ws = [d0.textlength(w, font=TEF) for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
                sc = min(1.0, 940 / max(tot, 1))
                f = TEF if sc >= 1 else ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', int(76 * sc), layout_engine=ImageFont.Layout.RAQM)
                if sc < 1:
                    try: f.set_variation_by_name('Black')
                    except Exception: pass
                    ws = [d0.textlength(w, font=f) for w in words]; sp = int(22 * sc); tot = sum(ws) + sp * (len(ws) - 1)
                im = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = W / 2 - tot / 2
                for k, (w, wd) in enumerate(zip(words, ws)):
                    col = (255, 178, 36, 255) if k == act else (244, 241, 234, 255)
                    d.text((x, 100), w, font=f, fill=col, anchor='lm', stroke_width=8, stroke_fill=(0, 0, 0, 220)); x += wd + sp
                TECACHE[key] = surf_from_pil(im)
            sf, _ = TECACHE[key]
            c.set_source_surface(sf, 0, y - 100); c.paint()
            break

# ---------------- images ----------------
def surf_from_pil(im):
    im = im.convert('RGBA'); a = np.array(im); bgra = a[:, :, [2, 1, 0, 3]].copy()
    # premultiply
    al = bgra[:, :, 3:4].astype(np.uint16)
    bgra[:, :, :3] = (bgra[:, :, :3].astype(np.uint16) * al // 255).astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, im.width, im.height)
    return s, bgra

def torn(im, seed=1, top=True, bottom=True, amp=7):
    """paper clipping: white margin, torn top/bottom edges, alpha mask."""
    pad = 26
    base = Image.new('RGB', (im.width + pad * 2, im.height + pad * 2), (250, 249, 245))
    base.paste(im, (pad, pad))
    m = Image.new('L', base.size, 255); d = ImageDraw.Draw(m); rng = np.random.default_rng(seed)
    wdt = base.width
    for edge in (['top'] if top else []) + (['bottom'] if bottom else []):
        pts = []
        for x in range(0, wdt + 8, 8):
            y = rng.uniform(0, amp)
            pts.append((x, y if edge == 'top' else base.height - y))
        poly = ([(0, 0)] + pts + [(wdt, 0)]) if edge == 'top' else ([(0, base.height)] + pts + [(wdt, base.height)])
        d.polygon(poly, fill=0)
    base.putalpha(m)
    return base, pad

CLIPS = {}
def clip(name):
    if name in CLIPS: return CLIPS[name]
    bbc = Image.open(ROOT + 'shot_bbc.jpg').convert('RGB'); hd = Image.open(ROOT + 'shot_heid.jpg').convert('RGB')
    spec = {
        'bbc_head': (bbc, [(250, 198, 540, 236), (88, 684, 450, 842)], []),
        'bbc_q1': (bbc, [(88, 1390, 448, 1456)], [(1, 196, 1411, 432, 1432), (2, 98, 1432, 240, 1453)]),
        'bbc_q2': (bbc, [(88, 1750, 448, 1813)], [(1, 98, 1750, 445, 1771), (2, 98, 1771, 445, 1792), (3, 98, 1792, 252, 1813)]),
        'heid_head': (hd, [(0, 360, 900, 708)], []),
        'heid_q': (hd, [(296, 1640, 896, 1754)], [(1, 758, 1663, 886, 1686), (2, 300, 1686, 886, 1709), (3, 300, 1709, 535, 1732)]),
    }[name]
    src, boxes, hls = spec
    parts = [src.crop(b) for b in boxes]
    wmax = max(p.width for p in parts); hsum = sum(p.height for p in parts) + 18 * (len(parts) - 1)
    im = Image.new('RGB', (wmax, hsum), (250, 249, 245)); y = 0; offs = []
    for p, b in zip(parts, boxes):
        x = (wmax - p.width) // 2; im.paste(p, (x, y)); offs.append((b, x, y)); y += p.height + 18
    paper, pad = torn(im, seed=len(name))
    # highlight rects in paper coords
    rects = []
    for (_, x0, y0, x1, y1) in hls:
        for (b, ox, oy) in offs:
            if b[0] <= x0 <= b[2] and b[1] <= y0 <= b[3]:
                rects.append((x0 - b[0] + ox + pad, y0 - b[1] + oy + pad, x1 - b[0] + ox + pad, y1 - b[1] + oy + pad))
    s = surf_from_pil(paper)
    CLIPS[name] = (s, rects)
    return CLIPS[name]

def draw_clip(c, name, cx, cy, wpx, t, t0, rot=-2.0, hl_t0=None, hl_dur=0.9, a=1.0, guide=True):
    if t < t0: return None
    (sf, _), rects = clip(name)
    u = e_out(prog(t, t0, t0 + 0.4))
    sc = wpx / sf.get_width()
    c.save(); c.translate(cx, cy + (1 - u) * 260); c.rotate(math.radians(rot + (1 - u) * 6)); c.scale(sc, sc)
    w, h = sf.get_width(), sf.get_height()
    c.set_source_rgba(0, 0, 0, 0.45 * u * a); c.rectangle(-w / 2 + 10, -h / 2 + 18, w, h); c.fill()
    c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u * a)
    tip = None
    if hl_t0 is not None and t >= hl_t0:
        n = len(rects); tot = sum(r[2] - r[0] for r in rects); done = prog(t, hl_t0, hl_t0 + hl_dur) * tot
        for (x0, y0, x1, y1) in rects:
            wl = x1 - x0; f = clamp(done / wl); done -= wl
            if f <= 0: break
            xa, xb = -w / 2 + x0 - 3, -w / 2 + x0 + wl * f + 3
            c.set_source_rgba(1.0, 0.70, 0.14, 0.42); c.rectangle(xa, -h / 2 + y0 - 1, xb - xa, y1 - y0 + 2); c.fill()
            if f < 1 or (f >= 1 and done <= 0): tip = c.user_to_device(xb, -h / 2 + (y0 + y1) / 2)
    # tape
    for tx in (-w / 2 + 70, w / 2 - 70):
        c.save(); c.translate(tx, -h / 2 + 4); c.rotate(math.radians(-30 if tx < 0 else 30))
        c.set_source_rgba(0.95, 0.89, 0.70, 0.75 * u); c.rectangle(-55 / sc * 0.6, -14 / sc * 0.6, 110 / sc * 0.6, 28 / sc * 0.6); c.fill(); c.restore()
    c.restore()
    if tip and guide and prog(t, hl_t0, hl_t0 + hl_dur) < 1: glowdot(c, tip[0], tip[1], 10)
    return u

def source_tag(c, txt, x, y, a=1.0):
    font(c, 'mono', 20); e = c.text_extents(txt)
    glass_dark(c, x - 14, y - 22, e.x_advance + 28, 40, 20, a)
    c.move_to(x, y + 6); c.set_source_rgba(*CREAM, a); c.show_text(txt)

PHOTO = {}
def print_photo(c, name, cx, cy, w, t, t0, rot=3, caption=None):
    if t < t0: return
    if name not in PHOTO:
        im = Image.open(ROOT + name).convert('RGB'); im.thumbnail((900, 1200))
        PHOTO[name] = surf_from_pil(im)
    sf, _ = PHOTO[name]; u = e_out(prog(t, t0, t0 + 0.35))
    sw, sh = sf.get_width(), sf.get_height(); sc = w / sw; h = sh * sc
    c.save(); c.translate(cx, cy - (1 - u) * 220); c.rotate(math.radians(rot * u + (1 - u) * 14))
    c.set_source_rgba(0, 0, 0, 0.45 * u); c.rectangle(-w / 2 - 10, -h / 2 - 2, w + 30, h + 90); c.fill()
    c.set_source_rgba(0.97, 0.96, 0.92, u); c.rectangle(-w / 2 - 18, -h / 2 - 18, w + 36, h + 84); c.fill()
    c.save(); c.translate(-w / 2, -h / 2); c.scale(sc, sc); c.set_source_surface(sf, 0, 0); c.paint_with_alpha(u); c.restore()
    if caption: mono(c, caption, 0, h / 2 + 32, 20, (0.25, 0.25, 0.25), a=u, kind='mono')
    c.save(); c.translate(0, -h / 2 - 10); c.set_source_rgba(0.95, 0.89, 0.70, 0.8 * u); c.rectangle(-60, -16, 120, 32); c.fill(); c.restore()
    c.restore()

def thread(c, x0, y0, x1, y1, t, t0, dur=0.6):
    u = e_io(prog(t, t0, t0 + dur))
    if u <= 0: return
    xm, ym = (x0 + x1) / 2, max(y0, y1) + 80
    c.save(); c.set_line_width(4); c.set_source_rgba(*AMBER, 0.85); c.set_line_cap(cairo.LINE_CAP_ROUND)
    # draw bezier partially by sampling
    pts = []
    for i in range(41):
        s = i / 40 * u
        x = (1 - s) ** 2 * x0 + 2 * (1 - s) * s * xm + s * s * x1
        y = (1 - s) ** 2 * y0 + 2 * (1 - s) * s * ym + s * s * y1
        pts.append((x, y))
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
    for p in (pts[0],): glowdot(c, p[0], p[1], 7)
    if u < 1: glowdot(c, pts[-1][0], pts[-1][1], 9)
    else: glowdot(c, pts[-1][0], pts[-1][1], 7)
    c.restore()

# ---------------- drawn objects ----------------
def metal_grad(x0, y0, x1, y1, gold=False, sat=1.0):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    if gold:
        cs = [(0, (0.55, 0.36, 0.05)), (0.35, (1.0, 0.82, 0.35)), (0.5, (1.0, 0.95, 0.65)), (0.7, (0.85, 0.6, 0.12)), (1, (0.45, 0.28, 0.04))]
        if sat < 1:   # drain towards silver
            sil = [(0.45, 0.47, 0.5), (0.85, 0.87, 0.9), (0.98, 0.98, 1), (0.7, 0.72, 0.75), (0.4, 0.42, 0.45)]
            cs = [(p, tuple(a * sat + b * (1 - sat) for a, b in zip(col, s))) for (p, col), s in zip(cs, sil)]
    else:
        cs = [(0, (0.45, 0.47, 0.5)), (0.35, (0.85, 0.87, 0.9)), (0.5, (0.98, 0.98, 1)), (0.7, (0.7, 0.72, 0.75)), (1, (0.4, 0.42, 0.45))]
    for p, col in cs: g.add_color_stop_rgb(p, *col)
    return g
def key_shape(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.arc(-70, 0, 46, 0, 2 * math.pi); c.new_sub_path(); c.arc(-70, 0, 18, 0, 2 * math.pi)
    c.rectangle(-28, -12, 150, 24); c.rectangle(80, 12, 16, 22); c.rectangle(104, 12, 12, 16)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.set_source(metal_grad(-120, -50, 130, 50)); c.paint_with_alpha(0) if a <= 0 else None
    c.save(); c.clip_preserve(); c.paint_with_alpha(a); c.restore(); c.new_path(); c.restore()
def spoon_shape(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1, 1.35); c.arc(0, -60, 44, 0, 2 * math.pi); c.restore()
    c.rectangle(-9, -30, 18, 170); c.save(); c.translate(0, 150); c.scale(1, 1.4); c.arc(0, 0, 14, 0, 2 * math.pi); c.restore()
    c.set_source(metal_grad(-50, -140, 50, 170)); c.save(); c.clip(); c.paint_with_alpha(a); c.restore(); c.restore()
def phone_shape(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -55, -110, 110, 220, 22); c.set_source(metal_grad(-60, -110, 60, 110)); c.save(); c.clip(); c.paint_with_alpha(a); c.restore()
    rrect(c, -46, -100, 92, 200, 16); c.set_source_rgba(0.07, 0.08, 0.1, a); c.fill(); c.restore()
def gold_bar(c, x, y, s, sat=1.0, a=1.0, glow=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 420); g.add_color_stop_rgba(0, *AMBER, 0.35 * glow * sat * a); g.add_color_stop_rgba(1, *AMBER, 0)
        c.set_source(g); c.arc(0, 0, 420, 0, 2 * math.pi); c.fill()
    # top face
    c.move_to(-200, -40); c.line_to(-150, -110); c.line_to(150, -110); c.line_to(200, -40); c.close_path()
    c.set_source(metal_grad(-200, -110, 200, -40, True, sat)); c.save(); c.clip(); c.paint_with_alpha(a); c.restore()
    # front face
    c.move_to(-200, -40); c.line_to(200, -40); c.line_to(220, 60); c.line_to(-220, 60); c.close_path()
    c.set_source(metal_grad(-220, -40, 220, 60, True, sat * 0.9 if sat < 1 else 0.9)); c.save(); c.clip(); c.paint_with_alpha(a)
    c.set_source_rgba(0, 0, 0, 0.18 * a); c.paint(); c.restore()
    c.restore()

def atom(c, cx, cy, r, t, shrink=0.0, heavy=0.0, a=1.0):
    c.save(); c.translate(cx, cy)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 90); g.add_color_stop_rgba(0, *AMBER, 0.95 * a); g.add_color_stop_rgba(1, *AMBER2, 0.0)
    c.set_source(g); c.arc(0, 0, 90, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, a); c.arc(0, 0, 54, 0, 2 * math.pi); c.fill()
    font(c, 'head', 46); e = c.text_extents('79'); c.move_to(-e.width / 2 - e.x_bearing, 16); c.set_source_rgba(*INK, a); c.show_text('79')
    for k, (rx, ry, rot, sp) in enumerate([(r * 0.42, r * 0.42, 0, 3.2), (r * 0.7, r * 0.32, 25, 1.6), (r * 0.95, r * 0.4, -35, 1.0)]):
        f = 1 - shrink * (0.25 if k == 0 else 0.08)
        c.save(); c.rotate(math.radians(rot)); c.scale(rx * f, ry * f)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*CREAM, 0.25 * a); c.set_line_width(2); c.stroke()
        ang = t * sp * (1 + (1.6 if k == 0 else 0)) + k
        x = math.cos(ang) * rx * f; y = math.sin(ang) * ry * f
        xr = x * math.cos(math.radians(rot)) - y * math.sin(math.radians(rot)); yr = x * math.sin(math.radians(rot)) + y * math.cos(math.radians(rot))
        rr = 10 + (8 * heavy if k == 0 else 0)
        if k == 0: glowdot(c, xr, yr, rr, a)
        else: c.set_source_rgba(*CREAM, 0.9 * a); c.arc(xr, yr, 8, 0, 2 * math.pi); c.fill()
    c.restore()

SPEC = [(0.0, (0.55, 0.2, 0.85)), (0.18, (0.2, 0.35, 1.0)), (0.32, (0.1, 0.75, 0.95)), (0.48, (0.2, 0.85, 0.3)), (0.62, (1.0, 0.92, 0.15)), (0.78, (1.0, 0.55, 0.1)), (1.0, (0.95, 0.15, 0.1))]
def spectrum(c, x, y, w, h, cut=0.0, a=1.0, label=None):
    """cut: 0..1 how much of the blue band (0.1-0.38) is pulled out."""
    g = cairo.LinearGradient(x, 0, x + w, 0)
    for p, col in SPEC: g.add_color_stop_rgba(p, *col, a)
    rrect(c, x, y, w, h, h / 2); c.set_source(g); c.fill()
    if cut > 0:
        bx0, bx1 = x + w * 0.1, x + w * 0.38
        c.set_source_rgba(0.04, 0.04, 0.05, a); c.rectangle(bx0, y - 2, (bx1 - bx0), h + 4); c.fill()
        # the pulled-out piece floats up
        c.save(); c.translate(0, -cut * 140)
        g2 = cairo.LinearGradient(bx0, 0, bx1, 0)
        for p, col in SPEC[1:4]: g2.add_color_stop_rgba((p - 0.1) / 0.28, *col, a * (1 - 0.5 * cut))
        rrect(c, bx0, y, bx1 - bx0, h, 10); c.set_source(g2); c.fill(); c.restore()

def toggle(c, cx, cy, on, a=1.0):
    w, h = 300, 120
    glass_dark(c, cx - w / 2 - 170, cy - h / 2 - 10, w + 360, h + 20, 70, a)
    mono(c, 'RELATIVITY', cx - 300, cy, 30, CREAM, a=a, anchor='l')
    x0 = cx + 30; rrect(c, x0, cy - 40, 160, 80, 40)
    if on > 0.5: c.set_source(agrad(x0, 0, x0 + 160, 0))
    else: c.set_source_rgba(0.3, 0.3, 0.33, a)
    c.fill()
    kx = x0 + 40 + 80 * on
    c.set_source_rgba(*CREAM, a); c.arc(kx, cy, 32, 0, 2 * math.pi); c.fill()
    mono(c, 'ON' if on > 0.5 else 'OFF', x0 + 200, cy, 28, AMBER if on > 0.5 else (0.6, 0.6, 0.6), a=a, anchor='l')

def droplets(c, x, y, t, a=1.0):
    rng = np.random.default_rng(5)
    for i in range(9):
        dx, dy, r = rng.uniform(-260, 260), rng.uniform(-60, 60), rng.uniform(18, 64)
        xx = x + dx + 6 * math.sin(t * 1.3 + i); yy = y + dy
        g = cairo.RadialGradient(xx - r * 0.35, yy - r * 0.45, r * 0.05, xx, yy, r)
        g.add_color_stop_rgba(0, 1, 1, 1, a); g.add_color_stop_rgba(0.35, 0.78, 0.8, 0.84, a); g.add_color_stop_rgba(1, 0.25, 0.27, 0.3, a)
        c.save(); c.translate(xx, yy); c.scale(1, 0.72); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.set_source(g); c.fill()

def board_bg(c, t):
    c.set_source_rgb(0.045, 0.045, 0.055); c.paint()
    g = cairo.RadialGradient(W / 2, 700, 0, W / 2, 700, 1100); g.add_color_stop_rgba(0, *AMBER, 0.07); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.paint()
    c.set_source_rgba(1, 1, 1, 0.035); c.set_line_width(1)
    for x in range(0, W, 60): c.move_to(x, 0); c.line_to(x, H)
    for y in range(0, H, 60): c.move_to(0, y); c.line_to(W, y)
    c.stroke(); K.grain(c)

TAGTE = None
def tag(c):
    global TAGTE
    if LANGV == 'te':
        if TAGTE is None:
            f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 26, layout_engine=ImageFont.Layout.RAQM)
            try: f.set_variation_by_name('Bold')
            except Exception: pass
            im = Image.new('RGBA', (300, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 30), 'గోల్డ్ · 3/6', font=f, fill=(244, 241, 234, 255), anchor='lm')
            TAGTE = surf_from_pil(im)
        glass_dark(c, 40, 92, 230, 54, 27); glowdot(c, 68, 119, 7)
        c.set_source_surface(TAGTE[0], 88, 89); c.paint(); return
    font(c, 'monob', 24); txt = 'GOLD · 3/6'; e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7)
    c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)

def ai_label(c, txt='ILLUSTRATION'):
    mono(c, txt, W - 150, 1250, 18, (1, 1, 1), a=0.6, anchor='r', kind='mono')

def draw_vid(c, name, t, t0, label=None, dim=0.15):
    n = len(os.listdir(ROOT + 'vid/' + name)); i = max(1, min(n, int((t - t0) * FPS) + 1))
    sf, _ = surf_from_pil(Image.open(f'{ROOT}vid/{name}/f_{i:04d}.jpg'))
    z = 1.0 + 0.05 * prog(t, t0, t0 + 3)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2); c.set_source_surface(sf, 0, 0); c.paint(); c.restore()
    if dim: c.set_source_rgba(0, 0, 0, dim); c.paint()
    g = cairo.LinearGradient(0, 1150, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75); c.set_source(g); c.paint()
    if label: mono(c, label, W - 150, 1250, 18, (1, 1, 1), a=0.7, anchor='r', kind='mono')

# ---------------- frame ----------------
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    # 1-3: metals -> gold
    if t < A['keys'] - 0.05:
        draw_vid(c, 'cut', t, 0, 'Kmeel.com Videos · Pexels')
    elif A['gold1'] <= t < A['thought'] - 0.05:
        draw_vid(c, 'ring', t, A['gold1'], 'Tima Miroshnichenko · Pexels', dim=0.05)
        pill(c, 'THE ONLY YELLOW ONE', W / 2, 1180, 40, AMBER, s=e_back(prog(t, A['gold1'] + 0.2, A['gold1'] + 0.45)))
    elif t < A['turns'] - 0.05:
        fade = 1 - 0.75 * prog(t, A['gold1'] - 0.1, A['gold1'] + 0.3)
        for (fn, x, t0, sc) in ((key_shape, 230, A['keys'], 1.55), (spoon_shape, 560, A['spoons'], 1.7), (phone_shape, 860, A['phone'], 1.7)):
            u = e_back(prog(t, t0, t0 + 0.3))
            if u > 0:
                yy = 700 - 160 * prog(t, A['gold1'] - 0.1, A['gold1'] + 0.4)
                fn(c, x, yy, sc * u, a=fade)
        if t < A['gold1']:
            if t >= A['silver1']:
                pill(c, 'SILVER · GREY · SILVER', W / 2, 1060, 38, CREAM, s=e_back(prog(t, A['silver1'], A['silver1'] + 0.25)))
        else:
            u = e_back(prog(t, A['gold1'], A['gold1'] + 0.35))
            gold_bar(c, W / 2, 1000 - 40 * prog(t, A['thought'], A['turns']), 1.5 * u, glow=1.0)
            if t >= A['yellow'] - 0.05:
                pill(c, 'THE ONLY YELLOW ONE', W / 2, 1210, 36, AMBER, s=e_back(prog(t, A['yellow'] - 0.05, A['yellow'] + 0.25)))
    # 4: Einstein
    elif t < A['atom'] - 0.1:
        gold_bar(c, 820, 1060, 0.6, glow=0.6, a=0.9)
        print_photo(c, 'einstein.jpg', 430, 640, 520, t, A['einstein'] - 0.25, rot=-3, caption='ALBERT EINSTEIN · ORREN JACK TURNER, 1947')
        if t >= A['einstein'] + 0.1:
            thread(c, 640, 1020, 760, 1000, t, A['einstein'] + 0.1)
    # 5: atom + BBC clipping with highlight
    elif t < A['at'] - 0.05:
        atom(c, W / 2, 560, 380, t, a=1.0 if t < A['some'] else 0.35)
        if t >= A['n79']: mono(c, '79 PROTONS', W / 2, 840, 30, AMBER, a=prog(t, A['n79'], A['n79'] + 0.3), kind='monob')
        if t >= A['some'] - 0.3:
            draw_clip(c, 'bbc_head', W / 2 - 40, 450, 820, t, A['some'] - 0.3, rot=-2.5)
            draw_clip(c, 'bbc_q1', W / 2 + 20, 880, 980, t, A['some'] - 0.05, rot=1.5, hl_t0=A['over'] - 0.15, hl_dur=1.0)
            if t >= A['some'] + 0.3: source_tag(c, 'BBC SCIENCE FOCUS · DR MARK LORCH', 120, 1110, a=prog(t, A['some'] + 0.3, A['some'] + 0.6))
    # 6: relativity -> heavier, closer
    elif t < A['changes'] - 0.1:
        sh = e_io(prog(t, A['closer'] - 0.2, A['closer'] + 0.4)); hv = e_io(prog(t, A['heavier'] - 0.1, A['heavier'] + 0.4))
        atom(c, W / 2, 700, 520, t, shrink=sh, heavy=hv)
        if t >= A['relativity'] - 0.1:
            pill(c, 'RELATIVITY', W / 2, 300, 46, AMBER, s=e_back(prog(t, A['relativity'] - 0.1, A['relativity'] + 0.2)))
        if t >= A['heavier']: pill(c, 'HEAVIER', 260, 1120, 34, CREAM, s=e_back(prog(t, A['heavier'], A['heavier'] + 0.25)))
        if t >= A['closer']: pill(c, 'PULLED CLOSER', 760, 1120, 34, CREAM, s=e_back(prog(t, A['closer'], A['closer'] + 0.25)))
    # 7: light: white -> minus blue -> yellow; BBC quote 2
    elif t < A['silver2'] - 0.05:
        u = prog(t, A['blue1'] - 0.1, A['blue1'] + 0.5)
        gold_bar(c, W / 2, 870, 0.75, glow=0.7)
        spectrum(c, 140, 420, 800, 90, cut=e_io(u))
        mono(c, 'WHITE LIGHT', 140, 380, 24, CREAM, anchor='l', kind='monob')
        if t >= A['blue1']: mono(c, 'BLUE · ABSORBED', 140 + 800 * 0.24, 250, 26, (0.55, 0.75, 1.0), a=prog(t, A['blue1'], A['blue1'] + 0.3), kind='monob')
        if t >= A['minus']:
            uy = e_out(prog(t, A['minus'], A['minus'] + 0.6))
            g = cairo.LinearGradient(140, 0, 940, 0); g.add_color_stop_rgba(0, 1.0, 0.86, 0.45, uy); g.add_color_stop_rgba(1, 1.0, 0.72, 0.25, uy)
            rrect(c, 140, 600, 800, 90, 45); c.set_source(g); c.fill()
            mono(c, '= WARM YELLOW', W / 2, 740, 30, AMBER, a=uy, kind='monob')
        if t >= A['soaks'] - 0.2:
            draw_clip(c, 'bbc_q2', W / 2, 1180 if t < A['minus'] else 1180, 900, t, A['swallows'] - 0.1, rot=-1.5, hl_t0=A['blue1'] - 0.05, hl_dur=2.2, a=1.0)
    # 8: silver bounces everything (UV is invisible)
    elif t < A['silver2'] + 1.4:
        draw_vid(c, 'jew', t, A['silver2'] - 0.05, 'cottonbro studio · Pexels')
        pill(c, 'SILVER: SAME SETUP', W / 2, 1180, 38, CREAM, s=e_back(prog(t, A['silver2'], A['silver2'] + 0.25)))
    elif t < A['which'] - 0.05:
        spectrum(c, 230, 520, 700, 80)
        mono(c, 'VISIBLE LIGHT', 230, 480, 24, CREAM, anchor='l', kind='monob')
        c.set_source_rgba(0.5, 0.35, 0.95, 0.35); c.set_dash([8, 10]); c.set_line_width(3); rrect(c, 50, 520, 170, 80, 40); c.stroke(); c.set_dash([])
        mono(c, 'ULTRAVIOLET', 135, 640, 22, (0.7, 0.6, 1.0), kind='monob'); mono(c, "CAN'T SEE IT", 135, 672, 20, (0.7, 0.6, 1.0), kind='mono')
        if t >= A['see'] - 0.2:
            glowdot(c, 135, 560, 12)
        # silver mirror bar reflects everything
        c.save(); c.translate(W / 2, 980)
        rrect(c, -330, -70, 660, 140, 30); c.set_source(metal_grad(-330, -70, 330, 70)); c.fill(); c.restore()
        mono(c, 'SILVER', W / 2, 980, 40, INK, kind='monob')
        if t >= A['bounces']:
            u = e_out(prog(t, A['bounces'], A['bounces'] + 0.5))
            for k in range(7):
                col = SPEC[k][1]; ang = math.radians(-60 - k * 10)
                c.set_source_rgba(*col, 0.85 * u); c.set_line_width(8)
                c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(14); c.move_to(W / 2 - 150 + k * 50, 900); c.line_to(W / 2 - 150 + k * 50 + math.cos(ang) * 300 * u, 900 + math.sin(ang) * 300 * u); c.stroke()
            mono(c, 'BOUNCES BACK EVERYTHING', W / 2, 1150, 28, CREAM, a=u, kind='monob')
    # 9: toggle relativity OFF -> gold drains to silver -> ON again
    elif t < A['notjust'] - 0.1:
        off = prog(t, A['without'] - 0.05, A['without'] + 0.2)
        back = prog(t, A['silver3'] + 0.7, A['silver3'] + 0.95)
        on = 1 - off + back
        sat = 1 - e_io(prog(t, A['without'] + 0.2, A['silver3'] + 0.1)) + e_io(back)
        gold_bar(c, W / 2, 900, 1.6, sat=clamp(sat), glow=clamp(sat))
        toggle(c, W / 2, 420, clamp(on))
        if t >= A['silver3'] - 0.05 and back <= 0:
            pill(c, 'GOLD WOULD LOOK LIKE THIS', W / 2, 1180, 36, CREAM, s=e_back(prog(t, A['silver3'] - 0.05, A['silver3'] + 0.2)))
    # 10: mercury — Heidelberg clipping
    elif t < A['full'] - 0.1:
        draw_clip(c, 'heid_head', W / 2, 400, 980, t, A['y2013'] - 0.2, rot=-1.5)
        draw_clip(c, 'heid_q', W / 2 + 10, 780, 1000, t, A['mercury'] - 0.1, rot=1.2, hl_t0=A['without2'] - 0.1, hl_dur=2.0)
        if t >= A['mercury'] + 0.2:
            source_tag(c, 'HEIDELBERG UNIVERSITY · PRESS RELEASE 195/2013', 90, 960, a=prog(t, A['mercury'] + 0.2, A['mercury'] + 0.5))
        if t >= A['liquid'] - 0.1:
            droplets(c, W / 2 - 170, 1150, t, a=prog(t, A['liquid'] - 0.1, A['liquid'] + 0.3))
        if t >= A['n105']:
            u = e_back(prog(t, A['n105'], A['n105'] + 0.3))
            c.save(); c.translate(W - 230, 1150); c.scale(u, u)
            font(c, 'head', 120); e = c.text_extents('+105°C'); c.move_to(-e.width / 2 - e.x_bearing, 42); c.text_path('+105°C')
            c.set_source_rgba(0, 0, 0, 0.8); c.set_line_width(14); c.stroke_preserve(); c.set_source(agrad(-e.width / 2, 0, e.width / 2, 0)); c.fill(); c.restore()
    # 11: CTA — the board zooms out: every piece of evidence, connected
    else:
        u = e_out(prog(t, A['full'] - 0.1, A['full'] + 0.6))
        print_photo(c, 'einstein.jpg', 250, 470, 260, t, A['full'] - 0.1, rot=-4)
        draw_clip(c, 'bbc_head', 760, 380, 500, t, A['full'], rot=3)
        draw_clip(c, 'heid_head', 720, 760, 560, t, A['full'] + 0.15, rot=-2)
        gold_bar(c, 280, 900, 0.55, glow=0.6)
        thread(c, 380, 520, 560, 400, t, A['full'] + 0.3, 0.5)
        thread(c, 760, 470, 720, 660, t, A['full'] + 0.5, 0.5)
        thread(c, 340, 900, 470, 800, t, A['full'] + 0.7, 0.5)
        if t >= A['comment'] - 0.1:
            u2 = e_back(prog(t, A['comment'] - 0.1, A['comment'] + 0.2))
            c.save(); c.translate(W / 2, 1110); c.scale(u2, u2)
            glass_dark(c, -400, -90, 800, 180, 40)
            head(c, 'GOT A WHY?', 0, -26, 60, CREAM, shadow=False)
            mono(c, 'COMMENT IT · WE FIND THE ANSWER', 0, 42, 24, AMBER, kind='monob'); c.restore()
    (K.captions(c, t, y=1400) if LANGV == 'en' else te_captions(c, t, y=1400))
    tag(c)
    return s

def main(part=0, parts=1, out=None, still=None):
    if still is not None:
        os.makedirs(ROOT + 'stills', exist_ok=True)
        for tt in still: frame(tt).write_to_png(f'{ROOT}stills/f_{tt:05.2f}.png')
        return
    n = int(DUR * FPS); a = n * part // parts; b = n * (part + 1) // parts
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        s = frame(i / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'still': main(still=[float(x) for x in sys.argv[2:]])
    else: main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
