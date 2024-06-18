from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from manager.forms import *
from manager.models import Wallet, Transaction
from django.contrib import messages
from django.http import JsonResponse, FileResponse
# from django.db.models import Sum
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from io import BytesIO
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
# Create your views here.

def index(request):
    return render(request, 'manager/index.html')

def lineChart(wallet):
    endDate = datetime.now()
    startDate = endDate -timedelta(days=365)
    months = [(startDate + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(12)]
    months = sorted(list(set(months)))
    transactions = Transaction.objects.filter(wallet=wallet, date__range=[startDate, endDate]).order_by('date')
    totalMonthTransactions = transactions.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('value')).order_by('month')
    monthSumDict = {entry['month'].strftime('%Y-%m'): float(entry['total']) for entry in totalMonthTransactions}
    labels = []
    values = []

    for month in months:
        labels.append(month)
        values.append(monthSumDict.get(month, 0.0))

    lineFig = go.Figure(data=go.Scatter(x=labels, y=values, mode='lines+markers'))
    lineFig.update_layout(title='Monthly Transaction Sum', xaxis_title='Month', yaxis_title='Total Transactions')
    lineDiv = plot(lineFig, output_type='div')

    return lineDiv

def doughnutChart(wallet):
    endDate = datetime.now()
    currentMonth = endDate.month
    currentYear = endDate.year
    transactions = Transaction.objects.filter(wallet=wallet, date__month=currentMonth, date__year=currentYear)
    categoriesSum = transactions.values('transactionCategory').annotate(total=Sum('value'))
    categories  =[transaction.get_transactionCategory_display() for transaction in transactions]
    values = [entry['total'] for entry in categoriesSum]

    doughnutFig = go.Figure(data=[go.Pie(labels=categories, values=values, hole=0.4)])
    doughnutFig.update_layout(title='Expenses by Category (Current Month)')
    doughnutDiv = plot(doughnutFig, output_type='div')

    return doughnutDiv

@login_required(login_url='sign-in/')
def dashboard(request):
    user = request.user
    wallet = Wallet.objects.get(owner=user)
    chart1 = lineChart(wallet)
    chart2 = doughnutChart(wallet)

    context = {
        'line_chart': chart1,
        'doughnut_chart': chart2,
    }

    return render(request, 'dashboard/dashboard.html', context)

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
            transaction = Transaction(wallet=usrWallet, value=data['value'], date=data['date'], transactionCategory=data['category'], description=data['description'])
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
        file.drawString(100, y - 40, f"Category: {transaction.get_transactionCategory_display}")
        file.drawString(100, y - 60, f"Description: {transaction.description}")
        y -= 120

    file.showPage()
    file.save()
    buffer.seek(0)

    return buffer

@login_required(login_url='sign-in/')
def help(request):
    return render(request, 'dashboard/help.html')

# @login_required(login_url='sign-in/')
# def getTransactionData(request):
#     transactions = Transaction.objects.all()
#     data = {'date':[transaction.date.strftime('%Y-%m-%d') for transaction in transactions],
#             'values':[transaction.value for transaction in transactions],
#             'category':[transaction.get_transactionCategory_display() for transaction in transactions]}
    
#     return JsonResponse(data)

# @login_required(login_url='sign-in/')
# def getUserBalanceVariation(request):
#     user = request.user
#     wallet = Wallet.objects.get(owner=user)
#     transactions = Transaction.objects.filter(wallet=wallet).order_by('date')
    
#     # Create a dictionary for monthly balances
#     monthlyBalances = {}
    
#     # Initialize the current balance
#     currentBalance = float(wallet.balance)
    
#     # Get the current date and one year ago date
#     today = datetime.today()
#     one_year_ago = today - timedelta(days=365)
    
#     # Iterate through all months in the past year
#     for i in range(12):
#         month = (today - timedelta(days=i*30)).strftime('%Y-%m')
#         monthlyBalances[month] = 0

#     # Update the monthly balances with actual transaction data
#     for transaction in transactions:
#         month = transaction.date.strftime('%Y-%m')
#         if month in monthlyBalances:
#             monthlyBalances[month] += float(transaction.value)
    
#     # Generate ordered list of months and balance data
#     orderedMonths = sorted(monthlyBalances.keys())
#     labels = []
#     balances = []
    
#     for month in orderedMonths:
#         labels.append(month)
#         currentBalance += monthlyBalances[month]
#         balances.append(currentBalance)
    
#     responseData = {'labels': labels, 'values': balances}
#     return JsonResponse(responseData)
