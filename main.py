import os
import uvicorn
from backend.main import app

if __name__ == "__main__":
    # Pull the dynamic port from Railway's environment, defaulting to 8000 locally
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
