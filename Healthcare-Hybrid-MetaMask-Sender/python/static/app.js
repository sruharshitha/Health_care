// ==========================
// 📤 SEND MESSAGE
// ==========================
async function sendMessage() {

    const message = document.getElementById("message").value;
    const patient_id = document.getElementById("patient_id").value;

    if (!message) {
        alert("Enter message!");
        return;
    }

    if (!patient_id) {
        alert("Enter Patient ID!");
        return;
    }

    const formData = new FormData();
    formData.append("message", message);
    formData.append("patient_id", patient_id);

    document.getElementById("result").innerHTML = "⏳ Sending...";

    try {
        const res = await fetch("/secure_send", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        // 🚨 AI BLOCK
        if (data.status === "blocked") {
            document.getElementById("result").innerHTML = `
                <div class="result-box error">
                    <h3>🚨 ANOMALY DETECTED</h3>
                    <p><b>Reason:</b> ${data.reason}</p>
                </div>
            `;
            return;
        }

        // ❌ ERROR
        if (data.status === "error") {
            document.getElementById("result").innerHTML =
                "❌ Receiver not reachable";
            return;
        }

        // ✅ SUCCESS (FULL DETAILS)
        if (data.status === "success") {
            document.getElementById("result").innerHTML = `
                <div class="result-box success">
                    <h3>✅ Message Sent Securely</h3>
                    <p><b>CID:</b> ${data.cid}</p>
                    <p><b>Block:</b> ${data.blockNumber}</p>
                    <p><b>Gas:</b> ${data.gasUsed}</p>
                    <p><b>Time:</b> ${data.timestamp}</p>
                </div>
            `;
        }

    } catch (err) {
        console.error(err);
        document.getElementById("result").innerHTML =
            "❌ Error sending message";
    }
}


// ==========================
// 📥 CHECK RESPONSE
// ==========================
async function checkResponse() {

    try {
        const res = await fetch("/read_response");
        const data = await res.json();

        if (!data.message || data.message === "No response yet") {
            document.getElementById("responseBox").innerHTML =
                "⚠️ Waiting for response...";
            return;
        }

        document.getElementById("responseBox").innerHTML = `
            <div style="color:green;">
                <h3>✅ Response Received</h3>
                <p>${data.message}</p>
            </div>
        `;

    } catch (err) {
        console.error(err);
        document.getElementById("responseBox").innerHTML =
            "⚠️ Waiting for response...";
    }
}

// AUTO CHECK
setInterval(checkResponse, 3000);