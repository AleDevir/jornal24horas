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
    criado_em = models.DateField('criado', help_text='yyyy/mm/dd', auto_now_add=True)
    conteudo= models.TextField(default='', verbose_name='Conteudo')
    imagem = models.ImageField(upload_to='', blank=True)
    autor = models.ForeignKey(User, on_delete=models.RESTRICT)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)

    class Meta:
        '''
        Metamodelo
        '''
        db_table = 'noticias'
        permissions = [
            ("pode_publicar", "Permissão atribuida à Editores para a publicação da Notícia"),
            ("autor_noticia", "Permissão atribuida aos Autores das Notícias."),
        ]

    def __str__(self):
        '''
        str
        '''
        return f"Publicada em: {self.criado_em}  Titulo: {' '} {str(self.titulo)} Subitulo: {' '} {str(self.titulo)} {str(self.subtitulo)} Categoria: {' '} {str(self.categoria).capitalize()} Autor: {' '} {str(self.autor).capitalize()}"
