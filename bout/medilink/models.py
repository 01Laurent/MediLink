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
    

class DoctorsDash(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    total_patients = models.IntegerField(default=0)
    active_patients = models.IntegerField(default=0)
    total_appointments = models.IntegerField(default=0)
    appointments_completed = models.IntegerField(default=0)
    appointments_canceled = models.IntegerField(default=0)
    average_patient_recovery_time = models.DurationField(null=True, blank=True)
    common_conditions = models.TextField(null=True, blank=True)
    show_upcoming_appointments = models.BooleanField(default=True)
    show_patient_summary = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard for Dr. {self.doctor.username}"