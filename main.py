import os
import httpx
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

app = FastAPI(title="GLUVIAS // SPATIAL CONSOLE")

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "index.html"

@app.get("/")
async def serve_workspace():
    if HTML_PATH.exists():
        return FileResponse(str(HTML_PATH))
    return {"error": "File not found"}

@app.get("/api/search")
async def proxy_geocode(q: str):
    headers = {
        "User-Agent": "GluviasSpatialConsoleEngine/9.0 (stuttassociates@internal.com)"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "format": "json",
                    "q": q.strip(),
                    "limit": 1,
                    "addressdetails": 1
                },
                headers=headers
            )
            
            # BYPASS ALL SERIALIZATION: Grab the raw string/bytes directly from the source
            # and send them untouched with a strict JSON content type header.
            return Response(
                content=response.text, 
                media_type="application/json",
                status_code=response.status_code
            )
            
        except Exception as e:
            return Response(
                content=f'{{"error": "{str(e)}"}}', 
                media_type="application/json", 
                status_code=500
            )
