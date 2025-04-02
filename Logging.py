import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_detections(loaded_model,frame):
   

    results = loaded_model(frame)
    detections = results.pred[0]

    if detections is not None:
        for *box, conf, cls in detections:
            class_id  = int(cls.item())
            label = loaded_model.names[class_id]

            if label == "person":
                logging.info("person detected!");

    rendered_frame = np.squeeze(results.render())
    return rendered_frame