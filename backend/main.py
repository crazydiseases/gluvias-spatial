import os
import httpx
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="GLUVIAS // SPATIAL CONSOLE")

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = BASE_DIR / "index.html"

@app.get("/")
async def serve_workspace():
    if HTML_PATH.exists():
        return FileResponse(str(HTML_PATH))
    return {"error": "File not found"}

@app.get("/api/search")
async def proxy_geocode(q: str):
    headers = {
        "User-Agent": "GluviasSpatialConsoleApp/4.0 (internal-contact@stuttassociates.internal)"
    }
    
    # Passing query arguments using a dictionary mapping guarantees proper percent-encoding format
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
            return response.json()
        except Exception as e:
            return {"error": str(e)}
