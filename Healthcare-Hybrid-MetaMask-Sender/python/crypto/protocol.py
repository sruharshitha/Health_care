import hashlib, os, time

def h(data):
    return hashlib.sha256(data.encode()).hexdigest()

def generate_nonce():
    return os.urandom(8).hex()

def current_timestamp():
    return str(int(time.time()))
