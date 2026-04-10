from pydantic import BaseModel
from typing import List, Optional, Literal

class Ticket(BaseModel):
    id: int
    text: str
    priority: Literal["low", "medium", "high", "urgent"]
    sla: int
    resolved: bool

class Observation(BaseModel):
    tickets: List[Ticket]
    steps: int
    satisfaction: float

class Action(BaseModel):
    type: Literal["close", "escalate", "reply"]
    ticket_id: int
    message: Optional[str] = None

class Reward(BaseModel):
    score: float
    feedback: str