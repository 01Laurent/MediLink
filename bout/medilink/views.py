from django.shortcuts import render
# from .models import Post
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DoctorsDash


def HomeView(request):
    return render(request, 'home.html')

class DocDashView(LoginRequiredMixin, TemplateView):
    template_name = 'docdash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'doctorprofile'):
            profile = user.doctorprofile
            context['dashboard'] = {
                'patients_treated': profile.patients_treated,
                'upcoming_appointments': profile.upcoming_appointments,
                'total_earnings': profile.total_earnings,
                'notes': profile.notes,
            }
        return context