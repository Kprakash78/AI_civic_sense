"""
ml/preprocessor.py
------------------
Text preprocessing utilities for the ML pipeline.
Pure function – no DB or HTTP dependencies.
"""

import re


def clean_text(raw: str) -> str:
    """
    Basic text cleanup for downstream ML models.

    Steps
    -----
    1. Strip leading/trailing whitespace.
    2. Collapse multiple spaces.
    3. Remove non-printable characters.
    4. Lowercase.

    Parameters
    ----------
    raw : str
        Raw complaint text from user input.

    Returns
    -------
    str
        Cleaned text ready for model inference.
    """
    text = raw.strip()
    text = re.sub(r"\s+", " ", text)           # collapse whitespace
    text = re.sub(r"[^\x20-\x7E]+", "", text)  # remove non-printable chars
    text = text.lower()
    return text
