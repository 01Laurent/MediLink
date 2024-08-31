from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .forms import DoctorRegistrationForm, PatientRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from medilink.models import DoctorProfile, PatientsProfile
from django.contrib.auth import login
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            return reverse_lazy('doc_dashboard')
        elif hasattr(user, 'patientsprofile'):
            return reverse_lazy('pat_dashboard')
        return reverse_lazy('home')

class DoctorRegisterView(generic.CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'registration/register_doctor.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        DoctorProfile.objects.create(
            user=user,
            contact=form.cleaned_data['contact'],
            speciality=form.cleaned_data['speciality'],
            license_number=form.cleaned_data['license_number'],
            education=form.cleaned_data['education'],
            experience=form.cleaned_data['experience'],
            clinics_worked=form.cleaned_data['clinics_worked']
        )
        login(self.request, user)
        return super().form_valid(form)
    
class PatientRegisterView(generic.CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'registration/register_patient.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        PatientsProfile.objects.create(
            user=user,
            contact=form.cleaned_data['contact'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            medical_history=form.cleaned_data['medical_history'],
            medications=form.cleaned_data['medications']
        )
        login(self.request, user)
        return super().form_valid(form)

