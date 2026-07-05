+++
title = "Disaster Recovery na AWS: 4 estratégias e como escolher a certa"
date = 2026-03-22
draft = false
category = "Segurança"
description = "De Backup & Restore a Multi-Site Active-Active — entenda o tradeoff entre RTO, RPO e custo para proteger seu negócio."
banner_gradient = "#1B2838, #2A1A3D, #0F1620"
banner_icon = '<img src="https://d1.awsstatic.com/icons/jp/console_backup_icon.9f1aa78e61083e8a498e8e24b07a9e919e0cdb29.png" alt="AWS Backup" style="width:72px;height:72px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.3));">'
+++

Se o seu ambiente parar, quanto tempo o negócio aguenta? Essa pergunta define qual estratégia de Disaster Recovery (DR) faz sentido — e quanto investir.

## Os dois números que importam

- **RTO** (Recovery Time Objective): tempo máximo aceitável para restaurar o serviço
- **RPO** (Recovery Point Objective): quantidade máxima aceitável de dados perdidos

Quanto menor o RTO/RPO, maior o custo de infraestrutura. O segredo é encontrar o equilíbrio certo para cada carga de trabalho.

## As 4 estratégias (do mais barato ao mais rápido)

### 1. Backup & Restore

Backups automatizados em S3 + snapshots de EBS/RDS. Recuperação em horas. Ideal para ambientes não-críticos.

- **RTO**: 4–24 horas
- **RPO**: 1–24 horas
- **Custo**: Baixo (só armazenamento)

### 2. Pilot Light

Componentes core (banco de dados, AD) replicados e prontos. Compute é provisionado sob demanda no momento do desastre.

- **RTO**: 1–4 horas
- **RPO**: Minutos (replicação contínua)
- **Custo**: Moderado

### 3. Warm Standby

Ambiente completo rodando em escala reduzida. No evento de DR, escala-se para produção completa.

- **RTO**: 15–60 minutos
- **RPO**: Segundos
- **Custo**: Alto

### 4. Multi-Site Active-Active

Duas regiões servindo tráfego simultaneamente. Failover instantâneo via Route 53.

- **RTO**: Segundos
- **RPO**: Zero (replicação síncrona)
- **Custo**: Muito alto

## Na prática

A maioria dos nossos clientes opera com **Pilot Light para sistemas críticos** e **Backup & Restore para o restante**. É o melhor equilíbrio entre proteção e custo.

> O DR que nunca foi testado é o DR que não funciona. Simulamos failover trimestralmente com cada cliente — sem surpresas no dia que importa.
