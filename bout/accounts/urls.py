from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DoctorRegisterView, PatientRegisterView, CustomLoginView, EditProfileView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/doctor/', DoctorRegisterView.as_view(), name='doctor_register'),
    path('register/patient/', PatientRegisterView.as_view(), name='patient_register'),
    path('<int:pk>/edit_profile_page/', EditProfileView.as_view(), name='edit_profile'),
]