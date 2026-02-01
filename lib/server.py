import datetime
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from pydantic import BaseModel
import os, logging
from lib.Chat import get_chatbot_response
from lib.API_Modules import LoggerCustom

# Setup logging FIRST
LoggerCustom("app.log").setup_logging()
logger = logging.getLogger("fastapiserver")

# Add parent directory to path so we can import main
# Go up to project root, then into src/
base_dir = Path(__file__).resolve().parent.parent  # = /var/home/staygold/.../
resources_dir = base_dir / "src"                   # Correct: project_root/src/ ✅


# Add debug print (remove later)
logger.info(f"Static dir: {resources_dir / 'static'}")
logger.info(f"Templates dir: {resources_dir / 'templates'}")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=str(resources_dir / "static")),
    name="static",
)
templates = Jinja2Templates(directory=str(resources_dir / "templates"))


# Request model for chatbot queries
class ChatQuery(BaseModel):
    question: str

# In-memory storage for chat sessions and their levels
chat_levels = {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = str(resources_dir / "static" / "favicon.ico")  # src/static/favicon.ico
    if os.path.isfile(favicon_path):
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat(query: ChatQuery):
    try:
        response_obj = get_chatbot_response(query.question)
        # Extract content (handles AIMessage, str, etc.)
        if hasattr(response_obj, 'content'):
            response_text = response_obj.content
        else:
            response_text = str(response_obj)
        logger.info(str(response_text))
        logger.info(f"Chat response ({len(response_text)} chars): {response_text[:200]}...")
        return JSONResponse({"success": True, "response": response_text})
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/chat-session")
async def create_chat_session():
    """Create a new chat session and initialize level"""
    import uuid
    session_id = str(uuid.uuid4())
    chat_levels[session_id] = "L1"  # Default level
    return JSONResponse({"session_id": session_id, "level": "L1"})