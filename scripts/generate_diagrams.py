#!/usr/bin/env python3
"""
Generator of official AWS Reference Architecture Diagrams for CoreScale Catalog Offers.
Generates:
1. Clean, highly legible, standalone vector SVGs for web embedding and modal preview.
2. Official editable .drawio files with AWS4 stencils and shapes.
3. Multi-page consolidated .drawio file for client delivery.
"""

import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape
import datetime

OUT_DIR = Path('/home/jcastro/hermes-data/projects/cscale.com.br/cscale.com.br/hugo/static/diagrams')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Colors according to official AWS Guidelines and CoreScale Brand
AWS_NAVY = "#232F3E"
AWS_ORANGE = "#ED7100"
AWS_PURPLE = "#8C4FFF"
AWS_MAGENTA = "#C925D1"
AWS_RED = "#DD344C"
AWS_PINK = "#E7157B"
AWS_GREEN = "#7AA116"
AWS_BLUE = "#147EBA"
AWS_TEAL = "#01A88D"
TEXT_DARK = "#1E293B"
TEXT_MUTED = "#64748B"
BORDER_LIGHT = "#CBD5E1"
BG_LIGHT = "#F8FAFC"
CONTAINER_BG = "#FFFFFF"

# Helper for drawing SVG
def create_svg_diagram(title, subtitle, code, width, height, elements_fn):
    """Generates a professional AWS reference architecture in standalone SVG format."""
    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#0F172A;font-family:'Inter',system-ui,-apple-system,sans-serif;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.95"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38BDF8"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#F97316"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#22C55E"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="{width}" height="{height}" fill="#0B0F19"/>

  <!-- Subtle Blueprint Grid -->
  <g opacity="0.06">
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#94A3B8" stroke-width="1"/>' for x in range(0, width, 40))}
    {''.join(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#94A3B8" stroke-width="1"/>' for y in range(0, height, 40))}
  </g>

  <!-- Header Banner -->
  <rect x="30" y="24" width="{width - 60}" height="76" rx="12" fill="url(#headerGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
  
  <!-- CoreScale Badge -->
  <rect x="50" y="42" width="130" height="38" rx="8" fill="#F97316" fill-opacity="0.15" stroke="#F97316" stroke-width="1"/>
  <text x="115" y="66" fill="#F97316" font-size="14" font-weight="800" text-anchor="middle" letter-spacing="1.5">CORESCALE</text>
  
  <text x="200" y="56" fill="#F8FAFC" font-size="20" font-weight="700">{title}</text>
  <text x="200" y="80" fill="#94A3B8" font-size="13" font-weight="500">{subtitle}</text>

  <!-- Tag Code Badge -->
  <rect x="{width - 210}" y="44" width="160" height="34" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1"/>
  <circle cx="{width - 190}" cy="61" r="5" fill="#22C55E"/>
  <text x="{width - 110}" y="67" fill="#E2E8F0" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1">REF: {code}</text>

  <!-- Inner Architectural Elements -->
''')
    elements_fn(svg)

    # Footer note
    svg.append(f'''
  <!-- Footer Legal / Watermark -->
  <line x1="30" y1="{height - 35}" x2="{width - 30}" y2="{height - 35}" stroke="#1E293B" stroke-width="1"/>
  <text x="40" y="{height - 16}" fill="#64748B" font-size="11">Arquitetura de Referência Oficial CoreScale • Padrão AWS Well-Architected & Prescriptive Guidance</text>
  <text x="{width - 40}" y="{height - 16}" fill="#64748B" font-size="11" text-anchor="end">Suporte & Implementação: contato@corescale.com.br</text>
</svg>''')
    return '\n'.join(svg)


def draw_container(svg, x, y, w, h, title, subtitle="", stroke="#334155", badge_color="#38BDF8", dashed=False):
    """Draws a boundary/container box (e.g. AWS Cloud, VPC, Subnet, OU)"""
    dash_attr = 'stroke-dasharray="6 6"' if dashed else ''
    svg.append(f'''
  <!-- Boundary: {title} -->
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#0F172A" fill-opacity="0.8" stroke="{stroke}" stroke-width="1.5" {dash_attr}/>
    <rect x="{x}" y="{y}" width="{w}" height="38" rx="14" fill="{stroke}" fill-opacity="0.15"/>
    <rect x="{x+16}" y="{y+10}" width="8" height="18" rx="3" fill="{badge_color}"/>
    <text x="{x+32}" y="{y+23}" fill="#F1F5F9" font-size="13" font-weight="700">{title}</text>
    {f'<text x="{x+w-16}" y="{y+23}" fill="#94A3B8" font-size="11" text-anchor="end">{subtitle}</text>' if subtitle else ''}
  </g>''')

def draw_node(svg, x, y, w, h, label, sublabel, icon_type, color_accent="#F97316"):
    """Draws a service node with AWS iconography"""
    svg.append(f'''
  <!-- Node: {label} -->
  <g transform="translate({x}, {y})">
    <rect width="{w}" height="{h}" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="6" height="{h}" rx="3" fill="{color_accent}"/>
    
    <!-- Icon Container -->
    <rect x="14" y="{(h-42)//2}" width="42" height="42" rx="8" fill="{color_accent}" fill-opacity="0.15" stroke="{color_accent}" stroke-width="1.5"/>
    <text x="35" y="{(h-42)//2 + 26}" fill="{color_accent}" font-size="16" font-weight="800" text-anchor="middle">{icon_type[:3].upper()}</text>
    
    <!-- Text Labels -->
    <text x="68" y="{(h-16)//2 + 2}" fill="#F8FAFC" font-size="13" font-weight="700">{label}</text>
    <text x="68" y="{(h-16)//2 + 20}" fill="#94A3B8" font-size="11">{sublabel}</text>
  </g>''')

def draw_arrow(svg, x1, y1, x2, y2, label="", color="#38BDF8", marker="arrow"):
    """Draws a directional connector between components"""
    svg.append(f'''
  <path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#{marker})" stroke-linecap="round"/>''')
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        svg.append(f'''
  <rect x="{mx - 60}" y="{my - 11}" width="120" height="20" rx="4" fill="#0B0F19" stroke="#334155" stroke-width="1"/>
  <text x="{mx}" y="{my + 3}" fill="#E2E8F0" font-size="10" font-weight="600" text-anchor="middle">{label}</text>''')


# -------------------------------------------------------------
# 1. SEC-ASSESS: Security Assessment & CIS Benchmark
# -------------------------------------------------------------
def build_sec_assess():
    def elements(s):
        # Boundaries
        draw_container(s, 40, 125, 340, 480, "Fontes de Telemetria & Contas AWS", "Produção / Multi-Account", stroke="#334155", badge_color="#F97316")
        draw_container(s, 420, 125, 480, 480, "Núcleo de Auditoria & Detecção AWS", "Audit & Security OU", stroke="#DD344C", badge_color="#DD344C")
        draw_container(s, 940, 125, 320, 480, "Plano de Remediação CoreScale", "Entrega Executiva", stroke="#22C55E", badge_color="#22C55E")

        # Telemetria Nodes
        draw_node(s, 65, 185, 290, 68, "AWS CloudTrail", "Trilha global de auditoria de APIs", "TRAIL", AWS_PINK)
        draw_node(s, 65, 275, 290, 68, "VPC Flow Logs", "Registro de tráfego de rede IP", "VPC", AWS_PURPLE)
        draw_node(s, 65, 365, 290, 68, "AWS Config", "Histórico de conformidade de recursos", "CFG", AWS_PINK)
        draw_node(s, 65, 455, 290, 68, "IAM Access Analyzer", "Identificação de acesso público/externo", "IAM", AWS_RED)

        # Security OU Nodes
        draw_node(s, 445, 185, 430, 80, "AWS Security Hub", "CIS AWS Foundations v3.0 & FSBP Scores", "SHUB", AWS_RED)
        draw_node(s, 445, 295, 430, 80, "Amazon GuardDuty", "Detecção de ameaças com ML (DNS, S3, IAM, EKS)", "GDUTY", AWS_RED)
        draw_node(s, 445, 405, 430, 80, "Amazon Inspector", "Varredura contínua de CVEs em EC2 e ECR", "INSP", AWS_RED)

        # Output / Deliverable Nodes
        draw_node(s, 965, 185, 270, 75, "Quick Wins Imediatos", "Fechamento de portas 22/3389 e S3 exposto", "WIN", AWS_GREEN)
        draw_node(s, 965, 295, 270, 75, "Relatório CIS Benchmark", "Score de conformidade & LGPD auditada", "REP", AWS_BLUE)
        draw_node(s, 965, 405, 270, 75, "Sustentação SEC-MNG", "Proposta contínua de segurança gerenciada", "MNG", AWS_PURPLE)

        # Connectors
        draw_arrow(s, 355, 219, 445, 219, "Eventos")
        draw_arrow(s, 355, 309, 445, 325, "Fluxos de Rede")
        draw_arrow(s, 355, 399, 445, 235, "Config Drift")
        draw_arrow(s, 355, 489, 445, 245, "Alertas IAM")

        draw_arrow(s, 875, 225, 965, 225, "Prioridade Alta", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 875, 335, 965, 335, "Matriz Severidade", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 875, 445, 965, 445, "Backlog Técnico", color="#22C55E", marker="arrow-green")

    return create_svg_diagram(
        "Assessment & Auditoria de Postura AWS",
        "Detecção de brechas, verificação CIS Benchmark v3.0 e plano de remediação imediata",
        "SEC-ASSESS", 1300, 650, elements
    )


# -------------------------------------------------------------
# 2. WAR-EXPRESS: Well-Architected Review Express
# -------------------------------------------------------------
def build_war_express():
    def elements(s):
        draw_container(s, 40, 125, 340, 480, "Workload AWS Avaliado", "Produção do Cliente", stroke="#334155", badge_color="#F97316")
        draw_container(s, 420, 125, 480, 480, "AWS Well-Architected Tool", "Revisão dos 6 Pilares", stroke="#E7157B", badge_color="#E7157B")
        draw_container(s, 940, 125, 320, 480, "Sprint Remediação & Financiamento", "Geração de Valor", stroke="#22C55E", badge_color="#22C55E")

        # Workload Nodes
        draw_node(s, 65, 185, 290, 68, "Compute & Aplicações", "Amazon EC2, EKS, ECS, Lambda", "EC2", AWS_ORANGE)
        draw_node(s, 65, 275, 290, 68, "Bancos de Dados & Storage", "RDS Aurora, DynamoDB, Amazon S3", "RDS", AWS_MAGENTA)
        draw_node(s, 65, 365, 290, 68, "Rede & Segurança", "VPC Multi-AZ, AWS WAF, Route 53", "NET", AWS_PURPLE)
        draw_node(s, 65, 455, 290, 68, "Observabilidade & Logs", "Amazon CloudWatch, AWS X-Ray", "CW", AWS_BLUE)

        # WAR Tool Nodes
        draw_node(s, 445, 185, 430, 78, "Avaliação dos 6 Pilares", "Segurança, Confiabilidade, Performance, Custo, Ops, Sustentabilidade", "WAR", AWS_PINK)
        draw_node(s, 445, 295, 430, 78, "Mapeamento HRIs e MRIs", "High Risk Issues e Medium Risk Issues catalogados", "HRI", AWS_RED)
        draw_node(s, 445, 405, 430, 78, "Backlog Oficial de Ação", "Plano prescritivo gerado pela ferramenta oficial", "DOC", AWS_BLUE)

        # Remediation & Credits Nodes
        draw_node(s, 965, 185, 270, 75, "Sprint CoreScale (>=25%)", "Correção técnica comprovada dos HRIs críticos", "FIX", AWS_GREEN)
        draw_node(s, 965, 295, 270, 75, "Submissão Oficial AWS", "Validação no portal de parceiros com evidências", "AWS", AWS_ORANGE)
        draw_node(s, 965, 405, 270, 75, "Até US$ 5.000 em Créditos", "Crédito na fatura AWS para cobrir custos", "USD", AWS_GREEN)

        # Connectors
        draw_arrow(s, 355, 219, 445, 219, "Diagnóstico")
        draw_arrow(s, 355, 309, 445, 235, "Telemetria")
        draw_arrow(s, 355, 399, 445, 250, "Topologia")

        draw_arrow(s, 660, 263, 660, 295, "Identifica")
        draw_arrow(s, 660, 373, 660, 405, "Prescreve")

        draw_arrow(s, 875, 335, 965, 225, "Execução", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 1100, 260, 1100, 295, "Comprova", color="#F97316", marker="arrow-orange")
        draw_arrow(s, 1100, 370, 1100, 405, "Destrava", color="#22C55E", marker="arrow-green")

    return create_svg_diagram(
        "AWS Well-Architected Review (WAR) Express",
        "Auditoria dos 6 pilares, eliminação de HRIs e destravamento de até US$ 5.000 em créditos AWS",
        "WAR-EXPRESS", 1300, 650, elements
    )


# -------------------------------------------------------------
# 3. AI-RAG: Enterprise RAG no Bedrock
# -------------------------------------------------------------
def build_ai_rag():
    def elements(s):
        draw_container(s, 40, 125, 280, 480, "Fontes de Dados Corporativos", "S3 / Repositórios", stroke="#334155", badge_color="#7AA116")
        draw_container(s, 360, 125, 540, 480, "Amazon Bedrock & Vector Store", "Hospedado na Conta do Cliente", stroke="#01A88D", badge_color="#01A88D")
        draw_container(s, 940, 125, 320, 480, "Canais de Consumo & Usuários", "Interface Segura", stroke="#8C4FFF", badge_color="#8C4FFF")

        # Ingestion
        draw_node(s, 65, 185, 230, 75, "Amazon S3", "PDFs, DOCX, Manuais, Políticas", "S3", AWS_GREEN)
        draw_node(s, 65, 295, 230, 75, "SharePoint / Drive", "Sincronização via Connectors", "DRV", AWS_BLUE)
        draw_node(s, 65, 405, 230, 75, "Bancos / ERP Docs", "Extração contínua de relatórios", "DB", AWS_PURPLE)

        # Bedrock Core
        draw_node(s, 385, 185, 490, 78, "Knowledge Bases for Bedrock", "Chunking semântico & Titan Text Embeddings v2", "KB", AWS_TEAL)
        draw_node(s, 385, 280, 490, 78, "OpenSearch Serverless", "Vector Engine isolado com criptografia KMS", "VEC", AWS_PURPLE)
        draw_node(s, 385, 375, 490, 78, "Anthropic Claude 3.5 Sonnet", "Inferência privada no Amazon Bedrock (sem treino externo)", "LLM", AWS_ORANGE)
        draw_node(s, 385, 470, 490, 78, "Bedrock Guardrails", "Filtro PII / LGPD, anti-jailbreak e citações estritas", "SEC", AWS_RED)

        # Interface
        draw_node(s, 965, 185, 270, 75, "Chat Corporativo Web", "Interface limpa com link da fonte citada", "WEB", AWS_BLUE)
        draw_node(s, 965, 295, 270, 75, "Microsoft Teams / Slack", "Bot interno para colaboradores", "BOT", AWS_PURPLE)
        draw_node(s, 965, 405, 270, 75, "API Gateway / Lambda", "Integração com sistemas internos e ERP", "API", AWS_ORANGE)

        # Connectors
        draw_arrow(s, 295, 222, 385, 222, "Data Sync")
        draw_arrow(s, 295, 332, 385, 235, "Conector")
        
        draw_arrow(s, 630, 263, 630, 280, "Vetores")
        draw_arrow(s, 630, 358, 630, 375, "Busca Híbrida")
        draw_arrow(s, 630, 453, 630, 470, "Proteção")

        draw_arrow(s, 875, 400, 965, 225, "Resposta + Fonte", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 875, 415, 965, 332, "Notificação", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 875, 430, 965, 442, "REST JSON", color="#22C55E", marker="arrow-green")

    return create_svg_diagram(
        "Assistente de Conhecimento Corporativo (Enterprise RAG)",
        "Amazon Bedrock Knowledge Bases + OpenSearch Serverless + Claude 3.5 Sonnet com citações exatas",
        "AI-RAG", 1300, 650, elements
    )


# -------------------------------------------------------------
# 4. AI-EXTRACT: Extração Inteligente de Documentos
# -------------------------------------------------------------
def build_ai_extract():
    def elements(s):
        draw_container(s, 40, 125, 270, 480, "Ingestão de Documentos", "S3 Inbound Bucket", stroke="#334155", badge_color="#7AA116")
        draw_container(s, 350, 125, 540, 480, "Pipeline Serverless AWS", "OCR + IA Generativa", stroke="#01A88D", badge_color="#01A88D")
        draw_container(s, 930, 125, 330, 480, "Destino ERP & Exceções", "Automação Contábil", stroke="#22C55E", badge_color="#22C55E")

        # Ingestion
        draw_node(s, 65, 205, 220, 75, "Upload de Arquivos", "Notas Fiscais, Faturas, Boletos", "DOC", AWS_GREEN)
        draw_node(s, 65, 345, 220, 75, "Amazon S3 Inbound", "Eventos de criação de objeto", "S3", AWS_GREEN)

        # Processing Core
        draw_node(s, 375, 175, 490, 75, "AWS Lambda Orchestrator", "Gatilho automático e orquestração assíncrona", "LBD", AWS_ORANGE)
        draw_node(s, 375, 275, 490, 75, "Amazon Textract", "OCR estruturado (AnalyzeDocument / Tables)", "TXT", AWS_TEAL)
        draw_node(s, 375, 375, 490, 75, "Amazon Bedrock (Haiku)", "Normalização semântica em JSON validado", "LLM", AWS_TEAL)
        draw_node(s, 375, 475, 490, 75, "Validador de Regras", "Checagem de CNPJ, totais e impostos", "VAL", AWS_BLUE)

        # Output
        draw_node(s, 955, 195, 280, 80, "Integração ERP (API)", "SAP, Totvs, Senior, Omie via Webhook", "ERP", AWS_GREEN)
        draw_node(s, 955, 315, 280, 80, "Amazon DynamoDB", "Histórico de auditoria e payload completo", "DDB", AWS_PURPLE)
        draw_node(s, 955, 435, 280, 80, "Fila SQS de Exceções", "Transbordo para conferência humana", "SQS", AWS_RED)

        # Connectors
        draw_arrow(s, 175, 280, 175, 345, "Upload")
        draw_arrow(s, 285, 382, 375, 212, "S3 Event")
        
        draw_arrow(s, 620, 250, 620, 275, "Executa OCR")
        draw_arrow(s, 620, 350, 620, 375, "Raw Text")
        draw_arrow(s, 620, 450, 620, 475, "JSON Estruturado")

        draw_arrow(s, 865, 512, 955, 235, "Válido (>=95%)", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 865, 512, 955, 355, "Gravação", color="#38BDF8", marker="arrow")
        draw_arrow(s, 865, 512, 955, 475, "Erro / Divergência", color="#EF4444", marker="arrow")

    return create_svg_diagram(
        "Extração Inteligente de Documentos para ERP",
        "Pipeline serverless com Amazon Textract e Bedrock para automação contábil com validação estrita",
        "AI-EXTRACT", 1300, 650, elements
    )


# -------------------------------------------------------------
# 5. AI-AGENT: Agente Autônomo de Atendimento
# -------------------------------------------------------------
def build_ai_agent():
    def elements(s):
        draw_container(s, 40, 125, 270, 480, "Canais Omnichannel", "Entrada de Clientes", stroke="#334155", badge_color="#8C4FFF")
        draw_container(s, 350, 125, 540, 480, "Amazon Bedrock AgentCore", "Raciocínio & Ferramentas", stroke="#01A88D", badge_color="#01A88D")
        draw_container(s, 930, 125, 330, 480, "Sistemas & Transbordo", "Ações Conectadas", stroke="#22C55E", badge_color="#22C55E")

        # Ingestion
        draw_node(s, 65, 195, 220, 75, "WhatsApp Business", "API oficial de mensagens", "WPP", AWS_GREEN)
        draw_node(s, 65, 315, 220, 75, "Webchat Corporativo", "Widget responsivo no site", "WEB", AWS_BLUE)
        draw_node(s, 65, 435, 220, 75, "API Gateway", "Webhook seguro com rate-limit", "API", AWS_ORANGE)

        # Processing Core
        draw_node(s, 375, 175, 490, 75, "Bedrock Agent Router", "Orquestração ReAct e intenções", "AGT", AWS_TEAL)
        draw_node(s, 375, 275, 490, 75, "Knowledge Base Integrada", "Perguntas frequentes e catálogo de produtos", "KB", AWS_TEAL)
        draw_node(s, 375, 375, 490, 75, "Action Groups (Lambda)", "Chamadas para APIs de negócio", "ACT", AWS_ORANGE)
        draw_node(s, 375, 475, 490, 75, "Amazon DynamoDB", "Memória de contexto e histórico de sessão", "DDB", AWS_PURPLE)

        # Output
        draw_node(s, 955, 195, 280, 80, "APIs de Negócio", "ERP, CRM, Status de Pedido, 2ª Via", "API", AWS_GREEN)
        draw_node(s, 955, 315, 280, 80, "Transbordo Humano", "Fila de atendimento (Zendesk / GLPI)", "SUP", AWS_ORANGE)
        draw_node(s, 955, 435, 280, 80, "Auditoria CloudWatch", "Métricas de FRT, tokens e conversões", "LOG", AWS_BLUE)

        # Connectors
        draw_arrow(s, 285, 232, 375, 212, "Mensagem")
        draw_arrow(s, 285, 352, 375, 225, "Chat")
        draw_arrow(s, 285, 472, 375, 235, "Webhook")
        
        draw_arrow(s, 620, 250, 620, 275, "Consulta RAG")
        draw_arrow(s, 620, 350, 620, 375, "Executa Ação")
        draw_arrow(s, 620, 450, 620, 475, "Salva Contexto")

        draw_arrow(s, 865, 412, 955, 235, "Executa API", color="#22C55E", marker="arrow-green")
        draw_arrow(s, 865, 212, 955, 355, "Handover", color="#F97316", marker="arrow-orange")
        draw_arrow(s, 865, 512, 955, 475, "Logs & Métricas", color="#38BDF8", marker="arrow")

    return create_svg_diagram(
        "Agente Autônomo de Atendimento e Triagem",
        "Orquestração conversacional com Bedrock Agents, integração com APIs internas e transbordo humano",
        "AI-AGENT", 1300, 650, elements
    )


# -------------------------------------------------------------
# Generate Editable .drawio XML (using official mxgraph.aws4 stencils)
# -------------------------------------------------------------
def generate_drawio_xml():
    """Generates a multi-page .drawio file with official AWS stencils."""
    diagrams = []
    
    pages = [
        ("sec-assess", "SEC-ASSESS — Security Assessment", [
            ("shub", "AWS Security Hub", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;fillColor=#DD344C;fontColor=#232F3E;align=center;", 500, 200, 78, 78),
            ("gd", "Amazon GuardDuty", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;fillColor=#DD344C;fontColor=#232F3E;align=center;", 500, 350, 78, 78),
            ("trail", "AWS CloudTrail", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudtrail;fillColor=#E7157B;fontColor=#232F3E;align=center;", 200, 200, 78, 78),
            ("cfg", "AWS Config", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;fillColor=#E7157B;fontColor=#232F3E;align=center;", 200, 350, 78, 78),
            ("rep", "Relatório CIS Benchmark & Remediação", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=14;", 800, 275, 220, 60),
        ]),
        ("war-express", "WAR-EXPRESS — Well-Architected", [
            ("tool", "Well-Architected Tool", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.well_architect_tool;fillColor=#E7157B;fontColor=#232F3E;align=center;", 500, 250, 78, 78),
            ("ec2", "Compute (EC2 / EKS)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#ED7100;fontColor=#232F3E;align=center;", 200, 180, 78, 78),
            ("rds", "Storage & DB", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;fillColor=#C925D1;fontColor=#232F3E;align=center;", 200, 320, 78, 78),
            ("fix", "Sprint de Remediação CoreScale (>=25% HRIs)", "rounded=1;fillColor=#ED7100;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;", 750, 200, 240, 50),
            ("cred", "Até US$ 5.000 Créditos AWS", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=14;fontStyle=1;", 750, 300, 240, 50),
        ]),
        ("ai-rag", "AI-RAG — Enterprise RAG", [
            ("s3", "Amazon S3", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;fillColor=#7AA116;fontColor=#232F3E;align=center;", 150, 250, 78, 78),
            ("kb", "Bedrock Knowledge Bases", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#01A88D;fontColor=#232F3E;align=center;", 400, 250, 78, 78),
            ("vec", "OpenSearch Serverless", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;fillColor=#8C4FFF;fontColor=#232F3E;align=center;", 650, 180, 78, 78),
            ("llm", "Claude 3.5 Sonnet", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#ED7100;fontColor=#232F3E;align=center;", 650, 320, 78, 78),
            ("chat", "Interface Corporativa com Citação de Fonte", "rounded=1;fillColor=#38BDF8;fontColor=#0F172A;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 900, 250, 220, 60),
        ]),
        ("ai-extract", "AI-EXTRACT — Extração para ERP", [
            ("s3", "Amazon S3 Inbound", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;fillColor=#7AA116;fontColor=#232F3E;align=center;", 150, 250, 78, 78),
            ("lbd", "AWS Lambda", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;fontColor=#232F3E;align=center;", 350, 250, 78, 78),
            ("txt", "Amazon Textract", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.textract;fillColor=#01A88D;fontColor=#232F3E;align=center;", 550, 180, 78, 78),
            ("bed", "Amazon Bedrock", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#01A88D;fontColor=#232F3E;align=center;", 550, 320, 78, 78),
            ("erp", "Webhook ERP (JSON Validado)", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;", 800, 250, 200, 60),
        ]),
        ("ai-agent", "AI-AGENT — Atendimento Autônomo", [
            ("chat", "WhatsApp / Webhook", "shape=mxgraph.aws4.client;fillColor=#232F3E;fontColor=#232F3E;align=center;", 150, 250, 78, 78),
            ("agent", "Bedrock AgentCore", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock_agentcore;fillColor=#01A88D;fontColor=#232F3E;align=center;", 450, 250, 78, 78),
            ("lbd", "Action Groups (Lambda)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;fontColor=#232F3E;align=center;", 750, 180, 78, 78),
            ("ddb", "DynamoDB (Sessões)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;fillColor=#8C4FFF;fontColor=#232F3E;align=center;", 750, 320, 78, 78),
            ("erp", "APIs de Negócio / Handover Humano", "rounded=1;fillColor=#F97316;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;", 1000, 250, 200, 60),
        ])
    ]

    for pid, pname, nodes in pages:
        model = ['<mxGraphModel dx="1400" dy="800" grid="1" gridSize="10" page="1" pageScale="1" pageWidth="1200" pageHeight="600"><root><mxCell id="0"/><mxCell id="1" parent="0"/>']
        for nid, nlabel, nstyle, nx, ny, nw, nh in nodes:
            model.append(f'<mxCell id="{nid}" value="{escape(nlabel)}" style="{nstyle}" vertex="1" parent="1"><mxGeometry x="{nx}" y="{ny}" width="{nw}" height="{nh}" as="geometry"/></mxCell>')
        # Connect nodes in a line for quick editing
        for idx in range(len(nodes) - 1):
            src = nodes[idx][0]
            tgt = nodes[idx+1][0]
            model.append(f'<mxCell id="e_{idx}" edge="1" parent="1" source="{src}" target="{tgt}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#64748B;strokeWidth=2;endArrow=block;"><mxGeometry relative="1" as="geometry"/></mxCell>')
        model.append('</root></mxGraphModel>')
        diagrams.append(f'<diagram id="{pid}" name="{escape(pname)}">{escape("".join(model), quote=False)}</diagram>')

    return ('<?xml version="1.0" encoding="UTF-8"?><mxfile host="app.diagrams.net" modified="' +
            datetime.datetime.now(datetime.timezone.utc).isoformat() +
            '" agent="CoreScale Architect" version="24.7.17" compressed="false">' +
            ''.join(diagrams) + '</mxfile>')


def main():
    print("Generating official reference architecture diagrams...")
    
    # 1. SVGs
    items = [
        ("sec-assess-architecture.svg", build_sec_assess()),
        ("war-express-architecture.svg", build_war_express()),
        ("ai-rag-architecture.svg", build_ai_rag()),
        ("ai-extract-architecture.svg", build_ai_extract()),
        ("ai-agent-architecture.svg", build_ai_agent()),
    ]
    
    for filename, content in items:
        path = OUT_DIR / filename
        path.write_text(content, encoding='utf-8')
        print(f"Generated SVG: {path} ({path.stat().st_size} bytes)")

    # 2. Draw.io
    drawio_content = generate_drawio_xml()
    drawio_path = OUT_DIR / "corescale-catalog-architectures.drawio"
    drawio_path.write_text(drawio_content, encoding='utf-8')
    print(f"Generated Draw.io: {drawio_path} ({drawio_path.stat().st_size} bytes)")

    # Individual drawio files
    root = ET.fromstring(drawio_content)
    for d in root.findall('diagram'):
        did = d.get('id')
        single_xml = f'<?xml version="1.0" encoding="UTF-8"?><mxfile host="app.diagrams.net">{ET.tostring(d, encoding="unicode")}</mxfile>'
        single_path = OUT_DIR / f"{did}-architecture.drawio"
        single_path.write_text(single_xml, encoding='utf-8')
        print(f"Generated single Draw.io: {single_path}")

    print("\nAll architectural diagrams generated successfully!")

if __name__ == '__main__':
    main()
