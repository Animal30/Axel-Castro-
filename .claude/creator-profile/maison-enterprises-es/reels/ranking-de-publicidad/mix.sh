#!/bin/bash
# voice (cut) + quiet SFX: pop when each card appears, impact when it lands in its row, shine on the S verdict
set -e; P=~/videos/ranking-rank; X=/home/user/Axel-Castro-/.claude/creator-profile/nahuel/assets/sfx
V=~/reel-work/ranking/out/cam_full.mp4; OUT=$1
EV="2.49:pop:-30 9.27:impact:-28 9.67:pop:-30 19.27:impact:-28 19.83:pop:-30 30.27:impact:-28 30.49:pop:-30 39.81:impact:-28 40.31:pop:-30 51.81:impact:-26 51.95:shine:-27"
IN=(-i "$V"); F=""; k=2; L="[v]"
for e in $EV; do t=${e%%:*}; r=${e#*:}; n=${r%%:*}; g=${r#*:}; IN+=(-i "$X/$n.mp3"); ms=$(python3 -c "print(int($t*1000))")
 F+="[$k:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${g}dB,adelay=${ms}|${ms}[s$k];"; L+="[s$k]"; k=$((k+1)); done
F="[1:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=11[v];$F${L}amix=inputs=$((k-1)):normalize=0:duration=first,alimiter=limit=0.89[a]"
ffmpeg -v error -y -i $P/work/_final_v.mp4 "${IN[@]}" -filter_complex "$F" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 320k -ar 48000 -t 57.33 -movflags +faststart "$OUT"
echo done "$OUT"
