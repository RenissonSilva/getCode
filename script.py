import os
import time
import re
import pyperclip
import pytchat
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()
youtube_url = os.getenv("YOUTUBE_LIVE_URL")

def extrair_video_id(url):
    query = parse_qs(urlparse(url).query)
    return query["v"][0] if "v" in query else None

video_id = extrair_video_id(youtube_url)

if not video_id:
    print("❌ ID do vídeo não encontrado. Verifique sua URL no .env")
    exit()

def extrair_codigo(texto):
    padrao = r"[A-Z0-9]{4,5}-[A-Z0-9]{4,5}-[A-Z0-9]{4,5}"
    match = re.search(padrao, texto, re.IGNORECASE)
    return match.group() if match else None

print(f"🔍 Monitorando chat da live: {youtube_url}")
chat = pytchat.create(video_id=video_id)

while chat.is_alive():
    for c in chat.get().sync_items():
        codigo = extrair_codigo(c.message)

        if codigo:
            print(f"✅ Código encontrado no chat: {codigo}")
            pyperclip.copy(codigo)
            os.system("paplay /usr/share/sounds/freedesktop/stereo/message.oga")
    time.sleep(1)
