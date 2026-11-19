import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(title="AmoMusica YouTube Audio Stream Microservice")

# Permite chamadas CORS de qualquer origem (inclusive Hostinger)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "AmoMusica YouTube Audio Stream Service",
        "version": "1.1"
    }

def get_ydl_options():
    return {
        'format': 'bestaudio[ext=m4a]/bestaudio/18/b/ba',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'tv_embedded']
            }
        }
    }

@app.get("/audio")
def get_audio_url(v: str = Query(..., description="YouTube Video ID (11 chars)")):
    """Retorna o link direto do fluxo de áudio do YouTube compatível com o AmoMúsica."""
    v = v.strip()
    if len(v) != 11:
        raise HTTPException(status_code=400, detail="Invalid YouTube Video ID format.")

    ydl_opts = get_ydl_options()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={v}", download=False)
            audio_url = info.get('url')
            if not audio_url:
                raise HTTPException(status_code=404, detail="Audio stream not found.")

            return {
                "sucesso": True,
                "video_id": v,
                "titulo": info.get("title"),
                "duracao": info.get("duration"),
                "audio_url": audio_url
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair áudio: {str(e)}")

@app.get("/stream")
def stream_audio(v: str = Query(..., description="YouTube Video ID")):
    """Redireciona diretamente para o streaming do Google Video."""
    v = v.strip()
    if len(v) != 11:
        raise HTTPException(status_code=400, detail="Invalid YouTube Video ID format.")

    ydl_opts = get_ydl_options()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={v}", download=False)
            audio_url = info.get('url')
            if not audio_url:
                raise HTTPException(status_code=404, detail="Audio stream not found.")

            return RedirectResponse(url=audio_url, status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair áudio: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
