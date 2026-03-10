"""
api/routes_complaints.py
------------------------
Public and officer-facing complaint endpoints.
"""

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Officer
from api.schemas import ComplaintCreate, ComplaintResponse, StatusUpdate
from core.security import get_current_officer
from services import complaint_service

router = APIRouter(prefix="/complaints", tags=["Complaints"])


# ── Public intake ─────────────────────────────────────────

@router.post("/", response_model=ComplaintResponse, status_code=201)
def submit_complaint(
    payload: ComplaintCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public endpoint – no auth.
    Ingests a complaint, triggers the Priority Engine, and returns the
    enriched record with scores and explainability.
    """
    user_ip = request.client.host if request.client else None
    complaint = complaint_service.create_complaint(db, payload, user_ip=user_ip)
    return complaint


# ── List / filter ─────────────────────────────────────────

@router.get("/", response_model=list[ComplaintResponse])
def list_complaints(
    ward: str | None = Query(None, description="Filter by ward"),
    status: str | None = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Retrieve complaints, optionally filtered by ward and/or status."""
    return complaint_service.get_complaints(
        db, ward=ward, status_filter=status, skip=skip, limit=limit,
    )


# ── Single complaint ─────────────────────────────────────

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a single complaint by ID."""
    return complaint_service.get_complaint_by_id(db, complaint_id)


# ── Status transition (officer-only) ─────────────────────

@router.patch("/{complaint_id}/status", response_model=ComplaintResponse)
def transition_status(
    complaint_id: int,
    body: StatusUpdate,
    officer: Officer = Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    """
    Officer endpoint – JWT required.
    Transitions a complaint through the state machine.
    """
    return complaint_service.update_complaint_status(
        db, complaint_id, body.new_status,
    )
