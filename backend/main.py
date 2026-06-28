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
        "User-Agent": "GluviasSpatialConsole/3.0 (stuttassociates@internal.com)"
    }
    
    clean_q = q.strip()
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Primary Sweep: Look for exact match
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"format": "json", "q": clean_q, "limit": 1, "addressdetails": 1},
                headers=headers
            )
            data = response.json()
            
            # Fallback Sweep: If empty array, append regional context anchor to force a valid node layout
            if not data or len(data) == 0:
                fallback_q = f"{clean_q}, Cornwall"
                response = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"format": "json", "q": fallback_q, "limit": 1, "addressdetails": 1},
                    headers=headers
                )
                data = response.json()
                
            return data
        except Exception as e:
            return {"error": str(e)}
