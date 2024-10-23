'''
MODELS app_j24
'''
from datetime import datetime
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone
from .util.tempo_util import calcular_tempo_decorrido

class MyUser(AbstractUser):
    '''
    Usuário
    '''
    pass

    class Meta:
        '''
        Metamodelo
        '''
        db_table='auth_user'



class Categoria(models.Model):
    '''
    Categoria
    '''
    nome = models.CharField('Categoria', max_length=30)
    imagem = models.ImageField(upload_to='', blank=True)

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
    titulo = models.CharField('Título', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, editable=False, unique=True)
    subtitulo = models.CharField('Subtítulo', max_length=300)
    criada_em = models.DateTimeField('criado', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    atualizada_em = models.DateTimeField('atualizada', help_text='dd/mm/yyyy hh:MM', auto_now_add=True)
    publicada_em = models.DateTimeField('Publicada em', help_text='dd/mm/yyyy hh:MM', null=True, editable=False)
    conteudo= models.TextField('Conteúdo', max_length=3000, default='')
    imagem = models.ImageField(upload_to='', blank=True)
    autor = models.ForeignKey(MyUser, on_delete=models.RESTRICT, editable=False)
    categorias = models.ManyToManyField(Categoria)
    publicada = models.BooleanField('publicada', default=False )

    def _calcular_tempo_da_atualizacao(self) -> str:
        '''
        Calculo do tempo de atualização da notícia:
        '''
        return calcular_tempo_decorrido(self.atualizada_em)

    atualizacao_tempo = property(_calcular_tempo_da_atualizacao)

    def _calcular_tempo_da_publicacao(self) -> str:
        '''
        Calculo do tempo de publicação da notícia:
        '''
        return calcular_tempo_decorrido(self.publicada_em)

    publicacao_tempo = property(_calcular_tempo_da_publicacao)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        if self.publicada and not self.publicada_em:
            self.publicada_em = datetime.now()
        elif not self.publicada and self.publicada_em:
            self.publicada_em = None
        return super().save(*args, **kwargs)

    class Meta:
        '''
        Metamodelo
        '''
        db_table = 'noticias'
        permissions = [
            ("pode_publicar", "Permissão atribuida à Editores para a publicação da Notícia"),
        ]

    def __str__(self):
        '''
        str
        '''
        if self.publicada:
            return  f"Título: {str(self.titulo)} - PUBLICADA"
        return f"Título: {str(self.titulo)}"
