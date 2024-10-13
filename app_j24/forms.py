'''
Modulo Forms
'''

# from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm


class CriarUsuarioForm(UserCreationForm):
    '''
    Cria um Usuário
    '''
    email = EmailField(required=True)
    class Meta:
        '''
        Metamodelo
        '''
        model = User
        fields = ['username', 'email', 'password1', 'password2']
