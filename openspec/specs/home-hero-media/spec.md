# home-hero-media Specification

## Purpose

Defines how the home page hero and the scroll journey present motion media: which assets load on which devices, how the hero video plays, the static fallbacks, and the asset size budgets that keep the page fast.

## Requirements

### Requirement: Hero plays the migration-to-growth video once on capable desktops
The home hero SHALL play the migration-to-growth video (rack corridor, data particles, meshed cloud, growth chart) exactly once, muted and inline, when the viewport is at least 1000px wide with a fine pointer, the user has not requested reduced motion, and Save-Data is off. When playback ends, the hero SHALL keep the final growth-chart frame visible as its background. The video SHALL NOT loop.

#### Scenario: Desktop visitor sees the video play once
- **WHEN** a visitor opens the home page on a 1440px-wide desktop with a mouse, motion allowed and Save-Data off
- **THEN** the hero video starts muted after it can play, fades in over the poster, plays its 15-second sequence once, and stays on the final growth-chart frame

#### Scenario: Autoplay is blocked
- **WHEN** the browser rejects muted autoplay
- **THEN** the hero shows the static first-frame poster and no error is visible to the visitor

### Requirement: Hero does not download video where it does not play
The home page SHALL NOT download any hero video bytes on viewports narrower than 1000px, when the user has requested reduced motion, or when Save-Data is on. In those cases the hero SHALL present a static image or the solid hero background, and all hero text and calls to action SHALL stay fully visible.

#### Scenario: Mobile visitor
- **WHEN** a visitor opens the home page on a 390px-wide phone
- **THEN** no request for the hero MP4 or WebM file is made and the hero headline, copy and both CTAs are visible

#### Scenario: Reduced motion on desktop
- **WHEN** a desktop visitor has `prefers-reduced-motion: reduce`
- **THEN** no hero video request is made and the hero shows the static poster image

#### Scenario: Save-Data on desktop
- **WHEN** a desktop visitor has Save-Data enabled
- **THEN** no hero video request is made and the hero shows the static poster image

### Requirement: Hero video is served in two formats without audio
The hero video SHALL be available as WebM (VP9) and MP4 (H.264). The page SHALL request WebM when the browser can play VP9 and MP4 otherwise. Neither file SHALL contain an audio track. The poster SHALL be the first frame of the video, so the fade from poster to video shows no visual jump.

#### Scenario: Browser without VP9 support
- **WHEN** a capable desktop browser cannot play `video/webm; codecs="vp9"`
- **THEN** the page requests the MP4 file

#### Scenario: Assets carry no audio
- **WHEN** the published hero WebM and MP4 files are inspected
- **THEN** each contains exactly one video stream and no audio stream

### Requirement: Hero media stays within size budgets
The published hero media SHALL stay within these budgets: MP4 at most 3.5 MB, WebM at most 2.5 MB, desktop poster WebP at most 200 KB, mobile still WebP at most 100 KB. The 14.7 MB source file SHALL NOT be published with the site.

#### Scenario: Audit checks the budgets
- **WHEN** `tests/site-audit.sh` runs against a fresh Hugo build
- **THEN** it fails if any hero media file exceeds its budget or if the source file appears in the build output

### Requirement: Hero effects stay legible over the video
While the hero video is playing, the decorative neural canvas SHALL run at reduced intensity so that it does not compete with the particles and mesh inside the video. The hero headline, copy, CTAs and KPI strip SHALL keep at least WCAG AA contrast against every frame of the video, including the final growth-chart frame.

#### Scenario: Neural canvas while video plays
- **WHEN** the hero video is playing on a capable desktop
- **THEN** the neural canvas is visibly dimmer than when no video is playing

#### Scenario: Final frame legibility
- **WHEN** the video has ended on the growth-chart frame at 1280px, 1440px and 1920px widths
- **THEN** the headline, copy, CTAs and KPI strip remain readable, and the orange growth curve stays visible in the gap between the text column and the credentials card (the chart bars may sit partly behind the text column and the card)

### Requirement: Journey chapters use stills from the same video
The scroll journey (`#jornada`) SHALL use stills from the same video for its three chapters: the rack corridor for "01 · Migração para a AWS", the meshed cloud for "02 · Operação gerenciada 24/7", and the growth chart for "03 · Segurança & resultado". Each chapter SHALL also have a mobile-sized still. Chapter copy and CTAs SHALL NOT change.

#### Scenario: Desktop journey
- **WHEN** a desktop visitor scrolls through the journey
- **THEN** the backgrounds move from the rack corridor to the meshed cloud to the growth chart in chapter order

#### Scenario: Mobile journey
- **WHEN** a mobile visitor scrolls through the stacked chapters
- **THEN** each chapter shows the mobile still of its matching scene

### Requirement: Retired hero media is removed
Media files that the home no longer references after this change SHALL be removed from the site, and the home SHALL NOT reference any removed file.

#### Scenario: No dangling references
- **WHEN** the Hugo build completes
- **THEN** every `/media/` URL referenced by the home exists in the build output, and no retired file (for example `hero-loop.mp4`) is present
