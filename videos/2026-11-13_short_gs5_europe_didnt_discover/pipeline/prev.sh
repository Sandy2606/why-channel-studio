#!/bin/bash
cd /home/claude/gs5
r(){ L=$1; N=$2; A=$3; B=$4; LANGV=$L PLAT=yt python3 render.py $A $B prev/${L}_$N.v.mp4 && ffmpeg -v error -y -i prev/${L}_$N.v.mp4 -ss $A -to $B -i mix_${L}_yt.wav -map 0:v -map 1:a -c:v copy -af "afade=t=in:d=0.08,afade=t=out:st=$(python3 -c "print($B-$A-0.3)"):d=0.3" -c:a aac -b:a 192k -shortest -movflags +faststart prev/GS5_preview_${N}_${L^^}.mp4 && rm prev/${L}_$N.v.mp4; }
rng(){ LANGV=$1 python3 -c "import cues as c;print(round(c.S('53A')-0.45,2), round(c.S('Q2')-0.2,2), round(c.S('5.6a')-0.35,2), round(c.E('PILOT')+0.5,2))"; }
read EA0 EA1 EB0 EB1 <<< $(rng en); read TA0 TA1 TB0 TB1 <<< $(rng te)
echo "EN A $EA0-$EA1 B $EB0-$EB1 | TE A $TA0-$TA1 B $TB0-$TB1"
r en A_ocean_monsoon $EA0 $EA1 & r te A_ocean_monsoon $TA0 $TA1 & wait
r en B_pilot_evidence $EB0 $EB1 & r te B_pilot_evidence $TB0 $TB1 & wait
ls -la prev
