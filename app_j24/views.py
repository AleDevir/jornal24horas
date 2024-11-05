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
from django.http import HttpRequest
from django.db.models import Model
from django.views.generic import  DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Categoria, Noticia, MyUser, UserAction
from .forms import RegistrationForm, CategoriaForm, NoticiaForm

def log_user_action(request : HttpRequest, obj: Model, action: str, object_name: str = '') -> None:
    '''
    Registro das ações de autores e editores
    '''
    UserAction.objects.create(
        user=request.user,
        action=action,
        object_id = obj.pk,
        object_name = obj.__doc__ if not object_name else object_name,
        object_text = str(obj)
    )

def root(request) -> HttpResponse:
    '''
    Redirecionamento de root para home
    '''
    return HttpResponseRedirect(reverse("home"))

class NoticiaCreateView(PermissionRequiredMixin, CreateView):
    '''
    Notícia Criar
    '''
    model = Noticia
    form_class = NoticiaForm
    permission_required = "app_j24.add_noticia"
    template_name = 'cadastro_noticia.html'
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if not self.request.user.has_perm('app_j24.add_noticia'):
            raise PermissionDenied('Permissão para adicionar notícia negada! Você não possui permissão necessária.')
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Incluiu')
        return reverse('noticias')

class NoticiaUpdateView(PermissionRequiredMixin, UpdateView):
    '''
    Atualiza a Notícia
    '''
    permission_required = "app_j24.change_noticia"
    model = Noticia
    form_class = NoticiaForm    
    template_name = 'cadastro_noticia.html'
    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        eh_editor: bool = self.request.user.has_perm('app_j24.pode_publicar')
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para alterar a notícia negada! Você não é o autor da notícia.')
        form.instance.atualizada_em = datetime.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Alterou')
        return reverse('noticias')

class NoticiaDeleteView(PermissionRequiredMixin, DeleteView):
    '''
    Excluir Notícia
    '''
    permission_required = "app_j24.delete_noticia"
    model = Noticia
    template_name = 'noticia_confirm_delete.html'  

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        eh_editor = self.request.user.has_perm('app_j24.pode_publicar')
        if self.object.publicada and not eh_editor:
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não possui permissão necessária.')
        if not eh_editor and self.object.autor != self.request.user:
            raise PermissionDenied('Permissão para excluir a notícia negada! Você não é o autor da notícia.')
        return super().form_valid(form)
    
    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Excluiu')
        return reverse('noticias')

class NoticiaBaseDetailView(DetailView):
    '''
    Classe Base dos detalhes de uma notícia
    '''
    model = Noticia
    template_name = 'noticia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids_das_categorias = [categoria.id for categoria in self.object.categorias.all()]
        noticias_relacionadas = Noticia.objects.filter(categorias__in=ids_das_categorias,publicada=True).exclude(id=self.object.id).distinct().order_by('-publicada_em')
        context['object_list'] = noticias_relacionadas
        
        return context

    def acrescentar_visualizacao(self, noticia_id: int = 0) -> None:
        '''
        Estrutura para uma classe filha implementar.
        '''
        pass

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        eh_editor: bool = self.request.user.has_perm('app_j24.pode_publicar')
        eh_autor: bool = self.request.user.has_perm('app_j24.add_noticia')
        eh_autor_da_noticia: bool = eh_autor and self.object.autor == request.user
        pode_ver_noticia_nao_publicada: bool = eh_editor or eh_autor_da_noticia
        if not self.object.publicada and not pode_ver_noticia_nao_publicada:
            raise PermissionDenied('Permissão para ver a notícia negada! Está notícia não foi publicada.')
        
        identificador = kwargs.get('pk', 0)
        self.acrescentar_visualizacao(identificador)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class NoticiaDetailView(NoticiaBaseDetailView):
    '''
    Detalhe da notícia no Jornal 24Horas
    '''

    def acrescentar_visualizacao(self, noticia_id: int = 0):
        '''
        Uma notícia visualizada no Jornal 24Horas deve ser acrescentado
        o seu número de visualizações.
        '''
        if self.object.publicada and not noticia_id:
            self.object.num_visualizacoes += 1
            self.object.save()    

class NoticiaAdmDetailView(PermissionRequiredMixin, NoticiaBaseDetailView):
    '''
    Detalhe da Notícia na Área Administrativa.
    '''
    permission_required = "app_j24.view_noticia"

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
    paginate_by = 3
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
            log_user_action(request=request, obj=noticia, action='Publicou')
        else:
            noticia.publicada = False
            noticia.publicada_em = None
            log_user_action(request=request, obj=noticia, action='Retirou a publicação')
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
        log_user_action(
            request=self.request,
            obj=self.object,
            action='alterou perfil',
            object_name='Usuário'
        )
        return reverse('home')

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password_edit.html'
    def get_success_url(self):
        log_user_action(
            request=self.request,
            obj=self.request.user,
            action='trocou a senha',
            object_name='Usuário'
        )
        return reverse('home')

class CategoriasView(PermissionRequiredMixin, ListView):
    '''
    Visualiza a área administrativa de categorias
    '''
    model = Categoria
    permission_required = "app_j24.view_categoria"
    context_object_name = 'categorias'
    template_name = 'categorias_table.html'
      
    def get_success_url(self):
        return reverse('categorias')
    
class CadastrarCategoriaView(PermissionRequiredMixin, CreateView):
    '''
    Visualiza o cadastro de categoria na área administrativa de categorias
    '''
    model = Categoria
    form_class = CategoriaForm
    permission_required = "app_j24.add_categoria"
    template_name = 'categoria_cadastro.html'

    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Incluiu')
        return reverse('categorias')
    
class EditarCategoriaView(PermissionRequiredMixin, UpdateView):
    '''
    Visualiza a edição de categoria na área administrativa de categorias
    '''
    model = Categoria
    form_class = CategoriaForm
    permission_required = "app_j24.change_categoria"
    template_name = 'categoria_cadastro.html'   
    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Alterou')
        return reverse('categorias')
    
class ExcluirCategoriaView(PermissionRequiredMixin, DeleteView):
    '''
    Visualiza a decisão de deletar uma categoria na área administrativa de categorias
    '''
    model = Categoria
    permission_required = "app_j24.delete_categoria"
    template_name = 'categoria_confirm_delete.html'
    context_object_name = 'categoria'

    def get_success_url(self):
        log_user_action(request=self.request, obj=self.object, action='Excluiu')
        return reverse('categorias')

class UserActionView(PermissionRequiredMixin, ListView):
    '''
    Visualiza a área auditoria
    '''
    model = UserAction
    permission_required = "app_j24.view_useraction"
    context_object_name = 'actions'
    template_name = 'useractions_table.html'
    paginate_by = 20

    def get_queryset(self):
        return UserAction.objects.all().order_by('-timestamp')
 
    def get_success_url(self):
        return reverse('logs')
  

   