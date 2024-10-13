'''
MODELS app_j24
'''

from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    '''
    Categoria
    '''
    nome = models.CharField('Categoria', max_length=30)
    criado_em = models.DateField(auto_now_add=True)
    def __str__(self):
        '''
        str
        '''
        return str(self.nome)

class Noticia(models.Model):
    '''
    Noticia
    '''
    titulo = models.CharField('Título', max_length=300)
    subtitulo = models.CharField('Subtítulo', max_length=300)
    criada_em = models.DateTimeField('criado', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    atualizada_em = models.DateTimeField('atualizada', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    publicada_em = models.DateTimeField('publicada', help_text='dd/mm/yyyy hh:MM', null=True)
    conteudo= models.TextField(default='', verbose_name='Conteudo')
    imagem = models.ImageField(upload_to='', blank=True)
    autor = models.ForeignKey(User, on_delete=models.RESTRICT)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    publicada = models.BooleanField('publicada', default=False )

    class Meta:
        '''
        Metamodelo
        '''
        db_table = 'noticias'
        permissions = [
            ("pode_publicar", "Permissão atribuida à Editores para a publicação da Notícia"),
            ("noticia_criar", "Permissão para criar Notícias."),
            ("noticia_alterar", "Permissão para alterar Notícias."),
            ("noticia_excluir", "Permissão para excluir Notícias."),
        ]

    def __str__(self):
        '''
        str
        '''
        return f"Publicada em: {self.atualizada_em}  Titulo: {' '} {str(self.titulo)} Subitulo: {' '} {str(self.titulo)} {str(self.subtitulo)} Categoria: {' '} {str(self.categoria).capitalize()} Autor: {' '} {str(self.autor).capitalize()}"
