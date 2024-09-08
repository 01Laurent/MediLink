from django.db import models
from django.db import models
from django.contrib.auth.models import User
# from django.urls import reverse
from datetime import datetime, date
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date

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
    date_of_birth = models.DateField()
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

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor} on {self.appointment_date} at {self.appointment_time}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    encrypted_content = models.TextField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None and self.content: 
            fernet = Fernet(settings.ENCRYPTION_KEY)
            self.encrypted_content = fernet.encrypt(self.content.encode()).decode()
        #     self.content = None
        # elif self.pk and self.encrypted_content and not self.content:
        #      fernet = Fernet(settings.ENCRYPTION_KEY)
        #      self.content = fernet.decrypt(self.encrypted_content.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_content(self):
        if self.encrypted_content:
            fernet = Fernet(settings.ENCRYPTION_KEY)
            return fernet.decrypt(self.encrypted_content.encode()).decode()
        return self.content

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"