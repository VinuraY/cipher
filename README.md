# 🔐 Cipher — Encrypted Reverse Shell Framework

Cipher is a Python-based encrypted reverse shell tool composed of three components:

- **Victim** — connects to the proxy via WebSocket, executes commands, and sends encrypted results.  
- **Listener** — connects to the proxy via TCP, sends encrypted commands, and receives decrypted output.  
- **Proxy** — acts as a bridge between victim and listener, relaying encrypted data using WebSocket (victim side) and TCP (listener side).

Communication is secured using strong RSA (2048-bit) and AES-GCM (128-bit) encryption, ensuring confidentiality and tamper-proof data transmission.

---

## 🧩 Features

- Hybrid RSA + AES encryption for secure key exchange and fast symmetric encryption  
- Forward secrecy: a unique AES key is generated per session  
- Uses WebSockets and TCP for flexible connections  
- Modular design for easy maintenance and extension  
- Lightweight and simple to deploy  
- Supports remote command execution on victim machines  

---

## ⚙️ How It Works

1. Victim connects to the proxy via WebSocket.  
2. Listener connects to the proxy via TCP.  
3. RSA public keys are exchanged between listener and victim.  
4. Listener sends an AES key encrypted with the victim's public key.  
5. All further communication is encrypted with AES-GCM using the shared AES key.  
6. Listener sends commands → Victim executes → Encrypted results are sent back.

---

## 📦 Requirements

- Python 3.8 or higher  
- `pycryptodome` library  
- `websockets` library
- `psutil` library
- `platform` library 
- `asyncio` (built-in with Python)  

Install dependencies via pip:

```bash
pip install pycryptodome websockets psutil platform
```
---
## ⚠️ Important Notes

- This tool is for authorized and educational use only.
- Use responsibly and ensure you have permission to access any target machines.
- Tested on Linux environments.

---
