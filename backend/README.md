
## User profile enrichment based on LLM

Example from LangMem https://langchain-ai.github.io/langmem/guides/manage_user_profile/

```python
from langmem import create_memory_manager
from pydantic import BaseModel

# Memory manager initialization

# Define profile structure
class UserProfile(BaseModel):
    """Represents the full representation of a user."""

    name: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

# Configure extraction
manager = create_memory_manager(
    "anthropic:claude-3-5-sonnet-latest",
    schemas=[UserProfile],  # (optional) customize schema
    instructions="Extract user profile information",
    enable_inserts=False,  # Profiles update in-place
)

# First conversation
conversation1 = [{"role": "user", "content": "I'm Alice from California"}]
memories = manager.invoke({"messages": conversation1})
print(memories[0])
# ExtractedMemory(id='profile-1', content=UserProfile(
#    name='Alice',
#    language=None,
#    timezone='America/Los_Angeles'
# ))

# Second conversation updates existing profile
conversation2 = [{"role": "user", "content": "I speak Spanish too!"}]
update = manager.invoke({"messages": conversation2, "existing": memories})
print(update[0])
# ExtractedMemory(id='profile-1', content=UserProfile(
#    name='Alice',
#    language='Spanish',  # Updated
#    timezone='America/Los_Angeles'
# ))
```