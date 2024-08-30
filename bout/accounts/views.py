from django.shortcuts import render
from django.views import generic
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib import messages


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
