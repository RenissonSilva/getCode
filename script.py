import os
import time
import re
import pyperclip
import pyautogui
import pytchat
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()
youtube_url = os.getenv("YOUTUBE_LIVE_URL")
auto_colar_enviar = os.getenv("AUTO_COLAR_ENVIAR", "false").lower() == "true"

def extrair_video_id(url):
    query = parse_qs(urlparse(url).query)
    return query["v"][0] if "v" in query else None

video_id = extrair_video_id(youtube_url)

if not video_id:
    print("❌ ID do vídeo não encontrado. Verifique sua URL no .env")
    exit()

def extrair_codigo(texto):
    padrao1 = r"\b[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\b"
    padrao2 = r"\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b"

    match = re.search(padrao2, texto, re.IGNORECASE)
    if match and "face" not in match.group().lower():
        return match.group()

    match = re.search(padrao1, texto, re.IGNORECASE)
    if match and "face" not in match.group().lower():
        return match.group()

    return None

def colar_e_enviar():
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

print(f"🔍 Monitorando chat da live: {youtube_url}")
chat = pytchat.create(video_id=video_id)

while chat.is_alive():
    for c in chat.get().sync_items():
        codigo = extrair_codigo(c.message)

        if codigo:
            print(f"✅ Código encontrado no chat: {codigo}")
            pyperclip.copy(codigo)
            os.system("paplay /usr/share/sounds/freedesktop/stereo/message.oga")
            if auto_colar_enviar:
                colar_e_enviar()
    time.sleep(1)
