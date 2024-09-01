from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DoctorsDash, PatientsProfile, Appointment, DoctorAvailability
from .forms import AppointmentForm, DoctorAvailabilityForm


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
        return context

class PatDahView(LoginRequiredMixin, TemplateView):
    template_name = 'patdash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'patientsprofile'):
            profile = user.patientsprofile
            context['dashboard'] = {
                
            }
        return context
    
class ScheduleAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'schedule_appointment.html'
    success_url = reverse_lazy('pat_dashboard')

    def form_valid(self, form):
        form.instance.patient = self.request.user
        return super().form_valid(form)
    
class DoctorAvailabilityView(CreateView):
    model = DoctorAvailability
    form_class = DoctorAvailabilityForm
    template_name = 'doctor_availability.html'
    success_url = reverse_lazy('doc_dashboard')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
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