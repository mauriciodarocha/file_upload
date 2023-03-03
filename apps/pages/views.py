"""MAIN VIEW"""
from django.shortcuts import render

def home_page(request):
    """Main view"""

    return render(request, 'home.html')