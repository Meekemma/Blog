from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['name', 'email', 'body']

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']    

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields = '__all__'
        exclude = ['user']            