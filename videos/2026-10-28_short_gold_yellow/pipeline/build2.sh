#!/bin/bash
set -e
cd /home/claude/g3
for L in en te; do
  (LANGV=$L PLAT=yt python3 render3.py 0 2 r0_${L}_yt.mp4) & (LANGV=$L PLAT=ig python3 render3.py 0 2 r0_${L}_ig.mp4) & wait
done
for L in en te; do for P in yt ig; do
  export LANGV=$L PLAT=$P
  ffmpeg -v error -y -f concat -safe 0 -i cat_${L}_${P}.txt -c copy base_${L}_${P}.mp4
  N0=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['nudge'][0],2))")
  N1=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['nudge'][1],2))")
  EE=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['end']+0.3,2))")
  ffmpeg -v error -y -i base_${L}_${P}.mp4 -loop 1 -i ov3_nudge_${P}.png -loop 1 -i ov3_end_${P}.png -i mix_${L}_${P}.wav -filter_complex "[1:v]format=rgba,fade=t=in:st=${N0}:d=0.2:alpha=1,fade=t=out:st=${N1}:d=0.2:alpha=1[n];[2:v]format=rgba,fade=t=in:st=${EE}:d=0.25:alpha=1[e];[0:v][n]overlay=0:0:enable='between(t,${N0},${N1}+0.2)':shortest=1[v1];[v1][e]overlay=0:0:enable='gte(t,${EE})':shortest=1[v]" -map "[v]" -map 3:a -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart Gold3_${L^^}_${P^^}.mp4
done; done
for f in Gold3_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
