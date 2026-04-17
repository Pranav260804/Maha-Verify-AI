from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Import backend modules
from backend.config import settings
from backend.auth import router as auth_router, verify_token
from backend.database import init_db
from backend.routes import document, rera, history

# Initialize FastAPI app
app = FastAPI(
    title="Maha Verify AI",
    description="Real Estate Document Auditor with AI & RERA Integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(document.router, prefix="/api", tags=["document"])
app.include_router(rera.router, prefix="/api", tags=["rera"])
app.include_router(history.router, prefix="/api", tags=["history"])

# Serve static files (HTML, CSS, JS)
static_dir = Path(__file__).parent.parent

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve login page or dashboard based on auth status"""
    file_path = static_dir / "login.html"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve main dashboard (requires authentication)"""
    file_path = static_dir / "index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/style.css", response_class=FileResponse)
async def serve_css():
    """Serve style.css"""
    file_path = static_dir / "style.css"
    return FileResponse(file_path, media_type="text/css")

@app.get("/app.js", response_class=FileResponse)
async def serve_js():
    """Serve app.js"""
    file_path = static_dir / "app.js"
    return FileResponse(file_path, media_type="application/javascript")

@app.get("/login.html", response_class=FileResponse)
async def serve_login_html():
    """Serve login.html"""
    file_path = static_dir / "login.html"
    return FileResponse(file_path, media_type="text/html")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Serve login page"""
    file_path = static_dir / "login.html"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/favicon.ico")
async def favicon():
    """Return a simple favicon (404 is fine, won't break anything)"""
    return {"detail": "Not Found"}, 404

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": "Maha Verify AI"}

@app.get("/api/user/profile")
async def get_user_profile(token: str = Depends(verify_token)):
    """Get current user profile"""
    return {
        "email": token.get("email"),
        "name": token.get("name"),
        "picture": token.get("picture")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
