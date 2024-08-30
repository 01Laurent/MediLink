from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from medilink.models import DoctorProfile, PatientsProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class DoctorRegistrationForm(UserCreationForm):
    contact = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    speciality = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(max_length=150,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience = forms.CharField(max_length=10,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    clinics_worked = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','contact', 'speciality', 'license_number', 'education', 'experience', 'clinics_worked']

class PatientRegistrationForm(UserCreationForm):
    contact = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    medications = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'contact', 'date_of_birth', 'medical_history', 'medications']