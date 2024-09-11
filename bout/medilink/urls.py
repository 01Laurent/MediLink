from django.urls import path
from .import consumers
from .views import DocDashView, PatDahView, ScheduleAppointmentView, DoctorAvailabilityView, AppointmentListView,ComposeMessageView, SentMessagesView, InboxView, home, HomeView, request_appointment, appointment_confirmation
from .import views

urlpatterns = [
    path('', HomeView, name='home'),
    path('doctors/dashboard', DocDashView.as_view(), name='doc_dashboard'),
    path('patients/dashboard', PatDahView.as_view(), name='pat_dashboard'),
    path('schedule/', ScheduleAppointmentView.as_view(), name='schedule_appointment'),
    path('availability/', DoctorAvailabilityView.as_view(), name='doctor_availability'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentMessagesView.as_view(), name='sent_messages'),
    path('compose/', ComposeMessageView.as_view(), name='compose_message'),
    path('chat/', views.chat_view, name='chat'),
    path('search_doctors/', home, name='search_doctors'),
    path('request_appointment/<int:doctor_id>/', request_appointment, name='request_appointment'),
    path('appointment_confirmation/', appointment_confirmation, name='appointment_confirmation'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    path('respond_to_appointment/<int:appointment_id>/<str:response>/', views.respond_to_appointment, name='respond_to_appointment'),
    path('patient_appointments/', views.patient_appointments, name='patient_appointments'),
]

websocket_urlpatterns = [
    path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
]