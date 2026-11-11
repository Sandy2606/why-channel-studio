# GS 5/6 voice assembly: approved S5 film/Short audio (sentence-level cuts at measured pauses) + approved NEW takes.
import json, subprocess, numpy as np, scipy.io.wavfile as wf
SR=48000; VD='/home/claude/why-channel-studio/videos/2026-11-13_short_gs5_europe_didnt_discover/voice/'
SRC={l:f'/home/claude/gs/out/{l}/GS_S1_S5_{l.upper()}_voice.wav' for l in ('en','te')}
def load(f,ss=None,to=None):
    cmd=['ffmpeg','-v','error','-i',f]+(['-ss',str(ss)] if ss is not None else [])+(['-to',str(to)] if to is not None else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32).copy()
def rms(a):
    x=a[np.abs(a)>0.02]; return float(np.sqrt(np.mean(x**2))) if len(x) else 1e-3
def trim(a,th=0.012,pad=0.04):
    i=np.where(np.abs(a)>th)[0]
    return a[max(0,i[0]-int(pad*SR)):min(len(a),i[-1]+int(pad*SR))] if len(i) else a
# cut points sit inside measured pauses (pauses.py, threshold 0.01) and match the Whisper word times
CUT={'en':{'S5_hook':[(0.00,8.40)],'5.3b':[(15.95,19.80)],'5.5':[(19.92,29.40)],'5.6a':[(29.50,38.65)],
           '5.7':[(42.00,56.05)],'5.8':[(56.48,66.38)],'5.9':[(66.48,74.80)],'tease':[(81.15,88.20)]},
     'te':{'S5_hook':[(0.00,4.60)],'5.3b':[(14.25,17.95)],'5.4':[(18.03,24.80)],'5.5':[(24.85,35.85)],'5.6a':[(35.90,48.55)],
           '5.7':[(53.38,69.30)],'5.8':[(69.70,82.60)],'tease':[(90.60,98.05)]}}
NEW_GAP={'Q1':.40,'Q2':.40,'Q3':.40,'L':.30,'53A':.30,'PILOT':.40,'FORCE':.35,'OLD':.35}
ORDER={'en':['S5_hook','Q1','53A','5.3b','5.5','Q2','5.6a','PILOT','Q3','5.7','5.8','5.9','FORCE','tease','SLIDE','L'],
       'te':['S5_hook','Q1','53A','5.3b','5.4','5.5','Q2','5.6a','PILOT','Q3','5.7','5.8','OLD','FORCE','tease','SLIDE','L']}
if __name__=='__main__':
    rep={}
    for l in ('en','te'):
        ref=load(SRC[l]); R=rms(ref); out=[]; marks={}; t=0.0; lv={}
        for i,k in enumerate(ORDER[l]):
            nxt=ORDER[l][i+1] if i+1<len(ORDER[l]) else None
            if k=='SLIDE': a=np.zeros(int(2.0*SR),np.float32); g=0.0
            elif k in NEW_GAP:
                a=trim(load(VD+f'{l}_{k}.mp3')); lv[k]=round(20*np.log10(rms(a)/R),1); a*=R/rms(a)
                f=int(.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f); g=NEW_GAP[k]
                if k=='53A': g=0.30
                wf.write(VD+f'{l}_{k}_trim.wav',SR,(np.clip(a,-1,1)*32767).astype(np.int16))
            else:
                parts=[]
                for s,e in CUT[l][k]:
                    p=load(SRC[l],s,e); f=int(.008*SR); p[:f]*=np.linspace(0,1,f); p[-f:]*=np.linspace(1,0,f); parts+=[p,np.zeros(int(.30*SR),np.float32)]
                a=np.concatenate(parts[:-1])
                g=0.25 if nxt in ('Q1','Q2','Q3') else (0.20 if k=='tease' else 0.30)
            marks[k]=[round(t,3),round(t+len(a)/SR,3)]; out+=[a,np.zeros(int(g*SR),np.float32)]; t+=len(a)/SR+g
        v=np.clip(np.concatenate(out),-1,1); wf.write(f'voice_{l}.wav',SR,(v*32767).astype(np.int16)); json.dump(marks,open(f'marks_{l}.json','w'),indent=0)
        rep[l]=dict(total=round(t,2),new_take_level_vs_film_dB=lv); print(l,round(t,2),'=',f'{int(t//60)}:{t%60:04.1f}','raw level of new takes vs film (dB):',lv)
    json.dump(rep,open('voice_report.json','w'),indent=1)
