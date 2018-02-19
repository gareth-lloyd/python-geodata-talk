from django.shortcuts import render

from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView

from reporting import (
    models as reporting_models,
    serializers as reporting_serializers)


class Home(TemplateView):
    template_name = 'reporting/home.html'


class ListCreateReport(ListCreateAPIView):
    serializer_class = reporting_serializers.ReportSerializer
    queryset = reporting_models.Report.objects.all()
