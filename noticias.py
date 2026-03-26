import requests
import os

# Configuración
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def obtener_noticias():
    url = f"https://newsapi.org/v2/top-headlines?country=es&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])[:5] # Tomamos las 5 mejores
    return articles

def enviar_a_discord(articulos):
    for art in articulos:
        data = {
            "content": f"**{art['title']}**\n{art['url']}",
            "username": "Noticias España Bot"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=data)

if __name__ == "__main__":
    noticias = obtener_noticias()
    if noticias:
        enviar_a_discord(noticias)
