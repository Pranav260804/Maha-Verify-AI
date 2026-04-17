#!/usr/bin/env python3
"""
Maha Verify AI - Quick Start Script
Initializes the project and starts the server
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent
UPLOAD_DIR = PROJECT_ROOT / "uploads"
VENV_DIR = PROJECT_ROOT / "venv"


def check_python_version():
    """Verify Python 3.8+"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ required")
        sys.exit(1)
    logger.info(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def check_virtual_env():
    """Verify virtual environment is active"""
    if not os.getenv('VIRTUAL_ENV'):
        logger.warning("⚠️  Virtual environment not active. Run: python -m venv venv")
        if sys.platform == "win32":
            logger.warning("⚠️  Then: venv\\Scripts\\activate")
        else:
            logger.warning("⚠️  Then: source venv/bin/activate")


def create_directories():
    """Create necessary directories"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    logger.info("✓ Directories created")


def install_dependencies():
    """Install Python packages"""
    logger.info("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], cwd=PROJECT_ROOT)
    logger.info("✓ Dependencies installed")


def setup_env():
    """Setup environment configuration"""
    env_file = PROJECT_ROOT / ".env"
    env_example = PROJECT_ROOT / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            logger.info("⚠️  Created .env file - Please configure API keys!")
        else:
            logger.warning("⚠️  .env file not found - Configure manually")
    else:
        logger.info("✓ .env file exists")


def initialize_database():
    """Initialize database"""
    try:
        from backend.database import init_db
        init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")


def start_server():
    """Start FastAPI server"""
    logger.info("\n" + "="*60)
    logger.info("🚀 Starting Maha Verify AI Server")
    logger.info("="*60)
    logger.info("📍 Frontend: http://localhost:8000")
    logger.info("📍 API Docs: http://localhost:8000/docs")
    logger.info("📍 Health: http://localhost:8000/health")
    logger.info("="*60 + "\n")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--reload",
        "--port", "8000"
    ], cwd=PROJECT_ROOT)


def main():
    """Run setup and start server"""
    logger.info("🔧 Maha Verify AI - Setup\n")
    
    check_python_version()
    check_virtual_env()
    create_directories()
    setup_env()
    install_dependencies()
    
    try:
        initialize_database()
    except ImportError:
        logger.warning("⚠️  Skipping database init (config not yet set)")
    
    logger.info("\n✅ Setup complete!\n")
    
    # Ask before starting server
    response = input("Start server now? (y/n): ").strip().lower()
    if response == 'y':
        start_server()


if __name__ == "__main__":
    main()
