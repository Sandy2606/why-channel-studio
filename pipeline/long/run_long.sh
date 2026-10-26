L=$1; O=out_$L; mkdir -p $O; cd /home/claude/long
python3 render_long.py $L $O audio
python3 render_long.py $L $O part 0 2 & python3 render_long.py $L $O part 1 2 & wait
printf "file 'part0.mp4'\nfile 'part1.mp4'\n" > $O/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $O/audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $O/dussehra_three_stories_$L.mp4
echo DONE $L
