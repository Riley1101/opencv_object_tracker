import websockets
import base64
import asyncio
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import numpy as np

PORT = 7890
print("Server listening on Port " + str(PORT))

async def stream(socket_client):
    tracker = cv2.TrackerKCF_create()
    video = cv2.VideoCapture("video.mp4")
    if not video.isOpened():
        print("INFO : Cannot open camera")
        exit()
    ok, frame = video.read()
# select frame from video
    bbox = cv2.selectROI(frame)
    ok = tracker.init(frame, bbox)
    while True:
        ok, frame = video.read()
        if not ok:
            break
        ok, bbox = tracker.update(frame)
        if ok:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2, 1)
        else:
            cv2.putText(frame, 'Error', (100, 0),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        img_str = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
        await socket_client.send(img_str);

# A set of connected ws clients
connected = set()

# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    # Add the client to the set of connected clients
    connected.add(websocket)
    while True:
        await websocket.send("Welcome to the server!")
        await stream(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn != websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        connected.remove(websocket)

# Start the server
start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
