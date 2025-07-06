import os
import sys
import uuid
from typing import Dict, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app first, so health endpoint works even if imports fail
app = FastAPI(
    title="Real Estate Poster Template Agent API",
    description="API for creating customized real estate poster templates",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define template image placeholder URLs
TEMPLATE_PLACEHOLDER_IMAGES = {
    1: "https://example.com/templates/modern_home_preview.jpg",
    2: "https://example.com/templates/house_agent_preview.jpg",
    3: "https://example.com/templates/best_home_preview.jpg",
}

# Session storage
sessions: Dict[str, AgentState] = {}

@app.get("/templates")
async def templates_endpoint():
    """Get information about available templates"""
    return {"templates": : "Hi"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
