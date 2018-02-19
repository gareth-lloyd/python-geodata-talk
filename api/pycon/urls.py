from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from reporting import views

urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'api/reports/$', views.ListCreateReport.as_view()),
    path(r'admin/', admin.site.urls),
]
