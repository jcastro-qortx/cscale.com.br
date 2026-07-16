# CoreScale Site Improvements — Design

## Objetivo

Melhorar conversão, acessibilidade, SEO técnico, desempenho e manutenção do site institucional CoreScale sem alterar sua identidade visual, infraestrutura de publicação AWS ou afirmações comerciais existentes.

## Escopo aprovado

A implementação seguirá a abordagem equilibrada:

- preservar o layout, a paleta, a tipografia e a hierarquia visual atuais;
- preservar afirmações comerciais e métricas, incluindo “0 downtime”, “8–15×”, “até 40%” e “99,9% garantido”;
- acrescentar uma ressalva discreta informando que resultados e benefícios variam conforme ambiente, contrato, elegibilidade e projeto;
- preservar todas as alterações locais existentes no repositório;
- validar localmente, sem publicar automaticamente na AWS.

## Formulário de contato

O formulário continuará enviando dados para o endpoint existente. Os campos terão identificadores, labels associados, atributos de preenchimento automático, validação nativa e mensagens acessíveis. Um campo honeypot real chamado `website` será incluído fora do fluxo visual e enviado com o valor recebido, em vez de ser fixado como vazio.

O envio terá estados acessíveis de progresso, sucesso e erro exibidos na própria página por uma região `aria-live`. O botão será desabilitado durante a requisição. A mensagem de privacidade terá link para `/privacidade/`. Não serão adicionados novos campos comerciais obrigatórios, integrações de CRM ou analytics nesta etapa.

## SEO e compartilhamento social

O template base passará a produzir:

- descrição com fallback para a descrição global;
- URL canônica absoluta;
- Open Graph para site e artigos;
- Twitter Card;
- imagem social existente quando aplicável;
- dados estruturados JSON-LD para `Organization`/`ProfessionalService` e `Article`;
- metadados de publicação para artigos.

Os dados virão do conteúdo e da configuração Hugo sempre que possível. Nenhuma URL de deploy nova será introduzida.

## Acessibilidade

O site receberá um link “Pular para o conteúdo”, foco visível global e um destino principal identificável. O botão do menu móvel usará `aria-controls` e atualizará `aria-expanded`; o menu fechará por Escape e devolverá o foco ao botão. O botão flutuante de WhatsApp e links sociais terão nomes acessíveis explícitos.

Animações serão efetivamente desativadas para usuários com preferência por movimento reduzido. O comportamento atual para mouse será preservado, com estados equivalentes para teclado quando necessário.

## Conteúdo dinâmico

Os três cards de blog escritos manualmente na home serão substituídos por uma consulta Hugo aos três artigos publicados mais recentes. Título, categoria, data, tempo de leitura e URL virão do front matter e do conteúdo.

As métricas comerciais serão preservadas. Uma nota metodológica curta será apresentada próxima ao bloco de resultados ou migração, sem enfraquecer a mensagem principal.

## Hugo e taxonomias

A configuração migrará de `languageCode` para a chave suportada pela versão atual do Hugo. Serão criados templates mínimos para a listagem de categorias e para cada categoria, reutilizando a linguagem visual do blog. O build não deverá emitir os avisos atualmente observados.

## Imagens e arquivos estáticos

Imagens de conteúdo receberão dimensões conhecidas quando práticas, carregamento tardio fora da primeira viewport e decodificação assíncrona. Arquivos grandes só serão removidos quando não houver qualquer referência no projeto e sua finalidade for claramente obsoleta. Não haverá recompressão destrutiva nem substituição visual nesta etapa.

## Organização e manutenção

Não será feita uma refatoração ampla dos estilos inline. Serão adicionadas apenas regras compartilhadas necessárias para foco, acessibilidade, formulário e utilitários. Isso reduz risco de regressão visual e mantém a mudança compatível com a estrutura atual.

## Tratamento de erros

Falhas de validação serão apresentadas antes da requisição. Respostas inválidas ou não JSON do endpoint serão convertidas em uma mensagem segura para o usuário. Erros de rede manterão os dados preenchidos para nova tentativa. O formulário só será limpo após confirmação de sucesso.

## Validação

A implementação será validada por testes estruturais automatizados executados contra os templates e a saída gerada, cobrindo metadados, formulário, acessibilidade, conteúdo dinâmico e ausência de referências quebradas relevantes. O build Hugo será executado com destino temporário e deverá concluir sem avisos do projeto.

Será feita inspeção do diff para garantir que alterações locais preexistentes não foram sobrescritas. Teste visual em navegador e publicação AWS ficam fora do escopo aprovado.

## Fora do escopo

- publicação ou alteração da infraestrutura AWS;
- instalação de analytics, CRM ou gerenciador de consentimento;
- comprovação externa das métricas comerciais;
- redesign ou refatoração integral de CSS;
- alteração da API Lambda além do necessário caso o contrato atual não aceite o honeypot real;
- mudanças nos textos dos artigos que já estão modificados localmente, salvo ajustes indispensáveis à renderização.
