# backend.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can narrow this to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/enrich-profile")
async def enrich_profile(req: Request):
    body = await req.json()
    message = body.get("message", "")

    # Placeholder enrichment (replace with real LLM or logic)
    suggestions = {
        "summary": f"Enriched insight from: {message}",
        "topics": ["Memory", "Nazi propaganda", "Survivor stories"]
    }

    return suggestions