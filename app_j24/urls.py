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
    SignUpView,
)

APP_NAME = "app_j24"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path("noticias/", NoticiasListView.as_view(), name="noticias"),
    path('noticias/editor/publicar/<int:noticia_id>/<int:publicado>', views.publicar_noticia, name='publicar_noticia'),
    path('noticias/cadastro/', NoticiaCreate.as_view(), name='cadastro-noticias'),
    path('noticias/cadastro/<int:pk>', NoticiaUpdate.as_view(), name='atualizar-noticia'),
    path('noticias/excluir/<int:pk>', NoticiaDelete.as_view(), name='excluir-noticia'),
    path("register/", SignUpView.as_view(), name='registrar-usuario'),

]
