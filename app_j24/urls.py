'''
URLs Aplicação
'''
from django.urls import path
from . import views
from .views import (
    CategoriasView,
    CadastrarCategoriaView,
    EditarCategoriaView,
    ExcluirCategoriaView,
    ChangePasswordView,
    HomeListView,
    NoticiasListView,
    NoticiaCreateView,
    NoticiaDeleteView,
    NoticiaUpdateView,
    NoticiaDetailView,
    NoticiaAdmDetailView,
    SignUpView,
    UserUpdateView,
    UserActionView,
)

APP_NAME = "app_j24"


urlpatterns = [
    # Área Pública da Notícia
    path('', views.root, name='root'),
    path("j24/", HomeListView.as_view(), name='home'),
    path("j24/<slug:slug>/", NoticiaDetailView.as_view(), name="noticia-ver"),

    # Área Pública do usuário
    path("register/", SignUpView.as_view(), name='registrar-usuario'),
    path('register/edit/user/<int:pk>', UserUpdateView.as_view(), name='atualizar-usuario'),
    path('register/edit/password/<int:pk>', ChangePasswordView.as_view(), name='atualizar-senha'),
    path('comentario/noticia/', views.add_comentario, name='adicionar-comentario'),


    # Área de Editores e Autores
    path("adm/noticias/", NoticiasListView.as_view(), name="noticias"),
    path('adm/noticias/<int:pk>/', NoticiaAdmDetailView.as_view(), name="noticia-adm-detail"),
    path('adm/noticias/cadastro/', NoticiaCreateView.as_view(), name='cadastro-noticias'),
    path('adm/noticias/<int:pk>/cadastro/', NoticiaUpdateView.as_view(), name='atualizar-noticia'),
    path('adm/noticias/<int:pk>/exclusao/', NoticiaDeleteView.as_view(), name='excluir-noticia'),
    path('adm/logs/', UserActionView.as_view(), name='logs'),

    # Área de Editores
    path('adm/noticias/<int:noticia_id>/publicado/<int:publicado>', views.publicar_noticia, name='publicar_noticia'),
    path('adm/categorias/', CategoriasView.as_view(), name='categorias'),
    path('adm/categorias/cadastro/', CadastrarCategoriaView.as_view(), name='cadastrar_categoria'),
    path('adm/categorias/<int:pk>/cadastro/', EditarCategoriaView.as_view(), name='editar_categoria'),
    path('adm/categorias/<int:pk>/remove/', ExcluirCategoriaView.as_view(), name='excluir_categoria'),

]
