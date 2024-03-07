from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, UserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

User = settings.AUTH_USER_MODEL

def registerView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f"You account was succesfully created.")
            return redirect("userauths:sign-in")
    else:
        form = UserRegisterForm()
    
    context = {
        'form' : form
    }

    return render(request, "userauths/sign-up.html", context)

def loginView(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manager:dashboard')
        else:
            messages.error(request, f'Invalid username/password.')
    else:
        form = UserAuthenticationForm()

    context = {
        'form':form
    }

    return render(request, 'userauths/sign-in.html', context)

def logoutView(request):
    logout(request)
    messages.success(request, f"Sucessfully logged out.")
    return redirect("userauths:sign-in")

# @login_required(login_url='sign-in')
# def dashboardView(request):
#     context = {
#         'temp':
#     }

#     return render(request, "userauths/sign-in.html", context)