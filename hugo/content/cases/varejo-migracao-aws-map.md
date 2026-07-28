+++
title = "Grande grupo de varejo migra 100% para a AWS com governança enterprise e IA preditiva"
date = 2026-03-15
draft = false
sector = "Varejo & Distribuição · VMware → AWS"
metric = "650%"
metricLabel = "ROI do projeto"
desafio = "Infraestrutura legada sem redundância, com 87h/ano de indisponibilidade e crescimento limitado."
solucao = "Migração completa com Landing Zone multi-account, governança de segurança e IA preditiva."
resultado = "Zero downtime, R$ 237 mil em créditos AWS e economia de 30% nos custos operacionais."
description = "Como migramos 100% da infraestrutura de um grande grupo de varejo para a AWS — com Landing Zone segura, governança multi-account e IA preditiva para previsão de demanda."
+++

## O Desafio

Um grande grupo de varejo e distribuição operava sistemas críticos — ERP corporativo e plataforma de gestão comercial responsável por operações fiscais, folha de pagamento e vendas — em servidores físicos VMware **sem redundância geográfica**.

O cenário antes da migração:

- **Disponibilidade de 99,0%** — cerca de 87 horas de indisponibilidade por ano
- **Backup limitado a 7 dias** sem automação
- **Zero redundância geográfica** — um desastre no datacenter significava parada total
- **Provisionamento lento** — dias para subir um novo servidor
- **Custos crescentes** com licenciamento VMware pós-Broadcom

O objetivo não era simplesmente "ir para a nuvem". Era redesenhar a infraestrutura para suportar o crescimento com segurança, resiliência e controle de custos — sem risco de parar a operação.

## A Solução

A CoreScale conduziu a migração completa utilizando a **metodologia de migração da AWS**, organizada em quatro frentes:

### 1. Governança e Segurança como Fundação

Antes da primeira VM ser migrada, implementamos uma Landing Zone completa:

- **AWS Control Tower** com arquitetura multi-account (7 contas)
- **Organizational Units** segmentadas: Produção, Desenvolvimento, Infraestrutura e Segurança
- **Service Control Policies (SCPs)** com guardrails automáticos
- **SSO via IAM Identity Center** — acesso centralizado e rastreável
- **CloudTrail** centralizado para auditoria completa

### 2. Migração e Arquitetura Resiliente

Operação em **duas regiões AWS** (São Paulo para LGPD + Virgínia) com:

- **Transit Gateway** centralizando a conectividade
- **VPN Site-to-Site** com o datacenter on-premises
- **45+ servidores** migrados via AWS Application Migration Service
- **8 bancos de dados** (Oracle e PostgreSQL) migrados com AWS DMS
- **15 TB de dados** movidos sem interrupção

### 3. Segurança Contínua

Postura de segurança enterprise desde o dia zero:

- **Security Hub** consolidando findings
- **GuardDuty** para detecção de ameaças
- **AWS Config** para compliance contínuo
- **Macie** para proteção de dados sensíveis
- **MFA obrigatório** e criptografia com KMS em repouso

### 4. IA em Produção + FinOps

Diferente de uma migração comum, levamos a IA do cliente para produção:

- **Amazon SageMaker** — plataforma de previsão de demanda e gestão de estoque
- **Pipeline de dados** com Glue, Athena e Redshift
- **FinOps** com Savings Plans, Reserved Instances e rightsizing

## Resultados

| Indicador | Antes | Depois |
|-----------|-------|--------|
| Disponibilidade | 99,0% (~87h parada/ano) | **99,7%** |
| Redundância geográfica | Nenhuma | **2 regiões AWS** |
| Retenção de backup | 7 dias manual | **Automatizado e ampliado** |
| Provisionamento | Dias | **95% mais rápido** |
| Custo operacional | Base on-premises | **−30%** |
| Downtime na migração | — | **Zero** |

### Números do projeto

- **R$ 237 mil em créditos AWS** obtidos via programas de migração
- **R$ 2,5 milhões** em benefícios financeiros projetados em 3 anos
- **ROI de 650%** com payback em 2 meses
- **R$ 30,3 mil/mês** em economia adicional mapeada (Savings Plans, Graviton, rightsizing)

## Ficha Técnica

| | |
|---|---|
| **Setor** | Varejo & Distribuição |
| **Programa** | Migração e Modernização AWS |
| **Parceiro** | CoreScale — AWS Advanced Tier |
| **Regiões** | São Paulo (sa-east-1) + Virgínia (us-east-1) |
| **Contas AWS** | 7 (multi-account com Organizations) |
| **Duração** | 9 meses |
| **Servidores migrados** | 45+ |
| **Bancos de dados** | 8 (Oracle + PostgreSQL) |
| **Dados migrados** | 15 TB |
| **Downtime** | Zero |

## Linha do Tempo

1. **Assess** (Jun/2025) — Inventário, Business Case e elegibilidade a créditos
2. **Mobilize** (Jul–Set/2025) — Control Tower, Landing Zone e aprovação de créditos
3. **Migrate** (Set–Nov/2025) — Migração de bancos, compute e storage
4. **ML/IA** (Dez/2025) — Migração da plataforma de machine learning
5. **Validação** (Jan/2026) — Testes de DR, performance e segurança
6. **100% Migrado** (Fev/2026) — Operação completa na AWS, fase de otimização
