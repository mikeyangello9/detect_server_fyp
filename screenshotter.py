import torch
from PIL import ImageGrab, ImageDraw, ImageFont
import numpy as np
import cv2
import logging
import time
from flask import Flask, jsonify, Response, request
from aiortc import RTCPeerConnection, RTCSessionDescription
import threading
import queue
import os

model = torch.hub.load("ultralytics/yolov5", "yolov5s")
screenshot_queue = queue.Queue()

def screenshot_worker():
    while True:
        frame, yolo_model = screenshot_queue.get()
        if frame is None:
            break

        results = yolo_model(frame)
        detections = results.xyxy[0]  # Get detections

        # Check if "person" or any specific class is detected
        for *box, conf, cls in detections:
            class_id = int(cls.item())
            label = yolo_model.names[class_id]
            if label == "person" or label == "vandalism" or label == "Fighting":  # Check for 'person' class
                logging.info("Person detected, taking screenshot")
                rendered_img = np.squeeze(results.render())
                annotated_img = cv2.cvtColor(rendered_img, cv2.COLOR_RGB2BGR)

                
                ## write screenshots to folder
                screenshot_folder = os.path.join("screenshots")
                os.makedirs(screenshot_folder, exist_ok=True) ## check is the folder exists

                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.jpg"
                filepath = os.path.join(screenshot_folder, filename)
                cv2.imwrite(filepath, annotated_img)


                ## create filename with timestamp
        
                logging.info(f"Screenshot saved as {filename}, to the folder {filepath}")



screenshot_thread = threading.Thread(target=screenshot_worker, daemon=True)
screenshot_thread.start()


def capture_person(frame, yolo_model):
    screenshot_queue.put((frame, yolo_model))

