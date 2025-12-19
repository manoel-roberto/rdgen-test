# asgi.py - Configuração ASGI para o projeto Django RDGen
# Este arquivo configura a aplicação para deployment com servidores ASGI (Asynchronous Server Gateway Interface)
# ASGI permite comunicação assíncrona full-duplex, suportando WebSockets, HTTP/2 e long polling
# Diferente do WSGI (síncrono), ASGI é ideal para aplicações em tempo real
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/howto/deployment/asgi/

"""
Configuração ASGI para o projeto rdgen.

Expõe o callable ASGI como uma variável de módulo chamada ``application``.

Para mais informações sobre este arquivo, consulte
https://docs.djangoproject.com/pt-br/5.0/howto/deployment/asgi/
"""

# Importação do módulo 'os' para manipulação de variáveis de ambiente
# Necessário para configurar o módulo de settings do Django
import os

# Importação da função get_asgi_application do Django
# Esta função cria e retorna a aplicação ASGI configurada com as settings do projeto
from django.core.asgi import get_asgi_application

# Configuração do módulo de settings do Django
# Define qual arquivo settings.py usar (padrão: 'rdgen.settings')
# Equivalente ao DJANGO_SETTINGS_MODULE no WSGI
# IMPORTANTE: Deve corresponder ao nome do seu projeto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rdgen.settings')

# Criação da aplicação ASGI
# Esta é a variável que o servidor ASGI (como Daphne, Uvicorn, Hypercorn) irá usar
# Exemplo de uso com Uvicorn: uvicorn rdgen.asgi:application
# Exemplo de uso com Daphne: daphne rdgen.asgi:application
application = get_asgi_application()
