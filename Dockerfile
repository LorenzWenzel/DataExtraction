# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# # Installiere Systemabhängigkeiten
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die Datei requirements.txt in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendungsdateien in das Arbeitsverzeichnis
COPY . .

#app/images ordner erstellen
RUN mkdir -p /app/images

# Stelle den Port 5000 zur Verfügung
EXPOSE 5000

# Definiere Umgebungsvariablen
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# Setze Umgebungsvariablen für Tesseract und Poppler
ENV TESSERACT_CMD_PATH=/usr/bin/tesseract
ENV POPLER_PATH=/usr/bin

# Starte die Flask-Anwendung
CMD ["flask", "run"]
