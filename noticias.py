import requests
import os
import feedparser

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MEMORIA_FILE = "enviados.txt"

def cargar_memoria():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "r") as f:
            return set(line.strip() for line in f)
    return set()

def guardar_en_memoria(url):
    with open(MEMORIA_FILE, "a") as f:
        f.write(url + "\n")

def obtener_noticias():
    fuentes = [
        "https://www.rtve.es/noticias/rss/temas/espana.xml",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml"
    ]
    
    memoria = cargar_memoria()
    articulos = []
    
    for url_fuente in fuentes:
        try:
            feed = feedparser.parse(url_fuente)
            nombre_fuente = getattr(feed.feed, 'title', "Noticias")
            
            for entry in feed.entries[:3]:
                if entry.link not in memoria:
                    articulos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'source': nombre_fuente
                    })
        except Exception as e:
            print(f"Error en {url_fuente}: {e}")
            
    return articulos

def enviar_a_discord(articulos):
    for art in articulos:
        try:
            data = {
                "content": f"📢 **{art['source']}**: {art['title']}\n🔗 {art['url']}",
                "username": "Noticias España"
            }
            r = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
            if r.status_code == 204 or r.status_code == 200:
                guardar_en_memoria(art.get('url'))
                print(f"Enviado y guardado: {art['title'][:30]}...")
        except Exception as e:
            print(f"Error enviando: {e}")

if __name__ == "__main__":
    noticias = obtener_noticias()
    if noticias:
        enviar_a_discord(noticias)
    else:
        print("No hay noticias nuevas.")
