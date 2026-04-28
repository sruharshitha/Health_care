from flask import Flask, render_template, request, jsonify, redirect, session
import secrets, requests, json, os
from datetime import datetime

from cryptography.hazmat.primitives import serialization
from web3 import Web3

from ipfs.ipfs import upload
from crypto.aes256 import encrypt_message
from crypto.ecdh import derive_secret, load_doctor_keys, load_public_key
from crypto.session import derive_session_key

from ai_model import check_anomaly
from crypto.protocol import generate_nonce, current_timestamp

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "doctor_secret"

# 🔥 IMPORTANT: change this if different system
RECEIVER_IP = "10.10.201.63"
RECEIVER_PORT = "7000"

HANDSHAKE_URL = f"http://{RECEIVER_IP}:{RECEIVER_PORT}/handshake"
RECEIVE_URL   = f"http://{RECEIVER_IP}:{RECEIVER_PORT}/receive_secure"
GET_RESPONSE_URL = f"http://{RECEIVER_IP}:{RECEIVER_PORT}/get_response"

VALID_USERS = {"doctor1": "1234"}

# ================= BLOCKCHAIN =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

with open(os.path.join(BASE_DIR, "blockchain", "contract.json")) as f:
    contract_data = json.load(f)

contract = w3.eth.contract(address=contract_data["address"], abi=contract_data["abi"])
account = w3.eth.accounts[0]

# ================= LOGIN =================
@app.route("/")
def login():
    return render_template("index.html")

@app.route("/challenge")
def challenge():
    return jsonify({"message": "Doctor Login: " + secrets.token_hex(16)})

@app.route("/verify_doctor", methods=["POST"])
def verify_doctor():
    return jsonify({"status": "success", "redirect": "/credentials"})

@app.route("/credentials")
def credentials():
    return render_template("credentials.html")

@app.route("/login_credentials", methods=["POST"])
def login_credentials():
    if request.form["username"] == "doctor1" and request.form["password"] == "1234":
        session["user"] = "doctor"
        return redirect("/sender")
    return "Invalid login"

@app.route("/sender")
def sender():
    if "user" not in session:
        return redirect("/")
    return render_template("sender.html")

# ================= SEND MESSAGE =================
@app.route("/secure_send", methods=["POST"])
def secure_send():
    try:
        message = request.form.get("message")
        patient_id = request.form.get("patient_id")

        print("\n📤 ================= SENDING =================")

        # AI
        result, reason = check_anomaly(message, patient_id)
        print("🧠 AI:", result, reason)

        if result == -1:
            return jsonify({"status": "blocked", "reason": reason})

        # KEYS
        doctor_private, doctor_public = load_doctor_keys()

        doctor_pub = doctor_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # HANDSHAKE (SAFE FIX)
        n1 = generate_nonce()
        T1 = current_timestamp()

        try:
            res = requests.post(HANDSHAKE_URL, json={
                "doctor_public": doctor_pub,
                "n1": n1,
                "T1": T1
            }, timeout=5)

            if res.status_code != 200:
                return jsonify({"status": "error", "message": "Receiver not reachable"})

            res = res.json()

        except Exception as e:
            print("❌ HANDSHAKE ERROR:", e)
            return jsonify({"status": "error", "message": "Receiver connection failed"})

        print("✅ Handshake OK")

        # KEY DERIVATION
        robot_public = load_public_key(res["robot_public"])
        shared = derive_secret(doctor_private, robot_public)
        final_key = derive_session_key(shared, n1)

        # ENCRYPT
        cipher = encrypt_message(message, final_key)

        # IPFS
        print("📦 Uploading to IPFS...")
        cid = upload({
            "cipher": cipher,
            "doctor_public": doctor_pub
        })
        print("📦 CID:", cid)

        # BLOCKCHAIN
        tx = contract.functions.storeMessage(
            cid,
            account,
            str(datetime.now())
        ).transact({"from": account})

        receipt = w3.eth.wait_for_transaction_receipt(tx)

        block = receipt.blockNumber
        gas = receipt.gasUsed
        timestamp = w3.eth.get_block(block).timestamp

        print("⛓ Block:", block)
        print("⛽ Gas:", gas)
        print("⏱ Time:", timestamp)

        # SEND TO RECEIVER
        try:
            send_res = requests.post(RECEIVE_URL, json={
                "cid": cid,
                "SK1": n1,
                "blockNumber": block,
                "gasUsed": gas,
                "timestamp": timestamp
            }, timeout=5)

            print("📡 Receiver:", send_res.text)

        except Exception as e:
            print("❌ SEND ERROR:", e)
            return jsonify({"status": "error", "message": "Receiver not reachable"})

        return jsonify({
            "status": "success",
            "cid": cid,
            "blockNumber": block,
            "gasUsed": gas,
            "timestamp": timestamp
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"status": "error", "message": str(e)})

# ================= READ RESPONSE =================
@app.route("/read_response")
def read_response():
    try:
        res = requests.get(GET_RESPONSE_URL).json()
        return res
    except:
        return {"message": "No response yet"}

# ================= RUN =================
if __name__ == "__main__":
    print("🚀 Sender Running on 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)