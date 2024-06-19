from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import torch
import os
# from opensoundscape.metrics import predict_multi_target_labels
from django.http import FileResponse
from .apps import MlConfig
import pandas as pd
import os.path
from glob import glob
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

        audio_file = request.FILES.getlist('audio')  # This is an instance of MIME (in-memory object)
        response_data = {
            "HEADER" : {
                    "fileName": "Summary",
                    "Lat": None,
                    "Long": None,
                    "NumFiles": None,
                    "TotalMins": None,
                    "animal": {},
                },
            "audioFiles" : {}
            }

        try:
            # Save audio file temporarily
            temp_file_path = 'tmp/'
            results_file_path = 'results/'
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            # with open(temp_file_path, 'wb') as f:
            #     f.write(audio_file.read())
            for x in range(len(audio_file)):
                # Handle each file
                with open(temp_file_path + audio_file[x].name, 'wb+') as destination:
                    for chunk in audio_file[x].chunks():
                        destination.write(chunk)
                response_data["audioFiles"][x] = {'filename': audio_file[x].name,
                                                    'animal': {},
                                                    } # to create dictionary of filenames change this line

            '''
            SAMPLE DICTIONARY RESPONSE
            {
                "HEADER": {
                    "fileName": "Summary",
                    "Lat": "1.35",
                    "Long": "103.81",
                    "NumFiles": "100",
                    "TotalMins":"532",
                    "animal": {
                        "Greater Racket-tailed Drongo_Dicrurus paradiseus": { "file": [1], "occurrences": [1] },
                        "Sunda Scops Owl_Otus lempiji": { "file": [1], "occurrences": [1] },
                        "Red Junglefowl_Gallus gallus": { "file": [2], "occurrences": [2] },
                    }
                },
                "audioFiles": {
                  "1": {
                      "fileName": "Audio 1",
                      "animal": {
                          "Greater Racket-tailed Drongo_Dicrurus paradiseus": { "0": 0.1176, "1": 0, "2": 0},
                          "Sunda Scops Owl_Otus lempiji": { "0": 0, "1": 0, "2": 0.1648}
                      }
                  },
                  "2": {
                      "fileName": "Audio 2",
                      "animal": {
                          "Red Junglefowl_Gallus gallus": { "0": 0.8262, "1": 0.1715, "2": 0},
                      }
                  },
                }
            }
            '''

            input_arg = '--i'
            input_path = temp_file_path
            output_arg = '--o'
            output_path = results_file_path
            output_file_arg = '--rtype'
            output_file_type = 'csv'

            analyze.main([input_arg, input_path, output_arg, output_path, output_file_arg, output_file_type])

            count = 0
            duration = 0
            for file in os.listdir(output_path):
                model_output = pd.read_csv(output_path + file)   # read model output csv into pd dataframe for processing
                model_output = model_output.sort_values(by='Confidence', ascending=False).drop_duplicates(subset=['Scientific name', 'Common name', 'Start (s)'])
                os.remove(output_path + file) # delete old csv
                updated_csv = model_output.to_csv(output_path + file)

                max_end_time = model_output["End (s)"].max()    # creates interval windows for each file read
                intervals = range(0, int(max_end_time) + 3, 3)
                print("1a")
                print(int(max_end_time))
                duration += int(max_end_time)
                # print("duration: ", + str(duration))

                print("01")

                for _, row in model_output.iterrows():
                    common_name = row["Common name"]
                    scientific_name = row["Scientific name"]
                    animal_key = f"{common_name}_{scientific_name}"
                    # print("01a")
                    # loop through results of each file
                    print(str(animal_key))
                    print(str(count))
                    print(response_data)
                    if str(animal_key) not in response_data["audioFiles"][count]["animal"]:
                        # print("01b")
                        response_data["audioFiles"][count]["animal"][animal_key] = {str(i // 3): 0 for i in intervals} # initialize animal detection confidence scores to 0
                    # print("01c")
                    if animal_key not in response_data["HEADER"]["animal"]:
                        # print("01d")
                        response_data["HEADER"]["animal"][animal_key] = {"file": set(), "occurrences": [0]}

                # print("02")

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
                            response_data["audioFiles"][count]["animal"][animal_key][str(i)] = confidence
                            # print("02x")
                            response_data["HEADER"]["animal"][animal_key]["occurrences"][0] += 1

                            # print("02a")

                            if count not in response_data["HEADER"]["animal"][animal_key]["file"]:
                                response_data["HEADER"]["animal"][animal_key]["file"].add(count)         # add file number to "file" : {}

                            # print("02b")

                # print("03")

                count += 1

            # print("04")
            response_data["HEADER"]["NumFiles"] = count
            m, s = divmod(duration, 60)
            h, m = divmod(m, 60)
            print("1b")
            print(h)
            print(m)
            print(s)
            total_time = f'{h:d}:{m:02d}:{s:02d}'
            print(total_time)
            response_data["HEADER"]["TotalMins"] = total_time
            # For front-end to receive
            data = {'result': response_data}

            # Clean up temp folder
            for f in os.listdir(input_path):
                os.remove(input_path + f)
            os.rmdir(input_path)
            for f in os.listdir(output_path):
                os.remove(output_path + f)
            os.rmdir(output_path)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response(data)
        return Response(data)

class PredictWithCsvView(APIView):
    permission_classes = [AllowAny]  # Allow this endpoint even without logged in user
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
