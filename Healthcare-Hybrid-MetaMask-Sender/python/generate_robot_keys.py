from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import json

# Generate key
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Convert public key to DER → HEX
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

robot_keys = {
    "robot_public": public_bytes.hex()
}

with open("robot_keys.json", "w") as f:
    json.dump(robot_keys, f, indent=4)

print("✅ robot_keys.json generated")