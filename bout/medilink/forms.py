from django import forms
from .models import Appointment, DoctorAvailability

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