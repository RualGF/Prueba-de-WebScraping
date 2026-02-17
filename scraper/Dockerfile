FROM python:3.14.2-slim
WORKDIR /app
# Copiamos solo su requirements
COPY scraper/requirements.txt . 
RUN pip install -r requirements.txt
COPY scraper/ .
# Ejecuta el script de scraping
CMD ["python", "scraping.py"]