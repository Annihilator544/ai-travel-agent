import pytest

from agents.privacy.masking import mask_pii


def test_mask_pii_basic():
    s = "Contact john.doe@example.com or +1 555-123-4567. CC: 4111 1111 1111 1111"
    masked = mask_pii(s)
    assert "***@***" in masked
    assert "***-***-****" in masked
    assert "**** **** **** ****" in masked
