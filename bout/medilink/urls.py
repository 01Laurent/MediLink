from django.urls import path
from .views import HomeView, DocDashView, PatDahView, ScheduleAppointmentView, DoctorAvailabilityView, AppointmentListView,ComposeMessageView, SentMessagesView, InboxView

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
]