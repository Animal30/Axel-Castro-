---
name: sfx-library
description: The agency's own curated library of real sound effects (CC0, found through Openverse / Freesound) for reels, ads and short-form edits - whooshes, risers, impacts, sub drops, pops, clicks, typing, UI dings, camera shutters, coins, glitches, paper - chosen for the sound of current short-form marketing, measured and cleaned, with credits. Use whenever an edit needs sound effects (with real-sfx, which reads this library as its main one), when the user asks to add, rebuild, update or extend the SFX library, asks which sounds the agency has, or says "biblioteca de sonidos", "mis efectos", "sonidos de la agencia".
---

# sfx-library: the agency's sound effects

The library lives at `sounds/library/` in this repository, so every chat on this repo has it:

- `sounds/library/<role>/<role>_NN_<name>.wav` - the sounds, 48 kHz, 24-bit, peak -1 dBFS, leading silence removed
- `catalog.json` - what each sound is (real-sfx reads it), `CREDITS.md` - author and link of every sound,
  `report.json` - every candidate with its measurements and why it was kept or dropped

## Using it in an edit

real-sfx is the tool that places the sounds. Point it at the library once per machine or cloud session (its
`config.json` is not committed):

```bash
cd .claude/skills/real-sfx
python3 scripts/setup.py add-library agencia "$(git rev-parse --show-toplevel)/sounds/library" --tier main --index
python3 scripts/setup.py init --uisfx     # only if uisfx (UI cues) is missing; needs npm
```

Then follow real-sfx as usual. Rules for this agency's reels (the voice carries them):

- **Few and quiet.** About one effect every 4-6 s, only on the changes that matter (a graphic or full-screen card
  arriving, a reveal, a number, the CTA), never on every cut back to the face. Under the voice: `mix.py --voice-safe`.
- **Match the picture.** A whoosh peaks just after the cut it covers; clicks, pops and UI sounds start on the frame;
  a riser ends on the reveal it builds to; an impact or sub drop lands on the hook or the big statement, at most one
  or two per reel.
- **Always show the version without and the version with effects** so the person can judge. You cannot hear: say
  what was measured, not how it sounds.

## Rebuilding or extending it

`manifest.json` holds the candidates: per role several CC0 sounds chosen from Openverse search results by title,
tags, length and author (what is used in short-form marketing now: short air whooshes and swipes, soft pops and
clicks for text, sub drops and cinematic hits for the hook, risers into reveals, typing for on-screen text, UI dings
for results, camera shutters, coins / cash for money, glitches for transitions, paper for documents). `build.py`
downloads every candidate, converts it, measures it, drops the bad ones (clipped, wrong length for its role, noisy
tail, slow start on a sound that must start at once) and keeps the best 3 per role.

```bash
pip install numpy soundfile          # plus ffmpeg (Mac: brew install ffmpeg)
python3 .claude/skills/sfx-library/build.py            # then commit sounds/library
```

Freesound (where nearly all of Openverse's sound effects are hosted) refuses downloads from cloud machines, so run
the build on the user's own computer (a local Claude Code session) and commit the result; every chat then has it.
To add sounds: add entries to `manifest.json` (`role`, `id`, `title`, `creator`, `license`, `landing`, `url`) from
`https://api.openverse.org/v1/audio/?q=...&license=cc0`, and rebuild. Keep to CC0 so the sounds are safe for paid
client work without credits.
