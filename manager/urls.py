from django.urls import path
from manager import views

appName = "manager"

urlpatterns = [
    path("", views.index, name="index"),
]

