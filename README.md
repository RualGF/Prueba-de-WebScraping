# Pipeline de Web Scraping y Procesamiento de Datos

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-data-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.0+-red.svg)

---

## 📌 Descripción

Proyecto de ingeniería de datos enfocado en la extracción, transformación y almacenamiento de información textual mediante técnicas de web scraping.

El sistema implementa un pipeline de datos que recopila citas de personajes famosos desde una web pública, procesa la información y la almacena en formatos estructurados para su posterior análisis y visualización.

Como capa final, se incluye un dashboard interactivo desarrollado con Dash para explorar los datos generados.

---

## 📊 Arquitectura del sistema

El flujo de datos sigue la siguiente estructura:

Web origen  
→ Extracción (BeautifulSoup + Requests)  
→ Transformación (Pandas)  
→ Almacenamiento (CSV / Pickle)  
→ Consumo de datos  
→ Visualización (Dash)

### Componentes

- **Extracción**: scraping dinámico navegando entre páginas hasta detectar el final  
- **Transformación**: limpieza de texto, estructuración y enriquecimiento de datos  
- **Almacenamiento**: persistencia en CSV (portabilidad) y Pickle (eficiencia interna)  
- **Consumo**: lectura de datos para análisis y visualización  

---

## ⚙️ Funcionalidades principales

- Pipeline completo de scraping y procesamiento de datos  
- Extracción automática sin límite fijo de páginas  
- Limpieza y estructuración de datos textuales  
- Almacenamiento en múltiples formatos  
- Visualización interactiva mediante dashboard  

---

## 🧩 Decisiones técnicas relevantes

### Scraping dinámico
El proceso de extracción no depende de un número fijo de páginas, sino que detecta automáticamente la existencia de contenido adicional mediante el botón "Next".

### Transformación de datos
Se implementa una lógica específica para:
- Extraer información biográfica  
- Calcular siglos de nacimiento  
- Convertir valores a nomenclatura en números romanos  

### Estrategia de almacenamiento
Se utiliza un sistema dual:
- CSV → interoperabilidad y análisis externo  
- Pickle → preservación de estructuras complejas de Python  

---

## 📁 Estructura del proyecto

```
quotes-dashboard/
│
├── scraping.py              # Pipeline de extracción
├── dashboard.py             # Visualización de datos
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este archivo
│
├── quotes_data.pkl         # Datos procesados
└── quotes_data.csv        
```


---

## 🚀 Instalación

git clone https://github.com/RualGF/Prueba-de-WebScraping.git  
cd Prueba-de-WebScraping  

python -m venv .venv  
.venv/Scripts/activate  

pip install -r requirements.txt  

---

## ▶️ Uso

### 1. Ejecutar pipeline de scraping

python scraping.py  

Esto genera:
- quotes_data.csv  
- quotes_data.pkl  

---

### 2. Ejecutar dashboard

python dashboard.py  

Abrir en navegador:
http://127.0.0.1:8050  

---

## 📊 Datos generados

Cada registro contiene:

- Texto de la cita  
- Autor  
- Etiquetas  
- Información biográfica  
- Fecha y lugar de nacimiento  

---

## 👤 Contribución

- Diseño e implementación del pipeline de scraping  
- Procesamiento y estructuración de datos  
- Definición del modelo de almacenamiento  
- Desarrollo del dashboard para consumo de datos  

---

## 🧪 Posibles mejoras

- Persistencia en base de datos (SQLite/PostgreSQL)  
- Automatización del pipeline (scheduler)  
- Contenerización con Docker  
- Exposición de datos mediante API
