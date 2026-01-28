import datetime
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from pydantic import BaseModel
import os, logging, json, tempfile
from lib.Chat import get_chatbot_response
from lib.API_Modules import LoggerCustom

# Setup logging FIRST
LoggerCustom("app.log").setup_logging()
logger = logging.getLogger("fastapiserver")

# Add parent directory to path so we can import main
# Go up to project root, then into src/
base_dir = Path(__file__).resolve().parent.parent  # = /var/home/staygold/.../
resources_dir = base_dir / "src"  # Correct: project_root/src/ ✅

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
    level: str = "L1"  # Default level
    session_id: str = None  # Optional session ID


# In-memory storage for chat sessions and their levels
chat_levels = {}
# In-memory storage for uploaded JSON data per session
session_data = {}


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
    import uuid
    request_id = str(uuid.uuid4())[:8]  # Short ID for logging

    try:
        logger.info(f"[{request_id}] Received chat request: {query.question[:100]}...")

        # # Set uploaded data context if session exists
        # if query.session_id and query.session_id in session_data:
        #     uploaded_data = session_data[query.session_id]
        #     if uploaded_data:
        #         set_uploaded_data(query.session_id, uploaded_data["data"])

        logger.info(f"[{request_id}] Calling get_chatbot_response...")
        response_obj = get_chatbot_response(query.question, query.level, query.session_id)

        # Extract content (handles AIMessage, str, etc.)
        if hasattr(response_obj, 'content'):
            response_text = response_obj.content
        else:
            response_text = str(response_obj)

        logger.info(f"[{request_id}] Response generated ({len(response_text)} chars)")
        logger.info(f"[{request_id}] Response content: {response_text[:200]}...")

        # Check if response is the unhelpful one
        if "unable to provide strategies" in response_text.lower() or "provide more context" in response_text.lower():
            logger.warning(f"[{request_id}] Detected unhelpful response - this might be a prompt issue")

        return JSONResponse({"success": True, "response": response_text, "request_id": request_id})

    except Exception as e:
        logger.error(f"[{request_id}] Chat error: {str(e)}")
        return JSONResponse({"success": False, "error": str(e), "request_id": request_id}, status_code=500)


@app.post("/api/load-example-data")
async def load_example_data(session_id: str):
    """Load the example.json file for testing purposes"""
    try:
        example_file_path = base_dir / "example.json"
        if not example_file_path.exists():
            return JSONResponse(
                {"success": False, "error": "example.json file not found"},
                status_code=404
            )

        # Read and parse the example JSON file
        with open(example_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Store data in session
        session_data[session_id] = {
            "filename": "example.json",
            "data": json_data
        }
        # Update the chat module with the new data
        set_uploaded_data(session_id, json_data)

        logger.info(f"Example data loaded for session: {session_id}")
        return JSONResponse({
            "success": True,
            "message": "Example data loaded successfully",
            "filename": "example.json"
        })

    except Exception as e:
        logger.error(f"Error loading example data: {str(e)}")
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )


@app.post("/api/upload-file")
async def upload_file(session_id: str = None, file: UploadFile = File(...)):
    """Handle JSON file uploads"""
    try:
        # Validate file type
        if not file.filename.endswith('.json'):
            return JSONResponse(
                {"success": False, "error": "Only .json files are supported"},
                status_code=400
            )

        # Read and parse JSON content
        content = await file.read()
        json_data = json.loads(content.decode('utf-8'))

        # Store data in session if session_id provided
        if session_id:
            session_data[session_id] = {
                "filename": file.filename,
                "data": json_data
            }
            # Update the chat module with the new data
            set_uploaded_data(session_id, json_data)

        logger.info(f"File uploaded successfully: {file.filename}, Session: {session_id}")
        return JSONResponse({
            "success": True,
            "message": f"File '{file.filename}' uploaded successfully",
            "filename": file.filename
        })

    except json.JSONDecodeError:
        return JSONResponse(
            {"success": False, "error": "Invalid JSON file"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )


@app.post("/api/chat-session")
async def create_chat_session():
    """Create a new chat session and initialize level"""
    import uuid
    session_id = str(uuid.uuid4())
    chat_levels[session_id] = "L1"  # Default level
    session_data[session_id] = None  # Initialize empty data
    return JSONResponse({"session_id": session_id, "level": "L1"})