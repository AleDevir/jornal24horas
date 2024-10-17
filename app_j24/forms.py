'''
Modulo Forms
'''

from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    '''
    Cria um Usuário
    '''
    email = forms.EmailField(required=True)
    class Meta:
        '''
        Metamodelo
        '''
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ChangePasswordForm(forms.Form):
    antiga_senha = forms.CharField(widget=forms.PasswordInput())
    nova_senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())