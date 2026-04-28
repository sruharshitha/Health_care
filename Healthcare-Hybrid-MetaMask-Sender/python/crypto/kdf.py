import hashlib

def derive_session_key(private_key, shared_key):

    data = str(private_key) + str(shared_key)

    return hashlib.sha256(data.encode()).digest()