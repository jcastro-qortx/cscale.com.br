#!/usr/bin/env bash
# Encode the home hero video and journey stills from a single source clip.
#
# Usage: scripts/encode-hero-media.sh <source.mp4>
#
# Env overrides:
#   FFMPEG       ffmpeg binary (default: ffmpeg on PATH)
#   MP4_CRF      H.264 CRF (default 28)
#   WEBM_CRF     VP9 CRF (default 38)
#   T_MIGRATION  still timestamp for chapter 01 (default 1.0)
#   T_CLOUD      still timestamp for chapter 02 (default 9.5)
#   T_GROWTH     still timestamp for chapter 03 (default: last frame)
#
# Outputs (hugo/static/media/):
#   hero-shift.mp4, hero-shift.webm
#   hero-shift-poster.webp, hero-shift-poster-mobile.webp
#   journey-{migration,cloud,growth}.webp + -mobile.webp
set -euo pipefail

src="${1:-}"
[[ -n "$src" && -f "$src" ]] || { echo "usage: $0 <source.mp4>" >&2; exit 1; }

ff="${FFMPEG:-ffmpeg}"
command -v "$ff" >/dev/null 2>&1 || { echo "ffmpeg not found (set FFMPEG)" >&2; exit 1; }

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$repo_root/hugo/static/media"
mkdir -p "$out"

mp4_crf="${MP4_CRF:-28}"
webm_crf="${WEBM_CRF:-38}"
t_migration="${T_MIGRATION:-1.0}"
t_cloud="${T_CLOUD:-9.5}"

run() { "$ff" -hide_banner -loglevel error -y "$@"; }

echo "▶ MP4 (H.264, CRF $mp4_crf)"
run -i "$src" -an -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -preset slow -crf "$mp4_crf" -movflags +faststart "$out/hero-shift.mp4"

echo "▶ WebM (VP9, CRF $webm_crf, two-pass)"
passlog="$(mktemp -d)/vp9"
run -i "$src" -an -c:v libvpx-vp9 -b:v 0 -crf "$webm_crf" -row-mt 1 \
  -pass 1 -passlogfile "$passlog" -f null /dev/null
run -i "$src" -an -c:v libvpx-vp9 -b:v 0 -crf "$webm_crf" -row-mt 1 \
  -pass 2 -passlogfile "$passlog" "$out/hero-shift.webm"
rm -rf "$(dirname "$passlog")"

# still <seek-args> <name>: writes <name>.webp (2048w) and <name>-mobile.webp (1080w)
still() {
  local name="${*: -1}"
  local seek=("${@:1:$#-1}")
  run "${seek[@]}" -i "$src" -frames:v 1 -vf "scale=2048:-2:flags=lanczos" \
    -c:v libwebp -quality 80 "$out/$name.webp"
  run "${seek[@]}" -i "$src" -frames:v 1 -vf "scale=1080:-2:flags=lanczos" \
    -c:v libwebp -quality 78 "$out/$name-mobile.webp"
}

echo "▶ Stills"
still -ss 0 hero-shift-poster
still -ss "$t_migration" journey-migration
still -ss "$t_cloud" journey-cloud
if [[ -n "${T_GROWTH:-}" ]]; then
  still -ss "$T_GROWTH" journey-growth
else
  still -sseof -0.1 journey-growth
fi

echo "✓ Done:"
ls -l "$out"/hero-shift* "$out"/journey-*
