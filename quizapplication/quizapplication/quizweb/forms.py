from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class RegisterationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["email","username","password1","password2"]

    
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    