from django.urls import path
from .views import HomeView, DocDashView

urlpatterns = [
    path('', HomeView, name='home'),
    path('doctors/dashboard', DocDashView.as_view(), name='doc_dashboard'),
]