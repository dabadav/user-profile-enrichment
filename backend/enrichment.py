import json
from typing import Dict, List, Optional, Union

import requests
from pydantic import BaseModel


class UserProfile(BaseModel):
    age: Optional[int] = None
    region: Optional[str] = ""
    topics: Optional[List[str]] = []
    knowledge: Optional[str] = ""
    connection: Optional[str] = ""

    # Explicit structured intent
    intent: Optional[str] = ""
    intent_entities: Optional[Dict[str, Union[str, None]]] = {}


# Define the schema for user profile extraction
def build_extraction_prompt(conversation: List[dict], schema_model: BaseModel):
    schema = "\n".join(f"- {k}: {v}" for k, v in schema_model.__annotations__.items())
    dialogue = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}" for m in conversation
    )

    return f"""
You are an assistant that extracts a user profile and their search intent from a conversation.

Return a JSON object matching the following schema:
{schema}

- `intent` is the inferred user goal such as "search_person", "learn_topic", etc.
- `intent_entities` is a dictionary with keys like:
  - person_name
  - location
  - datetime
  - relation
  - topic

Be concise. Only include fields with meaningful values.

Conversation:
{dialogue}

JSON:
"""


# Use Ollama to generate completion
def call_ollama(prompt: str, model: str = "qwen2.5") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    return response.json()["response"]


# Extract user profile from conversation using LLM
def extract_user_profile(conversation: list[dict]) -> UserProfile:
    prompt = build_extraction_prompt(conversation, UserProfile)
    raw_output = call_ollama(prompt)

    try:
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        extracted_json = raw_output[start:end]
        parsed = json.loads(extracted_json)
        return UserProfile(**parsed)
    except Exception as e:
        raise ValueError(
            f"Failed to parse user profile: {e}\n\nRaw output:\n{raw_output}"
        )
