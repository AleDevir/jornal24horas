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
from .forms import PesquisarNoticiaForm


class NoticiaBase(PermissionRequiredMixin):
    '''
    Manter Notícia BASE
    '''
    model = Noticia

    def get_success_url(self):
        if self.request.user.has_perm('app_j24.noticia_criar'):
            return reverse('noticias_autor')
        if self.request.user.has_perm('app_j24.pode_publicar'):
            return reverse('editor_noticias')
        return reverse('home')

class NoticiaCadastro(NoticiaBase):
    '''
    Notícia Cadastro
    '''
    fields = ['titulo', 'subtitulo', 'conteudo',  'categoria', 'imagem']
    template_name = 'cadastro_noticia.html'

class NoticiaCreate(NoticiaCadastro, CreateView):
    '''
    Notícia Criar
    '''
    permission_required = "app_j24.noticia_criar"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.autor = self.request.user
        return super().form_valid(form)

class NoticiaUpdate(NoticiaCadastro, UpdateView):
    '''
    Atualiza a Notícia
    '''
    permission_required = "app_j24.noticia_alterar"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.atualizada_em = datetime.now()
        return super().form_valid(form)

class NoticiaDelete(NoticiaBase, DeleteView):
    '''
    Excluir Notícia
    '''
    permission_required = "app_j24.noticia_excluir"
    template_name = 'noticia_confirm_delete.html'


class HomeListView(ListView):
    '''
    Listar as nóticias na página Home
    '''
    titulo = ''
    categoria = 0     
    model = Noticia
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.titulo = ''
        self.categoria = 0   
        if self.request.method == 'POST':
            self.titulo = self.request.POST['titulo']
            if self.request.POST['categoria']:
                self.categoria = int(self.request.POST['categoria'])

        print('______________________________________________')
        print(f"titulo=|{self.titulo}|")
        print(f"catergoria=|{self.categoria}| TIPO={type(self.categoria)}")
        print('______________________________________________')

        return render(request, 'home.html', {
            "titulo": self.titulo,
            "categoria": self.categoria,
            "categorias": Categoria.objects.all(),
            "object_list": self.get_queryset(),
        })

    def get_queryset(self):
        if self.titulo and self.categoria != 0:
            return Noticia.objects.filter(publicada=True, titulo__icontains=self.titulo, categoria=self.categoria)

        if self.titulo:
            return Noticia.objects.filter(publicada=True, titulo__icontains=self.titulo)

        if self.categoria != 0:
            return Noticia.objects.filter(publicada=True, categoria=self.categoria)
           
        return Noticia.objects.filter(publicada=True).order_by('-publicada_em')

    def get_context_data(self, **kwargs):
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        print(f"kwargs={kwargs}")
        print('ccccccccccccccccccccccccccccccccccccccccccc')
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()     
        return context



class NoticiaDetailView(DetailView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'noticia.html'

@login_required(login_url="/accounts/login/")
@permission_required("app_j24.noticia_criar")
def noticias_autor(request) -> HttpResponse:
    '''
   Notícias de um determinado autor
    '''
    # if request.method == "POST":
    #     titulo = request.POST['titulo']
    #     uma_noticia = Noticia.objects.filter(titulo__icontains=titulo).first()
    #     if uma_noticia:
    #         return HttpResponseRedirect(reverse("noticias/cadastro/", args=(uma_noticia.id,)))
    #     raise Http404(f"Notícia de título {titulo} não encontrada!")

    lista = Noticia.objects.filter(autor=request.user)
    form = PesquisarNoticiaForm()
    return render(request, 'minhas_noticias.html', {
        "form": form,
        "noticias_autor": lista,
    })

@login_required(login_url="/accounts/login/")
@permission_required("app_j24.pode_publicar")
def editor_noticias(request) -> HttpResponse:
    '''
    Notícias  para o editor publicar ou não
    '''
    lista = Noticia.objects.all()
    form = PesquisarNoticiaForm()
    return render(request, 'editor_noticias.html', {
        "form": form,
        "editor_noticias": lista,
    })


# def pesquisar_noticias(request) -> HttpResponse:
#     '''
#     Pesquisar Notícias
#     '''
#     titulo = request.POST['titulo']
#     categoria = request.POST['categoria']
#     print('______________________________________________')
#     print(f"titulo=|{titulo}|")
#     print(f"catergoria=|{categoria}| TIPO={type(categoria)}")
#     print('______________________________________________')
#     noticias = []
#     if titulo and categoria != '0':
#         noticias = Noticia.objects.filter(titulo__icontains=titulo, categoria=categoria)
#     elif titulo:
#         noticias = Noticia.objects.filter(titulo__icontains=titulo)
#     elif categoria != '0':
#         noticias = Noticia.objects.filter(categoria=categoria)
#     else:
#         noticias = Noticia.objects.all()
#     return render(request, 'home.html', {
#         "titulo": titulo,
#         "categoria": categoria,
#         "object_list": noticias,
#     })


@login_required(login_url="/accounts/login/")
@permission_required("app_j24.pode_publicar")
def publicar_noticia(request, noticia_id: int, publicado: int) -> HttpResponse:
    '''
    Publicar Notícia
    '''
    print('publicar_noticia.............................')
    print(f"noticia_id={noticia_id}")
    print(f"publicado={publicado}")
    try:
        noticia = Noticia.objects.get(pk=noticia_id)
        if publicado == 1:
            noticia.publicada = True
            noticia.publicada_em = datetime.now()
        else:
            noticia.publicada = False
            noticia.publicada_em = None
        noticia.save()
    except Noticia.DoesNotExist as not_found:
        raise Http404(
            f"Notícia não encontrada! Não foi possível publicar a Notícia de ID={noticia_id} porque ela não existe na base de dados."
        ) from not_found
    return HttpResponseRedirect(reverse("editor_noticias"))
