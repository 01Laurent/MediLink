from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from medilink.models import DoctorProfile, PatientsProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff or instance.is_superuser:
            return
        if hasattr(instance, 'role') and instance.role == 'doctor':
            DoctorProfile.objects.create(user=instance)
        else:
            PatientsProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_staff or instance.is_superuser:
        return
    if hasattr(instance, 'role') and instance.role == 'doctor':
        if hasattr(instance, 'doctorprofile'):
            instance.doctorprofile.save()
    else:
        if hasattr(instance, 'patientsprofile'):
            instance.patientsprofile.save()