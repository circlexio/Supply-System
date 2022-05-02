from distutils.log import error
import websocket
from supplySystem import *
import json

import asyncio
use_ip=json
ws = websocket

with open('ip.json', 'r') as f:
        ip_addresses = json.loads(f.readline())
        if len(ip_addresses['ip']) > 1:
            use_ip = ip_addresses['ip'][1]
        else:
            print("IP address not Found")
            exit(0)
            
def connect():
    global ws
    

    try:
        ws = websocket.create_connection("ws://"+ use_ip +":8015/")

    except ConnectionRefusedError:
        print("trying to reconnect...")
        ws = websocket.create_connection("ws://"+ use_ip +":8015/")


json_data = {}
sendState = {}
prevState = {}

def mainLoop():
    global ws,prevState, sendState, json_data
    setup()

    while True:
        json_data = loop()
        if(json_data != prevState):
            # print(json_data)
            prevState = json_data
            try:
                ws.send(json_data)
            except BrokenPipeError:
                print("BrokenPipeError")
                ws = websocket.create_connection("ws://"+ use_ip +":8015/")
            except ConnectionResetError:
                print("ConnectionResetError")
                ws = websocket.create_connection("ws://"+ use_ip +":8015/")


def main():
    connect()
    mainLoop()

if __name__ == "__main__":
    main()