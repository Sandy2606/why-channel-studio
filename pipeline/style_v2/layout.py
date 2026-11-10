"""Shared layout components + automated layout QC for every Why? / Why? Telugu video.

- badge(): the ONE corner badge used for the series tag (top-left) and the section chip (top-right).
  Drawn at 3x and downsampled, fill inset inside the border, text centred on its real ink box
  (works for Telugu vowel signs and descenders), fixed height, padding, radius and edge margins.
- reg(): every component registers the boxes it draws (container + text ink) for the frame.
- check(): containment, padding, edge-margin and overlap rules; used by qc_layout.py per frame.
Human visual inspection stays mandatory (playbook "Professional visual QC").
"""
import functools
from PIL import Image, ImageDraw
from core import pick, INK, CREAM, AMBER

EDGE = 64            # margin from the left/right frame edge for corner badges
BADGE_Y = 178        # vertical centre of the corner badges (inside the 9:16 top safe band)
BADGE_H = 60; BADGE_PADX = 26; BADGE_R = 30; DOT = 14; DOT_GAP = 14; SS = 3
LAYOUT = []          # boxes registered for the current frame: dict(kind, box, ink, owner)

def reset(): LAYOUT.clear()
def reg(kind, box, ink=None, owner=None, group=None):
    LAYOUT.append(dict(kind=kind, box=tuple(float(v) for v in box), ink=tuple(float(v) for v in ink) if ink else None, owner=owner, group=group))

def ink_box(s, f):
    """real ink bounds of s for font f, relative to an 'ls' (left, baseline) origin"""
    return f.getbbox(s, anchor='ls')

def _fit(s, kind, px, maxw, minpx):
    f = pick(s, kind, px)
    while px > minpx and f.getlength(s) > maxw: px -= 1; f = pick(s, kind, px)
    return f, px

@functools.lru_cache(64)
def _badge_sprite(s, kind, px, bg, fg, border, dot, alpha):
    f, px = _fit(s, kind, px, 440, int(px * .82))
    l, t, r, b = ink_box(s, f); tw = r - l; th = b - t
    w = int(round(BADGE_PADX * 2 + tw + (DOT + DOT_GAP if dot else 0))); h = BADGE_H
    big = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    bw = 2 * SS if border else 0
    if border: d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), BADGE_R * SS, fill=border + (alpha,))
    d.rounded_rectangle((bw, bw, w * SS - 1 - bw, h * SS - 1 - bw), BADGE_R * SS - bw, fill=bg + (alpha,))   # fill INSIDE the border
    x = BADGE_PADX
    if dot:
        cy = h / 2; d.ellipse(((x) * SS, (cy - DOT / 2) * SS, (x + DOT) * SS, (cy + DOT / 2) * SS), fill=AMBER + (255,)); x += DOT + DOT_GAP
    fb = pick(s, kind, px * SS); l3, t3, r3, b3 = ink_box(s, fb)
    ox = x * SS - l3; oy = (h * SS) / 2 - (t3 + b3) / 2          # centre the actual ink, not the font box
    d.text((ox, oy), s, font=fb, fill=fg + (255,), anchor='ls')
    spr = big.resize((w, h), Image.LANCZOS)
    inkbox = (x, h / 2 - th / 2, x + tw, h / 2 + th / 2)
    return spr, inkbox

def badge(img, s, side='left', style='tag', a=1.0, y=BADGE_Y):
    """side: 'left' | 'right'. style: 'tag' (ink, amber text, dot, hairline border) | 'chip' (cream, ink text)"""
    if a <= 0.01 or not s: return
    if style == 'tag': spr, ib = _badge_sprite(s, 'monob', 30, (10, 10, 10), AMBER, (88, 70, 30), True, 235)
    else: spr, ib = _badge_sprite(s, 'head', 30, CREAM, INK, None, False, 255)
    W = img.size[0]; x0 = EDGE if side == 'left' else W - EDGE - spr.width; y0 = int(round(y - spr.height / 2))
    if a < 1: spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda p: int(p * a)))
    img.paste(spr, (int(x0), y0), spr)
    reg('badge', (x0, y0, x0 + spr.width, y0 + spr.height), (x0 + ib[0], y0 + ib[1], x0 + ib[2], y0 + ib[3]), owner=s, group='corner')

# ------------------------------------------------------------------ checks
def _inside(a, b, pad=0): return a[0] >= b[0] + pad - .5 and a[1] >= b[1] + pad - .5 and a[2] <= b[2] - pad + .5 and a[3] <= b[3] - pad + .5
def _overlap(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

def check(W=1080, H=1920, edge=40, min_pad=8):
    """returns a list of defect strings for the boxes registered this frame"""
    out = []
    for e in LAYOUT:
        b = e['box']
        if e['kind'] != 'image' and (b[0] < edge or b[2] > W - edge or b[1] < edge or b[3] > H - edge): out.append(f"{e['kind']} '{e['owner']}' closer than {edge}px to a frame edge {tuple(int(v) for v in b)}")
        if e['ink'] and not _inside(e['ink'], b, min_pad): out.append(f"{e['kind']} '{e['owner']}' text not inside its box with {min_pad}px padding")
    tops = [e for e in LAYOUT if e['kind'] in ('badge', 'caption', 'credit', 'card', 'label')]
    caps = [e for e in LAYOUT if e['kind'] == 'caption']
    for c in caps:   # captions must never sit on a picture panel or any on-screen text
        for e in LAYOUT:
            if e['kind'] in ('image',) and _overlap(c['box'], e['box']): out.append(f"caption '{c['owner']}' on image '{e['owner']}'")
    for i in range(len(tops)):
        for j in range(i + 1, len(tops)):
            a, b = tops[i], tops[j]
            if a['group'] and a['group'] == b['group']: continue
            if _overlap(a['box'], b['box']): out.append(f"overlap: {a['kind']} '{a['owner']}' x {b['kind']} '{b['owner']}'")
    lefts = [e for e in LAYOUT if e['kind'] == 'badge']
    if len(lefts) == 2 and abs((lefts[0]['box'][1] + lefts[0]['box'][3]) - (lefts[1]['box'][1] + lefts[1]['box'][3])) > 1: out.append('corner badges not on one centre line')
    return out
