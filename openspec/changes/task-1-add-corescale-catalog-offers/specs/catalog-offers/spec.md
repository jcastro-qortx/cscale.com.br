# Spec Delta

## Purpose

Fornecer um catálogo público, responsivo e interativo de ofertas fechadas de prateleira da CoreScale na rota `/catalogo/`, permitindo aos decisores técnicos e executivos avaliar escopo, fases, entregáveis, prazos e métricas auditáveis em Segurança AWS, Well-Architected Review (WAR) e IA Aplicada.

## ADDED Requirements

### Requirement: Navegação e listagem de ofertas estruturadas
O sistema SHALL disponibilizar a página `/catalogo/` contendo a lista completa de ofertas de prateleira da CoreScale categorizadas por verticais de negócio.

#### Scenario: Visualização inicial do catálogo
- **WHEN** o usuário acessa a URL `/catalogo/`
- **THEN** o sistema exibe o título institucional, a descrição das ofertas de prateleira e a lista completa de cards contendo escopo, duração típica, público-alvo e entregáveis.

### Requirement: Filtragem dinâmica por vertical técnica
O sistema SHALL permitir ao usuário filtrar as ofertas exibidas em tempo real por categoria sem recarregar a página.

#### Scenario: Filtro por vertical específica
- **WHEN** o usuário clica no botão de filtro de categoria (ex.: "IA Aplicada" ou "Segurança")
- **THEN** o sistema exibe apenas os cards correspondentes à categoria selecionada e oculta os demais com transição suave.

#### Scenario: Retorno à visualização global
- **WHEN** o usuário clica no filtro "Todos"
- **THEN** o sistema reexibe todas as ofertas disponíveis no catálogo.

### Requirement: Conversão contextualizada com pré-preenchimento
Cada card de oferta SHALL fornecer canais diretos de contato (WhatsApp e formulário de avaliação) com parâmetros identificadores do produto selecionado.

#### Scenario: Acionamento de contato via WhatsApp
- **WHEN** o visitante clica no botão de agendamento de uma oferta específica
- **THEN** o link do WhatsApp é aberto com mensagem pré-definida contendo o nome e o código da oferta correspondente.

### Requirement: Acessibilidade e conformidade semântica
A página de catálogo SHALL manter conformidade com os padrões de acessibilidade WCAG, suporte a navegação por teclado e semântica estruturada.

#### Scenario: Navegação acessível por teclado
- **WHEN** um usuário navega utilizando a tecla Tab
- **THEN** o foco visual percorre sequencialmente os filtros de categoria e os botões de ação dos cards sem armadilhas de teclado.
