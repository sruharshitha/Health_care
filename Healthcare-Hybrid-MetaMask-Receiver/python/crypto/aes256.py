from Crypto.Cipher import AES
import base64
import hashlib


# =========================
# 🔑 KEY NORMALIZATION
# =========================
def normalize_key(key):
    if isinstance(key, str):
        key = key.encode()

    # Always 32 bytes (AES-256)
    return hashlib.sha256(key).digest()


# =========================
# 🔐 ENCRYPT (AES-GCM)
# =========================
def encrypt_message(message, key):
    key = normalize_key(key)

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    encrypted = cipher.nonce + tag + ciphertext

    return base64.b64encode(encrypted).decode()


# =========================
# 🔓 DECRYPT (AES-GCM)
# =========================
def decrypt_message(encrypted_data, key):
    try:
        key = normalize_key(key)

        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()

        raw = base64.b64decode(encrypted_data)

        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        decrypted = cipher.decrypt_and_verify(ciphertext, tag)

        return decrypted.decode()

    except Exception as e:
        print("❌ DECRYPT ERROR:", e)
        return "DECRYPT FAILED"