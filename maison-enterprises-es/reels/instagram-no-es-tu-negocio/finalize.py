#!/usr/bin/env python3
"""Depth render (silent) + voice from the cut -> SFX mix -> -14 LUFS master + phone copy. No outro, no logo (Nahuel, 2026-10-26)."""
import json, os, subprocess, sys
sys.argv = ["mix.py", "renders", "x", "x"]
exec(open("mix.py").read().split("os.makedirs(\"renders\"")[0])
OUTDIR = "/mnt/project-files/maison-enterprises-es/instagram-no-es-tu-negocio"; os.makedirs(OUTDIR, exist_ok=True)
TITLE = "Maison ES - Instagram no es tu negocio"; CUT = os.path.expanduser("~/reel-work/promo/cut.mp4")
run = lambda *c: subprocess.run(list(c), check=True)
run("ffmpeg", "-v", "error", "-y", "-i", "renders/v.mp4", "-i", CUT, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "renders/voice.mp4")
mix("renders/voice.mp4", EV, "renders/sfx.mp4")
M = f"{OUTDIR}/{TITLE} (master).mp4"
run("ffmpeg", "-v", "error", "-y", "-i", "renders/sfx.mp4", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", M)
run("ffmpeg", "-v", "error", "-y", "-i", M, "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-maxrate", "4000k", "-bufsize", "8000k", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUTDIR}/{TITLE} (celular).mp4")
print("done")
