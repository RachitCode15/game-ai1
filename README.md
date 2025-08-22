
# Gaming AI Assistant

## Overview
AI assistant that analyzes game clips and gives improvement tips using Gemini API.

## Tech Stack
- Backend: Python (FastAPI)
- Frontend: HTML/CSS/JS
- Database: SQLite

## Setup
```bash
# Clone repo
cd gaming-ai-assistant

# Install deps
pip install fastapi uvicorn requests

# Set Gemini API key
export GEMINI_API_KEY=AIzaSyBhnKg9ITowPzB0iaexjI91bJ7Rt-4D-ug

# Run backend
uvicorn app.main:app --reload

# Open frontend
open frontend/index.html
```

## Example Usage
- Upload a clip via UI
- AI analyzes and suggests tips

## Scalability Improvements
- Replace dummy analyzer with ML/computer vision (OpenCV, PyTorch)
- Use PostgreSQL for scaling DB
- Add user authentication
- Deploy on cloud (Render/Heroku)
- Add real-time chat interface
"""