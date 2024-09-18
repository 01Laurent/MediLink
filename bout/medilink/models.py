from django.db import models
from django.db import models
from django.contrib.auth.models import User
# from django.urls import reverse
from datetime import datetime, date
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    contact = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    location = models.CharField(max_length=100,)
    is_available = models.BooleanField(default=True)
    license_number = models.CharField(max_length=50, unique=True)
    education = models.CharField(max_length=150)
    experience = models.CharField(max_length=10)
    clinics_worked = models.TextField()

    patients_treated = models.IntegerField(default=0)
    upcoming_appointments = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} {self.specialty}"
User.add_to_class(
    'is_doctor', 
    property(lambda u: DoctorProfile.objects.filter(user=u).exists())
)

class PatientsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=False)
    medical_history = models.TextField()
    medications = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
User.add_to_class('is_patient', property(lambda u: hasattr(u, 'patientsprofile')))
    
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
    

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor} - {self.day} {self.start_time}-{self.end_time}"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    patient = models.ForeignKey(PatientsProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_treated = models.BooleanField(default=False)
    is_not_treated = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    not_treated_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} on {self.appointment_date}"
    def accept(self):
        self.status = 'accepted'
        self.save()
    def reject(self):
        self.status = 'rejected'
        self.save()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.timestamp}"
    def mark_as_read(self):
        self.read = True
        self.save()

    class Meta:
        ordering = ['-timestamp']