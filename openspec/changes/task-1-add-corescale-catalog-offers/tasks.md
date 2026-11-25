# Tasks

## 1. Estruturação dos Dados de Ofertas

- [x] 1.1 Criar o diretório `hugo/data` e o arquivo `hugo/data/catalogo.yaml` contendo as 6 ofertas com metadados (id, categoria, título, duração, público, ambiente de partida, fases, entregáveis, indicadores medidos e texto do CTA WhatsApp). Verificar sintaxe válida com parser YAML.
- [x] 1.2 Criar o arquivo de conteúdo Hugo `hugo/content/catalogo/_index.md` com título, descrição de SEO e metadados de compartilhamento.

## 2. Layouts e Componentes do Catálogo

- [x] 2.1 Criar `hugo/layouts/catalogo/list.html` implementando o Hero escuro temático, barra de filtros interativa (Todos, Segurança, Arquitetura, IA Aplicada), grid responsivo de cards e tabela colapsável de indicadores.
- [x] 2.2 Integrar script vanilla JS para filtro por categoria (`data-filter` e `data-category`) com sincronização de estados ARIA e comportamento acessível por teclado.
- [x] 2.3 Atualizar os menus globais em `hugo/layouts/partials/rd-header.html` e `hugo/layouts/partials/rd-footer.html` adicionando o link para `/catalogo/`.

## 3. Testes Regressivos e Validação Local

- [x] 3.1 Atualizar `tests/site-audit.sh` adicionando asserções para existência de `/catalogo/index.html`, presença dos filtros e das 6 ofertas renderizadas.
- [x] 3.2 Executar `bash tests/site-audit.sh` e `hugo --source hugo --cleanDestinationDir --minify` e verificar saída 100% verde sem avisos ou erros.

## 4. Publicação e Deploy Contínuo

- [x] 4.1 Realizar commit das alterações com mensagem padronizada no repositório `cscale.com.br`.
- [x] 4.2 Enviar push para o branch `main` no GitHub e monitorar a execução bem-sucedida do workflow do GitHub Actions (S3 sync e CloudFront invalidation).
- [x] 4.3 Validar a página `/catalogo/` respondendo em produção com status HTTP 200 e dados corretos.

## 5. Arquiteturas de Referência Oficiais AWS

- [x] 5.1 Desenhar arquiteturas de referência oficiais AWS com stencils e paleta oficial (`SEC-ASSESS`, `WAR-EXPRESS`, `AI-RAG`, `AI-EXTRACT`, `AI-AGENT`) em SVG vetorial autônomo e `.drawio` editável.
- [x] 5.2 Integrar preview visual e modal interativo no catálogo com suporte a download dos diagramas e `.drawio`.
- [x] 5.3 Deploy em produção e validação live HTTP 200 no CloudFront.
