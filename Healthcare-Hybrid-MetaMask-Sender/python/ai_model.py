from sklearn.ensemble import IsolationForest
import numpy as np
import time

# =========================
# TRAIN DATA (NORMAL)
# =========================
X_train = [
    [25, 1, 98, 1, 0],
    [30, 1, 100, 1, 0],
    [20, 0, 99, 1, 0],
    [35, 1, 101, 1, 0],
    [28, 0, 98, 1, 0],
    [40, 1, 99, 1, 0],
    [22, 0, 97, 1, 0]
]

model = IsolationForest(contamination=0.15, random_state=42)
model.fit(X_train)

# =========================
# MEMORY
# =========================
recent_messages = []
recent_cids = set()
last_timestamp = 0

# =========================
# EXTRACT ID
# =========================
def extract_id_from_message(message):
    for word in message.split():
        if word.isdigit():
            return word
    return None

# =========================
# FEATURE EXTRACTION (IMPROVED)
# =========================
def extract_features(message, patient_id):
    message = message.lower()

    length = len(message)

    medical_words = ["fever", "tablet", "treatment", "injection", "medicine"]
    has_medical = 1 if any(w in message for w in medical_words) else 0

    danger_words = ["kill", "attack", "hack", "poison", "die"]
    has_danger = 1 if any(w in message for w in danger_words) else 0

    temp = 98
    for word in message.split():
        if word.isdigit():
            val = int(word)
            if 90 <= val <= 110:
                temp = val

    try:
        patient_valid = 1 if 1 <= int(patient_id) <= 500 else 0
    except:
        patient_valid = 0

    return [length, has_medical, temp, patient_valid, has_danger]

# =========================
# MAIN CHECK
# =========================
def check_anomaly(message, patient_id, cid=None, receiver_ok=True):

    global recent_messages, recent_cids, last_timestamp

    message_lower = message.lower()

    # -------------------------
    # RULE 1: VALID PATIENT ID
    # -------------------------
    try:
        if not (1 <= int(patient_id) <= 500):
            return -1, "Invalid Patient ID"
    except:
        return -1, "Invalid Patient ID"

    # -------------------------
    # RULE 2: ID MUST EXIST + MATCH
    # -------------------------
    msg_id = extract_id_from_message(message)

    if msg_id is None:
        return -1, "Patient ID missing in message"

    if msg_id != str(patient_id):
        return -1, f"Patient ID mismatch (Form: {patient_id}, Msg: {msg_id})"

    # -------------------------
    # RULE 3: MALICIOUS CONTENT
    # -------------------------
    danger_words = [
        "attack", "hack", "breach",
        "kill", "harm", "poison",
        "overdose", "die", "terminate",
        "destroy", "shutdown"
    ]

    if any(word in message_lower for word in danger_words):
        return -1, "Malicious instruction detected"

    # -------------------------
    # RULE 4: TOO SHORT / INVALID FORMAT
    # -------------------------
    if len(message.strip()) < 10:
        return -1, "Message too short or incomplete"

    # -------------------------
    # RULE 5: CID CHECK (REPLAY)
    # -------------------------
    if cid:
        if cid in recent_cids:
            return -1, "Duplicate CID (Replay attack)"
        recent_cids.add(cid)

    # -------------------------
    # RULE 6: RECEIVER CHECK
    # -------------------------
    if receiver_ok is False:
        return -1, "Receiver not reachable"

    # -------------------------
    # RULE 7: FLOOD DETECTION
    # -------------------------
    now = time.time()
    if last_timestamp != 0 and (now - last_timestamp < 1):
        return -1, "Too many messages (Flooding detected)"
    last_timestamp = now

    # -------------------------
    # AI MODEL CHECK
    # -------------------------
    features = extract_features(message, patient_id)
    prediction = model.predict([features])

    if prediction[0] == -1:
        return -1, "AI detected abnormal pattern"

    # -------------------------
    # STORE HISTORY
    # -------------------------
    recent_messages.append(message)
    if len(recent_messages) > 10:
        recent_messages.pop(0)

    # -------------------------
    # NORMAL
    # -------------------------
    return 1, "Normal"