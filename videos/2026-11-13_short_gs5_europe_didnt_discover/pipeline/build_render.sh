cd /home/claude/gs5 && cat head.py scenes.py > render.py && sed -n '/^# ---- series slide/,$p' /home/claude/why-channel-studio/videos/2026-11-12_short_gs4_follow_the_money/pipeline/render_tail.py | sed '/^def s_slide/,/^    return img$/d; /^@functools.lru_cache(1)\ndef frame0/,+2d' > tail.tmp
python3 - <<'PY'
t=open('tail.tmp').read()
i=t.index("if __name__ == '__main__':"); open('render.py','a').write('\n'+t[i:])
PY
rm tail.tmp
