"""
services/priority_engine.py
----------------------------
The Priority Engine – system brain that fuses ML scores into a
final priority_score, priority_label, and explainability payload.

Implements ML_LOGIC.md §4 exactly:
  • Standard weighting:  P = (0.7 × S) + (0.3 × C)
  • Emergency Override:  if S > 0.85 → P = 0.95
  • Label mapping:       CRITICAL ≥ 0.80 | HIGH ≥ 0.60 | MEDIUM ≥ 0.35 | LOW < 0.35
"""

from ml.severity_model import predict_severity
from ml.credibility_model import predict_credibility

# ── Weight constants ──────────────────────────────────────
W_SEVERITY: float = 0.7
W_CREDIBILITY: float = 0.3
EMERGENCY_THRESHOLD: float = 0.85
EMERGENCY_OVERRIDE_SCORE: float = 0.95


def _map_priority_label(score: float) -> str:
    """Map a numeric priority score to a human-readable label."""
    if score >= 0.80:
        return "CRITICAL"
    if score >= 0.60:
        return "HIGH"
    if score >= 0.35:
        return "MEDIUM"
    return "LOW"


def calculate_priority(
    text: str,
    user_ip: str | None = None,
    db=None,
) -> dict:
    """
    Run the full prioritization pipeline for a complaint.

    Parameters
    ----------
    text : str
        Raw complaint text.
    user_ip : str, optional
        IP address of the submitter (for credibility frequency checks).
    db : optional
        Database session (forwarded to credibility model).

    Returns
    -------
    dict
        {
            "severity_score":    float,
            "credibility_score": float,
            "priority_score":    float,
            "priority_label":    str,
            "explanation": {
                "severity_reason":      str,
                "credibility_reason":   str,
                "weight_profile_used":  str,    # "Standard" | "Emergency Override"
            }
        }
    """

    # ── 1. Invoke ML models ──────────────────────────────
    severity_result = predict_severity(text)
    credibility_result = predict_credibility(text, user_ip=user_ip, db=db)

    severity_score: float = severity_result["score"]
    credibility_score: float = credibility_result["score"]

    # ── 2. Priority calculation ──────────────────────────
    if severity_score > EMERGENCY_THRESHOLD:
        # Emergency Override (ML_LOGIC.md §4)
        priority_score = EMERGENCY_OVERRIDE_SCORE
        weight_profile = "Emergency Override"
    else:
        # Standard weighting
        priority_score = (W_SEVERITY * severity_score) + (W_CREDIBILITY * credibility_score)
        weight_profile = "Standard"

    priority_score = round(priority_score, 4)
    priority_label = _map_priority_label(priority_score)

    # ── 3. Build explainability payload (ML_LOGIC.md §5) ─
    shap_data = severity_result.get("shap_explanation", {})
    top_tokens = shap_data.get("top_positive_tokens", [])
    severity_reason = (
        f"Top SHAP triggers: {', '.join(top_tokens)}"
        if top_tokens
        else "No significant SHAP triggers identified."
    )

    explanation = {
        "severity_reason": severity_reason,
        "credibility_reason": credibility_result["reason"],
        "weight_profile_used": weight_profile,
    }

    return {
        "severity_score": severity_score,
        "credibility_score": credibility_score,
        "priority_score": priority_score,
        "priority_label": priority_label,
        "explanation": explanation,
    }
