"""
Contact form Lambda handler.
Receives form submissions via API Gateway and sends email via SES.
"""

import json
import os
import boto3
from botocore.exceptions import ClientError

ses_client = boto3.client("ses", region_name=os.environ.get("AWS_SES_REGION", "us-east-1"))

CONTACT_EMAIL = os.environ["CONTACT_EMAIL"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
ALLOWED_ORIGIN = "https://corescale.com.br"


def handler(event, context):
    """Handle POST /contact requests."""
    # Extract origin and build CORS headers conditionally
    origin = event.get("headers", {}).get("origin", "")
    headers = {"Content-Type": "application/json"}
    if origin == ALLOWED_ORIGIN:
        headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    try:
        body = json.loads(event.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Invalid request body"}),
        }

    # 1. Honeypot check (raw, no strip)
    honeypot = body.get("website", "")
    if honeypot:  # non-empty = bot
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Mensagem enviada com sucesso!"}),
        }

    # 2. Extract and validate fields
    name = body.get("name", "").strip()
    email = body.get("email", "").strip()
    company = body.get("company", "").strip()
    message = body.get("message", "").strip()

    # Name validation: 2-200 chars
    if len(name) < 2 or len(name) > 200:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Campo 'name' deve ter entre 2 e 200 caracteres."}),
        }

    # Email validation: must contain @ with dot in domain part
    if "@" not in email:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Campo 'email' deve conter um endereço válido."}),
        }
    domain_part = email.split("@", 1)[1]
    if "." not in domain_part:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Campo 'email' deve conter um endereço válido."}),
        }

    # Message validation: 10-5000 chars
    if len(message) < 10 or len(message) > 5000:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "Campo 'message' deve ter entre 10 e 5000 caracteres."}),
        }

    # Send email via SES
    subject = f"[CoreScale Site] Nova mensagem de {name}"
    company_line = f"\nEmpresa: {company}" if company else ""
    email_body = f"""Nova mensagem do formulário de contato do site:

Nome: {name}
Email: {email}{company_line}

Mensagem:
{message}

---
Enviado automaticamente pelo formulário de contato do site cscale.com.br
"""

    try:
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={"ToAddresses": [CONTACT_EMAIL]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": email_body, "Charset": "UTF-8"}},
            },
            ReplyToAddresses=[email],
        )
    except ClientError as e:
        print(f"SES error: {e}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Erro ao enviar mensagem. Tente novamente."}),
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({"message": "Mensagem enviada com sucesso!"}),
    }
