import asyncio
import edge_tts
import tempfile
import os
from enum import Enum
from aiohttp import TCPConnector
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Voice(str, Enum):
    farid_persian_female = "fa-IR-FaridNeural"
    aria_english_female = "en-US-AriaNeural"
    zira_english_female = "en-US-ZiraNeural"
    david_english_male = "en-US-DavidNeural"
    mark_english_male = "en-US-MarkNeural"
    lori_persian_female = "fa-IR-LoriNeural"
    golnaz_persian_female = "fa-IR-GolnazNeural"
    dilara_turkish_female = "tr-TR-DilaraNeural"
    # Add more as needed

class TTSRequest(BaseModel):
    text: str
    voice: Voice = Voice.farid_persian_female

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def speak(text: str, voice: str = "fa-IR-FaridNeural") -> str:
    connector = TCPConnector()

    communicate = edge_tts.Communicate(
        text,
        voice,
        connector=connector
    )
    filename = tempfile.mktemp(suffix=".mp3")
    await communicate.save(filename)
    return filename

@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    try:
        filename = await speak(request.text, request.voice)
        return FileResponse(path=filename, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)