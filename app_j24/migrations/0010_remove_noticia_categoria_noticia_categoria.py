# Generated by Django 5.1.1 on 2024-10-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_j24', '0009_alter_noticia_autor_alter_noticia_publicada_em'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='categoria',
        ),
        migrations.AddField(
            model_name='noticia',
            name='categoria',
            field=models.ManyToManyField(to='app_j24.categoria'),
        ),
    ]
