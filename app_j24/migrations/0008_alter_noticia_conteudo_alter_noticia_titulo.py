# Generated by Django 5.1.1 on 2024-10-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_j24', '0007_rename_criado_em_noticia_criada_em_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='conteudo',
            field=models.TextField(default='', max_length=3000, verbose_name='Conteúdo'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='Título'),
        ),
    ]
