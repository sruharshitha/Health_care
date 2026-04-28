// ==========================
// 📥 FETCH MESSAGE
// ==========================
async function fetchMessage() {

    const box = document.getElementById("msgBox");
    if (!box) return;

    try {
        const res = await fetch("/get_message");
        const data = await res.json();

        // ✅ ACCEPTED
        if (data.status === "accepted") {
            box.innerHTML = `
                <div style="color:green;">
                    <h3>✅ Message Accepted</h3>
                    <p><b>Message:</b> ${data.message}</p>
                    <p><b>Status:</b> ${data.reason}</p>
                </div>
            `;
        }

        // 🚨 REJECTED
        else if (data.status === "rejected") {
            box.innerHTML = `
                <div style="color:red;">
                    <h3>🚨 Message Rejected</h3>
                    <p><b>Message:</b> ${data.message}</p>
                    <p><b>Reason:</b> ${data.reason}</p>
                </div>
            `;
        }

        // ⏳ WAITING
        else {
            box.innerHTML = "⏳ Waiting for message...";
        }

    } catch (err) {
        console.error(err);
        box.innerHTML = "❌ Error fetching message";
    }
}

// AUTO REFRESH
setInterval(fetchMessage, 2000);


// ==========================
// 📤 SEND RESPONSE
// ==========================
async function sendResponse() {

    const message = document.getElementById("responseText").value;

    if (!message) {
        alert("Enter response!");
        return;
    }

    try {
        document.getElementById("status").innerHTML = "⏳ Sending...";

        const res = await fetch("/send_response", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message })
        });

        const data = await res.json();

        // ✅ SUCCESS (FIXED KEYS)
        if (data.status === "success") {
            document.getElementById("status").innerHTML = `
                <div style="color:green;">
                    <h3>✅ Response Sent</h3>
                    <p><b>CID:</b> ${data.cid || "-"}</p>
                    <p><b>Block:</b> ${data.block || "-"}</p>
                    <p><b>Gas:</b> ${data.gas || "-"}</p>
                    <p><b>Time:</b> ${data.time || "-"}</p>
                </div>
            `;
        }

        // 🚨 BLOCKED BY AI
        else if (data.status === "blocked") {
            document.getElementById("status").innerHTML = `
                <div style="color:red;">
                    <h3>🚨 Blocked by AI</h3>
                    <p>${data.reason}</p>
                </div>
            `;
        }

        else {
            document.getElementById("status").innerHTML =
                "❌ Failed to send response";
        }

    } catch (err) {
        console.error(err);
        document.getElementById("status").innerHTML =
            "❌ Error sending response";
    }
}