import sys,os
from PIL import Image
sys.argv=['x']; exec(open('render.py').read().split("if __name__ == '__main__':")[0])
ts=[float(x) for x in os.environ['TS'].split(',')]
ims=[render(t).resize((360,640),Image.LANCZOS) for t in ts]
cols=6; sh=Image.new('RGB',(cols*360,((len(ims)+cols-1)//cols)*640))
for i,im in enumerate(ims): sh.paste(im,((i%cols)*360,(i//cols)*640))
sh.save(os.environ['OUT'],quality=85)
