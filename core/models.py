import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser

def generate_national_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Citizen(models.Model):
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=8, unique=True, blank=True)  
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=15)  

    def save(self, *args, **kwargs):
        
        if not self.national_id:
            self.national_id = generate_national_id()
        super(Citizen, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class DeceasedCitizen(models.Model):
    citizen = models.OneToOneField(Citizen, on_delete=models.CASCADE)  
    date_of_death = models.DateField()
    cause_of_death = models.TextField()

    def __str__(self):
        return f"{self.citizen.full_name} - Deceased"

class User(AbstractUser):    
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)   
    email = models.EmailField(unique=True, blank=True, null=True)  
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    role = models.ForeignKey('UserRole', on_delete=models.SET_NULL, null=True)  

    def __str__(self):
        return self.username

class UserRole(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True)  

    def __str__(self):
        return self.name
