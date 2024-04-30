from django.urls import path
from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/transactions", views.transactions, name="transactions"),
    path("dashboard/wallet", views.wallet, name="wallet"),
    path("dashboard/create-wallet", views.walletCreation, name="create-wallet"),
    path("dashboard/update-wallet", views.updateWallet, name="update-wallet"),
    path("dashboard/delete-wallet", views.deleteWallet, name="delete-wallet"),
]

