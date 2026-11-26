# Design

## Context

See `proposal.md` for motivation and `specs/home-hero-media/spec.md` for the required behavior.

Current state, observed in the repository:

- `hugo/layouts/index.html` hero: `<img>` with `scene-migration.webp` (2048w) and `scene-migration-mobile.webp` (1080w), an empty `<video data-cine-video poster=... preload="none">`, the `.cine-hero-grade` overlay, and the `.cine-neural` canvas.
- `hugo/static/js/cinematic.js` already has the play-once logic: on desktop (`min-width: 1000px` and `pointer: fine`), without reduced motion and without Save-Data, it reads `data-src-webm`/`data-src-mp4`, prefers VP9 WebM, sets `preload="auto"`, adds `.is-ready` on `canplay`, and calls `play()`. Without `loop`, the last frame stays. With no `data-src-*` attributes it does nothing, which is why the video is off today.
- `hugo/static/css/cinematic.css`: video fades in with `.is-ready`; `object-fit: cover` at `object-position: center 58%`; below 1000px and under reduced motion, video and hero image are hidden.
- The neural canvas in the hero runs at `opacity: .85` with `mix-blend-mode: screen` and is controlled by an IntersectionObserver.
- Journey (`#jornada`): three `.cine-layer` divs plus three `.cine-chapter` articles that point at `scene-migration`, `scene-core-end` and `scene-core` (with `-mobile` variants for mobile).
- `hugo/layouts/_default/baseof.html` preloads `scene-migration.webp` with a mobile srcset.
- `hugo/static/media/hero-loop.{mp4,webm}` are not referenced anywhere.
- Source video: 1920x1080, 25 fps, 15.12 s, H.264 at about 7.8 Mbit/s, no audio, 14.7 MB, at the repository root and untracked.
- No `ffmpeg` is installed on the host. A static binary from the `imageio-ffmpeg` wheel, installed in a scratch directory, worked during planning.

## Goals / Non-Goals

**Goals:**

- Reuse the existing play-once pipeline. Supply assets and attributes; keep JavaScript changes minimal.
- Keep mobile page weight unchanged.
- Make encoding reproducible with one script.

**Non-Goals:**

- Scroll-scrubbed video in the journey. That needs all-keyframe encoding and much larger files.
- Mobile video playback.
- Changes to `/the-next-shift/` or to page copy.

## Decisions

### D1. Encoding targets
- MP4: H.264 High, `yuv420p`, 1920x1080 at 25 fps, CRF about 26 to 28, `-preset slow`, `-movflags +faststart`, `-an`. Tune CRF to land at or under 3.5 MB.
- WebM: VP9, 1920x1080, two-pass or CRF about 36 to 40 with `-b:v 0`, `-row-mt 1`, `-an`. Tune to land at or under 2.5 MB.
- Rationale: the old `hero-loop.mp4` was 3.5 MB, which sets an accepted ceiling. A dark, slow scene compresses well. Downscaling to 1600w is the fallback if quality at budget is poor.
- Alternative rejected: AV1. Encoding time and Safari support do not justify it for one 15-second clip.

### D2. File names
New names, never reusing old ones, so the 300-second CloudFront and S3 cache-control setting cannot serve stale bytes under a reused name:
- `hero-shift.mp4`, `hero-shift.webm`
- `hero-shift-poster.webp` (frame at 0 s, 2048w) and `hero-shift-poster-mobile.webp` (1080w)
- `journey-migration.webp`, `journey-cloud.webp`, `journey-growth.webp`, plus `-mobile` variants at 1080w

### D3. Still selection
- Poster: the exact first frame (t = 0), so the poster-to-video fade has no jump.
- Journey stills, picked by visual check from the planning contact sheet: about 1 s (rack corridor), about 9 to 10 s (meshed cloud fully formed), and the last frame (growth chart with the orange curve). Final timestamps are chosen at implementation time by looking at frames.
- WebP quality about 78 to 82, tuned to the budgets.

### D4. Reproducible encoding script
Add `scripts/encode-hero-media.sh` that takes the source path as an argument, finds `ffmpeg` (system binary or the `FFMPEG` environment variable), and writes all outputs into `hugo/static/media/`. The source video is not committed. Options for it are listed under Open Questions.

### D5. Neural canvas coupling
In `cinematic.js`, when the hero video gets `.is-ready`, add a class to the hero (for example `is-playing-video`) that lowers `.cine-neural` opacity from 0.85 to about 0.35 through a CSS transition. On `ended`, keep the lower opacity, because the final chart frame already carries the visual weight. Reduced motion and mobile paths are unaffected, because the canvas is already hidden there.
- Alternative rejected: stop the canvas entirely. A faint network over the video keeps the brand motif and continuity with sections that have no video.

### D6. Framing against the hero layout
The final frame centers the growth chart, while the hero puts text on the left and the credentials card on the right. Plan:
1. Visual QA of the end frame at 1280, 1440 and 1920 widths.
2. If the chart is hidden behind the card, shift `object-position` horizontally, or soften the right-side grade.
3. Keep the existing left-side dark grade for text contrast.

All changes stay in `cinematic.css`. The layout grid does not change.

Outcome of the QA: the chart is about 35% of the frame width and the gap between the columns is about 10%, so no `object-position` can show it uncovered. The user accepted the current framing: text stays legible, the curve shows in the gap, and the bars sit partly behind the text column and the card. The spec scenario was updated to match. The hero `object-position` and grade are unchanged.

### D7. Preload
Change the `baseof.html` preload to `hero-shift-poster.webp` with the same srcset pattern. The mobile preload of a hero image that CSS hides below 1000px is an existing inefficiency. Fixing it is cheap and in the same line, so the preload gets `media="(min-width: 1000px)"`.

### D8. Audit coverage
Extend `tests/site-audit.sh`:
- The home HTML contains `data-src-webm="/media/hero-shift.webm"` and `data-src-mp4="/media/hero-shift.mp4"`.
- Each referenced `/media/*` file exists in the build output.
- Size budgets use `stat -c %s` (Linux, matching the CI runner).
- The output contains no `hero-loop.*` file and no file named like the source video.
- Audio-stream checks need `ffprobe`. They run only when it is available; otherwise the audit skips them with a note.

## Risks / Trade-offs

- [Quality at budget: banding in dark gradients under VP9 or H.264] → Tune CRF; add light grain (`-tune grain` or a `noise` filter) if banding shows; fall back to 1600w.
- [Chart hidden behind the credentials card on the final frame] → D6 visual QA and `object-position` tuning before merge.
- [Desktop page weight grows by about 2.5 to 3.5 MB] → Loads only on capable desktops, after first paint with the poster; Save-Data respected; no impact on mobile LCP.
- [Stale CDN cache] → New file names (D2).
- [Removing `scene-*.webp` breaks a reference missed in search] → The D8 audit asserts that every referenced `/media/` file exists; a repository-wide search runs before deletion.

## Migration Plan

1. Encode assets and commit them together with the layout, CSS and JS changes in one commit.
2. Run `tests/site-audit.sh` and visual QA locally (`hugo server`).
3. Deploy through the existing GitHub Actions workflow (`aws s3 sync --delete`), only after explicit approval.
4. Rollback: revert the commit. Old file names are gone, but the revert restores them, and the next sync re-uploads them.

## Open Questions

- Resolved: the 14.7 MB source file stays at the repository root and is ignored through a `/*.mp4` rule in `.gitignore`.
