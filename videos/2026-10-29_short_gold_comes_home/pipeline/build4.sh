#!/bin/bash
set -e
cd /home/claude/g4
for L in en te; do for P in yt ig; do
  export LANGV=$L PLAT=$P
  python3 mix4.py
  python3 render4.py 0 2 r0_${L}_${P}.mp4 & python3 render4.py 1 2 r1_${L}_${P}.mp4 & wait
  printf "file r0_${L}_${P}.mp4\nfile r1_${L}_${P}.mp4\n" > cat_${L}_${P}.txt
  ffmpeg -v error -y -f concat -safe 0 -i cat_${L}_${P}.txt -c copy base_${L}_${P}.mp4
  N0=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['nudge'][0],2))")
  N1=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['nudge'][1],2))")
  EE=$(python3 -c "import json;d=json.load(open('ov_${L}_${P}.json'));print(round(d['end']+0.3,2))")
  ffmpeg -v error -y -i base_${L}_${P}.mp4 -loop 1 -i ov4_nudge_${P}.png -loop 1 -i ov4_end_${P}.png -i mix_${L}_${P}.wav -filter_complex "[1:v]format=rgba,fade=t=in:st=${N0}:d=0.2:alpha=1,fade=t=out:st=${N1}:d=0.2:alpha=1[n];[2:v]format=rgba,fade=t=in:st=${EE}:d=0.25:alpha=1[e];[0:v][n]overlay=0:0:enable='between(t,${N0},${N1}+0.2)':shortest=1[v1];[v1][e]overlay=0:0:enable='gte(t,${EE})':shortest=1[v]" -map "[v]" -map 3:a -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart Gold4_${L^^}_${P^^}.mp4
  echo "done $L $P"
done; done
ls -la Gold4_*.mp4
