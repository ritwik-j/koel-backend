from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# Create your views here.

class PredictView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    
    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request):
        # p=Prediction()
        # response_dict=p.predict(request)
        # response_data=response_dict['response']

        # basic helloworld response        
        data = {'message': 'Hello post world!'}
        return Response(data)