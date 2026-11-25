# Proposal: Catálogo de Produtos e Ofertas de Prateleira CoreScale

Backlog task: TASK-1

## Why

Atualmente o site da CoreScale (`corescale.com.br`) foca em serviços corporativos genéricos (MSP, Migração, FinOps e IA Generativa) sem apresentar produtos de escopo fechado, prazos rígidos, entregáveis padronizados e métricas contratuais auditáveis.
Seguindo referências de mercado de parceiros AWS de alto desempenho (como a RFX Tecnologia), a criação de um Catálogo de Produtos de Prateleira (`/catalogo/`) permite qualificação imediata de leads, diminui a fricção do ciclo comercial e estabelece ofertas de entrada claras para Segurança (CIS/LGPD), Arquitetura (Well-Architected Review com financiamento AWS) e GenAI aplicada (Bedrock, Knowledge Bases e Textract).

## What Changes

- Criação da seção e página de Catálogo de Ofertas (`/catalogo/`) no site Hugo.
- Estruturação de 6 ofertas de prateleira com modelo padronizado:
  1. `SEC-ASSESS`: Assessment & Auditoria de Postura AWS (CIS v3.0 / GuardDuty / IAM).
  2. `WAR-EXPRESS`: AWS Well-Architected Review Express com destrave de até US$ 5.000 em créditos AWS.
  3. `AI-ASSESS`: AI Readiness Assessment (diagnóstico de prontidão, LGPD, custos e seleção do caso piloto).
  4. `AI-RAG`: Base de Conhecimento Corporativa Segura (Amazon Bedrock Knowledge Bases + Guardrails).
  5. `AI-EXTRACT`: Extração Inteligente de Documentos para ERP (Textract + Bedrock).
  6. `AI-AGENT`: Agente Autônomo de Atendimento e Triagem (WhatsApp / Webchat via Bedrock AgentCore).
- Sistema de filtragem interativo e responsivo no frontend: `Todos`, `Segurança`, `Arquitetura`, `FinOps`, `IA Aplicada`.
- Cards com badges de prazo estimado (`1 a 2 semanas`, `2 a 3 semanas`, etc.), público-alvo, escopo por fases e tabela de indicadores medidos.
- Links de CTA contextualizados com pré-preenchimento no WhatsApp e no formulário de contato oficial.
- Inclusão do link do Catálogo no menu global (`rd-header.html`) e rodapé (`rd-footer.html`).
- Metadados SEO OpenGraph e Structured Data `ItemList` / `Product` para indexação orgânica.

## Capabilities

### New Capabilities
- `catalog-offers`: Catálogo interativo de produtos de prateleira com filtros por vertical técnica, detalhamento de escopo, entregáveis, prazos, indicadores medidos e conversão direta.

### Modified Capabilities
<!-- Nenhuma especificação anterior existe no repositório. -->

## Impact

- **Código:** Novos templates Hugo em `hugo/layouts/catalogo/`, novo conteúdo em `hugo/content/catalogo/` e ajustes de links em `hugo/layouts/partials/rd-header.html` e `rd-footer.html`.
- **Testes:** Extensão de `tests/site-audit.sh` para verificar a existência de `/catalogo/`, filtros, marcação semântica e links funcionais.
- **Deploy:** Validação automática e deploy contínuo em S3 e CloudFront via pipeline existente do GitHub Actions.
