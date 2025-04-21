from flask import Flask, render_template, Response, request, jsonify
from aiortc import RTCPeerConnection, RTCSessionDescription
import cv2
import json
import uuid
import asyncio
import logging
import time
import torch
import numpy
import threading

import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from flask_socketio import SocketIO
from Logging import log_detections
from screenshotter import capture_person

app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app, cors_allowed_origins="*")
yolo_model = None

def send_alert(class_action):
    socketio.emit('Alert', {'message': class_action})
    return {"status": "Alert sent"}, 200

def load_yolo(): ## load yolo once
    """load YOLO model once"""
    global yolo_model
    if yolo_model is None:
        yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        logging.info("Yolo model loaded correctly")
    else:
        logging.info("YOLO model already loaded")

def capture_person_thread(frame):
    thread = threading.Thread(target=capture_person, args=(frame, yolo_model))
    thread.daemon = True
    thread.start()

def generate_frames():
    global yolo_model
    if yolo_model is None:
        logging.error("YOLO model is not loaded!")
        return

    camera = cv2 .VideoCapture(0)
    while True:
        start_time= time.time()
        success, frame = camera.read()
        
        if not success:
            break

       ## call logging
        rendered_frame, detection_message = log_detections(yolo_model, frame)
        capture_person(frame, yolo_model) ## screenshot classes
        if detection_message:
            send_alert(detection_message)
        ## Emit to client
        

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', rendered_frame)
        if not ret:
            continue

        frame = buffer.tobytes()            
        yield(b'--frame\r\n'b'content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elapsed_time = time.time() - start_time
        logging.debug(f"Frame generation time: {elapsed_time} seconds")

load_yolo()

@app.route('/')
def index():
    return render_template('index.html')


async def offer_async():
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()

    pc_id = "Peer connection(%s)" % uuid .uuid4()
    pc_id = pc_id[:8]

    await pc.createOffer(offer)
    await pc.setLocalDescription(offer)

    response_data = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    return jsonify(response_data)


def offer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    future = asyncio.run_coroutine_threadsafe(offer_async(), loop)
    return future.result()

@app.route('/offer', methods=['POST'])
def offer_route():
    return offer()


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)