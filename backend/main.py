from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, session, health, debug
from app.config import settings
from app.middleware.error_handler import setup_error_handlers
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kristal Agent PoC API",
    description="Backend API for Kristal Agent Proof of Concept",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Root route
@app.get("/")
async def root():
    return {
        "message": "Kristal Agent PoC API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
        "status": "running"
    }

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(session.router, prefix="/api", tags=["session"])
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(debug.router, prefix="/api", tags=["debug"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Kristal Agent PoC API")
    logger.info(f"Agent API URL: {settings.AGENT_API_URL}")
    cors_list = settings.get_cors_origins_list()
    logger.info(f"CORS Origins: {cors_list}")
    logger.info(f"CORS Origins count: {len(cors_list)}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Kristal Agent PoC API")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

