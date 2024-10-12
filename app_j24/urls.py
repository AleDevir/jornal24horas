'''
URLs Aplicação
'''

from django.urls import path
from .views import NoticiaCreate, HomeListView, NoticiaDetailView

APP_NAME = "app_j24"

urlpatterns = [
    path("", HomeListView.as_view(), name='home'),
    path("<int:pk>/", NoticiaDetailView.as_view(), name="noticia-detail"),
    # path('noticias/minhas/', xxxx, name='minhas-noticias'),
    path('noticias/cadastro/', NoticiaCreate.as_view(), name='cadastro-noticias'),
]
