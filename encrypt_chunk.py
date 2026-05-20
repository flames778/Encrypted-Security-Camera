import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_chunk(plaintext: bytes, key: bytes) -> bytes:
    """
    Encrypts a chunk of bytes using AES-256-GCM.
    Returns: nonce (12 bytes) + ciphertext + auth tag (16 bytes)
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext

def decrypt_chunk(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypts a chunk of bytes using AES-256-GCM.
    Expects: nonce (12 bytes) + ciphertext + auth tag (16 bytes)
    """
    if len(encrypted_data) < 28: # 12 (nonce) + 16 (tag)
        raise ValueError("Encrypted data is too short")
        
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext
