from django import forms
from django.forms import DateTimeInput, DateField
from .models import *

class WalletCreationForm(forms.Form):
    currency = forms.ChoiceField(choices=Wallet.CURRENCY)
    income = forms.DecimalField(max_digits=7, decimal_places=2)
    balance = forms.DecimalField(max_digits=10, decimal_places=2)

class WalletUpdateForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance', 'monthlyIncome', 'currencyType']
    
class TransactionCreationForm(forms.Form):
    value = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))

class TransactionEditForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['value', 'date', 'description']