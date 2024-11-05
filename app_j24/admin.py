'''
ADMIN: Registrar modelos da aplicação na área administrativa.
'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    MyUser,
    Categoria,
    Noticia,
    UserAction,
    Comentario
)

class NoticiaAdmin(admin.ModelAdmin):
    '''
    NoticiaAdmin
    '''
    list_display = [
        'titulo',
        'slug',
        'subtitulo',
        'criada_em',
        'atualizada_em',
        'publicada',
        'publicada_em',
        'imagem',
        'autor',
        
    ]
    list_filter = ['publicada', 'categorias']
    search_fields = ['titulo', 'categorias']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

class UserActionAdmin(admin.ModelAdmin):
    '''
    UserActionAdmin
    '''
    list_filter = ['user', 'object_name']
    search_fields = ['user__username']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

class CategoriaAdmin(admin.ModelAdmin):
    '''
    CategoriaAdmin
    '''
    list_display = [
        'nome',
        'imagem',
    ]

    search_fields = ['nome']

class ComentarioAdmin(admin.ModelAdmin):
    '''
    ComentarioAdmin
    '''
    list_display = [
        'usuario',
        'criado_em',
        'noticia',
        'conteudo',
        
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(MyUser, UserAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(UserAction, UserActionAdmin)
admin.site.register(Comentario, ComentarioAdmin)