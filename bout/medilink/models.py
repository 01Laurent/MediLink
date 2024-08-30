from django.db import models
from django.db import models
from django.contrib.auth.models import User
# from django.urls import reverse
from datetime import datetime, date


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    education = models.CharField(max_length=150)
    experience = models.CharField(max_length=10)
    clinics_worked = models.TextField()

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} {self.speciality}"
    
class PatientsProfile(models.Model):
    contact = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField
    medical_history = models.TextField()
    medications = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"