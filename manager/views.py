from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'manager/index.html')

@login_required(login_url='sign-in/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='sign-in/')
def transactions(request):
    return render(request, 'dashboard/transactions.html')