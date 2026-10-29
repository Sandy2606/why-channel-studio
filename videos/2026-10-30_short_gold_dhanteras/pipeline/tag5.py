def qmark(c, t, x, y, size, morph=0.0):
    host.draw(c, x, y, size, morph=morph, glow=0.8, eye='open', look=(0, 0), brow=0, tilt=3 * math.sin(t * 2), sq=1.0)

TAGS = None
def tag(c):
    global TAGS
    txt = 'GOLD · 5/6' if LANGV == 'en' else 'గోల్డ్ · 5/6'
    if LANGV == 'te':
        if TAGS is None:
            f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 26, layout_engine=ImageFont.Layout.RAQM)
            try: f.set_variation_by_name('Bold')
            except Exception: pass
            im = Image.new('RGBA', (300, 60), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 30), txt, font=f, fill=(244, 241, 234, 255), anchor='lm')
            TAGS = surf_from_pil(im)
        glass_dark(c, 40, 92, 230, 54, 27); glowdot(c, 68, 119, 7); c.set_source_surface(TAGS[0], 88, 89); c.paint(); return
    font(c, 'monob', 24); e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7); c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)
