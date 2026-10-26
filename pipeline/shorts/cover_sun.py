import sys; sys.path.insert(0,'/home/claude/elnino')
from thumb3 import stroke_text, red_box, logo, vignette, WHITE, AMBER
from PIL import Image, ImageDraw
import numpy as np
W,H=1080,1920
def cover(lang,out):
    im=Image.open('/home/claude/sun/media/AI09_Ravana_inside_us_shadow_9x16.png').convert('RGB')
    s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1)).crop((0,0,W,H)).convert('RGBA')
    g=np.zeros((H,W,4),np.uint8); y=np.linspace(0,1,H); g[...,3]=(np.clip((y-.45)/.35,0,1)*235)[:,None]; im.alpha_composite(Image.fromarray(g))
    vignette(im,.5)
    if lang=='en':
        stroke_text(im,'NOT IN THE',(W//2,1190),120,WHITE,anchor='ma')
        red_box(im,'RAMAYANA!',(W//2,1350),140,anchor='ma')
        stroke_text(im,'SO WHY BURN HIM?',(W//2,1550),84,AMBER,anchor='ma')
        stroke_text(im,'DUSSEHRA SERIES · FINAL PART',(W//2,1740),44,WHITE,anchor='ma')
    else:
        stroke_text(im,'రామాయణంలో',(W//2,1150),140,WHITE,anchor='ma')
        red_box(im,'లేదు!',(W//2,1330),130,anchor='ma')
        stroke_text(im,'మరి ఎందుకు కాలుస్తాం?',(W//2,1520),88,AMBER,anchor='ma')
        stroke_text(im,'దసరా సిరీస్ · చివరి పార్ట్',(W//2,1740),56,WHITE,anchor='ma')
    d=ImageDraw.Draw(im); d.rounded_rectangle((W-300,60,W-40,104),radius=10,fill=(0,0,0,170))
    from modern import mono; mono(im,'AI ILLUSTRATION',W-170,82,20,(244,241,234))
    logo(im,50,50,64)
    im.convert('RGB').save(out,quality=92)
cover('en','/home/claude/sun/share/cover_sunday_EN.jpg'); cover('te','/home/claude/sun/share/cover_sunday_TE.jpg')
