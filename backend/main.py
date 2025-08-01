# backend.py
from enum import Enum
from typing import Any, List, Union
from uuid import UUID

from enrichment import UserProfile, extract_user_profile
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can narrow this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PayloadType(str, Enum):
    survey = "survey"
    message = "message"


class MessagePayload(BaseModel):
    message: str


class SurveyPayload(BaseModel):
    age: int
    region: str
    topics: List[str]
    knowledge: str
    personal_connection: str


class UnifiedPayload(BaseModel):
    type: PayloadType  # "message" or "survey"
    payload: dict[str, Any]


user_store: dict[str, UserProfile] = {}


def merge_profiles(existing: UserProfile, updates: dict) -> UserProfile:
    updated = existing.model_dump()
    for k, v in updates.items():
        if v and updated.get(k) in (None, "", [], {}, 0):
            updated[k] = v
    return UserProfile(**updated)


@app.post("/enrich-profile")
async def enrich_profile(request: UnifiedPayload):
    user: UserProfile = None

    if request.type == "message":
        # Enrich user profile from message
        user_msg = request.payload["message"]
        user = extract_user_profile([{"role": "user", "content": user_msg}])

        # Merge with existing profile (if any)
        existing = user_store.get("user1")
        merged = merge_profiles(existing, user.model_dump()) if existing else user
        user_store["user1"] = merged

        # Process message...
        return {"response": f"Go on ..."}

    if request.type == "survey":
        user = UserProfile(**request.payload)
        user_store["user1"] = user
        topics = ", ".join(user.topics or [])

        # Personalized welcome message
        message = (
            f"Thanks for your input! I see you're from {user.region}, "
            f"interested in {topics}, and you have {user.knowledge.lower()}. "
            f"{'It’s powerful that you have a personal family connection to WWII.' if user.connection == 'Yes' else ''} "
            f"What are you most curious about next?"
        )
        return {"response": message.strip()}

    return {"response": "Invalid type."}


@app.get("/user-profile")
async def get_user_profile():
    user = user_store.get("user1")
    if user:
        return user.model_dump()
    return {"error": "User profile not found."}
