from django import forms
from .models import Appointment, DoctorAvailability, Message, User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class AppointmentForm(forms.ModelForm):
    doctor = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    notes = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}))


    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'notes']

class DoctorAvailabilityForm(forms.ModelForm):
    day = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))

    class Meta:
        model = DoctorAvailability
        fields = ['day', 'start_time', 'end_time']

class MessageForm(forms.ModelForm):
    class Meta:

        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.exclude(id=self.initial.get('exclude_user_id'))

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Doctors', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))