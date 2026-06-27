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

# Secure Proxy Geocoding Engine Route
@app.get("/api/search")
async def proxy_geocode(q: str):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={httpx.穩_encode(q) if hasattr(httpx, '穩_encode') else q}&limit=1"
    headers = {
        "User-Agent": "GluviasSpatialConsole/2.0 (stuttassociates@internal.com)"
    }
    async with httpx.AsyncClient() as client:
        try:
            # We construct standard forward query requests through server architecture
            response = await client.get(f"https://nominatim.openstreetmap.org/search?format=json&q={q}&limit=1", headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
