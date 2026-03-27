import requests
import os
import feedparser

# Configuración
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def obtener_noticias():
    # Lista de fuentes RSS fiables de España
    fuentes = [
        "https://www.rtve.es/noticias/rss/temas/espana.xml",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml"
    ]
    
    articulos = []
    
    for url in fuentes:
        try:
            feed = feedparser.parse(url)
            # Tomamos las 2 más recientes de cada fuente para no saturar
            for entry in feed.entries[:2]: 
                articulos.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': feed.feed.title if hasattr(feed.feed, 'title') else "Fuente España"
                })
        except Exception as e:
            print(f"Error al leer la fuente {url}: {e}")
            
    return articulos

def enviar_a_discord(articulos):
    for art in articulos:
        # Formato con la fuente incluida para mayor claridad
        data = {
            "content": f"📢 **{art['source']}**: {art['title']}\n🔗 {art['url']}",
            "username": "Noticias España Bot"
        }
        r = requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"Envío a Discord: {r.status_code}")

if __name__ == "__main__":
    if not DISCORD_WEBHOOK_URL:
        print("Error: No se ha configurado la variable DISCORD_WEBHOOK_URL")
    else:
        noticias = obtener_noticias()
        if noticias:
            print(f"Se encontraron {len(noticias)} noticias. Enviando...")
            enviar_a_discord(noticias)
        else:
            print("No se encontraron noticias para enviar.")
