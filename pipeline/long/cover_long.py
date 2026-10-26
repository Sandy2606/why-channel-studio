import sys; sys.path.insert(0,'/home/claude/elnino')
from PIL import Image, ImageDraw, ImageFilter
from epic import font
W,H=1280,720; M='/home/claude/long/media/'
def panel(name, focus, w):
    s=Image.open(M+name).convert('RGB'); sc=H/s.height*1.15; s=s.resize((int(s.width*sc),int(s.height*sc)),Image.LANCZOS)
    x0=int((s.width-w)*focus[0]); y0=int((s.height-H)*focus[1]); return s.crop((x0,y0,x0+w,y0+H))
def make(lang, out):
    im=Image.new('RGB',(W,H),(10,10,10)); pw=W//3+30
    for i,(n,f) in enumerate([('L_setu.jpg',(.24,.3)),('L_durga_fight.jpg',(.33,.3)),('L_shami.jpg',(.86,.25))]):
        p=panel(n,f,pw); m=Image.new('L',(pw,H),255)
        im.paste(p,(i*(W//3)-15,0))
    d=ImageDraw.Draw(im)
    for i in (1,2):
        x=i*W//3; d.polygon([(x-6,0),(x+14,0),(x-14,H),(x-34,H)],fill=(10,10,10))
    g=Image.new('L',(W,H)); gd=ImageDraw.Draw(g)
    for y in range(H): gd.line((0,y,W,y),fill=int(max(0,(y-300)/420)**1.3*235))
    im.paste(Image.new('RGB',(W,H),(8,8,8)),(0,0),g)
    for i,(lab) in enumerate((['RAMA','DURGA','PANDAVAS'] if lang=='en' else ['రాముడు','దుర్గమ్మ','పాండవులు'])):
        f=font('archivo',38) if lang=='en' else font('tesans',34); cx=i*W//3+W//6
        tw=f.getlength(lab); d.rounded_rectangle((cx-tw/2-18,22,cx+tw/2+18,80),radius=14,fill=(255,178,36)); d.text((cx,51),lab,font=f,fill=(10,10,10),anchor='mm')
    if lang=='en':
        f1=font('archivo',62); f2=font('archivo',150)
        d.text((W/2,470),'DUSSEHRA IS NOT',font=f1,fill=(244,241,234),anchor='mm',stroke_width=6,stroke_fill=(0,0,0))
        d.text((W/2,590),'ONE STORY',font=f2,fill=(255,178,36),anchor='mm',stroke_width=9,stroke_fill=(0,0,0))
    else:
        f1=font('tesans',64); f2=font('tesans',140)
        d.text((W/2,465),'దసరా ఒక్క కథ కాదు',font=f1,fill=(244,241,234),anchor='mm',stroke_width=6,stroke_fill=(0,0,0))
        d.text((W/2,595),'3 కథలు',font=f2,fill=(255,178,36),anchor='mm',stroke_width=9,stroke_fill=(0,0,0))
    d.text((W-26,H-22),'WHY?' if lang=='en' else 'WHY? తెలుగు',font=font('mono',22) if lang=='en' else font('tesans',24),fill=(255,178,36),anchor='rb')
    im.save(out,quality=92)
make('en','cover_long_en.jpg'); make('te','cover_long_te.jpg')
