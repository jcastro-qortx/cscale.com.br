Backlog task: TASK-2

## Why

The home hero video has been disabled since the previous loop was retired; `hugo/layouts/index.html` keeps an empty `<video data-cine-video>` slot waiting for a new take of the "corridor (migration)" scene. A new 15-second continuous shot now exists (`One-single-continuous-15-second-camera-m.mp4`, 1920x1080, 25 fps, H.264, no audio, 14.7 MB) that tells the CoreScale story in one camera move: server-rack corridor, data particles, a meshed cloud, and a growth chart with an orange curve that settles on a stable final frame. Reactivating the hero with it, and reusing its key frames in the scroll journey, gives the home one coherent visual narrative (migration, cloud operation, business result).

## What Changes

- Encode the new source into web-ready hero assets (MP4 H.264 and WebM VP9, no audio track, size-budgeted) under `hugo/static/media/`, plus a first-frame poster and stills in WebP.
- Reactivate the home hero video: give `[data-cine-video]` the new `data-src-webm`/`data-src-mp4` sources and a first-frame poster so the play-once behavior already in `static/js/cinematic.js` takes over; the final growth-chart frame stays as the hero background.
- Adjust hero effects so they do not fight the video: lower the neural canvas intensity while the video is playing, since the video already carries particles and a network mesh, and verify text legibility and the credentials card placement against the final frame.
- Replace the three journey (`#jornada`) scene backgrounds with stills taken from the new video: rack corridor (01 Migração), meshed cloud (02 Operação gerenciada), growth chart (03 Segurança & resultado), keeping mobile variants.
- Update the hero image preload in `hugo/layouts/_default/baseof.html` to the new poster.
- Remove retired, unreferenced media (`hero-loop.mp4`, `hero-loop.webm`, and the old `scene-*.webp` files once no reference remains).
- Extend `tests/site-audit.sh` with assertions for the hero video sources, poster, and asset size budgets.
- Keep the 14.7 MB source file out of the deployed site and out of Git history.

Out of scope: `/the-next-shift/` (its reduced hero effects stay as they are), copy changes, and mobile video playback.

## Capabilities

### New Capabilities

- `home-hero-media`: How the home hero and the scroll journey present motion media: which assets load, when the video plays, the static fallbacks for mobile, reduced motion and Save-Data, and the asset size budgets.

### Modified Capabilities

None. No capability specs exist yet in `openspec/specs/`.

## Impact

- `hugo/layouts/index.html`: hero `<img>`/`<video>` sources and poster; journey `cine-layer` and `cine-chapter` background URLs.
- `hugo/layouts/_default/baseof.html`: hero image preload.
- `hugo/static/js/cinematic.js`: neural canvas intensity coupled to hero video state.
- `hugo/static/css/cinematic.css`: possible `object-position` and grade tuning for the new framing.
- `hugo/static/media/`: new encoded assets; retired assets deleted.
- `tests/site-audit.sh`: new media assertions.
- Deploy: no pipeline change; `.github/workflows/deploy.yml` already syncs `hugo/public/` to S3. Desktop page weight grows by the hero video (bounded by the size budget); mobile weight does not change.
