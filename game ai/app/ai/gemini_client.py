import os
import requests
from typing import Dict


class GeminiClient:
    def __init__(self):
        # Prefer .env but fall back to env var
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Newer Gemini models use 1.5; old "gemini-pro" may be deprecated
        self.base_url = (
        os.getenv("GEMINI_BASE_URL")
            or "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        )


    def get_tips(self, analysis: Dict) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not set")


        prompt = (
            "You are a professional gaming coach AI."
        
            f"Based on this gameplay analysis: {analysis},"
        
            "give the player exactly 3 short, practical, numbered tips to improve."
        
            "Keep each tip under 20 words."
        )
        resp = requests.post(
            f"{self.base_url}?key={self.api_key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=20,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No tips available.")
        )