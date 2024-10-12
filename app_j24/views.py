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
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Noticia
from .forms import PesquisarNoticiaForm


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

def edit_noticia(request, noticia_id: int) -> HttpResponse:
    '''
    Editar notícia
    '''
   
    try:
        uma_noticia = Noticia.objects.get(pk=noticia_id)
    except Noticia.DoesNotExist as not_found:
        raise Http404(
            f"Notícia não encontrada! A noticícia de ID={noticia_id} não existe na base de dados."
        ) from not_found

    contexto = {
        'noticia': uma_noticia
    }
    return render(request, 'noticia_edit.html', context=contexto)

def noticia_edit_save(request, noticia_id: int) -> HttpResponse:
    '''
    Salvar edição de noticia
    '''
    try:
        if noticia_id == 0:
            uma_noticia = Noticia.objects.create(criado_em=datetime.now())
        else:
            uma_noticia = Noticia.objects.get(pk=noticia_id)
    except Noticia.DoesNotExist as not_found:
        raise Http404(
            f"Notícia não encontrada! A notícia de ID={noticia_id} não existe na base de dados."
        ) from not_found
    
    uma_noticia.titulo = request.POST["titulo"]
    uma_noticia.subtitulo = request.POST["subtitulo"]
    uma_noticia.conteudo = request.POST["conteudo"]
    uma_noticia.imagem = request.POST["imagem"]
    uma_noticia.categoria = request.POST["categoria"]

    uma_noticia.save()
    return HttpResponseRedirect(reverse('exibir_noticias'))

def noticia_delete(request, noticia_id: int) -> HttpResponse:
    '''
    Deletar Noticia
    '''
    try:
        uma_noticia = Noticia.objects.get(pk=noticia_id)
        uma_noticia.delete()
    except Noticia.DoesNotExist as not_found:
        print(not_found)
        raise Http404(
            f"Notícia não encontrada! A notícia de ID={noticia_id} não existe na base de dados."
        ) from not_found

    return HttpResponseRedirect(reverse('exibir_noticias'))