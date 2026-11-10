import json,subprocess,numpy as np
SR=48000
def load(f):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
for l in ('en','te'):
    a=load(f'/home/claude/gs/out/{l}/GS_S1_S4_{l.upper()}_voice.wav')
    d=[x for x in json.load(open(f'/home/claude/gs/out/shorts_{l}.json')) if x['short']=='S4'][0]
    hop=int(.01*SR); e=np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)])
    thr=max(e)*0.03
    for k,s,t in d['segments']:
        if k not in ('4.2','4.5','4.6','4.8','S4_tease'): continue
        seg=e[int(s*100):int(t*100)]; quiet=seg<thr; ps=[]; i=0
        while i<len(quiet):
            if quiet[i]:
                j=i
                while j<len(quiet) and quiet[j]: j+=1
                if (j-i)>=18: ps.append((round(s+i/100,2),round(s+j/100,2)))
                i=j
            else: i+=1
        print(l,k,s,t,ps)
