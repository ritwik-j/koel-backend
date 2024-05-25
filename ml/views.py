from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from PIL import Image
import numpy as np
import cv2
import torch

from ultralytics import YOLO

# Create your views here.

class PredictView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request):
        # p=Prediction()
        # response_dict=p.predict(request)
        # response_data=response_dict['response']

        '''Later to be abstracted away'''
        # passing image to model trial
        if 'image' not in request.FILES:
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']  # This is an instance of MIME
        
        try: 
            image = Image.open(image_file) # Use PIL to open image
            image_np = np.array(image)  # Convert PIL to np array. 
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model
            results = model(image_bgr) # np array is a valid source for model. check np shape (640,640,3)

            # Process results list
            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs
                masks = result.masks  # Masks object for segmentation masks outputs
                keypoints = result.keypoints  # Keypoints object for pose outputs
                probs = result.probs  # Probs object for classification outputs
                obb = result.obb  # Oriented boxes object for OBB outputs
                result.show()
                # result.save(filename="result.jpeg")  # save to disk
            
            data = {'message': 'Image detection complete'}

        except Exception as e:
            data = {'message': 'Image detection failed'}
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(data)