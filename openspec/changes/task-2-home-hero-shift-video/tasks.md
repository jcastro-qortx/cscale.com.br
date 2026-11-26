# Tasks

## 1. Media encoding

- [x] 1.1 Add `scripts/encode-hero-media.sh` (source path as argument; resolves `ffmpeg` from PATH or `FFMPEG` env) that writes `hero-shift.{mp4,webm}`, `hero-shift-poster{,-mobile}.webp` and `journey-{migration,cloud,growth}{,-mobile}.webp` to `hugo/static/media/`; verify `bash -n` passes and a run produces all 10 files
- [x] 1.2 Tune MP4 (H.264, faststart, `-an`) to ≤ 3.5 MB and WebM (VP9, `-an`) to ≤ 2.5 MB at 1920x1080; verify with `stat -c %s` and `ffprobe` showing one video stream and no audio stream; visually check dark gradients for banding
- [x] 1.3 Pick journey still timestamps by inspecting frames (corridor ~1 s, cloud ~9–10 s, final chart frame); poster is t=0; verify desktop WebP ≤ 200 KB and mobile WebP ≤ 100 KB

## 2. Hero reactivation

- [x] 2.1 In `hugo/layouts/index.html`, point hero `<img>` srcset and `<video poster>` to `hero-shift-poster{,-mobile}.webp`, add `data-src-webm="/media/hero-shift.webm"` and `data-src-mp4="/media/hero-shift.mp4"`, and replace the "vídeo desativado" comment; verify on `hugo server` (desktop) that the video fades in, plays once and holds the final frame
- [x] 2.2 In `hugo/layouts/_default/baseof.html`, switch the hero preload to `hero-shift-poster.webp` and add `media="(min-width: 1000px)"`; drop the `poster` attribute from `<video>` (the `<img>` already shows frame 0); verify in DevTools Network that a 390px viewport fetches no video and no desktop poster (only the 36 KB mobile poster via the existing `<img>`)
- [x] 2.3 In `cinematic.js`, add an `is-playing-video` class on the hero when playback actually starts (`playing` event, so blocked autoplay keeps full intensity), and in `cinematic.css` transition `.cine-neural` opacity to ~0.35 under that class; verify the canvas visibly dims when playback starts and stays dimmed after `ended`
- [x] 2.4 Visual QA of the final frame at 1280, 1440 and 1920 widths; tune `object-position` and the right side of `.cine-hero-grade` so the growth chart is not covered by the text column and stays readable next to the credentials card; verify with screenshots of each width

## 3. Journey stills

- [x] 3.1 Update the three `.cine-layer` backgrounds and the `--chbg`/`--chbg-m` variables of the three `.cine-chapter` articles to `journey-migration`, `journey-cloud` and `journey-growth` (+ `-mobile`); verify desktop scroll shows corridor → cloud → chart and a 390px viewport shows the matching mobile stills
- [x] 3.2 Check chapter text contrast over the new stills (especially the brighter cloud mesh); adjust tint class per layer if needed; verify the chapter headline and copy stay readable on desktop and mobile

## 4. Cleanup

- [x] 4.1 Run `rg -n "hero-loop|scene-migration|scene-core" hugo tests` and delete `hero-loop.{mp4,webm}` and every `scene-*.webp` with no remaining reference; verify the search returns no hits outside docs
- [x] 4.2 Ensure the 14.7 MB source video is neither committed nor under `hugo/`: resolve the design open question with the user (move outside the repo or `.gitignore` it); verify `git status` does not list it as a file to commit

## 5. Audit and verification

- [x] 5.1 Extend `tests/site-audit.sh`: home contains both `data-src-*` hero attributes; every `/media/` URL referenced by the home exists in the build; size budgets for MP4, WebM, poster and mobile stills; no `hero-loop.*` or source file in the build; optional `ffprobe` no-audio check that is skipped with a note when `ffprobe` is missing; verify the script fails on a temporarily oversized file and passes on the real assets
- [x] 5.2 Run the full `tests/site-audit.sh` and confirm it passes with no Hugo warnings
- [x] 5.3 Cross-check reduced motion (DevTools emulation), Save-Data and autoplay-blocked behavior against the spec scenarios; record the results in the Backlog task TASK-2 notes
