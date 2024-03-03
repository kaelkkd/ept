from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, UserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

User = settings.AUTH_USER_MODEL

def registerView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            newUser = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"You account was succesfully created.")
            newUser = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, newUser)

            return redirect("manager:index") #maybe redirect to the login page instead
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
            credentials = form.cleaned_data
            user = authenticate(username=credentials['username'], password=credentials['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('manager:dashboard')
            else:
                messages.error(request, f"The user does not exist.")

        else:
            messages.error(request, f'Invalid email/password.')
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