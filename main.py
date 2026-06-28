import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIXED ROOT HANDLER: Serves your index.html file whenever someone goes to the app's address
@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.get("/api/search")
async def search_location(q: str = Query(...)):
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&addressdetails=1&limit=1"
    headers = {"User-Agent": "GluviasSpatialConsole/2.0 (railway; contact: admin@app)"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return JSONResponse(status_code=response.status_code, content={"error": "Directory dropped trace"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/boundaries")
async def get_property_boundaries(bbox: str = Query(...)):
    # Direct pipeline tunnel to HM Land Registry's ArcGIS Open Server asset node
    arcgis_url = "https://services.arcgis.com/hkgg97S808S37IuI/ArcGIS/rest/services/INSPIRE_Index_Polygons_Open/FeatureServer/0/query"
    
    params = {
        "f": "geojson",
        "geometry": bbox,
        "geometryType": "esriGeometryEnvelope",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outSR": "4326",
        "returnGeometry": "true",
        "outFields": "INSPIREID"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(arcgis_url, params=params, timeout=15.0)
            if response.status_code == 200:
                return response.json()
            return JSONResponse(status_code=response.status_code, content={"error": "HMLR Server dropped proxy stream"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
        
