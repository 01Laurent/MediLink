from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Appointment, Notification

@shared_task
def send_appointment_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(appointment_date=tomorrow, status='accepted')

    for appointment in appointments:
        # Create a reminder notification
        Notification.objects.create(
            recipient=appointment.patient.user,
            message=f"Reminder: You have an appointment with Dr. {appointment.doctor.user.last_name} tomorrow at {appointment.appointment_time}."
        )