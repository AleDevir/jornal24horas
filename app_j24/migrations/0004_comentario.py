# Generated by Django 5.1.1 on 2024-11-05 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_j24', '0003_noticia_fonte_informacao_noticia_num_visualizacoes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField(default='', max_length=3000, verbose_name='Conteúdo')),
                ('criado_em', models.DateTimeField(auto_now_add=True, help_text='dd/mm/yyyy hh:MM', verbose_name='Criado')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app_j24.noticia')),
                ('usuario', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comentarios',
            },
        ),
    ]
