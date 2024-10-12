

## 01. Criar o projeto:
```
django-admin startproject <nome_do_projet> .

```

## 02. Criar uma aplicação:
```
python manage.py startapp <nome_da_aplicação>
```

## 03. Rodar o projeto / aplicação para testar o funcionamento:
```
python manage.py runserver

```

## 04. Criar uma rota e página para o caminho root (http://127.0.0.1:8000/)
```
# 04.1 Criar página de base em views.py em <nome_da_aplicação>
# 04.2 Criar a rota em urls.py na pasta 'projeto'
```

## 07. Incluir o nome da aplicação em INSTALLED_APPS de 'settings.py':
```
INSTALLED_APPS = [
    'app_noticias.apps.AppBibliotecaConfig',
    ...
    ...
]
```

## 08. Configuração Brasil:
```
# Em settings.py:

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
```


## 09. Configurando o Banco de Dados:
```
python manage.py migrate
```


## 09.1. Criar o model e executar a migração: https://docs.djangoproject.com/pt-br/5.1/intro/tutorial02/
```
python manage.py makemigrations <nome-aplicacao>
```

## 09.2. comando mostrar o status das migrações.
```
python manage.py showmigrations
```
## 09.3. comando sqlmigrate recebe o nome da migração e o seu SQL.
```
python manage.py sqlmigrate <nome-aplicacao> 0001
```

## 09.4. Aplicando as alterações (modelos) ao Banco de Dados:
```
python manage.py migrate
```

## 09.5. checa problemas no seu projeto sem criar migrations ou tocar seu banco de dados.
```
python manage.py check
```

## 10. Area administrativa: criando um usuário administrativo
```
python manage.py createsuperuser
```

## 10.1 Torne a aplicação de app_noticias editável no site de administração
```
# No módulo admin.py de 'app_noticiasa' registrar os modelos
Exemplo:

from .models import Autor

admin.site.register(Autor)
```

### registrar as alterações em migrations
```
python manage.py makemigrations <nome_aplicação>
```

### Aplicar as alterações de migrations no db
```
python manage.py migrate
```