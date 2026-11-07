"""Edited sequences for single narration lines: several cuts per line, timed to words (EN) or phrase position (TE)."""
import math
import numpy as np
import flib as FL, fx
from flib import W, H, put, text, eo, GOLD, PAPER

C = {}            # filled by init(): cue, TE, M, P
def init(cue, TE, M, P): C.update(cue=cue, TE=TE, M=M, P=P)
def cue(i, en, te): return C['cue'](i, en, te)
def L(en, te): return te if C['TE'] else en

def cuts(t, parts, fade=0.0):
    """parts: [(start, fn(t, a, b))] in time order; hard cuts unless fade > 0."""
    idx = 0
    for k, (s, _) in enumerate(parts):
        if t >= s: idx = k
    s, fn = parts[idx]; e = parts[idx + 1][0] if idx + 1 < len(parts) else s + 30
    fr = fn(t, s, e)
    if fade > 0 and idx > 0 and t - s < fade:
        ps, pfn = parts[idx - 1]; prev = pfn(t, ps, s); k = (t - s) / fade
        fr = Image_blend(prev, fr, k)
    return fr
def Image_blend(a, b, k):
    from PIL import Image
    return Image.blend(a.convert('RGBA'), b.convert('RGBA'), max(0, min(1, k)))

def still(key, c0, c1, z0, z1, alive=None):
    """camera on a still (no depth warp), optional living effect alive(arr, t)."""
    def f(t, a, b):
        arr = FL.img(key)
        if alive: arr = alive(arr, t)
        return fx.to_rgba(fx.cam(arr, (t - a) / max(0.1, b - a), c0, c1, z0, z1))
    return f

# ------------------------------------------------------------------ 2.1  "Why would a country ban a fabric? ... follow the hands."
def s21(t, a, b):
    c_ban = cue('2.1', 'ban', 'నిషేధిస్తుంది'); c_hands = cue('2.1', 'follow', 'చేతుల') - 0.05
    macro = still('MET1', (.60, .30), (.61, .31), 5.2, 5.5)
    snap = still('MET1', (.61, .31), (.61, .315), 7.0, 7.3)
    d = 0.25
    return cuts(t, [(a, macro), (c_ban + 0.05, snap),
                    (c_hands, still('G04', (.45, .5), (.46, .5), 1.25, 1.32)),
                    (c_hands + d, still('T5', (.22, .36), (.23, .37), 2.6, 2.7)),
                    (c_hands + 2 * d, still('T6', (.40, .44), (.41, .44), 2.4, 2.5)),
                    (c_hands + 3 * d, still('G05', (.64, .38), (.64, .40), 1.9, 2.0))])

# ------------------------------------------------------------------ 2.2  spinner -> many spinners, one loom
def s22(t, a, b):
    c_close = cue('2.2', 'spinning', 'రాట్నం'); c_diag = cue('2.2', 'It', 'ఒక్క') - 0.15
    c_many = cue('2.2', 'many', 'ఎంతోమంది'); c_loom = cue('2.2', 'loom', 'మగ్గం')
    wide = still('T5', (.47, .50), (.42, .52), 1.04, 1.12, alive=lambda arr, tt: fx.wheel(tt))
    close = still('T5', (.17, .60), (.19, .60), 1.85, 1.95, alive=lambda arr, tt: fx.wheel(tt))
    diag = lambda tt, s, e: fx.spinners(tt, s, e, c_many, c_loom, L('MANY SPINNERS', 'ఎంతోమంది వడికేవాళ్లు'), L('ONE LOOM', 'ఒక్క మగ్గం'))
    return cuts(t, [(a, wide), (c_close, close), (c_diag, diag)])

# ------------------------------------------------------------------ 2.3  weaver, broker, price, bargaining power
LAB23 = dict(en=dict(weaver='WEAVER', broker='BROKER', advance='PAID IN ADVANCE', price='PRICE · SET BY THE BROKER', power='BARGAINING POWER'),
             te=dict(weaver='నేతగాడు', broker='దళారి', advance='ముందుగానే డబ్బు', price='ధర · దళారి నిర్ణయం', power='బేరమాడే శక్తి'))
def s23(t, a, b):
    c_fam = cue('2.3', 'whole', 'కుటుంబం'); c_brk = cue('2.3', 'Weavers', 'దళారులు') - 0.15
    c_skill = cue('2.3', 'World', 'ప్రపంచస్థాయి') - 0.1; c_pow0 = cue('2.3', 'very', 'బేరమాడే') - 0.3
    adv = cue('2.3', 'advance', 'ముందుగానే'); brk = cue('2.3', 'brokers', 'దళారులు')
    cues = dict(weaver=c_brk + 0.15, broker=min(brk, adv - 0.3), beam=c_brk + 0.15, advance=adv,
                price=cue('2.3', 'price', 'ధర'), power=cue('2.3', 'bargaining', 'బేరమాడే'))
    lab = LAB23['te' if C['TE'] else 'en']
    wl = (L('WARP', 'పడుగు'), L('WEFT', 'పేక'), L('SHUTTLE', 'నాడె'))
    weave1 = lambda tt, s, e: fx.weave(tt, s, e, s + 0.2, labels=wl)
    weave2 = lambda tt, s, e: fx.weave(tt, s, e, s + 0.1, push=(1.35, 1.45))
    fam = still('T6', (.62, .55), (.55, .55), 1.06, 1.14)
    diag = lambda tt, s, e: fx.broker(tt, s, e, cues, lab)
    return cuts(t, [(a, weave1), (c_fam, fam), (c_brk, diag), (c_skill, weave2), (c_pow0, diag)])
def s23_hits(a, b):
    c_fam = cue('2.3', 'whole', 'కుటుంబం'); c_skill = cue('2.3', 'World', 'ప్రపంచస్థాయి') - 0.1; c_pow0 = cue('2.3', 'very', 'బేరమాడే') - 0.3
    return fx.weave_hits(a + 0.2, c_fam) + fx.weave_hits(c_skill + 0.1, c_pow0)

# ------------------------------------------------------------------ 2.4  the dyer
def s24(t, a, b):
    c = cue('2.4', 'dire', 'రంగులు') - 0.1
    rip = lambda arr, tt: fx.ripple(arr, tt, (560, 1400), (520, 130))
    return cuts(t, [(a, still('G06', (.50, .45), (.47, .47), 1.02, 1.08, alive=rip)), (c, still('G06', (.16, .80), (.17, .82), 2.0, 2.15, alive=rip))])

# ------------------------------------------------------------------ 2.6  kalam: the real palampore being made
def s26(t, a, b):
    c_draw = cue('2.6', 'drew', 'design'); c_out = cue('2.6', 'weeks', 'వారాల') - 0.9
    lab = L('PALAMPORE · COROMANDEL COAST, 18TH C. · THE MET', 'పలంపోర్ · కోరమాండల్ తీరం, 18వ శతాబ్దం · The Met')
    anim = lambda tt, s, e: fx.kalam(tt, s, e, c_draw, cue('2.6', 'reds', 'ఎరుపు'), cue('2.6', 'blue', 'నీలం'), cue('2.6', 'wax', 'మైనం'), c_out, lab, L('ILLUSTRATIVE RECONSTRUCTION OF THE TECHNIQUE', 'పద్ధతికి ఉదాహరణ పునఃసృష్టి'))
    return cuts(t, [(a, still('G05', (.63, .42), (.64, .44), 1.45, 1.6)), (c_draw - 0.15, anim)])

# ------------------------------------------------------------------ 3.2  Golconda -> the sea gate
def s32(t, a, b, mapfn):
    c = cue('3.2', 'seagate', 'సముద్ర') - 0.1
    sw = lambda arr, tt: fx.water(fx.swing(arr, tt, (1140, 80), fx.G21_BALE), 'G21', tt)
    bale = still('G09', (.07, .76), (.08, .75), 3.2, 3.0, alive=lambda arr, tt: fx.water(arr, 'G09', tt))
    return cuts(t, [(a, mapfn), (c, bale), (c + 1.0, still('G21', (.45, .40), (.50, .42), 1.0, 1.08, alive=sw))])

# ------------------------------------------------------------------ 3.3  ships from four seas; Dutch and English; brokers to weaving villages
def flag_marker(fr, t, c, x, y, label):
    k = eo((t - c) / 0.4)
    if k <= 0: return
    from PIL import ImageDraw
    d = ImageDraw.Draw(fr); r = 26 + 30 * (1 - eo((t - c) / 0.7))
    d.ellipse((x - r, y - r, x + r, y + r), outline=GOLD + (int(230 * k),), width=4)
    d.line((x, y + r, x, y + 120), fill=GOLD + (int(200 * k),), width=3)
    im = text(label, 'label', 30, PAPER); bg = fx.Image.new('RGBA', (im.width + 30, im.height + 16), (14, 12, 18, int(190 * k)))
    bg.alpha_composite(im, (15, 8)); put(fr, bg, x, y + 124, k, 'ct')
def s33(t, a, b, shipsmap, netmap):
    c_g09 = cue('3.3', 'The', '1600ల') - 0.1; c_mkt = cue('3.3', 'Local', 'దళారులు') - 0.1
    c_buy = cue('3.3', 'Local', 'దళారులు') + 1.0; c_net = cue('3.3', 'buyers', 'కొనుగోలుదారులను') - 0.1
    c_du = cue('3.3', 'Dutch', 'డచ్'); c_en = cue('3.3', 'English', 'ఇంగ్లీష్')
    def harbour(tt, s, e):
        u = (tt - s) / max(0.1, e - s)
        arr = fx.water(FL.img('G09'), 'G09', tt)
        z0, z1, c0, c1 = 1.18, 1.26, (.62, .40), (.70, .38)
        fr = fx.to_rgba(fx.cam(arr, u, c0, c1, z0, z1))
        # project the two flagged ships into the frame with the same camera
        h, w = arr.shape[:2]; base = max(W / w, H / h); e_ = fx.sm(u) * .8 + u * .2; sc = base * fx.lerp(z0, z1, e_)
        fxx, fyy = fx.lerp(c0[0], c1[0], e_), fx.lerp(c0[1], c1[1], e_); hw, hh = W / 2 / sc, H / 2 / sc
        cx = min(max(fxx * w, hw), w - hw); cy = min(max(fyy * h, hh), h - hh)
        P_ = lambda X, Y: ((X - cx) * sc + W / 2, (Y - cy) * sc + H / 2)
        x, y = P_(2290, 470); flag_marker(fr, tt, c_du, x, y, L('DUTCH · EARLY 1600s', 'డచ్ · 1600ల మొదట్లో'))
        x, y = P_(1890, 450); flag_marker(fr, tt, c_en, x, y, L('ENGLISH · 1611', 'ఇంగ్లీష్ · 1611'))
        return fr
    import fx3
    return cuts(t, [(a, shipsmap), (c_g09, harbour), (c_mkt, still('G10', (.36, .48), (.38, .48), 1.55, 1.62)), (c_buy, lambda tt, s_, e_: fx3.chain(tt, s_, b))])

# ------------------------------------------------------------------ 0.5  the land the world came to... a company that came to trade
def s05(t, a, b):
    c = cue('0.5', 'company', 'కంపెనీ') - 0.1
    return cuts(t, [(a, still('T2', (.45, .55), (.45, .50), 1.02, 1.1)), (c, still('T2', (.60, .10), (.60, .12), 2.6, 2.8))])
# ------------------------------------------------------------------ 7.1  permission, silver... then Plassey
def s71(t, a, b):
    c_s = cue('7.1', 'silver', 'వెండి') - 0.15; c_p = cue('7.1', 'Then', 'తర్వాత') - 0.1
    return cuts(t, [(a, still('G24', (.45, .5), (.47, .5), 1.05, 1.12)), (c_s, still('G19', (.30, .72), (.32, .70), 1.7, 1.8)),
                    (c_p, still('G29', (.5, .55), (.52, .55), 1.02, 1.1))])
