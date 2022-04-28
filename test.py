import asyncio
import websockets
import time
import json

json_data = {
    "pumpOn": "ON",
    "speedI": "70%",
    "speedR": "21%",
    "pressureI": "35%",
    "pressureR" : "42%"
}


async def test():
    global json_data
    async with websockets.connect('ws://localhost:8001') as websocket:
        while True:
            await websocket.send(json.dumps(json_data))
            response = await websocket.recv()
            time.sleep(1)
        # print(response)



asyncio.get_event_loop().run_until_complete(test())