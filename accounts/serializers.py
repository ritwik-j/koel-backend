from rest_framework import serializers
from .models import User
from animals.serializers import AnimalSerializer

class UserSerializer(serializers.ModelSerializer):
    identified_animals = AnimalSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'level', 'identified_animals','friends']