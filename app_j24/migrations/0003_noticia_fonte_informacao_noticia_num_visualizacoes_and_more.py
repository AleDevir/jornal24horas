# Generated by Django 5.1.1 on 2024-11-04 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_j24', '0002_categoria_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='fonte_informacao',
            field=models.CharField(max_length=400, null=True, verbose_name='Fonte'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='num_visualizacoes',
            field=models.IntegerField(default=0, editable=False, verbose_name='Número de visualizações'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(max_length=30, unique=True, verbose_name='Categoria'),
        ),
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(editable=False, help_text='Ação realizada no objeto.', max_length=255)),
                ('object_id', models.IntegerField(editable=False, help_text='ID do objeto manipulado', verbose_name='Identificador')),
                ('object_name', models.CharField(editable=False, help_text='Nome do Modelo do objeto manipulado', max_length=20, verbose_name='Modelo')),
                ('object_text', models.CharField(editable=False, help_text='Texto (__str__) do objeto manipulado', max_length=100, verbose_name='Texto')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Data da ação')),
                ('user', models.ForeignKey(editable=False, help_text='Usuário que realizou a ação', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
