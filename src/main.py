from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from src.loader import _vpn_client
from src.api.bot_api import router as bot_router
from src.api.vpn_api import router as vpn_router
from src.api.pay_api import router as pay_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting Argent-core")
    
    yield

    print("stopping Argent-core")
    await _vpn_client.close()
    print("succes client closing")

app = FastAPI(
    title="Argent Core API",
    description="heart of Argent-service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(bot_router)
app.include_router(vpn_router)
app.include_router(pay_router)

@app.get("/")
async def root():
    return {
        "project": "Argent Core",
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)