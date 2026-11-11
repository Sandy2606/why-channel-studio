import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
SR=16000
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
m=WhisperModel('/home/claude/models/te_med',device='cpu',compute_type='int8')
for f in sys.argv[1:]:
    a=load(f); w=int(.02*SR); e=np.array([np.sqrt(np.mean(a[i:i+w]**2)) for i in range(0,len(a)-w,w)])
    sil=e<0.01; cuts=[0]; run=0
    for i,s in enumerate(sil):
        run=run+1 if s else 0
        if run==15 and (i*w-cuts[-1])>1.5*SR: cuts.append(i*w-7*w)
    cuts.append(len(a)); print(f, 'pauses at', [round(c/SR,1) for c in cuts])
    for s,e2 in zip(cuts,cuts[1:]):
        segs,_=m.transcribe(a[s:e2],language='te',beam_size=3)
        print(f'  {s/SR:5.1f}-{e2/SR:5.1f}', ' '.join(x.text.strip() for x in segs),flush=True)
