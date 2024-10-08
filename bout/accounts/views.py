from django.forms import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import DoctorRegistrationForm, PatientRegistrationForm, DoctorEditForm, PatientEditForm
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
        login(self.request, user)
        # Ensure the DoctorProfile is only created if it doesn't exist
        if not DoctorProfile.objects.filter(user=user).exists():
            DoctorProfile.objects.create(
                user=user,
                contact=form.cleaned_data['contact'],
                specialty=form.cleaned_data['specialty'],
                location=form.cleaned_data['location'],
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
        if not PatientsProfile.objects.filter(user=user).exists():
            PatientsProfile.objects.create(
                user=user,
                contact=form.cleaned_data['contact'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                medical_history=form.cleaned_data['medical_history'],
                medications=form.cleaned_data['medications']
            )
        login(self.request, user)
        return super().form_valid(form)
        
class EditDoctorsProfileView(generic.UpdateView):
    model = DoctorProfile
    form_class = DoctorEditForm
    template_name = ('registration/edit_doctors_profile_page.html')
    # fields = ['contact', 'specialty', 'location', 'is_available', 'education', 'experience', 'clinics_worked']
    success_url = reverse_lazy('doc_dashboard')

    # def get_object(self):
    #     return self.request.user

class EditPatientsView(generic.UpdateView):
    model = PatientsProfile
    form_class = PatientEditForm
    template_name = ('registration/edit_patients_profile.html')
    # fields = ['contact', 'form_class = DoctorEditFormdate_of_birth', 'medical_history', 'medications']
    success_url = reverse_lazy('home')
 