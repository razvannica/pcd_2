import asyncio
import json

import websockets

users = set()


async def notify_users():
        if users:
                message = json.dumps({"type": "users", "count": len(users)})
                await asyncio.wait([user.send(message) for user in users])


async def register(websocket):
        users.add(websocket)
        await notify_users()


async def unregister(websocket):
        users.remove(websocket)
        print("Client removed")
        #await notify_users()


async def handle(websocket, path):
        await register(websocket)
        async for message in websocket:
                #client_message = await websocket.recv()
                print("Message from client : ", message)
                await websocket.send("I can confirm I got your message!")

        await unregister(websocket)

start_server = websockets.serve(handle, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()