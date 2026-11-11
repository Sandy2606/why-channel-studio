import sys,subprocess,numpy as np
SR=16000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32)
w=int(.01*SR); e=np.array([np.sqrt(np.mean(a[i:i+w]**2)) for i in range(0,len(a)-w,w)])
th=float(sys.argv[2]) if len(sys.argv)>2 else 0.01; lo,hi=(float(x) for x in sys.argv[3:5]) if len(sys.argv)>4 else (0,1e9)
s=None; out=[]
for i,v in enumerate(np.append(e,1)):
    if v<th and s is None: s=i
    elif v>=th and s is not None:
        if i-s>=18 and lo<=s/100<=hi: out.append(f'{s/100:.2f}-{i/100:.2f}({(i-s)/100:.2f})')
        s=None
print(' '.join(out))
