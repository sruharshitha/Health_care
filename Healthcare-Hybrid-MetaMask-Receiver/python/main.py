from flask import Flask, render_template, request, jsonify, redirect, session
import secrets

from cryptography.hazmat.primitives import serialization

from ipfs.ipfs import download
from crypto.aes256 import decrypt_message
from crypto.ecdh import derive_secret, load_robot_keys, load_public_key
from crypto.session import derive_session_key

from ai_model import check_anomaly

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "robot_secret"

VALID_USERS = {"robot1": "1234"}

latest_message = {
    "status": "waiting",
    "message": "",
    "reason": "",
    "cid": "-",
    "block": "-",
    "gas": "-",
    "time": "-"
}

latest_response = {"message": "No response yet"}

# ================= LOGIN =================
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/challenge")
def challenge():
    return jsonify({"message": "Robot Login: " + secrets.token_hex(16)})

@app.route("/verify_robot", methods=["POST"])
def verify_robot():
    return jsonify({"status": "success", "redirect": "/credentials"})

@app.route("/credentials")
def credentials():
    return render_template("credentials.html")

@app.route("/login_credentials", methods=["POST"])
def login_credentials():
    if request.form["username"] == "robot1" and request.form["password"] == "1234":
        session["user"] = "robot"
        return redirect("/receiver")
    return "Invalid login"

@app.route("/receiver")
def receiver():
    if "user" not in session:
        return redirect("/")
    return render_template("receiver.html")

@app.route("/get_message")
def get_message():
    return jsonify(latest_message)

# ================= HANDSHAKE =================
@app.route("/handshake", methods=["POST"])
def handshake():
    print("🤝 Handshake received")

    robot_private, robot_public = load_robot_keys()

    return {
        "robot_public": robot_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }

# ================= RECEIVE =================
@app.route("/receive_secure", methods=["POST"])
def receive_secure():
    global latest_message, latest_response

    try:
        data = request.json

        print("\n📥 MESSAGE RECEIVED")

        ipfs_data = download(data["cid"])

        doctor_public = load_public_key(ipfs_data["doctor_public"])
        robot_private, _ = load_robot_keys()

        shared = derive_secret(robot_private, doctor_public)
        final_key = derive_session_key(shared, data["SK1"])

        decrypted = decrypt_message(ipfs_data["cipher"], final_key)

        print("📩 Message:", decrypted)

        result, reason, *_ = check_anomaly(decrypted, "101", cid=data.get("cid"))

        status = "accepted" if result == 1 else "rejected"

        latest_message = {
            "status": status,
            "message": decrypted,
            "reason": reason,
            "cid": data.get("cid", "-"),
            "block": data.get("blockNumber", "-"),
            "gas": data.get("gasUsed", "-"),
            "time": data.get("timestamp", "-")
        }

        if result == 1:
            latest_response = {"message": "ACK: Message received"}
        else:
            latest_response = {"message": "Rejected: " + reason}

        return jsonify({"status": "success"})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"status": "error"})

# ================= SEND RESPONSE =================
@app.route("/send_response", methods=["POST"])
def send_response():
    global latest_response, latest_message

    try:
        msg = request.json["message"]

        correct_patient_id = "0"
        if latest_message.get("message"):
            for word in latest_message["message"].split():
                if word.isdigit():
                    correct_patient_id = word
                    break

        result, reason, *_ = check_anomaly(msg, correct_patient_id)

        if result == -1:
            return jsonify({
                "status": "blocked",
                "reason": reason
            })

        latest_response = {"message": msg}

        print("📤 Response Sent:", msg)

        return jsonify({
            "status": "success",
            "cid": latest_message.get("cid", "-"),
            "block": latest_message.get("block", "-"),
            "gas": latest_message.get("gas", "-"),
            "time": latest_message.get("time", "-")
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"status": "error"})

# ================= GET RESPONSE (FIX) =================
@app.route("/get_response")
def get_response():
    global latest_response
    return jsonify(latest_response)

# ================= RUN =================
if __name__ == "__main__":
    print("🤖 Receiver Running on 7000")
    app.run(host="0.0.0.0", port=7000, debug=True)