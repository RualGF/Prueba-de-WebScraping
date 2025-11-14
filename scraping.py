import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

def extraer_citas():
    """
    Realiza el scraping de todas las citas de quotes.toscrape.com
    y guarda los datos en un archivo pickle.
    """
    print("="*60)
    print("🚀 INICIANDO SCRAPING DE CITAS")
    print("="*60)
    
    lista = []
    i = 1
    
    while True:
        url = f"https://quotes.toscrape.com/page/{i}/"
        respuesta = requests.get(url)
        print(f"\n📄 Sacando citas de la página {i}...")
        sopa = BeautifulSoup(respuesta.text, "html.parser")
            
        for q in sopa.find_all("div", "quote"):
            datos = {} 
            datos['quote'] = q.find("span", "text").text
            datos['author'] = q.find("small", "author").text
            datos['enlace'] = q.find("a")["href"]
            datos['tags'] = q.find("meta", "keywords")['content'].split(",")
            
            # Obtener información del autor
            urlAutor = f"https://quotes.toscrape.com" + (datos['enlace'])
            rAutor = requests.get(urlAutor)
            sAutor = BeautifulSoup(rAutor.text, "html.parser")
            datos['author_about'] = sAutor.find("div", "author-description").text.strip().replace("\\", "")
            datos['author_birthdate'] = dt.strptime(sAutor.find("span", "author-born-date").text, "%B %d, %Y")
            datos['author_birthplace'] = sAutor.find("span", "author-born-location").text.replace("in ", "")
            
            lista.append(datos)
        
        print(f"✓ Página {i} completada ({len(sopa.find_all('div', 'quote'))} citas)")
        
        # Verificar si hay más páginas
        if sopa.find("li", "next") == None:
            print("\n🏁 No hay más páginas. Extracción completada.")
            break
        i += 1
    
    # Crear DataFrame
    df = pd.DataFrame(lista)
    
    # Guardar datos
    df.to_pickle('quotes_data.pkl')
    df.to_csv('quotes_data.csv', index=False, encoding='utf-8')
    
    print("\n" + "="*60)
    print("✅ SCRAPING COMPLETADO")
    print("="*60)
    print(f"📊 Total de citas extraídas: {len(df)}")
    print(f"👥 Autores únicos: {df['author'].nunique()}")
    print(f"🏷️  Etiquetas únicas: {len(set([tag for tags in df['tags'] for tag in tags]))}")
    print(f"\n💾 Datos guardados en:")
    print(f"   - quotes_data.pkl (para el dashboard)")
    print(f"   - quotes_data.csv (para análisis externo)")
    print("="*60)
    
    return df

if __name__ == '__main__':
    try:
        df = extraer_citas()
        print("\n🎉 ¡Listo! Ahora puedes ejecutar 'dashboard.py' para visualizar los datos.")
    except Exception as e:
        print(f"\n❌ Error durante el scraping: {e}")
        import traceback
        traceback.print_exc()