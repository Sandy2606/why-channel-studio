# Why? sound-design kit: tonal, clean SFX (no hissy noise whooshes — user feedback "sounds like sneezing").
import numpy as np
from pedalboard import Pedalboard, Reverb, LowpassFilter, HighpassFilter
SR = 48000
_rv = Pedalboard([Reverb(room_size=.55, damping=.6, wet_level=.28, dry_level=.8, width=.9)])
_rv_big = Pedalboard([Reverb(room_size=.85, damping=.5, wet_level=.35, dry_level=.75, width=1.0)])

def _t(d): return np.arange(int(d * SR)) / SR
def _env(t, a=.004, k=8.0): return np.minimum(1, t / a) * np.exp(-t * k)
def _verb(x, big=False, tail=.8):
    x = np.concatenate([x, np.zeros(int(tail * SR), np.float32)]).astype(np.float32)
    y = (_rv_big if big else _rv)(np.stack([x, x]), SR)
    return y.T.astype(np.float32)          # (n, 2)
def _st(x): x = x.astype(np.float32); return np.stack([x, x], 1)

def tick(f=2600, g=.10):
    """soft wooden tick for ordinary cuts"""
    t = _t(.05); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t)) * _env(t, .001, 90)
    return _st(x * g)

def thock(g=.22):
    """card / label landing: short low-mid knock"""
    t = _t(.18); f = 180 * np.exp(-t * 20) + 140
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(t, .002, 26) + .3 * np.sin(2 * np.pi * 900 * t) * _env(t, .001, 120)
    return _verb(x * g, tail=.3)

def impact(g=.45, big=True):
    """cinematic low hit (sine sub + body), with room tail"""
    t = _t(1.1); f = 95 * np.exp(-t * 7) + 42
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(t, .003, 3.2) + .35 * np.sin(2 * np.pi * 160 * t) * _env(t, .002, 14)
    return _verb(x * g, big=big, tail=1.0)

def pop(g=.28):
    t = _t(.10); x = np.sin(2 * np.pi * (240 + 900 * np.exp(-t * 45)) * t) * _env(t, .001, 34)
    return _verb(x * g, tail=.2)

def bell(f=880, g=.16, d=1.2):
    """soft bell / ping (inharmonic partials)"""
    t = _t(d); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k) for r, a, k in [(1, 1, 3.5), (2.76, .35, 6), (5.4, .15, 9), (2, .25, 5)])
    return _verb(x * _env(t, .002, 0) * g, tail=.8)

def ping(i=0, g=.14):
    """map pin: ascending pentatonic pings"""
    scale = [659.3, 740.0, 880.0, 987.8, 1174.7, 1318.5, 1480.0]
    return bell(scale[i % len(scale)], g, .9)

def ding(g=.18): return bell(1318.5, g, 1.4) + bell(1975.5, g * .5, 1.4)

def nope(g=.22):
    """✕ : two dull low tones (tonal 'uh-uh')"""
    t = _t(.16); a = np.sin(2 * np.pi * 196 * t) * _env(t, .004, 18); b = np.sin(2 * np.pi * 165 * t) * _env(t, .004, 18)
    x = np.concatenate([a, np.zeros(int(.04 * SR)), b]); x = np.tanh(x * 2.2) * .6
    return _verb(x * g, tail=.3)

def glide(d=1.0, f0=300, f1=900, g=.07):
    """tonal swoosh: a soft sine glide with a swell (replaces noise whooshes)"""
    t = _t(d); f = f0 * (f1 / f0) ** (t / d)
    x = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)) * np.sin(np.pi * t / d) ** 2
    return _verb(x * g, tail=.5)

def riser(d=1.2, g=.08):
    t = _t(d); f = 160 * (2 ** (2.3 * t / d))
    x = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)) * (t / d) ** 2.2
    return _verb(x * g, tail=.2)

def shimmer(g=.12):
    """reveal sparkle: quick 3-note bell arpeggio"""
    out = np.zeros((int(1.8 * SR), 2), np.float32)
    for k, f in enumerate([987.8, 1318.5, 1760.0]):
        b = bell(f, g * (1 - .15 * k), 1.0); j = int(k * .07 * SR); out[j:j + len(b)] += b[:len(out) - j]
    return out

def snap(g=.2):
    t = _t(.07); x = np.sin(2 * np.pi * (1600 * np.exp(-t * 60) + 300) * t) * _env(t, .001, 60)
    return _st(x * g)

def tap(g=.3):
    """subscribe tap: click then bell"""
    c = snap(g); b = ding(.16); out = np.zeros((len(b) + int(.05 * SR), 2), np.float32)
    out[:len(c)] += c; out[int(.05 * SR):int(.05 * SR) + len(b)] += b; return out

# ================= v2 "documentary" kit (user: v1 pings/bells/pops felt like a kids' video) =================
from pedalboard import Compressor
_rng = np.random.default_rng(11)
def _lp(x, hz): return LowpassFilter(hz)(x[None, :].astype(np.float32), SR)[0]
def _bp(x, lo, hi): return LowpassFilter(hi)(HighpassFilter(lo)(x[None, :].astype(np.float32), SR), SR)[0]

def sub_boom(g=.55):
    """deep cinematic boom: sub sine (tiny pitch fall) + low rumble body + big room"""
    t = _t(2.2); f = 52 + 14 * np.exp(-t * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(t, .006, 1.6)
    body = _lp(_rng.normal(0, 1, len(t)), 220) * _env(t, .004, 6) * 2.2
    x = np.tanh((sub + .5 * body) * 1.6) * .8
    return _verb(x * g, big=True, tail=1.2)

def low_swell(d=.9, g=.22):
    """reverse-style low swell into a hit (rumble, not hiss: everything under ~350 Hz)"""
    t = _t(d); r = _lp(_rng.normal(0, 1, len(t)), 350) * 2.0
    tone = np.sin(2 * np.pi * np.cumsum(70 + 40 * t / d) / SR) * .6
    x = (r + tone) * (t / d) ** 2.6
    return _st(x * g)

def thud(g=.22):
    """soft low knock for labels / numbers / list beats"""
    t = _t(.35); f = 85 + 40 * np.exp(-t * 30)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(t, .002, 14) + .4 * _lp(_rng.normal(0, 1, len(t)), 300) * _env(t, .001, 40)
    return _verb(x * g, tail=.3)

def mouse_click(g=.35):
    """realistic mouse click: press + release transients"""
    out = np.zeros(int(.12 * SR), np.float32)
    for k, (tt, a) in enumerate([(0, 1.0), (.055, .6)]):
        t = _t(.012); x = _bp(_rng.normal(0, 1, len(t)), 1800, 6000) * _env(t, .0003, 600) + np.sin(2 * np.pi * 1300 * t) * _env(t, .0003, 350) * .6
        j = int(tt * SR); out[j:j + len(x)] += x * a
    return _st(out * g)

def shutter(g=.28):
    """camera shutter for photos / proof cards"""
    out = np.zeros(int(.16 * SR), np.float32)
    for tt, a in [(0, 1.0), (.07, .8)]:
        t = _t(.03); x = _bp(_rng.normal(0, 1, len(t)), 900, 5000) * _env(t, .0005, 140) + np.sin(2 * np.pi * 420 * t) * _env(t, .0005, 120) * .5
        j = int(tt * SR); out[j:j + len(x)] += x * a
    return _st(out * g)

# ================= v3 motion-graphics kit: sounds for on-screen movement (mature, low, not hissy) =================
def swish(d=.5, f0=250, f1=1400, g=.16):
    """soft air swish that follows a movement: band-limited (<~2 kHz), smooth bell envelope"""
    t = _t(d); n = _rng.normal(0, 1, len(t)).astype(np.float32)
    # moving band: crossfade between a low and a higher band-limited copy
    lo = _bp(n, max(80, f0 * .6), f0 * 1.6); hi = _bp(n, f1 * .6, min(2400, f1 * 1.4)); u = t / d
    x = (lo * (1 - u) + hi * u) * np.sin(np.pi * u) ** 1.6 * 2.2
    return _verb(x * g, tail=.25)

def drop(g=.18):
    """object landing (map pin, chip, node): short low knock + tiny tick"""
    t = _t(.22); f = 120 + 60 * np.exp(-t * 40)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(t, .001, 22) + .25 * _bp(_rng.normal(0, 1, len(t)), 1500, 3500) * _env(t, .0005, 220)
    return _verb(x * g, tail=.25)

def lock(g=.24):
    """two things snapping together: mid knock + low body"""
    t = _t(.3); x = (np.sin(2 * np.pi * 95 * t) * _env(t, .001, 16) + .6 * np.sin(2 * np.pi * 310 * t) * _env(t, .001, 45)
                     + .35 * _bp(_rng.normal(0, 1, len(t)), 700, 2500) * _env(t, .0005, 160))
    return _verb(x * g, tail=.3)

def stamp(g=.3):
    """rubber-stamp slam for ✕ marks and rows: heavy low thump + short crunch"""
    t = _t(.4); x = (np.sin(2 * np.pi * np.cumsum(70 + 70 * np.exp(-t * 35)) / SR) * _env(t, .001, 11)
                     + .5 * _bp(_rng.normal(0, 1, len(t)), 300, 1800) * _env(t, .0005, 70))
    return _verb(np.tanh(x * 1.6) * g, tail=.35)
