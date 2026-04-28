from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import json

def generate_robot_keys():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    keys = {
        "private_key": private_pem,
        "public_key": public_pem
    }

    with open("robot_keys.json", "w") as f:
        json.dump(keys, f, indent=4)

    print("✅ robot_keys.json created successfully")

if __name__ == "__main__":
    generate_robot_keys()