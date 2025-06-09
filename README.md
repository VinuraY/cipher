# Cipher

Cipher is a Python-based encrypted reverse shell tool composed of three components:  
- **Victim** — connects to the proxy and executes commands  
- **Listener** — sends commands and receives output  
- **Proxy** — acts as a bridge between victim and listener  

Communication is secured using RSA and AES encryption, ensuring that all data transmitted is confidential and tamper-proof.

---

## Features

- Strong RSA and AES encryption for secure communication  
- Uses WebSockets and TCP for connections  
- Supports remote command execution on the victim machine  
- Simple and lightweight implementation  

---

## Requirements

- Python 3.8+  
- `pycryptodome` library  
- `websockets` library  
- `asyncio` (built-in)  

Install dependencies using:

```bash
pip install pycryptodome websockets
```
---
## Usage

### 1. Start the proxy server
```bash
python proxy.py
```

### 2. Start the listener
```bash
python listener.py
```

### 3. Start the victim
```bash
python victim.py
```

---
## Important Notes

- This tool is for authorized and educational use only.
- Use responsibly and ensure you have permission to access any target machines.
- Tested on Linux environments.

