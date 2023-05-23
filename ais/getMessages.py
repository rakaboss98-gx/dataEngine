import asyncio
import websockets
import json
from datetime import datetime, timezone

key = "b87ad4c6ccbb0b2365014beee52a4554e8125ab6"

async def connectToAIS():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": key,
                             "BoundingBoxes": [[
                                 [7.4377, 43.7418],
                                 [7.4163, 43.7316]
                             ]]}
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]
            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
                print(f"[{datetime.now(timezone.utc)}] \
                      ShipID: {ais_message['UserID']}\
                      Latitude: {ais_message['Latitude']}\
                      Longitude: {ais_message['Longitude']}")
                
if __name__ == "__main__":
    asyncio.run(connectToAIS())






