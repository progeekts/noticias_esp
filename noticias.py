import requests
import os

# Configuración
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def obtener_noticias():
    # AÑADIDO: User-Agent para evitar que la API bloquee la petición desde GitHub
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # OPCIONAL: Si 'country=es' sigue dando 0, puedes probar 'language=es'
    #url = f"https://newsapi.org/v2/top-headlines?country=es&apiKey={NEWS_API_KEY}"
    url = f"https://newsapi.org/v2/top-headlines?language=es&q=España&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Imprimimos para ver en los logs si hay algún mensaje de error específico
    print(f"Status Code: {response.status_code}")
    print(f"Datos recibidos: {data}")
    
    articles = data.get("articles", [])[:5]
    return articles

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
