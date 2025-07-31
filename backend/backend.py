# backend.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can narrow this to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnrichmentRequest(BaseModel):
    message: str


@app.post("/enrich-profile")
async def enrich_profile(payload: EnrichmentRequest):
    try:
        message = payload.message
        # Dummy response (you can plug LLM or enrichment logic here)
        return {
            "summary": f"We received: '{message}' and analyzed it.",
            "topics": ["Memory", "Holocaust education", "WWII resistance"],
        }
    except Exception as e:
        return {"error": str(e)}
