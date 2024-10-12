'''
Módulos views de cadastros
'''
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import BaseModelForm
from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
)

from django.http import Http404
from django.urls import reverse
from django.views.generic import  DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Categoria, Noticia
from .forms import NoticiaForm, PesquisarNoticiaForm


class NoticiaCreate(PermissionRequiredMixin, CreateView):
    '''
    Cadastra noticia
    '''
    model = Noticia
    fields = ['titulo', 'subtitulo', 'conteudo',  'categoria', 'imagem']
    template_name = 'cadastro_noticia.html'
    permission_required = "app_j24.autor_noticia"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('exibir_noticias')

class NoticiaUpdate(NoticiaCreate, UpdateView):
    '''
    Atualiza a Notícia
    '''
    pass

class NoticiaDelete(DeleteView):
    '''
    Atualiza a Notícia
    '''
    model = Noticia
    template_name = 'noticia_confirm_delete.html'
    def get_success_url(self):
        return reverse('exibir_noticias')


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

@login_required(login_url="/accounts/login/")
@permission_required("app_j24.autor_noticia")
def exibir_noticias(request) -> HttpResponse:
    '''
   Notícias de um determinado autor
    '''
    if request.method == "POST":
        titulo = request.POST['titulo']
        uma_noticia = Noticia.objects.filter(titulo__icontains=titulo).first()
        if uma_noticia:
            return HttpResponseRedirect(reverse("noticias/cadastro/", args=(uma_noticia.id,)))
        raise Http404(f"Notícia de título {titulo} não encontrada!")

    lista = Noticia.objects.filter(autor=request.user)
    form = PesquisarNoticiaForm()
    return render(request, 'minhas_noticias.html', {
        "form": form,
        "exibir_noticias": lista,
    })

def pesquisar_noticias(request) -> HttpResponse:
    '''
    Pesquisar Notícias
    '''
    titulo = request.POST['titulo']
    noticias = Noticia.objects.filter(titulo__icontains=titulo)

    lista = Noticia.objects.filter(autor=request.user)
    return render(request, 'noticias_filtradas.html', {
        "object_list": noticias,
    })
