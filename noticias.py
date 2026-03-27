import requests
import os
import feedparser

# Configuración
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def obtener_noticias():
    # Fuentes RSS estables de España
    fuentes = [
        "https://www.rtve.es/noticias/rss/temas/espana.xml",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml"
    ]
    
    articulos = []
    
    for url in fuentes:
        try:
            # Añadimos un timeout para que el script no se quede colgado si una web no responde
            feed = feedparser.parse(url)
            
            # Verificamos si el feed tiene entradas
            if not feed.entries:
                print(f"Aviso: La fuente {url} no devolvió noticias.")
                continue

            nombre_fuente = getattr(feed.feed, 'title', "Noticias España")
            
            for entry in feed.entries[:2]: 
                # Validamos que existan título y link antes de añadir
                if hasattr(entry, 'title') and hasattr(entry, 'link'):
                    articulos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'source': nombre_fuente
                    })
        except Exception as e:
            print(f"Error procesando {url}: {e}")
            
    return articulos

def enviar_a_discord(articulos):
    if not DISCORD_WEBHOOK_URL:
        print("Error: DISCORD_WEBHOOK_URL no configurado.")
        return

    for art in articulos:
        try:
            data = {
                "content": f"📢 **{art['source']}**: {art['title']}\n🔗 {art['url']}",
                "username": "Noticias España Bot"
            }
            # Timeout añadido para la petición a Discord
            r = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
            r.raise_for_status() # Lanza error si Discord responde mal
            print(f"Enviado: {art['title'][:30]}... OK")
        except Exception as e:
            print(f"Fallo al enviar a Discord: {e}")

if __name__ == "__main__":
    print("Iniciando bot de noticias...")
    noticias = obtener_noticias()
    
    if noticias:
        print(f"Se encontraron {len(noticias)} noticias en total.")
        enviar_a_discord(noticias)
    else:
        print("No se pudo obtener ninguna noticia de las fuentes.")
