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
    list_display = ['titulo', 'subtitulo', 'criado_em', 'conteudo', 'imagem', 'autor', 'categoria']
    #  list_filter = ['']
    search_fields = ['titulo']


admin.site.register(Noticia, NoticiaAdmin)

admin.site.register([
    Categoria,
])
