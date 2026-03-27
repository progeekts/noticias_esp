import requests
import os
import feedparser
# Configuración
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def obtener_noticias():
    # URL del RSS de noticias de última hora de RTVE
    url_rss = "https://www.rtve.es/noticias/rss/temas/espana.xml"
    feed = feedparser.parse(url_rss)
    
    articulos = []
    for entry in feed.entries[:5]: # Tomamos las 5 más recientes
        articulos.append({
            'title': entry.title,
            'url': entry.link
        })
    return articulos

def enviar_a_discord(articulos):
    for art in articulos:
        # Evitamos enviar artículos que han sido eliminados o están incompletos
        if art['title'] == "[Removed]":
            continue
            
        data = {
            "content": f"**{art['title']}**\n{art['url']}",
            "username": "Noticias España Bot"
        }
        r = requests.post(DISCORD_WEBHOOK_URL, json=data)
        print(f"Envío a Discord: {r.status_code}")

if __name__ == "__main__":
    noticias = obtener_noticias()
    if noticias:
        print(f"Se encontraron {len(noticias)} noticias. Enviando...")
        enviar_a_discord(noticias)
    else:
        print("No se encontraron noticias para enviar.")
