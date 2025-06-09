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
