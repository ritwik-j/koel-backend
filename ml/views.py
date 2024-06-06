from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import numpy as np
import torch
import os

# Create your views here
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
            # Save file temporarily
            temp_file_path = os.path.join('/tmp', audio_file.name)
            with open(temp_file_path, 'wb') as f:
                f.write(audio_file.read())
        
            # load model
            model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', 'BirdNET',trust_repo=True)   
            
            # Make predictions
            predictions = model.predict([temp_file_path])
            print(predictions)
            
            # Clean up - delete the temporary file
            os.remove(temp_file_path)
            
            data = {'predictions': predictions}
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get CSV content
        # csv_content = csv_file.getvalue()
        
        # Create response with CSV content
        # response = Response(content=csv_content, media_type="text/csv")
        # response.headers["Content-Disposition"] = "attachment; filename=sample.csv"
        
        return Response(data)
        

