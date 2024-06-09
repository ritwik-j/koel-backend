from django.db import models

# Create your models here.
class Animal(models.Model):
    species = models.CharField(max_length = 100)
    description = models.Text