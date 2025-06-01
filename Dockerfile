# Image officielle Python
FROM python:3.11-slim

# Installer les dépendances système nécessaires pour Playwright
RUN apt-get update && apt-get install -y \
    libgtk-4-1 libnss3 libxss1 libasound2 libx11-xcb1 libgbm1 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libpango-1.0-0 libpangocairo-1.0-0 libxcb1 libx11-6 libxext6 libxfixes3 libsecret-1-0 libenchant-2-2 libgraphene-1.0-0 libavif15 libmanette-0.2-0 wget \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer les navigateurs Playwright
RUN python3 -m playwright install

# Copier le reste du code
COPY . .

# Exposer le port 5000 (ou ton port d’API)
EXPOSE 5000

# Commande de lancement
CMD ["python3", "api.py"]
