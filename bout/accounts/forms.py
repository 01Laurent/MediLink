from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from medilink.models import DoctorProfile, PatientsProfile


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs['class']='form-control'
#         self.fields['password1'].widget.attrs['class']='form-control'
#         self.fields['password2'].widget.attrs['class']='form-control'

class DoctorRegistrationForm(UserCreationForm):
    contact = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    clinics_worked = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'contact', 'specialty', 'location', 'license_number', 'education', 'experience', 'clinics_worked']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Assuming doctors are staff members
        if commit:
            user.save()  # Only save the user
        return user

class DoctorEditForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['contact', 'specialty', 'location', 'is_available', 'education', 'experience', 'clinics_worked']
        
        # Add custom widgets to each field
        widgets = {
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Information'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialty'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            # 'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Education Background'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Experience Details'}),
            'clinics_worked': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Clinics Worked'}),
        }

class PatientRegistrationForm(UserCreationForm):
    contact = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    medications = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'contact', 'date_of_birth', 'medical_history', 'medications']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False 
        if commit:
            user.save() 
        return user
    
class PatientEditForm(forms.ModelForm):
    class Meta:
        model = PatientsProfile
        fields = ['contact', 'date_of_birth', 'medical_history', 'medications']
        
        # Add custom widgets to each field
        widgets = {
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Information'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medical History'}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Current Medications'}),
        }

