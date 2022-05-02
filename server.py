#!/usr/bin/env python

import asyncio

import websockets


connected = set()

async def handler(websocket):
    connected.add(websocket)

    try:
        async for message in websocket:
            for conn in connected:
                await conn.send(message)
    finally:
        connected.remove(websocket)


    # while True:
    #     message = await websocket.recv()
    #     print(message)


async def main():
    async with websockets.serve(handler, host="0.0.0.0", port=8015):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())