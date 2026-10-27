import sys, numpy as np
from epic import font, is_te
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
RED=(226,40,36); WHITE=(255,255,255); AMBER=(255,178,36)
def stroke_text(img,text,xy,px,fill,anchor='la',sw=None,kind=None):
    f=font(kind or ('tesans' if is_te(text) else 'archivo'),px); sw=sw or max(4,px//11)
    sh=Image.new('RGBA',img.size,(0,0,0,0)); ImageDraw.Draw(sh).text((xy[0]+6,xy[1]+8),text,font=f,fill=(0,0,0,200),anchor=anchor,stroke_width=sw,stroke_fill=(0,0,0,200))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(img).text(xy,text,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=(0,0,0))
    return ImageDraw.Draw(img).textbbox(xy,text,font=f,anchor=anchor,stroke_width=sw)
def red_box(img,text,xy,px,anchor='la',rot=-2):
    f=font('tesans' if is_te(text) else 'archivo',px); d=ImageDraw.Draw(img)
    b=d.textbbox((0,0),text,font=f,anchor='la'); w,h=b[2]-b[0]+px*.6,b[3]-b[1]+px*.5
    box=Image.new('RGBA',(int(w),int(h)),RED+(255,)); bd=ImageDraw.Draw(box)
    bd.text((px*.3-b[0],px*.25-b[1]),text,font=f,fill=WHITE)
    box=box.rotate(rot,expand=True,resample=Image.BICUBIC)
    x,y=xy
    if anchor=='ma': x-=box.width/2
    sh=Image.new('RGBA',img.size,(0,0,0,0)); sh.paste((0,0,0,170),(int(x)+8,int(y)+10,int(x)+box.width+8,int(y)+box.height+10)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(box,(int(x),int(y)))
def arrow(img,p0,p1,p2,w=18):
    d=ImageDraw.Draw(img); pts=[]
    for i in range(41):
        t=i/40; pts.append(((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]))
    d.line(pts,fill=(0,0,0),width=w+10,joint='curve'); d.line(pts,fill=RED,width=w,joint='curve')
    import math; dx,dy=pts[-1][0]-pts[-4][0],pts[-1][1]-pts[-4][1]; a=math.atan2(dy,dx); L=w*2.6
    tip=pts[-1]; l=(tip[0]-L*math.cos(a-0.5),tip[1]-L*math.sin(a-0.5)); r=(tip[0]-L*math.cos(a+0.5),tip[1]-L*math.sin(a+0.5))
    d.polygon([tip,l,r],fill=RED,outline=(0,0,0),width=4)
def logo(img,x,y,px=40):
    f=font('archivo',px); d=ImageDraw.Draw(img)
    d.text((x,y),'WHY',font=f,fill=WHITE,stroke_width=3,stroke_fill=(0,0,0)); w=d.textlength('WHY',font=f)
    d.text((x+w+2,y),'?',font=f,fill=AMBER,stroke_width=3,stroke_fill=(0,0,0))
def vignette(img,s=0.5):
    W,H=img.size; yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    a=(np.clip(r-0.6,0,1)*255*s).astype(np.uint8); v=Image.new('RGBA',(W,H),(0,0,0,0)); v.putalpha(Image.fromarray(a)); img.alpha_composite(v)

