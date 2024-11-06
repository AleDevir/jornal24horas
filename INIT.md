

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

## 094. Configurando o Banco de Dados:
```
python manage.py migrate
```

## 04.1. Criar o model e executar a migração: https://docs.djangoproject.com/pt-br/5.1/intro/tutorial02/
```
python manage.py makemigrations <nome-aplicacao>
```

## 04.2. comando mostrar o status das migrações.
```
python manage.py showmigrations
```

## 04.3. Aplicando as alterações (modelos) ao Banco de Dados:
```
python manage.py migrate
```

## 04.4. checa problemas no seu projeto sem criar migrations ou tocar seu banco de dados.
```
python manage.py check
```

## 5. Area administrativa: criando um usuário administrativo
```
python manage.py createsuperuser
```

### registrar as alterações em migrations
```
python manage.py makemigrations <nome_aplicação>

python manage.py makemigrations app_j24

```

### Aplicar as alterações de migrations no db
```
python manage.py migrate
```