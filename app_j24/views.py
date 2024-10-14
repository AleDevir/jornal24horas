'''
Módulos views de cadastros
'''
from datetime import datetime
from django.core.paginator import Paginator
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


class NoticiaBase(PermissionRequiredMixin):
    '''
    Manter Notícia BASE
    '''
    model = Noticia

    def get_success_url(self):
        if self.request.user.has_perm('app_j24.noticia_criar'):
            return reverse('noticias')
        if self.request.user.has_perm('app_j24.pode_publicar'):
            return reverse('noticias')
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

class NoticiaDetailView(DetailView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'noticia.html'

class NoticiasBaseListView(ListView):
    '''
    Listar as nóticias dos autores e editores
    '''
    titulo = ''
    categoria = 0
    publicada = None
    model = Noticia

    def post(self, request, *args, **kwargs):
        self.titulo = ''
        self.categoria = 0   
        if self.request.method == 'POST':
            self.titulo = self.request.POST['titulo']
            if self.request.POST['categoria']:
                self.categoria = int(self.request.POST['categoria'])

        if not self.paginate_by:
            return render(request, self.template_name, {
                "titulo": self.titulo,
                "categoria": self.categoria,
                "categorias": Categoria.objects.all(),
                "object_list": self.get_queryset(),
            })

        # https://docs.djangoproject.com/en/5.1/topics/pagination/
        noticias = self.get_queryset()
        paginator = Paginator(noticias, self.paginate_by)
        page_obj = paginator.get_page(1)

        return render(request, self.template_name, {
            "titulo": self.titulo,
            "categoria": self.categoria,
            "categorias": Categoria.objects.all(),
            "object_list": noticias,
            "page_obj": page_obj,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

    def get_queryset(self):
        filtragem = {}
        if self.titulo:
            filtragem['titulo__icontains'] = self.titulo
        if self.categoria != 0:
            filtragem['categoria'] = self.categoria
        if self.publicada:
            filtragem['publicada'] = self.publicada
        elif self.request.user.has_perm('app_j24.noticia_criar'):
            filtragem['autor'] = self.request.user

        if filtragem and self.publicada:
            return Noticia.objects.filter(**filtragem).order_by('-publicada_em')
        elif filtragem:
            return Noticia.objects.filter(**filtragem).order_by('titulo')
        
        return Noticia.objects.all().order_by('titulo')


class NoticiasListView(NoticiasBaseListView):
    '''
    Listar as nóticias dos autores e editores
    '''
    template_name = 'noticias_table.html'
    paginate_by = 5


class HomeListView(NoticiasBaseListView):
    '''
    Listar as nóticias na página Home
    '''
    # paginate_by = 4
    publicada = True
    template_name = 'home.html'


@login_required(login_url="/accounts/login/")
@permission_required("app_j24.pode_publicar")
def publicar_noticia(request, noticia_id: int, publicado: int) -> HttpResponse:
    '''
    Publicar Notícia
    '''
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
    return HttpResponseRedirect(reverse("noticias"))
