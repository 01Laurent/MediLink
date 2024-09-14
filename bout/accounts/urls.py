from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DoctorRegisterView, PatientRegisterView, CustomLoginView, EditDoctorsProfileView, EditPatientsView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/doctor/', DoctorRegisterView.as_view(), name='doctor_register'),
    path('register/patient/', PatientRegisterView.as_view(), name='patient_register'),
    path('edit_doctors_profile/<int:pk>/', EditDoctorsProfileView.as_view(), name='doc_edit_profile'),
    path('edit_patients_profile/<int:pk>/', EditPatientsView.as_view(), name='pat_edit_profile'),
]