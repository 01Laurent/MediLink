from typing import Any
from django.db import models
from django.db.models import Max, Q, Count
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from medilink.models import DoctorsDash, PatientsProfile, Appointment, DoctorAvailability, Message, DoctorProfile, Notification
from .forms import AppointmentForm, DoctorAvailabilityForm, AppointmentRequestForm, SetAppointmentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def HomeView(request):
    return render(request, 'home.html')

class DocDashView(LoginRequiredMixin, TemplateView):
    template_name = 'docdash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            profile = user.doctorprofile
            context['dashboard'] = {
                'patients_treated': profile.patients_treated,
                'upcoming_appointments': profile.upcoming_appointments,
                'total_earnings': profile.total_earnings,
                'notes': profile.notes,
            }
            context['appointments'] = Appointment.objects.filter(doctor=profile)

        return context

class PatDahView(LoginRequiredMixin, TemplateView):
    template_name = 'patdash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'patientsprofile'):
            profile = user.patientsprofile

            # appointments = Appointment.objects.filter(patient=profile).order_by('-created_at')

            # context['dashboard'] = {'appointments': appointments}
            context['appointments'] = Appointment.objects.filter(patient=profile)
        return context
    
# @login_required
# @csrf_exempt
# def request_appointment_ajax(request):
#     if request.method == 'POST':
#         doctor_id = request.POST.get('doctor_id')
#         illness_description = request.POST.get('illness_description')

#         if not doctor_id or not illness_description:
#             return JsonResponse({'success': False, 'error': 'Doctor ID and illness description are required.'})

#         try:
#             doctor = DoctorProfile.objects.get(id=doctor_id)
#         except DoctorProfile.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Doctor not found.'})

#         # Create the appointment
#         appointment = Appointment.objects.create(
#             patient=PatientsProfile.objects.get(user=request.user),
#             doctor=doctor,
#             status='pending',
#             description=illness_description
#         )

#         # Send notification (optional)
#         Notification.objects.create(
#             recipient=doctor.user,
#             message=f"New appointment request from {request.user.first_name} {request.user.last_name}"
#         )

#         return JsonResponse({'success': True})

#     return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
@login_required
def request_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == 'POST':
        appointment = Appointment.objects.create(
            patient=PatientsProfile.objects.get(user=request.user),
            doctor=doctor,
            status='pending',
            # created_at = timezone.now()
        )
        Notification.objects.create(
            recipient=doctor.user,
            message=f"New appointment request from {request.user.first_name} {request.user.last_name}"
        )
        return redirect('appointment_confirmation')
        # form = AppointmentRequestForm(request.POST)
        # if form.is_valid():
    #         appointment = form.save(commit=False)
    #         appointment.patient = PatientsProfile.objects.get(user=request.user)
    #         appointment.doctor = doctor
    #         appointment.status = 'pending'
    #         appointment.save()
    #         return redirect('appointment_confirmation')
    # else:
    #         form = AppointmentRequestForm()

    return render(request, 'request_appointment.html', {'doctor': doctor})
    
@login_required
def manage_appointments(request):
    if hasattr(request.user, 'doctorprofile'):
        doctor = request.user.doctorprofile
        appointments = Appointment.objects.filter(doctor=doctor)

        return render(request, 'docdash.html', {'appointments': appointments})
    return redirect('home')

@login_required
def respond_to_appointment(request, appointment_id, response):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user !=appointment.doctor.user:
        return redirect('home') # ntaeka message ya you are not a doctor
    if response == 'accept':
        if request.method == 'POST':
            form = SetAppointmentForm(request.POST, instance=appointment)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.status = 'accepted'
                appointment.save()

                Notification.objects.create(
                    recipient=appointment.patient.user,
                    message=f"Your appointment with Dr. {appointment.doctor.user.last_name} has been accepted."
                )
                return redirect('doc_dashboard')
        else:
            form = SetAppointmentForm(instance=appointment)
        return render(request, 'set_appointment.html', {'form': form, 'appointment': appointment})
    elif response == 'reject':
        appointment.reject()
        Notification.objects.create(
            recipient=appointment.patient.user,
            message=f"Your appointment with Dr. {appointment.doctor.user.last_name} has been rejected."
        )
        return redirect('doc_dashboard')

@login_required
def patient_appointments(request):
    appointments = request.user.appointments.all()
    return render(request, 'patient_appointments.html', {'appointments': appointments})

def appointment_confirmation(request):
    return render(request, 'appointment_confirmation.html')

def update_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        if 'rating' in request.POST:
            appointment.is_treated = True
            appointment.rating = int(request.POST.get('rating'))
            appointment.save()
        
        if 'not_treated_reason' in request.POST:
            appointment.is_not_treated = True
            appointment.not_treated_reason = request.POST.get('not_treated_reason')
            appointment.save()

        return redirect('pat_dashboard')
    return redirect('pat_dashboard')

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    unread_count = notifications.count()
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_view')

    
class ScheduleAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'schedule_appointment.html'
    success_url = reverse_lazy('pat_dashboard')

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)
    
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user)
        elif user.is_patient:
            return Appointment.objects.filter(patient=user)
        else:
            return Appointment.objects.none()
        
def home(request):
    specialty = request.GET.get('specialty', '')
    location = request.GET.get('location', '')
    availability = request.GET.get('availability', '')

    doctors = DoctorProfile.objects.all()

    if specialty :
        doctors = doctors.filter(specialty__icontains=specialty )

    if location:
        doctors = doctors.filter(location__icontains=location)

    if availability == 'available':
        doctors = doctors.filter(is_available=True)
    elif availability == 'not_available':
        doctors = doctors.filter(is_available=False)
    results = list(doctors.values('id', 'user__first_name', 'user__last_name', 'specialty', 'location', 'is_available'))
    return JsonResponse({'doctors': results})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Message, User

@login_required
def chat_inbox(request):
    recipient_id = request.GET.get('recipient')
    recipient = User.objects.filter(id=recipient_id).first() if recipient_id else None

    # Search for users by username if there's a search query
    search_query = request.GET.get('search', '')

    if search_query:
        # Filter users by username that contains the search query, excluding the logged-in user
        senders = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    else:
        # Get list of users who have sent or received messages with the logged-in user
        senders = User.objects.filter(
            Q(sent_messages__recipient=request.user) | Q(received_messages__sender=request.user)
        ).distinct()

    # Fetch chat messages with the selected recipient (if any)
    if recipient:
        # Fetch messages between the current user and the recipient
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=request.user))
        ).order_by('timestamp')

        # If a message is posted, save it to the database
        if request.method == 'POST':
            message_content = request.POST.get('message')
            if message_content:
                Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    content=message_content
                )
            return redirect('chat_inbox')  # Redirect to avoid form resubmission

        # Generate room name based on usernames (e.g., "user1_user2")
        room_name = f"{request.user.username}_{recipient.username}"

    else:
        messages = []
        room_name = None  # No room selected if no recipient

    context = {
        'senders': senders,
        'messages': messages,
        'recipient': recipient,
        'room_name': room_name,  # Pass the room name to the template for WebSocket connection
        'search_query': search_query,  # Keep the search query populated in the input
    }

    return render(request, 'inbox.html', context)


# @login_required
# def chat_inbox(request):
#     # Get the latest message for each unique sender for the logged-in user
#     latest_messages = Message.objects.filter(recipient=request.user) \
#         .values('sender') \
#         .annotate(latest_timestamp=Max('timestamp'))

#     # Fetch the actual message objects for the latest messages
#     senders = Message.objects.filter(
#         recipient=request.user,
#         timestamp__in=[msg['latest_timestamp'] for msg in latest_messages]
#     ).order_by('-timestamp')

#     # Handle recipient selection
#     recipient_id = request.GET.get('recipient')
#     recipient = None
#     messages = []

#     if recipient_id:
#         recipient = get_object_or_404(User, id=recipient_id)
#         messages = Message.objects.filter(
#             (Q(sender=request.user, recipient=recipient) | 
#              Q(sender=recipient, recipient=request.user))
#         ).order_by('timestamp')

#     # Count unread messages for each sender
#     senders = senders.annotate(
#         unread_count=Count('id', filter=Q(recipient=request.user, read=False))
#     )

#     context = {
#         'senders': senders,
#         'recipient': recipient,
#         'messages': messages,
#     }

#     return render(request, 'inbox.html', context)