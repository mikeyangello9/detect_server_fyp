import torch
from PIL import ImageGrab, ImageDraw, ImageFont
import numpy as np
import cv2
import logging
import time
from flask import Flask, jsonify, Response, request
from aiortc import RTCPeerConnection, RTCSessionDescription
import threading

model = torch.hub.load("ultralytics/yolov5", "yolov5s")

def capture_and_annotate():
    im = ImageGrab.grab() # grabs the whole screen

    results = model(im) # inferanceon captured image
    rendered_img = np.squeeze(results.render())
    annotated_img = cv2.cvtColor(rendered_img, cv2.COLOR_RGB2BGR)

    cv2.imwrite('caught in 4k', annotated_img) # save images loosely
    cv2.imshow("Screenshot with Labels", annotated_img)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()




def capture_person(frame, yolo_model):
    im = ImageGrab.grab()

    # Inference on the captured image
    results = yolo_model(frame)
    detections = results.xyxy[0]  # Get detections

    # Check if "person" or any specific class is detected
    for *box, conf, cls in detections:
        class_id = int(cls.item())
        label = yolo_model.names[class_id]
        if label == "person":  # Check for 'person' class
            logging.info("Person detected, taking screenshot")
            rendered_img = np.squeeze(results.render())
            annotated_img = cv2.cvtColor(rendered_img, cv2.COLOR_RGB2BGR)


            ## save screenshot
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_img)
            logging.info(f"Screenshot saved as {filename}")
            ## display screenshot
            cv2.imshow("Detected", annotated_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


