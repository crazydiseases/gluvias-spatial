import os
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
    return {
        "error": "File not found",
        "attempted_path": str(HTML_PATH),
        "current_working_dir": os.getcwd()
    }
