# ---- series slide (platform specific, phone-readable: 3 items + button)
@functools.lru_cache(1)
def FILM_THUMB():
    return Image.open(f'/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/thumb_golden_sparrow_film_{LANGV.upper()}.jpg').convert('RGB')

def s_slide(t, s0, s1, plat=None):
    plat = plat or PLAT; v = t - s0
    img = radial_bg(W, H, (34, 28, 18), (8, 8, 9), cy=.4, reach=.8).copy()
    tx(img, L('THE GOLDEN SPARROW · SEASON 1', 'బంగారు పిచ్చుక · సీజన్ 1'), W / 2, 250, 40, AMBER, kind='head', maxw=ST.sw)
    rows = [(L('5/6', '5/6'), L("Europe didn't discover India", 'యూరప్ భారత్‌ను కనిపెట్టలేదు'), L("YOU'RE HERE", 'మీరు ఇక్కడ'), True),
            (L('NEXT · 6/6 · FINALE', 'తర్వాత · 6/6 · ముగింపు'), L('The company that came to trade', 'వ్యాపారానికి వచ్చిన కంపెనీ'), L('TOMORROW', 'రేపు'), False)]
    for i, (num, title, tag, here) in enumerate(rows):
        k = e_back(prog(v, .05 + .12 * i, .45 + .12 * i)); y = 350 + i * 180
        if k <= .01: continue
        x0 = 90 + (1 - min(1, k)) * 60
        dark_panel(img, (x0, y, x0 + 900, y + 160), 30, 230, AMBER + (255,) if here else (90, 90, 96, 255))
        text(img, num, x0 + 40, y + 50, 38, AMBER if here else CREAM, 'lm', 'monob')
        text(img, title, x0 + 40, y + 112, 46, CREAM, 'lm', 'head', maxw=560)
        chip(img, tag, x0 + 900 - 40 - pick(tag, 'head', 30).getlength(tag) / 2 - 22, y + 50, 30, AMBER if here else CREAM, INK)
    # full film pointer with the film thumbnail
    k = e_out(prog(v, .35, .75)); y = 735
    if k > .01:
        th = FILM_THUMB(); tw = 760; thh = int(tw * th.height / th.width); thi = th.resize((tw, thh), Image.LANCZOS)
        m = Image.new('L', thi.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, thh - 1), 26, fill=int(255 * k)); img.paste(thi, (160, y), m)
        lab = L('FULL FILM · RELATED VIDEO', 'పూర్తి సినిమా · RELATED VIDEO') if plat == 'yt' else L('FULL FILM ON YOUTUBE · LINK IN BIO', 'పూర్తి సినిమా YouTube లో · LINK IN BIO')
        chip(img, lab, W / 2, y + thh + 45, 38, AMBER, INK, a=k, scale=k)
    # subscribe / follow card
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    CTA.draw(c, t, s0 + 0.9, plat, LANGV, y=1360, t_out=None); surf.flush()
    a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4); rgba = Image.fromarray(a[..., [2, 1, 0, 3]].copy(), 'RGBA')
    img.paste(rgba, (0, 0), rgba)
    return img

@functools.lru_cache(1)
def frame0():
    img = s_hook(0.0, 0.0, 1.0, frame0=True); overlays(img, 0.0, 'hook'); return img

def s_loop(t, s0, s1):
    """slide fades out into frame 0 so the last frame matches the first"""
    k = e_io(prog(t, s0, s0 + 0.4)); b = frame0().copy()   # no zoom on rendered graphics (sharp-pictures rule)
    if k >= 1: return b
    a = s_slide(t, SC_START['slide'], s0); return Image.blend(a, b, k)

SC_START = {n: s for n, s in SC}
def zoom(img, z, cy=.5):
    if z <= 1.0005: return img.copy()
    w, h = W / z, H / z; y0 = min(max(H * cy - h / 2, 0), H - h); return img.resize((W, H), Image.BICUBIC, box=((W - w) / 2, y0, (W + w) / 2, y0 + h))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        ts = [float(x) for x in sys.argv[2].split(',')]; ims = [render(x).resize((270, 480), Image.LANCZOS) for x in ts]
        cols = 6; sh = Image.new('RGB', (cols * 276, ((len(ims) + cols - 1) // cols) * 506), (40, 40, 40)); d = ImageDraw.Draw(sh)
        for i, (x, im) in enumerate(zip(ts, ims)): sh.paste(im, ((i % cols) * 276 + 3, (i // cols) * 506 + 3)); d.text(((i % cols) * 276 + 8, (i // cols) * 506 + 486), f'{x:.1f}', fill='white')
        sh.save(sys.argv[3]); sys.exit()
    if sys.argv[1] == 'one':
        render(float(sys.argv[2])).save(sys.argv[3]); sys.exit()
    a, b, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    f0, f1 = int(round(a * FPS)), int(round(b * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-g', '60', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for f in range(f0, f1): p.stdin.write(render(f / FPS).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out); print('ok', out, f1 - f0)
