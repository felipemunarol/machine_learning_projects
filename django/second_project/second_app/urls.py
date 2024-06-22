from django.urls import path

from second_app.views import index, help, users

urlpatterns = [
    path("help", help, name="help"),
    path("users", users, name="users"),
    path("", index, name="index"),
]