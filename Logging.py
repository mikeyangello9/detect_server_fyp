import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_detections(loaded_model,frame):
   

    results = loaded_model(frame)
    detections = results.pred[0]
    message = None

    if detections is not None and len(detections) > 0:
        for *box, conf, cls in detections:
            class_id  = int(cls.item())
            label = loaded_model.names[class_id]

            if label == "person":
                message = "person detected!"
            elif label == "vandalism":
                message = "Vandals detected!"
            elif label == "Fighting":
                message = "fighting detected!"

            if message:
                logging.info(message)
                break
            
           

    rendered_frame = np.squeeze(results.render())
    return rendered_frame, message