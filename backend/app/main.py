from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import sms
from app.core.database import init_db
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized")
    if settings.ngrok_url:
        print(f"Ngrok URL: {settings.ngrok_url}")
    print(f"Server running on {settings.host}:{settings.port}")

# Include routers
app.include_router(sms.router, prefix="/api/v1", tags=["sms"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to SmartSense Inbox API",
        "version": settings.api_version,
        "endpoints": {
            "ingest": "POST /api/v1/sms",
            "messages": "GET /api/v1/messages",
            "digest": "GET /api/v1/digest",
            "query": "POST /api/v1/query",
            "upload": "POST /api/v1/upload-csv"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}