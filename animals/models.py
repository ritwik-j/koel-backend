from django.db import models

# Create your models here.
class Animal(models.Model):
    SPECIES_TYPES= (
        ('bird','Bird'),
        ('insect', 'Insect'),
    )

    species_type = models.CharField(max_length=50, choices=SPECIES_TYPES)
    species_name = models.CharField(max_length=100)
    description = models.TextField()
    habitat = models.CharField(max_length = 100)
    size = models.CharField(max_length=50)
    extinction_status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.species_name
