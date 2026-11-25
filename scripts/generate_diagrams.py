#!/usr/bin/env python3
"""
Generator of official AWS Reference Architecture Diagrams for CoreScale Catalog Offers.
Generates:
1. High-fidelity standalone vector SVGs with official AWS Architecture Icons embedded as base64.
2. Canonical, unescaped .drawio XML files with official AWS4 stencils and connectors.
3. Multi-page consolidated corescale-catalog-architectures.drawio.
"""

import os
import base64
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import datetime
from html import escape

BASE_DIR = Path('/home/jcastro/hermes-data/projects/cscale.com.br/cscale.com.br')
OUT_DIR = BASE_DIR / 'hugo/static/diagrams'
ICONS_DIR = BASE_DIR / 'scripts/aws-icons'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cached official AWS icon images as base64 data URIs
ICON_DATA = {}
for png_path in ICONS_DIR.glob('*.png'):
    name = png_path.stem
    b64 = base64.b64encode(png_path.read_bytes()).decode('utf-8')
    ICON_DATA[name] = f"data:image/png;base64,{b64}"

print(f"Loaded {len(ICON_DATA)} official AWS icons into memory.")

# Official AWS Color Palette
AWS_NAVY = "#232F3E"
AWS_ORANGE = "#ED7100"
AWS_PURPLE = "#8C4FFF"
AWS_MAGENTA = "#C925D1"
AWS_RED = "#DD344C"
AWS_PINK = "#E7157B"
AWS_GREEN = "#7AA116"
AWS_BLUE = "#147EBA"
AWS_TEAL = "#01A88D"

POINTS = '[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]]'

# ==============================================================================
# SVG Generator Engine
# ==============================================================================
def create_svg(title, subtitle, code, width, height, elements_fn):
    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#0F172A;font-family:'Inter',system-ui,-apple-system,sans-serif;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38BDF8"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#22C55E"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#F97316"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#0B0F19"/>

  <!-- Subtle Grid -->
  <g opacity="0.06">
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#94A3B8" stroke-width="1"/>' for x in range(0, width, 40))}
    {''.join(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#94A3B8" stroke-width="1"/>' for y in range(0, height, 40))}
  </g>

  <!-- Header Banner -->
  <rect x="30" y="24" width="{width - 60}" height="76" rx="12" fill="url(#headerGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
  
  <rect x="50" y="42" width="130" height="38" rx="8" fill="#F97316" fill-opacity="0.15" stroke="#F97316" stroke-width="1"/>
  <text x="115" y="66" fill="#F97316" font-size="14" font-weight="800" text-anchor="middle" letter-spacing="1.5">CORESCALE</text>
  
  <text x="200" y="56" fill="#F8FAFC" font-size="20" font-weight="700">{escape(title)}</text>
  <text x="200" y="80" fill="#94A3B8" font-size="13" font-weight="500">{escape(subtitle)}</text>

  <rect x="{width - 220}" y="44" width="170" height="34" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1"/>
  <circle cx="{width - 200}" cy="61" r="5" fill="#22C55E"/>
  <text x="{width - 115}" y="67" fill="#E2E8F0" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1">REF: {escape(code)}</text>

  <!-- Content Elements -->
''')
    elements_fn(svg)

    svg.append(f'''
  <!-- Footer -->
  <line x1="30" y1="{height - 35}" x2="{width - 30}" y2="{height - 35}" stroke="#1E293B" stroke-width="1"/>
  <text x="40" y="{height - 16}" fill="#64748B" font-size="11">Arquitetura de Referência Oficial CoreScale • Ícones Oficiais AWS • Padrão Prescriptive Guidance</text>
  <text x="{width - 40}" y="{height - 16}" fill="#64748B" font-size="11" text-anchor="end">Download .drawio disponível no catálogo • contato@corescale.com.br</text>
</svg>''')
    return '\n'.join(svg)

def svg_box(svg, x, y, w, h, title, subtitle="", stroke="#334155", badge_color="#38BDF8", dashed=False):
    dash_attr = 'stroke-dasharray="6 6"' if dashed else ''
    svg.append(f'''
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#0F172A" fill-opacity="0.85" stroke="{stroke}" stroke-width="1.5" {dash_attr}/>
    <rect x="{x}" y="{y}" width="{w}" height="38" rx="14" fill="{stroke}" fill-opacity="0.18"/>
    <rect x="{x+16}" y="{y+10}" width="8" height="18" rx="3" fill="{badge_color}"/>
    <text x="{x+32}" y="{y+23}" fill="#F1F5F9" font-size="13" font-weight="700">{escape(title)}</text>
    {f'<text x="{x+w-16}" y="{y+23}" fill="#94A3B8" font-size="11" text-anchor="end">{escape(subtitle)}</text>' if subtitle else ''}
  </g>''')

def svg_node(svg, x, y, w, h, label, sublabel, icon_key, color_accent="#F97316"):
    b64_img = ICON_DATA.get(icon_key, "")
    img_tag = f'<image href="{b64_img}" x="12" y="{(h-50)//2}" width="50" height="50" preserveAspectRatio="xMidYMid meet"/>' if b64_img else f'<rect x="14" y="{(h-42)//2}" width="42" height="42" rx="8" fill="{color_accent}" fill-opacity="0.2"/><text x="35" y="{(h-42)//2+26}" fill="{color_accent}" font-size="14" font-weight="700" text-anchor="middle">{icon_key[:3].upper()}</text>'
    
    svg.append(f'''
  <g transform="translate({x}, {y})">
    <rect width="{w}" height="{h}" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect width="5" height="{h}" rx="2.5" fill="{color_accent}"/>
    {img_tag}
    <text x="70" y="{(h-16)//2 + 2}" fill="#F8FAFC" font-size="13" font-weight="700">{escape(label)}</text>
    <text x="70" y="{(h-16)//2 + 20}" fill="#94A3B8" font-size="11">{escape(sublabel)}</text>
  </g>''')

def svg_arrow(svg, x1, y1, x2, y2, label="", color="#38BDF8", marker="arrow"):
    svg.append(f'''
  <path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#{marker})" stroke-linecap="round"/>''')
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        svg.append(f'''
  <rect x="{mx - 65}" y="{my - 11}" width="130" height="20" rx="4" fill="#0B0F19" stroke="#334155" stroke-width="1"/>
  <text x="{mx}" y="{my + 3}" fill="#E2E8F0" font-size="10" font-weight="600" text-anchor="middle">{escape(label)}</text>''')


# ==============================================================================
# 5 Architectures Definitions (SVG + Draw.io)
# ==============================================================================

# 1. SEC-ASSESS
def gen_sec_assess():
    def elements(s):
        svg_box(s, 40, 125, 340, 480, "Fontes de Telemetria (Contas AWS)", "Produção / Multi-Account", stroke="#334155", badge_color="#F97316")
        svg_box(s, 420, 125, 480, 480, "Núcleo de Auditoria & Detecção", "Security & Audit Account", stroke="#DD344C", badge_color="#DD344C")
        svg_box(s, 940, 125, 320, 480, "Plano de Remediação CoreScale", "Entrega Executiva & Suporte", stroke="#22C55E", badge_color="#22C55E")

        svg_node(s, 65, 185, 290, 68, "AWS CloudTrail", "Trilha global de auditoria de chamadas API", "cloudtrail", AWS_PINK)
        svg_node(s, 65, 275, 290, 68, "Amazon VPC Flow Logs", "Registro de fluxos e tráfego de rede IP", "vpc", AWS_PURPLE)
        svg_node(s, 65, 365, 290, 68, "AWS Config", "Avaliação e histórico de conformidade", "config", AWS_PINK)
        svg_node(s, 65, 455, 290, 68, "IAM Access Analyzer", "Identificação de acesso público / externo", "access-analyzer", AWS_RED)

        svg_node(s, 445, 185, 430, 80, "AWS Security Hub", "Score CIS AWS Foundations v3.0 & FSBP", "security-hub", AWS_RED)
        svg_node(s, 445, 295, 430, 80, "Amazon GuardDuty", "Detecção de ameaças com ML (DNS, S3, IAM)", "guardduty", AWS_RED)
        svg_node(s, 445, 405, 430, 80, "Amazon Inspector", "Varredura contínua de CVEs em EC2 e ECR", "inspector", AWS_RED)

        svg_node(s, 965, 185, 270, 75, "Quick Wins Imediatos", "Remediação de portas 22/3389 e S3 público", "security-hub", AWS_GREEN)
        svg_node(s, 965, 295, 270, 75, "Relatório CIS Benchmark", "Score de conformidade & Auditoria LGPD", "well-architected", AWS_BLUE)
        svg_node(s, 965, 405, 270, 75, "Sustentação SEC-MNG", "Plano contínuo de segurança gerenciada", "security-hub", AWS_PURPLE)

        svg_arrow(s, 355, 219, 445, 219, "Eventos API")
        svg_arrow(s, 355, 309, 445, 325, "Fluxos de Rede")
        svg_arrow(s, 355, 399, 445, 235, "Config Drift")
        svg_arrow(s, 355, 489, 445, 245, "Alertas IAM")

        svg_arrow(s, 875, 225, 965, 225, "Prioridade Alta", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 875, 335, 965, 335, "Matriz Severidade", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 875, 445, 965, 445, "Backlog Técnico", color="#22C55E", marker="arrow-green")

    svg = create_svg(
        "Assessment & Auditoria de Postura AWS",
        "Detecção de brechas, verificação CIS Benchmark v3.0 e plano de remediação imediata",
        "SEC-ASSESS", 1300, 650, elements
    )
    
    drawio_nodes = [
        ("shub", "AWS Security Hub", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.security_hub;fillColor=#DD344C;", 500, 200, 78, 78),
        ("gd", "Amazon GuardDuty", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.guardduty;fillColor=#DD344C;", 500, 350, 78, 78),
        ("trail", "AWS CloudTrail", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudtrail;fillColor=#E7157B;", 180, 180, 78, 78),
        ("cfg", "AWS Config", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.config;fillColor=#E7157B;", 180, 300, 78, 78),
        ("iam", "IAM Access Analyzer", "shape=mxgraph.aws4.access_analyzer;fillColor=#DD344C;", 180, 420, 78, 78),
        ("rep", "Relatório CIS Benchmark & Remediação", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 800, 275, 240, 65),
    ]
    drawio_edges = [
        ("trail", "shub", "Eventos"),
        ("cfg", "shub", "Drift"),
        ("iam", "shub", "Acessos"),
        ("shub", "rep", "Findings"),
        ("gd", "rep", "Ameaças"),
    ]
    return svg, drawio_nodes, drawio_edges


# 2. WAR-EXPRESS
def gen_war_express():
    def elements(s):
        svg_box(s, 40, 125, 340, 480, "Workload AWS Avaliado", "Produção Multi-AZ", stroke="#334155", badge_color="#F97316")
        svg_box(s, 420, 125, 480, 480, "AWS Well-Architected Tool", "Revisão dos 6 Pilares Oficiais", stroke="#E7157B", badge_color="#E7157B")
        svg_box(s, 940, 125, 320, 480, "Remediação & Financiamento", "Geração de Valor & Créditos", stroke="#22C55E", badge_color="#22C55E")

        svg_node(s, 65, 185, 290, 68, "Compute & Workloads", "Amazon EC2, EKS, ECS, Lambda", "ec2", AWS_ORANGE)
        svg_node(s, 65, 275, 290, 68, "Bancos de Dados & Storage", "RDS Aurora, DynamoDB, Amazon S3", "rds", AWS_MAGENTA)
        svg_node(s, 65, 365, 290, 68, "Rede & Segurança", "VPC Multi-AZ, AWS WAF, Shield", "vpc", AWS_PURPLE)
        svg_node(s, 65, 455, 290, 68, "Auditoria & Logs", "AWS CloudTrail, CloudWatch Logs", "cloudtrail", AWS_BLUE)

        svg_node(s, 445, 185, 430, 78, "Avaliação dos 6 Pilares", "Segurança, Confiabilidade, Performance, Custo, Ops, Sustentabilidade", "well-architected", AWS_PINK)
        svg_node(s, 445, 295, 430, 78, "Mapeamento HRIs e MRIs", "High Risk Issues e Medium Risk Issues catalogados", "security-hub", AWS_RED)
        svg_node(s, 445, 405, 430, 78, "Backlog Oficial de Ação", "Plano prescritivo gerado pela ferramenta oficial", "config", AWS_BLUE)

        svg_node(s, 965, 185, 270, 75, "Sprint CoreScale (>=25%)", "Correção técnica comprovada dos HRIs", "well-architected", AWS_GREEN)
        svg_node(s, 965, 295, 270, 75, "Submissão Oficial AWS", "Validação com evidências técnicas no portal", "cloudtrail", AWS_ORANGE)
        svg_node(s, 965, 405, 270, 75, "Até US$ 5.000 em Créditos", "Crédito na fatura para amortizar custos", "s3", AWS_GREEN)

        svg_arrow(s, 355, 219, 445, 219, "Diagnóstico")
        svg_arrow(s, 355, 309, 445, 235, "Telemetria")
        svg_arrow(s, 355, 399, 445, 250, "Topologia")

        svg_arrow(s, 660, 263, 660, 295, "Identifica")
        svg_arrow(s, 660, 373, 660, 405, "Prescreve")

        svg_arrow(s, 875, 335, 965, 225, "Execução", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 1100, 260, 1100, 295, "Comprova", color="#F97316", marker="arrow-orange")
        svg_arrow(s, 1100, 370, 1100, 405, "Destrava", color="#22C55E", marker="arrow-green")

    svg = create_svg(
        "AWS Well-Architected Review (WAR) Express",
        "Auditoria dos 6 pilares, eliminação de HRIs e destravamento de até US$ 5.000 em créditos AWS",
        "WAR-EXPRESS", 1300, 650, elements
    )
    
    drawio_nodes = [
        ("ec2", "Compute (EC2/EKS)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;fillColor=#ED7100;", 150, 180, 78, 78),
        ("rds", "Banco de Dados (RDS)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;fillColor=#C925D1;", 150, 320, 78, 78),
        ("tool", "Well-Architected Tool", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.well_architect_tool;fillColor=#E7157B;", 450, 250, 78, 78),
        ("fix", "Sprint Remediação CoreScale", "rounded=1;fillColor=#ED7100;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 780, 200, 220, 60),
        ("cred", "Até US$ 5.000 Créditos AWS", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=14;fontStyle=1;", 780, 310, 220, 60),
    ]
    drawio_edges = [
        ("ec2", "tool", "Análise"),
        ("rds", "tool", "Análise"),
        ("tool", "fix", "HRIs Identificados"),
        ("fix", "cred", "Validação AWS"),
    ]
    return svg, drawio_nodes, drawio_edges


# 3. AI-RAG
def gen_ai_rag():
    def elements(s):
        svg_box(s, 40, 125, 280, 480, "Fontes Corporativas", "S3 / Repositórios", stroke="#334155", badge_color="#7AA116")
        svg_box(s, 360, 125, 540, 480, "Amazon Bedrock & Vector Store", "Conta AWS Privada do Cliente", stroke="#01A88D", badge_color="#01A88D")
        svg_box(s, 940, 125, 320, 480, "Canais de Consumo", "Interface Segura", stroke="#8C4FFF", badge_color="#8C4FFF")

        svg_node(s, 65, 185, 230, 75, "Amazon S3", "PDFs, DOCX, Manuais, Políticas", "s3", AWS_GREEN)
        svg_node(s, 65, 295, 230, 75, "SharePoint / Drive", "Sincronização via Connectors", "config", AWS_BLUE)
        svg_node(s, 65, 405, 230, 75, "Bancos / ERP Docs", "Extração contínua de relatórios", "rds", AWS_PURPLE)

        svg_node(s, 385, 185, 490, 78, "Knowledge Bases for Bedrock", "Chunking inteligente & Titan Text Embeddings v2", "bedrock", AWS_TEAL)
        svg_node(s, 385, 280, 490, 78, "OpenSearch Serverless", "Vector Engine isolado com criptografia KMS", "opensearch", AWS_PURPLE)
        svg_node(s, 385, 375, 490, 78, "Anthropic Claude 3.5 Sonnet", "Inferência privada no Amazon Bedrock (sem retenção)", "bedrock", AWS_ORANGE)
        svg_node(s, 385, 470, 490, 78, "Bedrock Guardrails", "Filtro PII / LGPD, anti-jailbreak e citações estritas", "security-hub", AWS_RED)

        svg_node(s, 965, 185, 270, 75, "Chat Corporativo Web", "Interface limpa com link da fonte citada", "ec2", AWS_BLUE)
        svg_node(s, 965, 295, 270, 75, "Microsoft Teams / Slack", "Bot interno para colaboradores", "lambda", AWS_PURPLE)
        svg_node(s, 965, 405, 270, 75, "API Gateway / Lambda", "Integração com sistemas internos e ERP", "api-gateway", AWS_ORANGE)

        svg_arrow(s, 295, 222, 385, 222, "Data Sync")
        svg_arrow(s, 295, 332, 385, 235, "Conector")
        
        svg_arrow(s, 630, 263, 630, 280, "Vetores")
        svg_arrow(s, 630, 358, 630, 375, "Busca Híbrida")
        svg_arrow(s, 630, 453, 630, 470, "Proteção")

        svg_arrow(s, 875, 400, 965, 225, "Resposta + Fonte", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 875, 415, 965, 332, "Notificação", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 875, 430, 965, 442, "REST JSON", color="#22C55E", marker="arrow-green")

    svg = create_svg(
        "Assistente de Conhecimento Corporativo (Enterprise RAG)",
        "Amazon Bedrock Knowledge Bases + OpenSearch Serverless + Claude 3.5 Sonnet com citações exatas",
        "AI-RAG", 1300, 650, elements
    )
    
    drawio_nodes = [
        ("s3", "Amazon S3", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;fillColor=#7AA116;", 150, 250, 78, 78),
        ("kb", "Bedrock Knowledge Bases", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#01A88D;", 400, 250, 78, 78),
        ("vec", "OpenSearch Serverless", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elasticsearch_service;fillColor=#8C4FFF;", 650, 180, 78, 78),
        ("llm", "Claude 3.5 Sonnet", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#ED7100;", 650, 320, 78, 78),
        ("chat", "Interface Corporativa (Citação Exata)", "rounded=1;fillColor=#38BDF8;fontColor=#0F172A;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 920, 250, 220, 60),
    ]
    drawio_edges = [
        ("s3", "kb", "Sync"),
        ("kb", "vec", "Embeddings"),
        ("vec", "llm", "Contexto Relevante"),
        ("llm", "chat", "Resposta com Link de Página"),
    ]
    return svg, drawio_nodes, drawio_edges


# 4. AI-EXTRACT
def gen_ai_extract():
    def elements(s):
        svg_box(s, 40, 125, 270, 480, "Ingestão de Documentos", "S3 Inbound Bucket", stroke="#334155", badge_color="#7AA116")
        svg_box(s, 350, 125, 540, 480, "Pipeline Serverless AWS", "OCR + IA Generativa", stroke="#01A88D", badge_color="#01A88D")
        svg_box(s, 930, 125, 330, 480, "Destino ERP & Exceções", "Automação Contábil", stroke="#22C55E", badge_color="#22C55E")

        svg_node(s, 65, 205, 220, 75, "Upload de Arquivos", "Notas Fiscais, Faturas, Boletos", "s3", AWS_GREEN)
        svg_node(s, 65, 345, 220, 75, "Amazon S3 Inbound", "Eventos de criação de objeto", "s3", AWS_GREEN)

        svg_node(s, 375, 175, 490, 75, "AWS Lambda Orchestrator", "Gatilho automático e orquestração assíncrona", "lambda", AWS_ORANGE)
        svg_node(s, 375, 275, 490, 75, "Amazon Textract", "OCR estruturado (AnalyzeDocument / Tables)", "textract", AWS_TEAL)
        svg_node(s, 375, 375, 490, 75, "Amazon Bedrock (Haiku)", "Normalização semântica em JSON validado", "bedrock", AWS_TEAL)
        svg_node(s, 375, 475, 490, 75, "Validador de Regras", "Checagem de CNPJ, totais e impostos", "security-hub", AWS_BLUE)

        svg_node(s, 955, 195, 280, 80, "Integração ERP (API)", "SAP, Totvs, Senior, Omie via Webhook", "api-gateway", AWS_GREEN)
        svg_node(s, 955, 315, 280, 80, "Amazon DynamoDB", "Histórico de auditoria e payload completo", "dynamodb", AWS_PURPLE)
        svg_node(s, 955, 435, 280, 80, "Fila SQS de Exceções", "Transbordo para conferência humana", "sqs", AWS_RED)

        svg_arrow(s, 175, 280, 175, 345, "Upload")
        svg_arrow(s, 285, 382, 375, 212, "S3 Event")
        
        svg_arrow(s, 620, 250, 620, 275, "Executa OCR")
        svg_arrow(s, 620, 350, 620, 375, "Raw Text")
        svg_arrow(s, 620, 450, 620, 475, "JSON Estruturado")

        svg_arrow(s, 865, 512, 955, 235, "Válido (>=95%)", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 865, 512, 955, 355, "Gravação", color="#38BDF8", marker="arrow")
        svg_arrow(s, 865, 512, 955, 475, "Erro / Divergência", color="#EF4444", marker="arrow")

    svg = create_svg(
        "Extração Inteligente de Documentos para ERP",
        "Pipeline serverless com Amazon Textract e Bedrock para automação contábil com validação estrita",
        "AI-EXTRACT", 1300, 650, elements
    )
    
    drawio_nodes = [
        ("s3", "Amazon S3 Inbound", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;fillColor=#7AA116;", 150, 250, 78, 78),
        ("lbd", "AWS Lambda", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;", 350, 250, 78, 78),
        ("txt", "Amazon Textract", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.textract;fillColor=#01A88D;", 550, 180, 78, 78),
        ("bed", "Amazon Bedrock", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock;fillColor=#01A88D;", 550, 320, 78, 78),
        ("erp", "Webhook ERP (JSON)", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 800, 200, 200, 50),
        ("sqs", "Fila SQS (Exceções)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;fillColor=#DD344C;", 800, 320, 78, 78),
    ]
    drawio_edges = [
        ("s3", "lbd", "S3 Event"),
        ("lbd", "txt", "AnalyzeDocument"),
        ("txt", "bed", "Text Tables"),
        ("bed", "erp", "Confiança >= 95%"),
        ("bed", "sqs", "Divergência"),
    ]
    return svg, drawio_nodes, drawio_edges


# 5. AI-AGENT
def gen_ai_agent():
    def elements(s):
        svg_box(s, 40, 125, 270, 480, "Canais Omnichannel", "Entrada de Clientes", stroke="#334155", badge_color="#8C4FFF")
        svg_box(s, 350, 125, 540, 480, "Amazon Bedrock AgentCore", "Raciocínio & Ferramentas", stroke="#01A88D", badge_color="#01A88D")
        svg_box(s, 930, 125, 330, 480, "Sistemas & Transbordo", "Ações Conectadas", stroke="#22C55E", badge_color="#22C55E")

        svg_node(s, 65, 195, 220, 75, "WhatsApp Business", "API oficial de mensagens", "api-gateway", AWS_GREEN)
        svg_node(s, 65, 315, 220, 75, "Webchat Corporativo", "Widget responsivo no site", "ec2", AWS_BLUE)
        svg_node(s, 65, 435, 220, 75, "API Gateway", "Webhook seguro com rate-limit", "api-gateway", AWS_ORANGE)

        svg_node(s, 375, 175, 490, 75, "Bedrock Agent Router", "Orquestração ReAct e intenções", "bedrock", AWS_TEAL)
        svg_node(s, 375, 275, 490, 75, "Knowledge Base Integrada", "Perguntas frequentes e catálogo de produtos", "bedrock", AWS_TEAL)
        svg_node(s, 375, 375, 490, 75, "Action Groups (Lambda)", "Chamadas para APIs de negócio", "lambda", AWS_ORANGE)
        svg_node(s, 375, 475, 490, 75, "Amazon DynamoDB", "Memória de contexto e histórico de sessão", "dynamodb", AWS_PURPLE)

        svg_node(s, 955, 195, 280, 80, "APIs de Negócio", "ERP, CRM, Status de Pedido, 2ª Via", "api-gateway", AWS_GREEN)
        svg_node(s, 955, 315, 280, 80, "Transbordo Humano", "Fila de atendimento (Zendesk / GLPI)", "sns", AWS_ORANGE)
        svg_node(s, 955, 435, 280, 80, "Auditoria CloudWatch", "Métricas de FRT, tokens e conversões", "cloudtrail", AWS_BLUE)

        svg_arrow(s, 285, 232, 375, 212, "Mensagem")
        svg_arrow(s, 285, 352, 375, 225, "Chat")
        svg_arrow(s, 285, 472, 375, 235, "Webhook")
        
        svg_arrow(s, 620, 250, 620, 275, "Consulta RAG")
        svg_arrow(s, 620, 350, 620, 375, "Executa Ação")
        svg_arrow(s, 620, 450, 620, 475, "Salva Contexto")

        svg_arrow(s, 865, 412, 955, 235, "Executa API", color="#22C55E", marker="arrow-green")
        svg_arrow(s, 865, 212, 955, 355, "Handover", color="#F97316", marker="arrow-orange")
        svg_arrow(s, 865, 512, 955, 475, "Logs & Métricas", color="#38BDF8", marker="arrow")

    svg = create_svg(
        "Agente Autônomo de Atendimento e Triagem",
        "Orquestração conversacional com Bedrock Agents, integração com APIs internas e transbordo humano",
        "AI-AGENT", 1300, 650, elements
    )
    
    drawio_nodes = [
        ("gw", "API Gateway", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;fillColor=#ED7100;", 150, 250, 78, 78),
        ("agent", "Bedrock AgentCore", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.bedrock_agentcore;fillColor=#01A88D;", 450, 250, 78, 78),
        ("lbd", "Action Groups (Lambda)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;", 720, 180, 78, 78),
        ("ddb", "DynamoDB (Sessões)", "shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;fillColor=#C925D1;", 720, 320, 78, 78),
        ("erp", "APIs de Negócio", "rounded=1;fillColor=#22C55E;fontColor=#FFFFFF;strokeColor=none;align=center;fontSize=13;fontStyle=1;", 980, 250, 180, 50),
    ]
    drawio_edges = [
        ("gw", "agent", "Webhook Event"),
        ("agent", "lbd", "Call Tool"),
        ("agent", "ddb", "Context / Memory"),
        ("lbd", "erp", "REST JSON"),
    ]
    return svg, drawio_nodes, drawio_edges


# ==============================================================================
# Canonical Draw.io Builder (Real XML Elements)
# ==============================================================================
def build_drawio_diagram(pid, pname, nodes, edges):
    d = Element('diagram', {'id': pid, 'name': pname})
    m = SubElement(d, 'mxGraphModel', {
        'dx': '1400', 'dy': '800', 'grid': '1', 'gridSize': '10',
        'page': '1', 'pageScale': '1', 'pageWidth': '1300', 'pageHeight': '700'
    })
    r = SubElement(m, 'root')
    SubElement(r, 'mxCell', {'id': '0'})
    SubElement(r, 'mxCell', {'id': '1', 'parent': '0'})

    # Background
    bg = SubElement(r, 'mxCell', {
        'id': f'bg_{pid}', 'value': '',
        'style': 'rounded=0;fillColor=#F8FAFC;strokeColor=none;',
        'vertex': '1', 'parent': '1'
    })
    SubElement(bg, 'mxGeometry', {'x': '0', 'y': '0', 'width': '1300', 'height': '700', 'as': 'geometry'})

    # Title Box
    tb = SubElement(r, 'mxCell', {
        'id': f'title_{pid}', 'value': f'<b>CoreScale Architecture Reference — {pname}</b>',
        'style': 'text;html=1;align=left;verticalAlign=middle;fontSize=16;fontColor=#1E293B;',
        'vertex': '1', 'parent': '1'
    })
    SubElement(tb, 'mxGeometry', {'x': '40', 'y': '30', 'width': '800', 'height': '40', 'as': 'geometry'})

    # Nodes
    for nid, nlabel, nstyle, nx, ny, nw, nh in nodes:
        c = SubElement(r, 'mxCell', {
            'id': nid, 'value': nlabel, 'style': nstyle,
            'vertex': '1', 'parent': '1'
        })
        SubElement(c, 'mxGeometry', {'x': str(nx), 'y': str(ny), 'width': str(nw), 'height': str(nh), 'as': 'geometry'})

    # Edges
    for idx, (src, tgt, elabel) in enumerate(edges):
        e = SubElement(r, 'mxCell', {
            'id': f'e_{idx}', 'value': elabel,
            'style': 'edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#64748B;strokeWidth=2;endArrow=block;fontColor=#475569;fontSize=11;labelBackgroundColor=#F8FAFC;',
            'edge': '1', 'parent': '1', 'source': src, 'target': tgt
        })
        SubElement(e, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    return d


def main():
    generators = [
        ("sec-assess", "SEC-ASSESS — Security Assessment & CIS", gen_sec_assess()),
        ("war-express", "WAR-EXPRESS — Well-Architected Review", gen_war_express()),
        ("ai-rag", "AI-RAG — Enterprise Knowledge RAG", gen_ai_rag()),
        ("ai-extract", "AI-EXTRACT — Extração para ERP", gen_ai_extract()),
        ("ai-agent", "AI-AGENT — Atendimento Autônomo", gen_ai_agent()),
    ]

    # Consolidated Multi-Page Draw.io
    consolidated_root = Element('mxfile', {
        'host': 'app.diagrams.net',
        'modified': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'agent': 'CoreScale Architect Studio',
        'version': '24.7.17'
    })

    for pid, pname, (svg_content, nodes, edges) in generators:
        # 1. Save standalone SVG
        svg_path = OUT_DIR / f"{pid}-architecture.svg"
        svg_path.write_text(svg_content, encoding='utf-8')
        print(f"✓ Saved SVG: {svg_path} ({svg_path.stat().st_size} bytes)")

        # 2. Build Draw.io Diagram Element
        diag_elem = build_drawio_diagram(pid, pname, nodes, edges)
        consolidated_root.append(diag_elem)

        # 3. Save Single-Page Draw.io
        single_root = Element('mxfile', {'host': 'app.diagrams.net', 'version': '24.7.17'})
        single_root.append(diag_elem)
        single_path = OUT_DIR / f"{pid}-architecture.drawio"
        ElementTree(single_root).write(single_path, encoding='utf-8', xml_declaration=True)
        print(f"✓ Saved Draw.io: {single_path} ({single_path.stat().st_size} bytes)")

    # 4. Save Consolidated Draw.io
    consolidated_path = OUT_DIR / "corescale-catalog-architectures.drawio"
    ElementTree(consolidated_root).write(consolidated_path, encoding='utf-8', xml_declaration=True)
    print(f"✓ Saved Consolidated Draw.io: {consolidated_path} ({consolidated_path.stat().st_size} bytes)")


if __name__ == '__main__':
    main()
