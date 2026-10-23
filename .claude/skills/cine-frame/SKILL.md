---
name: cine-frame
description: Cine Frame - the studio's own cinematic talking-head reel (not part of the Creator Skill Pack). The footage sits in a 4:3 cinematic band centred on a black 9:16 canvas, a fixed 2-line uppercase headline sits just above the band, 1-3 word captions sit on the speaker's chest, film grade (cool shadows, low saturation, grain, vignette), 24 fps, fade to black at the end. Works for any client through their brand profile (CREATOR_PROFILE_DIR). Use when Nahuel says "Cine Frame", "edición cinemática", "estilo cinemático", "como el video del auto", "franja negra / letterbox", "más cine", or sends clips recorded for this style.
---

# Cine Frame

The studio's signature cinematic edit. One calm, confident talking head framed like a film still: black canvas,
a 4:3 picture band in the middle, the hook written above it, and short white captions on the band. It feels
premium because it is restrained: no B-roll, no split screen, no stickers, no emoji, few cuts.

Reference: `references/reference-analysis.md` (measured from the car reel Nahuel sent on 2026-10-23).

## Hard rules

- **Never** a watermark, logo bug, Nahuel's name, his company or any @handle on screen. Client logos only in
  the client's own outro, when the client's rules ask for one.
- Brand = the client's profile: `export CREATOR_PROFILE_DIR=<repo>/.claude/creator-profile/<client>` before any
  command. Read its `profile.json` and any `NOTES.md` / `notes/*.md` first; client rules win over these defaults.
- iPhone footage is often HDR (HLG). `prep` always tone-maps it to SDR bt709. Never render from the raw .MOV.
- Look at stills before the full render, and at the contact sheet after it. Never send a render you have not seen.

## Pipeline (cloud session, from the repo root)

```bash
export CREATOR_PROFILE_DIR=$PWD/.claude/creator-profile/<client>
S=.claude/skills/cine-frame/scripts/cine_frame.py
WK=~/reel-work/cine-<client>-<slug>

python3 $S prep CLIP1.MOV [CLIP2.MOV ...] --work $WK   # joins clips in order, HDR->SDR, 24 fps -> $WK/src.mp4
python3 $S transcribe --work $WK [--lang es]           # ElevenLabs Scribe (profile "transcriber") -> words.json
python3 $S plan --work $WK --tight                     # draft plan.json; --tight drops pauses > 0.45 s
#   ...edit $WK/plan.json (see below)...
python3 $S stills --work $WK --at 0.5,4,9              # quick frames to check framing, headline, captions
python3 $S render --work $WK --out /mnt/project-files/<client>/<name>.mp4
python3 $S sheet /mnt/project-files/<client>/<name>.mp4
```

A 40 s reel renders in about 1-2 minutes (plain ffmpeg, no browser).

## Editing plan.json (this is the creative part: do it yourself, don't ask)

All times are **source seconds** in `src.mp4`.

1. **Headline** (`headline.lines`): the hook in 2 short uppercase lines, max ~22 characters each, ending with a
   period, written from the script/transcript. Statement, not a question; the strongest idea of the video
   (reference: "GOD CAN TAKE AWAY / WHAT HE GAVE AT ANY TIME."). Same language as the speaker. Wrap 1 key word in
   `*asterisks*` to colour it with the client accent (optional, at most one).
2. **Captions**: the draft chunks 1-3 words, breaking at punctuation. Fix any transcription errors against the
   script PDF if there is one. Keep the creator's casing (sentence case, not uppercase). Mark at most one word every
   ~6-8 s with `*word*` for the accent colour; many captions should have none.
3. **Cut** (`segments`): with `--tight` pauses are already gone. Remove false starts, repeated takes and filler
   ("eh", "um") by splitting/removing segments. Keep a little breath: this style is calmer than the pack reels.
4. **Punch-ins**: give a segment `"zoom": 1.12` (1.08-1.2) to cut in closer on a key sentence, then back to 1.0
   on the next. At most one every ~5-8 s. A segment can also carry its own `"focus": {"x":..,"y":..}`.
5. **Framing**: `focus` is the crop centre in the source (0-1). Put the eyes in the upper third of the band
   (default y 0.42 suits a vertical selfie). Check in stills that the head is not cut off.
6. **Look**: `grade` = `cine` (default, cool and desaturated like the reference), `moody` (for bright, flat,
   yellowish phone footage such as a sunny cream wall: neutralises the yellow, keeps skin warm, deeper contrast),
   `warm`, `mono` or `none`; `grade_extra` = extra ffmpeg filters appended; `grain` 0-10 (default 5);
   `vignette` true (soft) or a number (4.2 = darker edges, pulls the eye to the face). Always compare the raw
   frame and the graded still: footage straight from the phone should never reach the final. `aspect` = `4:3` (default), `16:9`, `1.85`, `2.39`.
7. **Typography**: default is the brand bold sans (like the reference). For the **elegant / film** look
   (Nahuel's choice for reflective "thought" videos, 2026-10-23) use the bundled Cormorant Garamond serif:
   `"headline_font": "CormorantGaramond-SemiBold.ttf", "headline_tracking": 0.10, "headline_shadow": 0.5,
   "headline_color": "#F4F1EA", "headline": {"size": 62, "line_height": 1.12, ...}` and
   `"caption_font": "CormorantGaramond-SemiBold.ttf", "caption_size": 74, "caption_shadow": 0.85,
   "caption_color": "#FFFFFF"` (all white, deep shadow, no accent colour). Also bundled: `-Medium`,
   `-MediumItalic`. Any font: a file name in `assets/fonts` or the profile's fonts, or an absolute path.
8. **Colours**: `headline_color` / `caption_color` are `#FFFFFF` by default; set either to `"accent"` when the
   client's typography is brand-coloured (Nate Velazquez and Maison Enterprises use orange typography).
   A profile can set defaults once in `profile.json` under `"cine_frame": {"caption_color": "accent", ...}`.
9. **Audio**: voice is normalised to -14 LUFS. `music`: a file path (ducked under the voice, `music_db` -24 by
   default). If the client's music rule is "ask", ask Nahuel which track before the final render, or deliver
   without music and say so. `sfx`: `[{"t": <OUTPUT seconds>, "file": ".../impact.mp3", "db": -14}]`, sparingly
   (a soft hit on the headline idea at most). SFX from the profile's `sfx_dir`.
10. **End**: `fade_out` (seconds, default 1.2) fades picture and sound to black. `outro`: path to the client's
   outro clip (Nate/Maison cinematic logo outro, Sam's Iron Bird app + eagle ending) appended after the fade.
   Never add a CTA card or end screen that the client's rules don't ask for.

## Check before delivering

- Stills: headline fully above the band, never touching it; captions inside the band, not over the mouth; face
  not cropped; nothing in the bottom black area.
- Contact sheet of the final: captions change with the speech, punch-ins visible, fade at the end.
- `ffprobe`: 1080x1920, 24 fps, bt709, AAC. Loudness about -14 LUFS.
- Deliver to `/mnt/project-files/<client>/` and attach it in the client's thread.

## What to tell Nahuel for recording (iPhone 14 Pro)

Video mode (not Cinematic mode), 4K 24 fps, **HDR Video off**, Auto FPS off, Formats "Most Compatible", 1x lens
(or front camera handheld), vertical, face in the middle with some headroom, AE/AF lock on the face. Details in
`references/reference-analysis.md`.
