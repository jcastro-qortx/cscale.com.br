# CoreScale — Site (Hugo)

Site institucional da CoreScale no visual **redesign** (slate + laranja/lilás), pronto para o [Hugo](https://gohugo.io/).

## Rodar localmente

Requer **Hugo extended** (0.120+):

```bash
cd hugo
hugo server -D      # -D mostra também rascunhos (draft = true)
```

Abra http://localhost:1313. Para gerar o site estático em `public/`:

```bash
hugo --minify
```

## Estrutura

```
hugo/
├── hugo.toml                 # configuração (baseURL, título, params)
├── archetypes/               # TEMPLATES de novos conteúdos
│   ├── blog.md               # usado por "hugo new content blog/…"
│   └── cases.md              # usado por "hugo new content cases/…"
├── content/
│   ├── _index.md             # home
│   ├── migracao-vmware-aws.md
│   ├── privacidade.md
│   ├── blog/                 # 1 arquivo .md por artigo
│   └── cases/                # 1 arquivo .md por case
├── layouts/                  # templates do tema (não precisa editar p/ publicar)
│   ├── index.html            # home
│   ├── partials/             # rd-header, rd-footer, rd-cta
│   ├── blog/ · cases/ · migracao/ · privacidade/
│   └── _default/baseof.html  # <head>, fontes, estilos base
├── static/                   # imagens, /js/site.js, favicon, robots.txt
└── _preview/                 # prévias .html avulsas (abrem sem Hugo) — não são publicadas
```

## Publicar um novo artigo do blog

```bash
hugo new content blog/meu-artigo.md
```

Isso cria o arquivo a partir de `archetypes/blog.md`. Edite o front matter:

- `title` — título do artigo
- `date` — data de publicação
- `category` — selo do card (FinOps, Migração, MAP, Segurança, IA, Operação…)
- `description` — resumo de 1–2 frases (aparece no card e no topo)
- `draft` — mude para `false` para publicar

Escreva o corpo em **Markdown** (`##` seções, `###` subtítulos, listas, `>` citações). O tempo de leitura é calculado automaticamente. O artigo mais recente vira o **destaque** da página `/blog/`.

## Publicar um novo case

```bash
hugo new content cases/meu-case.md
```

A partir de `archetypes/cases.md`. Campos do front matter:

- `sector` — setor e origem (ex.: `"Logística · VMware → AWS"`)
- `metric` / `metricLabel` — número em destaque e legenda
- `desafio` / `solucao` / `resultado` — frases curtas mostradas no card da listagem
- `description` — resumo
- corpo em Markdown com as seções **Desafio / Solução / Resultado**

## Editar as páginas fixas

- **Home** — `layouts/index.html` (hero, bento de serviços, faixa MAP, parceria, métricas, contato).
- **Migração** — `layouts/migracao/single.html`.
- **Operação Gerenciada (MSP)** — `layouts/msp/single.html` (conteúdo em `content/msp.md`, rota `/msp/`).
- **IA Generativa** — `layouts/ia-generativa/single.html` (`content/ia-generativa.md`, rota `/ia-generativa/`).
- **Pagamento em Boleto** — `layouts/pagamento-boleto/single.html` (`content/pagamento-boleto.md`, rota `/pagamento-boleto/`).
- **Cabeçalho / rodapé / CTA** — `layouts/partials/rd-header.html`, `rd-footer.html`, `rd-cta.html`. O menu **Serviços** é um dropdown (hover) definido no `rd-header.html`; os itens do submenu apontam para `/msp/`, `/ia-generativa/`, `/migracao-vmware-aws/` e `/pagamento-boleto/`.
- **Cores/fontes base** — `layouts/_default/baseof.html`.

Os estilos são **inline** (fiéis ao design). Efeitos de hover/foco e o formulário de contato (abre o e-mail com os dados) são controlados por um pequeno script embutido em `layouts/_default/baseof.html` via atributos `data-hover` / `data-focus` / `data-contact-form`.

## Deploy

Qualquer host de site estático (Netlify, Cloudflare Pages, S3+CloudFront, GitHub Pages). Build: `hugo --minify`, publique a pasta `public/`. Ajuste `baseURL` no `hugo.toml`.
# Fri Jul 17 11:56:24 -03 2026
