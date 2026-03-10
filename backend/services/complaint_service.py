"""
services/complaint_service.py
-----------------------------
Service-layer CRUD for Complaints.
Enforces the PRD state machine and integrates with the Priority Engine.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import Complaint, ComplaintStatus, VALID_TRANSITIONS
from api.schemas import ComplaintCreate
from services.priority_engine import calculate_priority


# ── Create ────────────────────────────────────────────────

def create_complaint(
    db: Session,
    payload: ComplaintCreate,
    user_ip: str | None = None,
) -> Complaint:
    """
    Persist a new complaint and run the Priority Engine synchronously.
    """
    # Run prioritisation pipeline
    priority = calculate_priority(
        text=payload.text,
        user_ip=user_ip,
        db=db,
    )

    complaint = Complaint(
        text=payload.text,
        category=payload.category,
        ward=payload.ward,
        status=ComplaintStatus.PENDING,
        severity_score=priority["severity_score"],
        credibility_score=priority["credibility_score"],
        priority_score=priority["priority_score"],
        priority_label=priority["priority_label"],
        explanation_json=priority["explanation"],
        submitted_by_ip=user_ip,
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


# ── Read ──────────────────────────────────────────────────

def get_complaints(
    db: Session,
    ward: str | None = None,
    status_filter: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Complaint]:
    """Retrieve complaints with optional ward / status filters, sorted by priority desc."""
    query = db.query(Complaint)

    if ward:
        query = query.filter(Complaint.ward == ward)
    if status_filter:
        query = query.filter(Complaint.status == status_filter)

    return (
        query
        .order_by(Complaint.priority_score.desc().nullslast())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_complaint_by_id(db: Session, complaint_id: int) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint {complaint_id} not found",
        )
    return complaint


# ── Update Status (state-machine enforced) ────────────────

def update_complaint_status(
    db: Session,
    complaint_id: int,
    new_status_str: str,
) -> Complaint:
    """
    Transition a complaint to a new status.
    Raises 400 if the transition violates the PRD state machine.
    """
    complaint = get_complaint_by_id(db, complaint_id)

    try:
        new_status = ComplaintStatus(new_status_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status: '{new_status_str}'. "
                   f"Valid values: {[s.value for s in ComplaintStatus]}",
        )

    allowed = VALID_TRANSITIONS.get(complaint.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid transition: {complaint.status.value} → {new_status.value}. "
                f"Allowed next states: {[s.value for s in allowed]}"
            ),
        )

    complaint.status = new_status
    db.commit()
    db.refresh(complaint)
    return complaint
