import uvicorn
import sys
from pathlib import Path

# Add parent directory to path to ensure imports work
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("🚀 Starting ConvoxAI Development Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("\n⏳ Loading models and starting server...\n")
    
    uvicorn.run(
        "convoxai.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_dir / "convoxai")],
        log_level="info"
    )
