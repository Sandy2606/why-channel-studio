import sys, subprocess, cairo, numpy as np, json
sys.path.insert(0,'/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card as C
from PIL import Image
S0, D, T0 = 62.9, 4.4, 63.17
for plat in ('yt','ig'):
    subprocess.run(['ffmpeg','-v','error','-y','-ss','63.4','-i',f'Gold5_EN_{plat.upper()}.mp4','-frames:v','1','/tmp/bg.png'],check=True)
    bg=cairo.ImageSurface.create_from_png('/tmp/bg.png')
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',f'v_{plat}.mp4'],stdin=subprocess.PIPE)
    for i in range(int(D*30)):
        t=S0+i/30; s=cairo.ImageSurface(cairo.FORMAT_ARGB32,1080,1920); c=cairo.Context(s); c.set_source_surface(bg,0,0); c.paint()
        C.draw(c,t,T0,plat,'en',y=1150); s.flush(); p.stdin.write(bytes(s.get_data()))
        if i in (20,36,45,66,80): s.write_to_png(f'/tmp/claude-0/-home-claude/bcdab14f-1073-5a28-b971-b1361e5f0fec/scratchpad/cta_{plat}_{i}.png')
    p.stdin.close(); p.wait()
    # audio: original mix segment + ui sfx
    sr=48000; mix=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(S0),'-t',str(D),'-i',f'mix_en_{plat}.wav','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2).copy()
    for n,t,g in C.events(T0,plat):
        if n=='woosh_air': continue
        a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'/home/claude/why-channel-studio/sfx/{n}.wav','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True).stdout,np.float32).reshape(-1,2)
        hit=json.load(open('/home/claude/why-channel-studio/sfx/catalog.json'))[n]['hit_at']; k=int((t-hit-S0)*sr); j=min(len(mix),k+len(a)); mix[k:j]+=a[:j-k]*g
    import scipy.io.wavfile as wf; wf.write('/tmp/a.wav',sr,np.clip(mix,-1,1))
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'v_{plat}.mp4','-i','/tmp/a.wav','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',f'CTA_test_{plat.upper()}.mp4'],check=True)
print('ok')
