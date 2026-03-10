"""
db/models.py
------------
SQLAlchemy ORM models for the Rakshita system.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    Enum,
    DateTime,
    JSON,
)

from db.database import Base


# ── Enums ─────────────────────────────────────────────────

class ComplaintStatus(str, enum.Enum):
    """Strict state-machine: PENDING → ASSIGNED → IN_PROGRESS → RESOLVED."""
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class PriorityLabel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ── Valid state transitions (PRD §4) ─────────────────────

VALID_TRANSITIONS: dict[ComplaintStatus, list[ComplaintStatus]] = {
    ComplaintStatus.PENDING: [ComplaintStatus.ASSIGNED],
    ComplaintStatus.ASSIGNED: [ComplaintStatus.IN_PROGRESS],
    ComplaintStatus.IN_PROGRESS: [ComplaintStatus.RESOLVED],
    ComplaintStatus.RESOLVED: [],  # terminal state
}


# ── Complaint Model ──────────────────────────────────────

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    ward = Column(String(100), nullable=False)

    # ── State & Priority ──
    status = Column(
        Enum(ComplaintStatus),
        default=ComplaintStatus.PENDING,
        nullable=False,
    )
    priority_score = Column(Float, nullable=True)
    priority_label = Column(
        Enum(PriorityLabel),
        nullable=True,
    )

    # ── ML Scores ──
    severity_score = Column(Float, nullable=True)
    credibility_score = Column(Float, nullable=True)
    explanation_json = Column(JSON, nullable=True)

    # ── Metadata ──
    submitted_by_ip = Column(String(45), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Complaint id={self.id} status={self.status} priority={self.priority_label}>"


# ── Officer Model ─────────────────────────────────────────

class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    ward = Column(String(100), nullable=False)
    role = Column(String(50), default="officer", nullable=False)

    def __repr__(self) -> str:
        return f"<Officer id={self.id} username={self.username} ward={self.ward}>"
