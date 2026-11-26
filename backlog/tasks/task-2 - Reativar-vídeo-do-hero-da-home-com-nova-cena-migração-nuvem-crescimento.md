---
id: TASK-2
title: Reativar vídeo do hero da home com nova cena migração-nuvem-crescimento
status: In Progress
assignee:
  - '@claude'
created_date: '2026-11-26 23:37'
updated_date: '2026-11-26 23:50'
labels:
  - frontend
  - media
  - home
dependencies: []
documentation:
  - openspec/changes/task-2-home-hero-shift-video/proposal.md
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Usar o novo vídeo gerado (One-single-continuous-15-second-camera-m.mp4, 15s, 1920x1080: corredor de racks, partículas, nuvem em malha, gráfico de crescimento) para reativar o vídeo do hero da home, hoje desativado, e alinhar a jornada cinematográfica à mesma narrativa visual. Escopo apenas na home; /the-next-shift/ fora do escopo.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Hero da home reproduz o novo vídeo uma única vez em desktop sem movimento reduzido e sem Save-Data, terminando no quadro final estável
- [x] #2 Mobile, prefers-reduced-motion e Save-Data não baixam o vídeo e mostram imagem estática
- [x] #3 Assets otimizados: MP4 H.264 e WebM VP9 sem áudio, cada um dentro do orçamento de tamanho definido no design
- [x] #4 Jornada cinematográfica usa quadros do novo vídeo nos capítulos onde a cena corresponde
- [x] #5 tests/site-audit.sh passa com novas asserções de mídia do hero
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
OpenSpec change: openspec/changes/task-2-home-hero-shift-video (proposal, spec home-hero-media, design, tasks). Scope: home only, per user decision.

Progress (claude): 12/14 tasks. Assets encoded (MP4 3.40 MB CRF 28, WebM 2.47 MB VP9, no audio). Hero video plays once on desktop (verified headless Chromium, WebM path; MP4 path not exercised in browser). Mobile 390px, reduced motion and Save-Data: no video requests. Autoplay blocked: frame 0 stays, no errors, neural canvas stays at 0.85. Journey uses journey-{migration,cloud,growth} stills; shade and text-shadow tuned for legibility. Retired hero-loop.* and scene-*.webp removed. tests/site-audit.sh extended and passing (ffprobe audio check skipped, ffprobe not installed). Open: 2.4 final-frame framing vs spec, 4.2 source video location.

2.4 resolved: user accepted framing (curve visible in column gap, bars partly behind text/card); spec scenario updated. 4.2 resolved: /*.mp4 added to .gitignore. 14/14 tasks; openspec validate --strict OK.
<!-- SECTION:NOTES:END -->
