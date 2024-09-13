from django import forms
from .models import Appointment, DoctorAvailability, Message
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

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = []
class SetAppointmentForm(forms.ModelForm):
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time']

class FeedbackForm(forms.Form):
    TREATED_CHOICES = [(True, 'Treated'), (False, 'Not Treated')]
    
    is_treated = forms.ChoiceField(choices=TREATED_CHOICES, widget=forms.RadioSelect)
    rating = forms.IntegerField(min_value=1, max_value=5, required=False, help_text='Rate the doctor (1-5 stars)')
    not_treated_reason = forms.CharField(widget=forms.Textarea, required=False, help_text='Reason for not being treated')

    def clean(self):
        cleaned_data = super().clean()
        is_treated = cleaned_data.get('is_treated')
        rating = cleaned_data.get('rating')
        not_treated_reason = cleaned_data.get('not_treated_reason')

        if is_treated == 'True' and not rating:
            raise forms.ValidationError("Please provide a rating if you were treated.")
        if is_treated == 'False' and not not_treated_reason:
            raise forms.ValidationError("Please provide a reason if you were not treated.")
        
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