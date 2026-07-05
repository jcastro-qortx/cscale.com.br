#!/bin/bash
# Deploy CoreScale static site to S3
# Usage: ./deploy.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="$SCRIPT_DIR/terraform"

echo "═══════════════════════════════════════════"
echo "  CoreScale Site - Deploy"
echo "═══════════════════════════════════════════"

# 1. Terraform apply
echo ""
echo "▶ Running Terraform..."
cd "$TERRAFORM_DIR"

if [ ! -d ".terraform" ]; then
  terraform init
fi

terraform apply -auto-approve

# 2. Get outputs
BUCKET_NAME=$(terraform output -raw bucket_name)
API_URL=$(terraform output -raw contact_api_url)
WEBSITE_URL=$(terraform output -raw website_url)

echo ""
echo "▶ Bucket: $BUCKET_NAME"
echo "▶ API URL: $API_URL"

# 3. Update contact.html with actual API URL
cd "$SCRIPT_DIR"
sed "s|__API_URL__/contact|${API_URL}|g" contact.html > contact_deployed.html

# 4. Upload files to S3
echo ""
echo "▶ Uploading site files to S3..."

aws s3 cp index.html "s3://$BUCKET_NAME/index.html" \
  --content-type "text/html" \
  --cache-control "max-age=300"

aws s3 cp contact_deployed.html "s3://$BUCKET_NAME/contact.html" \
  --content-type "text/html" \
  --cache-control "max-age=300"

# Upload extensionless version for clean URLs (/contact)
aws s3 cp contact_deployed.html "s3://$BUCKET_NAME/contact" \
  --content-type "text/html" \
  --cache-control "max-age=300"

# Upload favicons
aws s3 cp favicon.png "s3://$BUCKET_NAME/favicon.png" \
  --content-type "image/png" \
  --cache-control "max-age=86400"

aws s3 cp favicon-32x32.png "s3://$BUCKET_NAME/favicon-32x32.png" \
  --content-type "image/png" \
  --cache-control "max-age=86400"

aws s3 cp favicon-16x16.png "s3://$BUCKET_NAME/favicon-16x16.png" \
  --content-type "image/png" \
  --cache-control "max-age=86400"

# Cleanup temp file
rm -f contact_deployed.html

echo ""
echo "═══════════════════════════════════════════"
echo "  ✓ Deploy concluído!"
echo "═══════════════════════════════════════════"
echo ""
echo "  Site: $WEBSITE_URL"
echo "  Contato: ${WEBSITE_URL}/contact.html"
echo "  API: $API_URL"
echo ""
echo "  ⚠️  IMPORTANTE: Verifique os emails de verificação do SES:"
echo "     - jcastro@cscale.com.br (destinatário)"
echo "     - site@corescale.com.br (remetente)"
echo "     O formulário só funcionará após a confirmação de AMBOS."
echo ""
