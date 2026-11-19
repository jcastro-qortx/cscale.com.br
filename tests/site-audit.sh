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
  rg -q "$pattern" "$file" || fail "$message"
}

assert_not_contains() {
  local file="$1"
  local pattern="$2"
  local message="$3"
  if rg -q "$pattern" "$file"; then
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

assert_file "$home"
assert_file "$article"
assert_file "$categories"
assert_contains "$categories" '<h1[^>]*>Categorias</h1>' "listagem de categorias sem título"
assert_contains "$categories" 'href="/categories/' "listagem de categorias sem links"

assert_contains "$home" '<link rel="canonical" href="https://corescale.com.br/">' "home sem URL canônica"
assert_contains "$home" '<meta name="description" content="[^"]+">' "home sem descrição"
assert_contains "$home" '<meta property="og:title" content="[^"]+">' "home sem og:title"
assert_contains "$home" '<meta property="og:description" content="[^"]+">' "home sem og:description"
assert_contains "$home" '<meta property="og:url" content="https://corescale.com.br/">' "home sem og:url"
assert_contains "$home" '<meta property="og:image" content="https://corescale.com.br/og-image.png">' "home sem imagem social absoluta"
assert_contains "$home" '<meta name="twitter:card" content="summary_large_image">' "home sem Twitter Card"
assert_contains "$home" '"@type":"ProfessionalService"' "home sem JSON-LD da empresa"
assert_contains "$article" '<meta property="og:type" content="article">' "artigo sem og:type article"
assert_contains "$article" '"@type":"Article"' "artigo sem JSON-LD Article"

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
assert_contains "$home" 'src="/cleiton.png"[^>]*loading="lazy"[^>]*decoding="async"' "foto do CEO sem hints de carregamento"
assert_contains "$home" 'src="/joao.png"[^>]*loading="lazy"[^>]*decoding="async"' "foto do CTO sem hints de carregamento"
assert_contains "$home" 'src="/corescale-logo.png"[^>]*width="[0-9]+"[^>]*height="[0-9]+"' "logo sem dimensões intrínsecas"
assert_not_contains "$home" 'header\.mp4|yas\.mov' "home referencia mídia obsoleta"

echo "site-audit: OK"
