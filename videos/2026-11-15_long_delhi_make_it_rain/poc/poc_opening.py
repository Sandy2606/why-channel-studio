"""Delhi Rain · opening motion proof of concept (≈20 s, 16:9).
Characters: real cutouts from the approved A0 sheet (refs/A0_family_master.png).
Sets: STAND-IN, drawn in code until B0 arrives. No voice: captions stand in for the approved narration.
Usage: python3 poc_opening.py en|te
"""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

ROOT = '/home/claude/why-channel-studio'
HERE = os.path.dirname(os.path.abspath(__file__)); VID = os.path.dirname(HERE)
sys.path.insert(0, ROOT + '/pipeline/style_v2'); sys.path.insert(0, ROOT + '/pipeline/styles')
import layout as LY
from core import pick, AMBER, CREAM, INK

LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
W, H, FPS, DUR = 1920, 1080, 30, 20.0
FR = os.path.join(HERE, f'frames_{LANG}'); os.makedirs(FR, exist_ok=True)
rng = np.random.default_rng(7)

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def prog(t, a, b): return min(1, max(0, (t - a) / (b - a)))

# ---------------------------------------------------------------- cutouts from A0
def cutouts():
    im = Image.open(VID + '/refs/A0_family_master.png').convert('RGB'); a = np.asarray(im).astype(float)
    d = np.sqrt(((a - np.array([172, 151, 136.])) ** 2).sum(2))
    lab, _ = ndi.label(d < 34)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = ~np.isin(lab, list(border)); fg = ndi.binary_opening(fg, iterations=1)
    # remove enclosed background pockets (between legs / bat), keep small real holes
    holes = ndi.binary_fill_holes(fg) & ~fg
    hl, hn = ndi.label(holes)
    for i in range(1, hn + 1):
        m = hl == i
        if m.sum() < 300: fg |= m
    al = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    rgba = im.convert('RGBA'); rgba.putalpha(al)
    out = {}
    for name, (x0, x1) in {'anu_front': (30, 388), 'anu_34': (441, 684), 'mum': (1032, 1295)}.items():
        c = rgba.crop((x0, 0, x1, 941)); out[name] = c.crop(c.getchannel('A').point(lambda p: 255 if p > 20 else 0).getbbox())
    # the bat alone (below Anu's hand) for the "bat goes back" action
    bat = rgba.crop((36, 520, 120, 885)); out['bat'] = bat.crop(bat.getchannel('A').point(lambda p: 255 if p > 20 else 0).getbbox())
    return out
C = cutouts()

def scaled(img, h):
    k = h / img.height; return img.resize((max(1, int(img.width * k)), int(h)), Image.LANCZOS)

# ---------------------------------------------------------------- painterly helpers
GRAIN = Image.fromarray((rng.normal(0, 1, (H, W)) * 9 + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
def paint(img):
    img = img.filter(ImageFilter.ModeFilter(5)).filter(ImageFilter.GaussianBlur(1.3))
    a = np.asarray(img.convert('RGB')).astype(float); g = (np.asarray(GRAIN).astype(float) - 128) / 128
    a = a * (1 + 0.05 * g[..., None]); return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def field(seed, cells=(48, 27)):
    r = np.random.default_rng(seed).random((cells[1], cells[0])).astype(np.float32)
    return np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((W + 400, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))).astype(np.float32) / 255
HZ1, HZ2 = field(1), field(2, (96, 54))
HAZE_RGB = np.array([186, 178, 166], np.float32)

def haze(arr, amt, t, mask=None, density=1.0):
    if amt <= 0.001: return arr
    off = int(t * 22) % 400; off2 = int(t * 40) % 400
    n = 0.7 + 0.3 * (0.6 * HZ1[:, off:off + W] + 0.4 * HZ2[:, off2:off2 + W])
    a = np.clip(amt * density * n, 0, 0.97)[..., None]
    if mask is not None: a = a * mask[..., None]
    return arr * (1 - a) + HAZE_RGB * a

# ---------------------------------------------------------------- set A: outside looking in at the balcony door
def set_door():
    im = Image.new('RGB', (W, H), (196, 172, 138)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(200 - y * .03), int(176 - y * .03), int(142 - y * .03)))   # exterior plaster
    # interior seen through the door
    d.rectangle((640, 110, 1280, 905), fill=(214, 190, 152))
    d.rectangle((640, 760, 1280, 905), fill=(150, 92, 66))                       # red-oxide floor
    for x in range(640, 1280, 64): d.line([(x, 760), (x - 40, 905)], fill=(138, 84, 60), width=2)
    d.rectangle((1110, 300, 1220, 420), fill=(120, 96, 70)); d.rectangle((1120, 310, 1210, 410), fill=(196, 182, 160))   # framed picture
    d.ellipse((720, 250, 800, 330), fill=(240, 232, 214), outline=(90, 70, 50), width=5)                                  # wall clock
    d.rectangle((660, 640, 900, 770), fill=(92, 110, 120)); d.rectangle((660, 610, 700, 770), fill=(80, 96, 106))         # sofa arm
    # door frame (wood) and an open door leaf
    d.rectangle((610, 80, 1310, 110), fill=(110, 72, 46)); d.rectangle((610, 80, 640, 905), fill=(110, 72, 46)); d.rectangle((1280, 80, 1310, 905), fill=(110, 72, 46))
    d.polygon([(1310, 110), (1450, 70), (1450, 940), (1310, 905)], fill=(122, 82, 52))
    # balcony floor + parapet (foreground) + tulsi pot
    d.rectangle((0, 905, W, 960), fill=(150, 146, 138))
    return paint(im)

def fg_parapet():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 810, W, H), fill=(178, 154, 122, 255)); d.rectangle((0, 796, W, 822), fill=(150, 128, 100, 255))
    for x in range(0, W, 120): d.line([(x, 822), (x, H)], fill=(168, 144, 112, 255), width=2)
    d.ellipse((150, 700, 330, 820), fill=(160, 84, 52, 255)); d.rectangle((170, 740, 310, 806), fill=(160, 84, 52, 255))
    return im.filter(ImageFilter.GaussianBlur(2.2))

def leaves(d, t, cx, cy, sway):
    for i in range(26):
        a = i * 2.39; r = 30 + (i % 7) * 11; s = math.sin(t * 2.1 + i) * sway
        x = cx + math.cos(a) * r * 1.2 + s; y = cy - abs(math.sin(a)) * r * 1.6 - i * 2
        d.ellipse((x - 14, y - 8, x + 14, y + 8), fill=(70 + i % 3 * 12, 112 + i % 4 * 9, 58, 255))

def towels(d, t, sway, y0=40, xs=(820, 1020)):
    d.line([(0, y0), (W, y0 + 14)], fill=(70, 70, 70, 255), width=3)
    for i, (x, col) in enumerate(zip(xs, [(46, 112, 116), (212, 150, 48)])):
        sw = math.sin(t * 1.6 + i * 1.3) * sway
        d.polygon([(x, y0 + 6), (x + 130, y0 + 9), (x + 130 + sw, y0 + 190), (x + sw * .7, y0 + 186)], fill=col + (255,))
        d.line([(x + sw * .7, y0 + 172), (x + 130 + sw, y0 + 176)], fill=(240, 236, 226, 255), width=6)

# ---------------------------------------------------------------- set B: her view out over the parapet
def set_view():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): k = y / H; d.line([(0, y), (W, y)], fill=(int(170 + 50 * k), int(200 + 30 * k), int(226 + 8 * k)))
    # opposite block across the road
    d.rectangle((260, 150, 1660, 900), fill=(226, 212, 186))
    for fl in range(5):
        y = 190 + fl * 140
        d.rectangle((260, y + 96, 1660, y + 112), fill=(150, 110, 80))
        for x in range(320, 1620, 190):
            d.rectangle((x, y, x + 110, y + 86), fill=(96, 92, 88)); d.rectangle((x + 6, y + 6, x + 104, y + 80), fill=(150, 160, 166))
            d.rectangle((x - 14, y + 60, x + 124, y + 70), fill=(60, 56, 54))
    d.rectangle((0, 820, W, 900), fill=(140, 136, 128))   # road edge
    return paint(im)

def fg_rail():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 880, W, H), fill=(180, 156, 124, 255)); d.rectangle((0, 868, W, 888), fill=(150, 128, 100, 255))
    d.rectangle((0, 640, W, 652), fill=(30, 30, 32, 255))
    for x in range(20, W, 64): d.rectangle((x, 652, x + 7, 870), fill=(32, 32, 34, 255))
    for x in range(52, W, 128): d.ellipse((x - 22, 720, x + 22, 764), outline=(32, 32, 34, 255), width=5)
    # small rain-gauge cup on the rail
    d.rectangle((1500, 560, 1550, 642), outline=(210, 220, 228, 255), width=4)
    for k in range(4): d.line([(1505, 580 + k * 16), (1520, 580 + k * 16)], fill=(210, 220, 228, 255), width=2)
    return im.filter(ImageFilter.GaussianBlur(1.6))

# ---------------------------------------------------------------- set C: windowsill close-up and the paper boat
def set_sill():
    im = Image.new('RGB', (W, H), (206, 184, 150)); d = ImageDraw.Draw(im)
    d.rectangle((380, 90, 1540, 700), fill=(236, 232, 222))       # window frame
    d.rectangle((410, 120, 950, 680), fill=(176, 200, 214)); d.rectangle((970, 120, 1510, 680), fill=(176, 200, 214))
    d.rectangle((0, 700, W, 790), fill=(132, 88, 56)); d.rectangle((0, 790, W, 820), fill=(104, 68, 44))   # wooden sill
    return paint(im)
GLASS = np.zeros((H, W), np.float32); GLASS[120:680, 410:950] = 1; GLASS[120:680, 970:1510] = 1
GLASS = ndi.gaussian_filter(GLASS, 2)

def boat(scale=1.0):
    s = 3; w, h = int(420 * scale), int(260 * scale)
    im = Image.new('RGBA', (w * s, h * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * s * scale, y * s * scale) for x, y in pts]
    d.polygon(P([(10, 150), (410, 150), (330, 245), (90, 245)]), fill=(246, 244, 236, 255))        # hull
    d.polygon(P([(90, 150), (210, 20), (330, 150)]), fill=(238, 236, 228, 255))                     # sail
    d.polygon(P([(210, 20), (330, 150), (250, 150)]), fill=(214, 212, 204, 255))                    # sail shade
    d.polygon(P([(10, 150), (90, 245), (130, 150)]), fill=(222, 220, 212, 255))
    for k in range(6):                                                                               # ruled lines
        y = 165 + k * 14; d.line(P([(40 + k * 6, y), (380 - k * 6, y)]), fill=(150, 182, 214, 255), width=2 * s)
    d.line(P([(120, 150), (150, 245)]), fill=(214, 96, 96, 255), width=2 * s)                       # red margin line
    return im.resize((w, h), Image.LANCZOS)

def paste(base, spr, x, y, alpha=1.0, blur=0.0):
    if blur > 0: spr = spr.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1: spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda p: int(p * alpha)))
    base.alpha_composite(spr, (int(x), int(y)))

# ---------------------------------------------------------------- captions (narration stand-in; approved wording)
CAP = {
 'en': [(0.4, 2.9, "Okay, picture a winter morning in Delhi. Mayur Vihar."),
        (2.9, 5.6, "A nine-year-old… let's call her Anu… wants to go down and play."),
        (5.8, 8.6, "But from the balcony, the building across the road has vanished."),
        (8.6, 10.3, "Just grey."),
        (10.6, 14.2, "Her mum shakes her head. Not today. Again."),
        (14.6, 16.8, "So Anu folds a paper boat. For the puddles."),
        (17.0, 19.8, "And Delhi gets… no rain.")],
 'te': [(0.4, 2.9, "ఒక్కసారి ఊహించండి… ఢిల్లీలో ఒక చలికాలం ఉదయం. మయూర్ విహార్."),
        (2.9, 5.6, "వాళ్ల తొమ్మిదేళ్ల పాప… అను… కిందకి వెళ్లి ఆడుకోవాలనుకుంటోంది."),
        (5.8, 8.6, "కానీ balcony నుంచి చూస్తే, ఎదురుగా ఉన్న building కనిపించట్లేదు."),
        (8.6, 10.3, "అంతా బూడిద రంగు."),
        (10.6, 14.2, "అమ్మ తల అడ్డంగా ఊపింది. ఈ రోజు కూడా కాదు. మళ్లీ."),
        (14.6, 16.8, "అను ఒక కాగితం పడవ చేసింది. వాన నీళ్ల కోసం."),
        (17.0, 19.8, "కానీ ఢిల్లీలో… వర్షం పడలేదు.")]}

def caption(img, t):
    for a, b, s in CAP[LANG]:
        if a <= t < b:
            al = min(prog(t, a, a + .15), 1 - prog(t, b - .15, b))
            f = pick(s, 'te' if LANG == 'te' else 'head', 46 if LANG == 'en' else 48)
            while f.getlength(s) > 1500: f = pick(s, 'te' if LANG == 'te' else 'head', f.size - 2)
            tw = f.getlength(s); x = (W - tw) / 2; y = 1010
            sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            ds.text((x, y), s, font=f, fill=(0, 0, 0, int(200 * al)), anchor='ls'); sh = sh.filter(ImageFilter.GaussianBlur(9))
            img.alpha_composite(sh); img.alpha_composite(sh)
            dt = ImageDraw.Draw(img); dt.text((x, y), s, font=f, fill=(255, 255, 255, int(255 * al)), anchor='ls')
            LY.reg('caption', (x, y - 50, x + tw, y + 14), owner='caption')

def tags(img, t):
    LY.badge(img, 'DELHI RAIN · FULL STORY' if LANG == 'en' else 'ఢిల్లీ వర్షం · పూర్తి కథ', 'left', 'tag', y=70)
    f = pick('x', 'monob', 22); d = ImageDraw.Draw(img)
    s1 = 'MOTION TEST · STAND-IN SETS · NO VOICE'
    d.text((W - 64 - f.getlength(s1), 80), s1, font=f, fill=(255, 255, 255, 200), anchor='ls')
    if t < 10.4:   # ILLUSTRATIVE tag on Anu's first appearance
        a = prog(t, 0.6, 1.0) * (1 - prog(t, 9.8, 10.3))
        lab = 'ILLUSTRATIVE EXAMPLE · NOT A REAL PERSON' if LANG == 'en' else 'ఉదాహరణ కోసం మాత్రమే · నిజమైన వ్యక్తి కాదు'
        fl = pick(lab, 'te' if LANG == 'te' else 'monob', 24); tw = fl.getlength(lab)
        d.rounded_rectangle((60, 892, 60 + tw + 36, 940), 10, fill=(10, 10, 10, int(190 * a)))
        d.text((78, 925), lab, font=fl, fill=AMBER + (int(255 * a),), anchor='ls')

# ---------------------------------------------------------------- shots
DOOR, VIEW, SILL = set_door(), set_view(), set_sill()
PARA, RAIL = fg_parapet(), fg_rail()
DOORMASK = np.zeros((H, W), np.float32); DOORMASK[110:905, 640:1280] = 1
ANU_F = scaled(C['anu_front'], 640); ANU_34 = scaled(C['anu_34'], 640).transpose(Image.FLIP_LEFT_RIGHT)
MUM = scaled(C['mum'], 720); BAT = scaled(C['bat'], 280); BOAT = boat(0.9)
T1, T2, T3 = 5.6, 10.4, 14.4

def frame(t):
    if t < T1 or T2 <= t < T3:                                   # outside looking in
        second = t >= T2
        img = DOOR.convert('RGBA'); d = ImageDraw.Draw(img)
        # light through the door cools and dims once the haze has come
        if second:
            mum_x = 560 + 240 * ease(prog(t, T2 + 0.3, T2 + 1.5)); mum_a = prog(t, T2 + 0.2, T2 + 0.6)
            paste(img, MUM, mum_x, 905 - MUM.height + 40 + 4 * math.sin(t * 6) * (1 - prog(t, T2 + 1.3, T2 + 1.6)), mum_a, blur=1.2)
            turn = prog(t, T2 + 1.9, T2 + 2.2)
            if turn < 1:
                paste(img, ANU_F, 960 - ANU_F.width / 2, 1000 - ANU_F.height, 1 - turn)
            if turn > 0:
                paste(img, ANU_34, 930 - ANU_34.width / 2, 1000 - ANU_34.height, turn)
            # the bat goes back against the door frame
            k = ease(prog(t, T2 + 2.1, T2 + 2.9))
            bx = 1000 + (1255 - 1000) * k; by = 720 + (625 - 720) * k
            b = BAT.rotate(-12 * k, expand=True, resample=Image.BICUBIC)
            if turn > 0: paste(img, b, bx, by, min(1, turn * 2))
        else:
            # Anu is in frame from frame 1 (bright, readable opening → DIR-08) and walks towards camera to the threshold;
            # her legs stay hidden behind the parapet, so no fake walk cycle is needed
            enter = ease(prog(t, 0.3, 2.6)); walking = 1 - prog(t, 2.4, 2.7)
            hgt = 470 + 170 * enter; spr = ANU_F.resize((int(ANU_F.width * hgt / ANU_F.height), int(hgt)), Image.LANCZOS)
            spr = spr.rotate(1.6 * math.sin(t * 7.0) * walking, resample=Image.BICUBIC, center=(spr.width / 2, spr.height))
            bob = abs(math.sin(t * 7.0)) * 9 * walking
            cx = 900 + 70 * enter; fy = 900 + 100 * enter
            paste(img, spr, cx - spr.width / 2, fy - spr.height - bob, 1.0, blur=0.8 * (1 - enter))
        img.alpha_composite(PARA)
        d = ImageDraw.Draw(img)
        sway = 26 * (1 - (prog(t, 6.5, 9.5) if not second else 1))
        leaves(d, t, 240, 712, 3 * (1 - (1 if second else 0)))
        towels(d, t, sway if not second else 1.5)
        arr = np.asarray(img.convert('RGB')).astype(np.float32)
        if second:
            arr = arr * np.array([0.9, 0.9, 0.93])                     # cooler, dimmer
            arr = haze(arr, 0.42, t)
        else:
            arr = arr * (1 + 0.04 * math.sin(t))                       # morning light breathes
        img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
    elif t < T2:                                                 # her view: the block disappears
        img = VIEW.convert('RGBA'); arr = np.asarray(img.convert('RGB')).astype(np.float32)
        k = ease(prog(t, T1 + 0.4, T1 + 3.6))
        arr = haze(arr, 1.0 * k, t, density=1.0)
        img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
        rail = RAIL.copy(); d = ImageDraw.Draw(rail)
        towels(d, t, 26 * (1 - prog(t, T1 + 0.6, T1 + 3.2)), y0=10, xs=(140, 1620))
        img.alpha_composite(rail)
        arr = haze(np.asarray(img.convert('RGB')).astype(np.float32), 0.25 * k, t + 3)
        img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
    else:                                                        # the sill and the dry boat
        img = SILL.convert('RGBA')
        arr = np.asarray(img.convert('RGB')).astype(np.float32)
        arr = haze(arr, 0.95, t, mask=GLASS)
        img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
        k = ease(prog(t, T3 + 0.2, T3 + 1.0))
        x = -420 + (760 + 420) * k; y = 520 + 40 * (1 - k)
        sh = Image.new('RGBA', BOAT.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((40, BOAT.height - 40, BOAT.width - 40, BOAT.height - 6), fill=(0, 0, 0, 90))
        paste(img, sh.filter(ImageFilter.GaussianBlur(10)), x, y + 18, k)
        paste(img, BOAT, x, y)
        # dust motes drifting in a weak light shaft: the only movement in a held, still beat (HOLD: the dry boat)
        d = ImageDraw.Draw(img)
        for i in range(26):
            px = (300 + i * 61 + t * 14 * (1 + i % 3)) % W; py = 180 + (i * 97 + t * 9) % 480
            d.ellipse((px, py, px + 3, py + 3), fill=(255, 250, 236, 90))
    LY.reset(); tags(img, t); caption(img, t)
    return img.convert('RGB')

if __name__ == '__main__':
    n = int(DUR * FPS)
    for i in range(n):
        frame(i / FPS).save(f'{FR}/f{i:04d}.jpg', quality=92)
    print('frames', n)
