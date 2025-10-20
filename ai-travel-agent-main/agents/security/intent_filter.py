import re

"""Simple intent recognition to detect potentially malicious or jailbreak prompts.

This module provides conservative checks for known jailbreak patterns and a
basic sanitizer. It's not foolproof but helps reduce obvious adversarial inputs.
"""

# Very small example blacklist and patterns (extend as needed)
_BLACKLISTED_PHRASES = [
    r"ignore (previous|earlier) instructions",
    r"bypass (policy|filter)",
    r"d(?:o|on)'t follow rules",
    r"write me a malicious",
    r"how to hack",
]

_BLACKLISTED_RE = [re.compile(pat, re.IGNORECASE) for pat in _BLACKLISTED_PHRASES]


def is_malicious(text: str) -> bool:
    if not text:
        return False
    for rx in _BLACKLISTED_RE:
        if rx.search(text):
            return True
    return False


def sanitize(text: str) -> str:
    # Minimal sanitizer: redact blacklisted patterns
    out = text
    for rx in _BLACKLISTED_RE:
        out = rx.sub('[REDACTED]', out)
    return out
