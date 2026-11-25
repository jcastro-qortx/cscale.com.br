# Design: Catálogo de Produtos e Ofertas de Prateleira CoreScale

## Context

O site da CoreScale é construído em Hugo (Go templates), utiliza HTML semântico com estilização inline consistente (`theme/palette CoreScale`), vanilla JavaScript modular sem frameworks pesados externos e é entregue via AWS S3 + CloudFront.
Para a introdução de ofertas fechadas em `/catalogo/`, o design deve manter a velocidade e leveza do site (< 100ms de build, zero dependências externas de CDN), garantindo plena compatibilidade com o pipeline GitHub Actions e a suíte de auditoria (`site-audit.sh`).

## Goals / Non-Goals

**Goals:**
- Implementar a página `/catalogo/` como uma seção nativa do Hugo (`hugo/content/catalogo/_index.md` + `hugo/layouts/catalogo/list.html`).
- Estruturar o modelo de dados de cada oferta em data files ou frontmatter para facilitar manutenção pelo time comercial/marketing.
- Implementar filtragem reativa via atributos `data-category` em vanilla JavaScript com acessibilidade ARIA (`role="tab"`, `aria-selected`).
- Criar cards de produto densos em informação:
  - Header: Código interno (`SEC-ASSESS`, `WAR-EXPRESS`), Badge de vertical e Duração típica.
  - Corpo: Resumo do problema, ambiente de partida, fases e entregáveis.
  - Tabela colapsável de indicadores medidos (o que mede vs o que muda).
  - CTA com URL encoding para WhatsApp e atalho para o formulário.
- Atualizar links do menu e rodapé.
- Validar no harness regressivo e compilação do Hugo.

**Non-Goals:**
- Não construir checkout ou cobrança online (as ofertas iniciam com agendamento de alinhamento técnico/comercial).
- Não criar páginas filhas individuais para cada oferta neste primeiro momento (todas as 6 ofertas vivem em visualização consolidada com colapso/expansão na página principal `/catalogo/`).
- Não adicionar bibliotecas pesadas de frontend (React, Vue, jQuery).

## Decisions

### Decisão 1: Modelo de Dados das Ofertas via Hugo Data Files (`data/catalogo.yaml`)
- **Escolha:** Armazenar as 6 ofertas estruturadas em `hugo/data/catalogo.yaml` e iterar no template `hugo/layouts/catalogo/list.html`.
- **Racional:** Desacopla o conteúdo técnico e comercial da marcação HTML, permitindo que novos produtos ou mudanças de escopo sejam adicionados simplesmente editando o YAML.
- **Alternativa descartada:** Criar 6 arquivos markdown separados com layouts complexos, o que fragmentaria a navegação do usuário e dificultaria a comparação de ofertas.

### Decisão 2: Filtragem de Categorias via Vanilla JS e CSS Display
- **Escolha:** Uso de botões com `data-filter` e cards com `data-category`. Ao clicar, um script leve altera a exibição e os atributos `aria-pressed`/`aria-selected`.
- **Racional:** Respeita a regra de zero frameworks JS, carrega instantaneamente e preserva renderização mesmo se o script falhar (fallback padrão exibe todos os cards).

### Decisão 3: Padronização Visual e Paleta CoreScale
- **Escolha:** Reutilizar os componentes canônicos: Hero escuro com gradientes (`#1E2839` / `#1A2333`), cards em fundo branco (`#ffffff`) sobre fundo bege suave (`#F4F2EA`), badges com acentos laranja AWS (`#FF9900`) e roxo CoreScale (`#8A4FBE`).

## Risks / Trade-offs

- **[Risco] Conteúdo dos cards ficar visualmente muito longo**  
  → *Mitigação*: Uso de seções colapsáveis (`<details>` / `<summary>` estilizados nativamente) para a tabela de fases e indicadores medidos, mantendo a visualização inicial dos cards compacta e escaneável.
- **[Risco] Quebra na suíte regressiva `site-audit.sh`**  
  → *Mitigação*: Adicionar novas asserções ao script de auditoria que testam a compilação de `/catalogo/index.html` e a presença dos cards e links.

## Migration Plan

1. Criar `hugo/data/catalogo.yaml` com as 6 ofertas completas.
2. Criar `hugo/layouts/catalogo/list.html` e `hugo/content/catalogo/_index.md`.
3. Inserir links de navegação em `hugo/layouts/partials/rd-header.html` e `hugo/layouts/partials/rd-footer.html`.
4. Atualizar `tests/site-audit.sh` com asserções da nova rota.
5. Executar suíte local de auditoria e build `--minify`.
6. Submeter ao GitHub para disparo automático do pipeline S3 + CloudFront.
