'''
URLs Aplicação
'''
from django.urls import path
from . import views
from .views import (
    HomeListView,
    NoticiasListView,
    NoticiaCreate,
    NoticiaDelete,
    NoticiaUpdate,
    NoticiaDetailView,
)

APP_NAME = "app_j24"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path("noticias/", NoticiasListView.as_view(), name="noticias"),
    # path('noticias/minhas/', views.noticias_autor, name='noticias_autor'),
    # path('noticias/editor/', views.editor_noticias, name='editor_noticias'),
    path('noticias/editor/publicar/<int:noticia_id>/<int:publicado>', views.publicar_noticia, name='publicar_noticia'),
    path('noticias/cadastro/', NoticiaCreate.as_view(), name='cadastro-noticias'),
    path('noticias/cadastro/<int:pk>', NoticiaUpdate.as_view(), name='atualizar-noticia'),
    path('noticias/excluir/<int:pk>', NoticiaDelete.as_view(), name='excluir-noticia'),
    # path('noticias/editar/<int:noticia_id>', views.edit_noticia, name='edit_noticia'),
    # path("noticias/salvar/<int:noticia_id>", views.noticia_edit_save, name='noticia_edit_save'),
    # path("noticias/excluir/<int:noticia_id>", views.noticia_delete, name='noticia_delete'),
    # path("noticias/filtradas", views.pesquisar_noticias, name='pesquisar_noticias'),
]
