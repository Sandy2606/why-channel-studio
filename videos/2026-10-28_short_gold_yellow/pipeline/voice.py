import sys, json, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0,'/home/claude/sandy2606/why-channel-studio/pipeline/shorts')
import proasm
proasm.ROOT='/home/claude/g3/'
BASE=[
 (2.43,9.46,'raw'), # 0 look at every metal ... silver or grey
 (9.9,11.92),     # 1 gold is the only one that's yellow
 (14.2,17.15),    # 2 I always thought that was just how gold is
 (18.75,20.75),   # 3 turns out the answer is Einstein
 (29.9,34.36),    # 4 a gold atom is huge ... electrons
 (43.15,45.9),    # 5 that some of them move at over half the speed of light
 (53.85,59.62),   # 6 at that speed ... pulled in closer
 (67.35,69.72),   # 7 and that changes which light gold soaks up
 (72.7,77.52),    # 8 gold swallows the blue and white light minus blue looks warm yellow
 (106.9,112.86),  # 9 silver has the same setup ... bounces back everything
 (114.5,115.26),  # 10 which means
 (127.2,130.25),  # 11 without relativity gold would look just like silver
 (131.6,132.86),  # 12 and it's not just gold
 (149.95,153.98), # 13 in 2013 scientists showed ... mercury is a liquid
 (154.5,157.42),  # 14 without it ... 105 degrees higher
 (163.35,166.25,'raw'), # 15 the full gold story is out now on our channel
]
CTA={'ig':(168.55,171.55,'raw'),'yt':(171.95,175.0)}
COMMENT=(180.4,182.35)
PAUSE={3:0.30,4:0.25,6:0.2,9:0.3,10:0.45,11:0.35,12:0.45,15:0.45}
for plat in ('yt','ig'):
    keep=BASE+[CTA[plat],COMMENT]
    proasm.build('g3',keep,f'/home/claude/g3/v0_{plat}.wav',gap=0.07)
    sr,y=wf.read(f'v0_{plat}.wav'); m=json.load(open(f'v0_{plat}.wav.map.json'))
    out=[];last=0;starts=[];shift=0
    for i,p in enumerate(m):
        s=p[0]
        if i in PAUSE:
            k=int(s*sr); out+= [y[last:k], np.zeros(int(PAUSE[i]*sr),y.dtype)]; last=k; shift+=PAUSE[i]
        starts.append(round(s+shift,2))
    out.append(y[last:]); v=np.concatenate(out); wf.write(f'voice_{plat}.wav',sr,v)
    json.dump(starts,open(f'starts_{plat}.json','w')); print(plat, len(v)/sr)
