import asyncio
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse

from app.routes.health import router as health_router
from app.routes.chat import router as chat_router
from app.routes.sync import router as sync_router
from app.routes.action import router as action_router
from app.services.report_cleanup_service import cleanup_expired_reports

# Ensure reports directory exists before mounting
REPORTS_DIR = Path("app/static/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Ensure static directory exists
STATIC_DIR = Path("app/static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="TRMS RAG Server",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for reports
app.mount(
    "/reports",
    StaticFiles(directory=str(REPORTS_DIR)),
    name="reports"
)

app.include_router(health_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(sync_router, prefix="/api")
app.include_router(action_router, prefix="/api")


@app.get("/")
async def serve_chatbot():
    """Serve the chatbot frontend at root URL."""
    return FileResponse("app/static/chatbot.html", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/chatbot")
async def serve_chatbot_alt():
    """Alternative chatbot URL."""
    return FileResponse("app/static/chatbot.html", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.on_event("startup")
async def start_report_cleanup_task():
    """Initialize report cleanup on startup and run every 10 minutes."""
    print("[Startup] Initializing report cleanup service...")
    
    # Run initial cleanup
    try:
        deleted = cleanup_expired_reports()
        print(f"[Startup] Initial cleanup completed. Deleted {deleted} expired report files.")
    except Exception as e:
        print(f"[Startup] Initial cleanup error (non-critical): {e}")
    
    # Start background cleanup loop
    async def cleanup_loop():
        while True:
            await asyncio.sleep(600)  # 10 minutes
            try:
                deleted = cleanup_expired_reports()
                if deleted > 0:
                    print(f"[Cleanup] Deleted {deleted} expired report files")
            except Exception as e:
                print(f"[Cleanup] Error during scheduled cleanup: {e}")
    
    # Create background task (non-blocking)
    asyncio.create_task(cleanup_loop())
    print("[Startup] Report cleanup background task started (runs every 10 minutes)")