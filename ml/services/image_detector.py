import os
import pickle
import json
from rest_framework import status 

from ultralytics import YOLO

base_path = os.getcwd() 
pickle_path=os.path.normpath(base_path+os.sep+'pickle')
log_path=os.path.normpath(base_path+os.sep+'log')

# Load a model
model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model

# save pickled model
pickle_file = os.path.normpath(pickle_path+os.sep+'model.sav')
model.dump(model, open(pickle_file, 'wb'))

'''
# Run batched inference on a list of images
results = model(["./input/test_img.jpeg"])  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="./output/result.jpeg")  # save to disk

'''