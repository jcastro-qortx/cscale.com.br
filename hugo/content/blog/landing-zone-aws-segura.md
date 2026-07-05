+++
title = "Landing Zone AWS: como montar uma base segura antes de migrar"
date = 2026-04-15
draft = false
category = "Segurança"
description = "Multi-account, guardrails e automação — os pilares de uma Landing Zone que escala sem virar caos."
banner_gradient = "#0D2137, #1A3A5C, #0F1B2E"
banner_icon = '<img src="https://d1.awsstatic.com/icons/jp/console_control-tower_icon.d3a30e77e4a2e8a2d3f673e0c498e0ca7ac52681.png" alt="AWS Control Tower" style="width:72px;height:72px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.3));">'
+++

Migrar para a AWS sem uma Landing Zone bem definida é como construir um prédio sem fundação. Funciona no início, mas cedo ou tarde desmorona — em segurança, custos ou governança.

## O que é uma Landing Zone

É a estrutura base da sua conta AWS: organização multi-account, redes segmentadas, políticas de acesso e automação de provisionamento. O objetivo é que toda carga nova já nasça dentro de um padrão seguro.

## Multi-account é obrigatório

Uma conta única para tudo — desenvolvimento, homologação e produção — é o cenário que mais gera incidentes. Com o AWS Organizations e SCPs (Service Control Policies), cada ambiente fica isolado com limites claros.

## Guardrails, não porteiros

Em vez de criar processos manuais de aprovação, implantamos controles preventivos e detectivos:

- **SCPs** que impedem ações destrutivas em produção
- **AWS Config Rules** que detectam desvios em tempo real
- **CloudTrail** centralizado para auditoria completa

## Rede segmentada desde o dia 1

VPCs com CIDR planejado, subnets privadas como padrão, Transit Gateway para conectividade entre contas e peering com on-premises via Direct Connect ou Site-to-Site VPN.

## Automação é o que sustenta

Landing Zone manual vira legado em 6 meses. Usamos Infrastructure as Code (Terraform/CloudFormation) para que cada nova conta ou recurso siga o padrão automaticamente — sem depender de memória humana.

> Uma Landing Zone bem feita não atrasa a migração — ela acelera, porque remove decisões repetitivas e erros humanos do caminho.
