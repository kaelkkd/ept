from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from manager.forms import *
from manager.models import Wallet, Transaction
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'manager/index.html')

@login_required(login_url='sign-in/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='sign-in/')
def transactions(request):
    return render(request, 'dashboard/transactions.html')

@login_required(login_url='sign-in/')
def wallet(request):
    return render(request, 'dashboard/wallet.html')

@login_required(login_url='sign-in/')
def walletCreation(request):
    if request.method == 'POST':
        form = WalletCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            wallet = Wallet(balance = data['balance'], monthlyIncome = data['income'], currencyType = data['currency'])
            wallet.owner = request.user
            wallet.save()
            messages.success(request, f"Wallet sucessfully created!")
    else:
        form = WalletCreationForm()
    context = {'form':form}

    return render(request, 'dashboard/create-wallet.html', context)

@login_required(login_url='sign-in/')
def updateWallet(request):
    wallet = get_object_or_404(Wallet, owner = request.user)
    if request.method == "POST":
        form = WalletUpdateForm(request.POST, instance = wallet)
        if form.is_valid():
            form.save()
            messages.success(f"The wallet was sucessfully updated.")
        else:
            messages.error(f"There was an error, try again.")
    else:
        form = WalletUpdateForm(instance=wallet)

    context = {'form':form, 'wallet':wallet}

    return render(request, 'dashboard/update-wallet.html', context)

@login_required(login_url="sign-in/")
def deleteWallet(request):
    wallet = get_object_or_404(Wallet, owner=request.user)
    if request.method == "POST":
        wallet.delete()
        messages.success(f"Your wallet was sucessfully deleted.")
        return redirect('manager:wallet')

    return render(request, 'dashboard/delete-wallet.html')
