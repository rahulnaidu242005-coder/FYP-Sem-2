#python
import datetime
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from pydantic import BaseModel
import sys
from typing import Dict, Any, Optional

# Add parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import get_chatbot_response, analyze_incident

resources_dir = Path("C:/RP Y3S2/C300_Project/FYP-Sem-2/UI2/src")

app = FastAPI()

# use absolute path so running from another cwd still works
app.mount("/static", StaticFiles(directory=str(resources_dir)), name="static")
templates = Jinja2Templates(directory=str(resources_dir))

# Request models
class ChatQuery(BaseModel):
    question: str
    level: str = "L1"
    incident: Optional[Dict[str, Any]] = None  # Optional incident data for incident analysis

class IncidentQuery(BaseModel):
    incident: Dict[str, Any]
    level: str = "L1"

# In-memory storage for chat sessions and their levels
chat_levels = {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = resources_dir / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(str(favicon_path))
    raise HTTPException(status_code=404)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat(query: ChatQuery):
    """API endpoint for chatbot queries with optional incident data for incident analysis"""
    try:
        # Pass incident data if provided
        response = get_chatbot_response(
            query.question, 
            query.level,
            incident_data=query.incident
        )
        return JSONResponse({"success": True, "response": response})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/chat-session")
async def create_chat_session():
    """Create a new chat session and initialize level"""
    import uuid
    session_id = str(uuid.uuid4())
    chat_levels[session_id] = "L1"  # Default level
    return JSONResponse({"session_id": session_id, "level": "L1"})

@app.get("/api/chat-level/{session_id}")
async def get_chat_level(session_id: str):
    """Get current level for a chat session"""
    level = chat_levels.get(session_id, "L1")
    return JSONResponse({"session_id": session_id, "level": level})

@app.post("/api/analyze-incident")
async def analyze_incident_endpoint(query: IncidentQuery):
    """API endpoint for incident analysis at different tiers (L1, L2, L3)"""
    try:
        # Validate tier level
        tier = query.level.upper()
        if tier not in ["L1", "L2", "L3"]:
            return JSONResponse(
                {"success": False, "error": f"Invalid tier level '{query.level}'. Must be L1, L2, or L3."},
                status_code=400
            )
        
        # Analyze incident
        analysis = analyze_incident(query.incident, tier)
        
        return JSONResponse({
            "success": True,
            "incident_id": query.incident.get("id", "Unknown"),
            "tier": tier,
            "analysis": analysis
        })
    except Exception as e:
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )

@app.post("/api/batch-analyze-incidents")
async def batch_analyze_incidents(queries: list[IncidentQuery]):
    """Batch analyze multiple incidents"""
    results = []
    
    for query in queries:
        try:
            tier = query.level.upper()
            if tier not in ["L1", "L2", "L3"]:
                results.append({
                    "incident_id": query.incident.get("id", "Unknown"),
                    "success": False,
                    "error": f"Invalid tier level '{query.level}'"
                })
                continue
            
            analysis = analyze_incident(query.incident, tier)
            results.append({
                "incident_id": query.incident.get("id", "Unknown"),
                "tier": tier,
                "success": True,
                "analysis": analysis
            })
        except Exception as e:
            results.append({
                "incident_id": query.incident.get("id", "Unknown"),
                "success": False,
                "error": str(e)
            })
    
    return JSONResponse({
        "total": len(queries),
        "successful": sum(1 for r in results if r.get("success")),
        "results": results
    })