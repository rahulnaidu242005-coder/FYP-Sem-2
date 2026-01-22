"""
FYP FastAPI Server - Fixed reload
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "lib.server:app",       # Import string: "module:app_object"
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
