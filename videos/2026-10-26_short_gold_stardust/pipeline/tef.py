import numpy as np,scipy.io.wavfile as wf,sys
from faster_whisper import WhisperModel
_,a=wf.read("rec/te_16k.wav"); a=a.astype(np.float32)/32768
h=160; n=len(a)//h; db=20*np.log10(np.sqrt((a[:n*h].reshape(n,h)**2).mean(1))+1e-9)
thr=np.percentile(db,10)+16; v=db>thr
# islands split by >=0.14s silence
isl=[];i=0
while i<n:
    if v[i]:
        j=i;gap=0
        while j<n and (v[j] or gap<14):
            gap=0 if v[j] else gap+1; j+=1
        isl.append((i/100,(j-gap)/100)); i=j
    else: i+=1
m=WhisperModel("/home/claude/models/te_med",device="cpu",compute_type="int8",cpu_threads=4)
W=[tuple(map(float,x.split('-'))) for x in sys.argv[1:]]
for s,e in isl:
    if e-s<0.12 or not any(s<b and e>a0 for a0,b in W): continue
    x=a[max(0,int((s-.06)*16000)):int((e+.1)*16000)]
    r,_=m.transcribe(x,language="te",beam_size=5,condition_on_previous_text=False,without_timestamps=True)
    print(f"{s:7.2f}-{e:7.2f} {' '.join(q.text.strip() for q in r)}",flush=True)
