#!/bin/bash
cd /home/claude/gs4
r(){ L=$1; N=$2; A=$3; B=$4; T=${5:-flap}; TEASE=$T LANGV=$L PLAT=yt python3 render.py $A $B prev/${L}_$N.v.mp4 && ffmpeg -v error -y -i prev/${L}_$N.v.mp4 -ss $A -to $B -i mix_${L}_yt.wav -map 0:v -map 1:a -c:v copy -af "afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($B-$A-0.25)"):d=0.25" -c:a aac -b:a 192k -shortest -movflags +faststart prev/GS4_preview_${N}_${L^^}.mp4 && rm prev/${L}_$N.v.mp4; }
r en 1_money_chain 10.15 32.24 & r te 1_money_chain 12.77 39.98 &
r en 2_famine_to_sea 69.16 104.09 & r te 2_famine_to_sea 87.39 129.28 &
r en 3_tease_alt_rollback 98.96 104.09 roll & r te 3_tease_alt_rollback 123.2 129.28 roll &
wait; ls -la prev
