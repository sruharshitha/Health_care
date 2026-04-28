import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# -------------------------
# LOAD PUBLIC KEY
# -------------------------
def load_public_key(key_data):
    """
    Load public key from PEM or HEX
    """

    from cryptography.hazmat.primitives import serialization

    try:
        # ✅ If PEM format (NEW SYSTEM)
        if isinstance(key_data, str) and "BEGIN PUBLIC KEY" in key_data:
            return serialization.load_pem_public_key(
                key_data.encode()
            )

        # ✅ If HEX format (OLD SYSTEM)
        if isinstance(key_data, str):
            return serialization.load_der_public_key(
                bytes.fromhex(key_data)
            )

        # ✅ If bytes
        if isinstance(key_data, (bytes, bytearray)):
            return serialization.load_der_public_key(key_data)

    except Exception as e:
        print("❌ Public key load error:", e)
        return None


# -------------------------
# LOAD DOCTOR KEYS (JSON)
# -------------------------
def load_doctor_keys():
    """
    Load doctor keys from doctor_keys.json
    """
    try:
        with open("doctor_keys.json", "r") as f:
            keys = json.load(f)

        private_pem = keys["private_key"]
        public_pem = keys["public_key"]

        private_key = serialization.load_pem_private_key(
            private_pem.encode(),
            password=None,
            backend=default_backend()
        )

        public_key = serialization.load_pem_public_key(
            public_pem.encode(),
            backend=default_backend()
        )

        return private_key, public_key

    except Exception as e:
        print("❌ Doctor key load error:", e)
        return None, None


# -------------------------
# LOAD ROBOT KEYS (JSON)
# -------------------------
def load_robot_keys():
    """
    Load robot keys from robot_keys.json
    """
    try:
        with open("robot_keys.json", "r") as f:
            keys = json.load(f)

        private_pem = keys["private_key"]
        public_pem = keys["public_key"]

        private_key = serialization.load_pem_private_key(
            private_pem.encode(),
            password=None,
            backend=default_backend()
        )

        public_key = serialization.load_pem_public_key(
            public_pem.encode(),
            backend=default_backend()
        )

        return private_key, public_key

    except Exception as e:
        print("❌ Robot key load error:", e)
        return None, None


# -------------------------
# DERIVE SHARED SECRET
# -------------------------
def derive_secret(private_key, peer_public_key):
    """
    Derive shared secret using ECDH
    """
    try:
        shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
        return shared_secret
    except Exception as e:
        print("❌ Error deriving secret:", e)
        return None