from django.urls import path
from .views import UserRegisterView
from django.contrib.auth.views import LoginView
from .views import DoctorRegisterView, PatientRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/doctor/', DoctorRegisterView.as_view(), name='doctor_register'),
    path('register/patient/', PatientRegisterView.as_view(), name='patient_register'),
]