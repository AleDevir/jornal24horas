'''
Módulos views de cadastros
'''
from django.urls import reverse
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Noticia


class NoticiaCreate(CreateView):
    '''
    Cadastra noticia
    '''
    model = Noticia
    fields = ['titulo', 'subtitulo', 'conteudo', 'autor', 'categoria', 'imagem']
    template_name = 'noticia.html'
    def get_success_url(self):
        return reverse('home')



class HomeListView(ListView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'home.html'
    def get_queryset(self):
        return Noticia.objects.all()


class NoticiaDetailView(DetailView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'noticia.html'
