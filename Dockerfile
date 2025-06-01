FROM python:3.11-slim

# Installer les dépendances système nécessaires (exemple, à adapter)
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libx11-xcb1 \
    libnss3 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libpango-1.0-0 \
    libxss1 \
    libxshmfence1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le requirements.txt et installer les packages Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer les navigateurs Playwright (Chromium, Firefox, WebKit)
RUN python3 -m playwright install

# Copier tout le code dans le conteneur
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python3", "api.py"]
