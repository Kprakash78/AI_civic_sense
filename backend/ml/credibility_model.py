"""
ml/credibility_model.py
-----------------------
Hybrid Credibility Model (ML base + rule-based penalties).

Input:  Cleaned text, user IP, DB session.
Output: Float ∈ [0, 1]  and  human-readable reason string.

NOTE: The base ML score is a **placeholder**.
Replace with a real NLP model when trained artefacts are ready.
"""

import random

from ml.preprocessor import clean_text


def predict_credibility(text: str, user_ip: str | None = None, db=None) -> dict:
    """
    Evaluate the credibility of a complaint using a hybrid approach.

    Rule-based penalties (ML_LOGIC.md §3)
    --------------------------------------
    • ALL CAPS SPAM  → reduce score by 0.3
    • Word count < 4 → reduce score by 0.4
    • High frequency (>5 in 10 min from same IP) → cap at 0.1  [TODO: needs DB query]

    Parameters
    ----------
    text : str
        Raw complaint text.
    user_ip : str, optional
        Submitter IP for frequency checks.
    db : Session, optional
        Database session for high-frequency lookup.

    Returns
    -------
    dict
        {"score": float, "reason": str}
    """
    cleaned = clean_text(text)
    penalties: list[str] = []

    # ── Placeholder base ML score ─────────────────────────
    base_score: float = round(random.uniform(0.5, 1.0), 4)
    score = base_score

    # ── Rule: ALL CAPS SPAM ───────────────────────────────
    raw_alpha = "".join(c for c in text if c.isalpha())
    if raw_alpha and raw_alpha == raw_alpha.upper() and len(raw_alpha) > 3:
        score -= 0.3
        penalties.append("ALL CAPS detected (-0.3)")

    # ── Rule: Short length ────────────────────────────────
    word_count = len(cleaned.split())
    if word_count < 4:
        score -= 0.4
        penalties.append(f"Short text ({word_count} words) (-0.4)")

    # ── Rule: High frequency (TODO – implement DB query) ──
    # if user_ip and db:
    #     recent_count = _count_recent_submissions(db, user_ip, minutes=10)
    #     if recent_count > 5:
    #         score = min(score, 0.1)
    #         penalties.append(f"High frequency ({recent_count} in 10 min), capped at 0.1")

    # ── Clamp to [0, 1] ──────────────────────────────────
    score = round(max(0.0, min(1.0, score)), 4)

    reason = (
        f"Base ML confidence: {base_score}. "
        + ("Penalties applied: " + "; ".join(penalties) if penalties else "No penalties applied.")
    )

    return {"score": score, "reason": reason}
