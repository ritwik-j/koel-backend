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
from ml.services.birdnet import analyze
from collections import defaultdict

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
            temp_file_path = os.path.join(os.getcwd(), '\\tmp', audio_file.name)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            with open(temp_file_path, 'wb') as f:
                f.write(audio_file.read())

            input_arg = '--i'
            input_path = temp_file_path
            output_arg = '--o'
            output_path = os.path.join(os.getcwd(), audio_file.name[:-4] + '.csv')
            output_file_arg = '--rtype'
            output_file_type = 'csv' 

            analyze.main([input_arg, input_path, output_arg, output_path, output_file_arg, output_file_type])

            # print("TEMP " + temp_file_path)
            # print("IN " + input_path)
            # print("OUT " + output_path)
            
            # Clean up temp folder
            os.remove(temp_file_path)


            model_output = pd.read_csv(output_path)   # read model output csv into pd dataframe for processing
            model_output = model_output.sort_values(by='Confidence', ascending=False).drop_duplicates(subset=['Scientific name', 'Common name', 'Start (s)'])

            result = {
                "0": {
                    "fileName": "Summary",
                    "Lat": "1.35",
                    "Long": "103.81",
                    "animal": {}
                },
                "1": {
                    "fileName": audio_file.name[:-4],
                    "animal": {}
                }
            }

            max_end_time = model_output["End (s)"].max()
            intervals = range(0, int(max_end_time) + 3, 3)

            for _, row in model_output.iterrows():
                common_name = row["Common name"]
                scientific_name = row["Scientific name"]
                animal_key = f"{common_name}_{scientific_name}"

                if animal_key not in result["1"]["animal"]:
                    result["1"]["animal"][animal_key] = {str(i // 3): 0 for i in intervals}

                if animal_key not in result["0"]["animal"]:
                    result["0"]["animal"][animal_key] = {"file": [], "occurrences": [0]}

            for _, row in model_output.iterrows():
                start, end = row["Start (s)"], row["End (s)"]
                common_name = row["Common name"]
                scientific_name = row["Scientific name"]
                confidence = row["Confidence"]
                animal_key = f"{common_name}_{scientific_name}"

                for i in range(len(intervals)):
                    interval_start = intervals[i]
                    interval_end = intervals[i + 1] if i + 1 < len(intervals) else interval_start + 3
                    
                    if start < interval_end and end > interval_start:
                        result["1"]["animal"][animal_key][str(i)] = confidence
                        result["0"]["animal"][animal_key]["occurrences"][0] += 1

                        if not result["0"]["animal"][animal_key]["file"]:
                            result["0"]["animal"][animal_key]["file"] = set(result["0"]["animal"][animal_key]["file"])

                        result["0"]["animal"][animal_key]["file"].add(1)         # for multi-file processing, remove hardcoding


            data = {'scores': result}

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response(data)
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