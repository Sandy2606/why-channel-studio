"""splice re-rendered windows into a main part at keyframe boundaries (frame-exact, stream copy)"""
import subprocess, sys
def splice(main, wins, out):
    # wins: list of (a, b, file) with a, b keyframe times (s) in main
    seg = []; pos = 0; tmp = []
    for i, (a, b, f) in enumerate(sorted(wins)):
        fa, fb = round(a * 30), round(b * 30)
        if fa > pos:
            h = f'parts/_seg{i}h.mp4'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{pos / 30:.6f}', '-i', main, '-frames:v', str(fa - pos), '-c', 'copy', h], check=True); seg.append(h)
        seg.append(f); pos = fb
    t = 'parts/_segt.mp4'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{pos / 30:.6f}', '-i', main, '-c', 'copy', t], check=True); seg.append(t)
    open('parts/_join.txt', 'w').write(''.join(f"file '/home/claude/gs6/{s}'\n" for s in seg))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'parts/_join.txt', '-c', 'copy', out], check=True)
if __name__ == '__main__':
    main, out = sys.argv[1], sys.argv[2]; w = sys.argv[3:]
    splice(main, [(float(w[i]), float(w[i + 1]), w[i + 2]) for i in range(0, len(w), 3)], out)
