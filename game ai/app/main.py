# Project: Gaming AI Assistant
# ========================================
# Purpose: Analyze game clips + provide AI tips using Gemini API.
# Tech: Python (FastAPI backend), HTML/CSS/JS frontend, SQLite DB.

# ---------------------------
# FILE: app/__init__.py
# ---------------------------
# (empty file to mark this as a Python package)

# ---------------------------
# FILE: app/main.py
# ---------------------------
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analyzers.clip_analyzer import analyze_clip
from app.analyzers.clip_analyzer import analyze_clip
from app.ai.gemini_client import GeminiClient
from app.db.database import init_db, save_analysis
import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now the relative imports will work
from app.analyzers.clip_analyzer import analyze_clip
...

app = FastAPI(title="Gaming AI Assistant")

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
init_db()

# Gemini client
client = GeminiClient()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile, user_id: str = Form(...)):
    """Upload game clip, run analysis, and get AI tips."""
    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")

    clip_path = os.path.join("uploads", file.filename)
    try:
        with open(clip_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Step 1: Local analysis (e.g., motion detection, stats)
    local_result = analyze_clip(clip_path)

    # Step 2: Get AI-generated tips from Gemini (with safe fallback)
    tips = ""
    try:
        tips = client.get_tips(local_result)
    except Exception as e:
        tips = (
            "Could not reach Gemini. Fallback tips: practice recoil control in TDM, "
            "use cover between peeks, and pre-aim common angles."
        )

    # Step 3: Save to DB
    try:
        save_analysis(user_id, local_result, tips)
    except Exception as e:
        # Don't fail the request if DB write fails; just return a warning
        return {"analysis": local_result, "tips": tips, "warning": f"DB save failed: {e}", "filename": file.filename, "filepath": clip_path}

    return {"analysis": local_result, "tips": tips, "filename": file.filename, "filepath": clip_path}