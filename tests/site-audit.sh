#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_dir="$(mktemp -d "${TMPDIR:-/tmp}/corescale-site-audit.XXXXXX")"
build_log="$build_dir/hugo-build.log"
trap 'rm -rf "$build_dir"' EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

assert_file() {
  [[ -f "$1" ]] || fail "arquivo ausente: $1"
}

assert_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  grep -E -q "$pattern" "$file" || fail "$message"
}

assert_not_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if grep -E -q "$pattern" "$file"; then
    fail "$message"
  fi
}

hugo --source "$repo_root/hugo" \
  --destination "$build_dir/public" \
  --cleanDestinationDir \
  --printPathWarnings >"$build_log" 2>&1 || {
    cat "$build_log" >&2
    fail "build Hugo falhou"
  }

assert_not_contains "$build_log" "WARN|deprecated" "build Hugo contém avisos"

home="$build_dir/public/index.html"
article="$build_dir/public/blog/finops-reduzir-fatura-aws/index.html"
categories="$build_dir/public/categories/index.html"
catalogo="$build_dir/public/catalogo/index.html"

assert_file "$home"
assert_file "$article"
assert_file "$categories"
assert_file "$catalogo"

assert_contains "$catalogo" "Catálogo de Ofertas CoreScale" "catálogo sem título principal"
assert_contains "$catalogo" "data-filter=\"seguranca\"" "catálogo sem filtro de segurança"
assert_contains "$catalogo" "data-filter=\"ia\"" "catálogo sem filtro de IA"
assert_contains "$catalogo" "SEC-ASSESS" "catálogo sem oferta SEC-ASSESS"
assert_contains "$catalogo" "WAR-EXPRESS" "catálogo sem oferta WAR-EXPRESS"
assert_contains "$catalogo" "AI-RAG" "catálogo sem oferta AI-RAG"
assert_contains "$home" "href=\"/catalogo/\"" "home sem link para catálogo no header"
assert_contains "$catalogo" 'id="rm-menu-btn"' "catálogo sem header de navegação"
assert_contains "$catalogo" 'href="/catalogo/" aria-current="page"' "catálogo sem item de menu ativo"
assert_not_contains "$home" 'aria-current="page"' "home marca item de menu como ativo indevidamente"
assert_not_contains "$repo_root/hugo/layouts/partials/rd-header.html" 'href="/catalogo/" style="[^"]*color:#FF9900' "link do catálogo com cor de destaque fixa"
assert_contains "$categories" '<h1[^>]*>Categorias</h1>' "listagem de categorias sem título"
assert_contains "$categories" 'href="/categories/' "listagem de categorias sem links"

assert_contains "$home" '<link rel="canonical" href="https://corescale.com.br/">' "home sem URL canônica"
assert_contains "$home" '<meta name="description" content="[^"]+">' "home sem descrição"
assert_contains "$home" '<meta property="og:title" content="[^"]+">' "home sem og:title"
assert_contains "$home" '<meta property="og:description" content="[^"]+">' "home sem og:description"
assert_contains "$home" '<meta property="og:url" content="https://corescale.com.br/">' "home sem og:url"
assert_contains "$home" '<meta property="og:image" content="https://corescale.com.br/og-image.png">' "home sem imagem social absoluta"
assert_contains "$home" '<meta name="twitter:card" content="summary_large_image">' "home sem Twitter Card"
assert_contains "$home" '"@type": *"ProfessionalService"' "home sem JSON-LD da empresa"
assert_contains "$article" '<meta property="og:type" content="article">' "artigo sem og:type article"
assert_contains "$article" '"@type": *"Article"' "artigo sem JSON-LD Article"

assert_contains "$home" 'href="#conteudo-principal"[^>]*>Pular para o conteúdo</a>' "home sem link para pular conteúdo"
assert_contains "$home" '<main id="conteudo-principal"' "home sem landmark principal"
assert_contains "$home" 'id="rm-menu-btn"[^>]*aria-controls="rm-mobile-nav"[^>]*aria-expanded="false"' "botão do menu sem estado ARIA"
assert_contains "$home" 'aria-label="Falar com a CoreScale pelo WhatsApp"' "atalho do WhatsApp sem nome acessível"
assert_contains "$home" 'aria-label="CoreScale no LinkedIn"' "link do LinkedIn sem nome acessível"
assert_contains "$repo_root/hugo/layouts/_default/baseof.html" 'menuBtn\.setAttribute\(.aria-expanded.' "script não atualiza aria-expanded"
assert_contains "$repo_root/hugo/layouts/_default/baseof.html" "e\.key==='Escape'" "menu não fecha pela tecla Escape"

assert_contains "$home" '<label[^>]*for="contato-nome"' "label de nome sem associação"
assert_contains "$home" 'id="contato-nome"[^>]*required[^>]*autocomplete="name"' "campo nome sem semântica de formulário"
assert_contains "$home" 'id="contato-email"[^>]*required[^>]*autocomplete="email"' "campo e-mail sem semântica de formulário"
assert_contains "$home" 'id="contato-telefone"[^>]*required[^>]*autocomplete="tel"' "campo telefone sem semântica de formulário"
assert_contains "$home" 'name="website"' "formulário sem honeypot real"
assert_contains "$home" 'aria-live="polite"' "formulário sem região de status acessível"
assert_contains "$home" 'href="/privacidade/"' "formulário sem link de privacidade"
assert_contains "$repo_root/hugo/layouts/_default/baseof.html" "website:g\('website'\)" "script não envia o valor real do honeypot"
assert_not_contains "$repo_root/hugo/layouts/_default/baseof.html" 'alert\(' "feedback do formulário ainda usa alert"

assert_contains "$repo_root/hugo/layouts/index.html" 'where \.Site\.RegularPages "Section" "blog"' "home não consulta artigos dinamicamente"
assert_contains "$repo_root/hugo/layouts/index.html" 'first 3' "home não limita a consulta aos três artigos mais recentes"
assert_contains "$home" 'FinOps na AWS: como reduzir a fatura em 30–40% sem perder performance' "home não contém o artigo mais recente"
assert_contains "$home" 'IA Generativa na AWS: como usar o Bedrock sem virar refém de vendor lock-in' "home não contém o segundo artigo mais recente"
assert_contains "$home" 'VMware e Broadcom: por que 2026 é o ano de migrar para a AWS' "home não contém o terceiro artigo mais recente"
assert_contains "$home" 'Resultados e benefícios variam conforme' "home sem qualificação dos claims"

assert_contains "$home" 'src="/aws-logo.png"[^>]*loading="lazy"[^>]*decoding="async"' "imagem AWS sem hints de carregamento"
# assert_contains "$home" 'src="/cleiton.png"[^>]*loading="lazy"[^>]*decoding="async"' "foto do CEO sem hints de carregamento"
# assert_contains "$home" 'src="/joao.png"[^>]*loading="lazy"[^>]*decoding="async"' "foto do CTO sem hints de carregamento"
assert_contains "$home" 'src="/corescale-logo.png"[^>]*width="[0-9]+"[^>]*height="[0-9]+"' "logo sem dimensões intrínsecas"
assert_not_contains "$home" 'header\.mp4|yas\.mov' "home referencia mídia obsoleta"

# Mídia do hero e da jornada (spec home-hero-media)
public_dir="$build_dir/public"
assert_contains "$home" 'data-src-webm="/media/hero-shift\.webm"' "hero sem fonte WebM do vídeo"
assert_contains "$home" 'data-src-mp4="/media/hero-shift\.mp4"' "hero sem fonte MP4 do vídeo"
assert_not_contains "$home" 'hero-loop\.|scene-migration|scene-core' "home referencia mídia aposentada"

while IFS= read -r media_path; do
  assert_file "$public_dir$media_path"
done < <(grep -oE '/media/[A-Za-z0-9._-]+' "$home" | sort -u)

assert_max_size() {
  local file="$1"
  local max_bytes="$2"
  assert_file "$file"
  local size
  size="$(stat -c %s "$file")"
  (( size <= max_bytes )) || fail "$(basename "$file") com $size bytes excede o orçamento de $max_bytes bytes"
}

assert_max_size "$public_dir/media/hero-shift.mp4" 3500000
assert_max_size "$public_dir/media/hero-shift.webm" 2500000
for still in hero-shift-poster journey-migration journey-cloud journey-growth; do
  assert_max_size "$public_dir/media/$still.webp" 200000
  assert_max_size "$public_dir/media/$still-mobile.webp" 100000
done

if find "$public_dir" -name 'hero-loop.*' -o -name 'One-single-continuous-*' | grep -q .; then
  fail "build contém mídia aposentada ou o vídeo-fonte"
fi

if command -v ffprobe >/dev/null 2>&1; then
  for video in "$public_dir/media/hero-shift.mp4" "$public_dir/media/hero-shift.webm"; do
    [[ -z "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$video")" ]] \
      || fail "$(basename "$video") contém trilha de áudio"
  done
else
  echo "site-audit: ffprobe ausente, verificação de áudio do hero ignorada"
fi

echo "site-audit: OK"

# Verificação da Landing Page The Next Shift (pós-evento privada)
next_shift="$build_dir/public/the-next-shift/index.html"
assert_file "$next_shift"
assert_contains "$next_shift" 'name="robots" content="noindex, nofollow"' "landing page the-next-shift deve conter meta noindex, nofollow"
assert_contains "$next_shift" "The Next Shift" "landing page sem menção ao The Next Shift"
assert_contains "$next_shift" "Workshop de Priorização de IA" "landing page sem Trilha 1 (IA)"
assert_contains "$next_shift" "Fundação de Dados e Migração para IA" "landing page sem Trilha 2 (Fundação de Dados)"
assert_contains "$next_shift" "Fale Diretamente com o Nosso Time pelo WhatsApp" "landing page sem chamada para a comunidade WhatsApp"
