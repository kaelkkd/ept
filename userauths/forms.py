from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholde":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholde":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholde":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholde":"Confirm password"}))
    
    
    class Meta:
        model = User
        fields = ['username', 'email']