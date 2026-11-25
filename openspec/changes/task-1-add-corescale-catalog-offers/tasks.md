# Tasks

## 1. Estruturação dos Dados de Ofertas

- [ ] 1.1 Criar o diretório `hugo/data` e o arquivo `hugo/data/catalogo.yaml` contendo as 6 ofertas com metadados (id, categoria, título, duração, público, ambiente de partida, fases, entregáveis, indicadores medidos e texto do CTA WhatsApp). Verificar sintaxe válida com parser YAML.
- [ ] 1.2 Criar o arquivo de conteúdo Hugo `hugo/content/catalogo/_index.md` com título, descrição de SEO e metadados de compartilhamento.

## 2. Layouts e Componentes do Catálogo

- [ ] 2.1 Criar `hugo/layouts/catalogo/list.html` implementando o Hero escuro temático, barra de filtros interativa (Todos, Segurança, Arquitetura, IA Aplicada), grid responsivo de cards e tabela colapsável de indicadores.
- [ ] 2.2 Integrar script vanilla JS para filtro por categoria (`data-filter` e `data-category`) com sincronização de estados ARIA e comportamento acessível por teclado.
- [ ] 2.3 Atualizar os menus globais em `hugo/layouts/partials/rd-header.html` e `hugo/layouts/partials/rd-footer.html` adicionando o link para `/catalogo/`.

## 3. Testes Regressivos e Validação Local

- [ ] 3.1 Atualizar `tests/site-audit.sh` adicionando asserções para existência de `/catalogo/index.html`, presença dos filtros e das 6 ofertas renderizadas.
- [ ] 3.2 Executar `bash tests/site-audit.sh` e `hugo --source hugo --cleanDestinationDir --minify` e verificar saída 100% verde sem avisos ou erros.

## 4. Publicação e Deploy Contínuo

- [ ] 4.1 Realizar commit das alterações com mensagem padronizada no repositório `cscale.com.br`.
- [ ] 4.2 Enviar push para o branch `main` no GitHub e monitorar a execução bem-sucedida do workflow do GitHub Actions (S3 sync e CloudFront invalidation).
- [ ] 4.3 Validar a página `/catalogo/` respondendo em produção com status HTTP 200 e dados corretos.
