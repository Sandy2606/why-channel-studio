#!/bin/bash
# Resumable render: 50 s chunks (1500 frames at 30 fps), 2 workers.
# A chunk is written to *.tmp.mp4 and renamed only when complete, so after any interruption
# re-running this script skips finished chunks and redoes only the unfinished ones.
L=$1; O=/home/claude/gs/film3/out/chunks_$L; mkdir -p $O; cd /home/claude/gs/film3
TOT=$(python3 -c "import json;print(json.load(open('/home/claude/gs/out/timeline_$L.json'))['total'])")
N=$(python3 -c "import math;print(math.ceil($TOT/50))")
job() { L=$1; k=$2; TOT=$3; O=$4; f=$(printf "%s/c%03d.mp4" $O $k)
  [ -s "$f" ] && exit 0
  a=$((k*50)); b=$(python3 -c "print(min($TOT, ($k+1)*50))")
  python3 film.py $L seg $a $b ${f%.mp4}.tmp.mp4 > ${f%.mp4}.log 2>&1 && mv ${f%.mp4}.tmp.mp4 $f; }
export -f job
seq 0 $((N-1)) | xargs -P 2 -I{} bash -c "job $L {} $TOT $O"
ls $O/c*.mp4 | grep -v tmp | sort | sed "s/.*/file '&'/" > $O/list.txt
echo "CHUNKS $L $(grep -c . $O/list.txt)/$N"
