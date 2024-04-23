from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userauths.models import User
from .models import Wallet

class WalletCreationForm(forms.Form):
    currency = forms.ChoiceField(choices=Wallet.CURRENCY)
    income = forms.DecimalField(max_digits=7, decimal_places=2)
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
    