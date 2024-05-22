from django.contrib.auth.models import AbstractUser
from django.db import models
from animals.models import Animal

class User(AbstractUser):
    email = models.EmailField(unique=True)
    level = models.IntegerField(default=1)
    identified_animals = models.ManyToManyField(Animal, blank=True, related_name='identifiers')
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username
    
 