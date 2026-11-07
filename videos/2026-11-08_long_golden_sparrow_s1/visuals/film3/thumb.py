"""Golden Sparrow S1 film thumbnail: six chapter photos as a contact sheet, undivided subcontinent in gold, channel branding."""
import sys, json, math
sys.path.insert(0, '/home/claude/gs/film3')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import flib as FL
from shapely.geometry import shape
from shapely.ops import unary_union
W, H = 1280, 720; B = '/home/claude/why-channel-studio/brand/fonts/'
F_ARCH = lambda s: ImageFont.truetype(B + 'ArchivoBlack-Regular.ttf', s)
F_MONO = lambda s: ImageFont.truetype(B + 'SpaceMono-Bold.ttf', s)
def F_TE(s):
    f = ImageFont.truetype(B + 'NotoSansTelugu.ttf', s, layout_engine=ImageFont.Layout.RAQM); f.set_variation_by_name('Black'); return f
lang = sys.argv[1]
# ---- background: contact sheet of the six chapter-card photos
PH = [('PD03', .45, .17, 2.2), ('G01', .5, .55, 1.4), ('MET1', .47, .40, 2.2), ('G09', .07, .75, 3.6), ('G16', .30, .48, 1.8), ('T1', .5, .55, 1.3)]
bg = Image.new('RGB', (W, H), (12, 10, 14)); cw, ch = W // 3, H // 2
for k, (key, fx, fy, z) in enumerate(PH):
    a = FL.img(key); h, w = a.shape[:2]; tw = int(w / z); th = int(tw * ch / cw)
    x0 = max(0, min(w - tw, int(fx * w) - tw // 2)); y0 = max(0, min(h - th, int(fy * h) - th // 2))
    tile = Image.fromarray(a[y0:y0 + th, x0:x0 + tw]).resize((cw - 6, ch - 6), Image.LANCZOS)
    bg.paste(tile, ((k % 3) * cw + 3, (k // 3) * ch + 3))
arr = np.asarray(bg).astype(np.float32)
Y, X = np.mgrid[0:H, 0:W]; v = np.clip(0.16 + 0.62 * (X / W) ** 1.1, 0, 1) * (1 - 0.35 * ((Y - H / 2) / H * 2) ** 2)   # dark on the text side
arr = arr * v[..., None] * np.array([1.0, 0.92, 0.8]); fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
# ---- foreground: the undivided subcontinent (India + Pakistan + Bangladesh), gold
sys.path.insert(0, '/home/claude/gs/vis'); import gsmap
svg = [list(q) for q in gsmap.india_polys() if len(q) > 2] + [q for n in ('Pakistan', 'Bangladesh') for q in gsmap.polys(n) if len(q) > 2]
xs = [x for q in svg for x, y in q]; ys = [y for q in svg for x, y in q]
bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
sc = min(470 / (bx1 - bx0), 640 / (by1 - by0)); ox = 1258 - (bx1 - bx0) * sc - bx0 * sc; oy = 36 - by0 * sc
T = lambda q: [(x * sc + ox, y * sc + oy) for x, y in q]
mask = Image.new('L', (W, H), 0); md = ImageDraw.Draw(mask)
for q in svg: md.polygon(T(q), fill=255)
glow = mask.filter(ImageFilter.GaussianBlur(26)); gl = Image.new('RGBA', (W, H), (255, 190, 80, 0)); gl.putalpha(glow.point(lambda x: int(x * 0.75))); fr.alpha_composite(gl)
grad = np.zeros((H, W, 4), np.uint8); t_ = (np.mgrid[0:H, 0:W][0] / H)[..., None]
grad[..., :3] = (np.array([255, 214, 120]) * (1 - t_) + np.array([196, 120, 30]) * t_).astype(np.uint8); grad[..., 3] = np.asarray(mask)
gold = Image.fromarray(grad, 'RGBA'); tex = np.asarray(FL.img('MET1').mean(2)); tex = cv2.resize(tex, (W, H)).astype(np.float32)
g2 = np.asarray(gold).astype(np.float32); g2[..., :3] *= (0.86 + 0.14 * (tex / 255.0))[..., None]; gold = Image.fromarray(g2.astype(np.uint8), 'RGBA')
fr.alpha_composite(gold)
od = ImageDraw.Draw(fr)
from PIL import ImageChops
edge = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(5)), mask); fr.paste((120, 70, 16, 255), (0, 0), edge)
# ---- text + branding
def shadow_text(xy, s, font, fill, sh=8):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=(0, 0, 0, 220))
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(sh))); ImageDraw.Draw(fr).text(xy, s, font=font, fill=fill)
def gold_text(xy, s, font):
    lay = Image.new('L', (W, H), 0); ImageDraw.Draw(lay).text(xy, s, font=font, fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.filter(ImageFilter.GaussianBlur(9)).point(lambda x: int(x * 0.9))); fr.alpha_composite(sh)
    gg = np.zeros((H, W, 4), np.uint8); tt = (np.mgrid[0:H, 0:W][0] / H)[..., None]
    gg[..., :3] = (np.array([255, 216, 120]) * (1 - tt) + np.array([232, 150, 40]) * tt).astype(np.uint8); gg[..., 3] = np.asarray(lay); fr.alpha_composite(Image.fromarray(gg, 'RGBA'))
if lang == 'en':
    shadow_text((60, 175), 'OUR TRUTH', F_ARCH(112), (250, 246, 238))
    gold_text((60, 305), 'BEFORE', F_ARCH(112)); gold_text((60, 430), 'BRITISH', F_ARCH(112))
    pill = 'THE GOLDEN SPARROW · S1'
else:
    shadow_text((56, 170), 'బ్రిటిష్', F_TE(120), (250, 246, 238))
    gold_text((56, 320), 'రాకముందు', F_TE(110)); gold_text((56, 455), 'మన నిజం', F_TE(110))
    pill = 'THE GOLDEN SPARROW · S1'
d = ImageDraw.Draw(fr); f = F_MONO(26); tw = d.textlength(pill, font=f)
d.rounded_rectangle((60, 600, 60 + tw + 52, 652), 26, fill=(14, 12, 16, 200), outline=(240, 170, 60, 255), width=3); d.text((86, 608), pill, font=f, fill=(244, 180, 70))
fw = F_ARCH(46); d.text((52, 44), 'WHY', font=fw, fill=(255, 255, 255)); d.text((52 + d.textlength('WHY', font=fw), 44), '?', font=fw, fill=(246, 166, 35))
out = f'/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/thumb_golden_sparrow_film_{lang.upper()}.jpg'
fr.convert('RGB').save(out, quality=92); print(out)
