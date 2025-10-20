from cryptography.fernet import Fernet
import os

"""Encryption utilities using Fernet (symmetric) for demo purposes.

In production, use a robust KMS (AWS KMS, Azure Key Vault) and rotate keys.
"""


def generate_key() -> bytes:
    return Fernet.generate_key()


def get_fernet():
    key = os.environ.get('FERNET_KEY')
    if not key:
        raise RuntimeError('FERNET_KEY environment variable is required')
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_bytes(data: bytes) -> bytes:
    f = get_fernet()
    return f.encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    f = get_fernet()
    return f.decrypt(token)


def encrypt_text(text: str) -> str:
    return encrypt_bytes(text.encode()).decode()


def decrypt_text(token: str) -> str:
    return decrypt_bytes(token.encode()).decode()
