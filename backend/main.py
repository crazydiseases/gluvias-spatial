import os
import httpx
import urllib.parse
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
        "User-Agent": "GluviasSpatialConsole/2.0 (stuttassociates@internal.com)"
    }
    
    # Strictly URL-encode the string parameters to handle spaces like "st day" safely
    safe_query = urllib.parse.quote(q.strip())
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={safe_query}&limit=1"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
