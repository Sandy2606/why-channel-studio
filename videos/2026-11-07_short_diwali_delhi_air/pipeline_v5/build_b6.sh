#!/bin/bash
set -e
cd /home/claude/b7
for L in en te; do for P in yt ig; do
  export LANGV=$L PLAT=$P
  python3 mix_b7.py
  python3 render_b6.py 0 4 r0_${L}_${P}.mp4 & python3 render_b6.py 1 4 r1_${L}_${P}.mp4 & python3 render_b6.py 2 4 r2_${L}_${P}.mp4 & python3 render_b6.py 3 4 r3_${L}_${P}.mp4 & wait
  printf "file r0_${L}_${P}.mp4\nfile r1_${L}_${P}.mp4\nfile r2_${L}_${P}.mp4\nfile r3_${L}_${P}.mp4\n" > cat_${L}_${P}.txt
  ffmpeg -v error -y -f concat -safe 0 -i cat_${L}_${P}.txt -c copy base_${L}_${P}.mp4
  ffmpeg -v error -y -i base_${L}_${P}.mp4 -i mix_${L}_${P}.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart Diwali6_${L^^}_${P^^}.mp4
  echo "done $L $P"
done; done
