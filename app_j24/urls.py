'''
URLs Aplicação
'''
from django.urls import path
from . import views
from .views import NoticiaCreate, HomeListView, NoticiaDetailView

APP_NAME = "app_j24"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    path('noticias/minhas/', views.exibir_noticias, name='exibir_noticias'),
    path('noticias/cadastro/', NoticiaCreate.as_view(), name='cadastro-noticias'),
    path('noticias/editar/<int:noticia_id>', views.edit_noticia, name='edit_noticia'),
    path("noticias/salvar/<int:noticia_id>", views.noticia_edit_save, name='noticia_edit_save'),
]
