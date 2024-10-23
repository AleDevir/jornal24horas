'''
URLs Aplicação
'''
from django.urls import path
from . import views
from .views import (
    ChangePasswordView,
    HomeListView,
    NoticiasListView,
    NoticiaCreateView,
    NoticiaDeleteView,
    NoticiaUpdateView,
    NoticiaDetailView,
    SignUpView,
    UserUpdateView,
)

APP_NAME = "app_j24"


urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-ver"),
    path("noticias/", NoticiasListView.as_view(), name="noticias"),
    path('noticias/editor/publicar/<int:noticia_id>/<int:publicado>', views.publicar_noticia, name='publicar_noticia'),
    path('noticias/cadastro/', NoticiaCreateView.as_view(), name='cadastro-noticias'),
    path('noticias/cadastro/<int:pk>', NoticiaUpdateView.as_view(), name='atualizar-noticia'),
    path('noticias/excluir/<int:pk>', NoticiaDeleteView.as_view(), name='excluir-noticia'),
    path("register/", SignUpView.as_view(), name='registrar-usuario'),
    path('register/edit/user/<int:pk>', UserUpdateView.as_view(), name='atualizar-usuario'),
    path('register/edit/password/<int:pk>', ChangePasswordView.as_view(), name='atualizar-senha'),
    path("<slug:slug>/", NoticiaDetailView.as_view(), name="noticia-detail"),
]
