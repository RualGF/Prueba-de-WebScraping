FROM python:3.14.2-slim
WORKDIR /app
COPY dashboard/requirements.txt .
RUN pip install -r requirements.txt
COPY dashboard/ .
EXPOSE 8050
# Ejecuta la app de Dash
CMD ["python", "dashboard.py"]