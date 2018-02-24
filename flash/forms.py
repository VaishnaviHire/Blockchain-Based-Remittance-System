from django.contrib.auth.models import User
from django import forms
from django.db import models
from music.models import Lists
from music.models import Transfer
from music.models import Notification, AddToWallet

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-Mail'}),
        }

class TransferForm(forms.ModelForm):

    class Meta:

        model = Transfer
        fields = ['amount']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Lists
        fields = ['amount','recipient']


class NotifyForm(forms.ModelForm):

    class Meta:

        model = Notification
        fields = ['store_latitude','store_longitude','store_name']


class AddWalletForm(forms.ModelForm):

    class Meta:
        model = AddToWallet
        fields = ['amount']
