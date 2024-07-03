from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, json
from enum import Enum
from datetime import datetime
from typing import Union

class EventKind(str, Enum):
    content_management = 'content_management'
    social_network = 'social_network'
    marketplace = 'marketplace'
    vto = 'vto'
    dream_journal = 'dream_journal'

@dataclass(frozen=True)
class Event(BaseModel):
    """Represents an event."""
    event_id: int
    event_name: str
    event_creation_ts: str
    event_source: EventKind
    event_kind: EventKind
    event_location: str
    event_processed_ts: Union[str, None] = None
    event_payload: Optional[str] = None
