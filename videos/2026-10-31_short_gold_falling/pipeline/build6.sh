#!/bin/bash
set -e
cd /home/claude/g6
for L in en te; do for P in yt ig; do
  export LANGV=$L PLAT=$P
  python3 mix6.py
  python3 render6.py 0 2 r0_${L}_${P}.mp4 & python3 render6.py 1 2 r1_${L}_${P}.mp4 & wait
  printf "file r0_${L}_${P}.mp4\nfile r1_${L}_${P}.mp4\n" > cat_${L}_${P}.txt
  ffmpeg -v error -y -f concat -safe 0 -i cat_${L}_${P}.txt -c copy base_${L}_${P}.mp4
  ffmpeg -v error -y -i base_${L}_${P}.mp4 -i mix_${L}_${P}.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart Gold6_${L^^}_${P^^}.mp4
  echo "done $L $P"
done; done
