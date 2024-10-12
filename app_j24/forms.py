'''
Modulo Forms
'''

# from django import forms
from django.forms import EmailField, ModelForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from .models import Noticia


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


class NoticiaForm(ModelForm):
    '''
    Noticia
    '''
    class Meta:
        '''
        Metamodelo
        '''
        model = Noticia
        fields = ['titulo', 'subtitulo', 'conteudo',  'categoria', 'imagem']


class PesquisarNoticiaForm(ModelForm):
    '''
    Pesquisar Noticia
    '''
    class Meta:
        '''
        Metamodelo
        '''
        model = Noticia
        fields = ['id', 'titulo']


