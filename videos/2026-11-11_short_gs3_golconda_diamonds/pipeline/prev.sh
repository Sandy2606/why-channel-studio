#!/bin/bash
cd /home/claude/gs3
r(){ L=$1; N=$2; A=$3; B=$4; LANGV=$L PLAT=yt python3 render.py $A $B prev/${L}_$N.v.mp4 && ffmpeg -v error -y -i prev/${L}_$N.v.mp4 -ss $A -to $B -i mix_${L}_yt.wav -map 0:v -map 1:a -c:v copy -af "afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($B-$A-0.25)"):d=0.25" -c:a aac -b:a 192k -shortest -movflags +faststart prev/GS3_preview_${N}_${L^^}.mp4 && rm prev/${L}_$N.v.mp4; }
r en A_opening 0 10.2 & r te A_opening 0 8.8 & wait
r en B_payoff 43.4 59.9 & r te B_payoff 50.9 71.0 & wait
r en C_port 70.3 85.9 & r te C_port 83.5 101.1 & wait
ls -la prev
