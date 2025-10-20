import re
from typing import Pattern


"""PII masking utilities for VoyageVerse.

This module provides lightweight, regex-based masking utilities to remove or
mask common personally-identifiable information (PII) from text before it is
sent in emails, logs, or responses. It is intentionally conservative and
designed to reduce accidental leakage of sensitive strings like emails,
credit card numbers, phone numbers, and SSNs.
"""


# Regular expressions used for basic PII detection.
_EMAIL_RE: Pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_CC_RE: Pattern = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_PHONE_RE: Pattern = re.compile(r"\b\+?\d[\d\-\s]{7,}\b")
_SSN_RE: Pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def mask_emails(text: str) -> str:
    return _EMAIL_RE.sub("***@***", text)


def mask_credit_cards(text: str) -> str:
    # Replace detected long digit sequences with a masked pattern
    return _CC_RE.sub("**** **** **** ****", text)


def mask_phone_numbers(text: str) -> str:
    return _PHONE_RE.sub("***-***-****", text)


def mask_ssn(text: str) -> str:
    return _SSN_RE.sub("***-**-****", text)


def mask_pii(text: str) -> str:
    """Return a copy of text with common PII masked.

    This function applies several conservative regex masks. It is not a
    substitute for secure data handling, but reduces accidental exposure in
    generated outputs.
    """
    if not text:
        return text
    out = text
    out = mask_credit_cards(out)
    out = mask_ssn(out)
    out = mask_emails(out)
    out = mask_phone_numbers(out)
    return out


def mask_pii_in_obj(obj):
    """Recursively mask PII in Python objects (str, list, dict).

    Returns a new object with the same structure where any string values are
    passed through mask_pii. Non-string leaves are returned mostly unchanged.
    """
    if obj is None:
        return obj
    if isinstance(obj, str):
        return mask_pii(obj)
    if isinstance(obj, list):
        return [mask_pii_in_obj(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(mask_pii_in_obj(x) for x in obj)
    if isinstance(obj, dict):
        return {k: mask_pii_in_obj(v) for k, v in obj.items()}
    # For other types (int, float, bool, objects) return as-is
    return obj
