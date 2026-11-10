"""GS 1/6 Short covers (1080x1920). Key text kept inside the centre 1080x1350 (Instagram grid crop) and clear of Shorts UI."""
import sys, numpy as np
sys.path.insert(0, '/home/claude/gs/film3'); sys.path.insert(0, '/home/claude/gs2'); sys.path.insert(0, '/home/claude/gs/vis')
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
im = Image.open(FL.A['MET1']).convert('RGB'); s_ = max(W / im.width, H / im.height) * 1.25
im = im.resize((int(im.width * s_), int(im.height * s_)), Image.LANCZOS); cx = im.width // 2; cy = int(im.height * .45)
bg = im.crop((cx - W // 2, cy - H // 2, cx + W // 2, cy + H // 2))
arr = np.asarray(bg).astype(np.float32); Y = np.mgrid[0:H, 0:W][0] / H
v = 0.30 + 0.30 * np.exp(-((Y - .36) / .2) ** 2)
arr = arr * v[..., None]; fr = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
def shadow_text(xy, s, font, fill, anchor='mm', sh=10):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).text(xy, s, font=font, fill=(0, 0, 0, 230), anchor=anchor)
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(sh))); ImageDraw.Draw(fr).text(xy, s, font=font, fill=fill, anchor=anchor)
def gold_text(xy, s, font, anchor='mm'):
    lay = Image.new('L', (W, H), 0); ImageDraw.Draw(lay).text(xy, s, font=font, fill=255, anchor=anchor)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.filter(ImageFilter.GaussianBlur(10)).point(lambda x: int(x * .9))); fr.alpha_composite(sh)
    tt = (np.mgrid[0:H, 0:W][0] / H)[..., None]; g = np.zeros((H, W, 4), np.uint8)
    g[..., :3] = (np.array([255, 220, 130]) * (1 - tt * 1.6).clip(0, 1) + np.array([232, 150, 40]) * (tt * 1.6).clip(0, 1)).astype(np.uint8); g[..., 3] = np.asarray(lay)
    fr.alpha_composite(Image.fromarray(g, 'RGBA'))
lay = Image.new('RGBA', (860, 300), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
dl.rounded_rectangle((10, 10, 850, 290), 30, fill=(14, 12, 10, 225), outline=(246, 166, 35, 255), width=14)
t1 = 'LAW PASSED' if lang == 'en' else 'చట్టం ఆమోదం'; f1 = F_ARCH(78) if lang == 'en' else F_TE(80)
dl.text((430, 105), t1, font=f1, fill=(246, 166, 35), anchor='mm'); dl.text((430, 215), '1721', font=F_ARCH(110), fill=(246, 166, 35), anchor='mm')
lay = lay.rotate(-6, expand=True, resample=Image.BICUBIC); fr.alpha_composite(lay, (W // 2 - lay.width // 2, 720 - lay.height // 2))
if lang == 'en':
    shadow_text((W // 2, 1300), 'THE CLOTH', F_ARCH(112), (250, 246, 238))
    gold_text((W // 2, 1425), "EUROPE COULDN'T", F_ARCH(86)); gold_text((W // 2, 1520), 'COPY', F_ARCH(86))
    sub = 'SPINNERS · WEAVERS · DYERS'; subf = F_MONO(32)
else:
    shadow_text((W // 2, 1300), 'యూరప్ కాపీ', F_TE(116), (250, 246, 238))
    gold_text((W // 2, 1445), 'చేయలేని గుడ్డ', F_TE(112))
    sub = 'వడికేవారు · నేతగాళ్లు · రంగులు'; subf = F_TE(36)
d = ImageDraw.Draw(fr); d.text((W // 2, 1600), sub, font=subf, fill=(210, 200, 185), anchor='mm')
# brand: WHY? mark + series pill (inside the grid crop)
fw = F_ARCH(54); x0 = 80; d.text((x0, 320), 'WHY', font=fw, fill=(255, 255, 255)); d.text((x0 + d.textlength('WHY', font=fw), 320), '?', font=fw, fill=(246, 166, 35))
pill = 'GOLDEN SPARROW · 2/6' if lang == 'en' else 'బంగారు పిచ్చుక · 2/6'
f = F_MONO(30) if lang == 'en' else F_TE(32); tw = d.textlength(pill, font=f); px = W - 80 - tw - 56
d.rounded_rectangle((px, 322, W - 80, 384), 31, fill=(14, 12, 16, 210), outline=(240, 170, 60, 255), width=3); d.text(((px + W - 80) / 2, 353), pill, font=f, fill=(244, 180, 70), anchor='mm')
out = f'/home/claude/why-channel-studio/videos/2026-11-10_short_gs2_cloth_world_wanted/cover_GS2_{lang.upper()}_{plat.upper()}.jpg'
img = fr.convert('RGB')
if plat == 'ig':   # Instagram: same art; add a subtle "FULL FILM ON YOUTUBE" tag low in the frame (outside grid crop, visible in Reel)
    d2 = ImageDraw.Draw(img); t = 'FULL FILM ON YOUTUBE' if lang == 'en' else 'పూర్తి సినిమా YouTube లో'; f2 = F_MONO(30) if lang == 'en' else F_TE(32)
    tw = d2.textlength(t, font=f2); d2.rounded_rectangle((W / 2 - tw / 2 - 30, 1640, W / 2 + tw / 2 + 30, 1700), 30, fill=(240, 170, 60)); d2.text((W / 2, 1670), t, font=f2, fill=(14, 12, 16), anchor='mm')
img.save(out, quality=93); print(out)
