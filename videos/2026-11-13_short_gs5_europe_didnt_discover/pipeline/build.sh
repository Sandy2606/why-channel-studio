#!/bin/bash
# resumable: skips parts that exist
cd /home/claude/gs5; mkdir -p parts
for L in en te; do
  SL=$(LANGV=$L python3 -c "import cues;print(dict(cues.SC)['slide'])"); DUR=$(LANGV=$L python3 -c "import cues;print(cues.DUR)")
  MID=$(python3 -c "print(round($SL/2*30)/30)")
  [ -f parts/${L}_a1.mp4 ] || LANGV=$L PLAT=yt python3 render.py 0 $MID parts/${L}_a1.mp4 &
  [ -f parts/${L}_a2.mp4 ] || LANGV=$L PLAT=yt python3 render.py $MID $SL parts/${L}_a2.mp4 &
  wait
  [ -f parts/${L}_yt.mp4 ] || LANGV=$L PLAT=yt python3 render.py $SL $DUR parts/${L}_yt.mp4 &
  [ -f parts/${L}_ig.mp4 ] || LANGV=$L PLAT=ig python3 render.py $SL $DUR parts/${L}_ig.mp4 &
  wait
  echo "video done $L"
done
mkdir -p out
for L in en te; do
  for P in yt ig; do
    printf "file 'parts/${L}_a1.mp4'\nfile 'parts/${L}_a2.mp4'\nfile 'parts/${L}_${P}.mp4'\n" > cat_${L}_${P}.txt
    ffmpeg -v error -y -f concat -safe 0 -i cat_${L}_${P}.txt -c copy parts/${L}_${P}_v.mp4
    ffmpeg -v error -y -i parts/${L}_${P}_v.mp4 -i mix_${L}_${P}.wav -map 0:v -map 1:a -c:v copy -af "volume=-0.6dB,alimiter=limit=0.79:level=false" -c:a aac -b:a 192k -shortest -movflags +faststart out/GoldenSparrow5_${L^^}_${P^^}.mp4
  done
done
ls -la out
