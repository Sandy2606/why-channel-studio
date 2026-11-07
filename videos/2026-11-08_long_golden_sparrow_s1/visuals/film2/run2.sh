#!/bin/bash
# final render, video only (audio muxed after the sound pass)
L=$1; O=/home/claude/gs/film2/out
TOT=$(python3 -c "import json;print(json.load(open('/home/claude/gs/out/timeline_$L.json'))['total'])")
MID=$(python3 -c "print(round($TOT/2,3))")
cd /home/claude/gs/film2
python3 film.py $L seg 0 $MID $O/${L}_a.mp4 > $O/${L}_a.log 2>&1 &
python3 film.py $L seg $MID $TOT $O/${L}_b.mp4 > $O/${L}_b.log 2>&1 &
wait
echo "VIDEO DONE $L"
