from django import forms
from .models import Wallet

class WalletCreationForm(forms.Form):
    currency = forms.ChoiceField(choices=Wallet.CURRENCY)
    income = forms.DecimalField(max_digits=7, decimal_places=2)
    balance = forms.DecimalField(max_digits=10, decimal_places=2)

class WalletUpdateForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance', 'monthlyIncome', 'currencyType']
    
# class TransactionCreationForm(forms.Form):
#     value = forms.DecimalField(max_digits=10, decimal_places=2)
#     # date = forms.DateField(auto_now=True)
#     description = forms.TextInput()