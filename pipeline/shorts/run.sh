cd /home/claude/sun
r(){ L=$1; P=$2; D=out_${L}_$P; mkdir -p $D; export MUSIC=meridian PLAT=$P; python3 render_sun.py $L $D audio && python3 render_sun.py $L $D part 0 1 && ffmpeg -v error -y -i $D/part0.mp4 -i $D/audio.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $D/why_burn_ravana_${L^^}_${P^^}.mp4 && echo FIN $D; }
r en yt > l_en_yt.log 2>&1 & r te yt > l_te_yt.log 2>&1 & wait
r en ig > l_en_ig.log 2>&1 & r te ig > l_te_ig.log 2>&1 & wait
cat l_*.log
