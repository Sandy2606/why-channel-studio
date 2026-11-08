#!/bin/bash
# resumable: skips parts that exist
cd /home/claude/gs1s; mkdir -p parts
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
