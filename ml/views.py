from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import numpy as np
import torch
import os
from io import BytesIO
import csv
from opensoundscape.metrics import predict_multi_target_labels
from opensoundscape.metrics import predict_single_target_labels

# Create your views here
class PredictAudioView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request): 
        '''to be abstracted away'''
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio']  # This is an instance of MIME (in-memory object)

        try: 
            # Save audio file temporarily
            temp_file_path = os.path.join('/tmp', audio_file.name)
            with open(temp_file_path, 'wb') as f:
                f.write(audio_file.read())
        
            # load pretrained model
            model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', 'BirdNET',trust_repo=True)   
            
            # Make predictions
            predictions = model.predict([temp_file_path])
            
            # Clean up temp folder
            os.remove(temp_file_path)

            scores = predict_multi_target_labels(predictions, threshold=0.5) # filter predictions above thresh value
            scores = scores.loc[:, (scores != 0).any(axis=0)] # discard scores which are 0

            # print("nfnrifnri , ", type(scores), scores.columns, scores)
            data = {'scores': scores}

            # csv code
            # csv_file = BytesIO()
            # scores.to_csv(csv_file, sep=',')

            # Get CSV content
            # csv_content = csv_file.getvalue()
            # print(csv_content, "hfirfo9828")
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)