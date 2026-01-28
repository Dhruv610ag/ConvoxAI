"""
ConvoxAI - Main Entry Point
Run the FastAPI application server
"""
import uvicorn
from api.app import app

def main():
    """
    Start the ConvoxAI FastAPI server
    """
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
