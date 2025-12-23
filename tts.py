import asyncio
import edge_tts
from playsound import playsound
import certifi
import ssl
from aiohttp import TCPConnector

async def speak(text, voice="fa-IR-FaridNeural"):
    # SSL context برای حل مشکل certificate
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = TCPConnector(ssl=ssl_context)
    
    communicate = edge_tts.Communicate(
        text,
        voice,
        connector=connector
    )
    await communicate.save("output.mp3")

# متن تست
text = "سلام من مهدی کوشکی هستم خالق این چت بات"

# اجرا
asyncio.run(speak(text))

# پخش صدا
playsound("output.mp3")