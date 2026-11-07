#!/bin/bash
# render one language in 2 parallel halves, concat, mux final mix
L=$1; U=$(echo $L | tr a-z A-Z); O=/home/claude/gs/film/out
TOT=$(python3 -c "import json;print(json.load(open('/home/claude/gs/out/timeline_$L.json'))['total'])")
MID=$(python3 -c "print(round($TOT/2,3))")
cd /home/claude/gs/film
python3 film.py $L seg 0 $MID $O/${L}_a.mp4 > $O/${L}_a.log 2>&1 &
python3 film.py $L seg $MID $TOT $O/${L}_b.mp4 > $O/${L}_b.log 2>&1 &
wait
printf "file '%s'\nfile '%s'\n" $O/${L}_a.mp4 $O/${L}_b.mp4 > $O/${L}_list.txt
ffmpeg -v error -y -f concat -safe 0 -i $O/${L}_list.txt -i /home/claude/gs/out/$L/GS_S1_film_$U.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $O/GoldenSparrow_S1_Film_${U}_16x9.mp4
echo "DONE $L $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/GoldenSparrow_S1_Film_${U}_16x9.mp4)"
