+++
title = "Observabilidade na AWS: CloudWatch, Grafana e o que monitorar de verdade"
date = 2026-02-10
draft = false
category = "Operação"
description = "Métricas, logs e traces — como montar uma stack de observabilidade que detecta problemas antes dos usuários."
banner_gradient = "#0F2027, #203A43, #2C5364"
banner_icon = '<img src="https://d1.awsstatic.com/icons/jp/console_cloudwatch_icon.c37766cc2de56dfc99383251c3e9a0293c3e0382.png" alt="Amazon CloudWatch" style="width:72px;height:72px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.3));">'
+++

Monitoramento não é ter dashboards bonitos. É **detectar problemas antes que o cliente perceba** e ter contexto suficiente para resolver em minutos, não horas.

## Os 3 pilares

- **Métricas**: números agregados ao longo do tempo (CPU, latência, error rate)
- **Logs**: eventos discretos com contexto (stack traces, requests, audit trail)
- **Traces**: o caminho de uma request através de múltiplos serviços (distributed tracing)

Sem os três, você sempre vai ter pontos cegos.

## Stack que recomendamos

| Pilar | Ferramenta | Por quê |
|-------|-----------|---------|
| Métricas | CloudWatch Metrics + Grafana | CloudWatch coleta nativamente, Grafana visualiza melhor |
| Logs | CloudWatch Logs + Insights | Busca poderosa sem infra adicional |
| Traces | X-Ray ou OpenTelemetry | Trace distribuído entre Lambda, ECS, API Gateway |
| Alertas | CloudWatch Alarms + SNS → PagerDuty/Slack | Escalonamento automático |

## O que monitorar (de verdade)

Esqueça métricas de vaidade. Foque no que impacta o negócio:

### Sinais de ouro (Golden Signals)

1. **Latência** — P50, P95, P99 das APIs e páginas críticas
2. **Error rate** — % de respostas 5xx e 4xx anômalas
3. **Tráfego** — requests/s por endpoint (detecta anomalias e ataques)
4. **Saturação** — CPU, memória, IOPS, conexões do banco

### Alarmes que acordam alguém de madrugada

- Error rate > 5% por 3 minutos consecutivos
- Latência P99 > 2x do baseline por 5 minutos
- Disco de banco acima de 85%
- Fila de processamento crescendo sem drenar

## Grafana como camada de visualização

O CloudWatch é excelente para coleta e alarmes, mas a UX de dashboards é limitada. Usar o Amazon Managed Grafana como camada de visualização dá:

- Dashboards mais legíveis e compartilháveis
- Correlação entre métricas, logs e traces na mesma tela
- Alertas visuais com contexto do incidente

## O anti-padrão mais comum

Ter 200 alarmes configurados que ninguém olha. Resultado: alarm fatigue — quando tudo é urgente, nada é urgente.

> Menos alarmes, mais precisos. Cada alarme deve ter um runbook associado: "se disparou, faça X". Sem runbook, o alarme não deveria existir.
