from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import torch
import os
from opensoundscape.metrics import predict_multi_target_labels
from django.http import FileResponse
from .apps import MlConfig
import pandas as pd
import os.path

from glob import glob

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
        
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES.getlist('audio')  # This is an instance of MIME (in-memory object)
        file_names = []

        try:
            # Save audio file temporarily
            temp_file_path = 'tmp/'
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            # with open(temp_file_path, 'wb') as f:
            #     f.write(audio_file.read())
            for file in audio_file:
                # Handle each file
                with open(temp_file_path + file.name, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_names.append(str.strip(str(file.name)))

            # return Response({'status': 'success', 'files': response_data}) # for testing
            files_to_predict = glob(temp_file_path + '*')
            # Load from MLconfig and make predictions
            predictions = MlConfig.model.predict(files_to_predict)

            # Clean up temp folder
            # os.remove(os.path.join(os.getcwd(), temp_file_path)) # shutil.rmtree(temp_file_path, ignore_errors=True)
            for f in files_to_predict:
                os.remove(f)
            os.rmdir(temp_file_path)

            scores = predict_multi_target_labels(predictions, threshold=0.9) # filter predictions above thresh value
            scores = scores.loc[:, (scores != 0).any(axis=0)] # discard scores which are 0

            scores_df = pd.DataFrame(scores)
            scores_df.to_csv('csv_outputs.csv', sep=',')
            
            data = []
            print(files_to_predict)
            for file in files_to_predict:
                animals = scores_df.loc[file].columns.tolist()
                file_scores = scores_df.loc[file].reset_index(drop=True)
                animal_detection_dict = {}
                for animal in animals:
                    animal_scores_list = file_scores[animal].tolist()
                    if sum(animal_scores_list) > 0:
                        animal_detection_dict[animal] = animal_scores_list
                data.append({file: animal_detection_dict})
        
            print(data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data)

class PredictWithCsvView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request): 
        
        try: 
            # Save audio file temporarily
           os.path.isfile('csv_outputs.csv')


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response(data)
        return FileResponse(open('csv_outputs.csv', 'rb'), as_attachment=True)