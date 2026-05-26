import feedparser
from deep_translator import GoogleTranslator
import json
import os

# 1. Definir los feeds y categorías
FEEDS = {
    "Artículos científicos": [
        "https://www.nature.com/tpj.rss",
        "https://www.frontiersin.org/journals/pharmacology/rss"
    ],
    "Webs médicas": [
        "https://www.pharmgkb.org/rss" 
    ]
}

translator = GoogleTranslator(source='auto', target='es')
feed_data = []

# 2. Parsear y procesar
for category, urls in FEEDS.items():
    for url in urls:
        parsed_feed = feedparser.parse(url)
        # Limitamos a los 5 más recientes por feed para no saturar
        for entry in parsed_feed.entries[:5]:
            try:
                title_es = translator.translate(entry.title)
                # Extraemos la descripción/abstract si existe
                description = entry.description if hasattr(entry, 'description') else "Sin abstract disponible."
                
                feed_data.append({
                    "title": title_es,
                    "original_title": entry.title,
                    "link": entry.link,
                    "category": category,
                    "raw_text": description
                })
            except Exception as e:
                print(f"Error procesando {entry.title}: {e}")

# 3. Guardar en JSON
with open('feed_data.json', 'w', encoding='utf-8') as f:
    json.dump(feed_data, f, ensure_ascii=False, indent=2)
print("Feed actualizado correctamente.")
