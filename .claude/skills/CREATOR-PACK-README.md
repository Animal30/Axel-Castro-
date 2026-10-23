# Creator Skill Pack: client templates

22 skills with everything personal removed and replaced by placeholders, plus the nine HyperFrames engine skills
they build on. Start with `creator-setup`: it interviews the new owner once and fills every other skill from the same
profile. Client-facing install steps are in `INSTALL.md`.

| Skill | What it does |
|---|---|
| `creator-setup` | Run first. One interview (brand, fonts, tools, references) that fills every other skill. |
| `business-short-form-reels` | Raw business talking-head clip -> finished 9:16 reel: tight cut, hook, full screen / split / animation, captions, motion graphics, sound. |
| `personal-short-form-reels` | Raw personal clip -> fast 9:16 reel with the creator's own B-roll, one-word captions, graphics, logos, music. |
| `explainer-panel-reel` | Close-ups plus a bottom panel with explainer animations above, one-line captions with emphasis words. |
| `glass-explainer-reel` | The panel edit with business graphics on rectangular glass cards. |
| `visual-essay-reel` | Dark reel with a cut-out presenter and an evidence wall. |
| `broll-stacked-text-edit` | Tight cut, library B-roll, full captions and selective stacked text. |
| `fitted-stacked-captions` | Big accent anchor word with the other words fitted around it; works on top of the reel styles. |
| `image-cluster-reel` | Presenter low in frame, clusters of metaphor images above the head, tiny captions. |
| `cutout-backdrop-reel` | Presenter cut out over a full-screen image per idea, hook over a collage. |
| `cutout-grid-reel` | Presenter centred over a 2x2 grid of four images that change together. |
| `depth-ui-reel` | Presenter full frame with real interfaces behind the head and chest captions. |
| `ranking-format` | Tier-list reel: S to F table, item cards drop into rows. |
| `split-reel` | 9:16 face on top, animations below, with full-screen windows (Remotion kit). |
| `educational-youtube-editor` | Raw long-form teaching video -> finished 16:9 YouTube edit: clean dialogue cut, then motivated visuals. |
| `split-screen-document-plus-animations` | Camera plus on-screen document: document left, presenter right, animations in the full-screen parts. |
| `lesson-doc-builder` | Script or outline -> the white on-screen teaching document used in split-screen lessons. |
| `coaching-call-clips` | A recorded call -> ranked clips with 16:9 and 9:16 editing prompts and source cuts. |
| `youtube-clips` | The clip system pointed at a long-form YouTube video (file or link). |
| `personal-broll-library` | Indexes the creator's own B-roll once, then searches and matches it in plain English. |
| `video-to-written-content` | A YouTube link or video -> emails and social posts in the creator's voice. |
| `watch` | Watch any video (link or file): frames, transcript, answers questions about it. MIT licence, by Bradley Bonanno. |

Also in the pack (not templates): `hyperframes`, `hyperframes-animation`, `-audio`, `-cli`, `-core`, `-creative`,
`-keyframes`, `-registry`, `-studio` (Apache-2.0, see `NOTICE-HyperFrames.txt`) and `watch` (MIT, licence inside).
Not in the pack by decision: the carousel skills, the Nero skills, and the review-gate app.

## What the client needs to install

- **Claude Code** on a Mac (the editing scripts are written for macOS).
- **HyperFrames**: it builds and renders every video edit. Needs Node.js 22 or newer; check with `npx hyperframes doctor`.
- **ffmpeg**: `brew install ffmpeg`. `yt-dlp` as well for the two skills that take YouTube links: `brew install yt-dlp`.
- **A transcriber.** **ElevenLabs is the best** and is what the skills were built on (an account plus an API key,
  about $0.22 per hour of audio, speaker labels on calls). The free alternative runs on the client's own computer
  through HyperFrames. The setup interview asks which, and they can switch later.
- `lesson-doc-builder` is the light one: it needs only Node and a Chromium-family browser (Chrome, Edge, Brave, Arc).
  No HyperFrames, no transcriber, no API key.

## Installing a skill

Copy the skill's folder into `~/.claude/skills/` (or unzip the matching file from `dist/` there). Nothing else.
Always install `creator-setup` and the `hyperframes*` folders with them. Dependencies between skills: `ranking-format` and
`depth-ui-reel` use the cut steps of `business-short-form-reels`; `split-screen-document-plus-animations` needs
`educational-youtube-editor`; `fitted-stacked-captions` sits on top of the reel styles; `personal-short-form-reels` is
better with `personal-broll-library`. Each skill's SETUP.md checks for what it needs and says so.

## The first run

The first time a skill is used, Claude:

1. checks the tools above and says exactly what is missing;
2. asks the setup questions **one at a time**: who they are, their brand colours and fonts, their transcriber, where
   files live, then the questions that belong to that skill (how they film, how they like to work, what must never be
   shown, and so on);
3. for the editing skills, asks for **two or three reference videos**: the client downloads them and drops them into
   the chat, Claude studies them and proposes which of the defaults to change;
4. fills every placeholder in the skill and confirms.

Answers are saved once in `~/.claude/creator-profile/` and shared between the skills, so a client who installs a
second skill is only asked that skill's own questions. "Redo my setup" re-runs it. Anything the client tells Claude
while working ("never do X") is saved to their notes file and applied from then on.

The API key is never typed into the chat: the interview tells the client how to add it to their own shell profile.

## How the placeholders work (for whoever maintains the pack)

- Placeholders are written `@@LIKE_THIS@@` and live in the skill files themselves (instructions, engine code, CSS).
- `setup/SETUP.md` is the interview for the skill; `setup/SHARED-SETUP.md` holds the questions shared by every skill;
  `setup/questions.json` lists every answer and which ones are required.
- `setup/apply_profile.py` saves answers (`--set`, `--set-skill`), reports what is missing (`--status`) and fills the
  placeholders. It keeps an untouched copy of the template in `setup/.pristine/`, so answers can be changed and
  re-applied at any time.
- `scripts/stt.py` is the single transcription door: ElevenLabs or local, same output shape either way.
- `_shared/setup/` is the master copy of the shared files; `_build/make_templates.py` and `_build/TEMPLATE-SPEC.md`
  record how the templates were produced from the originals.

## Before sending to a client

- Each skill's style section is the tested default look. It is deliberately kept: clients change it through their
  references and corrections, not by starting from nothing.
- The `examples/` folders hold worked builds from the original style, scrubbed of names and assets, as code
  references only. Delete a skill's `examples/` folder if you would rather clients did not see them.
- No commercial fonts, sound packs, music or footage ship in the pack. Clients bring their own, and the interview
  asks where they are.
