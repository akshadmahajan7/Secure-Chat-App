# 🔐 Secure Chat Application with End-to-End Encryption

---

## 🌟 Project Overview

This project is a secure, real-time messaging application designed to demonstrate true End-to-End Encryption (E2EE). Unlike standard chat apps where the server might have access to message content, this application ensures that messages are encrypted on the sender's device and only decrypted on the recipient's device. The server acts merely as a relay and storage for encrypted blobs, having zero knowledge of the actual conversation content. It implements a hybrid cryptography model, combining the speed of AES for message encryption with the security of RSA for key exchange.

---

## ✨ Features and Technology Stack

| Component | Technology | Description | 
| --- | --- | --- | 
| Primary Language | $\text{Python}$ | The core backend development language. | 
| Real-Time Engine | $\text{Flask-SocketIO}$ | Enables bi-directional, low-latency communication between clients and server. | 
| Cryptography | $\text{Cryptography (Python)}$, $\text{Web Crypto API (JS)}$ | Implements RSA-2048 for key exchange and AES-GCM for message encryption. |
| Data Storage | $\text{JSON/SQLite}$ | Stores encrypted chat logs. The server never stores plaintext. | 
| User Interface | $\text{HTML/JavaScript}$ | A clean front-end handling client-side key generation and decryption. | 

---

## 🛡️ The Hybrid Encryption Strategy

The system employs a standard cryptographic handshake to ensure privacy and integrity:

_**Phase 1:**_ _Identity & Key Exchange (RSA)_ When a user joins:
* Key Generation: The client generates a completely new RSA Key Pair (Public/Private) in their browser.
* Public Key Distribution: The Public Key is sent to the server and broadcast to other users. The Private Key never leaves the user's device.

_**Phase 2:**_ _Secure Communication (AES)_ For every message sent:
1. Session Key: The sender generates a random AES symmetric key.
2. Payload Encryption: The message text is encrypted using this AES key.
3. Key Encapsulation: The AES key itself is encrypted using the recipient's RSA Public Key.
4. Transmission: The encrypted message + encrypted key are sent to the server.
5. Decryption: The recipient uses their RSA Private Key to decrypt the AES key, then uses the AES key to decrypt the message.

---

## 📁 Project Structure

```
Secure-Chat-App/
├── app/
│   ├── templates/
│   │   └── index.html         # Chat interface & Client-side crypto logic.
│   ├── main.py                # Flask-SocketIO server entry point.
│   └── storage/
│       └── chat_logs.json     # Encrypted logs storage.
├── utils/
│   └── crypto_helpers.py      # Server-side validation helpers.
├── requirements.txt           # Python dependencies.
├── README.md                  # Project documentation.
└── LICENSE                    # License file.
```

---

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
*  $\text{Python 3.8+}$
*  $\text{pip}$ (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/your-username/Secure-Chat-App.git](https://github.com/your-username/Secure-Chat-App.git)
cd Secure-Chat-App
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask-SocketIO server:
```bash
python app/main.py
```

2. Access the App:
Open your browser at `http://127.0.0.1:5000/`.

_Tip: Open the URL in two different windows (or Incognito mode) to simulate two distinct users interacting._

---

## 🤝 Contributing

We value contributions! If you want to make this chat app even more secure, consider tackling one of these tasks:

Contribution Points
* Persistence: Integrate a proper database (PostgreSQL/MongoDB) to replace the JSON file storage for encrypted logs.
* Authentication: Add a user login system (e.g., OAuth or JWT) to persist keys across sessions so users don't need new keys every refresh.
* Group Chat: Expand the AES key distribution logic to support multi-user group chats (sending the AES key encrypted with multiple RSA public keys).
* UI/UX: Enhance the index.html to show a visual indicator (like a lock icon) when a secure handshake is successfully established.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
