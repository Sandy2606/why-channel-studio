cd /home/claude/dl
for pair in "0 1" "2 3"; do
  for p in $pair; do
    if [ ! -f done_te_$p ]; then (LANGV=te python3 render.py $p 4 > log_te_$p.txt 2>&1 && touch done_te_$p) & fi
  done
  wait
done
