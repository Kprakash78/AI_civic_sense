"""
ml/severity_model.py
--------------------
Severity / Danger Detection model.

Input:  Cleaned text string.
Output: Float ∈ [0, 1]  and  SHAP explanation dict.

NOTE: This is a **placeholder** implementation.
Replace the body of `predict_severity` with actual model inference
(e.g. scikit-learn / XGBoost pipeline + SHAP explainer) when the
trained artefacts are available.
"""

import random

from ml.preprocessor import clean_text


def predict_severity(text: str) -> dict:
    """
    Predict how dangerous / urgent a complaint is.

    Parameters
    ----------
    text : str
        Raw (or pre-cleaned) complaint text.

    Returns
    -------
    dict
        {
            "score": float,            # ∈ [0, 1]  – 1.0 = immediate threat
            "shap_explanation": dict    # top contributing tokens
        }
    """
    cleaned = clean_text(text)

    # ── Placeholder: replace with real model inference ────
    score = round(random.uniform(0.0, 1.0), 4)

    shap_explanation = {
        "top_positive_tokens": ["placeholder_token_1", "placeholder_token_2"],
        "top_negative_tokens": ["placeholder_token_3"],
        "note": "PLACEHOLDER – wire a trained model + SHAP explainer here.",
    }

    return {
        "score": score,
        "shap_explanation": shap_explanation,
    }
