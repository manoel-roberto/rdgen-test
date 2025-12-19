# wsgi.py - Configuração WSGI para o projeto Django RDGen
# Este arquivo configura a aplicação para deployment com servidores WSGI (Web Server Gateway Interface)
# WSGI é o padrão Python para comunicação entre servidores web e aplicações web
# Permite que servidores como Apache, Nginx + Gunicorn, uWSGI sirvam aplicações Django
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/howto/deployment/wsgi/

"""
Configuração WSGI para o projeto rdgen.

Expõe o callable WSGI como uma variável de módulo chamada ``application``.

Para mais informações sobre este arquivo, consulte
https://docs.djangoproject.com/pt-br/5.0/howto/deployment/wsgi/
"""

# Importação do módulo 'os' para manipulação de variáveis de ambiente
# Necessário para configurar o módulo de settings do Django antes de criar a aplicação
import os

# Importação da função get_wsgi_application do Django
# Esta função cria e retorna a aplicação WSGI configurada com as settings do projeto
# Equivalente ao get_asgi_application() mas para WSGI (síncrono)
from django.core.wsgi import get_wsgi_application

# Configuração do módulo de settings do Django
# Define qual arquivo settings.py usar (padrão: 'rdgen.settings')
# IMPORTANTE: Deve ser definido ANTES de chamar get_wsgi_application()
# Equivalente ao DJANGO_SETTINGS_MODULE em variáveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rdgen.settings')

# Criação da aplicação WSGI
# Esta é a variável que o servidor WSGI (Gunicorn, uWSGI, etc.) irá usar
# Exemplo de uso com Gunicorn: gunicorn rdgen.wsgi:application
# Exemplo de uso com uWSGI: uwsgi --http :8000 --wsgi-file rdgen/wsgi.py --callable application
# Exemplo com Apache: WSGIScriptAlias / /caminho/para/rdgen/wsgi.py
application = get_wsgi_application()
