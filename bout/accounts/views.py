from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .forms import SignUpForm, DoctorRegistrationForm, PatientRegistrationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User


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
        return super().form_valid(form)
    
class PatientRegisterView(generic.CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'registration/register_patient.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)

