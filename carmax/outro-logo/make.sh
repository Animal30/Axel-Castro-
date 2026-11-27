#!/bin/bash
# Build CarMax 2 s outros: bash make.sh OUTDIR  (needs opencv-python-headless)
set -e; O=$1; mkdir -p "$O"; H=$(dirname "$0"); T=$(mktemp -d)
python3 $H/outro.py A $T/A.mp4 & python3 $H/outro.py B $T/B.mp4 & wait
mux(){ ffmpeg -v error -y -i $T/$1.mp4 -i $H/$2.mp3 -filter_complex "[1:a]atrim=0:2,afade=t=out:st=1.8:d=0.2,loudnorm=I=-14:TP=-1.2:LRA=11,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/$3"; }
mux A sting1 carmax-logo-barrido-con-musica.mp4
mux B sting3 carmax-logo-impacto-con-musica.mp4
cp $T/A.mp4 "$O/carmax-logo-barrido-sin-musica.mp4"; cp $T/B.mp4 "$O/carmax-logo-impacto-sin-musica.mp4"
