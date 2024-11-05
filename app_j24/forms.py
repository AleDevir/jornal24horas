'''
Modulo Forms
'''

from django import forms
from django.forms import EmailField
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Categoria, Noticia, Comentario

class RegistrationForm(UserCreationForm):
    '''
    Cria um Usuário
    '''
    email = forms.EmailField(required=True)
    class Meta:
        '''
        Metamodelo
        '''
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

class ChangePasswordForm(forms.Form):
    antiga_senha = forms.CharField(widget=forms.PasswordInput())
    nova_senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

class CategoriaForm(forms.ModelForm):
    '''
    Formulário de cadastro de categoria
    '''
    class Meta:
        '''
        Metamodelo
        '''
        model = Categoria
        fields = ['nome',  'imagem']

class NoticiaForm(forms.ModelForm):
    '''
    Formulário de cadastro de notícia
    '''
    class Meta:
        '''
        Metamodelo
        '''
        model = Noticia
        fields = ['titulo', 'subtitulo', 'conteudo', 'imagem', 'categorias', 'fonte_informacao']

class ComentarioForm(forms.ModelForm):
    '''
    Formulário de comentário da notícia
    '''
    class Meta:
        '''
        Metamodelo
        '''
        model = Comentario
        fields = ['conteudo']


    