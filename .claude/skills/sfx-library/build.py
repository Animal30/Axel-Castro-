#!/usr/bin/env python3
"""Build the agency's curated SFX library from manifest.json (CC0 sounds found through Openverse).

  python build.py                 # download what is missing, measure, keep the best per role, write the library
  python build.py --keep 3        # sounds kept per role (default: the manifest's "keep", else 3)
  python build.py --dry-run       # list what would be downloaded

Each manifest entry is a candidate. Every candidate is downloaded, converted to 48 kHz WAV, its leading silence
trimmed and its peak set to -1 dBFS, then measured. Candidates that fail a check (clipped, too long or too short for
their role, a noisy tail, a slow start on a sound that must start at once) are dropped; the rest are ranked per role
and the best are kept. Output, at the repository root:

  sounds/library/<role>/<name>.wav   the kept sounds
  sounds/library/catalog.json        type / file / source rows, read by real-sfx's build_index.py
  sounds/library/CREDITS.md          title, author, licence and link of every kept sound
  sounds/library/report.json         every candidate with its measurements and why it was kept or dropped

Then it points real-sfx at the library (config.json + index) when real-sfx is installed next to this skill.
Freesound refuses downloads from cloud machines: run this on your own computer, then commit sounds/library.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
LIB = REPO / "sounds" / "library"
REAL_SFX = HERE.parent / "real-sfx"
UA = {"User-Agent": "agency-sfx-library/1.0 (+https://github.com/Animal30/Axel-Castro-)"}
SR = 48000

# Per role: allowed length in seconds after trimming, and whether the sound must start at once (attack check).
ROLE_RULES = {
    "whoosh": (0.25, 2.5, False), "riser": (1.0, 8.0, False), "impact": (0.15, 6.0, True),
    "sub_drop": (0.4, 6.0, True), "pop": (0.03, 0.8, True), "click": (0.02, 0.6, True),
    "typing": (0.8, 12.0, True), "ui": (0.05, 2.5, True), "chime": (0.15, 4.0, True),
    "camera": (0.05, 2.0, True), "coin": (0.1, 4.0, True), "glitch": (0.1, 3.0, False),
    "foley": (0.1, 6.0, False), "paper": (0.2, 4.0, False), "error": (0.1, 2.0, True),
}
# real-sfx reads the catalog "type" as its pack type; roles it has no pack type for go by the words of the source
PACK_TYPE = {"impact": "impact", "sub_drop": "impact", "coin": "other"}


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40] or "sound"


def download(url, dst):
    if dst.exists() and dst.stat().st_size > 0:
        return
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                dst.write_bytes(r.read())
            return
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def to_wav(src, dst):
    # leading silence below -50 dBFS out, peak to -1 dBFS later (numpy), 48 kHz, original channel count
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
         "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.005", "-ar", str(SR), str(dst)])


def read_wav(p):
    import soundfile as sf
    x, sr = sf.read(str(p), always_2d=True)
    return x, sr


def measure(x, sr):
    mono = x.mean(axis=1)
    peak = float(np.abs(x).max()) or 1e-9
    db = lambda v: 20 * np.log10(max(v, 1e-9))
    win = max(1, int(0.01 * sr))
    env = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, mode="same"))
    loud = env.max() or 1e-9
    # end: last 10 ms window within 40 dB of the loudest one
    above = np.where(env > loud * 10 ** (-40 / 20))[0]
    end = (above[-1] + 1) / sr if len(above) else len(mono) / sr
    tail = mono[int(end * sr):]
    floor_db = db(float(np.sqrt((tail ** 2).mean()))) - db(loud) if len(tail) > win * 5 else -90.0
    clipped = float((np.abs(x) >= 0.999 * peak).mean()) if peak >= 0.99 else 0.0
    return {
        "dur": round(len(mono) / sr, 3), "end": round(end, 3),
        "peak_at": round(int(np.argmax(env)) / sr, 3),
        "attack_ms": round(1000 * (int(np.argmax(env > loud * 0.5)) / sr), 1),
        "crest_db": round(db(peak) - db(float(np.sqrt((mono ** 2).mean()))), 1),
        "tail_floor_db": round(floor_db, 1), "clipped_share": round(clipped, 5),
        "raw_peak_db": round(db(peak), 2),
    }


def verdict(role, m):
    lo, hi, fast = ROLE_RULES.get(role, (0.03, 10.0, False))
    if m["end"] < lo:
        return f"too short ({m['end']} s < {lo})"
    if m["end"] > hi:
        return f"too long ({m['end']} s > {hi})"
    if m["clipped_share"] > 0.0005:
        return "clipped"
    if fast and m["attack_ms"] > 40:
        return f"slow start ({m['attack_ms']} ms)"
    if m["tail_floor_db"] > -35:
        return f"noisy tail ({m['tail_floor_db']} dB)"
    return None


def score(role, m, rank):
    # cleaner tail, more punch (crest) and the curator's own order win; length near the middle of the range helps
    lo, hi, _ = ROLE_RULES.get(role, (0.03, 10.0, False))
    mid = (lo + hi) / 2
    return (-m["tail_floor_db"] * 0.15 + min(m["crest_db"], 24) * 0.2 - rank * 0.8
            - abs(m["end"] - mid) / (hi - lo))


def finish(src, dst, end):
    import soundfile as sf
    x, sr = read_wav(src)
    x = x[: int(min(len(x), (end + 0.08) * sr))]
    fade = min(len(x), int(0.06 * sr))
    if fade:
        x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    x *= 10 ** (-1 / 20) / (np.abs(x).max() or 1)
    dst.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(dst), x, sr, subtype="PCM_24")


def configure_real_sfx():
    if not (REAL_SFX / "scripts" / "setup.py").exists():
        return "real-sfx not found next to this skill: skipped"
    cfg = REAL_SFX / "config.json"
    data = json.loads(cfg.read_text()) if cfg.exists() else json.loads((REAL_SFX / "config.example.json").read_text())
    data["libraries"] = [l for l in data.get("libraries", []) if l.get("name") != "agencia"]
    data["libraries"].insert(0, {"name": "agencia", "path": str(LIB), "tier": "main"})
    cfg.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    subprocess.run([sys.executable, str(REAL_SFX / "scripts" / "build_index.py")], check=True)
    return f"real-sfx now uses {LIB} (config.json + index rebuilt)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(HERE / "manifest.json"))
    ap.add_argument("--keep", type=int)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found: install it first (Mac: brew install ffmpeg)")
    man = json.loads(Path(a.manifest).read_text())
    keep = a.keep or man.get("keep", 3)
    cands = man["sounds"]
    if a.dry_run:
        for c in cands:
            print(f"{c['role']:9} {c['title'][:50]:50} {c['url']}")
        return

    cache = Path(tempfile.gettempdir()) / "agency-sfx-cache"
    cache.mkdir(exist_ok=True)
    report, per_role = [], {}
    for i, c in enumerate(cands):
        row = {k: c[k] for k in ("role", "title", "creator", "license", "landing", "url")}
        try:
            raw = cache / f"{c['id']}.{c.get('filetype', 'mp3')}"
            download(c["url"], raw)
            wav = cache / f"{c['id']}.48k.wav"
            to_wav(raw, wav)
            x, sr = read_wav(wav)
            m = measure(x, sr)
            row.update(m)
            row["dropped"] = verdict(c["role"], m)
        except Exception as e:
            row["dropped"] = f"error: {e}"
        print(f"[{i + 1}/{len(cands)}] {c['role']:9} {c['title'][:45]:45} -> {row['dropped'] or 'ok'}", flush=True)
        if not row["dropped"]:
            per_role.setdefault(c["role"], []).append((c, row, wav))
        report.append(row)
        time.sleep(0.5)

    if not per_role:
        sys.exit("no candidate passed the checks: the library was left as it was")
    if LIB.exists():
        shutil.rmtree(LIB)
    LIB.mkdir(parents=True)
    catalog, credits = [], ["# Créditos de la biblioteca de efectos", "",
                            "Todos los sonidos son CC0 (dominio público): se pueden usar en trabajos comerciales sin "
                            "atribución. Igual se listan sus autores.", "",
                            "| Archivo | Sonido | Autor | Licencia |", "|---|---|---|---|"]
    for role, items in sorted(per_role.items()):
        order = [c for c in cands if c["role"] == role]
        ranked = sorted(items, key=lambda t: -score(role, t[1], order.index(t[0])))
        for n, (c, row, wav) in enumerate(ranked[:keep], 1):
            rel = f"{role}/{role}_{n:02d}_{slug(c['title'])}.wav"
            finish(wav, LIB / rel, row["end"])
            row["kept_as"] = rel
            catalog.append({"type": PACK_TYPE.get(role, role), "file": rel,
                            "source": f"{role.replace('_', ' ')}/{c['title']} by {c['creator']}",
                            "hit": 1, "hits_in_source": 1})
            credits.append(f"| `{rel}` | [{c['title']}]({c['landing']}) | {c['creator']} | {c['license'].upper()} |")
    (LIB / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    (LIB / "CREDITS.md").write_text("\n".join(credits) + "\n")
    (LIB / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    roles = {r: len([c for c in catalog if c["file"].startswith(r + "/")]) for r in sorted(per_role)}
    print(f"\nkept {len(catalog)} sounds: " + ", ".join(f"{r} {n}" for r, n in roles.items()))
    missing = sorted({c["role"] for c in cands} - set(per_role))
    if missing:
        print("no usable candidate for: " + ", ".join(missing))
    print(configure_real_sfx())


if __name__ == "__main__":
    main()
