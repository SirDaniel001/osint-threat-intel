# ------------------------------------
# OSINT Threat Intelligence Full Pipeline (Tor + Dashboard + SOCKS Support)
# ------------------------------------
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    tor \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into container
COPY . /app

# Install Python dependencies including SOCKS support
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install "requests[socks]"

# Configure Tor for SOCKS and ControlPort
RUN echo "ControlPort 9051" >> /etc/tor/torrc && \
    echo "CookieAuthentication 0" >> /etc/tor/torrc && \
    echo "SOCKSPort 9050" >> /etc/tor/torrc

# Expose ports
EXPOSE 8050 9050

# Add entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Default command (MODE can override)
ENTRYPOINT ["/app/entrypoint.sh"]
