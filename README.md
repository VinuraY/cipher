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
### Version 2 Updates
---

### 🔧 **Cipher Reverse Shell – New Capabilities**

The latest updates to the `cipher` tool have significantly improved its performance, scalability, and stealth. Below are the **newly added features**:

---

#### ⚡ 1. **Asynchronous Multi-Victim Handling**

* Fully asynchronous architecture using `asyncio`.
* Supports **simultaneous control of multiple victims**, each managed as independent sessions.

#### 🔁 2. **Proxy Relay Channel**

* Introduced a **dedicated `proxy.py`** component to act as a **relay server**.
* Victims now communicate through the proxy, enabling:

  * Layered anonymity
  * Internal network pivoting
  * Evasion of IP-based filtering

#### 🧬 3. **Encrypted Data Transport (XOR + JSON)**

* All communication between components is now:

  * **XOR-encrypted** with a shared secret key
  * Encapsulated in **JSON payloads**
* Provides basic obfuscation against traffic inspection and packet-based detection.

#### 🛰️ 4. **Victim Metadata Broadcasting**

* Victims automatically transmit key telemetry data such as:

  * Hostname
  * IP address
  * System details (e.g., OS info, privilege level)
* Data is displayed on the listener’s console in real time.

#### 🧪 5. **Improved Command Execution Flow**

* Commands sent from the listener are now:

  * **Queue-based and non-blocking**
  * Cleanly parsed and returned from the victim
* Prevents command backlog or data corruption in noisy networks.

#### 🔄 6. **Heartbeat & Auto-Reconnect**

* Victims now **auto-reconnect** on disconnect, with retry intervals.
* Proxy and listener track **session health** via heartbeat checks.

#### ⚙️ 7. **Structured Component Separation**

* Codebase refactored into clean, modular components:

  * `listener.py`
  * `victim.py`
  * `proxy.py`
* Easier to debug, extend, and maintain.

---

