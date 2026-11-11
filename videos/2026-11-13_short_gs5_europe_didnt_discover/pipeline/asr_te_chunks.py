import subprocess,numpy as np,json
from faster_whisper import WhisperModel
SR=16000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','voice_te.wav','-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
w=int(.02*SR); e=np.array([np.sqrt(np.mean(a[i:i+w]**2)) for i in range(0,len(a)-w,w)])
cuts=[0]; run=0
for i,s in enumerate(e<0.01):
    run=run+1 if s else 0
    if run==12 and (i*w-cuts[-1])>1.2*SR: cuts.append(i*w-5*w)
cuts.append(len(a))
m=WhisperModel('/home/claude/models/te_med',device='cpu',compute_type='int8'); out=[]
for s,e2 in zip(cuts,cuts[1:]):
    segs,_=m.transcribe(a[s:e2],language='te',beam_size=3)
    out.append([s/SR,e2/SR,' '.join(x.text.strip() for x in segs)])
json.dump(out,open('asr_te_chunks.json','w'),ensure_ascii=False,indent=0); print(len(out))
