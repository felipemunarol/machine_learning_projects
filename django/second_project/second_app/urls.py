from django.urls import path

from second_app.views import index, help

urlpatterns = [
    path("help", help, name="help"),
    path("", index, name="index"),
]