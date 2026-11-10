"""GS 1/6 Short covers (1080x1920). Key text kept inside the centre 1080x1350 (Instagram grid crop) and clear of Shorts UI."""
import sys, numpy as np
sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs3'); sys.path.insert(0, '/home/claude/gs/vis')
_a = sys.argv; sys.argv = _a[:1]
import flib as FL
sys.argv = _a
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os; os.environ.setdefault('LANGV', 'en')
W, H = 1080, 1920; B = '/home/claude/why-channel-studio/brand/fonts/'
F_ARCH = lambda s: ImageFont.truetype(B + 'ArchivoBlack-Regular.ttf', s)
F_MONO = lambda s: ImageFont.truetype(B + 'SpaceMono-Bold.ttf', s)
def F_TE(s):
    f = ImageFont.truetype(B + 'NotoSansTelugu.ttf', s, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_name('Black'); return f
lang, plat = sys.argv[1], sys.argv[2]
import cv2
def crop(key, cx, cy, w_, h_, sc):
    a = FL.img(key); h, w = a.shape[:2]; cw, ch = int(w_ / sc), int(h_ / sc); x0 = int(min(max(cx * w - cw / 2, 0), w - cw)); y0 = int(min(max(cy * h - ch / 2, 0), h - ch))
    return cv2.resize(a[y0:y0 + ch, x0:x0 + cw], (w_, h_), interpolation=cv2.INTER_AREA).astype(np.float32)
top = crop('G11', .58, .50, W, 1000, 1000 / 1512 * 1.05); bot = crop('G13', .50, .55, W, 1000, 1000 / 1512 * 1.0)
arr = np.zeros((H, W, 3), np.float32); m = np.clip((np.arange(H) - 880) / 160, 0, 1)[:, None, None]
TT_ = np.zeros((H, W, 3), np.float32); TT_[:1000] = top; BB_ = np.zeros((H, W, 3), np.float32); BB_[920:] = bot[:1000][:H - 920]
arr = TT_ * (1 - m) + BB_ * m
Y = np.mgrid[0:H, 0:W][0] / H; v = 0.55 + 0.45 * np.exp(-((Y - .28) / .18) ** 2)
v = v * np.where(Y > .55, 0.62, 1.0); arr = arr * v[..., None]
fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
def shadow_text(xy, s, font, fill, anchor='mm', sh=10):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=(0, 0, 0, 230), anchor=anchor)
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(sh))); ImageDraw.Draw(fr).text(xy, s, font=font, fill=fill, anchor=anchor)
def gold_text(xy, s, font, anchor='mm'):
    lay = Image.new('L', (W, H), 0); ImageDraw.Draw(lay).text(xy, s, font=font, fill=255, anchor=anchor)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.filter(ImageFilter.GaussianBlur(10)).point(lambda x: int(x * .9))); fr.alpha_composite(sh)
    tt = (np.mgrid[0:H, 0:W][0] / H)[..., None]; g = np.zeros((H, W, 4), np.uint8)
    g[..., :3] = (np.array([255, 220, 130]) * (1 - tt * 1.6).clip(0, 1) + np.array([232, 150, 40]) * (tt * 1.6).clip(0, 1)).astype(np.uint8); g[..., 3] = np.asarray(lay)
    fr.alpha_composite(Image.fromarray(g, 'RGBA'))
if lang == 'en':
    gold_text((W // 2, 1000), 'DIAMONDS', F_ARCH(120)); shadow_text((W // 2, 1110), 'MADE THE LEGENDS', F_ARCH(70), (250, 246, 238))
    gold_text((W // 2, 1330), 'CLOTH', F_ARCH(120)); shadow_text((W // 2, 1440), 'FILLED THE SHIPS', F_ARCH(70), (250, 246, 238))
    sub = 'GOLCONDA · MACHILIPATNAM'; subf = F_MONO(32)
else:
    gold_text((W // 2, 1010), 'వజ్రాలు కథలు', F_TE(110)); shadow_text((W // 2, 1130), 'సృష్టించాయి', F_TE(74), (250, 246, 238))
    gold_text((W // 2, 1340), 'గుడ్డ ఓడలు', F_TE(110)); shadow_text((W // 2, 1460), 'నింపింది', F_TE(74), (250, 246, 238))
    sub = 'గోల్కొండ · మచిలీపట్నం'; subf = F_TE(38)
d = ImageDraw.Draw(fr); d.text((W // 2, 1600), sub, font=subf, fill=(210, 200, 185), anchor='mm')
# brand: WHY? mark + series pill (inside the grid crop)
fw = F_ARCH(54); x0 = 80; d.text((x0, 320), 'WHY', font=fw, fill=(255, 255, 255)); d.text((x0 + d.textlength('WHY', font=fw), 320), '?', font=fw, fill=(246, 166, 35))
pill = 'GOLDEN SPARROW · 3/6' if lang == 'en' else 'బంగారు పిచ్చుక · 3/6'
f = F_MONO(30) if lang == 'en' else F_TE(32); tw = d.textlength(pill, font=f); px = W - 80 - tw - 56
d.rounded_rectangle((px, 322, W - 80, 384), 31, fill=(14, 12, 16, 210), outline=(240, 170, 60, 255), width=3); d.text(((px + W - 80) / 2, 353), pill, font=f, fill=(244, 180, 70), anchor='mm')
out = f'/home/claude/why-channel-studio/videos/2026-11-11_short_gs3_golconda_diamonds/cover_GS3_{lang.upper()}_{plat.upper()}.jpg'
img = fr.convert('RGB')
if plat == 'ig':   # Instagram: same art; add a subtle "FULL FILM ON YOUTUBE" tag low in the frame (outside grid crop, visible in Reel)
    d2 = ImageDraw.Draw(img); t = 'FULL FILM ON YOUTUBE' if lang == 'en' else 'పూర్తి సినిమా YouTube లో'; f2 = F_MONO(30) if lang == 'en' else F_TE(32)
    tw = d2.textlength(t, font=f2); d2.rounded_rectangle((W / 2 - tw / 2 - 30, 1640, W / 2 + tw / 2 + 30, 1700), 30, fill=(240, 170, 60)); d2.text((W / 2, 1670), t, font=f2, fill=(14, 12, 16), anchor='mm')
img.save(out, quality=93); print(out)
