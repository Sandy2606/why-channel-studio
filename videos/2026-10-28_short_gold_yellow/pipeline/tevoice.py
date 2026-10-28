import sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0,'/home/claude/sandy2606/why-channel-studio/pipeline/shorts')
import proasm
SR=48000
sr,a=wf.read('take2.wav'); a=a.astype(np.float32)/32768
def seg(s,e):
    x=a[int(s*SR):int(e*SR)].copy(); f=int(.01*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f); return x
BODY=(0.0,75.10); SUB=(75.30,78.85); FOL=(79.05,82.50); COM=(82.80,86.64)
for plat,cta in (('yt',SUB),('ig',FOL)):
    parts=[seg(*BODY),np.zeros(int(.35*SR),np.float32),seg(*cta),np.zeros(int(.12*SR),np.float32),seg(*COM)]
    y=np.concatenate(parts)
    db=proasm.rms_db(y); thr=np.percentile(db,10)+16; med=np.median(db[db>thr])
    proasm.CUTS.clear(); y=proasm.squeeze(y,med-24,maxgap=0.22,keep=0.14)
    off_cta=len(seg(*BODY))+int(.35*SR); off_com=off_cta+len(seg(*cta))+int(.12*SR)
    json.dump({'cuts':proasm.CUTS,'off_cta':off_cta,'off_com':off_com,'body':BODY,'cta':cta,'com':COM},open(f'map_{plat}.json','w'))
    wf.write(f'te_{plat}.raw.wav',SR,(np.clip(y,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'te_{plat}.raw.wav','-af','atempo=1.06','-ar','48000',f'te_{plat}.t.wav'],check=True)
    _,z=wf.read(f'te_{plat}.t.wav'); z=z.astype(np.float32)/32768
    z=proasm.CHAIN(z[None,:],SR)[0]
    wf.write(f'te_{plat}.ch.wav',SR,(np.clip(z,-1,1)*32767).astype(np.int16))
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'te_{plat}.ch.wav','-af','loudnorm=I=-14:TP=-1.0:LRA=6','-ar','48000',f'/home/claude/g3/voice_te_{plat}.wav'],check=True)
    print(plat, len(z)/SR)
