from django.urls import path
from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/transactions", views.transactions, name="transactions"),
    path("dashboard/wallet", views.walletView, name="wallet"),
]

