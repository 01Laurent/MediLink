from django.contrib import admin
from .models import DoctorProfile, PatientsProfile, DoctorsDash

# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientsProfile)
admin.site.register(DoctorsDash)
