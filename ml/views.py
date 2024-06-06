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
import librosa
import io
from io import StringIO
from io import BytesIO
import pydub
import os

from opensoundscape.audio import Audio
from opensoundscape.metrics import predict_multi_target_labels
from opensoundscape.metrics import predict_single_target_labels
from ultralytics import YOLO

# Create your views here.

def convert_to_mp3(y, sr):
        # Convert the audio time series to a pydub AudioSegment
        audio = pydub.AudioSegment(
            y.tobytes(), 
            frame_rate=sr,
            sample_width=y.dtype.itemsize, 
            channels=1  # Assuming mono; set to 2 for stereo
        )

        # Export the AudioSegment to an MP3 bytes buffer
        mp3_buffer = BytesIO()
        audio.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)
        
        return mp3_buffer

class PredictAudioView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request): 
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio']  # This is an instance of MIME (in-memory object)

        try: 
            # Save the file temporarily
            temp_file_path = os.path.join('/tmp', audio_file.name)
            with open(temp_file_path, 'wb') as f:
                f.write(audio_file.read())
            
            print(temp_file_path)
            
            # Load the audio file using OpenSoundscape
            # audio = Audio.from_file(temp_file_path)

            # load model
            model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', 'BirdNET',trust_repo=True)   
            # Make predictions
            predictions = model.predict([temp_file_path])
            print(predictions)
            
            # Clean up - delete the temporary file
            # os.remove(temp_file_path)
            
            # data = {'predictions': predictions}
            data = {'predictions': 'hi'}
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        # try: 
        #     audio_data = io.BytesIO(audio_file.read())  # Read the file into a BytesIO object

        #     # Use librosa to load the audio from the BytesIO object
        #     audio, sr = librosa.load(audio_data, sr=None)
        #     audio_mp3 = convert_to_mp3(audio, sr)
        #     data = {'message': 'read audio to librosa'}

        #     model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', 'BirdNET',trust_repo=True)   # load model
        #     data = {'message': 'next- predict'}

        #     # predictions = model.predict([audio_mp3]) # predict on the model's classes

        #     # print(predictions)

        #     # scores = predict_multi_target_labels(predictions, threshold=0.5) # filter predictions to confirm positive detections using threshold
        #     # data = {'message': 'scores thingy'}
        #     # scores = scores.loc[:, (scores != 0).any(axis=0)] # discard scores which are 0
        #     # # print(scores.head()) # for testing
        #     # csv_file = StringIO()
        #     # scores.to_csv(csv_file, sep=',') # convert to a csv file to save
                        
        # except Exception as e:
        #     data = {'message': 'Image detection failed'}
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get CSV content
        # csv_content = csv_file.getvalue()
        
        # Create response with CSV content
        # response = Response(content=csv_content, media_type="text/csv")
        # response.headers["Content-Disposition"] = "attachment; filename=sample.csv"
        
        return Response(data)
        

class PredictImageView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request):
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
                # result.show()
                result.save(filename="./ml/services/output/result.jpeg")  # save to disk
            
            data = {'message': 'Image detection complete'}

        except Exception as e:
            data = {'message': 'Image detection failed'}
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(data)