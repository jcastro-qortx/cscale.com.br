# CoreScale Site — Infraestrutura AWS

Site institucional da CoreScale servido em `https://site.corescale.com.br`.

## Arquitetura

![Arquitetura AWS](generated-diagrams/corescale-architecture.png)

### Componentes

| Componente | Recurso AWS | Função |
|-----------|-------------|--------|
| CDN | CloudFront Distribution | Entrega do site com HTTPS, cache e security headers |
| URL Rewrite | CloudFront Function | Resolve `/path/` → `/path/index.html` para OAC |
| Storage | S3 `cscale-website` | Armazena HTML, imagens e assets (acesso via OAC apenas) |
| API | API Gateway v2 HTTP | Endpoint `POST /contact` com CORS restrito e rate limiting |
| Compute | Lambda `cscale-contact-form` | Processa formulário: honeypot, validação, envio de email |
| Email | SES | Envia emails de contato para `jcastro@cscale.com.br` |
| Certificado | ACM | SSL/TLS para o domínio custom |

### Fluxo — Conteúdo Estático

```
Usuário → CloudFront (HTTPS) → CF Function (URL rewrite) → S3 (via OAC assinado)
```

### Fluxo — Formulário de Contato

```
Usuário → API Gateway (CORS + throttle 10 req/s) → Lambda (honeypot + validação) → SES → email
```

## Security Hardening

Implementado em Julho/2026:

| Controle | Status | Detalhes |
|----------|--------|----------|
| HTTPS forçado | ✅ | CloudFront `redirect-to-https` |
| HSTS | ✅ | `max-age=31536000; includeSubDomains` |
| X-Frame-Options | ✅ | `DENY` (anti-clickjacking) |
| Referrer-Policy | ✅ | `strict-origin-when-cross-origin` |
| Permissions-Policy | ✅ | `camera=(), microphone=(), geolocation=()` |
| CORS restrito | ✅ | Apenas `https://site.corescale.com.br` |
| Rate Limiting | ✅ | 10 req/s, burst 20 (API Gateway) |
| Anti-Bot | ✅ | Honeypot field + validação server-side |
| S3 privado | ✅ | OAC — bucket inacessível sem CloudFront |
| SES verificado | ✅ | Sender e recipient verificados |
| X-Content-Type-Options | ⚠️ | Desabilitado (incompatível com bundler legacy) |
| Content-Security-Policy | ⚠️ | Desabilitado (incompatível com bundler legacy) |

> **Nota:** CSP e `nosniff` serão re-ativados quando o site migrar completamente para o build Hugo (HTML estático sem blob URLs).

## Estrutura de Diretórios

```
corescale/
├── terraform/
│   ├── main.tf              # Infraestrutura AWS (S3, CloudFront, Lambda, API GW, SES)
│   ├── variables.tf         # Variáveis (região, bucket, domínio, emails)
│   ├── outputs.tf           # Outputs (URLs, DNS records)
│   └── lambda/
│       └── contact.py       # Handler do formulário de contato
├── hugo/                    # Site institucional (Hugo SSG)
│   ├── hugo.toml            # Configuração Hugo
│   ├── content/             # Conteúdo Markdown (blog, cases, páginas)
│   ├── layouts/             # Templates HTML
│   ├── static/              # Assets estáticos (imagens, favicon)
│   └── public/              # Output gerado (hugo --minify)
├── contact.html             # Formulário standalone (legacy)
├── deploy.sh                # Script de deploy (terraform + upload S3)
├── index.html               # Home bundled (legacy — será substituída pelo Hugo)
└── generated-diagrams/      # Diagramas de arquitetura
```

## Deploy

### Pré-requisitos

- AWS CLI configurado com credenciais
- Terraform >= 1.5.0
- Hugo extended >= 0.120 (para o site Hugo)

### Deploy completo (infraestrutura + site)

```bash
cd corescale
./deploy.sh
```

### Deploy apenas do site Hugo

```bash
cd corescale/hugo
hugo --minify
aws s3 sync public/ s3://cscale-website/ --delete --cache-control "max-age=300"
aws cloudfront create-invalidation --distribution-id E100PKYXLCMDIC --paths "/*"
```

### Deploy apenas da infraestrutura

```bash
cd corescale/terraform
terraform init
terraform apply
```

## Configuração

### Variáveis Terraform (`variables.tf`)

| Variável | Default | Descrição |
|----------|---------|-----------|
| `aws_region` | `us-east-1` | Região AWS |
| `bucket_name` | `cscale-website` | Nome do bucket S3 |
| `domain_name` | `site.corescale.com.br` | Domínio custom |
| `contact_email` | `jcastro@cscale.com.br` | Destinatário dos emails |
| `sender_email` | `site@cscale.com.br` | Remetente SES |

### SES (Email)

O SES está em **sandbox mode**. Ambos os emails precisam estar verificados:
- `site@cscale.com.br` — remetente (sender)
- `jcastro@cscale.com.br` — destinatário (recipient)

Para sair do sandbox e enviar para qualquer destinatário, solicite produção via AWS Console → SES → Account Dashboard → Request Production Access.

### DNS

| Registro | Tipo | Valor |
|----------|------|-------|
| `site.corescale.com.br` | CNAME | `d32opakjll1yhp.cloudfront.net` |
| ACM validation | CNAME | Conforme output `acm_validation_records` |

## Lambda — Lógica do Formulário

O handler (`terraform/lambda/contact.py`) implementa:

1. **CORS condicional** — header `Access-Control-Allow-Origin` apenas quando `Origin == https://site.corescale.com.br`
2. **Honeypot** — campo `website` verificado raw (sem trim); se não-vazio = bot → retorna 200 silenciosamente
3. **Validação** — `name` (2-200 chars), `email` (@ + dot no domínio), `message` (10-5000 chars)
4. **Envio** — SES `send_email` apenas quando honeypot vazio + validação OK

### Respostas

| Cenário | Status | Body |
|---------|--------|------|
| Bot detectado | 200 | `{"message": "Mensagem enviada com sucesso!"}` |
| Validação falhou | 400 | `{"error": "Campo 'X' ..."}` |
| Sucesso | 200 | `{"message": "Mensagem enviada com sucesso!"}` |
| Erro SES | 500 | `{"error": "Erro ao enviar mensagem..."}` |

## Hugo — Site Institucional

O site Hugo substitui o bundler single-file legacy. Gera HTML estático normal, compatível com todas as security headers.

```bash
cd hugo
hugo server -D          # Dev server (http://localhost:1313)
hugo --minify           # Build produção → public/
hugo new content blog/meu-artigo.md   # Novo blog post
hugo new content cases/meu-case.md    # Novo case
```

Para detalhes sobre o Hugo, veja [`hugo/README.md`](hugo/README.md).

## Histórico de Mudanças

### Julho 2026 — Security Hardening

- Migração S3 website hosting → OAC (bucket privado)
- CloudFront Response Headers Policy (HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy)
- CloudFront Function para URL rewrite (`/path/` → `/path/index.html`)
- API Gateway: CORS restrito a `site.corescale.com.br`, rate limit 10 req/s
- Lambda: CORS condicional, honeypot anti-bot, validação enhanced
- Formulário de contato: honeypot field, envio via API (substituiu mailto)
- SES: verificação do sender + recipient
- Favicon e assets estáticos incluídos no deploy
