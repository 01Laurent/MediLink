from django.contrib import admin
from .models import DoctorProfile, PatientsProfile, DoctorsDash, DoctorAvailability, Appointment, Message

# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientsProfile)
admin.site.register(DoctorsDash)
admin.site.register(DoctorAvailability)
admin.site.register(Appointment)
admin.site.register(Message)
