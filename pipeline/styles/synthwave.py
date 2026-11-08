"""4) Synthwave: neon road, striped sun, chrome headlines flying in.
Best for: tech, 80s/90s history, 'the future' sections. Use for short bursts, it is loud."""
import functools, math
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from core import *

DURATION = 8.0
PINK = (255, 62, 165); CYAN = (70, 225, 255); VIOLET = (58, 18, 96); NIGHT = (11, 7, 30)
DEFAULT = dict(events=[dict(t=0, big='1991', small='INDIA OPENS UP'), dict(t=2.7, big='2007', small='THE SMARTPHONE ARRIVES'), dict(t=5.4, big='2016', small='DATA GETS CHEAP')])


@functools.lru_cache(4)
def _sky(W, H, hz):
    img = vgradient(W, hz, [(0, NIGHT), (.5, VIOLET), (.86, (176, 38, 128)), (1, (255, 128, 80))]); full = Image.new('RGB', (W, H), (6, 4, 18)); full.paste(img, (0, 0)); d = ImageDraw.Draw(full); r = np.random.default_rng(3)
    for _ in range(240):
        x, y, s = r.uniform(0, W), r.uniform(0, hz * .72), r.uniform(1, 3.2); c = int(r.uniform(120, 255)); d.ellipse((x - s, y - s, x + s, y + s), fill=(c, c, min(255, c + 25)))
    return full


@functools.lru_cache(4)
def _sun(R):
    D = int(R * 2); g = vgradient(D, D, [(0, (255, 232, 130)), (.45, AMBER), (.72, (255, 90, 120)), (1, PINK)]); return g


@functools.lru_cache(4)
def _hills(W, H, hz):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); r = np.random.default_rng(8)
    for (amp, col, n) in ((.17, (34, 16, 74, 255), 15), (.09, (20, 10, 48, 255), 22)):
        xs = np.linspace(-20, W + 20, n); ys = hz - r.uniform(.15, 1, n) * amp * H * (np.abs(np.linspace(-1, 1, n)) ** 1.4 + .08)
        pts = [(hx, hz)] if False else [(-20, hz)] + list(zip(xs.tolist(), ys.tolist())) + [(W + 20, hz)]; d.polygon(pts, fill=col); d.line(pts, fill=(255, 62, 165, 150), width=2)
    return L


@functools.lru_cache(16)
def _chrome(s, px, maxw):
    f, px = fit(s, 'head', px, maxw); tw = int(f.getlength(s)) + 90; h = int(px * 1.75); m = Image.new('L', (tw, h), 0); ImageDraw.Draw(m).text((tw / 2, h / 2), s, font=f, fill=255, anchor='mm')
    g = vgradient(tw, h, [(.14, (250, 250, 255)), (.44, (120, 190, 255)), (.52, (34, 18, 70)), (.58, (255, 140, 200)), (.86, (255, 244, 214))])
    e = m.filter(ImageFilter.MaxFilter(7)); spr = Image.new('RGBA', (tw, h), (0, 0, 0, 0)); spr.paste((255, 62, 165, 255), (0, 0), e); spr.paste(g, (0, 0), m); return spr


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); W, H = st.W, st.H; hz = int(H * (.56 if st.portrait else .58)); img = _sky(W, H, hz).copy()
    R = W * (.27 if st.portrait else .17); cx, cy = W / 2 if st.portrait else W * .73, hz - R * .62; sun = _sun(R); m = Image.new('L', sun.size, 0); d = ImageDraw.Draw(m); D = sun.size[0]; d.ellipse((0, 0, D - 1, D - 1), fill=255)
    for i in range(7):
        y = D * (.48 + ((i + (v * .32) % 1) / 7) * .56); t = D * (.012 + .012 * i); d.rectangle((0, y, D, y + t), fill=0)
    sf = Image.new('RGB', (W, H), 0); sf.paste(sun, (int(cx - R), int(cy - R)), m); img = glow(img, sf, 110, .85); img.paste(sun, (int(cx - R), int(cy - R)), m)
    h = _hills(W, H, hz); img.paste(h, (0, 0), h); d = ImageDraw.Draw(img); d.rectangle((0, hz, W, H), fill=(7, 4, 20))
    L = Image.new('RGB', (W, H), 0); dl = ImageDraw.Draw(L); B = H - hz
    for i in range(-20, 21):
        x = W / 2 + i * W * (.42 if st.portrait else .19); dl.line([(W / 2 + i * 22, hz), (x, H)], fill=PINK, width=3)
    for i in range(16):
        u = (i + (v * 1.5) % 1) / 16; y = hz + B * (u ** 3.0) * 1.03; c = shade(PINK, .35 + .65 * u); dl.line([(0, y), (W, y)], fill=c, width=max(1, int(1 + u * 4)))
    img = glow(img, L, 26, 1.0); img = ImageChops.screen(img, L); dh = ImageDraw.Draw(img); dh.line([(0, hz), (W, hz)], fill=(255, 190, 230), width=3)
    evs = s['events']; cur = [e for e in evs if e['t'] <= v][-1] if any(e['t'] <= v for e in evs) else evs[0]; age = v - cur['t']
    k = e_back(prog(age, 0, .42), 1.1) if cur['t'] > 0 else 1.0; big = 240 if st.portrait else 220; yc = st.y0 + 170 if st.portrait else st.y0 + 200; tx = st.cx if st.portrait else int(W * .3); mw = st.sw if st.portrait else int(W * .52)
    spr = _chrome(cur['big'], big, mw); sc = max(.05, k * (1 + .03 * age)); sp = spr.resize((int(spr.width * sc), int(spr.height * sc)), Image.BILINEAR)
    L2 = Image.new('RGB', (W, H), 0); L2.paste(PINK, (int(tx - sp.width / 2), int(yc - sp.height / 2)), sp.getchannel('A')); img = glow(img, L2, 40, .75); img.paste(sp, (int(tx - sp.width / 2), int(yc - sp.height / 2)), sp)
    a2 = prog(age, .18, .4) if cur['t'] > 0 else 1.0; text(img, cur['small'], tx, yc + big * .62, 54 if st.portrait else 56, CYAN, a=a2, maxw=mw, kind='head')
    return img
