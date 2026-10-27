import sys; sys.path.insert(0,'/home/claude/elnino')
from thumbkit import stroke_text, red_box, logo, vignette, WHITE, AMBER
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
W,H=1080,1920
def base(nf):
    neb=Image.open(f'cf/N/{nf:04d}.jpg').convert('RGB')                      # NASA collision glow (band y330-1320)
    neb=neb.crop((0,330,1080,1320)).resize((1500,1375)).crop((210,0,1290,1375))
    bg=Image.new('RGB',(W,H),(6,7,12)); bg.paste(neb,(0,0))
    m=np.zeros((H,W),np.float32); y=np.arange(H); m[:1375]=np.clip((1375-y[:1375])/260,0,1)[:,None]
    bg=Image.composite(bg,Image.new('RGB',(W,H),(6,7,12)),Image.fromarray((m*255).astype(np.uint8)))
    ring=Image.open('cf/R/0060.jpg').convert('RGB').crop((0,420,1080,1240)).resize((1000,760))
    ring=ImageEnhance.Brightness(ring).enhance(1.25)
    lay=Image.new('RGB',(W,H),(0,0,0)); lay.paste(ring,(40,560))
    im=ImageChops.lighter(ImageEnhance.Brightness(bg).enhance(.8),lay).convert('RGBA')
    g=np.zeros((H,W,4),np.uint8); g[...,3]=(np.clip((y-1080)/320,0,1)*230)[:,None]; im.alpha_composite(Image.fromarray(g))
    vignette(im,.45); return im
def cover(lang,out,nf):
    im=base(nf)
    if lang=='en':
        stroke_text(im,'YOUR GOLD IS',(W//2,1170),118,WHITE,anchor='ma')
        red_box(im,'NOT FROM EARTH!',(W//2,1330),90,anchor='ma')
        stroke_text(im,'IT CAME FROM DEAD STARS',(W//2,1530),60,AMBER,anchor='ma')
        stroke_text(im,'GOLD WEEK · 1/6',(W//2,1740),46,WHITE,anchor='ma')
    else:
        stroke_text(im,'మీ గోల్డ్',(W//2,1130),150,WHITE,anchor='ma')
        red_box(im,'భూమిది కాదు!',(W//2,1330),124,anchor='ma')
        stroke_text(im,'చనిపోయిన స్టార్స్ నుంచి వచ్చింది',(W//2,1530),62,AMBER,anchor='ma')
        stroke_text(im,'గోల్డ్ వీక్ · 1/6',(W//2,1740),56,WHITE,anchor='ma')
    logo(im,50,50,64); im.convert('RGB').save(out,quality=92)
nf=int(sys.argv[1]) if len(sys.argv)>1 else 386
cover('en','share/cover_gold1_EN.jpg',nf); cover('te','share/cover_gold1_TE.jpg',nf)
