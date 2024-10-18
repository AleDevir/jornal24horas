'''
ADMIN: Registrar modelos da aplicação na área administrativa.
'''

from django.contrib import admin
from .models import (

    Categoria,
    Noticia
)

class NoticiaAdmin(admin.ModelAdmin):
    '''
    NoticiaAdmin
    '''
    list_display = [
        'titulo',
        'subtitulo',
        'criada_em',
        'atualizada_em',
        'publicada',
        'publicada_em',
        'imagem',
        'autor',
        
    ]
    list_filter = ['publicada']
    search_fields = ['titulo']

def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Noticia, NoticiaAdmin)

admin.site.register([
    Categoria,
])
