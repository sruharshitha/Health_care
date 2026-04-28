import requests
import json
import os

IPFS_API = "http://127.0.0.1:5001/api/v0"

# =========================
# UPLOAD
# =========================
def upload(data):
    try:
        if not isinstance(data, dict):
            print("❌ Upload data must be dictionary")
            return None

        temp_file = "temp_ipfs.json"

        with open(temp_file, "w") as f:
            json.dump(data, f)

        with open(temp_file, "rb") as f:
            response = requests.post(f"{IPFS_API}/add", files={"file": f})

        if os.path.exists(temp_file):
            os.remove(temp_file)

        if response.status_code != 200:
            print("❌ IPFS upload failed:", response.text)
            return None

        cid = response.json().get("Hash")

        print("📤 Uploaded CID:", cid)

        return cid

    except Exception as e:
        print("❌ IPFS Upload Error:", e)
        return None


# =========================
# DOWNLOAD
# =========================
def download(cid):
    try:
        if not cid:
            print("❌ Invalid CID")
            return None

        response = requests.post(f"{IPFS_API}/cat?arg={cid}")

        if response.status_code != 200:
            print("❌ IPFS fetch failed:", response.text)
            return None

        raw = response.content.decode()

        print("📥 RAW IPFS DATA:", raw)

        if not raw:
            print("❌ Empty IPFS data")
            return None

        try:
            data = json.loads(raw)
        except Exception as e:
            print("❌ JSON parse error:", e)
            return None

        # =========================
        # ✅ FINAL FIX (IMPORTANT)
        # =========================
        if "cipher" not in data:
            print("❌ Missing cipher:", data)
            return None

        # Accept BOTH cases
        if "doctor_public" not in data and "robot_public" not in data:
            print("❌ Missing public key:", data)
            return None

        return data

    except Exception as e:
        print("❌ IPFS Download Error:", e)
        return None