# Import the necessary modules for asynchronous operations, WebSockets, JSON parsing, and datetime operations
import asyncio
import websockets
import json
from datetime import datetime, timezone

# Import the 'extractBBox' function from the 'aisUtils' module
from aisUtils import extractBBox

# Define the path to the configuration file
configFilePath = "testExamples/config.json"

# Open and load the JSON configuration file
with open(configFilePath) as f:
    configFile = json.load(f)

# Define an asynchronous function to connect to the AIS stream
async def connectToAIS():
    
    # Open a WebSocket connection to the AIS stream service
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        
        # Open the GeoJSON file specified in the configuration file and extract the bounding boxes
        with open(configFile["pathToGeoJson"]) as f:
            bboxList = extractBBox(f)
            
        # Define the subscription message to be sent to the AIS stream service
        subscribe_message = {
            "APIKey": configFile["aistreamKey"],  # API key from the configuration file
            "BoundingBoxes": bboxList  # List of bounding boxes extracted from the GeoJSON file
        }

        # Convert the subscription message into a JSON formatted string
        subscribe_message_json = json.dumps(subscribe_message)

        # Send the subscription message to the AIS stream service over the WebSocket connection
        await websocket.send(subscribe_message_json)

        # Continuously listen for new messages from the AIS stream service
        async for message_json in websocket:

            # Convert each incoming message from a JSON formatted string into a Python dictionary
            message = json.loads(message_json)
            
            # Extract the message type from the message
            message_type = message["MessageType"]

            # If the message type is "PositionReport", process the AIS message
            if message_type == "PositionReport":
                
                # Extract the AIS message from the incoming message
                ais_message = message['Message']['PositionReport']
                
                # Print the current time (in UTC), the ship's ID, and its latitude and longitude
                print(f"[{datetime.now(timezone.utc)}] \
                      ShipID: {ais_message['UserID']}\
                      Latitude: {ais_message['Latitude']}\
                      Longitude: {ais_message['Longitude']}")

# If this script is the main program, run the 'connectToAIS' function within an asyncio event loop
if __name__ == "__main__":
    asyncio.run(connectToAIS())