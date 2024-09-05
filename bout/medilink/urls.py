from django.urls import path
from .import consumers
from .views import HomeView, DocDashView, PatDahView, ScheduleAppointmentView, DoctorAvailabilityView, AppointmentListView,ComposeMessageView, SentMessagesView, InboxView
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
]

websocket_urlpatterns = [
    path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
]