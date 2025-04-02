import logging
import cv2
import torch
import numpy as np


## configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def testLogging():

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    logging.info("Yolo model loaded correctly")      

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        logging.error("failed to open webcam")
        return
    
    while True:
        success, frame = camera.read()
        
        if not success:
            logging.error("failed to capture frame")
            break

        # Run YOLOv5 detection
        results = model(frame)
        detections = results.pred[0]

        if detections is not None:
            for *box, conf, cls in detections:
                class_id  = int(cls.item())
                label = model.names[class_id]

                if label == "person":
                    logging.info("person detected!");

        cv2.imshow("Yolov5 detection", np.squeeze(results.render()))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
       
       
testLogging()