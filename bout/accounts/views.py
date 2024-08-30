from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .forms import SignUpForm, DoctorRegistrationForm, PatientRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from medilink.models import DoctorProfile, PatientsProfile
from django.contrib.auth import login


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class DoctorRegisterView(generic.CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'registration/register_doctor.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        DoctorProfile.objects.create(
            user=User,
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
            user=User,
            contact=form.cleaned_data['contact'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            medical_history=form.cleaned_data['medical_history'],
            medications=form.cleaned_data['medications']
        )
        login(self.request, user)
        return super().form_valid(form)

