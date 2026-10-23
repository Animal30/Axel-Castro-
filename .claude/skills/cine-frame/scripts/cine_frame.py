#!/usr/bin/env python3
"""Cine Frame: a talking-head reel where the footage sits in a cinematic band on a black 9:16 canvas,
with a fixed headline above the band and 1-3 word captions on the band.

    python3 cine_frame.py prep CLIP [CLIP ...] --work DIR     # HDR -> SDR bt709, joins clips -> DIR/src.mp4
    python3 cine_frame.py transcribe --work DIR [--lang es]    # -> DIR/words.json
    python3 cine_frame.py plan --work DIR [--tight]            # -> DIR/plan.json (draft: edit it, then render)
    python3 cine_frame.py stills --work DIR [--at 1.5,8,20]   # -> DIR/stills/*.png from the plan (no full render)
    python3 cine_frame.py render --work DIR [--out FILE]       # -> DIR/out.mp4 (or FILE)
    python3 cine_frame.py sheet VIDEO                          # contact sheet next to the video

Brand comes from $CREATOR_PROFILE_DIR/profile.json (accent, bg, font_main_bold). All times in plan.json are
SOURCE times (seconds in src.mp4); render maps them through the kept segments. Nothing is ever drawn that names
the editor: no watermark, no signature.
"""
import argparse, json, math, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
W, H = 1080, 1920
ASPECTS = {"4:3": 4 / 3, "1.85": 1.85, "16:9": 16 / 9, "2.39": 2.39, "1:1": 1.0}
GRADES = {
    # cool shadows, soft highlights, low saturation: the reference look
    "cine": "eq=contrast=1.07:saturation=0.80:gamma=0.97,"
            "colorbalance=rs=-0.05:gs=-0.01:bs=0.06:rm=-0.01:bm=0.02:rh=0.03:gh=0.01:bh=-0.03,"
            "curves=all='0/0.015 0.25/0.21 0.5/0.5 0.8/0.83 1/0.95'",
    "warm": "eq=contrast=1.06:saturation=0.88:gamma=0.98,"
            "colorbalance=rs=0.02:bs=-0.03:rm=0.03:bm=-0.03:rh=0.04:bh=-0.04,"
            "curves=all='0/0.02 0.25/0.22 0.5/0.5 0.8/0.82 1/0.95'",
    # for bright, flat, yellowish phone footage (sunny wall, overexposed): pull exposure down, neutralise the
    # yellow toward cool, keep skin warm, deep contrast. "Inside the scene" look.
    "moody": "eq=contrast=1.16:saturation=0.55:gamma=0.90,"
             "colortemperature=temperature=8200:mix=0.5,"
             "colorbalance=rm=0.03:gm=-0.01:bm=-0.01:rs=-0.03:bs=0.05:bh=-0.02,"
             "curves=r='0/0 0.5/0.49 1/0.92':g='0/0.01 0.5/0.48 1/0.91':b='0/0.05 0.5/0.47 1/0.88'"
             ":all='0/0 0.2/0.13 0.6/0.55 1/0.94'",
    "mono": "hue=s=0,eq=contrast=1.12:gamma=0.96,curves=all='0/0.02 0.5/0.48 1/0.95'",
    "none": "null",
}


def vignette(plan):
    """vignette: true = soft (PI/5); a number = strength, e.g. 4.2 -> PI/4.2 (smaller = darker edges)."""
    v = plan.get("vignette")
    return f"vignette=angle=PI/{5 if v is True else float(v)}"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit("command failed: " + " ".join(cmd[:6]) + " ...\n" + r.stderr[-2500:])
    return r.stdout


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))


def vstream(info):
    return next(s for s in info["streams"] if s["codec_type"] == "video")


# ---------- profile ----------

def profile_dir():
    return os.path.expanduser(os.environ.get("CREATOR_PROFILE_DIR", "~/.claude/creator-profile"))


def load_profile():
    p = os.path.join(profile_dir(), "profile.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def font_path(prof):
    f = (prof.get("font_main_bold") or {}).get("file", "Inter-Bold.otf")
    pd = profile_dir()
    cands = [os.path.join(pd, "assets/fonts", f)]
    parent = os.path.dirname(pd.rstrip("/"))
    if os.path.isdir(parent):                                   # client profiles may borrow fonts from a sibling
        cands += [os.path.join(parent, d, "assets/fonts", f) for d in sorted(os.listdir(parent))]
    cands.append(os.path.join(SKILL, "assets/fonts/Inter-Bold.otf"))
    return next(c for c in cands if os.path.exists(c))


def named_font(name, prof):
    """A font file by name: absolute path, the skill's assets/fonts, then the profile's fonts. None = brand bold."""
    if not name:
        return font_path(prof)
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for d in (os.path.join(SKILL, "assets/fonts"), os.path.join(profile_dir(), "assets/fonts")):
        if os.path.exists(os.path.join(d, name)):
            return os.path.join(d, name)
    sys.exit(f"font not found: {name}")


def colour(v, prof):
    if v in (None, "", "accent"):
        return prof.get("accent", "#FF7A1A") if v == "accent" else "#FFFFFF"
    return v


# ---------- prep ----------

def is_hdr(vs):
    return vs.get("color_transfer") in ("arib-std-b67", "smpte2084") or vs.get("color_primaries") == "bt2020"


def cmd_prep(a):
    os.makedirs(a.work, exist_ok=True)
    first = vstream(probe(a.clips[0]))
    rot = abs(int(next((d.get("rotation", 0) for d in first.get("side_data_list", []) if "rotation" in d), 0)))
    fw, fh = (first["height"], first["width"]) if rot in (90, 270) else (first["width"], first["height"])
    short = min(1440, fw, fh)                                   # 1440 short side: room to punch in without upscaling
    tw, th = (short, round(short * fh / fw / 2) * 2) if fw <= fh else (round(short * fw / fh / 2) * 2, short)
    parts = []
    for i, c in enumerate(a.clips):
        vs = vstream(probe(c))
        vf = []
        if is_hdr(vs):
            vf.append("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
                      "zscale=t=bt709:m=bt709:r=tv")
            print(f"{os.path.basename(c)}: HDR ({vs.get('color_transfer')}) -> tone-mapped to SDR bt709")
        vf += [f"scale={tw}:{th}:force_original_aspect_ratio=increase", f"crop={tw}:{th}", "setsar=1",
               f"fps={a.fps}", "format=yuv420p"]
        out = os.path.join(a.work, f"part{i:02d}.mp4")
        has_audio = any(s["codec_type"] == "audio" for s in probe(c)["streams"])
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", c]
        if not has_audio:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest"]
        cmd += ["-vf", ",".join(vf), "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", str(a.fps),
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out]
        run(cmd)
        parts.append(out)
    src = os.path.join(a.work, "src.mp4")
    if len(parts) == 1:
        shutil.move(parts[0], src)
    else:
        lst = os.path.join(a.work, "parts.txt")
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", src])
        for p in parts:
            os.remove(p)
    d = float(probe(src)["format"]["duration"])
    json.dump({"clips": a.clips, "width": tw, "height": th, "fps": a.fps, "duration": d},
              open(os.path.join(a.work, "info.json"), "w"), indent=1)
    print(f"src.mp4 {tw}x{th} {a.fps}fps {d:.2f}s")


# ---------- transcribe ----------

def cmd_transcribe(a):
    sys.path.insert(0, HERE)
    from stt import transcribe
    flac = os.path.join(a.work, "audio.flac")
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(a.work, "src.mp4"), "-vn", "-ac", "1", "-ar", "16000", flac])
    J = transcribe(flac, language=a.lang, events=False)
    J["words"] = [w for w in J["words"] if w.get("type", "word") == "word"]
    json.dump(J, open(os.path.join(a.work, "words.json"), "w"), indent=1, ensure_ascii=False)
    print(J.get("_engine"), len(J["words"]), "words")
    print(" ".join(w["text"] for w in J["words"]))


# ---------- plan ----------

def chunk(words, max_words, max_chars):
    caps, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        txt = " ".join(x["text"] for x in cur)
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= max_words or re.search(r"[.,!?;:]$", w["text"]) or nxt is None
               or len(txt + " " + nxt["text"]) > max_chars or nxt["start"] - w["end"] > 0.35)
        if brk:
            caps.append({"text": txt, "start": round(cur[0]["start"], 3), "end": round(cur[-1]["end"], 3)})
            cur = []
    return caps


def tight_segments(words, dur, gap=0.45, pad=0.12):
    """Keep speech; drop pauses longer than `gap` (each kept edge gets `pad` of air)."""
    if not words:
        return [{"start": 0, "end": round(dur, 3)}]
    segs, s, e = [], max(0, words[0]["start"] - pad), words[0]["end"]
    for w in words[1:]:
        if w["start"] - e > gap:
            segs.append({"start": round(s, 3), "end": round(min(dur, e + pad), 3)})
            s = w["start"] - pad
        e = w["end"]
    segs.append({"start": round(s, 3), "end": round(min(dur, e + 0.6), 3)})
    return segs


def cmd_plan(a):
    info = json.load(open(os.path.join(a.work, "info.json")))
    wp = os.path.join(a.work, "words.json")
    words = json.load(open(wp))["words"] if os.path.exists(wp) else []
    prof = load_profile()
    st = prof.get("cine_frame", {})
    plan = {
        "_note": "All times are SOURCE seconds in src.mp4. Edit headline, captions (*word* = accent colour), "
                 "segments (cuts + zoom punch-ins), then render.",
        "profile_dir": profile_dir(),
        "aspect": st.get("aspect", "4:3"),
        "band_center_y": 0.5,
        "focus": {"x": 0.5, "y": 0.42},
        "fps": info["fps"],
        "segments": tight_segments(words, info["duration"]) if a.tight else [{"start": 0, "end": round(info["duration"], 3)}],
        "grade": st.get("grade", "cine"),
        "grain": 5,
        "vignette": True,
        "headline": {"lines": ["WRITE THE HOOK HERE", "IN TWO SHORT LINES."], "size": 58},
        "headline_color": st.get("headline_color", "#FFFFFF"),
        "caption_color": st.get("caption_color", "#FFFFFF"),
        "accent": prof.get("accent", "#FF7A1A"),
        "caption_size": 60,
        "caption_y": 0.64,
        "captions": chunk(words, a.max_words, a.max_chars),
        "fade_out": 1.2,
        "loudness": -14,
        "music": None,
        "music_db": -24,
        "sfx": [],
        "outro": st.get("outro"),
    }
    out = os.path.join(a.work, "plan.json")
    json.dump(plan, open(out, "w"), indent=1, ensure_ascii=False)
    kept = sum(s["end"] - s["start"] for s in plan["segments"])
    print(f"plan.json: {len(plan['segments'])} segments, {kept:.2f}s kept of {info['duration']:.2f}s, "
          f"{len(plan['captions'])} captions")


# ---------- layout ----------

def band_geom(plan):
    A = ASPECTS.get(str(plan["aspect"]), None) or float(plan["aspect"])
    bh = round(W / A / 2) * 2
    top = round((H * plan.get("band_center_y", 0.5) - bh / 2) / 2) * 2
    return bh, top


def seg_map(plan):
    off, m = 0.0, []
    for s in plan["segments"]:
        m.append((s["start"], s["end"], off))
        off += s["end"] - s["start"]
    return m, off


def to_out(t, m):
    for s, e, off in m:
        if s - 1e-3 <= t <= e + 1e-3:
            return off + min(max(t, s), e) - s
    return None


def crop_for(seg, plan, sw, sh, bh):
    A = W / bh
    z = float(seg.get("zoom", 1.0))
    f = dict(plan.get("focus", {}), **seg.get("focus", {}))
    if sw / sh < A:
        cw = sw / z
        ch = cw / A
    else:
        ch = sh / z
        cw = ch * A
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    cx = int(min(max(f.get("x", 0.5) * sw - cw / 2, 0), sw - cw)) // 2 * 2
    cy = int(min(max(f.get("y", 0.42) * sh - ch / 2, 0), sh - ch)) // 2 * 2
    return cw, ch, cx, cy


def draw_layers(plan, prof, outdir):
    """One full-frame RGBA PNG per caption state (headline always included). Returns [(png, out_start, out_end)]."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    os.makedirs(outdir, exist_ok=True)
    fp = font_path(prof)
    hfont = named_font(plan.get("headline_font"), prof)
    cfont = named_font(plan.get("caption_font"), prof)
    bh, top = band_geom(plan)
    accent = colour(plan.get("accent") or "accent", prof)
    hcol, ccol = colour(plan.get("headline_color"), prof), colour(plan.get("caption_color"), prof)

    def text_layer(img, runs_lines, size, y_top, align_bottom=None, shadow=0.55, maxw=960, font_file=None,
                   tracking=0.0, line_h=1.05):
        """runs_lines: list of lines, each a list of (text, colour). Draws centred lines.
        tracking = extra letter spacing as a fraction of the font size."""
        def tlen(font, t):
            return font.getlength(t) + tracking * font.size * len(t)

        while True:
            font = ImageFont.truetype(font_file or fp, size)
            widths = [sum(tlen(font, t) for t, _ in ln) for ln in runs_lines]
            if max(widths or [0]) <= maxw or size < 24:
                break
            size -= 2
        lh = round(size * line_h)
        total = lh * len(runs_lines)
        y0 = align_bottom - total if align_bottom is not None else y_top
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        fg = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ds, df = ImageDraw.Draw(sh), ImageDraw.Draw(fg)
        for i, ln in enumerate(runs_lines):
            x = (W - widths[i]) / 2
            y = y0 + i * lh
            for t, c in ln:
                if tracking:
                    for ch in t:
                        ds.text((x, y + 3), ch, font=font, fill=(0, 0, 0, int(255 * shadow)))
                        df.text((x, y), ch, font=font, fill=c)
                        x += tlen(font, ch)
                else:
                    ds.text((x, y + 3), t, font=font, fill=(0, 0, 0, int(255 * shadow)))
                    df.text((x, y), t, font=font, fill=c)
                    x += font.getlength(t)
        if shadow:
            blurred = sh.filter(ImageFilter.GaussianBlur(size * 0.12))
            img.alpha_composite(blurred)
            if shadow > 0.6:                                          # deep shadow: a second, wider pass
                img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * 0.35)))
        img.alpha_composite(fg)

    def runs(text, base):
        out = []
        for part in re.split(r"(\*[^*]+\*)", text):
            if part:
                out.append((part.strip("*"), accent) if part.startswith("*") else (part, base))
        return out

    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hl = plan.get("headline") or {}
    if hl.get("lines"):
        text_layer(base, [runs(l, hcol) for l in hl["lines"]], hl.get("size", 58), None,
                   align_bottom=top - 34, shadow=plan.get("headline_shadow", 0.0), font_file=hfont,
                   tracking=plan.get("headline_tracking", 0.0), line_h=hl.get("line_height", 1.05))
    m, total = seg_map(plan)
    caps = []
    for c in plan.get("captions", []):
        s, e = to_out(c["start"], m), to_out(c["end"], m)
        if s is None:
            continue
        caps.append([s, e if e is not None else s + 0.4, c["text"]])
    for i, c in enumerate(caps):                                 # hold each caption until the next one if the gap is short
        nxt = caps[i + 1][0] if i + 1 < len(caps) else total
        c[1] = nxt if nxt - c[1] < 0.6 else c[1] + 0.15
    states, t, n = [], 0.0, 0
    blank = os.path.join(outdir, "blank.png")
    base.save(blank)
    for s, e, text in caps:
        if s > t + 1e-3:
            states.append((blank, t, s))
        img = base.copy()
        cy = top + bh * plan.get("caption_y", 0.64)
        text_layer(img, [runs(text, ccol)], plan.get("caption_size", 60), cy - plan.get("caption_size", 60) * 0.6,
                   shadow=plan.get("caption_shadow", 0.55), font_file=cfont,
                   tracking=plan.get("caption_tracking", 0.0))
        p = os.path.join(outdir, f"c{n:04d}.png")
        img.save(p)
        n += 1
        states.append((p, s, min(e, total)))
        t = min(e, total)
    if t < total:
        states.append((blank, t, total))
    return states, total


# ---------- render ----------

def build_graph(plan, prof, work, layers_list, sw, sh, total):
    bh, top = band_geom(plan)
    fps = plan.get("fps", 24)
    bg = prof.get("bg", "#000000").lstrip("#")
    f, vl, al = [], [], []
    for i, s in enumerate(plan["segments"]):
        cw, ch, cx, cy = crop_for(s, plan, sw, sh, bh)
        d = s["end"] - s["start"]
        f.append(f"[0:v]trim={s['start']}:{s['end']},setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},"
                 f"scale={W}:{bh}:flags=lanczos,setsar=1[v{i}]")
        f.append(f"[0:a]atrim={s['start']}:{s['end']},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.3f}:d=0.012[a{i}]")
        vl.append(f"[v{i}]")
        al.append(f"[a{i}]")
    n = len(plan["segments"])
    f.append("".join(v + a for v, a in zip(vl, al)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    look = [GRADES.get(plan.get("grade", "cine"), GRADES["cine"])] + ([plan["grade_extra"]] if plan.get("grade_extra") else [])
    if plan.get("vignette"):
        look.append(vignette(plan))
    if plan.get("grain"):
        look.append(f"noise=alls={int(plan['grain'])}:allf=t")
    f.append(f"[vc]{','.join(look)},pad={W}:{H}:0:{top}:color=0x{bg},fps={fps},format=yuv420p[vb]")
    f.append("[1:v]format=rgba[cap]")
    fo = float(plan.get("fade_out") or 0)
    vend = f",fade=t=out:st={total - fo:.3f}:d={fo}" if fo else ""
    f.append(f"[vb][cap]overlay=0:0:shortest=1:format=auto{vend},format=yuv420p[vout]")
    # audio: voice + optional music (ducked under the voice) + optional sfx (output time)
    idx, mix = 2, ["[ac]"]
    extra = []
    if plan.get("music"):
        extra += ["-stream_loop", "-1", "-i", plan["music"]]
        f.append(f"[{idx}:a]atrim=0:{total:.3f},volume={plan.get('music_db', -24)}dB,"
                 f"afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[mus]")
        f.append("[ac]asplit[ac1][key]")
        f.append("[mus][key]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=350[mduck]")
        mix = ["[ac1]", "[mduck]"]
        idx += 1
    for j, fx in enumerate(plan.get("sfx", [])):
        extra += ["-i", fx["file"]]
        ms = int(float(fx["t"]) * 1000)
        f.append(f"[{idx}:a]volume={fx.get('db', -12)}dB,adelay={ms}|{ms}[sfx{j}]")
        mix.append(f"[sfx{j}]")
        idx += 1
    if len(mix) > 1:
        f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[am]")
        src_a = "[am]"
    else:
        src_a = "[ac]"
    aend = f",afade=t=out:st={total - fo:.3f}:d={fo}" if fo else ""
    f.append(f"{src_a}loudnorm=I={plan.get('loudness', -14)}:TP=-1.5:LRA=11{aend},aresample=48000[aout]")
    return ";".join(f), extra


def write_concat(states, path):
    lines = []
    for p, s, e in states:
        lines += [f"file '{os.path.abspath(p)}'", f"duration {max(e - s, 0.001):.4f}"]
    lines.append(f"file '{os.path.abspath(states[-1][0])}'")
    open(path, "w").write("\n".join(lines) + "\n")


def cmd_render(a):
    plan = json.load(open(os.path.join(a.work, "plan.json")))
    if plan.get("profile_dir"):
        os.environ["CREATOR_PROFILE_DIR"] = plan["profile_dir"]
    prof = load_profile()
    src = os.path.join(a.work, "src.mp4")
    vs = vstream(probe(src))
    states, total = draw_layers(plan, prof, os.path.join(a.work, "layers"))
    cl = os.path.join(a.work, "layers.txt")
    write_concat(states, cl)
    graph, extra = build_graph(plan, prof, a.work, states, vs["width"], vs["height"], total)
    out = a.out or os.path.join(a.work, "out.mp4")
    main = out if not plan.get("outro") else os.path.join(a.work, "main.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-f", "concat", "-safe", "0", "-i", cl] + extra + [
        "-filter_complex", graph, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-crf", "18", "-preset", a.preset, "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", main]
    run(cmd)
    if plan.get("outro"):
        append_outro(main, plan["outro"], out, plan.get("fps", 24))
    d = float(probe(out)["format"]["duration"])
    print(f"rendered {out} ({d:.2f}s)")


def append_outro(main, outro, out, fps):
    has_a = any(s["codec_type"] == "audio" for s in probe(outro)["streams"])
    ins = ["-i", main, "-i", outro] + ([] if has_a else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"])
    oa = "[1:a]" if has_a else "[2:a]"
    od = float(probe(outro)["format"]["duration"])
    g = (f"[1:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,"
         f"fps={fps},format=yuv420p[ov];{oa}atrim=0:{od:.3f},aresample=48000,aformat=channel_layouts=stereo[oa];"
         f"[0:v][0:a][ov][oa]concat=n=2:v=1:a=1[v][a]")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", g, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", out])


def cmd_stills(a):
    """Render only the requested output-time frames (fast check before the full render)."""
    plan = json.load(open(os.path.join(a.work, "plan.json")))
    if plan.get("profile_dir"):
        os.environ["CREATOR_PROFILE_DIR"] = plan["profile_dir"]
    prof = load_profile()
    src = os.path.join(a.work, "src.mp4")
    vs = vstream(probe(src))
    states, total = draw_layers(plan, prof, os.path.join(a.work, "layers"))
    bh, top = band_geom(plan)
    m, _ = seg_map(plan)
    ats = [float(x) for x in a.at.split(",")] if a.at else [total * k / 6 for k in range(1, 6)]
    od = os.path.join(a.work, "stills")
    os.makedirs(od, exist_ok=True)
    look = GRADES.get(plan.get("grade", "cine"), GRADES["cine"]) + ("," + plan["grade_extra"] if plan.get("grade_extra") else "") \
        + ("," + vignette(plan) if plan.get("vignette") else "")
    for t in ats:
        k = next(i for i, (s, e, off) in enumerate(m) if off <= t <= off + (e - s) or i == len(m) - 1)
        s, e, off = m[k]
        st = s + min(t - off, e - s - 0.01)
        cw, ch, cx, cy = crop_for(plan["segments"][k], plan, vs["width"], vs["height"], bh)
        layer = next((p for p, a0, a1 in states if a0 <= t < a1), states[-1][0])
        bg = prof.get("bg", "#000000").lstrip("#")
        p = os.path.join(od, f"t{t:06.2f}.png")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st:.3f}", "-i", src, "-i", layer, "-filter_complex",
             f"[0:v]crop={cw}:{ch}:{cx}:{cy},scale={W}:{bh},{look},pad={W}:{H}:0:{top}:color=0x{bg}[b];[b][1:v]overlay=0:0",
             "-frames:v", "1", p])
        print(p)


def cmd_sheet(a):
    d = float(probe(a.video)["format"]["duration"])
    out = os.path.splitext(a.video)[0] + "_sheet.jpg"
    run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf",
         f"fps={12 / max(d, 1):.5f},scale=270:-1,tile=6x2:padding=6:color=white", "-frames:v", "1", out])
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("prep"); p.add_argument("clips", nargs="+"); p.add_argument("--work", required=True)
    p.add_argument("--fps", type=int, default=24)
    p = sp.add_parser("transcribe"); p.add_argument("--work", required=True); p.add_argument("--lang", default=None)
    p = sp.add_parser("plan"); p.add_argument("--work", required=True); p.add_argument("--tight", action="store_true")
    p.add_argument("--max-words", type=int, default=3); p.add_argument("--max-chars", type=int, default=16)
    p = sp.add_parser("stills"); p.add_argument("--work", required=True); p.add_argument("--at", default="")
    p = sp.add_parser("render"); p.add_argument("--work", required=True); p.add_argument("--out")
    p.add_argument("--preset", default="medium")
    p = sp.add_parser("sheet"); p.add_argument("video")
    a = ap.parse_args()
    {"prep": cmd_prep, "transcribe": cmd_transcribe, "plan": cmd_plan, "stills": cmd_stills,
     "render": cmd_render, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    main()
