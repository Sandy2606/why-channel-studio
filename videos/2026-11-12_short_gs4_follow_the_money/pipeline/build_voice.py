import json, subprocess, numpy as np, scipy.io.wavfile as wf
SR=48000; VD='/home/claude/why-channel-studio/videos/2026-11-12_short_gs4_follow_the_money/voice/'
SRC={l:f'/home/claude/gs/out/{l}/GS_S1_S4_{l.upper()}_voice.wav' for l in ('en','te')}
def load(f,ss=None,to=None):
    cmd=['ffmpeg','-v','error','-i',f]+(['-ss',str(ss)] if ss is not None else [])+(['-to',str(to)] if to is not None else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32).copy()
def rms(a):
    x=a[np.abs(a)>0.02]; return float(np.sqrt(np.mean(x**2))) if len(x) else 1e-3
def trim(a,th=0.012,pad=0.04):
    i=np.where(np.abs(a)>th)[0]
    return a[max(0,i[0]-int(pad*SR)):min(len(a),i[-1]+int(pad*SR))] if len(i) else a
# reused pieces: key -> list of (start,end) in the approved S4 voice (sentence boundaries, ASR-verified)
CUT={'en':{'S4_hook':[(0.15,6.63)],'MONEY':[(39.70,40.67)],'4.6a':[(40.85,54.30)],'4.8a':[(59.08,69.95)],
           '4.2t':[(9.45,11.12),(21.60,27.30)],'4.4':[(27.48,36.23)],'SYSTEM':[(36.41,39.35)],
           '4.9':[(73.34,78.27)],'4.10':[(78.45,93.34)],'tease2':[(101.80,106.43)]},
     'te':{}}
NEW_GAP={'Q1':.40,'Q2':.40,'Q3':.40,'L':.30,'FARMAN':.35,'VIRJI':.35,'TURN':.30,'MADANNA':.35}
ORDER={'en':['S4_hook','Q1','MONEY','4.6a','FARMAN','4.8a','VIRJI','Q2','4.2t','4.4','SYSTEM','Q3','4.9','4.10','TURN','tease2','SLIDE','L'],
       'te':['S4_hook','Q1','MONEY','4.6a','FARMAN','MADANNA','4.8a','VIRJI','Q2','4.2t','SYSTEM','Q3','4.9','4.10','TURN','tease2','SLIDE','L']}
if __name__=='__main__':
    import sys
    CUT['te']=json.load(open('cut_te.json'))
    for l in ('en','te'):
        ref=load(SRC[l]); R=rms(ref); out=[]; marks={}; t=0.0
        for i,k in enumerate(ORDER[l]):
            nxt=ORDER[l][i+1] if i+1<len(ORDER[l]) else None
            if k=='SLIDE': a=np.zeros(int(2.0*SR),np.float32); g=0.0
            elif k in NEW_GAP:
                a=trim(load(VD+f'{l}_{k}.mp3')); a*=R/rms(a); f=int(.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f); g=NEW_GAP[k]
                wf.write(VD+f'{l}_{k}_trim.wav',SR,(np.clip(a,-1,1)*32767).astype(np.int16))
            else:
                parts=[]
                for s,e in CUT[l][k]:
                    p=load(SRC[l],s,e); f=int(.008*SR); p[:f]*=np.linspace(0,1,f); p[-f:]*=np.linspace(1,0,f)
                    parts+=[p,np.zeros(int(.30*SR),np.float32)]
                a=np.concatenate(parts[:-1])
                g=0.25 if nxt in ('Q1','Q2','Q3') else (0.20 if k=='tease2' else 0.30)
                if k=='S4_hook': g=0.30
            marks[k]=[round(t,3),round(t+len(a)/SR,3)]; out+=[a,np.zeros(int(g*SR),np.float32)]; t+=len(a)/SR+g
        v=np.clip(np.concatenate(out),-1,1); wf.write(f'voice_{l}.wav',SR,(v*32767).astype(np.int16)); json.dump(marks,open(f'marks_{l}.json','w'),indent=0)
        print(l,round(t,2),'=',f'{int(t//60)}:{t%60:04.1f}')
