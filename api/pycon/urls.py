from django.contrib import admin
from django.urls import path

from reporting import views

urlpatterns = [
    url(r'^$', views.Home.as_view()),
    path('admin/', admin.site.urls),
]
