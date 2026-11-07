#!/bin/bash
# Join the chunks (stream copy, no re-encode), check the frame count, mux the single continuous final mix.
L=$1; U=$(echo $L | tr a-z A-Z); C=/home/claude/gs/film3/out/chunks_$L; F=/home/claude/gs/film3/out/GoldenSparrow_S1_Film_${U}_16x9.mp4
TOT=$(python3 -c "import json;print(json.load(open('/home/claude/gs/out/timeline_$L.json'))['total'])")
N=$(python3 -c "import math;print(math.ceil($TOT/50))"); HAVE=$(ls $C/c[0-9][0-9][0-9].mp4 | wc -l)
[ "$HAVE" = "$N" ] || { echo "MISSING chunks $HAVE/$N"; exit 1; }
ls $C/c[0-9][0-9][0-9].mp4 | sort | sed "s/.*/file '&'/" > $C/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $C/list.txt -i /home/claude/gs/out/$L/GS_S1_film_${U}_v3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart $F
GOT=$(ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 $F)
WANT=$(python3 -c "print(round($TOT*30))")
echo "ASSEMBLED $L frames $GOT expected $WANT"
