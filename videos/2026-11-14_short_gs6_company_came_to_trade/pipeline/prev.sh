#!/bin/bash
cd /home/claude/gs6 && ./build_render.sh
r(){ L=$1; N=$2; A=$3; B=$4; LANGV=$L PLAT=yt python3 render.py $A $B prev/${L}_$N.v.mp4 && ffmpeg -v error -y -i prev/${L}_$N.v.mp4 -ss $A -to $B -i mix_${L}_yt.wav -map 0:v -map 1:a -c:v copy -af "afade=t=in:d=0.08,afade=t=out:st=$(python3 -c "print($B-$A-0.3)"):d=0.3" -c:a aac -b:a 192k -shortest -movflags +faststart prev/GS6_preview_${N}_${L^^}.mp4 && rm prev/${L}_$N.v.mp4; }
rng(){ LANGV=$1 python3 -c "import cues as c;d=dict(c.SC);print(round(d['plassey']-0.3,2), round(d['buxar']+0.2,2), round(d['payoff']-0.3,2), round(d['tease']-0.1,2))"; }
read EA0 EA1 EB0 EB1 <<< $(rng en); read TA0 TA1 TB0 TB1 <<< $(rng te)
echo "EN A $EA0-$EA1 B $EB0-$EB1 | TE A $TA0-$TA1 B $TB0-$TB1"
r en A_Plassey $EA0 $EA1 & r te A_Plassey $TA0 $TA1 & wait
ls -la prev
