#!/usr/bin/env python3
"""Reel (no SFX render) -> SFX mix -> + Maison outro (with its own SFX) -> master + phone copy."""
import json, os, subprocess, sys
sys.argv = ["mix.py", "renders", "x", "x"]
src_code = open("mix.py").read().split("os.makedirs(\"renders\"")[0]
exec(src_code)  # defines S, role, mix, EV (reads sfx.json)

OUTDIR = "/mnt/project-files/maison-enterprises-es/por-que-tus-anuncios-no-funcionan"
OUTRO = "/mnt/project-files/maison-enterprises-es/brand/maison-cierre-es.mp4"
TITLE = "Maison ES - Por qué tus anuncios no funcionan"
run = lambda *c: subprocess.run(list(c), check=True)

mix("renders/master_cap.mp4", EV, "renders/reel_sfx.mp4")
# outro: SDR 23.976, silent track + its own sound effects
run("ffmpeg", "-v", "error", "-y", "-i", OUTRO, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", "fps=24000/1001,format=yuv420p",
    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-shortest", "renders/outro_silent.mp4")
mix("renders/outro_silent.mp4", [(0.0, "riser", -27), (0.6, "impact", -24), (1.45, "swoosh", -27), (2.6, "shine", -24), (3.6, "pop", -24)], "renders/outro_sfx.mp4")
# join (re-encode so both halves share one stream format)
run("ffmpeg", "-v", "error", "-y", "-i", "renders/reel_sfx.mp4", "-i", "renders/outro_sfx.mp4", "-filter_complex",
    "[0:v]fps=24000/1001,format=yuv420p,setsar=1[v0];[1:v]fps=24000/1001,format=yuv420p,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][ax];[ax]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", f"{OUTDIR}/{TITLE} (master).mp4")
M = f"{OUTDIR}/{TITLE} (master).mp4"
D = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", M]).decode())
BR = int(min(2900, 23 * 8000 / D - 160))
run("ffmpeg", "-v", "error", "-y", "-i", M, "-c:v", "libx264", "-preset", "slow", "-b:v", f"{BR}k", "-maxrate", f"{BR * 5 // 4}k", "-bufsize", "6000k", "-pass", "1", "-passlogfile", "renders/pass", "-an", "-f", "mp4", "/dev/null")
run("ffmpeg", "-v", "error", "-y", "-i", M, "-c:v", "libx264", "-preset", "slow", "-b:v", f"{BR}k", "-maxrate", f"{BR * 5 // 4}k", "-bufsize", "6000k", "-pass", "2", "-passlogfile", "renders/pass", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUTDIR}/{TITLE} (celular).mp4")
print("done", D)
