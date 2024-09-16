from typing import Any
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
from .forms import AppointmentForm, DoctorAvailabilityForm, MessageForm, AppointmentRequestForm, SetAppointmentForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'notifications.html', {'notifications': notifications})

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
        
class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'inbox.html'
    content_type_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-timestamp')
        print(messages)
    
class SentMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'sent_messages.html'
    content_type_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')
    
class ComposeMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'compose_message.html'
    success_url = reverse_lazy('inbox')

    def form_valid(self, form):
        print("Form data before saving:", form.cleaned_data)
        form.instance.sender = self.request.user
        response = super().form_valid(form)
        print("Message saved with content:", form.instance.content)
        return response

def chat_view(request):
    return render(request, 'chat.html')

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
