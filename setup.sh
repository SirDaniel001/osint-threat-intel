#!/bin/bash

echo "=============================="
echo "OSINT Threat Intel Project Setup"
echo "=============================="

# 1. Create virtual environment
echo "[INFO] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
echo "[INFO] Upgrading pip..."
pip install --upgrade pip

# 3. Install dependencies
echo "[INFO] Installing dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "[ERROR] requirements.txt not found! Please create it first."
    exit 1
fi

# 4. Create necessary directories
echo "[INFO] Creating data and logs directories..."
mkdir -p data logs

# 5. Create .env file if not exists
if [ ! -f .env ]; then
    echo "[INFO] Creating .env file template..."
    cat <<EOT >> .env
# WHOIS API Key
WHOIS_API_KEY=your_whoisxml_api_key_here

# Email credentials
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
EMAIL_RECEIVER=receiver_email@gmail.com

# SMTP (default Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EOT
    echo "[INFO] .env file created. Please edit it and add real credentials."
else
    echo "[INFO] .env file already exists. Skipping..."
fi

echo "=============================="
echo "[+] Setup completed successfully!"
echo "Activate your virtual environment with: source venv/bin/activate"
echo "Then run your scripts as usual."
echo "=============================="
