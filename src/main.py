from fastapi import FastAPI
import uvicorn
from src.api.bot_api import router as bot_router
from src.api.vpn_api import router as vpn_router

app = FastAPI(
    title="Argent Core API",
    description="heart of Argent-service",
    version="0.1.0"
)

app.include_router(bot_router)
app.include_router(vpn_router)

@app.get("/")
async def root():
    return {
        "project": "Argent Core",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)