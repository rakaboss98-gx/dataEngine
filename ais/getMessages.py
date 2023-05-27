# Import the necessary modules for asynchronous operations, WebSockets, JSON parsing, and datetime operations
import asyncio
import websockets
import json
from datetime import datetime, timezone

# Import the 'extractBBox' function from the 'aisUtils' module
from aisUtils import extractBBox

class AISStreamer:
    def __init__(self, configFilePath):
        # Define the path to the configuration file and load it
        with open(configFilePath) as f:
            self.configFile = json.load(f)
        
        # Open the GeoJSON file specified in the configuration file and extract the bounding boxes
        with open(self.configFile["pathToGeoJson"]) as f:
            self.bboxList = extractBBox(f)
    
    # Define an asynchronous method to connect to the AIS stream
    async def connectToAIS(self):
        # Open a WebSocket connection to the AIS stream service
        async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
            
            # Define the subscription message to be sent to the AIS stream service
            subscribe_message = {
                "APIKey": self.configFile["aistreamKey"],  # API key from the configuration file
                "BoundingBoxes": self.bboxList  # List of bounding boxes extracted from the GeoJSON file
            }

            # Convert the subscription message into a JSON formatted string
            subscribe_message_json = json.dumps(subscribe_message)

            # Send the subscription message to the AIS stream service over the WebSocket connection
            await websocket.send(subscribe_message_json)

            # Continuously listen for new messages from the AIS stream service
            async for message_json in websocket:
                # Convert each incoming message from a JSON formatted string into a Python dictionary
                message = json.loads(message_json)
                
                # Print each incoming message
                print(message)

# If this script is the main program, create an instance of the AISStreamer class and run the 'connectToAIS' method within an asyncio event loop
if __name__ == "__main__":
    streamer = AISStreamer("testExamples/config.json")
    asyncio.run(streamer.connectToAIS())
