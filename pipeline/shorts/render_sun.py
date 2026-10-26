# Ravana Short (9:16, full-screen, v3 style). usage: python3 render_rv.py en|te OUTDIR [stills t,...] | [part i n]
import sys, os, subprocess, functools, math
sys.path.insert(0, '/home/claude/elnino')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import load_wav, SR, FPS, whoosh, boom
import modern
from modern import *
modern.CLIPD = '/home/claude/sun/clipf/'

LANG = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TE = LANG == 'te'; W, H = 1080, 1920
voice = load_wav(f'/home/claude/sun/voice_{LANG}_' + os.environ.get('PLAT', 'yt') + '.wav'); VLEN = len(voice) / SR
LEAD = 0.15; TAIL = 0.7; TOTAL = LEAD + VLEN + TAIL
IMG = '/home/claude/sun/media/'
from cues_sun import get_cues
SC, EV = get_cues(LANG)
SUB_T = 29.8 if not TE else 32.1
FULLV_T = 36.4 if not TE else 38.6
SERIES = 'DUSSEHRA SERIES · FINAL PART' if not TE else 'దసరా సిరీస్ · చివరి పార్ట్'          # scenes, timed overlay events
BRAND = 'WHY? తెలుగు' if TE else 'WHY?'
PLAT = os.environ.get('PLAT', 'yt')
BTN = ('FOLLOW', 'FOLLOWING') if PLAT == 'ig' else ('SUBSCRIBE', 'SUBSCRIBED')
from caps import words, chunks
CH = chunks(words(LANG), maxw=3 if not TE else 2, maxc=18 if not TE else 22)
CH[0] = (0.0,) + tuple(CH[0][1:])
DIMK = 0.5

# ---------- full-screen stills ----------
@functools.lru_cache(12)
def _src(name):
    return Image.open(IMG + name).convert('RGB')

@functools.lru_cache(12)
def _blurfill(name):
    s = _src(name); sc = max(W / s.width, H / s.height)
    b = s.resize((int(s.width * sc) + 2, int(s.height * sc) + 2), Image.BILINEAR)
    x0 = (b.width - W) // 2; y0 = (b.height - H) // 2
    b = b.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(40))
    return Image.blend(b, Image.new('RGB', (W, H), (0, 0, 0)), .45).convert('RGBA')

def still_bg(img, name, v, t0, t1, dim=.35, focus=(.5, .5), zoom=(1.0, 1.08), fit=None):
    """fit=None: cover full frame. fit=(w,h,cy): blurred fill + sharp crop of that box"""
    s = _src(name); u = e_io(prog(v, t0, t1 + .5)); z = zoom[0] + (zoom[1] - zoom[0]) * u
    if fit is None:
        bw, bh, cy = W, H, H / 2
    else:
        img.paste(_blurfill(name), (0, 0)); bw, bh, cy = fit
    sc = max(bw / s.width, bh / s.height) * z; cw, ch = bw / sc, bh / sc
    x0 = (s.width - cw) * focus[0]; y0 = (s.height - ch) * focus[1]
    im = s.resize((bw, bh), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert('RGBA')
    img.alpha_composite(im, (0, int(cy - bh / 2)))
    if dim: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * dim))))

@functools.lru_cache(2)
def _vign():
    g = np.zeros((H, W, 4), np.uint8)
    y = np.linspace(0, 1, H)
    a = np.clip((y - .5) / .5, 0, 1) ** 1.4 * 215 + np.clip((.2 - y) / .2, 0, 1) ** 2 * 150
    g[..., 3] = a[:, None].astype(np.uint8); return Image.fromarray(g, 'RGBA')

def background(img, b, v, t0, t1):
    kind = b[0]
    if kind == 'clip':
        video_bg(img, b[1], v, t0, t1, dim=(b[2] if len(b) > 2 else .4) * DIMK, grad=False, zoom=(1.0, 1.08))
    elif kind == 'img':
        still_bg(img, b[1], v, t0, t1, dim=(b[2] if len(b) > 2 else .35) * DIMK, focus=b[3] if len(b) > 3 else (.5, .5),
                 fit=b[4] if len(b) > 4 else None)
    elif kind == 'black':
        pass
    elif kind == 'grid':
        for q, cid in enumerate(b[1]):
            fr = clip_frame(cid, v - t0 + q * .4, W // 2, H // 2, 1.0, (1.0, 1.06), prog(v, t0, t1))
            alpha_paste(img, fr, (q % 2) * W // 2, (q // 2) * H // 2, 1.0)
        img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * b[2] * DIMK))))
        if len(b) > 3:
            for q, lab in enumerate(b[3]): pill(img, lab, (q % 2) * W // 2 + W // 4, (q // 2) * H // 2 + (300 if q < 2 else 700), 34, AMBER, (10, 10, 10), 1.0)
        d = ImageDraw.Draw(img); d.line((W // 2, 0, W // 2, H), fill=(10, 10, 10, 255), width=8); d.line((0, H // 2, W, H // 2), fill=(10, 10, 10, 255), width=8)
    img.alpha_composite(_vign())

# ---------- overlays ----------
def tag(img, text, x, y, a=1.0, px=24, fill=(10, 10, 10, 190), col=CREAM):
    """small mono label with dark backing (AI ILLUSTRATION / credits / sources)"""
    if a <= 0: return
    f = mono_font(text, px); w = f.getlength(text) + (len(text) * 2 if not is_te(text) else 0) + 36; h = px * 1.9
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=fill)
    alpha_paste(img, im, x, y, a); mono(img, text, x + 18, y + h / 2, px, col, a, anchor='l', track=2)

def credit(img, text, a=1.0):
    f = mono_font(text, 19); w = f.getlength(text) + len(text) * 1 + 28
    tag(img, text, (W - w) / 2, H - 92, a * .95, px=19, col=(200, 196, 188))

def place_header(img, v, t0, num, name, state, a=1.0):
    k = e_out(prog(v, t0, t0 + .45))
    if k <= 0: return
    mono(img, f'PLACE {num}/06' if not TE else f'ప్రాంతం {num}/06', W / 2, 360, 30, AMBER, k * a)
    text_plain(img, name, W / 2, 470 + 40 * (1 - k), 150 if not is_te(name) else 128, CREAM, k * a)
    pill(img, state, W / 2, 610 + 30 * (1 - k), 38, AMBER, (10, 10, 10), prog(v, t0 + .25, t0 + .6) * a)

def source_line(img, text, a=1.0):
    tag(img, ('SOURCE · ' if not TE else 'ఆధారం · ') + text, 60, H - 210, a, px=22, fill=(10, 10, 10, 200), col=AMBER)

def strike_list(img, v, items, y0, gap=170):
    for i, (txt, ti) in enumerate(items):
        if v < ti: continue
        a = prog(v, ti, ti + .25); y = y0 + i * gap
        w = text_plain(img, txt, W / 2, y + 30 * (1 - e_out(a)), 78 if not is_te(txt) else 70, CREAM, a)
        sk = e_io(prog(v, ti + .35, ti + .7))
        if sk > 0:
            d = ImageDraw.Draw(img); x0 = W / 2 - w / 2 - 20
            d.rounded_rectangle((x0, y - 7, x0 + (w + 40) * sk, y + 9), radius=6, fill=RED + (255,))

def chips(img, v, items, y0, gap=150, px=60):
    for i, (txt, ti) in enumerate(items):
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .4)); y = y0 + i * gap
        f = head_font(txt, px); b = f.getbbox(txt); w = b[2] - b[0] + 120; h = px * 1.9
        im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=(12, 12, 12, 225), outline=AMBER + (255,), width=4)
        d.ellipse((30, h / 2 - 12, 54, h / 2 + 12), fill=AMBER + (255,))
        d.text((80 - b[0], (h - (b[3] - b[1])) / 2 - b[1]), txt, font=f, fill=CREAM)
        paste_c(img, im, W / 2 - 80 * (1 - k), y, k)

def calendar(img, v, t0, lab):
    """365-day grid, all dim, one day (Dasara) lights up"""
    if v < t0: return
    cols, rows = 21, 18; cs = 46; gx = (W - cols * cs) / 2; gy = 690
    d = ImageDraw.Draw(img); k = prog(v, t0, t0 + 1.0)
    hit = 8 * cols + 13
    for i in range(365):
        r, c = divmod(i, cols)
        if i / 365 > k: break
        x = gx + c * cs; y = gy + r * cs
        d.rounded_rectangle((x + 4, y + 4, x + cs - 4, y + cs - 4), radius=6, fill=(60, 60, 62, 230))
        if i == hit:
            lk = prog(v, t0 + 1.1, t0 + 1.4)
            if lk > 0:
                g = 8 + 10 * (0.5 + 0.5 * math.sin(v * 6))
                d.rounded_rectangle((x + 4 - g * lk, y + 4 - g * lk, x + cs - 4 + g * lk, y + cs - 4 + g * lk), radius=10, fill=AMBER + (int(255 * lk),))
    a = prog(v, t0 + 1.3, t0 + 1.7)
    text_plain(img, lab, W / 2, gy + rows * cs + 90, 66 if not TE else 60, AMBER, a)

def recap(img, v, t0, names):
    for i, (n, s) in enumerate(names):
        ti = t0 + .2 + i * .22
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .4)); y = 520 + i * 200
        d = ImageDraw.Draw(img)
        d.ellipse((90, y - 42, 174, y + 42), fill=AMBER + (int(255 * k),))
        text_plain(img, str(i + 1), 132, y, 48, (10, 10, 10), k)
        text_plain(img, n, 214 + 40 * (1 - k), y - 18, 64 if not is_te(n) else 58, CREAM, k, anchor='l')
        mono(img, s, 216 + 40 * (1 - k), y + 40, 24, GREY, k, anchor='l', track=2)

def stack_words(img, v, items, y0, gap=190, px=120):
    for i, (txt, ti, col) in enumerate(items):
        if v < ti: continue
        k = e_out(prog(v, ti, ti + .3))
        text_plain(img, txt, W / 2, y0 + i * gap + 30 * (1 - k), px if not is_te(txt) else int(px * .8), col, k)

def big35(img, v, t0, sub):
    if v < t0: return
    k = e_out(prog(v, t0, t0 + .9)); n = int(round(35 * k))
    text_plain(img, f'{n}', W / 2 - 60, 900, 420, AMBER, prog(v, t0, t0 + .2))
    text_plain(img, 'FT' if not TE else 'అడుగులు', W / 2 + (250 if not TE else 300), 1010, 110 if not TE else 70, CREAM, prog(v, t0 + .3, t0 + .6))
    text_plain(img, sub, W / 2, 1200, 56 if not TE else 50, CREAM, prog(v, t0 + .5, t0 + .9))
    # height bar
    d = ImageDraw.Draw(img); hb = 520 * k
    d.rounded_rectangle((110, 1130 - hb, 140, 1130), radius=8, fill=AMBER + (255,))


# ---------- subscribe button ----------
def bell(d, cx, cy, r, col, ring=0.0):
    a = math.sin(ring * 30) * 18 * max(0, 1 - ring * 2)
    import math as _m
    pts = []
    for t in range(0, 181, 10):
        ang = _m.radians(180 + t); pts.append((cx + r * .62 * _m.cos(ang), cy - r * .15 + r * .7 * _m.sin(ang)))
    pts += [(cx + r * .75, cy + r * .55), (cx - r * .75, cy + r * .55)]
    d.polygon(pts, fill=col); d.ellipse((cx - r * .18, cy + r * .55, cx + r * .18, cy + r * .85), fill=col)

def sub_button(img, v, t_in, cx, cy, s=1.0, tap=0.9, label_te=False):
    if v < t_in: return
    k = e_back(prog(v, t_in, t_in + .4)); a = prog(v, t_in, t_in + .2)
    pressed = v >= t_in + tap
    dip = .9 if t_in + tap <= v < t_in + tap + .12 else 1.0
    txt = BTN[1] if pressed else BTN[0]
    f = font('archivo', int(46 * s)); tw = f.getlength(txt); h = int(104 * s); w = int(tw + 150 * s)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(70, 70, 72, 255) if pressed else (230, 30, 30, 255))
    bell(d, 62 * s, h / 2, 30 * s, CREAM + (255,), ring=(v - t_in - tap) if pressed else 0)
    d.text((110 * s, h / 2), txt, font=f, fill=CREAM, anchor='lm')
    paste_c(img, im, cx, cy, a, k * dip)
    rp = prog(v, t_in + tap - .05, t_in + tap + .45)
    if 0 < rp < 1:
        g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g); R = 30 + 90 * rp
        tx, ty = cx + w * s * .25, cy + 10
        gd.ellipse((tx - R, ty - R, tx + R, ty + R), outline=(255, 255, 255, int(220 * (1 - rp))), width=6)
        gd.ellipse((tx - 22, ty - 22, tx + 22, ty + 22), fill=(255, 255, 255, int(200 * (1 - rp))))
        img.alpha_composite(g)

def sub_pop(img, v, t0, dur=3.6):
    if not (t0 <= v < t0 + dur): return
    a = prog(v, t0, t0 + .25) * (1 - prog(v, t0 + dur - .3, t0 + dur))
    k = e_out(prog(v, t0, t0 + .35)); y = 150 + 110 * k
    sub_button(img, v, t0, W / 2, y, .8, tap=1.4)
    mono(img, 'A NEW WHY EVERY DAY' if not TE else 'రోజూ ఒక కొత్త "ఎందుకు"', W / 2, y + 80, 26 if not TE else 28, CREAM, a)

# ---------- word captions ----------
@functools.lru_cache(2)
def _capband():
    g = np.zeros((H, W, 4), np.uint8); y = np.arange(H)[:, None]
    a = np.exp(-((y - CAP_Y) / 230.0) ** 2) * 150
    g[..., 3] = a.astype(np.uint8); return Image.fromarray(g, 'RGBA')
CAP_Y = 1250
def caption(img, v):
    cur = None
    for c in CH:
        if c[0] - .05 <= v < c[1]: cur = c
    img.alpha_composite(_capband())
    if not cur: return
    s0, e0, ws = cur; px = 82 if not TE else 76
    f = font('archivo', px) if not TE else font('tesans', px)
    toks = [x[2].upper() if not TE else x[2] for x in ws]
    sp = f.getlength(' '); wid = [f.getlength(t) for t in toks]; tot = sum(wid) + sp * (len(toks) - 1)
    lines = [list(range(len(toks)))]
    if tot > 960:
        cut = len(toks) // 2 + (len(toks) % 2); lines = [list(range(cut)), list(range(cut, len(toks)))]
    k = e_back(prog(v, s0 - .05, s0 + .12))
    for li, ln in enumerate(lines):
        lw = sum(wid[i] for i in ln) + sp * (len(ln) - 1); x = W / 2 - lw / 2
        y = CAP_Y + (li - (len(lines) - 1) / 2) * px * 1.25
        for i in ln:
            active = ws[i][0] - .03 <= v < (ws[i + 1][0] if i + 1 < len(ws) else e0)
            said = v >= ws[i][0] - .03
            col = AMBER if active else (CREAM if said else (200, 196, 188))
            sc = (1.08 if active else 1.0) * (.85 + .15 * k)
            im = Image.new('RGBA', (int(wid[i] + 40), int(px * 1.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.text((20, px * .9), toks[i], font=f, fill=col, anchor='lm', stroke_width=7, stroke_fill=(0, 0, 0))
            paste_c(img, im, x + wid[i] / 2, y, 1.0, sc)
            x += wid[i] + sp

# ---------- frame ----------
def scene_at(v):
    idx = 0
    for i, s in enumerate(SC):
        if v >= s['t'] - 1e-6: idx = i
    s = SC[idx]; t1 = SC[idx + 1]['t'] if idx + 1 < len(SC) else VLEN + TAIL
    return idx, s, t1

def frame_at(T):
    v = T - LEAD
    idx, s, t1 = scene_at(v); t0 = s['t']
    img = bg(W, H).convert('RGBA') if True else None
    background(img, s['bg'], v, t0, t1)
    if t1 - t0 > 2.6 and s['bg'][0] != 'black':
        pk = e_out(prog(v, t0 + (t1 - t0) * .5, t0 + (t1 - t0) * .5 + .12))
        if pk > 0:
            z = 1 + .07 * pk; cw, ch = W / z, H / z
            img = img.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
    k = s['kind']
    if k == 'head' and False:
        headline(img, s['text'], v, t0 + s.get('d', .05), W / 2, s.get('y', 1180), s.get('px', 96 if not TE else 92), 960, hl=s.get('hl', ()))
        if 'sub' in s:
            headline(img, s['sub'], v, s['sub_t'], W / 2, s.get('sub_y', 1480), s.get('sub_px', 70 if not TE else 64), 960, hl=s.get('sub_hl', ()), color=CREAM)
    elif k == 'why':
        sc = e_back(prog(v, t0, t0 + .35))
        text_plain(img, 'WHY?' if not TE else 'ఎందుకు?', W / 2, H / 2, int(260 * max(.3, sc)) if not TE else int(220 * max(.3, sc)), AMBER, prog(v, t0, t0 + .15))
    elif k == 'place':
        place_header(img, v, t0, s['num'], s['name'], s['state'])
        if 'text' in s and False:
            headline(img, s['text'], v, s['tt'], W / 2, s.get('y', 1250), s.get('px', 84 if not TE else 80), 960, hl=s.get('hl', ()))
    elif k == 'strike':
        headline(img, s['text'], v, t0 + .05, W / 2, 520, 80 if not TE else 76, 960, hl=s.get('hl', ()))
        strike_list(img, v, s['items'], 860)
    elif k == 'big35':
        headline(img, s['text'], v, t0 + .05, W / 2, 470, 80 if not TE else 76, 960, hl=s.get('hl', ()))
        big35(img, v, t0 + .2, s['sub'])
    elif k == 'cal':
        headline(img, s['text'], v, t0 + .05, W / 2, 470, 84 if not TE else 78, 960, hl=s.get('hl', ()))
        calendar(img, v, t0 + .3, s['lab'])
    elif k == 'chips':
        headline(img, s['text'], v, t0 + .05, W / 2, 470, 84 if not TE else 80, 960, hl=s.get('hl', ()))
        chips(img, v, s['items'], 1050, 190, 54 if not TE else 50)
    elif k == 'recap':
        headline(img, s['text'], v, t0 + .05, W / 2, 330, 80 if not TE else 76, 960, hl=s.get('hl', ()))
        recap(img, v, t0, s['items'])
    elif k == 'stack':
        stack_words(img, v, s['items'], s.get('y0', 640))
        if 'text' in s: headline(img, s['text'], v, s['tt'], W / 2, 1420, 110 if not TE else 96, 960, hl=s.get('hl', ()), hl_col=RED)
    elif k == 'big':
        sc = e_back(prog(v, t0 + s.get('bd', .1), t0 + s.get('bd', .1) + .35))
        if sc > 0: text_plain(img, s['big'], W / 2, s.get('by', 860), int(s.get('bpx', 300) * max(.2, sc)), s.get('bcol', AMBER), prog(v, t0 + s.get('bd', .1), t0 + s.get('bd', .1) + .15))
        if 'lab' in s: mono(img, s['lab'], W / 2, s.get('by', 860) - s.get('bpx', 300) * .62, 30 if not TE else 32, CREAM, prog(v, t0, t0 + .3))
        if 'text' in s and False: headline(img, s['text'], v, s.get('tt', t0 + .3), W / 2, s.get('y', 1250), s.get('px', 80 if not TE else 76), 960, hl=s.get('hl', ()))
        if 'sub' in s and False: headline(img, s['sub'], v, s['sub_t'], W / 2, s.get('sub_y', 1500), s.get('sub_px', 68 if not TE else 62), 960, hl=s.get('sub_hl', ()))
    elif k == 'cta':
        text_plain(img, 'WHY?', W / 2, 600, 230, CREAM, prog(v, t0, t0 + .25))
        sub_button(img, v, t0 + 1.0, W / 2, 900, 1.2, tap=1.3)
        mono(img, s['src'], W / 2, 1640, 22 if not TE else 24, GREY, prog(v, t0 + 1.2, t0 + 1.6))
    # labels that belong to the scene
    if s.get('ai'): tag(img, 'AI ILLUSTRATION', W - 330, 200, prog(v, t0, t0 + .3), px=22)
    if s.get('credit'): credit(img, s['credit'], prog(v, t0, t0 + .3))
    if s.get('src'):
        if k != 'cta': source_line(img, s['src'], prog(v, t0 + .3, t0 + .6))
    # timed overlay events (proof cards)
    for e in EV:
        if e['t'] <= v < e['t1']:
            a_out = 1 - prog(v, e['t1'] - .3, e['t1'])
            news_card(img, e['source'], e['date'], e['head'], W / 2, e.get('y', 1500), v, e['t'], w=940, hl_words=e.get('hl', ()), tilt=e.get('tilt', -2), a_out=a_out)
    caption(img, v)
    # brand + mid-video subscribe nudge
    mono(img, BRAND, W / 2, 120, 28, AMBER)
    sub_pop(img, v, SUB_T)
    if s['kind'] != 'cta': tag(img, SERIES, 40, 175, 1.0, px=20, fill=(10, 10, 10, 170), col=AMBER)
    if FULLV_T <= v < FULLV_T + 3.8:
        a = prog(v, FULLV_T, FULLV_T + .25) * (1 - prog(v, FULLV_T + 3.5, FULLV_T + 3.8)); k = e_back(prog(v, FULLV_T, FULLV_T + .35))
        pill(img, 'FULL VIDEO ON OUR CHANNEL' if not TE else 'ఫుల్ వీడియో మన ఛానెల్‌లో', W / 2, 300, 34, AMBER, (10, 10, 10), a, max(.3, k))
    # cut flash
    f = 1 - prog(v, t0, t0 + .12)
    arr = np.asarray(img.convert('RGB'), np.float32)
    if f > 0 and idx > 0: arr = arr * (1 - .35 * f) + 255 * .35 * f * 0
    fade = 1 - prog(T, TOTAL - .35, TOTAL)
    return np.clip(arr * fade, 0, 255).astype(np.uint8)

def build_audio(path):
    from scipy.ndimage import uniform_filter1d
    from scipy.signal import butter, lfilter
    n = int(TOTAL * SR) + SR; out = np.zeros((n, 2), np.float32)
    i0 = int(LEAD * SR); out[i0:i0 + len(voice)] += voice
    m = load_wav('/home/claude/sun/' + os.environ.get('MUSIC', 'meridian') + '.wav')
    from pedalboard import Pedalboard, PeakFilter, HighShelfFilter, LowpassFilter, HighpassFilter
    bed = Pedalboard([HighpassFilter(60), PeakFilter(cutoff_frequency_hz=2200, gain_db=-5, q=0.7), HighShelfFilter(cutoff_frequency_hz=6000, gain_db=-5), LowpassFilter(10000)])
    m = bed(m.T.copy(), SR).T.astype(np.float32)
    m = m[:n] if len(m) >= n else np.concatenate([m, np.zeros((n - len(m), 2), np.float32)])
    env = uniform_filter1d(np.abs(out[:, 0]), int(.12 * SR)); sc = np.clip(env / .04, 0, 1)
    g = float(os.environ.get('MGAIN', .24)) * (1 - .62 * sc)
    fi = int(.3 * SR); g[:fi] *= np.linspace(0, 1, fi)
    e = int((TOTAL - .05) * SR); fo = int(1.6 * SR); g[e - fo:e] *= np.linspace(1, 0, fo); g[e:] = 0
    def riser(d=1.4):
        # tonal riser (no noise): two detuned rising sines
        t = np.arange(int(d * SR)) / SR; f = 180 * (2 ** (2.2 * t / d))
        y = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .6 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR))
        return y * (t / d) ** 2 * .07
    def hit(a=.55):
        b = boom(1.2, f0=90, f1=40, amp=a); b = b if b.ndim == 1 else b[:, 0]
        t = np.arange(int(.08 * SR)) / SR; b[:len(t)] += np.random.default_rng(5).normal(0, 1, len(t)) * np.exp(-t * 60) * .25; return b
    def add(x, t, k=1.0):
        j = int(t * SR)
        if j < 0: x = x[-j:]; j = 0
        x = x[:max(0, n - j)]; out[j:j + len(x)] += (x[:, None] if x.ndim == 1 else x) * k
    def soft_tr():
        # non-hissy transition: soft low tonal 'thump-swell' (no broadband noise)
        t = np.arange(int(.35 * SR)) / SR
        f = 140 * np.exp(-t * 6) + 55
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * .22
        return y
    for q, s in enumerate(SC):
        if s.get('drop'):
            d0 = int((LEAD + s['t'] - .05) * SR); d1 = int((LEAD + SC[q + 1]['t'] - .02) * SR)
            g[d0:d1] = 0; r = int(.02 * SR); g[d1:d1 + r] *= np.linspace(0, 1, r)
            add(riser(), LEAD + s['t'] - 1.38); add(hit(), LEAD + SC[q + 1]['t'] - .03, .8)
    out += m * g[:, None]
    add(hit(), LEAD - .02, .9)
    def click():
        t = np.arange(int(.06 * SR)) / SR; return (np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * .35 + np.random.default_rng(7).normal(0, 1, len(t)) * np.exp(-t * 200) * .15)
    ct = SC[-1]['t'] + 1.0 + 1.3
    for tt in [SUB_T + 1.4, ct]: add(click(), LEAD + tt)
    for s in SC[1:]:
        if s.get('sfx', True): add(soft_tr(), LEAD + s['t'] - .06)
        if s.get('boom'): add(hit(.4), LEAD + s['t'], .6)
        if s['kind'] == 'big':
            tp = np.arange(int(.09 * SR)) / SR; pop = np.sin(2 * np.pi * (220 + 900 * np.exp(-tp * 40)) * tp) * np.exp(-tp * 35) * .35
            add(pop, LEAD + s['t'] + s.get('bd', .1))
    import scipy.io.wavfile as wf
    wf.write(path + '.pre.wav', SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path + '.pre.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=7', '-ar', '48000', path], check=True)

if __name__ == '__main__':
    mode = sys.argv[3] if len(sys.argv) > 3 else 'full'
    if mode == 'stills':
        for t in sys.argv[4].split(','): Image.fromarray(frame_at(float(t) + LEAD)).save(f"{OUT}/still_{float(t):06.2f}.jpg", quality=85)
        sys.exit()
    if mode == 'audio':
        build_audio(f"{OUT}/audio.wav"); sys.exit()
    if mode == 'part':
        i, nparts = int(sys.argv[4]), int(sys.argv[5]); N = int(TOTAL * FPS); a, b = N * i // nparts, N * (i + 1) // nparts
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', f"{OUT}/part{i}.mp4"], stdin=subprocess.PIPE)
        for f in range(a, b): p.stdin.write(frame_at(f / FPS).tobytes())
        p.stdin.close(); p.wait(); print('part done', i)
