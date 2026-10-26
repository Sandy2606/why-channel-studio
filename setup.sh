#!/usr/bin/env bash
# Rebuild the Why? production workspace in a fresh session.  Usage: bash setup.sh
set -e
R=$(cd "$(dirname "$0")" && pwd)
pip install --break-system-packages -q faster-whisper pedalboard noisereduce scipy pillow numpy >/dev/null 2>&1 || true
mkdir -p /home/claude/elnino/geo /home/claude/fonts /home/claude/long/sounds /home/claude/long/music
ln -sf $R/pipeline/lib/epic.py /home/claude/elnino/epic.py
ln -sf $R/pipeline/lib/modern.py /home/claude/elnino/modern.py
ln -sf $R/pipeline/lib/countries.geojson /home/claude/elnino/geo/countries.geojson
for f in $R/brand/fonts/*; do ln -sf $f /home/claude/fonts/$(basename $f); done
for f in $R/pipeline/long/*.py; do ln -sf $f /home/claude/long/$(basename $f); done
ln -sf $R/pipeline/long/run_long.sh /home/claude/long/run_long.sh
# sounds: library (sfx_*.wav names expected by render_long) + ambience beds
for f in $R/sfx/*.wav; do ln -sf $f /home/claude/long/sounds/$(basename $f); done
for a in fire crowd drums; do ffmpeg -v error -y -i $R/sfx/amb_$a.mp3 -ar 48000 -ac 2 /home/claude/long/sounds/$a.wav; done
# music beds as 48 kHz wav
for f in $R/music/*.mp3; do ffmpeg -v error -y -i $f -ar 48000 -ac 2 /home/claude/long/music/$(basename ${f%.mp3}).wav; done
echo "Workspace ready. Telugu ASR model: download kavithajohn/whisper-telugu-medium-ct2 to /home/claude/models/te_med if needed."
