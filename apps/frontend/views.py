# from django.shortcuts import render
from django.views.generic import TemplateView

class FrontendView(TemplateView):
    """Base view"""
    template_name = "base.html"
