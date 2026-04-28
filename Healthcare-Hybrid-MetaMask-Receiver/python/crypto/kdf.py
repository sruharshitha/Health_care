# crypto/kdf.py
from cryptography.hazmat.primitives import hashes

def sha256_kdf(shared_secret):
    """
    Converts shared secret into a 32-byte AES key
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared_secret)
    return digest.finalize()