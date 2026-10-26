import sys, json, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0,'/home/claude/long')
from asm import load, env
from faster_whisper import WhisperModel
W=[(2.6,10.6),(10.6,13.2),(18.7,22.8),(96.5,103.0),(144.0,149.8),(156.6,163.6),(193.6,198.2),(241.2,264.7),(281.4,294.3),(301.9,311.1),
(370.8,387.1),(387.1,398.6),(423.7,429.0),(455.7,475.4),(481.6,501.0),(501.2,519.2),(542.3,562.3),(563.0,583.9),(583.9,597.4),(607.8,614.0),
(622.9,637.5),(650.2,661.8),(671.4,689.8),(690.1,712.2),(712.3,725.3),(0,2.6)]
sr,a=load('te_16k'); db,thr=env(a,sr); v=db>thr
m=WhisperModel("/home/claude/models/te_med",device="cpu",compute_type="int8",cpu_threads=2)
for s0,e0 in W:
    i=int(s0*100); n=int(e0*100); G=12; segs=[]
    while i<n:
        if v[i]:
            j=i
            while j<n and (v[j] or v[j:j+G].any()): j+=1
            if (j-i)>=12: segs.append((i/100,j/100))
            i=j
        else: i+=1
    print(f'=== {s0}-{e0}',flush=True)
    for s,e in segs:
        x=a[max(0,int((s-.06)*sr)):int((e+.1)*sr)]
        r,_=m.transcribe(x,language='te',beam_size=5,condition_on_previous_text=False,without_timestamps=True)
        print(f'  {s:7.2f}-{e:7.2f} {" ".join(q.text.strip() for q in r)}',flush=True)
