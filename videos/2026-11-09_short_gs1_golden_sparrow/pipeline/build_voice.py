"""Assemble the S1 voice track per language from reused film-Short audio + new lines; write marks_<l>.json"""
import json, subprocess, numpy as np, scipy.io.wavfile as wf
SR=48000; VD='/home/claude/why-channel-studio/videos/2026-11-09_short_gs1_golden_sparrow/voice/'
SRC={'en':'/home/claude/gs/out/en/GS_S1_S1_EN_voice.wav','te':'/home/claude/gs/out/te/GS_S1_S1_TE_voice.wav'}
def load(f,ss=None,to=None):
    cmd=['ffmpeg','-v','error','-i',f]+(['-ss',str(ss)] if ss is not None else [])+(['-to',str(to)] if to is not None else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32).copy()
def rms(a):
    x=a[np.abs(a)>0.02]; return float(np.sqrt(np.mean(x**2))) if len(x) else 1e-3
seg={l:{s[0]:(s[1],s[2]) for s in [x for x in json.load(open(f'/home/claude/gs/out/shorts_{l}.json')) if x['short']=='S1'][0]['segments']} for l in ('en','te')}
# (key, source, gap_after)
PLAN={'en':[('1.1','r',.35),('1.3','r',.25),('Q1','n',.40),('1.4','r',.18),('1.4e','r',.25),('Q2','n',.45),('1.5','r',.18),('1.6','r',.18),('1.7','r',.25),('Q3','n',.40),('1.8b','r',.45),('T','n',.35),('tease2','r',.20),('SLIDE','s',.0),('L','n',.30)],
      'te':[('1.1','r',.35),('1.3','r',.25),('Q1','n',.40),('1.4','r',.25),('Q2','n',.45),('1.5','r',.18),('1.6','r',.18),('1.7','r',.25),('Q3','n',.40),('1.8b','r',.45),('T','n',.35),('tease2','r',.20),('SLIDE','s',.0),('L','n',.30)]}
SPLIT={'en':{'1.8b':('1.8',2.70,None),'tease2':('S1_tease',4.10,None)},'te':{'1.8b':('1.8',4.00,None),'tease2':('S1_tease',4.29,None)}}
for l in ('en','te'):
    ref=load(SRC[l]); R=rms(ref); out=[]; marks={}; t=0.0
    for k,src,g in PLAN[l]:
        if src=='s': a=np.zeros(int(2.0*SR),np.float32)
        elif src=='n':
            a=load(VD+f'{l}_{k}_trim.wav'); a*=R/rms(a)
            f=int(.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f)
        else:
            if k in SPLIT[l]:
                base,off,_=SPLIT[l][k]; s,e=seg[l][base]; a=load(SRC[l],s+off,e)
            else:
                s,e=seg[l][k]; a=load(SRC[l],s,e)
        marks[k]=[round(t,3),round(t+len(a)/SR,3)]; out.append(a); out.append(np.zeros(int(g*SR),np.float32)); t+=len(a)/SR+g
    v=np.concatenate(out); v=np.clip(v,-1,1)
    wf.write(f'voice_{l}.wav',SR,(v*32767).astype(np.int16)); json.dump(marks,open(f'marks_{l}.json','w'),indent=0)
    print(l,round(t,2),marks)
