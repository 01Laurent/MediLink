from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from medilink.models import DoctorProfile, PatientsProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            DoctorProfile.objects.create(user=instance)
        else:
            PatientsProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff:
        instance.doctorprofile.save()
    else:
        instance.patientprofile.save()