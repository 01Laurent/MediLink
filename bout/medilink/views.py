from django.shortcuts import render
# from .models import Post
# from django.views.generic import ListView

def HomeView(request):
    return render(request, 'home.html')