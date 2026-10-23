# Clics sin ventas (Maison Enterprises ES, guion 1 de 6)

Reel built with business-short-form-reels (HyperFrames). Raw: /mnt/project-files/Video a modificar, clics sin ventas.mp4 (1080x1920 30 fps SDR).

- Raw conformed to 23.976 fps, then cut with edl.json (flubs.json drops the first two hook takes): 93.6 s -> 60.2 s.
- cam_full = the cut as is; cam_top = crop 1080x960 at y=400.
- Captions from phrases.txt (06_captions.py on words_cap.json, "uno por ciento" -> "1%", "Mason" -> "Maison").
- build.py = the reel; finalize.py = SFX mix + Maison outro (maison-cierre-es.mp4) + phone copy.
- Output: /mnt/project-files/maison-enterprises-es/clics-sin-ventas/
