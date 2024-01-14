from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
# Create your views here.

def registerView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            newUser = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"You account was succesfully created.")
            newUser = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, newUser)

            return redirect("manager:index")
    else:
        form = UserRegisterForm()
    
    context = {
        'form' : form
    }

    return render(request, "userauths/sign-up.html", context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect("manager:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        

