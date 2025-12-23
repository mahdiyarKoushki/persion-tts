import asyncio
import edge_tts
import tempfile
import os
from aiohttp import TCPConnector
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice: str = "fa-IR-FaridNeural"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def speak(text: str, voice: str = "fa-IR-FaridNeural") -> str:
    connector = TCPConnector(ssl=False)

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