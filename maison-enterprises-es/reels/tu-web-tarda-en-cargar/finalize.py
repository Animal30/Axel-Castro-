#!/usr/bin/env python3
"""Reel (no SFX, no captions) + fitted captions overlay -> SFX mix -> loudnorm -14 -> master + phone copy. No outro (no Maison logo)."""
import subprocess, sys
sys.argv = ["mix.py", "renders", "x", "x"]
exec(open("mix.py").read().split("os.makedirs(\"renders\"")[0])  # defines S, role, mix, EV (reads sfx.json)
OUTDIR = "/mnt/project-files/maison-enterprises-es/tu-web-tarda-en-cargar"
TITLE = "Maison ES - Tu web tarda en cargar"
CAPS = "/root/reel-work/demora/caps/captions.mov"
run = lambda *c: subprocess.run(list(c), check=True)
run("mkdir", "-p", OUTDIR)
run("ffmpeg", "-v", "error", "-y", "-i", "renders/master_nosfx.mp4", "-i", CAPS, "-filter_complex", "[0:v][1:v]overlay=0:0:eof_action=pass,format=yuv420p[v]",
    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-c:a", "copy", "renders/master_cap.mp4")
mix("renders/master_cap.mp4", EV, "renders/reel_sfx.mp4")
M = f"{OUTDIR}/{TITLE} (master).mp4"
run("ffmpeg", "-v", "error", "-y", "-i", "renders/reel_sfx.mp4", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", M)
run("ffmpeg", "-v", "error", "-y", "-i", M, "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUTDIR}/{TITLE} (celular).mp4")
print("done", M)
