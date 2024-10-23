'''
Módulos views de cadastros
'''

from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import BaseModelForm
from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
)
from django.http import (
    Http404, 
    QueryDict,
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from django.views.generic import  DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Categoria, Noticia, MyUser
from .forms import RegistrationForm


class NoticiaBaseView(PermissionRequiredMixin):
    '''
    Manter Notícia BASE
    '''
    model = Noticia

    def get_success_url(self):
        return reverse('noticias')

class NoticiaCadastroView(NoticiaBaseView):
    '''
    Notícia Cadastro
    '''
    fields = ['titulo', 'subtitulo', 'conteudo',  'categorias', 'imagem']
    template_name = 'cadastro_noticia.html'

class NoticiaCreateView(NoticiaCadastroView, CreateView):
    '''
    Notícia Criar
    '''
    permission_required = "app_j24.add_noticia"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if not self.request.user.has_perm('app_j24.add_noticia'):
            raise PermissionDenied('Permissão para adicionar notícia negada! Você não possui permissão necessária.')
        form.instance.autor = self.request.user
        return super().form_valid(form)

class NoticiaUpdateView(NoticiaCadastroView, UpdateView):
    '''
    Atualiza a Notícia
    '''
    permission_required = "app_j24.change_noticia"

    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        eh_editor: bool = self.request.user.has_perm('app_j24.pode_publicar')
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não é o autor da notícia.')
        form.instance.atualizada_em = datetime.now()
        return super().form_valid(form)

class NoticiaDeleteView(NoticiaBaseView, DeleteView):
    '''
    Excluir Notícia
    '''
    permission_required = "app_j24.delete_noticia"
    template_name = 'noticia_confirm_delete.html'  

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        eh_editor = self.request.user.has_perm('app_j24.pode_publicar')
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não é o autor da notícia.')
        return super().form_valid(form)

class NoticiaDetailView(DetailView):
    '''
    Listar as nóticias na página Home
    '''
    model = Noticia
    template_name = 'noticia.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        eh_editor: bool = self.request.user.has_perm('app_j24.pode_publicar')
        eh_autor: bool = self.request.user.has_perm('app_j24.add_noticia')
        eh_autor_da_noticia: bool = eh_autor and self.object.autor == request.user
        pode_ver_noticia_nao_publicada: bool = eh_editor or eh_autor_da_noticia
        if not self.object.publicada and not pode_ver_noticia_nao_publicada:
            raise PermissionDenied('Permissão para ver a notícia negada! Está notícia não foi publicada.')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class NoticiasBaseListView(ListView):
    '''
    Listar as nóticias dos autores e editores
    '''
    titulo = ''
    categoria = 0
    publicada = None
    model = Noticia

    def set_pesquisa(self):
        querystring = self.request.GET.dict()
        self.titulo = querystring.get('titulo', '')
        self.categoria = int(querystring.get('categoria', 0))

    def get(self, request, *args, **kwargs):
        self.set_pesquisa()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.titulo = self.request.POST['titulo']
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
        query_dict = QueryDict(f"titulo={self.titulo}&categoria={self.categoria}")

        contexto = {
            "titulo": self.titulo,
            "categoria": self.categoria,
            "categorias": Categoria.objects.all(),
            "object_list": noticias[0:self.paginate_by],
            "page_obj": page_obj,
            'pesquisa': query_dict,
        }
        return render(request, self.template_name, context=contexto)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['categoria'] = self.categoria
        context['categorias'] = Categoria.objects.all()
        pesquisa = self.request.GET.copy()
        if pesquisa.get('page'):
            pesquisa.pop('page')
        context['pesquisa'] = pesquisa
        return context

    def get_queryset(self):
        filtragem = {}
        if self.titulo:
            filtragem['slug__contains'] = slugify(self.titulo)
        if self.categoria != 0:
            filtragem['categorias'] = int(self.categoria)
        if self.publicada:
            filtragem['publicada'] = self.publicada
        elif self.request.user.has_perm('app_j24.add_noticia'):
            filtragem['autor'] = self.request.user

        if filtragem and self.publicada:
            return Noticia.objects.filter(**filtragem).order_by('-publicada_em')
        elif filtragem:
            return Noticia.objects.filter(**filtragem).order_by('titulo')
        
        return Noticia.objects.all().order_by('titulo')

class NoticiasListView(PermissionRequiredMixin, NoticiasBaseListView):
    '''
    Listar as nóticias dos autores e editores
    '''
    permission_required = "app_j24.change_noticia"
    template_name = 'noticias_table.html'
    paginate_by = 10

class HomeListView(NoticiasBaseListView):
    '''
    Listar as nóticias na página Home
    '''
    paginate_by = 4
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

class SignUpView(CreateView):
    
    model = MyUser
    template_name = 'register.html'
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('login')

class UserUpdateView(UpdateView):
    '''
    Atualiza a Usuário
    '''
    model = MyUser
    fields = ['username', 'email']
    template_name = 'user_edit.html'
    def get_success_url(self):
        return reverse('home')

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_edit.html'
    def get_success_url(self):
        return reverse('home')



   