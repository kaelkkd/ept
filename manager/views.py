from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from manager.forms import *
from manager.models import Wallet, Transaction
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
# Create your views here.

def index(request):
    return render(request, 'manager/index.html')

@login_required(login_url='sign-in/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='sign-in/')
def transactions(request):
    userWallet = Wallet.objects.get(owner=request.user)
    if userWallet:
        transactions = Transaction.objects.filter(wallet=userWallet)
    else:
        transactions = []

    context = {'transactions':transactions}

    return render(request, 'dashboard/transactions.html', context)

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
            messages.success(request, f"The wallet was sucessfully updated.")
        else:
            messages.error(request, f"There was an error, try again.")
    else:
        form = WalletUpdateForm(instance=wallet)

    context = {'form':form, 'wallet':wallet}

    return render(request, 'dashboard/update-wallet.html', context)

@login_required(login_url="sign-in/")
def deleteWallet(request):
    wallet = get_object_or_404(Wallet, owner=request.user)
    if request.method == "POST":
        wallet.delete()
        messages.success(request, f"Your wallet was sucessfully deleted.")
        return redirect('manager:wallet')

    return render(request, 'dashboard/delete-wallet.html')

@login_required(login_url="sign-in/")
def addTransaction(request):
    if request.method == "POST":
        form = TransactionCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            usrWallet, created = Wallet.objects.get_or_create(owner= user)
            if created:
                messages.warning(request, f"A new wallet was created.")
            transaction = Transaction(wallet=usrWallet, value=data['value'], date=data['date'], description=data['description'])
            transaction.save()
            messages.success(request, f"Transaction sucessfully added.")
            redirect('dashboard/transaction.html')
    else:
        form = TransactionCreationForm()

    context = {'form':form}

    return render(request, 'dashboard/add-transaction.html', context)

@login_required(login_url='sign-in/')
@require_POST
def deleteTransaction(request):
    transactionId = request.POST.get('transactionId')
    if transactionId:
        try:
            transaction = Transaction.objects.get(pk=transactionId)
            transaction.delete()
            return JsonResponse({'success': True, 'message': 'Transaction successfully deleted.'})
        except Transaction.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Transaction does not exist.'})
        
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required(login_url='sign-in/')
def generateStatement(request):
    response = FileResponse(generateStatementFile(), as_attachment=True, filename='user_statement.pdf')

    return response

def generateStatementFile():
    buffer = BytesIO()
    file = canvas.Canvas(buffer)
    transactions = Transaction.objects.all()
    file.drawString(100, 750, "Transaction history")
    y = 700

    for transaction in transactions:
        file.drawString(100, y, f"Value: {transaction.value}")
        file.drawString(100, y - 20, f"Date: {transaction.date}")
        file.drawString(100, y - 40, f"Description: {transaction.description}")
        y -= 80

    file.showPage()
    file.save()
    buffer.seek(0)

    return buffer