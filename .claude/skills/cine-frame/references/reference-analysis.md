# Cine Frame reference: measured specs

Source: the "referencia cinematica" reel Nahuel sent on 2026-10-23 (man talking to camera in a car, 23 s).

## File

- 720x1280 (9:16), H.264 High, **24 fps** constant, SDR bt709 (tv range), AAC stereo 44.1 kHz.
- Platform re-encode (about 330 kb/s), so the original was probably 1080x1920.

## Layout (scaled to 1080x1920)

| Element | Measure |
|---|---|
| Canvas | solid black |
| Picture band | full width, ~1080x830 (4:3), vertically centred (top ~543, bottom ~1374) |
| Headline | 2 lines, uppercase, white, bold geometric sans (Inter Bold / SF Pro Display Bold), centred, bottom edge ~35 px above the band, cap height ~40 px, no shadow, no box |
| Captions | 1-3 words, sentence case, white bold sans with a soft dark shadow, centred, ~64% down the band (chest height) |
| Bottom area | empty black |

## Picture and motion

- One continuous take (no scene cuts detected), camera fixed on the dashboard, slight wide angle.
- Grade: cool/teal shadows, warm skin, low saturation, soft roll-off in the highlights, deep blacks.
- Ending: picture, text and sound fade down together over the last ~1 s.
- Pace comes from the captions changing every 0.3-0.8 s, not from cuts.

## iPhone 14 Pro settings to record for this style

Settings > Camera > Record Video:

- **4K at 24 fps** (30 fps is fine if he prefers smoother motion; the edit converts to 24).
- **HDR Video: OFF.** HDR (HLG / Dolby Vision) made the earlier renders fail. If it is left on, `prep` tone-maps
  to SDR automatically, but recording SDR gives truer colour.
- **Auto FPS: off.** Formats: **Most Compatible** (H.264).
- Use normal **Video** mode, not Cinematic mode (Cinematic adds fake background blur and records HDR; the film
  look is added in the edit).
- Lens **1x** on the rear camera when the phone is mounted; the front camera is fine handheld.
- Hold it **vertical**. The edit crops a 4:3 band from the middle, so keep the face in the centre with some
  space above the head and nothing important at the very top or bottom.
- Long-press on the face to lock exposure and focus (AE/AF LOCK).
