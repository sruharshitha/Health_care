🔐 AI-Based Secure Device Communication using Blockchain & IPFS


📌 Overview
This project presents a secure and decentralized system for device-to-device communication by integrating Blockchain (Ethereum) and IPFS for data integrity and storage. It ensures secure transmission using cryptographic techniques and enhances reliability with AI-based anomaly detection.
________________________________________
🚀 Key Features
•	🔗 Decentralized Communication using Ethereum Blockchain
•	📦 Distributed Storage with IPFS
•	🔐 Secure Key Exchange using Elliptic Curve Diffie-Hellman (ECDH)
•	🔒 Data Encryption using AES for secure transmission
•	🤖 AI-Based Anomaly Detection using Isolation Forest
•	✅ Data Integrity & Verification via blockchain hashing
•	🌐 REST API Support using Flask
________________________________________
🧭 Methodology
The system follows a secure, layered approach combining cryptography, decentralized storage, and AI monitoring:
1.	Session Initialization
o	Devices authenticate and establish a secure session using ECDH key exchange.
2.	Key Derivation
o	A shared secret is derived and converted into a symmetric key for encryption.
3.	Secure Transmission
o	Data is encrypted using AES before transmission.
4.	Decentralized Storage
o	Encrypted data is uploaded to IPFS, generating a unique content hash.
5.	Blockchain Registration
o	The IPFS hash is stored on the Ethereum blockchain for immutable verification.
6.	Verification & Retrieval
o	Receiver retrieves data from IPFS and verifies integrity using the blockchain hash.
7.	Anomaly Detection
o	Communication patterns are analyzed using Isolation Forest to detect malicious activity in real time.
________________________________________
🏗️ System Architecture
+-----------+        +------------------+        +-------------+
|  Device A | -----> |   Flask Backend  | -----> |    IPFS     |
+-----------+        |  (API Layer)     |        +-------------+
       |             |   |          |    |              |
       |             |   |          |    |              v
       |             |   |          |----|----> +----------------+
       |             |   |          |           |  Ethereum      |
       |             |   |          |           |  Blockchain    |
       |             |   v          v           +----------------+
       |             | Crypto    ML Module
       |             |(ECDH/AES) (Isolation Forest)
       v             +------------------+
+-----------+
|  Device B |
+-----------+
🔄 Workflow Summary
•	Devices communicate via secure APIs
•	Encryption handled by cryptographic module
•	Storage handled by IPFS
•	Integrity ensured via blockchain
•	Security monitored by AI model
________________________________________


## ▶️ Execution Steps

### Step 1: Start Blockchain (Hardhat)
```bash
cd hardhat
npx hardhat node
Step 2: Deploy Smart Contract
npx hardhat run scripts/deploy.js --network localhost
Copy the contract address and update it in the project.
Step 3: Start IPFS at both sender and receiver side
ipfs daemon
Step 4: Run Sender Side
python add_patient.py
Step 5: Run Receiver Side
python main.py
Step 6: Start Web Server
python web_server.py
🧠 AI Component
•	Implemented Isolation Forest for anomaly detection
•	Detects abnormal or malicious communication patterns
•	Enables real-time monitoring of data transmission behavior
________________________________________
🔐 Security Design
•	Confidentiality: AES encryption protects transmitted data
•	Integrity: Blockchain-stored IPFS hashes prevent tampering
•	Authentication: ECDH ensures secure session establishment
•	Anomaly Detection: AI identifies suspicious communication patterns
________________________________________
🛠️ Tech Stack
•	Programming: Python
•	Backend: Flask (REST APIs)
•	Blockchain: Ethereum
•	Storage: IPFS
•	Machine Learning: Scikit-learn (Isolation Forest)
•	Cryptography: ECDH, AES
________________________________________
📂 Project Structure
├── app.py                # Main Flask application
├── blockchain/          # Ethereum interaction scripts
├── ipfs/                # IPFS integration
├── crypto/              # Encryption (ECDH, AES)
├── ml_model/            # Isolation Forest model
├── routes/              # API endpoints
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
________________________________________
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/project-name.git
cd project-name
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the application
python app.py
________________________________________
🔌 API Endpoints (Sample)
•	POST /send-data → Securely send encrypted data
•	GET /verify-data → Verify data integrity using blockchain
•	POST /detect-anomaly → Analyze communication data
________________________________________
📊 Use Cases
•	Secure IoT device communication
•	Smart city infrastructure
•	Healthcare data transmission
•	Industrial automation systems
________________________________________
⚡ Performance & Scalability Notes
•	IPFS reduces centralized storage bottlenecks
•	Blockchain ensures trust without centralized authority
•	System can scale with additional nodes and distributed devices
________________________________________
🎯 Future Enhancements
•	Integration with cloud deployment (AWS/GCP)
•	Real-time dashboard for anomaly monitoring
•	Support for additional blockchain networks
•	Improved AI models for adaptive threat detection
________________________________________
👤 Author
•	sruharshitha
•	Email: sruharshitha@gmail.com
________________________________________
⭐ Acknowledgements
This project was developed as part of academic research to explore secure and intelligent communication systems using emerging technologies.

