from Crypto.Cipher import AES
import base64

def decrypt_message(encrypted_data, key):
    """
    Decrypt AES-256 GCM encrypted message
    """

    try:
        # ✅ Ensure key is 32 bytes
        key = key[:32]

        # ✅ Convert encrypted data from string → bytes
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()

        # ✅ Base64 decode
        raw = base64.b64decode(encrypted_data)

        # ✅ Extract parts
        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]

        # 🔐 AES GCM decrypt
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        decrypted = cipher.decrypt_and_verify(ciphertext, tag)

        result = decrypted.decode()

        print("🔑 RECEIVER KEY:", key)
        print("✅ DECRYPT SUCCESS")

        return result

    except Exception as e:
        print("❌ DECRYPT ERROR:", e)
        raise e