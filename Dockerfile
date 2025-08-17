# Minimal, basierend auf Debian Bookworm
FROM python:3-slim-bookworm

# Keine .pyc Files und sofortiges Logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Standard Serial Device (überschreibbar mit -e SERIAL=...)
ENV SERIAL=/dev/ttyUSB0

# System-Tools für Debugging (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installiere Python Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Verzeichnis
WORKDIR /app
COPY . /app

# Default Command
CMD ["python", "/app/nfm.py"]
