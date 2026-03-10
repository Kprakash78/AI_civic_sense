"""
api/schemas.py
--------------
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Complaint Schemas ─────────────────────────────────────

class ComplaintCreate(BaseModel):
    """Public intake form – no auth required."""
    text: str = Field(..., min_length=1, description="Complaint description")
    category: str = Field(..., min_length=1, description="e.g. Pothole, Water, Electricity")
    ward: str = Field(..., min_length=1, description="Ward name or code")


class ComplaintResponse(BaseModel):
    """Full complaint record returned to caller."""
    id: int
    text: str
    category: str
    ward: str
    status: str
    priority_score: Optional[float] = None
    priority_label: Optional[str] = None
    severity_score: Optional[float] = None
    credibility_score: Optional[float] = None
    explanation_json: Optional[dict] = None
    submitted_by_ip: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 ORM mode


class StatusUpdate(BaseModel):
    """Request body to transition complaint state."""
    new_status: str = Field(
        ...,
        description="Target status: ASSIGNED | IN_PROGRESS | RESOLVED",
    )


# ── Auth Schemas ──────────────────────────────────────────

class OfficerLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    ward: Optional[str] = None
    role: Optional[str] = None
