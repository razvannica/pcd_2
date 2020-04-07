import asyncio
import json
import requests

import websockets

users = set()


async def post(message):
    r"""Posts message to Google Pub/Sub server """
    res = requests.post('http://localhost:6666/pubsub/test', json={"data": message})
    if res.ok:
        return res.json()


async def register(websocket):
    users.add(websocket)


async def unregister(websocket):
    users.remove(websocket)
    print("Client removed")


async def handle(websocket, path):
    await register(websocket)
    async for message in websocket:
        data = json.loads(message)
        if data["user"] is not None and data["mess"] is None:
            print("User connected :  ", data["user"])
            await post("User " + data["user"] + " now connected.")

        if data["mess"] is not None:
            print("Message from " + data["user"] + ":" + data["mess"])
            await post("Message from " + data["user"] + " : " + data["mess"])

    await unregister(websocket)


start_server = websockets.serve(handle, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
