+++
title = "AWS Graviton: até 40% mais barato com mais performance"
date = 2026-05-08
draft = false
category = "FinOps"
description = "Os processadores ARM da AWS entregam melhor relação preço-performance. Saiba quando e como migrar suas cargas."
banner_gradient = "#1A2F4D, #0F3460, #162447"
banner_icon = '<img src="https://d1.awsstatic.com/icons/jp/console_ec2_icon.1b8234c83c8cb1e2b3b5537e1df1a0f0ab3e1912.png" alt="Amazon EC2 Graviton" style="width:72px;height:72px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.3));">'
+++

Se sua infraestrutura AWS roda em instâncias Intel ou AMD, você provavelmente está pagando mais do que precisa. Os processadores Graviton (ARM64) da AWS entregam até **40% mais performance por real gasto** — e a migração é mais simples do que parece.

## Por que Graviton é mais barato

A AWS projeta seus próprios chips ARM. Sem margens de fabricante intermediário e com arquitetura otimizada para cloud, o custo por vCPU é significativamente menor. Uma `m7g.large` (Graviton3) custa ~20% menos que a `m7i.large` (Intel) equivalente — com performance igual ou superior.

## Quando migrar faz sentido

Graviton funciona nativamente com:

- **Containers** (ECS, EKS) — imagens multi-arch são triviais
- **Aplicações Linux** compiladas (Go, Rust, Java 11+, .NET 6+, Python, Node.js)
- **Bancos de dados gerenciados** (RDS, ElastiCache, OpenSearch) — basta trocar a família

## Quando ter cuidado

- Aplicações com dependências binárias x86 sem versão ARM
- Softwares Windows (Graviton é Linux-only)
- Libraries nativas compiladas sem suporte ARM (raro em 2026)

## O caminho prático

1. **Comece pelos bancos**: RDS e ElastiCache suportam Graviton com um clique (modify instance class)
2. **Containers**: adicione `arm64` no build e use instâncias Graviton no node group
3. **EC2 direto**: teste em staging, valide benchmarks, promova para produção

## Números reais

Em migrações que fizemos para clientes:

| Carga | Intel → Graviton | Economia |
|-------|-----------------|----------|
| API (Java 17 / ECS) | m6i.xlarge → m7g.xlarge | 23% |
| PostgreSQL (RDS) | db.r6i.large → db.r7g.large | 19% |
| Redis (ElastiCache) | r6g.large → r7g.large | 15% |
| Kubernetes nodes | m5.2xlarge → m7g.2xlarge | 28% |

> Graviton não é futuro — é o presente. Cada instância que não migrou é dinheiro deixado na mesa.
