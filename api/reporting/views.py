from django.shortcuts import render

from django_filters import rest_framework
from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView

from reporting import (
    filters as reporting_filters, models as reporting_models,
    serializers as reporting_serializers)


class Home(TemplateView):
    template_name = 'reporting/home.html'


class CreateReport(CreateAPIView):
    serializer_class = reporting.ReportSerializer
