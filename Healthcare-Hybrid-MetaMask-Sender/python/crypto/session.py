import hashlib
import base64

def derive_session_key(shared_secret, token):
    # Combine secret + token
    combined = shared_secret + token.encode()

    # Hash
    digest = hashlib.sha256(combined).digest()

    # Convert to Fernet key (32 bytes → base64)
    return base64.urlsafe_b64encode(digest)