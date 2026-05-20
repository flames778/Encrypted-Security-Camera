import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config import KEY_FILE

def get_or_create_key() -> bytes:
    """
    Loads the AES-256-GCM key from disk, or generates a new one if it doesn't exist.
    """
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            key = f.read()
            if len(key) != 32:
                raise ValueError("Key file is invalid (must be 32 bytes).")
            return key
    else:
        print("Generating new AES-256 key...")
        key = AESGCM.generate_key(bit_length=256)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
